# %% [markdown]
# # Lab 3: Variabel Dummy dan Uji Asumsi Klasik
#
# **Durasi:** 90 menit
#
# Tujuan: mengubah data kategorikal jadi variabel dummy, lalu memeriksa
# empat asumsi klasik dan menangani pelanggarannya.

# %% [markdown]
# **Posisi dalam alur workshop.** Memvalidasi model dari Lab 1 dan 2. Lab
# 4 mengganti jenis variabel Y.

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
# Panduan simbol dan contoh tambahan ada di `panduan/cara_menggunakan_notebook.md`.

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
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", palette=["#2F5D50", "#C15937", "#D9A441", "#5B8A8F"])
plt.rcParams.update({"figure.dpi": 110, "axes.titleweight": "bold", "font.size": 11})

# %% [markdown]
# ## 1. Contoh terbimbing: variabel dummy
#
# Data `data/latihan_dummy_1.csv`: gaji, pengalaman, gender, dan status
# 30 karyawan. Kategori dibuat dummy secara manual supaya kategori
# basisnya jelas: Wanita dan Lajang.

# %% [markdown]
# <!-- kamus_variabel:latihan_dummy_1.csv -->
#
# ### Kenali data: Gaji dan karakteristik pekerja
#
# **Data:** `data/latihan_dummy_1.csv`. **Satu baris:** satu pekerja pada contoh latihan.
#
# Nama singkat di kode berasal dari penggantian nama kolom CSV; isi angkanya tetap sama.
#
# | Kolom CSV | Nama di kode | Pengertian | Satuan atau kode | Peran |
# |---|---|---|---|---|
# | `No` | `No` | Nomor urut pekerja. | Nomor identitas | Penanda, bukan besaran ekonomi |
# | `GAJI` | `gaji` | Besarnya gaji pekerja. | Uang; skala/periode gaji tidak dirinci | Y: target |
# | `PENGALAMAN` | `pengalaman` | Lama pengalaman kerja pekerja. | Satuan waktu tidak dirinci sumber | X: penjelas |
# | `GENDER` | `gender` | Kategori gender yang dicatat dalam berkas. | Teks: Pria atau Wanita | X: penjelas |
# | `STATUS` | `status` | Status perkawinan pekerja. | Teks: Menikah atau Lajang | X: penjelas |
#
# Kategori teks diubah menjadi dummy 0/1 saat praktik; kelompok acuan dijelaskan pada bagian pembentukan dummy.
#
# Kolom turunan berikut dibuat saat praktik; kolom ini belum ada pada CSV awal.
#
# | Kolom turunan | Pengertian | Satuan/kode |
# |---|---|---|
# | `dummy_pria` | Indikator kategori Pria; kelompok selain Pria menjadi acuan. | 1 = Pria; 0 = selain Pria |
# | `dummy_menikah` | Indikator status Menikah; kelompok selain Menikah menjadi acuan. | 1 = Menikah; 0 = selain Menikah |
#
# Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

# %%
gaji = pd.read_csv(URL_DATA + "latihan_dummy_1.csv")
gaji = gaji.rename(
    columns={
        "GAJI": "gaji",
        "PENGALAMAN": "pengalaman",
        "GENDER": "gender",
        "STATUS": "status",
    }
)
gaji["dummy_pria"] = (gaji["gender"] == "Pria").astype(int)
gaji["dummy_menikah"] = (gaji["status"] == "Menikah").astype(int)
gaji.head()

# %%
sampel_model_dummy_mentah = gaji[["gaji", "dummy_pria", "dummy_menikah"]].dropna()
X_model_dummy_mentah = sampel_model_dummy_mentah[["dummy_pria", "dummy_menikah"]]
y_model_dummy_mentah = sampel_model_dummy_mentah["gaji"]

model_dummy_mentah = LinearRegression()
model_dummy_mentah.fit(X_model_dummy_mentah, y_model_dummy_mentah)

koefisien_model_dummy_mentah = pd.Series(
    model_dummy_mentah.coef_, index=X_model_dummy_mentah.columns
)
koefisien_model_dummy_mentah.loc["Intercept"] = model_dummy_mentah.intercept_

# Pelengkap statistik: standard error dan pengujian pada sampel yang sama.
uji_model_dummy_mentah = sm.OLS(
    y_model_dummy_mentah,
    sm.add_constant(X_model_dummy_mentah, has_constant="add").rename(
        columns={"const": "Intercept"}
    ),
).fit()
print("Tanpa kontrol pengalaman:")
print(koefisien_model_dummy_mentah.round(3))
print(uji_model_dummy_mentah.pvalues.round(4))

# %%
sampel_model = gaji[["gaji", "pengalaman", "dummy_pria", "dummy_menikah"]].dropna()
X_model = sampel_model[["pengalaman", "dummy_pria", "dummy_menikah"]]
y_model = sampel_model["gaji"]

model = LinearRegression()
model.fit(X_model, y_model)

koefisien_model = pd.Series(model.coef_, index=X_model.columns)
koefisien_model.loc["Intercept"] = model.intercept_

# Pelengkap statistik: standard error dan pengujian pada sampel yang sama.
uji_model = sm.OLS(
    y_model,
    sm.add_constant(X_model, has_constant="add").rename(columns={"const": "Intercept"}),
).fit()
print("Dengan kontrol pengalaman:")
print(koefisien_model.round(3))
print(uji_model.pvalues.round(4))

# %% [markdown]
# ### Membaca hasil
#
# Di model mentah, pria tampak bergaji lebih tinggi 3,35 dan yang menikah
# 7,05, keduanya signifikan. Setelah pengalaman kerja dikontrol, keduanya
# mengecil mendekati nol dan tidak signifikan. Artinya: perbedaan gaji
# mentah itu sebagian besar dijelaskan oleh pengalaman kerja.
#
# Pelajaran: koefisien dummy adalah perbedaan antar kelompok SETELAH
# variabel lain dikontrol. Selalu sebut kategori basisnya di laporan.

# %% [markdown]
# ## 2. Contoh terbimbing: multikolinearitas
#
# Data `data/latihan_multikolinieritas_1.csv`: harga rumah dijelaskan luas
# bangunan, luas tanah, dan jumlah kamar. Hitung VIF (Variance Inflation
# Factor). Aturan praktis: VIF di atas 10 menandakan masalah.

# %% [markdown]
# <!-- kamus_variabel:latihan_multikolinieritas_1.csv -->
#
# ### Kenali data: Harga dan ukuran rumah
#
# **Data:** `data/latihan_multikolinieritas_1.csv`. **Satu baris:** satu rumah pada contoh latihan.
#
# Nama singkat di kode berasal dari penggantian nama kolom CSV; isi angkanya tetap sama.
#
# | Kolom CSV | Nama di kode | Pengertian | Satuan atau kode | Peran |
# |---|---|---|---|---|
# | `No` | `No` | Nomor rumah/pengamatan. | Nomor identitas | Penanda, bukan besaran ekonomi |
# | `HARGA` | `harga` | Harga jual rumah. | Uang; skala tidak dirinci | Y: target |
# | `LUAS_BANGUNAN` | `luas_bangunan` | Luas fisik bangunan rumah. | Satuan luas tidak dirinci sumber | X: penjelas |
# | `LUAS_TANAH` | `luas_tanah` | Luas tanah tempat rumah berada. | Satuan luas tidak dirinci sumber | X: penjelas |
# | `JML_KAMAR` | `jml_kamar` | Jumlah kamar pada rumah. | Kamar | X: penjelas |
#
# Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

# %%
from statsmodels.stats.outliers_influence import variance_inflation_factor

rumah = pd.read_csv(URL_DATA + "latihan_multikolinieritas_1.csv")
rumah = rumah.rename(
    columns={
        "HARGA": "harga",
        "LUAS_BANGUNAN": "luas_bangunan",
        "LUAS_TANAH": "luas_tanah",
        "JML_KAMAR": "jml_kamar",
    }
)

# add_constant wajib supaya VIF dihitung bersama intersep
X = sm.add_constant(rumah[["luas_bangunan", "luas_tanah", "jml_kamar"]])
# VIF dihitung per kolom; baris const di hasil wajar dan boleh diabaikan
# Kolom 0 adalah konstanta; kolom 1 sampai 3 adalah variabel penjelas.
vif_bangunan = variance_inflation_factor(X.values, 1)
vif_tanah = variance_inflation_factor(X.values, 2)
vif_kamar = variance_inflation_factor(X.values, 3)

vif = pd.DataFrame(
    {
        "variabel": ["luas_bangunan", "luas_tanah", "jml_kamar"],
        "VIF": [vif_bangunan, vif_tanah, vif_kamar],
    }
)
vif

# %%
sampel_model_rumah = rumah[
    ["harga", "luas_bangunan", "luas_tanah", "jml_kamar"]
].dropna()
X_model_rumah = sampel_model_rumah[["luas_bangunan", "luas_tanah", "jml_kamar"]]
y_model_rumah = sampel_model_rumah["harga"]

model_rumah = LinearRegression()
model_rumah.fit(X_model_rumah, y_model_rumah)

# Pelengkap statistik: standard error dan pengujian pada sampel yang sama.
uji_model_rumah = sm.OLS(
    y_model_rumah,
    sm.add_constant(X_model_rumah, has_constant="add").rename(
        columns={"const": "Intercept"}
    ),
).fit()
print("R2:", round(model_rumah.score(X_model_rumah, y_model_rumah), 4))
print(uji_model_rumah.pvalues.round(4))

# %% [markdown]
# Perhatikan gejalanya: R kuadrat sangat tinggi, tapi ada variabel yang
# tidak signifikan. Penyebabnya luas bangunan dan luas tanah berkorelasi
# 0,99. Solusinya: buang salah satu variabel.

# %% [markdown]
# ### Coba sendiri (5 menit)
#
# Prediksi gaji Wanita, status Lajang, dengan pengalaman 8 tahun.
#
# Tulis di sel di bawah, baru buka jawabannya.

# %%
# Tulis kode Anda di sini

# %% [markdown]
# <details><summary>Lihat jawaban</summary>
#
# 4,0548 + 1,3489 x 8 = 14,85. Kedua dummy bernilai nol karena
# Wanita dan Lajang adalah kategori basis.
#
# </details>

# %% [markdown]
# ## 3. Latihan mandiri
#
# **Latihan 1: heteroskedastisitas.** Data `data/hetero_2.csv`
# (`Pendapatan ~ Pendidikan + Pengalaman + Usia`).
#
# - Jalankan uji Breusch-Pagan dan White.
# - Estimasi ulang dengan robust standard error (`cov_type="HC3"`).
# - Bandingkan p-value biasa dan robust. Apakah kesimpulannya berubah?

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
# kerja = pd.read_csv(URL_DATA + "hetero_2.csv")
# X_kerja = kerja[["Pendidikan", "Pengalaman", "Usia"]]
# y_kerja = kerja["Pendapatan"]
# model_kerja = LinearRegression()
# model_kerja.fit(X_kerja, y_kerja)
# residu_kerja = y_kerja - model_kerja.predict(X_kerja)
# from statsmodels.stats.diagnostic import het_breuschpagan, het_white
# Xk = sm.add_constant(X_kerja)
# # Angka pada posisi [1] adalah p-value dari tiap uji.
# print("BP p:", het_breuschpagan(residu_kerja, Xk)[1])
# print("White p:", het_white(residu_kerja, Xk)[1])
# # Pelengkap inferensi pada X dan y yang sama.
# uji_kerja = sm.OLS(y_kerja, Xk).fit()
# uji_kerja_robust = sm.OLS(y_kerja, Xk).fit(cov_type="HC3")
# print(uji_kerja.pvalues)
# print(uji_kerja_robust.pvalues)
# ...

# %% [markdown]
# **Latihan 2: normalitas.** Data `data/latihan_normalitas_3.csv`
# (`Harga ~ Luas_Bangunan + Jumlah_Kamar + Usia_Rumah`).
#
# - Tampilkan histogram residual.
# - Uji Jarque-Bera. p-value di atas 0,05 berarti residual normal.

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
# nrumah = pd.read_csv(URL_DATA + "latihan_normalitas_3.csv")
# sampel_model_n = nrumah[
#     ["Harga", "Luas_Bangunan", "Jumlah_Kamar", "Usia_Rumah"]
# ].dropna()
# X_model_n = sampel_model_n[["Luas_Bangunan", "Jumlah_Kamar", "Usia_Rumah"]]
# y_model_n = sampel_model_n["Harga"]
#
# model_n = LinearRegression()
# model_n.fit(X_model_n, y_model_n)
#
# prediksi_model_n = pd.Series(model_n.predict(X_model_n), index=y_model_n.index)
# residu_model_n = y_model_n - prediksi_model_n
# from statsmodels.stats.stattools import jarque_bera
#
# print(jarque_bera(residu_model_n))
# ...

# %% [markdown]
# **Latihan 3: kasus tanpa pelanggaran.** Data `data/hetero_1.csv`
# (`Penjualan ~ Iklan + Salesperson + Diskon`). Dugaan di soal:
# variabilitas penjualan membesar saat iklan tinggi. Uji dengan
# Breusch-Pagan dan White.
#
# Pertanyaan: apakah dugaan itu didukung data? Kalau tidak, laporkan
# p-value kedua uji dan tulis bahwa hipotesis tidak didukung data. Jangan
# mengubah kesimpulan agar terlihat sesuai dugaan.

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
# jual = pd.read_csv(URL_DATA + "hetero_1.csv")
# ...

# %% [markdown]
# ### Selanjutnya
#
# Selanjutnya: Lab 4, model kategorikal.
