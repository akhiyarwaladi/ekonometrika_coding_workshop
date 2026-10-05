# %% [markdown]
# # Kunci Lab 0: Mulai dari Nol
#
# Jawaban latihan Lab 0.

# %% [markdown]
# ## Persiapan: pastikan data tersedia

# %%
import zipfile
from pathlib import Path

if not Path("data").exists() and Path("data-ekonometrika.zip").exists():
    zipfile.ZipFile("data-ekonometrika.zip").extractall(".")

print("File data siap:", len(list(Path("data").glob("*.csv"))))

# %%
import pandas as pd
import statsmodels.formula.api as smf

# %% [markdown]
# ## Latihan 1 dan 2: baca data dan hitung rata-rata

# %%
harapan_hidup = pd.read_csv("data/uts-4.csv")
print("Jumlah observasi:", len(harapan_hidup))
harapan_hidup.head()

# %%
print("Rata-rata harapan hidup :", round(harapan_hidup["Y_Angka_Harapan_Hidup"].mean(), 2))
print("Rata-rata imunisasi     :", round(harapan_hidup["X2_Tingkat_Imunisasi"].mean(), 2))

# %% [markdown]
# ## Latihan 3: regresi sederhana

# %%
model = smf.ols(
    "Y_Angka_Harapan_Hidup ~ X1_Pengeluaran_Kesehatan",
    data=harapan_hidup).fit()
print(model.params.round(5))
print(model.pvalues.round(4))

# %% [markdown]
# Kesimpulan: koefisien pengeluaran kesehatan 0,00243 dengan p-value
# 0,0000, jadi signifikan. Setiap tambahan satu unit pengeluaran kesehatan
# diiringi kenaikan harapan hidup 0,00243 tahun. R kuadrat model ini
# sekitar 0,91.
