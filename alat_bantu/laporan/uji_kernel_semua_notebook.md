# Pengujian seluruh notebook pada kernel baru

Hasil: **23/23 notebook lulus** pada Python 3.13.5.
Setiap notebook dijalankan dari foldernya sendiri, termasuk sel instalasi paket.
Sel pemeriksaan tambahan tidak disimpan ke materi peserta. Output pembelajaran disimpan.

| Notebook | Status | Sel kode | Grafik | Model scikit-learn | Perbandingan inferensi |
|---|---|---:|---:|---:|---:|
| [materi/01_ekonometrika/00_persiapan_colab.ipynb](../../materi/01_ekonometrika/00_persiapan_colab.ipynb) | PASS | 9 | 1 | 1 | 1 |
| [materi/01_ekonometrika/01_regresi_dasar.ipynb](../../materi/01_ekonometrika/01_regresi_dasar.ipynb) | PASS | 13 | 3 | 3 | 3 |
| [materi/01_ekonometrika/02_bentuk_fungsional.ipynb](../../materi/01_ekonometrika/02_bentuk_fungsional.ipynb) | PASS | 13 | 2 | 5 | 5 |
| [materi/01_ekonometrika/03_dummy_asumsi_klasik.ipynb](../../materi/01_ekonometrika/03_dummy_asumsi_klasik.ipynb) | PASS | 19 | 2 | 7 | 6 |
| [materi/01_ekonometrika/04_model_kategorikal.ipynb](../../materi/01_ekonometrika/04_model_kategorikal.ipynb) | PASS | 27 | 0 | 6 | 2 |
| [materi/01_ekonometrika/05_deret_waktu_kointegrasi.ipynb](../../materi/01_ekonometrika/05_deret_waktu_kointegrasi.ipynb) | PASS | 18 | 3 | 3 | 3 |
| [materi/01_ekonometrika/06_panel_garch.ipynb](../../materi/01_ekonometrika/06_panel_garch.ipynb) | PASS | 19 | 2 | 0 | 0 |
| [materi/02_latihan/00_persiapan_colab.ipynb](../../materi/02_latihan/00_persiapan_colab.ipynb) | PASS | 8 | 1 | 1 | 1 |
| [materi/02_latihan/01_regresi_dasar.ipynb](../../materi/02_latihan/01_regresi_dasar.ipynb) | PASS | 10 | 0 | 1 | 1 |
| [materi/02_latihan/02_bentuk_fungsional.ipynb](../../materi/02_latihan/02_bentuk_fungsional.ipynb) | PASS | 9 | 0 | 1 | 1 |
| [materi/02_latihan/03_dummy_asumsi_klasik.ipynb](../../materi/02_latihan/03_dummy_asumsi_klasik.ipynb) | PASS | 11 | 0 | 3 | 3 |
| [materi/02_latihan/04_model_kategorikal.ipynb](../../materi/02_latihan/04_model_kategorikal.ipynb) | PASS | 14 | 0 | 2 | 1 |
| [materi/02_latihan/05_deret_waktu_panel.ipynb](../../materi/02_latihan/05_deret_waktu_panel.ipynb) | PASS | 17 | 2 | 2 | 1 |
| [materi/02_latihan/06_data_indonesia.ipynb](../../materi/02_latihan/06_data_indonesia.ipynb) | PASS | 25 | 3 | 1 | 1 |
| [materi/03_regresi_housing/01_regresi_housing.ipynb](../../materi/03_regresi_housing/01_regresi_housing.ipynb) | PASS | 29 | 6 | 3 | 0 |
| [materi/04_dashboard_indonesia/01_dashboard_ekonomi.ipynb](../../materi/04_dashboard_indonesia/01_dashboard_ekonomi.ipynb) | PASS | 11 | 0 | 0 | 0 |
| [pengajar/kunci_jawaban/00_persiapan_colab.ipynb](../../pengajar/kunci_jawaban/00_persiapan_colab.ipynb) | PASS | 5 | 0 | 1 | 1 |
| [pengajar/kunci_jawaban/01_regresi_dasar.ipynb](../../pengajar/kunci_jawaban/01_regresi_dasar.ipynb) | PASS | 6 | 0 | 3 | 2 |
| [pengajar/kunci_jawaban/02_bentuk_fungsional.ipynb](../../pengajar/kunci_jawaban/02_bentuk_fungsional.ipynb) | PASS | 7 | 0 | 6 | 2 |
| [pengajar/kunci_jawaban/03_dummy_asumsi_klasik.ipynb](../../pengajar/kunci_jawaban/03_dummy_asumsi_klasik.ipynb) | PASS | 5 | 1 | 3 | 1 |
| [pengajar/kunci_jawaban/04_model_kategorikal.ipynb](../../pengajar/kunci_jawaban/04_model_kategorikal.ipynb) | PASS | 5 | 0 | 2 | 1 |
| [pengajar/kunci_jawaban/05_deret_waktu_panel.ipynb](../../pengajar/kunci_jawaban/05_deret_waktu_panel.ipynb) | PASS | 6 | 0 | 0 | 0 |
| [pengajar/kunci_jawaban/06_data_indonesia.ipynb](../../pengajar/kunci_jawaban/06_data_indonesia.ipynb) | PASS | 7 | 0 | 3 | 3 |

Perbandingan inferensi memastikan prediksi dari estimator tanpa penalti sesuai dengan
pelengkap statistik pada X dan y yang sama dalam toleransi numerik. Koefisien dan
intersep harus berhingga; peluang multinomial harus berjumlah satu dan mengikuti urutan classes_.

Peringatan pada demonstrasi separation atau model khusus dibaca bersama catatan notebook.
Pengujian kernel lokal ini tidak memeriksa antarmuka Google Colab secara langsung.
