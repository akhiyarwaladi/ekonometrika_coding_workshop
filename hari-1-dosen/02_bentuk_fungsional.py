# %% [markdown]
# # Hari 1, Sesi 2: Bentuk Fungsional Model Regresi
#
# **Durasi:** 75 menit
#
# Hubungan ekonomi jarang berbentuk garis lurus. Sesi ini membahas lima bentuk
# fungsional yang muncul terus di perkuliahan, lengkap dengan cara menafsirkan
# koefisiennya.
#
# | Bentuk | Persamaan | Makna koefisien |
# |---|---|---|
# | Linear | $Y = \beta_0 + \beta_1 X$ | tambahan 1 unit X menaikkan Y sebesar $\beta_1$ unit |
# | Log-lin | $\ln Y = \beta_0 + \beta_1 X$ | tambahan 1 unit X menaikkan Y sekitar $100\beta_1$ persen |
# | Lin-log | $Y = \beta_0 + \beta_1 \ln X$ | kenaikan X 1 persen menaikkan Y sebesar $\beta_1/100$ unit |
# | Log-log | $\ln Y = \beta_0 + \beta_1 \ln X$ | elastisitas: kenaikan X 1 persen menaikkan Y $\beta_1$ persen |
# | Reciprocal | $Y = \beta_0 + \beta_1 \frac{1}{X}$ | efek mengecil saat X membesar, ada batas asimtot $\beta_0$ |
# | Polinomial | $Y = \beta_0 + \beta_1 X + \beta_2 X^2$ | bisa naik lalu turun, ada titik puncak |
#
# ## Persiapan: pastikan data tersedia
#
# Notebook ini membaca CSV dari folder `data/`. Kalau belum ada (misalnya di
# Colab), unggah `data-ekonometrika.zip` lewat panel Files, lalu jalankan
# sel di bawah sekali.

# %% [markdown]
# **Posisi dalam alur workshop.** Melanjutkan Sesi 1 yang berakhir dengan
# model linear yang gagal. Setelah bentuk model tepat, Sesi 3 memeriksa
# kelayakan asumsinya.

# %%
import zipfile
from pathlib import Path

if not Path("data").exists() and Path("data-ekonometrika.zip").exists():
    zipfile.ZipFile("data-ekonometrika.zip").extractall(".")

jumlah = len(list(Path("data").glob("*.csv")))
print(f"{jumlah} file data siap dipakai dari folder data/")
if jumlah == 0:
    print("Folder data/ kosong. Unggah data-ekonometrika.zip dulu, lalu jalankan sel ini lagi.")

# %% [markdown]
# ## Kasus 1: Fungsi produksi Cobb-Douglas (log-log)
#
# Data 30 observasi tenaga kerja (L), modal (K), dan produksi (Q) dari
# `regresi-log.csv`. Model yang diuji: $Q = A L^{\beta_1} K^{\beta_2}$.
# Setelah di-log, bentuknya linear dan koefisiennya elastisitas.

# %%
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", palette=["#2F5D50", "#C15937", "#D9A441", "#5B8A8F"])
plt.rcParams.update({"figure.dpi": 110, "axes.titleweight": "bold", "font.size": 11})

produksi = pd.read_csv("data/regresi-log.csv").rename(columns={
    "Observasi ke-": "obs", "Tenaga Kerja (L)": "L", "Modal (K)": "K",
    "Produksi (Q)": "Q"})
produksi["lnQ"] = np.log(produksi["Q"])
produksi["lnL"] = np.log(produksi["L"])
produksi["lnK"] = np.log(produksi["K"])
produksi.head()

# %%
model_cd = smf.ols("lnQ ~ lnL + lnK", data=produksi).fit()
print(model_cd.summary())

# %% [markdown]
# Baca koefisien `lnL` dan `lnK` sebagai elastisitas. Kalau `lnL` = 0,6,
# tambahan tenaga kerja 1 persen menaikkan produksi sekitar 0,6 persen.
#
# Jumlah kedua elastisitas menentukan skala pengembalian (returns to scale):
#
# - $\beta_1 + \beta_2 = 1$: skala tetap (constant returns to scale)
# - $> 1$: skala meningkat
# - $< 1$: skala menurun

# %%
b_L = model_cd.params["lnL"]
b_K = model_cd.params["lnK"]
print(f"Elastisitas tenaga kerja : {b_L:.4f}")
print(f"Elastisitas modal        : {b_K:.4f}")
print(f"Jumlah (skala)           : {b_L + b_K:.4f}")

# Uji gabungan: apakah skalanya tepat 1?
print(model_cd.f_test("lnL + lnK = 1"))

# %% [markdown]
# ### Catatan untuk mengajar
#
# Aproksimasi "100 x beta persen" cukup akurat untuk beta kecil, tapi untuk
# beta di atas 0,15 lebih baik pakai rumus eksak $100(e^{\beta} - 1)$.
# Contoh: beta = 0,25. Aproksimasi bilang 25 persen, eksak 28,4 persen.
# Sebutkan ini sekali saja, jangan sampai mahasiswa tersesat di detail.

# %%
beta = 0.25
print(f"Aproksimasi 100*beta     : {100 * beta:.2f} persen")
print(f"Eksak 100*(exp(beta)-1)  : {100 * (np.exp(beta) - 1):.2f} persen")


# %% [markdown]
# ### Coba sendiri (5 menit)
#
# Menurut model log-log di atas, kalau modal naik 10 persen, berapa
# persen produksi diperkirakan naik? (Kalikan elastisitasnya.)
#
# Tulis di sel di bawah, baru buka jawabannya.

# %%
# Tulis jawaban singkat Anda di sini

# %% [markdown]
# <details><summary>Lihat jawaban</summary>
#
# Elastisitas modal 0,6093, jadi kenaikan 10 persen modal berhubungan
# dengan kenaikan produksi sekitar 6,1 persen, ceteris paribus.
#
# </details>

# %% [markdown]
# ## Kasus 2: Regresi reciprocal
#
# Data pengalaman kerja (X) dan waktu produksi (Y) dari
# `regresi-reciprocal.csv`. Hubungan yang diduga: makin berpengalaman,
# waktu produksi makin pendek, tapi perbaikannya mengecil dan mendekati
# batas tertentu.
#
# $$Y = \beta_0 + \beta_1 \left(\frac{1}{X}\right)$$
#
# Kalau X membesar, $1/X$ mendekati nol, jadi Y mendekati $\beta_0$. Nilai
# $\beta_0$ adalah batas waktu produksi teoretis yang tidak bisa dilewati.

# %%
recip = pd.read_csv("data/regresi-reciprocal.csv").rename(columns={
    "Pengalaman (X)": "pengalaman", "Waktu Produksi (Y)": "waktu"})
recip["satu_per_x"] = 1 / recip["pengalaman"]
model_r = smf.ols("waktu ~ satu_per_x", data=recip).fit()
print(model_r.summary())

# %%
b0r = model_r.params["Intercept"]
b1r = model_r.params["satu_per_x"]

fig, ax = plt.subplots(figsize=(7, 4.5))
ax.scatter(recip["pengalaman"], recip["waktu"], color="#2F5D50", s=26)
xs = np.linspace(recip["pengalaman"].min(), recip["pengalaman"].max(), 100)
ax.plot(xs, b0r + b1r / xs, color="#C15937", lw=2)
ax.axhline(b0r, color="gray", ls="--", lw=1)
ax.text(xs.max() * 0.55, b0r + 0.6, f"Batas asimtot = {b0r:.2f}")
ax.set_xlabel("Pengalaman (tahun)")
ax.set_ylabel("Waktu produksi")
plt.show()

# %% [markdown]
# ## Kasus 3: Regresi polinomial
#
# Kasus yang sama seperti sesi 1 (biaya iklan dan penjualan), tapi sekarang
# kita curiga ada titik jenuh: iklan menambah penjualan, tapi lama-lama
# tambahannya berkurang, lalu berbalik menurun.
#
# Model: $\text{penjualan} = \beta_0 + \beta_1 X + \beta_2 X^2$.
# Titik puncak berada di $X^* = -\beta_1 / (2\beta_2)$.

# %%
polinom = pd.read_csv("data/regresi-polinom.csv").rename(columns={
    "Biaya Iklan (X)": "iklan", "Penjualan (Y)": "penjualan"})
polinom["iklan2"] = polinom["iklan"] ** 2

# Regresi yang sama dengan `model_salah` di Sesi 1; di sini dipakai
# sebagai pembanding model polinomial
model_lin = smf.ols("penjualan ~ iklan", data=polinom).fit()
model_poli = smf.ols("penjualan ~ iklan + iklan2", data=polinom).fit()

print(f"Adj R2 linear    : {model_lin.rsquared_adj:.4f}")
print(f"Adj R2 polinomial: {model_poli.rsquared_adj:.4f}")
print(f"Koefisien X2     : {model_poli.params['iklan2']:.4f} "
      f"(p = {model_poli.pvalues['iklan2']:.4f})")

# %%
b1p = model_poli.params["iklan"]
b2p = model_poli.params["iklan2"]
puncak = -b1p / (2 * b2p) if b2p != 0 else np.nan
print(f"Titik puncak pada X = {puncak:.2f}")

fig, ax = plt.subplots(figsize=(7, 4.5))
ax.scatter(polinom["iklan"], polinom["penjualan"], color="#2F5D50", s=26)
xs = np.linspace(polinom["iklan"].min(), polinom["iklan"].max(), 100)
ax.plot(xs, model_lin.params["Intercept"] + model_lin.params["iklan"] * xs,
        color="gray", lw=1.5, label="linear")
ax.plot(xs, model_poli.params["Intercept"] + b1p * xs + b2p * xs**2,
        color="#C15937", lw=2, label="kuadratik")
ax.axvline(puncak, color="#D9A441", ls=":", lw=1.5)
ax.legend()
ax.set_xlabel("Biaya iklan")
ax.set_ylabel("Penjualan")
plt.show()

# %% [markdown]
# ## Contoh soal dari halaman kuliah: usia dan kinerja penjualan
#
# Hipotesis di materi Pertemuan 3: kinerja naik seiring usia, memuncak di
# usia tertentu, lalu menurun. Model kuadratik adalah jawaban standarnya.

# %%
usia = pd.DataFrame({
    "usia": [23, 25, 28, 30, 32, 34, 36, 38, 40, 41, 42, 43, 44, 45, 46,
             47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61],
    "unit": [52.1, 58.8, 66.9, 71.5, 75.1, 77.8, 79.9, 81.2, 82.0, 81.9,
             81.5, 80.8, 79.9, 78.5, 77.1, 75.4, 73.6, 71.5, 69.1, 66.5,
             63.8, 60.9, 57.8, 54.5, 51.1, 47.5, 43.8, 39.9, 35.9, 31.7],
})
usia["usia2"] = usia["usia"] ** 2

model_usia = smf.ols("unit ~ usia + usia2", data=usia).fit()
print(model_usia.summary())

# %%
ba = model_usia.params["usia"]
bb = model_usia.params["usia2"]
print(f"Usia puncak = {(-ba / (2 * bb)):.2f} tahun")

# %% [markdown]
# Usia puncaknya sekitar 40 tahun, cocok dengan hipotesis di soal. Perhatikan
# `usia2` bernilai negatif: itulah yang membuat kurvanya melengkung ke bawah.


# %% [markdown]
# ### Coba sendiri (5 menit)
#
# Data `data/jam-skor.csv` punya efek jenuh. Jalankan model reciprocal
# `Skor_Ujian ~ 1/Jam_Belajar`, lalu sebutkan batas skor maksimalnya.
#
# Tulis di sel di bawah, baru buka jawabannya.

# %%
# Tulis kode Anda di sini

# %% [markdown]
# <details><summary>Lihat jawaban</summary>
#
# Intersep (asimtot) = 99,73. Skor mendekati 100 tapi tidak pernah
# melewatinya; itulah bentuk khas reciprocal.
#
# </details>

# %% [markdown]
# ## Cara memilih bentuk fungsional
#
# Urutannya: teori dulu, data kemudian.
#
# 1. Tanya dulu hubungan ekonominya seperti apa. Elastisitas konstan? Pakai
#    log-log. Ada titik jenuh? Pakai kuadratik atau reciprocal.
# 2. Baru bandingkan kecocokan. R kuadrat hanya boleh dibandingkan kalau
#    variabel Y-nya sama. Log-lin dan linear tidak bisa dibanding R kuadrat
#    langsung, karena Y-nya beda skala.
# 3. Periksa pola residual. Kalau residual membentuk lengkungan, model linear
#    kemungkinan kurang tepat.
# 4. Ingat batas praktis: log tidak bisa dipakai kalau ada nilai nol atau
#    negatif.

# %% [markdown]
# ## Latihan
#
# 1. Regresikan `waktu` pada `1/pengalaman` dan hitung prediksi untuk
#    pengalaman 6 bulan. Apa arti batas asimtot di kasus ini?
# 2. Pada model usia di atas, bandingkan R kuadrat terkoreksi model
#    kuadratik dengan model linear (`unit ~ usia`). Apakah tambahan `usia2`
#    sepadan?
# 3. Data `regresi-log.csv`: uji apakah model skala tetap ditolak. Pakai
#    hasil `f_test` yang sudah dijalankan.

# %% [markdown]
# ### Selanjutnya
#
# Selanjutnya: Sesi 3 memeriksa apakah model sudah memenuhi asumsi klasik.
