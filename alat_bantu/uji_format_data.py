"""Periksa tujuh format dengan tujuh kasus Indonesia yang berbeda."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent.parent
FORMAT_DATA = [
    ("Excel", "xlsx", 'pd.read_excel(..., sheet_name="data")'),
    ("SPSS", "sav", "pd.read_spss(...)"),
    ("Stata", "dta", "pd.read_stata(...)"),
    ("Teks tab/TSV", "tsv", 'pd.read_csv(..., sep="\\t")'),
    ("JSON", "json", 'pd.read_json(..., orient="records")'),
    ("Parquet", "parquet", "pd.read_parquet(...)"),
]


def periksa_format():
    import pandas as pd
    import pyreadstat

    catalog = json.loads((ROOT / "alat_bantu/kamus_variabel.json").read_text(encoding="utf-8"))
    kamus = catalog["dataset"]
    folder = ROOT / "data/contoh_format"
    names = catalog["contoh_format"]
    assert len(names) == 6
    assert {p.name for p in folder.iterdir() if p.is_file()} == set(names)
    macro_path = ROOT / "data/makro_indonesia_tahunan.csv"
    macro = pd.read_csv(macro_path)
    assert macro.shape == (26, 7) and macro.tahun.tolist() == list(range(2000, 2026))
    hasil = [{"format": "CSV", "berkas": macro_path.relative_to(ROOT).as_posix(),
              "baris": len(macro), "kolom": len(macro.columns), "kasus": "Makroekonomi Indonesia",
              "sumber": kamus[macro_path.name]["sumber"], "status": "PASS"}]
    data = {}
    for nama, ext, _ in FORMAT_DATA:
        filename = next(n for n in names if n.endswith("." + ext))
        item = kamus[filename]
        path = ROOT / item["lokasi"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == item["sha256"], path
        if ext == "xlsx":
            frame = pd.read_excel(path, sheet_name="data")
            assert pd.ExcelFile(path).sheet_names == ["data", "sumber"]
            assert abs(frame.produksi_padi_ton.sum() - item["total_padi_sumber"]) <= 14
            assert abs(frame.produksi_beras_ton.sum() - item["total_beras_sumber"]) <= 14
            assert frame.loc[frame.kabupaten_kota == "Indramayu", "produksi_padi_ton"].item() == 1583262
            assert frame.loc[frame.kabupaten_kota == "Kota Depok", "produksi_padi_ton"].item() == 52
        elif ext == "sav":
            frame = pd.read_spss(path)
            _, metadata = pyreadstat.read_sav(str(path), metadataonly=True)
            assert all(metadata.column_names_to_labels.values())
            assert frame.kemiskinan_persen.between(0, 100).all()
        elif ext == "dta":
            frame = pd.read_stata(path)
            with pd.io.stata.StataReader(path) as reader:
                assert all(reader.variable_labels().values())
            assert frame.pengguna_internet_persen.between(0, 100).all()
        elif ext == "tsv":
            frame = pd.read_csv(path, sep="\t")
            assert frame.ekspor_usd.gt(0).all()
        elif ext == "json":
            frame = pd.read_json(path, orient="records")
            assert frame.kelurahan.eq("Simpang IV Sipin").all()
            assert frame.kelembapan_persen.between(0, 100).all()
            assert pd.to_datetime(frame.waktu_lokal).is_monotonic_increasing
            assert not pd.to_datetime(frame.waktu_lokal).duplicated().any()
        else:
            frame = pd.read_parquet(path)
            assert frame.jumlah_penduduk.gt(0).all()
            assert pd.api.types.is_integer_dtype(frame.jumlah_penduduk)
        assert len(frame) == item["baris"]
        assert list(frame.columns) == item["kolom"]
        assert list(frame.columns) == [v["kolom"] for v in item["variabel"]]
        assert not frame.isna().any().any()
        assert not frame.duplicated().any()
        if "tahun" in frame and ext != "xlsx":
            assert frame.tahun.is_unique and frame.tahun.is_monotonic_increasing
        data[ext] = frame
        hasil.append({"format": nama, "berkas": item["lokasi"], "kasus": item["judul"], "sumber": item["sumber"],
                      "baris": len(frame), "kolom": len(frame.columns),
                      "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "status": "PASS"})
    schemas = {tuple(macro.columns)} | {tuple(frame.columns) for frame in data.values()}
    assert len(schemas) == 7, "Setiap format harus mempunyai kasus dan kolom yang berbeda."
    return {"status": "PASS", "jumlah_format": 7, "kasus_berbeda": 7,
            "asal": "World Bank, BPS Jawa Barat, dan BMKG; konversi dijelaskan per kasus.", "hasil": hasil}


def main():
    from laporan_bersama import simpan_ringkasan
    report = periksa_format()
    (ROOT / "alat_bantu/laporan/uji_format_data.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    simpan_ringkasan()
    print("PASS: tujuh format, tujuh kasus Indonesia berbeda; sumber, satuan, label, hash, dan angka contoh diperiksa.")


if __name__ == "__main__":
    main()
