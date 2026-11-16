# Skript error triage and safe reload

## Procedure

1. Resolve target server from live panel inventory. Read `/resources`, `/plugins/Skript/scripts/<name>.sk`, and `/logs/latest.log` before editing.
2. Separate historical errors from current reload output. Search latest log tail for reload time, `Successfully reloaded`, `Encountered ... errors`, `Can't understand`, `Severe Error`, and the exception's first plugin frame.
3. For placeholder failures, identify syntax and lifecycle. Test syntax already accepted by the server's loaded scripts; do not assume `placeholder "..." from player` works in every Skript/addon version.
4. Guard player-dependent placeholders at the call site: evaluate only while the player is online. Re-check after delayed `on join` waits.
5. Keep smallest fix: inline placeholder in existing online-player loop when helper syntax is rejected. Remove stale helper calls during refactors; upload success is not reload success.
6. Back up exact remote script, upload, read back byte-for-byte, then issue `sk reload <name>` through client command endpoint.
7. Verify log contains `Successfully reloaded <name>` and no new reload errors. Do not restart unless requested.

## Rules and pitfalls

- Match placeholder syntax to installed Skript/addon grammar; valid-looking syntax can fail at reload and leave previous script active.
- Verify every caller after deleting or inlining a function; stale references make reload fail.
- Treat `Skript Severe Error` as runtime fault, not automatically server crash; prove causality from watchdog, stop, crash-report, or OOM evidence.
- Use exact remote readback after every script write because HTTP `204` or successful SFTP proves transport, not parser acceptance.
- Preserve remote backup and power state; reload only after syntax is valid, and never hide historical warnings by claiming they disappeared.
