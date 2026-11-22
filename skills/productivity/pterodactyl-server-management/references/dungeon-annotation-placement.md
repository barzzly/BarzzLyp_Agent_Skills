# Dungeon annotation placement and config-only expansion

- Read Sketchfab embed HTML and HTML-unescape its hotspot JSON to recover annotation names, order, and positions; do not infer room names from broad floor bands.
- Cross-check annotation coordinates against user-owned terrain materials. Annotation positions can float or intersect glass/slabs; choose safe standing cells separately. Require support/headroom and distinguish point safety from proven traversal.
- Do not use a ceiling-within-28-blocks interior filter as the only geometry source; it omits tall halls and balconies.
- Preserve original chest block-entity positions. Bind every chest block to personal locked loot; adjacency alone does not prove double-chest state. Check block-state type: an unmatched adjacent chest can expose vanilla inventory.
- Discover added chest candidates from actual floor palettes and room geometry. Require solid support, headroom, nearby wall/ceiling, and an adjacent broad supported approach; otherwise a point may be safe only as a parkour jump pillar.
- Distribute exploration chests with per-area quotas and minimum spacing across elevations, wings, corridors, and perimeter alcoves; a larger count clustered beside bosses does not satisfy this user's exploration preference.
- Keep optional secrets out of mandatory objective chains and navigation waypoints. Native ENTER_REGION triggers use params.region and once:true; a subtle sound can mark discovery without revealing locations. A discovery trigger does not prove a constructed hidden room or accessible route.
- Use separate low-value exploration loot tables for large chest expansions; otherwise multiplying containers also multiplies premium rewards. Preserve original chest loot and encounter balance unless requested.
- Reserve mob spawn, boss spawn, arrival, original chest, and altar coordinates before placing new chests. Assert no solid gate occupies spawn/teleport cells and no altar shares a chest.
- Final wave must explicitly COMPLETE_OBJECTIVE for WAVE_COMPLETION; wave chaining alone does not advance objective.
- Snapshot fresh live YAML and inspect active sessions before editing. For chest-only work, assert waves, bosses, waypoints, original chests, and objective chains unchanged; otherwise a builder can silently restore stale encounter config.
- Use installed NoeDungeon JAR's DungeonSerializer.load(id, yaml) and DungeonValidator for exact headless validation. Update expected harness counts when expanding content and propagate process failures; a stale count assertion is not a validation pass.
- Deploy only affected files after backup and concurrency comparison, byte-read back targets, reload, then run live validation. Read all config files after enable: serializer rewrites multiple files, so prior hashes become stale.
- Verify final name, enabled state, chest totals, discovery-trigger totals, and preserved encounters programmatically. Supply an updated placement plan; report geometry checks separately from untested jump paths, secret access, and complete gameplay.
- Do not substitute teleport checkpoints for a requested original parkour route. Report jump/access paths untested unless client traversal verifies them.
- Clone Cuboss skill references into dungeon namespace when summons must use no-drop minions. Remove direct commands and codex/death rewards only from new variants, never shared pack.
- Keep dungeon display name exact; retaining existing dungeon ID avoids duplicate entries and lost progression unless user requests ID migration.
