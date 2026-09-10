---
name: vps-self-healing-sentinel
description: Use when configuring autonomous self-healing monitoring.
metadata:
  hermes:
    tags: [devops, monitoring, self-healing, sentinel, vps, memory, pm2, docker]
    category: devops
---

# VPS Self-Healing Sentinel

## Architecture and Design Principles
- Combine lightweight deterministic telemetry scripts (`vps-sentinel.py`) with scheduled LLM reasoning for high-signal, anti-slop executive reporting.
- Decouple health checks from heavy inference: verify network sockets (`127.0.0.1:<port>`), systemd states (`systemctl is-active <service>`), and process tables directly in Python stdlib before waking the agent.
- Calculate real memory footprint using the `htop` metric (`total - free - buffers - cached - SReclaimable`) rather than raw `free` used output, which includes reclaimable kernel slab caches.

## Self-Healing Procedures
- **Orphaned Daemons & Memory Leaks:** If no active browser instance (`chrome`/`chromium`) is running, kill orphaned worker daemons (`pkill -f '\[b\]rowser_harness.daemon'`) to recover leaked RAM.
- **Node/PM2 Services:** Validate PM2 process state and listening port. Require two consecutive failed probes before recovery; transient socket/PM2 output failures must not restart a healthy app or be reported as downtime. Parse `pm2 jlist` only when exit code is zero and stderr is empty. If confirmed down or errored, execute `pm2 resurrect || pm2 restart <app_name>`. Persist the process table with `pm2 save`. Report a recovery only when that same run actually performed it; never carry a past recovery into current status.
- **Docker Containers:** Inspect container status with `docker inspect -f '{{.State.Status}}' <container>`. If stopped or unreachable on its exposed port, execute `docker restart <container>` and verify socket readiness after 2 seconds.
- **Systemd Daemons:** Check unit status with `systemctl is-active <unit>`. Avoid calling restart wrappers on the active gateway from within its own execution context.

## Hermes Cronjob Integration
- Use `hermes cron create <schedule> "<prompt>" --name "<name>" --script "<script>" --deliver "<target>" --model "<model>" --provider "<provider>"` to establish scheduled AI monitoring.
- Pass telemetry script stdout directly into the model context. Instruct the model to report anomalies, self-healing recovery actions, and core health metrics concisely without conversational filler.
- Keep diagnostic scripts in `~/.hermes/scripts/` (for cron runner resolution) and mirror clean maintenance copies under `~/Scripts/Sentinel/`.
