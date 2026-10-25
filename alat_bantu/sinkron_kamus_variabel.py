"""Perbarui definisi variabel pada notebook dan satu katalog data.

Notebook .ipynb adalah sumber utama. Kode serta keluaran tetap dipertahankan.
"""
import argparse
import ast
import copy
import csv
import hashlib
import json
import re
from pathlib import Path

import nbformat
from uji_format_data import FORMAT_DATA

ROOT = Path(__file__).resolve().parent.parent
KATALOG = ROOT / "data/README.md"
PENANDA = "<!-- kamus_variabel:"

def baca_kamus():
    kamus = json.loads((ROOT / "alat_bantu/kamus_variabel.json").read_text(encoding="utf-8"))["dataset"]
    csv_files = sorted((ROOT / "data").rglob("*.csv"))
    assert len(csv_files) == 59
    assert {p.name for p in csv_files} == {k for k in kamus if k.endswith(".csv")}
    for path in csv_files:
        assert path.relative_to(ROOT).as_posix() == kamus[path.name]["lokasi"], path
        with path.open(encoding="utf-8-sig", newline="") as stream:
            columns = next(csv.reader(stream))
        assert columns == [v["kolom"] for v in kamus[path.name]["variabel"]], path
    for dataset in kamus.values():
        for variabel in dataset["variabel"]:
            assert all(variabel[k].strip() for k in ("kolom", "arti", "satuan", "peran"))
    return kamus

def dataset_dibaca(sel, path):
    nama = re.findall(r"read_csv\(\s*['\"](?:data/)?([a-z0-9_]+\.csv)['\"]", sel)
    nama += re.findall(r"read_csv\(\s*URL_DATA\s*\+\s*['\"]([a-z0-9_]+\.csv)['\"]", sel)
    if "sm.datasets.spector.load_pandas()" in sel:
        nama.append("spector")
    if path.parent.name == "03_regresi_housing":
        if "pd.read_csv(lokasi_data)" in sel:
            nama.append("housing.csv")
        if "jarak = pd.DataFrame(" in sel:
            nama.append("contoh_taksi")
    if "harapan_hidup = pd.read_csv(...)" in sel:
        nama.append("uts_4.csv")
    return list(dict.fromkeys(nama))

def tabel_variabel(name, dataset, alias=None, kode=None):
    alias = alias or {}
    lines = [f"### Kenali data: {dataset['judul']}", ""]
    lokasi = f"`{dataset['lokasi']}`" if name.endswith(".csv") else ("dataset bawaan statsmodels (`spector`)" if name == "spector" else "tabel contoh yang dibuat langsung di kode")
    lines += [f"**Data:** {lokasi}. **Satu baris:** {dataset['satu_baris']}.", ""]
    if alias:
        lines += ["Nama singkat di kode berasal dari penggantian nama kolom CSV; isi angkanya tetap sama.", "", "| Kolom CSV | Nama di kode | Pengertian | Satuan atau kode | Peran |", "|---|---|---|---|---|"]
    else:
        lines += ["| Variabel/kolom | Pengertian | Satuan atau kode | Peran |", "|---|---|---|---|"]
    for v in dataset["variabel"]:
        row = [f"`{v['kolom']}`"]
        if alias:
            row.append(f"`{alias.get(v['kolom'], v['kolom'])}`")
        row += [v["arti"], v["satuan"], v["peran"]]
        assert not any("|" in value for value in row)
        lines.append("| " + " | ".join(row) + " |")
    lines.append("")
    if dataset["catatan"]:
        lines += [dataset["catatan"], ""]
    turunan = [v for v in dataset.get("turunan", []) if kode is None or re.search(r"\b" + re.escape(v["kolom"]) + r"\b", kode)]
    if turunan:
        lines += ["Kolom turunan berikut dibuat saat praktik; kolom ini belum ada pada CSV awal.", "", "| Kolom turunan | Pengertian | Satuan/kode |", "|---|---|---|"]
        for v in turunan:
            lines.append(f"| `{v['kolom']}` | {v['arti']} | {v['satuan']} |")
        lines.append("")
    source = dataset["sumber"]
    lines += [(f"Sumber definisi: [rujukan data]({source})." if source.startswith("https://") else f"Sumber: {source}."), ""]
    return "\n".join(lines)

def alias_dan_kode(cells, kamus):
    alias = {name: {} for name in kamus}
    kode = []
    for cell in cells:
        if cell.cell_type != "code":
            continue
        source = "\n".join("pass" if line.lstrip().startswith(("%pip ", "%%writefile ")) else line for line in cell.source.splitlines())
        kode.append(source)
        for node in ast.walk(ast.parse(source)):
            if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "rename"):
                continue
            for kw in node.keywords:
                if kw.arg != "columns" or not isinstance(kw.value, ast.Dict):
                    continue
                mapping = ast.literal_eval(kw.value)
                for name, dataset in kamus.items():
                    if mapping and set(mapping).issubset({v["kolom"] for v in dataset["variabel"]}):
                        alias[name].update(mapping)
    return alias, "\n".join(kode + [c.source for c in cells])


def sinkron(path, kamus, periksa=False):
    nb = nbformat.read(path, as_version=4)
    code_before = copy.deepcopy([c for c in nb.cells if c.cell_type == "code"])
    base = [c for c in nb.cells if PENANDA not in c.source]
    alias, kode = alias_dan_kode(base, kamus)
    events = {}
    for i, cell in enumerate(base):
        if cell.cell_type == "code":
            for name in dataset_dibaca(cell.source, path):
                assert name in kamus, (path, name)
                events.setdefault(name, i)
    for i, cell in enumerate(base):
        for name in dataset_dibaca(cell.source, path):
            assert name in kamus, (path, name)
            events.setdefault(name, i)
    assert events, path
    cells = []
    for i, cell in enumerate(base):
        for name, position in events.items():
            if position == i:
                text = f"{PENANDA}{name} -->\n\n" + tabel_variabel(name, kamus[name], alias[name], kode)
                cell_id = hashlib.sha256(f"{path.relative_to(ROOT)}:{i}:{name}".encode()).hexdigest()[:12]
                cells.append(nbformat.v4.new_markdown_cell(text, id=cell_id, metadata={"tags": ["kamus_variabel"]}))
        cells.append(cell)
    nb.cells = cells
    assert code_before == [c for c in nb.cells if c.cell_type == "code"]
    nbformat.validate(nb)
    if periksa:
        old = nbformat.read(path, as_version=4)
        assert [(c.cell_type, c.source) for c in old.cells] == [(c.cell_type, c.source) for c in cells], path
    else:
        nbformat.write(nb, path)
    return list(events)


def katalog(kamus, result):
    lines = ["# Data tutorial dan arti variabel", "",
             "**Data tidak perlu diunggah ke Colab.** Notebook membaca atau mengunduh berkas langsung dari GitHub.",
             "Untuk dashboard, data yang dipakai hanya **provinsi_2021.csv**.", "",
             "- **44 CSV aktif** berada di folder data/.",
             "- **15 CSV cadangan** berada di data/cadangan/ dan belum dipakai oleh notebook saat ini.",
             "- Arti variabel juga tersedia pada bagian **Kenali data** di setiap notebook.", "",
             "[Kembali ke materi](../README.md) · [Dasar notebook](../README.md#dasar-notebook)", "",
             "## Contoh berbagai format pada Sesi 0", "",
             "Satu tabel makro Indonesia 2000 sampai 2025, berisi 26 baris dan tujuh kolom.",
             "[CSV sumber](idn_makro_tahunan.csv) tetap menjadi acuan. Enam salinan berikut berada pada satu folder contoh_format/ dan semuanya dipakai dalam tutorial pembuka.",
             "SPSS dan Stata adalah hasil konversi untuk latihan membaca berkas, bukan mikrodata survei asli. Nama kolom dan angka dipertahankan.", "",
             "| Format | Berkas | Cara membaca |", "|---|---|---|"]
    for nama, ext, pembaca in FORMAT_DATA:
        lines.append(f"| {nama} | [idn_makro_tahunan.{ext}](contoh_format/idn_makro_tahunan.{ext}) | `{pembaca}` |")
    lines += ["", "Definisi kolom mengikuti [kamus makro Indonesia](#idn_makro_tahunan_csv). Excel menyediakan lembar data dan sumber.",
              "Sumber: [World Bank Indonesia](https://data.worldbank.org/country/indonesia), lisensi CC BY 4.0. Salinan CSV tutorial dipertahankan agar angka konsisten dengan Lab 6.", "",
              "## Data yang dipakai tiap notebook", "", "| Notebook | Data |", "|---|---|"]
    usage = {name: [] for name in kamus}
    for row in result:
        target = row["notebook"]
        names = []
        for name in row["dataset"]:
            usage[name].append(target)
            names.append(f"[{name}](#{name.replace('.', '_')})")
        lines.append(f"| [{target}](../{target}) | {', '.join(names)} |")
    lines += ["", "## Cari nama dataset", "", "| Data | Status | Isi |", "|---|---|---|"]
    for name, item in sorted(kamus.items()):
        lines.append(f"| [{name}](#{name.replace('.', '_')}) | {item.get('status', 'contoh di kode')} | {item['judul']} |")
    lines += ["", "## Definisi variabel", "",
              "X adalah variabel penjelas, sedangkan Y adalah target. Satuan yang tidak dijelaskan sumber tidak ditebak dari besar angkanya."]
    for name, item in sorted(kamus.items()):
        lines += ["", f'<a id="{name.replace(".", "_")}"></a>', "", tabel_variabel(name, item)]
        if name.endswith(".csv"):
            location = Path(item["lokasi"]).relative_to("data").as_posix()
            lines += [f"[Buka CSV]({location}).", ""]
        if usage[name]:
            lines += ["Dipakai pada: " + ", ".join(f"[{Path(p).stem}](../{p})" for p in usage[name]) + "."]
        else:
            lines += ["Data cadangan: bahan tambahan pengajar, belum dibaca oleh notebook saat ini."]
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--periksa", action="store_true")
    args = parser.parse_args()
    kamus = baca_kamus()
    paths = sorted((ROOT / "materi").rglob("*.ipynb")) + sorted((ROOT / "pengajar/kunci_jawaban").glob("*.ipynb"))
    assert len(paths) == 23
    result = [{"notebook": p.relative_to(ROOT).as_posix(), "dataset": sinkron(p, kamus, args.periksa)} for p in paths]
    text = katalog(kamus, result)
    if args.periksa:
        assert KATALOG.read_text(encoding="utf-8") == text
    else:
        KATALOG.write_text(text, encoding="utf-8")
        report = {"status": "PASS", "jumlah_csv": 59, "jumlah_definisi_kolom": sum(len(d["variabel"]) for d in kamus.values()),
                  "jumlah_notebook": len(paths), "jumlah_tabel_di_tutorial": sum(len(r["dataset"]) for r in result),
                  "kode_dan_output_notebook_tetap": True, "tutorial": result}
        (ROOT / "alat_bantu/laporan/kamus_variabel.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"PASS: 59 CSV; {len(paths)} notebook; {sum(len(r['dataset']) for r in result)} tabel definisi; kode dan output utuh.")


if __name__ == "__main__":
    main()
