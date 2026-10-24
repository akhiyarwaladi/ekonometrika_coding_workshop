"""Sisipkan definisi variabel ke sumber .py dan notebook tanpa mengubah kode.

Jalankan dari folder utama:
    python alat_bantu/sinkron_kamus_variabel.py
    python alat_bantu/sinkron_kamus_variabel.py --periksa

Sumber definisi: alat_bantu/kamus_variabel.json. Hasil eksekusi notebook dipertahankan.
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

from konversi_notebook import ke_sumber, parse_sel

ROOT = Path(__file__).resolve().parent.parent
KATALOG = ROOT / "panduan/07_kamus_variabel.md"
PENANDA = "<!-- kamus_variabel:"


def pecah_sel(teks):
    posisi = list(re.finditer(r"(?m)^# %%(?: \[markdown\])?[ \t]*\n", teks))
    assert posisi, "Penanda sel # %% tidak ditemukan."
    assert not teks[: posisi[0].start()].strip()
    return [
        teks[m.start() : posisi[i + 1].start() if i + 1 < len(posisi) else len(teks)]
        for i, m in enumerate(posisi)
    ]


def baca_kamus():
    kamus = json.loads((ROOT / "alat_bantu/kamus_variabel.json").read_text(encoding="utf-8"))["dataset"]
    csv_files = sorted((ROOT / "data").glob("*.csv"))
    assert len(csv_files) == 59
    assert {p.name for p in csv_files} == {k for k in kamus if k.endswith(".csv")}
    for path in csv_files:
        with path.open(encoding="utf-8-sig", newline="") as stream:
            columns = next(csv.reader(stream))
        assert columns == [v["kolom"] for v in kamus[path.name]["variabel"]], path
    for dataset in kamus.values():
        for variabel in dataset["variabel"]:
            assert all(variabel[k].strip() for k in ("kolom", "arti", "satuan", "peran"))
    return kamus


def dataset_dibaca(sel, path):
    nama = re.findall(r"read_csv\(\s*['\"](?:data/)?([a-z0-9_]+\.csv)['\"]", sel)
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


def alias_dan_kode(sels, kamus):
    alias = {k: {} for k in kamus}
    semua_kode = []
    for sel in sels:
        if sel.startswith("# %% [markdown]"):
            continue
        kode = "\n".join(
            "pass" if line.lstrip().startswith("%pip ") else line
            for line in sel.splitlines()[1:]
        )
        semua_kode.append(kode)
        for node in ast.walk(ast.parse(kode)):
            if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "rename"):
                continue
            for kw in node.keywords:
                if kw.arg != "columns" or not isinstance(kw.value, ast.Dict):
                    continue
                mapping = ast.literal_eval(kw.value)
                for name, dataset in kamus.items():
                    columns = {v["kolom"] for v in dataset["variabel"]}
                    if mapping and set(mapping).issubset(columns):
                        alias[name].update(mapping)
    # Petunjuk kode dalam latihan juga dapat menyebut variabel turunan.
    return alias, "\n".join(semua_kode + sels)


def tabel_variabel(name, dataset, alias=None, kode=None):
    alias = alias or {}
    lines = [f"### Kenali data: {dataset['judul']}", ""]
    lokasi = f"`data/{name}`" if name.endswith(".csv") else ("dataset bawaan statsmodels (`spector`)" if name == "spector" else "tabel contoh yang dibuat langsung di kode")
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


def sinkron(path, kamus, periksa):
    raw = path.read_bytes().decode("utf-8")
    newline = "\r\n" if "\r\n" in raw else "\n"
    teks = raw.replace("\r\n", "\n")
    sels = [s for s in pecah_sel(teks) if PENANDA not in s]
    # Tabel lama Housing diganti oleh tabel terpusat yang lebih lengkap.
    sels = [re.sub(r"(?m)^# \| Kolom \| Arti ringkas \|\n(?:# \|.*\n)+", "", s) for s in sels]
    alias, kode = alias_dan_kode(sels, kamus)
    events = {}
    # Data yang benar-benar dibaca mendapat definisi tepat sebelum sel kode.
    for i, sel in enumerate(sels):
        if sel.startswith("# %% [markdown]"):
            continue
        for name in dataset_dibaca(sel, path):
            assert name in kamus, (path, name)
            events.setdefault(name, i)
    # Latihan yang kodenya masih berupa petunjuk tetap dijelaskan datanya.
    for i, sel in enumerate(sels):
        for name in dataset_dibaca(sel, path):
            assert name in kamus, (path, name)
            events.setdefault(name, i)
    assert events, f"Tidak ada dataset yang dikenali: {path}"

    notebook_path = path.with_suffix(".ipynb")
    notebook = nbformat.read(notebook_path, as_version=4)
    original_code = copy.deepcopy([c for c in notebook.cells if c.cell_type == "code"])
    base_cells = [c for c in notebook.cells if PENANDA not in c.source]
    assert len(base_cells) == len(sels), path
    new_sels, new_cells = [], []
    for i, (sel, cell) in enumerate(zip(sels, base_cells)):
        for name, position in events.items():
            if position != i:
                continue
            markdown = f"{PENANDA}{name} -->\n\n" + tabel_variabel(name, kamus[name], alias[name], kode)
            block = "# %% [markdown]\n" + "\n".join("# " + line if line else "#" for line in markdown.splitlines()) + "\n\n"
            new_sels.append(block)
            cell_id = hashlib.sha256(f"{path.relative_to(ROOT)}:{i}:{name}".encode()).hexdigest()[:12]
            _, source_lines = parse_sel(block)[0]
            markdown_source = "".join(ke_sumber("markdown", source_lines))
            new_cells.append(nbformat.v4.new_markdown_cell(markdown_source, id=cell_id, metadata={"tags": ["kamus_variabel"]}))
        kind, lines = parse_sel(sel)[0]
        assert kind == cell.cell_type
        source = "".join(ke_sumber(kind, lines))
        if kind == "code":
            assert source.strip() == cell.source.strip(), (path, i)
        else:
            cell.source = source
        new_sels.append(sel)
        new_cells.append(cell)
    new_text = "".join(new_sels)
    notebook.cells = new_cells
    assert original_code == [c for c in notebook.cells if c.cell_type == "code"], path
    nbformat.validate(notebook)
    if periksa:
        assert teks == new_text, f"Definisi .py belum sinkron: {path}"
        existing = nbformat.read(notebook_path, as_version=4)
        assert [(c.cell_type, c.source) for c in existing.cells] == [(c.cell_type, c.source) for c in notebook.cells], f"Definisi notebook belum sinkron: {notebook_path}"
    else:
        path.write_bytes(new_text.replace("\n", newline).encode("utf-8"))
        nbformat.write(notebook, notebook_path)
    return list(events)


def katalog(kamus, usage):
    lines = ["# Kamus variabel data tutorial", "", "Tabel ini menjelaskan seluruh 59 CSV, data Spector, dan contoh taksi pada tutorial.", "Definisi yang diperlukan juga ditampilkan sebelum pembacaan data di setiap", "sumber `.py` dan notebook `.ipynb`, termasuk latihan serta kunci jawaban.", "", "X adalah variabel penjelas dan Y adalah target yang dijelaskan/diprediksi.", "Kolom identitas dan waktu membantu mengenali pengamatan; keduanya tidak otomatis", "menjadi fitur numerik model. Peran suatu kolom dapat berbeda mengikuti pertanyaan model.", "", "Satuan yang tidak dijelaskan sumber ditulis apa adanya. Ukuran angka tidak cukup", "untuk menetapkan rupiah, juta rupiah, persen, atau skala lainnya.", "", "## Cari dataset", "", "| Data | Isi |", "|---|---|"]
    for name in sorted(kamus):
        anchor = name.replace(".", "_")
        lines.append(f"| [{name}](#{anchor}) | {kamus[name]['judul']} |")
    for name in sorted(kamus):
        lines += ["", f'<a id="{name.replace(".", "_")}"></a>', "", tabel_variabel(name, kamus[name])]
        if name.endswith(".csv"):
            lines += [f"[Buka berkas data](../data/{name}).", ""]
        if usage[name]:
            lines += ["Dijelaskan pada:", ""]
            for notebook in usage[name]:
                target = Path(notebook).with_suffix(".ipynb").as_posix()
                lines.append(f"- [{target}](../{target})")
        else:
            lines += ["Data cadangan: belum dibaca oleh notebook contoh, latihan, atau kunci jawaban saat ini."]
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--periksa", action="store_true", help="Periksa tanpa mengubah berkas.")
    args = parser.parse_args()
    kamus = baca_kamus()
    paths = sorted((ROOT / "materi").rglob("*.py")) + sorted((ROOT / "pengajar/kunci_jawaban").glob("*.py"))
    assert len(paths) == 22
    usage = {k: [] for k in kamus}
    result = []
    for path in paths:
        names = sinkron(path, kamus, args.periksa)
        relative = path.relative_to(ROOT).as_posix()
        for name in names:
            usage[name].append(relative)
        result.append({"sumber": relative, "dataset": names})
    text = katalog(kamus, usage)
    if args.periksa:
        assert KATALOG.read_text(encoding="utf-8") == text
    else:
        KATALOG.write_text(text, encoding="utf-8")
        report = {"status": "PASS", "jumlah_csv": 59, "jumlah_definisi_kolom": sum(len(x["variabel"]) for x in kamus.values()), "jumlah_pasangan_tutorial": len(paths), "jumlah_tabel_di_tutorial": sum(len(r["dataset"]) for r in result), "kode_dan_output_notebook_tetap": True, "tutorial": result}
        (ROOT / "laporan/kamus_variabel.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"PASS: kamus 59 CSV; {len(paths)} pasangan .py/.ipynb; {sum(len(r['dataset']) for r in result)} tabel definisi; kode dan output notebook tetap utuh.")


if __name__ == "__main__":
    main()
