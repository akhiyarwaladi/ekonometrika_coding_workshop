# %% [markdown]
# # Lab 0: Mulai dari Nol di Google Colab
#
# **Durasi:** 30 sampai 45 menit
#
# Lab ini membawa Anda dari nol sampai regresi pertama. Tidak perlu
# pengalaman Python sebelumnya. Semua yang dibutuhkan sudah disiapkan.
#
# Cara kerja di Colab:
# 1. Klik sel (kotak abu-abu berisi kode).
# 2. Tekan `Shift + Enter` untuk menjalankan.
# 3. Hasilnya muncul di bawah sel.
#
# **Data.** Semua data ada di folder `data/`. Kalau belum ada (misalnya saat
# pertama kali membuka di Colab), unggah `data-ekonometrika.zip` lewat panel
# Files di kiri layar, lalu jalankan sel pertama di bawah sekali.

# %% [markdown]
# **Posisi dalam alur workshop.** Lab 0 sampai 5 mengikuti urutan Hari 1
# (Sesi 1 sampai 5). Lab 6 menutup dengan data Indonesia asli.

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
# ## 1. Senjata yang dipakai
#
# Lima baris impor di bawah ini muncul di hampir semua analisis:
# pandas untuk tabel, numpy untuk angka, statsmodels untuk regresi,
# matplotlib dan seaborn untuk grafik.

# %%
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", palette=["#2F5D50", "#C15937", "#D9A441", "#5B8A8F"])
plt.rcParams.update({"figure.dpi": 110, "axes.titleweight": "bold", "font.size": 11})

# %% [markdown]
# ## 2. Baca data pertama
#
# Satu baris perintah: `pd.read_csv("data/uts-2.csv")`. Fungsi `head()`
# menampilkan 5 baris pertama supaya kita tahu isinya.

# %%
saham = pd.read_csv("data/uts-2.csv")
saham.head()

# %% [markdown]
# ## 3. Grafik pertama
#
# Selalu lihat data sebelum menghitung. Kita pakai scatter plot sederhana.

# %%
sns.scatterplot(data=saham, x="X1_Pendapatan_per_Saham", y="Y_Harga_Saham")
plt.title("Pendapatan per saham vs harga saham")
plt.xlabel("EPS")
plt.ylabel("Harga saham")
plt.show()

# %% [markdown]
# ## 4. Regresi pertama
#
# Rumus regresi ditulis `y ~ x`. Bagian kiri tilde adalah variabel yang
# dijelaskan, bagian kanan adalah penjelasnya. `fit()` yang menaksir model.
#
# Pertanyaan: apakah EPS berhubungan dengan harga saham?

# %%
model = smf.ols("Y_Harga_Saham ~ X1_Pendapatan_per_Saham", data=saham).fit()
print(model.summary())

# %% [markdown]
# Tiga angka yang dibaca:
#
# - `coef` baris pertama: intersep, nilai Y kalau X = 0.
# - `coef` baris kedua: kemiringan, perubahan Y per satu unit X.
# - `P>|t|` baris kedua: kalau di bawah 0,05, hubungannya signifikan.
#
# **Cara membaca hasilnya:** kenaikan EPS satu unit diiringi kenaikan harga
# saham sekitar 10,4 unit, dan hubungan itu signifikan (p-value jauh di
# bawah 0,05).

# %%
print("Koefisien:")
print(model.params.round(3))
print()
print("R-squared:", round(model.rsquared, 3))


# %% [markdown]
# ### Coba sendiri (5 menit)
#
# Pakai `model` yang sudah jadi. Prediksi harga saham untuk EPS = 25.
#
# Tulis di sel di bawah, baru buka jawabannya.

# %%
# Tulis kode Anda di sini

# %% [markdown]
# <details><summary>Lihat jawaban</summary>
#
# `model.predict(pd.DataFrame({"X1_Pendapatan_per_Saham": [25]}))`
# menghasilkan sekitar 348,1.
#
# </details>

# %% [markdown]
# ## 5. Latihan
#
# 1. Baca `data/uts-4.csv` ke variabel `harapan_hidup`. Tampilkan 5 baris
#    pertama.
# 2. Hitung rata-rata kolom `Y_Angka_Harapan_Hidup` dan `X2_Tingkat_Imunisasi`
#    dengan `.mean()`.
# 3. Jalankan regresi `Y_Angka_Harapan_Hidup ~ X1_Pengeluaran_Kesehatan`.
#    Apakah koefisiennya signifikan?

# %%
# Tulis jawaban Anda di sini.
# harapan_hidup = pd.read_csv(...)
# harapan_hidup.head()
# ...

# %% [markdown]
# ### Selanjutnya
#
# Selanjutnya: Lab 1, regresi linear lengkap.
