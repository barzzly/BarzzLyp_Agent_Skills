# Cross-panel bot migration

Use this sequence for Pterodactyl bot moves between panels:

1. Resolve source and target explicitly. Query both Client API bases at `/api/client`; print only server IDs, names, nodes, SFTP endpoints, limits, image, invocation, variables, and allocations. A valid token against the wrong panel is still a migration failure.
2. Stop source bots before copying. Keep source offline during cutover so Discord tokens do not create duplicate sessions. Stop target too when replacing partial files.
3. Archive source through Client API: list `/`, compress all real top-level entries, download the signed file URL, upload to target `/files/upload`, then decompress at `/`. Never copy `.env` into chat or log its contents.
4. Verify before starting: compare representative files and entrypoint files (`index.js`, `main.py`, `package.json`), then inspect Docker state and application logs. `204` power responses and API `starting` are acknowledgements, not runtime proof.
5. Start targets only after every archive is decompressed. Confirm Docker container `running`, Discord login identity, and any HTTP listener. Keep source offline until target health passes.
6. If panel remains yellow/`starting` while container is healthy, configure the egg's startup completion words with text emitted after boot, such as `Bot aktif sebagai`. Put this in egg startup configuration, not server environment variables; Wings needs completion output to transition to Running.
7. Compare source and target egg image, invocation, startup variables, allocations, and limits. Do not silently change Node/Python entrypoints during migration; a different egg can alter package installation and completion behavior.
8. Fix application errors after migration health is established. Read logs, make the smallest code/dependency fix, restart only affected bot, and verify bot login plus command/HTTP behavior. Ignore npm audit/deprecation warnings unless they cause runtime failure.
