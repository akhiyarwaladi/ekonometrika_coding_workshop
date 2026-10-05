# %% [markdown]
# # Kunci Lab 3: Dummy dan Asumsi Klasik

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
import statsmodels.api as sm
import statsmodels.formula.api as smf

# %% [markdown]
# ## Latihan 1: heteroskedastisitas (hetero-2)

# %%
from statsmodels.stats.diagnostic import het_breuschpagan, het_white

kerja = pd.read_csv("data/hetero-2.csv")
model_kerja = smf.ols("Pendapatan ~ Pendidikan + Pengalaman + Usia", data=kerja).fit()

Xk = sm.add_constant(kerja[["Pendidikan", "Pengalaman", "Usia"]])
print("BP p   :", round(het_breuschpagan(model_kerja.resid, Xk)[1], 4))
print("White p:", round(het_white(model_kerja.resid, Xk)[1], 4))

model_robust = smf.ols("Pendapatan ~ Pendidikan + Pengalaman + Usia",
                       data=kerja).fit(cov_type="HC3")
banding = pd.DataFrame({
    "p_biasa": model_kerja.pvalues,
    "p_robust": model_robust.pvalues,
})
print(banding.round(4))

# %% [markdown]
# Kesimpulan: Breusch-Pagan menolak homoskedastis (p = 0,0025), White
# tidak menolak pada 5% (p = 0,064). Karena ada bukti heteroskedastis,
# laporkan versi robust. Perubahan yang terlihat: p-value pendidikan
# naik dari 0,0089 ke 0,0286, tetap signifikan tapi lebih lemah.

# %% [markdown]
# ## Latihan 2: normalitas (latihan-normalitas-3)

# %%
from statsmodels.stats.stattools import jarque_bera
import matplotlib.pyplot as plt
import seaborn as sns

nrumah = pd.read_csv("data/latihan-normalitas-3.csv")
model_n = smf.ols("Harga ~ Luas_Bangunan + Jumlah_Kamar + Usia_Rumah", data=nrumah).fit()

jb, p_jb, skew, kurt = jarque_bera(model_n.resid)
print(f"Jarque-Bera = {jb:.4f}, p = {p_jb:.4f}")

sns.histplot(model_n.resid, kde=True)
plt.title("Histogram residual")
plt.show()

# %% [markdown]
# Kesimpulan: p = 0,2032 di atas 0,05, jadi residual tidak menyimpang
# jauh dari normal. Asumsi normalitas terpenuhi untuk data ini.

# %% [markdown]
# ## Latihan 3: kasus tanpa pelanggaran (hetero-1)

# %%
jual = pd.read_csv("data/hetero-1.csv")
model_jual = smf.ols("Penjualan ~ Iklan + Salesperson + Diskon", data=jual).fit()
Xj = sm.add_constant(jual[["Iklan", "Salesperson", "Diskon"]])
print("BP p   :", round(het_breuschpagan(model_jual.resid, Xj)[1], 4))
print("White p:", round(het_white(model_jual.resid, Xj)[1], 4))

# %% [markdown]
# Kesimpulan: kedua uji tidak menolak homoskedastis (p = 0,997 dan 0,542).
# Dugaan "variabilitas penjualan membesar saat iklan tinggi" tidak
# didukung data ini. Yang benar: laporkan apa adanya, jangan paksakan
# narasi. Ini juga contoh bahwa hipotesis bisa ditolak data.
