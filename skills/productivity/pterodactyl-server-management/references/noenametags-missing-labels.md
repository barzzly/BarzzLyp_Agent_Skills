# NoeNameTags intermittent missing player labels

- Inspect live `logs/latest.log` for `PlayerTrackEntityEvent` failure before changing display settings. EntityLib `Metadata.copyFrom` can throw `ConcurrentModificationException` reading its unsynchronized pending `HashMap` from tracker thread; viewer spawn aborts. In NoeNameTags fork, snapshot owner metadata with `ownerMetadata.createPacket()` and apply via `metadata.setMetaFromPacket(...)` after clearing destination, preserving viewer overrides. Verify `PacketNameTag.class` against active JAR: ZIP timestamps can change whole-JAR SHA despite identical content.
- If user forbids restart, leave active JAR untouched. Back it up locally; upload tested JAR to `plugins/update/` with exactly active filename; read back both hashes; confirm server remains running. Check `bukkit.yml` has `update-folder: update`. Signed upload may land at server root despite `directory=/plugins`; locate and rename via files API. Next user-controlled restart applies update. Do not claim gameplay fixed before restart and player-level validation.

## UnlimitedNameTags migration & MiniMessage parser compatibility

- When migrating or configuring `plugins/UnlimitedNameTags/settings.yml`, setting `format: MINIMESSAGE` causes `ParsingException: Legacy formatting codes have been detected in a MiniMessage string` if team/rank placeholders (e.g. `%betterteams_color%`, legacy prefixes) output section signs `§` or ampersands `&`.
- Always set `behavior.format: UNIVERSAL`. This allows Adventure MiniMessage tags, hex codes, and legacy color codes to coexist without throwing parser exceptions.
- Optimize runtime performance with `behavior.displayAnimationInterval: 20` and disable unused `glowAnimations`.
- Reload live without server restart via console command `unt reload`.
