# PLAYBOOK — Aturan Tetap Bounty make.fun

> **Baca PERTAMA sebelum memulai bounty apa pun.**  
> Dipakai bersama `LESSONS.md` (jangan ditimpa).

---

## A. Klasifikasi Bounty

Selalu klasifikasi dulu sebelum terjun:

- **Dinilai angka murni** (forecast / kecepatan / akurasi) = **prioritas**.
- **Dinilai juri AI** = hanya ikut kalau ada rencana konkret masuk **5 besar**.

Untuk setiap bounty, **laporkan dulu**:
1. Cara penilaian
2. Pembagian hadiah
3. Biaya masuk (*entry fee*)
4. Kuota submit
5. Jam tutup (**WIB**)
6. Apakah ada putaran final yang menilai ulang?

---

## B. Strategi Anti-Disalip

1. **Jaring pengaman:** Masukkan versi kuat lebih awal, lalu kunci sebagai *final-entry*.
2. **Benchmark nyata:** Selama fase dev, baca alasan juri untuk entri **kita**, plus judul/cover/repo publik **5–10 entri teratas**. Bandingkan langsung dengan mereka, bukan cuma dengan entri *house*. Skor tinggi melawan *house* **bukan berarti kuat melawan peserta**.
3. **Serangan balik tepat waktu:** Lakukan 2–3 jam sebelum tutup, bukan di menit terakhir. Perhitungkan:
   - Antrean penilaian
   - Kuota 3 submit/hari UTC (**reset 07:00 WIB**)
   - Login yang bisa kedaluwarsa
   - Ganti *final-entry* **hanya kalau versi baru terbukti lebih baik**.
4. **Target 5 besar dengan jarak aman:** Selisih skor di bawah **1 poin** dianggap derau (*noise*).

---

## C. Aturan Keamanan (Selalu Berlaku)

- ❌ Jangan sentuh / pindahkan *credentials*
- ❌ Jangan daftar ulang (*re-register*)
- ❌ Jangan tanda tangani transaksi
- ❌ *Prompt* pembuka sesi rekaman harus diketik **user sendiri**
- ❌ Repo publik hanya berisi file yang perlu dan **di-scan sebelum push**
- ❌ **Push dan submit selalu minta izin user**
- 🕐 Semua jam dalam **WIB**

---

## D. Kuota Claude

Sebelum mulai pekerjaan berat, cek apakah ada jadwal cron yang menunggu:

```bash
crontab -l
```

Jangan habiskan kuota menjelang jadwal itu.

---

## E. Pelajaran dari Pemain Top (cheneyc9, $427 dalam 10 hari)

1. **Ralat bagian A:** Prioritas bukan "dinilai angka", tapi **"di mana kita punya keunggulan nyata"**. *Forecast* / *trading* tetap ketat persaingannya.
2. **Bounty tulisan pendek juri AI** (*laugh / happy / excited / relaxed*): murah dan bisa masuk 3 besar. Kuncinya: sangat pendek, ada kejutan, suara khas, **tidak menceramahi juri**.
3. **Bounty berhadiah besar** (*game / code*): kirim beberapa versi yang terus diperbaiki — satu juara 2 bisa bernilai **$200**.
4. **Jangan lewatkan bounty ringan** (gambar, tagline) kalau biaya kuotanya kecil.
5. **Hindari bot trading martingale.**

---

## F. Kuota Submit Indonesia (High-Risk Country)

Indonesia diklasifikasi "high-risk country" di make.fun:
- **3 submit/hari UTC** untuk akun tanpa win/podium (cap naik ke 10/hari setelah menang pertama)
- **20 total entries** per competition (hard limit)
- Untuk bounty harian yang tutup 00:00 UTC (07:00 WIB): hanya 3 slot total!

**Strategi:**
1. **Submit versi terbaik di slot pertama.** Jangan buang slot untuk tes.
2. **Cek payout delegation sebelum bounty pertama** di akun baru: `GET /api/agents/me/delegations`. Revoke kalau ada, atau pastikan agent key punya scope `profile`.
3. **Bundle butuh flags lengkap** untuk Qwen Code: `--dry-run` dulu, lalu isi `--system-prompt`, `--context`, `--harness`, `--provider`, `--model`, `--effort`, `--mcp`.
4. **`gh auth setup-git`** sekali setelah `gh auth login --with-token` agar `git push` jalan.
5. **Full 40-char SHA** untuk submit (bukan short SHA).
6. **README badges + GitHub About** wajib sebelum submit (3 badge live + topic `makefun`).

## G. Pola Gambar Pemenang (news-image bounty)

Dari analisis pixel top 5 `news-image-20261117`:
- **42 stories** di 6 continents (bukan 18, bukan 30 — tepat 42)
- Struktur: **3 lead stories (dengan ilustrasi SVG) → 10 panels → 29 "also" list (4 kolom)**
- Background: **cream `#f7f2e6`**, bukan putih/gelap
- Tanggal: **serif besar** (NotoSerif/DejaVu), ~52-80px, centered
- **Day-in-numbers strip**: 6 statistik kunci
- **World map**: 10-32% area gambar, simplified continents + region dots
- Region colors: EU=blue, ME=orange, AS=purple, AF=green, AM=red, OC=teal
- File size: **100-360KB** (jangan <50KB = over-compressed; jangan >500KB kecuali perlu)
- Ilustrasi SVG di lead stories = value besar untuk judge AI
- Judge: `z-ai/glm-5.3-flash` (gambar dibandingkan berpasangan, Bradley-Terry win rate)
- Tiebreaker: playoff wins → **file lebih kecil menang** → submit lebih awal

## H. Infrastruktur Termux

- **No `/tmp`**: redirect log ke project dir atau `$PREFIX/tmp`
- **No `termux-wake-lock`** (non-root): layar harus menyala untuk background jobs
- **No `crontab`**: pakai polling-loop bash + nohup
- **Cloudflare tunnel**: `cloudflared tunnel --url http://127.0.0.1:<port>` untuk serve local page ke Android browser
- **Phantom signing**: `sign.py` local HTML page → user sign di Phantom app → paste base58 signature
- Fonts: Roboto + RobotoCondensed + NotoSerif tersedia di `/system/fonts/`

---

*Terakhir diperbarui: 2026-11-19*