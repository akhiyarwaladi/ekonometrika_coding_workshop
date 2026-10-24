# %% [markdown]
# # Lab 1: Regresi Linear dari Data sampai Keputusan
#
# **Durasi:** 90 menit
#
# Tujuan lab ini: Anda bisa menjalankan regresi, membaca outputnya, dan
# mengambil kesimpulan yang bisa dipertanggungjawabkan.
#
# **Persiapan data:** Jalankan sel alamat data di bawah. `URL_DATA` menyimpan alamat folder CSV di GitHub;
# `pd.read_csv(...)` membaca tabel sesuai nama CSV pada sel kode berikutnya.
# Gunakan koneksi internet dan jalankan sel berurutan dengan **Shift + Enter**.

# %% [markdown]
# **Posisi dalam alur workshop.** Setelah regresi pertama di Lab 0, ini
# versi lengkapnya: berganda, interpretasi, prediksi. Pertanyaan tentang
# bentuk model dijawab di Lab 2.

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
import statsmodels.api as sm
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", palette=["#2F5D50", "#C15937", "#D9A441", "#5B8A8F"])
plt.rcParams.update({"figure.dpi": 110, "axes.titleweight": "bold", "font.size": 11})

# %% [markdown]
# ## 1. Contoh terbimbing: penjualan produk elektronik
#
# Manajer pemasaran ingin tahu apa yang memengaruhi penjualan unit:
# biaya iklan, harga produk sendiri, atau harga kompetitor? Data ada di
# `data/uts_6.csv`.

# %% [markdown]
# <!-- kamus_variabel:uts_6.csv -->
#
# ### Kenali data: Penjualan produk
#
# **Data:** `data/uts_6.csv`. **Satu baris:** satu pengamatan penjualan produk dalam contoh latihan.
#
# Nama singkat di kode berasal dari penggantian nama kolom CSV; isi angkanya tetap sama.
#
# | Kolom CSV | Nama di kode | Pengertian | Satuan atau kode | Peran |
# |---|---|---|---|---|
# | `Y_Penjualan_Unit` | `penjualan` | Banyaknya produk yang terjual. | Unit produk dalam data simulasi | Y: target |
# | `X1_Biaya_Iklan` | `iklan` | Biaya promosi/iklan untuk produk tersebut. | Uang; skala tidak dirinci | X: penjelas |
# | `X2_Harga_Produk` | `harga` | Harga jual produk milik perusahaan. | Uang per unit; skala tidak dirinci | X: penjelas |
# | `X3_Harga_Kompetitor` | `harga_kompetitor` | Harga produk pesaing yang menjadi pembanding. | Uang per unit; skala tidak dirinci | X: penjelas |
#
# Harga produk sendiri dan harga kompetitor adalah dua variabel berbeda. Periode penjualan dan skala mata uang tidak dijelaskan pada sumber.
#
# Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

# %%
jual = pd.read_csv(URL_DATA + "uts_6.csv")
jual = jual.rename(
    columns={
        "Y_Penjualan_Unit": "penjualan",
        "X1_Biaya_Iklan": "iklan",
        "X2_Harga_Produk": "harga",
        "X3_Harga_Kompetitor": "harga_kompetitor",
    }
)
jual.head()

# %%
sampel_model = jual[["penjualan", "iklan", "harga", "harga_kompetitor"]].dropna()
X_model = sampel_model[["iklan", "harga", "harga_kompetitor"]]
y_model = sampel_model["penjualan"]

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
tabel = pd.DataFrame(
    {
        "koefisien": koefisien_model,
        "p_value": uji_model.pvalues,
    }
)
tabel.round(4)

# %% [markdown]
# ### Memprediksi
#
# `predict` membutuhkan DataFrame dengan nama kolom yang sama seperti di
# tabel X saat pelatihan. Coba prediksi penjualan kalau iklan 60, harga 100, dan harga
# kompetitor 105.

# %%
situasi_baru = pd.DataFrame({"iklan": [60], "harga": [100], "harga_kompetitor": [105]})
pd.Series(
    model.predict(situasi_baru[["iklan", "harga", "harga_kompetitor"]]),
    index=situasi_baru.index,
)

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
# **Latihan 1: produktivitas padi.** Data `data/uts_3.csv` berisi 50
# wilayah. Jawab pertanyaan: pupuk, curah hujan, atau sinar matahari yang
# paling berperan bagi produktivitas padi?
#
# Langkah: baca data, jalankan regresi
# `Y_Produktivitas_Padi ~ X1_Jumlah_Pupuk + X2_Curah_Hujan + X3_Sinar_Matahari`,
# lalu isi kolom interpretasi di bawah.

# %% [markdown]
# <!-- kamus_variabel:uts_3.csv -->
#
# ### Kenali data: Produktivitas padi
#
# **Data:** `data/uts_3.csv`. **Satu baris:** satu wilayah pertanian pada contoh latihan.
#
# | Variabel/kolom | Pengertian | Satuan atau kode | Peran |
# |---|---|---|---|
# | `Y_Produktivitas_Padi` | Hasil panen padi per luas lahan. | Produktivitas per hektar; skala massa tidak dirinci sumber | Y: target |
# | `X1_Jumlah_Pupuk` | Banyaknya pupuk yang digunakan pada pertanian. | Jumlah pupuk; satuan/cakupan luas tidak dirinci | X: penjelas |
# | `X2_Curah_Hujan` | Banyaknya hujan pada wilayah pertanian. | Satuan/periode tidak dirinci sumber | X: penjelas |
# | `X3_Sinar_Matahari` | Lama penyinaran matahari yang diterima lahan. | Jam; periode akumulasi tidak dirinci | X: penjelas |
#
# Sumber menyebut produktivitas per hektar, tetapi tidak merinci semua skala. Interpretasi dalam ton, kg, atau mm memerlukan konfirmasi metadata, bukan hanya dugaan dari angka.
#
# Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

# %%
# padi = pd.read_csv(URL_DATA + "uts_3.csv")
# X_padi = padi[["X1_Jumlah_Pupuk", "X2_Curah_Hujan", "X3_Sinar_Matahari"]]
# y_padi = padi["Y_Produktivitas_Padi"]
# model_padi = LinearRegression()
# model_padi.fit(X_padi, y_padi)
# print(model_padi.coef_)

# %% [markdown]
# Tulis kesimpulan Anda:
#
# - Variabel yang signifikan: ...
# - Tanda koefisiennya sesuai dugaan? (curah hujan diharapkan positif pada
#   rentang data ini; pupuk dan sinar bisa lemah) ...
# - Prediksi kalau pupuk 160, hujan 1900, sinar 230: ...

# %% [markdown]
# **Latihan 2: angka harapan hidup.** Data `data/uts_4.csv` berisi 50
# negara. Regresikan `Y_Angka_Harapan_Hidup` pada pengeluaran kesehatan,
# tingkat imunisasi, dan konsumsi kalori. Variabel mana yang signifikan?

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
# harapan = pd.read_csv(URL_DATA + "uts_4.csv")
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
