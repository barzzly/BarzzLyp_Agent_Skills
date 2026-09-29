---
name: minecraft-plugin-performance
description: "Use when optimizing Paper plugins. Keep gameplay safe."
version: 1.0.0
author: Hermes Agent
---

# Paper Minecraft Plugin Performance

## Procedure

For this user's Minecraft work, use Astra for parent and delegated agents. Inspect the delegation model override and verify a spawned child's actual model; changing the parent does not change a pinned child model. If correcting model selection, stop old-model workers before assigning their files to replacements.

For this user's VPS, do not launch local Minecraft/Paper servers or graphical clients unless explicitly reauthorized. Use one Gradle worker and lightweight production-class regressions; perform runtime checks only on the authorized remote server after backup. Do not substitute production stress tests or mass spawns. Confirm restart timing when players are online, and report visual/gameplay gaps separately. This constraint overrides isolated-server recipes below.

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
   - Hash the final JAR and the copy loaded by the authorized runtime; rerun affected runtime gates after any production edit. Namespace-only changes also invalidate prior runtime evidence; publishing a release does not authorize another deployment or restart. Parse named case markers and expected counts, not merely client exit code: clients can exit zero while server assertions fail.
   - Treat a production-readiness request as implementation plus integration, not an audit deliverable. For requests to finish or optimize every feature, first enumerate feature families and record each audit finding, runnable acceptance check, unchanged-safe decision, and unresolved dependency. Turn fixable blockers into failing tests and continue repairs within authorized scope; a targeted patch is not completion of the full request. Keep unsafe artifacts undeployed; pause only for a concrete external blocker or required user action, stating exactly what input unblocks it. Distinguish compiled, built, runtime-tested, and deployed states in the final short report.
   - When work continues in background, state that explicitly and name each worker's role; verify live worker status before answering whether work stopped. Do not imply that a final chat reply alone means repairs are still running. Absorb delayed notifications already covered by newer evidence. When this user asks to hear only when production-ready, suppress routine partial updates; report verified readiness or a concrete decision requiring their input. Answer requested progress with current gates and exact test results, not an invented percentage. Readiness notification is not deployment authorization.
   - Report commit hash only if pushed; do not claim throughput improvement without a measured benchmark or universal compatibility from one Paper version.

For biome-only CustomFishing configuration, read [references/biome-fishing-config.md](references/biome-fishing-config.md): additive pools, gear bypasses, lava preservation, index labels, and configuration verification.

For durable economy transfer work, load [references/durable-economy-review.md](references/durable-economy-review.md): account ownership, async snapshot atomicity, pending-fund fences, exact receipts, and release layers.

## Offline wallet expectations

- For Noesantara minigames, the user expects ECO RPG balances to remain inspectable while the player is offline and cares about Minecraft request/load costs. Distinguish last-known cached balance from a fresh offline-provider lookup; label snapshot age, never present stale data as realtime, and never use display caches to authorize transfers.
- Explain browser-to-web polling separately from plugin-to-web batch publishing. Verify actual intervals and provider calls from code before quoting them; do not infer live TPS impact from architecture alone.

## Offline wallet display

- Prefer existing web-DB snapshots for offline balance display when minimum Minecraft overhead is priority. Return a separate `lastKnownIngameBalance` display-only field; keep `ingameBalance` null while offline/stale so existing transfer gates remain fail-closed. Preserve original timestamp, label cached data explicitly, handle zero versus missing snapshots, and test logout presence without refreshing age. Do not add offline account scans, per-visitor Minecraft calls, or new cache processes for data already stored.
- Do not equate no added Minecraft work with measured zero CPU/RAM. State unchanged polling and provider behavior; quantify usage only with runtime measurements.

## Snapshot efficiency checks

- For NoeWebApi bug/performance work, keep execution foreground when requested. Target low measured CPU/allocation without promising zero usage; preserve live Vault checks and fsync safeguards.
- Reduce unchanged empty-presence heartbeats only below backend capability TTL; publish first player, last disconnect, and provider changes immediately and retry failed transport on normal ticks. Do not cache balances used to authorize money mutations.
- Precompile per-player validation patterns. Isolate individual Vault read failures so one unavailable account does not suppress healthy players; omit unavailable account rather than invent its balance.
- Rebuild the fixture-loaded JAR after class edits: PaperTest loads plugin classes from the JAR, so compiling build/classes alone tests stale code. Measure CPU time and allocated bytes separately from retained heap, report mocked provider/transport boundaries, and avoid presenting microbenchmark reductions as live-server savings.

## Inventory layout verification

- Inventory symmetry changes must test packaged YAML and empty-layout Java fallbacks together, including row counts; moving only resource slots leaves missing-file menus inconsistent.
- Fill paginated content left-to-right from the first available slot, then continue on the next row; never center partial pages. Pass the same slot to item rendering and click registration. Preserve explicit custom slot order, list capacities, conditional party controls, destructive confirmation, and editable loot boundaries. Keep Create Party bottom-center and Previous/Next at opposite footer corners; do not confuse paging with Back.
- For headless Paper API builds whose ItemStack constructors require registry-backed ItemType, use test-only boundary shims and restore Material item-type suppliers and Bukkit.server after each test. Exercise real menu build/set/click methods; do not claim native metadata/NBT or client rendering from those shims. Verify final JAR in separate Paper harness before deployment.
- Preserve existing CRLF sources during narrow edits; use `git -c core.whitespace=cr-at-eol diff --check` rather than normalizing whole files merely to silence carriage-return warnings.

## Objective presentation optimization

- Replace per-refresh objective sorting with one ordinal-count pass; preserve insertion-order ties, lower-order entries after the current objective, and total count. Avoid static template caches without invalidation.
- Compare native BossBar title/progress before setter calls. Test-only BossBar proxies must implement getTitle/getProgress with native defaults (progress starts at 1); missing getter shims can make a correct optimization look broken. Count unchanged setter calls and verify changed progress still renders.
- Benchmark actual presentation method with thread allocated bytes and CPU time after warmup; retain baseline and optimized XML outside mutable build/test-results. Label synthetic objective count and invocation count; these are not whole-plugin heap or live MSPT savings. Validate exact final JAR on Paper before production readback.

## Dungeon removal and departure regressions

- Distinguish real death from EntityRemoveEvent removal and chunk UNLOAD. Removed wave mobs must decrement alive ownership and receive delayed, coalesced replacements without kill credit; replace only vanished count, not already killed mobs. Keep pending replacement visible to wave-clear logic and cancel through session tasks. Never replace ordinary unloads or cleanup removals. Test native remove, replacement death, real wave completion, and boss removal/death separately. Current recovery does not cover failed replacement providers or mobs merely wandering/unloading; report these ceilings honestly.
- Never issue a second teleport from PlayerChangedWorldEvent when player already reached a safe external world. Preserve actual destination and detach only participant. Test target coordinates, actual EssentialsSpawn namespaced command (`essentialsspawn:spawn`), and real Nether portal traversal. Keep survivor clients away from portal blocks; placing a portal under all party members correctly ends an empty instance and is not evidence of party-wide failure.
- Verify live artifact and failure reason before claiming repeated departure bug solved. After a user reports recurrence despite passing local tests, switch to authenticated live reproduction rather than repeating the same isolated assertions: capture the exact command/portal, session ID/state, remaining participant count, and physical survivor location before and after departure. If only one authorized bot identity is available, arrange one named user participant; verify invitation acceptance and shared-session admission before the exit test. Log bounded lifecycle reasons/remaining counts; absence of failure logs when no session ran proves nothing. Distinguish a fixed nested-teleport defect from an unreplicated whole-party failure, and never claim measured MSPT savings from a structural change alone.

## Dungeon terrain protection

- Protect exact WorldManager-managed disposable instances before checking OP/build-bypass permissions; allow template editing outside instances. Cover break/place, buckets, burn/ignite, piston/fluid movement, entity block changes, block/entity explosions and decoration removal. Deny terrain conversion without blanket-blocking weapon item use or puzzle pressure plates. Native Bukkit events cannot prevent vendor code directly calling setType; never promise all custom skills are sandboxed.
- Use existing world-to-sessions index for move/teleport/interact containment rather than scanning all sessions. Iterate all candidates within shared PUBLIC worlds, not only byWorld's last entry; test removal, empty regions and unchanged foreign-party isolation. Avoid prefix-based world ownership and new recurring protection loops.
- Require native Player.breakBlock checks for ordinary and OP clients plus explicit environmental event dispatch and native mob damage on isolated Paper. Distinguish scripted event checks from naturally generated explosions. Do not claim MSPT savings without live measurements.

## Dungeon navigation and lifecycle efficiency

- Hide body-follow waypoint holograms once the player reaches the checkpoint; keep them hidden during that checkpoint's combat objective, and reveal only when the next destination becomes actionable. Preserve per-player arrival for stragglers, clear old objective targets, and do not reactivate a reached waypoint merely because consecutive travel/combat objectives reference the same ID. Region-based arrival can complete before the waypoint coordinate, so respect the authoritative arrival region instead of distance alone.
- Give each completed objective one private sound and bounded particle burst for participants, not a recurring effect or fullscreen totem animation. Reuse existing action dispatch where possible; check whether particle actions support player-relative positions before promising effects around each participant.
- For this user's dungeon lifecycle, retain a fresh PRIVATE world per run; do not switch to pooled/public arenas without a new request. HuskClaims 1.5.11 supports `claims.unclaimable_worlds: ['rd_*']`; its world-load path returns before DB reads/creation for matching worlds. Verify installed wildcard semantics and preserve existing exclusions. Ultimate_BlockRegeneration 2.0.51 reloads region YAML unconditionally on WorldLoad; FancyHolograms 2.12.0 logging toggles suppress logs only. If native exclusion is absent, use narrow public Bukkit RegisteredListener wrappers for their WorldLoad/WorldUnload callbacks with exact WorldManager ownership, not name-prefix guesses; preserve priorities/cancellation, install idempotently before creation, and restore original registrations on shutdown. Never disable whole plugins or alter vendor JARs for per-instance exclusion. Verify real vendor callbacks on isolated Paper and fresh live entry/unload; distinguish lifecycle exclusion from disabling every gameplay listener.
- Test production vendor JAR Java requirements before starting fixtures: FancyHolograms 2.12.0 may require Java 25 even when RukhDungeon targets Java 21. Run exact vendor bytes with matching JRE; do not substitute another vendor version. Retain successful acceptance files before visual reruns, respect dungeon cooldown, and capture actual client sound/particle packets plus rendered combat-without-hologram evidence.
- Distinguish async template copying from synchronous world load and third-party WorldLoad listeners. Spawn-preparation milliseconds are not full world-create timing, and `Waiting 60s` is a timeout limit, not measured elapsed time when halt completes immediately. Prefer bounded persistent arena slots when maps can reset safely, but verify gate/block/chest/mob/task/claim isolation and reset completion before reuse; warm cloned worlds move load earlier and consume idle RAM rather than removing lifecycle cost.
- Diagnose repeated world-load registry errors from exact inherited config keys; an invalid `chunks.entity-per-chunk-save-limit` entry can log on every world load without proving dungeon CPU saturation. Fix the version-invalid key separately from performance optimization; never silence all load warnings.

## Private navigation and arrival checks

- User requires packet-only per-player dungeon holograms, not hidden server TextDisplay entities. RukhDungeon uses cached Mojang-mapped Paper packet bindings, native Entity.nextEntityId allocation, typed metadata accessors, and direct owner connection sends; no entity construction/world insertion. Send spawn+metadata once, movement/text only on changes, destroy on arrival/cleanup, and clear client cache on respawn. Test exact server version (1.21.11 verified), two-client privacy, zero world TextDisplays, packet cleanup, stationary zero sends, and rendered screenshots. Do not claim measured CPU savings from removing entity tracking alone. Native TextDisplay rules below apply only to legacy renderers, not current preferred implementation.

- Use native `TextDisplay` spawn consumers to set `visibleByDefault=false` before world insertion, then `Player.showEntity(plugin, display)` only for its owner. Describe this accurately as server-side entities with private visibility, not pure virtual packets. Use one shared main-thread refresh for stationary yaw, track display UUID ownership, and remove displays on missing session/player, world change, clear, and disable.
- Reconcile private display visibility after movement and on stationary refresh with `if (!owner.canSee(display)) owner.showEntity(plugin, display)`. Paper `ServerLevel.EntityCallbacks.onTrackingEnd` calls `CraftPlayer.onEntityRemove`, clearing UUID visibility grants; initial-spawn-only grants can disappear across tracking lifecycle changes. Keep `visibleByDefault=false`, reveal only owner, and test grant loss during teleport plus between refreshes without respawn or redundant healthy grants. Confirm exact live reset trigger separately from bytecode lifecycle evidence.
- Keep arrival-only regions out of forward-only stage indexing in both movement detection and fallback lookup. Prefer an explicit region objective over widening waypoint radius across a locked gate; bare force-complete region triggers cannot enforce current-objective prerequisites.
- Distinguish chest objective/key/table denials before atomic claims; repeated denied clicks must never burn claims. Add readable new-message fallbacks for existing message files and preserve genuine duplicate-claim feedback.

For Damage Indicator forks, load [references/damage-indicator-fork.md](references/damage-indicator-fork.md) for modern-only builds, low-resource testing, animation batching, toggle races and production migration.

## MythicMobs transient particle variables

- For Cuboss Slime minion `PlaceholderFloat` errors on `<caster.var.modelScaled>*0.3`, inspect live mob defaults and every setter before editing. A narrow `<caster.var.modelScaled|2>*0.3` fallback preserves normal configured scale and protects missing-variable particle spread for minions whose declared default is 2; do not apply that value to the boss default 1.5 or rewrite all math expressions.
- Test downloaded exact vendor JAR VariableIdentifier/VariableRegistry missing-variable behavior with cached Guava without launching Paper. `StringVariable` static initialization requires a running Mythic provider, so a registry-only check cannot establish full particle execution or populated-variable integration. Report that boundary; do not invent the missing variable's lifecycle cause from a matching warning alone.
- Back up exact YAML, reject concurrent remote edits, compare semantic non-target fields, read back uploaded bytes, require fresh native reload completion, and verify unchanged vendor JAR hash. Quiet post-reload logs do not prove boss spawn/despawn reproduction; request a normal encounter rather than mass-spawning or mutating player fights. Archived fixed warnings must not be presented as current failures.

## Live Spark baseline and ongoing monitoring

- Inspect `spark profiler info` before starting anything: Paper may already run its background sampler. Use `spark profiler open` for a temporary live viewer without cancelling another capture. Preserve profiler data and timestamped Pterodactyl resource samples locally. Installed command syntax can lag docs: if `spark health show` rejects `show`, use `spark health`.
- Label plugin-view percentages as sampled server-thread time, not machine CPU or active-tick shares; idle/park time and startup can dilute rankings. Inspect matching gameplay windows and stack callers before blaming a plugin. Zero samples does not prove zero cost, and a two-player idle session cannot establish busy-server capacity.
- Distinguish Spark JVM heap, heap committed/max, and Pterodactyl container memory; do not present their different denominators as a leak. Keep CPU normalization/source explicit. Use `minecraft:list` for unformatted authoritative player count, and verify actual backend membership plus fresh bot heartbeat.
- Leave existing profiler continuous and use a verified recurring read-only diagnostic job for requested ongoing monitoring; disclose its interval, bot idle-only scope, and lack of continuous AI gameplay. Check schedules before adding duplicates. Do not enable force-GC/heapdump, restart, or config changes for an audit. Treat repeated pack metadata errors and Mythic placeholder arithmetic warnings as repair candidates, not proven lag causes without stack evidence.

## Pitfalls

- Isolate snapshot-only release source lists when transfer workers share checkout; preserve exact JAR and verification outside mutable build outputs before releasing ownership. Compile cached official Vault API into dependency-only classes, never shade vendor classes into bridge JAR. Missing Vault linkage must remain inside optional snapshot boundary so web authentication still loads.

- Guard same-JVM file ownership before opening another channel to an already locked inode; closing a rejected duplicate descriptor can drop process-associated POSIX locks while Java still reports the original FileLock valid. Reserve canonical path before open, release on actual close, and test a separate-process challenger after a rejected duplicate constructor.
- Keep durable-success acknowledgement monotonic: replaying the exact stored receipt must preserve ACK and avoid a rewrite. Recovery must query provider receipts, never replay monetary mutation; bound HTTP retries per recovery cycle so outage recovery cannot monopolize the shared IO queue.

- Before exact-JAR combined acceptance, check copied backend relative imports, snapshot source hashes, and pin disposable DB identity with `SELECT @@port,@@datadir`. Afterward compare copied inputs with current sources and read back schema absence, closed loopback ports, and stopped fixture processes. Report unrelated concurrent source changes separately; they invalidate whole-web freeze claims, not unchanged copied-module evidence. Keep native Bukkit dispatch distinct from client-packet command coverage and manually seeded snapshots distinct from production publication.
- Validate the current ServicesManager economy provider name against real runtime evidence, not Vault startup log labels; EssentialsX may register `EssentialsX Economy` while Vault logs `Essentials Economy`. Exercise native PluginCommand dispatch through production HTTPS/HMAC wiring and rerun exact unmodified release bytes after correcting fixtures.
- Saturate signed-auth replay caches in tests before sending fresh revocation. Capacity rejection must clear positive authorization and advance its issuance high-water mark; otherwise a dropped logout preserves access or an older positive revives when entries expire. Keep unsigned/mismatched input unable to alter grants.
- Filter unrelated command labels before regex argument splitting. Benchmark the actual JAR-loaded handler with CPU time and allocation counters; keep case-insensitive/namespaced labels, cancellation, and password scrubbing regressions unchanged.
- Include cached Vault API provider JAR in isolated reflection probes when plugin fields reference Economy: getDeclaredField can resolve every declared field type even though optional Vault absence does not prevent normal auth startup. Do not shade Vault into production plugin to fix a probe dependency.
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
