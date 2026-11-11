# Cross-Panel Server Migrations & Wings API Transfers

When moving server archives or migrating servers between Pterodactyl panels (e.g., Ultraservers to local console):

## 1. Direct Transfer via Wings API (No Local Intermediate Hop)
Avoid routing large archives (multi-hundred MBs) through the local host disk:
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
