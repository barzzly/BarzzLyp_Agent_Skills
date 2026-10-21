# Pterodactyl API File Upload & Remote Backups

## Cloudflare / WAF User-Agent Requirement
- When querying Pterodactyl Client API (`/api/client/...`) on WAF-protected panels (e.g., UltraServers), always specify a standard browser `User-Agent` header (e.g., `User-Agent: Mozilla/5.0`). Omitting it or using default Python `urllib` causes `HTTP Error 403: Forbidden`.

## Direct File Upload to Wings
To deploy or upload plugins/files without SFTP credentials:
1. Request signed upload URL from panel:
   `GET /api/client/servers/{server_id}/files/upload`
   Extract `data.attributes.url` (e.g., `https://<node>:60001/upload/file?token=...`).
2. Append target directory query parameter:
   `${UPLOAD_URL}&directory=/plugins`
3. POST multipart form payload:
   - Form field name: `files`
   - Content-Type: `multipart/form-data; boundary=...`
   - Payload: binary contents of the file with filename attribute (e.g., `DriveBackupV2.jar`).

## Remote Cloud Backups (DriveBackupV2)
- For off-site Google Drive backups, avoid manual GCP project/OAuth setup on headless VPS.
- Deploy `DriveBackupV2.jar` (latest official release from `MaxMaeder/DriveBackupV2`) directly into `/plugins`.
- Link Google Drive via console command:
  `drivebackup linkaccount googledrive`
  This uses DriveBackupV2's hosted authenticator (`auth.drivebackupv2.com`), generating a direct browser authorization link without needing custom Google Cloud API keys.
