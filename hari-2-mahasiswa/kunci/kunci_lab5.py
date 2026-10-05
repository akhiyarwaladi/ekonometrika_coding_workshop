# %% [markdown]
# # Kunci Lab 5: Deret Waktu dan Data Panel

# %% [markdown]
# ## Persiapan: pastikan data tersedia
#
# Jalankan dua sel di bawah sekali supaya folder `data/` siap dan paket
# `linearmodels` terpasang.

# %%
import zipfile
from pathlib import Path

if not Path("data").exists() and Path("data-ekonometrika.zip").exists():
    zipfile.ZipFile("data-ekonometrika.zip").extractall(".")

print("File data siap:", len(list(Path("data").glob("*.csv"))))

# %%
%pip install linearmodels -q

# %%
import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf

# %% [markdown]
# ## Latihan 1: ADF dan ARIMA untuk saham

# %%
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA

saham_ts = pd.read_csv("data/ts-saham.csv")
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

ie = pd.read_csv("data/ihsg-emas.csv")
p_kointe = coint(ie["IHSG_Y"], ie["Emas_X"])[1]
print("Uji kointegrasi: p =", round(p_kointe, 4))

# %% [markdown]
# Kesimpulan: p = 0,4941, jauh di atas 0,05. IHSG dan emas TIDAK
# terkointegrasi. Walaupun dua-duanya bergerak sepanjang waktu, tidak ada
# hubungan jangka panjang yang mengikat. Karena itu ECM tidak layak
# dipakai di kasus ini. Bandingkan dengan konsumsi-pendapatan
# (p = 0,0001): di sana ECM layak, di sini tidak.

# %% [markdown]
# ## Latihan 3: panel retail CEM vs FEM

# %%
from linearmodels.panel import PanelOLS

retail = pd.read_csv("data/panel-retail.csv").set_index(["StoreID", "Month"])
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
