---
name: minecraft-essentials-multihome
description: Use when configuring Minecraft EssentialsX home quotas.
metadata:
  hermes:
    category: productivity
    tags: [minecraft, essentialsx, luckperms, pterodactyl]
---

# EssentialsX Multi-home

- Load `pterodactyl-server-management` first. Identify exact live server and rank IDs via `/lp listgroups` and `/lp group <name> info`; ask when user spelling differs from existing group rather than creating typo rank.
- Read `plugins/Essentials/config.yml`: `sethome-multiple` maps arbitrary home-tier names to quotas. Player needs BOTH `essentials.sethome.multiple` and `essentials.sethome.multiple.<tier>`. Existing rank inheritance can supply base gate and lower-tier grants. Highest matching tier wins. Preserve existing nodes and grant only missing permissions.
- Back up exact live YAML before narrow edit. Read back remotely and parse `sethome-multiple`; use console LuckPerms commands for permissions, then read fresh `logs/latest.log` for success. LuckPerms `permission info` paginates; inspect page 2 as needed. Run `essentials reload` and confirm fresh reload message plus running server state. Do not claim in-game verification without player test.
- For alias-only cooldowns (e.g. `/eheal`), use `command-cooldowns: {eheal: 120}` rather than changing `heal-cooldown`, which affects both `/heal` and `/feed`. Verify alias via EssentialsX command reference or live plugin. Back up/read back/reload as above; `essentials.commandcooldowns.bypass` can exempt players. Gameplay cooldown needs a non-bypass player test.
- Pterodactyl API via local credentials needs `User-Agent: Mozilla/5.0` and JSON Content-Type for `/command`. Never expose credentials or endpoints in output.
