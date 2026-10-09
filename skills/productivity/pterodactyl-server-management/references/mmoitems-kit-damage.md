# MMOItems kit weapon damage on Noesantara ECORPG

- Inspect live `plugins/MMOItems/item/kit_*.yml` and `item-types.yml` first: kit categories inherit `MISCELLANEOUS`, so NETHERITE_SWORD material alone does not guarantee vanilla melee damage, and BOW/CROSSBOW materials deal near-zero arrow damage because MythicLib projectile calculation uses `shooter.getStat("ATTACK_DAMAGE")`.
- Melee baseline: Netherite sword total = 8, axe = 10; set numeric `base.attack-damage` on each melee item.
- Ranged baseline: Bow = 8.0 (scales with Power enchant to 20-24.75 damage), Crossbow = 9.0 (vanilla flat arrow damage).
- MMOItems generated instances persist NBT stats; set `base.revision-id: 1` (or increment existing ID) to migrate old instances; confirm `item-revision` in `config.yml` preserves gems/enchants before doing so.
- Download all affected YAML first, validate each live file against snapshot, make per-file backups, apply narrow insertion, parse original/updated YAML and assert only target fields differ, read back each file.
- Apply live without restarting: `mi reload` via client API; verify `MMOItems ... reloaded` in new logs and inspect errors. Unrelated existing template warnings should be reported separately. Live damage still needs in-game measurement.
