# Paper Threading and Verification

## Audit commands

Use before structural optimization:

```bash
grep -RInE 'runTaskAsynchronously|CompletableFuture\.(runAsync|supplyAsync)|ExecutorService|ScheduledExecutorService' src/main/java
grep -RInE 'getHighestBlockYAt|spawnEntity|teleport\(|callEvent|\.getBlock\(|getChunk\(' src/main/java
```

Inspect each overlap manually. Bukkit API touchpoints must run on Paper scheduler. A custom async event name does not make listener behavior thread-safe.

## Generator design

- Keep `Map<WorldName, Deque<Location>>` for each generation class, such as underground and surface.
- Use a small fixed pool. Refill one candidate per scheduled run, alternating pool/world when more than one world exists.
- Check empty pool with `pollFirst()`; return `null` cleanly if unavailable so caller can retry later.
- For generated-chunk-only mode, reject unloaded chunks before any expensive block/height lookup where API allows it.

## Performance checks

- Convert range checks from `distance` to `distanceSquared` after confirming same world.
- Skip move listener work unless block coordinate changed.
- Bound coordinate caches with a size and access-expiry policy. Cache negative lookups only when expiry is short and lifecycle invalidation is understood.

## Release gate

1. Project regression script passes.
2. `git diff --check` passes.
3. Gradle `clean shadowJar` passes with resolved dependencies.
4. Start on target Paper + Java runtime.
5. Smoke-test dynamic generation per configured world, mob wave spawn/despawn, command spawn, player enter protection, reload, and disable.
6. Only then publish JAR or claim full target support.
