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


def panduan_perintah(cells, path):
    """Satu tabel per tahap; fungsi yang sudah dijelaskan tidak diulang."""
    daftar = json.loads((ROOT / "alat_bantu/kamus_variabel.json").read_text(encoding="utf-8"))["panduan_perintah"]
    groups, current = [], []
    for cell in cells:
        if cell.cell_type == "markdown" and cell.source.startswith("## ") and current:
            groups.append(current)
            current = []
        current.append(cell)
    if current:
        groups.append(current)
    result, seen, count = [], set(), 0
    for group in groups:
        kode = "\n".join(c.source for c in group if c.cell_type == "code")
        rows = []
        for i, item in enumerate(daftar):
            if i not in seen and re.search(item["pola"], kode):
                seen.add(i)
                rows.append("| " + " | ".join([f"`{item['nama']}`", item["tujuan"], item["argumen"], item["hasil"]]) + " |")
        table = None
        if rows:
            text = "<!-- panduan_perintah -->\n\n**Perintah pada tahap ini.** Baca kegunaan dan masukan sebelum menjalankan contoh. Fungsi yang sudah dijelaskan tidak diulang pada setiap sel.\n\n"
            text += "| Perintah | Untuk apa? | Arti masukan atau argumen | Hasil dan cara membacanya |\n|---|---|---|---|\n" + "\n".join(rows)
            cell_id = hashlib.sha256(f"perintah:{path.relative_to(ROOT)}:{count}".encode()).hexdigest()[:12]
            table = nbformat.v4.new_markdown_cell(text, id=cell_id, metadata={"tags": ["panduan_perintah"]})
            count += 1
        inserted = False
        for cell in group:
            if table is not None and not inserted and cell.cell_type == "code":
                result.append(table)
                inserted = True
            result.append(cell)
    return result


def alur_belajar(path):
    tahap = {
        "00": ("Belum perlu pengalaman coding; kenali sel, baris, kolom, dan satuan.", "Baca tujuh format dari kasus Indonesia yang berbeda; periksa kualitas, ringkasan, dan grafik.", "Pertanyaan ekonomi dan tabel yang dipahami untuk regresi dasar Sesi 01."),
        "01": ("Sesi 00: membaca tabel dan pola pada grafik.", "Susun X dan y, latih regresi linear, baca koefisien, dan bandingkan aktual dengan prediksi.", "Pola residual dan hubungan melengkung mengantar pemilihan bentuk pada Sesi 02."),
        "02": ("Sesi 01: regresi linear dan residual.", "Bandingkan skala level, log, kuadrat, dan kebalikan; jelaskan satuan koefisien.", "Model yang bentuknya masuk akal diperiksa asumsi dan variabel dummy pada Sesi 03."),
        "03": ("Sesi 01 dan 02: koefisien, residual, dan bentuk model.", "Pahami kategori X, pemeriksaan asumsi, koreksi standard error, dan contoh DiD.", "Sesudah kategori X, Sesi 04 mempelajari target Y yang berupa kategori atau hitungan."),
        "04": ("Regresi dasar dan dummy; pahami label kejadian pada Y.", "Pilih model untuk probabilitas, urutan, sensor, atau hitungan; nilai keputusan kredit pada data terpisah.", "Sesi 05 menambah urutan waktu sehingga latihan dan evaluasi harus mendahului masa depan."),
        "05": ("Sesi 01 sampai 03; data harus sudah diurutkan menurut waktu.", "Pelajari lag, stasioneritas, ramalan, kointegrasi, dan koreksi kesalahan.", "Sesi 06 menambah banyak unit dalam panel dan perubahan risiko melalui GARCH."),
        "06": ("Sesi 05 untuk urutan waktu; regresi dasar untuk arti koefisien.", "Bedakan efek unit pada panel dan ragam yang berubah pada GARCH; terapkan pada data yang sesuai.", "Praktik regresi rumah memperkuat evaluasi; dashboard menyajikan data, grafik, dan skenario kepada pengguna."),
    }
    if path.parent.name == "03_regresi_rumah":
        values = ("Sesi 01 sampai 03: X, y, koefisien, dan residual.", "Pelajari train/test, imputasi, model pembanding, Pipeline, dan underfitting/overfitting pada harga rumah.", "Dashboard memakai kembali pemisahan latihan/uji, grafik, metrik, dan skenario prediksi.")
    elif path.parent.name == "04_dashboard_indonesia":
        values = ("EDA, regresi scikit-learn, dan evaluasi pada data terpisah.", "Gabungkan tabel, filter, grafik interaktif, model, unduhan, dan skenario dalam satu notebook.", "Pratinjau di notebook lalu bagikan tautan ngrok; jelaskan sumber, tahun data, dan batas interpretasi.")
    else:
        values = tahap[path.stem[:2]]
        if path.stem == "05_deret_waktu_panel":
            values = ("Sesi 05 untuk deret waktu dan bagian panel Sesi 06; Lab 05 menggabungkan keduanya.", "Terapkan ARIMA, kointegrasi/ECM, dan panel pada contoh terbimbing.", "Lab 06 memindahkan kebiasaan ini ke seri dan panel ekonomi yang sumbernya dicatat.")
        elif path.stem == "06_data_indonesia":
            values = ("Sesi 01 sampai 06, terutama deret waktu dan panel.", "Kenali sumber serta satuan data Indonesia, lalu pilih model sesuai bentuk datanya.", "Gunakan hasil untuk proyek mini; dashboard menjadi penutup komunikasi hasil analisis.")
    return "<!-- alur_belajar -->\n\n**Kaitan dengan materi lain**\n\n| Bekal sebelumnya | Fokus notebook ini | Hasil yang dibawa berikutnya |\n|---|---|---|\n| " + " | ".join(values) + " |"

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
    readers = r"read_(?:csv|excel|spss|stata|json|parquet)"
    extensions = r"(?:csv|xlsx|sav|dta|tsv|json|parquet)"
    nama = re.findall(readers + r"\(\s*['\"](?:data/)?([a-z0-9_]+\." + extensions + r")[ '\"]", sel)
    nama += re.findall(readers + r"\(\s*(?:URL_DATA|URL_FORMAT)\s*\+\s*['\"]([a-z0-9_]+\." + extensions + r")[ '\"]", sel)
    if "sm.datasets.spector.load_pandas()" in sel:
        nama.append("spector")
    if path.parent.name == "03_regresi_rumah":
        if "pd.read_csv(lokasi_data)" in sel:
            nama.append("harga_rumah_boston.csv")
        if "jarak = pd.DataFrame(" in sel:
            nama.append("contoh_taksi")
    if "harapan_hidup = pd.read_csv(...)" in sel:
        nama.append("harapan_hidup.csv")
    if "bantuan_did = pd.DataFrame(" in sel:
        nama.append("contoh_did")
    return list(dict.fromkeys(nama))

def tabel_variabel(name, dataset, alias=None, kode=None, peran=True):
    alias = alias or {}
    lines = [f"### Kenali data: {dataset['judul']}", ""]
    lokasi = f"`{dataset['lokasi']}`" if "lokasi" in dataset else ("dataset bawaan statsmodels (`spector`)" if name == "spector" else "tabel contoh yang dibuat langsung di kode")
    lines += [f"**Data:** {lokasi}. **Satu baris:** {dataset['satu_baris']}.", ""]
    if alias:
        lines += ["Nama singkat di kode berasal dari penggantian nama kolom CSV; isi angkanya tetap sama.", "", "| Kolom CSV | Nama di kode | Pengertian | Satuan atau kode" + (" | Peran |" if peran else " |"), "|---|---|---|---|" + ("---|" if peran else "")]
    else:
        lines += ["| Variabel/kolom | Pengertian | Satuan atau kode" + (" | Peran |" if peran else " |"), "|---|---|---|" + ("---|" if peran else "")]
    for v in dataset["variabel"]:
        row = [f"`{v['kolom']}`"]
        if alias:
            row.append(f"`{alias.get(v['kolom'], v['kolom'])}`")
        row += [v["arti"], v["satuan"]]
        if peran:
            row.append(v["peran"])
        assert not any("|" in value for value in row)
        lines.append("| " + " | ".join(row) + " |")
    lines.append("")
    if dataset["catatan"]:
        lines += [dataset["catatan"], ""]
    turunan = [v for v in dataset.get("turunan", []) if kode is None or re.search(r"\b" + re.escape(v["kolom"]) + r"\b", kode)]
    if turunan:
        lines += ["Kolom turunan berikut dibuat saat praktik; kolom ini belum ada pada data awal.", "", "| Kolom turunan | Pengertian | Satuan/kode |", "|---|---|---|"]
        for v in turunan:
            lines.append(f"| `{v['kolom']}` | {v['arti']} | {v['satuan']} |")
        lines.append("")
    source = dataset["sumber"]
    lines += [(f"Sumber definisi: [rujukan data]({source})." if source.startswith("https://") else f"Sumber: {source}."), ""]
    if dataset.get("sumber_unduhan"):
        lines += [f"[Tabel atau API asal]({dataset['sumber_unduhan']}). Salinan diakses pada {dataset['tanggal_akses']}; berkas latihan disimpan agar hasil kelas dapat diulang.", ""]
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
    base = [c for c in nb.cells if PENANDA not in c.source and "<!-- panduan_perintah -->" not in c.source and "<!-- alur_belajar -->" not in c.source]
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
                text = f"{PENANDA}{name} -->\n\n" + tabel_variabel(name, kamus[name], alias[name], kode, peran=path.stem != "00_persiapan_colab")
                cell_id = hashlib.sha256(f"{path.relative_to(ROOT)}:{i}:{name}".encode()).hexdigest()[:12]
                cells.append(nbformat.v4.new_markdown_cell(text, id=cell_id, metadata={"tags": ["kamus_variabel"]}))
        cells.append(cell)
    cells = panduan_perintah(cells, path)
    cell_id = hashlib.sha256(f"alur:{path.relative_to(ROOT)}".encode()).hexdigest()[:12]
    cells.insert(1, nbformat.v4.new_markdown_cell(alur_belajar(path), id=cell_id, metadata={"tags": ["alur_belajar"]}))
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
             "Untuk dashboard, data yang dipakai hanya **indikator_provinsi_2021.csv**.", "",
             "- **45 CSV aktif** berada di folder data/.",
             "- **14 CSV latihan tambahan** berada di data/latihan_tambahan/ untuk pilihan kasus pengajar.",
             "- Arti variabel juga tersedia pada bagian **Kenali data** di setiap notebook.", "",
             "[Kembali ke materi](../README.md) · [Dasar notebook](../README.md#dasar-notebook)", "",
             "## Contoh berbagai format pada Sesi 0", "",
             "Tujuh format memakai tujuh kasus Indonesia yang berbeda. Sumber, unit pengamatan, arti kolom, dan konversi dijelaskan sebelum kode di notebook.",
             "CSV makro berada di data/. Enam format lainnya dikumpulkan di data/contoh_format/.",
             "Berkas SPSS, Stata, TSV, dan Parquet adalah konversi seri publik World Bank; Excel menyalin tabel BPS; JSON BMKG diratakan menjadi rekaman. Ini bukan mikrodata survei BPS.", "",
             "| Format | Berkas dan kasus | Cara membaca | Sumber |", "|---|---|---|---|",
             "| CSV | [Makro Indonesia](makro_indonesia_tahunan.csv) | `pd.read_csv(...)` | [World Bank](https://data.worldbank.org/country/indonesia) |"]
    format_names = json.loads((ROOT / "alat_bantu/kamus_variabel.json").read_text(encoding="utf-8"))["contoh_format"]
    for nama, ext, pembaca in FORMAT_DATA:
        filename = next(n for n in format_names if n.endswith("." + ext))
        item = kamus[filename]
        lines.append(f"| {nama} | [{item['judul']}](contoh_format/{filename}) | `{pembaca}` | [Sumber]({item['sumber']}) |")
    lines += ["", "Excel menyediakan lembar data dan sumber. Prakiraan cuaca adalah salinan bertanggal, bukan data cuaca yang terus diperbarui di notebook.", "",
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
        if "lokasi" in item:
            location = Path(item["lokasi"]).relative_to("data").as_posix()
            lines += [f"[Buka data]({location}).", ""]
        if usage[name]:
            lines += ["Dipakai pada: " + ", ".join(f"[{Path(p).stem}](../{p})" for p in usage[name]) + "."]
        else:
            lines += ["Data tambahan pengajar: pilih sesuai kebutuhan latihan."]
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
                  "jumlah_tabel_fungsi": sum(sum("panduan_perintah" in c.metadata.get("tags", []) for c in nbformat.read(p, as_version=4).cells) for p in paths),
                  "jumlah_tabel_alur": len(paths),
                  "kode_dan_output_notebook_tetap": True, "tutorial": result}
        (ROOT / "alat_bantu/laporan/kamus_variabel.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"PASS: 59 CSV; {len(paths)} notebook; {sum(len(r['dataset']) for r in result)} tabel definisi; kode dan output utuh.")


if __name__ == "__main__":
    main()
