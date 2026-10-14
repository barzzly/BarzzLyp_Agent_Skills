---
name: pterodactyl-server-management
description: Use when managing Pterodactyl game servers via SFTP or API.
version: 1.0.0
author: BarzzLy, Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [pterodactyl, minecraft, sftp, game-server, wings, api]
    category: productivity
---

# Pterodactyl Server Management (SFTP & Client API)

Honor final power state. For player wipes, see [database reset](references/player-data-reset.md). For schedule/task cloning, see [schedule replication](references/pterodactyl-schedule-replication.md). For dungeon WorldGuard/abilities, see [dungeon-worldguard scope](references/dungeon-worldguard-scope.md).

## Execution preference

- Work directly on active remote server; use backed-up edits and read-back checks. Avoid local Paper launches and mass-spawn tests. Mark untested items clearly.
- For dungeon mob substitutions or stat scaling, scope new MythicMobs IDs to the requested dungeon/server rather than editing shared vanilla overrides or existing custom mobs; back up live dungeon files, preserve wave/objective IDs and bosses, check every new spawn reference, reload MythicMobs before the dungeon plugin, then validate the dungeon and read back deployed files. Config validation does not prove in-game health or combat.
- Keep deployment critical path in the foreground. On takeover, inspect existing artifacts before changing files; interruption does not undo writes. For timed work, reserve verification time and distinguish a worker's exit from task completion.
- In reports, name target server and separate local, deployed YAML, and JAR state. Hash the remote JAR against release artifact; version alone is insufficient. Distinguish config validation from real gameplay.
- For persistent PUBLIC open-world dungeon setup, follow [world and spawner deployment](references/open-world-dungeon-deployment.md) and [read-only Anvil coordinate validation](references/anvil-readonly-spawn-validation.md). Restore original production power state after any temporary stop before reporting.
- Panel signed upload may place files at server root despite `directory=/plugins`; list root and verify signed download before renaming into `/plugins`. When replacing a JAR, stop first, rename old JAR to a non-.jar backup, then rename staged JAR into exact original filename; multi-file rename can fail on destination collision. Read back exact hashes and verify fresh startup. For persistent PUBLIC edits, disable template before changing YAML: `rd disable` serializes in-memory state and overwrites disk, including newly added worldwide/chests. After disable, rewrite desired YAML, reload, then enable on the new JAR. Old JAR's validation of worldwide chests will report out-of-bound errors until the new JAR starts.

- When the user stops a background mission and its reminder, inspect both worker processes and scheduled jobs, remove the matching report/reminder, and stop only still-running mission workers and test clients. Verify both surfaces afterward; stopping automation does not authorize stopping the production game server or reverting deployed JARs/configs. Report running workers separately from waiting schedules and unrelated preview servers.

## NoeAntiSpamChat toxic-list updates

- Inspect the active JAR SettingsLoader before editing YAML: NoeAntiSpamChat 1.0.0 reads root `abbreviations`, not `forbidden-words.abbreviations`. Alias values must normalize to an existing forbidden term or the loader silently ignores them. Preserve old terms/settings and deduplicate identical YAML mapping keys when fixing indentation.
- Prefer config-only updates and native `noeantispamchat:antispam reload`; back up config/JAR, compare remote config before writing, read back exact bytes, and require fresh reload success in the log. Verify unchanged JAR hash rather than replacing it unnecessarily.
- Test downloaded real JAR `SettingsLoader`, `TextNormalizer`, and `ToxicWordFilter` with Bukkit YamlConfiguration and existing Paper runtime libraries. Cover every supplied term, uppercase, leetspeak, phrases, separators, and safe words containing short aliases. Short terms are token-matched; direct terms of length >=4 also match compact substrings, so do not promise context-sensitive filtering or universal bypass resistance. Distinguish local engine tests from actual live player chat tests.

## Noesantara message branding

- Prefix NoeWeb player messages with `NoeWeb >> `: six-letter gradient from `#0038FF` to `#90E0F0`, gray separator, white body. Preserve original message text and transaction behavior; cover transfer outcomes/errors and webconnect replies, not only usage messages. Verify stripped text and real client rendering.

## Noesantara deposit interaction

- Create transfers on the website with amount and account-bound expiry. User wants Vault withdrawals processed automatically from the web without ingame commands, while deposits retain `/depositweb CODE` or `/web deposit CODE`. Keep prepare/claim, account ownership, expiry, balance, journal and duplicate fences intact. User requires automatic Vault WD while recipient is online OR offline; authenticate via owning web session/password and signed bridge, resolve exact known UUID using OfflinePlayer on main thread, and credit through Vault rather than raw eco give. Keep online signed-player authentication for deposits/manual commands and inactive durable-provider flow. Test real client disconnect before WD request, zero online players through settlement, exact credit and no duplicate; remove online gates from WD form, creation and discovery together. ECO RPG server itself must remain running.
- Parse whole-Money grouped inputs explicitly: `523,631`, `523.631`, and `523631` mean integer `523631`. Validate grouping before removing separators; reject mixed grouping, decimal fractions, exponent notation and malformed input. Use the same parser for preflight, POST amount and response comparison; backend still enforces integer bounds.
- Paginate automatic withdrawal discovery with a bounded stable cursor that advances past locally blocked/skipped owners. A fixed oldest-eight query can starve other players while uncertain journals remain locked. Never clear journals, refund, or replay mutations to unblock discovery; test more than eight owners and an unprocessable first page.
- Check current Vault balance on the main thread immediately before withdrawal from the game account, not only when generating the web request. Reject insufficient funds before invoking the money mutation, with clear player feedback and zero website credit. Preserve signed identity, claim, journal, expiry and idempotency checks around this shortcut.
- Test balance falling between request and confirmation, duplicate confirmation, foreign-owner and expired codes, and insufficient funds through the native command. Checking balance prevents overspending, not EssentialsX crash rollback.

## Noesantara minigames economy boundary

- Preserve existing EssentialsX/Vault/shop integration and real balances. Use unchanged EssentialsX for the explicitly approved best-effort bridge; do not infer permission to patch or replace the provider from a bridge feature request. Require separate scope, compatibility checks and isolated crash tests for any provider persistence change. A balance-persistence patch does not make ShopGUIPlus inventory delivery and money changes one atomic transaction.
- Without provider-owned durable receipts, never replay previous-boot monetary mutations or treat previous-boot unacknowledged SUCCESS/FAILED as certain. Quarantine ambiguous journals for reconciliation; backend must reject new certain settlements while disabled and retain unknown withdrawal reservations. In explicitly accepted best-effort mode, replaying a persisted exact result after restart is distinct from repeating the money mutation; retain UNKNOWN reservations and label provider rollback risk rather than claiming durable settlement.

## Noesantara NoeWebApi password login

- Place NoeWebApi on NoeRPG Paper/Bukkit, not Velocity. Reuse existing NoeWebAuth proxy companion only for signed JPremium identity grants; keep UUID/name/backend connection/challenge/expiry checks and HTTP off main thread.
- Use `/webconnect CODE password`: website issues five-character random code valid ten minutes, actual command sender must match requested nickname, user chooses persistent 5–64 ASCII non-whitespace password excluding case-insensitive substring `password`. Store Argon2id separately from monetary PIN; approval alone never grants browser session. Login takes nickname/password; setup/reset revokes prior sessions, devices, and competing challenges.
- Disable native `spigot.yml` `commands.log` before exposing password commands. Paper may log before PlayerCommandPreprocessEvent, so cancellation/redaction alone is insufficient. Keep proxy command logging disabled and audit spy plugins separately. Never print secrets in tests or logs.
- Include new challenge polling paths in existing GET throttles; serialize account password resets before challenge locks, index cleanup queries, and test concurrency beyond DB pool capacity. Release/fence plugin pending requests across disable/re-enable, including disconnected players.

## Noesantara minigames login preference (legacy PIN flow)

- Use one `/web approve CODE` command to approve browser verification; do not require a second `/web confirm`. Keep proxy-auth identity checks, browser-bound expiring challenge, exact login/reset purpose, PIN verification, replay controls, and disabled unsafe transfers intact. Explain that codes from other people grant browser access. Read Vault only on the server thread; perform HTTP off-thread and recheck current player/auth after preparation and before approval.
- Give minigames PIN fields independent accessible eye toggles, hidden by default, without changing values or submitting forms.

## Bridge release verification

- Test the exact final JAR against real Paper, the official economy provider, and isolated web backend/DB; fixture-only source corrections do not validate the release. Compare reviewed source hashes and runtime JAR hashes before deployment.
- Select the website build from its verified manifest, not a remembered staging directory; later UI changes can leave an older valid build beside the intended release. Verify staged source and asset hashes, back up live dist/environment/database, apply additive migrations, deploy that exact dist, then reload only the target PM2 app with `--update-env`.
- Verify public HTML references and downloaded asset hashes against deployed files, then check the session endpoint's fresh matching bridge capability. An enabled configuration flag alone does not prove plugin/backend connectivity. Probe native and namespaced command registration separately without transferring money, and explicitly distinguish these smoke checks from authenticated live transaction tests.
- Verify economy provider names from runtime rather than guessing: official EssentialsX 2.22.0 reports `EssentialsX Economy`.
- Persist newly created journal directory entries by forcing parent directories before readiness; test syscall ordering and injected fsync failures. File fsync alone cannot preserve a missing directory entry.
- Retain definitive late mutation results after timeouts. Upgrade only the same validated attempt from UNKNOWN to SUCCESS, persist before delivery, and require a fresh acknowledgment. Never infer a refund from a timeout.
- Reset browser secret fields and private async state on session identity changes; test expiry, replacement login, and stale completions in an actual browser, not only a bundling test.

## RukhDungeon overlapping points and stale editors

- Resolve every point at the selected world/block and open coordinate-filtered paginated PointListMenu when multiple matches exist; retain type/ID and include start/exit. Verify existing overlapping spawners through native selector and selected editor title without editing template.
- Use update-only Map.replace in editor replacement methods; missing IDs must not be resurrected by stale callbacks. Keep creation in explicit create paths.
- Detect identical loot items with differing entry settings before accepting grid movement; lock ambiguous grid with clear feedback while retaining Chances controls. Rejecting only at close can discard newly deposited items. Block bottom-inventory COLLECT_TO_CURSOR as well as shift-transfer. Preserve unchanged grid snapshots and refresh snapshots after successful saves.
- Allocate distinct loot navigation/control slots once and reuse for drawing/click routing; customized Save slots must not overlap hardcoded Next/Previous.

## RukhDungeon editor interaction regressions

- Resolve client-only point markers nearest-first on both RIGHT_CLICK_AIR and RIGHT_CLICK_BLOCK before creation-menu fallback; server can report terrain behind fake glass. Stop at real solid obstruction and bound reach. Test both event paths independently (reset captured menu), stale sessions, occlusion and unchanged point count; verify live point-menu title without mutating template.
- Preserve complete LootEntry on unchanged grid saves, including amount range, provider and serialized metadata. Display configured minAmount rather than embedded stack count; chance editor must store exact zero now that LootEntry supports it. Distinguish proxy unit checks from real serialized-item roundtrip coverage; identical-item matching after reorder remains ambiguous.

## RukhDungeon player browser design

- User wants `/rd menu` four rows with contrasting blue glass perimeter, gray interior, and dungeon heads filled LEFT TO RIGHT from first interior slot 10, then 11–16 and 19–25. Never center a singleton or fill center-out; 3/4 dungeons occupy 10–12/10–13. Screenshot's highlighted center means interior area, not centered ordering. Use custom player-head treasure-chest texture for Hollow, preserving entry validation/lore. Migrate live legacy navigation slots 45/49/53 to 27/31/35 alongside JAR, because existing YAML overrides bundled defaults. Verify actual graphical screenshot after chat-security toast disappears and stop temporary client/Xvfb afterward.

## RukhDungeon live template reload and boss healthbars

- Respect the user's choice to let an active dungeon run finish before maintenance. A later generic “continue” does not authorize stopping that run. Keep pending edits separate from deployed fixes, and never claim a waiting worker has applied them. Recheck exact target sessions before reload; unrelated idle arena sessions need not be interrupted.

- In-memory dungeon templates are pinned by active sessions during `/rd reload`. Because ARENA mode sessions run continuously in the background, `/rd reload` skips reloading an active arena template from disk. Furthermore, running `rd disable <dungeon>` invokes `dungeon.save()`, which overwrites on-disk YAML with the in-memory state if disk edits were uploaded prior to disabling. To hot-reload an arena template without restarting the server or interrupting players in other instances: (1) run `rd disable <dungeon>`, (2) clean the idle session with `rd admin clean <sessionId>`, (3) upload the modified YAML via SFTP, (4) run `rd reload` (unpinned template loads freshly from disk), and (5) run `rd enable <dungeon>` (saves and re-registers the new configuration).
- When bosses utilize custom MythicMobs floating display-entity healthbars (such as `NOE_HP`), disable Bukkit BossBars in `objectives.yml` via `boss-triggers.<id>.boss-bar: false` to eliminate duplicate health UI at the top of the player's screen.

## NoeDungeon deployment and namespace migration

- NoeRPG uses active `plugins/NoeDungeon-1.1.0.jar` and `plugins/NoeDungeon/`; verify current state rather than assuming historical RukhDungeon paths. When old JAR is unexpectedly absent and server offline, confirm maintenance ownership before starting. Preserve inactive source folder locally and verify exact bytes before removing it remotely.
- Before namespace migration, snapshot complete plugin data and every world/playerdata/*.dat, scan NBT structurally for old PDC keys, and query LuckPerms user/group permission tables read-only for old nodes. Rename only exact PDC namespace keys with collision rejection and compare reverse-transformed NBT to original; never byte-replace compressed NBT. Preserve cooldowns, rewards, map paths and unrelated tags. Inspect companion plugin descriptors/class references separately.
- Preserve explicit `HOLLOW_` world-prefix overrides. When changing default `rd_` to `nd_`, add `nd_*` to HuskClaims exclusions without deleting existing patterns. NoeRPG Skript's `/dungeon` convenience menu delegates to `nd menu`; this shortcut is separate from NoeDungeon's `/noedungeon` and `/nd` dispatcher.
- Require exact post-start file hashes, plugin author/version, registered dispatcher, dungeon validator and fresh enabled/Done markers. Existing Nexo armor metadata/trim errors and a MythicLib dependency-cycle warning can coexist with successful NoeDungeon enable; compare prior boot and report separately. `dungeon1` missing exit-location warning is not a clean validator result even when validation passes. Console player-only response verifies registration, not inbox GUI gameplay.

## RukhDungeon inventory layout deployment

- Audit all 17 bundled menu YAMLs plus Java fallback positions; existing `plugins/RukhDungeon/menu/*.yml` override new JAR defaults, so deploy minimal layout changes alongside JAR. Preserve labels, actions, permissions, item metadata and dungeon data.
- Use center close column 4 and back column 7 (zero-based), leaving columns 5–6 clear; align supporting actions at column 1 where appropriate. Fill partial player/content lists left-to-right, never centered; preserve editable loot slots 0–44, save boundaries, and explicit custom slot arrays.
- For invite-player screenshots, locate the actual head slot rather than the floating tooltip. Start bordered invite lists at slot 10 (first interior cell of row two), continue through 16, then 19–25; a six-row inventory has 28 interior cells. Inspect live `PartyInviteMenu` bytecode with `javap -c -p -classpath <live.jar> <class>` alongside YAML before editing: hardcoded `set(i - from, ...)` ignores layout settings and overwrites the top border. Map page-local index with `10 + (index / 7) * 9 + index % 7` and cap page size at 28 together, preserving invite validation and navigation.
- Correct layout tests that encode the old wrong positions before patching production code; require RED on actual menu build/action slots. Cover a partial row crossing, a full 28-entry page, entry 29 on the next page, and preserved border/navigation. Separate passing headless tests and packaged-artifact checks from live deployment and visual proof.
- Test legacy Gate/Region `rows: 3`, `close.slot: 26`: centering eight choices would overwrite eighth choice at 26. Keep sequential slots 18–25 when navigation shares picker row; only center when close has separate row. Exercise custom close collision too.
- Verify all menu constructors on isolated loopback Paper and actual client screenshots; shorten overlong list titles, keep instructions in lore. Check Back destinations and native loot save roundtrip. Keep test fixture plugin off production. Separate local visual proof from live JAR/config hash readback and fresh startup logs.

For Hollow chest/material/boss edits, read [Hollow content maintenance](references/hollow-content-maintenance.md) for cached API reads, map marker diffs, native loot pools and verification boundaries.

## Full-map dungeon expansion

- Audit every spawn point's activation binding before bulk mob replacement or chest relocation. Points with no objective, no explicit wave, and no membership in any wave auto-activate on entry; converting an overlooked editor/test point into a custom mob preserves that unwanted spawn. Match suspect coordinates to removed chest locations, remove only confirmed obsolete points, and assert every retained point has an intended activation path before release.
- Inventory actual block entities in fresh region snapshots before assigning loot; distinguish constructed footprint from pregenerated terrain. Register existing chest coordinates without rewriting template map, and separate nonempty loot-service checks from physical player reach and native clicks.
- Include partial collision surfaces and ladder transitions in route analysis. A bottom slab's occupied foot block is not passable even though its upper surface is walkable; air-only graphs falsely disconnect treasure platforms. Explicitly report parkour/high-chest gaps rather than calling a connected main-route graph complete coverage.
- Extend from fresh deployed YAML and exact live JAR, preserving installed Mythic IDs, gate dependencies and per-player loot claims. Validate progression in isolated runtime before native reload; scripted teleport/kill checks do not establish survival balance or native navigation.

## Dungeon map-driven progression checks

- Keep each progression gate closed until its area's objective completes. Read live `initial-state`, `required-objective`, and matching `OPEN_GATE` actions together; verify the runtime barrier blocks traversal before completion and opens afterward. Distinguish decorative map entrances from plugin-created barriers in disposable instances, because template screenshots cannot establish runtime locking.
- For gate screenshot requests, capture the active barrier before objective completion and the same viewpoint after opening. Inspect images before sending, label local-copy versus live-server evidence, and do not substitute an architectural entrance, bossbar, or filename containing 'gate' for a visible locked gate. If only scenery images exist, state that the requested locked-state screenshot is missing.

- Survey a copy of actual template with Paper matching its DataVersion; older Paper can replace unsupported blocks with AIR and invalidate route findings. Retain untouched downloads and include slab/carpet collision surfaces in walk graphs. Shape disposable gate cuboids around existing AIR passages; never overwrite map artwork to fit guessed coordinates.
- Keep gate regions separate from forward-only gameplay stage indices while retaining ENTER_REGION trigger dispatch. Otherwise traversing multiple gate cuboids can trap respawned players behind an earlier region. Test both index lookup and actual return traversal.
- Use full-block gate material when projectile gaps matter; bars admit pearls. Test survival teleport causes against closed gates and preserve trusted lifecycle teleports. Paper 1.21.11 exposes chorus behavior as CONSUMABLE_EFFECT; compile-compatible enum-name check may be needed when supporting older API.
- Probe native and namespaced dungeon commands through authenticated live player. Existing DeluxeMenus can own /dungeon and reject subcommands; preserve menu and use verified /rd alias in dungeon instructions rather than hijacking registration.
- Distinguish scripted Bukkit lifecycle assertions from native combat and inventory transfer. Keep per-run assertion files, validate counts programmatically, and test separate real clients for party clone isolation/personal claims. Native leave must detach any participant independently, including non-leaders; verify both command and world-change paths rather than inferring them from death/disconnect tests.
- Preserve CRLF files during scoped edits; run git -c core.whitespace=cr-at-eol diff --check when plain checks flag retained carriage returns. Do not normalize unrelated uncommitted patches.

## Objective mob aliases

- Configure per-dungeon `mob-names.<PROVIDER>.<exact mob ID>` in dungeon `config.yml`; values may include a short prefix such as `[Boss]`. Apply aliases only to wave/boss objective presentation, preserving provider+ID grouping, actual spawn IDs, counters and entity nametags. Blank/formatted-empty aliases fall back; persistence must survive editor save and repository reload.
- Before isolated JAR tests, enumerate plugin descriptors and keep exactly one enabled JAR for each plugin name. Different filenames with duplicate RukhDungeon descriptors can load stale bytecode and cause misleading NoSuchMethodError despite correct release hashes.

## Objective bossbar and arrow verification

- Keep objective presentation separate from optional timer bossbar; reuse shared timer tick, actual per-session death counts, and cleanup. Never infer kills from delayed or failed spawns. Restrict wave labels to wave objectives; preserve ordinary objective counters and boss/travel instructions.
- Allow the shared 20-tick refresh before asserting first objective bar: SessionService initializes timer before objectives.begin. Verify real client boss_bar add/update/remove packets and local rendered screenshots separately; resource-pack acknowledgments are not render proof.
- User now requires packet-only body-follow holograms, not hidden server entities. Verify owner/observer packet isolation, no server TextDisplay creation, changed-only updates, respawn reset and cleanup; test exact Paper version and live spawn/text/destroy receipts. Verify personal body-follow navigation with owner and nearby observer clients: readable TextDisplay arrow/label/distance, stationary yaw changes, movement, and cleanup. Current user preference is a hologram following the body, not particles or actionbar. Native hidden-by-default TextDisplay uses server entities and private visibility packets; do not call it pure client-only packet rendering. Recheck owner visibility after movement because Paper tracking end can discard showEntity grants while the display remains valid. Preserve timer in bossbar.
- Test gate-arrival objectives across the full exit passage rather than only the central waypoint; keep arrival regions out of forward-only stage indices and require current objective dependencies. Distinguish locked-objective chest denial from actual prior claim; repeated early clicks must never consume claims. Label scripted Paper events separately from native walking/combat.

## Lightweight dungeon gate effects

- Style gate announcement with MiniMessage `<bold><gradient:#0038FF:#90E0F0>GERBANG TERBUKA</gradient></bold>`; user rejected flat aqua. Preserve native title timing and existing shake/sounds. Verify real rendered client before release; MiniMessage gradient is per-character horizontal, not a custom vertical shader.

- Group component gates by session and required objective, then announce only after their queued AIR fills finish. Keep initial OPEN states, altar gates without objective dependencies, duplicate opens and closed/locked gates silent. Preserve shared per-tick block budget.
- Use one short title, two low-pitch native sounds and three cosmetic `Player.playHurtAnimation` pulses (0/4/8 ticks) for weight without entities, damage, teleportation or permanent animation loops. Recheck membership/physical containment and running state for delayed pulses; own them through session TaskManager. Player hurt-camera settings can reduce or disable perceived shake.
- Verify actual title/timing/hurt packets per grouped gate, six existing objective totem bursts per complete dungeon, and actual rendered title. Separate local packet/visual checks from live JAR hash/fresh-start verification; bounded packet counts are not a measured production MSPT benchmark.

## Permission refresh diagnosis

- AuraSkills 2.3.12 caches multiplier permissions in `BukkitLuckPermsHook` and listens to NodeAdd/NodeRemove, not all bulk-clear/context refresh paths. Reproduce on one non-OP disposable online user: inherit a disposable group with `auraskills.multiplier.37`, prime `%auraskills_multiplier%` at 1.37, clear only that group's permissions, then compare LP undefined with stale Aura 1.37. Never clear real player/rank permissions. Native mitigation is `hooks.LuckPerms.use_permission_cache: false`; fallback reads effective Bukkit permissions instead. Require after-change same-session return to 1 without relog. This proves the multiplier cache bug, not every shop/mining permission symptom.
- AuraSkills 2.3.12 `skills reload` does not reconstruct its LuckPerms hook; the cache flag is constructor-final, so restart the backend safely to activate it. LuckPerms 5.5.85 similarly schedules `sync-minutes` only at enable; reloadconfig alone does not start a previously disabled sync timer. Do not add broad polling or change already-working SQL messaging without evidence.

- For permissions that work only after relog, inspect live `lp info` messaging/storage plus exact affected permission and plugin before changing sync configuration. SQL messaging enabled and DB connected do not prove every notification was received; command audit logs prove a grant, not consuming-plugin refresh. Distinguish local async command completion, cross-server propagation, context/negative nodes and plugin-owned cached benefits. UBR 2.0.51 checks `Player.hasPermission` during block breaking, so do not label UBR a join-only permission cache. Reproduce with the affected online player and actual failing action before claiming a cause or fix.

## ExcellentCrates preview placeholders

- Compare live `plugins/ExcellentCrates/previews/default.yml` with installed JAR constants for literal tooltip tokens. ExcellentCrates 6.6.1 uses `%reward_name%` and `%reward_description%`, not legacy `%reward_preview_name%` and `%reward_preview_lore%`. This is internal placeholder migration, not evidence of a resource-pack or PlaceholderAPI fault. When authorized, back up and change only confirmed stale tokens; preserve rewards, chances and layout. Read back config and verify native reload logs; client rendering needs a live view.

## MMOItems kit lore and category icons

- Give this user's kit entries short English flavor lore matching kit theme and visible item form, with existing three-stop MiniMessage palette and gradient `displayed-type` like sword.yml. Keep lore cosmetic: do not imply new abilities, crate unlocks, equipped flight or stat bonuses. Preserve enchants, material/CMD, identifiers, armor and Nexo originals.
- Set category icons using `display: MATERIAL:CMD` in item-types.yml. Installed MMOUtils.readIcon splits on colon and calls setCustomModelData; an extra sibling custom-model-data field is not consumed there. Choose a real representative model per kit and verify exact source material/CMD pair. Distinct pairs prove configuration identity, not client rendering; disclose visual verification gaps.

## MMOItems kit enchantment updates

- Scope kit enchants to existing `kit_*.yml`; preserve ARMOR and Nexo source files. Match enchant eligibility to actual Bukkit material, not model names (a spear model on NETHERITE_SWORD uses sword enchants). User requests level V including Mending; skip non-enchantable COAL/EMERALD/BLAZE_ROD cosmetic/key entries. Avoid incompatible enchant pairs and unsafe Quick Charge V; disclose exclusions. Do not invent stat boosts or migrate already-issued items via revisions unless requested.
- Use native `base.enchants` mapping with modern lowercase Minecraft keys; installed Enchants.getEnchant resolves NamespacedKey before legacy names, and numeric formulas retain requested unsafe levels. Verify all source fields except enchants unchanged, every applied level exact, fresh reload without kit errors, and old missing-skill warnings separately. Config reload verification does not prove already-issued items updated or native combat/equip behavior.

## MMOItems Nexo source boundary

- For ECORPG kit grouping, leave existing ARMOR definitions and Nexo armor bindings untouched. User wants one kit-named type for weapons/tools/cosmetics/keys, not per-weapon subtypes. Final scope excludes chest (including opening variants) and backpacks, which stay Nexo-only. User explicitly accepts material/CMD model copies without a bridge; give each kit-themed item a readable three-stop MiniMessage gradient like sword.yml, preserving source material plus CMD together. Do not invent stats, crate-key bindings or cosmetic equip behavior.
- Inspect installed provider bytecode before inventing `material: nexo:<id>`: MMOItems 6.10.1 MaterialStat uses Bukkit Material.valueOf and ItemStackBuilder constructs a fresh vanilla ItemStack. Its NexoCompatibility covers crafting inputs/outputs, not importing full Nexo item metadata. Nexo `mmoitem` works in the opposite direction. Material/CMD copies alone lose Nexo PDC identity and furniture behavior; flat custom-nbt paths do not create BukkitValues compounds. Ask before adding a bridge plugin rather than silently deploying a cosmetic-only substitute.

- Supply `unident-item` with at least a name on every new custom type. Installed MMOItems 6.10.1 constructs UnidentifiedItem directly from that section; parent inheritance does not fill a missing section and reload fails `Config cannot be null`. Require a fresh successful type count and native item listings matching every manifest ID, not only YAML parsing or a generic reload-success line. Keep old populated definitions even if currently unregistered; archive/delete only empty unregistered legacy files. Distinguish source/model parity and native registry verification from live visual or combat tests.

## MMOItems kit type planning

- Scope this user's Nexo Kits work to ECORPG once confirmed; do not inspect sibling servers merely because a command/plugin name differs. Verify exact target before presenting inventory results.
- Inspect kit item materials and existing `mmoitem` bindings before creating one custom type per kit. MMOItems Type has one parent, inherited interaction provider, and one modifier source; a mixed armor/weapon/tool kit cannot preserve all native behaviors merely by sharing a kit-named type. Resolve armor-only versus per-category subtype scope before migration. Preserve issued-item type IDs and dependent references; `disable-removed-items` makes deleting old definitions risky. Empty legacy YAML files are not proof of registered unused types.

## MMOItems dodge balance changes

- Interpret “reduce by 80%” as old value multiplied by 0.2, not subtracting 80 percentage points. Inspect NumericStatFormula and `additive-spread-formula`: with relative spread, scale base while retaining spread/max-spread to scale the entire distribution; additive spread needs different treatment. Preserve unrelated stats and revisions. Verify exact remote bytes and native `mmoitems:mmoitems reload`; config reload does not prove already-issued or socketed gems migrated.
- Separate dodge providers from consumers and labels: MMOItems gems/set bonuses supply stats, MythicLib mitigation rolls consume them and enforce caps, AdvancedEnchantments Dodge cancels attacks independently, and Skript/gkits may grant that enchant. Glyph/lore matches and named Evasive Shot skills are not additional random dodge bonuses. Report excluded compiled code, DB/player items and asset/state subtrees in cross-plugin config scans.

For NoeSellwand normal/premium/charge menu migration, read [Sellwand CoinShop](references/sellwand-coinshop.md).

## Pickaxe shop and regeneration tool audits

- Compare every DeluxeMenus purchase command against UBR `items.yml`, decoding JSON display/lore before comparison and checking material, Fortune tier, displayed price, balance gate and charged amount. Use the region's materials file when `Global_Settings: false`; global `materials.yml` can have empty Req_Tools while the active region enforces custom tools.
- Audit `Req_Tools` and `Needs_Permission` separately. UBR 2.0.51 checks the tool and then player permission independently; correct pickaxe metadata does not grant ore access. Fortune variants without permission grants can fail for players who skipped the base-tier purchase. Report this condition without assuming every player's LuckPerms grants. Do not alter items or player permissions during a read-only consistency check.

- When fixing shop permissions, grant the full allowed ore-permission set on every successful tier/variant purchase, not only newly unlocked ores; preserve cost, mining threshold, cooldown and tool gates. Do not retroactively grant permissions to all players without ownership evidence.
- UBR 2.0.51 `Req_Tool` compares display name and entire lore list exactly, and only checks enchantment types (not levels). Cleaning existing tool lore can invalidate already-issued items. Preserve old serialized variants under distinct legacy IDs and add those IDs only to the original accepted block lists; keep purchase commands on cleaned IDs. This preserves old items without weakening name/lore checks.
- DeluxeMenus 1.14.1 enchant previews use `enchantments: ['DIG_SPEED;1', 'LOOT_BONUS_BLOCKS;1', 'MENDING;1', 'DURABILITY;3']` with actual per-item levels. Loader uses Bukkit `Enchantment.getByName`, not namespaced modern IDs. Require separate `dm reload <menu>` success for each modified menu and native `regen reload`; read back exact uploaded bytes and preserve vendor JAR hashes. Distinguish reload/config verification from actual player purchase/mining and rendered preview tests.

## Historical Pikeman sound targeting

- When the user describes a bubbling sound on spear carriers, inspect shared `PikeHitDamage` before assuming Flail Knight's `entity.witch.throw` timer. Pikeman red/blue hit damage uses `item.wolf_armor.damage`; mute only that sound mechanic when targeting spear-hit noise, preserving damage/bleed, particles, other packs and other sounds. Distinguish verified config removal/native reload from user-confirmed acoustic match; onomatopoeia alone does not prove the exact sound ID.

## MythicMobs reload warnings

- Wrap placeholder arithmetic delay inside attributes (`delay{ticks="<random.14to24>*10"}`); bare `delay <random.14to24>*10` can enter health-conditional parsing and throw NumberFormatException. Verify exact deployed Mythic version through local reload before live change.
- For animation increments whose initialized frame is 1, use documented numeric fallback `<caster.var.iteration|1>+1` when missing caster variables produce UNDEFINED arithmetic. Reproduce missing-variable aura locally first; preserve normal initialized increments and do not claim fallback explains why caster state disappeared. Validate live post-reload window; quiet logs alone do not prove every visual animation.
- Distinguish bundled example dialog callbacks that reference nonexistent skills from real quests. Comment only nonexistent example bindings with backups, keeping dialog definitions. Deprecated Placeholder API warnings from MMO integrations/MCPets need provider updates, not disabled logging; absence after another reload may be warning deduplication.

## Vanilla dungeon and MMOItems entry checks

- Inspect the exact source RukhDungeon JAR before cross-version deployment: old builds can lack `REACH_REGION` and use obsolete `net.Indyuce.mmoitems.api.item.NBTItem`; current MMOItems identity comes from `io.lumine.mythic.lib.api.item.NBTItem` in MythicLib. Require fresh integration-enabled logs, not a successful YAML validator alone. Do not transplant newer packet holograms onto 1.21.1 without compatibility tests: `PositionMoveRotation` and teleport constructors differ. Check world `level.dat` AND region chunk DataVersion rather than relying on the server version string.

- Match isolated MythicMobs `mobs/VanillaMobs.yml` to live before asserting vanilla identity; generated example overrides can register ordinary WITHER_SKELETON as Mythic and produce false failures. Do not change production overrides merely to satisfy tests.
- Test selected existing MMOItems key through real provider build/matches, plain-material rejection, no-key entry denial and exact one-item consumption. Clear only disposable test-player entry throttle between immediate negative/positive lifecycle probes; never weaken production throttling. Keep final boss definition byte-equivalent semantically when replacing other encounters, and distinguish scripted kills from survival balance.

## MythicMobs dungeon configuration acceptance

- For modest dungeon length increases, add sequential reinforcement waves at verified spawn cells rather than raising simultaneous caps or inventing new map routes. Move COMPLETE_OBJECTIVE exclusively to the last wave; assert gates and boss remain locked through added waves. Preserve native pack IDs, map, loot and cosmetic JAR. Report extra wave/mob counts, not an unmeasured minutes estimate.

- Reuse installed pack internal IDs and inspect their skills before assigning dungeon spawns; premium pack models may require ModelEngine and delayed summons remain outside the current dungeon spawn-permission scope. Verify actual Mythic active-mob registry, wave counts, boss death progression and cleanup on an isolated copy with the exact deployed JARs. Scripted setHealth(0) tests do not prove native combat balance or every boss skill.
- For gate material changes, preserve gate cuboids, objective dependencies and altar material. Check every gate cell closed and open locally, then read live block packets separately from YAML readback. Config-only reload needs no JAR replacement; active sessions pin previous templates until ending.
- Use `execute as <test-player> at @s run tp @s ...` for disposable local-world screenshots; bare console `tp <player> ...` can resolve coordinates in the console default world and terminate the instance. Require actual changed position after remote console dispatch; accepted API calls may not move the player. Label local visuals and live packet checks separately.

## Dungeon flight and god restrictions

- Exclude disabled templates from the start-world ability predicate. An unfinished disabled dungeon whose start points to ordinary `world` can otherwise cancel Essentials fly/god across that entire world. Keep exact WorldManager-owned instances restricted independently of template enablement; never use loose prefixes or exit/lobby locations. Test disabled, enabled and unrelated worlds. Shared active-template worlds remain world-scoped under this policy.
- Paper 1.21.1 lacks `PositionMoveRotation`; packet-only hologram movement needs the legacy ClientboundTeleportEntityPacket FriendlyByteBuf decoder (VarInt ID, XYZ doubles, yaw/pitch bytes, boolean). Release Netty buffers in finally and preserve modern constructor path. Test full reflection initialization, native ID allocation and decoded coordinates on exact vendor classes without starting a server. Resolve libraries from matching Paperclip `META-INF/libraries.list`, not all cached JARs: mixed authlib versions cause false NoSuchMethodError. These checks do not prove full gameplay on 1.21.1.

- Block Essentials FlyStatusChangeEvent/GodStatusChangeEvent using `getAffected().getBase()`, not controller; this covers console/other-player grants and aliases. Clear existing flight and raw Essentials god state on entry/join and with one shared bounded sweep. Preserve outside-world behavior and item enchant metadata; state disabled on entry need not auto-enable on exit.
- For AdvancedEnchantments Wings, register `AEAPI.forceEnchantToTriggerEvent("wings")` before listening to EnchantActivateEvent, and add world conditions only to Wings. Copy live groups.yml into isolated runtime: missing MYSTIC group prevents Wings loading and invalidates tests. Native command dispatch from another command can queue until callback returns; execute PluginCommand directly or assert next tick instead of assuming immediate effects.
- Test template world and generated managed instances; per-dungeon `worlds.instance-prefix: HOLLOW_` changes new worlds while `display.name: DungeonHollow` leaves internal dungeon ID/data intact. Distinguish rendered/native equip tests from synthetic activation-event assertions. Explicit spectator flight exemption is for admin inspection, not Essentials/Wings gameplay bypass.

## Dungeon friendly-fire protection

- Reject player-owned attacks within physical dungeon containment, including same-party melee, projectile shooters, tameable owners and attributed magic; cross-session isolation alone still permits friendly fire. Set native PVP false for managed instance WorldInit, without changing outside-world combat.
- Bind optional MythicMobs MythicDamageEvent and MythicLib AttackEvent before provider health mutation; Bukkit damage cancellation alone is insufficient for skill paths. Resolve reflection accessors once and fail visibly on incompatible installed APIs. Preserve MythicLib SUPPORT interaction checks while rejecting OFFENSE checks.
- Test two real clients, native melee health, an actual Mythic damage skill with ignoreArmor, provider cancellation events, and native damage against an owned dungeon mob. Synthetic EntityDamageByEntityEvent dispatch may be cancelled by MythicLib because it lacks native attack context; isolate guard unit assertions and separately verify real mob health loss rather than weakening production protection. These checks do not prove every custom weapon script, especially direct setHealth mechanics.
- Inspect the complete startup log for test plugin dependency cycles; Paper can reach Done after silently excluding a fixture from the registered plugin list. Isolate only unnecessary local plugins to break fixture cycles, never alter production dependencies as a test workaround.

## Dungeon individual elimination and paginated menus

- Death/disconnect must end only that participant, including leader; keep survivor waves/timer running. Detach player index before teleport callbacks, record failure/deaths/cooldown once, remove private navigation and all bossbars, and exclude eliminated players from completion rewards. Stop/clean when no participants remain; PREPARING still aborts admission safely.
- Persist a safe pending exit on the player before detaching; recover on respawn/join and reject entry until recovery completes. Verify three real clients: leader death, member disconnect/reconnect, survivor completion, last-player death and quit cleanup. Do not claim process-crash durability from ordinary reconnect tests. Explicit `/rd leave` (including non-leaders) and world departure must use the same individual elimination path as death/disconnect. Never call whole-run stop from a participant exit or fire legacy session-wide PLAYER_LEAVE actions there. Preserve explicit admin stop and PREPARING admission abort. Reproduce both native command dispatch and real cross-world teleport against the old JAR before patching; verify leader-first/member-first exit, duplicate exit, surviving wave/timer/completion, excluded leaver rewards, and last-participant cleanup against the exact release JAR.
- Fill every paginated menu's content left-to-right from its first available slot, then the next row; never center partial pages. Interior party/point grids start at slot 10; full-width lists start at 0; gate picker starts at 18. Preserve custom slot order and non-list controls. Verify last-page item identity and real screenshot after clicking Next.
- Party landing removes Close and places Create Party at bottom-center; Previous/Next occupy left/right footer corners. Paginate session admin, party browser, point lists, loot lists/select/chances, gate picker, and editable loot grid; preserve slot 0–44 editable boundary. Move loot picker clear-binding away from Previous. Update live menu YAML overrides along with defaults, not JAR alone.
- Editable loot pages must save only their loaded slice and preserve unseen/non-display entries plus chance/weight/unique metadata; fail without replacement on serialization failure. Exercise real item serialization, page-two edits, back/forward, and close against a table exceeding 45 entries. Keep per-page content identity distinct from visual slot index.

## Dungeon lifecycle regression checks

- Scope combat isolation to physical session containment, not registration alone: PRIVATE sessions register before async copying, and completed sessions stay indexed during evacuation. Check players, tameable mobs, projectiles, PREPARING and post-exit states so dungeon entry cannot grant outside-world immunity.
- Exclude wave-listed spawn points from automatic objective spawning even when their explicit `waveId` is null. Establish wave ownership before first spawn; otherwise existing mobs can fill the cap without wave tags and their deaths never complete a zero-timeout wave.

## Dungeon spawn and temporary-world checks

- Treat editor point glass as client-only preview, not proof that template blocks changed. For generated PRIVATE worlds, clear exact persisted point cells before teleport, gates and spawn activation; preserve source template, unmarked blocks, floor below, external-world exits and existing loot chests. Clear stone/legacy glass at loot points so normal chest initialization runs. Test actual SessionService start on copied Paper world, exact mob Y and source reload; never clear all matching glass by material or mutate shared PUBLIC arenas without restoration design.

- Inspect persisted `amount` and `max-alive` together: runtime fills `min(amount, maxAlive)`, so raising Amount alone can leave the default cap at one. Test actual menu clicks from 1 to 10, raise cap with upward Amount edits, and retain explicit lower-cap edits. Back up live spawner and change only requested fields.
- Scope spawn restrictions to WorldManager-owned instances, including PREPARING, not arbitrary `rd_` prefixes or whole template worlds. Set mob gamerule at WorldInit and cancel non-dungeon CreatureSpawnEvent sources; saved template mobs require EntitiesLoadEvent cleanup, preserving decorations and owned entities.
- Provider spawn events precede post-return PDC ownership. Wrap ordinary and boss provider calls in world-scoped synchronous permission with finally cleanup; do not allow every CUSTOM spawn. Delayed Mythic skill summons fall outside this scope and need explicit ownership integration if requested. Verify real Paper HARD spawns, cap, six non-dungeon sources, saved-template entities, and preserved armor stands.
- Trace Multiverse missing-world spam to its caller. TAB animations using `%multiverse-core_alias%` query unregistered disposable worlds repeatedly. Prefer native `%world%` with explicit output replacements preserving existing aliases; do not import every ephemeral world into persistent Multiverse config or silence all warnings. Verify YAML readback and TAB reload; absence of warnings with no player inside an instance is not a live gameplay test.

## Live Bot Acceptance Rules

- Distinguish connection, authenticated gameplay, chat capture, scripted commands, and AI conversation before promising capabilities. When the user asks an agent to join and follow player chat, do not silently substitute a regex command bot for an AI participant. Explicitly disclose a reduced scope; claim AI participation only after a real model-backed response and safe action are verified in-game.
- Verify each claimed capability separately: backend connection in server logs, designated player's message captured with identity, outgoing reply delivered, and requested command's actual effect. A running background process proves none of these by itself.
- Keep chat authority limited to the user-designated player and gameplay scope. Require explicit approval through the trusted control channel for destructive, privilege, security, or host actions; never feed player text into unrestricted shell execution.
- Preserve performance-test scope when the user adds live interaction: save samples and report measured metrics or mark the assessment incomplete. A low ping or successful join is not proof of healthy TPS/MSPT or capacity.
- State the active bot's lifetime and what continues autonomously after the reply. A logged message is not continuous AI review; an allowlist is not natural-language understanding.

For ordered setup, authentication, resource-pack handling, and chat checks, read [Headless Minecraft testing](references/minecraft-headless-testing.md).

See [PlayerAuctions confirmation/bids](references/playerauctions-confirmation.md).

## Prerequisites

- SSH Key pair generated locally (`~/.ssh/id_ed25519.pub`).
- SFTP connection details from server Settings (Host, Port, Username format `<user>.<server_id>`).
- Optional Client API Key (`ptlc_...`) from Account Settings -> API Credentials for console & power control.

## Noesantara visual changes

- Use the website's blue identity for in-game branding: `#0038FF` with icy `#90E0F0` highlights. When asked to remove yellow/green branding, include solid yellow/gold text, animated TAB frames, command highlights, and NPC hologram gradients—not only logo/footer gradients. Preserve semantic error/status and item-rarity colors unless explicitly included; distinguish bitmap icon colors from text formatting.
- Deliver actual in-game screenshots after visual changes. For “all holograms,” enumerate target IDs first and track readable screenshots separately from attempted captures; an image of an empty location is not visual verification. Include representative images directly and a labeled archive for bulk evidence, with permission/visibility gaps stated.
- Verify configuration, generated pack, client-loaded pack, and public player delivery as separate gates. Do not call a locally loaded test pack a public deployment, or regenerate and replace a customized pack without preserving its additional assets.

For ordered glyph, theme, pack, and screenshot procedures, read [Nexo glyph migration](references/nexo-glyph-migration.md).

## Procedure 1: SFTP File Access via SSH Key (Bypass Web/Cloudflare)

When web panel logins are blocked by Cloudflare Turnstile, bypass the web UI entirely using direct SFTP:

1. **Register SSH Public Key**:
   - Provide `cat ~/.ssh/id_ed25519.pub` to the user to paste into **Account -> SSH Keys** on the panel.
   - Note: Do NOT provide the fingerprint (`SHA256:...`); the panel requires the full public key string starting with `ssh-ed25519` or `ssh-rsa`.

2. **Acquire Connection Details**:
   - Obtain from the server's **Settings -> SFTP Details**:
     - Host: use `PTERODACTYL_SFTP_HOST` from local environment; never commit the real host
     - Port: use `PTERODACTYL_SFTP_PORT` from local environment; common values are `2022` or a provider-assigned port
     - Username: use `PTERODACTYL_SFTP_USER` from local environment; format is usually `<username>.<server_short_uuid>`

3. **Execute Non-Interactive SFTP Operations**:
   Use batch mode with `StrictHostKeyChecking=accept-new` to prevent interactive prompt hanging:

   ```bash
   # List root files and plugins
   sftp -P <PORT> -o BatchMode=yes -o StrictHostKeyChecking=accept-new <USER>@<HOST> << 'EOF'
   ls -la
   ls -la plugins
   bye
   EOF
   ```

   ```bash
   # Upload a plugin or config
   sftp -P <PORT> -o BatchMode=yes <USER>@<HOST> << 'EOF'
   put /path/to/local/plugin.jar plugins/
   bye
   EOF
   ```

   ```bash
   # Download a config file for inspection or editing
   sftp -P <PORT> -o BatchMode=yes <USER>@<HOST> << 'EOF'
   get plugins/Essentials/config.yml /tmp/config.yml
   bye
   EOF
   ```

For IP/port migration, follow [network allocations](references/network-allocation-migration.md).

## Procedure 2: Server Control & File Editing via Client REST API

1. **Authentication & User-Agent**:
   Client API requires a Bearer token with the full key starting with `ptlc_` (~48 characters):
   `Authorization: Bearer ptlc_xxxxxxxxxxxxxxxxxxxxxxxx`
   Always include a browser User-Agent (`-H "User-Agent: Mozilla/5.0"`); Cloudflare blocks default programming client User-Agents (e.g. Python urllib) with HTTP 403.

2. **Check Server Resources & Status**:
   ```bash
   curl -s -H "Authorization: Bearer $PTERO_TOKEN" \
        -H "Accept: application/json" \
        -H "User-Agent: Mozilla/5.0" \
        https://<PANEL_HOST>/api/client/servers/<SERVER_ID>/resources
   ```

3. **Read and Write Files via Client API**:
   - **Read File Content**:
     ```bash
     curl -s -H "Authorization: Bearer $PTERO_TOKEN" \
          -H "Accept: application/json" \
          -H "User-Agent: Mozilla/5.0" \
          "https://<PANEL_HOST>/api/client/servers/<SERVER_ID>/files/contents?file=$(python3 -c 'import urllib.parse, sys; print(urllib.parse.quote(sys.argv[1]))' 'plugins/luckperms/config.yml')"
     ```
   - **Write File Content** (raw body, returns 204 No Content):
     ```bash
     curl -s -X POST \
          -H "Authorization: Bearer $PTERO_TOKEN" \
          -H "Accept: application/json" \
          -H "Content-Type: text/plain" \
          -H "User-Agent: Mozilla/5.0" \
          --data-binary @updated_config.yml \
          "https://<PANEL_HOST>/api/client/servers/<SERVER_ID>/files/write?file=$(python3 -c 'import urllib.parse, sys; print(urllib.parse.quote(sys.argv[1]))' 'plugins/luckperms/config.yml')"
     ```

4. **Send Power Signal** (`start`, `stop`, `restart`, `kill`):
   - Before restart, save the current log and record the stop/start boundary. After starting, require both API state `running` and a new startup sequence with target-plugin enable and `Done (` after that boundary. Merely finding `Done (` or detecting changed file contents is insufficient: `latest.log` can still contain the previous boot plus newly appended shutdown lines while the server is `starting`.
   - Compare new startup errors with the saved pre-restart log. Report existing unrelated errors separately; do not claim whole-server health from one plugin enabling. Verify database connection completion where applicable and re-download the active JAR to compare its SHA-256 with the tested artifact.
   ```bash
   curl -s -X POST \
        -H "Authorization: Bearer $PTERO_TOKEN" \
        -H "Accept: application/json" \
        -H "Content-Type: application/json" \
        -H "User-Agent: Mozilla/5.0" \
        -d '{"signal": "restart"}' \
        https://<PANEL_HOST>/api/client/servers/<SERVER_ID>/power
   ```

5. **Send Console Command**:
   - Inspect command registration and sender restrictions before choosing a smoke command. Player-only GUI commands can return `Incorrect argument for command` from console even when correctly registered; this neither proves GUI failure nor validates gameplay. Use a supported console command for startup checks and an authenticated player for menu acceptance. Do not guess a `help` subcommand.
   ```bash
   curl -s -X POST \
        -H "Authorization: Bearer $PTERO_TOKEN" \
        -H "Accept: application/json" \
        -H "Content-Type: application/json" \
        -H "User-Agent: Mozilla/5.0" \
        -d '{"command": "lp reloadconfig"}' \
        https://<PANEL_HOST>/api/client/servers/<SERVER_ID>/command
   ```

## Procedure 3: Server Backups via Client REST API

Pterodactyl stores backup archives (.tar.gz) outside the server's chrooted SFTP directory. Checking `/backups` or file paths via SFTP will yield nothing. Manage backups via the REST API:

1. **List Existing Backups**:
   ```bash
   curl -s -H "Authorization: Bearer $PTERO_TOKEN" \
        -H "Accept: application/json" \
        https://<PANEL_HOST>/api/client/servers/<SERVER_ID>/backups
   ```

2. **Trigger New Server Backup**:
   ```bash
   curl -s -X POST \
        -H "Authorization: Bearer $PTERO_TOKEN" \
        -H "Accept: application/json" \
        -H "Content-Type: application/json" \
        -d '{"name": "Pre-maintenance Backup"}' \
        https://<PANEL_HOST>/api/client/servers/<SERVER_ID>/backups
   ```

3. **Get Backup Download URL**:
   ```bash
   curl -s -H "Authorization: Bearer $PTERO_TOKEN" \
        -H "Accept: application/json" \
        https://<PANEL_HOST>/api/client/servers/<SERVER_ID>/backups/<BACKUP_UUID>/download
   ```

LegacySchool Nexo imports: [pack deployment](references/legacyschool-nexo-pack.md).

## Procedure 4: Bulk File Transfer & Unarchiving (Handling Wings Daemon Limits)

When deploying large plugin bundles, archives, or backups to a server:

1. **Wings Decompress API Fragility**:
   - The Pterodactyl client endpoint `/api/client/servers/<ID>/files/unarchive` often returns `500 ErrorException` or validation failures when processing `.tar.gz` archives on custom host configurations.
   - For multi-gigabyte transfers, prefer direct recursive SFTP upload (`put -r <local_dir>/* <remote_dir>/`) rather than relying on panel-side extraction of remote archives.

2. **Long-Running SFTP Uploads via Background Process**:
   - Transferring directories with thousands of small files (like plugin configurations, language files, and libraries) will exceed foreground tool timeouts (180s).
   - Run large recursive SFTP uploads as background terminal commands:
     ```bash
     sftp -P <PORT> -o BatchMode=yes <USER>@<HOST> << 'EOF'
     cd <TARGET_DIR>
     put -r /path/to/staging/* .
     bye
     EOF
     ```
     Pair with `background=true, notify=true` and monitor with `process_manage(action='poll')`.

3. **Staging & Excluding Database/State Folders**:
   - Heavy local logging plugins (e.g. `CoreProtect` with multi-gigabyte `database.db` files) should be excluded during recovery/migration staging to prevent bandwidth saturation and node disk quota exhaustion.

## Procedure 5: Database Maintenance, Pre-Wipe Dump & Safe Data Reset

When performing server wipes, seasonal resets, or clearing game databases associated with Pterodactyl servers:

1. **Retrieve Database Credentials via API**:
   Query all allocated databases and passwords in one call:
   ```bash
   curl -s -H "Authorization: Bearer $PTERO_TOKEN" \
        -H "Accept: application/json" \
        "https://<PANEL_HOST>/api/client/servers/<SERVER_ID>/databases?include=password"
   ```
   Extract `name`, `host.address`, `host.port`, `username`, and `relationships.password.attributes.password`.

2. **Stop Server Before Database Operations**:
   Confirm `offline` before target wipes/truncation. For imports/clones with an unchanged source, follow [database clone verification](references/database-clone-verification.md).

3. **Pre-Wipe Local Backup (Mandatory)**:
   Always dump all databases locally before any destructive command:
   ```bash
   mariadb-dump -h<HOST> -P<PORT> -u<USER> -p<PWD> <DATABASE> > /path/to/backup/<DATABASE>.sql
   ```

4. **Safe Truncation (Preserve Schema Structure)**:
   Never run `DROP TABLE` or `DROP DATABASE`. Run `TRUNCATE TABLE` with disabled foreign key checks:
   ```sql
   SET FOREIGN_KEY_CHECKS = 0;
   TRUNCATE TABLE `table_name`;
   SET FOREIGN_KEY_CHECKS = 1;
   ```

5. **Protect Migration & Metadata Tables**:
   Never truncate migration tracking or schema metadata tables (e.g. `*_schema_migrations`, `*_metadata`, `*_migrations`). If migration records are wiped while tables exist, plugins attempt to run initialization DDL on boot and crash with `Table already exists` or `Duplicate column name`.

## Procedure 6: Full Plugin Backup & Purge Procedure

When wiping, replacing, or rebuilding a server's plugin suite:

1. **Catalog Active JARs**:
   Query all files in `plugins/` via `GET /api/client/servers/<ID>/files/list?directory=plugins` and filter for `.jar` files.

2. **Full Local Backup Before Purge (Mandatory)**:
   Create a dedicated local backup directory (e.g. `/home/barzzly/backup_plugins_<server>/`). Download every JAR using signed URLs (`GET /api/client/servers/<ID>/files/download?file=plugins/<jar>`). Verify that downloaded file count matches the server and total size is greater than 0.

3. **Stop Server Before Deletion**:
   Always transition server state to `offline` (`signal: stop`) and poll `resources` until state is `offline`. Never delete JAR files while the JVM is active.

4. **Chunked Deletion via API**:
   Delete files in batches of 40 via `POST /api/client/servers/<ID>/files/delete` with payload `{"root": "plugins", "files": [...]}`. Verify with a list call that 0 JARs remain.

5. **Direct Delivery on Request**:
   Deliver requested JAR files from the local backup directly via `MEDIA:/absolute/path/to/file.jar`.

## Maintenance cleanup preference

- Wings may reject Paramiko `posix_rename` overwrite even after staging upload succeeds. Verify server remains offline and inspect exact active/staged hashes before recovery; use ordinary sequential `rename(active, rollback)` then `rename(staged, active)`. Read back both activated files before start, require fresh startup completion, and remove remote rollback copies only after matching retained local backups and verifying service health. Never blindly rerun the whole deployment after partial failure.

- After completed and verified NoeRPG maintenance, remove agent-created remote `.pre-*` rollback copies and temporary fixtures instead of leaving them scattered beside live files. Keep recoverable backups consolidated in a private local Minecraft maintenance archive. Do not infer permission to delete plugin-managed backups, disabled content, world/player data or active JARs. Inventory exact paths, archive and verify hashes before removing obsolete copies, read back absence, compare active counterparts, and disclose pruned scan areas rather than claiming whole-server coverage.

## Procedure 7: Stale Config & Backup Scanning via Ephemeral SFTP

When auditing server storage or cleaning up obsolete configs (`.old`, `.bak`, `.backup*`, `.save*`, `~`, `.broken`):

1. **Avoid REST API for Deep Directory Crawling**:
   Pterodactyl client endpoint `/files/list` only lists one level per call. Scanning deep plugin directories via HTTP creates hundreds of rate-limited requests. Direct SFTP traversal via Python + Paramiko (`uv run --with paramiko python3`) is orders of magnitude faster.

2. **Exclude Chunk & Texture Directories**:
   Always skip `region/`, `poi/`, `entities/`, `playerdata/`, `stats/`, `data/`, `libraries/`, `assets/`, `textures/`, `models/`, and `blueprints/` during recursive directory walks to prevent timeouts scanning tens of thousands of binary chunk files and assets.

3. **Decode Wings `/.trash` File Names**:
   Files deleted via the panel/API are moved into `/.trash/` named after the base64-encoded original path, optionally suffixed with `_YYYYMMDD_HHMMSS`. Decode base64 strings with standard padding (`base64.b64decode(name + '=' * (-len(name) % 4))`) to identify candidates for restoration.

## Pitfalls

- **Vault SUCCESS is not economy persistence**: For EssentialsX YAML-backed economy, Vault mutation can return SUCCESS before its queued atomic save; bridge journal fsync does not make provider state durable. Never credit external wallets or release reservations based on response alone. Require exact observed delta plus provider-owned async durable receipt/revision with propagated errors, file and directory fsync, and coordinated recovery. Stock `blockingSave()`, pending-write counts, worker reflection, sleeps, or reading YAML are not safe durability barriers. Keep durable mode disabled without that verified barrier. Enable a separate best-effort mode only with explicit acceptance of provider rollback risk, exact-delta receipts, durable bridge journaling, idempotent result delivery and conservative UNKNOWN handling; never silently downgrade durable mode.
- **Bukkit proxy authentication attestations**: Backend reachability, offline UUIDs, whitelist, or missing AuthMe never establish JPremium login. Use fresh signed proxy login attestations tied to exact Player UUID/name, backend-generated per-connection random challenge, pinned proxy connection, short expiry and replay protection. Parse envelopes with strict streaming JSON, duplicate-field rejection and UTF-8 decoder REPORT; Gson JsonParser can accept lenient syntax/duplicate keys. Clear on disconnect and signed negatives.

- **Dependent bulk renames race**: A single API rename payload containing `active -> active.old` followed by `active.new -> active` can partially apply and return 409. Run dependent renames sequentially (SFTP batch or separate API calls), inspect exact directory state after failure, and verify active/backup hashes before start. Never blindly replay a partial rename batch.

- **SFTP Directory Traversal Bottlenecks on World Regions and Assets**: Minecraft server folders contain hundreds of thousands of chunk `.mca` files and asset `.json`/`.png` textures. Always prune `region`, `poi`, `entities`, `playerdata`, `stats`, `models`, and `textures` when traversing via SFTP to avoid stalling execution.
- **MythicLib Negative Damage Healing on High Defense**: When configuring weapon skills in MythicMobs and MMOItems, check MythicLib's defense formula (`defense-application: natural: '#damage# - #defense#'`). When an attacked target's defense exceeds incoming base skill damage, the difference produces negative damage, which Bukkit and Minecraft treat as health regeneration (healing the target). Ensure defense formulas clamp to zero or use percentage scaling (`#damage# * (1 - (#defense# / (#defense# + 100)))`), and check skill targeting conditions like `mmoCanTarget{interaction=OFFENSE_ACTION} false` which route execution to heal mechanics inside claims, party protection, or PvE-disabled zones.
- **Decoding Wings Base64 Trash Entries**: Files inside `.trash` are renamed to standard Base64 representations of their original paths with trailing timestamps. Decode with standard Base64 padding (`base64.b64decode(name + '=' * (-len(name) % 4))`) to inspect deleted items.
- **Server Stop Mandatory Before Bulk JAR Deletions**: Always transition server state to `offline` before deleting all plugin JARs. Deleting JAR files while the server is active causes classloader crashes (`NoClassDefFoundError` on background schedulers) and leaves corrupted locks in `.paper-remapped`.
- **Chunked Deletions for Large Plugin Suites**: Pterodactyl API's `/files/delete` endpoint should process files in batches of 40. Sending 80+ files in one request can trigger proxy timeouts or daemon connection reset.

- **OpenSSH SFTP rm lacks recursive flag**: OpenSSH `sftp` `rm` command rejects `-r` (`rm: Invalid flag -r`). To remove remote directories, use a generated bottom-up exact file delete + `rmdir` script or rename/move.
- **Never delete or replace whole plugin root directories**: Live servers contain existing third-party assets, rank cosmetics, and active configs in `plugins/ItemsAdder/contents` and `plugins/MMOItems`. Replacing or deleting whole plugin roots wipes out non-pack server assets. Always delete and upload only exact pack-specific subfolders (e.g. `contents/SL_*`).
- **Verify plugin JAR naming after staging**: Plugin jars ending in `.jar.old` or `.disable` are silently ignored by Paper/Spigot loader during startup. Dependent plugins (like MythicLib and MMOItems) will boot with missing class/skill errors if prerequisite jars are renamed.
- **SFTP Timeouts on Deep Directory Trees**: Minecraft plugin suites (like `AxVaults`, `FastAsyncWorldEdit`, `LuckPerms`) contain deeply nested library directories (`libs/com/...`). A recursive `put -r` will easily exceed short execution timeouts. Always launch recursive directory uploads in a background process (`background=true, notify=true`).
- **Archive Extraction Quirks on Pterodactyl**: Pterodactyl Wings handles `.zip` files more reliably than `.tar.gz` through its API, but if the panel API fails or crashes on decompression, immediately stage files locally and upload uncompressed directories directly via SFTP.

- **Backups Inaccessible via SFTP**: Pterodactyl backup archives (.tar.gz) live on the host node or S3/remote storage managed by the daemon/panel, not inside the server root directory accessible via SFTP. Checking `/backups` or searching files via SFTP will yield nothing; querying or downloading backups requires the Client REST API (`/api/client/servers/<SERVER_ID>/backups`) or the panel web interface.
- **Kopia Snapshot Backups Fail API Download**: When a panel uses Kopia as its backup driver (`"disk": "kopia"` in backup attributes), requesting a download URL (`/download`) returns `400 BadRequestHttpException: Something went wrong. Failed to Download Backup.` because Kopia stores deduplicated chunks rather than standalone archive files. These backups can only be restored in-place via the panel API (`/api/client/servers/<SERVER_ID>/backups/<UUID>/restore`) or the web UI, not downloaded to a remote machine.
- **Truncated API Key Token Prefix**: Pterodactyl displays only the public 16-character key identifier in the active keys table (e.g. `ptlc_m1XvAKRdQYw`). The full 48-character bearer token is displayed exactly once in a modal dialog upon creation. If a user copies the key from the list view rather than the post-creation modal, all API calls fail with `401 Unauthenticated`. Instruct the user to create a new key and immediately copy from the modal.

- **Cloudflare Turnstile on Web Panel**: Never loop attempting headless clicks on Cloudflare Turnstile inside CDP browser sessions; Turnstile detects headless environments and will not pass. Pivot immediately to SFTP (SSH Key) or REST API.
- **Cloudflare 403 on REST API Requests**: Cloudflare WAF on Pterodactyl panels blocks requests with programming language default User-Agents (e.g. Python urllib). Always set `-H "User-Agent: Mozilla/5.0"` on all HTTP/curl calls.
- **LuckPerms Cross-Server Permission Sync**: When running a network (Proxy + backend Paper/Purpur instances) sharing SQL storage, always explicitly configure `messaging-service: sql` across all servers. The default `auto` frequently fails to bind the SQL messaging queue silently, forcing players to relog to receive updated permissions. Verify active cross-server sync by triggering `/lp networksync` from console and confirming `[LP] Other servers were notified via Sql Messaging successfully`.
- **Primary Game Databases vs Leaderboard Plugins**: Third-party leaderboard plugins (like ajLeaderboards) only populate offline metrics if players exist in local server storage/usercache. Always prioritize reading directly from the primary plugin database (e.g. `s4077_PlayerPoint` for PlayerPoints coins) when displaying network-wide leaderboards or analytics.
- **In-Game Currency Nomenclature**: Always verify in-game branding before exposing metrics on web dashboards; plugins named PlayerPoints often serve as "Coins" in server economies. Multi-server networks should segment public leaderboards by gamemode/server first (e.g. ECO RPG, PVP SL, RP REBEL) before showing specific stat categories.
- **ajLeaderboards Setup & Database Integration**: Store credentials in `plugins/ajLeaderboards/cache_storage.yml` with `method: mysql`, remote `ip:port`, `database`, `username`, and `password`. In `config.yml`, set `enable-dontupdate-permission: false` so admins/OPs are not skipped. Register boards via console `/ajlb add %placeholder%`. Map DeluxeMenus items to `%ajlb_lb_<board>_<pos>_alltime_name%` and `%ajlb_lb_<board>_<pos>_alltime_value%`, and player stats to `%ajlb_position_<board>_<type>%` and `%ajlb_value_<board>_<type>%`.
- **ajLeaderboards Offline Population**: Newly created boards show empty `--- - ---` until players join or until offline update runs. Execute `/ajlb updatealloffline <board>` via console to parse offline player data from Vanilla stats and Essentials/Vault into MySQL. Note that some third-party stats (e.g. AuraSkills) do not support offline player parsing and require live player login.
- **Server-to-Server JAR Transfer via Signed API URLs**: Transfer plugin files between panel instances without downloading locally by requesting a signed download URL (`GET /api/client/servers/<SRC>/files/download?file=<path>`) and streaming to a signed upload URL (`GET /api/client/servers/<DST>/files/upload?directory=<path>`) with `curl -X POST "$upload_url" -F "files=@-"`.
- **Truncated API Key**: Pterodactyl tokens are ~48 chars starting with `ptlc_`. If only the visible snippet (16 chars) is copied, the API returns `401 Unauthenticated`. Always verify key length.
- **SSH Fingerprint vs Public Key**: Users frequently paste the SHA256 fingerprint instead of the `~/.ssh/id_ed25519.pub` content. Explicitly instruct them to copy the raw public key string.
- **Non-Standard SFTP Ports**: Pterodactyl SFTP rarely uses port 22. Standard is port `2022`, but providers may assign custom ports. Always verify the exact port from panel SFTP details and keep it in `PTERODACTYL_SFTP_PORT`, never in public documentation.
- **Extracting Server Pack Textures & Serving in Embeds**: Custom in-game textures and rank icons (e.g. Nexo or ItemsAdder glyphs) reside deep in server pack directories (`plugins/Nexo/pack/external_packs/<Pack>/assets/<namespace>/textures/`). To discover the exact registered glyph names and texture mappings, inspect the Nexo glyphs definition file (e.g. `plugins/Nexo/glyphs/Icon Rank ( 0xE400 - 0xE40D )/Icon Rank ( 0xE400 - 0xE40D ).yml`). Always download the complete hierarchy including default player ranks (`warga.png` for `default`), staff tiers (`staff.png`, `admin.png`, `dev.png`, `owner.png`), and network partner tiers (`noe.png`, `iestari.png`) alongside paid tiers (`prime`, `rogue`, `midas`, `aether`, `donatur`, `tajir`, `youtube`, `tiktok`, `media`). Rather than opening slow manual SFTP sessions, query the client API for a signed download URL (`GET /api/client/servers/<ID>/files/download?file=<url_encoded_path>`), download the asset programmatically, and copy it to a public web/CDN directory (e.g. `client/public/ranks/` and `dist/public/ranks/`). Never use raw file attachments (`files: [attachment]`) inside Discord ephemeral interaction embeds, as local file attachments prevent Discord mobile clients (iOS/Android) from dismissing the message. Instead, serve the thumbnail via public HTTPS URL (`.setThumbnail('https://<domain>/ranks/<name>.png')`). In web modals, render the badge directly inside the rank stat box rather than crowding the player's nickname.
- **Discord Bot Interactive Store & Catalog Embeds (Ranks, Items, Coins)**:
  1. **Main Embed Formatting**: Use the server's official animated emojis (`<a:crown_animated:...>`, `<a:animatedarrowyellow:...>`, `<a:animatedarrowred:...>`), never generic mobile emojis. Format items as `<a:animatedarrowred:...> **NAME** <a:animatedarrowyellow:...> **Harga**` (bold prices without backticks, no redundant shorthand in parentheses like `(40K)`). Mention outside the embed must use spoiler tags: `|| @everyone ||`.
  2. **Dropdown Select Menus**: Keep labels clean (`NAME - Harga`) and omit subtitle descriptions (`description`) to prevent cluttered mobile views. Avoid duplicate button rows if a select menu is already provided.
  3. **Role & Creator Separation**: Separate distinct creator tiers into individual options: `YOUTUBE` (Subscribers threshold), `TIKTOK` (Followers threshold), and `MEDIA` (higher tier for active live streamers with viewer requirements).
  4. **Coin Shop Messaging**: For currency/coin packages, state terms clearly: coins persist permanently across season resets, only decrease when spent, and can also be earned in-game via votes and quests.
  5. **Ephemeral Dismissal Fix**: To prevent stuck/undismissible ephemeral responses on mobile, do not attach local files. Serve images over HTTPS CDN and add a dedicated `[ Tutup Pesan ]` button (`customId: '..._dismiss'`) that executes `await interaction.deferUpdate(); await interaction.deleteReply();`.
- **Webstore In-Game Leaderboards & Navigation**:
  1. **Server-First Segmentation**: For multi-server networks, segment public in-game leaderboards by gamemode/server first (`ECO RPG`, `PVP SL`, `RP REBEL`) before displaying stat categories (`Uang`, `Coin`, `Playtime`, `Kills`, `Deaths`, `Skills`).
  2. **Economy Naming**: Verify server economy branding before publishing; `PlayerPoints` data typically maps to "Coin", not points.
  3. **Clean Typography**: Remove all decorative emojis (`💸`, `🧿`, `⚔`, etc.) from leaderboard category pills and cards.
  4. **Mobile Navbar Controls**: Never hide the login action on mobile with responsive hiding classes (`hidden sm:inline-flex`); show an accessible icon button (`User`) in mobile top navigation. Use a segmented pill switcher (`[ ID | EN ]`) with clear active state styling instead of a single ambiguous text button.
- **AuraSkills / AureliumSkills Migration from YAML to MySQL**:
  Enabling SQL in `config.yml` alone does NOT migrate existing player userdata from YAML files to MySQL. To migrate safely without data loss:
  1. While still running YAML storage, execute `/skills backup save` via console. Verify the archive in `plugins/AuraSkills/backups/` (`backup-<timestamp>.yml`).
  2. Configure `plugins/AuraSkills/config.yml` under `sql:` (`enabled: true`, `type: mysql`, remote `host`, `port`, `database`, `username`, `password`).
  3. Restart the server. AuraSkills connects to MySQL and creates the schema (`auraskills_users`, `auraskills_skill_levels`, `auraskills_modifiers`, etc.).
  4. Import all player data into MySQL by executing `/skills backup load <filename>` from console.
  5. Web integrations can read live skill progression directly: `auraskills_users.player_uuid` matches Mojang/LuckPerms UUID. Read `skill_name`, `skill_level`, and `skill_xp` from `auraskills_skill_levels`. Total Power Level is the sum of `skill_level`.
- **Webstore Player Profiles & Donation Calculation**:
  1. **Historical Log Merging & Preventing Double-Counting**: When historical donations exist in a dedicated dataset (e.g. `DONATORS_DATA`) and are subsequently imported into the MariaDB `transactions` table, ensure the merge function (`mergeDonatorsWithTransactions`) treats the database as the authoritative single source of truth when populated. Adding static historical arrays on top of imported database rows causes player totals to double (e.g. inflating Rp 1.84M to Rp 3.68M). Only use the static array as a fallback when database rows are empty or unreachable.
  2. **Channel Donation Log Scraping (Bot Embeds + Human Codeblocks)**: When scraping donation log channels (e.g. `#donation-log`), never parse embed objects alone. Up to half of transactions may be posted by human staff as plain-text markdown codeblocks (`\`\`\`NAMA: ... HARGA: ...\`\`\``). Parse both embed descriptions/fields and raw message content. Detect couple donations (`+`, `&`, `dan`, `💖`, `❤️`) and split the price 50/50 so each partner's order history and donation total receive equal credit.
  3. **Private history identity**: Require a server-authenticated owner or active admin. Match `WHERE LOWER(username) = LOWER(?)` against the verified canonical name only. Preserve leading dots: `Foo` and `.Foo` are distinct accounts. Never combine dot-stripped variants for private purchase history; display-only nickname selection is not authentication.
  4. **Discord Bot `/donation` Amount Parsing**: When parsing user-input price fields in Discord slash commands or modals, never use raw digit stripping (`replace(/[^0-9]/g, '')`). Shorthand inputs like `50k` or `120k` will reduce to `50` or `120`. Always support `k` multipliers (`* 1000`), strip currency affixes (`rp`, `rupiah`, `rb`), and discard decimal cents (`,00`) before extracting values.
  5. **Trust Device Session Expiry**: In storefronts with username-only login modals, enforce a 1-hour trust device session window (`USER_SESSION_MS = 3600000`). Store `loginAt: Date.now()` in persistent local storage. Attach an automated watchdog timer in the root application component that evaluates `checkSession()` periodically (every 30s) and on window `focus` / rehydration, automatically clearing user and cart state upon expiration to prevent open sessions on shared devices.
  6. **Iconography Perceived as Emojis**: Users frequently perceive vector/SVG icons (`<Receipt />`, `<LogOut />`, `<Crown />`, `<Trophy />`) as "emojis". When instructed to remove all emojis, strip decorative icon pictograms from navigation buttons, card headers, and badges in favor of strict, clean typography.
  7. **In-Game Rank Prefix Badges**: Avoid duplicating rank text and wrapping images in redundant borders (e.g. `TIER RANK Midas [Midas]`). Render the authentic 80x16 pixelated PNG texture (`style={{ imageRendering: 'pixelated' }}`) directly under the `TIER RANK` header without surrounding card containers or redundant name labels. Leave the player nickname header clean without adjacent icons.
  8. **Footer Spacing**: Ensure profile and transaction dashboards maintain generous bottom padding (`pb-28 md:pb-36`) so tables and stat cards do not crowd the footer.
  9. **Draggable Cards & Carousel Button Clicks**: When placing buttons or links inside draggable/swipeable tracks, parent track `onMouseDown` and `onTouchStart` listeners will intercept clicks and activate `pointer-events-none` before child click events fire. Always guard parent handlers with `if ((e.target as HTMLElement).closest("a, button")) return;`, add `onMouseDown` and `onTouchStart` `stopPropagation` on the child button, and place links below text descriptions rather than overlapping character art or feet.
  10. **Maintenance & Alert Banners**: Prefer clean dark/neutral borders (e.g. `border-2 border-[#1A1A1A]`) over yellow/gold borders that feel dated or messy. Center alert/warning icons vertically (`items-center`) with accompanying copy rather than forcing top alignment with `items-start mt-1`.
- **Social Media Link Previews (OpenGraph / WhatsApp) Cache Busting**:
  WhatsApp, Discord, and Telegram link crawlers aggressively cache `og:image` by URL. When replacing legacy branding with modern logos or when the user supplies custom artwork:
  1. For messaging platforms (WhatsApp, Telegram) that favor square (1:1) previews, use the full artwork as the square image (`og-image.png` 1254x1254 or `og-square.png` 512x512).
  2. For landscape cards (Twitter/X, Discord `summary_large_image`), generate a 1200x630 version (`og-banner.png`) extending or padding the background to match the art edge tone.
  3. Always append cache-busting query parameters (e.g. `og-image.png?v=banner`) across `index.html` (`og:image`, `og:image:secure_url`, `link rel="image_src"`, `twitter:image`) and React Helmet/dynamic `<SEO>` components simultaneously so crawler caches are broken immediately.
- **BatchMode Required**: Always pass `-o BatchMode=yes` with `sftp` in automation scripts. If authentication fails, it terminates immediately with exit code 255 rather than hanging indefinitely on a password prompt.
- **Wings Signed Upload URL Target Directory**: When requesting a signed upload URL via `GET /api/client/servers/<ID>/files/upload`, appending `&directory=<target_dir>` (e.g. `&directory=plugins`) directly to the daemon upload URL (`https://<node>/upload/file?token=...&directory=plugins`) and specifying the filename in curl (`-F "files=@/path/to/file.jar;filename=plugin.jar"`) will land files directly into the target folder without requiring a separate move/rename API call.

- **Geyser/Floodgate Velocity Updates**: Resolve official metadata at `https://download.geysermc.org/v2/projects/<geyser|floodgate>/versions/latest/builds/latest`, then pin version/build in `/versions/<version>/builds/<build>/downloads/velocity`. Verify SHA-256 against `downloads.velocity.sha256` and inspect `velocity-plugin.json`. Back up both JARs, configs, and Floodgate key locally in a private categorized directory. Upload with non-`.jar` staging suffix, read back hashes, stop and confirm offline, rename old JARs to non-loading backups, activate staged JARs, verify hashes, then start. Check fresh startup logs, not merely running state: GeyserUtils can throw `NoSuchMethodError` for `NbtMapBuilder.putList` while Geyser still binds UDP and reports Done; report this custom-entity failure explicitly without claiming full gameplay health. Geyser can migrate config schema automatically; compare diffs before claiming configs unchanged. Preserve Floodgate key and avoid changing unrelated plugins without scope.

- **Server Plugin Sourcing & Server Isolation Rules**:
  When performing automated plugin upgrades on server instances:
  1. **Strict Server Isolation (NEVER Cross-Copy Outside Noesantara)**: NEVER cross-copy, scrape, or transplant JARs or configurations from servers outside the Noesantara ecosystem (e.g. Queencraft, LegacySchool, or third-party servers on the same panel). Plugin borrowing is strictly limited to instances bearing the `Noesantara` project name. Sibling servers belonging to outside projects have separate licenses, configs, and environments; copying across them breaks isolation and violates licensing.
  2. **Official External Sourcing Only**: All updates must be downloaded directly from official, authoritative external repositories:
     - Modrinth API (`https://api.modrinth.com/v2/project/<id>/version` -> download primary loader build)
     - GitHub Releases (`https://api.github.com/repos/<owner>/<repo>/releases/latest` -> download matching asset)
     - Official project download endpoints (e.g. `download.luckperms.net`, EssentialsX GitHub, GeyserMC downloads API)
  3. **Premium / Commercial Plugins**: Commercial/licensed plugins (such as `AdvancedEnchantments`, `DeluxeSellwands`, `ShopGUIPlus`, `RoseStacker`, `MMOItems`, `Nexo`, `PlayerAuctions`, `Ultimate_BlockRegeneration`) cannot be downloaded from open public repositories. NEVER transplant them from other panel servers; leave the server's existing version intact and clearly report to the operator that manual file upload is required.
  4. **Coupled Plugin Dependencies (e.g. NightExpress Suite)**: When updating core framework plugins, update all dependent plugins simultaneously. For example, `ExcellentCrates` 6.x requires `nightcore` 2.16.x or newer; deploying `ExcellentCrates-6.6.1` while leaving `nightcore-2.7.3` will cause runtime startup crashes. Both are available on Modrinth.
  5. **Custom Internal Plugins**: Plugins with custom prefixes (e.g. `Noe*`) belong to the network's proprietary codebase and must never be overwritten from external sources.
  6. **Restoring Deleted Files from Pterodactyl Wings `/.trash`**: When files are deleted via the Client API (`/files/delete`), Wings moves them into `/.trash` named with base64-encoded original paths (e.g. `L3BsdWdpbnMvQWR2YW5jZWRFbmNoYW50bWVudHMtOS4yNC44Lmphcg`). To restore an accidentally deleted file without node disk access, invoke the rename API (`PUT /api/client/servers/<ID>/files/rename`) with `{"root": ".trash", "files": [{"from": "<base64_name>", "to": "../plugins/<original_filename>"}]}`.
- **Creative glyph duplication reproduction**: User requires Nexo/MMOItems items with glyph lore to remain duplicable through native creative/GMC while preserving visible glyphs, stats, enchants and custom data. Disabling creative duplication, removing glyphs or requiring plugin give commands is not an acceptable permanent fix. User reports these items develop nesting errors after creative duplication. Treat creative inventory round-trip as a reproduction lead, not proven root cause. Compare freshly generated item with creative clone across repeated clone/move/reopen cycles; measure component depth and preserve custom data. Check whether client-rendered glyph components return through creative inventory packets and get formatted again even with clean placeholder configuration. Avoid creative cloning affected items while diagnosing; generate fresh instances through their owning plugin. Do not claim AxVaults generated the corruption merely because its loader reports it.

- **Nesting error diagnosis before repair**: Inspect archived Paper logs as well as latest.log; after restart a clean latest log may only mean the affected vault owner has not loaded. Find the first `Failed to unflatten text component json`, then trace serializer frames and preceding join. AxVaults `H2.loadVaults` with repeated `nexo:default` indicates malformed stored item text, not a wallet/WD failure. Audit current glyph placeholders separately: zero self-matching placeholders does not repair previously stored recursive components. Do not delete vault DBs or player items; preserve backups and identify exact affected records before proposing repair. Treat nearby login as correlation until DB ownership is verified.

- **Nexo Glyph Recursion & Gson 255 Nesting Limit (`AxVaults` / MMOItems / DFU)**:
  When configuring Nexo custom glyphs (e.g. `plugins/Nexo/glyphs/...`), NEVER set the `placeholders` entry to the raw unicode character itself (e.g. `char: ` with `placeholders: [- ]`). When `Plugin.formatting.items: true` is enabled in `plugins/Nexo/settings.yml`, Nexo intercepts item components over packets and wraps placeholder characters in a new text component with `font: "nexo:default"`. If the placeholder is identical to the glyph character, Nexo replaces the glyph with itself on every inventory tick/re-render, wrapping the component in another layer of `{"extra": ...}`. After 255 re-renders (a few minutes of gameplay), Gson crashes with `MalformedJsonException: Nesting limit 255 reached` whenever plugins like `AxVaults` or Paper's DataFixerUpper deserialize the item.
  
  To keep `Plugin.formatting.items: true` active (so glyphs format automatically across all item lore and names) without triggering recursion:
  1. **Purge Raw Unicode Characters from `placeholders`**: Scan all files under `plugins/Nexo/glyphs/` and replace any placeholder matching `char` with a textual token (e.g. change `placeholders: ['']` to `placeholders: [':gemsstone:']` or `[':<glyph_name>:']`). When placeholders are textual, Nexo replaces the token once and will never re-match the resulting unicode character on subsequent inventory ticks.
  2. **Keep `Plugin.formatting.items: true`**: Do not disable item formatting if the server relies on Nexo font encapsulation for custom fonts.
  3. **Recover corrupted items selectively**: Back up first and identify exact affected records. Test text-component repair on a copy while preserving item stats, enchants, quantity and custom data. Do not purge inventories or reset `AxVaults/data.mv.db`; removal requires explicit approval for exact items. Fixing placeholders does not repair existing stored components or prove creative duplication safe.
- **Paper Watchdog Auto-Save Freeze Warnings (`DO NOT REPORT THIS TO PAPER`)**:
  When server console logs print `--- DO NOT REPORT THIS TO PAPER - THIS IS NOT A BUG OR A CRASH --- The server has not responded for 10 seconds! Creating thread dump` with stack traces pointing to `LevelStorageSource$LevelStorageAccess.saveLevelData` -> `ServerLevel.saveIncrementally` -> `createTempFile`, the server main thread is blocked waiting for disk I/O to complete writing world data (`level.dat`). This is caused by storage I/O bottlenecks on the hosting node during synchronous world auto-saves. Mitigate this by increasing `ticks-per.autosave` in `bukkit.yml` or `paper-global.yml` (e.g. from 6000 to 12000 ticks) or scheduling non-peak incremental saves to prevent thread watchdog alerts.
- **Auditing Plugin Health & Red Plugin Diagnostics**:
  To identify failed plugins programmatically:
  1. Count JARs in `plugins/` via API (`GET /api/client/servers/<ID>/files/list?directory=plugins`).
  2. Send `plugins` or `pl` to console (`POST /api/client/servers/<ID>/command`) and parse `logs/latest.log`. Plugins prefixed with `*` or listed under `Disabling <Plugin>` are RED in-game and disabled due to uncaught initialization exceptions.
  3. Compare plugin data folders against active JARs to identify orphan folders left behind by removed plugins.
- **MMOItems & MythicLib Version/Build Coupling**:
  In the Lumine/PhoenixDevt ecosystem, MMOItems and MythicLib builds must match strictly. Modern builds of MythicLib (1.7.1 b100+) relocated base class `MMOPlugin` from `io.lumine.mythic.lib.util.MMOPlugin` to `io.lumine.mythic.lib.module.MMOPlugin`, and deliberately throw `java.lang.RuntimeException` in the old constructor. Installing an older release of MMOItems (e.g. `MMOItems-6.10.jar`) with a newer MythicLib causes an immediate `InvalidPluginException: Exception initializing main class 'net.Indyuce.mmoitems.MMOItems'` on startup. Always deploy matching builds (e.g. `MMOItems-6.10.1.jar` with `MythicLib-dist-1.7.1-b106`). When resolving mismatches on premium plugins, inform the operator to upload the matching purchased JAR rather than transplanting files from other panel instances.
- **Server Database Resets & Preserving Schema Migrations & Currencies**:
  When emptying or resetting server databases (e.g. for season wipes):
  1. Retrieve connection parameters via `GET /api/client/servers/<ID>/databases?include=password`.
  2. Always transition server to `offline` state before executing wipes to prevent active HikariCP connection pool locks or in-flight write corruption.
  3. Dump every database to local `.sql` files before executing any table modifications.
  4. Truncate tables (`SET FOREIGN_KEY_CHECKS = 0; TRUNCATE TABLE \`table\`; SET FOREIGN_KEY_CHECKS = 1;`) rather than dropping tables so schemas, indexes, and column types persist.
  5. **Never truncate migration tables**: Skip tables containing `migration` or `metadata` (e.g. `auraskills_schema_migrations`, `huskclaims_metadata`, `playerpoints_migrations`). Clearing migration history while tables exist triggers initial creation DDL on the next server startup, crashing plugins with `Table already exists` or `Duplicate column name`.
  6. **Player Currency Preservation**: Network economy tables (e.g. `s4077_PlayerPoint`) hold permanent player coins, username caches, and transaction logs that must be preserved across seasonal wipes. Always verify explicit database exclusion lists before executing bulk database commands.
- **ModelEngine 4 Cross-Version Compatibility with ViaVersion / ViaBackwards (1.20.1 to 1.21.4+)**:
  On Minecraft servers running 1.21.4+ (such as UniverseSpigot/Paper 1.21.11), ModelEngine 4 defaults to `Force-Custom-Model-Data: false` in `plugins/ModelEngine/config.yml`. Under this default, ModelEngine transmits modern `item_model` data components on `BONE` or `GLASS` items instead of integer `CustomModelData`. When older clients (Minecraft 1.20.1 through 1.21.3) connect via ViaVersion / ViaBackwards proxy, the client does not support `item_model` components, causing ViaVersion to drop the model metadata and downgrade the item to plain unmodeled `Material.GLASS` or `leather_horse_armor` (which renders in-game as an untextured red translucent cube or crystal). To restore proper model rendering across all client versions 1.20.1 through 1.21.4+:
  1. Set `Force-Custom-Model-Data: true` under `Model-Engine:` in `plugins/ModelEngine/config.yml`.
  2. **Full Server Restart Required**: Do NOT rely on `/meg reload` alone. `/meg reload` only re-parses blueprints and model files; the NMS packet handler (`NMSHandler_v26_2`) initializes its internal `forceCMD` state on startup and will continue sending `Material.GLASS` without CustomModelData until a full server restart is performed.
  3. **Resource Pack Dual Compatibility & 1.20.1 Root Fallback**:
     - Maintain legacy predicate overrides with `custom_model_data` in `assets/minecraft/models/item/leather_horse_armor.json` and modern definitions in `assets/minecraft/items/leather_horse_armor.json`.
     - Minecraft 1.20.1 does not support resource pack `overlays` (introduced in 1.20.2). Any item models placed inside overlay directories (such as `modelengine_1_19_4/assets/minecraft/models/item/player_head.json`) MUST also be copied directly to the root `assets/minecraft/models/item/player_head.json` so 1.20.1 clients load without missing models.
     - In `pack.mcmeta`, declare `pack_format: 15` alongside `"supported_formats": {"min_inclusive": 15, "max_inclusive": 32767}` to eliminate red incompatible-version warnings across both legacy and modern clients.

