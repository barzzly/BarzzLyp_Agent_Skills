# LuckPerms command context audit

- Scan current remote text configs/scripts via SFTP; persist matched files and exclusions. Inspect DeluxeMenus, Vouchers, rank plugins, and Skript. Ignore comments; distinguish disabled dash-prefixed scripts from active scripts.
- Add `server=noerpg` only to supported mutation commands lacking server context. Preserve explicitly scoped commands and do not migrate existing global player nodes without separate scope approval. Pair permission set/unset context for toggles.
- Validate YAML/JSON and preserve all unrelated scalars; compare live bytes before each write, back up, reload owning plugins, then reread exact targets. NoeUpRank supports `uprank reload`; inspect installed command class before relying on undocumented commands.
- A file disappearing after successful write/readback may be concurrent maintenance, not failed upload. Do not recreate deleted scripts or removed aliases blindly; report concurrency gap and inspect replacement paths. Existing global nodes remain global after command-template edits.
- Fire/Air/Cosmic gem names must match original families: Fire §c, Air §2, Cosmic §9, including new 33–44 tools. Keep smallfont; do not apply Heroic/Void gradient to these families. Verify current numbered IDs rather than assuming compatibility aliases still exist.
