---
name: minecraft-menu-design
description: Use when designing Minecraft menus. Keep layouts tidy.
version: 0.1.0
author: BarzzLy, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
---

# Minecraft menu design

## When to use
- Create or change DeluxeMenus, plugin inventory GUIs, class/quest pages, or shops.
- User asks for tidy menus, smallfont, centered icons, or spacing.
- Apply to every affected page, not merely the first screenshot or one submenu.

## Design standard
- Treat user-approved CoinShop Tags layout as baseline: centered, symmetric groups, one horizontal slot gap, clear footer separation. Preserve an explicit new reference over this default.
- Inspect existing live config and supplied screenshots with read_file/vision_analyze before editing. Reuse established colors, glyphs, materials and navigation; do not invent a new visual theme.
- Use consistent Unicode smallfont for titles, labels, descriptions and feedback. Preserve color codes, placeholders, commands, URLs, permission nodes, identifiers and resource-pack glyph tokens exactly. Transform human text only.
- Use one empty top row; leave a full content-free spacer row before footer. Filler panes may occupy empty rows, but no actionable icons.
- Center one item at slot 13. For two/three/four items use 12,14 / 11,13,15 / 10,12,14,16 (zero-based). Four-row menus have 36 slots; footer actions at 28,31,34 with close centered at 31.
- For 11 items use 54 slots: 10,12,14,16; 19,21,23,25; 29,31,33. Row 36–44 is spacer; footer 45–53, back/close at 49. Do not cram 11 items into a smaller inventory merely to reduce rows.
- Use WHITE_STAINED_GLASS_PANE for content filler and BLACK_STAINED_GLASS_PANE for footer when matching existing CoinShop. Filler names blank, lore empty, lower display priority than products. Never obscure content icons.
- Keep lore short and ordered: category, blank line, purpose/usage, blank line, price or rewards, blank line, click instruction. Hide implementation details such as quest Tipe and raw console commands.
- Show actual configured rewards and costs; same category/tier uses consistent values if requested. Preserve distinct glyphs instead of replacing all names with generic text.
- Keep layout policy consistent across CLASS, confirmation, quest home and daily/weekly/class pages; updating only quest lists does not fix CLASS.

## Procedure
1. Snapshot exact live targets. Enumerate source entries into JSON; calculate included/excluded counts in code.
2. Choose smallest inventory size that preserves spacing. Check zero-based slots, unique product positions, footer bounds and filler priority.
3. Edit only requested menu behavior. Preserve economy amounts unless authorized; reuse existing prices where applicable and state them.
4. For shops, validate exact permission IDs, explicit LuckPerms boolean/context, ownership denial and sufficient-balance check. Close after purchase to discourage repeated clicks. Do not claim separate economy/permission commands form an atomic transaction.
5. Parse candidate YAML or compile plugin; leave a runnable layout/count check. Verify every requested page and item, not a subset.
6. Read back uploaded target, verify menu-specific reload or plugin activation. Do not restart for a reloadable menu-only change.

## MCPets CoinShop

- Derive pet IDs, ownership permissions, BRICK CustomModelData icons and ability lore from live MCPets definitions, never guessed display names. Grant base Permission plus every Skins.*.Permission for an all-skins mount bundle, explicitly true in server=noerpg context; avoid wildcard permissions that unlock unrelated pets. Forest Tusker and Red Raptor each currently have three named skins including base appearance.
- Mirror existing CoinShop balance/ownership checks and navigation without changing unrelated entries. Current DeluxeMenus purchases use separate LuckPerms permission grants and PlayerPoints deductions; closing menus and ownership checks do not make the two providers atomic. Disclose purchase-test and transaction limitations rather than claiming crash-safe or duplicate-proof delivery.
- Register new submenu in DeluxeMenus config, upload submenu before parent link/registration, reload natively, verify dm list plus exact live YAML. User rejected six pets arranged as three narrow pair rows and a standalone ARROW Back. Prefer 45 slots: pet categories in columns 11/20 (cosmetic), 13/22 (attack), 15/24 (mount); top row empty, 27–35 spacer, footer 36–44 and Back 40. User also rejected the seven-category parent 4+3 layout (10/12/14/16 then 20/22/24). Do not treat mathematical symmetry as visual approval. After repeated layout rejection, inspect real external in-game references and show a preview for direction approval before another live redesign; leave current menus unchanged during reference selection.
- Match navigation to existing live submenu's material/model, name, sound and action rather than choosing a generic arrow. If reference contains malformed/truncated texture data, preserve its identifier literally when explicitly matching current behavior, disclose validation gap, and do not invent a repaired token or claim a valid texture. Config equality and successful reload are not rendered-client proof; request a fresh screenshot when no authorized visual client exists.

## Pitfalls
- A horizontal gap does not solve content pressed against footer; reserve vertical spacer too.
- Never convert entire YAML to smallfont; technical tokens must remain executable.
- Never copy retired shop tag permissions when live DeluxeTags defines different IDs.
- Client connected to proxy lobby may report unknown commands; confirm intended backend before diagnosing GUI failure.
- Protocol inventory data proves rows/slots/lore, not rendered resource-pack appearance. Label visual verification separately.

## Verification
- Compare source count, selected IDs and exclusions programmatically; save manifest.
- Check all titles, slot counts, product positions, spacer and footer placement.
- Check smallfont consistency, preserved glyph/placeholder tokens, unchanged prices and correct actions.
- For live client tests, subtract player inventory from window slot count; verify each submenu and navigation. Do not spend real player currency for syntax testing.
- Report config/reload, live protocol, rendered visuals and actual purchase tests separately. Stop test clients after checks.
