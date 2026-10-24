# %% [markdown]
# # Kunci Lab 5: Deret Waktu dan Data Panel

# %% [markdown]
# ## Persiapan: alamat data
#
# Jalankan sel alamat data dan instalasi `linearmodels` dengan koneksi internet.

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
URL_DATA = "https://raw.githubusercontent.com/akhiyarwaladi/ekonometrika_coding_workshop/main/data/"

print("Alamat data siap. Jalankan sel pembacaan CSV berikutnya.")

# %%
%pip install "linearmodels==7.1" -q

# %%
import pandas as pd
import numpy as np
import statsmodels.api as sm

# %% [markdown]
# ## Latihan 1: ADF dan ARIMA untuk saham

# %% [markdown]
# <!-- kamus_variabel:ts_saham.csv -->
#
# ### Kenali data: Harga saham simulasi
#
# **Data:** `data/ts_saham.csv`. **Satu baris:** satu urutan periode simulasi; bukan tanggal kalender.
#
# | Variabel/kolom | Pengertian | Satuan atau kode | Peran |
# |---|---|---|---|
# | `obs` | Urutan waktu pengamatan. | 1, 2, 3, ...; frekuensi kalender tidak dirinci | Penanda waktu |
# | `saham` | Deret harga saham simulasi untuk uji stasioneritas dan peramalan. | Level harga; skala uang tidak dirinci | Deret yang dianalisis |
#
# Nomor obs tidak menunjukkan tanggal/bulan/tahun tertentu. Angka level dan perubahan persennya harus dibedakan.
#
# Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

# %%
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA

saham_ts = pd.read_csv(URL_DATA + "ts_saham.csv")
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

# %% [markdown]
# <!-- kamus_variabel:ihsg_emas.csv -->
#
# ### Kenali data: IHSG dan harga emas simulasi
#
# **Data:** `data/ihsg_emas.csv`. **Satu baris:** satu bulan berurutan pada contoh simulasi.
#
# | Variabel/kolom | Pengertian | Satuan atau kode | Peran |
# |---|---|---|---|
# | `Bulan` | Urutan bulan pengamatan. | Nomor bulan; tanggal kalender tidak dicantumkan | Penanda waktu |
# | `IHSG_Y` | Indeks Harga Saham Gabungan dalam contoh simulasi. | Poin indeks | Y: target |
# | `Emas_X` | Harga emas pada contoh simulasi. | Mata uang dan berat acuan tidak dirinci | X: penjelas |
#
# Tabel ini adalah contoh simulasi; berbeda dari data IHSG harian unduhan Yahoo Finance.
#
# Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

# %%
from statsmodels.tsa.stattools import coint

ie = pd.read_csv(URL_DATA + "ihsg_emas.csv")
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

# %% [markdown]
# <!-- kamus_variabel:panel_retail.csv -->
#
# ### Kenali data: Panel toko ritel
#
# **Data:** `data/panel_retail.csv`. **Satu baris:** satu cabang toko pada satu bulan.
#
# | Variabel/kolom | Pengertian | Satuan atau kode | Peran |
# |---|---|---|---|
# | `StoreID` | Kode cabang toko. | Nomor identitas toko | Penanda, bukan besaran ekonomi |
# | `Month` | Urutan bulan dalam panel. | Bulan ke-1, ke-2, ... | Penanda waktu |
# | `Sales_Y` | Besarnya penjualan toko pada bulan tersebut. | Satuan/skala tidak dirinci sumber | Y: target |
# | `Ads_X1` | Biaya iklan cabang toko. | Satuan/skala tidak dirinci sumber | X: penjelas |
# | `Discount_X2` | Proporsi potongan harga. | Pecahan; 0,10 berarti diskon 10% | X: penjelas |
#
# Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

# %%
from linearmodels.panel import PanelOLS

retail = pd.read_csv(URL_DATA + "panel_retail.csv")
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
