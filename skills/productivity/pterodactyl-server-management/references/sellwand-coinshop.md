# NoeSellwand CoinShop migration

- For DeluxeTags shop updates, derive exact tag glyph and permission from live DeluxeTags config, not retired shop entries. Exclude exact IDs `winner`, `noe`, `sultan`; `noebiru_tags` remains eligible. Preserve existing regular price unless changed by user. Use explicit LuckPerms boolean/context, matching ownership denial and balance checks, and smallfont lore without transforming glyph IDs or commands. Count source/included/excluded in a saved manifest, verify exact uploaded menu and menu-specific reload; do not claim a purchase was tested from reload alone.

- Match existing Unicode small-cap typography in every added CoinShop display name and lore line, including uses, charge instructions, owner/tax labels and currency labels. Preserve color codes, numeric values, placeholders, URLs, commands and technical IDs exactly; never convert whole YAML text blindly.

- Read live `plugins/NoeSellwand/sellwands/` and charge config before replacing legacy DeluxeSellwands commands. Use `noesellwand give %player_name% <definition-id> 1` and `noesellwand givecharge %player_name% 1`; supplied username is an example, not a hardcoded buyer. Preserve prices, currency checks and premium Discord payment unless separately changed.
- Match menu material/CMD, multiplier, uses and charge uses to actual definitions. Normal BLAZE_ROD may lack CMD while premium uses CMD 1. Keep premium manual fulfillment manual; never add free give commands to its Discord button.
- Use chest-menu sizes divisible by nine and preserve slots. Back up, read back uploaded YAML, require menu-specific `dm reload` success and label purchase tests separately. Do not spend player money or grant charges merely to test syntax.
