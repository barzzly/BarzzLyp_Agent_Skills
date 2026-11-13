# CustomFishing modest rarity tuning

- Read live loot-conditions.yml, item rarity lore, rod/bait effects and command registration before tuning. CustomFishing 2.3.26 uses relative weights; matching parent and biome subgroup weights accumulate, then gear effects can modify eligible loot. Docs: https://mo-mi.gitbook.io/xiaomomi-plugins/customfishing/plugin-wiki/customfishing/weight-system-must-read
- Do not infer rarity from ID alone: rainbow_fish and rubbish are labeled trash; tuna_fish_silver_star has inconsistent common lore. Keep lore untouched during probability-only requests and explicitly classify silver quality separately if needed.
- For a small buff, apply bounded factors to existing additive loot weights only: trash 0.80, uncommon/silver 1.15, rare 1.20, legendary 1.10, secret unchanged. Preserve conditions, biome identity, common baseline, prices, rod limits, requirements and minigame settings. These are weight multipliers, not percentage-point increases in actual probability.
- Leave secret raw weights unchanged but explain normalization can still increase their final odds after trash reduction. Sparse jungle/cave fish pools can remain trash-heavy; report remaining imbalance rather than secretly multiplying rare fish manyfold.
- Assert exact semantic delta, positive weights and decreased base-pool trash across all biome subgroups; label calculations as no-gear theoretical pools, not measured catches. Back up fresh remote source, compare before write, read back bytes, and use registered customfishing reload.
- A concurrent restart can queue console reload while latest.log rotates. Require fresh Done, current running state, reload confirmation and final source readback; do not claim own task restarted server when no power signal was sent.

## Read-only CustomFishing catalog audits

- Partition item definitions into entries with explicit `size` and loot without `size`; preserve every ID and compare expected/collected sets, not counts alone. Fish-named trash can lack size; never invent its maximum.
- Report `size` upper bound as base maximum, not loot weight or rod capacity. Inspect global `restricted-size-range`, bait/hook/equipment/enchant/totem size effects, and unit labels in both item lore and global messages. If kg/cm labels conflict or stacking/clamp order is unproved, expose the conflict and do not calculate a final gear maximum.
- Traverse every loot-condition branch with inherited parent conditions. Keep water, lava, environment, world, rod, and time gates separate; item groups, categories, and index-habitat lore are not proof of biome eligibility.
- Resolve names from explicit CustomFishing display fields before external providers. Check item-detection-order and actual inheritance references; matching Nexo material plus CustomModelData proves a model association, not inheritance of names or stats. Preserve mismatched/alias IDs exactly and list missing category references separately from active fish.
- Leave a runnable coverage check with the catalog: exact ID sets, no duplicate YAML top-level IDs, every fish base maximum matches source, and snapshot hashes remain unchanged. Restrict private config extracts to gameplay fields; never copy operational endpoints or credentials into reports.

## CustomFishing EXP scaling & live reload

- CustomFishing lacks native EXP or global EXP multiplier in `config.yml`. EXP is granted via commands in item catch events: `command_action: type: command, value: ['sk xp add {player} fishing <amount>']` under `contents/item/default.yml`.
- Scaling fishing EXP requires multiplying the command amount for all item entries AND updating the corresponding `index-xp: <amount> XP` custom-data attribute so the `/fishingindex` GUI displays accurate numbers to players.
- Also inspect `contents/competition/default.yml` for competition reward tiers (`sk xp add {player} fishing <amount>`) and scale them proportionally so competition rewards remain balanced against standard fishing catches.
- Hot-reload live using `/cfishing reload` or `/customfishing reload` via console (completes in ~50-150ms without server restart).
