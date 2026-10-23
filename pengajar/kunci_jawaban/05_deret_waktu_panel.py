# %% [markdown]
# # Kunci Lab 5: Deret Waktu dan Data Panel

# %% [markdown]
# ## Persiapan: pastikan data tersedia
#
# Jalankan dua sel di bawah sekali supaya folder `data/` siap dan paket
# `linearmodels` terpasang.

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
%pip install "linearmodels==7.1" -q

# %%
import pandas as pd
import numpy as np
import statsmodels.api as sm

# %% [markdown]
# ## Latihan 1: ADF dan ARIMA untuk saham

# %%
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA

saham_ts = pd.read_csv("data/ts_saham.csv")
print("ADF level       :", round(adfuller(saham_ts["saham"])[1], 4))
print("ADF selisih     :", round(adfuller(saham_ts["saham"].diff().dropna())[1], 4))

model_saham = ARIMA(saham_ts["saham"], order=(1, 1, 0)).fit()
ramalan = model_saham.get_forecast(steps=5).predicted_mean
print("Ramalan 5 periode:", np.round(np.asarray(ramalan), 1).tolist())

# %% [markdown]
# Kesimpulan: saham tidak stasioner di level (p = 0,98) dan stasioner
# setelah selisih (p = 0,0000), khas random walk. Ramalan ARIMA(1,1,0)
# hampir datar di sekitar 5.787: wajar, karena random walk tidak bisa
# diprediksi arahnya.

# %% [markdown]
# ## Latihan 2: kointegrasi IHSG dan emas

# %%
from statsmodels.tsa.stattools import coint

ie = pd.read_csv("data/ihsg_emas.csv")
p_kointe = coint(ie["IHSG_Y"], ie["Emas_X"])[1]
print("Uji kointegrasi: p =", round(p_kointe, 4))

# %% [markdown]
# Kesimpulan: p = 0,4941, jauh di atas 0,05. IHSG dan emas TIDAK
# terkointegrasi. Walaupun dua-duanya bergerak sepanjang waktu, tidak ada
# hubungan jangka panjang yang mengikat. Karena itu ECM tidak layak
# dipakai di kasus ini. Bandingkan dengan konsumsi-pendapatan
# (p coint = 0,0001). Pada konsumsi-pendapatan, ADF log di level justru
# menolak akar unit; karena itu ECM di sana hanya demonstrasi perhitungan,
# bukan bukti empiris kointegrasi yang memenuhi syarat I(1).

# %% [markdown]
# ## Latihan 3: panel retail CEM vs FEM

# %%
from linearmodels.panel import PanelOLS

retail = pd.read_csv("data/panel_retail.csv")
retail = retail.set_index(["StoreID", "Month"])
y = retail["Sales_Y"]
X = retail[["Ads_X1", "Discount_X2"]]

cem = PanelOLS(y, sm.add_constant(X)).fit()
fem = PanelOLS(y, X, entity_effects=True).fit()

print("CEM:")
print(cem.params.round(3))
print("\nFEM:")
print(fem.params.round(3))

# %% [markdown]
# Kesimpulan: di CEM, koefisien diskon -157 (signifikan) karena model
# mencampur perbedaan antar toko: toko beromzet tinggi kebetulan juga
# memberi diskon besar. Setelah efek toko dikontrol (FEM), koefisien
# diskon hanya -1,9 dan tidak signifikan. Untuk kebijakan diskon, yang
# relevan adalah perubahan DI DALAM toko yang sama, jadi FEM lebih
# dipercaya. Uji Chow p-value sangat kecil, mendukung FEM.
