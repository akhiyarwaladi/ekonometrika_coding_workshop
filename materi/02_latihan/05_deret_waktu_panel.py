# %% [markdown]
# # Lab 5: Deret Waktu dan Data Panel
#
# **Durasi:** 90 menit
#
# Tujuan: menguji stasioneritas, meramal dengan ARIMA, menguji
# kointegrasi, dan menaksir model data panel.

# %% [markdown]
# **Posisi dalam alur workshop.** Menambah dimensi waktu dan individu ke
# model. Lab 6 menutup dengan data Indonesia asli.

# %% [markdown]
# ## Persiapan: alamat data
#
# Jalankan sel alamat data di bawah. `URL_DATA` menyimpan alamat folder CSV di GitHub;
# `pd.read_csv(...)` membaca tabel sesuai nama CSV pada sel kode berikutnya.
# Gunakan koneksi internet dan jalankan sel berurutan dengan **Shift + Enter**. Paket `linearmodels` dipasang di sel berikutnya
# (butuh internet sekali saja).

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
%pip install "linearmodels==7.1" -q

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
# ## 1. Stasioneritas dan ARIMA
#
# Data `data/ts_inflasi.csv`: indeks harga 50 periode yang naik terus.
# Langkah pertama selalu melihat plot.

# %% [markdown]
# <!-- kamus_variabel:ts_inflasi.csv -->
#
# ### Kenali data: Deret harga/inflasi simulasi
#
# **Data:** `data/ts_inflasi.csv`. **Satu baris:** satu urutan periode simulasi; bukan tanggal kalender.
#
# | Variabel/kolom | Pengertian | Satuan atau kode | Peran |
# |---|---|---|---|
# | `obs` | Urutan waktu pengamatan. | 1, 2, 3, ...; frekuensi kalender tidak dirinci | Penanda waktu |
# | `inflasi` | Deret level bertendensi naik, dicontohkan sebagai IHK pada sumber. | Level/indeks simulasi; bukan otomatis persen inflasi | Deret yang dianalisis |
#
# Nomor obs tidak menunjukkan tanggal/bulan/tahun tertentu. Angka level dan perubahan persennya harus dibedakan.
#
# Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

# %%
inflasi = pd.read_csv(URL_DATA + "ts_inflasi.csv")

plt.figure(figsize=(9, 4))
plt.plot(inflasi["obs"], inflasi["inflasi"], lw=1.6)
plt.title("Inflasi: tren naik terus")
plt.xlabel("Periode")
plt.show()

# %%
from statsmodels.tsa.stattools import adfuller

p_level = adfuller(inflasi["inflasi"])[1]
p_diff = adfuller(inflasi["inflasi"].diff().dropna())[1]
print(f"ADF di level          : p = {p_level:.4f}")
print(f"ADF setelah selisih   : p = {p_diff:.4f}")

# %% [markdown]
# ### Membaca hasil
#
# Di level, p-value besar: data tidak stasioner (ada tren). Setelah satu
# kali selisih, p-value kecil: sudah stasioner. Kesimpulan: pakai d = 1.
#
# Model ARIMA(1,1,0) artinya: satu kali selisih, satu komponen AR.

# %%
from statsmodels.tsa.arima.model import ARIMA

model = ARIMA(inflasi["inflasi"], order=(1, 1, 0)).fit()
print(model.summary())

# %%
ramalan = model.get_forecast(steps=5)
print("Ramalan inflasi 5 periode ke depan:")
print(np.asarray(ramalan.predicted_mean).round(2))

plt.figure(figsize=(9, 4))
plt.plot(inflasi["obs"], inflasi["inflasi"], label="aktual")
masa_depan = np.arange(51, 56)
plt.plot(masa_depan, np.asarray(ramalan.predicted_mean), marker="o", label="ramalan")
plt.legend()
plt.title("Ramalan inflasi")
plt.show()

# %% [markdown]
# ## 2. Kointegrasi dan ECM
#
# Data `data/konsumsi_pendapatan.csv`. Dua variabel yang sama-sama
# tidak stasioner bisa tetap berjalan bersama dalam jangka panjang.

# %% [markdown]
# <!-- kamus_variabel:konsumsi_pendapatan.csv -->
#
# ### Kenali data: Konsumsi dan pendapatan runtun waktu
#
# **Data:** `data/konsumsi_pendapatan.csv`. **Satu baris:** satu tahun berurutan pada data simulasi.
#
# Nama singkat di kode berasal dari penggantian nama kolom CSV; isi angkanya tetap sama.
#
# | Kolom CSV | Nama di kode | Pengertian | Satuan atau kode | Peran |
# |---|---|---|---|---|
# | `Tahun` | `Tahun` | Nomor tahun dalam urutan simulasi, bukan tahun kalender. | 1, 2, 3, ... | Penanda waktu |
# | `Konsumsi_Y` | `konsumsi` | Nilai konsumsi pada periode tersebut. | Skala uang tidak dirinci | Y: target |
# | `Pendapatan_X` | `pendapatan` | Nilai pendapatan pada periode yang sama. | Skala uang tidak dirinci | X: penjelas |
#
# Kolom turunan berikut dibuat saat praktik; kolom ini belum ada pada CSV awal.
#
# | Kolom turunan | Pengertian | Satuan/kode |
# |---|---|---|
# | `ln_konsumsi` | Logaritma alami nilai konsumsi. | Skala logaritma |
# | `ln_pendapatan` | Logaritma alami nilai pendapatan. | Skala logaritma |
# | `d_konsumsi` | Selisih log konsumsi dari periode sebelumnya. | Perubahan log, belum dikalikan 100 |
# | `d_pendapatan` | Selisih log pendapatan dari periode sebelumnya. | Perubahan log, belum dikalikan 100 |
# | `ect` | Error Correction Term: penyimpangan dari hubungan jangka panjang pada periode sebelumnya. | Residual log periode sebelumnya |
#
# Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

# %%
from statsmodels.tsa.stattools import coint

makro = pd.read_csv(URL_DATA + "konsumsi_pendapatan.csv")
makro = makro.rename(columns={"Konsumsi_Y": "konsumsi", "Pendapatan_X": "pendapatan"})
makro["ln_konsumsi"] = np.log(makro["konsumsi"])
makro["ln_pendapatan"] = np.log(makro["pendapatan"])

print("ADF level:")
print("  ln(konsumsi)  :", round(adfuller(makro["ln_konsumsi"])[1], 4))
print("  ln(pendapatan):", round(adfuller(makro["ln_pendapatan"])[1], 4))

# %% [markdown]
# **Batas contoh simulasi ini.** ADF dengan konstanta pada log kedua seri
# memberi p sekitar 0,023 dan 0,013: akar unit sudah ditolak pada level.
# Jadi hasil coint di bawah tidak cukup untuk menyatakan kedua seri I(1)
# terkointegrasi. Perhitungan berikut memperagakan bentuk persamaan jangka
# panjang dan komponen ECM, bukan bukti empiris kointegrasi yang sah.
# Untuk penelitian, tetapkan tren/konstanta berdasarkan teori dan grafik,
# periksa orde integrasi, lalu gunakan uji kointegrasi yang sesuai.

# %%
p_kointe = coint(makro["ln_konsumsi"], makro["ln_pendapatan"])[1]
print(f"\nUji kointegrasi: p = {p_kointe:.4f}")
print("ECM berikut adalah demonstrasi; syarat I(1) belum terpenuhi pada contoh ini.")

# %%
sampel_model_lr = makro[["ln_konsumsi", "ln_pendapatan"]].dropna()
X_model_lr = sampel_model_lr[["ln_pendapatan"]]
y_model_lr = sampel_model_lr["ln_konsumsi"]

model_lr = LinearRegression()
model_lr.fit(X_model_lr, y_model_lr)

koefisien_model_lr = pd.Series(model_lr.coef_, index=X_model_lr.columns)
koefisien_model_lr.loc["Intercept"] = model_lr.intercept_

prediksi_model_lr = pd.Series(model_lr.predict(X_model_lr), index=y_model_lr.index)
residu_model_lr = y_model_lr - prediksi_model_lr
print("Persamaan jangka panjang:")
print(koefisien_model_lr.round(3))

# %%
# Siapkan komponen ECM: selisih untuk efek jangka pendek
makro["d_konsumsi"] = makro["ln_konsumsi"].diff()
makro["d_pendapatan"] = makro["ln_pendapatan"].diff()
# ECT = residual jangka panjang periode sebelumnya (koreksi ketidakseimbangan)
makro["ect"] = residu_model_lr.shift(1)

sampel_model_ecm = makro[["d_konsumsi", "d_pendapatan", "ect"]].dropna()
X_model_ecm = sampel_model_ecm[["d_pendapatan", "ect"]]
y_model_ecm = sampel_model_ecm["d_konsumsi"]

model_ecm = LinearRegression()
model_ecm.fit(X_model_ecm, y_model_ecm)

koefisien_model_ecm = pd.Series(model_ecm.coef_, index=X_model_ecm.columns)
koefisien_model_ecm.loc["Intercept"] = model_ecm.intercept_

# Pelengkap statistik: standard error dan pengujian pada sampel yang sama.
uji_model_ecm = sm.OLS(
    y_model_ecm,
    sm.add_constant(X_model_ecm, has_constant="add").rename(
        columns={"const": "Intercept"}
    ),
).fit()
print("\nECM:")
print(koefisien_model_ecm.round(3))
print(uji_model_ecm.pvalues.round(4))

# %% [markdown]
# ### Membaca hasil
#
# Koefisien `ect` = -0,70 dan signifikan. Artinya 70 persen
# ketidakseimbangan periode sebelumnya dikoreksi pada periode ini, menuju
# keseimbangan jangka panjang.

# %% [markdown]
# ## 3. Data panel
#
# Data `data/panel_padi.csv`: 5 petak sawah x 10 musim. Hasil panen
# dijelaskan pupuk dan curah hujan. Dengan struktur panel, kita bisa
# memisahkan pengaruh yang melekat pada tiap petak.

# %% [markdown]
# <!-- kamus_variabel:panel_padi.csv -->
#
# ### Kenali data: Panel hasil panen padi
#
# **Data:** `data/panel_padi.csv`. **Satu baris:** satu petak sawah pada satu musim tanam.
#
# | Variabel/kolom | Pengertian | Satuan atau kode | Peran |
# |---|---|---|---|
# | `FarmID` | Kode petak sawah yang diamati berulang. | Nomor identitas lahan | Penanda, bukan besaran ekonomi |
# | `Season` | Urutan musim tanam. | Musim tanam ke-1, ke-2, ... | Penanda waktu |
# | `Yield_Y` | Jumlah gabah yang dihasilkan oleh petak sawah. | Ton gabah; bukan otomatis ton per hektar | Y: target |
# | `Fertilizer_X1` | Banyaknya pupuk yang digunakan. | Kilogram (kg) | X: penjelas |
# | `Rainfall_X2` | Banyaknya curah hujan pada musim tanam. | Milimeter (mm) | X: penjelas |
#
# Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

# %%
from linearmodels.panel import PanelOLS

padi = pd.read_csv(URL_DATA + "panel_padi.csv")
padi = padi.set_index(["FarmID", "Season"])
y = padi["Yield_Y"]
X = padi[["Fertilizer_X1", "Rainfall_X2"]]

fem = PanelOLS(y, X, entity_effects=True).fit(cov_type="clustered", cluster_entity=True)
print(fem.summary)

# %%
print("Uji Chow (pooled vs fixed effect):")
print(fem.f_pooled)

# %% [markdown]
# ### Membaca hasil
#
# p-value uji Chow sangat kecil: efek individu petak sawah nyata, jadi
# Fixed Effect lebih tepat daripada mencampur semua petak. Koefisien
# pupuk sekitar 0,038: tambahan satu kg pupuk per hektar menaikkan hasil
# sekitar 0,038 ton per hektar dalam petak yang sama.

# %% [markdown]
# ### Coba sendiri (5 menit)
#
# Jalankan CEM (tanpa `entity_effects`) untuk data padi. Bandingkan
# koefisien pupuknya dengan FEM di atas. Kenapa berbeda?
#
# Tulis di sel di bawah, baru buka jawabannya.

# %%
# Tulis kode Anda di sini

# %% [markdown]
# <details><summary>Lihat jawaban</summary>
#
# CEM memberi koefisien pupuk 0,0507, FEM 0,0382. CEM mencampur
# perbedaan antar petak sawah dengan perubahan dalam satu petak,
# sehingga angkanya lebih besar. FEM lebih tepat untuk pertanyaan
# perubahan dalam petak yang sama.
#
# </details>

# %% [markdown]
# ## 4. Latihan mandiri
#
# **Latihan 1: ADF dan ARIMA untuk saham.** Data `data/ts_saham.csv`.
# - Cek ADF di level dan setelah selisih. Stasioner di level atau setelah
#   selisih?
# - Estimasi ARIMA(1,1,0) dan ramalkan 5 periode.

# %% [markdown]
# <!-- kamus_variabel:ts_saham.csv -->
#
# ### Kenali data: Harga saham simulasi
#
# **Data:** `data/ts_saham.csv`. **Satu baris:** satu urutan periode simulasi; bukan tanggal kalender.
#
# | Variabel/kolom | Pengertian | Satuan atau kode | Peran |
# |---|---|---|---|
# | `obs` | Urutan waktu pengamatan. | 1, 2, 3, ...; frekuensi kalender tidak dirinci | Penanda waktu |
# | `saham` | Deret harga saham simulasi untuk uji stasioneritas dan peramalan. | Level harga; skala uang tidak dirinci | Deret yang dianalisis |
#
# Nomor obs tidak menunjukkan tanggal/bulan/tahun tertentu. Angka level dan perubahan persennya harus dibedakan.
#
# Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

# %%
# saham_ts = pd.read_csv(URL_DATA + "ts_saham.csv")
# ...

# %% [markdown]
# **Latihan 2: kointegrasi IHSG dan emas.** Data `data/ihsg_emas.csv`.
# - Jalankan uji `coint(IHSG_Y, Emas_X)`.
# - Kalau p < 0,05, estimasi ECM. Kalau tidak, jelaskan kenapa ECM
#   sebaiknya tidak dipakai.

# %% [markdown]
# <!-- kamus_variabel:ihsg_emas.csv -->
#
# ### Kenali data: IHSG dan harga emas simulasi
#
# **Data:** `data/ihsg_emas.csv`. **Satu baris:** satu bulan berurutan pada contoh simulasi.
#
# | Variabel/kolom | Pengertian | Satuan atau kode | Peran |
# |---|---|---|---|
# | `Bulan` | Urutan bulan pengamatan. | Nomor bulan; tanggal kalender tidak dicantumkan | Penanda waktu |
# | `IHSG_Y` | Indeks Harga Saham Gabungan dalam contoh simulasi. | Poin indeks | Y: target |
# | `Emas_X` | Harga emas pada contoh simulasi. | Mata uang dan berat acuan tidak dirinci | X: penjelas |
#
# Tabel ini adalah contoh simulasi; berbeda dari data IHSG harian unduhan Yahoo Finance.
#
# Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

# %%
# ie = pd.read_csv(URL_DATA + "ihsg_emas.csv")
# ...

# %% [markdown]
# **Latihan 3: panel retail.** Data `data/panel_retail.csv`
# (5 toko x 10 bulan, `Sales_Y ~ Ads_X1 + Discount_X2`).
# - Estimasi CEM (tanpa `entity_effects`) dan FEM (dengan
#   `entity_effects=True`).
# - Bandingkan koefisien diskon di kedua model. Mana yang Anda percaya
#   untuk kebijakan diskon? Kenapa?

# %% [markdown]
# <!-- kamus_variabel:panel_retail.csv -->
#
# ### Kenali data: Panel toko ritel
#
# **Data:** `data/panel_retail.csv`. **Satu baris:** satu cabang toko pada satu bulan.
#
# | Variabel/kolom | Pengertian | Satuan atau kode | Peran |
# |---|---|---|---|
# | `StoreID` | Kode cabang toko. | Nomor identitas toko | Penanda, bukan besaran ekonomi |
# | `Month` | Urutan bulan dalam panel. | Bulan ke-1, ke-2, ... | Penanda waktu |
# | `Sales_Y` | Besarnya penjualan toko pada bulan tersebut. | Satuan/skala tidak dirinci sumber | Y: target |
# | `Ads_X1` | Biaya iklan cabang toko. | Satuan/skala tidak dirinci sumber | X: penjelas |
# | `Discount_X2` | Proporsi potongan harga. | Pecahan; 0,10 berarti diskon 10% | X: penjelas |
#
# Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

# %%
# retail = pd.read_csv(URL_DATA + "panel_retail.csv").set_index(["StoreID", "Month"])
# ...

# %% [markdown]
# ### Selanjutnya
#
# Selanjutnya: Lab 6, data Indonesia asli.
