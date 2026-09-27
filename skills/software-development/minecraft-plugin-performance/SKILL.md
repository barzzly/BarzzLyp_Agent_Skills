---
name: minecraft-plugin-performance
description: "Use when optimizing Paper plugins. Keep gameplay safe."
version: 1.0.0
author: Hermes Agent
---

# Paper Minecraft Plugin Performance

## Procedure

For this user's Minecraft work, use Astra for parent and delegated agents. Inspect the delegation model override and verify a spawned child's actual model; changing the parent does not change a pinned child model. If correcting model selection, stop old-model workers before assigning their files to replacements.

1. Establish build gate before edits.
   - Run project identity/verification scripts, `git diff --check`, and project build command.
   - If dependency resolution blocks compilation, record exact missing artifacts; do not claim runtime compatibility or release a JAR.

2. Audit execution context before optimizing hot paths.
   - Search plugin code for `CompletableFuture.runAsync`, `supplyAsync`, executor services, async scheduler calls, and Bukkit/Paper world/entity/event API calls.
   - Move Bukkit world reads, entity mutation, module transitions, region work, and scheduler-owned state to the appropriate Paper/Folia scheduler. Inspect custom event contracts first: preserve deliberately asynchronous events and separate their surrounding Bukkit operations rather than changing event thread semantics blindly.
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
   - Assign one source/build owner per checkout, including the parent agent; while that owner edits or runs Gradle, all other workers stay read-only or use isolated runtime trees. Never start a second compile or patch files being compiled. After interrupted or overlapping work, freeze source, rerun verification, and preserve each run's XML/logs before another test invocation replaces them.
   - Run `git diff --check`, full build, then all registered runnable regressions. Compile-only or source-token checks do not replace executing production methods.
   - Hash the final JAR and the copy loaded by isolated Paper; rerun affected runtime gates after any production edit. Parse named case markers and expected counts, not merely client exit code: clients can exit zero while server assertions fail.
   - Treat a production-readiness request as implementation plus integration, not an audit deliverable. Turn fixable blockers into failing tests and continue repairs within authorized scope instead of repeatedly telling this user to wait or keep the feature disabled. Keep unsafe artifacts undeployed; escalate only a concrete external blocker or scope decision. Distinguish compiled, built, runtime-tested, and deployed states in the final short report.
   - When work continues in background, state that explicitly and name each worker's role; verify live worker status before answering whether work stopped. Do not imply that a final chat reply alone means repairs are still running. Absorb delayed notifications already covered by newer evidence. When this user asks to hear only when production-ready, suppress routine partial updates; report verified readiness or a concrete decision requiring their input. Answer requested progress with current gates and exact test results, not an invented percentage. Readiness notification is not deployment authorization.
   - Report commit hash only if pushed; do not claim throughput improvement without a measured benchmark or universal compatibility from one Paper version.

For biome-only CustomFishing configuration, read [references/biome-fishing-config.md](references/biome-fishing-config.md): additive pools, gear bypasses, lava preservation, index labels, and configuration verification.

For durable economy transfer work, load [references/durable-economy-review.md](references/durable-economy-review.md): account ownership, async snapshot atomicity, pending-fund fences, exact receipts, and release layers.

## Pitfalls

- Guard same-JVM file ownership before opening another channel to an already locked inode; closing a rejected duplicate descriptor can drop process-associated POSIX locks while Java still reports the original FileLock valid. Reserve canonical path before open, release on actual close, and test a separate-process challenger after a rejected duplicate constructor.
- Keep durable-success acknowledgement monotonic: replaying the exact stored receipt must preserve ACK and avoid a rewrite. Recovery must query provider receipts, never replay monetary mutation; bound HTTP retries per recovery cycle so outage recovery cannot monopolize the shared IO queue.

- Bound whole HTTP exchanges, not only response headers: JDK `BodyHandlers.ofInputStream()` can return before body arrives, leaving `readNBytes` stuck beyond request timeout. Use a fixed-size subscriber, timed completion wait, cancellation on timeout/interruption, and a real TLS partial-body regression; keep waiting on dedicated IO only.
- Spread heartbeat and balance collection over bounded ticks; publish full presence snapshots only. Guard incremental iterators with a membership/auth generation, reject stale queued batches, and document that continuous churn can defer snapshots. A per-tick item cap is not a latency guarantee for arbitrary third-party Vault calls.
- Test Gson parser modes with signed malformed fixtures. `setLenient(false)` in Gson 2.10.1 remains legacy-strict and accepts uppercase booleans and some non-JSON strings. Preserve cross-plugin Gson compatibility while rejecting lexical violations; never assume parser naming proves strictness.

- Do not move Bukkit calls to a plain Java executor for throughput; Paper world/entity state is scheduler-confined and races become intermittent corruption.
- Do not make one global location queue for multiple worlds; callers request a specific world and cross-world locations break dungeon placement.
- Do not schedule several expensive terrain probes in one burst; `getHighestBlockYAt`, block and chunk reads can cause tick spikes.
- Do not claim Paper-version support solely from API dependency coordinates; require dependency resolution, compilation, and server smoke test.
- Do not label custom Bukkit event execution as safe merely because event class is named `Async`; listeners can still call Bukkit APIs.

See [references/paper-threading-and-verification.md](references/paper-threading-and-verification.md) for audit patterns and release gates.

For whole CustomFishing audits, load [references/fishing-audit-regressions.md](references/fishing-audit-regressions.md) for delayed rewards, bag/market boundaries, atomic storage, and real-runtime fixture pitfalls.

For built-in CustomFishing menus, load [references/native-fishing-index.md](references/native-fishing-index.md): shaded Adventure compatibility, native stats aliases, command migration, read-only inventory safety, and isolated Paper smoke tests.
