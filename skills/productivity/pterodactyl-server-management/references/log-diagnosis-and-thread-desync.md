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

### 4. BetterTeams StringUtil Infinite Loop / Watchdog Timeout
- **Signature**:
  - `The server has not responded for 10/30/60 seconds! Creating thread dump`
  - Stack trace on Server thread in `java.lang.StringBuilder.replace` called by `com.booksaw.betterTeams.util.StringUtil.setPlaceholders`.
  - Console STDOUT right before freeze: `[BetterTeams] [STDOUT] Description : {0}`.
  - Server halts with `Exit code: 70`.
- **Root Cause**:
  In BetterTeams upstream (including 5.1.8), `StringUtil.setPlaceholders(String, Object...)` uses `while ((index = formatted.indexOf(placeholder)) != -1)`. Because it searches from index 0 on every iteration, if a team description or input contains `{n}` (e.g. `{0}`), it replaces `{0}` with `{0}` infinitely on the main tick thread.
- **Fix**:
  1. **Data Cleanup**: In `plugins/BetterTeams/teams.yml`, remove any `description: '{0} '` or `{n}` patterns.
  2. **Bytecode / Source Patch**: Update `StringUtil.java`:
     ```java
     int index = 0;
     while ((index = formatted.indexOf(placeholder, index)) != -1) {
         formatted.replace(index, index + placeholder.length(), replacement);
         index += replacement.length();
     }
     ```
     Recompile and inject `StringUtil.class` back into `BetterTeams-<ver>.jar`.


### 4. Recursive Placeholder Infinite Loop (Watchdog Timeout / Exit Code 70)
- **Signature**:
  - `[ERROR]: The server has not responded for X seconds! Creating thread dump`
  - Thread dump on `Server thread` stuck at `StringBuilder.replace` / `StringUtil.setPlaceholders` called via plugin message formatters (e.g. `BetterTeams.message.MessageManager.sendSafeReplacedMessage` -> `ReferencedFormatSafeMessage.sendMessage`).
  - Server killed by Paper Watchdog with `Exit code: 70`, `Out of memory: false`.
- **Root Cause**:
  Plugin string replacement routines (e.g. `BetterTeams.util.StringUtil.setPlaceholders`) scan for indexed placeholders like `{0}` from index 0 repeatedly via `while ((index = formatted.indexOf(placeholder)) != -1)`. If user-controlled input (e.g. team description, team tag, or custom rank title) contains `{0}` or `{n}`, replacing `{0}` with the input string leaves `{0}` in the buffer. The matcher hits the same placeholder again, causing an infinite while loop that pegs CPU to 100% and completely locks the main tick thread.
- **Immediate Mitigation / Fix**:
  1. Inspect the thread dump in the latest crash report or log for the exact plugin method and logged values (e.g. `[BetterTeams] [STDOUT] Description : {0}`).
  2. Search data files (e.g. `plugins/BetterTeams/teams.yml`) for entries containing `{0}` or placeholder syntax:
     - Search regex: `description:\s*['"]?\{[0-9]+\}`
  3. Cleanse the offending strings (set to `''` or strip `{n}`) directly in the data file.
  4. Ensure input validation or command pre-processing filters out indexed format strings (`{[0-9]+}`) from user-submitted text fields.
