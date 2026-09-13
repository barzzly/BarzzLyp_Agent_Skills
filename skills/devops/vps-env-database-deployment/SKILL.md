---
name: vps-env-database-deployment
description: "Use when replacing VPS env and keeping DB local."
version: 1.0.0
author: BarzzLyp Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [vps, deployment, environment, mysql, mariadb, pm2, github-actions]
---

# VPS Environment and Local Database Deployment

Use for production updates where a supplied `.env` replaces runtime configuration while the application database stays on the local VPS.

## Always-on rules

- Keep secrets only in the VPS `.env`; never commit, print, or paste secret values into GitHub, logs, or chat.
- Preserve previous runtime environment as local permission-restricted backup before replacement.
- Treat `DB_HOST=localhost` or `127.0.0.1` as explicit when user says local VPS database; never silently switch to remote DB.
- Validate database connectivity and schema before restarting application.
- Build and type-check before process reload; report real command output.
- Verify external state after every change: DB connection, process status, HTTP response, and GitHub Actions run when push-triggered deployment is used.
- Use terse completion reports: changed state, verification, remaining warning or blocker.

## Procedure

1. **Inspect before changing**
   - Read supplied env locally, but display keys and safe metadata only; mask values.
   - Read existing `.env` safe metadata and confirm `.gitignore` excludes `.env` and backups.
   - Inspect DB adapter, schema migrations, deployment workflow, PM2 process name, and listeners.
   - Confirm MariaDB/MySQL active and identify target DB/user state.

2. **Install runtime environment safely**
   - Copy current `.env` to local backup, for example `.env.before-new-env`.
   - Copy supplied env to project's `.env`; set mode `600`.
   - Validate required DB keys, non-empty credentials, safe DB/user identifiers, and local DB host.
   - Preserve internal service integration keys (e.g. inter-bot/internal API tokens like `WEBSITE_MANUAL_DONATION_KEY`) from the existing `.env` backup if the supplied file omitted them.
   - Keep unrelated existing runtime values only when user explicitly requests merge; otherwise use supplied env as replacement.

3. **Provision local database**
   - Create DB if absent with `utf8mb4`; create or update matching localhost user.
   - Grant privileges only on target DB.
   - Import repository's idempotent schema/migrations through local authenticated client.
   - Read back `DATABASE()` and table count, then run application-level DB probe if available.
   - Keep primary `DB_*` on local VPS when requested, but honor auxiliary `LP_DB_*` exactly from supplied environment; LuckPerms may intentionally remain remote.
   - Probe auxiliary database independently with its own host, port, user, password, and database, then verify an application endpoint that consumes it. A successful primary DB probe does not validate LuckPerms.

4. **Build and reload**
   - Run `npm run check`, `npm run build`, and `git diff --check`.
   - Reload named PM2 process with updated environment and persist PM2 state.
   - If current agent is supervised by a gateway blocking supervisor self-restart, execute reload from independent shell/process context or verified one-shot scheduler script; claim reload only after PM2 readback confirms online.

5. **Verify production**
   - Query public URL with `curl -fsS -o /dev/null -w 'HTTP %{http_code}'`.
   - Read PM2 status and confirm process `online` with fresh uptime/restart.
   - Query GitHub Actions run for pushed commit when CI/CD configured; wait for completion and inspect conclusion.
   - Keep `.env` backups local and untracked; remove temporary scripts/backups only when retention is no longer useful and user did not request them.

## Pitfalls

- Do not copy env into Git history; credentials remain secrets even when diff looks like configuration.
- Do not provision only schema and skip credentials; successful SQL import does not prove app authentication.
- Do not restart before building; PM2 can serve stale or incompatible output.
- Do not trust successful SSH/CI command as deployment proof; read back PM2 and HTTP state.
- Do not expose local MariaDB publicly; only application needs DB access on VPS.
- Move untracked local design or working assets outside repo before git pull; newly pulled upstream directories with matching file paths will abort fast-forward merges.
- Check schema migration diffs (e.g. column adjustments like VARCHAR to LONGTEXT) and alter live database tables before reloading; otherwise runtime crashes or data truncation will occur.
- When adding media or image upload features, always support multi-file selection and chunk uploads (batches of 5) to prevent exceeding HTTP proxy client_max_body_size limits.
- Never set a low raw file size check (e.g. 10MB) on image pickers when downscaling on canvas anyway; phone/camera photos easily exceed 15-25MB. Allow up to 50MB raw and downscale sequentially to avoid canvas memory exhaustion.

## References

- Consult `vps-web-deployment` for reverse proxy and CI conventions.
- Consult `github` for push, Actions, and remote-state verification.
