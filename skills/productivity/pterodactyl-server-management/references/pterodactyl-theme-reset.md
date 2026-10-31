# Pterodactyl Panel Clean Default Reset & Theme Purge

Procedure to completely remove custom themes, addons, modified controllers, and build artifacts from a Pterodactyl panel installation and restore the 100% official release.

## When to Use
- User requests removing a custom theme (e.g., Blueprint, Recode, Enola, NookTheme, Iceberg, custom fork) to return to official default Pterodactyl.
- Custom Webpack/Vite assets in `public/assets` conflict or produce stale/broken UI.
- Upstream controllers or routes were injected and need to be wiped clean while preserving the database, `.env`, and existing servers.

## Invariant Safety Rules
- **NEVER overwrite or delete `/var/www/pterodactyl/.env`**: Contains `APP_KEY`, DB credentials, and encryption salts.
- **NEVER delete `/var/www/pterodactyl/storage/`**: Contains server SSL certificates, logs, and user avatars.
- **Database remains untouched**: MySQL/MariaDB schema retains servers, nodes, allocations, and users.
- **Take a backup first**: Create an isolated tarball of `/var/www/pterodactyl` (excluding `vendor` and `storage/logs`) before touching any file.

## Step-by-Step Restoration Procedure

### 1. Pre-Flight Backup
```bash
sudo tar --exclude='vendor' --exclude='node_modules' --exclude='.login-build' \
  -czf /root/pterodactyl-backup-before-default.tar.gz -C /var/www pterodactyl
```

### 2. Download Official Release Tarball
Check the latest stable release tag (or match existing major version):
```bash
cd /tmp
curl -sLo panel.tar.gz https://github.com/pterodactyl/panel/releases/latest/download/panel.tar.gz
rm -rf /tmp/official_panel && mkdir -p /tmp/official_panel
tar -xzf panel.tar.gz -C /tmp/official_panel
```

### 3. Enter Maintenance Mode & Purge Custom Additions
Unpacking a tarball only overwrites existing files; it does **not** delete extraneous files injected by custom themes (such as `ServerCard.tsx`, custom banner folders, `api/addons/`, or obsolete hashed JS bundles). You must explicitly purge the custom directories:
```bash
cd /var/www/pterodactyl
php artisan down || true

# Remove custom frontend and backend additions
rm -rf .login-build
rm -rf resources/scripts resources/views
rm -rf public/assets
rm -rf app routes config database bootstrap
```

### 4. Copy Clean Official Files
```bash
cp -r /tmp/official_panel/app .
cp -r /tmp/official_panel/bootstrap .
cp -r /tmp/official_panel/config .
cp -r /tmp/official_panel/database .
cp -r /tmp/official_panel/resources .
cp -r /tmp/official_panel/routes .
cp -r /tmp/official_panel/public/assets public/
cp -r /tmp/official_panel/public/themes public/
cp -r /tmp/official_panel/public/favicons public/
cp -r /tmp/official_panel/public/js public/
cp /tmp/official_panel/public/index.php public/
cp /tmp/official_panel/artisan .
cp /tmp/official_panel/composer.json .
cp /tmp/official_panel/composer.lock .
cp /tmp/official_panel/package.json .
cp /tmp/official_panel/webpack.config.js .
cp /tmp/official_panel/tailwind.config.js .
```

### 5. Fix Storage & Cache Permissions
```bash
chmod -R 755 storage bootstrap/cache
```

### 6. Synchronize Composer Dependencies
Ensure platform dependencies match the official lockfile:
```bash
composer install --no-dev --optimize-autoloader
```

### 7. Clear Caches & Reseed Migrations
```bash
php artisan view:clear
php artisan config:clear
php artisan route:clear
php artisan migrate --seed --force
```

### 8. Fix Web Ownership & Restart Services
```bash
chown -R www-data:www-data /var/www/pterodactyl

# Restart queue worker, PHP-FPM, and web server
systemctl restart pteroq
systemctl restart php*-fpm
systemctl reload nginx

php artisan up
```

### 9. Verification Gates
1. **Panel Version**: Run `php artisan p:info` and verify `Up-to-Date: Yes` with canonical version tag (not `canary` or custom string).
2. **Clean Asset Hash**: Inspect `curl -sL https://<domain>/ | grep bundle` to confirm only the single official release bundle (e.g. `/assets/bundle.<hash>.js`) is loaded, not multiple stacked custom bundles.
3. **HTTP Readiness**: Probe both `https://<domain>/` and `https://<domain>/auth/login` to confirm `HTTP/1.1 200 OK` without Blade/template compilation errors.
4. **Clean Workspace**: Wipe `/tmp/official_panel` and `/tmp/panel.tar.gz`.
