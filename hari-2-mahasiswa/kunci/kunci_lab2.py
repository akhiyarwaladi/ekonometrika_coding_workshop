# %% [markdown]
# # Kunci Lab 2: Bentuk Fungsional

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
# ## Latihan 1: pendidikan dan pendapatan (log-lin)

# %%
didik = pd.read_csv("data/pendidikan-pendapatan.csv")
didik["ln_pendapatan"] = np.log(didik["Pendapatan_Tahunan"])

model_didik = smf.ols("ln_pendapatan ~ Tahun_Pendidikan", data=didik).fit()
print(model_didik.params.round(4))
print("Kenaikan pendapatan per tahun pendidikan (persen):",
      round(100 * model_didik.params["Tahun_Pendidikan"], 2))

# %%
# Pembanding: model linear biasa
model_linear = smf.ols("Pendapatan_Tahunan ~ Tahun_Pendidikan", data=didik).fit()
print("R2 log-lin:", round(model_didik.rsquared, 4))
print("R2 linear :", round(model_linear.rsquared, 4))

# %% [markdown]
# Kesimpulan: setiap tambahan satu tahun pendidikan menaikkan pendapatan
# sekitar 21,4 persen. Model log-lin lebih sesuai karena efeknya
# proporsional, dan R kuadratnya juga lebih tinggi (0,994 berbanding
# 0,884).

# %% [markdown]
# ## Latihan 2: usia dan kinerja (kuadratik)

# %%
usia = pd.read_csv("data/usia-unit.csv")
usia["usia2"] = usia["Usia"] ** 2

model_usia = smf.ols("Unit_Terjual ~ Usia + usia2", data=usia).fit()
print(model_usia.params.round(3))

b1 = model_usia.params["Usia"]
b2 = model_usia.params["usia2"]
print("Usia puncak:", round(-b1 / (2 * b2), 2), "tahun")

# %% [markdown]
# Kesimpulan: kinerja memuncak di usia sekitar 39,5 tahun. Koefisien `usia2`
# negatif, itulah yang membuat kurva melengkung ke bawah.

# %% [markdown]
# ## Latihan 3: jam belajar dan skor (reciprocal)

# %%
skor = pd.read_csv("data/jam-skor.csv")
skor["satu_per_jam"] = 1 / skor["Jam_Belajar"]

model_skor = smf.ols("Skor_Ujian ~ satu_per_jam", data=skor).fit()
print(model_skor.params.round(2))

# %% [markdown]
# Kesimpulan: batas skor maksimal (asimtot) sekitar 99,7, dibaca dari
# intersep. Koefisien `satu_per_jam` negatif dan besar, artinya tambahan
# jam belajar membantu, tapi manfaatnya mengecil dan skor mendekati batas
# 99,7.

# %% [markdown]
# ## Latihan 4: memilih bentuk untuk data UTS-1

# %%
uts1 = pd.read_csv("data/uts-1.csv")

# Linear
model_lin = smf.ols(
    "Y_Pertumbuhan_Ekonomi ~ X1_Investasi + X2_Inflasi + X3_Keterbukaan_Perdagangan",
    data=uts1).fit()

# Log-log
uts1["ln_y"] = np.log(uts1["Y_Pertumbuhan_Ekonomi"])
uts1["ln_inv"] = np.log(uts1["X1_Investasi"])
uts1["ln_inflasi"] = np.log(uts1["X2_Inflasi"])
uts1["ln_terbuka"] = np.log(uts1["X3_Keterbukaan_Perdagangan"])
model_log = smf.ols("ln_y ~ ln_inv + ln_inflasi + ln_terbuka", data=uts1).fit()

print("R2 linear:", round(model_lin.rsquared, 4))
print("R2 log-log:", round(model_log.rsquared, 4))
print("p-value linear:")
print(model_lin.pvalues.round(4))
print("p-value log-log:")
print(model_log.pvalues.round(4))

# %% [markdown]
# Kesimpulan: kedua bentuk punya R kuadrat hampir sama (0,995 berbanding
# 0,994). Model linear menampilkan inflasi dan keterbukaan sebagai
# signifikan; model log-log hanya keterbukaan. Pilihan terakhir tetap
# bergantung teori: kalau ingin membaca elastisitas, pakai log-log.
