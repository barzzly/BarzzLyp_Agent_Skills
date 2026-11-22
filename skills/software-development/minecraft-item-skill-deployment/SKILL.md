---
name: minecraft-item-skill-deployment
description: Use for Minecraft item skill deployment and reload checks.
version: 1.0.0
author: BarzzLy
platforms: [linux]
metadata:
  hermes:
    tags: [minecraft, mythicmobs, nexo, items, skills, pterodactyl]
    category: software-development
---

# Minecraft Item Skill Deployment

Use for remote MythicMobs/Nexo item interactions, custom-model matching, and reload-only fixes.

## Procedure

1. Resolve target server from live inventory and confirm active remote path. Do not infer from local snapshots.
2. Read complete target skill and item definition before editing. Identify base material, model value, item ID, trigger command, and reward skills.
3. Save local backup of exact remote file before writing. Keep backup path in result.
4. Prefer documented MythicMobs item conditions and item matchers. For custom-model matching, use `custommodeldata{m=<value>}` when supported by installed version; otherwise compare documented item model placeholder, for example `stringequals{val1=<caster.held.item.model>;val2=<value>}`. Do not invent placeholder names or debug substitutions.
5. Remove temporary diagnostic skills before final deployment. Debug output that prints unresolved placeholders is not proof of a working trigger.
6. Write smallest YAML change. Read exact remote file back and compare with intended content before reload.
7. For Nexo item clicks that launch MythicMobs, use a console command mechanic such as `mm m spawn -p %p% <animation_mob>`; verify the installed Nexo placeholder against working items. `<player>` can remain literal and produce `Player <player> not found`. Let the spawned mob `sudoskill` the reward skill as the nearby player. This avoids player-permission and Mythic skill-command registration gaps.
8. Put card animation in a short-lived invisible ArmorStand mob: custom item in `Options.ItemHead`, `spin`, particles/sounds, then `remove{delay=...}`. Keep reward timing in the skill with explicit delays; Nexo `one_usage` handles item consumption.
9. Run narrow plugin reload command, not server restart, unless restart is explicitly approved. Read fresh log segment after reload; require successful skill loading and no new configuration errors.
10. If user declines bot/client testing, stop after reload and log verification. Report runtime behavior as untested; never claim item consumption or reward rolls were verified.

## Rules

- Preserve power state and unrelated packs. Scope edits to named skill/item files.
- Separate config-load verification from gameplay verification: clean reload proves syntax and registration, not trigger behavior or reward distribution.
- Keep reward pools and probabilities unchanged unless explicitly requested; matching fixes must not alter loot semantics.
- Use installed plugin syntax and version, because similarly named conditions can be absent or differ across MythicMobs releases. A clean reload with `custommodeldata` rejected means remove that condition, not leave a broken skill registered.
- Keep Nexo custom item ID syntax out of MythicMobs `holding{m=...}` unless installed adapter explicitly supports it; invalid `nexo:<id>` matchers can prevent the entire skill from loading.
- When matching an existing gacha animation, inspect its full skill, preview mob, item model geometry, display transforms, front/back textures, and reveal timing. Copy the working motion instead of inventing particles or spin durations. Preserve reward pools and consumption semantics.
- Inspect the regenerated ZIP mapping, not only YAML: `Pack.texture` produces a generated flat item; `Pack.model` must map to the intended card geometry. Preserve custom model identifiers. Check every referenced texture exists.
- Separate pack generation from client delivery. With Nexo hosting `NONE` and dispatch disabled, reload does not distribute the ZIP. Inspect the actual server resource-pack URL; do not claim client visuals are fixed before the new pack reaches that client. Do not change global hosting or server.properties without scope approval.
- Report exact remote path, backup path, reload result, fresh-log result, and remaining test gap in terse bullets.
