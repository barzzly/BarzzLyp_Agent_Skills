# Pterodactyl Backup & Client API WAF Handling

## Client API Request Headers (WAF Bypass)
- UltraServers and Cloudflare edge proxies block default programmatic HTTP user agents (such as Python `urllib` or basic curl without headers) with `HTTP 403 Forbidden`.
- In every programmatic request to `${PTERODACTYL_PANEL_URL}/api/client/...`, always supply:
  - `Authorization: Bearer <API_KEY>`
  - `Accept: application/json`
  - `User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)`

## Full Server Backup & Storage Safety
- **Size Risk**: Minecraft production servers (e.g., Survival, EcoRPG, Lobby) often produce backup archives ranging from 60 GB to 190 GB+.
- **Disk Space Check**: Never download full archives directly to the local VPS without inspecting free storage (`df -h`). VPS disk space is often far smaller than the uncompressed or archived server.
- **Workflow for Remote Backup (e.g. to Google Drive / S3 / Object Storage)**:
  1. Trigger backup creation via API:
     `POST /api/client/servers/{server_id}/backups`
  2. Poll backup status until `is_successful: true` (or listen to completion event):
     `GET /api/client/servers/{server_id}/backups`
  3. Fetch signed direct download URL:
     `GET /api/client/servers/{server_id}/backups/{backup_id}/download`
  4. Stream directly to remote storage without staging on VPS disk:
     - Using rclone: `rclone copyurl "<signed_download_url>" <remote>:<folder>/<filename>.tar.gz`
     - Or pipe directly into remote storage CLI stream.
