# Nexo glyphs, branding, and visual acceptance

## 1. Discover actual sources and scope

- For Noesantara tag additions, merge glyph definitions into the existing `Icon Tags ( 0xSTART - 0xEND )/Icon Tags ( 0xSTART - 0xEND ).yml`, not a standalone pack-named YAML. Derive both folder and filename ranges from actual minimum/maximum registered chars; preserve IDs/placeholders/metrics, move redundant definition files outside glyph tree, reload and verify one provider per char.
- Read active `plugins/Nexo/glyphs/**/*.yml`. Build `char` to existing textual `:name:` mappings, reject ambiguous mappings, and never guess unknown PUA characters. Preserve glyph definitions, spacing/font data, databases, and existing player items unless separately authorized.
- Locate every texture namespace before replacing a filename: `iconrank:noe.png` and `icontags:noe.png` are distinct glyphs with different display dimensions. Use the full original transparent artwork, not a screenshot or resized preview.
- For text theming, inspect TAB `config.yml`, `animations.yml`, and `groups.yml`, plus FancyHolograms text. Scan legacy `&e`/`&6`, hex-per-letter sequences, and MiniMessage gradients. A hex-only scan misses solid yellow command highlights and animated frames. Inspect other providers only when observed text points to them; AFK titles are not necessarily FancyHolograms.
- Inspect `server.properties` resource-pack URL and Nexo `Pack.server.type`/dispatch before generation. A static external pack can remain player-visible while Nexo generation succeeds. Compare archive contents before proposing replacement; absent customized assets make wholesale replacement unsafe.

## 2. Snapshot and transform safely

- Snapshot target text files and textures over SFTP with hashes. Prune models, libraries, player data, backups and inactive archives; record exclusions instead of claiming complete coverage.
- Decode YAML/JSON scalar escapes, not only literal UTF-8. Edit scalar source spans and quote replacements containing trailing `:`; assert parsed output equals the original with only intended string substitutions. Preserve commands, placeholders, locations, permissions, rewards and timings. Keep a small idempotence/semantic-equivalence self-check.
- Preserve color syntax: paired `<#HEX>...</#HEX>` tags need matching replacements; per-letter legacy colors must retain formatting codes. Avoid recoloring every hex value in a file: error colors and item rarity can share decorative palettes.
- Audit live LuckPerms with `lp export`, not stale `h2.json`. Split shared prefix contexts when changing one server, then verify fresh export with singleton context strings/lists normalized. Compare unrelated nodes semantically; disappearing default-only export users require investigation, not invented equality.
- For wordmark textures, crop transparent padding and preserve aspect ratio. Check the installed Nexo validator's glyph limit; when 512-wide exceeds 256×256, use 256-wide with proportional height. Tune glyph `height` and `ascent` independently: larger ascent raises artwork. Validate both scoreboard and TAB because one glyph can serve both.

## 3. Deploy and reload exact targets

- Stage with non-loading suffix and verify hashes. Keep texture backups outside external-pack trees: the importer tries to parse arbitrary backup suffixes there. Recheck originals immediately before activation and retain rollback copies.
- For JAR changes, stop and verify offline before activation; require fresh plugin-enable and Done logs after restart. For supported text/font-only changes, use native reloads rather than restarting the whole server: verified examples include `tab reload`, `fancyholograms reload`, `essentials reload`, `announce reload`, and `nexo reload pack`. Confirm registration for the installed version and read fresh completion logs.
- Read files back after initialization. DeluxeTags, ExcellentCrates, FancyHolograms and UnlimitedNameTags may reserialize YAML; compare parsed values before treating hash differences as corruption.
- Inspect generated ZIP textures and font providers, verify CRC/archive integrity, texture hashes, `height`, `ascent`, and glyph chars. Exclude backup/staging files from the pack. Generation success is not proof of player delivery.
- Permit generated atlas changes only after comparing parsed old/new JSON: adding a glyph namespace may extend an item-atlas filter. Assert the exact expected additive delta; preserve every other source and existing provider instead of allowing arbitrary atlas changes. Run validators separately from chained client setup commands so a later failure cannot masquerade as validator failure.
- During interrupted-client cleanup, identify Java clients by exact `--gameDir`, not any Minecraft process. Restore shared options/server-list bytes only when that gameDir is idle and the current delta matches the stopped worker; leave independently running clients and their workspaces untouched.
- Check native and namespaced plugin commands. Skript dummy commands and DeluxeMenus aliases can shadow `/dungeon`; preserve existing menus and identify a working alias rather than silently replacing gameplay.

## 4. Test the exact pack in a real client

- Use the graphical-client procedure in `minecraft-headless-testing.md`. When public delivery still points elsewhere, back up the isolated client's options/server list, decline the server pack locally, and enable the exact generated ZIP from its local resourcepacks directory. Verify the ResourceManager log names that ZIP and capture the rendered result. Restore client preferences after testing.
- Check full wordmark, margins, baseline, first text row, TAB header, and footer at native screenshot resolution. Keep logo, background and UI layers distinct. A selected item without glyph lore does not prove glyph rendering: hover a known mapped item and cross-check its configured placeholder.
- For DeluxeTags tests, inspect `/deluxetags:tags help` and grant only the new tag permission temporarily to the test account. `tags set` can reject an existing tag when that player lacks its permission. Capture both the hovered tag and current-tag tooltip, then clear the test selection and revoke temporary permission. Glyph `ascent: 40` can place artwork above the tooltip border; distinguish that from a missing glyph. Map `:` to X11 keysym `colon` when typing namespaced commands.
- Keep status claims separate: files changed, generation verified, local rendering verified, and public delivery verified. Never infer all four from one successful reload.

## 5. Capture hologram coverage without gameplay damage

1. Enumerate changed hologram IDs, locations, `linkedNpc`, visibility mode and text into a manifest before moving the camera. Check `PERMISSION_REQUIRED` first; an invisible permission-gated hologram is not evidence of a rendering bug. Preserve visibility policy and report gaps unless temporary scoped test access is authorized.
2. Use a dedicated bounded test account. Record original world, position, game mode and relevant state. Confirm alive/respawned state, move to a safe known location in the intended world, then establish spectator mode and verify it before approaching geometry. World transitions can reset game mode; do not assume a console success survives transfer.
3. Qualify both commands: `minecraft:execute in <dimension> run minecraft:tp <test-player> <x> <y> <z> <yaw> <pitch>`. Resolve the dimension from live state. Bare nested `tp` can invoke Essentials and change world semantics. Never target other players for camera work.
4. For linked NPCs, try saved yaw plus 180 degrees; for standalone tips, try saved yaw. Begin roughly 3–5 blocks away, then inspect one screenshot from each layout class. These are starting points, not guaranteed framing. Adjust angle/distance around pillars and stalls before batching; do not modify world geometry for screenshots.
5. Use F1 for unobstructed hologram evidence and a separate HUD-visible TAB/scoreboard capture. Wait for chunks/text updates. Crop relevant regions for inspection while retaining native originals; scaled contact-sheet coordinates are not original click coordinates.
6. Append captures incrementally by target ID. Track `captured`, `readable`, `occluded`, and `permission-gated` separately. Reframe failed views; count files and target IDs programmatically. Contact sheets aid review but cannot prove small text legibility. Label archives honestly as location captures when some target text remains unverified.
7. Restore account mode/location and client preferences; stop the client and display process. If a test accident changes inventory or other state, disclose and reconcile it rather than silently claiming a clean test.

## Completion report

Provide representative screenshots plus a labeled bulk archive when requested. State residual unknown glyphs, parser gaps, permission exclusions, existing unrelated pack errors, and whether the public pack changed. Do not replay already-handled process notifications when they add no new result.
