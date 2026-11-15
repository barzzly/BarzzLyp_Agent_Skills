---
name: blockbench-modeling-workshop
description: Use when creating or modifying Blockbench models, textures, or animations. Preserve originals, use native codecs, render and validate exports.
metadata:
  hermes:
    tags: [minecraft, blockbench, modeling, textures, animation]
    category: creative
---

# Blockbench modeling workshop

## Safe iterative work
- Inventory source models and hash originals before editing. Work on derivative copies in a separate workspace; do not deploy or publish vendor assets without authorization.
- Use real https://web.blockbench.net/ editor for import, editing, preview and export. Save actual `.bbmodel` artifacts, not scripts or logs alone.
- Distinguish Generic/ModelEngine animation from vanilla Java static item exports. Generic animation is not automatically compatible with vanilla item JSON.
- Keep experiment history in workspace journal. Record only verified reusable techniques in this skill; never store private endpoints, credentials, proprietary texture data, or operational paths here.

## Native model workflow
1. Inspect the source format and intended consumer. Hash source files; make a working copy before editing.
2. Open/import through Blockbench's native codec. Inspect hierarchy, geometry, texture dimensions/alpha, UVs and animation count before changes. For v5, `groups` metadata is separate from `outliner`; preserve UUID relationships and hierarchy.
3. Make one concrete change at a time. Preserve unrelated geometry, texture pixels, IDs and animation clips. For animated models, sample native timeline poses at representative times and inspect world transforms rather than relying only on local Euler values.
4. Render front, side, quarter and thumbnail views. Measure alpha bounds and framing; inspect silhouette, proportions, UV stretching, pivots, clipping and readability. Structural counts do not prove visual quality.
5. Compile/export with the native codec, then reimport the saved artifact. Compare element/group/texture/animation counts, IDs, texture data and keyframes against the intended derivative. Keep vanilla Java item JSON and PNGs distinct from editable `.bbmodel` animation deliverables.
6. Package only requested files. Verify every texture reference, ZIP CRC, entry count, documented archive path and embedded texture byte equality. Preserve the original source.
7. Report structural tests, visual review and live Minecraft compatibility as separate evidence. A valid export does not prove in-game rendering or behavior.

## Verified Blockbench browser workflow (v5.1.6)
- Navigate to `https://web.blockbench.net/`, wait for load, inspect `page_info()` and `typeof Codecs`. Session pages may reset to about:blank; batch navigation, import, edits and export in one browser call when needed.
- Load native project data with `Codecs.project.load(model, {path:'copy.bbmodel'})`. Inspect `Outliner.elements`, `Group.all`, `Texture.all` and `Animation.all`.
- Wait for texture images before canvas edits. Preserve alpha with ImageData processing; apply a changed canvas with `texture.fromDataURL(canvas.toDataURL('image/png'))` and inspect `texture.error` after reload.
- Create animations through native `Animation` and keyframes (`channel`, `time`, `interpolation`, `data_points`). Sample using `Modes.options.animate.select(); Timeline.setTime(t); Animator.preview()` and read transformed meshes. A sampled pose proves evaluation, not attractive visuals.
- Compile via `Codecs.project.compile({raw:true, bitmaps:true, absolute_paths:false})`. Reimport saved output and compare counts and errors. Do not handcraft old v4 layouts for v5 projects.
- Capture the actual viewport and inspect image bounds. A successful PNG export can still contain an empty or tiny subject. Ensure tab is visible for playback; hidden tabs may suspend requestAnimationFrame. Explicit timeline sampling is a fallback, not visible continuous playback.
- Chunk large model JSON across browser calls if evaluator payload limits are hit. Do not return cyclic native objects over CDP; return scalar summaries.

## Model and texture craft
- Establish silhouette first, then one primary focal feature, secondary structure and quiet tertiary seams. Repeated rails/brackets need consistent thickness and spacing; every brace should visibly connect to a mount.
- For pixel art, inspect opaque pixel rows and alpha at native resolution. Use nearest-neighbor enlargement only for review; preserve native-size delivery and transparency.
- Avoid coplanar overlaps, floating parts, accidental tangencies and texture flecks. Verify supports/contact in native renders; parent hierarchy alone does not establish visible connection.
- For animated geometry, inspect intermediate keyframes and transform behavior, not only start/end. Preserve camera-matched evidence when comparing poses; independently auto-fitting every frame can hide motion.

## Java item JSON and textures
- Import Java item/block JSON with `Codecs.java_block.load(...)`; resolve `namespace:path` to matching `assets/<namespace>/textures/...png`, including aliases and parent inheritance.
- Bind imported textures explicitly with `Texture.all.find(t=>t.id===id).fromDataURL(dataURL)`; preserve face UUID mapping. Validate `textures.particle` separately.
- Preserve `.png.mcmeta` sidecars for animated vertical strips. Check frame dimensions/count/frametime and verify native texture animation samples across a frame boundary.
- Export with `Codecs.java_block.compile({raw:true})`. Verify every emitted texture link, transform and sidecar. Effective identity transforms may be omitted by native serialization.
- Java item JSON and editable BBModel are separate deliverables. Skeletal animations do not transfer into vanilla Java item JSON.

## Evidence and delivery limits
- Check preview alpha bounds immediately. If MediaPreview export is blank, reimport the saved model and capture `Preview.selected` instead; preserve failed evidence and do not treat export success as visual proof.
- Set projection before camera position when switching to orthographic; resize and read back the active camera. Fit using rendered alpha bounds rather than invisible geometry bounds.
- For small images, inspect opaque pixels and palette; RGB under alpha=0 is not visible color. Composite transparent sources on neutral backgrounds for review.
- Preserve source artifacts until derivative is reviewed. User design approval is not deployment approval or proof of Minecraft runtime compatibility.
- Clean only browser resources owned by the current task; avoid broad process-kill patterns.
