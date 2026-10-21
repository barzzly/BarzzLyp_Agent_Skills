# Pterodactyl Large File Streaming & API Uploads

## User-Agent Header Requirement
- UltraServers and Cloudflare/WAF-protected Pterodactyl panels block automated API requests (returning `403 Forbidden`) if default language/script user agents are detected.
- Always include `'User-Agent': 'Mozilla/5.0'` alongside `'Authorization': 'Bearer ...'` and `'Accept': 'application/json'` on all Client API HTTP requests.

## Streaming Large Server Files Without Local Disk Spills
- Minecraft server backups or archives (`.zip`, `.tar.gz`) frequently exceed 50–150GB. When VPS local disk space is constrained, never download large archives locally before re-uploading.
- Generate a direct signed Wings download URL via Client API:
  `GET /api/client/servers/{server_id}/files/download?file={urlencoded_path}`
- Extract `data.attributes.url` and stream directly to remote storage using `rclone copyurl`:
  ```bash
  rclone copyurl "<signed_wings_url>" "<remote>:<path/to/dest.zip>"
  ```
  `rclone copyurl` copies directly from URL to destination remote without saving to temporary local disk storage.

## Direct Plugin / JAR Uploads via Client API
- Obtain temporary multipart upload endpoint:
  `GET /api/client/servers/{server_id}/files/upload`
- Append directory target query param to the returned URL (e.g., `&directory=/plugins`).
- Send multipart/form-data POST with form field `files` containing the binary JAR payload. Does not require SFTP credentials or stopping the server.

## Headless Google Drive OAuth via Rclone
- On headless servers without a local GUI browser, avoid manual Google Cloud Console project creation when standard rclone auth suffices:
  1. Launch background listener: `rclone authorize "drive" --auth-no-open-browser`
  2. Query listener redirect at `http://127.0.0.1:53682/auth?state=<state>` to extract the pre-built OAuth consent URL.
  3. Send URL to user; user signs in on mobile/desktop browser. The browser redirects to `http://127.0.0.1:53682/?state=...&code=...` (which fails in browser).
  4. User copies redirect URL with authorization code; agent fetches `http://127.0.0.1:53682/?state=...&code=...` locally on VPS to complete token exchange.
