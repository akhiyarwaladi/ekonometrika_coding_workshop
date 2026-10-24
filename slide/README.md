# Slide tutorial

Untuk menampilkan materi regresi, gunakan [folder PNG tajam](png_regresi_tajam).
Ada **31 gambar terpisah**, bernama `halaman_01.png` sampai `halaman_31.png`.
Setiap gambar berukuran **6000 × 3375 piksel dengan metadata 600 dpi**.
Logo, header, dan footer berwarna telah ditutup putih.

Untuk mengambil semua gambar sekaligus, unduh [ZIP 31 PNG tajam](../alat_bantu/paket/png_regresi_tajam.zip).
Ekstrak ZIP tersebut, lalu masukkan gambar ke presentasi sesuai nomor halaman.

| Berkas | Kegunaan |
|---|---|
| [png_regresi_tajam/](png_regresi_tajam) | PNG yang dipakai untuk mengajar. |
| [01_pengantar_workshop.pptx](01_pengantar_workshop.pptx) | 18 slide pembuka dan catatan pengajar. |
| [03_regresi_machine_learning_tajam.pdf](03_regresi_machine_learning_tajam.pdf) | Versi untuk mengajar: kode, tabel kecil, dan beberapa rumus memakai vektor. |
| [02_regresi_machine_learning.pdf](02_regresi_machine_learning.pdf) | PDF sumber, disimpan sebagai acuan pembuatan ulang. |

Ekspor lama 300 dpi disimpan lokal di `alat_bantu/arsip/slide/png_regresi_300_dpi/`.
Folder PNG aktif di sini hanya memuat versi tajam. Versi tajam juga mengoreksi
target pelatihan pada contoh kode dan menyamakan R²/RMSE dengan notebook Housing.
Praktik yang mengikuti materi ini ada di
[notebook Housing](../materi/03_regresi_housing/01_regresi_housing.ipynb).


## Pilih halaman praktik

| Contoh yang dicari | Gambar |
|---|---|
| Membagi data latih dan uji | [halaman_20.png](png_regresi_tajam/halaman_20.png) |
| Melatih regresi linear | [halaman_21.png](png_regresi_tajam/halaman_21.png) |
| Memeriksa VIF | [halaman_24.png](png_regresi_tajam/halaman_24.png) |
| Melihat korelasi | [halaman_25.png](png_regresi_tajam/halaman_25.png) |
| Menghitung R² | [halaman_27.png](png_regresi_tajam/halaman_27.png) |
| Menghitung RMSE | [halaman_28.png](png_regresi_tajam/halaman_28.png) |

## Ketajaman dan perbaikan

Ekspor sebelumnya mempunyai ukuran 3000 × 1688 piksel. Teks asli PDF cukup jelas,
tetapi beberapa contoh kode merupakan screenshot JPEG sekitar 133–144 dpi.
Tabel kecil tertentu hanya sekitar 116–119 dpi, dan gambar persamaan garis
sekitar 74 dpi pada ukuran penempatannya. Ekspor dengan dpi lebih tinggi
tidak mengembalikan bentuk huruf yang sudah hilang pada screenshot.

[Manifest ekspor](../alat_bantu/laporan/ekspor_slide_tajam.json) mencatat ukuran, halaman, hash sumber, dan metrik yang digunakan.

### Bagian yang dibangun ulang

| Halaman | Perbaikan |
|---|---|
| 13 | Rumus jumlah kuadrat residual menjadi vektor; dua lapis gambar rumus lama dihilangkan. |
| 14 | Persamaan garis menjadi vektor dan posisinya disesuaikan agar tidak bertabrakan dengan label. |
| 19 | Tabel Temperature dan Curah_Hujan diketik ulang sesuai angka pada slide sumber. |
| 20 | Kode pembagian train/test menjadi teks monospace vektor. |
| 21 | Kode pelatihan dan tabel koefisien menjadi vektor. Salah ketik target diperbaiki menjadi `linreg.fit(feature_train, target_train)`. |
| 23 | Rumus VIF menjadi vektor; simbol panah yang gagal tampil diganti garis vektor. |
| 24 | Kode VIF dan 13 baris tabel diketik ulang. Angka tabel mengikuti slide sumber; penanda RAD/TAX digambar ulang. |
| 25 | Kode heatmap menjadi teks monospace vektor. |
| 27 | Argumen R² diperbaiki menjadi aktual lalu prediksi; contoh memakai data test Housing dan model tanpa RAD. Penjelasan mencakup kemungkinan R² negatif. |
| 28 | Rumus RMSE dan kode menjadi vektor; contoh memakai data test Housing. Penjelasan satuan diperbaiki dan tidak menyamakan RMSE dengan interval prediksi. |

Perubahan halaman 27–28 menjaga contoh evaluasi sesuai notebook yang sudah diuji:
506 observasi, pembagian train/test 80:20, `random_state=42`, serta model 12 fitur
tanpa RAD. R² test **0,6390347738951445** dan RMSE test **5,144992285668699**.
Kode dan angka ini diperiksa kembali saat pembuatan slide. Nilai tabel VIF dan
tabel Temperature tetap merupakan contoh historis dari slide sumber, bukan hasil
baru dari data Housing. Materi lengkap yang bisa dijalankan ada di
[notebook Housing](../materi/03_regresi_housing/01_regresi_housing.ipynb).

### Pemeriksaan

Seluruh 31 PNG diperiksa ukuran, format RGB, keterbacaan berkas, serta metadata dpi.
Halaman yang diubah dirender dan diperiksa secara visual untuk mendeteksi
teks terpotong, tumpukan rumus, dan tabel yang bertabrakan dengan kode.
PDF sumber dan seluruh 31 PNG lama diperiksa dengan SHA-256 dan tetap sama.
PNG lama dipindahkan ke arsip lokal `alat_bantu/arsip/slide/png_regresi_300_dpi/`, sehingga
folder slide aktif hanya memuat PNG versi tajam.
Enam blok kode yang ditampilkan diuji eksekusinya. Contoh Temperature diuji
dengan lima baris contoh yang terlihat pada slide; tabel koefisien historisnya
tetap mengikuti sumber. Kode VIF diuji pada 13 fitur Housing. Angka R² dan RMSE
yang ditampilkan berasal dari model Housing tanpa RAD yang dihitung ulang.

Beberapa grafik dan ilustrasi yang hanya tersedia sebagai gambar pada PDF tetap
mengikuti aset sumber. Ketajaman detail kecil di grafik tersebut masih dibatasi
resolusi gambar asal. Perbaikan utama pada versi ini adalah kode, tabel kecil,
rumus yang diganti, dan seluruh teks asli PDF yang dirender ulang pada 600 dpi.

Untuk membuat ulang, jalankan `python alat_bantu/ekspor_slide_tajam.py` dari folder utama.
ZIP PNG diperbarui otomatis setelah ekspor selesai. Untuk mengemas kembali gambar
yang sudah ada, jalankan `python alat_bantu/kemas_png.py`.
