# %% [markdown]
# # Supervised Learning: Regression (I)
# ## Praktik terbimbing dengan housing.csv
#
# **Untuk peserta yang belum pernah coding.** Kita mulai dari membaca tabel,
# membuat regresi sederhana, lalu menyusun regresi berganda dan menilai prediksinya.
# Alurnya mengikuti materi slide: supervised learning, regresi linear, modelling,
# multikolinearitas, evaluasi, serta underfitting dan overfitting.
#
# **Cara mulai di komputer:** buka notebook ini dan pertahankan susunan folder
# proyek. Data dibaca otomatis dari `data/housing.csv`.
# **Di Google Colab:** unggah notebook ini, lalu unggah `housing.csv` dari folder
# `data/` atau `data_tutorial.zip` dari folder `paket/` melalui panel **Files**.
# Jalankan sel berurutan dengan **Shift + Enter** atau **Run all**. Tidak perlu
# menyambungkan Google Drive atau menuliskan lokasi folder komputer tertentu.
#
# Hasil eksekusi disimpan di notebook ini. Jika ingin mencoba sendiri dari awal,
# mulai ulang kernel/runtime dan jalankan semua sel berurutan.

# %% [markdown]
# ### Peta materi dan tujuan belajar
#
# | Bagian notebook | Acuan slide | Setelah praktik, peserta dapat... |
# |---|---|---|
# | 1. Konsep dan persamaan garis | 4-15 | Membedakan fitur/target, slope/intersep, dan jenis regresi. |
# | 2-4. Data, pembagian, dan pembersihan | 17-20 | Membaca CSV, membagi 80:20, dan mengisi data kosong dengan benar. |
# | 5. Regresi sederhana | 18-21 | Memakai RM untuk memprediksi MEDV dan membaca koefisien. |
# | 6-8. VIF, korelasi, dan regresi berganda | 22-25 | Menilai multikolinearitas dan membandingkan model dengan/tanpa RAD. |
# | 9. Evaluasi | 26-28 | Membaca RMSE, R², serta grafik aktual dan prediksi. |
# | 10. Prediksi baru | 5-6 | Memakai model untuk dua profil baru, termasuk data kosong. |
# | 11. Pipeline | Pengayaan dari notebook awal | Menggabungkan langkah yang sudah dipahami. |
# | 12. Underfitting/overfitting | 29-30 | Membaca perbedaan hasil train dan validasi. |
# | 13. Latihan dan ringkasan | Penutup | Menjelaskan hasil dengan satuan dan batasan yang benar. |
#
# Untuk pertemuan pertama, utamakan bagian 1-10. Bagian 11-12 adalah pendalaman.
# Semua sel kode sudah lengkap dan dapat dijalankan; latihan tambahan ada di akhir.
#
# ### Cara membaca kode
#
# | Kode/simbol | Arti |
# |---|---|
# | `# ...` | Catatan yang tidak dihitung oleh Python. |
# | `data = ...` | Simpan hasil dengan nama `data`. |
# | `data["RM"]` | Ambil satu kolom. `data[["RM"]]` mempertahankan bentuk tabel. |
# | `data.head()` | Tampilkan lima baris pertama. |
# | `model.fit(X, y)` | Pelajari hubungan fitur dan target dari data train. |
# | `model.predict(X_baru)` | Hitung prediksi untuk fitur yang diberikan. |
#
# Nama kolom harus sama persis, termasuk huruf besar. Desimal di kode memakai titik.

# %% [markdown]
# ## 1. Konsep yang dipakai
#
# Pada **supervised learning**, data latihan sudah mempunyai target atau jawaban.
# Pada kasus ini, fitur adalah karakteristik wilayah/perumahan dan target adalah
# `MEDV`. **Regresi** memprediksi angka kontinu; **klasifikasi** memprediksi kategori.
# Pada unsupervised learning, target tidak disediakan, misalnya pengelompokan wilayah.
#
# | Model pada slide | Kegunaan |
# |---|---|
# | Regresi linear sederhana | Satu fitur untuk memprediksi target kontinu. |
# | Regresi linear berganda | Beberapa fitur untuk memprediksi target kontinu. |
# | Regresi polinomial | Menambahkan pangkat fitur untuk hubungan melengkung. |
# | Ridge dan Lasso | Memberi penalti koefisien; berguna saat perlu regularisasi. |
# | Logistic regression | Walaupun namanya regression, umumnya dipakai untuk klasifikasi. |
#
# Fokus praktik ini adalah regresi linear. Polinomial dipakai kembali di bagian 12.
#
# Persamaan sederhana: $\hat{y} = b_0 + b_1 x$. Intersep $b_0$ adalah nilai prediksi
# saat x nol; slope $b_1$ adalah perubahan prediksi untuk tambahan satu unit x.
# Pada model berganda, tambahkan $b_2 x_2$, $b_3 x_3$, dan seterusnya.
# OLS memilih koefisien yang meminimalkan jumlah kuadrat error pada data train.
#
# ### Contoh persamaan garis dari slide: tarif taksi
#
# Tarif awal kedua taksi Rp5.000. Slope taksi standar Rp4.000/km, sedangkan
# taksi premium Rp7.500/km. Contoh ini membantu membaca persamaan sebelum memakai model.

# %% [markdown]
# ### Persiapan lokasi data
#
# Jalankan sel ini apa adanya. Sel ini menemukan data pada susunan folder
# proyek atau membuka paket data yang Anda unggah di Colab.

# %%
import os
import zipfile
from pathlib import Path

# Di komputer sendiri, temukan folder data dari lokasi notebook ini.
# Di Colab, folder kerja tetap memakai lokasi unggahan Anda.
if not Path("data").is_dir() and Path("../../data").is_dir():
    os.chdir("../..")

if Path("data_tutorial.zip").exists() and not Path("data/housing.csv").exists():
    with zipfile.ZipFile("data_tutorial.zip") as paket:
        paket.extractall(".")

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.dummy import DummyRegressor
from sklearn.metrics import mean_squared_error, r2_score
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.tools.tools import add_constant

# Pengaturan tampilan; cukup jalankan apa adanya.
pd.set_option("display.max_columns", 14)
pd.set_option("display.precision", 3)
sns.set_theme(style="whitegrid")
plt.rcParams["figure.dpi"] = 110

# %%
jarak = pd.DataFrame({"km": [0, 1, 2, 3]})
jarak["taksi_standar"] = 5000 + 4000 * jarak["km"]
jarak["taksi_premium"] = 5000 + 7500 * jarak["km"]
jarak

# %%
plt.figure(figsize=(7, 4))
plt.plot(jarak["km"], jarak["taksi_standar"], marker="o", label="Standar")
plt.plot(jarak["km"], jarak["taksi_premium"], marker="o", label="Premium")
plt.xlabel("Jarak (km)")
plt.ylabel("Tarif (rupiah)")
plt.title("Intersep sama, slope berbeda")
plt.legend()
plt.tight_layout()
plt.show()

# %% [markdown]
# ## 2. Baca dan kenali data
#
# Kita memakai **berkas lokal yang diberikan**, `housing.csv`, tanpa mengunduh data.
# Satu baris mewakili karakteristik suatu wilayah dalam dataset historis Boston Housing,
# bukan satu rumah tertentu di Indonesia. `MEDV` adalah nilai median rumah yang dihuni
# pemiliknya, dalam **ribuan dolar AS pada data historis**. MEDV = 24 berarti sekitar
# US$24.000 pada konteks data tersebut, bukan Rp24 juta atau harga saat ini.
#
# | Kolom | Arti ringkas |
# |---|---|
# | CRIM | Tingkat kejahatan per kapita wilayah. |
# | ZN | Proporsi lahan hunian dengan ukuran kavling lebih dari 25.000 kaki persegi. |
# | INDUS | Proporsi lahan bisnis nonritel. |
# | CHAS | Dummy berbatasan dengan Sungai Charles: 1 ya, 0 tidak. |
# | NOX | Konsentrasi nitrogen oksida, bagian per 10 juta. |
# | RM | Rata-rata jumlah kamar per hunian. |
# | AGE | Proporsi hunian milik penghuni yang dibangun sebelum 1940. |
# | DIS | Jarak tertimbang ke lima pusat pekerjaan. |
# | RAD | Indeks akses ke jalan raya radial. |
# | TAX | Tarif pajak properti per US$10.000. |
# | PTRATIO | Rasio murid terhadap guru. |
# | BLACK | Variabel historis B: transformasi komposisi ras penduduk. |
# | LSTAT | Persentase penduduk berstatus sosial ekonomi rendah menurut definisi historis dataset. |
# | MEDV | Target: median nilai rumah dalam ribuan dolar AS. |
#
# **Catatan dataset untuk dibahas di kelas.** Boston Housing mempunyai persoalan etis,
# terutama rekayasa variabel B/BLACK berdasarkan asumsi tentang ras. Kita mempertahankan
# kolom berkas untuk mereproduksi latihan dan membahas batasannya. Dataset ini bukan
# dasar untuk membuat keputusan harga atau menilai kelompok penduduk; menghapus satu
# kolom saja juga belum menjamin hilangnya bias. Sebagian nilai MEDV berhenti pada 50,
# sehingga pembacaan prediksi di sekitar batas tersebut perlu hati-hati.
# Rujukan definisi dan catatan ini ada di akhir notebook.

# %%
# CSV tunggal yang diunggah ke Colab dapat dibaca dari folder unggahan.
lokasi_data = "data/housing.csv"
if not Path(lokasi_data).exists() and Path("housing.csv").exists():
    lokasi_data = "housing.csv"

data = pd.read_csv(lokasi_data)
print("Jumlah baris:", data.shape[0])
print("Jumlah kolom:", data.shape[1])
data.head()

# %% [markdown]
# `info()` menunjukkan jenis kolom dan banyaknya nilai yang terisi. `describe()`
# merangkum rata-rata, sebaran, dan rentang. Pemeriksaan data dilakukan sebelum modelling.

# %%
data.info()

# %%
data.describe().round(2)

# %%
pemeriksaan = pd.DataFrame({"jumlah_kosong": data.isna().sum()})
pemeriksaan["persen_kosong"] = 100 * pemeriksaan["jumlah_kosong"] / len(data)
print("Baris duplikat:", data.duplicated().sum())
print("Target MEDV kosong:", data["MEDV"].isna().sum())
pemeriksaan

# %% [markdown]
# Pada berkas yang diuji, terdapat 506 baris, 14 kolom, tanpa nilai kosong atau
# duplikat. Kita tetap memperagakan imputasi karena data baru dapat belum lengkap.
# Jangan mengarang nilai target yang kosong untuk pelatihan. Jika data diganti,
# periksa kembali hasil pemeriksaan ini sebelum melanjutkan.

# %% [markdown]
# ## 3. Pisahkan fitur, target, dan data train-test
#
# `X` berisi 13 fitur; `y` berisi MEDV. **MEDV tidak boleh masuk ke X**, karena itulah
# jawaban yang hendak diprediksi. Data dibagi **80% train, 20% test** seperti slide.
# `random_state=42` membuat pembagian bisa diulang dengan hasil yang sama.
#
# Data train dipakai untuk mempelajari pola, median imputasi, serta korelasi/VIF.
# Data test disimpan untuk evaluasi setelah model ditentukan. Jangan mengubah model
# berulang kali untuk mengejar nilai test yang lebih bagus; pemilihan model memerlukan
# validasi di dalam data train. Contohnya ada di bagian 12.

# %%
X = data.drop(columns=["MEDV"])
y = data["MEDV"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42
)

print("Data train:", len(X_train), "baris")
print("Data test :", len(X_test), "baris")
print("Jumlah fitur:", X_train.shape[1])
X_train.head()

# %% [markdown]
# ## 4. Tangani data kosong tanpa membocorkan informasi test
#
# Median dihitung **hanya dari train** menggunakan `fit_transform()`. Data test
# memakai median yang sama lewat `transform()`. Ini tetap perlu dijaga walaupun
# CSV saat ini lengkap. Menghitung median dari gabungan train dan test akan
# memakai informasi yang seharusnya belum diketahui saat melatih model.
#
# Hasil imputer berupa kumpulan angka. Kita ubah kembali menjadi tabel dengan
# nama kolom **dan indeks baris yang sama**. Indeks adalah penanda observasi;
# menjaganya memastikan fitur dan MEDV tetap berpasangan saat digabung.

# %%
pengisi_kosong = SimpleImputer(strategy="median")

angka_train = pengisi_kosong.fit_transform(X_train)
angka_test = pengisi_kosong.transform(X_test)

X_train_bersih = pd.DataFrame(angka_train, columns=X_train.columns, index=X_train.index)
X_test_bersih = pd.DataFrame(angka_test, columns=X_test.columns, index=X_test.index)

print("Nilai kosong train:", X_train_bersih.isna().sum().sum())
print("Nilai kosong test :", X_test_bersih.isna().sum().sum())
print("Indeks fitur dan target train sama:", X_train_bersih.index.equals(y_train.index))
X_train_bersih.head()

# %% [markdown]
# ## 5. Regresi sederhana: satu fitur RM
#
# Pertanyaan: apakah rata-rata jumlah kamar dapat membantu memprediksi MEDV?
# Kita memakai satu fitur, `RM`, dengan target yang sama. Grafik memakai data train.
# Pada slide contohnya suhu dan curah hujan; di sini langkah yang sama diterapkan
# pada data Housing sehingga seluruh praktik memakai CSV yang Anda miliki.

# %%
X_train_sederhana = X_train_bersih[["RM"]]
X_test_sederhana = X_test_bersih[["RM"]]

model_sederhana = LinearRegression()
model_sederhana.fit(X_train_sederhana, y_train)

intersep = model_sederhana.intercept_
slope_rm = model_sederhana.coef_[0]
print("Intersep:", round(intersep, 3))
print("Koefisien RM:", round(slope_rm, 3))
print("Persamaan MEDV =", round(intersep, 3), "+", round(slope_rm, 3), "x RM")

# %% [markdown]
# Koefisien RM dibaca dalam **ribuan dolar AS per tambahan satu kamar rata-rata**.
# Ini hubungan prediktif pada data, bukan bukti bahwa menambah kamar menyebabkan
# harga naik sebesar itu. Intersep saat RM = 0 berada di luar konteks rumah pada
# data ini sehingga tidak ditafsirkan sebagai harga rumah yang realistis.

# %%
garis = pd.DataFrame({"RM": [X_train_bersih["RM"].min(), X_train_bersih["RM"].max()]})
garis["prediksi"] = model_sederhana.predict(garis)

plt.figure(figsize=(7, 4.5))
plt.scatter(X_train_bersih["RM"], y_train, alpha=0.5, label="Data train")
plt.plot(garis["RM"], garis["prediksi"], color="#C15937", label="Garis OLS")
plt.xlabel("RM: rata-rata jumlah kamar")
plt.ylabel("MEDV: ribuan dolar AS")
plt.title("Regresi sederhana: MEDV dari RM")
plt.legend()
plt.tight_layout()
plt.show()

# %%
contoh_rm = pd.DataFrame({"RM": [6.0, 7.0]})
contoh_rm["prediksi_MEDV"] = model_sederhana.predict(contoh_rm)
contoh_rm

# %% [markdown]
# ## 6. Sebelum regresi berganda: korelasi dan VIF
#
# **Multikolinearitas** berarti fitur saling berhubungan kuat. Koefisien dapat menjadi
# tidak stabil dan sulit ditafsirkan, walaupun prediksi belum tentu buruk.
# VIF melihat hubungan satu fitur dengan kumpulan fitur lainnya; korelasi pasangan
# melengkapi pemeriksaan tersebut. Angka VIF sekitar 1 rendah; angka 5-10 patut
# diperiksa, dan di atas 10 sering dipakai sebagai tanda masalah besar. Ini pedoman,
# bukan batas otomatis untuk membuang variabel.
#
# ### 6.1 Korelasi pada data train
#
# Salin tabel fitur bersih, lalu tambahkan MEDV berdasarkan indeks barisnya.
# Target dimasukkan **hanya untuk analisis korelasi**, bukan sebagai fitur prediksi.

# %%
data_train = X_train_bersih.copy()
data_train["MEDV"] = y_train
korelasi = data_train.corr()

print("Baris data train untuk korelasi:", len(data_train))
print("Nilai kosong setelah penggabungan:", data_train.isna().sum().sum())
korelasi.loc[["TAX", "RAD"], ["TAX", "RAD", "MEDV"]].round(3)

# %%
plt.figure(figsize=(12, 10))
sns.heatmap(
    korelasi,
    annot=True,
    fmt=".2f",
    cmap="RdBu_r",
    center=0,
    vmin=-1,
    vmax=1,
    annot_kws={"size": 8},
)
plt.title("Korelasi fitur dan target pada data train")
plt.tight_layout()
plt.show()

# %% [markdown]
# TAX dan RAD berkorelasi kuat, sekitar 0,91. Hubungan TAX dengan MEDV pada
# train lebih kuat secara absolut daripada RAD dengan MEDV. Korelasi ini tidak
# menentukan sebab akibat dan tidak cukup sendirian untuk memilih semua fitur.
#
# ### 6.2 Hitung VIF tiap fitur
#
# `add_constant()` menambahkan konstanta pada kolom posisi 0. Perhitungan di bawah
# dimulai dari posisi 1 sampai 13 untuk fitur asli. Satu baris menghitung satu VIF;
# barisnya sengaja ditulis lengkap agar tidak perlu mempelajari perulangan.

# %%
matriks_vif = add_constant(X_train_bersih)
tabel_vif = pd.DataFrame({"fitur": X_train_bersih.columns})
tabel_vif["VIF"] = [
    variance_inflation_factor(matriks_vif.values, 1),
    variance_inflation_factor(matriks_vif.values, 2),
    variance_inflation_factor(matriks_vif.values, 3),
    variance_inflation_factor(matriks_vif.values, 4),
    variance_inflation_factor(matriks_vif.values, 5),
    variance_inflation_factor(matriks_vif.values, 6),
    variance_inflation_factor(matriks_vif.values, 7),
    variance_inflation_factor(matriks_vif.values, 8),
    variance_inflation_factor(matriks_vif.values, 9),
    variance_inflation_factor(matriks_vif.values, 10),
    variance_inflation_factor(matriks_vif.values, 11),
    variance_inflation_factor(matriks_vif.values, 12),
    variance_inflation_factor(matriks_vif.values, 13),
]
tabel_vif.round(3)

# %% [markdown]
# ### 6.3 Contoh pengurangan fitur sesuai slide: keluarkan RAD
#
# Untuk latihan ini kita membandingkan dua kandidat yang ditentukan sebelum membaca
# hasil test: semua fitur, dan fitur tanpa RAD. Kita mempertahankan TAX seperti contoh
# slide 25. Nama tabel baru menjaga data awal tetap tersedia. Penghapusan ini merupakan
# pilihan ilustratif berdasarkan korelasi dan konteks; tidak menjamin RMSE membaik.

# %%
X_train_ringkas = X_train_bersih.drop(columns=["RAD"])
X_test_ringkas = X_test_bersih.drop(columns=["RAD"])
print("Fitur model lengkap:", X_train_bersih.shape[1])
print("Fitur model ringkas:", X_train_ringkas.shape[1])

# %%
matriks_vif = add_constant(X_train_ringkas)
vif_tanpa_rad = pd.DataFrame({"fitur": X_train_ringkas.columns})
vif_tanpa_rad["VIF"] = [
    variance_inflation_factor(matriks_vif.values, 1),
    variance_inflation_factor(matriks_vif.values, 2),
    variance_inflation_factor(matriks_vif.values, 3),
    variance_inflation_factor(matriks_vif.values, 4),
    variance_inflation_factor(matriks_vif.values, 5),
    variance_inflation_factor(matriks_vif.values, 6),
    variance_inflation_factor(matriks_vif.values, 7),
    variance_inflation_factor(matriks_vif.values, 8),
    variance_inflation_factor(matriks_vif.values, 9),
    variance_inflation_factor(matriks_vif.values, 10),
    variance_inflation_factor(matriks_vif.values, 11),
    variance_inflation_factor(matriks_vif.values, 12),
]
vif_tanpa_rad.round(3)

# %% [markdown]
# Bandingkan VIF TAX sebelum dan sesudah RAD dikeluarkan. Penurunannya menunjukkan
# berkurangnya informasi berulang pada X. Kualitas prediksi tetap dinilai terpisah.

# %% [markdown]
# ## 7. Latih regresi berganda
#
# Model pertama memakai semua fitur. Model kedua memakai fitur tanpa RAD.
# Keduanya dilatih pada observasi train yang sama. `LinearRegression()` membuat
# wadah model, sedangkan `fit()` menghitung intersep dan koefisiennya.

# %%
model_berganda = LinearRegression()
model_berganda.fit(X_train_bersih, y_train)

model_ringkas = LinearRegression()
model_ringkas.fit(X_train_ringkas, y_train)

tabel_koefisien = pd.DataFrame(
    {"fitur": X_train_bersih.columns, "koefisien": model_berganda.coef_}
)
print("Intersep model berganda:", round(model_berganda.intercept_, 3))
tabel_koefisien.round(3)

# %% [markdown]
# Setiap koefisien berganda adalah perubahan prediksi MEDV untuk satu unit fitur
# tersebut **dengan fitur lain tetap**. Slope RM dapat berbeda dari model sederhana
# karena variabel lain kini ikut diperhitungkan. Koefisien terbesar secara absolut
# tidak otomatis menunjukkan fitur paling penting karena satuan fiturnya berbeda.
# scikit-learn pada praktik ini dipakai untuk prediksi; tabel ini tidak memberikan p-value.

# %% [markdown]
# ## 8. Buat prediksi pada data test
#
# Model sudah ditentukan sebelum evaluasi test. Satu prediksi dibuat untuk setiap
# baris test. Sebagai pembanding sederhana, `DummyRegressor` selalu memprediksi
# rata-rata MEDV **dari train**. Model sebaiknya memberikan manfaat dibanding tebakan ini.

# %%
prediksi_sederhana = model_sederhana.predict(X_test_sederhana)
prediksi_berganda = model_berganda.predict(X_test_bersih)
prediksi_ringkas = model_ringkas.predict(X_test_ringkas)

model_pembanding = DummyRegressor(strategy="mean")
model_pembanding.fit(X_train_bersih, y_train)
prediksi_pembanding = model_pembanding.predict(X_test_bersih)

hasil_uji = pd.DataFrame(
    {"aktual": y_test, "prediksi": prediksi_berganda}, index=y_test.index
)
hasil_uji["error"] = hasil_uji["aktual"] - hasil_uji["prediksi"]
hasil_uji.head(10).round(3)

# %% [markdown]
# ## 9. Evaluasi: RMSE, R², dan grafik
#
# **RMSE** adalah akar rata-rata kuadrat error. Satuannya sama dengan MEDV,
# yaitu ribuan dolar AS. Semakin kecil, semakin dekat prediksi dengan aktual secara
# keseluruhan. RMSE bukan jaminan bahwa setiap error berada dalam rentang ±RMSE
# dan bukan otomatis interval prediksi atau standar deviasi residual.
#
# **R²** membandingkan jumlah kuadrat error dengan variasi target pada sampel
# yang dievaluasi: $R^2 = 1 - SSE/SST$. Nilai 1 adalah kecocokan sempurna, 0 setara
# dengan patokan rata-rata target pada sampel evaluasi, dan **bisa negatif**.
# R² bukan persentase prediksi yang benar atau ukuran sebab akibat.
#
# Kita memakai `np.sqrt(mean_squared_error(...))` agar rumus RMSE terlihat jelas
# dan tidak bergantung pada ketersediaan fungsi RMSE pada versi paket tertentu.

# %%
rmse_pembanding = np.sqrt(mean_squared_error(y_test, prediksi_pembanding))
rmse_sederhana = np.sqrt(mean_squared_error(y_test, prediksi_sederhana))
rmse_berganda = np.sqrt(mean_squared_error(y_test, prediksi_berganda))
rmse_ringkas = np.sqrt(mean_squared_error(y_test, prediksi_ringkas))

r2_pembanding = r2_score(y_test, prediksi_pembanding)
r2_sederhana = r2_score(y_test, prediksi_sederhana)
r2_berganda = r2_score(y_test, prediksi_berganda)
r2_ringkas = r2_score(y_test, prediksi_ringkas)

evaluasi = pd.DataFrame(
    {
        "model": [
            "Rata-rata train",
            "Sederhana: RM",
            "Berganda: 13 fitur",
            "Berganda: tanpa RAD",
        ],
        "RMSE_test": [rmse_pembanding, rmse_sederhana, rmse_berganda, rmse_ringkas],
        "R2_test": [r2_pembanding, r2_sederhana, r2_berganda, r2_ringkas],
    }
)
evaluasi.round(4)

# %% [markdown]
# Pada data dan pembagian yang disediakan, model semua fitur memberi RMSE sekitar
# 4,93 dan R² sekitar 0,669. Tanpa RAD, RMSE sekitar 5,14 dan R² sekitar 0,639.
# Artinya, VIF yang lebih rendah **tidak otomatis memperbaiki prediksi**.
# Untuk model lengkap, RMSE 4,93 setara skala error kuadratik sekitar US$4.930
# dalam satuan data historis. Ini tidak menyatakan semua prediksi meleset sebesar itu.
#
# Angka pada slide dapat berbeda karena contoh, data, dan pembagian observasinya
# berbeda. Untuk berkas ini, gunakan output aktual. Tabel test melaporkan kandidat
# yang sudah ditetapkan; jangan melanjutkan pencarian model dengan melihat test berulang.

# %%
# Titik yang dekat dengan garis diagonal menunjukkan prediksi yang dekat aktual.
plt.figure(figsize=(6, 5))
plt.scatter(hasil_uji["aktual"], hasil_uji["prediksi"], alpha=0.7)
plt.plot([0, 55], [0, 55], linestyle="--", color="#C15937")
plt.xlabel("MEDV aktual (ribuan dolar AS)")
plt.ylabel("MEDV prediksi (ribuan dolar AS)")
plt.title("Model berganda: aktual dan prediksi pada test")
plt.tight_layout()
plt.show()

# %%
plt.figure(figsize=(7, 4))
plt.scatter(hasil_uji["prediksi"], hasil_uji["error"], alpha=0.7)
plt.axhline(0, linestyle="--", color="#C15937")
plt.xlabel("MEDV prediksi")
plt.ylabel("Error = aktual - prediksi")
plt.title("Periksa pola error pada data test")
plt.tight_layout()
plt.show()

# %% [markdown]
# Error positif berarti model memprediksi terlalu rendah; error negatif berarti
# terlalu tinggi. Pola melengkung, sebaran melebar, dan titik ekstrem dapat menjadi
# petunjuk keterbatasan model. Grafik ini bukan bukti bahwa semua asumsi sudah terpenuhi.

# %% [markdown]
# ## 10. Prediksi dua profil baru
#
# Tabel berikut adalah contoh profil wilayah, bukan observasi test atau harga rumah
# tertentu. Setiap kolom bernama sama seperti fitur train. Satu nilai CRIM sengaja
# dibuat kosong (`np.nan`) agar kita melihat imputer bekerja pada data baru.
# Gunakan `transform()`, bukan `fit_transform()`, sehingga median train tetap dipakai.

# %%
data_baru = pd.DataFrame(
    {
        "CRIM": [np.nan, 0.2],
        "ZN": [18.0, 0.0],
        "INDUS": [5.0, 7.0],
        "CHAS": [0, 1],
        "NOX": [0.50, 0.55],
        "RM": [6.5, 7.0],
        "AGE": [50.0, 35.0],
        "DIS": [4.0, 3.0],
        "RAD": [4, 5],
        "TAX": [300.0, 350.0],
        "PTRATIO": [18.0, 17.0],
        "BLACK": [390.0, 380.0],
        "LSTAT": [8.0, 10.0],
    }
)

data_baru_bersih = pd.DataFrame(
    pengisi_kosong.transform(data_baru), columns=X_train.columns, index=data_baru.index
)
print("CRIM sebelum diisi:")
print(data_baru["CRIM"])
print("CRIM setelah memakai median train:")
print(data_baru_bersih["CRIM"])

# %%
prediksi_baru = model_berganda.predict(data_baru_bersih)
hasil_baru = data_baru_bersih.copy()
hasil_baru["prediksi_MEDV"] = prediksi_baru
hasil_baru[["RM", "LSTAT", "prediksi_MEDV"]].round(3)

# %% [markdown]
# ## 11. Pengayaan: merangkai langkah dengan Pipeline
#
# Kita sudah melakukan dua langkah: mengisi nilai kosong dan menjalankan regresi.
# `make_pipeline()` merangkainya dengan urutan yang sama. Saat `fit()` dipanggil,
# median dan regresi dipelajari dari train. Saat `predict()`, transformasi train dipakai
# otomatis pada data yang diberikan. Jadi masukan pipeline adalah **fitur mentah**.
#
# Nama langkah tidak perlu ditulis sendiri pada contoh ini. Bagi pemula, pahami
# versi manual lebih dahulu, kemudian cocokkan hasil pipeline di bawah.

# %%
from sklearn.pipeline import make_pipeline

model_otomatis = make_pipeline(SimpleImputer(strategy="median"), LinearRegression())
model_otomatis.fit(X_train, y_train)

prediksi_otomatis = model_otomatis.predict(X_test)
print(
    "Prediksi pipeline sama dengan versi manual:",
    np.allclose(prediksi_otomatis, prediksi_berganda),
)
print("Prediksi profil baru dari data mentah:", model_otomatis.predict(data_baru))

# %% [markdown]
# ## 12. Pengayaan: underfitting dan overfitting
#
# **Underfitting:** model terlalu sederhana untuk menangkap pola; error train dan
# validasi sama-sama besar. **Overfitting:** model mengikuti detail/noise train;
# hasil train membaik tetapi tidak diikuti perbaikan pada data yang belum dipelajari.
#
# Untuk memperagakan ini, kita memakai **RM saja**, lalu mengambil train kecil dan
# validasi **dari data train awal**. Data test 102 baris tidak dipakai untuk memilih
# derajat polinomial. Perbandingan ini mempunyai tujuan berbeda dari model 13 fitur.
#
# Empat kandidat: tebakan konstan, garis lurus, kuadratik, dan polinomial derajat 10.
# Pangkat tinggi bukan otomatis lebih baik. StandardScaler mengubah skala RM sebelum
# pangkat dibuat agar perhitungan lebih stabil; semua parameter dipelajari dari train kecil.

# %%
from sklearn.preprocessing import StandardScaler, PolynomialFeatures

RM_latih, RM_validasi, harga_latih, harga_validasi = train_test_split(
    X_train[["RM"]], y_train, test_size=0.25, random_state=42
)

model_konstan = make_pipeline(
    SimpleImputer(strategy="median"), DummyRegressor(strategy="mean")
)
model_lurus = make_pipeline(SimpleImputer(strategy="median"), LinearRegression())
model_kuadrat = make_pipeline(
    SimpleImputer(strategy="median"),
    StandardScaler(),
    PolynomialFeatures(degree=2, include_bias=False),
    LinearRegression(),
)
model_lentur = make_pipeline(
    SimpleImputer(strategy="median"),
    StandardScaler(),
    PolynomialFeatures(degree=10, include_bias=False),
    LinearRegression(),
)

model_konstan.fit(RM_latih, harga_latih)
model_lurus.fit(RM_latih, harga_latih)
model_kuadrat.fit(RM_latih, harga_latih)
model_lentur.fit(RM_latih, harga_latih)
print("Train kecil:", len(RM_latih), "Validasi:", len(RM_validasi))

# %%
rmse_train_konstan = np.sqrt(
    mean_squared_error(harga_latih, model_konstan.predict(RM_latih))
)
rmse_train_lurus = np.sqrt(
    mean_squared_error(harga_latih, model_lurus.predict(RM_latih))
)
rmse_train_kuadrat = np.sqrt(
    mean_squared_error(harga_latih, model_kuadrat.predict(RM_latih))
)
rmse_train_lentur = np.sqrt(
    mean_squared_error(harga_latih, model_lentur.predict(RM_latih))
)

rmse_validasi_konstan = np.sqrt(
    mean_squared_error(harga_validasi, model_konstan.predict(RM_validasi))
)
rmse_validasi_lurus = np.sqrt(
    mean_squared_error(harga_validasi, model_lurus.predict(RM_validasi))
)
rmse_validasi_kuadrat = np.sqrt(
    mean_squared_error(harga_validasi, model_kuadrat.predict(RM_validasi))
)
rmse_validasi_lentur = np.sqrt(
    mean_squared_error(harga_validasi, model_lentur.predict(RM_validasi))
)

perbandingan_kompleksitas = pd.DataFrame(
    {
        "model": ["Konstan", "Linear", "Polinomial 2", "Polinomial 10"],
        "RMSE_train": [
            rmse_train_konstan,
            rmse_train_lurus,
            rmse_train_kuadrat,
            rmse_train_lentur,
        ],
        "RMSE_validasi": [
            rmse_validasi_konstan,
            rmse_validasi_lurus,
            rmse_validasi_kuadrat,
            rmse_validasi_lentur,
        ],
    }
)
perbandingan_kompleksitas.round(3)

# %% [markdown]
# Pada pembagian ini, polinomial 10 memperbaiki RMSE train dibanding kuadratik,
# tetapi RMSE validasinya memburuk. Itu tanda model lebih lentur mulai mengikuti
# detail train tanpa tambahan manfaat pada validasi. Model konstan menunjukkan
# keterbatasan model yang tidak memakai pola RM sama sekali. Kesimpulan ini
# bergantung sampel; derajat tinggi tidak selalu overfit pada setiap dataset.

# %%
kurva = pd.DataFrame(
    {"RM": np.linspace(RM_latih["RM"].min(), RM_latih["RM"].max(), 200)}
)

plt.figure(figsize=(9, 5))
plt.scatter(RM_latih["RM"], harga_latih, alpha=0.25, label="Train kecil")
plt.scatter(RM_validasi["RM"], harga_validasi, alpha=0.5, marker="x", label="Validasi")
plt.plot(kurva["RM"], model_lurus.predict(kurva), label="Linear")
plt.plot(kurva["RM"], model_kuadrat.predict(kurva), label="Polinomial 2")
plt.plot(kurva["RM"], model_lentur.predict(kurva), label="Polinomial 10")
plt.xlabel("RM: rata-rata jumlah kamar")
plt.ylabel("MEDV: ribuan dolar AS")
plt.title("Kelenturan model dan kemampuan membaca data baru")
plt.ylim(0, 65)
plt.legend()
plt.tight_layout()
plt.show()

# %% [markdown]
# ## 13. Latihan dan ringkasan
#
# 1. Dari persamaan regresi sederhana, berapa perubahan prediksi saat RM naik
#    dari 6 ke 7? Bandingkan dengan tabel `contoh_rm`.
# 2. Jelaskan mengapa `fit_transform()` hanya dijalankan pada train.
# 3. Bandingkan VIF TAX pada `tabel_vif` dan `vif_tanpa_rad`. Apakah RMSE test
#    pasti ikut membaik ketika VIF turun?
# 4. Pada `data_baru`, ubah RM profil pertama dari 6,5 menjadi 7,5, kemudian
#    jalankan ulang transformasi dan prediksinya. Fitur lain tetap. Bandingkan
#    perubahan prediksi dengan koefisien RM pada model berganda.
# 5. Mengapa R² = 0,669 tidak berarti 66,9% prediksi tepat?
#
# <details><summary>Petunjuk jawaban</summary>
#
# 1. Selisih kedua prediksi sederhana sama dengan slope RM karena selisih RM satu unit.
# 2. Median test/new data harus berasal dari train agar proses belajar tidak memakai
#    informasi data evaluasi.
# 3. VIF TAX turun setelah RAD dikeluarkan, tetapi pada berkas ini RMSE test model
#    ringkas justru lebih besar. Tujuan interpretasi dan tujuan prediksi perlu dibedakan.
# 4. Dengan perbedaan RM satu unit dan fitur lain tetap, selisih prediksi sama dengan
#    koefisien RM model berganda. Hasil imputer harus tetap berasal dari train yang sama.
# 5. R² mengukur perbandingan kuadrat error terhadap variasi target, bukan menghitung
#    proporsi prediksi yang dianggap tepat.
#
# </details>
#
# Tuliskan kesimpulan dengan pola: **data apa**, **model apa**, **hasil test**,
# **satuan**, dan **keterbatasan**. Contoh: pada pembagian 80:20 housing.csv,
# regresi 13 fitur menghasilkan RMSE test sekitar 4,93 ribu dolar AS historis dan
# R² sekitar 0,669. Hasil ini untuk latihan pada sampel tersebut, belum menjadi
# bukti kausal atau jaminan kinerja pada wilayah dan tahun lain.
#
# ### Jika muncul error
#
# | Pesan | Yang diperiksa |
# |---|---|
# | FileNotFoundError | Jalankan sel persiapan; di Colab unggah housing.csv atau data_tutorial.zip. |
# | NameError | Jalankan sel sebelumnya dari atas; periksa nama variabel. |
# | KeyError | Cocokkan nama kolom dengan `print(data.columns)`. |
# | ModuleNotFoundError | Pada komputer lokal, pasang paket dari requirements.txt sebelum membuka notebook. |
# | ValueError tentang fitur/NaN | Pastikan daftar kolom sama; gunakan imputer yang sudah dilatih. |
#
# ### Rujukan
#
# - Gambar slide: **slide/png_regresi_tajam/**, terutama halaman 17-30 (6000 × 3375 piksel).
# - [Definisi variabel Boston Housing, Carnegie Mellon](https://lib.stat.cmu.edu/datasets/boston).
# - [Catatan dataset Boston Housing, scikit-learn](https://scikit-learn.org/1.1/modules/generated/sklearn.datasets.load_boston.html).
# - [Pencegahan data leakage, scikit-learn](https://scikit-learn.org/stable/common_pitfalls.html).
# - [Definisi R², scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.r2_score.html).
# - [Definisi VIF, statsmodels](https://www.statsmodels.org/stable/generated/statsmodels.stats.outliers_influence.variance_inflation_factor.html).
