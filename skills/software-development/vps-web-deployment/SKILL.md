---
name: vps-web-deployment
description: Use when deploying web apps to Linux VPS. Deploy fullstack app with Nginx, MariaDB, PM2, and CI/CD.
---

# VPS Web Deployment

Standard procedure for deploying web applications (Node.js/Express, Vite/React, Fullstack) on a Linux VPS behind Nginx reverse proxy, process management (PM2/systemd), database provisioning, and Cloudflare DNS/SSL.

## Standard Deployment Workflow

### 1. Repository & Location
- Place all web projects under the designated web root (e.g. `/home/<user>/Website/<project-name>`). Keep the home directory tidy.
- Clone or pull latest code:
  ```bash
  gh repo clone <repo> || git clone <url>
  ```
- Install dependencies and build production bundle:
  ```bash
  npm ci || npm install
  npm run build
  ```

### 2. Database Provisioning & Auto-Migrations (MariaDB/MySQL)
- Verify service status:
  ```bash
  sudo systemctl status mariadb
  ```
  If missing: `sudo apt update && sudo apt install -y mariadb-server`.
- Create dedicated database and restricted user:
  ```sql
  CREATE DATABASE IF NOT EXISTS <db_name> CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
  CREATE USER IF NOT EXISTS '<db_user>'@'localhost' IDENTIFIED BY '<strong_password>';
  GRANT ALL PRIVILEGES ON <db_name>.* TO '<db_user>'@'localhost';
  FLUSH PRIVILEGES;
  ```
- Import initial schema:
  ```bash
  sudo mariadb <db_name> < migrations/schema.sql
  ```
- Use an idempotent migration runner (`templates/migrate.cjs` -> `script/migrate.cjs`) to track executed files in `_migrations` table so subsequent pushes apply only new `.sql` migrations.
- Local dev connection: Never bind MariaDB to `0.0.0.0` or open port 3306 on UFW for remote development. Tunnel via SSH instead: `ssh -N -L 3307:127.0.0.1:3306 <user>@<vps_ip>`.

### 3. Environment & Security Configuration (`.env`)
- Populate `.env` with required runtime variables (`PORT`, `DB_*`, secrets, URLs).
- Generate secure secrets using `openssl rand -base64 48` or `crypto.randomBytes(48).toString('base64url')`.
- Restrict file permissions:
  ```bash
  chmod 600 .env
  ```

### 4. Process Management (PM2 & Systemd Persistence)
- Install PM2 in user space or global:
  ```bash
  npm install -g pm2
  ```
- Define `ecosystem.config.cjs`:
  ```javascript
  module.exports = {
    apps: [
      {
        name: "<app-name>",
        script: "dist/index.cjs",
        cwd: "<absolute-app-path>",
        env: {
          NODE_ENV: "production",
          PORT: 5000
        }
      }
    ]
  };
  ```
- Start app and persist state:
  ```bash
  pm2 start ecosystem.config.cjs
  pm2 save
  ```
- For reliable boot persistence without interactive prompt issues or script blockers, install a systemd service at `/etc/systemd/system/pm2-<user>.service`:
  ```ini
  [Unit]
  Description=PM2 process manager
  After=network.target

  [Service]
  Type=forking
  User=<user>
  LimitNOFILE=infinity
  LimitNPROC=infinity
  LimitCORE=infinity
  Environment=PATH=<npm-global-bin>:/usr/local/bin:/usr/bin:/bin
  Environment=PM2_HOME=/home/<user>/.pm2
  PIDFile=/home/<user>/.pm2/pm2.pid
  ExecStart=<pm2-path> resurrect
  ExecReload=<pm2-path> reload all
  ExecStop=<pm2-path> kill

  [Install]
  WantedBy=multi-user.target
  ```
  Enable and load:
  ```bash
  sudo systemctl daemon-reload
  sudo systemctl enable pm2-<user>.service
  ```

### 5. Nginx Reverse Proxy Configuration
- Create `/etc/nginx/sites-available/<domain>`:
  ```nginx
  server {
      listen 80;
      server_name <domain>;

      location / {
          proxy_pass http://127.0.0.1:<port>;
          proxy_set_header Host $host;
          proxy_set_header X-Real-IP $remote_addr;
          proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
          proxy_set_header X-Forwarded-Proto https;
          proxy_http_version 1.1;
          proxy_set_header Upgrade $http_upgrade;
          proxy_set_header Connection "upgrade";
          proxy_read_timeout 300s;
      }
  }
  ```
- Enable and reload:
  ```bash
  sudo ln -sf /etc/nginx/sites-available/<domain> /etc/nginx/sites-enabled/
  sudo nginx -t
  sudo systemctl reload nginx
  ```

### 6. Cloudflare DNS & SSL Settings
- DNS record:
  - **Type**: `A`
  - **Name**: `<subdomain>` (or `@` for apex)
  - **IPv4**: `<vps_public_ip>`
  - **Proxy status**: Proxied (Orange Cloud)
- SSL/TLS encryption mode:
  - Set to **Full** (or **Flexible** if VPS listens only on port 80 HTTP).

### 7. Automated CI/CD via GitHub Actions (SSH Deploy on Push)
- Generate or ensure an SSH key pair exists (`~/.ssh/id_ed25519` and `id_ed25519.pub`).
- Append the public key to authorized keys:
  ```bash
  cat ~/.ssh/id_ed25519.pub >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys
  ```
- Store secrets in GitHub repo using `gh secret set`:
  ```bash
  gh secret set VPS_HOST --repo <owner>/<repo> --body "<vps_ip>"
  gh secret set VPS_USERNAME --repo <owner>/<repo> --body "<user>"
  gh secret set VPS_PORT --repo <owner>/<repo> --body "22"
  gh secret set VPS_SSH_KEY --repo <owner>/<repo> < ~/.ssh/id_ed25519
  ```
- Add workflow `.github/workflows/deploy.yml`:
  ```yaml
  name: Auto Deploy to VPS
  on:
    push:
      branches: [ main ]
  jobs:
    deploy:
      runs-on: ubuntu-latest
      steps:
        - name: Remote SSH deploy
          uses: appleboy/ssh-action@master
          with:
            host: ${{ secrets.VPS_HOST }}
            username: ${{ secrets.VPS_USERNAME }}
            key: ${{ secrets.VPS_SSH_KEY }}
            port: ${{ secrets.VPS_PORT || 22 }}
            script: |
              export PATH=$PATH:/home/<user>/.npm-global/bin:/usr/bin
              cd <app-path>
              git pull origin main
              npm ci --include=dev
              npm run db:migrate
              npm run build
              pm2 reload <app-name>
  ```

### 8. Network & Firewall Hardening (UFW)
- Only expose public web and SSH ports:
  ```bash
  sudo ufw default deny incoming
  sudo ufw default allow outgoing
  sudo ufw allow 22/tcp
  sudo ufw allow 80/tcp
  sudo ufw allow 443/tcp
  sudo ufw deny 5000/tcp
  sudo ufw deny 3306/tcp
  sudo ufw reload
  ```
- Verify default Nginx virtual host handles raw IP visits so internal applications only answer when requested by their exact domain name.

## Pitfalls & Core Rules

- **Non-Interactive SSH PATH in GitHub Actions**: Non-interactive SSH sessions spawned by CI runners do not load `.bashrc` or user profile PATH customizations. If `pm2` was installed via `npm install -g` into user space (`~/.npm-global/bin`), the deployment script will crash with `pm2: command not found`. Always export the explicit user npm bin directory in the deploy script (`export PATH=$PATH:/home/<user>/.npm-global/bin:/usr/bin`).
- **Cloudflare HTTPS Protocol Header**: When Nginx receives traffic on port 80 behind Cloudflare SSL, `$scheme` is `http`. If Nginx forwards `$scheme` instead of `https`, frameworks with `trust proxy` enabled will issue cookies without the `Secure` flag or reject HTTPS-only sessions, causing silent authentication redirects and broken login flows. Always force `proxy_set_header X-Forwarded-Proto https;` or use a map on `$http_x_forwarded_proto`.
- **Pre-check Port Conflicts**: Always inspect existing listeners (`ss -tulpn`) before picking an application port to prevent binding collisions with existing containers or Node/Python daemons.
- **Production Build Flags**: On hosts with `NODE_ENV=production`, run `npm ci --include=dev` or `npm install` before running the build step, because build toolchains (Vite, TSX, esbuild) reside in `devDependencies` and are stripped by default in production installs.
- **Claude Code Router Model Override**: Global `ANTHROPIC_DEFAULT_OPUS_MODEL` in settings can silently redirect a custom `--model` flag. Override routing cleanly per-invocation by passing `--settings '{"model":"<requested_id>","env":{"ANTHROPIC_DEFAULT_OPUS_MODEL":"<requested_id>"}}'`.
- **Frontend Dead Code & Component Pruning**: Boilerplate UI templates (like unreferenced shadcn components) bloat bundle chunks and increase compile times. Scripting cross-import reference checks across source files before production deployment cuts bundle size significantly (e.g. dropping CSS from 151KB to 102KB) without regressing active components.
- **Database Security for Remote Dev**: Exposing database ports (3306/5432) to public IP creates constant attack surfaces for credential brute-force. Keep database bound to `127.0.0.1` and firewalled (`ufw deny 3306/tcp`); connect remote development environments exclusively through encrypted SSH port-forwarding tunnels (`ssh -N -L <local_port>:127.0.0.1:<remote_port> <user>@<host>`).
