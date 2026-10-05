# %% [markdown]
# # Hari 1, Sesi 6: Data Panel dan Model Volatilitas GARCH
#
# **Durasi:** 90 menit
#
# Dua topik dari Pertemuan 14 dan 15.
#
# **Panel.** Struktur datanya individu x waktu. Pertanyaan utamanya: model
# mana yang cocok, Common Effect (CEM), Fixed Effect (FEM), atau Random
# Effect (REM)? Jawabannya lewat tiga uji: Chow, Hausman, dan LM.
#
# **GARCH.** Data keuangan punya pola "tenang mengelompok, gejolak
# mengelompok" (volatility clustering). OLS tidak bisa menangkap ini karena
# GARCH memodelkan varians, bukan rata-rata.

# %% [markdown]
# **Posisi dalam alur workshop.** Sesi penutup Hari 1: panel menggabungkan
# banyak unit dan waktu, GARCH mengganti objek pemodelan dari rata-rata ke
# varians. Hari 2 mengulang alur ini sebagai latihan.

# %% [markdown]
# ## Persiapan: pastikan data tersedia
#
# Notebook ini membaca CSV dari folder `data/`. Kalau belum ada (misalnya di
# Colab), unggah `data-ekonometrika.zip` lewat panel Files, lalu jalankan
# sel di bawah sekali. Paket `linearmodels` dan `arch` juga dipasang di sini.

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
%pip install linearmodels arch -q

# %%
import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", palette=["#2F5D50", "#C15937", "#D9A441", "#5B8A8F"])
plt.rcParams.update({"figure.dpi": 110, "axes.titleweight": "bold", "font.size": 11})

# %% [markdown]
# ## Bagian 1: Data panel
#
# Data `panel-gdp.csv`: 10 negara x 5 tahun. GDP dijelaskan FDI dan tenaga
# kerja. Pertama, data diubah ke format panel: indeks dua level, entity dan
# waktu.

# %%
gdp = pd.read_csv("data/panel-gdp.csv")
panel = gdp.set_index(["CountryID", "Year"])
panel.head()

# %%
from linearmodels.panel import PanelOLS, RandomEffects

y = panel["GDP_Y"]
X = panel[["FDI_X1", "Labor_X2"]]

# Common Effect (semua individu disatukan)
cem = PanelOLS(y, sm.add_constant(X)).fit(cov_type="clustered", cluster_entity=True)
# Catatan: di linearmodels, summary adalah properti, jadi tanpa tanda
# kurung. statsmodels memakai summary() dengan tanda kurung.
print(cem.summary)

# %%
# Fixed Effect (tiap negara punya intersep sendiri)
fem = PanelOLS(y, X, entity_effects=True).fit(cov_type="clustered", cluster_entity=True)
print(fem.summary)

# %%
# Random Effect (perbedaan antarnegara dianggap acak)
rem = RandomEffects(y, sm.add_constant(X)).fit(cov_type="clustered", cluster_entity=True)
print(rem.summary)

# %% [markdown]
# ### Uji pemilihan model
#
# | Uji | Membandingkan | Kesimpulan |
# |---|---|---|
# | Chow | CEM vs FEM | p < 0,05 pilih FEM |
# | Hausman | FEM vs REM | p < 0,05 pilih FEM |
# | LM | CEM vs REM | p < 0,05 pilih REM |
#
# Uji Chow tersedia langsung sebagai `f_pooled` dari model FEM. Hausman
# dihitung manual dengan rumus standarnya.

# %%
print("Uji Chow (poolability F-test):")
print(fem.f_pooled)

# %%
# Hausman: bandingkan koefisien FEM dan REM
from scipy.stats import chi2

nama_sama = [v for v in fem.params.index if v in rem.params.index]
beda = fem.params[nama_sama] - rem.params[nama_sama]
selisih_cov = fem.cov.loc[nama_sama, nama_sama] - rem.cov.loc[nama_sama, nama_sama]
# Statistik Hausman: selisih koefisien dibobot oleh selisih kovariansnya.
# pinv (pseudo-inverse) dipakai karena matriks selisih bisa singular.
stat_h = float(beda.values @ np.linalg.pinv(selisih_cov.values) @ beda.values)
p_h = chi2.sf(stat_h, len(nama_sama))
print(f"Hausman stat = {stat_h:.4f}, p = {p_h:.4f}")
print("p < 0,05: pilih Fixed Effect; p besar: pilih Random Effect.")

# %% [markdown]
# ### Membaca hasil pemilihan model
#
# Di data ini hasilnya bercabang, dan itu contoh nyata kenapa keputusan
# model tidak boleh hanya membaca satu p-value:
#
# - Uji Chow (p = 0,0000) menolak CEM, jadi efek individu nyata.
# - Hausman menghasilkan p = 0,098. Pada taraf 5% kita gagal menolak REM,
#   jadi keputusan akhirnya memakai Random Effect.
#
# Perhatikan: p Hausman 0,098 tidak "jelas REM" dan tidak "jelas FEM". Kalau
# taraf digeser ke 10%, kesimpulannya berbalik. Karena itu, laporkan
# p-value mentahnya, bukan sekadar "p < 0,05".

# %%
tabel = pd.DataFrame({
    "koefisien": rem.params,
    "std_err": rem.std_errors,
    "p_value": rem.pvalues,
})
tabel.round(4)


# %% [markdown]
# ### Coba sendiri (5 menit)
#
# Hausman tadi menghasilkan p = 0,098. Kalau taraf ujinya digeser ke
# 10 persen, model mana yang dipilih? Apa pesan metodologisnya?
#
# Tulis di sel di bawah, baru buka jawabannya.

# %%
# Tulis jawaban singkat Anda di sini

# %% [markdown]
# <details><summary>Lihat jawaban</summary>
#
# Pada taraf 10 persen, H0 ditolak, jadi pilih Fixed Effect. Pesannya:
# keputusan model bergantung taraf uji, karena itu laporkan p-value
# mentahnya, bukan hanya kata 'signifikan'.
#
# </details>

# %% [markdown]
# Panel selesai. Sekarang ganti fokus: yang dimodelkan bukan lagi rata-rata,
# melainkan varians.
#
# ## Bagian 2: GARCH
#
# Data `volatilitas.csv` berisi return saham 50 periode. Pola yang dicari:
# volatilitas mengelompok.

# %%
volatilitas = pd.read_csv("data/volatilitas.csv")
ret = volatilitas["Kasus_1_Saham_Return"]

fig, ax = plt.subplots(figsize=(9, 4))
ax.plot(ret, lw=1.4)
ax.axhline(0, color="gray", lw=0.8)
ax.set_xlabel("Periode")
ax.set_ylabel("Return")
ax.set_title("Return saham: ada periode tenang dan periode bergolak")
plt.show()

# %% [markdown]
# ## 2.1 Uji efek ARCH
#
# Langkah di EViews: estimasi persamaan mean dulu (`return c`), lalu
# View > Residual Diagnostics > Heteroskedasticity Tests > ARCH. Di
# statsmodels namanya `het_arch`.

# %%
from statsmodels.stats.diagnostic import het_arch

model_mean = smf.ols("Kasus_1_Saham_Return ~ 1", data=volatilitas).fit()
p_arch = het_arch(model_mean.resid, nlags=4)[1]
print(f"ARCH LM test: p-value = {p_arch:.4f}")
print("p < 0,05: ada efek ARCH, lanjut ke GARCH.")

# %% [markdown]
# ## 2.2 Estimasi GARCH(1,1)
#
# Persamaan variansnya:
#
# $$\sigma_t^2 = \omega + \alpha \varepsilon_{t-1}^2 + \beta \sigma_{t-1}^2$$
#
# - $\alpha$: reaksi terhadap guncangan baru
# - $\beta$: persistensi volatilitas lama
# - $\alpha + \beta$ mendekati 1 berarti volatilitas hilang perlahan

# %%
from arch import arch_model

model_garch = arch_model(ret, vol="Garch", p=1, q=1, rescale=True)
hasil_garch = model_garch.fit(disp="off")
print(hasil_garch.summary())

# %%
alpha = hasil_garch.params["alpha[1]"]
beta = hasil_garch.params["beta[1]"]
print(f"alpha = {alpha:.4f}")
print(f"beta  = {beta:.4f}")
print(f"alpha + beta = {alpha + beta:.4f}")

# %%
plt.figure(figsize=(9, 4))
plt.plot(hasil_garch.conditional_volatility, lw=1.5)
plt.title("Volatilitas bersyarat hasil GARCH(1,1)")
plt.xlabel("Periode")
plt.ylabel("Sigma")
plt.show()


# %% [markdown]
# Perhatikan puncak volatilitas di sekitar periode 26 sampai 30, tepat saat
# guncangan besar terjadi. Inilah yang tidak bisa ditangkap OLS.
#
# ### Kenapa beta = 0?
#
# Di data simulasi ini, semua reaksi volatilitas masuk lewat guncangan
# terbaru saja (murni ARCH), sehingga estimator menempatkan beta di nol.
# Di data keuangan nyata, beta biasanya 0,8 sampai 0,9 dan jumlah
# alpha + beta mendekati 0,95.
#
# Supaya terlihat bedanya, kita bangkitkan data dengan proses GARCH(1,1)
# asli (alpha = 0,12 dan beta = 0,83), lalu estimasi ulang.

# %%
rng = np.random.default_rng(42)
n = 1500
alpha_asli, beta_asli = 0.12, 0.83
sigma2 = np.zeros(n)
eps = np.zeros(n)
sigma2[0] = 1.0
# Simulasi GARCH(1,1): tiap periode, guncangan dibuat dari sigma saat ini,
# lalu sigma periode berikutnya mengikuti omega + alpha*eps^2 + beta*sigma^2.
for t in range(1, n):
    eps[t - 1] = np.sqrt(sigma2[t - 1]) * rng.normal()
    sigma2[t] = 0.05 + alpha_asli * eps[t - 1] ** 2 + beta_asli * sigma2[t - 1]

hasil_sim = arch_model(pd.Series(eps), vol="Garch", p=1, q=1).fit(disp="off")
print("Parameter asli    : alpha = 0.12, beta = 0.83")
print(f"Parameter estimasi: alpha = {hasil_sim.params['alpha[1]']:.3f}, "
      f"beta = {hasil_sim.params['beta[1]']:.3f}")
print(f"Persistensi (alpha + beta) = "
      f"{hasil_sim.params['alpha[1]'] + hasil_sim.params['beta[1]']:.3f}")

# %% [markdown]
# Sekarang bandingkan persistensi lintas kasus di `volatilitas.csv`.

# %%
for nama, kolom in [("Saham", "Kasus_1_Saham_Return"),
                    ("Forex", "Kasus_2_Forex_Return"),
                    ("Kripto", "Kasus_3_Kripto_Return")]:
    hasil = arch_model(volatilitas[kolom], vol="Garch", p=1, q=1, rescale=True).fit(disp="off")
    a = hasil.params["alpha[1]"]
    b = hasil.params["beta[1]"]
    print(f"{nama:8s} alpha={a:.3f}  beta={b:.3f}  alpha+beta={a + b:.3f}")

# %% [markdown]
# ### Coba sendiri (5 menit)
#
# Ubah simulasi: `alpha_asli = 0.3` dan `beta_asli = 0.6`. Jalankan
# ulang. Apakah estimator masih mendekati angka aslinya?
#
# Tulis di sel di bawah, baru buka jawabannya.

# %%
# Tulis kode Anda di sini

# %% [markdown]
# <details><summary>Lihat jawaban</summary>
#
# Hasil tipikal: alpha 0,34 dan beta 0,54 (persistensi 0,88; aslinya
# 0,90). Estimator tetap dekat, hanya perlu data yang cukup panjang.
#
# </details>

# %% [markdown]
# ## 2.3 Ringkasan alur GARCH
#
# 1. Estimasi persamaan mean (biasanya konstanta atau ARMA).
# 2. Uji efek ARCH pada residual. Kalau tidak ada, cukup OLS/ARIMA.
# 3. Kalau ada, estimasi GARCH(1,1). Bandingkan orde lain lewat AIC.
# 4. Uji diagnostik: ARCH LM pada residual standar GARCH. Harapannya sudah
#    bersih (p > 0,05).
# 5. Pakai untuk memodelkan risiko: nilai VaR, peramalan volatilitas.

# %% [markdown]
# ## Latihan
#
# 1. Panel kasus retail: `data/panel-retail.csv` (5 toko x 10 bulan,
#    `Sales_Y ~ Ads_X1 + Discount_X2`). Jalankan CEM, FEM, REM, lalu
#    putuskan model mana yang dipakai berdasarkan uji Chow dan Hausman.
#    Bandingkan koefisien diskon di model CEM dan FEM. Kenapa arahnya
#    berubah?
# 2. GARCH: jalankan ulang model saham dengan GARCH(2,1). Bandingkan AIC
#    dengan GARCH(1,1). Tambahan orde sepadan hanya kalau AIC turun
#    setidaknya 2 poin dan koefisien baru signifikan.
# 3. Opsional kalau ada internet: unduh data IHSG harian dengan
#    `yfinance` (`^JKSE`), hitung log-return, dan ulangi langkah GARCH.
#    Di data nyata, beta biasanya 0,8 sampai 0,9 dan alpha + beta
#    mendekati 0,95.
#
# ```python
# %pip install yfinance -q
# import yfinance as yf
# ihsg = yf.download("^JKSE", start="2023-01-01", end="2025-01-01")
# return_ihsg = 100 * np.log(ihsg["Close"]).diff().dropna()
# ```

# %% [markdown]
# ### Selanjutnya
#
# Selanjutnya: Hari 2, latihan mandiri dengan urutan yang sama, ditutup
# data Indonesia asli.
