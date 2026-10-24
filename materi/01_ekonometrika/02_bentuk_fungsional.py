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
# Colab), unggah `data_tutorial.zip` lewat panel Files, lalu jalankan
# sel di bawah sekali.

# %% [markdown]
# **Posisi dalam alur workshop.** Melanjutkan Sesi 1 yang berakhir dengan
# model linear yang gagal. Setelah bentuk model tepat, Sesi 3 memeriksa
# kelayakan asumsinya.

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

# %% [markdown]
# ## Kasus 1: Fungsi produksi Cobb-Douglas (log-log)
#
# Data 30 observasi tenaga kerja (L), modal (K), dan produksi (Q) dari
# `regresi_log.csv`. Model yang diuji: $Q = A L^{\beta_1} K^{\beta_2}$.
# Setelah di-log, bentuknya linear dan koefisiennya elastisitas.

# %% [markdown]
# <!-- kamus_variabel:regresi_log.csv -->
#
# ### Kenali data: Produksi, tenaga kerja, dan modal
#
# **Data:** `data/regresi_log.csv`. **Satu baris:** satu unit usaha/pengamatan dalam contoh produksi.
#
# Nama singkat di kode berasal dari penggantian nama kolom CSV; isi angkanya tetap sama.
#
# | Kolom CSV | Nama di kode | Pengertian | Satuan atau kode | Peran |
# |---|---|---|---|---|
# | `Observasi ke-` | `obs` | Nomor urut pengamatan. | Nomor identitas | Penanda, bukan besaran ekonomi |
# | `Tenaga Kerja (L)` | `L` | Input tenaga kerja untuk proses produksi (L = labor). | Jumlah tenaga kerja; cakupan waktu tidak dirinci | X: penjelas |
# | `Modal (K)` | `K` | Input modal yang digunakan untuk menghasilkan barang (K = capital). | Satuan/skala tidak dirinci sumber | X: penjelas |
# | `Produksi (Q)` | `Q` | Jumlah hasil produksi (Q = quantity/output). | Jumlah output; unit produk tidak dirinci | Y: target |
#
# Kolom turunan berikut dibuat saat praktik; kolom ini belum ada pada CSV awal.
#
# | Kolom turunan | Pengertian | Satuan/kode |
# |---|---|---|
# | `lnQ` | Logaritma alami dari produksi Q. | Skala logaritma |
# | `lnL` | Logaritma alami dari tenaga kerja L. | Skala logaritma |
# | `lnK` | Logaritma alami dari modal K. | Skala logaritma |
#
# Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

# %%
import pandas as pd
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", palette=["#2F5D50", "#C15937", "#D9A441", "#5B8A8F"])
plt.rcParams.update({"figure.dpi": 110, "axes.titleweight": "bold", "font.size": 11})

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
produksi.head()

# %%
sampel_model_cd = produksi[["lnQ", "lnL", "lnK"]].dropna()
X_model_cd = sampel_model_cd[["lnL", "lnK"]]
y_model_cd = sampel_model_cd["lnQ"]

model_cd = LinearRegression()
model_cd.fit(X_model_cd, y_model_cd)

koefisien_model_cd = pd.Series(model_cd.coef_, index=X_model_cd.columns)
koefisien_model_cd.loc["Intercept"] = model_cd.intercept_

# Pelengkap statistik: standard error dan pengujian pada sampel yang sama.
uji_model_cd = sm.OLS(
    y_model_cd,
    sm.add_constant(X_model_cd, has_constant="add").rename(
        columns={"const": "Intercept"}
    ),
).fit()
print(uji_model_cd.summary())

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
b_L = koefisien_model_cd["lnL"]
b_K = koefisien_model_cd["lnK"]
print(f"Elastisitas tenaga kerja : {b_L:.4f}")
print(f"Elastisitas modal        : {b_K:.4f}")
print(f"Jumlah (skala)           : {b_L + b_K:.4f}")

# Uji gabungan: apakah skalanya tepat 1?
print(uji_model_cd.f_test("lnL + lnK = 1"))

# %% [markdown]
# ### Catatan untuk mengajar
#
# Pada model log-lin (ln Y dijelaskan X), aproksimasi "100 x beta persen"
# cukup akurat untuk beta kecil. Untuk
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
# `regresi_reciprocal.csv`. Hubungan yang diduga: makin berpengalaman,
# waktu produksi makin pendek, tapi perbaikannya mengecil dan mendekati
# batas tertentu.
#
# $$Y = \beta_0 + \beta_1 \left(\frac{1}{X}\right)$$
#
# Kalau X membesar, $1/X$ mendekati nol, jadi Y mendekati $\beta_0$. Nilai
# $\beta_0$ adalah batas waktu produksi teoretis yang tidak bisa dilewati.

# %% [markdown]
# <!-- kamus_variabel:regresi_reciprocal.csv -->
#
# ### Kenali data: Pengalaman dan waktu produksi
#
# **Data:** `data/regresi_reciprocal.csv`. **Satu baris:** satu pengamatan pengalaman pekerja dan waktu produksinya.
#
# Nama singkat di kode berasal dari penggantian nama kolom CSV; isi angkanya tetap sama.
#
# | Kolom CSV | Nama di kode | Pengertian | Satuan atau kode | Peran |
# |---|---|---|---|---|
# | `Pengalaman (X)` | `pengalaman` | Lama/pengalaman melakukan pekerjaan produksi. | Satuan pengalaman tidak dirinci sumber | X: penjelas |
# | `Waktu Produksi (Y)` | `waktu` | Waktu yang diperlukan untuk menyelesaikan produksi. | Satuan waktu tidak dirinci sumber | Y: target |
#
# Kolom turunan berikut dibuat saat praktik; kolom ini belum ada pada CSV awal.
#
# | Kolom turunan | Pengertian | Satuan/kode |
# |---|---|---|
# | `satu_per_x` | Kebalikan pengalaman: 1 / pengalaman. | Kebalikan satuan pengalaman |
#
# Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

# %%
recip = pd.read_csv("data/regresi_reciprocal.csv")
recip = recip.rename(
    columns={"Pengalaman (X)": "pengalaman", "Waktu Produksi (Y)": "waktu"}
)
recip["satu_per_x"] = 1 / recip["pengalaman"]
sampel_model_r = recip[["waktu", "satu_per_x"]].dropna()
X_model_r = sampel_model_r[["satu_per_x"]]
y_model_r = sampel_model_r["waktu"]

model_r = LinearRegression()
model_r.fit(X_model_r, y_model_r)

koefisien_model_r = pd.Series(model_r.coef_, index=X_model_r.columns)
koefisien_model_r.loc["Intercept"] = model_r.intercept_

# Pelengkap statistik: standard error dan pengujian pada sampel yang sama.
uji_model_r = sm.OLS(
    y_model_r,
    sm.add_constant(X_model_r, has_constant="add").rename(
        columns={"const": "Intercept"}
    ),
).fit()
print(uji_model_r.summary())

# %%
b0r = koefisien_model_r["Intercept"]
b1r = koefisien_model_r["satu_per_x"]

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

# %% [markdown]
# <!-- kamus_variabel:regresi_polinom.csv -->
#
# ### Kenali data: Iklan dan penjualan
#
# **Data:** `data/regresi_polinom.csv`. **Satu baris:** satu tahun pengamatan pada contoh latihan.
#
# Nama singkat di kode berasal dari penggantian nama kolom CSV; isi angkanya tetap sama.
#
# | Kolom CSV | Nama di kode | Pengertian | Satuan atau kode | Peran |
# |---|---|---|---|---|
# | `Tahun ke-` | `Tahun ke-` | Urutan tahun pengamatan, bukan tahun kalender. | 1, 2, 3, dan seterusnya | Penanda waktu |
# | `Biaya Iklan (X)` | `iklan` | Biaya yang dikeluarkan untuk memasang iklan. | Satuan/skala tidak dirinci sumber | X: penjelas |
# | `Penjualan (Y)` | `penjualan` | Besarnya penjualan yang ingin dijelaskan oleh biaya iklan. | Satuan/skala tidak dirinci sumber | Y: target |
#
# Jangan menetapkan rupiah, juta rupiah, atau unit barang hanya dari besar angkanya; skala tersebut tidak dicantumkan pada sumber tabel.
#
# Kolom turunan berikut dibuat saat praktik; kolom ini belum ada pada CSV awal.
#
# | Kolom turunan | Pengertian | Satuan/kode |
# |---|---|---|
# | `iklan2` | Kuadrat biaya iklan: iklan × iklan; bukan biaya iklan baru. | Kuadrat satuan iklan |
#
# Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

# %%
polinom = pd.read_csv("data/regresi_polinom.csv")
polinom = polinom.rename(
    columns={"Biaya Iklan (X)": "iklan", "Penjualan (Y)": "penjualan"}
)
polinom["iklan2"] = polinom["iklan"] ** 2

# Regresi yang sama dengan `model_salah` di Sesi 1; di sini dipakai
# sebagai pembanding model polinomial
sampel_model_lin = polinom[["penjualan", "iklan"]].dropna()
X_model_lin = sampel_model_lin[["iklan"]]
y_model_lin = sampel_model_lin["penjualan"]

model_lin = LinearRegression()
model_lin.fit(X_model_lin, y_model_lin)

koefisien_model_lin = pd.Series(model_lin.coef_, index=X_model_lin.columns)
koefisien_model_lin.loc["Intercept"] = model_lin.intercept_

# Pelengkap statistik: standard error dan pengujian pada sampel yang sama.
uji_model_lin = sm.OLS(
    y_model_lin,
    sm.add_constant(X_model_lin, has_constant="add").rename(
        columns={"const": "Intercept"}
    ),
).fit()
sampel_model_poli = polinom[["penjualan", "iklan", "iklan2"]].dropna()
X_model_poli = sampel_model_poli[["iklan", "iklan2"]]
y_model_poli = sampel_model_poli["penjualan"]

model_poli = LinearRegression()
model_poli.fit(X_model_poli, y_model_poli)

koefisien_model_poli = pd.Series(model_poli.coef_, index=X_model_poli.columns)
koefisien_model_poli.loc["Intercept"] = model_poli.intercept_

# Pelengkap statistik: standard error dan pengujian pada sampel yang sama.
uji_model_poli = sm.OLS(
    y_model_poli,
    sm.add_constant(X_model_poli, has_constant="add").rename(
        columns={"const": "Intercept"}
    ),
).fit()

print(f"Adj R2 linear    : {uji_model_lin.rsquared_adj:.4f}")
print(f"Adj R2 polinomial: {uji_model_poli.rsquared_adj:.4f}")
print(
    f"Koefisien X2     : {koefisien_model_poli['iklan2']:.4f} "
    f"(p = {uji_model_poli.pvalues['iklan2']:.4f})"
)

# %%
b1p = koefisien_model_poli["iklan"]
b2p = koefisien_model_poli["iklan2"]
# Pada data ini koefisien kuadrat negatif, sehingga titik balik adalah puncak.
puncak = -b1p / (2 * b2p)
print(f"Titik puncak pada X = {puncak:.2f}")

fig, ax = plt.subplots(figsize=(7, 4.5))
ax.scatter(polinom["iklan"], polinom["penjualan"], color="#2F5D50", s=26)
xs = np.linspace(polinom["iklan"].min(), polinom["iklan"].max(), 100)
ax.plot(
    xs,
    koefisien_model_lin["Intercept"] + koefisien_model_lin["iklan"] * xs,
    color="gray",
    lw=1.5,
    label="linear",
)
ax.plot(
    xs,
    koefisien_model_poli["Intercept"] + b1p * xs + b2p * xs**2,
    color="#C15937",
    lw=2,
    label="kuadratik",
)
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

# %% [markdown]
# <!-- kamus_variabel:usia_unit.csv -->
#
# ### Kenali data: Usia dan kinerja penjual
#
# **Data:** `data/usia_unit.csv`. **Satu baris:** satu tenaga penjual.
#
# Nama singkat di kode berasal dari penggantian nama kolom CSV; isi angkanya tetap sama.
#
# | Kolom CSV | Nama di kode | Pengertian | Satuan atau kode | Peran |
# |---|---|---|---|---|
# | `Usia` | `usia` | Umur tenaga penjual. | Tahun | X: penjelas |
# | `Unit_Terjual` | `unit` | Jumlah penjualan bulanan pada contoh kinerja penjual. | Unit per bulan, berupa angka simulasi | Y: target |
#
# Kolom turunan berikut dibuat saat praktik; kolom ini belum ada pada CSV awal.
#
# | Kolom turunan | Pengertian | Satuan/kode |
# |---|---|---|
# | `usia2` | Kuadrat usia: usia × usia. | Tahun kuadrat |
#
# Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

# %%
usia = pd.read_csv("data/usia_unit.csv")
usia = usia.rename(columns={"Usia": "usia", "Unit_Terjual": "unit"})
usia["usia2"] = usia["usia"] ** 2

sampel_model_usia = usia[["unit", "usia", "usia2"]].dropna()
X_model_usia = sampel_model_usia[["usia", "usia2"]]
y_model_usia = sampel_model_usia["unit"]

model_usia = LinearRegression()
model_usia.fit(X_model_usia, y_model_usia)

koefisien_model_usia = pd.Series(model_usia.coef_, index=X_model_usia.columns)
koefisien_model_usia.loc["Intercept"] = model_usia.intercept_

# Pelengkap statistik: standard error dan pengujian pada sampel yang sama.
uji_model_usia = sm.OLS(
    y_model_usia,
    sm.add_constant(X_model_usia, has_constant="add").rename(
        columns={"const": "Intercept"}
    ),
).fit()
print(uji_model_usia.summary())

# %%
ba = koefisien_model_usia["usia"]
bb = koefisien_model_usia["usia2"]
print(f"Usia puncak = {(-ba / (2 * bb)):.2f} tahun")

# %% [markdown]
# Usia puncaknya sekitar 40 tahun, cocok dengan hipotesis di soal. Perhatikan
# `usia2` bernilai negatif: itulah yang membuat kurvanya melengkung ke bawah.

# %% [markdown]
# ### Coba sendiri (5 menit)
#
# Data `data/jam_skor.csv` punya efek jenuh. Jalankan model reciprocal
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
# 3. Data `regresi_log.csv`: uji apakah model skala tetap ditolak. Pakai
#    hasil `f_test` yang sudah dijalankan.

# %% [markdown]
# ### Selanjutnya
#
# Selanjutnya: Sesi 3 memeriksa apakah model sudah memenuhi asumsi klasik.
