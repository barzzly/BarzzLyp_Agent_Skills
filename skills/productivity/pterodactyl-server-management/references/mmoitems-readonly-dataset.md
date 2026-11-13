# Dataset MMOItems dari snapshot read-only

- Seleksi varian dari label nama dan batas bagian konfigurasi, bukan suffix ID saja; label permanen dapat memakai Unicode small caps. Cocokkan hasil seleksi independen, hitung IDs dan binding skill dengan Python.
- Bersihkan ikon, markup warna, dan seluruh bracket masa berlaku hanya pada display name. Pertahankan ID sumber, termasuk kapitalisasi dan typo, pada provenance.
- Telusuri `MMOItems ability.type -> MythicLib skill source -> MythicMobs metaskill`; periksa direktori MythicLib script tetapi jangan menempelkan script generik tanpa referensi eksplisit.
- Sertakan MythicMobs Packs selain Skills. Telusuri callback projectile/aura, castinstead/orelse, randomskill, summoned/projectile mobs, dan templates; jangan berhenti pada root wrapper.
- Gunakan YAML compose beserta mark posisi untuk mempertahankan duplicate top-level keys. Jangan memakai safe_load dictionary saja untuk audit konflik, karena definisi terdahulu hilang diam-diam.
- Bedakan root teresolusi, referensi hilang, deskripsi kosong, dan konflik global antar MMOItems/MMOCore. Snapshot tidak membuktikan urutan load runtime.
- Beri fungsi skill bahasa Indonesia dari mekanik, selain binding parameter dan raw trace. Jangan mengarang efek dari nama; jangan menyebut total DPS dari damage modifier tanpa menelusuri combo/target/repeat.
- Pertahankan angka timer/cooldown dan nyatakan satuan belum diverifikasi bila dokumentasi versi terpasang belum diperiksa. Jangan menebak konversi tick/detik dari nama field.
- Sediakan builder deterministik dengan `--check`: seleksi/count independen, setiap binding memiliki root, semua link trace valid, nama utama bebas label/ikon, fungsi readable ada pada setiap binding, artefak identik dengan regenerasi. Jalankan build lalu check setelah edit terakhir.
