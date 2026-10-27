# Proxy Tuning & Pterodactyl Memory Limits

Guidelines for JVM memory distribution, off-heap headroom, and runtime lifecycle for Minecraft network proxies (Velocity, BungeeCord, Waterfall) on Pterodactyl.

## 1. Velocity Proxy Out Of Memory (Exit Code 137 / SIGKILL)

### Symptom
Velocity container unexpectedly dies during player peaks or connection bursts without Java stack traces in `latest.log`. Pterodactyl Wings crash logs record:
```
Detected server process in a crashed state!
Exit code: 137
Out of memory: true
```

### Root Cause
Exit code 137 means the Linux kernel OOM Killer issued a `SIGKILL` to the Java container process because total Resident Set Size (RSS) exceeded the container RAM quota + swap limit.

In Pterodactyl's Velocity egg, the default startup command is:
```sh
java -Xms128M -Xmx$(({{SERVER_MEMORY}}*{{RAM_PERCENTAGE}}/100))M ... -jar server.jar
```
When `RAM_PERCENTAGE` is left at the default `90`:
- On a 6144 MB container, `-Xmx` receives `5529 MB` (leaving only `615 MB` for non-heap usage).
- Heavy network plugins consume large amounts of direct/native memory outside the JVM heap:
  1. **Geyser & Floodgate**: Bedrock RakNet/UDP protocol translation, packet queues, and texture decoders.
  2. **Simple Voice Chat**: Real-time UDP audio streams and socket buffers.
  3. **Netty Epoll Transport**: High-throughput Direct ByteBuffers for dozens of active Minecraft connections.
  4. **OpenSSL / libdeflate**: Native compression and cipher libraries.
  5. **Metaspace & Threads**: 15+ plugins and 200+ native OS threads (~1 MB stack each).
- When total off-heap usage exceeds ~600 MB, the process is killed instantly by the host OS kernel.

### Resolution
Lower the `RAM_PERCENTAGE` startup variable to `70` (or `75` max):
- For a 6144 MB container, `70%` allocates `~4300 MB` heap to `-Xmx`.
- Velocity itself needs modest heap (~2 to 3 GB is ample for hundreds of routed players).
- This reserves `~1.8 GB` of container headroom for off-heap Netty direct buffers and Geyser Bedrock translation, preventing kernel OOM kills.

---

## 2. FancyHolograms Runtime Lifecycle & Safe Deletion

### Lifecycle Caveats
- `FancyHolograms` keeps all loaded holograms in an active memory map.
- Periodic autosave (default `interval: 15` min in `config.yml`) and `/fancyholograms reload` invoke `HologramManagerImpl.unloadHolograms()`, which executes:
  ```java
  HologramStorage.saveBatch(holograms, false);
  ```
  This flushes currently loaded in-memory holograms back to `holograms.yml`.
- If an operator manually removes entries from `holograms.yml` on disk while the server is running, the next reload or autosave pass will write the in-memory entries back out, reviving deleted holograms.

### Safe Deletion Procedure
Dispatch deletion commands live via the console or Pterodactyl Client API:
```sh
holo remove <hologram_name_or_uuid>
# or
hologram remove <hologram_name_or_uuid>
```
This triggers `HologramDeleteEvent`, immediately despawns display entities from online player views, evicts the entry from the memory map, and updates `holograms.yml` on disk cleanly without requiring server restarts.

---

## 3. Hot-Reloading Proxy Routing & Queue Bypass (ajQueue, DeluxeHub, FancyNpcs)

When bypassing a proxy queue (like ajQueue) for specific backend servers without restarting servers:

### Pterodactyl API Write & List Quirks
- **Payload Encoding**: When writing configs via `POST /api/client/servers/{server_id}/files/write?file={path}`, always pass raw UTF-8 encoded bytes (`data=content.encode('utf-8')`). Passing unencoded strings can truncate multibyte characters or corrupt YAML files.
- **Root Directory Listing**: In `GET /api/client/servers/{server_id}/files/list`, never pass `directory=""` (which returns HTTP 422). Omit the `directory` query parameter or use `"/"`.

### Queue Bypass Matrix
- **DeluxeHub Menus (`menus/*.yml`)**: Replace `[COMMAND] queue <server>` with `[PROXY] <server>`. DeluxeHub's `ProxyAction` dispatches a native BungeeCord/Velocity `ConnectOther` plugin message directly to the proxy, bypassing the queue plugin entirely.
- **FancyNpcs (`npcs.yml`)**: Under `actions.ANY_CLICK`, replace `action: player_command` / `value: queue <server>` with `action: send_to_server` / `value: <server>`. FancyNpcs' `SendToServerAction` issues a native BungeeCord `Connect` plugin message directly to the proxy.
- **ajQueue Velocity (`plugins/ajqueue/config.yml`)**: Add the target server identifier to `send-instantly` list. If players still type `/queue <server>` or `/server <server>`, ajQueue forwards them immediately without holding them in the queue.

### Zero-Restart Hot-Reload Workflow
Dispatch reload commands directly via Pterodactyl Client API (`POST /api/client/servers/{server_id}/command` with `{"command": "..."}`):
1. Lobby: `fancynpcs reload`
2. Lobby: `deluxehub reload`
3. Velocity / Proxy: `ajqueue reload`
Verify confirmations in `logs/latest.log` (e.g. `Plugin has been reloaded`, `All configuration files has been reloaded in ...ms`) instead of rebooting server instances.

---

## 4. Simple Voice Chat (SVC) Velocity Sniffer & Reconnect Timeout

### Root Cause
- Older builds of `voicechat-velocity` (e.g. 2.6.13) fail to clear the client UDP socket bridge on reconnection packets (`handleSecretPacket` does not invoke `voiceProxy.disconnectBridge`), causing packets to route to stale sockets until the player reconnects to proxy.
- Default `keep_alive=1000` ms on backend servers triggers a strict 10s timeout (`keepAlive * 10L`). ISP latency spikes or packet drops cause mass voice disconnects.

### Zero-Restart Mitigation
1. **Proxy Update**: Stage official `voicechat-velocity-2.6.26.jar` into `/plugins` and rename old jar to `voicechat-velocity-<ver>.jar.old` via `PUT /api/client/servers/{server_id}/files/rename`.
2. **Backend Config**: In backend `plugins/voicechat/voicechat-server.properties`, set `keep_alive=3000` (raises timeout window from 10s to 30s).
3. Post-restart (scheduled or manual), the updated proxy bridge logic and relaxed timeout take effect seamlessly.

---

## 5. MariaDB Container Memory Hot-Shrink & Persistent Variables

When a Pterodactyl MariaDB container exceeds memory quotas due to buffer pool expansion or HikariCP idle connections:
1. **Live Resize InnoDB Pool**: MariaDB 10.6+ supports online buffer pool resizing. Run:
   ```sql
   SET GLOBAL innodb_buffer_pool_size = 268435456; -- 256MB (chunk size 128MB)
   SET GLOBAL table_open_cache = 400;
   SET GLOBAL thread_cache_size = 16;
   FLUSH TABLES;
   ```
2. **Eliminate Connection Leaks**: Inspect `/logs/server.log` for access denied / aborted connection loops (e.g. dev servers querying obsolete databases) and reconfigure offending plugins to SQLite or valid credentials.
3. **Persist Across Restarts**: Update `.my.cnf` and Pterodactyl startup variables via API:
   ```python
   PUT /api/client/servers/{server_id}/startup/variable
   {"key": "INNODB_BUFFER_POOL_SIZE", "value": "256M"}
   {"key": "MAX_CONNECTIONS", "value": "150"}
   ```

---

## 6. CustomFishing Exp Multiplier & Index Sync Workflow

### Architecture & Mechanism
In `CustomFishing`, fishing skill EXP is granted via action commands upon catch success rather than internal variables:
- Loot commands: `- sk xp add {player} fishing <amount>` in `contents/item/default.yml`.
- Index GUI: `custom-data.index-xp: <amount> XP` in `contents/item/default.yml` (displayed in `/fishingindex`).
- Competition rewards: `sk xp add {player} fishing <amount>` in `contents/competition/default.yml`.

### Multiplier Update & Hot-Reload Procedure
1. Backup `default.yml` to `.bak` in both `contents/item/` and `contents/competition/`.
2. Apply multiplier proportionally: update both `sk xp add ... fishing <N*multiplier>` and `index-xp: <N*multiplier> XP` so player-facing index matches actual XP gained.
3. Reload without server restart: dispatch `cfishing reload` via console (`POST /api/client/servers/{server_id}/command`). Verify reload time (~50-150ms) in `logs/latest.log`.

