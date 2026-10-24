# %% [markdown]
# # Kunci Lab 6: Data Indonesia Asli

# %% [markdown]
# ## Persiapan

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
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm

# %%
%pip install "linearmodels==7.1" "arch==8.0.0" -q

# %% [markdown]
# ## Latihan 1: GARCH pada kurs USD/IDR

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
kurs = pd.read_csv("data/kurs_harian.csv", parse_dates=["Tanggal"])
kurs["ret_kurs"] = 100 * kurs["Kurs_USD_IDR"].pct_change()
kurs_ret = kurs.dropna()

from arch import arch_model

hasil_kurs = arch_model(kurs_ret["ret_kurs"], vol="Garch", p=1, q=1).fit(disp="off")
a = hasil_kurs.params["alpha[1]"]
b = hasil_kurs.params["beta[1]"]
print(f"alpha = {a:.4f}")
print(f"beta  = {b:.4f}")
print(f"persistensi (alpha+beta) = {a + b:.4f}")

# %% [markdown]
# Kesimpulan: kurs jauh lebih persisten (alpha + beta = 0,9864) daripada
# IHSG (0,9508). Artinya guncangan nilai tukar hilang jauh lebih lambat.
# Beta kurs 0,9220, beta IHSG 0,8198. Secara ekonomi masuk akal: intervensi
# dan kebijakan membuat kurs bergerak dalam rezim yang panjang.

# %% [markdown]
# ## Latihan 2: GARCH jangka panjang dengan krisis

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
panjang = pd.read_csv("data/ihsg_panjang.csv", parse_dates=["Date"])
panjang["ret"] = 100 * np.log(panjang["Close"]).diff()
panjang = panjang.dropna()
print(
    "Observasi:",
    len(panjang),
    "rentang:",
    panjang["Date"].min().date(),
    "-",
    panjang["Date"].max().date(),
)

# Pilih periode dengan kondisi tanggal, lalu estimasi setiap bagian.
sebelum_2000 = panjang[panjang["Date"] < "2000-01-01"]
sejak_2000 = panjang[panjang["Date"] >= "2000-01-01"]
sejak_2019 = panjang[panjang["Date"] >= "2019-01-01"]

garch_penuh = arch_model(panjang["ret"], p=1, q=1).fit(disp="off")
garch_1990 = arch_model(sebelum_2000["ret"], p=1, q=1).fit(disp="off")
garch_2000 = arch_model(sejak_2000["ret"], p=1, q=1).fit(disp="off")
garch_2019 = arch_model(sejak_2019["ret"], p=1, q=1).fit(disp="off")

tabel_era = pd.DataFrame(
    {
        "penuh": garch_penuh.params,
        "1990-1999": garch_1990.params,
        "sejak 2000": garch_2000.params,
        "sejak 2019": garch_2019.params,
    }
)
tabel_era.loc["persistensi"] = tabel_era.loc["alpha[1]"] + tabel_era.loc["beta[1]"]
print(tabel_era.round(4))

# %% [markdown]
# Kesimpulan:
#
# - Periode penuh 1990-2026: persistensi 0,9901.
# - Periode 1990-1999 (krisis 1998): alpha + beta tepat 1,0000. Ini kasus
#   IGARCH: guncangan tidak pernah hilang dari sistem. Estimator menyentuh
#   batas, pertanda rezim krisis yang ekstrem.
# - Periode 2000-2026: persistensi turun ke 0,9802, dan periode terpendek
#   2019-2026 turun lagi ke 0,9510.
#
# Bacaan ekonomi: volatilitas IHSG makin cepat mereda dibanding era 1990-an.
# Ini contoh temuan yang hanya muncul dari data asli, tidak dari simulasi.

# %% [markdown]
# ## Latihan 3: cross-section 34 provinsi

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
# Kolom turunan berikut dibuat saat praktik; kolom ini belum ada pada CSV awal.
#
# | Kolom turunan | Pengertian | Satuan/kode |
# |---|---|---|
# | `ln_pdrb` | Logaritma alami PDRB_Kapita. | Skala logaritma |
#
# Sumber definisi: [rujukan data](https://github.com/sainsdataid/dataset/blob/main/Data%2034%20Provinsi%202021.csv).

# %%
prov = pd.read_csv("data/provinsi_2021.csv")
prov["ln_pdrb"] = np.log(prov["PDRB_Kapita"])

sampel_model_kemiskinan = prov[["Kemiskinan", "IPM"]].dropna()
X_model_kemiskinan = sampel_model_kemiskinan[["IPM"]]
y_model_kemiskinan = sampel_model_kemiskinan["Kemiskinan"]

model_kemiskinan = LinearRegression()
model_kemiskinan.fit(X_model_kemiskinan, y_model_kemiskinan)

koefisien_model_kemiskinan = pd.Series(
    model_kemiskinan.coef_, index=X_model_kemiskinan.columns
)
koefisien_model_kemiskinan.loc["Intercept"] = model_kemiskinan.intercept_

# Pelengkap statistik: standard error dan pengujian pada sampel yang sama.
uji_model_kemiskinan = sm.OLS(
    y_model_kemiskinan,
    sm.add_constant(X_model_kemiskinan, has_constant="add").rename(
        columns={"const": "Intercept"}
    ),
).fit()
print("Kemiskinan ~ IPM:")
print(koefisien_model_kemiskinan.round(4))
print(uji_model_kemiskinan.pvalues.round(4))
print("R2:", round(model_kemiskinan.score(X_model_kemiskinan, y_model_kemiskinan), 4))

sampel_model_lin = prov[["IPM", "PDRB_Kapita"]].dropna()
X_model_lin = sampel_model_lin[["PDRB_Kapita"]]
y_model_lin = sampel_model_lin["IPM"]

model_lin = LinearRegression()
model_lin.fit(X_model_lin, y_model_lin)

# Pelengkap statistik: standard error dan pengujian pada sampel yang sama.
uji_model_lin = sm.OLS(
    y_model_lin,
    sm.add_constant(X_model_lin, has_constant="add").rename(
        columns={"const": "Intercept"}
    ),
).fit()
sampel_model_log = prov[["IPM", "ln_pdrb"]].dropna()
X_model_log = sampel_model_log[["ln_pdrb"]]
y_model_log = sampel_model_log["IPM"]

model_log = LinearRegression()
model_log.fit(X_model_log, y_model_log)

# Pelengkap statistik: standard error dan pengujian pada sampel yang sama.
uji_model_log = sm.OLS(
    y_model_log,
    sm.add_constant(X_model_log, has_constant="add").rename(
        columns={"const": "Intercept"}
    ),
).fit()
print(
    "\nIPM ~ PDRB (linear): R2 =",
    round(model_lin.score(X_model_lin, y_model_lin), 4),
    "adj =",
    round(uji_model_lin.rsquared_adj, 4),
)
print(
    "IPM ~ ln(PDRB)     : R2 =",
    round(model_log.score(X_model_log, y_model_log), 4),
    "adj =",
    round(uji_model_log.rsquared_adj, 4),
)

# %% [markdown]
# Kesimpulan:
#
# - Koefisien kemiskinan terhadap IPM = -0,8945 dan sangat signifikan.
#   Kenaikan IPM satu poin berhubungan dengan penurunan kemiskinan sekitar
#   0,89 poin persen. R kuadrat 0,425.
# - Untuk IPM terhadap PDRB, bentuk linear sedikit lebih baik (R kuadrat
#   terkoreksi 0,2516 berbanding 0,2161). Di rentang PDRB provinsi
#   Indonesia, hubungan IPM dan PDRB masih mendekati linear, belum
#   menunjukkan efek jenuh yang kuat.
# - Latihan ini juga boleh dikaitkan dengan pembahasan multikolinearitas
#   di Sesi 3: coba masukkan `ln_pdrb` bersama `PDRB_Kapita` dan lihat
#   VIF-nya.

# %% [markdown]
# ## Latihan 4: panel dengan spesifikasi berbeda

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
# Sumber definisi: [rujukan data](https://databank.worldbank.org/source/world-development-indicators).

# %%
from linearmodels.panel import PanelOLS, RandomEffects

panel = pd.read_csv("data/asean_panel.csv")
panel = panel.set_index(["Negara", "Tahun"])
y = panel["PDB_Growth"]
X = panel[["FDI", "Inflasi"]]

fem = PanelOLS(y, X, entity_effects=True).fit(cov_type="clustered", cluster_entity=True)
rem = RandomEffects(y, sm.add_constant(X)).fit(
    cov_type="clustered", cluster_entity=True
)
print("FEM:", fem.params.round(4).to_dict(), "p:", fem.pvalues.round(4).to_dict())
print("REM:", rem.params.round(4).to_dict(), "p:", rem.pvalues.round(4).to_dict())
print("Chow p:", f"{fem.f_pooled.pval:.4g}")

# Hausman klasik memakai kovarians unadjusted pada sampel yang sama.
# Hasil clustered di atas tetap dipakai untuk pelaporan koefisien dan SE.
fem_uji = PanelOLS(y, X, entity_effects=True).fit()
rem_uji = RandomEffects(y, sm.add_constant(X)).fit()

# sigmamore menyamakan dasar varians galat kedua model memakai estimasi REM.
hausman = rem_uji.hausman(fem_uji, sigmamore=True)
print(hausman)

# %% [markdown]
# Kesimpulan: dengan FDI dan Inflasi, Hausman klasik dengan varians galat
# bersama memberi p sekitar 0,0005, sehingga H0 ditolak pada taraf 5%.
# Hasil mendukung FEM, sama dengan spesifikasi utama. Namun koefisiennya
# tetap perlu dibaca bersama standard error clustered dan konteks ekonomi.
# Untuk Hausman klasik, jangan memakai selisih kovarians clustered.

# %% [markdown]
# ## Latihan 5: jawaban bebas
#
# Tidak ada kunci tunggal. Yang dinilai:
#
# 1. Data berasal dari sumber yang disebutkan dengan jelas.
# 2. Variabel dependen dan penjelas punya satuan yang jelas.
# 3. Regresi dijalankan dan hasilnya dibaca dengan konteks, bukan sekadar
#    melihat tanda bintang.
# 4. Keterbatasan disebutkan (jumlah observasi, kualitas data, klaim
#    kausal tidak berlebihan).
