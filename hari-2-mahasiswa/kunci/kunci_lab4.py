# %% [markdown]
# # Kunci Lab 4: Model Kategorikal

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
import warnings
import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf

warnings.filterwarnings("ignore")

# %% [markdown]
# ## Latihan 1: perfect separation pada data kelulusan

# %%
lulus = pd.read_csv("data/logit-probit-2.csv")

formula = "LULUS_TEPAT ~ IPK_SEM2 + SKS_LULUS_SEM2 + KEAKTIFAN_ORG + BEASISWA"

m1 = smf.logit(formula, data=lulus).fit(disp=0)
print("Koefisien MLE polos (tidak stabil):")
print(m1.params.round(2))

m2 = smf.logit(formula, data=lulus).fit_regularized(alpha=0.5, L1_wt=0.0, disp=0)
print("\nKoefisien setelah regularisasi:")
print(m2.params.round(3))

# %% [markdown]
# Kesimpulan: kombinasi nilai X memprediksi kelulusan secara sempurna
# (perfect separation), sehingga likelihood maksimum tidak punya solusi
# berhingga dan koefisien meledak. Regularisasi menstabilkannya: IPK
# tetap positif (pengaruh terbesar), SKS dan keaktifan organisasi negatif
# setelah IPK dikontrol. Untuk laporan, sebutkan keterbatasan estimator
# ini karena p-value tidak tersedia.

# %% [markdown]
# ## Latihan 2: model ordinal (multi-ordinal-1)

# %%
from statsmodels.miscmodels.ordinal_model import OrderedModel

kepuasan = pd.read_csv("data/multi-ordinal-1.csv")
model_ord = OrderedModel(
    kepuasan["Kepuasan"],
    kepuasan[["Kecepatan", "Staf_Ramah", "Digital_App"]],
    distr="logit").fit(method="bfgs", disp=False)
print(model_ord.params.round(3))

# %% [markdown]
# Kesimpulan (baca tanda, bukan besaran):
#
# - Kecepatan (waktu tunggu, menit) negatif: makin lama menunggu, makin
#   tidak puas.
# - Staf_Ramah positif: makin ramah, makin puas.
# - Digital_App positif: yang sering memakai aplikasi cenderung lebih puas.
#
# Koefisien absolutnya puluhan karena data simulasi nyaris terpisah
# sempurna. Jangan mengutip besarannya di laporan dengan data seperti ini.

# %% [markdown]
# ## Latihan 3: Poisson (poisson-1)

# %%
klaim = pd.read_csv("data/poisson_data_1_klaim.csv")
model_pois = smf.poisson("JML_KLAIM ~ USIA + PENGALAMAN + TIPE_MOBIL",
                         data=klaim).fit(disp=0)

print("Koefisien:")
print(model_pois.params.round(3))
print("\nIRR:")
print(np.exp(model_pois.params).round(3))

overdisp = (model_pois.resid_pearson ** 2).sum() / model_pois.df_resid
print(f"\nOverdispersi (Pearson chi2 / df): {overdisp:.3f}")

model_nb = smf.negativebinomial("JML_KLAIM ~ USIA + PENGALAMAN + TIPE_MOBIL",
                                data=klaim).fit(disp=0)
print("AIC Poisson:", round(model_pois.aic, 2))
print("AIC NB     :", round(model_nb.aic, 2))

# %% [markdown]
# Kesimpulan: tidak ada variabel yang signifikan di data ini (semua
# p > 0,3). Overdispersi 0,14 (di bawah 1,5), jadi Poisson cukup, dan AIC
# Poisson lebih kecil dari Negative Binomial. Laporkan bahwa data ini
# tidak menunjukkan efek yang bisa dibedakan dari nol. Itu juga hasil
# penelitian, bukan kegagalan.
