# Pterodactyl schedule replication

Use when copying an established restart schedule between named servers/panels.

## Procedure

1. Load endpoints from `~/.config/pterodactyl.env`:
   - `PTERODACTYL_PANEL_URL` + `PTERODACTYL_API_KEY` for UltraServers.
   - `PTERODACTYL_CONSOLE_URL` + `PTERODACTYL_CONSOLE_API_KEY` for `https://panel.barzzly.com/`.
2. Query source schedules. Select schedule by name, not list position. Read its full task relationship and preserve task sequence, action, payload, offset, and `continue_on_failure`.
3. Convert requested WIB time to Pterodactyl cron UTC. For a ten-minute warning schedule, trigger at target minus ten minutes:
   - 10:00 WIB => `hour: 2`, `minute: 50` UTC.
   - 00:00 WIB => `hour: 16`, `minute: 50` UTC.
4. Exclude explicitly named servers before creating schedules. Do not infer inclusion from a shared node or similar name.
5. Create target schedule with JSON fields `name`, `day_of_week`, `day_of_month`, `month`, `hour`, `minute`, `only_when_online`; capture generated schedule ID.
6. Post child tasks sequentially to `/api/client/servers/{id}/schedules/{schedule_id}/tasks`. Restart task must be `action: "power"`, `payload: "restart"`; never use a console `restart` command because containers may lack `start.sh`.
7. Activate schedule with `POST /api/client/servers/{id}/schedules/{schedule_id}` and include the full required schedule payload (`name`, all cron fields, `is_active`, `only_when_online`). A partial body can return validation errors.
8. Read back every target schedule. Assert one intended active schedule, expected cron, expected task count, and exact task sequence. Delete duplicate inactive schedules only after the active replacement is verified; verify deletion.

## Pitfalls

- Pterodactyl schedules run in UTC; using `10` for a 10:00 WIB schedule runs at 10:00 UTC instead.
- A `204` from schedule deletion is not enough; list schedules afterward and confirm duplicate removal.
- Updating a schedule with `PUT` is unsupported on some panels; use the panel's supported `POST` update route and verify the response.
- Existing inactive schedules can hide a newly created active schedule. Select by active state and cron, then remove stale duplicates after verification.
- API `429`/`5xx` responses are transient. Retry with bounded backoff, but do not duplicate-create until a fresh schedule list confirms whether the first create succeeded.
- Preserve source task payloads exactly; changing warning offsets changes the actual restart time even when the cron trigger looks correct.
