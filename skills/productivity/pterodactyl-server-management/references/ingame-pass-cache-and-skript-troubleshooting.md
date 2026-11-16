# Ingame Pass Cache & Skript Migration Troubleshooting

## 1. Custom Pass In-Memory Cache Flush
When plugins maintain an in-memory LRU cache alongside YAML player data (e.g. `NoeWeeklyPass` with a 512-entry capacity), directly overwriting the player file on disk is ignored by runtime commands like `/weeklypass <pass> acc <nick>` because the memory cache still marks the pass as active or already granted.

### Protocol to Reset a Player Pass Live Without Server Restart:
1. **Identify Player UUID:** Fetch UUID via PAPI or usercache:
   `papi parse <nick> %player_uuid%`
2. **Update On-Disk YAML via Panel Client API:**
   Write the target player YAML in `plugins/<Plugin>/data/players/<UUID>.yml` with `start` set to current date, `authorized: true`, and empty claims/pending maps (`claims: {}`, `pending: {}`).
3. **Evict Plugin In-Memory Cache via RCON:**
   Flood the LRU cache beyond its size limit (e.g. 520 calls) with dummy UUID lookups via RCON:
   ```javascript
   for (let i = 1; i <= 520; i++) {
     const hex = i.toString(16).padStart(12, '0');
     await rcon.send(`weeklypass <pass> disacc 00000000-0000-0000-0000-${hex}`);
   }
   ```
4. **Verify:** When the player opens the menu in-game, the plugin reloads fresh state from disk with Day 1 available.

---

## Skript severe errors versus server crashes

1. Resolve the live server name and inspect `/resources`; preserve power state during diagnosis. Fetch `logs/latest.log` and retain a local evidence copy.
2. Extract one complete `[Skript] Severe Error` block, including `Caused by`, first plugin frame, `Current item`, and `Current trigger`. Count error blocks, not stack-trace lines; addon lists alone do not identify the culprit.
3. Read the named `.sk` function and its callers. For placeholder failures involving `Player.getLocation()` on a null player, inspect delayed join handlers and disconnect timing. A typed `player` argument does not guarantee an online player after `wait`; PlaceholderAPI may receive an OfflinePlayer whose live Player resolves to null.
4. Revalidate online status after each delay and immediately before online-only placeholders. Guard the shared function as well as delayed callers, and return a safe value when the player is gone. Treat this as a proposed fix until target-script reload and a join/disconnect reproduction confirm it; do not trigger a production crash merely to reproduce one.
5. Establish crash evidence separately: search for watchdog dumps, `OutOfMemoryError`, fatal tick exceptions, shutdown boundaries, and matching crash-report timestamps. A caught Skript exception is not proof that the JVM stopped. Read node `server.log` around shutdown to distinguish an explicit `stop` command from an unexpected exit. Label old crash reports historical rather than attributing them to current warnings.
6. If panel file listings omit recent logs, compare direct SFTP `listdir_attr('/logs')`, sort numeric `st_mtime`, and inspect recent compressed logs. Do not conclude no recent logs exist from a partial API listing.
7. Report exact script/function, failing expression, observed mechanism, current server state, and whether crash causality is confirmed. For check-only requests, stop at diagnosis; do not silently edit, reload, or restart.

## 2. Nexo Item Migration in Skript Commands
When servers migrate from legacy item managers (e.g. ItemsAdder) to Nexo:
- Replaced commands like `iagive <player> <item> <amount> silent` break silently in scripts.
- Replace with Nexo syntax: `nexo give <player> <item> <amount>`.
- Reload target scripts individually in runtime via RCON: `skript reload <script_name>.sk`.

---

## 3. Pterodactyl Auto-Restart Schedule Offsets
- Pterodactyl schedule crons run on **UTC**.
- For WIB (UTC+7):
  - 10:00 WIB target restart -> Cron at 02:50 UTC (09:50 WIB) with 10-minute warning sequences.
  - 09:00 WIB target restart (1 hour before 10:00 WIB) -> Cron at 01:50 UTC (08:50 WIB).
- Sequence tasks: 10m warning -> 5m -> 10s -> countdown 5s..1s with `save-all` -> `kickall` -> `restart` power action.
