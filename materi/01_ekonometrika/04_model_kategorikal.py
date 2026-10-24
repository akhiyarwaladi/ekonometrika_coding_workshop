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
# | Hitungan (jumlah klaim, jumlah pelanggan) | Poisson; Negative Binomial sebagai model khusus |
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
# | Model linear, logit, multinomial, Poisson, koefisien, prediksi | scikit-learn |
# | Standard error, p-value, efek marjinal, uji asumsi | statsmodels |
# | Uji heteroskedastisitas, normalitas, ADF, kointegrasi | statsmodels |
# | Model data panel | linearmodels |
# | Model volatilitas GARCH | arch |
# | Prediksi, splitting data, metrik klasifikasi (akurasi, ROC AUC) | scikit-learn |
#
# Model utama memakai scikit-learn dari awal. Standard error dan p-value
# disediakan pada bagian pelengkap statistik dengan nama `uji_...`. Probit,
# ordinal, Tobit, dan Negative Binomial dibahas sebagai model khusus.

# %% [markdown]
# **Posisi dalam alur workshop.** Sesi 1-3 menangani Y kontinu. Sesi ini
# menangani Y berupa kategori, hitungan, dan data tersensor. Sesi 5 masuk
# ke data deret waktu.

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

# Siapkan alat untuk contoh model khusus; jalankan apa adanya.
import sys
import tempfile
from urllib.request import urlretrieve

folder_alat = tempfile.mkdtemp(prefix="alat_ekonometrika_")
urlretrieve(
    "https://raw.githubusercontent.com/akhiyarwaladi/ekonometrika_coding_workshop/main/alat_bantu/metode_lanjutan.py",
    folder_alat + "/metode_lanjutan.py",
)
sys.path.insert(0, folder_alat)

print("Alamat data siap. Jalankan sel pembacaan CSV berikutnya.")

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

# %% [markdown]
# <!-- kamus_variabel:spector -->
#
# ### Kenali data: Efektivitas metode pengajaran Spector
#
# **Data:** dataset bawaan statsmodels (`spector`). **Satu baris:** satu mahasiswa; total 32 mahasiswa pada data sumber.
#
# | Variabel/kolom | Pengertian | Satuan atau kode | Peran |
# |---|---|---|---|
# | `GPA` | Grade Point Average: rata-rata prestasi akademik mahasiswa, sejenis IPK. | Poin rata-rata nilai | X: penjelas |
# | `TUCE` | Skor tes pemahaman ekonomi mahasiswa. | Poin tes | X: penjelas |
# | `PSI` | Keikutsertaan dalam Personalized System of Instruction, program/metode pengajaran yang diteliti. | 1 = mengikuti; 0 = tidak | X: penjelas |
# | `GRADE` | Apakah nilai mahasiswa meningkat pada pengamatan program. | 1 = meningkat; 0 = tidak meningkat | Y: target |
#
# GRADE bukan nilai huruf A/B/C dan 0 tidak berarti mahasiswa pasti gagal kuliah. Data ini dibaca dari statsmodels, sehingga tidak memiliki CSV terpisah di paket.
#
# Sumber definisi: [rujukan data](https://www.statsmodels.org/stable/datasets/generated/spector.html).

# %%
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import PoissonRegressor
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
print(f"Pseudo R2 (McFadden): {uji_model_logit.prsquared:.4f}")
print(f"LLR p-value         : {uji_model_logit.llr_pvalue:.6g}")

# %% [markdown]
# ## 2. Odds ratio
#
# $OR = e^{\beta}$. OR = 1,5 berarti kenaikan 1 unit X menaikkan odds
# (bukan peluang) sebesar 50%. Angka di bawah 1 berarti menurunkan odds.
# OR untuk PSI sekitar 10,8: mahasiswa yang ikut metode baru punya odds
# nilai meningkat sepuluh kali lipat dibanding yang tidak, setelah GPA dan
# tes awal dikontrol.

# %%
odds_ratio = np.exp(koefisien_model_logit)
pd.DataFrame(
    {
        "koefisien_log_odds": koefisien_model_logit,
        "odds_ratio": odds_ratio,
        "p_value": uji_model_logit.pvalues,
    }
).round(4)

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
# Efek marjinal merangkum perubahan peluang. `at="overall"` menghitungnya
# untuk setiap observasi lalu mengambil rata-rata (average marginal effect).
# Untuk dummy PSI, `dummy=True` menghitung perubahan saat PSI berganti 0 ke 1.
# Hasil 0,30 berarti perubahan sekitar 30 poin persentase, bukan 30 persen.

# %%
efek = uji_model_logit.get_margeff(at="overall", dummy=True)
print(efek.summary())

# %% [markdown]
# ## 4. Probit dan perbandingannya (model khusus)
#
# Probit memakai distribusi normal, bukan logistik. Kesimpulannya biasanya
# sama, hanya skala koefisiennya berbeda: koefisien logit sekitar 1,6
# sampai 1,8 kali koefisien probit. Cara aman membandingkan tetap lewat
# efek marjinal.

# %%
model_probit = smf.probit("GRADE ~ GPA + TUCE + PSI", data=spector).fit(disp=0)
print(model_probit.summary())

# %%
banding_me = pd.DataFrame(
    {
        "ME_logit": np.asarray(
            uji_model_logit.get_margeff(at="overall", dummy=True).margeff
        ),
        "ME_probit": np.asarray(
            model_probit.get_margeff(at="overall", dummy=True).margeff
        ),
    },
    index=["GPA", "TUCE", "PSI"],
)
banding_me.round(4)

# %% [markdown]
# ## 5. Menilai ketepatan klasifikasi
#
# Model probabilitas perlu diubah jadi keputusan ya/tidak pada ambang
# tertentu (lazimnya 0,5), lalu dibandingkan dengan kenyataan.

# %%
prediksi = (
    pd.Series(
        model_logit.predict_proba(spector[["GPA", "TUCE", "PSI"]])[:, 1],
        index=spector.index,
    )
    > 0.5
).astype(int)
tabel_klasifikasi = pd.crosstab(
    spector["GRADE"], prediksi, rownames=["aktual"], colnames=["prediksi"]
)
# Bandingkan prediksi dan hasil aktual; mean() adalah proporsi yang benar.
akurasi = (prediksi == spector["GRADE"]).mean()
print(tabel_klasifikasi)
print(f"Akurasi = {akurasi:.3f}")

# %% [markdown]
# ### Kalau layar Anda menampilkan peringatan "Perfect Separation"
#
# Data kredit mikro di `logit_probit_1.csv` dan data mahasiswa di
# `logit_probit_2.csv` hasil simulasi ternyata TERPISAH SEMPURNA: kombinasi
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
# Contoh dengan `logit_probit_2.csv`:

# %% [markdown]
# <!-- kamus_variabel:logit_probit_2.csv -->
#
# ### Kenali data: Kelulusan tepat waktu
#
# **Data:** `data/logit_probit_2.csv`. **Satu baris:** satu mahasiswa.
#
# Nama singkat di kode berasal dari penggantian nama kolom CSV; isi angkanya tetap sama.
#
# | Kolom CSV | Nama di kode | Pengertian | Satuan atau kode | Peran |
# |---|---|---|---|---|
# | `LULUS_TEPAT` | `lulus_tepat` | Apakah mahasiswa menyelesaikan studi tepat waktu. | 1 = tepat waktu; 0 = tidak tepat waktu | Y: target |
# | `IPK_SEM2` | `ipk_sem2` | Indeks Prestasi Kumulatif sampai semester 2. | Poin IPK | X: penjelas |
# | `SKS_LULUS_SEM2` | `sks_lulus_sem2` | Beban studi yang telah diselesaikan sampai semester 2; SKS = Satuan Kredit Semester. | SKS | X: penjelas |
# | `KEAKTIFAN_ORG` | `keaktifan_org` | Keaktifan mahasiswa dalam organisasi. | 1 = aktif; 0 = tidak aktif | X: penjelas |
# | `BEASISWA` | `beasiswa` | Status penerimaan beasiswa. | 1 = penerima; 0 = bukan penerima | X: penjelas |
#
# Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

# %%
lulus = pd.read_csv(URL_DATA + "logit_probit_2.csv")
lulus = lulus.rename(
    columns={
        "LULUS_TEPAT": "lulus_tepat",
        "IPK_SEM2": "ipk_sem2",
        "SKS_LULUS_SEM2": "sks_lulus_sem2",
        "KEAKTIFAN_ORG": "keaktifan_org",
        "BEASISWA": "beasiswa",
    }
)

# Alat bantu menangani kemungkinan MLE gagal, agar notebook bisa dilanjutkan.
# Sumbernya ada di alat_bantu/metode_lanjutan.py dan sudah ikut paket data.
from metode_lanjutan import coba_logit

rumus_lulus = "lulus_tepat ~ ipk_sem2 + sks_lulus_sem2 + keaktifan_org + beasiswa"
print(coba_logit(rumus_lulus, lulus))

sampel_model_reg = lulus[
    ["lulus_tepat", "ipk_sem2", "sks_lulus_sem2", "keaktifan_org", "beasiswa"]
].dropna()
X_model_reg = sampel_model_reg[
    ["ipk_sem2", "sks_lulus_sem2", "keaktifan_org", "beasiswa"]
]
y_model_reg = sampel_model_reg["lulus_tepat"]

model_reg = LogisticRegression(
    penalty="l1", C=2.0, solver="liblinear", max_iter=5000, tol=1e-9
)
model_reg.fit(X_model_reg, y_model_reg)

koefisien_model_reg = pd.Series(model_reg.coef_[0], index=X_model_reg.columns)
koefisien_model_reg.loc["Intercept"] = model_reg.intercept_[0]
print("\nKoefisien setelah regularisasi (lebih stabil):")
print(koefisien_model_reg.round(3))

# %% [markdown]
# Setelah regularisasi, tanda koefisien biasanya masuk akal (IPK positif,
# beasiswa positif), tapi p-value tidak tersedia karena estimatornya sudah
# bukan MLE biasa. Untuk laporan ilmiah dengan kasus begini, sebutkan
# keterbatasannya secara terbuka.

# %% [markdown]
# ## 6. Memeriksa koefisien dan mengevaluasi prediksi
#
# Periksa kesesuaian model utama dengan pelengkap inferensi ketika
# scikit-learn dijalankan tanpa regularisasi (`penalty=None`).

# %%
from sklearn.linear_model import LogisticRegression

X_sp = spector[["GPA", "TUCE", "PSI"]]
y_sp = spector["GRADE"]

sk_logit = model_logit
print(
    "Koefisien scikit-learn:",
    sk_logit.coef_.round(3),
    "| intersep:",
    round(sk_logit.intercept_[0], 3),
)
print(
    "Koefisien pelengkap inferensi:",
    uji_model_logit.params[["GPA", "TUCE", "PSI"]].round(3).to_list(),
    "| intersep:",
    round(uji_model_logit.params["Intercept"], 3),
)

# %% [markdown]
# Angkanya sangat dekat, dengan selisih kecil akibat optimasi numerik.
# Selanjutnya bagi data latih dan uji, lalu hitung metrik pada data uji.

# %%
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split

X_latih, X_uji, y_latih, y_uji = train_test_split(
    X_sp, y_sp, test_size=0.25, random_state=42
)

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
print(
    "Akurasi di data yang sama:",
    round(sk_lulus.score(lulus_X, lulus["lulus_tepat"]), 3),
)

# %% [markdown]
# ## 7. Multinomial logit: pilihan moda transportasi
#
# `multi_ordinal_2.csv`: pilihan transport (Motor, Mobil, Umum) dijelaskan
# waktu tempuh, biaya, dan jarak. Kategorinya tidak berurutan, jadi pakai
# multinomial. Model menghasilkan peluang untuk setiap kategori.
#
# scikit-learn dapat menerima label teks seperti Mobil, Motor, dan Umum.
# Data ini nyaris terpisah, sehingga kita memakai regularisasi L2 bawaan.

# %% [markdown]
# <!-- kamus_variabel:multi_ordinal_2.csv -->
#
# ### Kenali data: Pilihan transportasi kerja
#
# **Data:** `data/multi_ordinal_2.csv`. **Satu baris:** satu pekerja/responden perjalanan ke kantor.
#
# Nama singkat di kode berasal dari penggantian nama kolom CSV; isi angkanya tetap sama.
#
# | Kolom CSV | Nama di kode | Pengertian | Satuan atau kode | Peran |
# |---|---|---|---|---|
# | `Transport` | `transport` | Moda transportasi yang dipilih. | Kategori: Mobil, Motor, Umum; tidak berurutan | Y: target |
# | `Waktu_Tempuh` | `waktu` | Lama perjalanan menuju tempat kerja. | Menit | X: penjelas |
# | `Biaya` | `biaya` | Biaya transportasi yang dikeluarkan. | Ribu rupiah per hari | X: penjelas |
# | `Jarak_KM` | `jarak` | Jarak rumah ke kantor. | Kilometer (km) | X: penjelas |
#
# Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

# %%
transport = pd.read_csv(URL_DATA + "multi_ordinal_2.csv")
transport = transport.rename(
    columns={
        "Transport": "transport",
        "Waktu_Tempuh": "waktu",
        "Biaya": "biaya",
        "Jarak_KM": "jarak",
    }
)
transport["transport"].value_counts()

# %%
X_mn = transport[["waktu", "biaya", "jarak"]]
y_mn = transport["transport"]
model_mn = LogisticRegression(max_iter=5000)
model_mn.fit(X_mn, y_mn)
koefisien_mn = pd.DataFrame(
    model_mn.coef_, index=model_mn.classes_, columns=X_mn.columns
)
print(koefisien_mn.round(3))

# %% [markdown]
# Baris koefisien mengikuti `classes_`; scikit-learn memakai parameterisasi
# simetris, sehingga tabel ini tidak dibaca sebagai koefisien terhadap satu
# kategori basis. Untuk menyajikan hasil, gunakan `predict_proba()`.
# `predict()` langsung menghasilkan nama kategori yang diprediksi.

# %%
profil = pd.DataFrame(
    {
        "waktu": [20, 40, 60],
        "biaya": [8, 35, 15],
        "jarak": [5, 15, 14],
    }
)
# predict_proba() mengembalikan peluang sesuai urutan classes_.
peluang = pd.DataFrame(model_mn.predict_proba(profil), columns=model_mn.classes_)
peluang.index = ["Dekat dan murah", "Jauh dan mahal", "Lama tapi murah"]
peluang.round(3)

# %% [markdown]
# Baca kategori dengan peluang terbesar pada setiap baris. Bandingkan
# bagaimana waktu, biaya, dan jarak mengubah peluang perjalanan.
# Peluang bergantung pada data dan pengaturan regularisasi yang dipakai.

# %% [markdown]
# ### Coba sendiri (5 menit)
#
# Pakai model multinomial tadi. Hitung peluang untuk profil: waktu 30,
# biaya 12, jarak 8. Buat tabel profil baru, lalu gunakan `predict_proba()`.
#
# Tulis di sel di bawah, baru buka jawabannya.

# %%
# Tulis kode Anda di sini

# %% [markdown]
# <details><summary>Lihat jawaban</summary>
#
# `contoh = pd.DataFrame({"waktu": [30], "biaya": [12], "jarak": [8]})`
# lalu `pd.DataFrame(model_mn.predict_proba(contoh), columns=model_mn.classes_)`.
# Sebutkan kategori dengan peluang terbesar pada tabel yang dihasilkan.
#
# </details>

# %% [markdown]
# ## 8. Ordinal logit: kepuasan layanan bank (model khusus)
#
# `multi_ordinal_1.csv`: kepuasan 1 sampai 3 (sangat tidak puas, netral,
# puas), dijelaskan waktu tunggu (menit), keramahan staf, dan penggunaan
# aplikasi digital. Kategorinya berurutan, jadi pakai ordinal.
#
# Perhatian: data simulasi ini nyaris terpisah sempurna, jadi koefisien
# absolutnya ekstrem (puluhan). Yang dibaca adalah TANDA dan arah
# pengaruhnya, bukan besarannya.

# %% [markdown]
# <!-- kamus_variabel:multi_ordinal_1.csv -->
#
# ### Kenali data: Kepuasan layanan bank
#
# **Data:** `data/multi_ordinal_1.csv`. **Satu baris:** satu responden pengguna layanan bank.
#
# Nama singkat di kode berasal dari penggantian nama kolom CSV; isi angkanya tetap sama.
#
# | Kolom CSV | Nama di kode | Pengertian | Satuan atau kode | Peran |
# |---|---|---|---|---|
# | `Kepuasan` | `kepuasan` | Kategori kepuasan terhadap layanan, berurutan dari rendah ke tinggi. | 1 = sangat tidak puas; 2 = netral; 3 = puas | Y: target |
# | `Kecepatan` | `waktu_tunggu` | Lama menunggu pelayanan. Angka lebih besar berarti menunggu lebih lama. | Menit | X: penjelas |
# | `Staf_Ramah` | `staf_ramah` | Penilaian keramahan staf. | Skor 1 sampai 10 | X: penjelas |
# | `Digital_App` | `digital_app` | Frekuensi penggunaan aplikasi digital bank yang dibuat sebagai indikator. | 1 = sering memakai; 0 = jarang/tidak | X: penjelas |
#
# Nama Kecepatan pada CSV berarti waktu tunggu, bukan skor kecepatan. Di contoh utama namanya diperjelas menjadi waktu_tunggu.
#
# Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

# %%
from statsmodels.miscmodels.ordinal_model import OrderedModel

kepuasan = pd.read_csv(URL_DATA + "multi_ordinal_1.csv")
kepuasan = kepuasan.rename(
    columns={
        "Kepuasan": "kepuasan",
        "Kecepatan": "waktu_tunggu",
        "Staf_Ramah": "staf_ramah",
        "Digital_App": "digital_app",
    }
)
X_or = kepuasan[["waktu_tunggu", "staf_ramah", "digital_app"]]
model_ord = OrderedModel(kepuasan["kepuasan"], X_or, distr="logit")
hasil_ord = model_ord.fit(method="bfgs", disp=False)
print(hasil_ord.summary())

# %% [markdown]
# Wadah koefisien positif = mendorong ke kategori kepuasan lebih tinggi.
# Di data ini: waktu tunggu negatif (makin lama, makin tidak puas), staf
# ramah positif, aplikasi digital positif. Arahnya masuk akal semua.
#
# Parameter ambang di `summary()` disimpan dalam bentuk transformasi.
# Nilainya tidak boleh langsung dibandingkan sebagai batas kategori.
# Gunakan perintah berikut untuk menampilkan ambang pada skala aslinya.

# %%
ambang = model_ord.transform_threshold_params(hasil_ord.params)
print("Ambang asli, termasuk batas -inf dan inf:", ambang)

# %%
peluang_ord = hasil_ord.predict(X_or)
tebakan = np.asarray(peluang_ord).argmax(axis=1) + 1
print(
    pd.crosstab(
        kepuasan["kepuasan"], tebakan, rownames=["aktual"], colnames=["prediksi"]
    )
)

# %% [markdown]
# ## 9. Tobit: data tersensor di nol (model khusus)
#
# `tobit_data_1_rnd.csv`: pengeluaran R&D perusahaan. 28 dari 50 perusahaan
# melaporkan nol. Pada contoh ini kita mengasumsikan Y = max(0, Y laten),
# sehingga Tobit relevan. Nilai nol saja belum membuktikan sensor; pada
# penelitian nyata periksa mekanisme datanya terlebih dahulu.
#
# EViews mempunyai TOBIT bawaan. Di sini perhitungan maximum likelihood
# disediakan dalam `alat_bantu/metode_lanjutan.py` dan ikut paket data. Peserta cukup
# menentukan Y, daftar X, dan batas sensor. Fungsi tetap memakai likelihood
# Tobit normal; kode perhitungannya dapat dibaca pengajar sebagai pendalaman.

# %% [markdown]
# <!-- kamus_variabel:tobit_data_1_rnd.csv -->
#
# ### Kenali data: Pengeluaran penelitian dan pengembangan
#
# **Data:** `data/tobit_data_1_rnd.csv`. **Satu baris:** satu perusahaan.
#
# Nama singkat di kode berasal dari penggantian nama kolom CSV; isi angkanya tetap sama.
#
# | Kolom CSV | Nama di kode | Pengertian | Satuan atau kode | Peran |
# |---|---|---|---|---|
# | `RND` | `rnd` | Pengeluaran Research and Development (R&D), yaitu penelitian dan pengembangan. | Juta dolar AS; tersensor pada 0 | Y: target |
# | `PROFIT` | `profit` | Keuntungan perusahaan. | Juta dolar AS | X: penjelas |
# | `ASET` | `aset` | Total aset yang dimiliki perusahaan. | Miliar dolar AS | X: penjelas |
# | `PATEN` | `paten` | Jumlah paten pada tahun sebelumnya. | Paten | X: penjelas |
#
# RND = 0 adalah nilai pengeluaran yang tercatat pada batas bawah, bukan nilai kosong. Satuan PROFIT dan ASET berbeda skala.
#
# Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

# %%
from metode_lanjutan import estimasi_tobit

rnd = pd.read_csv(URL_DATA + "tobit_data_1_rnd.csv")
rnd = rnd.rename(
    columns={"RND": "rnd", "PROFIT": "profit", "ASET": "aset", "PATEN": "paten"}
)
hasil_tobit = estimasi_tobit(rnd, y="rnd", x=["profit", "aset", "paten"], batas=0)
print(hasil_tobit.round(4))

# %% [markdown]
# Bandingkan dengan OLS polos di data yang sama. Koefisien Tobit biasanya
# lebih besar pada kasus censoring berat. Ingat, koefisien Tobit adalah
# efek pada variabel laten (minat R&D yang tidak teramati), bukan efek
# langsung pada pengeluaran yang teramati.

# %%
print("Koefisien OLS dan Tobit pada sampel yang sama:")
print(hasil_tobit.round(4))

# %% [markdown]
# ## 10. Poisson: data hitungan
#
# `poisson_data_2_restoran.csv`: jumlah pelanggan per jam dijelaskan jam
# sibuk, akhir pekan, dan jumlah promo aktif. Model Poisson memakai
# log-link:
#
# $$\ln(\lambda_i) = \beta_0 + \beta_1 X_{1i} + \dots$$

# %% [markdown]
# <!-- kamus_variabel:poisson_data_2_restoran.csv -->
#
# ### Kenali data: Kunjungan pelanggan restoran
#
# **Data:** `data/poisson_data_2_restoran.csv`. **Satu baris:** satu interval pengamatan selama satu jam.
#
# Nama singkat di kode berasal dari penggantian nama kolom CSV; isi angkanya tetap sama.
#
# | Kolom CSV | Nama di kode | Pengertian | Satuan atau kode | Peran |
# |---|---|---|---|---|
# | `PELANGGAN` | `pelanggan` | Jumlah pelanggan yang datang pada jam pengamatan. | Orang per jam; bilangan bulat | Y: target |
# | `JAM_SIBUK` | `jam_sibuk` | Apakah jam pengamatan termasuk jam makan siang/malam. | 1 = jam sibuk; 0 = jam lainnya | X: penjelas |
# | `WEEKEND` | `weekend` | Apakah pengamatan berlangsung pada akhir pekan. | 1 = akhir pekan; 0 = hari kerja | X: penjelas |
# | `JML_PROMO` | `jml_promo` | Jumlah program promosi yang sedang aktif. | Program promosi | X: penjelas |
#
# Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

# %%
pelanggan = pd.read_csv(URL_DATA + "poisson_data_2_restoran.csv")
pelanggan = pelanggan.rename(
    columns={
        "PELANGGAN": "pelanggan",
        "JAM_SIBUK": "jam_sibuk",
        "WEEKEND": "weekend",
        "JML_PROMO": "jml_promo",
    }
)
sampel_model_pois = pelanggan[
    ["pelanggan", "jam_sibuk", "weekend", "jml_promo"]
].dropna()
X_model_pois = sampel_model_pois[["jam_sibuk", "weekend", "jml_promo"]]
y_model_pois = sampel_model_pois["pelanggan"]

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
print(uji_model_pois.summary())

# %%
irr = np.exp(koefisien_model_pois)
pd.DataFrame(
    {"koefisien": koefisien_model_pois, "IRR": irr, "p_value": uji_model_pois.pvalues}
).round(4)

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
overdisp = (uji_model_pois.resid_pearson**2).sum() / uji_model_pois.df_resid
print(f"Pearson chi2 / df = {overdisp:.3f}")
print("Di bawah 1,5: tidak ada indikasi overdispersi, Poisson cukup.")

# %% [markdown]
# Sekadar pembanding, ini hasil Negative Binomial yang lebih fleksibel.
# Bandingkan AIC-nya; model dengan AIC lebih kecil lebih disukai.

# %%
model_nb = smf.negativebinomial(
    "pelanggan ~ jam_sibuk + weekend + jml_promo", data=pelanggan
).fit(disp=0)
print(f"AIC Poisson : {uji_model_pois.aic:.2f}")
print(f"AIC NB      : {model_nb.aic:.2f}")

# %% [markdown]
# ## Latihan
#
# 1. Ulangi logit pada data `logit_probit_2.csv`, lalu jelaskan kenapa
#    koefisien MLE polosnya tidak bisa dipercaya. Bandingkan dengan hasil
#    `LogisticRegression` dengan regularisasi L1 dan L2. Mana yang paling mudah dijelaskan ke mahasiswa?
# 2. Ulangi model ordinal pada `multi_ordinal_1.csv` dengan
#    `distr="probit"`. Apakah tanda koefisiennya sama dengan versi logit?
# 3. Kasus `multi_ordinal_3.csv` sengaja disediakan sebagai bahan diskusi:
#    jalankan model ordinalnya, lalu tampilkan ambang asli memakai
#    `model.transform_threshold_params(hasil.params)`. Mengapa parameter
#    9,36 lalu 4,92 di summary bukan bukti bahwa ambangnya terbalik?
#    Periksa juga status konvergensi dan ketidakpastian estimasinya.
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
