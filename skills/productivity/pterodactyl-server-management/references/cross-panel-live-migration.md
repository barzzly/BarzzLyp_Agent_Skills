# Cross-Panel Live Server Migration

Procedures for migrating files and backups between Pterodactyl panels and wings nodes without stopping live source servers.

## Workflow

1. **Locate Server Identifiers:**
   - Query Client API `GET /api/client` on source and target panels to resolve server UUIDs and identifiers.
   - Verify power states and confirm live server is running.

2. **Download via Signed Client API URL:**
   - Call `GET /api/client/servers/<source-id>/files/download?file=<path>` to obtain temporary signed download URL (`tempra.../download/file?token=...`).
   - Stream download directly to target host or local scratch storage (`curl -o Backup.zip "$DOWNLOAD_URL"`).
   - Verify archive integrity (`unzip -t Backup.zip`) and byte counts before moving forward.

3. **Direct Local Volume Delivery (when target node is local):**
   - Identify volume directory under `/var/lib/pterodactyl/volumes/<server-uuid>`.
   - Before extracting archive into an active server directory:
     - Rename existing open binaries (e.g. `server.jar` -> `server.jar.paper_backup`) rather than truncating in-place, keeping JVM open file descriptors valid.
     - Extract archive (`unzip -o Backup.zip -d /var/lib/pterodactyl/volumes/<uuid>`).
   - Ensure permissions are recursively set to `pterodactyl:pterodactyl` (UID 997 / GID 988 or node pterodactyl user).

4. **Verify State:**
   - Check target file list via Client API `GET /api/client/servers/<target-id>/files/list`.
   - Confirm source server remains running and untouched.
