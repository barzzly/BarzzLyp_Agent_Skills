# Large Archive Cloud Streaming & Offsite Backups

- Constrained VPS disk vs massive server archives (50GB-100GB+): never download large `.zip` or `.tar.gz` files to local VPS disk if available storage is smaller than the archive. Stream directly using `rclone copyurl "<signed_wings_url>" "<remote>:<path>"`. This routes data entirely through memory/socket buffers with 0 bytes written to VPS local disk.
- Pterodactyl download signed URL (`GET /api/client/servers/{server_id}/files/download?file={path}`):
  - Always send custom `User-Agent: Mozilla/5.0` with panel API requests; panel WAF/Cloudflare rejects default python urllib user-agents with HTTP 403 Forbidden.
  - Wings HTTP download endpoint rejects `HEAD` requests with HTTP 401 Unauthorized; verify or initiate connections strictly with `GET`.
  - The JWT token payload has an expiration timestamp (`exp`, typically 15 minutes / 900s). Wings validates expiration only upon TCP/HTTP connection establishment. Once the response stream starts, the connection transfers the full file without cutoff regardless of elapsed time.
- Direct streaming performance tuning for large objects:
  - For Google Drive or object storage, pass `--drive-chunk-size 128M --buffer-size 64M --stats 15s --stats-one-line -v` to prevent upload throttling and avoid high API request counts.
  - Run long transfers in the background via detached processes logging to a designated log file so connection drops or session interruptions do not abort the transfer.
- Headless cloud remote authentication via Rclone:
  - When configuring OAuth remotes (Google Drive) on a headless VPS without a GUI browser, do not force users into complex Google Cloud Console project setups if not required.
  - Execute `rclone authorize "<remote_type>" --auth-no-open-browser` in the background; it spins up a local listener on `http://127.0.0.1:53682`.
  - Extract the Google OAuth URL from the HTTP 307 redirect (`curl -s -i "http://127.0.0.1:53682/auth?state=..."`).
  - Provide the redirect URL to the user to open in any browser. After authorization, the browser redirects to `http://127.0.0.1:53682/?state=...&code=...`. Even though the browser reports "connection failed", the user copies the address bar URL back.
  - Fetch `http://127.0.0.1:53682/?state=...&code=...` on the VPS via curl to complete the PKCE exchange. Rclone prints the token payload; write it to `~/.config/rclone/rclone.conf` with permissions 0600.
