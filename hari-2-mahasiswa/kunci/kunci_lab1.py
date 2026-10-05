# %% [markdown]
# # Kunci Lab 1: Regresi Linear
#
# File ini berisi solusi latihan Lab 1. Semua angka di sini dihasilkan dari
# data di folder `data/`, jadi hasil Anda harus sama (atau sangat dekat).

# %% [markdown]
# ## Persiapan: pastikan data tersedia
#
# Jalankan sel di bawah sekali supaya folder `data/` siap dipakai.

# %%
import zipfile
from pathlib import Path

if not Path("data").exists() and Path("data-ekonometrika.zip").exists():
    zipfile.ZipFile("data-ekonometrika.zip").extractall(".")

print("File data siap:", len(list(Path("data").glob("*.csv"))))

# %%
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf

# %% [markdown]
# ## Latihan 1: produktivitas padi

# %%
padi = pd.read_csv("data/uts-3.csv")
model_padi = smf.ols(
    "Y_Produktivitas_Padi ~ X1_Jumlah_Pupuk + X2_Curah_Hujan + X3_Sinar_Matahari",
    data=padi).fit()
print(model_padi.summary())

# %% [markdown]
# Kesimpulan:
#
# - Yang signifikan hanya curah hujan (p = 0,0000, koefisien 0,0029).
#   Kenaikan curah hujan 100 mm menaikkan produktivitas sekitar 0,29 ton.
# - Pupuk (p = 0,69) dan sinar matahari (p = 0,48) tidak signifikan.
# - R kuadrat 0,988, tapi lihat catatan: data simulasi.

# %%
print(model_padi.pvalues.round(4))

# %% [markdown]
# ## Latihan 2: angka harapan hidup

# %%
harapan = pd.read_csv("data/uts-4.csv")
model_harapan = smf.ols(
    "Y_Angka_Harapan_Hidup ~ X1_Pengeluaran_Kesehatan + X2_Tingkat_Imunisasi + X3_Konsumsi_Kalori",
    data=harapan).fit()
print(model_harapan.params.round(4))
print(model_harapan.pvalues.round(4))

# %% [markdown]
# Yang signifikan: tingkat imunisasi (0,1335; p = 0,0018) dan konsumsi
# kalori (0,0090; p = 0,0000). Pengeluaran kesehatan tidak signifikan
# (p = 0,23) setelah dua variabel lain dikontrol.

# %% [markdown]
# ## Latihan 3: prediksi

# %%
situasi = pd.DataFrame({
    "X1_Jumlah_Pupuk": [200], "X2_Curah_Hujan": [1500], "X3_Sinar_Matahari": [200]})
print("Prediksi produktivitas:", round(model_padi.predict(situasi)[0], 3))
print("Prediksi penjualan uts-6 (iklan 60, harga 100, kompetitor 105):")

jual = pd.read_csv("data/uts-6.csv")
model_jual = smf.ols(
    "Y_Penjualan_Unit ~ X1_Biaya_Iklan + X2_Harga_Produk + X3_Harga_Kompetitor",
    data=jual).fit()
situasi_jual = pd.DataFrame({
    "X1_Biaya_Iklan": [60], "X2_Harga_Produk": [100], "X3_Harga_Kompetitor": [105]})
print(round(model_jual.predict(situasi_jual)[0], 2))
