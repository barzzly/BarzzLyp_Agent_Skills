---
name: paper-plugin-integration
description: "Use when integrating Paper plugins."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [paper, minecraft, plugins, menus, api-integration, performance]
    category: software-development
---

# Paper Plugin Integration

## Procedure

1. Inspect both repositories before editing.
   - Read plugin source, `plugin.yml`, build file, tests, config, and dependency manifests.
   - Inspect target provider's exact source or installed JAR with `jar tf` and `javap`.
   - Confirm package names and descriptor names. Similar inspection JARs may be stale.

2. Establish build gate.
   - Run existing focused check before edits.
   - Use one Gradle worker: `bash ./gradlew clean check --no-daemon --max-workers=1`.
   - If sibling source-built artifact is only API match, add exact artifact compile/test-only; never shade provider classes.

3. Write behavior tests first.
   - Assert setting count, exact inventory slots, click boundaries, descriptor dependencies/permissions, and provider persistence.
   - Run test and observe expected RED before production edits.
   - Keep native rendering and restart durability separate from headless checks.

4. Integrate through public provider APIs.
   - Prefer provider getters/mutators over private reflection.
   - Use reflection only for optional providers without public state APIs; fail closed when fields or state are unavailable.
   - Preserve provider persistence. Do not create competing preference databases.

5. Build menu around semantic slots.
   - Put new actions in requested slot, especially deliberate center gaps.
   - Preserve close/filler slots. Validate clicks against registered settings, not broad ranges.
   - Disable italic decoration explicitly on ItemStack names and lore.

6. Keep menu configuration real.
   - Move titles, descriptions, status/action text, filler materials, close labels, and permissions into YAML when configurable settings are expected.
   - Reload YAML and derived in-memory assets in reload command.
   - Register reload aliases and allow console reload when permission permits; player-only menu opening remains separate.

7. Keep interaction lightweight.
   - Handle synchronous inventory click mutations directly when provider APIs are synchronous.
   - Do not add polling, per-second checks, or scheduler hops for simple toggles.
   - Search `src/main` for scheduler calls after editing. Retain recurring work only with measured reason, bounded cadence, and cleanup.

8. Verify final artifact.
   - Run `git diff --check`.
   - Run full `clean check` with one worker and inspect named self-check markers, not only exit code.
   - Build JAR, inspect packaged `plugin.yml` and config resources, record artifact path.
   - Report compiled, packaged, headless-tested, live-tested, and deployed states separately.

## Rules for this user's Paper plugins

- Keep `folia-supported: false` unless every Bukkit/entity/world operation is region-scheduler safe.
- Treat viewer-side visibility as distinct from owner broadcast visibility. Viewer hide/show must not remove an owner's nametag from other viewers.
- Do not deploy or restart live Minecraft server during local integration unless explicitly authorized. Built JAR is not deployed JAR.
- Zero-downtime plugin staging: When server restart is forbidden, stage new verified JARs directly into `/plugins/`, rename existing JARs to `.jar.old` via Pterodactyl API (`PUT /api/client/servers/{server}/files/rename`), and update on-disk configs (`.properties` / `.yml`) so updates take effect on the next scheduled server restart without causing immediate service downtime.
- Player teleportation into instances/arenas: Always invoke `if (player.isInsideVehicle()) player.leaveVehicle();` and `player.eject();` before `player.teleport(loc, PlayerTeleportEvent.TeleportCause.PLUGIN)`. Seated players (GSit chairs/stairs) or players carrying passengers/cosmetics cause Bukkit's bare `teleport(loc)` to return `false`. Always specify `TeleportCause.PLUGIN` rather than default `UNKNOWN` to avoid false cancels by teleport interception plugins.
- Case-insensitive world matching: Always use `loc.getWorld().getName().equalsIgnoreCase(worldName)` for containment checks and region boundaries. Multiverse aliases, folder casings (`/DungeonAloc`), and internal dimension keys (`minecraft:dungeonaloc`) frequently differ in case; strict `.equals()` causes false containment/teleport failures.
- Teleport refusal diagnostics: Always include detailed diagnostics (teleport boolean result, containment boolean, registration status, source and destination world names, coordinates) when throwing or catching entry/teleport failures instead of a bare `IllegalStateException`.
- Simple Voice Chat on Velocity proxy: Proxy versions prior to 2.6.26 fail to disconnect stale bridges on `SecretPacket` handling, routing reconnect packets to dead client UDP ports and permanently wedging voice chat. Keep `voicechat-velocity` at 2.6.26+ and set `keep_alive=3000` (30s timeout tolerance) in `voicechat-server.properties` across backend servers to prevent short network jitter from triggering mass disconnects.
- Prefer smallest diff: existing providers, menu structure, config keys, and tests before new abstractions.

## Common pitfalls

- Compile against exact provider bytes: package renames and stale inspection artifacts can expose wrong API.
- Do not use delayed scheduler merely to close GUI before synchronous preference mutation; extra task adds ordering cost and can race inventory state.
- Do not call broadcast hide for viewer preference; it changes what other players see.
- Do not treat source compile as packaged verification; loader reads final JAR resources/classes.
- Do not call config reload complete until derived menu assets are rebuilt; otherwise values stay stale until restart.
- Do not call bare `player.teleport(loc)` without dismounting vehicles/passengers; seated players (GSit) or players with pets/cosmetics cause Bukkit to return `false`, rejecting entry.
- Do not compare Bukkit `world.getName()` with strict case sensitivity against configured world names; dimension namespaces and folder casings frequently diverge across Multiverse and vanilla world managers.
