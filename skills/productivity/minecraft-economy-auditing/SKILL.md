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
4. First pin scope: comparing a local ZIP with live shops finds only differences between those sources; it cannot identify Minecraft items absent from *both*. For a local-vs-live comparison, normalize by `(shop, product ID)` and actual item signature (type, material, mob, potion/enchantment, metadata, quantity), then compare both directions. Category/ID renames can disguise existing products; reconcile them before calling items missing. Enumerate every local-only/live-only entry with disposition (added, existing elsewhere, excluded with reason), or attach a complete diff. If asked whether vanilla families such as froglights or copper variants are missing, separately compare both catalogs against the target server version's material registry; report absent-from-both explicitly rather than implying the ZIP covers all Minecraft items. Distinguish matching products with changed price/slot/page from missing products.
5. Group duplicate products by full item definition, not material alone; metadata, mob, potion, enchantment, and quantity can distinguish them. Separate identical-price category overlap from conflicting buy/sell prices. Evaluate arbitrage using positive per-unit buy and sell prices across exact comparable products; disabled `-1`, zero, and absent prices are different states, not negative-price exploits. Consider price modifiers, permissions, and `sellAll.findMaxSellPrice` before claiming actual transaction outcomes.
6. Report high-impact conflicts with exact category, item ID, prices, and locations. State static-config findings separately from live GUI/transaction proof and do not infer runtime behavior from YAML alone. Provide concise summary first, full findings as a file when lengthy.

When merging an old local shop ZIP into live ShopGUIPlus, compare full item signatures across categories before adding anything: local-only IDs can be duplicates, mislabeled materials, placeholder commands, or moved shops. Preserve live prices for existing products; price genuinely new material families against analogous live products (including sell-side abuse), and assign free `(page, slot)` rather than copying occupied ZIP positions. After adding pages, update page-title denominator, BALANCE specials, and both `config.yml` and `shops/shopmenu.yml` menu labels where present. Exclude the category the user explicitly requests removed, including its links in both menu files; back up and read back deletion. Reload with `shopguiplus:shop reload`, check fresh loaded item/shop/menu counts and plugin-specific warnings, and read back changed files. A preexisting SmartSpawner duplicate-provider warning is separate from ShopGUIPlus validation. ZIP configs may have duplicate `clickActions` keys, so do not replace live config wholesale.

For DeluxeMenus CoinShop price changes, discover the actual registered menu in `plugins/DeluxeMenus/config.yml` before editing. Read each purchasable entry's displayed price, balance `click_requirement`, and actual debit `click_commands`; update all three together and leave ownership grants intact, or players see one price and pay another. Validate parsed YAML and every target entry, back up exact remote bytes, write the single scoped file, read it back byte-for-byte, run `dm reload <registered-menu-id>`, and confirm fresh success in the log and server running. A successful reload proves config loading, not a real player's purchase.

For server connection, backups, and deployment rules, load `pterodactyl-server-management` too.
