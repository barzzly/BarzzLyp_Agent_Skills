# MCPets Vouchers

On scoped live server, inspect existing Vouchers JSON, MCPets base/Skins permissions and Nexo BRICK CustomModelData. Use native existing voucher template; preserve item, lore, glow, confirmation, consume behavior and permission context. Grant exact base permission plus every distinct skin permission via separate 100% COMMAND rewards in AUTOMATIC mode. Do not guess wildcard permissions. Existing donut voucher may already cover request; reuse rather than duplicate.

Vouchers 4.5.0 build 447 can have custom `syncfiles`: inspect live JAR command constants. `vouchers reload` only reloads settings/messages, not voucher JSON. Deploy after assert checks, preserve old definitions, read back writes, run `vouchers syncfiles`, require fresh updated/removed/failed summary. Automatic mode executes all configured chance-qualified rewards; maximum_rewards applies to nonautomatic modes. Existing BRICK voucher may have no model data; distinguish voucher material from pet icon model data. Do not inject unsupported JSON model fields.

Give syntax verified from live GiveCommand: `vouchers give <player> <#> <voucher> [args]`. Giving or redemption alters inventories/permissions; perform only when requested. Sync/readback proves definition loaded, not redemption or skin switching.
