# %% [markdown]
# # Hari 1, Sesi 5: Deret Waktu, Stasioneritas, Kointegrasi, dan ECM
#
# **Durasi:** 75 menit
#
# Alur berpikir yang harus terbawa:
#
# 1. Plot data dulu. Tren, siklus, dan lompatan struktural terlihat mata.
# 2. Uji akar unit (ADF). Kalau tidak stasioner di level, ambil selisih.
# 3. Kalau ada dua variabel yang sama-sama tidak stasioner, periksa
#    kointegrasi sebelum meregresikan apa pun. Regresi dua variabel tren
#    tanpa kointegrasi adalah regresi palsu (spurious).
# 4. Kalau terkointegrasi, pakai Error Correction Model (ECM).

# %% [markdown]
# **Posisi dalam alur workshop.** Sesi 1-4 memakai data cross-section.
# Sesi ini menambahkan dimensi waktu, dari stasioneritas sampai ECM. Sesi
# 6 menutup dengan data panel dan GARCH.

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

# %% [markdown]
# <!-- kamus_variabel:ts_gdp_growth.csv -->
#
# ### Kenali data: Pertumbuhan ekonomi simulasi
#
# **Data:** `data/ts_gdp_growth.csv`. **Satu baris:** satu urutan periode simulasi; bukan tanggal kalender.
#
# | Variabel/kolom | Pengertian | Satuan atau kode | Peran |
# |---|---|---|---|
# | `obs` | Urutan waktu pengamatan. | 1, 2, 3, ...; frekuensi kalender tidak dirinci | Penanda waktu |
# | `gdp_growth` | GDP growth: laju pertumbuhan Produk Domestik Bruto. | Persen dalam konteks pertumbuhan | Deret yang dianalisis |
#
# Nomor obs tidak menunjukkan tanggal/bulan/tahun tertentu. Angka level dan perubahan persennya harus dibedakan.
#
# Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

# %% [markdown]
# <!-- kamus_variabel:ts_kurs.csv -->
#
# ### Kenali data: Kurs simulasi
#
# **Data:** `data/ts_kurs.csv`. **Satu baris:** satu urutan periode simulasi; bukan tanggal kalender.
#
# | Variabel/kolom | Pengertian | Satuan atau kode | Peran |
# |---|---|---|---|
# | `obs` | Urutan waktu pengamatan. | 1, 2, 3, ...; frekuensi kalender tidak dirinci | Penanda waktu |
# | `kurs` | Nilai tukar simulasi yang mengalami perubahan level di tengah periode. | Level kurs; pasangan mata uang tidak dirinci sumber tabel | Deret yang dianalisis |
#
# Nomor obs tidak menunjukkan tanggal/bulan/tahun tertentu. Angka level dan perubahan persennya harus dibedakan.
#
# Kolom turunan berikut dibuat saat praktik; kolom ini belum ada pada CSV awal.
#
# | Kolom turunan | Pengertian | Satuan/kode |
# |---|---|---|
# | `pasca` | Indikator perubahan level mulai pengamatan ke-25 pada contoh. | 1 jika obs ≥ 25; 0 sebelumnya |
#
# Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

# %%
import pandas as pd
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", palette=["#2F5D50", "#C15937", "#D9A441", "#5B8A8F"])
plt.rcParams.update({"figure.dpi": 110, "axes.titleweight": "bold", "font.size": 11})

inflasi = pd.read_csv(URL_DATA + "ts_inflasi.csv")
saham_ts = pd.read_csv(URL_DATA + "ts_saham.csv")
gdp = pd.read_csv(URL_DATA + "ts_gdp_growth.csv")
kurs = pd.read_csv(URL_DATA + "ts_kurs.csv")

timeline = inflasi.merge(saham_ts, on="obs").merge(gdp, on="obs").merge(kurs, on="obs")
timeline.head()

# %% [markdown]
# ## 1. Lihat dulu bentuk datanya
#
# Empat tipe deret waktu, persis seperti empat kasus di Pertemuan 12: tren
# naik terus (inflasi), jalan acak (saham), siklus naik-turun (pertumbuhan
# ekonomi), dan patahan struktural (kurs).

# %%
fig, axes = plt.subplots(2, 2, figsize=(11, 7))
axes[0, 0].plot(timeline["obs"], timeline["inflasi"])
axes[0, 0].set_title("Inflasi: tren deterministik")
axes[0, 1].plot(timeline["obs"], timeline["saham"])
axes[0, 1].set_title("Harga saham: random walk")
axes[1, 0].plot(timeline["obs"], timeline["gdp_growth"])
axes[1, 0].set_title("Pertumbuhan GDP: siklus")
axes[1, 1].plot(timeline["obs"], timeline["kurs"])
axes[1, 1].set_title("Kurs: patahan struktural")
plt.tight_layout()
plt.show()

# %% [markdown]
# ## 2. Uji akar unit (ADF)
#
# Hipotesis nol ADF: data punya akar unit (tidak stasioner). p-value kecil
# berarti data stasioner. Uji di level dulu, lalu setelah satu kali selisih
# (first difference) kalau perlu.

# %%
from statsmodels.tsa.stattools import adfuller

# adfuller() mengeluarkan beberapa hasil; posisi [1] adalah p-value.
print("ADF pada level:")
print("Inflasi:", adfuller(timeline["inflasi"])[1])
print("Saham:", adfuller(timeline["saham"])[1])
print("Pertumbuhan GDP:", adfuller(timeline["gdp_growth"])[1])
print("Kurs:", adfuller(timeline["kurs"])[1])

# %%
# diff() menghitung selisih dengan periode sebelumnya.
# dropna() membuang baris pertama yang belum mempunyai selisih.
print("ADF setelah selisih pertama:")
print("Inflasi:", adfuller(timeline["inflasi"].diff().dropna())[1])
print("Saham:", adfuller(timeline["saham"].diff().dropna())[1])
print("Pertumbuhan GDP:", adfuller(timeline["gdp_growth"].diff().dropna())[1])
print("Kurs:", adfuller(timeline["kurs"].diff().dropna())[1])

# %% [markdown]
# Bacaan hasilnya: inflasi dan saham tidak stasioner di level, stasioner
# setelah selisih. GDP growth sudah stasioner di level. Kurs tetap sulit
# karena ada patahan; di bagian 5 kita tangani dengan dummy.

# %% [markdown]
# ## 3. ACF dan PACF
#
# Dua grafik ini membantu menebak orde AR (p) dan MA (q).

# %%
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

fig, axes = plt.subplots(2, 1, figsize=(9, 6))
plot_acf(timeline["gdp_growth"], lags=15, ax=axes[0])
plot_pacf(timeline["gdp_growth"], lags=15, ax=axes[1])
plt.tight_layout()
plt.show()

# %% [markdown]
# ## 4. ARIMA: estimasi dan peramalan
#
# Data GDP growth stasioner, jadi kita pakai ARIMA(p, 0, q). Untuk data yang
# perlu satu kali selisih, d = 1.
#
# Pemilihan orde: bandingkan AIC beberapa kandidat. Di bawah ini dipilih
# otomatis yang terkecil.

# %%
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.stats.diagnostic import acorr_ljungbox

# Kita tetap membandingkan sembilan kandidat p=0..2 dan q=0..2.
# Tiga angka pada order adalah (p, d, q); d=0 karena seri ini stasioner.
model_000 = ARIMA(timeline["gdp_growth"], order=(0, 0, 0)).fit()
model_001 = ARIMA(timeline["gdp_growth"], order=(0, 0, 1)).fit()
model_002 = ARIMA(timeline["gdp_growth"], order=(0, 0, 2)).fit()
model_100 = ARIMA(timeline["gdp_growth"], order=(1, 0, 0)).fit()
model_101 = ARIMA(timeline["gdp_growth"], order=(1, 0, 1)).fit()
model_102 = ARIMA(timeline["gdp_growth"], order=(1, 0, 2)).fit()
model_200 = ARIMA(timeline["gdp_growth"], order=(2, 0, 0)).fit()
model_201 = ARIMA(timeline["gdp_growth"], order=(2, 0, 1)).fit()
model_202 = ARIMA(timeline["gdp_growth"], order=(2, 0, 2)).fit()

# %%
perbandingan = pd.DataFrame(
    {
        "orde": [
            (0, 0, 0),
            (0, 0, 1),
            (0, 0, 2),
            (1, 0, 0),
            (1, 0, 1),
            (1, 0, 2),
            (2, 0, 0),
            (2, 0, 1),
            (2, 0, 2),
        ],
        "AIC": [
            model_000.aic,
            model_001.aic,
            model_002.aic,
            model_100.aic,
            model_101.aic,
            model_102.aic,
            model_200.aic,
            model_201.aic,
            model_202.aic,
        ],
    }
)
urutan = perbandingan.sort_values("AIC")
print(urutan)

# %%
# iloc[0] memilih baris pertama dari tabel yang sudah diurutkan.
orde_terbaik = urutan.iloc[0]["orde"]
p_terbaik = orde_terbaik[0]
q_terbaik = orde_terbaik[2]
print("Orde dengan AIC terkecil:", orde_terbaik)
model_terbaik = ARIMA(timeline["gdp_growth"], order=orde_terbaik).fit()
print(model_terbaik.summary())

# %%
lb = acorr_ljungbox(
    model_terbaik.resid, lags=[10], model_df=p_terbaik + q_terbaik, return_df=True
)
print("Ljung-Box: p > 0,05 berarti belum ada bukti autokorelasi sampai lag yang diuji.")
print(lb)

# %% [markdown]
# AIC memilih orde cukup tinggi di sini karena datanya siklus yang mulus.
# Di data nyata, imbangi dengan prinsip parsimoni: kalau selisih AIC dua
# model kurang dari 2, anggap seri dan pilih yang lebih sederhana.

# %%
ramalan = model_terbaik.get_forecast(steps=6)
# conf_int() bisa mengembalikan DataFrame atau array tergantung versi
# statsmodels; disamakan jadi DataFrame supaya .iloc aman dipakai
batas = pd.DataFrame(ramalan.conf_int(alpha=0.05))

fig, ax = plt.subplots(figsize=(9, 4.5))
ax.plot(timeline["obs"], timeline["gdp_growth"], label="aktual")
masa_depan = np.arange(len(timeline) + 1, len(timeline) + 7)  # setelah periode 50
ax.plot(masa_depan, np.asarray(ramalan.predicted_mean), marker="o", label="ramalan")
ax.fill_between(
    masa_depan, batas.iloc[:, 0], batas.iloc[:, 1], alpha=0.2, label="interval 95%"
)
ax.legend()
ax.set_xlabel("Periode")
ax.set_ylabel("Pertumbuhan GDP")
plt.show()

# %% [markdown]
# ### Coba sendiri (5 menit)
#
# Jalankan ARIMA(1, 0, 1) pada `gdp_growth` dan bandingkan AIC-nya
# dengan tabel kandidat di atas.
#
# Tulis di sel di bawah, baru buka jawabannya.

# %%
# Tulis kode Anda di sini

# %% [markdown]
# <details><summary>Lihat jawaban</summary>
#
# Bandingkan AIC model_101 dengan tabel kandidat. Angka yang lebih kecil
# lebih disukai. Tulis orde lengkap (p, d, q), misalnya (2, 0, 1),
# supaya orde MA tidak tertukar dengan jumlah differencing.
#
# </details>

# %% [markdown]
# ## 5. Patahan struktural pada kurs
#
# Kurs stabil di sekitar 14.000, lalu melonjak ke 15.000, lalu stabil lagi.
# ADF tidak dirancang untuk pola begini. Cara praktis: uji dengan dummy
# periode setelah patahan. Ini memeriksa pergeseran intersep pada tanggal
# yang ditentukan, bukan uji Chow penuh untuk semua koefisien.

# %%
timeline["pasca"] = (timeline["obs"] >= 25).astype(int)
sampel_model_kurs = timeline[["kurs", "obs", "pasca"]].dropna()
X_model_kurs = sampel_model_kurs[["obs", "pasca"]]
y_model_kurs = sampel_model_kurs["kurs"]

model_kurs = LinearRegression()
model_kurs.fit(X_model_kurs, y_model_kurs)

# Pelengkap statistik: standard error dan pengujian pada sampel yang sama.
uji_model_kurs = sm.OLS(
    y_model_kurs,
    sm.add_constant(X_model_kurs, has_constant="add").rename(
        columns={"const": "Intercept"}
    ),
).fit()
print(uji_model_kurs.summary())

# %% [markdown]
# Kalau koefisien `pasca` besar dan signifikan, lompatan levelnya nyata.
# Konsekuensinya untuk peramalan: jangan pakai satu garis tren lurus untuk
# seluruh periode.

# %% [markdown]
# ## 6. Kointegrasi: konsumsi dan pendapatan
#
# Dua variabel yang sama-sama tidak stasioner bisa tetap punya hubungan
# jangka panjang. Istilahnya kointegrasi. Analogi dari kuliah: pria mabuk
# dan anjingnya yang diikat tali, jalan masing-masing acak, tapi tidak
# pernah berpisah jauh.
#
# Langkah uji Engle-Granger versi ringkas:
# 1. Regresikan Y pada X (persamaan jangka panjang).
# 2. Ambil residualnya.
# 3. Uji akar unit residual dengan nilai kritis Engle-Granger melalui `coint()`.
#    Pastikan kedua seri berorde integrasi yang sama, umumnya I(1).

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
makro = pd.read_csv(URL_DATA + "konsumsi_pendapatan.csv")
makro = makro.rename(columns={"Konsumsi_Y": "konsumsi", "Pendapatan_X": "pendapatan"})
makro["ln_konsumsi"] = np.log(makro["konsumsi"])
makro["ln_pendapatan"] = np.log(makro["pendapatan"])

print("ADF level:")
print("ln(konsumsi):", adfuller(makro["ln_konsumsi"])[1])
print("ln(pendapatan):", adfuller(makro["ln_pendapatan"])[1])

sampel_model_lr = makro[["ln_konsumsi", "ln_pendapatan"]].dropna()
X_model_lr = sampel_model_lr[["ln_pendapatan"]]
y_model_lr = sampel_model_lr["ln_konsumsi"]

model_lr = LinearRegression()
model_lr.fit(X_model_lr, y_model_lr)

prediksi_model_lr = pd.Series(model_lr.predict(X_model_lr), index=y_model_lr.index)
residu_model_lr = y_model_lr - prediksi_model_lr

# Pelengkap statistik: standard error dan pengujian pada sampel yang sama.
uji_model_lr = sm.OLS(
    y_model_lr,
    sm.add_constant(X_model_lr, has_constant="add").rename(
        columns={"const": "Intercept"}
    ),
).fit()
print("\n--- Persamaan jangka panjang ---")
print(uji_model_lr.summary())

# %%
from statsmodels.tsa.stattools import coint

# Residual jangka panjang boleh digambar untuk melihat pola. Untuk keputusan
# kointegrasi, coint() memakai nilai kritis Engle-Granger yang sesuai.
# p-value ADF biasa pada residual hasil estimasi bukan penggantinya.

# Cara cepat dengan p-value langsung dari fungsi coint

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
print(f"Uji kointegrasi Engle-Granger: p = {p_kointe:.4f}")
print("Baca p-value ini bersama catatan orde integrasi pada data contoh.")

# %% [markdown]
# Koefisien jangka panjang di atas (elastisitas konsumsi terhadap
# pendapatan) hanya bisa dipercaya setelah kointegrasi terbukti. Tanpa itu,
# R kuadrat tinggi pada dua variabel tren bisa menyesatkan.

# %% [markdown]
# ### Coba sendiri (5 menit)
#
# Uji kointegrasi untuk kasus lain: `data/ekspor_kurs.csv`.
# Apakah ekspor dan kurs terkointegrasi?
#
# Tulis di sel di bawah, baru buka jawabannya.

# %%
# Tulis kode Anda di sini

# %% [markdown]
# <details><summary>Lihat jawaban</summary>
#
# `coint(ek["Ekspor_Y"], ek["Kurs_X"])` memberi p = 0,0016. Di bawah
# 0,05, jadi terkointegrasi. Bandingkan dengan IHSG-emas di Latihan yang
# tidak terkointegrasi.
#
# </details>

# %% [markdown]
# ## 7. Error Correction Model (ECM)
#
# Maksud ECM: perubahan jangka pendek Y dipengaruhi perubahan X, PLUS
# koreksi dari ketidakseimbangan periode sebelumnya (ECT). ECT adalah
# residual jangka panjang yang di-lag satu periode.
#
# $$\Delta Y_t = \alpha_0 + \alpha_1 \Delta X_t + \gamma \, ECT_{t-1} + u_t$$
#
# Syarat mutlak: koefisien $\gamma$ negatif dan signifikan. Nilainya
# menunjukkan kecepatan penyesuaian.

# %%
makro["d_konsumsi"] = makro["ln_konsumsi"].diff()
makro["d_pendapatan"] = makro["ln_pendapatan"].diff()
makro["ect"] = residu_model_lr.shift(1)

sampel_model_ecm = makro[["d_konsumsi", "d_pendapatan", "ect"]].dropna()
X_model_ecm = sampel_model_ecm[["d_pendapatan", "ect"]]
y_model_ecm = sampel_model_ecm["d_konsumsi"]

model_ecm = LinearRegression()
model_ecm.fit(X_model_ecm, y_model_ecm)

# Pelengkap statistik: standard error dan pengujian pada sampel yang sama.
uji_model_ecm = sm.OLS(
    y_model_ecm,
    sm.add_constant(X_model_ecm, has_constant="add").rename(
        columns={"const": "Intercept"}
    ),
).fit()
print(uji_model_ecm.summary())

# %% [markdown]
# Baca tiga hal dari output:
#
# 1. Tanda dan signifikansi `ect`. Harus negatif dan p < 0,05.
# 2. Besarnya `ect` = kecepatan penyesuaian per periode. Nilai -0,70
#    berarti 70 persen ketidakseimbangan dikoreksi tiap periode.
# 3. Koefisien `d_pendapatan` = elastisitas jangka pendek.

# %% [markdown]
# ## Latihan
#
# 1. Jalankan uji kointegrasi dan ECM untuk kasus IHSG dan emas
#    (`data/ihsg_emas.csv`). Apakah keduanya terkointegrasi? Kalau tidak,
#    apakah ECM masih layak dipakai?
# 2. Ramalkan inflasi lima periode ke depan dengan ARIMA(1,1,0). Bandingkan
#    dengan ramalan yang memakai d = 0. Perhatikan polanya: d = 0 menarik
#    ramalan ke rata-rata, d = 1 meneruskan arah tren. Pilih yang sesuai
#    perilaku data.
# 3. Kenapa ADF pada kurs gagal mendeteksi stasioneritas walaupun secara
#    visual kurs terlihat "datar" di dua rezim? Hubungkan dengan konsep
#    patahan struktural.

# %% [markdown]
# ### Selanjutnya
#
# Selanjutnya: Sesi 6 menutup Hari 1 dengan data panel dan GARCH.
