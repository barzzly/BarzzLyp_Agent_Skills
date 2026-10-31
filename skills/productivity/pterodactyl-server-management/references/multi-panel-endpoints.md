# Multi-Panel Pterodactyl Endpoints & Automated SSH Key Management

Reference for managing operations across multiple distinct Pterodactyl panel environments (e.g., UltraServers and self-hosted BarzzLy Console).

## 1. Environment Routing (`~/.config/pterodactyl.env`)

Always read credentials from `~/.config/pterodactyl.env`. Never hardcode API keys or hostnames.

```env
# UltraServers Panel (Noesantara & LegacySchool Minecraft production clusters)
PTERODACTYL_PANEL_URL=https://panel.ultraservers.com
PTERODACTYL_API_KEY=ptlc_...

# BarzzLy Console Panel (Self-hosted node: Bot WA, RP Rebel, Velocity)
PTERODACTYL_CONSOLE_URL=https://console.barzzly.com
PTERODACTYL_CONSOLE_API_KEY=ptlc_...
PTERODACTYL_CONSOLE_SSH_KEY=/home/barzzly/.ssh/id_pterodactyl_barzzly
```

### Resolution Rules:
- If target server is `NOESANTARA BOT WA` (`400a3758`), `NOESANTARA RP REBEL` (`237a7813`), or `NOESANTARA VELOCITY` (`5067ef6a`), route to `PTERODACTYL_CONSOLE_URL` using `PTERODACTYL_CONSOLE_API_KEY`.
- If target server is `ECORPG`, `JAWACAMP`, or other cluster servers under UltraServers, route to `PTERODACTYL_PANEL_URL` using `PTERODACTYL_API_KEY`.

---

## 2. Automated SSH Key Deployment via Client API

When bootstrapping SFTP access on a Pterodactyl panel, generate a dedicated ed25519 keypair and register it autonomously using the Client API so the user never needs to copy-paste keys through the web UI:

### Step 1: Generate Dedicated Keypair
```bash
ssh-keygen -t ed25519 -C "barzzly-pterodactyl-console" -f ~/.ssh/id_pterodactyl_barzzly -N ""
```

### Step 2: Register Public Key via Client API
Pterodactyl exposes an account SSH key registration endpoint on `POST /api/client/account/ssh-keys`:

```bash
PUB_KEY=$(cat ~/.ssh/id_pterodactyl_barzzly.pub)

curl -s -X POST "${PANEL_URL}/api/client/account/ssh-keys" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d "$(jq -n --arg name "BarzzLy-Agent-VPS" --arg key "$PUB_KEY" '{"name": $name, "public_key": $key}')"
```

### Response Attributes:
Returns `object: "ssh_key"` with fingerprint and timestamp:
```json
{
  "object": "ssh_key",
  "attributes": {
    "name": "BarzzLy-Agent-VPS",
    "fingerprint": "EmLhALm3ieCMdHlqKv7UhirakGVOcNoe3rXC6YkOtDg",
    "public_key": "...",
    "created_at": "2026-10-31T15:32:00+07:00"
  }
}
```

---

## 3. SFTP Ingress via Wings
Once registered, authenticate SFTP connections to Wings (port 2022 by default) using the dedicated key:
```bash
sftp -i ~/.ssh/id_pterodactyl_barzzly -P 2022 <username>.<server_identifier>@<node_sftp_ip>
```
Ensure permissions on the private key remain `chmod 600`.
