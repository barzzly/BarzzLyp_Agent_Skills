---
name: minecraft-plugin-performance
description: "Use when optimizing Paper plugins. Keep gameplay safe."
version: 1.0.0
author: Hermes Agent
---

# Paper Minecraft Plugin Performance

## Procedure

1. Establish build gate before edits.
   - Run project identity/verification scripts, `git diff --check`, and project build command.
   - If dependency resolution blocks compilation, record exact missing artifacts; do not claim runtime compatibility or release a JAR.

2. Audit execution context before optimizing hot paths.
   - Search plugin code for `CompletableFuture.runAsync`, `supplyAsync`, executor services, async scheduler calls, and Bukkit/Paper world/entity/event API calls.
   - Move Bukkit world reads, entity mutation, events, module transitions, region work, and scheduler-owned state to Paper server scheduler.
   - Keep async work only for data detached from Bukkit state. Never block server thread with `join()` or `get()`.
   - Advertise Folia support only after every entity/world operation is region-scheduler safe; otherwise set `folia-supported: false`.

3. Optimize generation without deleting behavior.
   - Precompute a small bounded location pool per configured world and generation mode.
   - Refill incrementally with a scheduled task; perform at most one candidate search per task run.
   - Poll pools non-blockingly and return no location when empty. Never assume a scheduled refill already ran.
   - Initialize generation config before constructing its pool, and key pool entries by world identity so multiworld dungeons never cross worlds.
   - Cancel refill tasks and clear pools during disable.

4. Optimize mobs while preserving configured counts, factions, drops, and waves.
   - Keep spawn and teleport checks on server thread.
   - Cache dungeon location, region, and squared radius once per update; use `distanceSquared` for range checks.
   - Remove invalid references for every faction. On cleanup, remove entity once and clear collection entry; do not damage an entity after removal.
   - Store and read dungeon association using same PDC key.

5. Bound recurring work and hot caches.
   - Skip `PlayerMoveEvent` logic when player stayed in same block.
   - Add maximum size and expiry to coordinate lookup caches that can receive every player position.
   - Do not broaden cache keys unless invalidation points are defined for spawn, despawn, delete, and reload.
   - Make module activation state equal actual activation result; reset it after exception/failure.

6. Verify and report.
   - Run textual safety checks covering plugin identity, Paper/Java target, async Bukkit ban, generator initialization, per-world pool access, and changed regression behavior.
   - Run `git diff --check`, then full build. Test in Paper server only after build succeeds.
   - Report verified checks, commit hash if pushed, and exact remaining external blocker.

## Pitfalls

- Do not move Bukkit calls to a plain Java executor for throughput; Paper world/entity state is scheduler-confined and races become intermittent corruption.
- Do not make one global location queue for multiple worlds; callers request a specific world and cross-world locations break dungeon placement.
- Do not schedule several expensive terrain probes in one burst; `getHighestBlockYAt`, block and chunk reads can cause tick spikes.
- Do not claim Paper-version support solely from API dependency coordinates; require dependency resolution, compilation, and server smoke test.
- Do not label custom Bukkit event execution as safe merely because event class is named `Async`; listeners can still call Bukkit APIs.

See [references/paper-threading-and-verification.md](references/paper-threading-and-verification.md) for audit patterns and release gates.
