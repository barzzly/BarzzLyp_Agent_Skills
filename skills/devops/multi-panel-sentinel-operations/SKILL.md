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
- **Category Titles & Headers:** Wajib BOLD (**Metrik Sistem VPS:**, **Status Service VPS:**, **Status Service C-Ultras:**).
- **Service & Server Names:** Wajib BOLD (**OS-Ubuntu (Host VPS)**, **NOESANTARA BOT DC**, dll).
- **Status Value:** Wajib BOLD (status **ONLINE**, status **RUNNING**, status **OFFLINE**, status **SUSPENDED**).
- **Spacing:** WAJIB beri 1 baris kosong (jarak 1 enter kosong) antara judul kategori dengan service pertamanya, serta 1 baris kosong di antara setiap baris service/server agar tidak rapat di Telegram.
- **Service Filtering:** Kecualikan service yang telah dipindahkan/dijalankan di dalam container panel Pterodactyl (seperti Discord bot) dari daftar service host VPS.
- **OS Base Memory Calculation:** Hitung physical RSS murni dari root core OS processes (`ps -u root` minus daemon Docker/Wings/DB/Apps). Jangan mengandalkan sisa pengurangan total memory jika host juga menampung container Pterodactyl/Minecraft lokal, agar RAM OS tidak tampak bengkak secara semu.

## Multi-Panel Pterodactyl Integration
- **Credentials:** Simpan endpoint dan API key di `~/.config/pterodactyl.env`:
  - `PTERODACTYL_PANEL_URL` & `PTERODACTYL_API_KEY` (UltraServers)
  - `PTERODACTYL_CONSOLE_URL` & `PTERODACTYL_CONSOLE_API_KEY` (BarzzLy Console)
- **Cloudflare & HTTP/2 Polling:** Panel game server pihak ketiga (seperti UltraServers) sering berada di balik Cloudflare WAF. Gunakan `curl --http2` dengan `--connect-timeout 5 --max-time 15`, sertakan header `-H 'User-Agent: curl/8.5.0'` (default Python `urllib` diblokir Cloudflare hingga timeout), dan gunakan konkurensi (`concurrent.futures.ThreadPoolExecutor`) saat polling `/resources` tiap server agar tidak memicu timeout atau memblokir eksekusi skrip cron.
- **Root Cause Server Down/Reboot:** Jika game server terpencil (misal UltraServers ECORPG) tiba-tiba shutdown bersih (`ThreadedAnvilChunkStorage: All dimensions are saved`), periksa error upstream database di log (`CommunicationsException` / HikariPool socket timeout). Reboot pada container database pusat (misal `NOESANTARA DATABASE` di console.barzzly) memicu shutdown protektif pada plugin Paper agar data chunk/player tidak korup. Selaraskan dengan power action di Wings host (`sudo tail -n 50 /var/log/pterodactyl/wings.log`) untuk melacak event `action=restart`/`action=stop`.
- **Pterodactyl Egg Startup Detection:** Jika container aplikasi di Pterodactyl berstatus kuning (`STARTING`) terus-menerus padahal service sudah aktif di log, periksa field `config_startup` pada tabel `eggs` di database panel (`panel.eggs`). Pastikan array `"done"` memuat teks unik yang dicetak aplikasi saat selesai booting (misal: `"Bot aktif sebagai"`).
- **Cron Worker Linger:** Pada host Ubuntu baru, pastikan user non-root di-set `sudo loginctl enable-linger <user>`. Tanpa linger, worker background cron Hermes berbasis `systemd-run --user --scope` akan gagal dispatch dengan error `User ID ... is not logged in or lingering`.
