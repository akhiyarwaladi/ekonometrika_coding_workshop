# %% [markdown]
# # Kunci Lab 4: Model Kategorikal

# %% [markdown]
# ## Persiapan: pastikan data tersedia
#
# Jalankan sel di bawah sekali supaya folder `data/` siap dipakai.

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
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import PoissonRegressor
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf

# %% [markdown]
# ## Latihan 1: perfect separation pada data kelulusan

# %% [markdown]
# <!-- kamus_variabel:logit_probit_2.csv -->
#
# ### Kenali data: Kelulusan tepat waktu
#
# **Data:** `data/logit_probit_2.csv`. **Satu baris:** satu mahasiswa.
#
# | Variabel/kolom | Pengertian | Satuan atau kode | Peran |
# |---|---|---|---|
# | `LULUS_TEPAT` | Apakah mahasiswa menyelesaikan studi tepat waktu. | 1 = tepat waktu; 0 = tidak tepat waktu | Y: target |
# | `IPK_SEM2` | Indeks Prestasi Kumulatif sampai semester 2. | Poin IPK | X: penjelas |
# | `SKS_LULUS_SEM2` | Beban studi yang telah diselesaikan sampai semester 2; SKS = Satuan Kredit Semester. | SKS | X: penjelas |
# | `KEAKTIFAN_ORG` | Keaktifan mahasiswa dalam organisasi. | 1 = aktif; 0 = tidak aktif | X: penjelas |
# | `BEASISWA` | Status penerimaan beasiswa. | 1 = penerima; 0 = bukan penerima | X: penjelas |
#
# Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

# %%
lulus = pd.read_csv("data/logit_probit_2.csv")

formula = "LULUS_TEPAT ~ IPK_SEM2 + SKS_LULUS_SEM2 + KEAKTIFAN_ORG + BEASISWA"

from alat_bantu.metode_lanjutan import coba_logit

print("Koefisien MLE polos (dapat gagal karena separation):")
print(coba_logit(formula, lulus))

sampel_m2 = lulus[
    ["LULUS_TEPAT", "IPK_SEM2", "SKS_LULUS_SEM2", "KEAKTIFAN_ORG", "BEASISWA"]
].dropna()
X_m2 = sampel_m2[["IPK_SEM2", "SKS_LULUS_SEM2", "KEAKTIFAN_ORG", "BEASISWA"]]
y_m2 = sampel_m2["LULUS_TEPAT"]

m2 = LogisticRegression(
    penalty="l1", C=2.0, solver="liblinear", max_iter=5000, tol=1e-9
)
m2.fit(X_m2, y_m2)

koefisien_m2 = pd.Series(m2.coef_[0], index=X_m2.columns)
koefisien_m2.loc["Intercept"] = m2.intercept_[0]
print("\nKoefisien setelah regularisasi:")
print(koefisien_m2.round(3))

# %% [markdown]
# Kesimpulan: kombinasi nilai X memprediksi kelulusan secara sempurna
# (perfect separation), sehingga likelihood maksimum tidak punya solusi
# berhingga dan koefisien meledak. Regularisasi menstabilkannya: IPK
# tetap positif (pengaruh terbesar), SKS dan keaktifan organisasi negatif
# setelah IPK dikontrol. Untuk laporan, sebutkan keterbatasan estimator
# ini karena p-value tidak tersedia.

# %% [markdown]
# ## Latihan 2: model ordinal (multi-ordinal-1)

# %% [markdown]
# <!-- kamus_variabel:multi_ordinal_1.csv -->
#
# ### Kenali data: Kepuasan layanan bank
#
# **Data:** `data/multi_ordinal_1.csv`. **Satu baris:** satu responden pengguna layanan bank.
#
# | Variabel/kolom | Pengertian | Satuan atau kode | Peran |
# |---|---|---|---|
# | `Kepuasan` | Kategori kepuasan terhadap layanan, berurutan dari rendah ke tinggi. | 1 = sangat tidak puas; 2 = netral; 3 = puas | Y: target |
# | `Kecepatan` | Lama menunggu pelayanan. Angka lebih besar berarti menunggu lebih lama. | Menit | X: penjelas |
# | `Staf_Ramah` | Penilaian keramahan staf. | Skor 1 sampai 10 | X: penjelas |
# | `Digital_App` | Frekuensi penggunaan aplikasi digital bank yang dibuat sebagai indikator. | 1 = sering memakai; 0 = jarang/tidak | X: penjelas |
#
# Nama Kecepatan pada CSV berarti waktu tunggu, bukan skor kecepatan. Di contoh utama namanya diperjelas menjadi waktu_tunggu.
#
# Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

# %%
from statsmodels.miscmodels.ordinal_model import OrderedModel

kepuasan = pd.read_csv("data/multi_ordinal_1.csv")
model_ord = OrderedModel(
    kepuasan["Kepuasan"],
    kepuasan[["Kecepatan", "Staf_Ramah", "Digital_App"]],
    distr="logit",
).fit(method="bfgs", disp=False)
print(model_ord.params.round(3))

# %% [markdown]
# Kesimpulan (baca tanda, bukan besaran):
#
# - Kecepatan (waktu tunggu, menit) negatif: makin lama menunggu, makin
#   tidak puas.
# - Staf_Ramah positif: makin ramah, makin puas.
# - Digital_App positif: yang sering memakai aplikasi cenderung lebih puas.
#
# Koefisien absolutnya puluhan karena data simulasi nyaris terpisah
# sempurna. Jangan mengutip besarannya di laporan dengan data seperti ini.

# %% [markdown]
# ## Latihan 3: Poisson (poisson-1)

# %% [markdown]
# <!-- kamus_variabel:poisson_data_1_klaim.csv -->
#
# ### Kenali data: Klaim asuransi mobil
#
# **Data:** `data/poisson_data_1_klaim.csv`. **Satu baris:** satu pengemudi/pemegang polis yang diamati selama satu tahun.
#
# | Variabel/kolom | Pengertian | Satuan atau kode | Peran |
# |---|---|---|---|
# | `JML_KLAIM` | Jumlah pengajuan klaim asuransi dalam setahun. | Klaim; bilangan bulat 0, 1, 2, ... | Y: target |
# | `USIA` | Umur pengemudi. | Tahun | X: penjelas |
# | `PENGALAMAN` | Lama pengalaman mengemudi. | Tahun | X: penjelas |
# | `TIPE_MOBIL` | Jenis mobil menurut pengelompokan pada sumber. | 1 = sport; 0 = keluarga | X: penjelas |
#
# Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

# %%
klaim = pd.read_csv("data/poisson_data_1_klaim.csv")
sampel_model_pois = klaim[["JML_KLAIM", "USIA", "PENGALAMAN", "TIPE_MOBIL"]].dropna()
X_model_pois = sampel_model_pois[["USIA", "PENGALAMAN", "TIPE_MOBIL"]]
y_model_pois = sampel_model_pois["JML_KLAIM"]

model_pois = PoissonRegressor(
    alpha=0, solver="newton-cholesky", max_iter=1000, tol=1e-9
)
model_pois.fit(X_model_pois, y_model_pois)

koefisien_model_pois = pd.Series(model_pois.coef_, index=X_model_pois.columns)
koefisien_model_pois.loc["Intercept"] = model_pois.intercept_

# Pelengkap statistik: standard error dan pengujian pada sampel yang sama.
uji_model_pois = sm.Poisson(
    y_model_pois,
    sm.add_constant(X_model_pois, has_constant="add").rename(
        columns={"const": "Intercept"}
    ),
).fit(disp=0)

print("Koefisien:")
print(koefisien_model_pois.round(3))
print("\nIRR:")
print(np.exp(koefisien_model_pois).round(3))

overdisp = (uji_model_pois.resid_pearson**2).sum() / uji_model_pois.df_resid
print(f"\nOverdispersi (Pearson chi2 / df): {overdisp:.3f}")

model_nb = smf.negativebinomial(
    "JML_KLAIM ~ USIA + PENGALAMAN + TIPE_MOBIL", data=klaim
).fit(disp=0)
print("AIC Poisson:", round(uji_model_pois.aic, 2))
print("AIC NB     :", round(model_nb.aic, 2))

# %% [markdown]
# Kesimpulan: tidak ada variabel yang signifikan di data ini (semua
# p > 0,3). Overdispersi 0,14 (di bawah 1,5), jadi Poisson cukup, dan AIC
# Poisson lebih kecil dari Negative Binomial. Laporkan bahwa data ini
# tidak menunjukkan efek yang bisa dibedakan dari nol pada sampel ini.
