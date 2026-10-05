# %% [markdown]
# # Hari 1, Sesi 3: Variabel Dummy dan Uji Asumsi Klasik
#
# **Durasi:** 90 menit
#
# Dua bagian besar. Pertama, variabel dummy untuk data kategorikal (gender,
# status, periode krisis). Kedua, empat uji asumsi klasik yang wajib bisa
# dijalankan dan ditafsirkan: multikolinearitas, heteroskedastisitas,
# normalitas, dan autokorelasi.
#
# Pola kerja yang dipakai sepanjang sesi:
#
# 1. Estimasi model OLS.
# 2. Jalankan uji diagnostik.
# 3. Kalau asumsi dilanggar, tangani dengan alat yang sesuai: robust
#    standard error (HC3) untuk heteroskedastisitas, HAC untuk
#    autokorelasi, dan buang atau gabungkan variabel untuk
#    multikolinearitas.
# 4. BARU interpretasi, karena koefisien dan p-value setelah perbaikan bisa
#    berbeda dari hasil OLS polos.

# %% [markdown]
# **Posisi dalam alur workshop.** Setelah bentuk model tepat (Sesi 2),
# sekarang periksa apakah hasilnya layak dipercaya. Sesi berikutnya
# mengganti jenis variabel Y dari kontinu ke kategorikal.

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
# ## 1. Variabel dummy
#
# Data `latihan-dummy-1.csv`: gaji, pengalaman, gender, dan status pernikahan
# 30 karyawan. Dua variabel terakhir kategorikal, jadi harus diubah ke angka
# dulu. Ini yang di EViews dilakukan otomatis lewat fitur dummy.

# %%
import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", palette=["#2F5D50", "#C15937", "#D9A441", "#5B8A8F"])
plt.rcParams.update({"figure.dpi": 110, "axes.titleweight": "bold", "font.size": 11})

gaji = pd.read_csv("data/latihan-dummy-1.csv").rename(columns={
    "GAJI": "gaji", "PENGALAMAN": "pengalaman", "GENDER": "gender",
    "STATUS": "status"})
gaji["gender"].value_counts(), gaji["status"].value_counts()

# %% [markdown]
# ### Dummy trap dan cara menghindarinya
#
# Kalau dua kategori (Pria/Wanita) dibuat dua kolom dummy, jumlah keduanya
# selalu 1. Kolom itu menjadi kombinasi linear sempurna dengan konstanta,
# dan OLS tidak bisa diestimasi. Solusinya: selalu buang satu kategori
# sebagai basis.
#
# `pd.get_dummies(..., drop_first=True)` melakukan ini otomatis, tapi
# kategori yang dibuang mengikuti urutan alfabet. Supaya kontrol tetap di
# tangan kita, di sini kolom dummy dibuat eksplisit. Basisnya: Wanita dan
# Lajang.

# %%
gaji_d = gaji.copy()
gaji_d["dummy_pria"] = (gaji_d["gender"] == "Pria").astype(int)
gaji_d["dummy_menikah"] = (gaji_d["status"] == "Menikah").astype(int)
gaji_d.head()

# %%
model_dummy_mentah = smf.ols("gaji ~ dummy_pria + dummy_menikah",
                             data=gaji_d).fit()
print(model_dummy_mentah.summary())

# %%
model_dummy = smf.ols("gaji ~ pengalaman + dummy_pria + dummy_menikah",
                      data=gaji_d).fit()
print(model_dummy.summary())

# %% [markdown]
# ### Menafsirkan dummy
#
# Basis di sini adalah Wanita dan Lajang. Di model mentah (tanpa kontrol),
# `dummy_pria` = +3,35 dan `dummy_menikah` = +7,05, keduanya signifikan.
# Setelah pengalaman kerja dikontrol, keduanya mengecil mendekati nol dan
# tidak lagi signifikan.
#
# Ini pelajaran penting: koefisien dummy adalah selisih antar kelompok
# SETELAH variabel lain dikontrol. Perbedaan mentah di data ini sebagian
# besar dijelaskan oleh pengalaman kerja yang berbeda antar kelompok.
# Model mana yang dilaporkan? Tergantung pertanyaan penelitian: untuk
# membandingkan perbedaan mentah antar kelompok, pakai model tanpa
# kontrol; untuk membandingkan kelompok dengan pengalaman yang setara,
# pakai model terkontrol. Yang tidak boleh: melaporkan model mentah lalu
# bicara seolah pengalaman sudah dikontrol.
#
# Intersep = rata-rata gaji kelompok basis saat pengalaman = 0.
# Di laporan, selalu sebut kategori basisnya secara eksplisit.

# %% [markdown]
# ## 2. Dummy untuk peristiwa: krisis ekonomi
#
# `latihan-dummy-2.csv`: PDB dan investasi tahunan, dengan dummy `KRISIS`
# bernilai 1 di tahun krisis. Model: `pdb ~ investasi + suku_bunga + krisis`.

# %%
krisis = pd.read_csv("data/latihan-dummy-2.csv").rename(columns={
    "Tahun": "tahun", "PDB": "pdb", "INVESTASI": "investasi",
    "SUKU_BUNGA": "suku_bunga", "KRISIS": "krisis"})
model_krisis = smf.ols("pdb ~ investasi + suku_bunga + krisis",
                       data=krisis).fit()
print(model_krisis.summary())

# %% [markdown]
# Koefisien `krisis` adalah perbedaan rata-rata PDB pada tahun krisis
# dibanding tahun normal, setelah investasi dan suku bunga dikontrol.
# Kalau negatif dan signifikan: krisis berdampak buruk, sesuai dugaan.


# %% [markdown]
# ### Coba sendiri (5 menit)
#
# Dengan model dummy di bagian 1, prediksi gaji untuk Wanita yang belum
# menikah dengan pengalaman 5 tahun.
#
# Tulis di sel di bawah, baru buka jawabannya.

# %%
# Tulis kode Anda di sini

# %% [markdown]
# <details><summary>Lihat jawaban</summary>
#
# Kedua dummy bernilai nol, jadi gajinya = intersep + 1,3489 x 5.
# Hasilnya sekitar 10,80 (satuan sama dengan kolom gaji).
#
# </details>

# %% [markdown]
# Bagian dummy selesai. Mulai di sini, kita kembali ke model OLS dengan
# variabel kontinu dan memeriksa satu per satu asumsi klasiknya.
#
# ## 3. Uji multikolinearitas
#
# Multikolinearitas = korelasi tinggi antar variabel penjelas. Akibatnya
# standard error membengkak, t-statistik mengecil, dan koefisien jadi tidak
# stabil. Deteksinya dengan VIF (Variance Inflation Factor).
#
# Aturan praktis: VIF di atas 10 menandakan masalah serius. Di antara 5 dan
# 10, perlu kehati-hatian.

# %%
from statsmodels.stats.outliers_influence import variance_inflation_factor

rumah = pd.read_csv("data/latihan-multikolinieritas-1.csv").rename(columns={
    "HARGA": "harga", "LUAS_BANGUNAN": "luas_bangunan",
    "LUAS_TANAH": "luas_tanah", "JML_KAMAR": "jml_kamar"})

X = sm.add_constant(rumah[["luas_bangunan", "luas_tanah", "jml_kamar"]])
vif = pd.DataFrame({
    "variabel": X.columns,
    "VIF": [variance_inflation_factor(X.values, i) for i in range(X.shape[1])],
})
vif

# %% [markdown]
# Kalau `luas_bangunan` dan `luas_tanah` punya VIF besar, lihat korelasinya.
# Di data ini korelasinya 0,99. Sebagai patokan, korelasi antar penjelas
# di atas 0,8 sudah patut dicurigai.

# %%
rumah[["luas_bangunan", "luas_tanah", "jml_kamar"]].corr()

# %%
model_rumah = smf.ols("harga ~ luas_bangunan + luas_tanah + jml_kamar",
                      data=rumah).fit()
print(f"R2 = {model_rumah.rsquared:.4f}")
print(model_rumah.summary())

# %% [markdown]
# Perhatikan kombinasi yang khas: R kuadrat tinggi dan uji F signifikan,
# tapi koefisien satu per satu tidak signifikan. Ini gejala klasik
# multikolinearitas. Solusinya: buang salah satu variabel yang redundan,
# gabungkan keduanya, atau perbesar sampel.


# %% [markdown]
# ### Coba sendiri (5 menit)
#
# Hitung ulang VIF setelah `luas_tanah` dibuang. Apakah masalahnya selesai?
#
# Tulis di sel di bawah, baru buka jawabannya.

# %%
# Tulis kode Anda di sini

# %% [markdown]
# <details><summary>Lihat jawaban</summary>
#
# VIF tersisa: `luas_bangunan` 13,4 dan `jml_kamar` 13,4. Membaik dari
# 64 dan 45, tapi masih di atas 10 karena korelasinya 0,96. Langkah
# lanjut: pertimbangkan hanya memakai satu di antaranya.
#
# </details>

# %% [markdown]
# ## 4. Uji heteroskedastisitas
#
# Varians residual yang berubah-ubah sepanjang nilai X. Dampaknya: standard
# error OLS salah, sehingga uji t dan uji F tidak valid. Gejalanya sering
# terlihat di scatter residual vs fitted.
#
# Data `hetero-3.csv`: harga rumah dijelaskan luas bangunan, jumlah kamar,
# dan skor lokasi. Dugaan di soal: variasi harga jauh lebih besar untuk
# rumah luas di lokasi premium.

# %%
hunian = pd.read_csv("data/hetero-3.csv").rename(columns={
    "Harga": "harga", "Luas": "luas", "Kamar": "kamar", "Lokasi": "lokasi"})
model_h = smf.ols("harga ~ luas + kamar + lokasi", data=hunian).fit()
print(model_h.summary())

# %%
fig, ax = plt.subplots(figsize=(7, 4.5))
ax.scatter(model_h.fittedvalues, model_h.resid, color="#2F5D50", s=26)
ax.axhline(0, color="#C15937", lw=1.2)
ax.set_xlabel("Nilai fitted")
ax.set_ylabel("Residual")
ax.set_title("Residual vs Fitted: cek pola melebar")
plt.show()

# %% [markdown]
# Kalau titik-titik membentuk corong (makin melebar ke kanan), itu tanda
# heteroskedastisitas. Tapi jangan hanya mengandalkan mata. Jalankan uji
# formal: Breusch-Pagan, White, dan Glejser.
#
# Hipotesis nol ketiganya sama: varians residual konstan (homoskedastis).
# p-value kecil = tolak H0 = ada heteroskedastisitas.

# %%
from statsmodels.stats.diagnostic import het_breuschpagan, het_white

Xh = sm.add_constant(hunian[["luas", "kamar", "lokasi"]])
resid = model_h.resid

for nama, hasil in [
    ("Breusch-Pagan", het_breuschpagan(resid, Xh)),
    ("White", het_white(resid, Xh)),
]:
    stat, p, _, _ = hasil
    print(f"{nama:15s} stat = {stat:8.3f}   p-value = {p:.4f}")

# Glejser: regresikan |residual| pada X, lihat apakah ada X yang signifikan
hunian["abs_resid"] = np.abs(resid)
glejser = smf.ols("abs_resid ~ luas + kamar + lokasi", data=hunian).fit()
print(glejser.summary())

# %% [markdown]
# ### Penanganan: robust standard error
#
# Cara paling praktis: tetap pakai OLS, tapi ganti standard error dengan
# versi robust (White). Di EViews ini opsi *White* di tab Options. Di
# statsmodels: `cov_type="HC3"`.

# %%
model_h_robust = smf.ols("harga ~ luas + kamar + lokasi",
                         data=hunian).fit(cov_type="HC3")

banding = pd.DataFrame({
    "koefisien": model_h.params,
    "SE_biasa": model_h.bse,
    "p_biasa": model_h.pvalues,
    "SE_robust": model_h_robust.bse,
    "p_robust": model_h_robust.pvalues,
})
banding

# %% [markdown]
# Koefisien tidak berubah, yang berubah hanya standard error dan p-value.
# Setelah ini, inferensi memakai kolom robust. Catat juga: kalau kesimpulan
# signifikansi berubah karena robust SE, itu temuan yang layak dilaporkan,
# bukan sesuatu yang disembunyikan.

# %% [markdown]
# ## 5. Uji normalitas residual
#
# Normalitas residual dibutuhkan untuk inferensi pada sampel kecil. Data
# `latihan-normalitas-1.csv`: harga saham dijelaskan suku bunga, tingkat
# pengangguran, dan pertumbuhan PDB.

# %%
saham_makro = pd.read_csv("data/latihan-normalitas-1.csv").rename(columns={
    "Harga_Saham": "harga_saham", "Tingkat_Suku_Bunga": "suku_bunga",
    "Tingkat_Pengangguran": "pengangguran", "Pertumbuhan_PDB": "pdb"})
model_n = smf.ols("harga_saham ~ suku_bunga + pengangguran + pdb",
                  data=saham_makro).fit()

from statsmodels.stats.stattools import jarque_bera
jb, p_jb, skew, kurt = jarque_bera(model_n.resid)
print(f"Jarque-Bera = {jb:.3f}")
print(f"p-value     = {p_jb:.4f}")
print(f"Skewness    = {skew:.3f}, Kurtosis = {kurt:.3f}")

# %%
fig, axes = plt.subplots(1, 2, figsize=(11, 4))
sns.histplot(model_n.resid, kde=True, ax=axes[0], color="#2F5D50")
axes[0].set_title("Histogram residual")
sm.qqplot(model_n.resid, line="s", ax=axes[1])
axes[1].set_title("Q-Q plot")
plt.tight_layout()
plt.show()

# %% [markdown]
# Aturan keputusan: p-value JB di bawah 0,05 = residual tidak normal.
# Yang perlu diperiksa kalau normalitas ditolak: outlier, data ekstrem,
# atau salah spesifikasi model. Dengan n di atas 30, penyimpangan ringan
# biasanya tidak fatal berkat teorema limit pusat. Sebutkan ini supaya
# mahasiswa tidak panik dan langsung membuang data begitu JB signifikan.

# %% [markdown]
# ## 6. Uji autokorelasi
#
# Autokorelasi = residual periode ini berkorelasi dengan residual periode
# sebelumnya. Kasus ini khas data deret waktu. Model OLS masih tak bias,
# tapi standard error salah dan p-value terlalu optimistis.
#
# Kita pakai `latihan-dummy-2.csv` (data tahunan PDB dan investasi). Dua
# variabel yang sama-sama bergerak sepanjang waktu sering menghasilkan
# residual berautokorelasi.

# %%
from statsmodels.stats.stattools import durbin_watson
from statsmodels.stats.diagnostic import acorr_breusch_godfrey

# Uji autokorelasi memakai model yang sama seperti bagian 2,
# di sini difokuskan ke diagnostik residualnya
model_ar = model_krisis
dw = durbin_watson(model_ar.resid)
bg_stat, bg_p, _, _ = acorr_breusch_godfrey(model_ar, nlags=2)

print(f"Durbin-Watson          = {dw:.3f}")
print(f"Breusch-Godfrey p-value = {bg_p:.4f}")

# %% [markdown]
# Panduan kasar DW: mendekati 2 = aman, di bawah 1,5 = indikasi
# autokorelasi positif, di atas 2,5 = autokorelasi negatif. Breusch-Godfrey
# lebih fleksibel karena bisa menguji lag berapa saja.
#
# Di data ini buktinya campuran: DW menunjukkan sinyal autokorelasi positif,
# tapi Breusch-Godfrey tidak menolak pada taraf 5%. Situasi campuran seperti
# ini wajar pada 30 observasi tahunan. Untuk data deret waktu, memakai HAC standard
# error adalah asuransi yang murah, dan di bawah terlihat p-value `krisis`
# berubah cukup banyak setelah koreksi.
#
# Penanganan praktis: Newey-West standard error (HAC). Di EViews: tab
# Options > Newey-West. Di statsmodels: `cov_type="HAC"`.

# %%
# Fit ulang model yang sama, kali ini dengan HAC standard error
model_ar_nw = smf.ols("pdb ~ investasi + suku_bunga + krisis",
                      data=krisis).fit(cov_type="HAC",
                                       cov_kwds={"maxlags": 2})
banding_ar = pd.DataFrame({
    "koefisien": model_ar.params,
    "SE_biasa": model_ar.bse,
    "p_biasa": model_ar.pvalues,
    "SE_HAC": model_ar_nw.bse,
    "p_HAC": model_ar_nw.pvalues,
})
banding_ar

# %% [markdown]
# ## 7. Alur keputusan diagnostik
#
# Ringkasnya, ini yang dilakukan saat memeriksa model:
#
# | Masalah | Deteksi | Penanganan cepat |
# |---|---|---|
# | Multikolinearitas | VIF > 10 | buang/gabung variabel, tambah sampel |
# | Heteroskedastisitas | BP/White/Glejser p < 0,05 | robust SE `HC3` |
# | Non-normalitas | JB p < 0,05 | cek outlier, transformasi; n besar relatif aman |
# | Autokorelasi | DW jauh dari 2, BG p < 0,05 | Newey-West `HAC` |
#
# Urutan pengujian yang dipakai di materi kuliah: multikolinearitas dulu
# (karena menentukan variabel mana yang dipakai), lalu heteroskedastisitas,
# normalitas, dan autokorelasi.

# %% [markdown]
# ## Latihan
#
# 1. Multikolinearitas kasus kedua: `latihan-multikolinieritas-2.csv`
#    (`konsumsi ~ pendapatan + kekayaan + jml_anggota`). Hitung VIF, buang
#    satu variabel dengan VIF tertinggi, lalu hitung VIF sisanya. Kalau
#    dua variabel bersaing, pertahankan yang paling relevan secara teori.
#    Bandingkan koefisien sebelum dan sesudah pembuangan.
# 2. Heteroskedastisitas kasus kedua: `hetero-2.csv`
#    (`pendapatan ~ pendidikan + pengalaman + usia`). Jalankan uji
#    Breusch-Pagan dan White, lalu bandingkan p-value biasa dan robust.
# 3. Kasus `hetero-1.csv` (`penjualan ~ iklan + salesperson + diskon`)
#    melatih melaporkan hipotesis yang ditolak: uji Breusch-Pagan dan
#    White di data itu tidak menolak homoskedastis, jadi dugaan "variasi
#    penjualan membesar saat iklan tinggi" tidak didukung data. Tulis
#    kesimpulan apa adanya, jangan paksakan narasi.
# 4. Normalitas kasus ketiga: `latihan-normalitas-3.csv`
#    (`harga ~ luas_bangunan + jumlah_kamar + usia_rumah`). Tampilkan
#    histogram residual dan uji Jarque-Bera.

# %% [markdown]
# ### Selanjutnya
#
# Selanjutnya: Sesi 4 mengganti jenis variabel Y dari kontinu ke
# kategorikal.
