---
name: multi-panel-sentinel-operations
description: Use when building multi-panel Pterodactyl sentinel cron.
metadata:
  hermes:
    tags: [devops, monitoring, pterodactyl, sentinel, cron, cloudflare]
    category: devops
---

# Multi-Panel Sentinel Operations

## Telemetry Report Format & Typography Rules
- **Delivery Destination:** Route VPS Sentinel reports directly to Discord monitoring channel (`1570029605107146752`) via BarzzLyDev Bot (`run-sentinel-discord.py`), BUKAN ke Telegram (`deliver: local` pada cron Hermes).
- **Discord Heading 1:** Gunakan `# Nama Kategori` (wajib ada spasi setelah `#`) di description embed agar Discord merender teks sebagai Heading 1 besar yang tegas.
- **Category Titles & Headers:** Wajib format Heading (`# Metrik Sistem VPS`, `# Status Service VPS`, `# Status Service C-Console`, `# Status Service C-Ultras`).
- **Service & Server Names:** Wajib BOLD (**OS-Ubuntu**, **NOESANTARA BOT DC**, dll).
- **Status Value:** Wajib format inline code (\`ONLINE\`, \`RUNNING\`, \`OFFLINE\`, \`SUSPENDED\`).
- **Spacing:** WAJIB beri 1 baris kosong (jarak 1 enter kosong / `\n\n`) antara judul kategori dengan service pertama, serta 1 baris kosong di antara setiap baris service/server agar tidak dempet di Discord mobile/desktop.
- **Footer Discord Embed:** Tampilkan teks `BarzzLyDev • MM/DD/YYYY hh:mm AM/PM` (WIB) dengan avatar BarzzLyDev icon. Jangan menyisipkan field spacer buatan (`\u200B`) sebelum footer karena membuat gap kosong terlalu jauh.
- **Embed Colors:**
  * START & FINISH (Done): Wajib Biru (`#3498db`). Embed rekapitulasi akhir backup yang sukses berwarna BIRU (bukan hijau).
  * ITEM SUCCESS: Hijau (`#2ecc71`).
  * ERROR / FAILED: Merah (`#e74c3c`).
  * ANOMALY / WARNING: Kuning (`#f1c40f`).
- **Service Filtering:** Kecualikan service yang telah dipindahkan/dijalankan di dalam container panel Pterodactyl (seperti Discord bot) dari daftar service host VPS.
- **OS Base Memory Calculation:** Hitung physical RSS murni dari root core OS processes (`ps -u root` minus daemon Docker/Wings/DB/Apps). Jangan mengandalkan sisa pengurangan total memory jika host juga menampung container Pterodactyl/Minecraft lokal, agar RAM OS tidak tampak bengkak secara semu.

## Multi-Panel Pterodactyl Integration
- For replicating daily restart schedules across panels, use `references/pterodactyl-schedule-replication.md`; convert WIB to UTC, clone tasks, use `action: power` with `payload: restart`, and read back active schedule/task counts.
- **Credentials:** Simpan endpoint dan API key di `~/.config/pterodactyl.env`:
  - `PTERODACTYL_PANEL_URL` & `PTERODACTYL_API_KEY` (UltraServers)
  - `PTERODACTYL_CONSOLE_URL` & `PTERODACTYL_CONSOLE_API_KEY` (BarzzLy panel, currently `https://panel.barzzly.com/`)
- **Cloudflare & HTTP/2 Polling:** Panel game server pihak ketiga (seperti UltraServers) sering berada di balik Cloudflare WAF. Gunakan `curl --http2` dengan `--connect-timeout 5 --max-time 15`, sertakan header `-H 'User-Agent: curl/8.5.0'` (default Python `urllib` diblokir Cloudflare hingga timeout), dan gunakan konkurensi (`concurrent.futures.ThreadPoolExecutor`) saat polling `/resources` tiap server agar tidak memicu timeout atau memblokir eksekusi skrip cron.
- **Root Cause Server Down/Reboot:** Jika game server terpencil (misal UltraServers ECORPG) tiba-tiba shutdown bersih (`ThreadedAnvilChunkStorage: All dimensions are saved`), periksa error upstream database di log (`CommunicationsException` / HikariPool socket timeout). Reboot pada container database pusat (misal `NOESANTARA DATABASE` di console.barzzly) memicu shutdown protektif pada plugin Paper agar data chunk/player tidak korup. Selaraskan dengan power action di Wings host (`sudo tail -n 50 /var/log/pterodactyl/wings.log`) untuk melacak event `action=restart`/`action=stop`.
- **Pterodactyl Egg Startup Detection:** Jika container aplikasi di Pterodactyl berstatus kuning (`STARTING`) terus-menerus padahal service sudah aktif di log, periksa field `config_startup` pada tabel `eggs` di database panel (`panel.eggs`). Pastikan field `"done"` berupa string regex/literal tunggal (misal: `{"done": "Bot aktif sebagai"}`), BUKAN JSON array. Pterodactyl Wings (Go) meng-unmarshal `"done"` sebagai string; jika diset array `["..."]`, unmarshal gagal dan status server tertahan `starting` permanen. Selain itu, pastikan script container mencetak newline `\n` sebelum string deteksi agar tidak tergabung dengan karakter spinner `npm install` (misal `/Bot aktif sebagai`).

## VPS & Panel Backup Sentinel Operations
- **Dynamic Server Discovery:** Jangan hardcode UUID server panel di script backup. Query tabel `panel.servers` (`SELECT uuid, name FROM panel.servers`) secara dinamis setiap kali cron jalan, agar server game/bot baru (seperti bot discord baru) langsung otomatis masuk ke daftar backup.
- **Backup Boundary:** Bedakan backup Google Drive + notifikasi Discord (`/usr/local/bin/backup-sentinel.py`, root cron `04:00`) dari backup skill GitHub Hermes (`~/.hermes/scripts/backup-agent-skills.py`, cron `06:00/14:00/22:00`). Keduanya punya tujuan, retention, dan verifikasi berbeda.
- **BarzzLy & Minecraft Skill Scope:** Backup Drive menyimpan `/home/barzzly/BarzzLy` ke `gdrive:Backup Server/BarzzLy/` bila folder ada, serta `/home/barzzly/Minecraft/skills` ke `gdrive:Backup Server/Minecraft/Skills/`. Exclude `.env`, key, database, log, ZIP/JAR, cache dan binary generated files. Verifikasi item upload dan notif Discord terpisah; local ZIP saja bukan bukti upload.
- **Kategori Destinasi Backup (Google Drive):**
  * `Server Panel/<NAMA_SERVER>/backup-<slug>-YYYY-MM-DD.zip`: Untuk semua server panel (kecuali container DB). Exclude file log & cache (`*.log`, `*/logs/*`, `*/cache/*`, `*/crash-reports/*`).
  * `Database/NOESANTARA DATABASE/backup-noesantara-database-YYYY-MM-DD.zip`: Khusus volume container DB panel (port 19138).
  * `Database/WEBSITE DATABASE/backup-website-database-YYYY-MM-DD.zip`: Dump host MariaDB via `mariadb-dump --all-databases --single-transaction --quick` lalu di-zip.
  * `Website/<NAMA_WEB>/backup-<slug>-YYYY-MM-DD.zip`: Folder web (seperti `Noesantara-Website`), exclude `node_modules/`, `.git/`, `dist/`.
- **Zero Game Lag & Disk Safety:**
  * Jalankan seluruh proses kompresi dan upload dengan prioritas terendah via `nice -n 19 ionice -c 3`.
  * Gunakan kompresi cepat (`zip -1 -q -r`) untuk menghindari spike CPU pada chunk Minecraft yang sudah terkompres Anvil. Lewati folder kosong jika tidak ada file untuk di-zip guna menghindari exit code 12 (`Nothing to do`).
  * Batasi bandwidth upload via `rclone copy --bwlimit 240M --tpslimit 10`. Batas query `--tpslimit 10` wajib disertakan agar shared OAuth client ID tidak terkena `403 RATE_LIMIT_EXCEEDED` dari Google Drive.
  * Tambahkan `--timeout 1m --contimeout 30s --drive-chunk-size 64M --retries 3 --low-level-retries 10` pada perintah rclone. Chunk 64 MB memaksimalkan throughput stream Google Drive API, dan timeout eksplisit mencegah rclone menggantung permanen pada socket TCP saat Google Drive idle commit.
  * Sanitasi nama folder target di Google Drive: gantikan karakter slash `/` menjadi tanda minus `-` (`name.upper().replace('/', '-')`, contoh: `NOESANTARA DEV/EVENT` menjadi `NOESANTARA DEV-EVENT`) agar rclone tidak salah memecahnya menjadi subfolder bersarang.
  * Backup per-item ke staging lokal (`/var/backups/sentinel_staging/`), upload ke remote, lalu hapus zip lokal seketika sebelum memproses item berikutnya agar disk VPS tetap 0% overhead.
  * Bersihkan file backup lama berumur > 7 hari di Google Drive otomatis pada setiap akhir proses backup via `rclone --tpslimit 10 delete --min-age 7d "gdrive:Backup Server"`.
  * Embed laporan backup wajib mencantumkan waktu mulai pada notifikasi start, serta waktu mulai, waktu selesai, total durasi, dan total ukuran pada notifikasi finish. Jarak footer harus natural tanpa spacer field dummy. Selesai akhir (finish) berwarna BIRU.
- **Headless Google Drive OAuth via rclone:**
  * Di VPS tanpa desktop browser, jalankan `rclone authorize "drive"` di background, tangkap URL lokal `http://127.0.0.1:53682/auth?state=...` dan redirect location Google OAuth.
  * User membuka link Google OAuth di browser HP/PC, login, dan klik Izinkan.
  * Saat browser diarahkan ke `http://127.0.0.1:53682/?state=...&code=...` dan menampilkan error koneksi, minta user menyalin URL address bar tersebut.
  * Script VPS melakukan HTTP GET ke `http://127.0.0.1:53682/?<query>` lokal, menyelesaikan handshake OAuth, dan menyimpan token ke `~/.config/rclone/rclone.conf`.
- **Root Crontab Rclone Config:** Saat script backup dijalankan dari root crontab, rclone secara default mencari config di `/root/.config/rclone/rclone.conf`. Buat symlink `/root/.config/rclone -> /home/barzzly/.config/rclone` atau lewatkan flag `--config /home/barzzly/.config/rclone/rclone.conf` secara eksplisit.
- **Cron Worker Linger:** Pada host Ubuntu baru, pastikan user non-root di-set `sudo loginctl enable-linger <user>`. Tanpa linger, worker background cron Hermes berbasis `systemd-run --user --scope` akan gagal dispatch dengan error `User ID ... is not logged in or lingering`.

## Host Utilities & Network Performance
- **Speedtest CLI Native:** Hindari menginstal paket `speedtest-cli` via `apt` (itu script Python lawas tahun 2021 yang single-thread, probing sering macet/stuck di server lambat, dan membatasi throughput < 1 Gbps). Gunakan binary native resmi Ookla (tarball dari `install.speedtest.net`) di `/usr/bin/speedtest`. Jalankan `hash -r` di sesi bash setelah mengganti binary untuk mereset cache path.
- **High-Speed Downloads (IDM Pattern):** Untuk mendownload file besar di Linux, hindari single-connection `wget` atau `curl`. Gunakan `aria2c -x 8 -s 8 -k 1M "<URL>"` agar file dipecah menjadi beberapa segmen simultan dan memaksimalkan port bandwidth VPS tanpa ter-throttle oleh rate limiter per koneksi di sisi server pengirim.
- **Discord Bot Permission Isolation:** Jika ada bot Discord pihak ketiga yang ditambahkan ke server Discord (misal bot asisten), periksa rolenya. Jika bot tersebut memegang role dengan permission `Administrator: true`, bot otomatis dapat melihat seluruh channel privat/tiket. Matikan centang `Administrator` pada role bot tersebut, lalu beri izin `View Channel`, `Send Messages`, dan `Read Message History` hanya pada channel spesifik yang diizinkan untuk diakses.
- **Pterodactyl Panel Web Asset Replacement (Favicon/Logo):** Mengganti favicon panel Pterodactyl tidak memerlukan restart Wings maupun daemon server. Generate asset favicon lengkap (`favicon.ico`, `favicon-16x16.png`, `favicon-32x32.png`, `favicon-96x96.png`, dan seluruh variasi ukuran apple/android icon) menggunakan `convert` (ImageMagick) ke direktori `/var/www/pterodactyl/public/favicons/` dan `/var/www/pterodactyl/public/favicon.ico`. Pastikan permission diset ke `chown -R www-data:www-data`. Browser pengguna cukup melakukan hard refresh (`Ctrl + F5` atau incognito) untuk membersihkan cache statis.
- **Zero-Disk Cloud Streaming (Pterodactyl to Cloud Storage):** Untuk backup atau migrasi file berukuran sangat besar (misal arsip zip puluhan GB) dari server game Pterodactyl yang memiliki batas disk lokal ketat, gunakan `rclone copyurl "<DOWNLOAD_URL>" <REMOTE>:<PATH>` langsung dari direct download endpoint Pterodactyl API (`/api/client/servers/<ID>/files/download`). Stream data ditampung dalam buffer RAM (`--buffer-size 64M --drive-chunk-size 64M/128M`), menghasilkan 0 byte konsumsi storage disk lokal VPS.
- **Handling Large Google Drive Shared Files via CLI:** File Google Drive publik/share berukuran besar (>100 MB) tidak bisa di-download via URL direct statis sederhana karena Google menyisipkan halaman konfirmasi virus scan (`Google Drive - Virus scan warning`). Dapatkan download token dan session cookies terlebih dahulu via `GET https://drive.usercontent.google.com/download?id=<FILE_ID>&export=download`, ekstrak nilai `confirm` dan `uuid` dari form HTML, lalu eksekusi download berkecepatan tinggi dengan resume support via `curl -L -C - -A "Mozilla/5.0" -H "Cookie: <COOKIES>" -o <DEST> "https://drive.usercontent.google.com/download?id=<FILE_ID>&export=download&confirm=<CONFIRM>&uuid=<UUID>"`.
- **Direct Large File Upload to Remote Pterodactyl (Wings API):** Saat mentransfer file raksasa (puluhan GB) ke server game Pterodactyl tanpa akses terminal host tujuan, minta endpoint upload via Client API (`POST /api/client/servers/<ID>/files/upload`). Endpoint tersebut mengembalikan URL Wings langsung (`https://<NODE_HOST>:<PORT>/upload/file?token=...`). Upload file utuh menggunakan streaming multipart curl: `curl -v -F "files=@<LOCAL_FILE>" "<UPLOAD_URL>&directory=%2F"`. Wings akan menampung dan menulis file secara streaming langsung ke direktori root volume server tanpa perantara panel HTTP proxy.
