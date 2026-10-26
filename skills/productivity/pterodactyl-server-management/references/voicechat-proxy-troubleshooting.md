# Simple Voice Chat & Proxy Plugin Management

## Zero-Downtime Plugin Staging (No Server Restart)

When the user specifies that servers must NOT be restarted immediately (e.g. "jangan restart server jika butuh restart besok aku restart sendiri"):
1. **Download official release**: Fetch verified release directly from author Modrinth CDN/GitHub; verify SHA1 hash against API.
2. **Stage without disruption**: Upload the new `.jar` to `/plugins/` via Pterodactyl Wings API or SFTP.
3. **Rename previous `.jar`**: Rename the old plugin to `.jar.old` or `.jar.disabled` via Pterodactyl API:
   - Method: `PUT /api/client/servers/{server_id}/files/rename`
   - Headers: `Authorization: Bearer <API_KEY>`, `Content-Type: application/json`
   - Body: `{"root": "/plugins", "files": [{"from": "plugin-old.jar", "to": "plugin-old.jar.old"}]}`
4. **Update config files on disk**: Edit `plugins/<Plugin>/config.yml` or `.properties` so new settings take effect cleanly on the next scheduled restart.
5. **Never trigger restart/kill**: Do not send restart, stop, or kill signals via API when forbidden.

## Simple Voice Chat Behind Velocity Proxy

### Root Cause of Reconnect / Desync Wedges
In `voicechat-velocity` versions prior to 2.6.26 (such as 2.6.13):
- Method `VoiceProxySniffer.handleSecretPacket` failed to call `voiceProxy.disconnectBridge(playerUUID)` when receiving a new `SecretPacket`.
- When a player experiences a connection timeout, the backend server re-authenticates and issues a new secret.
- The client mod opens a new UDP socket and sends `AuthenticatePacket`.
- Because Velocity retained the old bridge in `bridgeMap`, backend response packets (including `AuthenticateAckPacket`) are routed to the player's old closed UDP port.
- The player mod never receives ACK, never transmits `ConnectionCheckPacket`, and remains permanently stuck in an unvalidated/disconnected voice state until they completely relog from the proxy.

### Timeout Tolerance Tuning
- Default `keep_alive=1000` ms in `voicechat-server.properties` enforces a hard disconnect threshold of `keepAlive * 10L` = 10 seconds.
- High-latency or jittery player connections (e.g. mobile networks or ISP routing spikes) easily cross 10 seconds during world transitions or lag spikes, triggering mass timeouts.
- Set `keep_alive=3000` (or `4000`) in `voicechat-server.properties` across backend servers to expand the timeout window to 30–40 seconds.
