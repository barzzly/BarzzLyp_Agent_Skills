---
name: noerpg-advanced-enchants-menu
description: Use when fixing NoeRPG AdvancedEnchantments menus.
metadata:
  hermes:
    category: productivity
    tags: [minecraft, noerpg, advancedenchantments, menus]
---

# NoeRPG AdvancedEnchantments menu

- Load `pterodactyl-server-management` first. Target Noesantara ECO RPG only after live server identification. `/enchants` group selector is `plugins/AdvancedEnchantments/menus/customcommands.yml` under `enchantments.inventory.items`, NOT `groups.yml` or `menus/enchanter.yml`. Compare group IDs in `groups.yml` and actual enchant counts in `enchantments.yml` against selector slots before editing. Use 36-slot indexes 0–35, avoiding occupied positions. `fill` entry is background; explicit items use slot strings.
- Minimal backed-up edit, YAML parse and diff-check old config plus new slots, write remotely and read back. Never restart NoeRPG server for menu edits without explicit user approval, even if `/ae reload` warns it may not refresh menus; announcing downtime is not authorization. Try plugin-native `/ae reload`, report uncertainty if live GUI cannot be verified, and ask before any disruptive restart. Verify remotely saved YAML and live state separately; no in-game GUI claim without player-client test.
- `/enchants` category row alignment: FABLED slot 21, MYSTIC 22, MEGA 23 (zero-based), immediately below existing SIMPLE–LEGENDARY row (11–15). Check supplied screenshots against live slots before edits; do not place these at 22–24.
