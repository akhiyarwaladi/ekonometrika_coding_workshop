# %% [markdown]
# # Lab 6: Ekonometrika dengan Data Indonesia Asli
#
# **Durasi:** 90 menit
#
# Semua lab sebelumnya memakai data simulasi dari halaman kuliah. Lab ini
# memakai data Indonesia yang sungguhan, diunduh dari sumber terbuka:
#
# | File | Isi | Sumber |
# |---|---|---|
# | `ihsg-harian.csv` | IHSG harian, 2019 sampai 2026 | Yahoo Finance |
# | `ihsg-panjang.csv` | IHSG harian, 1990 sampai 2026 | Yahoo Finance |
# | `kurs-harian.csv` | Kurs USD/IDR harian, 2019 sampai 2026 | ECB via Frankfurter |
# | `idn-kurs-tahunan.csv` | Kurs tahunan, 1967 sampai 2025 | World Bank |
# | `idn-inflasi-bulanan.csv` | Inflasi bulanan, 1968 sampai 2025 | BPS via OECD/FRED |
# | `idn-makro-tahunan.csv` | Inflasi, PDB, pengangguran, kurs, 2000 sampai 2025 | World Bank |
# | `asean-panel.csv` | 10 negara ASEAN, 2000 sampai 2025 | World Bank |
# | `provinsi-2021.csv` | 34 provinsi: PDRB, IPM, kemiskinan, dll | kompilasi BPS |
#
# Semua file sudah tersedia di folder `data/`. Cara memperbarui datanya ada
# di akhir lab ini.

# %% [markdown]
# **Posisi dalam alur workshop.** Lab penutup: Lab 0-5 memakai data
# simulasi, lab ini memakai data Indonesia asli dan menggabungkan semua
# teknik. Setelah ini, lanjut ke proyek mini.

# %% [markdown]
# ## Persiapan: pastikan data tersedia

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
# ## 1. GARCH pada IHSG asli
#
# Inilah momen yang ditunggu: memakai data nyata yang volatilitasnya
# benar-benar mengelompok. Bandingkan hasilnya dengan data simulasi di
# Sesi 6 yang murni ARCH (beta = 0).

# %%
ihsg = pd.read_csv("data/ihsg-harian.csv", parse_dates=["Date"])
# Return logaritmik harian dalam persen: selisih log dikali 100
ihsg["ret"] = 100 * np.log(ihsg["Close"]).diff()
ihsg = ihsg.dropna()

print("Jumlah observasi:", len(ihsg))
print("Rentang:", ihsg["Date"].min().date(), "sampai", ihsg["Date"].max().date())

plt.figure(figsize=(10, 4))
plt.plot(ihsg["Date"], ihsg["ret"], lw=0.7)
plt.title("Return harian IHSG (persen)")
plt.xlabel("Tanggal")
plt.ylabel("Return")
plt.show()

# %% [markdown]
# Perhatikan lonjakan besar di sekitar Maret 2020 (COVID), lalu
# bandingkan dengan lonjakan pada 2025 dan 2026 yang lebih pendek.
# Sekarang uji efek ARCH, seperti di Sesi 6.

# %%
from statsmodels.stats.diagnostic import het_arch

# Regresi mean sederhana, hanya untuk mengambil residualnya
model_mean = smf.ols("ret ~ 1", data=ihsg).fit()
# [1] = p-value dari uji ARCH-LM
p_arch = het_arch(model_mean.resid, nlags=5)[1]
print(f"ARCH LM test: p-value = {p_arch:.3e}")
print("p jauh di bawah 0,05: efek ARCH sangat kuat.")

# %%
from arch import arch_model

hasil = arch_model(ihsg["ret"], vol="Garch", p=1, q=1).fit(disp="off")
print(hasil.summary())

# %%
alpha = hasil.params["alpha[1]"]
beta = hasil.params["beta[1]"]
print(f"alpha = {alpha:.4f}  (reaksi terhadap guncangan baru)")
print(f"beta  = {beta:.4f}  (persistensi volatilitas lama)")
print(f"alpha + beta = {alpha + beta:.4f}")
print()
print("Bandingkan dengan data simulasi Sesi 6: beta = 0, persistensi 0,81.")
print("Di data nyata, persistensi mendekati 0,95: guncangan hilang perlahan.")

# %% [markdown]
# ### Aplikasi sederhana: Value at Risk
#
# VaR 5 persen harian: berapa kerugian yang hanya terlampaui pada 5 persen
# hari terburuk. Ini cara cepat memakainya untuk manajemen risiko.

# %%
var95 = np.percentile(ihsg["ret"], 5)
print(f"VaR 5% harian: {var95:.3f} persen")
print(f"Untuk portofolio Rp 10 juta, risiko harian sekitar Rp {abs(var95) / 100 * 10_000_000:,.0f}")


# %% [markdown]
# ### Coba sendiri (5 menit)
#
# Dari volatilitas bersyarat GARCH IHSG tadi (`hasil.conditional_volatility`),
# cari tanggal dengan sigma tertinggi dan bandingkan dengan rata-ratanya.
#
# Tulis di sel di bawah, baru buka jawabannya.

# %%
# Tulis kode Anda di sini

# %% [markdown]
# <details><summary>Lihat jawaban</summary>
#
# Sigma tertinggi = 4,54 pada 27 Maret 2020 (puncak COVID), sementara
# rata-rata seluruh periode hanya 1,01. Artinya hari itu volatilitas
# 4,5 kali lebih besar dari hari biasa.
#
# </details>

# %% [markdown]
# ## 2. Panel ASEAN dengan data asli
#
# `asean-panel.csv` berisi 10 negara ASEAN, 2000 sampai 2025: pertumbuhan
# PDB, FDI (persen dari PDB), angkatan kerja, inflasi, dan pengangguran.
# Kita uji: apakah FDI berhubungan dengan pertumbuhan ekonomi?

# %%
panel = pd.read_csv("data/asean-panel.csv")
panel["ln_angkatan_kerja"] = np.log(panel["Angkatan_Kerja"])
print("Negara:", sorted(panel["Negara"].unique()))
panel.head()

# %%
from linearmodels.panel import PanelOLS, RandomEffects

data_panel = panel.set_index(["Negara", "Tahun"])
y = data_panel["PDB_Growth"]
X = data_panel[["FDI", "ln_angkatan_kerja"]]

cem = PanelOLS(y, sm.add_constant(X)).fit(cov_type="clustered", cluster_entity=True)
fem = PanelOLS(y, X, entity_effects=True).fit(cov_type="clustered", cluster_entity=True)
rem = RandomEffects(y, sm.add_constant(X)).fit(cov_type="clustered", cluster_entity=True)

print("=== CEM ===")
print(cem.params.round(4))
print("\n=== FEM ===")
print(fem.params.round(4))
print("\n=== REM ===")
print(rem.params.round(4))

# %% [markdown]
# ### Uji Chow dan Hausman

# %%
from scipy.stats import chi2

print("Uji Chow (CEM vs FEM):")
print(fem.f_pooled)

nama_sama = [v for v in fem.params.index if v in rem.params.index]
beda = fem.params[nama_sama] - rem.params[nama_sama]
selisih_cov = fem.cov.loc[nama_sama, nama_sama] - rem.cov.loc[nama_sama, nama_sama]
# Statistik Hausman: selisih koefisien dibobot selisih kovariansnya.
# pinv dipakai karena matriks selisih bisa singular.
stat_h = float(beda.values @ np.linalg.pinv(selisih_cov.values) @ beda.values)
print(f"\nHausman: stat = {stat_h:.4f}, p = {chi2.sf(stat_h, len(nama_sama)):.4f}")

# %% [markdown]
# ### Membaca hasil
#
# - Uji Chow menolak CEM: efek khas tiap negara nyata, jadi harus
#   diperhitungkan.
# - Hausman menolak REM (p di bawah 0,05), jadi keputusannya FEM.
# - Di FEM, koefisien FDI sekitar +0,21 dan signifikan. Artinya, DI DALAM
#   satu negara, tahun dengan FDI lebih tinggi cenderung tumbuh lebih
#   cepat. Di CEM koefisiennya hanya +0,09 dan tidak signifikan, karena
#   estimasi itu mencampur perbedaan antarnegara dengan perubahan dalam
#   negara.
# - Koefisien angkatan kerja negatif di FEM. Ini korelasi within, bukan
#   sebab akibat: periode dengan pertumbuhan angkatan kerja cepat
#   (misalnya setelah krisis) justru bersamaan dengan pertumbuhan PDB
#   yang lambat.


# %% [markdown]
# ### Coba sendiri (5 menit)
#
# Di bagian 2, Hausman memberi p = 0,0036. Model mana yang dipakai,
# dan apa artinya secara ekonomi untuk FDI?
#
# Tulis di sel di bawah, baru buka jawabannya.

# %%
# Tulis jawaban singkat Anda di sini

# %% [markdown]
# <details><summary>Lihat jawaban</summary>
#
# p < 0,05, jadi FEM. Artinya perbandingan antarnegara saja tidak cukup;
# yang dibaca adalah perubahan DI DALAM satu negara. Koefisien FDI +
# 0,21 berarti kenaikan FDI 1 poin persen berhubungan dengan
# pertumbuhan sekitar 0,21 poin persen lebih tinggi dalam negara yang sama.
#
# </details>

# %% [markdown]
# ## 3. Makro Indonesia tahunan
#
# Data 26 tahun, 2000 sampai 2025. Kita uji hubungan inflasi dan
# pengangguran, dua indikator yang selalu diberitakan bersama.

# %%
makro = pd.read_csv("data/idn-makro-tahunan.csv")
makro.tail()

# %%
plt.figure(figsize=(7, 4.5))
plt.scatter(makro["Pengangguran"], makro["Inflasi"])
plt.xlabel("Pengangguran (persen)")
plt.ylabel("Inflasi (persen)")
plt.title("Inflasi dan pengangguran Indonesia, 2000-2025")
plt.show()

# %%
model_makro = smf.ols("Inflasi ~ Pengangguran", data=makro).fit()
print(model_makro.summary())

# %% [markdown]
# ### Membaca hasil
#
# Koefisiennya positif dan sangat signifikan, kebalikan dari cerita
# Phillips curve klasik. Kenapa? Di Indonesia 2000-2025, periode dengan
# pengangguran tinggi (2005, 2008, 2020) justru bersamaan dengan inflasi
# tinggi karena keduanya didorong krisis, bukan hubungan sebab akibat
# langsung. Pelajaran: tanda koefisien harus dibaca dengan konteks sejarah,
# bukan sekadar mencocokkan teori.

# %% [markdown]
# ## 4. Kurs harian: stasioneritas
#
# Data kurs USD/IDR harian dari ECB. Uji ADF di level dan setelah selisih.

# %%
from statsmodels.tsa.stattools import adfuller

kurs = pd.read_csv("data/kurs-harian.csv", parse_dates=["Tanggal"])
print("Jumlah observasi:", len(kurs))
print("ADF di level      : p =", round(adfuller(kurs["Kurs_USD_IDR"])[1], 4))
print("ADF setelah selisih: p =", round(adfuller(kurs["Kurs_USD_IDR"].diff().dropna())[1], 4))

# %% [markdown]
# Seperti kurs di Sesi 5: tidak stasioner di level, stasioner setelah
# selisih. Ini pola khas nilai tukar.

# %% [markdown]
# ## 5. Krisis 1997-1998 dalam data asli
#
# Inflasi bulanan Indonesia tersedia sejak 1968, dan kurs tahunan sejak
# 1967. Keduanya menangkap krisis finansial Asia yang menghantam Indonesia
# pada 1997-1998: rupiah melemah dari sekitar 2.900 menjadi 10.000 per
# dolar, dan inflasi melonjak.

# %%
inflasi = pd.read_csv("data/idn-inflasi-bulanan.csv", parse_dates=["tanggal"])

plt.figure(figsize=(10, 4))
plt.plot(inflasi["tanggal"], inflasi["inflasi_yoy"], lw=0.8)
plt.axvspan(pd.Timestamp("1997-07-01"), pd.Timestamp("1999-12-31"),
            color="red", alpha=0.15)
plt.title("Inflasi tahunan (year-on-year) Indonesia, 1968-2025")
plt.xlabel("Tahun")
plt.ylabel("Inflasi YoY (persen)")
plt.show()

# %% [markdown]
# Puncak tahun 1998 terlihat jelas: inflasi tahunan menyentuh sekitar
# 58 persen. Sepuluh tahun terakhir jauh lebih tenang, di bawah 5 persen.

# %%
# Perbandingan string ("1997") dengan kolom tanggal dikerjakan otomatis
# oleh pandas, jadi tidak perlu diubah dulu menjadi Timestamp
for era, mulai, selesai in [
    ("1970-1979", "1970", "1980"),
    ("1980-1996", "1980", "1997"),
    ("1997-1999", "1997", "2000"),
    ("2000-2019", "2000", "2020"),
    ("2020-2025", "2020", "2026"),
]:
    bagian = inflasi[(inflasi["tanggal"] >= mulai) & (inflasi["tanggal"] < selesai)]
    print(f"{era:10s} rata-rata inflasi YoY = {bagian['inflasi_yoy'].mean():5.2f} persen")

# %%
from statsmodels.tsa.stattools import adfuller

print("ADF indeks harga (level)      : p =", round(adfuller(inflasi["indeks"].dropna())[1], 4))
print("ADF inflasi YoY (sudah transformasi): p =",
      round(adfuller(inflasi["inflasi_yoy"].dropna())[1], 4))

# %% [markdown]
# Ini pelajaran stasioneritas dengan data asli: indeks harga tidak
# stasioner karena selalu naik, tetapi inflasi YoY sudah stasioner karena
# kenaikan harga relatif stabil di sekitar levelnya.

# %%
kurs_panjang = pd.read_csv("data/idn-kurs-tahunan.csv")
print(kurs_panjang[kurs_panjang["tahun"].between(1996, 1999)])

kurs_panjang["pertumbuhan"] = 100 * kurs_panjang["kurs"].pct_change()
print("\nPertumbuhan kurs (persen):")
print(kurs_panjang[kurs_panjang["tahun"].between(1997, 1999)].round(2).to_string(index=False))

# %% [markdown]
# Rupiah melemah 24 persen pada 1997 dan 244 persen pada 1998, lalu
# menguat 22 persen pada 1999. Untuk analisis deret waktu, lonjakan ini
# adalah contoh patahan struktural (structural break) yang sebenarnya,
# bukan simulasi.

# %% [markdown]
# ## 6. Latihan mandiri
#
# **Latihan 1: GARCH pada kurs.** Data `data/kurs-harian.csv`.
# - Hitung return harian kurs (persen) dengan `.pct_change()`.
# - Estimasi GARCH(1,1) dan laporkan alpha, beta, serta persistensinya.
# - Bandingkan dengan IHSG. Mana yang lebih persisten?

# %%
# kurs = pd.read_csv("data/kurs-harian.csv", parse_dates=["Tanggal"])
# kurs["ret_kurs"] = 100 * kurs["Kurs_USD_IDR"].pct_change()
# kurs_ret = kurs.dropna()
# ...

# %% [markdown]
# **Latihan 2: GARCH jangka panjang.** Data `data/ihsg-panjang.csv` berisi
# IHSG sejak 1990, mencakup krisis 1998, krisis global 2008, dan COVID.
# - Estimasi GARCH(1,1) pada seluruh periode, lalu bandingkan dengan hasil
#   periode 2019-2026 di bagian 1 (persistensi 0,95).
# - Coba juga potong periode 1990-1999 saja. Apa yang terjadi pada
#   alpha + beta?

# %%
# panjang = pd.read_csv("data/ihsg-panjang.csv", parse_dates=["Date"])
# panjang["ret"] = 100 * np.log(panjang["Close"]).diff()
# panjang = panjang.dropna()
# ...

# %% [markdown]
# **Latihan 3: cross-section provinsi.** Data `data/provinsi-2021.csv`
# berisi 34 provinsi dengan indikator sosial ekonomi 2021.
# - Regresikan `Kemiskinan` pada `IPM`. Berapa koefisiennya dan apa
#   artinya?
# - Bandingkan model `IPM ~ PDRB_Kapita` (linear) dengan
#   `IPM ~ ln(PDRB_Kapita)` (log). Mana yang lebih cocok? Pakai R kuadrat
#   terkoreksi. Perbandingan ini sah karena variabel Y-nya sama (IPM);
#   yang berubah hanya bentuk variabel penjelasnya.

# %%
# prov = pd.read_csv("data/provinsi-2021.csv")
# ...

# %% [markdown]
# **Latihan 4: ganti spesifikasi panel.** Ulangi bagian 2 dengan
# `PDB_Growth ~ FDI + Inflasi` (tanpa angkatan kerja).
# - Apakah uji Hausman masih memilih FEM?
# - Apakah kesimpulan tentang FDI berubah? Bandingkan dengan bagian 2
#   yang memakai `ln_angkatan_kerja`.

# %%
# ...

# %% [markdown]
# **Latihan 5: data Anda sendiri.** Buka `referensi.md` di folder utama,
# bagian "Sumber data Indonesia". Ada tiga jalur untuk mengambil data
# sendiri: World Bank, BPS WebAPI, dan Yahoo Finance. Pilih satu, ambil
# data untuk topik yang Anda minati, dan jalankan regresi sederhana.
#
# Untuk memperbarui semua data di folder `data/` sekaligus, jalankan
# `python scripts/fetch_indonesia_data.py` di komputer sendiri (butuh
# internet).

# %% [markdown]
# ### Selanjutnya
#
# Selanjutnya: proyek mini. Buka proyek_mini.md, lalu susun analisis Anda
# sendiri.
