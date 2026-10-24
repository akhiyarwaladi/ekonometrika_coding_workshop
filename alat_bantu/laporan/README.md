# Laporan pemeriksaan

| Berkas | Isi |
|---|---|
| [penataan_folder.md](penataan_folder.md) | Ringkasan penataan, kesesuaian nama, dan hasil pengujian. |
| [ketajaman_slide.md](ketajaman_slide.md) | Penyebab buram, perbaikan teks vektor, dan perubahan pada contoh kode slide. |
| [uji_png_tajam.json](uji_png_tajam.json) | Pemeriksaan 31 PNG 6000 × 3375 piksel, 600 dpi, dan kecocokannya dengan versi tajam. |
| [uji_kernel_semua_notebook.md](uji_kernel_semua_notebook.md) | Pengujian terbaru seluruh notebook pada kernel Jupyter baru, beserta kesetaraan model dan inferensi. |
| [peta_perubahan_nama.csv](peta_perubahan_nama.csv) | Pencarian lokasi lama ke lokasi baru, beserta hash berkas sebelum penataan. |
| [kamus_variabel.json](kamus_variabel.json) | Cakupan definisi 266 kolom dan penempatan tabel pada 23 pasangan tutorial `.py`/`.ipynb`. |
| [uji_dashboard.json](uji_dashboard.json) | Hasil pengujian interaksi Streamlit, model, dan notebook penutup. |
| [uji_dashboard.md](uji_dashboard.md) | Ringkasan pengujian dashboard yang dapat dibaca pengajar. |
| [uji_regresi_housing.md](uji_regresi_housing.md) | Hasil eksekusi Housing pada kernel baru dan pemeriksaan prediksi. |
| [hasil_uji_regresi_housing.json](hasil_uji_regresi_housing.json) | Angka hasil uji Housing untuk diperiksa ulang. |

Uji umum membuat `uji_notebook_lokal`, `uji_notebook_folder_notebook`, dan
`uji_notebook_zip` dalam format `.json` (ringkasan) dan `.log` (rincian keluaran).
Peringatan statistik dicatat di log dan harus dibaca bersama catatan notebook.
