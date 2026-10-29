# Aloc boss position anchor

- On NoeRPG, PUBLIC dungeon `aloc` uses world `DungeonAloc`; boss `alocTheDemonicMech` spawns at `(0,64,0)` via `plugins/NoeDungeon/dungeons/aloc/objectives.yml`.
- Its MythicMobs mob config is `plugins/MythicMobs/packs/BOSS_AlocTheDemonicMech/Mobs/alocTheDemonicMechMobs.yml`. It already has `MovementSpeed: 0.001`, `KnockbackResistance: 1`, and an `~onDamaged` velocity reset, yet external knockback can move it. For a boss expected to remain anchored, MythicMobs documents `teleport @CasterSpawnLocation`; use a timer only on the boss and retain the combat skills. `@SpawnLocation` means world spawn, not this boss's spawn.
- Backup exact remote bytes, edit only Aloc boss, verify readback; `mm reload` reloads MythicMobs without restarting server. Confirm completion in `logs/latest.log` and server state via resources. A reload does not demonstrate that an already-spawned boss adopted new timer behavior; verify during next boss spawn/attack and report that gap.
- Read `logs/latest.log` for console commands sent via Pterodactyl Client API because HTTP 204 only confirms command queued. Avoid spawning a duplicate boss into a live PUBLIC arena merely to test.

## Shared Arena Entry & Teleportation Safety
- **Auto-dismount sitting/mounted players**:
  - `Player.teleport()` in Bukkit / Paper returns `false` (refusing the teleport) when a player is sitting (e.g. GSit chairs, poses), riding a vehicle, or carrying passengers. Always execute `player.leaveVehicle()` and `player.eject()` before invoking `player.teleport(destination, TeleportCause.PLUGIN)` to enter dungeons or arenas.
- **Case-insensitive world containment checks**:
  - Session and region boundary containment checks must compare world names case-insensitively (`equalsIgnoreCase`), because Bukkit/Paper dimension keys and world aliases (e.g. `minecraft:dungeonaloc` vs `DungeonAloc`) can differ in casing and cause false out-of-bounds rejections.
