# Workshop ekonometrika Python

Materi pelatihan FEB Universitas Jambi, 26 Oktober 2026.
**Mulai dari halaman ini. Semua kegiatan peserta dijalankan dalam notebook `.ipynb`.**

## Cara mulai

1. Pilih sesi pada [daftar materi](panduan/daftar_materi.md), lalu klik **Buka di Colab**.
2. Simpan salinan ke Google Drive.
3. Jalankan sel dari atas menggunakan **Shift + Enter** dengan koneksi internet.

**CSV dan ZIP tidak perlu diunggah.** Data dibaca langsung dari GitHub.
Jika memakai notebook dari komputer, cukup unggah satu file `.ipynb` yang dipilih.

## Pilih materi

| Urutan | Materi | Letak notebook |
|---|---|---|
| 1 | Contoh ekonometrika | [materi/01_ekonometrika/](materi/01_ekonometrika/) — mulai nomor 00, lanjut 01–06. |
| 2 | Latihan peserta | [materi/02_latihan/](materi/02_latihan/) — kerjakan nomor yang sesuai contoh. |
| 3 | Regresi mengikuti slide | [01_regresi_housing.ipynb](materi/03_regresi_housing/01_regresi_housing.ipynb). |
| 4 | Dashboard ekonomi | [01_dashboard_ekonomi.ipynb](materi/04_dashboard_indonesia/01_dashboard_ekonomi.ipynb). |

**Dashboard hanya satu notebook:** `01_dashboard_ekonomi.ipynb`.
Langkah 8 menampilkan pratinjau, langkah 9 menyediakan ngrok, langkah 10 menghentikannya.
Untuk ngrok, ubah `gunakan_ngrok` menjadi `True`, lalu masukkan token pada input tersembunyi.
Token pengajar disimpan lokal di `pengajar/token_ngrok.txt`; salin isinya saat diminta.

## Letak berkas

| Folder | Kegunaan |
|---|---|
| `materi/` | Notebook untuk peserta dan tugas proyek mini. |
| `data/` | 44 CSV aktif; 15 CSV tambahan berada di `data/cadangan/`. |
| `slide/` | PDF, presentasi, dan [31 PNG tajam](slide/png_regresi_tajam/). |
| `panduan/` | Daftar materi, cara menggunakan notebook, istilah, dan definisi data. |
| `pengajar/` | [Panduan mengajar](pengajar/panduan_mengajar.md), kunci jawaban, dan referensi. |
| `alat_bantu/` | Sumber `.py`, perkakas pengelola, gambar, laporan, paket ZIP, serta arsip. |

Untuk mengetahui CSV yang dipakai suatu sesi, buka [data yang dipakai](panduan/data_yang_dipakai.md).
Baca tabel **Kenali data** sebelum pemodelan; [kamus variabel](panduan/kamus_variabel.md) menjadi rujukan lengkap.
Jika baru memakai Colab, baca [cara menggunakan notebook](panduan/cara_menggunakan_notebook.md).
