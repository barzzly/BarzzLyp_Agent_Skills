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

