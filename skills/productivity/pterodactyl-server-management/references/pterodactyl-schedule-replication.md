# Pterodactyl Schedule Replication & Management

- Fetch source schedules via Client API `GET /api/client/servers/{source_id}/schedules`. Extract target schedule attributes (`name`, `is_active`, `cron` mapping minute/hour/day_of_month/month/day_of_week, and `only_when_online`).
- Create schedule on target server via `POST /api/client/servers/{target_id}/schedules` with the extracted cron and online gating payload. Retrieve generated target schedule ID.
- Replicate all child tasks from source `relationships.tasks.data` in sequence order via `POST /api/client/servers/{target_id}/schedules/{schedule_id}/tasks`:
  - Preserve `action` (`command` or `power`), exact multiline `payload`, integer `time_offset`, and `continue_on_failure`.
- Read back target schedule and task collection via `GET /api/client/servers/{target_id}/schedules/{schedule_id}`; assert identical task counts, sequence order, actions, offsets, and payloads.
- Console command syntax caution in scheduled tasks: in modern Paper/Purpur (1.20+), gamerule or world-scoped queries executed from console must specify dimension context (e.g., `execute in minecraft:overworld run gamerule minecraft:random_tick_speed`), as unqualified legacy commands fail argument validation.
