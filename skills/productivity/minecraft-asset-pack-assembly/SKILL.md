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

## Badge and glyph artwork previews

- For nametag overlap, inspect PNG alpha bounds before altering size. Full-height reconstructed glyphs with `ascent < height` extend below their row and collide with subsequent normal text; increasing ascent to unchanged height raises them while respecting vanilla `ascent <= height`. Padded artwork may need a small decrease instead. Compare each target in a native multiline TextDisplay, distinguish logo lettering from subsequent name/team rows, and reframe tall artwork rather than accepting cropped screenshots. Label isolated fixtures separately from live nametag-plugin verification.
- Rebuild compatibility from a freshly regenerated server ZIP when live assets changed; reapply only verified compatibility deltas from the fixed pack. Assert regeneration changes only intended font metrics, preserve textures/IDs and both model formats, and keep the 26.x text-font fix. Generation, local output, and public URL deployment are separate gates.

- For screenshot-only reconstruction, distinguish flattened RGB promotional previews from original RGBA textures before promising fidelity. Inventory every requested tag; preserve originals and label recovered textures as reconstructions. Occluded pixels and original alpha cannot be verified from flattened previews.
- If vision requests return HTTP 413, make a separate JPEG preview at at most 768 pixels on the longest edge, quality 80; retry that preview. For small details, use tightly cropped original-resolution regions instead of enlarging the full image. Never replace source files with reduced previews.

1. Resolve the exact target texture before drawing: tag and rank namespaces can contain identically named PNGs with different dimensions. Read source dimensions, RGBA alpha bounds, and glyph height/ascent when available; do not substitute the website wordmark for the in-game tag by filename alone.
2. Inspect the original at native size and an integer nearest-neighbor enlargement. Tiny stylized lettering is easily misread; confirm the actual letters before redesigning. Inspect current brand artwork separately for palette and style.
3. Preserve the requested canvas dimensions and transparency. Match apparent footprint and baseline as well as canvas size; check alpha bounds after downsampling because antialiasing can expand edges or clip bottom ornaments.
4. For Noesantara tag concepts, follow current requested lettering: user rejected generic block `NOE` and requested only `N`, with ornate detail comparable to original noetags. Prefer extracting/masking actual crystalline N from current logo over inventing a font. Use royal blue `#0038FF` with icy `#90E0F0` highlights and intricate ocean curls instead of feathers; avoid broad flat swooshes. Treat each revision as unapproved until user accepts.
5. Use Pillow for small deterministic artwork when sufficient: draw letter masks and sampled curves at higher resolution, apply gradients through masks, then downsample once with LANCZOS. Inspect the final native-sized PNG, not only the large working drawing; keep letter counters and dark separations legible.
6. Deliver a preview sheet with nearest-neighbor enlargement plus true-size samples on dark and light backgrounds. Label exact pixel dimensions and retain a separate transparent PNG; the opaque preview sheet is not the deployable texture.
7. When the user asks for preview first, stop after sending the preview. Do not upload, regenerate the resource pack, change glyph settings, or restart the server until separate installation approval. State clearly that the concept is not installed.

## Reconstructing badges from flattened promotional images

- Inventory and hash source bytes before processing; distinguish covers, detail screenshots, and actual transparent textures. Account for every requested label programmatically and verify ambiguous lettering with full-resolution crops rather than thumbnail OCR.
- When image inspection rejects large PNG payloads, create <=768px JPEG previews and separate small full-resolution detail crops. Keep sources untouched.
- Use guided silhouette masks plus selective scene-color removal; global sky/cyan keying can erase opaque pale ice and wing interiors. Restrict ambiguous color removal to silhouette edges, protect interiors, and inspect source-versus-cutout comparisons before accepting results.
- Preserve genuine detached ornaments. For translucent bubble rings, remove scene-filled centers but document uncertain rims; never invent hidden segments and call them recovered.
- Label chosen downsampled dimensions as reconstruction-native, not original vendor resolution. Retain high-resolution masked references, disclose omitted glow and edge-color uncertainty, and distinguish complete roster reconstruction from exact original recovery.
- Preview every asset at 1x and integer nearest-neighbor zoom on both light/dark backgrounds; size rows for the tallest sprite so preview clipping cannot masquerade as missing artwork. Verify RGBA alpha extrema, trimmed nonempty bounds, zero RGB under transparent pixels, config paths, source hashes, and archive member count/bytes.
- ItemsAdder font images use `contents/<namespace>/textures/font/<name>.png` with `font_images` entries containing `path: font/<name>.png`, `scale_ratio`, and `y_position`. Verify against current official docs. Large ornate badges need taller initial metrics than chat icons; document client-untested baseline and nametag integration separately. Do not assume ItemsAdder-assigned glyphs match a standalone vanilla font's codepoints.

## Real-client compatibility testing

- Test title and Options menu text, not only world glyphs/items. Nexo `rendertype_text.vsh` from 1.21.11 uses `texelFetch(Sampler2, UV2 / 16, 0)`; applying it to 26.1.2 (resource format 84.0) reproduces blank UI labels even on vanilla. Bound that legacy overlay to formats 75–76, matching the reference pack; 26.x then uses vanilla text shaders. Verify before/after on the same client and exact pack bytes. This disables that overlay's animated glyph effect on 26.x; do not claim Lunar validation from a vanilla test.

- Keep one graphical client active and record actual ZIP hash and ResourceManager reload stack per version. Declining a server pack tests local rendering only. Multiple accepted server packs can override candidate assets; verify downloaded bytes and precedence rather than assuming the newest request replaced old packs.
- Capture native plugin menus plus held item, readable scoreboard and actual summoned pet. A summon message or invisible base entity is not visual proof. Body-follow pets can stay outside first-person view; inspect third-person front view before changing pack/server settings. Distinguish missing model from camera position and pet configuration.
- Use exact `minecraft:tp` within `execute`; unqualified `tp` can resolve to Essentials. Clear chat input before typing after interrupted UI actions, and confirm actual menu state after each step.
- On low-memory software-rendering VPSs, test bounded client heap and one version at a time. Exit -9 proves forced termination, not OOM without kernel evidence. Do not count black screenshots or a launch helper's READY marker as gameplay success.
- Back up and update matching official ViaVersion/ViaBackwards versions before testing newly released clients; check ViaRewind compatibility too. Read fresh startup logs and active JAR hashes. A literal `${version}` in plugin metadata can defeat a version-string readiness check despite successful startup; report it and verify independently.

## Standing Rules

- User wants finished folder shaped like working reference pack, not copied reference assets.
- User prefers one consolidated `MMOItems/item/sword.yml` for this weapon-pack class; preserve only explicitly requested roster entries.
- When sending a fix-only archive, include only files actually changed plus unavoidable shared registries; do not resend every asset for that class unless user requests a standalone ready-to-install pack.
- Delete unused raw/vendor alternatives from final output; keep original source archives untouched unless explicitly asked.
- Prefer deterministic Python `zipfile` processing over manual extraction for nested archives, path safety, counting, and verification.
- Always perform 4-way cross-verification (`MMOItems` -> `ItemsAdder` -> `MythicLib` -> `MythicMobs`) before deploying, ensuring custom-model-data parity and valid ability cooldown numeric values.
- **Multi-Version Resource Pack & ModelEngine Overlay Compatibility (1.20.1 to 26.x+)**:
  - Minecraft 1.20.1 (`pack_format: 15`) does not support `overlays` in `pack.mcmeta` (introduced in 1.20.2 / `pack_format: 18`); vanilla 1.20.1 clients strictly ignore overlays and read only root `assets/`. When ModelEngine places item overrides (e.g. `player_head.json`) inside an overlay directory like `modelengine_1_19_4/`, copy it directly to root `assets/minecraft/models/item/player_head.json` so 1.20.1 clients load model definitions without errors.
  - Use `pack_format: 15` for 1.20.1 plus legacy `supported_formats` and modern `min_format`/`max_format` bounded to actual targets. Declaring 32767 only suppresses compatibility warnings; it does not guarantee future rendering. Verify official Mojang manifest and downloaded client `version.json`; never guess snapshot/release format numbers. In mixed legacy/modern packs, every overlay needs `formats`, including modern-only entries, or modern clients can reject the entire pack.
  - Port modern shader overlays from the exact target's official vanilla shaders, preserving OIT, glint, explicit attribute locations and game includes. Java 26.3 release uses resource format 97.1; its shaders use `#include` and `gl_VertexIndex`, not legacy `#moj_import`/`gl_VertexID`. Transplant only ModelEngine-specific displacement/fading and verify actual client pipeline compilation; compilation alone does not prove entity rendering. Never label a candidate complete until live items, pets and fonts are visually checked.
  - Always maintain dual item model formats in the pack root: `assets/minecraft/models/item/<item>.json` (predicate overrides with `custom_model_data` for 1.20.1 - 1.21.3 clients) alongside `assets/minecraft/items/<item>.json` (data-driven format for 1.21.4+ clients). Skipping either breaks rendering for that client range.
