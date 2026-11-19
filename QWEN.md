# Aturan Wajib Pengerjaan Bounty make.fun

1. **Integritas Transkrip (`thinking_priced` & `transcripts_witnessed`):**
   - Jangan pernah menghapus, mengedit, atau memadatkan (autocompact) riwayat pesan di dalam sesi build.
   - Pastikan seluruh sesi berjalan 100% menggunakan satu model resmi yang terdaftar harganya di `make.fun`.

2. **Efisiensi Token & Rate Limit:**
   - Gabungkan beberapa perintah `Shell` menggunakan `&&` dalam satu eksekusi.
   - Hindari membaca file log atau file kode raksasa berulang kali; baca seperlunya atau gunakan `grep`/`head`/`tail`.
   - Jangan pernah menuliskan atau meng-commit API key ke dalam kode maupun repositori.

3. **Standar Riset & Eksekusi Bounty:**
   - Selalu unduh kit terbaru dan baca `RULES.txt` secara lengkap sebelum menulis kode.
   - Ambil dan pelajari data leaderboard peringkat 1–10 yang tersedia secara publik, catat seluruh kelebihan dan keunggulan mereka, lalu kompilasikan menjadi solusi yang jauh lebih unggul dan akurat.
   - Pastikan output program 100% deterministik (2 kali run identik byte-by-byte; dilarang memakai `Date.now()`, `Math.random()`, atau network call saat runtime).

4. **Validasi & Rem Submit Manual:**
   - Jalankan pengujian lokal dan perintah `check` resmi hingga seluruh gate lulus 100%.
   - **DILARANG keras menjalankan `submit` secara otomatis.** Berhenti setelah laporan akhir dan status `check` tampil, lalu tunggu persetujuan manual dari pengguna.
