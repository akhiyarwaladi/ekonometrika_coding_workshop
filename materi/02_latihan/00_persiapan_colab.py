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
# **Data.** Jalankan sel alamat data di bawah. `URL_DATA` menyimpan alamat folder CSV di GitHub;
# `pd.read_csv(...)` membaca tabel sesuai nama CSV pada sel kode berikutnya.
# Gunakan koneksi internet dan jalankan sel berurutan dengan **Shift + Enter**.

# %% [markdown]
# **Posisi dalam alur workshop.** Lab 0 sampai 5 mengikuti urutan Hari 1
# (Sesi 1 sampai 5). Lab 6 menutup dengan data Indonesia asli.

# %% [markdown]
# ## Cara mengikuti notebook ini
#
# Jalankan sel berurutan dengan `Shift + Enter`. Setiap notebook dapat
# dimulai sendiri dengan koneksi internet yang aktif. Sel persiapan cukup dijalankan
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
URL_DATA = "https://raw.githubusercontent.com/akhiyarwaladi/ekonometrika_coding_workshop/main/data/"

print("Alamat data siap. Jalankan sel pembacaan CSV berikutnya.")

# %% [markdown]
# ## 1. Senjata yang dipakai
#
# Lima baris impor di bawah ini muncul di hampir semua analisis:
# pandas untuk tabel, numpy untuk angka, statsmodels untuk regresi,
# matplotlib dan seaborn untuk grafik.

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
# ## 2. Baca data pertama
#
# Satu baris perintah: `pd.read_csv(URL_DATA + "uts_2.csv")`. Fungsi `head()`
# menampilkan 5 baris pertama supaya kita tahu isinya.

# %% [markdown]
# <!-- kamus_variabel:uts_2.csv -->
#
# ### Kenali data: Harga saham perusahaan
#
# **Data:** `data/uts_2.csv`. **Satu baris:** satu perusahaan pada contoh latihan.
#
# | Variabel/kolom | Pengertian | Satuan atau kode | Peran |
# |---|---|---|---|
# | `Y_Harga_Saham` | Harga satu lembar saham perusahaan. | Uang per lembar; skala mata uang tidak dirinci | Y: target |
# | `X1_Pendapatan_per_Saham` | EPS (Earnings Per Share): laba per lembar saham; bukan total omzet perusahaan. | Uang per lembar; skala mata uang tidak dirinci | X: penjelas |
# | `X2_Rasio_Utang_Ekuitas` | DER (Debt to Equity Ratio): total utang dibagi ekuitas perusahaan. | Rasio; 1,5 berarti utang 1,5 kali ekuitas (150%) | X: penjelas |
# | `X3_Belanja_Iklan` | Jumlah pengeluaran perusahaan untuk iklan. | Uang; skala dan periode belanja tidak dirinci | X: penjelas |
#
# Nama harga, eps, der, dan iklan adalah nama singkat dari kolom di atas. Contoh DER tidak dibaca sebagai 1,5 persen.
#
# Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

# %%
saham = pd.read_csv(URL_DATA + "uts_2.csv")
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
sampel_model = saham[["Y_Harga_Saham", "X1_Pendapatan_per_Saham"]].dropna()
X_model = sampel_model[["X1_Pendapatan_per_Saham"]]
y_model = sampel_model["Y_Harga_Saham"]

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
print(koefisien_model.round(3))
print()
print("R-squared:", round(model.score(X_model, y_model), 3))

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
# 1. Baca `data/uts_4.csv` ke variabel `harapan_hidup`. Tampilkan 5 baris
#    pertama.
# 2. Hitung rata-rata kolom `Y_Angka_Harapan_Hidup` dan `X2_Tingkat_Imunisasi`
#    dengan `.mean()`.
# 3. Jalankan regresi `Y_Angka_Harapan_Hidup ~ X1_Pengeluaran_Kesehatan`.
#    Apakah koefisiennya signifikan?

# %% [markdown]
# <!-- kamus_variabel:uts_4.csv -->
#
# ### Kenali data: Angka harapan hidup
#
# **Data:** `data/uts_4.csv`. **Satu baris:** satu negara pada contoh latihan.
#
# | Variabel/kolom | Pengertian | Satuan atau kode | Peran |
# |---|---|---|---|
# | `Y_Angka_Harapan_Hidup` | Rata-rata lama hidup yang diharapkan menurut indikator pada contoh. | Tahun | Y: target |
# | `X1_Pengeluaran_Kesehatan` | Pengeluaran kesehatan per penduduk (per kapita). | Uang per kapita; mata uang/periode tidak dirinci | X: penjelas |
# | `X2_Tingkat_Imunisasi` | Persentase anak yang memperoleh imunisasi. | Persen; jenis imunisasi tidak dirinci | X: penjelas |
# | `X3_Konsumsi_Kalori` | Rata-rata konsumsi energi makanan per hari. | Kalori harian; rincian satuan energi mengikuti sumber | X: penjelas |
#
# Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

# %%
# Tulis jawaban Anda di sini.
# harapan_hidup = pd.read_csv(...)
# harapan_hidup.head()
# ...

# %% [markdown]
# ## Praktik pendampingan AI
#
# Setelah contoh regresi berjalan, salin satu sel dan minta AI:
#
# > Saya baru belajar coding. Jelaskan kode ini satu baris setiap kali
# > dalam bahasa Indonesia. Sebutkan masukannya, hasil yang disimpan,
# > serta bagian yang boleh saya ubah. Gunakan nama yang sama dan
# > jangan menambahkan fungsi buatan sendiri atau perulangan.
#
# Cocokkan penjelasannya dengan tabel data dan hasil kode yang dijalankan.
# AI tidak perlu menebak koefisien. Ganti satu nilai prediksi, jalankan ulang,
# lalu tulis kesimpulan sendiri dengan satuan yang benar. Contoh prompt
# untuk membaca output dan memahami error ada di panduan/02_panduan_ai.md.

# %% [markdown]
# ### Selanjutnya
#
# Selanjutnya: Lab 1, regresi linear lengkap.
