"""Periksa nama, tautan, isi paket data, dan kelengkapan berkas setelah penataan.

Jalankan dari folder utama: python alat_bantu/periksa_paket.py
Laporan disimpan ke alat_bantu/laporan/hasil_pemeriksaan.md; tidak menjalankan model.
"""

from pathlib import Path
from zipfile import ZipFile
import ast
import csv
import hashlib
import json
import re
from datetime import datetime
from urllib.parse import unquote, urlsplit

from PIL import Image
import nbformat
from laporan_bersama import simpan_ringkasan

from uji_notebook import periksa_notebook
from sinkron_kamus_variabel import baca_kamus, sinkron
from uji_format_data import periksa_format

ROOT = Path(__file__).resolve().parent.parent


def hash_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def baris_markdown(source):
    """Abaikan isi pagar kode ketika membaca judul dan tautan dokumen."""
    fenced = False
    for line in source.splitlines():
        if line.strip().startswith(("```", "~~~")):
            fenced = not fenced
            continue
        if not fenced:
            yield line


def isi_dokumen(path):
    if path.suffix == ".ipynb":
        nb = nbformat.read(path, as_version=4)
        return "\n\n".join(c.source for c in nb.cells if c.cell_type == "markdown")
    return path.read_text(encoding="utf-8")


def penanda_bagian(path):
    text = "\n".join(baris_markdown(isi_dokumen(path)))
    anchors = set(re.findall(r'<a\s+id=[\"\']([^\"\']+)', text))
    occurrences = {}
    for line in text.splitlines():
        match = re.match(r"^#{1,6}\s+(.+)", line)
        if not match:
            continue
        label = re.sub(r"\[([^]]+)\]\([^)]*\)", r"\1", match[1]).strip().lower()
        slug = re.sub(r"[^\w\- ]", "", label).replace(" ", "-")
        n = occurrences.get(slug, 0)
        occurrences[slug] = n + 1
        anchors.add(slug + (f"-{n}" if n else ""))
    return anchors


def periksa_tautan(path, berkas):
    text = "\n".join(baris_markdown(isi_dokumen(path)))
    prefix = (
        "https://colab.research.google.com/github/akhiyarwaladi/ekonometrika_coding_workshop/blob/main/",
        "https://github.com/akhiyarwaladi/ekonometrika_coding_workshop/blob/main/",
        "https://raw.githubusercontent.com/akhiyarwaladi/ekonometrika_coding_workshop/main/",
    )
    count = 0
    for target in re.findall(r"\[[^]\n]*\]\(([^)\n]+)\)", text):
        target = target.strip().strip("<>")
        parsed = urlsplit(target)
        own = next((p for p in prefix if target.startswith(p)), None)
        if own:
            destination = (ROOT / unquote(parsed.path.split("/main/", 1)[1])).resolve()
        elif parsed.scheme or parsed.netloc:
            continue
        else:
            destination = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path
        assert destination.is_relative_to(ROOT), (path, target)
        assert destination.exists(), (path.relative_to(ROOT), target)
        if parsed.fragment and destination.suffix in {".md", ".ipynb"}:
            assert unquote(parsed.fragment) in penanda_bagian(destination), (path.relative_to(ROOT), target, "Bagian tujuan tidak ditemukan")
        count += 1
    # Nama berkas yang disebut di dalam teks juga harus dapat ditelusuri.
    for name in re.findall(r"`([^`\n]+\.(?:csv|ipynb|md))`", text):
        if any(c in name for c in " ()\""):
            continue
        if "/" in name:
            assert (ROOT / name).exists() or (path.parent / name).exists(), (path, name)
        else:
            candidates = berkas.get(name, [])
            assert candidates, (path, name)
    return count


def periksa_bagian_notebook(path):
    nb = nbformat.read(path, as_version=4)
    titles, main_sections = [], []
    count = 0
    imports = set()
    level_sebelumnya = 0
    for cell in nb.cells:
        if cell.cell_type == "markdown":
            for line in baris_markdown(cell.source):
                heading = re.match(r"^(#{1,6}) ", line)
                if heading:
                    level = len(heading[1])
                    assert level <= level_sebelumnya + 1, (path, line, "Hierarki judul melompat")
                    level_sebelumnya = level
            headings = [line for line in baris_markdown(cell.source) if re.match(r"^#{1,2} ", line)]
            for line in headings:
                if line.startswith("# "):
                    titles.append(line)
                else:
                    assert cell.source.splitlines()[0] == line, (path, line, "Judul bagian harus mengawali sel")
                    count += 1
                    number = re.match(r"^## (\d+)\. ", line)
                    if number:
                        main_sections.append(int(number[1]))
        elif cell.cell_type == "code":
            assert cell.source.strip(), (path, "Sel kode kosong")
            if cell.source.startswith("%%") or "set_auth_token" in cell.source:
                continue
            source = "\n".join("pass" if s.lstrip().startswith("%") else s for s in cell.source.splitlines())
            for node in ast.parse(source).body:
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    signature = ast.dump(node, include_attributes=False)
                    assert signature not in imports, (path, "Impor identik berulang", ast.unparse(node))
                    imports.add(signature)
    assert len(titles) == 1 and nb.cells[0].source.startswith(titles[0]), (path, titles)
    assert main_sections == list(range(1, len(main_sections) + 1)), (path, main_sections)
    assert main_sections, (path, "Bagian inti belum diberi nomor")
    assert nb.cells[-1].source.startswith("## Selanjutnya"), path
    number = path.stem.split("_", 1)[0]
    if path.parent.name == "01_ekonometrika":
        assert titles[0].startswith(f"# Sesi {number}: "), (path, titles[0])
    elif path.parent.name in {"02_latihan", "kunci_jawaban"}:
        prefix = "# Kunci Lab" if path.parent.name == "kunci_jawaban" else "# Lab"
        assert titles[0].startswith(f"{prefix} {number}: "), (path, titles[0])
    return count


def main():
    abaikan = {".git", ".venv", "arsip", "hasil_dashboard", "__pycache__", ".ipynb_checkpoints", "administrasi"}
    standar = {"README.md", ".gitignore", ".gitattributes", "requirements.txt"}
    files = [p for p in ROOT.rglob("*") if not set(p.relative_to(ROOT).parts) & abaikan]
    for path in files:
        assert path.name in standar or re.fullmatch(
            r"[a-z0-9_]+(?:\.[a-z0-9_]+)?", path.name
        ), path

    with (ROOT / "alat_bantu/laporan/peta_perubahan_nama.csv").open(
        encoding="utf-8-sig", newline=""
    ) as f:
        pemetaan = list(csv.DictReader(f))
    terlindungi = 0
    lokal_saja = 0
    for baris in pemetaan:
        tujuan = ROOT / baris["lokasi_baru"]
        lokasi = baris["lokasi_baru"]
        if not tujuan.exists() and lokasi.startswith(("alat_bantu/arsip/", "alat_bantu/administrasi/")):
            lokal_saja += 1
            continue
        assert tujuan.exists(), tujuan
        if (
            lokasi.startswith(
                (
                    "data/", "alat_bantu/arsip/slide/png_regresi_300_dpi/",
                    "alat_bantu/gambar/ekonometrika/", "alat_bantu/administrasi/",
                )
            )
            or lokasi == "slide/02_regresi_machine_learning.pdf"
        ):
            assert hash_file(tujuan) == baris["sha256_sebelum"], tujuan
            terlindungi += 1

    csv_files = sorted((ROOT / "data").rglob("*.csv"))
    assert len(csv_files) == 59
    nama_lama = {b["lokasi_baru"]: b["lokasi_lama"] for b in pemetaan}
    cadangan_path = ROOT / "alat_bantu/arsip/cadangan_sebelum_penataan.zip"
    if cadangan_path.exists():
        with ZipFile(cadangan_path) as cadangan:
            for path in csv_files:
                lokasi = path.relative_to(ROOT).as_posix()
                sebelum_pemisahan = lokasi.replace("data/cadangan/", "data/", 1)
                assert (
                    cadangan.read(nama_lama.get(lokasi, sebelum_pemisahan)) == path.read_bytes()
                ), path
    aktif = sorted((ROOT / "data").glob("*.csv"))
    assert len(aktif) == 45
    assert len(list((ROOT / "data/cadangan").glob("*.csv"))) == 14
    data_lepas = [p for p in files if p.is_file() and p.suffix in {".csv", ".xlsx", ".xls"}
                  and not p.is_relative_to(ROOT / "data")
                  and p != ROOT / "alat_bantu/laporan/peta_perubahan_nama.csv"]
    assert not data_lepas, data_lepas
    expected = {p.relative_to(ROOT).as_posix() for p in aktif}
    format_data = periksa_format()
    expected.update(item["berkas"] for item in format_data["hasil"])
    expected.add("alat_bantu/metode_lanjutan.py")
    with ZipFile(ROOT / "alat_bantu/paket/data_tutorial.zip") as paket:
        assert set(paket.namelist()) == expected
        for nama in expected:
            assert paket.read(nama) == (ROOT / nama).read_bytes(), nama

    notebooks = sorted((ROOT / "materi").rglob("*.ipynb")) + sorted(
        (ROOT / "pengajar/kunci_jawaban").glob("*.ipynb")
    )
    assert len(notebooks) == 23
    assert not list((ROOT / "materi").rglob("*.py")), "Materi peserta memakai notebook sebagai sumber utama."
    assert not list((ROOT / "pengajar/kunci_jawaban").glob("*.py"))
    assert [p.relative_to(ROOT).as_posix() for p in notebooks if "dashboard" in p.stem] == [
        "materi/04_dashboard_indonesia/01_dashboard_ekonomi.ipynb"
    ], "Gunakan satu notebook dashboard untuk pratinjau dan ngrok."
    kamus = baca_kamus()
    jumlah_tabel_variabel = 0
    jumlah_bagian = 0
    for path in notebooks:
        periksa_notebook(path)
        nbformat.validate(nbformat.read(path, as_version=4))
        jumlah_tabel_variabel += len(sinkron(path, kamus, True))
        jumlah_bagian += periksa_bagian_notebook(path)
    for latihan in (ROOT / "materi/02_latihan").glob("*.ipynb"):
        kunci = ROOT / "pengajar/kunci_jawaban" / latihan.name
        assert kunci.exists(), latihan
        judul_latihan = nbformat.read(latihan, as_version=4).cells[0].source.splitlines()[0]
        judul_kunci = nbformat.read(kunci, as_version=4).cells[0].source.splitlines()[0]
        assert judul_kunci == judul_latihan.replace("# Lab", "# Kunci Lab", 1), (latihan, "Judul latihan dan kunci berbeda")

    jumlah_tautan = 0
    berkas = {}
    for path in files:
        if path.is_file():
            berkas.setdefault(path.name, []).append(path)
    for path in files:
        if path.suffix not in {".md", ".ipynb"} or not path.is_file():
            continue
        jumlah_tautan += periksa_tautan(path, berkas)

    folder_lama = ROOT / "alat_bantu/arsip/slide/png_regresi_300_dpi"
    png_files = sorted(folder_lama.glob("*.png"))
    if folder_lama.exists():
        assert len(png_files) == 31
    for i, path in enumerate(png_files, 1):
        assert path.name == f"halaman_{i:02d}.png"
        with Image.open(path) as gambar:
            assert gambar.size == (3000, 1688), (path, gambar.size)
            assert abs(gambar.info["dpi"][0] - 300) < 1

    png_tajam = sorted((ROOT / "slide/png_regresi_tajam").glob("*.png"))
    assert len(png_tajam) == 31
    with ZipFile(ROOT / "alat_bantu/paket/png_regresi_tajam.zip") as paket_png:
        assert set(paket_png.namelist()) == {p.name for p in png_tajam}
        for i, path in enumerate(png_tajam, 1):
            assert path.name == f"halaman_{i:02d}.png"
            with Image.open(path) as gambar:
                assert gambar.size == (6000, 3375), (path, gambar.size)
                assert abs(gambar.info["dpi"][0] - 600) < 1
            assert paket_png.read(path.name) == path.read_bytes(), path

    laporan = ROOT / "alat_bantu/laporan"
    hasil = {"status": "PASS", "notebook": len(notebooks), "csv_aktif": len(aktif),
             "csv_cadangan": 14, "hash_diperiksa": terlindungi, "tautan_lokal": jumlah_tautan,
             "bagian_notebook": jumlah_bagian, "judul_dan_nomor_bagian": "PASS",
             "tautan_dan_penanda_bagian": "PASS", "impor_identik_berulang": 0}
    (laporan / "struktur.json").write_text(json.dumps(hasil, indent=2), encoding="utf-8")
    simpan_ringkasan()
    print(
        f"PASS: {len(pemetaan) - lokal_saja} lokasi, {terlindungi} hash, {len(notebooks)} notebook, {jumlah_tautan} tautan, 31 PNG tajam dan ZIP."
    )


if __name__ == "__main__":
    main()
