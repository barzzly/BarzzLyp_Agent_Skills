# Pterodactyl API File Upload & Remote Backups

## Cloudflare / WAF User-Agent Requirement
- When querying Pterodactyl Client API (`/api/client/...`) on WAF-protected panels (e.g., UltraServers), always specify a standard browser `User-Agent` header (e.g., `User-Agent: Mozilla/5.0`). Omitting it or using default Python `urllib` causes `HTTP Error 403: Forbidden`.

## Direct Config Writing & Console Commands via Client API
- **Write text/config directly**:
  `POST /api/client/servers/{server_id}/files/write?file={url_encoded_path}`
  Headers: `Content-Type: text/plain`, standard browser `User-Agent`.
  Body: Raw UTF-8 string/text. Returns `204 No Content`. Use this instead of multipart file uploads for modifying `.yml`, `.json`, or properties files.
- **Execute console command**:
  `POST /api/client/servers/{server_id}/command`
  Headers: `Content-Type: application/json`, standard browser `User-Agent`.
  Payload: `{"command": "<command_without_slash>"}`. Returns `204 No Content`.
- **LuckPerms MCPets trial permission safety**:
  When granting trial pet access using wildcards (`mcpet.*`, `mcpets.*`, `skin.*`), always explicitly negate `mcpets.admin false` (e.g. `lp user %player% permission settemp mcpets.admin false <duration> server=<server>`), because `mcpets.*` wildcard grants `mcpets.admin` allowing players to execute administrative/reload commands.

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

## Remote Directory Creation & Archive Extraction Caveats
- Do not rely on panel archive extraction: decompression endpoint (`/api/client/servers/{server_id}/files/decompress`) returns `404 Not Found` and unarchive endpoint (`/api/client/servers/{server_id}/files/unarchive`) can return `500 Internal Server Error` on restricted container nodes.
- To deploy multi-directory trees cleanly, create parent folders recursively using `POST /api/client/servers/{server_id}/files/create-folder` with payload `{"root": parent_dir, "name": folder_name}`, then upload files directly to their target directories using the signed Wings upload URL (`multipart/form-data` with `directory` query param).

## Remote Cloud Backups (DriveBackupV2)
- For off-site Google Drive backups, avoid manual GCP project/OAuth setup on headless VPS.
- Deploy `DriveBackupV2.jar` (latest official release from `MaxMaeder/DriveBackupV2`) directly into `/plugins`.
- Link Google Drive via console command:
  `drivebackup linkaccount googledrive`
  This uses DriveBackupV2's hosted authenticator (`auth.drivebackupv2.com`), generating a direct browser authorization link without needing custom Google Cloud API keys.

## Tenant Database Inventory & Storage Profiling
- **Database Inventory & Credentials via Client API**:
  `GET /api/client/servers/{server_id}/databases?include=password`
  Returns full database list, credentials (`attributes.relationships.password.attributes.password`), and host/port mapping for tenant databases.
- **Tenant Permission Boundaries & Shared RAM Architecture**:
  - Shared MySQL hosts restrict tenant users: querying `information_schema.innodb_buffer_page` fails with `ERROR 1227: Access denied; you need the PROCESS privilege`.
  - MySQL memory (InnoDB Buffer Pool) is shared across the entire instance and daemon, not isolated or limited per database schema. When answering questions regarding database RAM usage, explain this shared-buffer architecture and distinguish it from plugin-side JVM memory caching (e.g. leaderboard caches in `ajLeaderboards` or UUID/balance caches in `PlayerPoints`).
- **Disk Storage Profiling per Database**:
  To profile database disk footprint across tables:
  ```sql
  SELECT 
      table_schema AS db_name,
      ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS total_mb,
      ROUND(SUM(data_length) / 1024 / 1024, 2) AS data_mb,
      ROUND(SUM(index_length) / 1024 / 1024, 2) AS index_mb,
      COUNT(table_name) AS table_count,
      SUM(table_rows) AS total_rows
  FROM information_schema.tables 
  WHERE table_schema = DATABASE()
  GROUP BY table_schema;
  ```
  An allocated Pterodactyl database may be 0 MB (0 tables) if the owning plugin fell back to flatfile storage (e.g. BetterTeams using `teams.yml`).

