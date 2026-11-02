# Watchdog file-I/O restart diagnosis

- Inspect the archived log immediately before the current API startup_datetime; latest.log usually contains only the new run. Midnight log rotation alone does not establish restart.
- Download compressed logs through files/download signed URLs, then decompress locally. Keep signed URLs and API keys out of reports and source; load credentials from the configured environment file.
- Extract bounded first/last watchdog samples and main-thread stacks; do not print overlapping contexts for every watchdog line.
- Main-thread native open0/write/close0 beneath PlayerAdvancements.save or ServerStatsCounter.save establishes blocking file I/O during player saves. It does not alone establish physical disk failure or provider oversubscription; host I/O latency/kernel metrics require provider evidence.
- Distinguish watchdog shutdown from scheduled restart using fatal watchdog messages and schedule timestamps. Errors raised while plugins disable can be secondary shutdown noise.
- Report restart time with explicit timezone, evidence file, current state, and host-level uncertainty. Do not disable watchdog or player persistence to mask storage stalls.
