---
name: minecraft-economy-auditing
description: Use when auditing Minecraft shop prices and duplicates.
version: 1.0.0
metadata:
  hermes:
    category: productivity
    tags: [minecraft, economy, shop, audit]
---

# Minecraft economy auditing

1. Identify target server and active shop plugins before analysis. Read live configs via approved remote access (Pterodactyl skill covers API/SFTP); do not treat old local snapshots as active. Keep server untouched unless user explicitly requests fixes. Record source and scope, including other shop/economy plugins excluded from audit.
2. Fetch primary config, modifiers, and every shop YAML. Parse with duplicate-key detection: ordinary YAML loaders silently keep last duplicate. Check top-level config keys and product fields; repeated `slot` or action maps can hide products or erase click behaviors. Validate `(shop, page, slot)` uniqueness after parse.
3. Count entries by transaction type (`item`, `enchantment`, `command`, `special`), not raw mapping size. Reconcile menu labels to the sum of purchasable entries, compare menu links to shop files, and mark unlinked shops as *potentially direct-command accessible*, not necessarily unreachable.
4. For a local-vs-live shop comparison, normalize both inventories by `(shop, product ID)` AND by actual item signature (type, material, mob, potion/enchantment, metadata, quantity). Compare both directions before reporting: live-only, local-only, and matching products with changed price, slot, page, or other fields. Category or ID renames can make an existing product appear missing; explain renamed equivalents separately. Explicitly check newly added material families in both inventories. State which side each absence refers to and list every missing item or attach a complete inventory diff; a short set of unique material signatures is not a complete difference report.
5. Group duplicate products by full item definition, not material alone; metadata, mob, potion, enchantment, and quantity can distinguish them. Separate identical-price category overlap from conflicting buy/sell prices. Evaluate arbitrage using positive per-unit buy and sell prices across exact comparable products; disabled `-1`, zero, and absent prices are different states, not negative-price exploits. Consider price modifiers, permissions, and `sellAll.findMaxSellPrice` before claiming actual transaction outcomes.
6. Report high-impact conflicts with exact category, item ID, prices, and locations. State static-config findings separately from live GUI/transaction proof and do not infer runtime behavior from YAML alone. Provide concise summary first, full findings as a file when lengthy.

When merging an old local shop ZIP into live ShopGUIPlus, compare full item signatures across categories before adding anything: local-only IDs can be duplicates, mislabeled materials, placeholder commands, or moved shops. Preserve live prices for existing products; price genuinely new material families against analogous live products (including sell-side abuse), and assign free `(page, slot)` rather than copying occupied ZIP positions. After adding pages, update page-title denominator, BALANCE specials, and both `config.yml` and `shops/shopmenu.yml` menu labels where present. Exclude the category the user explicitly requests removed, including its links in both menu files; back up and read back deletion. Reload with `shopguiplus:shop reload`, check fresh loaded item/shop/menu counts and plugin-specific warnings, and read back changed files. A preexisting SmartSpawner duplicate-provider warning is separate from ShopGUIPlus validation. ZIP configs may have duplicate `clickActions` keys, so do not replace live config wholesale.

For server connection, backups, and deployment rules, load `pterodactyl-server-management` too.
