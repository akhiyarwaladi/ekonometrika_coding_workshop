# %% [markdown]
# # Hari 1, Sesi 4: Model untuk Data Kategorikal dan Terbatas
#
# **Durasi:** 75 menit
#
# Peta modelnya dulu, biar tidak tersesat:
#
# | Bentuk Y | Model |
# |---|---|
# | 0/1 (disetujui atau tidak) | Logit / Probit biner |
# | 3+ kategori tanpa urutan (motor, mobil, bus) | Multinomial logit |
# | 3+ kategori berurutan (buruk, cukup, baik) | Ordinal logit/probit |
# | Kontinu tapi menumpuk di 0 (pengeluaran R&D) | Tobit |
# | Hitungan (jumlah klaim, jumlah pelanggan) | Poisson, Negative Binomial |
#
# Satu pesan yang harus terbawa: koefisien logit dan probit TIDAK bisa dibaca
# sebagai "tambah 1 unit X, tambah Y sekian unit". Yang dibaca adalah odds
# ratio atau efek marjinal.
#
# ### Pembagian tugas statsmodels dan scikit-learn
#
# Dua pustaka ini sering membingungkan pemula, jadi aturannya jelas sejak
# awal:
#
# | Kebutuhan | Pustaka |
# |---|---|
# | Koefisien, standard error, p-value, uji asumsi | statsmodels |
# | Uji heteroskedastisitas, normalitas, ADF, kointegrasi, panel | statsmodels |
# | Prediksi, splitting data, metrik klasifikasi (akurasi, ROC AUC) | scikit-learn |
#
# scikit-learn TIDAK mengeluarkan p-value atau standard error, jadi bukan
# pengganti statsmodels di ekonometrika. Pakai keduanya sesuai porsi:
# taksir dan uji dengan statsmodels, ukur kemampuan prediksi dengan
# scikit-learn. Contoh berdampingannya ada di bagian 6.

# %% [markdown]
# **Posisi dalam alur workshop.** Sesi 1-3 menangani Y kontinu. Sesi ini
# menangani Y berupa kategori, hitungan, dan data tersensor. Sesi 5 masuk
# ke data deret waktu.

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

# %% [markdown]
# ## 1. Logit biner: contoh klasik Spector dan Mazzeo
#
# Untuk demo logit, kita pakai dataset yang sudah terpasang di statsmodels:
# nilai 32 mahasiswa pada mata kuliah ekonomi. Variabelnya GRADE (1 kalau
# nilai meningkat setelah mengikuti program pengajaran baru), GPA, nilai
# tes awal (TUCE), dan PSI (1 kalau mengikuti metode pengajaran baru).
# Dataset ini dipakai di banyak buku ekonometrika, jadi hasilnya bisa
# dibandingkan dengan referensi lain.
#
# Model logit menaksir peluang lewat fungsi logistik:
#
# $$P(Y=1|X) = \frac{e^{\beta_0 + \beta_1 X_1 + \dots}}{1 + e^{\beta_0 + \beta_1 X_1 + \dots}}$$

# %%
import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", palette=["#2F5D50", "#C15937", "#D9A441", "#5B8A8F"])
plt.rcParams.update({"figure.dpi": 110, "axes.titleweight": "bold", "font.size": 11})

spector = sm.datasets.spector.load_pandas().data
spector.head()

# %%
model_logit = smf.logit("GRADE ~ GPA + TUCE + PSI", data=spector).fit(disp=0)
print(model_logit.summary())

# %% [markdown]
# Yang dibaca dari summary logit:
#
# - `coef` bekerja pada skala log-odds. Tanda positif berarti peluang
#   GRADE = 1 naik.
# - `Pseudo R-squ` (McFadden) bukan R kuadrat OLS. Nilai 0,2 sampai 0,4
#   sudah dianggap layak; di bawah 0,1 model hampir tidak menambah
#   informasi dibanding model tanpa variabel.
# - `LLR p-value` adalah uji likelihood ratio untuk model secara
#   keseluruhan. Di bawah 0,05 berarti model layak.

# %%
print(f"Pseudo R2 (McFadden): {model_logit.prsquared:.4f}")
print(f"LLR p-value         : {model_logit.llr_pvalue:.6g}")

# %% [markdown]
# ## 2. Odds ratio
#
# $OR = e^{\beta}$. OR = 1,5 berarti kenaikan 1 unit X menaikkan odds
# (bukan peluang) sebesar 50%. Angka di bawah 1 berarti menurunkan odds.
# OR untuk PSI sekitar 10,8: mahasiswa yang ikut metode baru punya odds
# nilai meningkat sepuluh kali lipat dibanding yang tidak, setelah GPA dan
# tes awal dikontrol.

# %%
odds_ratio = np.exp(model_logit.params)
pd.DataFrame({"koefisien_log_odds": model_logit.params,
              "odds_ratio": odds_ratio,
              "p_value": model_logit.pvalues}).round(4)


# %% [markdown]
# ### Coba sendiri (5 menit)
#
# Tanpa melihat tabel odds ratio, hitung sendiri `exp(koefisien PSI)`.
# Apakah cocok dengan angka di tabel sebelumnya?
#
# Tulis di sel di bawah, baru buka jawabannya.

# %%
# Tulis kode Anda di sini

# %% [markdown]
# <details><summary>Lihat jawaban</summary>
#
# Koefisien PSI = 2,3787, jadi exp(2,3787) = 10,79. Cocok dengan odds
# ratio di tabel: odds lulus naik sekitar 10,8 kali lipat.
#
# </details>

# %% [markdown]
# ## 3. Efek marjinal: angka yang paling mudah dijelaskan
#
# Efek marjinal menjawab: "kalau X naik 1 unit, peluang Y=1 berubah berapa
# poin persen, dengan variabel lain di nilai rata-ratanya?" Ini yang dipakai
# di laporan, bukan koefisien mentah. Untuk PSI, efek marjinalnya sekitar
# 0,30: peluang nilai meningkat naik sekitar 30 poin persen.

# %%
efek = model_logit.get_margeff()
print(efek.summary())

# %% [markdown]
# ## 4. Probit dan perbandingannya
#
# Probit memakai distribusi normal, bukan logistik. Kesimpulannya biasanya
# sama, hanya skala koefisiennya berbeda: koefisien logit sekitar 1,6
# sampai 1,8 kali koefisien probit. Cara aman membandingkan tetap lewat
# efek marjinal.

# %%
model_probit = smf.probit("GRADE ~ GPA + TUCE + PSI", data=spector).fit(disp=0)
print(model_probit.summary())

# %%
banding_me = pd.DataFrame({
    "ME_logit": np.asarray(model_logit.get_margeff().margeff),
    "ME_probit": np.asarray(model_probit.get_margeff().margeff),
}, index=["GPA", "TUCE", "PSI"])
banding_me.round(4)

# %% [markdown]
# ## 5. Menilai ketepatan klasifikasi
#
# Model probabilitas perlu diubah jadi keputusan ya/tidak pada ambang
# tertentu (lazimnya 0,5), lalu dibandingkan dengan kenyataan.

# %%
prediksi = (model_logit.predict(spector) > 0.5).astype(int)
tabel_klasifikasi = pd.crosstab(spector["GRADE"], prediksi,
                                rownames=["aktual"], colnames=["prediksi"])
akurasi = (tabel_klasifikasi.iloc[0, 0] + tabel_klasifikasi.iloc[1, 1]) / len(spector)
print(tabel_klasifikasi)
print(f"Akurasi = {akurasi:.3f}")

# %% [markdown]
# ### Kalau layar Anda menampilkan peringatan "Perfect Separation"
#
# Data kredit mikro di `logit-probit-1.csv` dan data mahasiswa di
# `logit-probit-2.csv` hasil simulasi ternyata TERPISAH SEMPURNA: kombinasi
# nilai X memprediksi Y dengan benar 100 persen. Akibatnya likelihood
# maksimum tidak punya solusi berhingga, dan koefisien "meledak" ke angka
# puluhan atau ribuan. EViews sering tetap menampilkan hasilnya tanpa
# peringatan; Python justru jujur memberi warning.
#
# Ini bukan bug, tapi sifat data. Dua penanganannya:
#
# 1. Regularisasi (penalized MLE), paling praktis di Python.
# 2. Firth logistic regression, standar di bidang statistik medis.
#
# Contoh dengan `logit-probit-2.csv`:

# %%
lulus = pd.read_csv("data/logit-probit-2.csv").rename(columns={
    "LULUS_TEPAT": "lulus_tepat", "IPK_SEM2": "ipk_sem2",
    "SKS_LULUS_SEM2": "sks_lulus_sem2", "KEAKTIFAN_ORG": "keaktifan_org",
    "BEASISWA": "beasiswa"})

model_logit_polos = smf.logit(
    "lulus_tepat ~ ipk_sem2 + sks_lulus_sem2 + keaktifan_org + beasiswa",
    data=lulus).fit(disp=0)
print("Koefisien MLE polos (tidak stabil):")
print(model_logit_polos.params.round(2))

model_reg = smf.logit(
    "lulus_tepat ~ ipk_sem2 + sks_lulus_sem2 + keaktifan_org + beasiswa",
    data=lulus).fit_regularized(alpha=0.5, L1_wt=0.0, disp=0)
print("\nKoefisien setelah regularisasi (lebih stabil):")
print(model_reg.params.round(3))

# %% [markdown]
# Setelah regularisasi, tanda koefisien biasanya masuk akal (IPK positif,
# beasiswa positif), tapi p-value tidak tersedia karena estimatornya sudah
# bukan MLE biasa. Untuk laporan ilmiah dengan kasus begini, sebutkan
# keterbatasannya secara terbuka.

# %% [markdown]
# ## 6. Versi scikit-learn: prediksi dan metrik klasifikasi
#
# Pertama, buktikan kedua pustaka menghasilkan koefisien yang sama bila
# scikit-learn dijalankan tanpa regularisasi (`penalty=None`).

# %%
from sklearn.linear_model import LogisticRegression

X_sp = spector[["GPA", "TUCE", "PSI"]]
y_sp = spector["GRADE"]

sk_logit = LogisticRegression(penalty=None, max_iter=1000)
sk_logit.fit(X_sp, y_sp)
print("Koefisien scikit-learn:", sk_logit.coef_.round(3),
      "| intersep:", round(sk_logit.intercept_[0], 3))
print("Koefisien statsmodels :",
      model_logit.params[["GPA", "TUCE", "PSI"]].round(3).to_list(),
      "| intersep:", round(model_logit.params["Intercept"], 3))

# %% [markdown]
# Angkanya sama persis. Sekarang bagian yang dikerjakan scikit-learn dengan
# rapi: membagi data latih dan uji, lalu menghitung metrik di data uji.

# %%
from sklearn.metrics import (accuracy_score, confusion_matrix,
                             precision_score, recall_score, roc_auc_score)
from sklearn.model_selection import train_test_split

X_latih, X_uji, y_latih, y_uji = train_test_split(
    X_sp, y_sp, test_size=0.25, random_state=42)

sk_latih = LogisticRegression(penalty=None, max_iter=1000).fit(X_latih, y_latih)
pred_uji = sk_latih.predict(X_uji)
peluang_uji = sk_latih.predict_proba(X_uji)[:, 1]

print("Akurasi :", round(accuracy_score(y_uji, pred_uji), 3))
print("Presisi :", round(precision_score(y_uji, pred_uji), 3))
print("Recall  :", round(recall_score(y_uji, pred_uji), 3))
print("ROC AUC :", round(roc_auc_score(y_uji, peluang_uji), 3))
print("Matriks konfusi:")
print(confusion_matrix(y_uji, pred_uji))

# %% [markdown]
# `predict_proba` mengeluarkan peluang per kelas. ROC AUC mengukur
# kemampuan mengurutkan dan tidak bergantung pada ambang 0,5, jadi lebih
# informatif daripada akurasi pada sampel kecil seperti ini.
#
# ### Bonus: regularisasi bawaan untuk data terpisah
#
# scikit-learn secara bawaan memakai regularisasi L2 (parameter `C`).
# Itulah sebabnya pada data kelulusan yang terpisah sempurna, koefisien
# sklearn tetap berhingga tanpa pengaturan tambahan. Koefisien hasil
# regularisasi bergantung pada skala variabel, jadi jangan dibaca
# besarannya; gunakan untuk prediksi saja.

# %%
# `lulus` berasal dari bagian Perfect Separation di atas
lulus_X = lulus[["ipk_sem2", "sks_lulus_sem2", "keaktifan_org", "beasiswa"]]
sk_lulus = LogisticRegression(max_iter=2000).fit(lulus_X, lulus["lulus_tepat"])
print("Koefisien sklearn (regularisasi bawaan):", sk_lulus.coef_.round(3))
print("Akurasi di data yang sama:",
      round(sk_lulus.score(lulus_X, lulus["lulus_tepat"]), 3))

# %% [markdown]
# ## 7. Multinomial logit: pilihan moda transportasi
#
# `multi-ordinal-2.csv`: pilihan transport (Motor, Mobil, Umum) dijelaskan
# waktu tempuh, biaya, dan jarak. Kategorinya tidak berurutan, jadi pakai
# multinomial. Satu kategori menjadi basis pembanding.
#
# Catatan teknis: variabel dependen untuk multinomial harus berupa angka,
# jadi kita encode dulu kategorinya. Data ini juga nyaris terpisah, jadi
# estimasi memakai regularisasi.

# %%
transport = pd.read_csv("data/multi-ordinal-2.csv").rename(columns={
    "Transport": "transport", "Waktu_Tempuh": "waktu",
    "Biaya": "biaya", "Jarak_KM": "jarak"})
peta = {"Mobil": 0, "Motor": 1, "Umum": 2}
transport["kode"] = transport["transport"].map(peta)
transport["transport"].value_counts()

# %%
X_mn = sm.add_constant(transport[["waktu", "biaya", "jarak"]])
model_mn = sm.MNLogit(transport["kode"], X_mn).fit_regularized(alpha=0.1, disp=0)
print("Kategori basis: Mobil (kode 0)")
print(model_mn.params.round(3))

# %% [markdown]
# Koefisien dibaca relatif terhadap kategori basis Mobil. Untuk menyajikan
# hasil, cara paling intuitif adalah menghitung peluang prediksi untuk
# beberapa profil perjalanan. Hasil regularisasi tidak menyediakan
# `predict`, jadi peluang dihitung manual dengan softmax: eksponensial
# setiap skor dibagi jumlah eksponensial semua kategori.

# %%
profil = pd.DataFrame({
    "const": [1, 1, 1],
    "waktu": [20, 40, 60],
    "biaya": [8, 35, 15],
    "jarak": [5, 15, 14],
})
beta = model_mn.params.values
# Kolom pertama = skor kategori basis (Mobil, selalu nol); dua kolom
# berikutnya dihitung dari data @ koefisien, lalu diubah jadi peluang
# dengan softmax.
skor = np.column_stack([np.zeros(len(profil)), profil.values @ beta])
exp_skor = np.exp(skor - skor.max(axis=1, keepdims=True))
peluang = pd.DataFrame(exp_skor / exp_skor.sum(axis=1, keepdims=True),
                       columns=["Mobil", "Motor", "Umum"])
peluang.index = ["Dekat dan murah", "Jauh dan mahal", "Lama tapi murah"]
peluang.round(3)

# %% [markdown]
# Bacaan hasilnya masuk akal: perjalanan dekat dan murah didominasi Motor,
# perjalanan jauh dan mahal didominasi Mobil, dan perjalanan lama tapi
# murah didominasi angkutan Umum. Arah seperti ini yang dilaporkan di
# laporan, bukan koefisien mentah yang sulit dibaca.


# %% [markdown]
# ### Coba sendiri (5 menit)
#
# Pakai model multinomial tadi. Hitung peluang untuk profil: waktu 30,
# biaya 12, jarak 8. Gunakan pola softmax yang sama seperti di atas.
#
# Tulis di sel di bawah, baru buka jawabannya.

# %%
# Tulis kode Anda di sini

# %% [markdown]
# <details><summary>Lihat jawaban</summary>
#
# Skornya menghasilkan peluang [Mobil 0,006; Motor 0,96; Umum 0,03].
# Profil ini didominasi Motor karena waktunya sedang dan biayanya murah.
#
# </details>

# %% [markdown]
# ## 8. Ordinal logit: kepuasan layanan bank
#
# `multi-ordinal-1.csv`: kepuasan 1 sampai 3 (sangat tidak puas, netral,
# puas), dijelaskan waktu tunggu (menit), keramahan staf, dan penggunaan
# aplikasi digital. Kategorinya berurutan, jadi pakai ordinal.
#
# Perhatian: data simulasi ini nyaris terpisah sempurna, jadi koefisien
# absolutnya ekstrem (puluhan). Yang dibaca adalah TANDA dan arah
# pengaruhnya, bukan besarannya.

# %%
from statsmodels.miscmodels.ordinal_model import OrderedModel

kepuasan = pd.read_csv("data/multi-ordinal-1.csv").rename(columns={
    "Kepuasan": "kepuasan", "Kecepatan": "waktu_tunggu",
    "Staf_Ramah": "staf_ramah", "Digital_App": "digital_app"})
X_or = kepuasan[["waktu_tunggu", "staf_ramah", "digital_app"]]
model_ord = OrderedModel(kepuasan["kepuasan"], X_or, distr="logit")
hasil_ord = model_ord.fit(method="bfgs", disp=False)
print(hasil_ord.summary())

# %% [markdown]
# Wadah koefisien positif = mendorong ke kategori kepuasan lebih tinggi.
# Di data ini: waktu tunggu negatif (makin lama, makin tidak puas), staf
# ramah positif, aplikasi digital positif. Arahnya masuk akal semua.
#
# Tanda ambang (thresholds) harus meningkat; kalau tidak, ada masalah
# spesifikasi atau kategori terlalu sedikit.

# %%
peluang_ord = hasil_ord.predict(X_or)
tebakan = np.asarray(peluang_ord).argmax(axis=1) + 1
print(pd.crosstab(kepuasan["kepuasan"], tebakan,
                  rownames=["aktual"], colnames=["prediksi"]))

# %% [markdown]
# ## 9. Tobit: data tersensor di nol
#
# `tobit_data_1_rnd.csv`: pengeluaran R&D perusahaan. 28 dari 50 perusahaan
# melaporkan nol (tidak ada belanja R&D), jadi datanya tersensor di 0.
# OLS biasa bias di kasus begini.
#
# EViews punya metode TOBIT bawaan. statsmodels tidak, jadi kita tulis
# estimasi maximum likelihood-nya langsung. Bagi peserta dari ilmu
# komputer, bagian ini menunjukkan bahwa ekonometrika pada dasarnya
# adalah optimisasi fungsi likelihood.

# %%
from scipy.optimize import minimize
from scipy.stats import norm

def buat_negloglik(X, y, batas=0.0):
    """Negative log-likelihood Tobit tersensor kiri."""
    def negloglik(params):
        beta, log_sigma = params[:-1], params[-1]
        sigma = np.exp(log_sigma)
        mu = X @ beta
        tersensor = y <= batas
        ll = np.where(
            tersensor,
            norm.logcdf((batas - mu) / sigma),
            norm.logpdf((y - mu) / sigma) - np.log(sigma),
        )
        return -ll.sum()
    return negloglik

rnd = pd.read_csv("data/tobit_data_1_rnd.csv").rename(columns={
    "RND": "rnd", "PROFIT": "profit", "ASET": "aset", "PATEN": "paten"})
X_tob = sm.add_constant(rnd[["profit", "aset", "paten"]].values)
y_tob = rnd["rnd"].values

# Nilai awal untuk optimizer: koefisien OLS, ditambah sigma awal
# (di-log supaya nilainya selalu positif saat dioptimasi)
ols_awal = sm.OLS(y_tob, X_tob).fit()
mulai = np.r_[ols_awal.params, np.log(np.std(ols_awal.resid) + 1e-6)]
opt = minimize(buat_negloglik(X_tob, y_tob), mulai, method="Nelder-Mead",
               options={"maxiter": 20000, "xatol": 1e-8, "fatol": 1e-8})

print(f"Konvergen: {opt.success}")
print(pd.Series(opt.x, index=["const", "profit", "aset", "paten", "log_sigma"]).round(4))
print(f"Observasi tersensor: {(y_tob <= 0).sum()} dari {len(y_tob)}")

# %% [markdown]
# Bandingkan dengan OLS polos di data yang sama. Koefisien Tobit biasanya
# lebih besar pada kasus censoring berat. Ingat, koefisien Tobit adalah
# efek pada variabel laten (minat R&D yang tidak teramati), bukan efek
# langsung pada pengeluaran yang teramati.

# %%
print("OLS polos:")
print(pd.Series(ols_awal.params, index=["const", "profit", "aset", "paten"]).round(4))

# %% [markdown]
# ## 10. Poisson: data hitungan
#
# `poisson_data_2_restoran.csv`: jumlah pelanggan per jam dijelaskan jam
# sibuk, akhir pekan, dan jumlah promo aktif. Model Poisson memakai
# log-link:
#
# $$\ln(\lambda_i) = \beta_0 + \beta_1 X_{1i} + \dots$$

# %%
pelanggan = pd.read_csv("data/poisson_data_2_restoran.csv").rename(columns={
    "PELANGGAN": "pelanggan", "JAM_SIBUK": "jam_sibuk",
    "WEEKEND": "weekend", "JML_PROMO": "jml_promo"})
model_pois = smf.poisson("pelanggan ~ jam_sibuk + weekend + jml_promo",
                         data=pelanggan).fit(disp=0)
print(model_pois.summary())

# %%
irr = np.exp(model_pois.params)
pd.DataFrame({"koefisien": model_pois.params, "IRR": irr,
              "p_value": model_pois.pvalues}).round(4)

# %% [markdown]
# IRR = 2,53 untuk jam sibuk: jumlah pelanggan pada jam sibuk sekitar 2,5
# kali lipat jam biasa. Weekend menambah sekitar 22 persen, dan setiap satu
# promo aktif menambah sekitar 21 persen.
#
# ### Cek overdispersi
#
# Poisson mengasumsikan mean = varians. Kalau varians data jauh lebih besar
# (overdispersi), standard error Poisson terlalu kecil. Cek dengan
# statistik Pearson chi-kuadrat dibagi derajat bebas. Di atas 1,5 berarti
# curiga overdispersi.

# %%
overdisp = (model_pois.resid_pearson ** 2).sum() / model_pois.df_resid
print(f"Pearson chi2 / df = {overdisp:.3f}")
print("Di bawah 1,5: tidak ada indikasi overdispersi, Poisson cukup.")

# %% [markdown]
# Sekadar pembanding, ini hasil Negative Binomial yang lebih fleksibel.
# Bandingkan AIC-nya; model dengan AIC lebih kecil lebih disukai.

# %%
model_nb = smf.negativebinomial("pelanggan ~ jam_sibuk + weekend + jml_promo",
                                data=pelanggan).fit(disp=0)
print(f"AIC Poisson : {model_pois.aic:.2f}")
print(f"AIC NB      : {model_nb.aic:.2f}")

# %% [markdown]
# ## Latihan
#
# 1. Ulangi logit pada data `logit-probit-2.csv`, lalu jelaskan kenapa
#    koefisien MLE polosnya tidak bisa dipercaya. Bandingkan dengan hasil
#    `fit_regularized` di statsmodels dan `LogisticRegression` bawaan
#    scikit-learn. Mana yang paling mudah dijelaskan ke mahasiswa?
# 2. Ulangi model ordinal pada `multi-ordinal-1.csv` dengan
#    `distr="probit"`. Apakah tanda koefisiennya sama dengan versi logit?
# 3. Kasus `multi-ordinal-3.csv` sengaja disediakan sebagai bahan diskusi:
#    jalankan model ordinalnya, lalu periksa threshold-nya. Kalau nilai
#    ambang tidak naik berurutan (misalnya 9,36 lalu 4,92), modelnya
#    tidak koheren dan koefisien absolutnya jangan dikutip; sebutkan
#    keterbatasan ini di laporan.
# 4. scikit-learn: ulangi pembagian data latih dan uji pada dataset
#    Spector dengan `test_size=0.3` dan `random_state` berbeda. Apakah
#    akurasinya berubah banyak? Diskusikan kenapa metrik pada sampel
#    sekecil 32 observasi tidak stabil.
# 5. Poisson kasus pertama: `poisson_data_1_klaim.csv`
#    (`jml_klaim ~ usia + pengalaman + tipe_mobil`). Hitung IRR, cek
#    overdispersi, dan bandingkan AIC Poisson dengan Negative Binomial.

# %% [markdown]
# ### Selanjutnya
#
# Selanjutnya: Sesi 5 masuk ke data deret waktu.
