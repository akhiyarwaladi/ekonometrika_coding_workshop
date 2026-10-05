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
# ## Persiapan: pastikan data tersedia
#
# Notebook ini membaca CSV dari folder `data/`. Kalau belum ada (misalnya di
# Colab), unggah `data-ekonometrika.zip` lewat panel Files, lalu jalankan
# sel di bawah sekali.

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

inflasi = pd.read_csv("data/ts-inflasi.csv")
saham_ts = pd.read_csv("data/ts-saham.csv")
gdp = pd.read_csv("data/ts-gdp-growth.csv")
kurs = pd.read_csv("data/ts-kurs.csv")

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
for ax, kolom, judul in [
    (axes[0, 0], "inflasi", "Inflasi: tren deterministik"),
    (axes[0, 1], "saham", "Harga saham: random walk"),
    (axes[1, 0], "gdp_growth", "Pertumbuhan GDP: siklus"),
    (axes[1, 1], "kurs", "Kurs: patahan struktural"),
]:
    ax.plot(timeline["obs"], timeline[kolom], lw=1.6)
    ax.set_title(judul, fontsize=10)
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

def laporan_adf(seri, nama):
    p = adfuller(seri)[1]
    status = "stasioner" if p < 0.05 else "TIDAK stasioner"
    print(f"{nama:28s} p-value = {p:.4f}   {status}")

print("--- Level ---")
for kolom in ["inflasi", "saham", "gdp_growth", "kurs"]:
    laporan_adf(timeline[kolom], kolom)

print("\n--- Setelah selisih pertama ---")
for kolom in ["inflasi", "saham", "gdp_growth", "kurs"]:
    laporan_adf(timeline[kolom].diff().dropna(), f"d({kolom})")

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

hasil_arima = {}
for p in range(3):
    for q in range(3):
        hasil_arima[(p, q)] = ARIMA(timeline["gdp_growth"], order=(p, 0, q)).fit().aic

pd.Series(hasil_arima).unstack().round(1)

# %%
p_terbaik, q_terbaik = min(hasil_arima, key=hasil_arima.get)
print(f"Orde dengan AIC terkecil: ARIMA({p_terbaik}, 0, {q_terbaik})")

model_terbaik = ARIMA(timeline["gdp_growth"], order=(p_terbaik, 0, q_terbaik)).fit()
print(model_terbaik.summary())

# %%
lb = acorr_ljungbox(model_terbaik.resid, lags=[10], return_df=True)
print("Uji Ljung-Box (p > 0,05 berarti residual sudah white noise):")
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
ax.fill_between(masa_depan, batas.iloc[:, 0], batas.iloc[:, 1], alpha=0.2, label="interval 95%")
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
# AIC ARIMA(1,0,1) = 9,3, jauh lebih besar dari ARIMA(2,1) yang -41,0.
# Orde (2,1) tetap juara di tabel.
#
# </details>

# %% [markdown]
# ## 5. Patahan struktural pada kurs
#
# Kurs stabil di sekitar 14.000, lalu melonjak ke 15.000, lalu stabil lagi.
# ADF tidak dirancang untuk pola begini. Cara praktis: uji dengan dummy
# periode setelah patahan. Di EViews, ini setara Chow test.

# %%
timeline["pasca"] = (timeline["obs"] >= 25).astype(int)
model_kurs = smf.ols("kurs ~ obs + pasca", data=timeline).fit()
print(model_kurs.summary())

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
# 3. Uji residual dengan ADF. Kalau stasioner, ada kointegrasi.

# %%
makro = pd.read_csv("data/konsumsi-pendapatan.csv").rename(columns={
    "Konsumsi_Y": "konsumsi", "Pendapatan_X": "pendapatan"})
makro["ln_konsumsi"] = np.log(makro["konsumsi"])
makro["ln_pendapatan"] = np.log(makro["pendapatan"])

print("ADF level:")
laporan_adf(makro["ln_konsumsi"], "ln(konsumsi)")
laporan_adf(makro["ln_pendapatan"], "ln(pendapatan)")

model_lr = smf.ols("ln_konsumsi ~ ln_pendapatan", data=makro).fit()
print("\n--- Persamaan jangka panjang ---")
print(model_lr.summary())

# %%
from statsmodels.tsa.stattools import coint

# Resep Engle-Granger bertahap: uji residual persamaan jangka panjang
laporan_adf(model_lr.resid, "residual jangka panjang")

# Cara cepat dengan p-value langsung dari fungsi coint
p_kointe = coint(makro["ln_konsumsi"], makro["ln_pendapatan"])[1]
print(f"Uji kointegrasi Engle-Granger: p = {p_kointe:.4f}")
print("p < 0,05 berarti kedua variabel terkointegrasi.")

# %% [markdown]
# Koefisien jangka panjang di atas (elastisitas konsumsi terhadap
# pendapatan) hanya bisa dipercaya setelah kointegrasi terbukti. Tanpa itu,
# R kuadrat tinggi pada dua variabel tren bisa menyesatkan.


# %% [markdown]
# ### Coba sendiri (5 menit)
#
# Uji kointegrasi untuk kasus lain: `data/ekspor-kurs.csv`.
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
makro["ect"] = model_lr.resid.shift(1)

model_ecm = smf.ols("d_konsumsi ~ d_pendapatan + ect", data=makro).fit()
print(model_ecm.summary())

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
#    (`data/ihsg-emas.csv`). Apakah keduanya terkointegrasi? Kalau tidak,
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
