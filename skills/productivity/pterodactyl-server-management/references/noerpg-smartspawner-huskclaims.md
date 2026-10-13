# NoeRPG SmartSpawner vs HuskClaims

- Diagnose using live target server, plugin configs and exact running JAR bytecode. SmartSpawner 1.8.2 `plugin.yml` and `IntegrationManager.checkProtectionPlugins()` register WorldGuard, GriefPrevention, Lands, etc., but no HuskClaims. NoeRPG ECORPG uses HuskClaims 1.5.11 for player land; log showed 137 claims and only `WorldGuard integration enabled successfully!` for SmartSpawner.
- `SpawnerClickManager.handleSpawnerInteraction` only consults `CheckOpenMenu.CanPlayerOpenMenu`, which loops registered protection hooks. Without HuskClaims hook, an ordinary claimed plot does not deny opening spawner GUI. `SpawnerMenuAction.collectExpForPlayer` contains no claim or ownership check before giving XP and zeroing storage. A cancellable `SpawnerExpClaimEvent` is emitted (except with no listeners). Therefore player-owned claims don't protect the SmartSpawner GUI/XP by default. OP or wildcard `*` bypass in `CheckOpenMenu` is another, distinct route.
- For a fix request, first establish an exact no-trust non-OP repro against a test spawner/claim and choose a supported official integration or narrow custom guard. Do not assume a config key or a WorldGuard region emulates HuskClaims. For a custom guard, validate at GUI entry and at XP mutation, including direct/list GUI and silent XP paths; `collectExpSilently` invokes AuraSkills XP and Mending **before** `SpawnerExpClaimEvent`, so event cancellation alone does not guarantee zero benefit. Preserve stored XP, trust levels, child claims and bypass semantics; test owner/trusted/untrusted/wilderness and avoid live player data mutation during diagnosis.

## SmartSpawner forensics & XP theft audit procedure

- Activity logs are kept at `plugins/SmartSpawner/logs/spawner-YYYY-MM-DD.log` (configured via `activity_log.yml`). Key logged events: `Experience claimed`, `Spawner placed`, `Spawner broken`, `Spawner stacked by hand`, `Items sold`.
- Log entry format: `[YYYY-MM-DD HH:MM:SS] <Action> | Player: <PlayerName> | Location: <world> (<x>, <y>, <z>) | [exp_amount=<n> | Entity: <mob> | total_price=<p>]`.
- To trace who looted or interacted with a victim's spawner:
  1. Retrieve victim UUID from `/usercache.json` or `plugins/Essentials/userdata/<uuid>.yml`. Look up home coordinates (`farm`, `home`) or logout coordinates to establish candidate farm XYZ bounds.
  2. Grep `plugins/SmartSpawner/logs/spawner-*.log` for coordinates where victim placed or interacted with spawners to build exact `(world, x, y, z)` spawner sets.
  3. Filter the spawner logs for all events at those coordinates where `Player != <victim>`. Non-owner `Experience claimed` entries immediately expose who drained the XP, the exact timestamp, and the stolen amount.
  4. Cross-reference timestamp against rotated server logs (`logs/YYYY-MM-DD-*.log.gz`) to correlate the player's session, chat history, teleportation, or staff duty status.
