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
import statsmodels.api as sm
import statsmodels.formula.api as smf

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
model_logit = smf.logit("GRADE ~ GPA + TUCE + PSI", data=spector).fit(disp=0)
print(model_logit.summary())

# %% [markdown]
# ### Membaca hasil
#
# Koefisien bekerja pada skala log-odds, jadi tandanya yang intuitif:
# GPA dan PSI positif (menaikkan peluang lulus), TUCE kecil dan tidak
# signifikan. Pseudo R2 sekitar 0,37 dan uji LLR signifikan: model layak.

# %%
print(f"Pseudo R2 : {model_logit.prsquared:.3f}")
print(f"LLR p     : {model_logit.llr_pvalue:.4f}")

# %% [markdown]
# ### Odds ratio
#
# Odds ratio = `exp(koefisien)`. Nilai 10 berarti odds naik sepuluh kali
# lipat per satu unit X.

# %%
print("Odds ratio:")
print(np.exp(model_logit.params).round(3))

# %% [markdown]
# ### Efek marjinal
#
# Angka yang paling mudah dijelaskan: perubahan peluang (poin persen) per
# satu unit X, pada nilai rata-rata variabel lain.

# %%
print(model_logit.get_margeff().summary())

# %% [markdown]
# ### Cek klasifikasi
#
# Ambang 0,5: prediksi di atas 0,5 dianggap "diperkirakan meningkat".

# %%
prediksi = (model_logit.predict(spector) > 0.5).astype(int)
tabel = pd.crosstab(spector["GRADE"], prediksi, rownames=["aktual"], colnames=["prediksi"])
# Dua sel diagonal (0,0) dan (1,1) adalah prediksi yang benar
akurasi = (tabel.iloc[0, 0] + tabel.iloc[1, 1]) / len(spector)
print(tabel)
print(f"Akurasi: {akurasi:.3f}")

# %% [markdown]
# ### Versi scikit-learn: untuk metrik prediksi
#
# Ingat pembagian tugasnya: statsmodels untuk estimasi dan p-value,
# scikit-learn untuk prediksi dan metrik. Koefisien kedua pustaka sama
# bila sklearn dijalankan tanpa regularisasi (`penalty=None`).

# %%
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score, confusion_matrix

X_sp = spector[["GPA", "TUCE", "PSI"]]
y_sp = spector["GRADE"]

sk_logit = LogisticRegression(penalty=None, max_iter=1000).fit(X_sp, y_sp)
print("Koefisien sklearn :", sk_logit.coef_.round(3))
print("Koefisien statsmodels:", model_logit.params[["GPA", "TUCE", "PSI"]].round(3).to_list())

# %%
# Bagi data latih (75%) dan uji (25%), lalu ukur di data uji
from sklearn.model_selection import train_test_split

X_latih, X_uji, y_latih, y_uji = train_test_split(X_sp, y_sp, test_size=0.25, random_state=42)
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
# `model_logit.predict(pd.DataFrame({"GPA": [3.5], "TUCE": [25],
# "PSI": [1]}))` menghasilkan sekitar 0,84. Jadi peluangnya 84 persen.
#
# </details>

# %% [markdown]
# ## 2. Latihan mandiri
#
# **Latihan 1: kenapa koefisien meledak?** Data `data/logit-probit-2.csv`
# (kelulusan tepat waktu). Jalankan logit biasa, perhatikan peringatan
# "Perfect Separation" dan koefisien yang tidak wajar. Lalu jalankan
# `fit_regularized` dan bandingkan.
#
# Pertanyaan: kenapa logit biasa gagal di data ini?

# %%
# lulus = pd.read_csv("data/logit-probit-2.csv")
# m1 = smf.logit("LULUS_TEPAT ~ IPK_SEM2 + SKS_LULUS_SEM2 + KEAKTIFAN_ORG + BEASISWA", data=lulus).fit(disp=0)
# print(m1.params.round(2))
# m2 = smf.logit("LULUS_TEPAT ~ IPK_SEM2 + SKS_LULUS_SEM2 + KEAKTIFAN_ORG + BEASISWA", data=lulus).fit_regularized(alpha=0.5, L1_wt=0.0, disp=0)
# print(m2.params.round(3))

# %% [markdown]
# **Latihan 2: ordinal.** Data `data/multi-ordinal-1.csv` (kepuasan
# layanan bank, skala 1 sampai 3). Estimasi model ordinal dan tentukan
# arah pengaruh setiap variabel.
#
# Catatan: data simulasi ini nyaris terpisah sempurna, jadi koefisien
# absolutnya ekstrem. Baca TANDA-nya, bukan besarannya.

# %%
# from statsmodels.miscmodels.ordinal_model import OrderedModel
# kepuasan = pd.read_csv("data/multi-ordinal-1.csv")
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
# model_pois = smf.poisson("JML_KLAIM ~ USIA + PENGALAMAN + TIPE_MOBIL", data=klaim).fit(disp=0)
# print(np.exp(model_pois.params).round(3))
# overdisp = (model_pois.resid_pearson ** 2).sum() / model_pois.df_resid
# print("Overdispersi:", round(overdisp, 3))

# %% [markdown]
# ### Selanjutnya
#
# Selanjutnya: Lab 5, deret waktu dan data panel.
