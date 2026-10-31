# Pterodactyl Backup & Client API WAF Handling

## Client API Request Headers (WAF Bypass)
- UltraServers and Cloudflare edge proxies block default programmatic HTTP user agents (such as Python `urllib` or basic curl without headers) with `HTTP 403 Forbidden`. Certain POST endpoints (e.g. `/files/compress`) trigger Cloudflare Turnstile/Managed Challenges.
- In every programmatic request to `${PTERODACTYL_PANEL_URL}/api/client/...`, always supply:
  - `Authorization: Bearer <API_KEY>`
  - `Accept: application/json`
  - `User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)`

## High-Speed Cross-Panel Migration via SFTP (lftp mirror)
When moving multi-gigabyte servers between Pterodactyl panels where `/files/compress` is blocked by WAF or `/backups/.../download` fails on Kopia backup engines:
1. **Add Local SSH Key to Remote Panel**:
   - `POST /api/client/account/ssh-keys` with `{"name": "...", "public_key": "<key_content>"}`.
2. **Find SFTP Username**:
   - Query `GET /api/client/account` to retrieve panel username (e.g. `h7hvbmjk`).
   - SFTP username is `<account_username>.<server_identifier>` (e.g. `h7hvbmjk.c7c7bf69`).
   - Host & port come from `GET /api/client/servers/{server_id}` under `attributes.sftp_details` (e.g. `nexora.ultraservers.com:${PTERODACTYL_SFTP_PORT}`).
3. **Mirror Directly with lftp**:
   - Use `lftp` with parallel directories and connections:
     ```bash
     lftp -u "<sftp_user>," -p <sftp_port> sftp://<sftp_host> << 'EOF'
     set sftp:connect-program "ssh -a -x -o StrictHostKeyChecking=no -i /path/to/private_key"
     set mirror:parallel-directories yes
     set net:connection-limit 8
     mirror --verbose --parallel=4 --exclude .trash/ --exclude backup_mounts/ / "/var/lib/pterodactyl/volumes/<target_uuid>"
     bye
     EOF
     ```
4. **Fix Target Ownership**:
   - Always run `chown -R 997:988 /var/lib/pterodactyl/volumes/<target_uuid>` after mirroring so Wings and container processes retain read/write access.
5. **Egg Startup String Matching**:
   - Proxies (Velocity/Bungee) will remain stuck on status starting (yellow) if registered under Paper egg because Paper waits for `)! For help, type "help"` whereas Velocity prints `Done (`. Always use dedicated Velocity egg.
6. **Allocation Notes & Port Alignment**:
   - Update allocation notes directly via Tinker or API (`POST /api/client/servers/{server}/network/allocations/{id}`) so ports are visibly documented (e.g. `Primary`, `Voice Chat`, `Skin512 Web API`).
   - For backend Minecraft servers running behind Velocity proxy, ensure `server.properties` (`server-port`, `query.port`, `management-server-port`) match the primary allocation and `velocity.toml` proxy routing.

## Geyser Bedrock Handshake "Terracotta" Error
When Bedrock / MCPE players experience disconnection with the error `Terracotta` (*no network path found*):
- **Root Cause**: `transport: nethernet` relies on WebRTC signaling and STUN. Mobile/cellular networks using symmetric NAT or CGNAT block WebRTC candidate exchange.
- **Fix**: In `plugins/Geyser-Velocity/config.yml` (or standalone Geyser `config.yml`), set:
  ```yaml
  bedrock:
    transport: both
  ```
  This opens dual listening: **RakNet (UDP 19132)** for traditional Bedrock mobile clients, and **NetherNet (UDP 25565)** for modern desktop clients, eliminating handshake failures across different mobile ISPs.


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
