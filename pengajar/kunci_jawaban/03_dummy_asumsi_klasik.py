# %% [markdown]
# # Kunci Lab 3: Dummy dan Asumsi Klasik

# %% [markdown]
# ## Persiapan: alamat data
#
# Jalankan sel alamat data di bawah. `URL_DATA` menyimpan alamat folder CSV di GitHub;
# `pd.read_csv(...)` membaca tabel sesuai nama CSV pada sel kode berikutnya.
# Gunakan koneksi internet dan jalankan sel berurutan dengan **Shift + Enter**.

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

# %%
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
import statsmodels.api as sm

# %% [markdown]
# ## Latihan 1: heteroskedastisitas (hetero-2)

# %% [markdown]
# <!-- kamus_variabel:hetero_2.csv -->
#
# ### Kenali data: Pendapatan dan karakteristik pekerja
#
# **Data:** `data/hetero_2.csv`. **Satu baris:** satu orang pada contoh latihan.
#
# | Variabel/kolom | Pengertian | Satuan atau kode | Peran |
# |---|---|---|---|
# | `Pendapatan` | Pendapatan selama satu tahun. | Puluhan juta rupiah per tahun, sesuai uraian sumber | Y: target |
# | `Pendidikan` | Lama pendidikan yang telah ditempuh. | Tahun | X: penjelas |
# | `Pengalaman` | Lama pengalaman kerja. | Tahun | X: penjelas |
# | `Usia` | Umur orang yang diamati. | Tahun | X: penjelas |
#
# Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

# %%
from statsmodels.stats.diagnostic import het_breuschpagan, het_white

kerja = pd.read_csv(URL_DATA + "hetero_2.csv")
sampel_model_kerja = kerja[["Pendapatan", "Pendidikan", "Pengalaman", "Usia"]].dropna()
X_model_kerja = sampel_model_kerja[["Pendidikan", "Pengalaman", "Usia"]]
y_model_kerja = sampel_model_kerja["Pendapatan"]

model_kerja = LinearRegression()
model_kerja.fit(X_model_kerja, y_model_kerja)

prediksi_model_kerja = pd.Series(
    model_kerja.predict(X_model_kerja), index=y_model_kerja.index
)
residu_model_kerja = y_model_kerja - prediksi_model_kerja

# Pelengkap statistik: standard error dan pengujian pada sampel yang sama.
uji_model_kerja = sm.OLS(
    y_model_kerja,
    sm.add_constant(X_model_kerja, has_constant="add").rename(
        columns={"const": "Intercept"}
    ),
).fit()

Xk = sm.add_constant(kerja[["Pendidikan", "Pengalaman", "Usia"]])
print("BP p   :", round(het_breuschpagan(residu_model_kerja, Xk)[1], 4))
print("White p:", round(het_white(residu_model_kerja, Xk)[1], 4))

# Pelengkap inferensi: koreksi standard error, dengan X dan y yang sama.
uji_model_robust = sm.OLS(
    y_model_kerja,
    sm.add_constant(X_model_kerja, has_constant="add").rename(
        columns={"const": "Intercept"}
    ),
).fit(cov_type="HC3")
banding = pd.DataFrame(
    {
        "p_biasa": uji_model_kerja.pvalues,
        "p_robust": uji_model_robust.pvalues,
    }
)
print(banding.round(4))

# %% [markdown]
# Kesimpulan: Breusch-Pagan menolak homoskedastis (p = 0,0025), White
# tidak menolak pada 5% (p = 0,064). Karena ada bukti heteroskedastis,
# laporkan versi robust. Perubahan yang terlihat: p-value pendidikan
# naik dari 0,0089 ke 0,0286, tetap signifikan tapi lebih lemah.

# %% [markdown]
# ## Latihan 2: normalitas (latihan-normalitas-3)

# %% [markdown]
# <!-- kamus_variabel:latihan_normalitas_3.csv -->
#
# ### Kenali data: Harga dan kondisi rumah
#
# **Data:** `data/latihan_normalitas_3.csv`. **Satu baris:** satu rumah pada contoh latihan.
#
# | Variabel/kolom | Pengertian | Satuan atau kode | Peran |
# |---|---|---|---|
# | `Harga` | Harga jual rumah pada data simulasi. | Sumber menyebut juta rupiah sekaligus simulasi dolar; skala ambigu | Y: target |
# | `Luas_Bangunan` | Luas bangunan rumah. | Sumber menyebut m² sekaligus simulasi kaki persegi; skala ambigu | X: penjelas |
# | `Jumlah_Kamar` | Jumlah kamar tidur. | Kamar | X: penjelas |
# | `Usia_Rumah` | Lama sejak rumah dibangun. | Tahun | X: penjelas |
#
# Sumber mencampurkan keterangan satuan untuk harga dan luas. Gunakan angka ini untuk latihan statistik; konfirmasi satuan sebelum memberi interpretasi nominal atau mengonversi luas.
#
# Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

# %%
from statsmodels.stats.stattools import jarque_bera
import matplotlib.pyplot as plt
import seaborn as sns

nrumah = pd.read_csv(URL_DATA + "latihan_normalitas_3.csv")
sampel_model_n = nrumah[
    ["Harga", "Luas_Bangunan", "Jumlah_Kamar", "Usia_Rumah"]
].dropna()
X_model_n = sampel_model_n[["Luas_Bangunan", "Jumlah_Kamar", "Usia_Rumah"]]
y_model_n = sampel_model_n["Harga"]

model_n = LinearRegression()
model_n.fit(X_model_n, y_model_n)

prediksi_model_n = pd.Series(model_n.predict(X_model_n), index=y_model_n.index)
residu_model_n = y_model_n - prediksi_model_n

jb, p_jb, skew, kurt = jarque_bera(residu_model_n)
print(f"Jarque-Bera = {jb:.4f}, p = {p_jb:.4f}")

sns.histplot(residu_model_n, kde=True)
plt.title("Histogram residual")
plt.show()

# %% [markdown]
# Kesimpulan: p = 0,2032 di atas 0,05, jadi residual tidak menyimpang
# jauh dari normal menurut uji ini; gagal menolak bukan membuktikan normalitas.

# %% [markdown]
# ## Latihan 3: kasus tanpa pelanggaran (hetero-1)

# %% [markdown]
# <!-- kamus_variabel:hetero_1.csv -->
#
# ### Kenali data: Iklan, tenaga penjualan, dan diskon
#
# **Data:** `data/hetero_1.csv`. **Satu baris:** satu pengamatan penjualan perusahaan dalam contoh.
#
# | Variabel/kolom | Pengertian | Satuan atau kode | Peran |
# |---|---|---|---|
# | `Penjualan` | Banyaknya produk terjual. | Ribuan unit | Y: target |
# | `Iklan` | Pengeluaran untuk iklan. | Juta rupiah | X: penjelas |
# | `Salesperson` | Jumlah tenaga penjualan yang bekerja. | Orang | X: penjelas |
# | `Diskon` | Rata-rata potongan harga yang diberikan. | Persen; 5,2 berarti 5,2% | X: penjelas |
#
# Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

# %%
jual = pd.read_csv(URL_DATA + "hetero_1.csv")
sampel_model_jual = jual[["Penjualan", "Iklan", "Salesperson", "Diskon"]].dropna()
X_model_jual = sampel_model_jual[["Iklan", "Salesperson", "Diskon"]]
y_model_jual = sampel_model_jual["Penjualan"]

model_jual = LinearRegression()
model_jual.fit(X_model_jual, y_model_jual)

prediksi_model_jual = pd.Series(
    model_jual.predict(X_model_jual), index=y_model_jual.index
)
residu_model_jual = y_model_jual - prediksi_model_jual
Xj = sm.add_constant(jual[["Iklan", "Salesperson", "Diskon"]])
print("BP p   :", round(het_breuschpagan(residu_model_jual, Xj)[1], 4))
print("White p:", round(het_white(residu_model_jual, Xj)[1], 4))

# %% [markdown]
# Kesimpulan: kedua uji tidak menolak homoskedastis (p = 0,997 dan 0,542).
# Dugaan "variabilitas penjualan membesar saat iklan tinggi" tidak
# didukung data ini. Yang benar: laporkan apa adanya, jangan paksakan
# narasi. Ini juga contoh bahwa hipotesis bisa ditolak data.
