# %% [markdown]
# # Hari 1, Sesi 1: Regresi Linear, dari Nol sampai Bisa Dibaca
#
# **Durasi:** 75 menit
#
# Regresi linear adalah alat utama di ekonometrika. Konsepnya sederhana: cari
# satu garis yang paling dekat dengan semua titik data, dengan "dekat" diukur
# sebagai jumlah kuadrat selisih vertikal (residual).
#
# $$Y_i = \beta_0 + \beta_1 X_{1i} + \beta_2 X_{2i} + \epsilon_i$$
#
# Materi sesi ini:
# 1. Regresi sederhana dengan scikit-learn dan pelengkap uji statistik.
# 2. Regresi berganda dan arti koefisien secara ekonomi.
# 3. Uji t, uji F, R kuadrat, dan R kuadrat terkoreksi (adjusted R2).
# 4. Prediksi dengan model.
#
# Setiap bagian punya catatan "cara menjelaskan ke mahasiswa" supaya sesi ini
# bisa langsung dipakai mengajar.

# %% [markdown]
# **Posisi dalam alur workshop.** Dari alat (Sesi 0) ke model pertama
# (Sesi 1). Di bagian 7 sesi ini model linear sengaja ditunjukkan gagal
# pada hubungan melengkung; Sesi 2 memperbaikinya.

# %% [markdown]
# ## Persiapan: pastikan data tersedia
#
# Notebook ini membaca CSV dari folder `data/`. Kalau belum ada (misalnya di
# Colab), unggah `data_tutorial.zip` lewat panel Files, lalu jalankan
# sel di bawah sekali. Di komputer sendiri, biarkan struktur folder proyek tetap utuh.

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
# ## 1. Data dan pertanyaan penelitian
#
# Kasus dari `data/uts_2.csv`: apa yang menjelaskan harga saham 50
# perusahaan? Variabel: pendapatan per saham (EPS), rasio utang terhadap
# ekuitas (DER), dan belanja iklan.
#
# Kita mulai dari satu variabel dulu: EPS. Pertanyaan sederhananya,
# "perusahaan dengan EPS lebih tinggi, apakah harga sahamnya juga lebih
# tinggi?"

# %%
import pandas as pd
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", palette=["#2F5D50", "#C15937", "#D9A441", "#5B8A8F"])
plt.rcParams.update({"figure.dpi": 110, "axes.titleweight": "bold", "font.size": 11})

saham = pd.read_csv("data/uts_2.csv")
saham = saham.rename(
    columns={
        "Y_Harga_Saham": "harga",
        "X1_Pendapatan_per_Saham": "eps",
        "X2_Rasio_Utang_Ekuitas": "der",
        "X3_Belanja_Iklan": "iklan",
    }
)
saham.head()

# %% [markdown]
# ## 2. Lihat data dulu, selalu
#
# Satu scatter plot sebelum regresi. Polanya hampir linear sempurna, sinyal
# bahwa regresi linear masuk akal untuk hubungan ini.

# %%
fig, ax = plt.subplots(figsize=(7, 4.5))
ax.scatter(saham["eps"], saham["harga"], color="#2F5D50", s=30)
ax.set_xlabel("Pendapatan per saham (EPS)")
ax.set_ylabel("Harga saham")
ax.set_title("EPS vs harga saham")
plt.show()

# %% [markdown]
# ## 3. Regresi sederhana
#
# Siapkan tabel X dan kolom y. `LinearRegression()` menyertakan intersep
# secara otomatis; `fit(X, y)` menghitung koefisien dengan metode OLS.

# %%
sampel_model1 = saham[["harga", "eps"]].dropna()
X_model1 = sampel_model1[["eps"]]
y_model1 = sampel_model1["harga"]

model1 = LinearRegression()
model1.fit(X_model1, y_model1)

koefisien_model1 = pd.Series(model1.coef_, index=X_model1.columns)
koefisien_model1.loc["Intercept"] = model1.intercept_

# Pelengkap statistik: standard error dan pengujian pada sampel yang sama.
uji_model1 = sm.OLS(
    y_model1,
    sm.add_constant(X_model1, has_constant="add").rename(
        columns={"const": "Intercept"}
    ),
).fit()
print(uji_model1.summary())

# %% [markdown]
# ### Cara membaca tabel output
#
# Tiga angka yang paling sering dipakai:
#
# - `coef` pada baris `Intercept`: nilai Y saat X = 0. Di kasus ini artinya
#   harga saham teoretis saat EPS nol. Tidak selalu masuk akal secara bisnis,
#   tapi tetap harus dilaporkan.
# - `coef` pada baris `eps`: perubahan Y untuk tambahan satu unit X.
#   Inilah jawaban dari pertanyaan penelitian.
# - `P>|t|`: p-value uji t. Jika koefisien populasi nol dan asumsi uji
#   berlaku, ini peluang memperoleh statistik uji setidaknya seekstrem
#   yang diamati. Di bawah 0,05 berarti signifikan pada taraf 5%.
#
# Kolom `R-squared` mengukur proporsi variasi Y yang diterangkan model.
# Hati-hati: data simulasi seperti `uts_2.csv` punya R kuadrat sangat tinggi
# karena dibangkitkan dari formula yang rapi. Di data riil, R kuadrat 0,3
# sampai 0,6 untuk data cross-section sudah wajar.

# %%
b0 = koefisien_model1["Intercept"]
b1 = koefisien_model1["eps"]
print(f"Intersep  : {b0:.3f}")
print(f"Slope     : {b1:.3f}")
print(f"R-squared : {model1.score(X_model1, y_model1):.3f}")
print(f"p-value eps: {uji_model1.pvalues['eps']:.3g}")

# %% [markdown]
# ### Visual: garis OLS dan residual
#
# Gambar ini memperlihatkan cara kerja OLS: garis merah adalah hasil
# estimasi, garis abu-abu adalah residual yang dikuadratkan lalu
# diminimalkan jumlahnya.

# %%
fig, ax = plt.subplots(figsize=(7, 4.5))
ax.scatter(saham["eps"], saham["harga"], color="#2F5D50", s=28, zorder=3)
xs = np.linspace(saham["eps"].min(), saham["eps"].max(), 50)
ax.plot(xs, b0 + b1 * xs, color="#C15937", lw=2, zorder=2)
# Cukup tampilkan 12 observasi agar garis residual mudah dilihat.
contoh = saham.head(12)
prediksi_contoh = pd.Series(model1.predict(contoh[["eps"]]), index=contoh.index)
ax.vlines(contoh["eps"], contoh["harga"], prediksi_contoh, color="gray", linewidth=0.9)
ax.set_xlabel("Pendapatan per saham (EPS)")
ax.set_ylabel("Harga saham")
ax.set_title(f"Harga = {b0:.1f} + {b1:.1f} x EPS")
plt.show()

# %% [markdown]
# ### Coba sendiri (5 menit)
#
# Ganti variabel penjelas dari `eps` ke `der` dan jalankan regresinya.
# Apakah `der` signifikan? Lalu, kenapa hasilnya berbeda dengan model
# berganda di bagian 6 nanti?
#
# Tulis di sel di bawah, baru buka jawabannya.

# %%
# Tulis kode Anda di sini

# %% [markdown]
# <details><summary>Lihat jawaban</summary>
#
# Sendirian, `der` tampak sangat signifikan (koefisien -131,3; p = 0,0000;
# R2 = 0,93). Tapi di model berganda (bagian 6) `der` justru tidak
# signifikan. Pelajaran: koefisien sederhana bisa menyesatkan karena
# mencampur pengaruh variabel lain, dalam hal ini EPS.
#
# </details>

# %% [markdown]
# ## 4. Arti koefisien dengan angka
#
# Dari output di atas, slope sekitar 10,4. Artinya: kenaikan EPS satu unit
# diiringi kenaikan harga saham sekitar 10,4 unit, dengan asumsi hal lain
# tidak berubah. Intersep sekitar 87,8 adalah titik potong teoretis di EPS = 0.

# %% [markdown]
# ## 5. Prediksi
#
# Prediksi adalah alasan orang membangun model. Di statsmodels, pakai
# `predict` dengan DataFrame berisi nilai X baru. Perhatikan bentuk datanya:
# harus DataFrame, bukan angka tunggal.

# %%
baru = pd.DataFrame({"eps": [15.0, 20.0, 25.0]})
baru["prediksi_harga"] = pd.Series(model1.predict(baru[["eps"]]), index=baru.index)
baru

# %% [markdown]
# Prediksi manual untuk satu nilai juga mudah: `b0 + b1 * eps`. Hasilnya
# harus sama persis dengan `model1.predict(pd.DataFrame({"eps": [15]}))`,
# selisih hanya mungkin dari pembulatan.

# %% [markdown]
# ## 6. Regresi berganda
#
# Sekarang kasusnya dilengkapi: harga saham dijelaskan EPS, DER, dan belanja
# iklan sekaligus.

# %%
sampel_model2 = saham[["harga", "eps", "der", "iklan"]].dropna()
X_model2 = sampel_model2[["eps", "der", "iklan"]]
y_model2 = sampel_model2["harga"]

model2 = LinearRegression()
model2.fit(X_model2, y_model2)

koefisien_model2 = pd.Series(model2.coef_, index=X_model2.columns)
koefisien_model2.loc["Intercept"] = model2.intercept_

# Pelengkap statistik: standard error dan pengujian pada sampel yang sama.
uji_model2 = sm.OLS(
    y_model2,
    sm.add_constant(X_model2, has_constant="add").rename(
        columns={"const": "Intercept"}
    ),
).fit()
print(uji_model2.summary())

# %% [markdown]
# ### Uji F: apakah model berguna secara keseluruhan?
#
# `Prob (F-statistic)` menguji hipotesis bahwa semua slope sama dengan nol.
# Kalau p-value kecil, setidaknya ada satu variabel yang menjelaskan Y.

# %%
print(f"F-statistic : {uji_model2.fvalue:.3f}")
print(f"Prob (F)    : {uji_model2.f_pvalue:.6g}")
print(f"R2          : {model2.score(X_model2, y_model2):.4f}")
print(f"Adj R2      : {uji_model2.rsquared_adj:.4f}")

# %% [markdown]
# ### Koefisien satu per satu
#
# Uji t di tabel output adalah uji parsial: apakah satu koefisien signifikan
# setelah variabel lain diperhitungkan. Ini berbeda dari korelasi biasa,
# karena pengaruh variabel lain sudah "dibersihkan".

# %%
tabel = pd.DataFrame(
    {
        "koefisien": koefisien_model2,
        "std_err": uji_model2.bse,
        "t": uji_model2.tvalues,
        "p_value": uji_model2.pvalues,
    }
)
tabel

# %% [markdown]
# Di data ini, EPS dan iklan signifikan, sementara DER tidak. Kenaikan DER
# satu unit berhubungan dengan kenaikan harga 2,94 unit, tapi p-value 0,48
# artinya angka itu belum bisa dibedakan dari nol secara statistik.

# %% [markdown]
# ### Coba sendiri (5 menit)
#
# Pakai `model2` (harga ~ eps + der + iklan). Prediksi harga untuk
# EPS = 18, DER = 1,5, dan belanja iklan = 60.
#
# Tulis di sel di bawah, baru buka jawabannya.

# %%
# Tulis kode Anda di sini

# %% [markdown]
# <details><summary>Lihat jawaban</summary>
#
# `model2.predict(pd.DataFrame({"eps": [18], "der": [1.5], "iklan": [60]}))`
# menghasilkan sekitar 275,6.
#
# </details>

# %% [markdown]
# ## 7. Kapan garis lurus tidak cukup
#
# Coba regresikan penjualan pada biaya iklan memakai `regresi_polinom.csv`.
# Hubungannya melengkung, dan model linear gagal total: R kuadrat hanya
# sekitar 0,007 dan slope tidak signifikan. Ini bukan alasan untuk menyerah,
# tapi tanda bahwa bentuk fungsionalnya perlu diganti. Itu topik Sesi 2.

# %%
iklan = pd.read_csv("data/regresi_polinom.csv")
iklan = iklan.rename(columns={"Biaya Iklan (X)": "iklan", "Penjualan (Y)": "penjualan"})
sampel_model_salah = iklan[["penjualan", "iklan"]].dropna()
X_model_salah = sampel_model_salah[["iklan"]]
y_model_salah = sampel_model_salah["penjualan"]

model_salah = LinearRegression()
model_salah.fit(X_model_salah, y_model_salah)

prediksi_model_salah = pd.Series(
    model_salah.predict(X_model_salah), index=y_model_salah.index
)

# Pelengkap statistik: standard error dan pengujian pada sampel yang sama.
uji_model_salah = sm.OLS(
    y_model_salah,
    sm.add_constant(X_model_salah, has_constant="add").rename(
        columns={"const": "Intercept"}
    ),
).fit()
print(f"R2 linear  : {model_salah.score(X_model_salah, y_model_salah):.4f}")
print(f"p-value iklan: {uji_model_salah.pvalues['iklan']:.3f}")

fig, ax = plt.subplots(figsize=(7, 4.5))
ax.scatter(iklan["iklan"], iklan["penjualan"], color="#2F5D50", s=26)
ax.plot(iklan["iklan"], prediksi_model_salah, color="#C15937", lw=1.5)
ax.set_xlabel("Biaya iklan")
ax.set_ylabel("Penjualan")
ax.set_title("Model linear pada hubungan yang melengkung")
plt.show()

# %% [markdown]
# ## 8. Catatan mengajar: tiga kesalahan yang paling sering muncul
#
# **Satu, menafsirkan intersep tanpa berpikir.** "Harga saham 87,8 padahal
# EPS nol" sering diucapkan seolah itu temuan. Intersep hanya berguna kalau
# X = 0 masuk akal secara ekonomi.
#
# **Dua, menyamakan R kuadrat tinggi dengan model benar.** Model dengan R
# kuadrat 0,95 bisa saja salah spesifikasi, misalnya karena tren palsu
# (spurious regression) pada data deret waktu. Ingat sesi 5.
#
# **Tiga, lupa satuan.** Koefisien 10,4 pada EPS diukur dalam satuan Y per
# satuan X. Kalau Y rupiah dan X persen, 10,4 berarti 10,4 rupiah per satu
# persen, bukan per 0,01 persen.
#
# Satu lagi yang sering luput: koefisien bersifat *ceteris paribus*, bukan
# pengaruh kausal. Bilang "berhubungan dengan" kecuali desain penelitiannya
# memang memungkinkan klaim kausal.

# %% [markdown]
# ## Latihan
#
# 1. Regresikan `produktivitas padi` pada pupuk, curah hujan, dan sinar
#    matahari (`uts_3.csv`). Laporkan koefisien, p-value, dan R kuadrat.
# 2. Prediksi produktivitas kalau pupuk 160, curah hujan 1900, sinar 230.
# 3. Setelah model Latihan 1 jadi (variabel `model_padi`), uji apakah
#    pupuk dan sinar matahari bersama-sama signifikan:
#    `model_padi.f_test("X1_Jumlah_Pupuk = 0, X3_Sinar_Matahari = 0")`.
#
# Kunci dan interpretasi ada di `pengajar/kunci_jawaban/catatan_latihan.md`.

# %% [markdown]
# ### Selanjutnya
#
# Selanjutnya: Sesi 2 menambal celah yang terlihat di bagian 7, yaitu
# model linear pada hubungan melengkung.
