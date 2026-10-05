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
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", palette=["#2F5D50", "#C15937", "#D9A441", "#5B8A8F"])
plt.rcParams.update({"figure.dpi": 110, "axes.titleweight": "bold", "font.size": 11})

# %% [markdown]
# ## 1. Contoh terbimbing: variabel dummy
#
# Data `data/latihan-dummy-1.csv`: gaji, pengalaman, gender, dan status
# 30 karyawan. Kategori dibuat dummy secara manual supaya kategori
# basisnya jelas: Wanita dan Lajang.

# %%
gaji = pd.read_csv("data/latihan-dummy-1.csv").rename(columns={
    "GAJI": "gaji", "PENGALAMAN": "pengalaman", "GENDER": "gender",
    "STATUS": "status"})
gaji["dummy_pria"] = (gaji["gender"] == "Pria").astype(int)
gaji["dummy_menikah"] = (gaji["status"] == "Menikah").astype(int)
gaji.head()

# %%
model_dummy_mentah = smf.ols("gaji ~ dummy_pria + dummy_menikah", data=gaji).fit()
print("Tanpa kontrol pengalaman:")
print(model_dummy_mentah.params.round(3))
print(model_dummy_mentah.pvalues.round(4))

# %%
model = smf.ols("gaji ~ pengalaman + dummy_pria + dummy_menikah", data=gaji).fit()
print("Dengan kontrol pengalaman:")
print(model.params.round(3))
print(model.pvalues.round(4))

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
# Data `data/latihan-multikolinieritas-1.csv`: harga rumah dijelaskan luas
# bangunan, luas tanah, dan jumlah kamar. Hitung VIF (Variance Inflation
# Factor). Aturan praktis: VIF di atas 10 menandakan masalah.

# %%
from statsmodels.stats.outliers_influence import variance_inflation_factor

rumah = pd.read_csv("data/latihan-multikolinieritas-1.csv").rename(columns={
    "HARGA": "harga", "LUAS_BANGUNAN": "luas_bangunan",
    "LUAS_TANAH": "luas_tanah", "JML_KAMAR": "jml_kamar"})

# add_constant wajib supaya VIF dihitung bersama intersep
X = sm.add_constant(rumah[["luas_bangunan", "luas_tanah", "jml_kamar"]])
# VIF dihitung per kolom; baris const di hasil wajar dan boleh diabaikan
vif = pd.DataFrame({
    "variabel": X.columns,
    "VIF": [variance_inflation_factor(X.values, i) for i in range(X.shape[1])],
})
vif

# %%
model_rumah = smf.ols("harga ~ luas_bangunan + luas_tanah + jml_kamar", data=rumah).fit()
print("R2:", round(model_rumah.rsquared, 4))
print(model_rumah.pvalues.round(4))

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
# **Latihan 1: heteroskedastisitas.** Data `data/hetero-2.csv`
# (`Pendapatan ~ Pendidikan + Pengalaman + Usia`).
#
# - Jalankan uji Breusch-Pagan dan White.
# - Estimasi ulang dengan robust standard error (`cov_type="HC3"`).
# - Bandingkan p-value biasa dan robust. Apakah kesimpulannya berubah?

# %%
# kerja = pd.read_csv("data/hetero-2.csv")
# model_kerja = smf.ols("Pendapatan ~ Pendidikan + Pengalaman + Usia", data=kerja).fit()
# from statsmodels.stats.diagnostic import het_breuschpagan, het_white
# Xk = sm.add_constant(kerja[["Pendidikan", "Pengalaman", "Usia"]])
# [1] yang diambil adalah p-value dari tiap uji
# print("BP p:", het_breuschpagan(model_kerja.resid, Xk)[1])
# print("White p:", het_white(model_kerja.resid, Xk)[1])
# model_robust = smf.ols("Pendapatan ~ Pendidikan + Pengalaman + Usia", data=kerja).fit(cov_type="HC3")
# ...

# %% [markdown]
# **Latihan 2: normalitas.** Data `data/latihan-normalitas-3.csv`
# (`Harga ~ Luas_Bangunan + Jumlah_Kamar + Usia_Rumah`).
#
# - Tampilkan histogram residual.
# - Uji Jarque-Bera. p-value di atas 0,05 berarti residual normal.

# %%
# nrumah = pd.read_csv("data/latihan-normalitas-3.csv")
# model_n = smf.ols("Harga ~ Luas_Bangunan + Jumlah_Kamar + Usia_Rumah", data=nrumah).fit()
# from statsmodels.stats.stattools import jarque_bera
# print(jarque_bera(model_n.resid))
# ...

# %% [markdown]
# **Latihan 3: kasus tanpa pelanggaran.** Data `data/hetero-1.csv`
# (`Penjualan ~ Iklan + Salesperson + Diskon`). Dugaan di soal:
# variabilitas penjualan membesar saat iklan tinggi. Uji dengan
# Breusch-Pagan dan White.
#
# Pertanyaan: apakah dugaan itu didukung data? Kalau tidak, laporkan
# p-value kedua uji dan tulis bahwa hipotesis tidak didukung data. Jangan
# mengubah kesimpulan agar terlihat sesuai dugaan.

# %%
# jual = pd.read_csv("data/hetero-1.csv")
# ...

# %% [markdown]
# ### Selanjutnya
#
# Selanjutnya: Lab 4, model kategorikal.
