# Damage Indicator fork and publication

## 1. Establish target and build

- Inspect upstream build modules and the intended server version before changing compatibility claims. When legacy NMS requires locally built Spigot artifacts, offer an explicit `modernOnly` path that excludes both legacy project includes and dependencies; do not silently call a modern artifact universal.
- Run `./gradlew build -PmodernOnly --no-daemon --max-workers=1` and preserve baseline output before editing. Use lightweight production-class checks with scheduler/entity/config/DB doubles, not a local Minecraft server. Distinguish boundary-double checks from native gameplay.

## 2. Optimize without changing gameplay

- Coalesce hologram animation into one main-thread task, cancel while idle, clean displays on disable, preserve lifetime/movement, and skip unchanged positions. Disable Folia declaration unless entity-owned scheduling is implemented.
- Deduplicate pending toggle DB loads with per-request identity. Invalidate on uncache/manual toggle and capture the owning database before queueing; otherwise late reads can overwrite explicit choices or populate a later login.
- Use literal replacement for literal placeholders and `charAt` instead of repeated `toCharArray` copies. Guard trailing ampersands; formatting must not crash on a final delimiter. Measure actual formatting method allocated bytes/CPU after warmup and label results synthetic rather than live TPS/MSPT savings.

## Ballistic packet indicators

- Use a reusable location and per-tick vertical velocity/gravity for jump-then-fall; positive gravity anchors the launch at hit-time target position, not the moving mob. Preserve zero-gravity legacy mode and bound invalid speed/duration. Document that target eye-height origin is not exact weapon impact raytrace and animation does not collide with terrain.
- Avoid confusing detached NMS ArmorStand packet builders with world-spawned entities. Set initial packet position before spawn, use setPos for detached movement, never insert into world, and reject unsupported entity-spawning fallback. Drop offline/cross-world viewers and end empty-audience tasks; select viewers before formatting/allocation. Test ascent/apex/descent, expiration, unchanged positions, empty audiences and idle cancellation separately; native startup alone is not visual motion proof.

- For random throw, sample bounded horizontal direction/speed once per spawn, not each tick; preserve vertical gravity and test nonzero bounded displacement plus direction variety. ArmorStand nametag backgrounds follow client settings; use packet-only detached TextDisplay with ARGB background 0 and style flags 0 when explicit transparent backdrop is required. Parse legacy text codes into components, preserve Nexo tokens, and distinguish metadata/alpha verification from actual live rendering. Never promise zero CPU/RAM.

## Custom numeric Nexo glyphs

- Use explicit `%glyph_value%` to emit contiguous textual digit tokens and one dot token for `.`/`,`; return before per-character formatting splits tokens. Preserve ordinary `%value%`. Scan all live glyph YAMLs before assigning PUA; never use raw Unicode as its own placeholder.
- Preserve shared baseline when cutting sprites; inspect JPEG background removal on dark/light previews. Draw missing punctuation explicitly as new artwork, not recovered source.
- Build multiversion pack from fresh generated Nexo ZIP and reapply only established compatibility deltas; preserve all fresh fonts/textures. Validate CRC, JSON, unique provider/codepoint, metrics and texture hashes. Static external pack URL remains unchanged until user uploads ZIP; generated pack is not public delivery. Do not start local Minecraft when user prohibits it.

## 3. Rebrand consistently

- For an explicitly requested full Noesantara rebrand, use `net.noesantara.damageindicator`, main class `NoeDamageIndicator`, plugin author `Noesantara`, and the requested version in both descriptor expansion and artifact filename. Preserve upstream copyright/license notices and attribution separately; changing plugin author must not erase original authorship.
- Update source paths, package/import declarations, reflection strings, scheduler class names, NMS lookup paths, shading destinations, plugin descriptor and test compilation paths together. Preserve external dependency coordinates and imports unless replacing those dependencies; they are not project-owned classes.
- Keep command aliases, permission nodes and SQLite schema stable unless explicitly changing them. Document that moving Java API packages breaks integrations importing upstream names.
- Write an identity regression before renaming: assert descriptor main/author/version, namespace of every project source, expected class entry in final JAR, and absence of old class paths. Exclude negative assertions from bulk replacements; otherwise the migration rewrites the test's forbidden tokens into desired tokens.
- Run a clean build after source moves so stale compiled classes cannot remain in the release JAR. Re-run behavior and packaged-identity checks; prior runtime success does not validate renamed reflective bindings.

## 4. Publish the fork

- Rewrite README around actual target, commands, migration, build/test commands, limitations and GPL attribution; remove inherited universal-compatibility or capacity claims not established for the fork.
- Remove upstream publication IDs, Modrinth sync/upload tasks and telemetry identifiers before pushing. Configure CI for the fork's build and regressions so a push cannot target upstream resources.
- Inspect publication candidates for credentials, private operational logs, backups, server endpoints and local paths. Keep those artifacts outside the source tree; preserve upstream history and copyright rather than rewriting authorship.
- Create the explicitly authorized public repository with `gh repo create OWNER/REPO --public --source . --remote origin --push`; retain the original remote as `upstream`. Publish the verified JAR via `gh release create` with an explicit target branch and honest runtime status.
- Read back repository visibility, branch commit and descriptor. Download the release asset and compare its SHA-256 with the local artifact before reporting publication complete. Do not call CI green without a completed run result.

## 5. Deploy only when authorized

- Confirm restart timing if players are online. Back up original JAR and complete data folder; refresh SQLite backup after confirmed stop because pre-stop copies can miss pending writes.
- Rename the data folder to fork identity while preserving exact custom glyph config, locales and database; disable the old JAR before activating staged, hash-verified bytes. Keep a stopped-state rollback path.
- Require fresh startup enable/Done, running state, native version/help aliases and active-JAR hash readback. Compare unrelated startup errors with pre-restart logs before blaming the fork. Keep visual combat verification separate from command/startup checks; never use production stress or mass spawning as a substitute.
