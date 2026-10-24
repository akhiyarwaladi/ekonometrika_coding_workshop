# Paket tutorial

## PNG slide versi tajam

[png_regresi_tajam.zip](png_regresi_tajam.zip) berisi 31 gambar PNG terpisah,
dari `halaman_01.png` sampai `halaman_31.png`. Setiap gambar berukuran
6000 × 3375 piksel dengan metadata 600 dpi. ZIP ini hanya berisi gambar PNG.
Gambar juga tersedia langsung di [folder PNG tajam](../../slide/png_regresi_tajam).
Pengelola membuat ulang ZIP dengan `python alat_bantu/kemas_png.py`.

## Salinan data offline opsional bagi pengajar

Lokasi berkas: **[alat_bantu/paket/data_tutorial.zip](data_tutorial.zip)**.
Isinya folder `data/` dengan **44 CSV aktif** dan `alat_bantu/metode_lanjutan.py`.
Lima belas CSV cadangan tidak disertakan karena belum dipakai oleh notebook saat ini.

Alur peserta adalah membuka notebook dan menjalankan sel `URL_DATA`; CSV dibaca
langsung dari GitHub dengan koneksi internet. Untuk mengetahui file yang dipakai,
buka [peta pemakaian data per notebook](../../panduan/data_yang_dipakai.md).
Dashboard hanya memakai `provinsi_2021.csv`.

Untuk kelas offline, pengajar mengekstrak ZIP dan menyiapkan pustaka terlebih dahulu,
lalu mengganti nilai `URL_DATA` menjadi alamat absolut folder `data/` lokal dengan `/` di akhir.
Contoh pada Windows: `URL_DATA = "C:/kelas/data/"`.
Pada model kategorikal, modul pendukung juga perlu tersedia pada kernel lokal.
Pratinjau Colab tetap memerlukan koneksi internet.

Pengelola membuat ulang ZIP dengan `python alat_bantu/kemas_data.py` dari folder utama.
