# %% [markdown]
# # Kunci Lab 4: Model Kategorikal

# %% [markdown]
# ## Persiapan: pastikan data tersedia
#
# Jalankan sel di bawah sekali supaya folder `data/` siap dipakai.

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
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import PoissonRegressor
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf

# %% [markdown]
# ## Latihan 1: perfect separation pada data kelulusan

# %%
lulus = pd.read_csv("data/logit_probit_2.csv")

formula = "LULUS_TEPAT ~ IPK_SEM2 + SKS_LULUS_SEM2 + KEAKTIFAN_ORG + BEASISWA"

from alat_bantu.metode_lanjutan import coba_logit

print("Koefisien MLE polos (dapat gagal karena separation):")
print(coba_logit(formula, lulus))

sampel_m2 = lulus[
    ["LULUS_TEPAT", "IPK_SEM2", "SKS_LULUS_SEM2", "KEAKTIFAN_ORG", "BEASISWA"]
].dropna()
X_m2 = sampel_m2[["IPK_SEM2", "SKS_LULUS_SEM2", "KEAKTIFAN_ORG", "BEASISWA"]]
y_m2 = sampel_m2["LULUS_TEPAT"]

m2 = LogisticRegression(
    penalty="l1", C=2.0, solver="liblinear", max_iter=5000, tol=1e-9
)
m2.fit(X_m2, y_m2)

koefisien_m2 = pd.Series(m2.coef_[0], index=X_m2.columns)
koefisien_m2.loc["Intercept"] = m2.intercept_[0]
print("\nKoefisien setelah regularisasi:")
print(koefisien_m2.round(3))

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

kepuasan = pd.read_csv("data/multi_ordinal_1.csv")
model_ord = OrderedModel(
    kepuasan["Kepuasan"],
    kepuasan[["Kecepatan", "Staf_Ramah", "Digital_App"]],
    distr="logit",
).fit(method="bfgs", disp=False)
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
sampel_model_pois = klaim[["JML_KLAIM", "USIA", "PENGALAMAN", "TIPE_MOBIL"]].dropna()
X_model_pois = sampel_model_pois[["USIA", "PENGALAMAN", "TIPE_MOBIL"]]
y_model_pois = sampel_model_pois["JML_KLAIM"]

model_pois = PoissonRegressor(
    alpha=0, solver="newton-cholesky", max_iter=1000, tol=1e-9
)
model_pois.fit(X_model_pois, y_model_pois)

koefisien_model_pois = pd.Series(model_pois.coef_, index=X_model_pois.columns)
koefisien_model_pois.loc["Intercept"] = model_pois.intercept_

# Pelengkap statistik: standard error dan pengujian pada sampel yang sama.
uji_model_pois = sm.Poisson(
    y_model_pois,
    sm.add_constant(X_model_pois, has_constant="add").rename(
        columns={"const": "Intercept"}
    ),
).fit(disp=0)

print("Koefisien:")
print(koefisien_model_pois.round(3))
print("\nIRR:")
print(np.exp(koefisien_model_pois).round(3))

overdisp = (uji_model_pois.resid_pearson**2).sum() / uji_model_pois.df_resid
print(f"\nOverdispersi (Pearson chi2 / df): {overdisp:.3f}")

model_nb = smf.negativebinomial(
    "JML_KLAIM ~ USIA + PENGALAMAN + TIPE_MOBIL", data=klaim
).fit(disp=0)
print("AIC Poisson:", round(uji_model_pois.aic, 2))
print("AIC NB     :", round(model_nb.aic, 2))

# %% [markdown]
# Kesimpulan: tidak ada variabel yang signifikan di data ini (semua
# p > 0,3). Overdispersi 0,14 (di bawah 1,5), jadi Poisson cukup, dan AIC
# Poisson lebih kecil dari Negative Binomial. Laporkan bahwa data ini
# tidak menunjukkan efek yang bisa dibedakan dari nol pada sampel ini.
