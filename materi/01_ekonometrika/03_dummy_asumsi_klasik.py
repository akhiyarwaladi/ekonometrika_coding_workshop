# %% [markdown]
# # Hari 1, Sesi 3: Variabel Dummy dan Uji Asumsi Klasik
#
# **Durasi:** 90 menit
#
# Dua bagian besar. Pertama, variabel dummy untuk data kategorikal (gender,
# status, periode krisis). Kedua, empat uji asumsi klasik yang wajib bisa
# dijalankan dan ditafsirkan: multikolinearitas, heteroskedastisitas,
# normalitas, dan autokorelasi.
#
# Pola kerja yang dipakai sepanjang sesi:
#
# 1. Estimasi model OLS.
# 2. Jalankan uji diagnostik.
# 3. Kalau asumsi dilanggar, tangani dengan alat yang sesuai: robust
#    standard error (HC3) untuk heteroskedastisitas, HAC untuk
#    autokorelasi, dan buang atau gabungkan variabel untuk
#    multikolinearitas.
# 4. Baca hasil sesuai koreksi yang dipilih. HC3/HAC mempertahankan
#    koefisien OLS, tetapi standard error dan p-value dapat berubah.

# %% [markdown]
# **Posisi dalam alur workshop.** Setelah bentuk model tepat (Sesi 2),
# sekarang periksa apakah hasilnya layak dipercaya. Sesi berikutnya
# mengganti jenis variabel Y dari kontinu ke kategorikal.

# %% [markdown]
# ## Persiapan: pastikan data tersedia
#
# Notebook ini membaca CSV dari folder `data/`. Kalau belum ada (misalnya di
# Colab), unggah `data_tutorial.zip` lewat panel Files, lalu jalankan
# sel di bawah sekali.

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

# %% [markdown]
# ## 1. Variabel dummy
#
# Data `latihan_dummy_1.csv`: gaji, pengalaman, gender, dan status pernikahan
# 30 karyawan. Dua variabel terakhir kategorikal, jadi harus diubah ke angka
# dulu. Ini yang di EViews dilakukan otomatis lewat fitur dummy.

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
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", palette=["#2F5D50", "#C15937", "#D9A441", "#5B8A8F"])
plt.rcParams.update({"figure.dpi": 110, "axes.titleweight": "bold", "font.size": 11})

gaji = pd.read_csv("data/latihan_dummy_1.csv")
gaji = gaji.rename(
    columns={
        "GAJI": "gaji",
        "PENGALAMAN": "pengalaman",
        "GENDER": "gender",
        "STATUS": "status",
    }
)
gaji["gender"].value_counts(), gaji["status"].value_counts()

# %% [markdown]
# ### Dummy trap dan cara menghindarinya
#
# Kalau dua kategori (Pria/Wanita) dibuat dua kolom dummy, jumlah keduanya
# selalu 1. Kolom itu menjadi kombinasi linear sempurna dengan konstanta,
# dan OLS tidak bisa diestimasi. Solusinya: selalu buang satu kategori
# sebagai basis.
#
# `pd.get_dummies(..., drop_first=True)` melakukan ini otomatis, tapi
# kategori yang dibuang mengikuti urutan alfabet. Supaya kontrol tetap di
# tangan kita, di sini kolom dummy dibuat eksplisit. Basisnya: Wanita dan
# Lajang.

# %%
gaji_d = gaji.copy()
gaji_d["dummy_pria"] = (gaji_d["gender"] == "Pria").astype(int)
gaji_d["dummy_menikah"] = (gaji_d["status"] == "Menikah").astype(int)
gaji_d.head()

# %%
sampel_model_dummy_mentah = gaji_d[["gaji", "dummy_pria", "dummy_menikah"]].dropna()
X_model_dummy_mentah = sampel_model_dummy_mentah[["dummy_pria", "dummy_menikah"]]
y_model_dummy_mentah = sampel_model_dummy_mentah["gaji"]

model_dummy_mentah = LinearRegression()
model_dummy_mentah.fit(X_model_dummy_mentah, y_model_dummy_mentah)

# Pelengkap statistik: standard error dan pengujian pada sampel yang sama.
uji_model_dummy_mentah = sm.OLS(
    y_model_dummy_mentah,
    sm.add_constant(X_model_dummy_mentah, has_constant="add").rename(
        columns={"const": "Intercept"}
    ),
).fit()
print(uji_model_dummy_mentah.summary())

# %%
sampel_model_dummy = gaji_d[
    ["gaji", "pengalaman", "dummy_pria", "dummy_menikah"]
].dropna()
X_model_dummy = sampel_model_dummy[["pengalaman", "dummy_pria", "dummy_menikah"]]
y_model_dummy = sampel_model_dummy["gaji"]

model_dummy = LinearRegression()
model_dummy.fit(X_model_dummy, y_model_dummy)

# Pelengkap statistik: standard error dan pengujian pada sampel yang sama.
uji_model_dummy = sm.OLS(
    y_model_dummy,
    sm.add_constant(X_model_dummy, has_constant="add").rename(
        columns={"const": "Intercept"}
    ),
).fit()
print(uji_model_dummy.summary())

# %% [markdown]
# ### Menafsirkan dummy
#
# Basis di sini adalah Wanita dan Lajang. Di model mentah (tanpa kontrol),
# `dummy_pria` = +3,35 dan `dummy_menikah` = +7,05, keduanya signifikan.
# Setelah pengalaman kerja dikontrol, keduanya mengecil mendekati nol dan
# tidak lagi signifikan.
#
# Ini pelajaran penting: koefisien dummy adalah selisih antar kelompok
# SETELAH variabel lain dikontrol. Perbedaan mentah di data ini sebagian
# besar dijelaskan oleh pengalaman kerja yang berbeda antar kelompok.
# Model mana yang dilaporkan? Tergantung pertanyaan penelitian: untuk
# membandingkan perbedaan mentah antar kelompok, pakai model tanpa
# kontrol; untuk membandingkan kelompok dengan pengalaman yang setara,
# pakai model terkontrol. Yang tidak boleh: melaporkan model mentah lalu
# bicara seolah pengalaman sudah dikontrol.
#
# Intersep = rata-rata gaji kelompok basis saat pengalaman = 0.
# Di laporan, selalu sebut kategori basisnya secara eksplisit.

# %% [markdown]
# ## 2. Dummy untuk peristiwa: krisis ekonomi
#
# `latihan_dummy_2.csv`: PDB dan investasi tahunan, dengan dummy `KRISIS`
# bernilai 1 di tahun krisis. Model: `pdb ~ investasi + suku_bunga + krisis`.

# %% [markdown]
# <!-- kamus_variabel:latihan_dummy_2.csv -->
#
# ### Kenali data: PDB, investasi, dan krisis
#
# **Data:** `data/latihan_dummy_2.csv`. **Satu baris:** satu tahun pada contoh ekonomi simulasi.
#
# Nama singkat di kode berasal dari penggantian nama kolom CSV; isi angkanya tetap sama.
#
# | Kolom CSV | Nama di kode | Pengertian | Satuan atau kode | Peran |
# |---|---|---|---|---|
# | `Tahun` | `tahun` | Tahun kalender pengamatan. | Tahun | Penanda waktu |
# | `PDB` | `pdb` | Indikator PDB yang menjadi target contoh. | Skala PDB tidak dirinci sumber | Y: target |
# | `INVESTASI` | `investasi` | Besarnya investasi pada periode tersebut. | Skala investasi tidak dirinci sumber | X: penjelas |
# | `SUKU_BUNGA` | `suku_bunga` | Tingkat bunga pada periode tersebut. | Persen dalam konteks latihan | X: penjelas |
# | `KRISIS` | `krisis` | Penanda apakah pengamatan termasuk periode krisis pada data. | 1 = krisis; 0 = bukan krisis | X: penjelas |
#
# PDB pada nama kolom tidak otomatis berarti pertumbuhan PDB. Berkas tidak menyertakan metadata skala level/pertumbuhan; jangan menyamakannya dengan PDB_Growth World Bank.
#
# Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

# %%
krisis = pd.read_csv("data/latihan_dummy_2.csv")
krisis = krisis.rename(
    columns={
        "Tahun": "tahun",
        "PDB": "pdb",
        "INVESTASI": "investasi",
        "SUKU_BUNGA": "suku_bunga",
        "KRISIS": "krisis",
    }
)
sampel_model_krisis = krisis[["pdb", "investasi", "suku_bunga", "krisis"]].dropna()
X_model_krisis = sampel_model_krisis[["investasi", "suku_bunga", "krisis"]]
y_model_krisis = sampel_model_krisis["pdb"]

model_krisis = LinearRegression()
model_krisis.fit(X_model_krisis, y_model_krisis)

koefisien_model_krisis = pd.Series(model_krisis.coef_, index=X_model_krisis.columns)
koefisien_model_krisis.loc["Intercept"] = model_krisis.intercept_

prediksi_model_krisis = pd.Series(
    model_krisis.predict(X_model_krisis), index=y_model_krisis.index
)
residu_model_krisis = y_model_krisis - prediksi_model_krisis

# Pelengkap statistik: standard error dan pengujian pada sampel yang sama.
uji_model_krisis = sm.OLS(
    y_model_krisis,
    sm.add_constant(X_model_krisis, has_constant="add").rename(
        columns={"const": "Intercept"}
    ),
).fit()
print(uji_model_krisis.summary())

# %% [markdown]
# Koefisien `krisis` adalah perbedaan rata-rata PDB pada tahun krisis
# dibanding tahun normal, setelah investasi dan suku bunga dikontrol.
# Kalau negatif dan signifikan: krisis berdampak buruk, sesuai dugaan.

# %% [markdown]
# ### Coba sendiri (5 menit)
#
# Dengan model dummy di bagian 1, prediksi gaji untuk Wanita yang belum
# menikah dengan pengalaman 5 tahun.
#
# Tulis di sel di bawah, baru buka jawabannya.

# %%
# Tulis kode Anda di sini

# %% [markdown]
# <details><summary>Lihat jawaban</summary>
#
# Kedua dummy bernilai nol, jadi gajinya = intersep + 1,3489 x 5.
# Hasilnya sekitar 10,80 (satuan sama dengan kolom gaji).
#
# </details>

# %% [markdown]
# Bagian dummy selesai. Mulai di sini, kita kembali ke model OLS dengan
# variabel kontinu dan memeriksa satu per satu asumsi klasiknya.
#
# ## 3. Uji multikolinearitas
#
# Multikolinearitas = korelasi tinggi antar variabel penjelas. Akibatnya
# standard error membengkak, t-statistik mengecil, dan koefisien jadi tidak
# stabil. Deteksinya dengan VIF (Variance Inflation Factor).
#
# Aturan praktis: VIF di atas 10 menandakan masalah serius. Di antara 5 dan
# 10, perlu kehati-hatian.

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

rumah = pd.read_csv("data/latihan_multikolinieritas_1.csv")
rumah = rumah.rename(
    columns={
        "HARGA": "harga",
        "LUAS_BANGUNAN": "luas_bangunan",
        "LUAS_TANAH": "luas_tanah",
        "JML_KAMAR": "jml_kamar",
    }
)

X = sm.add_constant(rumah[["luas_bangunan", "luas_tanah", "jml_kamar"]])
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

# %% [markdown]
# Kalau `luas_bangunan` dan `luas_tanah` punya VIF besar, lihat korelasinya.
# Di data ini korelasinya 0,99. Sebagai patokan, korelasi antar penjelas
# di atas 0,8 sudah patut dicurigai.

# %%
rumah[["luas_bangunan", "luas_tanah", "jml_kamar"]].corr()

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
print(f"R2 = {model_rumah.score(X_model_rumah, y_model_rumah):.4f}")
print(uji_model_rumah.summary())

# %% [markdown]
# Perhatikan kombinasi yang khas: R kuadrat tinggi dan uji F signifikan,
# tapi koefisien satu per satu tidak signifikan. Ini gejala klasik
# multikolinearitas. Solusinya: buang salah satu variabel yang redundan,
# gabungkan keduanya, atau perbesar sampel.

# %% [markdown]
# ### Coba sendiri (5 menit)
#
# Hitung ulang VIF setelah `luas_tanah` dibuang. Apakah masalahnya selesai?
#
# Tulis di sel di bawah, baru buka jawabannya.

# %%
# Tulis kode Anda di sini

# %% [markdown]
# <details><summary>Lihat jawaban</summary>
#
# VIF tersisa: `luas_bangunan` 13,4 dan `jml_kamar` 13,4. Membaik dari
# 64 dan 45, tapi masih di atas 10 karena korelasinya 0,96. Langkah
# lanjut: pertimbangkan hanya memakai satu di antaranya.
#
# </details>

# %% [markdown]
# ## 4. Uji heteroskedastisitas
#
# Varians residual yang berubah-ubah sepanjang nilai X. Dampaknya: standard
# error OLS salah, sehingga uji t dan uji F tidak valid. Gejalanya sering
# terlihat di scatter residual vs fitted.
#
# Data `hetero_3.csv`: harga rumah dijelaskan luas bangunan, jumlah kamar,
# dan skor lokasi. Dugaan di soal: variasi harga jauh lebih besar untuk
# rumah luas di lokasi premium.

# %% [markdown]
# <!-- kamus_variabel:hetero_3.csv -->
#
# ### Kenali data: Harga dan karakteristik rumah
#
# **Data:** `data/hetero_3.csv`. **Satu baris:** satu rumah pada contoh latihan.
#
# Nama singkat di kode berasal dari penggantian nama kolom CSV; isi angkanya tetap sama.
#
# | Kolom CSV | Nama di kode | Pengertian | Satuan atau kode | Peran |
# |---|---|---|---|---|
# | `Harga` | `harga` | Harga jual rumah. | Ratusan juta rupiah | Y: target |
# | `Luas` | `luas` | Luas bangunan rumah. | Meter persegi (m²) | X: penjelas |
# | `Kamar` | `kamar` | Jumlah kamar tidur. | Kamar | X: penjelas |
# | `Lokasi` | `lokasi` | Skor kelayakan/kualitas lokasi rumah; bukan kode alamat. | Skor 1 sampai 10 | X: penjelas |
#
# Kolom turunan berikut dibuat saat praktik; kolom ini belum ada pada CSV awal.
#
# | Kolom turunan | Pengertian | Satuan/kode |
# |---|---|---|
# | `abs_resid` | Nilai mutlak selisih harga aktual dan prediksi untuk uji Glejser. | Sama dengan satuan Harga |
#
# Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

# %%
hunian = pd.read_csv("data/hetero_3.csv")
hunian = hunian.rename(
    columns={"Harga": "harga", "Luas": "luas", "Kamar": "kamar", "Lokasi": "lokasi"}
)
sampel_model_h = hunian[["harga", "luas", "kamar", "lokasi"]].dropna()
X_model_h = sampel_model_h[["luas", "kamar", "lokasi"]]
y_model_h = sampel_model_h["harga"]

model_h = LinearRegression()
model_h.fit(X_model_h, y_model_h)

koefisien_model_h = pd.Series(model_h.coef_, index=X_model_h.columns)
koefisien_model_h.loc["Intercept"] = model_h.intercept_

prediksi_model_h = pd.Series(model_h.predict(X_model_h), index=y_model_h.index)
residu_model_h = y_model_h - prediksi_model_h

# Pelengkap statistik: standard error dan pengujian pada sampel yang sama.
uji_model_h = sm.OLS(
    y_model_h,
    sm.add_constant(X_model_h, has_constant="add").rename(
        columns={"const": "Intercept"}
    ),
).fit()
print(uji_model_h.summary())

# %%
fig, ax = plt.subplots(figsize=(7, 4.5))
ax.scatter(prediksi_model_h, residu_model_h, color="#2F5D50", s=26)
ax.axhline(0, color="#C15937", lw=1.2)
ax.set_xlabel("Nilai fitted")
ax.set_ylabel("Residual")
ax.set_title("Residual vs Fitted: cek pola melebar")
plt.show()

# %% [markdown]
# Kalau titik-titik membentuk corong (makin melebar ke kanan), itu tanda
# heteroskedastisitas. Tapi jangan hanya mengandalkan mata. Jalankan uji
# formal: Breusch-Pagan, White, dan Glejser.
#
# Hipotesis nol ketiganya sama: varians residual konstan (homoskedastis).
# p-value kecil = tolak H0 = ada heteroskedastisitas.

# %%
from statsmodels.stats.diagnostic import het_breuschpagan, het_white

Xh = sm.add_constant(hunian[["luas", "kamar", "lokasi"]])
resid = residu_model_h

# Hasil uji berupa empat angka. Angka pertama statistik LM, kedua p-value LM.
hasil_bp = het_breuschpagan(resid, Xh)
print("Breusch-Pagan, statistik LM:", hasil_bp[0])
print("Breusch-Pagan, p-value:", hasil_bp[1])

hasil_white = het_white(resid, Xh)
print("White, statistik LM:", hasil_white[0])
print("White, p-value:", hasil_white[1])

# Glejser: regresikan |residual| pada X, lihat apakah ada X yang signifikan
hunian["abs_resid"] = np.abs(resid)
sampel_glejser = hunian[["abs_resid", "luas", "kamar", "lokasi"]].dropna()
X_glejser = sampel_glejser[["luas", "kamar", "lokasi"]]
y_glejser = sampel_glejser["abs_resid"]

glejser = LinearRegression()
glejser.fit(X_glejser, y_glejser)

# Pelengkap statistik: standard error dan pengujian pada sampel yang sama.
uji_glejser = sm.OLS(
    y_glejser,
    sm.add_constant(X_glejser, has_constant="add").rename(
        columns={"const": "Intercept"}
    ),
).fit()
print(uji_glejser.summary())

# %% [markdown]
# ### Penanganan: robust standard error
#
# Cara paling praktis: tetap pakai OLS, tapi ganti standard error dengan
# versi robust (White). Di EViews ini opsi *White* di tab Options. Di
# statsmodels: `cov_type="HC3"`.

# %%
# Pelengkap inferensi: koreksi standard error, dengan X dan y yang sama.
uji_model_h_robust = sm.OLS(
    y_model_h,
    sm.add_constant(X_model_h, has_constant="add").rename(
        columns={"const": "Intercept"}
    ),
).fit(cov_type="HC3")

banding = pd.DataFrame(
    {
        "koefisien": koefisien_model_h,
        "SE_biasa": uji_model_h.bse,
        "p_biasa": uji_model_h.pvalues,
        "SE_robust": uji_model_h_robust.bse,
        "p_robust": uji_model_h_robust.pvalues,
    }
)
banding

# %% [markdown]
# Koefisien tidak berubah, yang berubah hanya standard error dan p-value.
# Setelah ini, inferensi memakai kolom robust. Catat juga: kalau kesimpulan
# signifikansi berubah karena robust SE, itu temuan yang layak dilaporkan,
# bukan sesuatu yang disembunyikan.

# %% [markdown]
# ## 5. Uji normalitas residual
#
# Normalitas residual dibutuhkan untuk inferensi pada sampel kecil. Data
# `latihan_normalitas_1.csv`: harga saham dijelaskan suku bunga, tingkat
# pengangguran, dan pertumbuhan PDB.

# %% [markdown]
# <!-- kamus_variabel:latihan_normalitas_1.csv -->
#
# ### Kenali data: Harga saham dan kondisi makro
#
# **Data:** `data/latihan_normalitas_1.csv`. **Satu baris:** satu pengamatan gabungan harga saham dan indikator makro.
#
# Nama singkat di kode berasal dari penggantian nama kolom CSV; isi angkanya tetap sama.
#
# | Kolom CSV | Nama di kode | Pengertian | Satuan atau kode | Peran |
# |---|---|---|---|---|
# | `Harga_Saham` | `harga_saham` | Harga penutupan saham pada pengamatan. | Uang per lembar; skala tidak dirinci | Y: target |
# | `Tingkat_Suku_Bunga` | `suku_bunga` | Tingkat bunga bank sentral. | Persen | X: penjelas |
# | `Tingkat_Pengangguran` | `pengangguran` | Tingkat pengangguran nasional. | Persen | X: penjelas |
# | `Pertumbuhan_PDB` | `pdb` | Laju pertumbuhan PDB kuartalan pada contoh sumber. | Persen | X: penjelas |
#
# Berkas tidak memiliki tanggal; jangan mengarang tahun kalender dari nomor baris.
#
# Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

# %%
saham_makro = pd.read_csv("data/latihan_normalitas_1.csv")
saham_makro = saham_makro.rename(
    columns={
        "Harga_Saham": "harga_saham",
        "Tingkat_Suku_Bunga": "suku_bunga",
        "Tingkat_Pengangguran": "pengangguran",
        "Pertumbuhan_PDB": "pdb",
    }
)
sampel_model_n = saham_makro[
    ["harga_saham", "suku_bunga", "pengangguran", "pdb"]
].dropna()
X_model_n = sampel_model_n[["suku_bunga", "pengangguran", "pdb"]]
y_model_n = sampel_model_n["harga_saham"]

model_n = LinearRegression()
model_n.fit(X_model_n, y_model_n)

prediksi_model_n = pd.Series(model_n.predict(X_model_n), index=y_model_n.index)
residu_model_n = y_model_n - prediksi_model_n

from statsmodels.stats.stattools import jarque_bera

jb, p_jb, skew, kurt = jarque_bera(residu_model_n)
print(f"Jarque-Bera = {jb:.3f}")
print(f"p-value     = {p_jb:.4f}")
print(f"Skewness    = {skew:.3f}, Kurtosis = {kurt:.3f}")

# %%
fig, axes = plt.subplots(1, 2, figsize=(11, 4))
sns.histplot(residu_model_n, kde=True, ax=axes[0], color="#2F5D50")
axes[0].set_title("Histogram residual")
sm.qqplot(residu_model_n, line="s", ax=axes[1])
axes[1].set_title("Q-Q plot")
plt.tight_layout()
plt.show()

# %% [markdown]
# Aturan keputusan: p-value JB di bawah 0,05 = residual tidak normal.
# Yang perlu diperiksa kalau normalitas ditolak: outlier, data ekstrem,
# atau salah spesifikasi model. Tidak ada batas ukuran sampel yang otomatis
# menjamin inferensi aman. Pertimbangkan ketergantungan data, pencilan,
# dan beratnya penyimpangan; jangan membuang data hanya agar uji lolos.

# %% [markdown]
# ## 6. Uji autokorelasi
#
# Autokorelasi = residual periode ini berkorelasi dengan residual periode
# sebelumnya. Kasus ini khas data deret waktu. Model OLS masih tak bias,
# tapi standard error salah dan p-value terlalu optimistis.
#
# Kita pakai `latihan_dummy_2.csv` (data tahunan PDB dan investasi). Dua
# variabel yang sama-sama bergerak sepanjang waktu sering menghasilkan
# residual berautokorelasi.

# %%
from statsmodels.stats.stattools import durbin_watson
from statsmodels.stats.diagnostic import acorr_breusch_godfrey

# Uji autokorelasi memakai model yang sama seperti bagian 2,
# di sini difokuskan ke diagnostik residualnya
model_ar = model_krisis
dw = durbin_watson(residu_model_krisis)
bg_stat, bg_p, _, _ = acorr_breusch_godfrey(uji_model_krisis, nlags=2)

print(f"Durbin-Watson          = {dw:.3f}")
print(f"Breusch-Godfrey p-value = {bg_p:.4f}")

# %% [markdown]
# Panduan kasar DW: mendekati 2 = aman, di bawah 1,5 = indikasi
# autokorelasi positif, di atas 2,5 = autokorelasi negatif. Breusch-Godfrey
# lebih fleksibel karena bisa menguji lag berapa saja.
#
# Di data ini buktinya campuran: DW menunjukkan sinyal autokorelasi positif,
# tapi Breusch-Godfrey tidak menolak pada taraf 5%. Situasi campuran seperti
# ini wajar pada 30 observasi tahunan. Untuk data deret waktu, memakai HAC standard
# error adalah asuransi yang murah, dan di bawah terlihat p-value `krisis`
# berubah cukup banyak setelah koreksi.
#
# Penanganan praktis: Newey-West standard error (HAC). Di EViews: tab
# Options > Newey-West. Di statsmodels: `cov_type="HAC"`.

# %%
# Fit ulang model yang sama, kali ini dengan HAC standard error
# Pelengkap inferensi: koreksi standard error, dengan X dan y yang sama.
uji_model_ar_nw = sm.OLS(
    y_model_krisis,
    sm.add_constant(X_model_krisis, has_constant="add").rename(
        columns={"const": "Intercept"}
    ),
).fit(cov_type="HAC", cov_kwds={"maxlags": 2})
banding_ar = pd.DataFrame(
    {
        "koefisien": koefisien_model_krisis,
        "SE_biasa": uji_model_krisis.bse,
        "p_biasa": uji_model_krisis.pvalues,
        "SE_HAC": uji_model_ar_nw.bse,
        "p_HAC": uji_model_ar_nw.pvalues,
    }
)
banding_ar

# %% [markdown]
# ## 7. Alur keputusan diagnostik
#
# Ringkasnya, ini yang dilakukan saat memeriksa model:
#
# | Masalah | Deteksi | Penanganan cepat |
# |---|---|---|
# | Multikolinearitas | VIF > 10 | buang/gabung variabel, tambah sampel |
# | Heteroskedastisitas | BP/White/Glejser p < 0,05 | robust SE `HC3` |
# | Non-normalitas | JB p < 0,05 | cek outlier, transformasi; n besar relatif aman |
# | Autokorelasi | DW jauh dari 2, BG p < 0,05 | Newey-West `HAC` |
#
# Urutan pengujian yang dipakai di materi kuliah: multikolinearitas dulu
# (karena menentukan variabel mana yang dipakai), lalu heteroskedastisitas,
# normalitas, dan autokorelasi.

# %% [markdown]
# ## Latihan
#
# 1. Multikolinearitas kasus kedua: `latihan_multikolinieritas_2.csv`
#    (`konsumsi ~ pendapatan + kekayaan + jml_anggota`). Hitung VIF, buang
#    satu variabel dengan VIF tertinggi, lalu hitung VIF sisanya. Kalau
#    dua variabel bersaing, pertahankan yang paling relevan secara teori.
#    Bandingkan koefisien sebelum dan sesudah pembuangan.
# 2. Heteroskedastisitas kasus kedua: `hetero_2.csv`
#    (`pendapatan ~ pendidikan + pengalaman + usia`). Jalankan uji
#    Breusch-Pagan dan White, lalu bandingkan p-value biasa dan robust.
# 3. Kasus `hetero_1.csv` (`penjualan ~ iklan + salesperson + diskon`)
#    melatih melaporkan hipotesis yang ditolak: uji Breusch-Pagan dan
#    White di data itu tidak menolak homoskedastis, jadi dugaan "variasi
#    penjualan membesar saat iklan tinggi" tidak didukung data. Tulis
#    kesimpulan apa adanya, jangan paksakan narasi.
# 4. Normalitas kasus ketiga: `latihan_normalitas_3.csv`
#    (`harga ~ luas_bangunan + jumlah_kamar + usia_rumah`). Tampilkan
#    histogram residual dan uji Jarque-Bera.

# %% [markdown]
# ### Selanjutnya
#
# Selanjutnya: Sesi 4 mengganti jenis variabel Y dari kontinu ke
# kategorikal.
