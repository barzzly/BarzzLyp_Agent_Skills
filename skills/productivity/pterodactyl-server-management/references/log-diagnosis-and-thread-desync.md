# Minecraft Server Log Diagnostics & Thread Desync Resolution

## Pterodactyl Client API Log Retrieval Quirks
- **WAF / Cloudflare 403**: Panel endpoints (e.g. `panel.ultraservers.com`) often block generic Python `urllib` user agents with `HTTP 403 Forbidden`. Always include a browser-like header: `'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'`.
- **Signed Download URLs Expire Quickly**: `GET /api/client/servers/{id}/files/download?file=logs/latest.log` returns a temporary signed URL that expires within minutes. Always re-fetch the signed URL immediately prior to streaming or reading rather than caching it across long operations.

## Critical Log Signatures & Fix Procedures

### 1. Off-Main Thread Entity Add / Skill Collision (TickThread Failure)
- **Signature**:
  - `[ca.spottedleaf.moonrise.common.util.TickThread] Thread failed main thread check: Cannot add entity off-main`
  - Followed by AdvancedEnchantments errors: `Failed to activate effect GUARD:... / EXP:... / LIGHTNING`
  - Accompanied by Netty serialization crashes: `EncoderException: Failed to encode packet 'clientbound/minecraft:container_set_content'` due to off-main ItemStack mutation.
  - Proxy symptoms: players kicked with `disconnect.timeout` or `read timed out`.
- **Root Cause**:
  `MythicMobs` / `MythicLib` runs target checks or auras on async scheduler threads (`lumine-fscheduler` / `Craft Scheduler Thread`). When `interaction_rules.enabled: true` in `plugins/MythicLib/config.yml`, MythicLib calls `EntityManager.canInteract()` which fires a synthetic `EntityDamageByEntityEvent` off the main thread to test damage rules. `AdvancedEnchantments` intercepts this fake event asynchronously and attempts to trigger combat abilities (`GUARD` entity spawn, `LIGHTNING`, exp drop) off-main, triggering Paper's Moonrise `TickThread` assertion failure and spiking CPU.
- **Fix**:
  1. In `plugins/MythicLib/config.yml`, set:
     ```yaml
     interaction_rules:
       enabled: false
     ```
     (Default upstream setting; PvP safety between parties/guilds remains handled by plugins like BetterTeams).
  2. Reload without restart: `/ml reload` or `/mythiclib reload`.

### 2. POI Data Mismatch (`POI data mismatch: never registered at BlockPos`)
- **Signature**:
  `[Server thread/ERROR]: POI data mismatch: never registered at BlockPos{x=..., y=..., z=...}`
- **Root Cause**:
  Point of Interest data in `world/poi/r.<x>.<z>.mca` desynchronized from actual workstation/bed blocks in that chunk (typically from bulk placement, WorldEdit, or block destruction in villager trading halls / crop farms).
- **Fix**:
  - **Live (No Restart)**: Break and replace the affected workstation or bed blocks in the coordinate area. Placing the block forces Paper to write a fresh, valid POI entry.
  - **Clean Rebuild (Maintenance)**: Stop server, delete the desynced region file (e.g. `world/poi/r.-4.-5.mca` for coordinates around -1800, -2440), and restart. Paper automatically rescans the chunk blocks and regenerates valid POI records.

### 3. Continuous "moved wrongly!" Spam
- **Signature**:
  `[Server thread/WARN]: <Player> moved wrongly!` logged repeatedly every second.
- **Root Cause**:
  Player client entity position stuck or desynced with server physics/blocks, forcing the server to send constant correction packets on the main tick thread.
- **Immediate Mitigation**:
  Teleport the player to a safe spawn location (`/tp <Player> <spawn_coords>`) or issue a kick (`/kick <Player> fix desync`) to cleanly reset the connection state without restarting the server.
