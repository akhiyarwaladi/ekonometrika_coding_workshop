# %% [markdown]
# # Kunci Lab 0: Mulai dari Nol
#
# Jawaban latihan Lab 0.

# %% [markdown]
# ## Persiapan: alamat data

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

# %% [markdown]
# ## Latihan 1 dan 2: baca data dan hitung rata-rata

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
harapan_hidup = pd.read_csv(URL_DATA + "uts_4.csv")
print("Jumlah observasi:", len(harapan_hidup))
harapan_hidup.head()

# %%
print(
    "Rata-rata harapan hidup :", round(harapan_hidup["Y_Angka_Harapan_Hidup"].mean(), 2)
)
print(
    "Rata-rata imunisasi     :", round(harapan_hidup["X2_Tingkat_Imunisasi"].mean(), 2)
)

# %% [markdown]
# ## Latihan 3: regresi sederhana

# %%
sampel_model = harapan_hidup[
    ["Y_Angka_Harapan_Hidup", "X1_Pengeluaran_Kesehatan"]
].dropna()
X_model = sampel_model[["X1_Pengeluaran_Kesehatan"]]
y_model = sampel_model["Y_Angka_Harapan_Hidup"]

model = LinearRegression()
model.fit(X_model, y_model)

koefisien_model = pd.Series(model.coef_, index=X_model.columns)
koefisien_model.loc["Intercept"] = model.intercept_

# Pelengkap statistik: standard error dan pengujian pada sampel yang sama.
uji_model = sm.OLS(
    y_model,
    sm.add_constant(X_model, has_constant="add").rename(columns={"const": "Intercept"}),
).fit()
print(koefisien_model.round(5))
print(uji_model.pvalues.round(4))

# %% [markdown]
# Kesimpulan: koefisien pengeluaran kesehatan 0,00243 dengan p-value
# 0,0000, jadi signifikan. Setiap tambahan satu unit pengeluaran kesehatan
# diiringi kenaikan harapan hidup 0,00243 tahun. R kuadrat model ini
# sekitar 0,91.
