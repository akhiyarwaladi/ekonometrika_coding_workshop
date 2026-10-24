# Pengujian notebook dan dashboard ekonomi provinsi

Hasil AppTest: **PASS**, 7 kelompok pengujian pada data 34 provinsi tahun 2021.

Notebook: [01_dashboard_ekonomi.ipynb](../materi/04_dashboard_indonesia/01_dashboard_ekonomi.ipynb).

## Perilaku yang diperiksa

- Ringkasan 34 provinsi, RMSE, dan R² sesuai perhitungan independen.
- Pilihan indikator peringkat dan sumbu grafik dapat diubah.
- Slider mengubah prediksi; hasil sesuai model OLS independen.
- Satu atau dua X bekerja; pilihan X kosong ditangani tanpa error.
- Filter Jambi, jumlah provinsi sedikit, dan pilihan kosong ditangani dengan benar.
- Model dan tabel mengikuti filter 10 provinsi yang dipilih.
- X konstan ditangani tanpa membentuk model yang menyesatkan.

Model default pada data uji: RMSE **4.446709 poin persentase**, R² **0.199292**.

Seluruh **10 sel kode** dijalankan pada kernel baru, termasuk instalasi, pembuatan berkas aplikasi, server, dan pratinjau lokal. Server uji dihentikan setelah pemeriksaan.

Kode aplikasi disimpan dalam empat sel notebook; tidak memerlukan langkah terminal dari peserta.
Pratinjau browser lokal disimpan pada [gambar simulasi](../gambar/dashboard/pratinjau_simulasi.png).

Interaksi Streamlit diuji dengan AppTest lokal; antarmuka Google Colab tidak dikendalikan dalam pengujian ini.
