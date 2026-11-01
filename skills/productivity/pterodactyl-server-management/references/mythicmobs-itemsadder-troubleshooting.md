# MythicMobs and ItemsAdder Runtime Troubleshooting

## MythicMobs EquipMechanic Drop Type Resolution
- `equip{item=<name>:<slot>}` resolves `<name>` strictly against `MythicMobs/Items/` (or vanilla materials).
- Un-namespaced custom items in skills/mobs must have matching definitions in `MythicMobs/Items/*.yml` (e.g. `Id: PAPER`, `Model: <cmd>`); missing entries trigger `Drop <name>:<slot> Drop type not found` on every equip tick.
- When consolidating vendor packs, preserve all `MythicMobs/Items/*.yml` alongside `mobs` and `skills`.

## Vendor Slot Syntax Concatenation Typos
- Vendor authors frequently concatenate slot names directly to item names without a colon (e.g., `item=shotgun_muzzle_1HEAD`, `focus_shot_1HAND`, `sniper_soldierHEAD`).
- MythicMobs parses the entire string as the item ID.
- Normalize using regex:
  `item=([a-zA-Z0-9_]+)(HEAD|HAND|CHEST|LEGS|FEET|OFFHAND)([;\}]) -> \1:\2\3`

## Common Targeter and Condition Typos
- `@true`: common typo for `@self` that triggers `Failed to load custom targeter TRUE`.
- `@self}`: trailing brace typo that triggers `Failed to load custom targeter SELF}`.
- `mobsinradius{r=5;a=<1}`: requires `types=ALL` or `t=ALL`. Omitting it triggers `The 'type' attribute must be a valid MythicMob or MythicEntity type.`
- Absent MetaSkills (`BLEED_FX_80`, `WITHER_FX_60`, `Cancelattack`, `Empower_Minions_GET`, `miu_slash_4`, `BassicAttack_v4`): define dummy no-op or fallback particle skills in a shared file to silence `Could not find MetaSkill` log spam.

## ItemsAdder & ModelEngine Texture Generation
- ItemsAdder scans `plugins/ModelEngine/resource pack/`. Files with Windows 8.3 filename truncation (`~1.png`, `texture(1).png`) trigger fatal ItemsAdder errors and abort resourcepack compilation, causing purple-and-black textures in-game. Clean these files before `/iazip`.
- If ItemsAdder textures or glyphs show purple/black boxes despite successful `/iazip`, verify `plugins/ItemsAdder/config.yml`: default hosting methods are disabled and `apply-on-join` is false. Enable `self-host` with the server's public IP and allocated ItemsAdder port, and set `apply-on-join: true`.
- When updating CustomModelData mappings, delete `plugins/ItemsAdder/storage/items_ids_cache.yml`; ItemsAdder preserves cached model IDs over new YAML configs unless cache is cleared.
