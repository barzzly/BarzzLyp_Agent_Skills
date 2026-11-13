# Cross-Panel Server Migrations & Wings API Transfers

When moving server archives or migrating servers between Pterodactyl panels (e.g., Ultraservers to local console):

## 1. Direct Transfer via Wings API (No Local Intermediate Hop)
Avoid routing large archives (multi-hundred MBs or GBs) through the local host disk:
1. **Generate Signed Download URL**:
   `GET /api/client/servers/<source_id>/files/download?file=<archive_name>`
   Extract `attributes.url` from response.
2. **Trigger Remote Pull on Target Panel**:
   `POST /api/client/servers/<target_id>/files/pull`
   Payload:
   ```json
   {
     "url": "<download_url>",
     "directory": ""
   }
   ```
   Wings downloads directly from the source Wings daemon over HTTPS.

## 2. Large Staging Archive Cleanup & Background Process Rules
If direct remote pull cannot be used (e.g. source requires external credentials) and a local staging archive must land on VPS disk:
- **Immediate Cleanup**: Never leave multi-GB staging archives (e.g. `BackupLegacySchool.zip`) on disk after upload or extraction completes. Disk fills rapidly and degrades VPS performance.
- **No Foreground Shell Wrappers**: Never launch cleanup watchdogs using `nohup <cmd> &` or `disown` in foreground terminal calls — Hermes will reject the command with an execution error. Instead, run the task with `terminal(command=..., background=true, notify=true)` or execute cleanup synchronously once upload confirms receipt.
- **Verify Receipt Before Delete**: Confirm the target panel lists the file via `GET /api/client/servers/<target_id>/files/list` before deleting the local staging copy.

## 2. Handling Target Archive Filename & Decompression
- Wings remote pull often writes the incoming stream as `file` (no extension) rather than preserving URL query filenames.
- Check file listing `GET /api/client/servers/<target_id>/files/list`.
- If named `file`, rename before extracting:
  `PUT /api/client/servers/<target_id>/files/rename` with `{"root": "/", "files": [{"from": "file", "to": "<archive_name>.zip"}]}`.
- Trigger decompression:
  `POST /api/client/servers/<target_id>/files/decompress` with `{"root": "/", "file": "<archive_name>.zip"}`.

## 3. Mandatory Post-Transfer Config Alignment (Before First Power On)
Before starting the target server, check its allocation ports via `GET /api/client/servers/<target_id>`:
- **Server Ports (`server.properties`)**:
  Align `server-port` and `query.port` with the primary allocation port.
- **Simple Voice Chat (`plugins/voicechat/voicechat-server.properties`)**:
  - `port`: set to designated secondary allocation port.
  - `voice_host`: set to `<node_public_ip>:<voice_port>` (never leave obsolete host/IP from old panel/VPS).
  - `bind_address`: set to `*`.
- **Velocity Proxy Registration (`velocity.toml`)**:
  If the backend server changed node or port, update `[servers]` mapping and reload/restart Velocity.
