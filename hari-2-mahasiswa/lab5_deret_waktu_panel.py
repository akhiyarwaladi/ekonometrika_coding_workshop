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
# Colab), unggah `data-ekonometrika.zip` lewat panel Files, lalu jalankan
# sel di bawah sekali. Paket `linearmodels` dipasang di sel berikutnya
# (butuh internet sekali saja).

# %%
import zipfile
from pathlib import Path

if not Path("data").exists() and Path("data-ekonometrika.zip").exists():
    zipfile.ZipFile("data-ekonometrika.zip").extractall(".")

jumlah = len(list(Path("data").glob("*.csv")))
print(f"{jumlah} file data siap dipakai dari folder data/")
if jumlah == 0:
    print("Folder data/ kosong. Unggah data-ekonometrika.zip dulu, lalu jalankan sel ini lagi.")

# %%
%pip install linearmodels -q

# %%
import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", palette=["#2F5D50", "#C15937", "#D9A441", "#5B8A8F"])
plt.rcParams.update({"figure.dpi": 110, "axes.titleweight": "bold", "font.size": 11})

# %% [markdown]
# ## 1. Stasioneritas dan ARIMA
#
# Data `data/ts-inflasi.csv`: indeks harga 50 periode yang naik terus.
# Langkah pertama selalu melihat plot.

# %%
inflasi = pd.read_csv("data/ts-inflasi.csv")

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
# Data `data/konsumsi-pendapatan.csv`. Dua variabel yang sama-sama
# tidak stasioner bisa tetap berjalan bersama dalam jangka panjang.

# %%
from statsmodels.tsa.stattools import coint

makro = pd.read_csv("data/konsumsi-pendapatan.csv").rename(columns={
    "Konsumsi_Y": "konsumsi", "Pendapatan_X": "pendapatan"})
makro["ln_konsumsi"] = np.log(makro["konsumsi"])
makro["ln_pendapatan"] = np.log(makro["pendapatan"])

print("ADF level:")
print("  ln(konsumsi)  :", round(adfuller(makro["ln_konsumsi"])[1], 4))
print("  ln(pendapatan):", round(adfuller(makro["ln_pendapatan"])[1], 4))

p_kointe = coint(makro["ln_konsumsi"], makro["ln_pendapatan"])[1]
print(f"\nUji kointegrasi: p = {p_kointe:.4f}")
print("p < 0,05 berarti terkointegrasi, lanjut ke ECM.")

# %%
model_lr = smf.ols("ln_konsumsi ~ ln_pendapatan", data=makro).fit()
print("Persamaan jangka panjang:")
print(model_lr.params.round(3))

# %%
# Siapkan komponen ECM: selisih untuk efek jangka pendek
makro["d_konsumsi"] = makro["ln_konsumsi"].diff()
makro["d_pendapatan"] = makro["ln_pendapatan"].diff()
# ECT = residual jangka panjang periode sebelumnya (koreksi ketidakseimbangan)
makro["ect"] = model_lr.resid.shift(1)

model_ecm = smf.ols("d_konsumsi ~ d_pendapatan + ect", data=makro).fit()
print("\nECM:")
print(model_ecm.params.round(3))
print(model_ecm.pvalues.round(4))

# %% [markdown]
# ### Membaca hasil
#
# Koefisien `ect` = -0,70 dan signifikan. Artinya 70 persen
# ketidakseimbangan periode sebelumnya dikoreksi pada periode ini, menuju
# keseimbangan jangka panjang.

# %% [markdown]
# ## 3. Data panel
#
# Data `data/panel-padi.csv`: 5 petak sawah x 10 musim. Hasil panen
# dijelaskan pupuk dan curah hujan. Dengan struktur panel, kita bisa
# memisahkan pengaruh yang melekat pada tiap petak.

# %%
from linearmodels.panel import PanelOLS

padi = pd.read_csv("data/panel-padi.csv").set_index(["FarmID", "Season"])
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
# **Latihan 1: ADF dan ARIMA untuk saham.** Data `data/ts-saham.csv`.
# - Cek ADF di level dan setelah selisih. Stasioner di level atau setelah
#   selisih?
# - Estimasi ARIMA(1,1,0) dan ramalkan 5 periode.

# %%
# saham_ts = pd.read_csv("data/ts-saham.csv")
# ...

# %% [markdown]
# **Latihan 2: kointegrasi IHSG dan emas.** Data `data/ihsg-emas.csv`.
# - Jalankan uji `coint(IHSG_Y, Emas_X)`.
# - Kalau p < 0,05, estimasi ECM. Kalau tidak, jelaskan kenapa ECM
#   sebaiknya tidak dipakai.

# %%
# ie = pd.read_csv("data/ihsg-emas.csv")
# ...

# %% [markdown]
# **Latihan 3: panel retail.** Data `data/panel-retail.csv`
# (5 toko x 10 bulan, `Sales_Y ~ Ads_X1 + Discount_X2`).
# - Estimasi CEM (tanpa `entity_effects`) dan FEM (dengan
#   `entity_effects=True`).
# - Bandingkan koefisien diskon di kedua model. Mana yang Anda percaya
#   untuk kebijakan diskon? Kenapa?

# %%
# retail = pd.read_csv("data/panel-retail.csv").set_index(["StoreID", "Month"])
# ...

# %% [markdown]
# ### Selanjutnya
#
# Selanjutnya: Lab 6, data Indonesia asli.
