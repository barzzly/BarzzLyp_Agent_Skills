# Plugin Permission Scoping & In-Game Redeem Rewards

## Strict Permission Scoping for Player Rewards & Trials
- **Never grant blanket plugin wildcards (`<plugin>.*`) in temporary permissions, trial rewards, or redeem codes**:
  - Many Bukkit/Paper plugins (such as MCPets) nest administrative and moderation capabilities under the exact same root namespace (e.g., `mcpets.admin` governs `/mcpets revoke <player>`, `/mcpets clearstats`, `/mcpets editor`).
  - Granting `mcpets.*` grants players full administrative power over the plugin, enabling them to revoke or despawn other players' active pets.
- **Auditing Permission Trees in Plugin Files & JAR Classes**:
  - Model and cosmetic assets frequently use different namespace conventions than the plugin's internal commands:
    - In MCPets, standard models (CubeDragons, RPGMounts, SamusDragons) use `mcpet.<id>` (`mcpet.*` is safe to grant because internal admin permissions reside strictly under `mcpets.admin`).
    - Author packs located under `mcpets.` must be targeted explicitly by prefix (e.g., `mcpets.elitedragon`, `mcpets.elitemountvol1*`), never `mcpets.*`.
    - Player capabilities and skins: `mcpets.mount` (allows riding mountable pets), `skin.*` (covers skin variants).
    - Administrative nodes that must remain restricted: `mcpets.admin`, `mcpets.color`.
- **LuckPerms Temporary Grant Syntax & Server Context**:
  - When awarding temporary trial perks via console or redeem plugins, use scoped durations and target server context:
    `lp user %player% permission settemp <node> true 2d server=<servername>`
  - Scoping to `server=<servername>` prevents temporary permissions from bleeding into other network servers (e.g., Lobby, Survival, Hub).

## Remote Config Deployment & Hot-Reload Workflow
1. **Deploy Config via Pterodactyl Client API**:
   - Write raw content via `POST /api/client/servers/{server_id}/files/write?file={url_encoded_path}` with `Content-Type: text/plain` and standard browser `User-Agent`.
2. **Read Back & Assert Security Gates**:
   - Fetch the file via `/files/contents` and assert dangerous wildcards (such as `mcpets.*`) are absent before players can access the code.
3. **Console Reload & Verification**:
   - Trigger plugin reload via `POST /api/client/servers/{server_id}/command` (e.g. `{"command": "advancedredeem reload"}`).
   - Inspect `logs/latest.log` to confirm reload success message (e.g., `Plugin has been successfully reloaded!`) and check for any syntax or database errors.

## Skript Reward Dispatch & Reload Aliasing
- **Explicit `execute` syntax required for console commands**:
  - In Skript scripts (`plugins/Skript/scripts/*.sk`), executing server commands requires `execute console command "<cmd>"`.
  - Omitting `execute` (e.g. writing `console command "/p give %loop-player% 50"`) produces a syntax compilation error (`Can't understand this condition/effect`). Any `send ...` lines in the same block continue to execute normally, causing players to receive chat notifications (e.g. "You received 50 coins") while the currency is silently dropped.
- **RCON Reload Command Collision with AuraSkills**:
  - Never execute shorthand `sk reload <script>` via RCON/console when AuraSkills or Skills plugins are present; `sk` aliases to `/skills reload`.
  - Always use `skript reload <script>` or `skript reload scripts` and check the console response to confirm 0 compilation errors.
