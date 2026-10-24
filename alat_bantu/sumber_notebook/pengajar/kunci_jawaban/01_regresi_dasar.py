# %% [markdown]
# # Kunci Lab 1: Regresi Linear
#
# File ini berisi solusi latihan Lab 1. Semua angka di sini dihasilkan dari
# data di folder `data/`, jadi hasil Anda harus sama (atau sangat dekat).

# %% [markdown]
# ## Persiapan: alamat data
#
# Jalankan sel alamat data di bawah. `URL_DATA` menyimpan alamat folder CSV di GitHub;
# `pd.read_csv(...)` membaca tabel sesuai nama CSV pada sel kode berikutnya.
# Gunakan koneksi internet dan jalankan sel berurutan dengan **Shift + Enter**.

# %% [markdown]
# ## Cara mengikuti notebook ini
#
# Jalankan sel berurutan dengan `Shift + Enter`. Setiap notebook dapat
# dimulai sendiri dengan koneksi internet yang aktif. Sel persiapan cukup dijalankan
# apa adanya; fokus latihan dimulai saat tabel data muncul.
#
# Baca penjelasan sebelum menjalankan kode, lalu sebutkan arti hasilnya.
# Ubah satu hal setiap mencoba: nama kolom pada X, pilihan model, atau nilai prediksi.
# Baris `#` adalah catatan. `=` menyimpan hasil dan `==` membandingkan nilai.
# Contoh `tabel["kolom"]` berarti memilih satu kolom dari tabel.
#
# Jika muncul error merah, berhenti di sel itu dan baca baris terakhirnya.
# Jika ada warning, baca pesannya dan periksa hasil estimasi sebelum lanjut.
# Panduan simbol dan contoh tambahan ada di `panduan/cara_menggunakan_notebook.md`.

# %% [markdown]
# ### Pola pemodelan yang dipakai
#
# `X` adalah tabel fitur dan `y` adalah kolom target. Model utama memakai
# scikit-learn: buat model, jalankan `fit(X, y)`, lalu gunakan `predict(X_baru)`.
# Koefisien ada pada `coef_` dan intersep pada `intercept_`. Tabel `koefisien_...`
# hanya memberi nama kolom agar angka mudah dibaca. `score(X, y)` pada regresi
# linear adalah R² pada data yang diberikan; hasil pada data latih belum mengukur
# kemampuan memprediksi data baru.
#
# Nama `uji_...` menandai pelengkap statistik untuk p-value, standard error, atau
# uji asumsi. Perhitungannya memakai X dan y yang sama. Bagian model khusus diberi
# catatan tersendiri ketika scikit-learn belum menyediakan estimatornya.

# %%
URL_DATA = "https://raw.githubusercontent.com/akhiyarwaladi/ekonometrika_coding_workshop/main/data/"

print("Alamat data siap. Jalankan sel pembacaan CSV berikutnya.")

# %%
import pandas as pd
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
import numpy as np

# %% [markdown]
# ## Latihan 1: produktivitas padi

# %% [markdown]
# <!-- kamus_variabel:uts_3.csv -->
#
# ### Kenali data: Produktivitas padi
#
# **Data:** `data/uts_3.csv`. **Satu baris:** satu wilayah pertanian pada contoh latihan.
#
# | Variabel/kolom | Pengertian | Satuan atau kode | Peran |
# |---|---|---|---|
# | `Y_Produktivitas_Padi` | Hasil panen padi per luas lahan. | Produktivitas per hektar; skala massa tidak dirinci sumber | Y: target |
# | `X1_Jumlah_Pupuk` | Banyaknya pupuk yang digunakan pada pertanian. | Jumlah pupuk; satuan/cakupan luas tidak dirinci | X: penjelas |
# | `X2_Curah_Hujan` | Banyaknya hujan pada wilayah pertanian. | Satuan/periode tidak dirinci sumber | X: penjelas |
# | `X3_Sinar_Matahari` | Lama penyinaran matahari yang diterima lahan. | Jam; periode akumulasi tidak dirinci | X: penjelas |
#
# Sumber menyebut produktivitas per hektar, tetapi tidak merinci semua skala. Interpretasi dalam ton, kg, atau mm memerlukan konfirmasi metadata, bukan hanya dugaan dari angka.
#
# Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

# %%
padi = pd.read_csv(URL_DATA + "uts_3.csv")
sampel_model_padi = padi[
    ["Y_Produktivitas_Padi", "X1_Jumlah_Pupuk", "X2_Curah_Hujan", "X3_Sinar_Matahari"]
].dropna()
X_model_padi = sampel_model_padi[
    ["X1_Jumlah_Pupuk", "X2_Curah_Hujan", "X3_Sinar_Matahari"]
]
y_model_padi = sampel_model_padi["Y_Produktivitas_Padi"]

model_padi = LinearRegression()
model_padi.fit(X_model_padi, y_model_padi)

# Pelengkap statistik: standard error dan pengujian pada sampel yang sama.
uji_model_padi = sm.OLS(
    y_model_padi,
    sm.add_constant(X_model_padi, has_constant="add").rename(
        columns={"const": "Intercept"}
    ),
).fit()
print(uji_model_padi.summary())

# %% [markdown]
# Kesimpulan:
#
# - Yang signifikan hanya curah hujan (p = 0,0000, koefisien 0,0029).
#   Kenaikan curah hujan 100 mm menaikkan produktivitas sekitar 0,29 ton.
# - Pupuk (p = 0,69) dan sinar matahari (p = 0,48) tidak signifikan.
# - R kuadrat 0,988, tapi lihat catatan: data simulasi.

# %%
print(uji_model_padi.pvalues.round(4))

# %% [markdown]
# ## Latihan 2: angka harapan hidup

# %% [markdown]
# <!-- kamus_variabel:uts_4.csv -->
#
# ### Kenali data: Angka harapan hidup
#
# **Data:** `data/uts_4.csv`. **Satu baris:** satu negara pada contoh latihan.
#
# | Variabel/kolom | Pengertian | Satuan atau kode | Peran |
# |---|---|---|---|
# | `Y_Angka_Harapan_Hidup` | Rata-rata lama hidup yang diharapkan menurut indikator pada contoh. | Tahun | Y: target |
# | `X1_Pengeluaran_Kesehatan` | Pengeluaran kesehatan per penduduk (per kapita). | Uang per kapita; mata uang/periode tidak dirinci | X: penjelas |
# | `X2_Tingkat_Imunisasi` | Persentase anak yang memperoleh imunisasi. | Persen; jenis imunisasi tidak dirinci | X: penjelas |
# | `X3_Konsumsi_Kalori` | Rata-rata konsumsi energi makanan per hari. | Kalori harian; rincian satuan energi mengikuti sumber | X: penjelas |
#
# Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

# %%
harapan = pd.read_csv(URL_DATA + "uts_4.csv")
sampel_model_harapan = harapan[
    [
        "Y_Angka_Harapan_Hidup",
        "X1_Pengeluaran_Kesehatan",
        "X2_Tingkat_Imunisasi",
        "X3_Konsumsi_Kalori",
    ]
].dropna()
X_model_harapan = sampel_model_harapan[
    ["X1_Pengeluaran_Kesehatan", "X2_Tingkat_Imunisasi", "X3_Konsumsi_Kalori"]
]
y_model_harapan = sampel_model_harapan["Y_Angka_Harapan_Hidup"]

model_harapan = LinearRegression()
model_harapan.fit(X_model_harapan, y_model_harapan)

koefisien_model_harapan = pd.Series(model_harapan.coef_, index=X_model_harapan.columns)
koefisien_model_harapan.loc["Intercept"] = model_harapan.intercept_

# Pelengkap statistik: standard error dan pengujian pada sampel yang sama.
uji_model_harapan = sm.OLS(
    y_model_harapan,
    sm.add_constant(X_model_harapan, has_constant="add").rename(
        columns={"const": "Intercept"}
    ),
).fit()
print(koefisien_model_harapan.round(4))
print(uji_model_harapan.pvalues.round(4))

# %% [markdown]
# Yang signifikan: tingkat imunisasi (0,1335; p = 0,0018) dan konsumsi
# kalori (0,0090; p = 0,0000). Pengeluaran kesehatan tidak signifikan
# (p = 0,23) setelah dua variabel lain dikontrol.

# %% [markdown]
# ## Latihan 3: prediksi

# %% [markdown]
# <!-- kamus_variabel:uts_6.csv -->
#
# ### Kenali data: Penjualan produk
#
# **Data:** `data/uts_6.csv`. **Satu baris:** satu pengamatan penjualan produk dalam contoh latihan.
#
# | Variabel/kolom | Pengertian | Satuan atau kode | Peran |
# |---|---|---|---|
# | `Y_Penjualan_Unit` | Banyaknya produk yang terjual. | Unit produk dalam data simulasi | Y: target |
# | `X1_Biaya_Iklan` | Biaya promosi/iklan untuk produk tersebut. | Uang; skala tidak dirinci | X: penjelas |
# | `X2_Harga_Produk` | Harga jual produk milik perusahaan. | Uang per unit; skala tidak dirinci | X: penjelas |
# | `X3_Harga_Kompetitor` | Harga produk pesaing yang menjadi pembanding. | Uang per unit; skala tidak dirinci | X: penjelas |
#
# Harga produk sendiri dan harga kompetitor adalah dua variabel berbeda. Periode penjualan dan skala mata uang tidak dijelaskan pada sumber.
#
# Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

# %%
situasi = pd.DataFrame(
    {"X1_Jumlah_Pupuk": [200], "X2_Curah_Hujan": [1500], "X3_Sinar_Matahari": [200]}
)
print(
    "Prediksi produktivitas:",
    round(
        pd.Series(
            model_padi.predict(
                situasi[["X1_Jumlah_Pupuk", "X2_Curah_Hujan", "X3_Sinar_Matahari"]]
            ),
            index=situasi.index,
        )[0],
        3,
    ),
)
print("Prediksi penjualan uts-6 (iklan 60, harga 100, kompetitor 105):")

jual = pd.read_csv(URL_DATA + "uts_6.csv")
sampel_model_jual = jual[
    ["Y_Penjualan_Unit", "X1_Biaya_Iklan", "X2_Harga_Produk", "X3_Harga_Kompetitor"]
].dropna()
X_model_jual = sampel_model_jual[
    ["X1_Biaya_Iklan", "X2_Harga_Produk", "X3_Harga_Kompetitor"]
]
y_model_jual = sampel_model_jual["Y_Penjualan_Unit"]

model_jual = LinearRegression()
model_jual.fit(X_model_jual, y_model_jual)
situasi_jual = pd.DataFrame(
    {"X1_Biaya_Iklan": [60], "X2_Harga_Produk": [100], "X3_Harga_Kompetitor": [105]}
)
print(
    round(
        pd.Series(
            model_jual.predict(
                situasi_jual[
                    ["X1_Biaya_Iklan", "X2_Harga_Produk", "X3_Harga_Kompetitor"]
                ]
            ),
            index=situasi_jual.index,
        )[0],
        2,
    )
)
