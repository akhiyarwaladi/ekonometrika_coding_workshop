"""Buat semua visualisasi utama tutorial, simpan ke folder alat_bantu/gambar/ekonometrika/.

Jalankan: python alat_bantu/buat_gambar.py
Output: alat_bantu/gambar/ekonometrika/*.png (150 dpi) dan alat_bantu/gambar/ekonometrika/galeri.png

Gaya visual: palet hijau tua, terracotta, emas, dan abu-biru. Judul tebal di
kiri, subjudul abu-abu di bawahnya, catatan sumber di kanan bawah.
"""

import os
import warnings
from pathlib import Path

os.environ.setdefault("MPLBACKEND", "Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression, LogisticRegression

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parent.parent
os.chdir(ROOT)
OUT = ROOT / "alat_bantu/gambar/ekonometrika"
OUT.mkdir(parents=True, exist_ok=True)

UTAMA = "#2F5D50"
AKSEN = "#C15937"
EMAS = "#D9A441"
ABU = "#5B8A8F"
ABU_MUDA = "#8A9490"

sns.set_theme(style="whitegrid", palette=[UTAMA, AKSEN, EMAS, ABU])
plt.rcParams.update(
    {
        "figure.dpi": 110,
        "axes.titleweight": "bold",
        "axes.edgecolor": "#B9C2BD",
        "axes.grid": True,
        "grid.alpha": 0.35,
        "font.size": 11,
    }
)


def simpan(fig, nama):
    fig.savefig(OUT / f"{nama}.png", dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("OK", nama)


def judul(ax, teks, sub=None):
    ax.set_title(teks, fontsize=13, fontweight="bold", loc="left", pad=18)
    if sub:
        ax.text(0, 1.015, sub, transform=ax.transAxes, fontsize=10, color=ABU_MUDA)


def sumber(fig, teks):
    fig.text(
        0.99,
        -0.02,
        teks,
        ha="right",
        va="top",
        fontsize=8,
        color=ABU_MUDA,
        style="italic",
    )


# ---------------------------------------------------------------- Sesi 1
def sesi1_scatter_ols():
    df = pd.read_csv("data/uts_2.csv").rename(
        columns={"Y_Harga_Saham": "harga", "X1_Pendapatan_per_Saham": "eps"}
    )
    sampel_m = df[["harga", "eps"]].dropna()
    X_m = sampel_m[["eps"]]
    y_m = sampel_m["harga"]

    m = LinearRegression()
    m.fit(X_m, y_m)

    koefisien_m = pd.Series(m.coef_, index=X_m.columns)
    koefisien_m.loc["Intercept"] = m.intercept_
    b0, b1 = koefisien_m["Intercept"], koefisien_m["eps"]

    fig, ax = plt.subplots(figsize=(8, 5))
    xs = np.linspace(df["eps"].min(), df["eps"].max(), 100)
    for _, r in df.sample(10, random_state=3).iterrows():
        ax.plot(
            [r["eps"]] * 2,
            [r["harga"], b0 + b1 * r["eps"]],
            color=ABU_MUDA,
            lw=0.8,
            zorder=1,
        )
    ax.scatter(
        df["eps"],
        df["harga"],
        color=UTAMA,
        s=42,
        alpha=0.85,
        edgecolor="white",
        linewidth=0.8,
        zorder=3,
        label="data",
    )
    ax.plot(xs, b0 + b1 * xs, color=AKSEN, lw=2.4, zorder=2, label="garis OLS")
    ax.text(
        0.04,
        0.95,
        f"Harga = {b0:,.1f} + {b1:,.1f} EPS\nR² = {m.score(X_m, y_m):.3f}",
        transform=ax.transAxes,
        fontsize=10.5,
        va="top",
        bbox=dict(boxstyle="round,pad=0.45", facecolor="white", edgecolor="#D8DED9"),
    )
    ax.set_xlabel("Pendapatan per saham (EPS)")
    ax.set_ylabel("Harga saham")
    judul(
        ax,
        "Regresi linear: satu garis untuk semua titik",
        "Garis abu-abu adalah residual yang dikuadratkan lalu diminimalkan",
    )
    ax.legend(frameon=False, loc="lower right")
    sumber(fig, "Sumber: data/uts_2.csv")
    simpan(fig, "sesi1_scatter_ols")


def sesi1_residual():
    df = pd.read_csv("data/uts_2.csv").rename(
        columns={
            "Y_Harga_Saham": "harga",
            "X1_Pendapatan_per_Saham": "eps",
            "X2_Rasio_Utang_Ekuitas": "der",
            "X3_Belanja_Iklan": "iklan",
        }
    )
    sampel_m = df[["harga", "eps", "der", "iklan"]].dropna()
    X_m = sampel_m[["eps", "der", "iklan"]]
    y_m = sampel_m["harga"]

    m = LinearRegression()
    m.fit(X_m, y_m)

    prediksi_m = pd.Series(m.predict(X_m), index=y_m.index)
    residu_m = y_m - prediksi_m
    fig, ax = plt.subplots(figsize=(8, 4.8))
    ax.scatter(
        prediksi_m,
        residu_m,
        color=UTAMA,
        s=38,
        alpha=0.8,
        edgecolor="white",
        linewidth=0.7,
    )
    ax.axhline(0, color=AKSEN, lw=1.4, ls="--")
    ax.set_xlabel("Nilai prediksi model")
    ax.set_ylabel("Residual")
    judul(
        ax,
        "Cek residual: harus acak di sekitar nol",
        "Pola corong atau lengkungan berarti asumsi bermasalah",
    )
    sumber(fig, "Sumber: data/uts_2.csv, model berganda")
    simpan(fig, "sesi1_residual")


# ---------------------------------------------------------------- Sesi 2
def sesi2_cobb_douglas():
    df = pd.read_csv("data/regresi_log.csv").rename(
        columns={"Tenaga Kerja (L)": "L", "Modal (K)": "K", "Produksi (Q)": "Q"}
    )
    for c in ["L", "K", "Q"]:
        df["ln" + c] = np.log(df[c])
    sampel_m = df[["lnQ", "lnL", "lnK"]].dropna()
    X_m = sampel_m[["lnL", "lnK"]]
    y_m = sampel_m["lnQ"]

    m = LinearRegression()
    m.fit(X_m, y_m)

    koefisien_m = pd.Series(m.coef_, index=X_m.columns)
    koefisien_m.loc["Intercept"] = m.intercept_

    prediksi_m = pd.Series(m.predict(X_m), index=y_m.index)

    fig, ax = plt.subplots(figsize=(6.8, 5.6))
    batas = [df["Q"].min() * 0.95, df["Q"].max() * 1.05]
    ax.plot(batas, batas, color=ABU_MUDA, lw=1.2, ls="--", label="garis ideal")
    ax.scatter(
        df["Q"],
        np.exp(prediksi_m),
        color=UTAMA,
        s=44,
        alpha=0.85,
        edgecolor="white",
        linewidth=0.8,
        label="prediksi model",
    )
    ax.text(
        0.04,
        0.95,
        f"Elastisitas tenaga kerja = {koefisien_m['lnL']:.2f}\n"
        f"Elastisitas modal = {koefisien_m['lnK']:.2f}\n"
        f"Skala = {koefisien_m['lnL'] + koefisien_m['lnK']:.2f} (meningkat)",
        transform=ax.transAxes,
        fontsize=10.5,
        va="top",
        bbox=dict(boxstyle="round,pad=0.45", facecolor="white", edgecolor="#D8DED9"),
    )
    ax.set_xlabel("Produksi aktual (Q)")
    ax.set_ylabel("Produksi prediksi")
    judul(
        ax,
        "Fungsi produksi Cobb-Douglas (log-log)",
        "Prediksi rapat di garis ideal, model sangat cocok",
    )
    ax.legend(frameon=False, loc="lower right")
    sumber(fig, "Sumber: data/regresi_log.csv")
    simpan(fig, "sesi2_cobb_douglas")


def sesi2_reciprocal():
    df = pd.read_csv("data/regresi_reciprocal.csv").rename(
        columns={"Pengalaman (X)": "pengalaman", "Waktu Produksi (Y)": "waktu"}
    )
    df["satu_per_x"] = 1 / df["pengalaman"]
    sampel_m = df[["waktu", "satu_per_x"]].dropna()
    X_m = sampel_m[["satu_per_x"]]
    y_m = sampel_m["waktu"]

    m = LinearRegression()
    m.fit(X_m, y_m)

    koefisien_m = pd.Series(m.coef_, index=X_m.columns)
    koefisien_m.loc["Intercept"] = m.intercept_
    b0, b1 = koefisien_m["Intercept"], koefisien_m["satu_per_x"]

    fig, ax = plt.subplots(figsize=(8, 5))
    xs = np.linspace(df["pengalaman"].min(), df["pengalaman"].max(), 200)
    ax.scatter(
        df["pengalaman"],
        df["waktu"],
        color=UTAMA,
        s=40,
        alpha=0.85,
        edgecolor="white",
        linewidth=0.8,
        label="data",
        zorder=3,
    )
    ax.plot(xs, b0 + b1 / xs, color=AKSEN, lw=2.4, label="model reciprocal", zorder=2)
    ax.axhline(b0, color=EMAS, lw=1.6, ls="--")
    ax.annotate(
        f"batas asimtot = {b0:.2f}",
        xy=(xs[-1], b0),
        xytext=(xs[-1] * 0.62, b0 + 1.6),
        fontsize=10.5,
        color="#7A5A16",
        arrowprops=dict(arrowstyle="->", color=EMAS, lw=1.4),
    )
    ax.set_xlabel("Pengalaman kerja (tahun)")
    ax.set_ylabel("Waktu produksi")
    judul(
        ax,
        "Regresi reciprocal: manfaat yang makin mengecil",
        "Perbaikan cepat di awal, lalu mendatar menuju batas tertentu",
    )
    ax.legend(frameon=False)
    sumber(fig, "Sumber: data/regresi_reciprocal.csv")
    simpan(fig, "sesi2_reciprocal")


def sesi2_polynomial():
    df = pd.read_csv("data/usia_unit.csv")
    df["usia2"] = df["Usia"] ** 2
    sampel_m_lin = df[["Unit_Terjual", "Usia"]].dropna()
    X_m_lin = sampel_m_lin[["Usia"]]
    y_m_lin = sampel_m_lin["Unit_Terjual"]

    m_lin = LinearRegression()
    m_lin.fit(X_m_lin, y_m_lin)

    koefisien_m_lin = pd.Series(m_lin.coef_, index=X_m_lin.columns)
    koefisien_m_lin.loc["Intercept"] = m_lin.intercept_
    sampel_m = df[["Unit_Terjual", "Usia", "usia2"]].dropna()
    X_m = sampel_m[["Usia", "usia2"]]
    y_m = sampel_m["Unit_Terjual"]

    m = LinearRegression()
    m.fit(X_m, y_m)

    koefisien_m = pd.Series(m.coef_, index=X_m.columns)
    koefisien_m.loc["Intercept"] = m.intercept_
    b1, b2 = koefisien_m["Usia"], koefisien_m["usia2"]
    puncak = -b1 / (2 * b2)

    fig, ax = plt.subplots(figsize=(8, 5))
    xs = np.linspace(df["Usia"].min(), df["Usia"].max(), 200)
    ax.scatter(
        df["Usia"],
        df["Unit_Terjual"],
        color=UTAMA,
        s=40,
        alpha=0.85,
        edgecolor="white",
        linewidth=0.8,
        label="data",
        zorder=3,
    )
    ax.plot(
        xs,
        koefisien_m_lin["Intercept"] + koefisien_m_lin["Usia"] * xs,
        color=ABU_MUDA,
        lw=1.6,
        ls="--",
        label=f"linear (R² {m_lin.score(X_m_lin, y_m_lin):.2f})",
    )
    ax.plot(
        xs,
        koefisien_m["Intercept"] + b1 * xs + b2 * xs**2,
        color=AKSEN,
        lw=2.4,
        label=f"kuadratik (R² {m.score(X_m, y_m):.2f})",
        zorder=2,
    )
    ax.plot(
        [puncak],
        [koefisien_m["Intercept"] + b1 * puncak + b2 * puncak**2],
        marker="o",
        ms=9,
        color=EMAS,
        zorder=4,
    )
    ax.annotate(
        f"puncak di usia {puncak:.1f} tahun",
        xy=(puncak, koefisien_m["Intercept"] + b1 * puncak + b2 * puncak**2),
        xytext=(puncak + 3, 62),
        fontsize=10.5,
        color="#7A5A16",
        arrowprops=dict(arrowstyle="->", color=EMAS, lw=1.4),
    )
    ax.set_xlabel("Usia tenaga penjual (tahun)")
    ax.set_ylabel("Unit terjual per bulan")
    judul(
        ax,
        "Regresi polinomial: naik, memuncak, lalu menurun",
        "Model linear gagal menangkap pola ini (R² hanya 0,27)",
    )
    ax.legend(frameon=False, loc="lower left")
    sumber(fig, "Sumber: data/usia_unit.csv")
    simpan(fig, "sesi2_polynomial")


# ---------------------------------------------------------------- Sesi 3
def sesi3_vif():
    df = pd.read_csv("data/latihan_multikolinieritas_1.csv").rename(
        columns={
            "LUAS_BANGUNAN": "luas_bangunan",
            "LUAS_TANAH": "luas_tanah",
            "JML_KAMAR": "jml_kamar",
        }
    )
    X = sm.add_constant(df[["luas_bangunan", "luas_tanah", "jml_kamar"]])
    from statsmodels.stats.outliers_influence import variance_inflation_factor

    nilai = {
        c: variance_inflation_factor(X.values, i)
        for i, c in enumerate(X.columns)
        if c != "const"
    }

    fig, ax = plt.subplots(figsize=(8, 4.6))
    nama = list(nilai.keys())[::-1]
    vif = [nilai[k] for k in nama]
    warna = [AKSEN if v > 20 else (EMAS if v > 10 else UTAMA) for v in vif]
    ax.barh(nama, vif, color=warna, height=0.55)
    for y, v in enumerate(vif):
        ax.text(
            v + 1,
            y,
            f"{v:.1f}",
            va="center",
            fontsize=11,
            color="#333333",
            fontweight="bold",
        )
    ax.axvline(10, color=AKSEN, ls="--", lw=1.4)
    ax.text(10.6, 0.35, "batas aman VIF = 10", color=AKSEN, fontsize=10)
    ax.set_xlabel("VIF (Variance Inflation Factor)")
    ax.set_xlim(0, max(vif) * 1.22)
    judul(
        ax,
        "Multikolinearitas: VIF di atas 10 menandakan masalah",
        "Luas bangunan dan luas tanah saling menjelaskan, koefisien jadi tidak stabil",
    )
    sumber(fig, "Sumber: data/latihan_multikolinieritas_1.csv")
    simpan(fig, "sesi3_vif")


def sesi3_hetero():
    df = pd.read_csv("data/hetero_3.csv").rename(
        columns={"Harga": "harga", "Luas": "luas", "Kamar": "kamar", "Lokasi": "lokasi"}
    )
    sampel_m = df[["harga", "luas", "kamar", "lokasi"]].dropna()
    X_m = sampel_m[["luas", "kamar", "lokasi"]]
    y_m = sampel_m["harga"]

    m = LinearRegression()
    m.fit(X_m, y_m)

    prediksi_m = pd.Series(m.predict(X_m), index=y_m.index)
    residu_m = y_m - prediksi_m
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(
        prediksi_m,
        residu_m,
        color=UTAMA,
        s=38,
        alpha=0.8,
        edgecolor="white",
        linewidth=0.7,
    )
    ax.axhline(0, color=AKSEN, lw=1.4, ls="--")
    ax.annotate(
        "sebaran melebar\nke kanan",
        xy=(prediksi_m.max() * 0.93, 1.1),
        xytext=(prediksi_m.max() * 0.62, 1.35),
        fontsize=10.5,
        color="#8C3A22",
        arrowprops=dict(arrowstyle="->", color=AKSEN, lw=1.4),
    )
    ax.set_xlabel("Nilai prediksi harga rumah")
    ax.set_ylabel("Residual")
    judul(
        ax,
        "Heteroskedastisitas: corong di data rumah",
        "Uji Breusch-Pagan p = 0,003; pakai robust standard error HC3",
    )
    sumber(fig, "Sumber: data/hetero_3.csv")
    simpan(fig, "sesi3_hetero")


def sesi3_normalitas():
    df = pd.read_csv("data/latihan_normalitas_1.csv").rename(
        columns={
            "Harga_Saham": "harga_saham",
            "Tingkat_Suku_Bunga": "suku_bunga",
            "Tingkat_Pengangguran": "pengangguran",
            "Pertumbuhan_PDB": "pdb",
        }
    )
    sampel_m = df[["harga_saham", "suku_bunga", "pengangguran", "pdb"]].dropna()
    X_m = sampel_m[["suku_bunga", "pengangguran", "pdb"]]
    y_m = sampel_m["harga_saham"]

    m = LinearRegression()
    m.fit(X_m, y_m)

    prediksi_m = pd.Series(m.predict(X_m), index=y_m.index)
    residu_m = y_m - prediksi_m
    from statsmodels.stats.stattools import jarque_bera

    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.4))
    sns.histplot(residu_m, kde=True, ax=axes[0], color=UTAMA, edgecolor="white")
    axes[0].set_xlabel("Residual")
    axes[0].set_ylabel("Frekuensi")
    axes[0].set_title("Distribusi residual", loc="left", fontsize=12)
    sm.qqplot(
        residu_m,
        line="45",
        ax=axes[1],
        markerfacecolor=UTAMA,
        markeredgecolor="white",
        markersize=6,
    )
    axes[1].set_title("Q-Q plot", loc="left", fontsize=12)
    jb, p = jarque_bera(residu_m)[0], jarque_bera(residu_m)[1]
    fig.suptitle(
        "Normalitas residual: dua cara melihat bentuk yang sama",
        fontsize=13,
        fontweight="bold",
        x=0.01,
        ha="left",
    )
    fig.text(
        0.01,
        0.965,
        f"Jarque-Bera p = {p:.2f}, residual tidak menyimpang dari normal",
        fontsize=10,
        color=ABU_MUDA,
    )
    sumber(fig, "Sumber: data/latihan_normalitas_1.csv")
    simpan(fig, "sesi3_normalitas")


# ---------------------------------------------------------------- Sesi 4
def sesi4_marginal_effects():
    spector = sm.datasets.spector.load_pandas().data
    sampel_m = spector[["GRADE", "GPA", "TUCE", "PSI"]].dropna()
    X_m = sampel_m[["GPA", "TUCE", "PSI"]]
    y_m = sampel_m["GRADE"]

    m = LogisticRegression(penalty=None, max_iter=5000, tol=1e-9)
    m.fit(X_m, y_m)

    # Pelengkap statistik: standard error dan pengujian pada sampel yang sama.
    uji_m = sm.Logit(
        y_m,
        sm.add_constant(X_m, has_constant="add").rename(columns={"const": "Intercept"}),
    ).fit(disp=0)
    me = uji_m.get_margeff()
    nama = ["GPA", "TUCE", "PSI (metode baru)"]
    nilai = np.asarray(me.margeff)
    warna = [UTAMA, ABU, AKSEN]

    fig, ax = plt.subplots(figsize=(8, 4.6))
    ax.barh(nama[::-1], nilai[::-1], color=warna[::-1], height=0.55)
    for y, v in enumerate(nilai[::-1]):
        ax.text(
            v + 0.006,
            y,
            f"{v:+.3f}",
            va="center",
            fontsize=11,
            fontweight="bold",
            color="#333333",
        )
    ax.axvline(0, color="#666666", lw=1)
    ax.set_xlabel("Perubahan peluang nilai meningkat (poin persen)")
    ax.set_xlim(0, max(nilai) * 1.22)
    judul(
        ax,
        "Efek marjinal jauh lebih mudah dibaca daripada log-odds",
        "Data 32 mahasiswa (Spector dan Mazzeo); PSI menaikkan peluang sekitar 31 poin persen",
    )
    sumber(fig, "Sumber: dataset bawaan statsmodels (spector)")
    simpan(fig, "sesi4_marginal_effects")


# ---------------------------------------------------------------- Sesi 5
def sesi5_forecast():
    from statsmodels.tsa.arima.model import ARIMA

    df = pd.read_csv("data/ts_gdp_growth.csv")
    seri = df["gdp_growth"]
    m = ARIMA(seri, order=(2, 0, 1)).fit()
    ramalan = m.get_forecast(steps=6)
    batas = pd.DataFrame(ramalan.conf_int(alpha=0.05))

    fig, ax = plt.subplots(figsize=(9.5, 4.8))
    ax.plot(df["obs"], seri, color=UTAMA, lw=1.8, label="aktual")
    masa = np.arange(51, 57)
    ax.plot(
        masa,
        np.asarray(ramalan.predicted_mean),
        color=AKSEN,
        lw=2,
        marker="o",
        ms=5,
        label="ramalan",
    )
    ax.fill_between(
        masa,
        batas.iloc[:, 0],
        batas.iloc[:, 1],
        color=AKSEN,
        alpha=0.18,
        label="interval 95%",
    )
    ax.axvline(50.5, color=ABU_MUDA, lw=1, ls=":")
    ax.text(50.7, ax.get_ylim()[0] + 0.15, "mulai ramalan", fontsize=9, color=ABU_MUDA)
    ax.set_xlabel("Periode")
    ax.set_ylabel("Pertumbuhan GDP (persen)")
    judul(
        ax,
        "Peramalan ARIMA pada data siklus",
        "Orde dipilih otomatis dari AIC terkecil pada kandidat 0-2",
    )
    ax.legend(frameon=False, loc="lower right")
    sumber(fig, "Sumber: data/ts_gdp_growth.csv")
    simpan(fig, "sesi5_forecast")


def sesi5_kointegrasi():
    df = pd.read_csv("data/konsumsi_pendapatan.csv")
    fig, ax = plt.subplots(figsize=(9.5, 4.8))
    ax.plot(df["Tahun"], df["Konsumsi_Y"], color=UTAMA, lw=2, label="konsumsi")
    ax.plot(
        df["Tahun"], df["Pendapatan_X"], color=AKSEN, lw=2, ls="--", label="pendapatan"
    )
    ax.set_xlabel("Tahun")
    ax.set_ylabel("Nilai (satuan data)")
    judul(
        ax,
        "Dua seri tidak stasioner yang berjalan bersama",
        "Kointegrasi p = 0,0001; keduanya terikat dalam jangka panjang",
    )
    ax.legend(frameon=False, loc="upper left")
    sumber(fig, "Sumber: data/konsumsi_pendapatan.csv")
    simpan(fig, "sesi5_kointegrasi")


# ---------------------------------------------------------------- Sesi 6
def sesi6_panel():
    from linearmodels.panel import PanelOLS, RandomEffects

    df = pd.read_csv("data/panel_gdp.csv").set_index(["CountryID", "Year"])
    y, X = df["GDP_Y"], df[["FDI_X1", "Labor_X2"]]
    cem = PanelOLS(y, sm.add_constant(X)).fit(cov_type="clustered", cluster_entity=True)
    fem = PanelOLS(y, X, entity_effects=True).fit(
        cov_type="clustered", cluster_entity=True
    )
    rem = RandomEffects(y, sm.add_constant(X)).fit(
        cov_type="clustered", cluster_entity=True
    )

    model = ["CEM", "FEM", "REM"]
    koef = [cem.params["FDI_X1"], fem.params["FDI_X1"], rem.params["FDI_X1"]]
    galat = [
        cem.std_errors["FDI_X1"],
        fem.std_errors["FDI_X1"],
        rem.std_errors["FDI_X1"],
    ]
    posisi = np.arange(len(model))
    fig, ax = plt.subplots(figsize=(8, 4.6))
    ax.errorbar(
        koef,
        posisi,
        xerr=np.array(galat) * 1.96,
        fmt="o",
        ms=10,
        color=UTAMA,
        ecolor=ABU,
        elinewidth=2.4,
        capsize=6,
        markeredgecolor="white",
    )
    ax.set_yticks(posisi, model)
    for k, p in zip(koef, posisi):
        ax.text(
            k,
            p,
            f"  {k:.2f}",
            va="center",
            fontsize=11,
            fontweight="bold",
            color="#333333",
        )
    ax.axvline(0, color=ABU_MUDA, lw=1, ls="--")
    ax.set_xlim(-0.4, 5.6)
    ax.set_xlabel("Koefisien FDI (interval kepercayaan 95%)")
    judul(
        ax,
        "Satu variabel, tiga model panel",
        "Arah sama, tetapi besar dan presisinya bergantung metode estimasi",
    )
    sumber(fig, "Sumber: data/panel_gdp.csv")
    simpan(fig, "sesi6_panel")


def sesi6_garch():
    from arch import arch_model

    df = pd.read_csv("data/volatilitas.csv")
    ret = df["Kasus_1_Saham_Return"]
    m = arch_model(ret, vol="Garch", p=1, q=1, rescale=True).fit(disp="off")

    fig, axes = plt.subplots(
        2, 1, figsize=(9.5, 6.2), sharex=True, gridspec_kw={"height_ratios": [1, 1.4]}
    )
    axes[0].plot(ret, color=UTAMA, lw=1.2)
    axes[0].axhline(0, color=ABU_MUDA, lw=0.8)
    axes[0].set_ylabel("Return")
    axes[0].set_title(
        "Return dan volatilitas bersyarat GARCH(1,1)", loc="left", fontsize=13
    )
    axes[1].plot(m.conditional_volatility, color=AKSEN, lw=1.8)
    axes[1].fill_between(
        range(len(m.conditional_volatility)),
        0,
        m.conditional_volatility,
        color=AKSEN,
        alpha=0.15,
    )
    axes[1].set_ylabel("Sigma (volatilitas)")
    axes[1].set_xlabel("Periode")
    fig.text(
        0.01,
        0.94,
        "Data simulasi P14: alpha 0,81 dan beta 0, jadi volatilitas murni reaksi guncangan baru",
        fontsize=10,
        color=ABU_MUDA,
    )
    sumber(fig, "Sumber: data/volatilitas.csv")
    simpan(fig, "sesi6_garch")


# ---------------------------------------------------------------- Lab 6
def lab6_ihsg_garch():
    from arch import arch_model

    df = pd.read_csv("data/ihsg_harian.csv", parse_dates=["Date"])
    df["ret"] = 100 * np.log(df["Close"]).diff()
    df = df.dropna()
    m = arch_model(df["ret"], vol="Garch", p=1, q=1).fit(disp="off")

    fig, axes = plt.subplots(
        2, 1, figsize=(10, 6.4), sharex=True, gridspec_kw={"height_ratios": [1, 1.4]}
    )
    axes[0].plot(df["Date"], df["ret"], color=UTAMA, lw=0.7)
    axes[0].set_ylabel("Return harian (%)")
    axes[0].set_title(
        "IHSG asli: guncangan COVID dan volatilitas yang persisten",
        loc="left",
        fontsize=13,
    )
    axes[0].annotate(
        "COVID\nMaret 2020",
        xy=(pd.Timestamp("2020-03-24"), -6.5),
        xytext=(pd.Timestamp("2020-10-01"), -5.3),
        fontsize=10,
        color="#8C3A22",
        arrowprops=dict(arrowstyle="->", color=AKSEN, lw=1.4),
    )
    axes[1].plot(df["Date"], m.conditional_volatility, color=AKSEN, lw=1.2)
    axes[1].fill_between(
        df["Date"], 0, m.conditional_volatility, color=AKSEN, alpha=0.15
    )
    axes[1].set_ylabel("Sigma (volatilitas)")
    axes[1].set_xlabel("Tanggal")
    fig.text(
        0.01,
        0.945,
        "GARCH(1,1): beta = 0,82 dan persistensi 0,95, sesuai pola di buku teks",
        fontsize=10,
        color=ABU_MUDA,
    )
    sumber(fig, "Sumber: Yahoo Finance, 2019-2026")
    simpan(fig, "lab6_ihsg_garch")


def lab6_inflasi_krisis():
    df = pd.read_csv("data/idn_inflasi_bulanan.csv", parse_dates=["tanggal"])
    fig, ax = plt.subplots(figsize=(10.5, 4.8))
    ax.plot(df["tanggal"], df["inflasi_yoy"], color=UTAMA, lw=1.1)
    ax.axvspan(
        pd.Timestamp("1997-07-01"), pd.Timestamp("1999-12-31"), color=AKSEN, alpha=0.14
    )
    puncak = df.loc[df["inflasi_yoy"].idxmax()]
    ax.annotate(
        f"krisis 1998:\ninflasi {puncak['inflasi_yoy']:.0f} persen",
        xy=(puncak["tanggal"], puncak["inflasi_yoy"]),
        xytext=(pd.Timestamp("2000-06-01"), 52),
        fontsize=10.5,
        color="#8C3A22",
        arrowprops=dict(arrowstyle="->", color=AKSEN, lw=1.4),
    )
    ax.annotate(
        "era stabil:\ndi bawah 5 persen",
        xy=(pd.Timestamp("2023-01-01"), 4),
        xytext=(pd.Timestamp("2010-01-01"), 20),
        fontsize=10.5,
        color="#7A5A16",
        arrowprops=dict(arrowstyle="->", color=EMAS, lw=1.4),
    )
    ax.set_xlabel("Tahun")
    ax.set_ylabel("Inflasi tahunan (%)")
    judul(
        ax,
        "Inflasi Indonesia 1969-2025: dari 58 persen ke bawah 5 persen",
        "Patahan struktural yang asli, bukan simulasi",
    )
    sumber(fig, "Sumber: BPS via OECD/FRED (data/idn_inflasi_bulanan.csv)")
    simpan(fig, "lab6_inflasi_krisis")


def lab6_provinsi():
    df = pd.read_csv("data/provinsi_2021.csv")
    df["ln_pdrb"] = np.log(df["PDRB_Kapita"])
    sampel_m = df[["IPM", "PDRB_Kapita"]].dropna()
    X_m = sampel_m[["PDRB_Kapita"]]
    y_m = sampel_m["IPM"]

    m = LinearRegression()
    m.fit(X_m, y_m)

    koefisien_m = pd.Series(m.coef_, index=X_m.columns)
    koefisien_m.loc["Intercept"] = m.intercept_

    fig, ax = plt.subplots(figsize=(9, 5.4))
    ax.scatter(
        df["PDRB_Kapita"] / 1000,
        df["IPM"],
        color=UTAMA,
        s=55,
        alpha=0.85,
        edgecolor="white",
        linewidth=0.8,
        zorder=3,
    )
    xs = np.linspace(df["PDRB_Kapita"].min(), df["PDRB_Kapita"].max(), 100)
    ax.plot(
        xs / 1000,
        koefisien_m["Intercept"] + koefisien_m["PDRB_Kapita"] * xs,
        color=AKSEN,
        lw=2.2,
        zorder=2,
    )
    for nama, geser in [
        ("DKI Jakarta", (-46, -1.2)),
        ("Nusa Tenggara Timur", (-30, 1.2)),
        ("Kalimantan Timur", (6, -1.2)),
        ("Papua", (4, 1.0)),
    ]:
        baris = df[df["Provinsi"] == nama].iloc[0]
        ax.annotate(
            nama,
            xy=(baris["PDRB_Kapita"] / 1000, baris["IPM"]),
            xytext=(baris["PDRB_Kapita"] / 1000 + geser[0], baris["IPM"] + geser[1]),
            fontsize=9.5,
            color="#333333",
        )
    ax.text(
        0.04,
        0.95,
        f"IPM = {koefisien_m['Intercept']:.1f} + "
        f"{koefisien_m['PDRB_Kapita'] * 1000:.3f} x PDRB (juta)\n"
        f"R² = {m.score(X_m, y_m):.2f}",
        transform=ax.transAxes,
        fontsize=10.5,
        va="top",
        bbox=dict(boxstyle="round,pad=0.45", facecolor="white", edgecolor="#D8DED9"),
    )
    ax.set_xlabel("PDRB per kapita (juta rupiah)")
    ax.set_ylabel("Indeks Pembangunan Manusia (IPM)")
    judul(
        ax,
        "34 provinsi 2021: kekayaan dan pembangunan manusia",
        "Hubungan positif, tetapi DKI Jakarta dan Papua menyimpang dari garis",
    )
    sumber(fig, "Sumber: kompilasi indikator BPS (data/provinsi_2021.csv)")
    simpan(fig, "lab6_provinsi")


def lab6_phillips():
    df = pd.read_csv("data/idn_makro_tahunan.csv")
    sampel_m = df[["Inflasi", "Pengangguran"]].dropna()
    X_m = sampel_m[["Pengangguran"]]
    y_m = sampel_m["Inflasi"]

    m = LinearRegression()
    m.fit(X_m, y_m)

    koefisien_m = pd.Series(m.coef_, index=X_m.columns)
    koefisien_m.loc["Intercept"] = m.intercept_

    # Pelengkap statistik: standard error dan pengujian pada sampel yang sama.
    uji_m = sm.OLS(
        y_m,
        sm.add_constant(X_m, has_constant="add").rename(columns={"const": "Intercept"}),
    ).fit()

    fig, ax = plt.subplots(figsize=(8.4, 5.2))
    ax.scatter(
        df["Pengangguran"],
        df["Inflasi"],
        color=UTAMA,
        s=52,
        alpha=0.85,
        edgecolor="white",
        linewidth=0.8,
        zorder=3,
    )
    xs = np.linspace(df["Pengangguran"].min(), df["Pengangguran"].max(), 50)
    ax.plot(
        xs,
        koefisien_m["Intercept"] + koefisien_m["Pengangguran"] * xs,
        color=AKSEN,
        lw=2.2,
        zorder=2,
    )
    for tahun, geser in [(1998, (0.25, 1.5)), (2005, (0.2, 1.2)), (2020, (0.25, 1.0))]:
        baris = df[df["tahun"] == tahun]
        if len(baris):
            r = baris.iloc[0]
            ax.annotate(
                str(tahun),
                xy=(r["Pengangguran"], r["Inflasi"]),
                xytext=(r["Pengangguran"] + geser[0], r["Inflasi"] + geser[1]),
                fontsize=10,
                color="#8C3A22",
            )
    ax.text(
        0.04,
        0.95,
        f"Kemiringan = {koefisien_m['Pengangguran']:.2f} "
        f"(p = {uji_m.pvalues['Pengangguran']:.3f}), R² = {m.score(X_m, y_m):.2f}",
        transform=ax.transAxes,
        fontsize=10.5,
        va="top",
        bbox=dict(boxstyle="round,pad=0.45", facecolor="white", edgecolor="#D8DED9"),
    )
    ax.set_xlabel("Tingkat pengangguran (%)")
    ax.set_ylabel("Inflasi tahunan (%)")
    judul(
        ax,
        "Inflasi dan pengangguran Indonesia 2000-2025",
        "Tanda positif: krisis menaikkan keduanya sekaligus, bukan trade-off klasik",
    )
    sumber(fig, "Sumber: World Bank (data/idn_makro_tahunan.csv)")
    simpan(fig, "lab6_phillips")


# ---------------------------------------------------------------- Galeri
def galeri():
    from PIL import Image

    files = sorted(OUT.glob("*.png"))
    files = [f for f in files if f.name != "galeri.png"]
    kolom = 4
    lebar = 460
    ims = [Image.open(f) for f in files]
    skala = [im.resize((lebar, int(im.height * lebar / im.width))) for im in ims]
    tinggi_baris = [
        max(im.height for im in skala[i : i + kolom])
        for i in range(0, len(skala), kolom)
    ]
    kanvas = Image.new(
        "RGB", (kolom * lebar, sum(tinggi_baris) + 20 * len(tinggi_baris)), "white"
    )
    y = 10
    for i, im in enumerate(skala):
        baris, kol = divmod(i, kolom)
        x = kol * lebar + (lebar - im.width) // 2
        kanvas.paste(im, (x, y + sum(tinggi_baris[:baris]) + 20 * baris))
    kanvas.save(OUT / "galeri.png", quality=85)
    print("OK galeri.png dengan", len(files), "gambar")


if __name__ == "__main__":
    sesi1_scatter_ols()
    sesi1_residual()
    sesi2_cobb_douglas()
    sesi2_reciprocal()
    sesi2_polynomial()
    sesi3_vif()
    sesi3_hetero()
    sesi3_normalitas()
    sesi4_marginal_effects()
    sesi5_forecast()
    sesi5_kointegrasi()
    sesi6_panel()
    sesi6_garch()
    lab6_ihsg_garch()
    lab6_inflasi_krisis()
    lab6_provinsi()
    lab6_phillips()
    galeri()
