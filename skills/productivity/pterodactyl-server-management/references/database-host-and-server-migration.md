# Pterodactyl Database Host, Server Migration & MariaDB Egg

## 1. Zero-Downtime Server File Migration

When transferring files between Pterodactyl panels (e.g. UltraServers to local console) without stopping servers:
1. **Signed Download URL**: Call `GET /api/client/servers/{server}/files/download?file={path}` to get direct download URL via Wings.
2. **Direct Volume Transfer**: If target is local Wings, download directly or stream to `/var/lib/pterodactyl/volumes/{target-uuid}/`.
3. **Atomic Jar Replacement**: Never overwrite an active `server.jar` in-place while JVM is running (`cp` truncates the open inode and crashes the JVM). Use atomic rename `mv server.jar server.jar.bak` first, then write the new jar so the active JVM retains its open file descriptor.
4. **Ownership**: Always enforce `chown -R pterodactyl:pterodactyl /var/lib/pterodactyl/volumes/{uuid}`.

## 2. Preserving Exact Database Names (Preventing Config Rework)

When migrating servers between panels, plugins (LuckPerms, JPremium, PlayerPoints) are configured with legacy database names (e.g. `s4449_jprem`). Normal panel creation forces `s{new_id}_{name}`:
- Use Laravel Tinker on the Pterodactyl panel host:
```php
$server = Pterodactyl\Models\Server::find($serverId);
$service = app(Pterodactyl\Services\Databases\DatabaseManagementService::class);
$service->create($server, [
    'database' => 's4449_jprem', // Passes validation as long as it matches /^(s[\d]+_)(.*)$/
    'remote' => '%',
    'database_host_id' => $hostId,
]);
```
- This registers the database in Pterodactyl with user/pass generation while matching existing plugin configs without requiring search-and-replace across plugin configurations.

## 3. Database Host & Docker Network Connectivity

- MariaDB must listen on `0.0.0.0` or the Docker bridge gateway (`172.18.0.1` on `pterodactyl_nw` / `pterodactyl0`) in `/etc/mysql/mariadb.conf.d/50-server.cnf` so containerized servers can connect to the host DB.
- Database host in panel should be created with `HostCreationService`:
```php
$service = app(Pterodactyl\Services\Databases\Hosts\HostCreationService::class);
$service->handle([
    'name' => 'Local MariaDB',
    'host' => '151.243.143.12',
    'port' => 3306,
    'username' => 'pterodactyl_admin',
    'password' => $adminPassword,
    'node_id' => 1,
]);
```

## 4. MariaDB Standalone Server Egg (Web Console REPL) & Pitfalls

When running MariaDB as a managed Pterodactyl server:
- **Docker Image**: `ghcr.io/parkervcp/yolks:mariadb_11.4` (LTS)
- **Binaries**: In modern MariaDB, daemon binary is `/usr/sbin/mariadbd` (not `mysqld`) and CLI client is `/usr/bin/mariadb` (not `mysql`).
- **Startup Command**:
  ```bash
  { /usr/sbin/mariadbd --defaults-file=/home/container/.my.cnf & } && sleep 3 && /usr/bin/mariadb --defaults-file=/home/container/.my.cnf -u root
  ```
- **Pitfall 1: Read-only socket failure (`/run/mysqld/mysqld.sock`)**:
  Default `my.cnf` templates end with `!include /etc/mysql/mariadb.cnf` and `!includedir /etc/mysql/conf.d/`. In container environments, these include system defaults that override `socket` back to `/run/mysqld/mysqld.sock` (which is read-only in Docker rootfs), crashing daemon with `Can't start server : Bind on unix socket: Read-only file system`.
  *Fix*: Comment out `!include` and `!includedir` in `/home/container/.my.cnf` and explicitly pass `--defaults-file=/home/container/.my.cnf` to both `mariadbd` and `mariadb`.
- **Pitfall 2: Root access denied (`ERROR 1698`)**:
  Pterodactyl containers run as unprivileged `container` user (UID 997). By default `mariadb-install-db` configures `root` with `unix_socket` auth, which rejects `mariadb -u root` because the running user is `container`, not `root`.
  *Fix*: Run `mariadb-install-db` with `--auth-root-authentication-method=normal` so password/empty-password auth applies.

## 5. Streaming Live Database Migration

Transfer databases directly across Pterodactyl database containers without stopping source servers:
1. Extract credentials from source panel via API: `GET /api/client/servers/{server}/databases?include=password`.
2. Direct dump and pipe to target:
   ```bash
   mariadb-dump -h <src_host> -P <src_port> -u <src_user> -p'<src_pass>' <dbname> | mariadb -h <dst_host> -P <dst_port> -u root -p'<dst_root_pass>' <dbname>
   ```
3. Verify row counts immediately:
   ```sql
   SELECT TABLE_SCHEMA, count(*) as tables, sum(TABLE_ROWS) as total_rows FROM information_schema.TABLES WHERE TABLE_SCHEMA = '<dbname>' GROUP BY TABLE_SCHEMA;
   ```
4. Re-point application configs (e.g. `plugins/luckperms/config.yml`, `plugins/jpremium/configuration.yml`) to `<dst_host>:<dst_port>`.
