---
name: pterodactyl-server-management
description: Use when managing Pterodactyl game servers via SFTP or API.
version: 1.0.0
author: BarzzLy, Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [pterodactyl, minecraft, sftp, game-server, wings, api]
    category: productivity
---

# Pterodactyl Server Management (SFTP & Client API)

Manage Minecraft and game servers hosted on Pterodactyl panel environments (UltraServers, PebbleHost, BisectHosting, or custom Wings nodes).

## Overview

Pterodactyl environments expose two programmatic control surfaces:
1. **SFTP Daemon (Wings)**: File transfers, configs, plugin jars, world data, logs.
2. **Client REST API**: Server power states (start/stop/restart), live console commands, resource metrics.

## When to Use

- Interacting with Minecraft or game servers hosted on Pterodactyl panels.
- Web automation fails or is blocked by Cloudflare Turnstile / anti-bot challenges on the panel domain.
- Uploading, inspecting, editing, or backing up server plugins (`plugins/` or `plugins_new/`), configs, and logs.
- Triggering server power actions or executing console commands programmatically.

## Prerequisites

- SSH Key pair generated locally (`~/.ssh/id_ed25519.pub`).
- SFTP connection details from server Settings (Host, Port, Username format `<user>.<server_id>`).
- Optional Client API Key (`ptlc_...`) from Account Settings -> API Credentials for console & power control.

## Procedure 1: SFTP File Access via SSH Key (Bypass Web/Cloudflare)

When web panel logins are blocked by Cloudflare Turnstile, bypass the web UI entirely using direct SFTP:

1. **Register SSH Public Key**:
   - Provide `cat ~/.ssh/id_ed25519.pub` to the user to paste into **Account -> SSH Keys** on the panel.
   - Note: Do NOT provide the fingerprint (`SHA256:...`); the panel requires the full public key string starting with `ssh-ed25519` or `ssh-rsa`.

2. **Acquire Connection Details**:
   - Obtain from the server's **Settings -> SFTP Details**:
     - Host: use `PTERODACTYL_SFTP_HOST` from local environment; never commit the real host
     - Port: use `PTERODACTYL_SFTP_PORT` from local environment; common values are `2022` or a provider-assigned port
     - Username: use `PTERODACTYL_SFTP_USER` from local environment; format is usually `<username>.<server_short_uuid>`

3. **Execute Non-Interactive SFTP Operations**:
   Use batch mode with `StrictHostKeyChecking=accept-new` to prevent interactive prompt hanging:

   ```bash
   # List root files and plugins
   sftp -P <PORT> -o BatchMode=yes -o StrictHostKeyChecking=accept-new <USER>@<HOST> << 'EOF'
   ls -la
   ls -la plugins
   bye
   EOF
   ```

   ```bash
   # Upload a plugin or config
   sftp -P <PORT> -o BatchMode=yes <USER>@<HOST> << 'EOF'
   put /path/to/local/plugin.jar plugins/
   bye
   EOF
   ```

   ```bash
   # Download a config file for inspection or editing
   sftp -P <PORT> -o BatchMode=yes <USER>@<HOST> << 'EOF'
   get plugins/Essentials/config.yml /tmp/config.yml
   bye
   EOF
   ```

## Procedure 2: Server Control & File Editing via Client REST API

1. **Authentication & User-Agent**:
   Client API requires a Bearer token with the full key starting with `ptlc_` (~48 characters):
   `Authorization: Bearer ptlc_xxxxxxxxxxxxxxxxxxxxxxxx`
   Always include a browser User-Agent (`-H "User-Agent: Mozilla/5.0"`); Cloudflare blocks default programming client User-Agents (e.g. Python urllib) with HTTP 403.

2. **Check Server Resources & Status**:
   ```bash
   curl -s -H "Authorization: Bearer $PTERO_TOKEN" \
        -H "Accept: application/json" \
        -H "User-Agent: Mozilla/5.0" \
        https://<PANEL_HOST>/api/client/servers/<SERVER_ID>/resources
   ```

3. **Read and Write Files via Client API**:
   - **Read File Content**:
     ```bash
     curl -s -H "Authorization: Bearer $PTERO_TOKEN" \
          -H "Accept: application/json" \
          -H "User-Agent: Mozilla/5.0" \
          "https://<PANEL_HOST>/api/client/servers/<SERVER_ID>/files/contents?file=$(python3 -c 'import urllib.parse, sys; print(urllib.parse.quote(sys.argv[1]))' 'plugins/luckperms/config.yml')"
     ```
   - **Write File Content** (raw body, returns 204 No Content):
     ```bash
     curl -s -X POST \
          -H "Authorization: Bearer $PTERO_TOKEN" \
          -H "Accept: application/json" \
          -H "Content-Type: text/plain" \
          -H "User-Agent: Mozilla/5.0" \
          --data-binary @updated_config.yml \
          "https://<PANEL_HOST>/api/client/servers/<SERVER_ID>/files/write?file=$(python3 -c 'import urllib.parse, sys; print(urllib.parse.quote(sys.argv[1]))' 'plugins/luckperms/config.yml')"
     ```

4. **Send Power Signal** (`start`, `stop`, `restart`, `kill`):
   ```bash
   curl -s -X POST \
        -H "Authorization: Bearer $PTERO_TOKEN" \
        -H "Accept: application/json" \
        -H "Content-Type: application/json" \
        -H "User-Agent: Mozilla/5.0" \
        -d '{"signal": "restart"}' \
        https://<PANEL_HOST>/api/client/servers/<SERVER_ID>/power
   ```

5. **Send Console Command**:
   ```bash
   curl -s -X POST \
        -H "Authorization: Bearer $PTERO_TOKEN" \
        -H "Accept: application/json" \
        -H "Content-Type: application/json" \
        -H "User-Agent: Mozilla/5.0" \
        -d '{"command": "lp reloadconfig"}' \
        https://<PANEL_HOST>/api/client/servers/<SERVER_ID>/command
   ```

## Procedure 3: Server Backups via Client REST API

Pterodactyl stores backup archives (.tar.gz) outside the server's chrooted SFTP directory. Checking `/backups` or file paths via SFTP will yield nothing. Manage backups via the REST API:

1. **List Existing Backups**:
   ```bash
   curl -s -H "Authorization: Bearer $PTERO_TOKEN" \
        -H "Accept: application/json" \
        https://<PANEL_HOST>/api/client/servers/<SERVER_ID>/backups
   ```

2. **Trigger New Server Backup**:
   ```bash
   curl -s -X POST \
        -H "Authorization: Bearer $PTERO_TOKEN" \
        -H "Accept: application/json" \
        -H "Content-Type: application/json" \
        -d '{"name": "Pre-maintenance Backup"}' \
        https://<PANEL_HOST>/api/client/servers/<SERVER_ID>/backups
   ```

3. **Get Backup Download URL**:
   ```bash
   curl -s -H "Authorization: Bearer $PTERO_TOKEN" \
        -H "Accept: application/json" \
        https://<PANEL_HOST>/api/client/servers/<SERVER_ID>/backups/<BACKUP_UUID>/download
   ```

## Procedure 4: Bulk File Transfer & Unarchiving (Handling Wings Daemon Limits)

When deploying large plugin bundles, archives, or backups to a server:

1. **Wings Decompress API Fragility**:
   - The Pterodactyl client endpoint `/api/client/servers/<ID>/files/unarchive` often returns `500 ErrorException` or validation failures when processing `.tar.gz` archives on custom host configurations.
   - For multi-gigabyte transfers, prefer direct recursive SFTP upload (`put -r <local_dir>/* <remote_dir>/`) rather than relying on panel-side extraction of remote archives.

2. **Long-Running SFTP Uploads via Background Process**:
   - Transferring directories with thousands of small files (like plugin configurations, language files, and libraries) will exceed foreground tool timeouts (180s).
   - Run large recursive SFTP uploads as background terminal commands:
     ```bash
     sftp -P <PORT> -o BatchMode=yes <USER>@<HOST> << 'EOF'
     cd <TARGET_DIR>
     put -r /path/to/staging/* .
     bye
     EOF
     ```
     Pair with `background=true, notify=true` and monitor with `process_manage(action='poll')`.

3. **Staging & Excluding Database/State Folders**:
   - Heavy local logging plugins (e.g. `CoreProtect` with multi-gigabyte `database.db` files) should be excluded during recovery/migration staging to prevent bandwidth saturation and node disk quota exhaustion.

## Pitfalls

- **OpenSSH SFTP rm lacks recursive flag**: OpenSSH `sftp` `rm` command rejects `-r` (`rm: Invalid flag -r`). To remove remote directories, use a generated bottom-up exact file delete + `rmdir` script or rename/move.
- **Never delete or replace whole plugin root directories**: Live servers contain existing third-party assets, rank cosmetics, and active configs in `plugins/ItemsAdder/contents` and `plugins/MMOItems`. Replacing or deleting whole plugin roots wipes out non-pack server assets. Always delete and upload only exact pack-specific subfolders (e.g. `contents/SL_*`).
- **Verify plugin JAR naming after staging**: Plugin jars ending in `.jar.old` or `.disable` are silently ignored by Paper/Spigot loader during startup. Dependent plugins (like MythicLib and MMOItems) will boot with missing class/skill errors if prerequisite jars are renamed.
- **SFTP Timeouts on Deep Directory Trees**: Minecraft plugin suites (like `AxVaults`, `FastAsyncWorldEdit`, `LuckPerms`) contain deeply nested library directories (`libs/com/...`). A recursive `put -r` will easily exceed short execution timeouts. Always launch recursive directory uploads in a background process (`background=true, notify=true`).
- **Archive Extraction Quirks on Pterodactyl**: Pterodactyl Wings handles `.zip` files more reliably than `.tar.gz` through its API, but if the panel API fails or crashes on decompression, immediately stage files locally and upload uncompressed directories directly via SFTP.

- **Backups Inaccessible via SFTP**: Pterodactyl backup archives (.tar.gz) live on the host node or S3/remote storage managed by the daemon/panel, not inside the server root directory accessible via SFTP. Checking `/backups` or searching files via SFTP will yield nothing; querying or downloading backups requires the Client REST API (`/api/client/servers/<SERVER_ID>/backups`) or the panel web interface.
- **Kopia Snapshot Backups Fail API Download**: When a panel uses Kopia as its backup driver (`"disk": "kopia"` in backup attributes), requesting a download URL (`/download`) returns `400 BadRequestHttpException: Something went wrong. Failed to Download Backup.` because Kopia stores deduplicated chunks rather than standalone archive files. These backups can only be restored in-place via the panel API (`/api/client/servers/<SERVER_ID>/backups/<UUID>/restore`) or the web UI, not downloaded to a remote machine.
- **Truncated API Key Token Prefix**: Pterodactyl displays only the public 16-character key identifier in the active keys table (e.g. `ptlc_m1XvAKRdQYw`). The full 48-character bearer token is displayed exactly once in a modal dialog upon creation. If a user copies the key from the list view rather than the post-creation modal, all API calls fail with `401 Unauthenticated`. Instruct the user to create a new key and immediately copy from the modal.

- **Cloudflare Turnstile on Web Panel**: Never loop attempting headless clicks on Cloudflare Turnstile inside CDP browser sessions; Turnstile detects headless environments and will not pass. Pivot immediately to SFTP (SSH Key) or REST API.
- **Cloudflare 403 on REST API Requests**: Cloudflare WAF on Pterodactyl panels blocks requests with programming language default User-Agents (e.g. Python urllib). Always set `-H "User-Agent: Mozilla/5.0"` on all HTTP/curl calls.
- **LuckPerms Cross-Server Permission Sync**: When running a network (Proxy + backend Paper/Purpur instances) sharing SQL storage, always explicitly configure `messaging-service: sql` across all servers. The default `auto` frequently fails to bind the SQL messaging queue silently, forcing players to relog to receive updated permissions. Verify active cross-server sync by triggering `/lp networksync` from console and confirming `[LP] Other servers were notified via Sql Messaging successfully`.
- **Primary Game Databases vs Leaderboard Plugins**: Third-party leaderboard plugins (like ajLeaderboards) only populate offline metrics if players exist in local server storage/usercache. Always prioritize reading directly from the primary plugin database (e.g. `s4077_PlayerPoint` for PlayerPoints coins) when displaying network-wide leaderboards or analytics.
- **In-Game Currency Nomenclature**: Always verify in-game branding before exposing metrics on web dashboards; plugins named PlayerPoints often serve as "Coins" in server economies. Multi-server networks should segment public leaderboards by gamemode/server first (e.g. ECO RPG, PVP SL, RP REBEL) before showing specific stat categories.
- **ajLeaderboards Setup & Database Integration**: Store credentials in `plugins/ajLeaderboards/cache_storage.yml` with `method: mysql`, remote `ip:port`, `database`, `username`, and `password`. In `config.yml`, set `enable-dontupdate-permission: false` so admins/OPs are not skipped. Register boards via console `/ajlb add %placeholder%`. Map DeluxeMenus items to `%ajlb_lb_<board>_<pos>_alltime_name%` and `%ajlb_lb_<board>_<pos>_alltime_value%`, and player stats to `%ajlb_position_<board>_<type>%` and `%ajlb_value_<board>_<type>%`.
- **ajLeaderboards Offline Population**: Newly created boards show empty `--- - ---` until players join or until offline update runs. Execute `/ajlb updatealloffline <board>` via console to parse offline player data from Vanilla stats and Essentials/Vault into MySQL. Note that some third-party stats (e.g. AuraSkills) do not support offline player parsing and require live player login.
- **Server-to-Server JAR Transfer via Signed API URLs**: Transfer plugin files between panel instances without downloading locally by requesting a signed download URL (`GET /api/client/servers/<SRC>/files/download?file=<path>`) and streaming to a signed upload URL (`GET /api/client/servers/<DST>/files/upload?directory=<path>`) with `curl -X POST "$upload_url" -F "files=@-"`.
- **Truncated API Key**: Pterodactyl tokens are ~48 chars starting with `ptlc_`. If only the visible snippet (16 chars) is copied, the API returns `401 Unauthenticated`. Always verify key length.
- **SSH Fingerprint vs Public Key**: Users frequently paste the SHA256 fingerprint instead of the `~/.ssh/id_ed25519.pub` content. Explicitly instruct them to copy the raw public key string.
- **Non-Standard SFTP Ports**: Pterodactyl SFTP rarely uses port 22. Standard is port `2022`, but providers may assign custom ports. Always verify the exact port from panel SFTP details and keep it in `PTERODACTYL_SFTP_PORT`, never in public documentation.
- **Extracting Server Pack Textures & Serving in Embeds**: Custom in-game textures and rank icons (e.g. Nexo or ItemsAdder glyphs) reside deep in server pack directories (`plugins/Nexo/pack/external_packs/<Pack>/assets/<namespace>/textures/`). Rather than opening slow manual SFTP sessions, query the client API for a signed download URL (`GET /api/client/servers/<ID>/files/download?file=<url_encoded_path>`), download the asset programmatically, and copy it to a public web/CDN directory (e.g. `client/public/ranks/` and `dist/public/ranks/`). Never use raw file attachments (`files: [attachment]`) inside Discord ephemeral interaction embeds, as local file attachments prevent Discord mobile clients (iOS/Android) from dismissing the message. Instead, serve the thumbnail via public HTTPS URL (`.setThumbnail('https://<domain>/ranks/<name>.png')`).
- **Discord Bot Interactive Store & Catalog Embeds (Ranks, Items, Coins)**:
  1. **Main Embed Formatting**: Use the server's official animated emojis (`<a:crown_animated:...>`, `<a:animatedarrowyellow:...>`, `<a:animatedarrowred:...>`), never generic mobile emojis. Format items as `<a:animatedarrowred:...> **NAME** <a:animatedarrowyellow:...> **Harga**` (bold prices without backticks, no redundant shorthand in parentheses like `(40K)`). Mention outside the embed must use spoiler tags: `|| @everyone ||`.
  2. **Dropdown Select Menus**: Keep labels clean (`NAME - Harga`) and omit subtitle descriptions (`description`) to prevent cluttered mobile views. Avoid duplicate button rows if a select menu is already provided.
  3. **Role & Creator Separation**: Separate distinct creator tiers into individual options: `YOUTUBE` (Subscribers threshold), `TIKTOK` (Followers threshold), and `MEDIA` (higher tier for active live streamers with viewer requirements).
  4. **Coin Shop Messaging**: For currency/coin packages, state terms clearly: coins persist permanently across season resets, only decrease when spent, and can also be earned in-game via votes and quests.
  5. **Ephemeral Dismissal Fix**: To prevent stuck/undismissible ephemeral responses on mobile, do not attach local files. Serve images over HTTPS CDN and add a dedicated `[ Tutup Pesan ]` button (`customId: '..._dismiss'`) that executes `await interaction.deferUpdate(); await interaction.deleteReply();`.
- **Webstore In-Game Leaderboards & Navigation**:
  1. **Server-First Segmentation**: For multi-server networks, segment public in-game leaderboards by gamemode/server first (`ECO RPG`, `PVP SL`, `RP REBEL`) before displaying stat categories (`Uang`, `Coin`, `Playtime`, `Kills`, `Deaths`, `Skills`).
  2. **Economy Naming**: Verify server economy branding before publishing; `PlayerPoints` data typically maps to "Coin", not points.
  3. **Clean Typography**: Remove all decorative emojis (`💸`, `🧿`, `⚔`, etc.) from leaderboard category pills and cards.
  4. **Mobile Navbar Controls**: Never hide the login action on mobile with responsive hiding classes (`hidden sm:inline-flex`); show an accessible icon button (`User`) in mobile top navigation. Use a segmented pill switcher (`[ ID | EN ]`) with clear active state styling instead of a single ambiguous text button.
- **BatchMode Required**: Always pass `-o BatchMode=yes` with `sftp` in automation scripts. If authentication fails, it terminates immediately with exit code 255 rather than hanging indefinitely on a password prompt.
