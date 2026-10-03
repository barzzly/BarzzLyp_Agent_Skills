# ExcellentCrates reward safety

- Inspect both `PreviewData` and `ItemsData` before treating a barrier icon as a distributed barrier. In ExcellentCrates 6.6.1, `ItemReward.loadAdditional` loads payout items from `ItemsData` (or migrates legacy `Items`); `giveContent` iterates only that item list. `PreviewData` does not become payout content when the list is empty.
- An empty ITEM reward can represent a no-item zonk: `hasContent` is false and inspection reports no items, but `AbstractReward.isRollable` tests positive weight rather than content. Do not claim the inspection warning itself excludes the reward from rolls.
- If user authorizes a fix only if barriers are distributed, preserve a preview-only barrier with no payout items; no change is necessary. Distinguish config/bytecode evidence from a live player inventory test.
- COMMAND rewards with an empty command list also trigger an inspection warning. Do not change type or add a no-op command merely to hide warnings without establishing intended behavior.
