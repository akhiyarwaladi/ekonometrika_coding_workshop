# Tutorial ekonometrika dan regresi

Materi untuk pelatihan Program Studi Ekonomi Pembangunan, FEB Universitas Jambi,
26 Oktober 2026. Tutorial dimulai dari contoh yang sudah tersedia, untuk peserta
yang belum mempunyai pengalaman coding.

## Pilih bahan yang dibutuhkan

| Keperluan | Buka |
|---|---|
| Menampilkan slide sebagai gambar | [31 PNG tajam, 6000 × 3375 piksel](slide/png_regresi_tajam/) atau [ZIP seluruh PNG](paket/png_regresi_tajam.zip). |
| Mulai belajar dari awal | [Panduan pemula](panduan/01_panduan_pemula.md), lalu [buka notebook persiapan di Colab](https://colab.research.google.com/github/akhiyarwaladi/ekonometrika_coding_workshop/blob/main/materi/01_ekonometrika/00_persiapan_colab.ipynb). |
| Praktik regresi mengikuti slide | [Buka notebook Housing di Colab](https://colab.research.google.com/github/akhiyarwaladi/ekonometrika_coding_workshop/blob/main/materi/03_regresi_housing/01_regresi_housing.ipynb). |
| Penutup: membuat dashboard interaktif | [Buka notebook dashboard di Colab](https://colab.research.google.com/github/akhiyarwaladi/ekonometrika_coding_workshop/blob/main/materi/04_dashboard_indonesia/01_dashboard_ekonomi.ipynb). Semua langkah dijalankan dari notebook. |
| Memilih contoh atau latihan berikutnya | [Daftar materi dan tautan Colab](panduan/00_daftar_materi.md). |
| Menyiapkan pengajaran | [Bahan pengajar](pengajar/README.md). |

## Langkah untuk peserta

1. Unduh [data_tutorial.zip](paket/data_tutorial.zip) dari folder `paket/`.
2. Buka notebook melalui tautan **Buka di Colab** pada [daftar materi](panduan/00_daftar_materi.md),
   lalu simpan salinan ke Google Drive.
3. Di panel **Files** sebelah kiri Colab, unggah `data_tutorial.zip`.
4. Jalankan sel dari atas dengan **Shift + Enter**. Baca penjelasan dan hasil
   sebelum beralih ke sel berikutnya.

Sebelum membaca tabel data, pelajari bagian **Kenali data** di notebook.
Bagian itu menjelaskan arti setiap kolom, satuan atau kode kategorinya,
serta nama singkat yang dipakai di kode. Definisi seluruh dataset juga ada di
[kamus variabel](panduan/07_kamus_variabel.md).

Gunakan **`.ipynb` untuk belajar dan mengajar**. Ikuti contoh di
`materi/01_ekonometrika/`, kemudian kerjakan `materi/02_latihan/` dengan nomor
yang sama. Praktik Housing di `materi/03_regresi_housing/` dapat dipelajari tersendiri.
ZIP PNG dipakai untuk gambar slide; ZIP data dipakai untuk menjalankan notebook.

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
| [materi/](materi/README.md) | Petunjuk memilih contoh, latihan, dan praktik Housing. |
| [materi/01_ekonometrika/](materi/01_ekonometrika/README.md) | Tujuh notebook contoh ekonometrika, urutan 00 sampai 06. |
| [materi/02_latihan/](materi/02_latihan/README.md) | Tujuh notebook latihan dan tugas proyek mini. |
| [materi/03_regresi_housing/](materi/03_regresi_housing/README.md) | Praktik regresi sesuai slide dengan data Housing. |
| [materi/04_dashboard_indonesia/](materi/04_dashboard_indonesia/README.md) | Materi penutup: dashboard, grafik interaktif, regresi, dan simulasi dari notebook. |
| [data/](data/README.md) | Seluruh 59 CSV untuk tutorial. |
| [paket/](paket/README.md) | Paket data untuk Colab dan ZIP berisi 31 PNG tajam. |
| [slide/](slide/README.md) | Slide pembuka, PDF regresi, dan 31 PNG tajam berukuran 6000 × 3375 piksel. |
| [gambar/](gambar/README.md) | Grafik ekonometrika dan regresi Housing. |
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

## Menjalankan lokal atau menyunting materi

Di Jupyter atau VS Code, buka `.ipynb` dan pertahankan susunan folder proyek.
Pasang paket dari [requirements.txt](requirements.txt) pada lingkungan Python
yang dipakai kernel. Sel persiapan menemukan data dari folder notebook atau
folder utama proyek.

Berkas `.py` dengan nama yang sama adalah sumber penyuntingan, dengan penanda
sel `# %%`. Sebagian berisi perintah `%pip` milik notebook. Jalankan per sel
di Jupyter/Colab. Cara memperbarui notebook dan memeriksa hasil ada di
[panduan alat bantu](alat_bantu/README.md).
