# %% [markdown]
# # Lab 4: Model Kategorikal (Logit, Ordinal, Poisson)
#
# **Durasi:** 90 menit
#
# Tujuan: menaksir model ketika variabel Y bukan angka kontinu, dan
# menafsirkan hasilnya dengan odds ratio atau efek marjinal.

# %% [markdown]
# **Posisi dalam alur workshop.** Y kontinu selesai di Lab 1-3. Sekarang Y
# kategorikal dan hitungan. Lab 5 masuk ke data waktu dan panel.

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

# %%
import pandas as pd
from sklearn.linear_model import LogisticRegression, PoissonRegressor
import numpy as np
import statsmodels.api as sm

# %% [markdown]
# ## 1. Contoh terbimbing: logit biner
#
# Data nilai 32 mahasiswa (dataset Spector dan Mazzeo, sudah terpasang di
# statsmodels). Y = GRADE (1 kalau nilai meningkat), X = GPA, TUCE (tes
# awal), dan PSI (ikut metode pengajaran baru).

# %%
spector = sm.datasets.spector.load_pandas().data
spector.head()

# %%
sampel_model_logit = spector[["GRADE", "GPA", "TUCE", "PSI"]].dropna()
X_model_logit = sampel_model_logit[["GPA", "TUCE", "PSI"]]
y_model_logit = sampel_model_logit["GRADE"]

model_logit = LogisticRegression(penalty=None, max_iter=5000, tol=1e-9)
model_logit.fit(X_model_logit, y_model_logit)

koefisien_model_logit = pd.Series(model_logit.coef_[0], index=X_model_logit.columns)
koefisien_model_logit.loc["Intercept"] = model_logit.intercept_[0]

# Pelengkap statistik: standard error dan pengujian pada sampel yang sama.
uji_model_logit = sm.Logit(
    y_model_logit,
    sm.add_constant(X_model_logit, has_constant="add").rename(
        columns={"const": "Intercept"}
    ),
).fit(disp=0)
print(uji_model_logit.summary())

# %% [markdown]
# ### Membaca hasil
#
# Koefisien bekerja pada skala log-odds, jadi tandanya yang intuitif:
# GPA dan PSI positif (menaikkan peluang lulus), TUCE kecil dan tidak
# signifikan. Pseudo R2 sekitar 0,37 dan uji LLR signifikan: model layak.

# %%
print(f"Pseudo R2 : {uji_model_logit.prsquared:.3f}")
print(f"LLR p     : {uji_model_logit.llr_pvalue:.4f}")

# %% [markdown]
# ### Odds ratio
#
# Odds ratio = `exp(koefisien)`. Nilai 10 berarti odds naik sepuluh kali
# lipat per satu unit X.

# %%
print("Odds ratio:")
print(np.exp(koefisien_model_logit).round(3))

# %% [markdown]
# ### Efek marjinal
#
# Ini rata-rata perubahan peluang di seluruh observasi, dalam poin
# persentase. Untuk dummy, hitung perubahan dari 0 menjadi 1.

# %%
efek = uji_model_logit.get_margeff(at="overall", dummy=True)
print(efek.summary())

# %% [markdown]
# ### Cek klasifikasi
#
# Ambang 0,5: prediksi di atas 0,5 dianggap "diperkirakan meningkat".

# %%
prediksi = (
    pd.Series(
        model_logit.predict_proba(spector[["GPA", "TUCE", "PSI"]])[:, 1],
        index=spector.index,
    )
    > 0.5
).astype(int)
tabel = pd.crosstab(
    spector["GRADE"], prediksi, rownames=["aktual"], colnames=["prediksi"]
)
# Dua sel diagonal (0,0) dan (1,1) adalah prediksi yang benar
akurasi = (prediksi == spector["GRADE"]).mean()
print(tabel)
print(f"Akurasi: {akurasi:.3f}")

# %% [markdown]
# ### Memeriksa koefisien dan mengevaluasi prediksi
#
# Model utama sejak awal memakai scikit-learn. Bandingkan koefisiennya
# dengan pelengkap inferensi pada data yang sama, lalu nilai prediksi
# pada data uji. Tanpa regularisasi, hasil koefisien seharusnya sangat dekat.

# %%
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score, confusion_matrix

X_sp = spector[["GPA", "TUCE", "PSI"]]
y_sp = spector["GRADE"]

sk_logit = model_logit
print("Koefisien sklearn :", sk_logit.coef_.round(3))
print(
    "Koefisien pelengkap inferensi:",
    uji_model_logit.params[["GPA", "TUCE", "PSI"]].round(3).to_list(),
)

# %%
# Bagi data latih (75%) dan uji (25%), lalu ukur di data uji
from sklearn.model_selection import train_test_split

X_latih, X_uji, y_latih, y_uji = train_test_split(
    X_sp, y_sp, test_size=0.25, random_state=42
)
sk_latih = LogisticRegression(penalty=None, max_iter=1000).fit(X_latih, y_latih)

peluang_uji = sk_latih.predict_proba(X_uji)[:, 1]  # kolom 1 = P(GRADE = 1)

print("Akurasi uji:", round(accuracy_score(y_uji, sk_latih.predict(X_uji)), 3))
print("ROC AUC uji:", round(roc_auc_score(y_uji, peluang_uji), 3))
print(confusion_matrix(y_uji, sk_latih.predict(X_uji)))

# %% [markdown]
# Catatan penting: dengan 32 observasi, hasil di data uji bisa berubah
# banyak hanya karena pembagian datanya berbeda. Coba tiga nilai
# `random_state` berbeda dan catat akurasi serta ROC AUC masing-masing.
# Hasilnya biasanya berayun beberapa poin persen. Karena itu, laporkan
# rentangnya, bukan satu angka seolah-olah pasti.

# %% [markdown]
# ### Coba sendiri (5 menit)
#
# Prediksi peluang GRADE = 1 untuk mahasiswa dengan GPA 3,5, TUCE 25,
# dan PSI 1.
#
# Tulis di sel di bawah, baru buka jawabannya.

# %%
# Tulis kode Anda di sini

# %% [markdown]
# <details><summary>Lihat jawaban</summary>
#
# Buat `profil = pd.DataFrame({"GPA": [3.5], "TUCE": [25], "PSI": [1]})`,
# lalu jalankan `model_logit.predict_proba(profil)[:, 1]`. Hasil sekitar
# 0,84 berarti peluang 84 persen; `predict(profil)` menghasilkan kelas 0/1.
#
# </details>

# %% [markdown]
# ## 2. Latihan mandiri
#
# **Latihan 1: kenapa koefisien meledak?** Data `data/logit_probit_2.csv`
# (kelulusan tepat waktu). Jalankan logit biasa, perhatikan peringatan
# "Perfect Separation" dan koefisien yang tidak wajar. Lalu jalankan
# `LogisticRegression` dengan regularisasi dan bandingkan.
#
# Pertanyaan: kenapa logit biasa gagal di data ini?

# %%
# lulus = pd.read_csv("data/logit_probit_2.csv")
# X_lulus = lulus[["IPK_SEM2", "SKS_LULUS_SEM2", "KEAKTIFAN_ORG", "BEASISWA"]]
# y_lulus = lulus["LULUS_TEPAT"]
# m1 = LogisticRegression(penalty=None, max_iter=5000)
# m1.fit(X_lulus, y_lulus)
# m2 = LogisticRegression(max_iter=5000)
# m2.fit(X_lulus, y_lulus)
# print(m1.coef_)
# print(m2.coef_)

# %% [markdown]
# **Latihan 2: ordinal.** Data `data/multi_ordinal_1.csv` (kepuasan
# layanan bank, skala 1 sampai 3). Estimasi model ordinal dan tentukan
# arah pengaruh setiap variabel.
#
# Catatan: data simulasi ini nyaris terpisah sempurna, jadi koefisien
# absolutnya ekstrem. Baca TANDA-nya, bukan besarannya.

# %%
# from statsmodels.miscmodels.ordinal_model import OrderedModel
# kepuasan = pd.read_csv("data/multi_ordinal_1.csv")
# model_ord = OrderedModel(kepuasan["Kepuasan"], kepuasan[["Kecepatan", "Staf_Ramah", "Digital_App"]], distr="logit")
# hasil = model_ord.fit(method="bfgs", disp=False)
# print(hasil.params.round(3))

# %% [markdown]
# **Latihan 3: Poisson.** Data `data/poisson_data_1_klaim.csv` (jumlah
# klaim asuransi per tahun). Hitung IRR (`exp(koefisien)`) dan cek
# overdispersi dengan Pearson chi-kuadrat dibagi derajat bebas.
# Di atas 1,5 berarti sebaiknya pindah ke Negative Binomial.

# %%
# klaim = pd.read_csv("data/poisson_data_1_klaim.csv")
# X_klaim = klaim[["USIA", "PENGALAMAN", "TIPE_MOBIL"]]
# y_klaim = klaim["JML_KLAIM"]
# model_pois = PoissonRegressor(alpha=0, solver="newton-cholesky", max_iter=1000)
# model_pois.fit(X_klaim, y_klaim)
# print(np.exp(model_pois.coef_).round(3))
# prediksi = model_pois.predict(X_klaim)
# residu_pearson = (y_klaim - prediksi) / np.sqrt(prediksi)
# derajat_bebas = len(y_klaim) - X_klaim.shape[1] - 1
# overdisp = (residu_pearson ** 2).sum() / derajat_bebas
# print("Overdispersi:", round(overdisp, 3))

# %% [markdown]
# ### Selanjutnya
#
# Selanjutnya: Lab 5, deret waktu dan data panel.
