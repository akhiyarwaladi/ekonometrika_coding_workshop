"""Pastikan tujuh format latihan berisi tabel makro Indonesia yang sama."""
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

    folder = ROOT / "data/contoh_format"
    sumber = ROOT / "data/idn_makro_tahunan.csv"
    asli = pd.read_csv(sumber)
    assert asli.shape == (26, 7)
    assert asli.tahun.tolist() == list(range(2000, 2026))
    assert asli.negara.eq("IDN").all()
    assert not asli.isna().any().any()
    expected = {f"idn_makro_tahunan.{ext}" for _, ext, _ in FORMAT_DATA}
    assert {p.name for p in folder.iterdir() if p.is_file()} == expected
    hasil = []
    for nama, ext, _ in FORMAT_DATA:
        path = folder / f"idn_makro_tahunan.{ext}"
        if ext == "xlsx":
            frame = pd.read_excel(path, sheet_name="data")
            assert pd.ExcelFile(path).sheet_names == ["data", "sumber"]
        elif ext == "sav":
            frame = pd.read_spss(path)
            _, metadata = pyreadstat.read_sav(str(path), metadataonly=True)
            assert all(metadata.column_names_to_labels.values())
        elif ext == "dta":
            frame = pd.read_stata(path)
            with pd.io.stata.StataReader(path) as reader:
                assert all(reader.variable_labels().values())
        elif ext == "tsv":
            frame = pd.read_csv(path, sep="\t")
        elif ext == "json":
            frame = pd.read_json(path, orient="records")
        else:
            frame = pd.read_parquet(path)
        pd.testing.assert_frame_equal(asli, frame, check_dtype=False, check_exact=False, rtol=1e-12, atol=1e-10)
        hasil.append({"format": nama, "berkas": path.relative_to(ROOT).as_posix(),
                      "baris": len(frame), "kolom": len(frame.columns),
                      "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "status": "PASS"})
    report = {"status": "PASS", "sumber_csv": sumber.relative_to(ROOT).as_posix(),
              "sha256_csv": hashlib.sha256(sumber.read_bytes()).hexdigest(),
              "periode": "2000 sampai 2025", "baris": 26, "kolom": 7, "jumlah_format": 7,
              "asal": "World Bank; salinan CSV tutorial yang sudah tersedia. Enam format lain dikonversi untuk latihan membaca berkas; nilai tidak diubah.",
              "sumber": "https://data.worldbank.org/country/indonesia", "lisensi": "CC BY 4.0", "hasil": hasil}
    return report


def main():
    from laporan_bersama import simpan_ringkasan
    report = periksa_format()
    (ROOT / "alat_bantu/laporan/uji_format_data.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    simpan_ringkasan()
    print("PASS: tujuh format menghasilkan 26 baris dan tujuh kolom dengan nilai yang sama.")


if __name__ == "__main__":
    main()
