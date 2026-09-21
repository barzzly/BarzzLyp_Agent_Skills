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

## Procedure 5: Database Maintenance, Pre-Wipe Dump & Safe Data Reset

When performing server wipes, seasonal resets, or clearing game databases associated with Pterodactyl servers:

1. **Retrieve Database Credentials via API**:
   Query all allocated databases and passwords in one call:
   ```bash
   curl -s -H "Authorization: Bearer $PTERO_TOKEN" \
        -H "Accept: application/json" \
        "https://<PANEL_HOST>/api/client/servers/<SERVER_ID>/databases?include=password"
   ```
   Extract `name`, `host.address`, `host.port`, `username`, and `relationships.password.attributes.password`.

2. **Stop Server Before Database Operations**:
   Always transition server state to `offline` via `POST /api/client/servers/<SERVER_ID>/power` with `{"signal": "stop"}` before wiping or truncating tables. This prevents HikariCP connection pool errors, locked tables, and in-flight write crashes during shutdown.

3. **Pre-Wipe Local Backup (Mandatory)**:
   Always dump all databases locally before any destructive command:
   ```bash
   mariadb-dump -h<HOST> -P<PORT> -u<USER> -p<PWD> <DATABASE> > /path/to/backup/<DATABASE>.sql
   ```

4. **Safe Truncation (Preserve Schema Structure)**:
   Never run `DROP TABLE` or `DROP DATABASE`. Run `TRUNCATE TABLE` with disabled foreign key checks:
   ```sql
   SET FOREIGN_KEY_CHECKS = 0;
   TRUNCATE TABLE `table_name`;
   SET FOREIGN_KEY_CHECKS = 1;
   ```

5. **Protect Migration & Metadata Tables**:
   Never truncate migration tracking or schema metadata tables (e.g. `*_schema_migrations`, `*_metadata`, `*_migrations`). If migration records are wiped while tables exist, plugins attempt to run initialization DDL on boot and crash with `Table already exists` or `Duplicate column name`.

## Procedure 6: Full Plugin Backup & Purge Procedure

When wiping, replacing, or rebuilding a server's plugin suite:

1. **Catalog Active JARs**:
   Query all files in `plugins/` via `GET /api/client/servers/<ID>/files/list?directory=plugins` and filter for `.jar` files.

2. **Full Local Backup Before Purge (Mandatory)**:
   Create a dedicated local backup directory (e.g. `/home/barzzly/backup_plugins_<server>/`). Download every JAR using signed URLs (`GET /api/client/servers/<ID>/files/download?file=plugins/<jar>`). Verify that downloaded file count matches the server and total size is greater than 0.

3. **Stop Server Before Deletion**:
   Always transition server state to `offline` (`signal: stop`) and poll `resources` until state is `offline`. Never delete JAR files while the JVM is active.

4. **Chunked Deletion via API**:
   Delete files in batches of 40 via `POST /api/client/servers/<ID>/files/delete` with payload `{"root": "plugins", "files": [...]}`. Verify with a list call that 0 JARs remain.

5. **Direct Delivery on Request**:
   Deliver requested JAR files from the local backup directly via `MEDIA:/absolute/path/to/file.jar`.

## Pitfalls

- **Server Stop Mandatory Before Bulk JAR Deletions**: Always transition server state to `offline` before deleting all plugin JARs. Deleting JAR files while the server is active causes classloader crashes (`NoClassDefFoundError` on background schedulers) and leaves corrupted locks in `.paper-remapped`.
- **Chunked Deletions for Large Plugin Suites**: Pterodactyl API's `/files/delete` endpoint should process files in batches of 40. Sending 80+ files in one request can trigger proxy timeouts or daemon connection reset.

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
- **Extracting Server Pack Textures & Serving in Embeds**: Custom in-game textures and rank icons (e.g. Nexo or ItemsAdder glyphs) reside deep in server pack directories (`plugins/Nexo/pack/external_packs/<Pack>/assets/<namespace>/textures/`). To discover the exact registered glyph names and texture mappings, inspect the Nexo glyphs definition file (e.g. `plugins/Nexo/glyphs/Icon Rank ( 0xE400 - 0xE40D )/Icon Rank ( 0xE400 - 0xE40D ).yml`). Always download the complete hierarchy including default player ranks (`warga.png` for `default`), staff tiers (`staff.png`, `admin.png`, `dev.png`, `owner.png`), and network partner tiers (`noe.png`, `iestari.png`) alongside paid tiers (`prime`, `rogue`, `midas`, `aether`, `donatur`, `tajir`, `youtube`, `tiktok`, `media`). Rather than opening slow manual SFTP sessions, query the client API for a signed download URL (`GET /api/client/servers/<ID>/files/download?file=<url_encoded_path>`), download the asset programmatically, and copy it to a public web/CDN directory (e.g. `client/public/ranks/` and `dist/public/ranks/`). Never use raw file attachments (`files: [attachment]`) inside Discord ephemeral interaction embeds, as local file attachments prevent Discord mobile clients (iOS/Android) from dismissing the message. Instead, serve the thumbnail via public HTTPS URL (`.setThumbnail('https://<domain>/ranks/<name>.png')`). In web modals, render the badge directly inside the rank stat box rather than crowding the player's nickname.
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
- **AuraSkills / AureliumSkills Migration from YAML to MySQL**:
  Enabling SQL in `config.yml` alone does NOT migrate existing player userdata from YAML files to MySQL. To migrate safely without data loss:
  1. While still running YAML storage, execute `/skills backup save` via console. Verify the archive in `plugins/AuraSkills/backups/` (`backup-<timestamp>.yml`).
  2. Configure `plugins/AuraSkills/config.yml` under `sql:` (`enabled: true`, `type: mysql`, remote `host`, `port`, `database`, `username`, `password`).
  3. Restart the server. AuraSkills connects to MySQL and creates the schema (`auraskills_users`, `auraskills_skill_levels`, `auraskills_modifiers`, etc.).
  4. Import all player data into MySQL by executing `/skills backup load <filename>` from console.
  5. Web integrations can read live skill progression directly: `auraskills_users.player_uuid` matches Mojang/LuckPerms UUID. Read `skill_name`, `skill_level`, and `skill_xp` from `auraskills_skill_levels`. Total Power Level is the sum of `skill_level`.
- **Webstore Player Profiles & Donation Calculation**:
  1. **Historical Log Merging & Preventing Double-Counting**: When historical donations exist in a dedicated dataset (e.g. `DONATORS_DATA`) and are subsequently imported into the MariaDB `transactions` table, ensure the merge function (`mergeDonatorsWithTransactions`) treats the database as the authoritative single source of truth when populated. Adding static historical arrays on top of imported database rows causes player totals to double (e.g. inflating Rp 1.84M to Rp 3.68M). Only use the static array as a fallback when database rows are empty or unreachable.
  2. **Channel Donation Log Scraping (Bot Embeds + Human Codeblocks)**: When scraping donation log channels (e.g. `#donation-log`), never parse embed objects alone. Up to half of transactions may be posted by human staff as plain-text markdown codeblocks (`\`\`\`NAMA: ... HARGA: ...\`\`\``). Parse both embed descriptions/fields and raw message content. Detect couple donations (`+`, `&`, `dan`, `💖`, `❤️`) and split the price 50/50 so each partner's order history and donation total receive equal credit.
  3. **Bedrock Dot Normalization & Case-Insensitive Queries**: Bedrock players frequently carry a leading dot prefix (`.TherryVa`). Preserve the dot in canonical display names, but write transaction lookup endpoints with flexible case-insensitivity and dot-stripping: `WHERE LOWER(username) = LOWER(?) OR LOWER(username) = LOWER(?) OR LOWER(username) = LOWER(?)` with `[rawUser, cleanUser, '.' + cleanUser]`. This ensures players see their full order history regardless of whether their browser session logged in with uppercase, lowercase, or without the prefix.
  4. **Discord Bot `/donation` Amount Parsing**: When parsing user-input price fields in Discord slash commands or modals, never use raw digit stripping (`replace(/[^0-9]/g, '')`). Shorthand inputs like `50k` or `120k` will reduce to `50` or `120`. Always support `k` multipliers (`* 1000`), strip currency affixes (`rp`, `rupiah`, `rb`), and discard decimal cents (`,00`) before extracting values.
  5. **Trust Device Session Expiry**: In storefronts with username-only login modals, enforce a 1-hour trust device session window (`USER_SESSION_MS = 3600000`). Store `loginAt: Date.now()` in persistent local storage. Attach an automated watchdog timer in the root application component that evaluates `checkSession()` periodically (every 30s) and on window `focus` / rehydration, automatically clearing user and cart state upon expiration to prevent open sessions on shared devices.
  6. **Iconography Perceived as Emojis**: Users frequently perceive vector/SVG icons (`<Receipt />`, `<LogOut />`, `<Crown />`, `<Trophy />`) as "emojis". When instructed to remove all emojis, strip decorative icon pictograms from navigation buttons, card headers, and badges in favor of strict, clean typography.
  7. **In-Game Rank Prefix Badges**: Avoid duplicating rank text and wrapping images in redundant borders (e.g. `TIER RANK Midas [Midas]`). Render the authentic 80x16 pixelated PNG texture (`style={{ imageRendering: 'pixelated' }}`) directly under the `TIER RANK` header without surrounding card containers or redundant name labels. Leave the player nickname header clean without adjacent icons.
  8. **Footer Spacing**: Ensure profile and transaction dashboards maintain generous bottom padding (`pb-28 md:pb-36`) so tables and stat cards do not crowd the footer.
  9. **Draggable Cards & Carousel Button Clicks**: When placing buttons or links inside draggable/swipeable tracks, parent track `onMouseDown` and `onTouchStart` listeners will intercept clicks and activate `pointer-events-none` before child click events fire. Always guard parent handlers with `if ((e.target as HTMLElement).closest("a, button")) return;`, add `onMouseDown` and `onTouchStart` `stopPropagation` on the child button, and place links below text descriptions rather than overlapping character art or feet.
  10. **Maintenance & Alert Banners**: Prefer clean dark/neutral borders (e.g. `border-2 border-[#1A1A1A]`) over yellow/gold borders that feel dated or messy. Center alert/warning icons vertically (`items-center`) with accompanying copy rather than forcing top alignment with `items-start mt-1`.
- **Social Media Link Previews (OpenGraph / WhatsApp) Cache Busting**:
  WhatsApp, Discord, and Telegram link crawlers aggressively cache `og:image` by URL. When replacing legacy branding with modern logos or when the user supplies custom artwork:
  1. For messaging platforms (WhatsApp, Telegram) that favor square (1:1) previews, use the full artwork as the square image (`og-image.png` 1254x1254 or `og-square.png` 512x512).
  2. For landscape cards (Twitter/X, Discord `summary_large_image`), generate a 1200x630 version (`og-banner.png`) extending or padding the background to match the art edge tone.
  3. Always append cache-busting query parameters (e.g. `og-image.png?v=banner`) across `index.html` (`og:image`, `og:image:secure_url`, `link rel="image_src"`, `twitter:image`) and React Helmet/dynamic `<SEO>` components simultaneously so crawler caches are broken immediately.
- **BatchMode Required**: Always pass `-o BatchMode=yes` with `sftp` in automation scripts. If authentication fails, it terminates immediately with exit code 255 rather than hanging indefinitely on a password prompt.
- **Wings Signed Upload URL Target Directory**: When requesting a signed upload URL via `GET /api/client/servers/<ID>/files/upload`, appending `&directory=<target_dir>` (e.g. `&directory=plugins`) directly to the daemon upload URL (`https://<node>/upload/file?token=...&directory=plugins`) and specifying the filename in curl (`-F "files=@/path/to/file.jar;filename=plugin.jar"`) will land files directly into the target folder without requiring a separate move/rename API call.

- **Server Plugin Sourcing & Server Isolation Rules**:
  When performing automated plugin upgrades on server instances:
  1. **Strict Server Isolation (NEVER Cross-Copy Outside Noesantara)**: NEVER cross-copy, scrape, or transplant JARs or configurations from servers outside the Noesantara ecosystem (e.g. Queencraft, LegacySchool, or third-party servers on the same panel). Plugin borrowing is strictly limited to instances bearing the `Noesantara` project name. Sibling servers belonging to outside projects have separate licenses, configs, and environments; copying across them breaks isolation and violates licensing.
  2. **Official External Sourcing Only**: All updates must be downloaded directly from official, authoritative external repositories:
     - Modrinth API (`https://api.modrinth.com/v2/project/<id>/version` -> download primary loader build)
     - GitHub Releases (`https://api.github.com/repos/<owner>/<repo>/releases/latest` -> download matching asset)
     - Official project download endpoints (e.g. `download.luckperms.net`, EssentialsX GitHub, GeyserMC downloads API)
  3. **Premium / Commercial Plugins**: Commercial/licensed plugins (such as `AdvancedEnchantments`, `DeluxeSellwands`, `ShopGUIPlus`, `RoseStacker`, `MMOItems`, `Nexo`, `PlayerAuctions`, `Ultimate_BlockRegeneration`) cannot be downloaded from open public repositories. NEVER transplant them from other panel servers; leave the server's existing version intact and clearly report to the operator that manual file upload is required.
  4. **Coupled Plugin Dependencies (e.g. NightExpress Suite)**: When updating core framework plugins, update all dependent plugins simultaneously. For example, `ExcellentCrates` 6.x requires `nightcore` 2.16.x or newer; deploying `ExcellentCrates-6.6.1` while leaving `nightcore-2.7.3` will cause runtime startup crashes. Both are available on Modrinth.
  5. **Custom Internal Plugins**: Plugins with custom prefixes (e.g. `Noe*`) belong to the network's proprietary codebase and must never be overwritten from external sources.
  6. **Restoring Deleted Files from Pterodactyl Wings `/.trash`**: When files are deleted via the Client API (`/files/delete`), Wings moves them into `/.trash` named with base64-encoded original paths (e.g. `L3BsdWdpbnMvQWR2YW5jZWRFbmNoYW50bWVudHMtOS4yNC44Lmphcg`). To restore an accidentally deleted file without node disk access, invoke the rename API (`PUT /api/client/servers/<ID>/files/rename`) with `{"root": ".trash", "files": [{"from": "<base64_name>", "to": "../plugins/<original_filename>"}]}`.
- **Nexo Glyph Recursion & Gson 255 Nesting Limit (`AxVaults` / MMOItems / DFU)**:
  When configuring Nexo custom glyphs (e.g. `plugins/Nexo/glyphs/...`), NEVER set the `placeholders` entry to the raw unicode character itself (e.g. `char: ` with `placeholders: [- ]`). When `Plugin.formatting.items: true` is enabled in `plugins/Nexo/settings.yml`, Nexo intercepts item components over packets and wraps placeholder characters in a new text component with `font: "nexo:default"`. If the placeholder is identical to the glyph character, Nexo replaces the glyph with itself on every inventory tick/re-render, wrapping the component in another layer of `{"extra": ...}`. After 255 re-renders (a few minutes of gameplay), Gson crashes with `MalformedJsonException: Nesting limit 255 reached` whenever plugins like `AxVaults` or Paper's DataFixerUpper deserialize the item.
  
  To keep `Plugin.formatting.items: true` active (so glyphs format automatically across all item lore and names) without triggering recursion:
  1. **Purge Raw Unicode Characters from `placeholders`**: Scan all files under `plugins/Nexo/glyphs/` and replace any placeholder matching `char` with a textual token (e.g. change `placeholders: ['']` to `placeholders: [':gemsstone:']` or `[':<glyph_name>:']`). When placeholders are textual, Nexo replaces the token once and will never re-match the resulting unicode character on subsequent inventory ticks.
  2. **Keep `Plugin.formatting.items: true`**: Do not disable item formatting if the server relies on Nexo font encapsulation for custom fonts.
  3. **Reset Corrupted Items**: Purge or `/clear` corrupted items from player inventories and databases (`AxVaults/data.mv.db`) once nesting has already exceeded the 255-level limit.
- **Paper Watchdog Auto-Save Freeze Warnings (`DO NOT REPORT THIS TO PAPER`)**:
  When server console logs print `--- DO NOT REPORT THIS TO PAPER - THIS IS NOT A BUG OR A CRASH --- The server has not responded for 10 seconds! Creating thread dump` with stack traces pointing to `LevelStorageSource$LevelStorageAccess.saveLevelData` -> `ServerLevel.saveIncrementally` -> `createTempFile`, the server main thread is blocked waiting for disk I/O to complete writing world data (`level.dat`). This is caused by storage I/O bottlenecks on the hosting node during synchronous world auto-saves. Mitigate this by increasing `ticks-per.autosave` in `bukkit.yml` or `paper-global.yml` (e.g. from 6000 to 12000 ticks) or scheduling non-peak incremental saves to prevent thread watchdog alerts.
- **Auditing Plugin Health & Red Plugin Diagnostics**:
  To identify failed plugins programmatically:
  1. Count JARs in `plugins/` via API (`GET /api/client/servers/<ID>/files/list?directory=plugins`).
  2. Send `plugins` or `pl` to console (`POST /api/client/servers/<ID>/command`) and parse `logs/latest.log`. Plugins prefixed with `*` or listed under `Disabling <Plugin>` are RED in-game and disabled due to uncaught initialization exceptions.
  3. Compare plugin data folders against active JARs to identify orphan folders left behind by removed plugins.
- **MMOItems & MythicLib Version/Build Coupling**:
  In the Lumine/PhoenixDevt ecosystem, MMOItems and MythicLib builds must match strictly. Modern builds of MythicLib (1.7.1 b100+) relocated base class `MMOPlugin` from `io.lumine.mythic.lib.util.MMOPlugin` to `io.lumine.mythic.lib.module.MMOPlugin`, and deliberately throw `java.lang.RuntimeException` in the old constructor. Installing an older release of MMOItems (e.g. `MMOItems-6.10.jar`) with a newer MythicLib causes an immediate `InvalidPluginException: Exception initializing main class 'net.Indyuce.mmoitems.MMOItems'` on startup. Always deploy matching builds (e.g. `MMOItems-6.10.1.jar` with `MythicLib-dist-1.7.1-b106`). When resolving mismatches on premium plugins, inform the operator to upload the matching purchased JAR rather than transplanting files from other panel instances.
- **Server Database Resets & Preserving Schema Migrations & Currencies**:
  When emptying or resetting server databases (e.g. for season wipes):
  1. Retrieve connection parameters via `GET /api/client/servers/<ID>/databases?include=password`.
  2. Always transition server to `offline` state before executing wipes to prevent active HikariCP connection pool locks or in-flight write corruption.
  3. Dump every database to local `.sql` files before executing any table modifications.
  4. Truncate tables (`SET FOREIGN_KEY_CHECKS = 0; TRUNCATE TABLE \`table\`; SET FOREIGN_KEY_CHECKS = 1;`) rather than dropping tables so schemas, indexes, and column types persist.
  5. **Never truncate migration tables**: Skip tables containing `migration` or `metadata` (e.g. `auraskills_schema_migrations`, `huskclaims_metadata`, `playerpoints_migrations`). Clearing migration history while tables exist triggers initial creation DDL on the next server startup, crashing plugins with `Table already exists` or `Duplicate column name`.
  6. **Player Currency Preservation**: Network economy tables (e.g. `s4077_PlayerPoint`) hold permanent player coins, username caches, and transaction logs that must be preserved across seasonal wipes. Always verify explicit database exclusion lists before executing bulk database commands.
- **ModelEngine 4 Cross-Version Compatibility with ViaVersion / ViaBackwards (1.20.1 to 1.21.4+)**:
  On Minecraft servers running 1.21.4+ (such as UniverseSpigot/Paper 1.21.11), ModelEngine 4 defaults to `Force-Custom-Model-Data: false` in `plugins/ModelEngine/config.yml`. Under this default, ModelEngine transmits modern `item_model` data components on `BONE` or `GLASS` items instead of integer `CustomModelData`. When older clients (Minecraft 1.20.1 through 1.21.3) connect via ViaVersion / ViaBackwards proxy, the client does not support `item_model` components, causing ViaVersion to drop the model metadata and downgrade the item to plain unmodeled `Material.GLASS` or `leather_horse_armor` (which renders in-game as an untextured red translucent cube or crystal). To restore proper model rendering across all client versions 1.20.1 through 1.21.4+:
  1. Set `Force-Custom-Model-Data: true` under `Model-Engine:` in `plugins/ModelEngine/config.yml`.
  2. **Full Server Restart Required**: Do NOT rely on `/meg reload` alone. `/meg reload` only re-parses blueprints and model files; the NMS packet handler (`NMSHandler_v26_2`) initializes its internal `forceCMD` state on startup and will continue sending `Material.GLASS` without CustomModelData until a full server restart is performed.
  3. **Resource Pack Dual Compatibility & 1.20.1 Root Fallback**:
     - Maintain legacy predicate overrides with `custom_model_data` in `assets/minecraft/models/item/leather_horse_armor.json` and modern definitions in `assets/minecraft/items/leather_horse_armor.json`.
     - Minecraft 1.20.1 does not support resource pack `overlays` (introduced in 1.20.2). Any item models placed inside overlay directories (such as `modelengine_1_19_4/assets/minecraft/models/item/player_head.json`) MUST also be copied directly to the root `assets/minecraft/models/item/player_head.json` so 1.20.1 clients load without missing models.
     - In `pack.mcmeta`, declare `pack_format: 15` alongside `"supported_formats": {"min_inclusive": 15, "max_inclusive": 32767}` to eliminate red incompatible-version warnings across both legacy and modern clients.

