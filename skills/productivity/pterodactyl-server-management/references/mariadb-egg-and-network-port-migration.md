# MariaDB Egg Setup & Network Port Migration in Pterodactyl

## 1. Pterodactyl MariaDB Server Egg Pitfalls

When setting up a standalone MariaDB container server in Pterodactyl using yolks images (`ghcr.io/parkervcp/yolks:mariadb_11.4`):

1. **System Config Overrides Socket (`Read-only file system`)**:
   - Upstream egg templates often include `!include /etc/mysql/mariadb.cnf` and `!includedir /etc/mysql/conf.d/` at the end of `.my.cnf`.
   - In Pterodactyl containers, these lines pull rootfs system configs that reset `socket` to `/run/mysqld/mysqld.sock`. Since `/run` is read-only inside Docker containers, MariaDB crashes on start.
   - **Fix**: Comment out or remove `!include` and `!includedir` in `.my.cnf` so MariaDB uses `/home/container/run/mysqld/mysqld.sock`.

2. **Root Auth Mismatch (`Access denied for user 'root'@'localhost'`)**:
   - Default `mariadb-install-db` on Debian/Ubuntu sets the authentication plugin for `root` to `unix_socket`.
   - The Pterodactyl container runs as non-root user `container` (UID 997). When the startup script invokes `mariadb -u root`, unix_socket auth rejects UID 997.
   - **Fix**: Run database initialization with `--auth-root-authentication-method=normal` so root authentication does not enforce OS user identity matching.

3. **Interactive Console Startup**:
   - Modern yolks images use `/usr/sbin/mariadbd` (daemon) and `/usr/bin/mariadb` (client).
   - Startup command for interactive console in panel:
     ```bash
     { /usr/sbin/mariadbd --defaults-file=/home/container/.my.cnf & } && sleep 3 && /usr/bin/mariadb --defaults-file=/home/container/.my.cnf -u root
     ```

## 2. Votifier Network Topology in Proxy Networks

In Velocity + Backend (Paper/Spigot) server networks:
- **Proxy (Velocity / BungeeCord)**: Runs `VotifierPlus` / `NuVotifier` on an allocated public port (e.g. `19139`). External voting websites connect to THIS port.
- **Backend (EcoRPG / Survival)**: Runs the receiver listener on its own internal port (e.g. `12016`).
- **Data Flow**: Web Voting Site -> Proxy Public Port (`19139`) -> Downstream Forwarding to Backend (`185.207.166.85:12016`).
- **Rule**: Backend servers NEVER initiate outbound connections to the proxy's Votifier port. When proxy Votifier ports change, backend servers require NO config changes.

## 3. Cross-Host Database Migration Procedure

When migrating plugin databases across remote panels/hosts:
1. Dump live tables directly via `mariadb-dump -h <source-host> -P <port> -u <user> -p'<pass>' <db> > <file>.sql`.
2. Import cleanly into target server container: `mariadb -h <dest-host> -P <port> -u root -p'<pass>' <db> < <file>.sql`.
3. Verify row and table counts against source before updating configs.
4. Update backend plugin configs across all servers:
   - Velocity: `luckperms/config.yml` (`address`), `jpremium/configuration.yml` (`storageHost`, `storagePort`)
   - Paper/Spigot backends:
     - `PlayerPoints/config.yml` (`hostname`, `port`)
     - `LuckPerms/config.yml` (`address`)
     - `CustomFishing/database.yml` (`host`, `port`)
     - `HuskClaims/config.yml` (`host`, `port`)
     - `NoeMarriage/config.yml` (`host`, `port`)
     - `ajLeaderboards/cache_storage.yml` (`ip`)
     - `AuraSkills/config.yml` (`host`, `port`)
5. Save compressed backup of dumps locally in `/home/barzzly/Minecraft/database-backups/` and trigger Pterodactyl panel backup snapshot via client API.
