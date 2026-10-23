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
# Colab), unggah `data_tutorial.zip` lewat panel Files, lalu jalankan
# sel di bawah sekali.

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
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", palette=["#2F5D50", "#C15937", "#D9A441", "#5B8A8F"])
plt.rcParams.update({"figure.dpi": 110, "axes.titleweight": "bold", "font.size": 11})

# %% [markdown]
# ## 1. Contoh terbimbing: fungsi produksi Cobb-Douglas
#
# Data `data/regresi_log.csv`: tenaga kerja (L), modal (K), dan produksi (Q)
# dari 30 observasi. Model yang diuji: $Q = A L^{\beta_1} K^{\beta_2}$.
# Setelah di-log, koefisiennya menjadi elastisitas.

# %%
produksi = pd.read_csv("data/regresi_log.csv")
produksi = produksi.rename(
    columns={
        "Observasi ke-": "obs",
        "Tenaga Kerja (L)": "L",
        "Modal (K)": "K",
        "Produksi (Q)": "Q",
    }
)
produksi["lnQ"] = np.log(produksi["Q"])
produksi["lnL"] = np.log(produksi["L"])
produksi["lnK"] = np.log(produksi["K"])

sampel_model = produksi[["lnQ", "lnL", "lnK"]].dropna()
X_model = sampel_model[["lnL", "lnK"]]
y_model = sampel_model["lnQ"]

model = LinearRegression()
model.fit(X_model, y_model)

koefisien_model = pd.Series(model.coef_, index=X_model.columns)
koefisien_model.loc["Intercept"] = model.intercept_

# Pelengkap statistik: standard error dan pengujian pada sampel yang sama.
uji_model = sm.OLS(
    y_model,
    sm.add_constant(X_model, has_constant="add").rename(columns={"const": "Intercept"}),
).fit()
print(uji_model.summary())

# %% [markdown]
# ### Membaca hasil
#
# - Elastisitas tenaga kerja sekitar 0,86: tambahan tenaga kerja 1 persen
#   menaikkan produksi sekitar 0,86 persen.
# - Elastisitas modal sekitar 0,61.
# - Jumlahnya 1,47 (lebih besar dari 1): skala pengembalian meningkat
#   (increasing returns to scale).

# %%
b = koefisien_model
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
# `data/pendidikan_pendapatan.csv` berisi 30 responden.
#
# Dugaan di soal: setiap tambahan tahun pendidikan menaikkan pendapatan
# dalam persen, bukan nominal tetap. Model yang cocok: log-lin.
#
# `ln(Pendapatan) ~ Tahun_Pendidikan`
#
# Pertanyaan: berapa persen kenaikan pendapatan per satu tahun tambahan
# pendidikan? (Petunjuk: koefisien dikali 100.)

# %%
# didik = pd.read_csv("data/pendidikan_pendapatan.csv")
# didik["ln_pendapatan"] = np.log(didik["Pendapatan_Tahunan"])
# sampel_model_didik = didik[["ln_pendapatan", "Tahun_Pendidikan"]].dropna()
# X_model_didik = sampel_model_didik[["Tahun_Pendidikan"]]
# y_model_didik = sampel_model_didik["ln_pendapatan"]
#
# model_didik = LinearRegression()
# model_didik.fit(X_model_didik, y_model_didik)
#
# # Pelengkap statistik: standard error dan pengujian pada sampel yang sama.
# uji_model_didik = sm.OLS(
#     y_model_didik,
#     sm.add_constant(X_model_didik, has_constant="add").rename(
#         columns={"const": "Intercept"}
#     ),
# ).fit()
# print(uji_model_didik.summary())

# %% [markdown]
# **Latihan 2: usia dan kinerja penjualan.** Data `data/usia_unit.csv`.
# Hipotesisnya: kinerja naik seiring usia, memuncak, lalu menurun. Pakai
# model kuadratik, lalu hitung usia puncaknya dengan rumus
# $-b_1 / (2 b_2)$.
#
# Pertanyaan: pada usia berapa kinerja mencapai puncak?

# %%
# usia = pd.read_csv("data/usia_unit.csv")
# usia["usia2"] = usia["Usia"] ** 2
# sampel_model_usia = usia[["Unit_Terjual", "Usia", "usia2"]].dropna()
# X_model_usia = sampel_model_usia[["Usia", "usia2"]]
# y_model_usia = sampel_model_usia["Unit_Terjual"]
#
# model_usia = LinearRegression()
# model_usia.fit(X_model_usia, y_model_usia)
#
# # Pelengkap statistik: standard error dan pengujian pada sampel yang sama.
# uji_model_usia = sm.OLS(
#     y_model_usia,
#     sm.add_constant(X_model_usia, has_constant="add").rename(
#         columns={"const": "Intercept"}
#     ),
# ).fit()
# print(uji_model_usia.summary())

# %% [markdown]
# **Latihan 3: jam belajar dan skor ujian.** Data `data/jam_skor.csv`.
# Ada efek jenuh: tambahan jam belajar makin kecil manfaatnya, dan ada
# batas skor maksimal. Model yang cocok: reciprocal,
# `Skor_Ujian ~ 1/X` dengan X = Jam_Belajar.
#
# Pertanyaan: berapa batas skor maksimal (asimtot) yang dibaca dari
# intersep? (Petunjuk: intersep adalah batas atas skor.)

# %%
# skor = pd.read_csv("data/jam_skor.csv")
# skor["satu_per_jam"] = 1 / skor["Jam_Belajar"]
# sampel_model_skor = skor[["Skor_Ujian", "satu_per_jam"]].dropna()
# X_model_skor = sampel_model_skor[["satu_per_jam"]]
# y_model_skor = sampel_model_skor["Skor_Ujian"]
#
# model_skor = LinearRegression()
# model_skor.fit(X_model_skor, y_model_skor)
#
# # Pelengkap statistik: standard error dan pengujian pada sampel yang sama.
# uji_model_skor = sm.OLS(
#     y_model_skor,
#     sm.add_constant(X_model_skor, has_constant="add").rename(
#         columns={"const": "Intercept"}
#     ),
# ).fit()
# print(uji_model_skor.summary())

# %% [markdown]
# **Latihan 4: pilih bentuk untuk data UTS.** Data `data/uts_1.csv`:
# pertumbuhan ekonomi, investasi, inflasi, dan keterbukaan perdagangan.
# Coba tiga bentuk: linear, log-log, dan kuadratik untuk investasi.
# Bandingkan R kuadrat terkoreksi dan p-value. Kriteria: pilih model
# dengan R kuadrat terkoreksi tertinggi di antara model yang tanda
# koefisiennya sesuai teori. Kalau dua model berdekatan, dahulukan yang
# lebih sederhana dan lebih mudah dijelaskan.

# %%
# uts1 = pd.read_csv("data/uts_1.csv")
# sampel_model_lin = uts1[
#     [
#         "Y_Pertumbuhan_Ekonomi",
#         "X1_Investasi",
#         "X2_Inflasi",
#         "X3_Keterbukaan_Perdagangan",
#     ]
# ].dropna()
# X_model_lin = sampel_model_lin[
#     ["X1_Investasi", "X2_Inflasi", "X3_Keterbukaan_Perdagangan"]
# ]
# y_model_lin = sampel_model_lin["Y_Pertumbuhan_Ekonomi"]
#
# model_lin = LinearRegression()
# model_lin.fit(X_model_lin, y_model_lin)
# ...

# %% [markdown]
# ### Selanjutnya
#
# Selanjutnya: Lab 3, uji asumsi klasik.
