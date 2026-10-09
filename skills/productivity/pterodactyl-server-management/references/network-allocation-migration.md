# Network allocation migration

- Read source and target `/network/allocations`; match default game allocation and labeled Voice Chat, Votifier, and RCON services. Patch only corresponding active network keys, not every matching number/IP: model IDs, economy values, ticks, database addresses and external proxy endpoints are separate semantics.
- Preserve wildcard bind addresses; update advertised `voice_host` to target public IP/UDP port. Back up exact files, compare before writing, read back bytes, and retain original power state. Offline config verification does not prove live connectivity.
- Avoid parallel recursive Client API scans: listing and contents can hit HTTP 429 and leave large coverage gaps. Prefer SSH-key SFTP using `/account` username plus `.<server_short_id>` and target `sftp_details`; use installed OpenSSH for narrow reads or `uv run --with paramiko` for full traversal.
- Track listing/read errors and verify collected coverage before reporting. Exclude binary assets/player data/backups; do not blanket replace numeric matches.
