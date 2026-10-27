# Pterodactyl MariaDB Database Container Tuning

Use when managing, diagnosing, or tuning dedicated database containers (`DB-Container-<server_id>`) in Pterodactyl without unexpected restarts.

## Container Identification

Database containers are mapped in Pterodactyl under the parent server:
1. Query parent server databases: `GET /api/client/servers/{server_id}/databases`.
2. Extract container identifier: `attributes.data[i].attributes.container.server_identifier`.
3. Check container resource utilization: `GET /api/client/servers/{container_id}/resources`.

## Interactive Database Console

Pterodactyl MariaDB containers (`ghcr.io/ptero-eggs/yolks:mariadb_*`) run an interactive `mysql` CLI session connected locally as `container@localhost` with `GRANT ALL PRIVILEGES ON *.* WITH GRANT OPTION`.
- Console commands sent via `POST /api/client/servers/{container_id}/command` (`PteroClient.send_command(...)`) execute directly as SQL statements.
- Query results and MariaDB engine notices output to `logs/server.log`.

## Live Memory Diagnostics & Dynamic Trimming (No Restart)

Containers allocated 1024 MB RAM frequently exceed limits and spill into swap when defaults (`innodb_buffer_pool_size=384M`, `table_open_cache=2000`, `thread_cache_size=256`) collide with multiple HikariCP connection pools (typically 10 idle connections per active plugin) and glibc heap allocation arenas.

### Diagnostic Queries
Execute via console or direct MySQL client:
```sql
SHOW GLOBAL STATUS WHERE Variable_name IN ('Threads_connected', 'Connections', 'Aborted_connects', 'Memory_used');
SHOW GLOBAL STATUS LIKE '%innodb_buffer_pool%';
SHOW VARIABLES WHERE Variable_name IN ('innodb_buffer_pool_size', 'table_open_cache', 'thread_cache_size', 'max_connections');
```

### Live Shrink Steps
1. **Verify Chunk Size**:
   ```sql
   SELECT @@innodb_buffer_pool_chunk_size; -- default 134217728 (128M)
   ```
2. **Resize Buffer Pool Live**:
   InnoDB buffer pool size must be an integer multiple of chunk size:
   ```sql
   SET GLOBAL innodb_buffer_pool_size = 268435456; -- 256M (2 chunks)
   ```
   MariaDB immediately frees allocated chunks and withdraws free blocks online without restarting the daemon.
3. **Trim Table, Thread, and Unused Key Caches**:
   ```sql
   -- Verify if any tables use MyISAM
   SELECT engine, count(*) FROM information_schema.tables GROUP BY engine;

   -- If zero MyISAM tables, trim key_buffer_size from default 128M to 16M (instantly frees ~112 MB with zero data risk)
   SET GLOBAL key_buffer_size = 16777216;

   -- Trim open table and thread caches
   SET GLOBAL table_open_cache = 400;
   SET GLOBAL thread_cache_size = 16;
   FLUSH TABLES;
   FLUSH QUERY CACHE;
   ```
   *Note on `aria_pagecache_buffer_size`:* In MariaDB 10.6, `aria_pagecache_buffer_size` is read-only at runtime (`ERROR 1238`). Set it in `.my.cnf` (`32M`) to take effect on the next boot.

4. **Cgroup Memory Caveat & Cross-Node Discrepancies**:
   - Live SQL shrinking reduces MariaDB internal `Memory_used` instantly (typically 200+ MB saved across buffer pool and key buffer).
   - Linux cgroup memory metrics in Pterodactyl dashboard include glibc heap fragmentation and OS kernel Page Cache (active disk I/O buffers from `ib_logfile0`, `ibdata1`, and `.ibd` tablespaces).
   - Do not compare cgroup RAM numbers across different physical nodes directly: an idle container with 9+ days uptime on one node may show ~144 MB because inactive pages were pushed to host swap, while an active container on another node shows ~920 MB because the kernel keeps working pages in RAM. Always check internal `Memory_used` via `SHOW GLOBAL STATUS` to verify actual allocation.

## Persisting Configuration

Prevent configuration regression on container restart:
1. **Update `.my.cnf`** in container root:
   ```ini
   [mysqld]
   port                           = 1026
   bind-address                   = 0.0.0.0
   pid-file                       = /home/container/run/mysqld/mysqld.pid
   socket                         = /home/container/run/mysqld/mysqld.sock
   general_log_file               = /home/container/log/mysql/mysql.log
   max_connections                = 150
   innodb_buffer_pool_size        = 256M
   table_open_cache               = 400
   thread_cache_size              = 16
   skip-name-resolve              = 1
   innodb_flush_log_at_trx_commit = 2
   ```
2. **Update Egg Startup Variables**:
   Update panel startup variables via API (`PUT /api/client/servers/{container_id}/startup/variable`):
   - `INNODB_BUFFER_POOL_SIZE`: `256M` (or `128M` for light workloads)
   - `MAX_CONNECTIONS`: `150`

## Connection Leak & Aborted Connect Storms

If `logs/server.log` floods with recurring authentication warnings (`[Warning] Access denied for user '...'@'...'`):
1. Note the client IP and connection ID in the log entry.
2. Match IP against Pterodactyl server allocations (`GET /api/client` relationships allocations) to locate the offending node.
3. Inspect plugin database configurations on that node (e.g. plugins still trying to connect to decommissioned databases after migrations).
4. Update plugin config to SQLite or correct active database host, then hot-reload the plugin (`<plugin> reload`).

## Synchronized Daily Restart Schedule

To prevent database corruption during scheduled parent server restarts:
1. Schedule the container restart at the same time as parent game server (e.g. 03:00 UTC), but set a 20-second time offset on the database restart task (`time_offset: 20`).
2. This ensures the game server kicks players, saves all world data (`save-all`), and gracefully closes HikariCP database connections before the database container restarts.
3. The database container boots in 2-3 seconds, fully ready before the game server finishes booting (~30-40 seconds later).
