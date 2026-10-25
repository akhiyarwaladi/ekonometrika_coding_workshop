# Hasil pemeriksaan materi

Notebook `.ipynb` adalah sumber utama. Grafik pembelajaran tersimpan pada keluaran notebook.
[Kembali ke materi](../../README.md)

## Eksekusi seluruh notebook

Hasil: **23/23 notebook lulus**. Waktu uji: 2026-10-25T17:02:06.
Setiap notebook dijalankan pada kernel baru, termasuk sel instalasi. Pemeriksaan model membandingkan prediksi scikit-learn dengan pelengkap inferensi yang sesuai.

| Notebook | Status | Sel kode | Gambar keluaran |
|---|---|---:|---:|
| [materi/01_ekonometrika/00_persiapan_colab.ipynb](../../materi/01_ekonometrika/00_persiapan_colab.ipynb) | PASS | 21 | 3 |
| [materi/01_ekonometrika/01_regresi_dasar.ipynb](../../materi/01_ekonometrika/01_regresi_dasar.ipynb) | PASS | 19 | 4 |
| [materi/01_ekonometrika/02_bentuk_fungsional.ipynb](../../materi/01_ekonometrika/02_bentuk_fungsional.ipynb) | PASS | 26 | 4 |
| [materi/01_ekonometrika/03_dummy_asumsi_klasik.ipynb](../../materi/01_ekonometrika/03_dummy_asumsi_klasik.ipynb) | PASS | 36 | 5 |
| [materi/01_ekonometrika/04_model_kategorikal.ipynb](../../materi/01_ekonometrika/04_model_kategorikal.ipynb) | PASS | 42 | 6 |
| [materi/01_ekonometrika/05_deret_waktu_kointegrasi.ipynb](../../materi/01_ekonometrika/05_deret_waktu_kointegrasi.ipynb) | PASS | 30 | 6 |
| [materi/01_ekonometrika/06_panel_garch.ipynb](../../materi/01_ekonometrika/06_panel_garch.ipynb) | PASS | 22 | 3 |
| [materi/02_latihan/00_persiapan_colab.ipynb](../../materi/02_latihan/00_persiapan_colab.ipynb) | PASS | 17 | 3 |
| [materi/02_latihan/01_regresi_dasar.ipynb](../../materi/02_latihan/01_regresi_dasar.ipynb) | PASS | 13 | 2 |
| [materi/02_latihan/02_bentuk_fungsional.ipynb](../../materi/02_latihan/02_bentuk_fungsional.ipynb) | PASS | 14 | 2 |
| [materi/02_latihan/03_dummy_asumsi_klasik.ipynb](../../materi/02_latihan/03_dummy_asumsi_klasik.ipynb) | PASS | 17 | 2 |
| [materi/02_latihan/04_model_kategorikal.ipynb](../../materi/02_latihan/04_model_kategorikal.ipynb) | PASS | 17 | 2 |
| [materi/02_latihan/05_deret_waktu_panel.ipynb](../../materi/02_latihan/05_deret_waktu_panel.ipynb) | PASS | 24 | 5 |
| [materi/02_latihan/06_data_indonesia.ipynb](../../materi/02_latihan/06_data_indonesia.ipynb) | PASS | 34 | 6 |
| [materi/03_regresi_housing/01_regresi_housing.ipynb](../../materi/03_regresi_housing/01_regresi_housing.ipynb) | PASS | 31 | 8 |
| [materi/04_dashboard_indonesia/01_dashboard_ekonomi.ipynb](../../materi/04_dashboard_indonesia/01_dashboard_ekonomi.ipynb) | PASS | 13 | 1 |
| [pengajar/kunci_jawaban/00_persiapan_colab.ipynb](../../pengajar/kunci_jawaban/00_persiapan_colab.ipynb) | PASS | 14 | 2 |
| [pengajar/kunci_jawaban/01_regresi_dasar.ipynb](../../pengajar/kunci_jawaban/01_regresi_dasar.ipynb) | PASS | 17 | 3 |
| [pengajar/kunci_jawaban/02_bentuk_fungsional.ipynb](../../pengajar/kunci_jawaban/02_bentuk_fungsional.ipynb) | PASS | 21 | 4 |
| [pengajar/kunci_jawaban/03_dummy_asumsi_klasik.ipynb](../../pengajar/kunci_jawaban/03_dummy_asumsi_klasik.ipynb) | PASS | 14 | 3 |
| [pengajar/kunci_jawaban/04_model_kategorikal.ipynb](../../pengajar/kunci_jawaban/04_model_kategorikal.ipynb) | PASS | 14 | 3 |
| [pengajar/kunci_jawaban/05_deret_waktu_panel.ipynb](../../pengajar/kunci_jawaban/05_deret_waktu_panel.ipynb) | PASS | 12 | 3 |
| [pengajar/kunci_jawaban/06_data_indonesia.ipynb](../../pengajar/kunci_jawaban/06_data_indonesia.ipynb) | PASS | 18 | 3 |

## Struktur dan integritas

Status **PASS**: 23 notebook, 44 CSV aktif, 15 CSV cadangan.
85 hash berkas terlindungi dan 244 tautan lokal diperiksa.
31 PNG slide tetap berukuran 6000 × 3375 piksel, 600 dpi, dan sesuai dengan ZIP PNG.
Definisi 266 kolom tersedia pada 86 tabel Kenali data; [katalog data](../../data/README.md) memuat seluruh CSV.

## Pembaca berbagai format data

Status **PASS**: CSV, Excel, SPSS, Stata, TSV, JSON, dan Parquet menghasilkan 26 baris dan 7 kolom dengan nilai yang sama.
Semua salinan berasal dari tabel makro Indonesia yang sama; berkas CSV asli dipertahankan. Label variabel SPSS/Stata dan kedua lembar Excel juga diperiksa.

## Visualisasi dan keterbacaan

Status **PASS**: 23 notebook diperiksa; total 83 gambar keluaran.
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
