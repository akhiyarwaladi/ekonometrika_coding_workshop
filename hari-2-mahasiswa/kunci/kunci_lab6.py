# %% [markdown]
# # Kunci Lab 6: Data Indonesia Asli

# %% [markdown]
# ## Persiapan

# %%
import zipfile
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

warnings.filterwarnings("ignore")

if not Path("data").exists() and Path("data-ekonometrika.zip").exists():
    zipfile.ZipFile("data-ekonometrika.zip").extractall(".")

print("File data siap:", len(list(Path("data").glob("*.csv"))))

# %% [markdown]
# ## Latihan 1: GARCH pada kurs USD/IDR

# %%
kurs = pd.read_csv("data/kurs-harian.csv", parse_dates=["Tanggal"])
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
panjang = pd.read_csv("data/ihsg-panjang.csv", parse_dates=["Date"])
panjang["ret"] = 100 * np.log(panjang["Close"]).diff()
panjang = panjang.dropna()
print("Observasi:", len(panjang), "rentang:",
      panjang["Date"].min().date(), "-", panjang["Date"].max().date())

for nama, potong in [("penuh 1990-2026", panjang),
                     ("1990-1999", panjang[panjang["Date"] < "2000"]),
                     ("2000-2026", panjang[panjang["Date"] >= "2000"]),
                     ("2019-2026", panjang[panjang["Date"] >= "2019"])]:
    g = arch_model(potong["ret"], vol="Garch", p=1, q=1).fit(disp="off")
    a = g.params["alpha[1]"]
    b = g.params["beta[1]"]
    print(f"{nama:16s} alpha={a:.4f} beta={b:.4f} persistensi={a + b:.4f} n={len(potong)}")

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
prov = pd.read_csv("data/provinsi-2021.csv")
prov["ln_pdrb"] = np.log(prov["PDRB_Kapita"])

model_kemiskinan = smf.ols("Kemiskinan ~ IPM", data=prov).fit()
print("Kemiskinan ~ IPM:")
print(model_kemiskinan.params.round(4))
print(model_kemiskinan.pvalues.round(4))
print("R2:", round(model_kemiskinan.rsquared, 4))

model_lin = smf.ols("IPM ~ PDRB_Kapita", data=prov).fit()
model_log = smf.ols("IPM ~ ln_pdrb", data=prov).fit()
print("\nIPM ~ PDRB (linear): R2 =", round(model_lin.rsquared, 4),
      "adj =", round(model_lin.rsquared_adj, 4))
print("IPM ~ ln(PDRB)     : R2 =", round(model_log.rsquared, 4),
      "adj =", round(model_log.rsquared_adj, 4))

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
from scipy.stats import chi2

panel = pd.read_csv("data/asean-panel.csv").set_index(["Negara", "Tahun"])
y = panel["PDB_Growth"]
X = panel[["FDI", "Inflasi"]]

fem = PanelOLS(y, X, entity_effects=True).fit(cov_type="clustered", cluster_entity=True)
rem = RandomEffects(y, sm.add_constant(X)).fit(cov_type="clustered", cluster_entity=True)
print("FEM:", fem.params.round(4).to_dict(), "p:", fem.pvalues.round(4).to_dict())
print("REM:", rem.params.round(4).to_dict(), "p:", rem.pvalues.round(4).to_dict())
print("Chow p:", f"{fem.f_pooled.pval:.4g}")

nama_sama = [v for v in fem.params.index if v in rem.params.index]
beda = fem.params[nama_sama] - rem.params[nama_sama]
selisih_cov = fem.cov.loc[nama_sama, nama_sama] - rem.cov.loc[nama_sama, nama_sama]
# Statistik Hausman: selisih koefisien dibobot selisih kovariansnya
stat_h = float(beda.values @ np.linalg.pinv(selisih_cov.values) @ beda.values)
print("Hausman p:", round(chi2.sf(stat_h, len(nama_sama)), 4))

# %% [markdown]
# Kesimpulan: dengan FDI dan Inflasi, Hausman menghasilkan p = 1,0,
# sehingga REM tidak tertolak. Namun tidak ada koefisien yang signifikan.
# Bandingkan dengan spesifikasi utama (FDI + ln angkatan kerja) yang
# memilih FEM dengan tegas dan signifikan. Pelajaran: hasil pemilihan
# model bisa berubah ketika spesifikasi berubah, jadi kedua-duanya layak
# dilaporkan dan dibahas, bukan dipilih yang paling enak saja.

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
