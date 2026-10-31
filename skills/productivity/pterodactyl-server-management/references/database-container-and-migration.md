# Pterodactyl Database Containers & Cross-Panel Migration

## 1. Pterodactyl Database Container Egg Pitfalls

- **Binary names in modern yolks:** Modern MariaDB images (`ghcr.io/parkervcp/yolks:mariadb_11.4`+) provide `/usr/sbin/mariadbd` and `/usr/bin/mariadb`, not legacy `mysqld` or `mysql`.
- **System config overriding socket:** Default MariaDB installation `my.cnf` often ends with `!include /etc/mysql/mariadb.cnf` and `!includedir /etc/mysql/conf.d/`. These pull host system configs that force the socket to `/run/mysqld/mysqld.sock` (which fails on container read-only rootfs). Comment out `!include` and `!includedir` so `.my.cnf` controls the socket path in `/home/container/run/mysqld/`.
- **Root socket authentication failure:** Default `mariadb-install-db` binds `root` to `unix_socket`. Because Pterodactyl runs processes under UID `container` (997), `mariadb -u root` gets access denied. Always run `mariadb-install-db --auth-root-authentication-method=normal` so root authentication does not enforce local unix socket match.
- **Explicit defaults file:** Explicitly pass `--defaults-file=/home/container/.my.cnf` to both daemon (`mariadbd`) and CLI client (`mariadb`) in startup invocations.

## 2. Cross-Panel Database Migration Procedure

1. **Extract source credentials:** Query `/api/client/servers/<server_id>/databases?include=password` via Client API to retrieve actual database names, usernames, and passwords.
2. **Never drop source tables during migration:** Take remote dumps using `mariadb-dump -h <host> -P <port> -u <user> -p'<password>' <db> > <file>.sql` while keeping source servers untouched.
3. **WAF & User-Agent caution:** Cloudflare/WAF on panel endpoints may hang or throttle default python-urllib (`Python-urllib/3.x`). Use `curl` with standard browser or curl headers for reliable API file reads/writes.
4. **Pre-create database & user grants:**
   - Create empty database with UTF-8 support: `CREATE DATABASE IF NOT EXISTS \`<name>\` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;`
   - Create matching user with `%` host: `CREATE USER IF NOT EXISTS '<user>'@'%' IDENTIFIED BY '<pass>';`
   - Grant full schema permissions: `GRANT ALL PRIVILEGES ON \`<name>\`.* TO '<user>'@'%'; FLUSH PRIVILEGES;`
5. **Import & verify counts:** Import via TCP socket: `mariadb -h <host> -P <port> -u root -p'<pass>' <db> < <dump>.sql`. Query `information_schema.TABLES` to compare table and row counts before and after migration.
6. **Archive backups locally & panel-side:**
   - Retain a compressed `.tar.gz` bundle of all `.sql` dumps in a persistent backup directory.
   - Trigger a panel snapshot via `POST /api/client/servers/<server_id>/backups` and verify `is_successful: true`.

## 3. Network-Wide Plugin Database Config Routing

When migrating a central database server, update every dependent server across the network:
- **Velocity Proxy:**
  - `plugins/luckperms/config.yml` (`address: <host>:<port>`)
  - `plugins/jpremium/configuration.yml` (`storageHost: '<host>'`, `storagePort: <port>`)
- **Lobby Sub-servers:**
  - `plugins/LuckPerms/config.yml` (`address: <host>:<port>`)
- **Survival / EcoRPG Sub-servers:**
  - `plugins/PlayerPoints/config.yml` (`hostname`, `port`)
  - `plugins/LuckPerms/config.yml` (`address`)
  - `plugins/CustomFishing/database.yml` (`MySQL.host`, `MySQL.port`)
  - `plugins/HuskClaims/config.yml` (`credentials.host`, `credentials.port`)
  - `plugins/NoeMarriage/config.yml` (`mysql.host`, `mysql.port`)
  - `plugins/ajLeaderboards/cache_storage.yml` (`ip: "<host>:<port>"`)
  - `plugins/AuraSkills/config.yml` (`sql.host`, `sql.port`)
- **Verify edits:** Always read back every modified config file from the server via API/SFTP to verify the new IP and port before taking the server out of maintenance.
