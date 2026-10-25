"""Ambil data Indonesia asli dari sumber terbuka, simpan ke folder data/.

Sumber:
1. World Bank API (tanpa kunci): makro Indonesia tahunan dan panel ASEAN.
2. Yahoo Finance via yfinance: IHSG harian (^JKSE).
3. Frankfurter API (ECB, tanpa kunci): kurs USD/IDR harian.

Jalankan: python alat_bantu/unduh_data_indonesia.py
Catatan: butuh internet saat menjalankan. File CSV hasil unduhan sudah
disertakan di folder data/, jadi notebook tidak perlu menjalankan script ini.
"""

import io
import zipfile
from pathlib import Path

import pandas as pd
import requests

DATA = Path(__file__).resolve().parent.parent / "data"

NEGARA_ASEAN = "IDN;MYS;SGP;THA;PHL;VNM;KHM;LAO;MMR;BRN"
INDIKATOR = {
    "NY.GDP.MKTP.KD.ZG": "PDB_Growth",
    "FP.CPI.TOTL.ZG": "Inflasi",
    "SL.UEM.TOTL.ZS": "Pengangguran",
    "PA.NUS.FCRF": "Kurs_USD",
    "BX.KLT.DINV.WD.GD.ZS": "FDI",
    "SL.TLF.TOTL.IN": "Angkatan_Kerja",
}


def world_bank(negara, indikator_id, nama_kolom, tahun="2000:2025"):
    url = (
        f"https://api.worldbank.org/v2/country/{negara}/indicator/{indikator_id}"
        f"?format=json&per_page=2000&date={tahun}"
    )
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    data = resp.json()[1]
    df = pd.DataFrame(
        [
            {
                "negara": d["countryiso3code"],
                "tahun": int(d["date"]),
                nama_kolom: d["value"],
            }
            for d in data
            if d["value"] is not None
        ]
    )
    return df


def main():
    # 1. Makro Indonesia tahunan
    print("Mengunduh makro Indonesia dari World Bank...")
    makro = None
    for kode, nama in INDIKATOR.items():
        if kode == "BX.KLT.DINV.WD.GD.ZS":
            continue
        bagian = world_bank("IDN", kode, nama)
        makro = bagian if makro is None else makro.merge(bagian, on=["negara", "tahun"])
    makro = makro.sort_values("tahun").reset_index(drop=True)
    makro.to_csv(DATA / "idn_makro_tahunan.csv", index=False)
    print(
        f"  OK idn_makro_tahunan.csv: {len(makro)} baris, {makro['tahun'].min()}-{makro['tahun'].max()}"
    )

    # 2. Panel ASEAN
    print("Mengunduh panel ASEAN dari World Bank...")
    panel = None
    for kode, nama in INDIKATOR.items():
        bagian = world_bank(NEGARA_ASEAN, kode, nama)
        panel = bagian if panel is None else panel.merge(bagian, on=["negara", "tahun"])
    panel = panel.rename(columns={"negara": "Negara", "tahun": "Tahun"})
    panel = panel.sort_values(["Negara", "Tahun"]).reset_index(drop=True)
    panel.to_csv(DATA / "asean_panel.csv", index=False)
    print(
        f"  OK asean_panel.csv: {len(panel)} baris, {panel['Negara'].nunique()} negara"
    )

    # 3. IHSG harian
    print("Mengunduh IHSG harian dari Yahoo Finance...")
    try:
        import yfinance as yf

        ihsg = yf.download(
            "^JKSE",
            start="2019-01-01",
            end="2026-09-30",
            progress=False,
            auto_adjust=True,
        )
        if len(ihsg) == 0:
            raise RuntimeError("data kosong")
        if isinstance(ihsg.columns, pd.MultiIndex):
            ihsg.columns = ihsg.columns.get_level_values(0)
        ihsg = ihsg.reset_index()
        ihsg.to_csv(DATA / "ihsg_harian.csv", index=False)
        print(f"  OK ihsg_harian.csv: {len(ihsg)} baris, kolom {list(ihsg.columns)}")
    except Exception as e:
        print(f"  GAGAL IHSG: {type(e).__name__}: {e}")
        print("  Coba lagi nanti; notebook memakai file CSV yang sudah ada.")

    # 4. Kurs harian
    print("Mengunduh kurs USD/IDR dari Frankfurter (ECB)...")
    try:
        resp = requests.get(
            "https://api.frankfurter.app/2019-01-01..2026-09-30?from=USD&to=IDR",
            timeout=30,
        )
        resp.raise_for_status()
        rates = resp.json()["rates"]
        kurs = pd.DataFrame(
            [{"Tanggal": t, "Kurs_USD_IDR": v["IDR"]} for t, v in sorted(rates.items())]
        )
        kurs.to_csv(DATA / "kurs_harian.csv", index=False)
        print(f"  OK kurs_harian.csv: {len(kurs)} baris")
    except Exception as e:
        print(f"  GAGAL kurs: {type(e).__name__}: {e}")

    # 5. Inflasi bulanan Indonesia (OECD MEI via FRED, tanpa kunci)
    print("Mengunduh inflasi bulanan Indonesia dari FRED...")
    try:
        resp = requests.get(
            "https://fred.stlouisfed.org/graph/fredgraph.csv?id=IDNCPIALLMINMEI",
            timeout=30,
        )
        resp.raise_for_status()
        cpi = pd.read_csv(io.StringIO(resp.text), parse_dates=["observation_date"])
        cpi.columns = ["tanggal", "indeks"]
        cpi = cpi.dropna().reset_index(drop=True)
        cpi["inflasi_mom"] = 100 * (cpi["indeks"] / cpi["indeks"].shift(1) - 1)
        cpi["inflasi_yoy"] = 100 * (cpi["indeks"] / cpi["indeks"].shift(12) - 1)
        cpi = cpi.dropna(subset=["inflasi_yoy"]).reset_index(drop=True)
        cpi.to_csv(DATA / "idn_inflasi_bulanan.csv", index=False)
        print(
            f"  OK idn_inflasi_bulanan.csv: {len(cpi)} baris, "
            f"{cpi['tanggal'].min().date()}-{cpi['tanggal'].max().date()}"
        )
    except Exception as e:
        print(f"  GAGAL inflasi bulanan: {type(e).__name__}: {e}")

    # 6. IHSG riwayat panjang (1990 sampai sekarang)
    print("Mengunduh IHSG riwayat panjang dari Yahoo Finance...")
    try:
        import yfinance as yf

        panjang = yf.download(
            "^JKSE",
            start="1990-01-01",
            end="2026-09-30",
            progress=False,
            auto_adjust=True,
        )
        if isinstance(panjang.columns, pd.MultiIndex):
            panjang.columns = panjang.columns.get_level_values(0)
        panjang = panjang.reset_index()
        panjang.to_csv(DATA / "ihsg_panjang.csv", index=False)
        print(
            f"  OK ihsg_panjang.csv: {len(panjang)} baris, "
            f"{panjang['Date'].min().date()}-{panjang['Date'].max().date()}"
        )
    except Exception as e:
        print(f"  GAGAL IHSG panjang: {type(e).__name__}: {e}")

    # 7. Kurs tahunan panjang (1967-2025), memuat krisis 1997-1998
    print("Mengunduh kurs tahunan panjang dari World Bank...")
    try:
        kurs_panjang = world_bank("IDN", "PA.NUS.FCRF", "kurs", "1967:2025")
        kurs_panjang = kurs_panjang[["tahun", "kurs"]].sort_values("tahun")
        kurs_panjang.to_csv(DATA / "idn_kurs_tahunan.csv", index=False)
        print(
            f"  OK idn_kurs_tahunan.csv: {len(kurs_panjang)} baris, "
            f"{kurs_panjang['tahun'].min()}-{kurs_panjang['tahun'].max()}"
        )
    except Exception as e:
        print(f"  GAGAL kurs tahunan: {type(e).__name__}: {e}")

    # 8. Cross-section 34 provinsi 2021 (kompilasi indikator BPS;
    #    nilai sudah dicek terhadap angka BPS, misalnya PDRB per kapita
    #    DKI Jakarta 274,7 juta)
    print("Mengunduh data provinsi 2021...")
    try:
        url = (
            "https://raw.githubusercontent.com/sainsdataid/dataset/main/"
            "Data%2034%20Provinsi%202021.csv"
        )
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        prov = pd.read_csv(io.StringIO(resp.text))
        prov = prov.rename(
            columns={
                "PDRB_KAPITA": "PDRB_Kapita",
                "TPT": "Pengangguran",
                "PST_KEMISKINAN": "Kemiskinan",
                "AHH_L": "AHH_Laki",
                "AHH_P": "AHH_Perempuan",
                "PST_PEROKOK": "Perokok",
                "APS_07_12": "APS_7_12",
                "APS_13_15": "APS_13_15",
                "APS_16_18": "APS_16_18",
                "APS_19_23": "APS_19_23",
            }
        )
        prov.to_csv(DATA / "provinsi_2021.csv", index=False)
        print(f"  OK provinsi_2021.csv: {len(prov)} baris, {len(prov.columns)} kolom")
    except Exception as e:
        print(f"  GAGAL provinsi: {type(e).__name__}: {e}")

    # 9. Data kredit default (UCI, subset 1000 baris berstratifikasi)
    print("Mengunduh data kredit default (UCI)...")
    try:
        url = (
            "https://archive.ics.uci.edu/static/public/350/"
            "default+of+credit+card+clients.zip"
        )
        resp = requests.get(url, timeout=60)
        resp.raise_for_status()
        with zipfile.ZipFile(io.BytesIO(resp.content)) as z:
            with z.open("default of credit card clients.xls") as f:
                uci = pd.read_excel(f, header=1)
        uci = uci.rename(
            columns={
                "LIMIT_BAL": "limit_kredit",
                "SEX": "jenis_kelamin",
                "EDUCATION": "pendidikan",
                "MARRIAGE": "status_nikah",
                "AGE": "usia",
                "default payment next month": "gagal_bayar",
            }
        )[
            [
                "limit_kredit",
                "jenis_kelamin",
                "pendidikan",
                "status_nikah",
                "usia",
                "gagal_bayar",
            ]
        ]
        contoh = (
            pd.concat(
                [
                    uci[uci["gagal_bayar"] == 1].sample(n=220, random_state=42),
                    uci[uci["gagal_bayar"] == 0].sample(n=780, random_state=42),
                ]
            )
            .sample(frac=1, random_state=42)
            .reset_index(drop=True)
        )
        (DATA / "cadangan").mkdir(parents=True, exist_ok=True)
        contoh.to_csv(DATA / "kredit_default.csv", index=False)
        print(f"  OK kredit_default.csv: {len(contoh)} baris")
    except ImportError:
        print("  GAGAL kredit default: butuh paket xlrd (pip install xlrd)")
    except Exception as e:
        print(f"  GAGAL kredit default: {type(e).__name__}: {e}")


if __name__ == "__main__":
    main()
