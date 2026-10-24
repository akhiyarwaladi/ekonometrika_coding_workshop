# Alat bantu pengelola tutorial

Peserta cukup membuka notebook di `materi/`. Perintah di bawah dijalankan dari
folder utama proyek, memakai Python yang sudah dipasangi `requirements.txt`.
Untuk perkakas pengelola, pasang tambahan dengan
`python -m pip install -r alat_bantu/requirements_pengelola.txt`.

| Perintah | Hasil |
|---|---|
| `python alat_bantu/konversi_notebook.py` | Membuat 23 notebook dari sumber `.py`, termasuk kunci jawaban dan dashboard. Output lama dikosongkan. |
| `python alat_bantu/sinkron_kamus_variabel.py` | Memperbarui tabel definisi pada 23 pasangan `.py`/`.ipynb` dan panduan kamus; kode serta output notebook dipertahankan. |
| `python alat_bantu/sinkron_kamus_variabel.py --periksa` | Memastikan seluruh kolom CSV sudah didefinisikan dan tabel definisi pada sumber/notebook tetap sinkron. |
| `python alat_bantu/kemas_data.py` | Membuat ulang `paket/data_tutorial.zip` dari 59 CSV dan `metode_lanjutan.py`. |
| `python alat_bantu/kemas_png.py` | Memeriksa ukuran dan kelengkapan 31 PNG tajam, lalu membuat ulang `paket/png_regresi_tajam.zip`. |
| `python alat_bantu/uji_notebook.py` | Memeriksa sinkronisasi, keterbacaan kode, dan eksekusi seluruh notebook dari folder utama. |
| `python alat_bantu/uji_notebook.py --dari-folder-notebook` | Menguji data ditemukan dari folder masing-masing notebook. |
| `python alat_bantu/uji_notebook.py --dari-zip` | Menguji setiap notebook pada folder kosong yang hanya berisi paket ZIP. |
| `python alat_bantu/uji_regresi_housing.py` | Menjalankan kernel baru, menyimpan output Housing, enam grafik, dan laporan pengujian. |
| `python alat_bantu/uji_semua_notebook.py` | Menjalankan seluruh 23 notebook pada kernel baru, termasuk sel instalasi; menyimpan output dan laporan kesesuaian model. |
| `python alat_bantu/uji_dashboard.py --notebook` | Menguji interaksi dashboard, angka evaluasi, filter kosong, dan seluruh sel notebook pada kernel baru; server uji dihentikan otomatis. |
| `python alat_bantu/periksa_paket.py` | Memeriksa nama, tautan, hash data, kesesuaian ZIP, dan pasangan notebook; menyimpan laporan penataan. |
| `python alat_bantu/buat_gambar.py` | Membuat ulang grafik di `gambar/ekonometrika/`. |
| `python alat_bantu/buat_slide.py` | Membuat ulang `slide/01_pengantar_workshop.pptx`. |
| `python alat_bantu/ekspor_slide_tajam.py` | Membuat 31 PNG 6K di `slide/png_regresi_tajam/`, memperbarui ZIP PNG, dan menyimpan PDF vektor pendamping. |
| `python alat_bantu/buat_data_simulasi.py` | Menulis ulang 17 CSV simulasi dari tabel yang tercantum dalam skrip. |
| `python alat_bantu/unduh_data_indonesia.py` | Memperbarui data dari sumber daring; memerlukan internet dan dapat mengubah isi CSV. |

`metode_lanjutan.py` memuat estimasi Tobit dan penanganan demonstrasi separation.
Peserta menggunakannya lewat notebook; kode implementasinya disimpan di sini.

Konversi dan uji umum menerima lokasi file/folder untuk mengerjakan sebagian materi,
misalnya `python alat_bantu/konversi_notebook.py materi/03_regresi_housing`.
Uji umum melewati sel instalasi `%pip`; dependensi harus sudah tersedia.
Log dan ringkasan uji tersimpan di [laporan/](../laporan/README.md).

Pemeriksaan paket juga dapat dijalankan setelah mengunduh repositori GitHub.
Surat administrasi dan arsip pengerjaan hanya disimpan lokal; pemeriksaan
perbandingan dengan ZIP cadangan dilakukan jika cadangan tersebut tersedia.

Jika memakai lingkungan lokal yang sudah disiapkan, ganti `python` dengan
`.venv\Scripts\python.exe`. Setelah mengubah sumber `.py`, jalankan konversi;
jalankan kembali uji Housing untuk mengisi output notebook Housing terbaru.
Gunakan `uji_semua_notebook.py` untuk mengisi output seluruh materi dan kunci jawaban.

Definisi variabel disunting pada `alat_bantu/kamus_variabel.json`, kemudian
jalankan `sinkron_kamus_variabel.py`. Tabelnya ditampilkan sebelum dataset
dibaca, termasuk untuk petunjuk latihan yang belum dijalankan.
Satuan yang tidak tersedia pada sumber ditandai secara terbuka; jangan menebak
skala mata uang hanya dari besar angka.
