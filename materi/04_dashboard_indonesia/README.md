# Penutup: membuat dashboard ekonomi Indonesia

Buka [01_dashboard_ekonomi.ipynb](01_dashboard_ekonomi.ipynb), atau
[langsung buka di Colab](https://colab.research.google.com/github/akhiyarwaladi/ekonometrika_coding_workshop/blob/main/materi/04_dashboard_indonesia/01_dashboard_ekonomi.ipynb).
Seluruh kode aplikasi dan langkah menjalankannya ada di notebook.
Peserta cukup menjalankan sel; tidak perlu membuka terminal.

1. Di Colab, simpan salinan notebook. Gunakan koneksi internet; data dibaca langsung dari GitHub.
2. Jalankan sel dari atas, termasuk instalasi dan persiapan data.
3. Empat sel `%%writefile` menyimpan bagian aplikasi; masing-masing dapat dijalankan ulang.
4. Jalankan sel server dan sel pratinjau. Di Colab, dashboard tampil dalam keluaran notebook.
5. Untuk tautan yang dapat dibuka dari perangkat lain, ikuti **langkah 9: ngrok** di bawah sel pratinjau.
6. Coba filter, grafik, regresi, dan slider. Akhiri dengan tantangan presentasi dua menit.

## Akses melalui ngrok

Pada notebook peserta, ubah `gunakan_ngrok = False` menjadi `True`, lalu jalankan
sel langkah 9 dan masukkan authtoken ngrok pada input tersembunyi. Klik tautan
**Buka dashboard melalui ngrok** yang muncul. Jika ngrok menampilkan halaman
pemberitahuan, klik **Visit Site**. Biarkan runtime dan server tetap berjalan.
Tautan membuka dashboard yang sama dengan pratinjau notebook.

Salinan pribadi pengajar disimpan lokal di
`pengajar/pribadi/01_dashboard_ekonomi_ngrok.ipynb`. Token dari notebook referensi
sudah terisi dan ngrok langsung diaktifkan. Berkas ini dikecualikan dari GitHub
karena memuat token akun; yang dibagikan kepada peserta adalah tautan dashboard.
Untuk menggunakan salinan pribadi di Colab, unggah notebook tersebut lalu jalankan dari atas.
Data tetap dibaca dari GitHub, sehingga tidak ada CSV yang perlu diunggah.

Langkah 10 menghentikan server dan koneksi ngrok milik notebook ini.
Menjalankan ulang langkah 9 mengganti koneksi sebelumnya.
[Rujukan ngrok untuk Colab](https://ngrok.com/docs/using-ngrok-with/googleColab).

Dashboard hanya memakai **[provinsi_2021.csv](../../data/provinsi_2021.csv)**: data 34 provinsi pada **2021**. Pengguna dapat memilih provinsi,
membandingkan IPM, pengangguran, dan kemiskinan, melatih regresi scikit-learn,
membaca RMSE/R², mencoba skenario, serta mengunduh data hasil filter.
Tabel arti variabel disediakan sebelum data dibaca.

![Contoh tampilan model dan slider simulasi](../../gambar/dashboard/pratinjau_simulasi.png)

Berkas aplikasi dibuat otomatis di folder sementara komputer/runtime; CSV dibaca dari GitHub. Berkas `.py`
di sebelah notebook adalah sumber penyuntingan bagi pengajar, mengikuti format
materi sebelumnya. Peserta menjalankan versi `.ipynb`.

**Durasi yang disarankan:** 60 menit. Setelah selesai, ubah `hentikan_dashboard`
menjadi `True` pada sel terakhir dan jalankan sel itu. Menutup runtime Colab
juga menghentikan aplikasi.

Notebook telah diuji pada kernel Jupyter lokal. Interaksi aplikasi diperiksa
otomatis dan tampilannya dibuka di browser. Pratinjau Colab memakai fasilitas
bawaan Colab; pengujian langsung pada sesi Colab belum dilakukan.
