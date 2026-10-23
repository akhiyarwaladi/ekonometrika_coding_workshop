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
