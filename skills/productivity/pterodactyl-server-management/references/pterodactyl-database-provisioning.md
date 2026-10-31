# Pterodactyl Database Provisioning & Standalone MariaDB Eggs

## Replicating Databases Across Panels
When migrating servers between panels (e.g. UltraServers to local console) where plugins already have configured database credentials:
1. Retrieve existing credentials from source panel:
   `GET /api/client/servers/{id}/databases?include=password`
   Returns exact database names (e.g. `s4449_LuckPerms`), usernames (`u4449_...`), and decrypted passwords.
2. Re-create identical databases, users, and passwords on the target database host.
3. This eliminates needing to edit plugin configuration files across multiple servers, preserving existing schemas and connections.

## Live Server Migration Without Stopping
- When copying files into an active, running server container volume without stopping it:
  - Do not overwrite or truncate an active `server.jar` in-place with `cp`; writing into an open jar file can crash the running JVM process with ClassNotFoundException or SIGBUS.
  - Safely rename the active jar first (`mv server.jar server.jar.backup`) so the running JVM process retains its open file descriptor on the old inode, then place the new jar.

## Standalone MariaDB Server Egg Setup
Running a dedicated MariaDB database server container in Pterodactyl (with interactive web console):

### Configuration Requirements
- **Socket Path**: In Docker rootfs, `/run/mysqld` is read-only. MariaDB must bind its socket to `/home/container/run/mysqld/mysqld.sock`.
- **System Config Override**: Default `.my.cnf` templates from legacy eggs often include `!include /etc/mysql/mariadb.cnf` and `!includedir /etc/mysql/conf.d/`. These override the custom socket back to `/run/mysqld/mysqld.sock` and cause startup crashes. Always comment out `!include` and `!includedir` in `/home/container/.my.cnf`.
- **Root Authentication**: MariaDB 10.4+ defaults to `unix_socket` auth for `root`. Because Pterodactyl runs containers as user `container` (UID 997), `mariadb -u root` fails with `Access denied`. During initialization, use:
  `mariadb-install-db --defaults-file=/home/container/.my.cnf --auth-root-authentication-method=normal`
  This enables password/normal auth so `container` can access the interactive root console.

### Startup Command
`{ /usr/sbin/mariadbd --defaults-file=/home/container/.my.cnf & } && sleep 3 && /usr/bin/mariadb --defaults-file=/home/container/.my.cnf -u root`

### Non-Interactive SQL Execution
`docker exec` without `-i` ignores stdin heredocs. Use an on-disk script or interactive flag:
`docker exec <container> sh -c "mariadb --defaults-file=/home/container/.my.cnf -u root < /home/container/init.sql"`
