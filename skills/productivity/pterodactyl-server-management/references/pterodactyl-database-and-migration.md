# Pterodactyl Server Migration & Database Provisioning

## Fast Server File Transfers via Client API Signed URLs

- When migrating or pulling files from a remote Pterodactyl server to a local Wings node, do not route through intermediary slow SFTP transfers.
- Query the Client API for a signed download link:
  `GET /api/client/servers/{server}/files/download?file=%2F<archive_or_file>`
- Direct curl to the target volume or temp directory:
  ```bash
  DOWNLOAD_URL=$(curl -s -H "Authorization: Bearer $KEY" -H "Accept: application/json" "$PANEL/api/client/servers/$ID/files/download?file=%2FBackup.zip" | jq -r '.attributes.url')
  curl -o Backup.zip "$DOWNLOAD_URL"
  ```
- **Safe in-place extraction on running servers**:
  - Overwriting an open executable or `server.jar` directly with `unzip` or `cp` modifies an active inode in place, potentially causing JVM `ClassNotFoundException` or corruption.
  - Safely move existing jar first (`mv server.jar server.jar.old`), then extract archive.
  - Always enforce ownership after extracting into volume roots: `chown -R pterodactyl:pterodactyl /var/lib/pterodactyl/volumes/<uuid>`.

## Database Host Configuration & Docker Connectivity

- Pterodactyl servers run inside Docker containers (e.g., `172.18.0.0/16` on `pterodactyl_nw` / `pterodactyl0`).
- If MariaDB is set to `bind-address = 127.0.0.1`, game containers cannot reach the database host. Set `bind-address = 0.0.0.0` in `/etc/mysql/mariadb.conf.d/50-server.cnf` so containers can connect to gateway `172.18.0.1` or the server public IP.
- If `POST /api/client/servers/{server}/databases` throws `NoSuitableDatabaseHostException`, no database host is bound to that node.
- To provision a Database Host via Panel CLI / Tinker:
  ```php
  $service = app(Pterodactyl\Services\Databases\Hosts\HostCreationService::class);
  $host = $service->handle([
      'name' => 'Local MariaDB',
      'host' => '151.243.143.12', // Reachable IP/hostname
      'port' => 3306,
      'username' => 'pterodactyl_admin',
      'password' => '<admin_password>',
      'node_id' => 1,
  ]);
  ```

## Preserving Legacy Database Names Across Migrations

- The Client API automatically forces database naming to `s<target_server_internal_id>_<input>`.
- When migrating multi-server networks where plugin configs (e.g. LuckPerms, JPremium, PlayerPoints) across proxies and backend servers already reference legacy database names (e.g. `s4449_LuckPerms`):
  - Do not manually break existing cross-server configs.
  - Use `Pterodactyl\Services\Databases\DatabaseManagementService`:
    ```php
    $server = Pterodactyl\Models\Server::find($serverId);
    $service = app(Pterodactyl\Services\Databases\DatabaseManagementService::class);
    $db = $service->create($server, [
        'database' => 's4449_LuckPerms',
        'remote' => '%',
        'database_host_id' => $hostId,
    ]);
    ```
  - This respects Pterodactyl regex `^(s[\d]+_)(.*)$`, provisions the DB and user grants in MariaDB, and registers the database into the Panel UI for the server.
