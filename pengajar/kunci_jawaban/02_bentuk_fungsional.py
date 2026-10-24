# %% [markdown]
# # Kunci Lab 2: Bentuk Fungsional

# %% [markdown]
# ## Persiapan: pastikan data tersedia
#
# Jalankan sel di bawah sekali supaya folder `data/` siap dipakai.

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

# %%
import pandas as pd
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
import numpy as np

# %% [markdown]
# ## Latihan 1: pendidikan dan pendapatan (log-lin)

# %% [markdown]
# <!-- kamus_variabel:pendidikan_pendapatan.csv -->
#
# ### Kenali data: Pendidikan dan pendapatan
#
# **Data:** `data/pendidikan_pendapatan.csv`. **Satu baris:** satu responden.
#
# | Variabel/kolom | Pengertian | Satuan atau kode | Peran |
# |---|---|---|---|
# | `Tahun_Pendidikan` | Total lama pendidikan yang telah ditempuh. | Tahun | X: penjelas |
# | `Pendapatan_Tahunan` | Pendapatan yang diterima selama satu tahun. | Juta rupiah per tahun | Y: target |
#
# Kolom turunan berikut dibuat saat praktik; kolom ini belum ada pada CSV awal.
#
# | Kolom turunan | Pengertian | Satuan/kode |
# |---|---|---|
# | `ln_pendapatan` | Logaritma alami dari Pendapatan_Tahunan. | Skala logaritma |
#
# Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

# %%
didik = pd.read_csv("data/pendidikan_pendapatan.csv")
didik["ln_pendapatan"] = np.log(didik["Pendapatan_Tahunan"])

sampel_model_didik = didik[["ln_pendapatan", "Tahun_Pendidikan"]].dropna()
X_model_didik = sampel_model_didik[["Tahun_Pendidikan"]]
y_model_didik = sampel_model_didik["ln_pendapatan"]

model_didik = LinearRegression()
model_didik.fit(X_model_didik, y_model_didik)

koefisien_model_didik = pd.Series(model_didik.coef_, index=X_model_didik.columns)
koefisien_model_didik.loc["Intercept"] = model_didik.intercept_
print(koefisien_model_didik.round(4))
print(
    "Kenaikan pendapatan per tahun pendidikan (persen):",
    round(100 * koefisien_model_didik["Tahun_Pendidikan"], 2),
)

# %%
# Pembanding: model linear biasa
sampel_model_linear = didik[["Pendapatan_Tahunan", "Tahun_Pendidikan"]].dropna()
X_model_linear = sampel_model_linear[["Tahun_Pendidikan"]]
y_model_linear = sampel_model_linear["Pendapatan_Tahunan"]

model_linear = LinearRegression()
model_linear.fit(X_model_linear, y_model_linear)
print("R2 log-lin:", round(model_didik.score(X_model_didik, y_model_didik), 4))
print("R2 linear :", round(model_linear.score(X_model_linear, y_model_linear), 4))

# %% [markdown]
# Kesimpulan: setiap tambahan satu tahun pendidikan menaikkan pendapatan
# sekitar 21,4 persen menurut pendekatan 100 x beta. Perubahan eksaknya
# adalah 100 x (exp(beta) - 1), sekitar 23,9 persen. Model log-lin memberi
# interpretasi proporsional; periksa apakah ini sesuai teori dan residual.
# R kuadrat 0,994 dan 0,884 tidak boleh dibandingkan langsung karena Y
# pada model log-lin dan linear berada pada skala yang berbeda.

# %% [markdown]
# ## Latihan 2: usia dan kinerja (kuadratik)

# %% [markdown]
# <!-- kamus_variabel:usia_unit.csv -->
#
# ### Kenali data: Usia dan kinerja penjual
#
# **Data:** `data/usia_unit.csv`. **Satu baris:** satu tenaga penjual.
#
# | Variabel/kolom | Pengertian | Satuan atau kode | Peran |
# |---|---|---|---|
# | `Usia` | Umur tenaga penjual. | Tahun | X: penjelas |
# | `Unit_Terjual` | Jumlah penjualan bulanan pada contoh kinerja penjual. | Unit per bulan, berupa angka simulasi | Y: target |
#
# Kolom turunan berikut dibuat saat praktik; kolom ini belum ada pada CSV awal.
#
# | Kolom turunan | Pengertian | Satuan/kode |
# |---|---|---|
# | `usia2` | Kuadrat usia: usia × usia. | Tahun kuadrat |
#
# Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

# %%
usia = pd.read_csv("data/usia_unit.csv")
usia["usia2"] = usia["Usia"] ** 2

sampel_model_usia = usia[["Unit_Terjual", "Usia", "usia2"]].dropna()
X_model_usia = sampel_model_usia[["Usia", "usia2"]]
y_model_usia = sampel_model_usia["Unit_Terjual"]

model_usia = LinearRegression()
model_usia.fit(X_model_usia, y_model_usia)

koefisien_model_usia = pd.Series(model_usia.coef_, index=X_model_usia.columns)
koefisien_model_usia.loc["Intercept"] = model_usia.intercept_
print(koefisien_model_usia.round(3))

b1 = koefisien_model_usia["Usia"]
b2 = koefisien_model_usia["usia2"]
print("Usia puncak:", round(-b1 / (2 * b2), 2), "tahun")

# %% [markdown]
# Kesimpulan: kinerja memuncak di usia sekitar 39,5 tahun. Koefisien `usia2`
# negatif, itulah yang membuat kurva melengkung ke bawah.

# %% [markdown]
# ## Latihan 3: jam belajar dan skor (reciprocal)

# %% [markdown]
# <!-- kamus_variabel:jam_skor.csv -->
#
# ### Kenali data: Jam belajar dan hasil ujian
#
# **Data:** `data/jam_skor.csv`. **Satu baris:** satu siswa/responden.
#
# | Variabel/kolom | Pengertian | Satuan atau kode | Peran |
# |---|---|---|---|
# | `Jam_Belajar` | Total waktu belajar yang dicatat pada contoh. | Jam | X: penjelas |
# | `Skor_Ujian` | Nilai/skor hasil ujian. | Poin skor; batas maksimum akan ditaksir dalam latihan | Y: target |
#
# Kolom turunan berikut dibuat saat praktik; kolom ini belum ada pada CSV awal.
#
# | Kolom turunan | Pengertian | Satuan/kode |
# |---|---|---|
# | `satu_per_jam` | Kebalikan jam belajar: 1 / Jam_Belajar. | Per jam |
#
# Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

# %%
skor = pd.read_csv("data/jam_skor.csv")
skor["satu_per_jam"] = 1 / skor["Jam_Belajar"]

sampel_model_skor = skor[["Skor_Ujian", "satu_per_jam"]].dropna()
X_model_skor = sampel_model_skor[["satu_per_jam"]]
y_model_skor = sampel_model_skor["Skor_Ujian"]

model_skor = LinearRegression()
model_skor.fit(X_model_skor, y_model_skor)

koefisien_model_skor = pd.Series(model_skor.coef_, index=X_model_skor.columns)
koefisien_model_skor.loc["Intercept"] = model_skor.intercept_
print(koefisien_model_skor.round(2))

# %% [markdown]
# Kesimpulan: batas skor maksimal (asimtot) sekitar 99,7, dibaca dari
# intersep. Koefisien `satu_per_jam` negatif dan besar, artinya tambahan
# jam belajar membantu, tapi manfaatnya mengecil dan skor mendekati batas
# 99,7.

# %% [markdown]
# ## Latihan 4: memilih bentuk untuk data UTS-1

# %% [markdown]
# <!-- kamus_variabel:uts_1.csv -->
#
# ### Kenali data: Pertumbuhan ekonomi
#
# **Data:** `data/uts_1.csv`. **Satu baris:** satu negara pada contoh 50 negara berkembang.
#
# | Variabel/kolom | Pengertian | Satuan atau kode | Peran |
# |---|---|---|---|
# | `Y_Pertumbuhan_Ekonomi` | Laju pertumbuhan kegiatan ekonomi/PDB. | Persen | Y: target |
# | `X1_Investasi` | Besarnya investasi dibandingkan PDB. | Persen dari PDB | X: penjelas |
# | `X2_Inflasi` | Laju kenaikan tingkat harga. | Persen | X: penjelas |
# | `X3_Keterbukaan_Perdagangan` | Ukuran keterbukaan perdagangan relatif terhadap PDB. | Persen dari PDB | X: penjelas |
#
# Rumus rinci ukuran keterbukaan tidak dicantumkan pada tabel sumber; jangan menganggapnya nilai ekspor saja.
#
# Kolom turunan berikut dibuat saat praktik; kolom ini belum ada pada CSV awal.
#
# | Kolom turunan | Pengertian | Satuan/kode |
# |---|---|---|
# | `ln_y` | Logaritma alami pertumbuhan ekonomi yang bernilai positif. | Skala logaritma |
# | `ln_inv` | Logaritma alami tingkat investasi. | Skala logaritma |
# | `ln_inflasi` | Logaritma alami tingkat inflasi yang bernilai positif. | Skala logaritma |
# | `ln_terbuka` | Logaritma alami ukuran keterbukaan perdagangan. | Skala logaritma |
#
# Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

# %%
uts1 = pd.read_csv("data/uts_1.csv")

# Linear
sampel_model_lin = uts1[
    [
        "Y_Pertumbuhan_Ekonomi",
        "X1_Investasi",
        "X2_Inflasi",
        "X3_Keterbukaan_Perdagangan",
    ]
].dropna()
X_model_lin = sampel_model_lin[
    ["X1_Investasi", "X2_Inflasi", "X3_Keterbukaan_Perdagangan"]
]
y_model_lin = sampel_model_lin["Y_Pertumbuhan_Ekonomi"]

model_lin = LinearRegression()
model_lin.fit(X_model_lin, y_model_lin)

# Pelengkap statistik: standard error dan pengujian pada sampel yang sama.
uji_model_lin = sm.OLS(
    y_model_lin,
    sm.add_constant(X_model_lin, has_constant="add").rename(
        columns={"const": "Intercept"}
    ),
).fit()

# Log-log
uts1["ln_y"] = np.log(uts1["Y_Pertumbuhan_Ekonomi"])
uts1["ln_inv"] = np.log(uts1["X1_Investasi"])
uts1["ln_inflasi"] = np.log(uts1["X2_Inflasi"])
uts1["ln_terbuka"] = np.log(uts1["X3_Keterbukaan_Perdagangan"])
sampel_model_log = uts1[["ln_y", "ln_inv", "ln_inflasi", "ln_terbuka"]].dropna()
X_model_log = sampel_model_log[["ln_inv", "ln_inflasi", "ln_terbuka"]]
y_model_log = sampel_model_log["ln_y"]

model_log = LinearRegression()
model_log.fit(X_model_log, y_model_log)

# Pelengkap statistik: standard error dan pengujian pada sampel yang sama.
uji_model_log = sm.OLS(
    y_model_log,
    sm.add_constant(X_model_log, has_constant="add").rename(
        columns={"const": "Intercept"}
    ),
).fit()

print("R2 linear:", round(model_lin.score(X_model_lin, y_model_lin), 4))
print("R2 log-log:", round(model_log.score(X_model_log, y_model_log), 4))
print("p-value linear:")
print(uji_model_lin.pvalues.round(4))
print("p-value log-log:")
print(uji_model_log.pvalues.round(4))

# %% [markdown]
# Kesimpulan: kedua R kuadrat berada pada skala Y yang berbeda, sehingga
# tidak digunakan sebagai dasar perbandingan langsung. Model linear menampilkan inflasi dan keterbukaan sebagai
# signifikan; model log-log hanya keterbukaan. Pilihan terakhir tetap
# bergantung teori: kalau ingin membaca elastisitas, pakai log-log.
