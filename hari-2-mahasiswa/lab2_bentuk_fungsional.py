# %% [markdown]
# # Lab 2: Bentuk Fungsional Model Regresi
#
# **Durasi:** 90 menit
#
# Tujuan: memilih bentuk model yang sesuai dengan cerita ekonominya.
# Hubungan yang melengkung tidak boleh dipaksa jadi garis lurus.

# %% [markdown]
# **Posisi dalam alur workshop.** Melanjutkan Lab 1 yang berakhir dengan
# pertanyaan bentuk model. Setelah bentuk tepat, Lab 3 memeriksa
# asumsinya.

# %% [markdown]
# ## Persiapan: pastikan data tersedia
#
# Notebook ini membaca CSV dari folder `data/`. Kalau belum ada (misalnya di
# Colab), unggah `data-ekonometrika.zip` lewat panel Files, lalu jalankan
# sel di bawah sekali.

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
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", palette=["#2F5D50", "#C15937", "#D9A441", "#5B8A8F"])
plt.rcParams.update({"figure.dpi": 110, "axes.titleweight": "bold", "font.size": 11})

# %% [markdown]
# ## 1. Contoh terbimbing: fungsi produksi Cobb-Douglas
#
# Data `data/regresi-log.csv`: tenaga kerja (L), modal (K), dan produksi (Q)
# dari 30 observasi. Model yang diuji: $Q = A L^{\beta_1} K^{\beta_2}$.
# Setelah di-log, koefisiennya menjadi elastisitas.

# %%
produksi = pd.read_csv("data/regresi-log.csv").rename(columns={
    "Observasi ke-": "obs", "Tenaga Kerja (L)": "L", "Modal (K)": "K",
    "Produksi (Q)": "Q"})
produksi["lnQ"] = np.log(produksi["Q"])
produksi["lnL"] = np.log(produksi["L"])
produksi["lnK"] = np.log(produksi["K"])

model = smf.ols("lnQ ~ lnL + lnK", data=produksi).fit()
print(model.summary())

# %% [markdown]
# ### Membaca hasil
#
# - Elastisitas tenaga kerja sekitar 0,86: tambahan tenaga kerja 1 persen
#   menaikkan produksi sekitar 0,86 persen.
# - Elastisitas modal sekitar 0,61.
# - Jumlahnya 1,47 (lebih besar dari 1): skala pengembalian meningkat
#   (increasing returns to scale).

# %%
b = model.params
print(f"Elastisitas tenaga kerja : {b['lnL']:.3f}")
print(f"Elastisitas modal        : {b['lnK']:.3f}")
print(f"Jumlah (skala)           : {b['lnL'] + b['lnK']:.3f}")


# %% [markdown]
# ### Coba sendiri (5 menit)
#
# Pakai model Cobb-Douglas di atas. Hitung prediksi produksi untuk
# L = 60 dan K = 120 (ingat: hasilnya dalam bentuk log, perlu di-exp).
#
# Tulis di sel di bawah, baru buka jawabannya.

# %%
# Tulis kode Anda di sini

# %% [markdown]
# <details><summary>Lihat jawaban</summary>
#
# ln Q = -1,99 + 0,86 x ln(60) + 0,61 x ln(120) = 4,46, jadi
# Q = exp(4,46) sekitar 86,5.
#
# </details>

# %% [markdown]
# ## 2. Latihan mandiri
#
# **Latihan 1: pendidikan dan pendapatan.** Data
# `data/pendidikan-pendapatan.csv` berisi 30 responden.
#
# Dugaan di soal: setiap tambahan tahun pendidikan menaikkan pendapatan
# dalam persen, bukan nominal tetap. Model yang cocok: log-lin.
#
# `ln(Pendapatan) ~ Tahun_Pendidikan`
#
# Pertanyaan: berapa persen kenaikan pendapatan per satu tahun tambahan
# pendidikan? (Petunjuk: koefisien dikali 100.)

# %%
# didik = pd.read_csv("data/pendidikan-pendapatan.csv")
# didik["ln_pendapatan"] = np.log(didik["Pendapatan_Tahunan"])
# model_didik = smf.ols("ln_pendapatan ~ Tahun_Pendidikan", data=didik).fit()
# print(model_didik.summary())

# %% [markdown]
# **Latihan 2: usia dan kinerja penjualan.** Data `data/usia-unit.csv`.
# Hipotesisnya: kinerja naik seiring usia, memuncak, lalu menurun. Pakai
# model kuadratik, lalu hitung usia puncaknya dengan rumus
# $-b_1 / (2 b_2)$.
#
# Pertanyaan: pada usia berapa kinerja mencapai puncak?

# %%
# usia = pd.read_csv("data/usia-unit.csv")
# usia["usia2"] = usia["Usia"] ** 2
# model_usia = smf.ols("Unit_Terjual ~ Usia + usia2", data=usia).fit()
# print(model_usia.summary())

# %% [markdown]
# **Latihan 3: jam belajar dan skor ujian.** Data `data/jam-skor.csv`.
# Ada efek jenuh: tambahan jam belajar makin kecil manfaatnya, dan ada
# batas skor maksimal. Model yang cocok: reciprocal,
# `Skor_Ujian ~ 1/X` dengan X = Jam_Belajar.
#
# Pertanyaan: berapa batas skor maksimal (asimtot) yang dibaca dari
# intersep? (Petunjuk: intersep adalah batas atas skor.)

# %%
# skor = pd.read_csv("data/jam-skor.csv")
# skor["satu_per_jam"] = 1 / skor["Jam_Belajar"]
# model_skor = smf.ols("Skor_Ujian ~ satu_per_jam", data=skor).fit()
# print(model_skor.summary())

# %% [markdown]
# **Latihan 4: pilih bentuk untuk data UTS.** Data `data/uts-1.csv`:
# pertumbuhan ekonomi, investasi, inflasi, dan keterbukaan perdagangan.
# Coba tiga bentuk: linear, log-log, dan kuadratik untuk investasi.
# Bandingkan R kuadrat terkoreksi dan p-value. Kriteria: pilih model
# dengan R kuadrat terkoreksi tertinggi di antara model yang tanda
# koefisiennya sesuai teori. Kalau dua model berdekatan, dahulukan yang
# lebih sederhana dan lebih mudah dijelaskan.

# %%
# uts1 = pd.read_csv("data/uts-1.csv")
# model_lin = smf.ols("Y_Pertumbuhan_Ekonomi ~ X1_Investasi + X2_Inflasi + X3_Keterbukaan_Perdagangan", data=uts1).fit()
# ...

# %% [markdown]
# ### Selanjutnya
#
# Selanjutnya: Lab 3, uji asumsi klasik.
