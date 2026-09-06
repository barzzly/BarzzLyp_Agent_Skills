---
name: minecraft-asset-pack-assembly
description: Use when assembling Minecraft plugin asset packs.
version: 1.0.0
metadata:
  hermes:
    tags: [minecraft, assets, itemsadder, modelengine, mythicmobs, mmoitems]
    category: productivity
---

# Minecraft Asset Pack Assembly

Build clean, deployable plugin data from vendor archives while preserving asset identities and plugin layout.

## Procedure

1. **Inventory before extraction**
   - List outer and nested ZIP members with Python `zipfile`; count files, unpacked bytes, top-level roots, and directory trees.
   - Treat each nested ZIP as one vendor package. Reject path traversal (`..` or absolute paths) before writing.
   - Inspect a known-good reference pack for structure only. Never copy its unrelated assets or runtime state into result.

2. **Choose deployable plugin variants**
   - Keep only plugin formats present in target stack, commonly `ItemsAdder`, `MMOItems`, `ModelEngine`, `MythicLib`, and `MythicMobs`.
   - Exclude alternate delivery formats such as Oraxen/Nexo, raw player resource packs, MythicRPG, documentation, macOS metadata, and nested archives when equivalent expanded files are retained.
   - For MythicMobs packages offering alternatives, select one compatible variant. Prefer explicit MMOItems/MMOCore damage variants over Crucible variants unless Crucible is requested.

3. **Normalize destination layout**
   - Put ItemsAdder namespaces under `ItemsAdder/contents/<namespace>/`; normalize legacy `ItemAdders` or namespace-only layouts.
   - Put ModelEngine sources under `ModelEngine/blueprints/`.
   - Put MMOItems definitions under `MMOItems/item/` and MythicLib skills under `MythicLib/skill/`.
   - If source MythicMobs contains `pack/` or `packs/`, place its contents under `MythicMobs/packs/`; never leave a separate top-level pack directory.
   - Put non-pack MythicMobs files under standard `items/`, `mobs/`, and `skills/` roots. Isolate package folders when filenames might collide.

4. **Merge without breaking identifiers**
   - Merge same-type YAML files only at document boundaries and preserve source comments for traceability.
   - When user wants one weapon registry, merge every weapon definition into `MMOItems/item/sword.yml` and remove now-empty type files; count semantic weapons by top-level YAML IDs, not source ZIP count.
   - Treat alternate/upgrade definitions as separate weapons unless user designates one as upgrade-only. If exact roster count is required, remove unwanted definition plus matching ItemsAdder item entry, model, and texture—not YAML alone.
   - For every weapon, cross-check MMOItems `material` + `custom-model-data` against ItemsAdder `resource.material` + `model_id`. Both fields form resource-pack predicate; mismatches can render another weapon's texture even when model JSON is correct.
   - If all weapons must share one base material, change that material consistently in MMOItems, ItemsAdder, and any MythicMobs item definition while preserving unique model IDs.
   - For custom sounds, resolve each MythicMobs `sound{s=...}` call against ItemsAdder `assets/<sound_namespace>/sounds.json`. Prefix event with namespace (`<namespace>:<event>`) when the JSON lives outside `assets/minecraft/`; an unqualified event otherwise resolves as vanilla namespace and stays silent.
   - Hash colliding binary/model files first. Drop byte-identical duplicates.
   - Never resolve differing `.bbmodel`, texture, sound, or YAML collisions by appending filename suffixes alone; configs usually reference original IDs, so renamed files become unreachable. Keep one only when assets intentionally share that ID. Otherwise isolate whole package and update every reference, or stop and report conflict.

5. **Clean and verify**
   - Remove empty directories, metadata, redundant nested ZIPs, docs, and unused plugin variants.
   - Assert expected top-level directories, no zero-byte files, no unexpected archives, no empty directories, and every MythicMobs pack path starts with `MythicMobs/packs/`.
   - Parse all YAML, parse every `.bbmodel` as JSON, and verify every retained custom sound event exists in its `sounds.json` under the namespace used by MythicMobs.
   - Assert requested weapon count from top-level keys in final MMOItems file, unique model IDs where required, and exact material/model-ID parity with ItemsAdder configs (see `references/rpg_pack_audit_matrix.md`).
   - Validate MMOItems ability cooldown keys: reject `skillcooldown:` in MMOItems ability blocks (which MMOItems ignores, falling back to 0.0s spam loops) and require standard `cooldown: <seconds>`.
   - Run combat rotation simulation across weapons (100s at 20 TPS) to catch runaway DPS (> 50 DPS on base tiers) and packet flood risks (> 25 packet events/sec).
   - Verify multi-phase boss encounters use persistent Aura phase locks (`duration=999999`) and `bulletType=DISPLAY` with bounded `md` ticks to protect server TPS.
   - Write machine-readable report containing source-package counts, semantic weapon count, final counts by plugin, skipped variants, collision policy, and unresolved conflicts.

6. **Package for delivery**
   - ZIP parent folder so archive extracts as one named directory.
   - Run `ZipFile.testzip()` and verify archived file count equals staged file count before sending.

## Standing Rules

- User wants finished folder shaped like working reference pack, not copied reference assets.
- User prefers one consolidated `MMOItems/item/sword.yml` for this weapon-pack class; preserve only explicitly requested roster entries.
- When sending a fix-only archive, include only files actually changed plus unavoidable shared registries; do not resend every asset for that class unless user requests a standalone ready-to-install pack.
- Delete unused raw/vendor alternatives from final output; keep original source archives untouched unless explicitly asked.
- Prefer deterministic Python `zipfile` processing over manual extraction for nested archives, path safety, counting, and verification.
- Always perform 4-way cross-verification (`MMOItems` -> `ItemsAdder` -> `MythicLib` -> `MythicMobs`) before deploying, ensuring custom-model-data parity and valid ability cooldown numeric values.
