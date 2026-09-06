# BarzzLyp Agent Skills

**BarzzLyp Agent Skills** adalah kumpulan skill, prosedur, template, dan tool workflow untuk **Hermes Agent** yang digunakan dan dikembangkan oleh **Pak Boss Barzzly**.

Repository ini menjadi backup publik serta arsip pengetahuan Agent. Backup berjalan otomatis dari mesin Hermes Agent ke GitHub.

## Tentang BarzzLyp Agent

BarzzLyp Agent adalah instance Hermes Agent milik Pak Boss Barzzly.

Agent membantu menjalankan pekerjaan teknis melalui terminal, browser, GitHub, file system, riset web, otomasi, dan tool lain yang tersedia. Agent memakai skill sebagai panduan prosedural supaya pekerjaan berulang lebih konsisten, dapat diverifikasi, dan tidak selalu dimulai dari nol.

Skill dapat berisi:

- Workflow software development dan GitHub.
- Riset, dokumentasi, dan knowledge base.
- Otomasi terminal, cron, dan background task.
- Pembuatan serta validasi dokumen.
- Workflow media, web, produktivitas, dan integrasi platform.
- Panduan khusus project yang dipelajari selama pekerjaan.

## Tentang Pak Boss Barzzly

**Pak Boss Barzzly** adalah pemilik dan pengarah BarzzLyp Agent.

Pak Boss Barzzly menentukan tujuan pekerjaan, standar hasil, batasan keamanan, gaya desain, dan keputusan akhir. Agent bertugas membantu mengeksekusi pekerjaan, memeriksa hasil dengan tool nyata, lalu melaporkan status secara singkat dan jujur.

## Hubungan Dengan Hermes Agent

Hermes Agent adalah framework agent open-source dari Nous Research. BarzzLyp Agent berjalan di atas Hermes Agent dengan konfigurasi, skill, memory, workflow, dan project context milik Pak Boss Barzzly.

Repository ini **bukan repository resmi Hermes Agent**. Isinya adalah backup skill yang digunakan oleh instance BarzzLyp Agent.

## Backup Otomatis

- **Source:** `~/.hermes/skills`
- **Backup script:** `~/.hermes/scripts/backup-agent-skills.py`
- **Repository:** `https://github.com/barzzly/BarzzLyp_Agent_Skills`
- **Branch:** `main`
- **Jadwal:** setiap hari pukul `06:00`, `14:00`, dan `22:00` UTC
- **Mode:** script-only, tanpa intervensi manual
- **Backup pertama:** berhasil dipush ke GitHub

Backup menyinkronkan skill terbaru ke repository saat jadwal berjalan. Perubahan hanya dipush jika ada perbedaan.

## Data Yang Tidak Disimpan

Backup mengecualikan:

- API key, access token, password, dan private key.
- File `.env` dan credential runtime.
- Memory pribadi dan session transcript.
- Usage telemetry dan curator state.
- Log runtime dan Python bytecode.

Skill tetap perlu ditinjau sebelum dibagikan karena dokumentasi bisa memuat contoh domain, path, nama service, atau detail operasional. Backup script melakukan redaksi endpoint operasional ke placeholder environment sebelum commit.

## Lisensi & Penggunaan

Isi repository ini adalah arsip workflow BarzzLyp Agent. Jangan menganggap semua skill sebagai dokumentasi resmi Hermes Agent atau dokumentasi resmi layanan pihak ketiga.

Gunakan dengan izin yang sesuai, periksa dependency, dan jangan menyalin credential atau data pribadi ke repository publik.
