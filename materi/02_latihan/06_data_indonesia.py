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
# | `ihsg_harian.csv` | IHSG harian, 2019 sampai 2026 | Yahoo Finance |
# | `ihsg_panjang.csv` | IHSG harian, 1990 sampai 2026 | Yahoo Finance |
# | `kurs_harian.csv` | Kurs USD/IDR harian, 2019 sampai 2026 | ECB via Frankfurter |
# | `idn_kurs_tahunan.csv` | Kurs tahunan, 1967 sampai 2025 | World Bank |
# | `idn_inflasi_bulanan.csv` | Inflasi bulanan, 1968 sampai 2025 | BPS via OECD/FRED |
# | `idn_makro_tahunan.csv` | Inflasi, PDB, pengangguran, kurs, 2000 sampai 2025 | World Bank |
# | `asean_panel.csv` | 10 negara ASEAN, 2000 sampai 2025 | World Bank |
# | `provinsi_2021.csv` | 34 provinsi: PDRB, IPM, kemiskinan, dll | kompilasi BPS |
#
# Semua file dibaca dari salinan GitHub melalui `URL_DATA`. Cara memperbarui datanya ada
# di akhir lab ini.

# %% [markdown]
# **Posisi dalam alur workshop.** Lab penutup: Lab 0-5 memakai data
# simulasi, lab ini memakai data Indonesia asli dan menggabungkan semua
# teknik. Setelah ini, lanjut ke proyek mini.

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
%pip install "linearmodels==7.1" "arch==8.0.0" -q

# %%
import pandas as pd
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression
import numpy as np
import statsmodels.api as sm
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

# %% [markdown]
# <!-- kamus_variabel:ihsg_harian.csv -->
#
# ### Kenali data: IHSG harian
#
# **Data:** `data/ihsg_harian.csv`. **Satu baris:** satu hari perdagangan di pasar saham.
#
# | Variabel/kolom | Pengertian | Satuan atau kode | Peran |
# |---|---|---|---|
# | `Date` | Tanggal hari perdagangan. | Tanggal YYYY-MM-DD | Penanda waktu |
# | `Close` | Nilai penutupan Indeks Harga Saham Gabungan (IHSG). | Poin indeks | Deret yang dianalisis |
# | `High` | Nilai indeks tertinggi pada hari tersebut. | Poin indeks | Informasi perdagangan |
# | `Low` | Nilai indeks terendah pada hari tersebut. | Poin indeks | Informasi perdagangan |
# | `Open` | Nilai indeks saat pembukaan hari perdagangan. | Poin indeks | Informasi perdagangan |
# | `Volume` | Volume perdagangan yang dilaporkan penyedia data untuk ticker indeks. | Satuan pelaporan Yahoo; bukan rupiah atau poin indeks | Informasi perdagangan |
#
# IHSG adalah indeks, sehingga Close = 6.000 berarti 6.000 poin, bukan Rp6.000. Return dihitung dari perubahan Close. Nilai Volume nol tidak otomatis menunjukkan tidak ada perdagangan; cakupan pelaporan mengikuti penyedia.
#
# Kolom turunan berikut dibuat saat praktik; kolom ini belum ada pada CSV awal.
#
# | Kolom turunan | Pengertian | Satuan/kode |
# |---|---|---|
# | `ret` | Return logaritmik harian: 100 × (ln Close hari ini - ln Close sebelumnya). | Persen log-return |
#
# Sumber definisi: [rujukan data](https://finance.yahoo.com/quote/%5EJKSE/history/).

# %%
ihsg = pd.read_csv(URL_DATA + "ihsg_harian.csv", parse_dates=["Date"])
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
sampel_model_mean = ihsg[["ret"]].dropna()
X_model_mean = pd.DataFrame({"konstanta": 1}, index=sampel_model_mean.index)
y_model_mean = sampel_model_mean["ret"]

model_mean = DummyRegressor(strategy="mean")
model_mean.fit(X_model_mean, y_model_mean)

prediksi_model_mean = pd.Series(
    model_mean.predict(X_model_mean), index=y_model_mean.index
)
residu_model_mean = y_model_mean - prediksi_model_mean
# [1] = p-value dari uji ARCH-LM
p_arch = het_arch(residu_model_mean, nlags=5)[1]
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
print(
    f"Untuk portofolio Rp 10 juta, risiko harian sekitar Rp {abs(var95) / 100 * 10_000_000:,.0f}"
)

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
# `asean_panel.csv` berisi 10 negara ASEAN, 2000 sampai 2025: pertumbuhan
# PDB, FDI (persen dari PDB), angkatan kerja, inflasi, dan pengangguran.
# Kita uji: apakah FDI berhubungan dengan pertumbuhan ekonomi?

# %% [markdown]
# <!-- kamus_variabel:asean_panel.csv -->
#
# ### Kenali data: Panel negara ASEAN dari World Bank
#
# **Data:** `data/asean_panel.csv`. **Satu baris:** satu negara pada satu tahun.
#
# | Variabel/kolom | Pengertian | Satuan atau kode | Peran |
# |---|---|---|---|
# | `Negara` | Kode negara ISO tiga huruf; misalnya IDN = Indonesia, MYS = Malaysia. | Kode negara | Penanda, bukan besaran ekonomi |
# | `Tahun` | Tahun kalender pengamatan. | Tahun | Penanda waktu |
# | `PDB_Growth` | Laju pertumbuhan tahunan PDB riil (Produk Domestik Bruto). | Persen per tahun; NY.GDP.MKTP.KD.ZG | Target pertumbuhan pada model panel |
# | `Inflasi` | Kenaikan tahunan indeks harga konsumen. | Persen per tahun; FP.CPI.TOTL.ZG | Y atau X sesuai model |
# | `Pengangguran` | Pengangguran sebagai bagian dari total angkatan kerja, estimasi model ILO. | Persen angkatan kerja; SL.UEM.TOTL.ZS | X: penjelas |
# | `Kurs_USD` | Kurs resmi rata-rata periode: mata uang lokal untuk memperoleh satu dolar AS. | Mata uang lokal per US$1; PA.NUS.FCRF | X: penjelas |
# | `FDI` | Arus masuk bersih investasi asing langsung relatif terhadap PDB. | Persen PDB; BX.KLT.DINV.WD.GD.ZS | X: penjelas |
# | `Angkatan_Kerja` | Penduduk yang bekerja atau aktif mencari pekerjaan. | Orang; SL.TLF.TOTL.IN | X: penjelas |
#
# Kurs_USD memakai mata uang negara masing-masing, sehingga IDN berarti rupiah/US$ dan MYS berarti ringgit/US$. FDI = 5 berarti 5% PDB; perubahan dari 5 ke 6 adalah 1 poin persen.
#
# Kolom turunan berikut dibuat saat praktik; kolom ini belum ada pada CSV awal.
#
# | Kolom turunan | Pengertian | Satuan/kode |
# |---|---|---|
# | `ln_angkatan_kerja` | Logaritma alami jumlah angkatan kerja. | Skala logaritma |
#
# Sumber definisi: [rujukan data](https://databank.worldbank.org/source/world-development-indicators).

# %%
panel = pd.read_csv(URL_DATA + "asean_panel.csv")
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
rem = RandomEffects(y, sm.add_constant(X)).fit(
    cov_type="clustered", cluster_entity=True
)

print("=== CEM ===")
print(cem.params.round(4))
print("\n=== FEM ===")
print(fem.params.round(4))
print("\n=== REM ===")
print(rem.params.round(4))

# %% [markdown]
# ### Uji Chow dan Hausman

# %%
print("Uji Chow (CEM vs FEM):")
print(fem.f_pooled)

# Hausman klasik memakai kovarians unadjusted pada sampel yang sama.
# Hasil clustered di atas tetap dipakai untuk pelaporan koefisien dan SE.
fem_uji = PanelOLS(y, X, entity_effects=True).fit()
rem_uji = RandomEffects(y, sm.add_constant(X)).fit()

# sigmamore menyamakan dasar varians galat kedua model memakai estimasi REM.
hausman = rem_uji.hausman(fem_uji, sigmamore=True)
print(hausman)

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
# Lihat p-value Hausman pada bagian 2. Model mana yang dipakai,
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

# %% [markdown]
# <!-- kamus_variabel:idn_makro_tahunan.csv -->
#
# ### Kenali data: Makroekonomi Indonesia tahunan
#
# **Data:** `data/idn_makro_tahunan.csv`. **Satu baris:** satu tahun kalender untuk Indonesia.
#
# | Variabel/kolom | Pengertian | Satuan atau kode | Peran |
# |---|---|---|---|
# | `negara` | Kode negara; IDN menunjukkan Indonesia. | Kode ISO negara | Penanda, bukan besaran ekonomi |
# | `tahun` | Tahun kalender pengamatan. | Tahun | Penanda waktu |
# | `PDB_Growth` | Laju pertumbuhan tahunan PDB riil (Produk Domestik Bruto). | Persen per tahun; NY.GDP.MKTP.KD.ZG | Target pertumbuhan pada model panel |
# | `Inflasi` | Kenaikan tahunan indeks harga konsumen. | Persen per tahun; FP.CPI.TOTL.ZG | Y atau X sesuai model |
# | `Pengangguran` | Pengangguran sebagai bagian dari total angkatan kerja, estimasi model ILO. | Persen angkatan kerja; SL.UEM.TOTL.ZS | X: penjelas |
# | `Kurs_USD` | Kurs resmi rata-rata periode: mata uang lokal untuk memperoleh satu dolar AS. | Mata uang lokal per US$1; PA.NUS.FCRF | X: penjelas |
# | `Angkatan_Kerja` | Penduduk yang bekerja atau aktif mencari pekerjaan. | Orang; SL.TLF.TOTL.IN | X: penjelas |
#
# Kurs_USD untuk Indonesia bersatuan rupiah per US$1. Inflasi dan pertumbuhan adalah laju persen, bukan nilai level harga atau level PDB.
#
# Sumber definisi: [rujukan data](https://databank.worldbank.org/source/world-development-indicators).

# %%
makro = pd.read_csv(URL_DATA + "idn_makro_tahunan.csv")
makro.tail()

# %%
plt.figure(figsize=(7, 4.5))
plt.scatter(makro["Pengangguran"], makro["Inflasi"])
plt.xlabel("Pengangguran (persen)")
plt.ylabel("Inflasi (persen)")
plt.title("Inflasi dan pengangguran Indonesia, 2000-2025")
plt.show()

# %%
sampel_model_makro = makro[["Inflasi", "Pengangguran"]].dropna()
X_model_makro = sampel_model_makro[["Pengangguran"]]
y_model_makro = sampel_model_makro["Inflasi"]

model_makro = LinearRegression()
model_makro.fit(X_model_makro, y_model_makro)

# Pelengkap statistik: standard error dan pengujian pada sampel yang sama.
uji_model_makro = sm.OLS(
    y_model_makro,
    sm.add_constant(X_model_makro, has_constant="add").rename(
        columns={"const": "Intercept"}
    ),
).fit()
print(uji_model_makro.summary())

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

# %% [markdown]
# <!-- kamus_variabel:kurs_harian.csv -->
#
# ### Kenali data: Kurs rupiah harian
#
# **Data:** `data/kurs_harian.csv`. **Satu baris:** satu tanggal tersedianya kurs acuan.
#
# | Variabel/kolom | Pengertian | Satuan atau kode | Peran |
# |---|---|---|---|
# | `Tanggal` | Tanggal kurs acuan tersedia; bukan selalu setiap hari kalender. | Tanggal YYYY-MM-DD | Penanda waktu |
# | `Kurs_USD_IDR` | Jumlah rupiah untuk memperoleh satu dolar AS (USD = dolar AS; IDR = rupiah). | Rupiah per US$1 | Deret yang dianalisis |
#
# Seri diambil melalui Frankfurter dari kurs acuan ECB. Perubahan kurs adalah kolom turunan, bukan arti nilai kurs level.
#
# Kolom turunan berikut dibuat saat praktik; kolom ini belum ada pada CSV awal.
#
# | Kolom turunan | Pengertian | Satuan/kode |
# |---|---|---|
# | `ret_kurs` | Perubahan relatif kurs harian: 100 × (kurs hari ini / kurs sebelumnya - 1). | Persen; positif berarti rupiah melemah |
#
# Sumber definisi: [rujukan data](https://www.frankfurter.dev/).

# %%
from statsmodels.tsa.stattools import adfuller

kurs = pd.read_csv(URL_DATA + "kurs_harian.csv", parse_dates=["Tanggal"])
print("Jumlah observasi:", len(kurs))
print("ADF di level      : p =", round(adfuller(kurs["Kurs_USD_IDR"])[1], 4))
print(
    "ADF setelah selisih: p =",
    round(adfuller(kurs["Kurs_USD_IDR"].diff().dropna())[1], 4),
)

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

# %% [markdown]
# <!-- kamus_variabel:idn_inflasi_bulanan.csv -->
#
# ### Kenali data: IHK dan inflasi Indonesia bulanan
#
# **Data:** `data/idn_inflasi_bulanan.csv`. **Satu baris:** satu bulan kalender.
#
# | Variabel/kolom | Pengertian | Satuan atau kode | Peran |
# |---|---|---|---|
# | `tanggal` | Bulan pengamatan; tanggal berfungsi sebagai penanda bulan. | Tanggal YYYY-MM-DD | Penanda waktu |
# | `indeks` | Indeks Harga Konsumen (IHK), yaitu ukuran tingkat harga keranjang konsumsi. | Poin indeks; tahun dasar mengikuti seri sumber | Level harga |
# | `inflasi_mom` | Persentase perubahan indeks dari bulan sebelumnya (month-on-month). | 100 × (indeks bulan ini / bulan lalu - 1) | Deret yang dianalisis |
# | `inflasi_yoy` | Persentase perubahan indeks dari bulan yang sama setahun sebelumnya (year-on-year). | 100 × (indeks bulan ini / indeks 12 bulan lalu - 1) | Deret yang dianalisis |
#
# indeks adalah level, sedangkan inflasi_mom dan inflasi_yoy adalah perubahan persen yang dihitung oleh skrip unduhan. Angka 2 pada kolom inflasi berarti 2%, bukan 0,02%.
#
# Kolom turunan berikut dibuat saat praktik; kolom ini belum ada pada CSV awal.
#
# | Kolom turunan | Pengertian | Satuan/kode |
# |---|---|---|
# | `era` | Label pengelompokan periode untuk ringkasan/grafik inflasi. | Kategori periode, bukan variabel inflasi baru |
#
# Sumber definisi: [rujukan data](https://fred.stlouisfed.org/series/IDNCPIALLMINMEI).

# %%
inflasi = pd.read_csv(URL_DATA + "idn_inflasi_bulanan.csv", parse_dates=["tanggal"])

plt.figure(figsize=(10, 4))
plt.plot(inflasi["tanggal"], inflasi["inflasi_yoy"], lw=0.8)
plt.axvspan(
    pd.Timestamp("1997-07-01"), pd.Timestamp("1999-12-31"), color="red", alpha=0.15
)
plt.title("Inflasi tahunan (year-on-year) Indonesia, 1968-2025")
plt.xlabel("Tahun")
plt.ylabel("Inflasi YoY (persen)")
plt.show()

# %% [markdown]
# Puncak tahun 1998 terlihat jelas: inflasi tahunan menyentuh sekitar
# 58 persen. Sepuluh tahun terakhir jauh lebih tenang, di bawah 5 persen.

# %%
# Bentuk kolom era satu langkah per batas tahun. loc berarti memilih baris.
inflasi["era"] = "1970-1979"
inflasi.loc[inflasi["tanggal"] >= "1980-01-01", "era"] = "1980-1996"
inflasi.loc[inflasi["tanggal"] >= "1997-01-01", "era"] = "1997-1999"
inflasi.loc[inflasi["tanggal"] >= "2000-01-01", "era"] = "2000-2019"
inflasi.loc[inflasi["tanggal"] >= "2020-01-01", "era"] = "2020-2025"
periode_analisis = inflasi[inflasi["tanggal"].between("1970-01-01", "2025-12-31")]
# groupby() mengelompokkan baris berdasarkan era, mean() menghitung rata-rata.
rata_per_era = periode_analisis.groupby("era")["inflasi_yoy"].mean()
print(rata_per_era.round(2))

# %%
from statsmodels.tsa.stattools import adfuller

print(
    "ADF indeks harga (level)      : p =",
    round(adfuller(inflasi["indeks"].dropna())[1], 4),
)
print(
    "ADF inflasi YoY (sudah transformasi): p =",
    round(adfuller(inflasi["inflasi_yoy"].dropna())[1], 4),
)

# %% [markdown]
# Ini pelajaran stasioneritas dengan data asli: indeks harga tidak
# stasioner karena selalu naik, tetapi inflasi YoY sudah stasioner karena
# kenaikan harga relatif stabil di sekitar levelnya.

# %% [markdown]
# <!-- kamus_variabel:idn_kurs_tahunan.csv -->
#
# ### Kenali data: Kurs rupiah tahunan
#
# **Data:** `data/idn_kurs_tahunan.csv`. **Satu baris:** satu tahun kalender.
#
# | Variabel/kolom | Pengertian | Satuan atau kode | Peran |
# |---|---|---|---|
# | `tahun` | Tahun pengamatan. | Tahun | Penanda waktu |
# | `kurs` | Kurs resmi rata-rata satu tahun, rupiah yang diperlukan untuk US$1. | Rupiah per dolar AS | Deret yang dianalisis |
#
# Kurs yang meningkat berarti satu dolar membutuhkan lebih banyak rupiah, sehingga rupiah melemah terhadap dolar.
#
# Kolom turunan berikut dibuat saat praktik; kolom ini belum ada pada CSV awal.
#
# | Kolom turunan | Pengertian | Satuan/kode |
# |---|---|---|
# | `pertumbuhan` | Perubahan relatif kurs dari tahun sebelumnya, dikalikan 100. | Persen per tahun |
#
# Sumber definisi: [rujukan data](https://data.worldbank.org/indicator/PA.NUS.FCRF).

# %%
kurs_panjang = pd.read_csv(URL_DATA + "idn_kurs_tahunan.csv")
print(kurs_panjang[kurs_panjang["tahun"].between(1996, 1999)])

kurs_panjang["pertumbuhan"] = 100 * kurs_panjang["kurs"].pct_change()
print("\nPertumbuhan kurs (persen):")
print(
    kurs_panjang[kurs_panjang["tahun"].between(1997, 1999)]
    .round(2)
    .to_string(index=False)
)

# %% [markdown]
# Rupiah melemah 24 persen pada 1997 dan 244 persen pada 1998, lalu
# menguat 22 persen pada 1999. Untuk analisis deret waktu, lonjakan ini
# adalah contoh patahan struktural (structural break) yang sebenarnya,
# bukan simulasi.

# %% [markdown]
# ## 6. Latihan mandiri
#
# **Latihan 1: GARCH pada kurs.** Data `data/kurs_harian.csv`.
# - Hitung return harian kurs (persen) dengan `.pct_change()`.
# - Estimasi GARCH(1,1) dan laporkan alpha, beta, serta persistensinya.
# - Bandingkan dengan IHSG. Mana yang lebih persisten?

# %%
# kurs = pd.read_csv(URL_DATA + "kurs_harian.csv", parse_dates=["Tanggal"])
# kurs["ret_kurs"] = 100 * kurs["Kurs_USD_IDR"].pct_change()
# kurs_ret = kurs.dropna()
# ...

# %% [markdown]
# **Latihan 2: GARCH jangka panjang.** Data `data/ihsg_panjang.csv` berisi
# IHSG sejak 1990, mencakup krisis 1998, krisis global 2008, dan COVID.
# - Estimasi GARCH(1,1) pada seluruh periode, lalu bandingkan dengan hasil
#   periode 2019-2026 di bagian 1 (persistensi 0,95).
# - Coba juga potong periode 1990-1999 saja. Apa yang terjadi pada
#   alpha + beta?

# %% [markdown]
# <!-- kamus_variabel:ihsg_panjang.csv -->
#
# ### Kenali data: IHSG riwayat panjang
#
# **Data:** `data/ihsg_panjang.csv`. **Satu baris:** satu hari perdagangan di pasar saham.
#
# | Variabel/kolom | Pengertian | Satuan atau kode | Peran |
# |---|---|---|---|
# | `Date` | Tanggal hari perdagangan. | Tanggal YYYY-MM-DD | Penanda waktu |
# | `Close` | Nilai penutupan Indeks Harga Saham Gabungan (IHSG). | Poin indeks | Deret yang dianalisis |
# | `High` | Nilai indeks tertinggi pada hari tersebut. | Poin indeks | Informasi perdagangan |
# | `Low` | Nilai indeks terendah pada hari tersebut. | Poin indeks | Informasi perdagangan |
# | `Open` | Nilai indeks saat pembukaan hari perdagangan. | Poin indeks | Informasi perdagangan |
# | `Volume` | Volume perdagangan yang dilaporkan penyedia data untuk ticker indeks. | Satuan pelaporan Yahoo; bukan rupiah atau poin indeks | Informasi perdagangan |
#
# IHSG adalah indeks, sehingga Close = 6.000 berarti 6.000 poin, bukan Rp6.000. Return dihitung dari perubahan Close. Nilai Volume nol tidak otomatis menunjukkan tidak ada perdagangan; cakupan pelaporan mengikuti penyedia.
#
# Kolom turunan berikut dibuat saat praktik; kolom ini belum ada pada CSV awal.
#
# | Kolom turunan | Pengertian | Satuan/kode |
# |---|---|---|
# | `ret` | Return logaritmik harian: 100 × selisih log Close. | Persen log-return |
#
# Sumber definisi: [rujukan data](https://finance.yahoo.com/quote/%5EJKSE/history/).

# %%
# panjang = pd.read_csv(URL_DATA + "ihsg_panjang.csv", parse_dates=["Date"])
# panjang["ret"] = 100 * np.log(panjang["Close"]).diff()
# panjang = panjang.dropna()
# ...

# %% [markdown]
# **Latihan 3: cross-section provinsi.** Data `data/provinsi_2021.csv`
# berisi 34 provinsi dengan indikator sosial ekonomi 2021.
# - Regresikan `Kemiskinan` pada `IPM`. Berapa koefisiennya dan apa
#   artinya?
# - Bandingkan model `IPM ~ PDRB_Kapita` (linear) dengan
#   `IPM ~ ln(PDRB_Kapita)` (log). Mana yang lebih cocok? Pakai R kuadrat
#   terkoreksi. Perbandingan ini sah karena variabel Y-nya sama (IPM);
#   yang berubah hanya bentuk variabel penjelasnya.

# %% [markdown]
# <!-- kamus_variabel:provinsi_2021.csv -->
#
# ### Kenali data: Indikator 34 provinsi tahun 2021
#
# **Data:** `data/provinsi_2021.csv`. **Satu baris:** satu provinsi pada tahun 2021 dalam kompilasi sumber.
#
# | Variabel/kolom | Pengertian | Satuan atau kode | Peran |
# |---|---|---|---|
# | `Provinsi` | Nama provinsi yang diamati. | Nama wilayah | Penanda, bukan besaran ekonomi |
# | `PDRB_Kapita` | Produk Domestik Regional Bruto per penduduk, ukuran output ekonomi per kapita. | Skala sumber; dipakai sebagai ribu rupiah dalam tutorial | Y atau X sesuai model |
# | `IPM` | Indeks Pembangunan Manusia yang merangkum dimensi kesehatan, pendidikan, dan taraf hidup. | Poin indeks, bukan persen | Y atau X sesuai model |
# | `Pengangguran` | Tingkat Pengangguran Terbuka (TPT). | Persen angkatan kerja | X: penjelas |
# | `Kemiskinan` | Penduduk yang berada di bawah garis kemiskinan. | Persen penduduk | Y: target |
# | `AHH_Laki` | Angka Harapan Hidup laki-laki pada kompilasi sumber. | Tahun | Indikator pendamping |
# | `AHH_Perempuan` | Angka Harapan Hidup perempuan pada kompilasi sumber. | Tahun | Indikator pendamping |
# | `APS_7_12` | Angka Partisipasi Sekolah penduduk umur 7 sampai 12 tahun. | Persen penduduk kelompok umur tersebut | Indikator pendamping |
# | `APS_13_15` | Angka Partisipasi Sekolah penduduk umur 13 sampai 15 tahun. | Persen penduduk kelompok umur tersebut | Indikator pendamping |
# | `APS_16_18` | Angka Partisipasi Sekolah penduduk umur 16 sampai 18 tahun. | Persen penduduk kelompok umur tersebut | Indikator pendamping |
# | `APS_19_23` | Angka Partisipasi Sekolah penduduk umur 19 sampai 23 tahun. | Persen penduduk kelompok umur tersebut | Indikator pendamping |
# | `Perokok` | Persentase perokok pada kompilasi data provinsi. | Persen; cakupan umur mengikuti sumber | Indikator pendamping |
#
# Berkas ini adalah kompilasi indikator, bukan tabel metadata lengkap BPS. Cakupan indikator dan skala PDRB perlu diperiksa pada sumber BPS sebelum dipakai untuk riset; barisnya mengikuti 34 provinsi pada tahun 2021.
#
# Sumber definisi: [rujukan data](https://github.com/sainsdataid/dataset/blob/main/Data%2034%20Provinsi%202021.csv).

# %%
# prov = pd.read_csv(URL_DATA + "provinsi_2021.csv")
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
# **Latihan 5: data Anda sendiri.** Buka `panduan/04_referensi.md` di folder utama,
# bagian "Sumber data Indonesia". Ada tiga jalur untuk mengambil data
# sendiri: World Bank, BPS WebAPI, dan Yahoo Finance. Pilih satu, ambil
# data untuk topik yang Anda minati, dan jalankan regresi sederhana.
#
# Untuk memperbarui semua data di folder `data/` sekaligus, jalankan
# `python alat_bantu/unduh_data_indonesia.py` di komputer sendiri (butuh
# internet).

# %% [markdown]
# ### Selanjutnya
#
# Selanjutnya: proyek mini. Buka 07_proyek_mini.md, lalu susun analisis Anda
# sendiri.
