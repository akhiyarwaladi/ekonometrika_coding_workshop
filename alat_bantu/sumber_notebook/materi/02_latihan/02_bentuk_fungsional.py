# %% [markdown]
# # Lab 2: Bentuk Fungsional Model Regresi
#
# **Durasi:** 90 menit
#
# Tujuan: memilih bentuk model yang sesuai dengan cerita ekonominya.
# Hubungan yang melengkung tidak boleh dipaksa jadi garis lurus.

# %% [markdown]
# **Posisi dalam alur workshop.** Melanjutkan Lab 1 yang berakhir dengan
# pertanyaan bentuk model. Setelah bentuk tepat, Lab 3 memeriksa
# asumsinya.

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
import statsmodels.api as sm
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", palette=["#2F5D50", "#C15937", "#D9A441", "#5B8A8F"])
plt.rcParams.update({"figure.dpi": 110, "axes.titleweight": "bold", "font.size": 11})

# %% [markdown]
# ## 1. Contoh terbimbing: fungsi produksi Cobb-Douglas
#
# Data `data/regresi_log.csv`: tenaga kerja (L), modal (K), dan produksi (Q)
# dari 30 observasi. Model yang diuji: $Q = A L^{\beta_1} K^{\beta_2}$.
# Setelah di-log, koefisiennya menjadi elastisitas.

# %% [markdown]
# <!-- kamus_variabel:regresi_log.csv -->
#
# ### Kenali data: Produksi, tenaga kerja, dan modal
#
# **Data:** `data/regresi_log.csv`. **Satu baris:** satu unit usaha/pengamatan dalam contoh produksi.
#
# Nama singkat di kode berasal dari penggantian nama kolom CSV; isi angkanya tetap sama.
#
# | Kolom CSV | Nama di kode | Pengertian | Satuan atau kode | Peran |
# |---|---|---|---|---|
# | `Observasi ke-` | `obs` | Nomor urut pengamatan. | Nomor identitas | Penanda, bukan besaran ekonomi |
# | `Tenaga Kerja (L)` | `L` | Input tenaga kerja untuk proses produksi (L = labor). | Jumlah tenaga kerja; cakupan waktu tidak dirinci | X: penjelas |
# | `Modal (K)` | `K` | Input modal yang digunakan untuk menghasilkan barang (K = capital). | Satuan/skala tidak dirinci sumber | X: penjelas |
# | `Produksi (Q)` | `Q` | Jumlah hasil produksi (Q = quantity/output). | Jumlah output; unit produk tidak dirinci | Y: target |
#
# Kolom turunan berikut dibuat saat praktik; kolom ini belum ada pada CSV awal.
#
# | Kolom turunan | Pengertian | Satuan/kode |
# |---|---|---|
# | `lnQ` | Logaritma alami dari produksi Q. | Skala logaritma |
# | `lnL` | Logaritma alami dari tenaga kerja L. | Skala logaritma |
# | `lnK` | Logaritma alami dari modal K. | Skala logaritma |
#
# Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

# %%
produksi = pd.read_csv(URL_DATA + "regresi_log.csv")
produksi = produksi.rename(
    columns={
        "Observasi ke-": "obs",
        "Tenaga Kerja (L)": "L",
        "Modal (K)": "K",
        "Produksi (Q)": "Q",
    }
)
produksi["lnQ"] = np.log(produksi["Q"])
produksi["lnL"] = np.log(produksi["L"])
produksi["lnK"] = np.log(produksi["K"])

sampel_model = produksi[["lnQ", "lnL", "lnK"]].dropna()
X_model = sampel_model[["lnL", "lnK"]]
y_model = sampel_model["lnQ"]

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
# - Elastisitas tenaga kerja sekitar 0,86: tambahan tenaga kerja 1 persen
#   menaikkan produksi sekitar 0,86 persen.
# - Elastisitas modal sekitar 0,61.
# - Jumlahnya 1,47 (lebih besar dari 1): skala pengembalian meningkat
#   (increasing returns to scale).

# %%
b = koefisien_model
print(f"Elastisitas tenaga kerja : {b['lnL']:.3f}")
print(f"Elastisitas modal        : {b['lnK']:.3f}")
print(f"Jumlah (skala)           : {b['lnL'] + b['lnK']:.3f}")

# %% [markdown]
# ### Coba sendiri (5 menit)
#
# Pakai model Cobb-Douglas di atas. Hitung prediksi produksi untuk
# L = 60 dan K = 120 (ingat: hasilnya dalam bentuk log, perlu di-exp).
#
# Tulis di sel di bawah, baru buka jawabannya.

# %%
# Tulis kode Anda di sini

# %% [markdown]
# <details><summary>Lihat jawaban</summary>
#
# ln Q = -1,99 + 0,86 x ln(60) + 0,61 x ln(120) = 4,46, jadi
# Q = exp(4,46) sekitar 86,5.
#
# </details>

# %% [markdown]
# ## 2. Latihan mandiri
#
# **Latihan 1: pendidikan dan pendapatan.** Data
# `data/pendidikan_pendapatan.csv` berisi 30 responden.
#
# Dugaan di soal: setiap tambahan tahun pendidikan menaikkan pendapatan
# dalam persen, bukan nominal tetap. Model yang cocok: log-lin.
#
# `ln(Pendapatan) ~ Tahun_Pendidikan`
#
# Pertanyaan: berapa persen kenaikan pendapatan per satu tahun tambahan
# pendidikan? (Petunjuk: koefisien dikali 100.)

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
# didik = pd.read_csv(URL_DATA + "pendidikan_pendapatan.csv")
# didik["ln_pendapatan"] = np.log(didik["Pendapatan_Tahunan"])
# sampel_model_didik = didik[["ln_pendapatan", "Tahun_Pendidikan"]].dropna()
# X_model_didik = sampel_model_didik[["Tahun_Pendidikan"]]
# y_model_didik = sampel_model_didik["ln_pendapatan"]
#
# model_didik = LinearRegression()
# model_didik.fit(X_model_didik, y_model_didik)
#
# # Pelengkap statistik: standard error dan pengujian pada sampel yang sama.
# uji_model_didik = sm.OLS(
#     y_model_didik,
#     sm.add_constant(X_model_didik, has_constant="add").rename(
#         columns={"const": "Intercept"}
#     ),
# ).fit()
# print(uji_model_didik.summary())

# %% [markdown]
# **Latihan 2: usia dan kinerja penjualan.** Data `data/usia_unit.csv`.
# Hipotesisnya: kinerja naik seiring usia, memuncak, lalu menurun. Pakai
# model kuadratik, lalu hitung usia puncaknya dengan rumus
# $-b_1 / (2 b_2)$.
#
# Pertanyaan: pada usia berapa kinerja mencapai puncak?

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
# usia = pd.read_csv(URL_DATA + "usia_unit.csv")
# usia["usia2"] = usia["Usia"] ** 2
# sampel_model_usia = usia[["Unit_Terjual", "Usia", "usia2"]].dropna()
# X_model_usia = sampel_model_usia[["Usia", "usia2"]]
# y_model_usia = sampel_model_usia["Unit_Terjual"]
#
# model_usia = LinearRegression()
# model_usia.fit(X_model_usia, y_model_usia)
#
# # Pelengkap statistik: standard error dan pengujian pada sampel yang sama.
# uji_model_usia = sm.OLS(
#     y_model_usia,
#     sm.add_constant(X_model_usia, has_constant="add").rename(
#         columns={"const": "Intercept"}
#     ),
# ).fit()
# print(uji_model_usia.summary())

# %% [markdown]
# **Latihan 3: jam belajar dan skor ujian.** Data `data/jam_skor.csv`.
# Ada efek jenuh: tambahan jam belajar makin kecil manfaatnya, dan ada
# batas skor maksimal. Model yang cocok: reciprocal,
# `Skor_Ujian ~ 1/X` dengan X = Jam_Belajar.
#
# Pertanyaan: berapa batas skor maksimal (asimtot) yang dibaca dari
# intersep? (Petunjuk: intersep adalah batas atas skor.)

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
# skor = pd.read_csv(URL_DATA + "jam_skor.csv")
# skor["satu_per_jam"] = 1 / skor["Jam_Belajar"]
# sampel_model_skor = skor[["Skor_Ujian", "satu_per_jam"]].dropna()
# X_model_skor = sampel_model_skor[["satu_per_jam"]]
# y_model_skor = sampel_model_skor["Skor_Ujian"]
#
# model_skor = LinearRegression()
# model_skor.fit(X_model_skor, y_model_skor)
#
# # Pelengkap statistik: standard error dan pengujian pada sampel yang sama.
# uji_model_skor = sm.OLS(
#     y_model_skor,
#     sm.add_constant(X_model_skor, has_constant="add").rename(
#         columns={"const": "Intercept"}
#     ),
# ).fit()
# print(uji_model_skor.summary())

# %% [markdown]
# **Latihan 4: pilih bentuk untuk data UTS.** Data `data/uts_1.csv`:
# pertumbuhan ekonomi, investasi, inflasi, dan keterbukaan perdagangan.
# Coba tiga bentuk: linear, log-log, dan kuadratik untuk investasi.
# Bandingkan R kuadrat terkoreksi dan p-value. Kriteria: pilih model
# dengan R kuadrat terkoreksi tertinggi di antara model yang tanda
# koefisiennya sesuai teori. Kalau dua model berdekatan, dahulukan yang
# lebih sederhana dan lebih mudah dijelaskan.

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
# Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

# %%
# uts1 = pd.read_csv(URL_DATA + "uts_1.csv")
# sampel_model_lin = uts1[
#     [
#         "Y_Pertumbuhan_Ekonomi",
#         "X1_Investasi",
#         "X2_Inflasi",
#         "X3_Keterbukaan_Perdagangan",
#     ]
# ].dropna()
# X_model_lin = sampel_model_lin[
#     ["X1_Investasi", "X2_Inflasi", "X3_Keterbukaan_Perdagangan"]
# ]
# y_model_lin = sampel_model_lin["Y_Pertumbuhan_Ekonomi"]
#
# model_lin = LinearRegression()
# model_lin.fit(X_model_lin, y_model_lin)
# ...

# %% [markdown]
# ### Selanjutnya
#
# Selanjutnya: Lab 3, uji asumsi klasik.
