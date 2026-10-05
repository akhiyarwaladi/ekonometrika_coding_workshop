# %% [markdown]
# # Hari 1, Sesi 0: Persiapan Google Colab untuk Ekonometrika
#
# **Durasi:** 30 menit
#
# Notebook ini untuk dosen atau pengajar. Isinya: menyiapkan lingkungan kerja,
# menyiapkan data, dan mengenali padanan perintah EViews dengan Python.
#
# **Sebelum mulai:** notebook ini membaca file CSV dari folder `data/`.
# Kalau folder itu belum ada, unggah `data-ekonometrika.zip` lewat panel
# Files di kiri layar Colab, lalu jalankan sel pertama di bawah sekali.
# Di komputer sendiri, cukup ekstrak zip-nya di folder yang sama.
#
# Cara menjalankan sel: klik selnya, tekan `Shift + Enter`.

# %% [markdown]
# **Posisi dalam alur workshop.** Sesi pembuka: menyiapkan alat dan data.
# Semua sesi setelah ini memakai pola yang sama, yaitu muat data, estimasi
# model, baca output, uji, lalu interpretasi.

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
# ## 1. Cek lingkungan
#
# Colab sudah menyediakan pandas, statsmodels, matplotlib, dan seaborn.
# Dua paket tambahan yang belum ada dipasang sekali di bawah ini:
# `linearmodels` untuk data panel (Sesi 6) dan `arch` untuk GARCH.

# %%
%pip install linearmodels arch -q

# %%
import sys
import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
import sklearn
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", palette=["#2F5D50", "#C15937", "#D9A441", "#5B8A8F"])
plt.rcParams.update({"figure.dpi": 110, "axes.titleweight": "bold", "font.size": 11})

print("Python", sys.version.split()[0])
print("pandas", pd.__version__)
print("statsmodels", sm.__version__)
print("scikit-learn", sklearn.__version__)

# %% [markdown]
# ## 2. Baca data pertama
#
# Semua data ada di folder `data/`. Cara membacanya selalu satu baris:
# `pd.read_csv("data/regresi-polinom.csv")`.

# %%
data = pd.read_csv("data/regresi-polinom.csv")
print("Ukuran data:", data.shape)
data.head()

# %% [markdown]
# ## 3. Sel pertama yang berguna: satu grafik
#
# Sebelum masuk regresi, lihat datanya dulu. Satu scatter plot bisa
# menyelamatkan Anda dari salah spesifikasi yang mahal.

# %%
sns.scatterplot(data=data, x="Biaya Iklan (X)", y="Penjualan (Y)")
plt.title("Biaya Iklan vs Penjualan")
plt.show()

# %% [markdown]
# ## 4. Fungsi bantu: ringkasan angka kunci
#
# Output `summary()` panjang. Fungsi kecil ini mengambil lima angka yang
# paling sering ditanya.

# %%
def angka_kunci(hasil):
    """Ambil N, R2, Adj R2, p-value uji F, dan AIC dari hasil regresi."""
    return pd.Series({
        "N": int(hasil.nobs),
        "R2": hasil.rsquared,
        "Adj_R2": hasil.rsquared_adj,
        "F_pvalue": hasil.f_pvalue,
        "AIC": hasil.aic,
    })

polinom = data.rename(columns={"Biaya Iklan (X)": "iklan", "Penjualan (Y)": "penjualan"})
model = smf.ols("penjualan ~ iklan", data=polinom).fit()
angka_kunci(model)


# %% [markdown]
# ### Coba sendiri (5 menit)
#
# Baca `data/uts-4.csv` ke variabel baru, lalu tampilkan jumlah baris dan
# rata-rata kolom `Y_Angka_Harapan_Hidup`. Butuh berapa baris kode?
#
# Tulis di sel di bawah, baru buka jawabannya.

# %%
# Tulis kode Anda di sini

# %% [markdown]
# <details><summary>Lihat jawaban</summary>
#
# Dua baris: `uts4 = pd.read_csv("data/uts-4.csv")` lalu
# `print(len(uts4), uts4["Y_Angka_Harapan_Hidup"].mean())`.
# Hasilnya 50 baris dan rata-rata 76,95.
#
# </details>

# %% [markdown]
# ## 5. Padanan perintah EViews dan Python
#
# Materi kuliah memakai EViews. Tabel ini jembatannya:
#
# | EViews | Python (statsmodels) |
# |---|---|
# | `ls y c x1 x2` | `smf.ols("y ~ x1 + x2", data=df).fit()` |
# | `ls log(y) c log(x)` | `smf.ols("np.log(y) ~ np.log(x)", data=df).fit()` |
# | Method **BINARY - Logit** | `smf.logit("y ~ x1", data=df).fit()` |
# | Method **BINARY - Probit** | `smf.probit("y ~ x1", data=df).fit()` |
# | Method **ORDERED** | `OrderedModel(...)` dari statsmodels |
# | Method **COUNT - Poisson** | `smf.poisson("y ~ x1", data=df).fit()` |
# | Method **ARCH - GARCH(1,1)** | `arch_model(y, vol="Garch", p=1, q=1)` |
# | Options > White robust SE | `.fit(cov_type="HC3")` |
# | Panel Options: Fixed | `PanelOLS(..., entity_effects=True)` |
#
# Nama kolom output juga beda, artinya sama:
#
# | EViews | statsmodels | Arti |
# |---|---|---|
# | Coefficient | `coef` | koefisien |
# | Std. Error | `std err` | galat baku |
# | t-Statistic | `t` | statistik uji |
# | Prob. | `pvalue` (ditulis P di output) | p-value |
# | R-squared | `rsquared` | proporsi variasi terjelaskan |
#
# ### Dua pustaka Python dan porsinya
#
# - **statsmodels**: estimasi, koefisien, standard error, p-value, dan
#   semua uji ekonometrika (multikolinearitas, heteroskedastisitas,
#   normalitas, ADF, kointegrasi, panel, GARCH).
# - **scikit-learn**: prediksi, pembagian data latih dan uji, serta metrik
#   klasifikasi seperti akurasi dan ROC AUC.
#
# scikit-learn tidak mengeluarkan p-value, jadi bukan pengganti
# statsmodels. Di workshop ini keduanya dipakai sesuai porsinya, dan di
# Sesi 4 ada contoh berdampingan supaya bedanya terlihat jelas.
#
# ## 6. Peta materi semester ke notebook ini
#
# | Pertemuan kuliah | Topik | Notebook |
# |---|---|---|
# | 1-2 | Regresi linear dan bentuk fungsional | `01`, `02` |
# | 3-4 | Variabel dummy, multikolinearitas | `03` |
# | 5-7 | Heteroskedastisitas, normalitas, autokorelasi | `03` |
# | 9-10 | Logit, probit, multinomial, ordinal | `04` |
# | 11 | Tobit dan Poisson | `04` |
# | 12-13 | Deret waktu, kointegrasi, ECM | `05` |
# | 14-15 | GARCH, data panel | `06` |
#
# Dua hari tidak cukup menuntaskan 16 pertemuan. Yang dikejar di workshop
# ini: alur kerja lengkap dari data sampai interpretasi, plus contoh kode
# untuk setiap topik. Sisanya latihan mandiri.

# %% [markdown]
# ## Latihan singkat
#
# 1. Baca `data/uts-4.csv` (data harapan hidup). Tampilkan 5 baris pertama.
# 2. Berapa jumlah observasi dan berapa rata-rata `Y_Angka_Harapan_Hidup`?
#
# (Kunci ada di `kunci_latihan.md`.)

# %%
# Tulis jawaban Anda di sini
# uts4 = pd.read_csv("data/uts-4.csv")
# ...

# %% [markdown]
# ### Selanjutnya
#
# Selanjutnya: Sesi 1, model regresi pertama.
