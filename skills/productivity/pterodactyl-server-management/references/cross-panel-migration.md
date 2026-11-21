# Cross-panel migration

Use when moving Pterodactyl servers between panels while retaining files and runtime state.

1. Validate both Client API tokens with `GET /api/client`; reject `401/403` before touching servers. Match source and target by exact server name and identifier; never infer from list order.
2. Snapshot source inventory: identifier, name, allocation, limits, startup variables, and top-level file entries. Confirm target server already exists and target allocation is correct.
3. Stop source and target servers. Wait for both to report `offline`; this prevents duplicate bot processes and prevents extraction over changing files.
4. Archive the complete source tree with Client API `POST /files/compress`, excluding prior migration archives. Download through signed `GET /files/download` URL. Upload archive through target `GET /files/upload` URL, then `POST /files/decompress`.
5. Read back target file entries and representative startup files. Compare counts and required files before starting. Keep source offline until target health passes.
6. Start targets only after all copies complete. Verify three independent signals: panel resource state, Docker container state, and application logs. `starting`, Docker `Up`, or a Discord login alone does not prove all gates passed.
7. For bot servers, configure egg completion words to match real console output, such as `Bot aktif sebagai`; restart and verify panel state becomes `running`. Keep completion-word changes scoped to the intended egg/server; changing a shared egg can affect unrelated servers.
8. If target remains `starting` while Docker and application are healthy, inspect the egg's startup completion configuration before changing runtime code. If a bot crashes, inspect container logs and fix the application dependency/import error rather than forcing panel state.

Do not delete source data until target runtime and application checks pass. Rotate API tokens exposed in chat. Client API tokens do not replace SFTP credentials; Wings host public keys are not file-transfer private keys.