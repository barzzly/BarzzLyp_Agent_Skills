# Watchdog file-I/O & database connection diagnosis

- Inspect the archived log immediately before the current API startup_datetime; latest.log usually contains only the new run. Midnight log rotation alone does not establish restart.
- Download compressed logs through files/download signed URLs, then decompress locally. Keep signed URLs and API keys out of reports and source; load credentials from the configured environment file.
- Extract bounded first/last watchdog samples and main-thread stacks; do not print overlapping contexts for every watchdog line.
- Main-thread native open0/write/close0 beneath PlayerAdvancements.save or ServerStatsCounter.save establishes blocking file I/O during player saves. When this occurs alongside database pool warnings, check database health before blaming storage alone:
  - If server logs show `Failed to validate connection ... (No operations allowed after connection closed.)`, inspect the MariaDB/MySQL instance.
  - Check whether `max_connections` was exceeded (`ERROR 1040 (08004): Too many connections`). Multiple Minecraft plugins (LuckPerms, AuraSkills, JPremium, HuskClaims, CustomFishing, etc.) run connection pools of 10 connections each, rapidly exceeding default limits of 100.
  - Check `wait_timeout` and `interactive_timeout`. Default 600s closes idle connections prematurely, triggering Hikari connection validation errors across all plugin workers. Raise `wait_timeout` to 28800s (8h) and `max_connections` to at least 500-1000.
- Distinguish watchdog shutdown from scheduled restart using fatal watchdog messages and schedule timestamps. Errors raised while plugins disable can be secondary shutdown noise.
- Report restart time with explicit timezone, evidence file, current state, and root cause findings clearly.
