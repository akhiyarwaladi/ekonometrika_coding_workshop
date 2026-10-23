# Tutorial ekonometrika dan regresi

Materi untuk pelatihan Program Studi Ekonomi Pembangunan, FEB Universitas Jambi,
26 Oktober 2026. Tutorial dimulai dari contoh yang sudah tersedia, untuk peserta
yang belum mempunyai pengalaman coding.

## Mulai belajar

1. Baca [panduan pemula](panduan/01_panduan_pemula.md).
2. Untuk ekonometrika, buka [00_persiapan_colab.ipynb](materi/01_ekonometrika/00_persiapan_colab.ipynb),
   lalu lanjutkan sesuai nomor. Untuk praktik regresi pada slide, buka
   [01_regresi_housing.ipynb](materi/03_regresi_housing/01_regresi_housing.ipynb).
3. Di Google Colab, unggah notebook dan [data_tutorial.zip](paket/data_tutorial.zip)
   lewat panel **Files**, lalu jalankan sel berurutan dengan **Shift + Enter**.
   Di komputer sendiri, pertahankan susunan folder ini; sel persiapan menemukan
   data secara otomatis dari folder notebook atau folder utama proyek.

Gunakan **`.ipynb` untuk mengajar dan belajar**. Berkas `.py` dengan nama yang sama
adalah sumber penyuntingan dengan penanda sel `# %%`. Sebagian berisi `%pip` milik
notebook; jalankan per sel di Jupyter/Colab, bukan dengan `python nama_file.py`.
Untuk menjalankan secara lokal, pasang paket dari [requirements.txt](requirements.txt)
ke lingkungan Python yang dipakai kernel Jupyter.

## Pola pemodelan

Model linear, logit, multinomial, dan Poisson memakai **scikit-learn** secara
konsisten: tentukan X dan y, buat model, jalankan `fit`, lalu `predict`.
Koefisien dibaca melalui `coef_` dan `intercept_`. Untuk klasifikasi,
`predict` menghasilkan kelas dan `predict_proba` menghasilkan peluang.

P-value, standard error, dan uji asumsi ada pada bagian pelengkap statistik
bernama `uji_...`. Model khusus seperti probit, ordinal, Tobit, ARIMA, panel,
dan GARCH tetap memakai pustaka yang sesuai. Rinciannya ada di
[panduan pemodelan](panduan/06_pola_pemodelan.md).

## Letak berkas

| Folder | Isi dan kegunaan |
|---|---|
| [panduan/](panduan/00_daftar_materi.md) | Daftar materi, cara mulai, glosarium, dan referensi. |
| [materi/01_ekonometrika/](materi/01_ekonometrika/) | Tujuh notebook contoh ekonometrika, urutan 00–06. |
| [materi/02_latihan/](materi/02_latihan/) | Tujuh notebook latihan dan tugas proyek mini. |
| [materi/03_regresi_housing/](materi/03_regresi_housing/) | Praktik regresi sesuai slide dengan data Housing. |
| [data/](data/README.md) | Seluruh 59 CSV untuk tutorial. |
| [paket/](paket/README.md) | Paket data untuk Colab dan ZIP berisi 31 PNG tajam. |
| [slide/](slide/README.md) | Slide pembuka, PDF regresi, dan 31 PNG tajam berukuran 6000 × 3375 piksel. |
| [gambar/](gambar/) | Grafik ekonometrika dan regresi Housing. |
| [pengajar/](pengajar/README.md) | Panduan fasilitator dan tujuh notebook kunci jawaban. |
| [alat_bantu/](alat_bantu/README.md) | Perkakas konversi, pengemasan, dan pemeriksaan. |
| [laporan/](laporan/README.md) | Hasil uji dan peta nama lama ke nama baru. |
| [arsip/](arsip/README.md) | Catatan cadangan dan berkas kerja yang disimpan lokal. |

Nama berkas memakai huruf kecil dan garis bawah, misalnya `01_regresi_dasar.ipynb`
dan `housing.csv`. Nomor menunjukkan urutan belajar. Kunci jawaban memakai nama
yang sama dengan latihan pasangannya. Nama kolom dalam CSV tetap mengikuti data asli.

Lihat [daftar seluruh notebook](panduan/00_daftar_materi.md) untuk memilih sesi,
[rincian kurikulum dan asal data](panduan/05_isi_materi_lengkap.md) untuk persiapan mengajar,
serta [peta perubahan nama](laporan/peta_perubahan_nama.csv) untuk mencari berkas lama.
