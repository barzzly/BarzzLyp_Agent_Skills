# Watchdog file-I/O & database connection diagnosis

- Inspect the archived log immediately before the current API startup_datetime; latest.log usually contains only the new run. Midnight log rotation alone does not establish restart.
- Download compressed logs through files/download signed URLs, then decompress locally. Keep signed URLs and API keys out of reports and source; load credentials from the configured environment file.
- Extract bounded first/last watchdog samples and main-thread stacks; do not print overlapping contexts for every watchdog line.
- Main-thread native open0/write/close0 beneath PlayerAdvancements.save or ServerStatsCounter.save establishes blocking file I/O during player saves. When this occurs alongside database pool warnings, check database health before blaming storage alone:
  - If server logs show `Failed to validate connection ... (No operations allowed after connection closed.)`, inspect the MariaDB/MySQL instance.
  - Check whether `max_connections` was exceeded (`ERROR 1040 (08004): Too many connections`). Multiple Minecraft plugins (LuckPerms, AuraSkills, JPremium, HuskClaims, CustomFishing, etc.) run connection pools and can exceed low defaults such as 100.
  - Check `wait_timeout` and `interactive_timeout`; short values can close idle connections and trigger Hikari validation errors. Change limits only after confirming live values and connection pressure, then apply runtime and persistent settings and verify with `SHOW VARIABLES` and `SHOW STATUS`.
  - Treat database pressure as causal only when connection errors/timeouts align with the stall or DB refuses connections; otherwise keep storage/file I/O as a separate hypothesis.
- Distinguish watchdog shutdown from scheduled restart using fatal watchdog messages and schedule timestamps. Errors raised while plugins disable can be secondary shutdown noise.
- For loot/config edits requested without restart, back up the exact active file, remove only matching loot-entry blocks, write through the panel file-write API, read back and validate that the target ID is absent, then invoke the plugin's reload command and confirm its success message. Do not use a generic reload or restart when the plugin exposes a narrower command.
