# Hasil pemeriksaan materi

Notebook `.ipynb` adalah sumber utama. Grafik pembelajaran tersimpan pada keluaran notebook.
Sesi 00 berfokus pada EDA; pembentukan model dimulai pada Sesi 01.
[Kembali ke materi](../../README.md)

## Eksekusi seluruh notebook

Hasil: **23/23 notebook lulus**. Waktu uji: 2026-10-25T23:48:13.
Setiap notebook dijalankan pada kernel baru, termasuk sel instalasi. Pemeriksaan model membandingkan prediksi scikit-learn dengan pelengkap inferensi yang sesuai.

| Notebook | Status | Sel kode | Gambar keluaran |
|---|---|---:|---:|
| [materi/01_ekonometrika/00_persiapan_colab.ipynb](../../materi/01_ekonometrika/00_persiapan_colab.ipynb) | PASS | 21 | 5 |
| [materi/01_ekonometrika/01_regresi_dasar.ipynb](../../materi/01_ekonometrika/01_regresi_dasar.ipynb) | PASS | 19 | 4 |
| [materi/01_ekonometrika/02_bentuk_fungsional.ipynb](../../materi/01_ekonometrika/02_bentuk_fungsional.ipynb) | PASS | 28 | 6 |
| [materi/01_ekonometrika/03_dummy_asumsi_klasik.ipynb](../../materi/01_ekonometrika/03_dummy_asumsi_klasik.ipynb) | PASS | 43 | 8 |
| [materi/01_ekonometrika/04_model_kategorikal.ipynb](../../materi/01_ekonometrika/04_model_kategorikal.ipynb) | PASS | 54 | 11 |
| [materi/01_ekonometrika/05_deret_waktu_kointegrasi.ipynb](../../materi/01_ekonometrika/05_deret_waktu_kointegrasi.ipynb) | PASS | 36 | 9 |
| [materi/01_ekonometrika/06_panel_garch.ipynb](../../materi/01_ekonometrika/06_panel_garch.ipynb) | PASS | 23 | 4 |
| [materi/02_latihan/00_persiapan_colab.ipynb](../../materi/02_latihan/00_persiapan_colab.ipynb) | PASS | 20 | 4 |
| [materi/02_latihan/01_regresi_dasar.ipynb](../../materi/02_latihan/01_regresi_dasar.ipynb) | PASS | 13 | 2 |
| [materi/02_latihan/02_bentuk_fungsional.ipynb](../../materi/02_latihan/02_bentuk_fungsional.ipynb) | PASS | 14 | 2 |
| [materi/02_latihan/03_dummy_asumsi_klasik.ipynb](../../materi/02_latihan/03_dummy_asumsi_klasik.ipynb) | PASS | 22 | 3 |
| [materi/02_latihan/04_model_kategorikal.ipynb](../../materi/02_latihan/04_model_kategorikal.ipynb) | PASS | 25 | 4 |
| [materi/02_latihan/05_deret_waktu_panel.ipynb](../../materi/02_latihan/05_deret_waktu_panel.ipynb) | PASS | 30 | 7 |
| [materi/02_latihan/06_data_indonesia.ipynb](../../materi/02_latihan/06_data_indonesia.ipynb) | PASS | 35 | 7 |
| [materi/03_regresi_rumah/01_regresi_rumah.ipynb](../../materi/03_regresi_rumah/01_regresi_rumah.ipynb) | PASS | 31 | 8 |
| [materi/04_dashboard_indonesia/01_dashboard_ekonomi.ipynb](../../materi/04_dashboard_indonesia/01_dashboard_ekonomi.ipynb) | PASS | 15 | 1 |
| [pengajar/kunci_jawaban/00_persiapan_colab.ipynb](../../pengajar/kunci_jawaban/00_persiapan_colab.ipynb) | PASS | 21 | 5 |
| [pengajar/kunci_jawaban/01_regresi_dasar.ipynb](../../pengajar/kunci_jawaban/01_regresi_dasar.ipynb) | PASS | 18 | 3 |
| [pengajar/kunci_jawaban/02_bentuk_fungsional.ipynb](../../pengajar/kunci_jawaban/02_bentuk_fungsional.ipynb) | PASS | 21 | 4 |
| [pengajar/kunci_jawaban/03_dummy_asumsi_klasik.ipynb](../../pengajar/kunci_jawaban/03_dummy_asumsi_klasik.ipynb) | PASS | 19 | 4 |
| [pengajar/kunci_jawaban/04_model_kategorikal.ipynb](../../pengajar/kunci_jawaban/04_model_kategorikal.ipynb) | PASS | 22 | 5 |
| [pengajar/kunci_jawaban/05_deret_waktu_panel.ipynb](../../pengajar/kunci_jawaban/05_deret_waktu_panel.ipynb) | PASS | 18 | 5 |
| [pengajar/kunci_jawaban/06_data_indonesia.ipynb](../../pengajar/kunci_jawaban/06_data_indonesia.ipynb) | PASS | 18 | 3 |

## Struktur dan integritas

Status **PASS**: 23 notebook, 45 CSV utama, 14 CSV latihan tambahan.
85 hash berkas terlindungi dan 522 tautan materi diperiksa, termasuk tujuan bagian dan tautan Colab.
31 PNG slide tetap berukuran 6000 × 3375 piksel, 600 dpi, dan sesuai dengan ZIP PNG.
187 bagian pada seluruh notebook diperiksa: judul sesi/latihan/kunci seragam, nomor bagian inti berurutan, dan setiap judul bagian mengawali sel.
Seluruh notebook mempunyai bagian Selanjutnya. Tidak ada impor identik yang berulang dalam ruang kerja yang sama.
Definisi 288 kolom tersedia pada 111 tabel Kenali data; [katalog data](../../data/README.md) memuat seluruh CSV.
113 tabel fungsi menjelaskan kegunaan, masukan/argumen, dan hasil perintah. 23 tabel alur menghubungkan bekal sebelumnya dengan materi berikutnya.

## Pembaca berbagai format data

Status **PASS**: tujuh format memakai 7 kasus Indonesia yang berbeda.
Sumber: World Bank, BPS Jawa Barat, dan BMKG. Bentuk tabel, satuan, label SPSS/Stata, kedua lembar Excel, dan hash salinan diperiksa.

| Format | Kasus | Baris | Kolom |
|---|---|---:|---:|
| CSV | Makroekonomi Indonesia | 26 | 7 |
| Excel | Produksi padi dan beras di Jawa Barat, 2025 | 27 | 4 |
| SPSS | Kemiskinan Indonesia menurut garis kemiskinan nasional | 26 | 2 |
| Stata | Penggunaan internet di Indonesia | 32 | 2 |
| Teks tab/TSV | Ekspor barang dan jasa Indonesia | 31 | 2 |
| JSON | Prakiraan cuaca Simpang IV Sipin, Kota Jambi | 17 | 7 |
| Parquet | Jumlah penduduk Indonesia | 66 | 2 |

## Visualisasi dan keterbacaan

Status **PASS**: 23 notebook diperiksa; total 114 gambar keluaran.
Setiap notebook mempunyai grafik, petunjuk cara membaca, dan kode yang dapat dijalankan berurutan. Pemeriksaan visual meliputi judul, label sumbu, keterbacaan, dan ukuran gambar.
Tinjauan tampilan: **PASS**.

## Regresi Housing

Pemeriksaan independen: **PASS**, dengan 404 baris latih dan 102 baris uji.

| Model | RMSE uji | R² uji |
|---|---:|---:|
| Rata-rata train | 8.6629 | -0.0233 |
| Sederhana: RM | 6.7930 | 0.3708 |
| Berganda: 13 fitur | 4.9286 | 0.6688 |
| Berganda: tanpa RAD | 5.1450 | 0.6390 |

RMSE memakai satuan MEDV, yaitu ribu dolar AS historis. Imputasi dipelajari dari data latih; prediksi manual dibandingkan dengan Pipeline serta solusi NumPy independen.

## Dashboard dan ngrok

Interaksi aplikasi: **PASS**, 7 kelompok pemeriksaan.
Model default: RMSE 4.446709 poin persentase; R² 0.199292.
Ngrok: PASS: HTTPS, healthcheck dan halaman Streamlit melalui internet.

## Batas pemeriksaan

Kernel dan akses HTTPS ngrok diuji secara lokal. Antarmuka Google Colab belum dikendalikan langsung.
Peringatan separation, konvergensi, atau model khusus dibaca bersama penjelasan notebook; p-value bukan pengganti pemeriksaan data dan asumsi.
Token pribadi dan tautan ngrok sementara tidak disimpan pada laporan. Cadangan sebelum perapian disimpan lokal di alat_bantu/arsip/.
