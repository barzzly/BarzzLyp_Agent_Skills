---
name: minecraft-asset-pack-consolidation
description: Use when merging raw Minecraft packs into plugin folders.
version: 1.0.0
platforms: [linux]
metadata:
  hermes:
    tags: [minecraft, itemsadder, modelengine, mythicmobs, mmoitems, mythiclib]
    category: productivity
---

# Minecraft Asset Pack Consolidation

Build one deployable plugin-folder tree from nested vendor archives, using an existing finished pack as structural reference.

## Procedure

1. Inspect archives without extracting first. Count files, unpacked bytes, roots, and nested ZIP structure with Python `zipfile`.
2. Treat finished pack as layout reference only. Never copy its unrelated assets into output.
3. Recursively inspect each vendor ZIP. Ignore `__MACOSX`, AppleDouble `._*`, documentation, terms files, and player-only resource packs.
4. Keep only plugin data required by target stack:
   - `ItemsAdder`: retain `contents/<namespace>/`; normalize old `ItemAdders/<namespace>` or direct namespace layouts to `ItemsAdder/contents/<namespace>`.
   - `ModelEngine`: retain `blueprints/` only. Skip generated resource-pack output.
   - `MMOItems`: retain `item/*.yml`; merge definitions when multiple packs use same item-type filename.
   - `MythicLib`: retain `skill/*.yml`.
   - `MythicMobs`: select MMOItems/MMOCore-compatible variant when vendor includes alternatives. Prefer `MythicMobs (Only Damage Mobs)`, then combined `MythicMobs (MMOCore, MMOItems)`, then plain `MythicMobs`; avoid Crucible variant unless requested.
5. Put any source `MythicMobs/pack` or `MythicMobs/packs` content directly under `MythicMobs/packs/`. Preserve pack directory and `packinfo.yml`.
6. For non-pack MythicMobs configs, place files under standard category roots (`items`, `mobs`, `skills`) and isolate each vendor asset in a named subfolder to avoid filename conflicts.
7. Handle collisions deliberately:
   - Identical files: keep one.
   - MMOItems YAML sharing item-type filename: concatenate whole top-level definitions with source comments.
   - Shared ModelEngine `Extras`: keep original filename from first copy; do not invent suffixed model filenames because MythicMobs references model IDs by filename. Record conflicts for review.
8. Remove nested archives after expanded content is present, then remove empty directories.
9. Normalize naming only after functionality is assembled. Mirror reference conventions (`ItemsAdder/contents/SL_*`, `ModelEngine/blueprints/SENJATA LEGEND/<class>`, `MythicMobs/{items,mobs,skills}/Senjata Legend/<class>`), but never rename `.bbmodel` files because MythicMobs uses filenames as model IDs.
10. Run static preflight before packaging:
   - Parse every `.bbmodel` as JSON and confirm texture sources are embedded before removing sibling source images.
   - Parse every YAML file.
   - Index top-level MythicMobs IDs across files and report duplicates.
   - Index `skill{s=...}` calls and report definitions missing from all supplied variants and reference pack.
   - Detect mutually exclusive `MMOCORE` and `MMOITEMS` files; retain only target backend.
11. Write JSON report with source packages, output counts, byte size, removed files/calls, unresolved dependencies, collisions, and collision policy.

## Verification

Assert all before completion:

- Output root contains only expected plugin folders.
- No nested ZIP/RAR/7z archives remain.
- No empty directories or zero-byte files remain.
- Every MythicMobs pack path begins with `MythicMobs/packs/`.
- File totals and per-root totals come from programmatic scan.
- Every `.bbmodel` parses as JSON; only `.bbmodel` remains under ModelEngine blueprints when all textures are embedded.
- Every YAML file parses without error.
- No unintended duplicate top-level MythicMobs IDs remain across integration variants.
- Missing MetaSkill calls are either supplied, explicitly removed with report, or documented as external dependencies.
- ZIP final folder, reopen archive, run `testzip()`, and verify entry count before delivery.
- If user supplies runtime log, compare post-fix log paths against output layout; an old path proves server still runs prior deployment.

## Pitfalls

- Vendor packs commonly contain several mutually exclusive MythicMobs variants. Copying every variant causes duplicate mob and skill IDs.
- Renaming colliding `.bbmodel` files does not resolve runtime conflicts; references still target original model ID.
- Vendor `ModelEngine/blueprints` may contain `.png` and `.aseprite` source files beside `.bbmodel`. When every bbmodel texture has embedded `data:image/...` content, remove non-bbmodel files; ModelEngine otherwise attempts to import them as models and emits `Unknown format` for each file.
- MMOItems and MMOCore MythicMobs skill files are alternatives, not additive. Keeping both duplicates nearly every top-level skill ID; select one integration variant.
- Vendor YAML can reference helper MetaSkills absent from every supplied variant. Search all nested archives before removing unresolved invocation lines, and record each removal.
- ItemsAdder duplicate-image reports can include intentional emissive base/`_e` pairs and generated ModelEngine resources. Do not delete these based on hash alone; distinguish warnings from conflicting resource paths.
- ItemsAdder vendor bundles sometimes include a duplicate namespace ZIP beside expanded files. Keep expanded files, remove nested ZIP.
- Do not copy Oraxen/Nexo or raw player resource packs when ItemsAdder is selected; these are alternate deployment formats, not extra required assets.
- Separate pack defects from server configuration. ItemsAdder's `please remove the resource-pack setting` comes from root `server.properties`, not plugin asset files; inspect live server properties and report required changes separately.
- MythicMobs Free rejects premium numeric math, variables, and random placeholders. Do not rewrite hundreds of expressions into guessed constants; require Premium or explicitly accept reduced functionality.
- ItemsAdder missing textures from namespaces absent in assembled pack usually belong to pre-existing server content. Do not add unrelated reference assets merely to silence that error.
- `Eye height is below 0` and `Missing hitbox` are model-author warnings. Preserve model behavior unless user requests visual/collision edits; classify them separately from load failures.
- **Never delete held items to simulate hiding (`removeHeldItem`)**: Vendor skills sometimes include `- removeHeldItem{a=1}` paired with a console give command to hide weapons during stealth/dash skills. On MMOItems/Paper servers, this permanently destroys player custom items or fails for non-op players. Strip `removeHeldItem` and command compensation entirely.
- **MythicMobs `Cooldown:` headers reject MythicLib placeholder expressions**: Expressions like `Cooldown: <modifier.skillcooldown>` parse as `0.0` in MythicMobs YAML headers. Under MMOItems `mode: SNEAK` or click triggers, zero cooldown causes the skill to fire every tick (20x/sec), flooding packets, resetting swing animations, and causing the client's held weapon to visually vanish. Replace `<modifier.skillcooldown>` with explicit numeric second values matching item balancing.
- **MMOItems `ability` sections require `cooldown:`, not `skillcooldown:`**: Placing `skillcooldown: 3` inside MMOItems ability definitions is ignored by MMOItems, defaulting the ability cooldown to 0.0s. Always use standard `cooldown: <seconds>`.
- **Companion pet maintenance auras must exceed MMOItems timer intervals**: When pets run despawn checks against holder auras (e.g. `hasaura{n=ISHOLDINGTOME} false`), the aura duration must comfortably exceed the MMOItems `timer:` interval (e.g. `duration=120` [6s] for a 3s timer). Short durations (e.g. 15 ticks) cause the pet to despawn 0.75s after spawning and loop endlessly.
- **Audit minion AI timer frequencies**: Minions spawned by skills must not have rapid projectile loops (e.g. `~onTimer:5 0.5` or `repeat=199`). Clamp minion attack timers to sane frequencies (`~onTimer:60`-`~onTimer:80`), enforce skill cooldowns, and prevent multiple active instances unless explicitly designed as swarms.
- **Never wipe live plugin root folders during deployment**: `plugins/ItemsAdder/contents` and `plugins/MMOItems` host existing server cosmetics, ranks, and third-party sets. Deploy only to strict pack allowlist namespaces (e.g. `SL_*`), never using blanket recursive directory removal.
