# %% [markdown]
# # Kunci Lab 1: Regresi Linear
#
# File ini berisi solusi latihan Lab 1. Semua angka di sini dihasilkan dari
# data di folder `data/`, jadi hasil Anda harus sama (atau sangat dekat).

# %% [markdown]
# ## Persiapan: pastikan data tersedia
#
# Jalankan sel di bawah sekali supaya folder `data/` siap dipakai.

# %% [markdown]
# ## Cara mengikuti notebook ini
#
# Jalankan sel berurutan dengan `Shift + Enter`. Setiap notebook dapat
# dimulai sendiri setelah paket data diunggah. Sel persiapan cukup dijalankan
# apa adanya; fokus latihan dimulai saat tabel data muncul.
#
# Baca penjelasan sebelum menjalankan kode, lalu sebutkan arti hasilnya.
# Ubah satu hal setiap mencoba: nama kolom pada X, pilihan model, atau nilai prediksi.
# Baris `#` adalah catatan. `=` menyimpan hasil dan `==` membandingkan nilai.
# Contoh `tabel["kolom"]` berarti memilih satu kolom dari tabel.
#
# Jika muncul error merah, berhenti di sel itu dan baca baris terakhirnya.
# Jika ada warning, baca pesannya dan periksa hasil estimasi sebelum lanjut.
# Panduan simbol dan contoh tambahan ada di `panduan/01_panduan_pemula.md`.

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
import os
import zipfile
from pathlib import Path

# Di komputer sendiri, temukan folder data dari lokasi notebook ini.
# Di Colab, folder kerja tetap memakai lokasi unggahan Anda.
if not Path("data").is_dir() and Path("../../data").is_dir():
    os.chdir("../..")

# Jalankan apa adanya. Paket dibuka jika alat bantu belum tersedia.
# Jika data sudah siap, menjalankan ulang sel ini tidak menimpa CSV.
if (
    Path("data_tutorial.zip").exists()
    and not Path("alat_bantu/metode_lanjutan.py").exists()
):
    with zipfile.ZipFile("data_tutorial.zip") as paket:
        paket.extractall(".")

if not Path("data/uts_2.csv").exists():
    raise FileNotFoundError(
        "Unggah data_tutorial.zip lewat panel Files di kiri Colab, "
        "lalu jalankan sel ini lagi."
    )

print("Data siap. Lanjutkan ke sel berikutnya.")

# %%
import pandas as pd
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
import numpy as np

# %% [markdown]
# ## Latihan 1: produktivitas padi

# %%
padi = pd.read_csv("data/uts_3.csv")
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

# %%
harapan = pd.read_csv("data/uts_4.csv")
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

jual = pd.read_csv("data/uts_6.csv")
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
