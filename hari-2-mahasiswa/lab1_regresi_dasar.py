# %% [markdown]
# # Lab 1: Regresi Linear dari Data sampai Keputusan
#
# **Durasi:** 90 menit
#
# Tujuan lab ini: Anda bisa menjalankan regresi, membaca outputnya, dan
# mengambil kesimpulan yang bisa dipertanggungjawabkan.
#
# **Persiapan data:** jalankan sel pertama di bawah. Kalau folder `data/`
# kosong, unggah `data-ekonometrika.zip` lewat panel Files di kiri, lalu
# jalankan ulang selnya.

# %% [markdown]
# **Posisi dalam alur workshop.** Setelah regresi pertama di Lab 0, ini
# versi lengkapnya: berganda, interpretasi, prediksi. Pertanyaan tentang
# bentuk model dijawab di Lab 2.

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
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", palette=["#2F5D50", "#C15937", "#D9A441", "#5B8A8F"])
plt.rcParams.update({"figure.dpi": 110, "axes.titleweight": "bold", "font.size": 11})

# %% [markdown]
# ## 1. Contoh terbimbing: penjualan produk elektronik
#
# Manajer pemasaran ingin tahu apa yang memengaruhi penjualan unit:
# biaya iklan, harga produk sendiri, atau harga kompetitor? Data ada di
# `data/uts-6.csv`.

# %%
jual = pd.read_csv("data/uts-6.csv").rename(columns={
    "Y_Penjualan_Unit": "penjualan",
    "X1_Biaya_Iklan": "iklan",
    "X2_Harga_Produk": "harga",
    "X3_Harga_Kompetitor": "harga_kompetitor",
})
jual.head()

# %%
model = smf.ols("penjualan ~ iklan + harga + harga_kompetitor", data=jual).fit()
print(model.summary())

# %% [markdown]
# ### Membaca hasil
#
# | Baris | Koefisien | Arti |
# |---|---|---|
# | iklan | +0,79 | tambahan 1 unit iklan menaikkan penjualan 0,79 unit |
# | harga | -1,20 | kenaikan harga sendiri menurunkan penjualan (sesuai teori) |
# | harga_kompetitor | +0,21 | tidak signifikan (p = 0,60), belum bisa dibedakan dari nol |
#
# R kuadrat 0,99 berarti model menjelaskan hampir semua variasi penjualan.
# Hati-hati: data ini simulasi, di data nyata R kuadrat setinggi ini jarang.

# %%
tabel = pd.DataFrame({
    "koefisien": model.params,
    "p_value": model.pvalues,
})
tabel.round(4)

# %% [markdown]
# ### Memprediksi
#
# `predict` membutuhkan DataFrame dengan nama kolom yang sama seperti di
# rumus. Coba prediksi penjualan kalau iklan 60, harga 100, dan harga
# kompetitor 105.

# %%
situasi_baru = pd.DataFrame({"iklan": [60], "harga": [100], "harga_kompetitor": [105]})
model.predict(situasi_baru)


# %% [markdown]
# ### Coba sendiri (5 menit)
#
# Dengan `model` penjualan di atas, prediksi penjualan untuk iklan = 80,
# harga = 95, dan harga kompetitor = 100.
#
# Tulis di sel di bawah, baru buka jawabannya.

# %%
# Tulis kode Anda di sini

# %% [markdown]
# <details><summary>Lihat jawaban</summary>
#
# Prediksinya sekitar 180 unit. Perhatikan harga turun menaikkan
# penjualan, sesuai koefisien -1,20.
#
# </details>

# %% [markdown]
# ## 2. Latihan mandiri
#
# **Latihan 1: produktivitas padi.** Data `data/uts-3.csv` berisi 50
# wilayah. Jawab pertanyaan: pupuk, curah hujan, atau sinar matahari yang
# paling berperan bagi produktivitas padi?
#
# Langkah: baca data, jalankan regresi
# `Y_Produktivitas_Padi ~ X1_Jumlah_Pupuk + X2_Curah_Hujan + X3_Sinar_Matahari`,
# lalu isi kolom interpretasi di bawah.

# %%
# padi = pd.read_csv("data/uts-3.csv")
# model_padi = smf.ols("...", data=padi).fit()
# print(model_padi.summary())

# %% [markdown]
# Tulis kesimpulan Anda:
#
# - Variabel yang signifikan: ...
# - Tanda koefisiennya sesuai dugaan? (curah hujan diharapkan positif pada
#   rentang data ini; pupuk dan sinar bisa lemah) ...
# - Prediksi kalau pupuk 160, hujan 1900, sinar 230: ...

# %% [markdown]
# **Latihan 2: angka harapan hidup.** Data `data/uts-4.csv` berisi 50
# negara. Regresikan `Y_Angka_Harapan_Hidup` pada pengeluaran kesehatan,
# tingkat imunisasi, dan konsumsi kalori. Variabel mana yang signifikan?

# %%
# harapan = pd.read_csv("data/uts-4.csv")
# ...

# %% [markdown]
# **Latihan 3: latihan prediksi.** Pakai model padi di Latihan 1. Prediksi
# produktivitas untuk situasi: pupuk 200, hujan 1500, sinar 200. Tulis
# hasilnya di komentar.

# %%
# situasi = pd.DataFrame({"X1_Jumlah_Pupuk": [200], "X2_Curah_Hujan": [1500],
#                         "X3_Sinar_Matahari": [200]})
# model_padi.predict(situasi)

# %% [markdown]
# ### Selanjutnya
#
# Selanjutnya: Lab 2, memilih bentuk model.
