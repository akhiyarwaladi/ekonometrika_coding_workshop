# Perkakas pengelola materi

Peserta mulai dari [README utama](../README.md). Notebook `.ipynb` merupakan sumber tunggal;
penjelasan, kode, dan grafik disunting di notebook yang sama.

## Pemeriksaan

Jalankan dari folder utama dengan lingkungan Python yang memiliki paket dari
`requirements.txt` dan `alat_bantu/requirements_pengelola.txt`.

| Perintah | Kegunaan |
|---|---|
| `python alat_bantu/sinkron_kamus_variabel.py` | Menyisipkan definisi variabel, tabel fungsi, kaitan materi, dan katalog data; kode serta output dipertahankan. |
| `python alat_bantu/sinkron_kamus_variabel.py --periksa` | Memeriksa definisi tanpa mengubah notebook. |
| `python alat_bantu/uji_semua_notebook.py` | Menjalankan seluruh notebook pada kernel baru dan menyimpan hasil serta grafik. |
| `python alat_bantu/uji_notebook.py --dari-zip` | Uji cepat dengan salinan data lokal; tidak mengubah keluaran notebook. |
| `python alat_bantu/uji_format_data.py` | Memeriksa tujuh format dengan kasus berbeda: skema, ukuran, nilai, label, dan hash berkas. |
| `python alat_bantu/uji_regresi_rumah.py` | Memeriksa prediksi, pembagian data, imputasi, metrik, dan Pipeline secara independen. |
| `python alat_bantu/uji_dashboard.py --ngrok` | Memeriksa interaksi aplikasi dan akses HTTPS memakai token yang sudah diisi pada notebook. |
| `python alat_bantu/periksa_paket.py` | Memeriksa integritas data, PNG slide, format notebook, dan tautan. |
| `python alat_bantu/audit_visual.py` | Memeriksa keluaran gambar dan membuat lembar tinjauan lokal. |

Semua perkakas memperbarui satu [hasil pemeriksaan](laporan/hasil_pemeriksaan.md).
Hasil terstruktur disimpan sebagai JSON untuk pemeriksaan ulang; log hanya disimpan lokal.
Fungsi khusus Tobit dan separation tetap tersedia pada `metode_lanjutan.py`.

Untuk menguji berkas baru sebelum tersedia di GitHub, gunakan
`python alat_bantu/uji_semua_notebook.py --data-lokal`. Pemeriksaan berjalan
di folder sementara dan tetap menyimpan alamat GitHub pada kode notebook.

Sesudah benar-benar memeriksa tampilan lembar grafik, jalankan
`python alat_bantu/audit_visual.py --selesai-ditinjau` untuk mencatat hasil tinjauan.

## Paket opsional

`paket/data_tutorial.zip` berisi 45 CSV aktif, enam contoh format dengan kasus berbeda untuk Sesi 00, dan modul model khusus.
`paket/png_regresi_tajam.zip` berisi 31 PNG slide tajam.
Keduanya salinan untuk pengajar; peserta membuka notebook dan membaca CSV dari GitHub.
Buat ulang dengan `kemas_data.py` atau `kemas_png.py` jika sumber paket berubah.

## Pemeliharaan bahan

`buat_data_simulasi.py` dan `unduh_data_indonesia.py` mengubah CSV; gunakan hanya saat memperbarui sumber data.
`buat_slide.py` membuat presentasi pembuka. `ekspor_slide_tajam.py` membuat ulang ekspor PNG.
Grafik analisis peserta dibuat di notebook, sehingga tidak ada generator grafik kedua yang perlu diselaraskan.

## Cadangan

`arsip/` memuat cadangan sebelum perubahan, sumber lama, dan berkas pengerjaan.
Isinya disimpan lokal dan tidak dibagikan sebagai materi kelas.
`administrasi/` berisi surat undangan lokal.
Token ngrok sudah diisi langsung pada notebook dashboard sesuai pengaturan pengajar.
Salinan token di `pengajar/token_ngrok.txt` tetap disimpan lokal.
