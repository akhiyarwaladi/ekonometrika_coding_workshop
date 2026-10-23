# %% [markdown]
# # Lab 5: Deret Waktu dan Data Panel
#
# **Durasi:** 90 menit
#
# Tujuan: menguji stasioneritas, meramal dengan ARIMA, menguji
# kointegrasi, dan menaksir model data panel.

# %% [markdown]
# **Posisi dalam alur workshop.** Menambah dimensi waktu dan individu ke
# model. Lab 6 menutup dengan data Indonesia asli.

# %% [markdown]
# ## Persiapan: pastikan data tersedia
#
# Notebook ini membaca CSV dari folder `data/`. Kalau belum ada (misalnya di
# Colab), unggah `data_tutorial.zip` lewat panel Files, lalu jalankan
# sel di bawah sekali. Paket `linearmodels` dipasang di sel berikutnya
# (butuh internet sekali saja).

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
from sklearn.linear_model import LinearRegression
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", palette=["#2F5D50", "#C15937", "#D9A441", "#5B8A8F"])
plt.rcParams.update({"figure.dpi": 110, "axes.titleweight": "bold", "font.size": 11})

# %% [markdown]
# ## 1. Stasioneritas dan ARIMA
#
# Data `data/ts_inflasi.csv`: indeks harga 50 periode yang naik terus.
# Langkah pertama selalu melihat plot.

# %%
inflasi = pd.read_csv("data/ts_inflasi.csv")

plt.figure(figsize=(9, 4))
plt.plot(inflasi["obs"], inflasi["inflasi"], lw=1.6)
plt.title("Inflasi: tren naik terus")
plt.xlabel("Periode")
plt.show()

# %%
from statsmodels.tsa.stattools import adfuller

p_level = adfuller(inflasi["inflasi"])[1]
p_diff = adfuller(inflasi["inflasi"].diff().dropna())[1]
print(f"ADF di level          : p = {p_level:.4f}")
print(f"ADF setelah selisih   : p = {p_diff:.4f}")

# %% [markdown]
# ### Membaca hasil
#
# Di level, p-value besar: data tidak stasioner (ada tren). Setelah satu
# kali selisih, p-value kecil: sudah stasioner. Kesimpulan: pakai d = 1.
#
# Model ARIMA(1,1,0) artinya: satu kali selisih, satu komponen AR.

# %%
from statsmodels.tsa.arima.model import ARIMA

model = ARIMA(inflasi["inflasi"], order=(1, 1, 0)).fit()
print(model.summary())

# %%
ramalan = model.get_forecast(steps=5)
print("Ramalan inflasi 5 periode ke depan:")
print(np.asarray(ramalan.predicted_mean).round(2))

plt.figure(figsize=(9, 4))
plt.plot(inflasi["obs"], inflasi["inflasi"], label="aktual")
masa_depan = np.arange(51, 56)
plt.plot(masa_depan, np.asarray(ramalan.predicted_mean), marker="o", label="ramalan")
plt.legend()
plt.title("Ramalan inflasi")
plt.show()

# %% [markdown]
# ## 2. Kointegrasi dan ECM
#
# Data `data/konsumsi_pendapatan.csv`. Dua variabel yang sama-sama
# tidak stasioner bisa tetap berjalan bersama dalam jangka panjang.

# %%
from statsmodels.tsa.stattools import coint

makro = pd.read_csv("data/konsumsi_pendapatan.csv")
makro = makro.rename(columns={"Konsumsi_Y": "konsumsi", "Pendapatan_X": "pendapatan"})
makro["ln_konsumsi"] = np.log(makro["konsumsi"])
makro["ln_pendapatan"] = np.log(makro["pendapatan"])

print("ADF level:")
print("  ln(konsumsi)  :", round(adfuller(makro["ln_konsumsi"])[1], 4))
print("  ln(pendapatan):", round(adfuller(makro["ln_pendapatan"])[1], 4))

# %% [markdown]
# **Batas contoh simulasi ini.** ADF dengan konstanta pada log kedua seri
# memberi p sekitar 0,023 dan 0,013: akar unit sudah ditolak pada level.
# Jadi hasil coint di bawah tidak cukup untuk menyatakan kedua seri I(1)
# terkointegrasi. Perhitungan berikut memperagakan bentuk persamaan jangka
# panjang dan komponen ECM, bukan bukti empiris kointegrasi yang sah.
# Untuk penelitian, tetapkan tren/konstanta berdasarkan teori dan grafik,
# periksa orde integrasi, lalu gunakan uji kointegrasi yang sesuai.

# %%
p_kointe = coint(makro["ln_konsumsi"], makro["ln_pendapatan"])[1]
print(f"\nUji kointegrasi: p = {p_kointe:.4f}")
print("ECM berikut adalah demonstrasi; syarat I(1) belum terpenuhi pada contoh ini.")

# %%
sampel_model_lr = makro[["ln_konsumsi", "ln_pendapatan"]].dropna()
X_model_lr = sampel_model_lr[["ln_pendapatan"]]
y_model_lr = sampel_model_lr["ln_konsumsi"]

model_lr = LinearRegression()
model_lr.fit(X_model_lr, y_model_lr)

koefisien_model_lr = pd.Series(model_lr.coef_, index=X_model_lr.columns)
koefisien_model_lr.loc["Intercept"] = model_lr.intercept_

prediksi_model_lr = pd.Series(model_lr.predict(X_model_lr), index=y_model_lr.index)
residu_model_lr = y_model_lr - prediksi_model_lr
print("Persamaan jangka panjang:")
print(koefisien_model_lr.round(3))

# %%
# Siapkan komponen ECM: selisih untuk efek jangka pendek
makro["d_konsumsi"] = makro["ln_konsumsi"].diff()
makro["d_pendapatan"] = makro["ln_pendapatan"].diff()
# ECT = residual jangka panjang periode sebelumnya (koreksi ketidakseimbangan)
makro["ect"] = residu_model_lr.shift(1)

sampel_model_ecm = makro[["d_konsumsi", "d_pendapatan", "ect"]].dropna()
X_model_ecm = sampel_model_ecm[["d_pendapatan", "ect"]]
y_model_ecm = sampel_model_ecm["d_konsumsi"]

model_ecm = LinearRegression()
model_ecm.fit(X_model_ecm, y_model_ecm)

koefisien_model_ecm = pd.Series(model_ecm.coef_, index=X_model_ecm.columns)
koefisien_model_ecm.loc["Intercept"] = model_ecm.intercept_

# Pelengkap statistik: standard error dan pengujian pada sampel yang sama.
uji_model_ecm = sm.OLS(
    y_model_ecm,
    sm.add_constant(X_model_ecm, has_constant="add").rename(
        columns={"const": "Intercept"}
    ),
).fit()
print("\nECM:")
print(koefisien_model_ecm.round(3))
print(uji_model_ecm.pvalues.round(4))

# %% [markdown]
# ### Membaca hasil
#
# Koefisien `ect` = -0,70 dan signifikan. Artinya 70 persen
# ketidakseimbangan periode sebelumnya dikoreksi pada periode ini, menuju
# keseimbangan jangka panjang.

# %% [markdown]
# ## 3. Data panel
#
# Data `data/panel_padi.csv`: 5 petak sawah x 10 musim. Hasil panen
# dijelaskan pupuk dan curah hujan. Dengan struktur panel, kita bisa
# memisahkan pengaruh yang melekat pada tiap petak.

# %%
from linearmodels.panel import PanelOLS

padi = pd.read_csv("data/panel_padi.csv")
padi = padi.set_index(["FarmID", "Season"])
y = padi["Yield_Y"]
X = padi[["Fertilizer_X1", "Rainfall_X2"]]

fem = PanelOLS(y, X, entity_effects=True).fit(cov_type="clustered", cluster_entity=True)
print(fem.summary)

# %%
print("Uji Chow (pooled vs fixed effect):")
print(fem.f_pooled)

# %% [markdown]
# ### Membaca hasil
#
# p-value uji Chow sangat kecil: efek individu petak sawah nyata, jadi
# Fixed Effect lebih tepat daripada mencampur semua petak. Koefisien
# pupuk sekitar 0,038: tambahan satu kg pupuk per hektar menaikkan hasil
# sekitar 0,038 ton per hektar dalam petak yang sama.

# %% [markdown]
# ### Coba sendiri (5 menit)
#
# Jalankan CEM (tanpa `entity_effects`) untuk data padi. Bandingkan
# koefisien pupuknya dengan FEM di atas. Kenapa berbeda?
#
# Tulis di sel di bawah, baru buka jawabannya.

# %%
# Tulis kode Anda di sini

# %% [markdown]
# <details><summary>Lihat jawaban</summary>
#
# CEM memberi koefisien pupuk 0,0507, FEM 0,0382. CEM mencampur
# perbedaan antar petak sawah dengan perubahan dalam satu petak,
# sehingga angkanya lebih besar. FEM lebih tepat untuk pertanyaan
# perubahan dalam petak yang sama.
#
# </details>

# %% [markdown]
# ## 4. Latihan mandiri
#
# **Latihan 1: ADF dan ARIMA untuk saham.** Data `data/ts_saham.csv`.
# - Cek ADF di level dan setelah selisih. Stasioner di level atau setelah
#   selisih?
# - Estimasi ARIMA(1,1,0) dan ramalkan 5 periode.

# %%
# saham_ts = pd.read_csv("data/ts_saham.csv")
# ...

# %% [markdown]
# **Latihan 2: kointegrasi IHSG dan emas.** Data `data/ihsg_emas.csv`.
# - Jalankan uji `coint(IHSG_Y, Emas_X)`.
# - Kalau p < 0,05, estimasi ECM. Kalau tidak, jelaskan kenapa ECM
#   sebaiknya tidak dipakai.

# %%
# ie = pd.read_csv("data/ihsg_emas.csv")
# ...

# %% [markdown]
# **Latihan 3: panel retail.** Data `data/panel_retail.csv`
# (5 toko x 10 bulan, `Sales_Y ~ Ads_X1 + Discount_X2`).
# - Estimasi CEM (tanpa `entity_effects`) dan FEM (dengan
#   `entity_effects=True`).
# - Bandingkan koefisien diskon di kedua model. Mana yang Anda percaya
#   untuk kebijakan diskon? Kenapa?

# %%
# retail = pd.read_csv("data/panel_retail.csv").set_index(["StoreID", "Month"])
# ...

# %% [markdown]
# ### Selanjutnya
#
# Selanjutnya: Lab 6, data Indonesia asli.
