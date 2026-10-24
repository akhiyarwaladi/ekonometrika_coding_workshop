# Hasil pemeriksaan notebook Regression (I)

Notebook: [01_regresi_housing.ipynb](../../materi/03_regresi_housing/01_regresi_housing.ipynb).
Data: [housing.csv](../../data/housing.csv), dibaca lokal tanpa Google Drive atau unduhan tambahan.
Folder kerja awal: folder notebook sendiri; sel persiapan menemukan folder data proyek.
Status: **29/29 sel kode berjalan pada kernel baru tanpa error.**
Notebook berisi 55 sel dan 6 grafik; seluruh output tersimpan.

## Data dan pembagian

- 506 baris, 14 kolom; 0 nilai kosong, 0 duplikat.
- 404 baris train dan 102 baris test, random_state=42.
- CSV tidak diubah; SHA-256: `8dbb8918b7e56ba8fd4db12d6aec7c8cf119954e4ea783cb4d7e39bfdf3c2195`.

## Evaluasi test

| Model | RMSE test | R² test |
|---|---:|---:|
| Rata-rata train | 8.6629 | -0.0233 |
| Sederhana: RM | 6.7930 | 0.3708 |
| Berganda: 13 fitur | 4.9286 | 0.6688 |
| Berganda: tanpa RAD | 5.1450 | 0.6390 |

RMSE memakai satuan MEDV (ribuan dolar AS historis). Mengurangi VIF dengan
mengeluarkan RAD tidak otomatis memperbaiki prediksi pada test ini.

## Pemeriksaan yang lulus

- Indeks fitur dan target konsisten; penggabungan untuk korelasi tidak menambah baris/kekosongan.
- Train dan test terpisah; target tidak masuk ke fitur.
- Median imputasi berasal dari train; prediksi baru tetap berhingga ketika CRIM kosong.
- Prediksi pipeline sama dengan proses manual.
- Prediksi regresi berganda sesuai penyelesaian least squares NumPy independen.
- RMSE dan R² sesuai perhitungan rumus manual.
- Contoh polinomial memakai validasi dari train, tidak memakai test untuk memilih derajat.
- Kode peserta tidak memakai fungsi buatan sendiri, perulangan, comprehension, atau operasi matriks manual.
- Format notebook valid dan seluruh sel berisi output eksekusi terbaru.

## Lingkungan uji

Python 3.13.5, pandas 2.2.3, NumPy 2.1.3,
scikit-learn 1.6.1, statsmodels 0.15.0.

Ini pemeriksaan eksekusi lokal, bukan pengujian antarmuka Google Colab.
