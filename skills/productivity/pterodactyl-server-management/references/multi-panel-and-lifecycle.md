# Multi-Panel Operations & Egg Lifecycle

## 1. Multi-Panel Environment (`~/.config/pterodactyl.env`)
Manage across the 2 distinct active panels:
- **UltraServers Panel**: `https://panel.ultraservers.com` (`PTERODACTYL_PANEL_URL`, `PTERODACTYL_API_KEY`).
  - *Cloudflare Bypass:* Always use HTTP/2 (`curl -s --http2`) with user-agent headers. Datacenter VPS IPs will trigger Cloudflare Turnstile blocks or stalls on standard HTTP/1.1 requests.
- **BarzzLy Console**: `https://console.barzzly.com` (`PTERODACTYL_CONSOLE_URL`, `PTERODACTYL_CONSOLE_API_KEY`, SSH key `~/.ssh/id_pterodactyl_barzzly`).

## 2. Egg "Starting" (Yellow Status) Resolution
When a server/bot stays in yellow ("Starting") status indefinitely even though its logs indicate full readiness:
- The egg's `config_startup` regex/string list is missing the completion string emitted by the application.
- Update `config_startup` on the egg (via Panel database `eggs.config_startup` or Admin API):
  ```json
  {
    "done": ["Bot aktif sebagai", "Donation Logger HTTP server running"]
  }
  ```
- Restart Wings (`sudo systemctl restart wings`) to pick up the egg configuration.

## 3. Wings Daemon Isolation
- Restarting the Wings daemon (`sudo systemctl restart wings`) does **not** stop, terminate, or restart running game/bot Docker containers.
- Docker daemon maintains container processes via live-restore while Wings reconnects to Pterodactyl Panel.

## 4. Custom Favicon / Branding Replacement
- Pterodactyl v1.15.2 references favicons under `/var/www/pterodactyl/public/favicons/` and `/public/favicon.ico`.
- When replacing panel favicon:
  - Generate PNG assets (16x16, 32x32, 96x96, 180x180, 192x192, 512x512) and multi-resolution `favicon.ico`.
  - Copy into `/var/www/pterodactyl/public/favicons/` and `/var/www/pterodactyl/public/favicon.ico`.
  - Ensure ownership `chown -R www-data:www-data`.
  - Clear Laravel view/config cache: `php artisan view:clear && php artisan config:clear`.
