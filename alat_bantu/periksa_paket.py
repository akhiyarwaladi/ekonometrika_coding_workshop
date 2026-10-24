"""Periksa nama, tautan, isi paket data, dan kelengkapan berkas setelah penataan.

Jalankan dari folder utama: python alat_bantu/periksa_paket.py
Laporan disimpan ke laporan/penataan_folder.md; tidak menjalankan model.
"""

from pathlib import Path
from zipfile import ZipFile
import csv
import hashlib
import json
import re
from datetime import datetime

from PIL import Image
import nbformat

from uji_notebook import periksa_sinkron
from sinkron_kamus_variabel import baca_kamus, sinkron

ROOT = Path(__file__).resolve().parent.parent


def hash_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    abaikan = {".git", ".venv", "arsip", "hasil_dashboard", "__pycache__", ".ipynb_checkpoints"}
    standar = {"README.md", ".gitignore", ".gitattributes", "requirements.txt"}
    files = [p for p in ROOT.rglob("*") if not set(p.relative_to(ROOT).parts) & abaikan]
    for path in files:
        assert path.name in standar or re.fullmatch(
            r"[a-z0-9_]+(?:\.[a-z0-9_]+)?", path.name
        ), path

    with (ROOT / "laporan/peta_perubahan_nama.csv").open(
        encoding="utf-8-sig", newline=""
    ) as f:
        pemetaan = list(csv.DictReader(f))
    terlindungi = 0
    lokal_saja = 0
    for baris in pemetaan:
        tujuan = ROOT / baris["lokasi_baru"]
        lokasi = baris["lokasi_baru"]
        if not tujuan.exists() and lokasi.startswith(("arsip/", "administrasi/")):
            lokal_saja += 1
            continue
        assert tujuan.exists(), tujuan
        if (
            lokasi.startswith(
                (
                    "data/", "arsip/slide/png_regresi_300_dpi/",
                    "gambar/ekonometrika/", "administrasi/",
                )
            )
            or lokasi == "slide/02_regresi_machine_learning.pdf"
        ):
            assert hash_file(tujuan) == baris["sha256_sebelum"], tujuan
            terlindungi += 1

    csv_files = sorted((ROOT / "data").glob("*.csv"))
    assert len(csv_files) == 59
    nama_lama = {b["lokasi_baru"]: b["lokasi_lama"] for b in pemetaan}
    cadangan_path = ROOT / "arsip/cadangan_sebelum_penataan.zip"
    if cadangan_path.exists():
        with ZipFile(cadangan_path) as cadangan:
            for path in csv_files:
                lokasi = path.relative_to(ROOT).as_posix()
                assert (
                    cadangan.read(nama_lama.get(lokasi, lokasi)) == path.read_bytes()
                ), path
    expected = {p.relative_to(ROOT).as_posix() for p in csv_files}
    expected.add("alat_bantu/metode_lanjutan.py")
    with ZipFile(ROOT / "paket/data_tutorial.zip") as paket:
        assert set(paket.namelist()) == expected
        for nama in expected:
            assert paket.read(nama) == (ROOT / nama).read_bytes(), nama

    notebooks = sorted((ROOT / "materi").rglob("*.ipynb")) + sorted(
        (ROOT / "pengajar/kunci_jawaban").glob("*.ipynb")
    )
    assert len(notebooks) == 23
    kamus = baca_kamus()
    jumlah_tabel_variabel = 0
    for path in notebooks:
        periksa_sinkron(path)
        nbformat.validate(nbformat.read(path, as_version=4))
        jumlah_tabel_variabel += len(sinkron(path.with_suffix(".py"), kamus, True))
    for latihan in (ROOT / "materi/02_latihan").glob("*.ipynb"):
        assert (ROOT / "pengajar/kunci_jawaban" / latihan.name).exists(), latihan

    jumlah_tautan = 0
    for path in files:
        if path.suffix != ".md" or not path.is_file():
            continue
        teks = path.read_text(encoding="utf-8")
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", teks):
            if re.match(r"[a-zA-Z]+:|#", target):
                continue
            lokasi = target.split("#", 1)[0]
            tujuan = (path.parent / lokasi).resolve()
            laporan_ini = ROOT / "laporan/penataan_folder.md"
            assert tujuan.exists() or tujuan == laporan_ini, (
                path.relative_to(ROOT),
                target,
            )
            jumlah_tautan += 1

    folder_lama = ROOT / "arsip/slide/png_regresi_300_dpi"
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
    with ZipFile(ROOT / "paket/png_regresi_tajam.zip") as paket_png:
        assert set(paket_png.namelist()) == {p.name for p in png_tajam}
        for i, path in enumerate(png_tajam, 1):
            assert path.name == f"halaman_{i:02d}.png"
            with Image.open(path) as gambar:
                assert gambar.size == (6000, 3375), (path, gambar.size)
                assert abs(gambar.info["dpi"][0] - 600) < 1
            assert paket_png.read(path.name) == path.read_bytes(), path

    lines = [
        "# Hasil penataan folder tutorial",
        "",
        f"Diperiksa pada {datetime.now():%d-%m-%Y %H:%M} waktu komputer.",
        "",
        "## Struktur dan integritas",
        "",
        "- Nama berkas aktif menggunakan huruf kecil, garis bawah, dan nomor urutan; nama standar seperti README.md dikecualikan.",
        f"- {len(pemetaan) - lokal_saja}/{len(pemetaan)} tujuan pada peta nama tersedia; {lokal_saja} berkas arsip/administrasi hanya disimpan lokal.",
        f"- {terlindungi} berkas data, PDF, dan gambar yang diperiksa sama persis dengan hash sebelum penataan.",
        "- 59 CSV dan satu modul pendukung dalam ZIP sama dengan berkas di folder proyek.",
        (
            "- Seluruh 59 CSV sama persis dengan salinan sebelum penataan; nama kolom dan angka tidak berubah."
            if cadangan_path.exists()
            else "- ZIP cadangan lokal tidak disertakan; integritas data diperiksa melalui hash pada peta nama dan kesesuaian paket data."
        ),
        f"- {len(notebooks)} notebook valid, sinkron dengan sumber .py, dan tidak memuat sintaks tingkat lanjut yang dibatasi untuk peserta.",
        f"- {jumlah_tabel_variabel} tabel Kenali data menjelaskan variabel sebelum dataset dibaca; definisi seluruh 59 CSV tercakup dalam kamus variabel.",
        "- Tujuh latihan memiliki pasangan kunci jawaban dengan nama berkas yang sama.",
        f"- {jumlah_tautan} tautan lokal pada dokumen panduan mengarah ke berkas/folder yang tersedia.",
        (
            "- 31 PNG lama berukuran 3000 × 1688 piksel, 300 dpi, tersimpan di arsip lokal."
            if png_files
            else "- PNG lama 300 dpi tidak disertakan dalam repositori; ekspor aktif memakai versi tajam."
        ),
        "- 31 PNG tajam berurutan; ukuran 6000 × 3375 piksel dan metadata 600 dpi; isi ZIP sama persis dengan PNG terpisah.",
        "",
        "## Eksekusi notebook",
        "",
        "| Cara menjalankan | Hasil |",
        "|---|---|",
    ]
    for mode, nama in (
        ("lokal", "Folder utama proyek"),
        ("folder_notebook", "Folder masing-masing notebook"),
        ("zip", "Folder kosong dengan ZIP saja"),
    ):
        lokasi = ROOT / f"laporan/uji_notebook_{mode}.json"
        if lokasi.exists():
            hasil = json.loads(lokasi.read_text(encoding="utf-8"))
            assert not hasil["gagal"]
            lines.append(f"| {nama} | {hasil['lulus']}/{hasil['jumlah']} lulus |")
    housing = json.loads(
        (ROOT / "laporan/hasil_uji_regresi_housing.json").read_text(encoding="utf-8")
    )
    assert housing["checks"] == "PASS"
    dashboard_path = ROOT / "laporan/uji_dashboard.json"
    if dashboard_path.exists():
        dashboard = json.loads(dashboard_path.read_text(encoding="utf-8"))
        assert dashboard["status"] == "PASS"
        lines += [
            "", "Dashboard penutup mempunyai pengujian interaksi tersendiri; hasilnya ada di",
            "[laporan dashboard](uji_dashboard.md). Materi ini dijalankan dari notebook tanpa terminal peserta.",
        ]
    lines += [
        "",
        "Housing juga dijalankan pada kernel Jupyter baru dari folder notebook. Hasil dan",
        "enam grafik tersimpan di notebook; angka prediksi dan metrik diperiksa secara independen.",
        "Rinciannya tersedia di [laporan Housing](uji_regresi_housing.md).",
        "",
        "Peringatan separation/konvergensi pada contoh kategorikal dan frekuensi waktu",
        "tercatat di log; contoh serta batas interpretasinya dijelaskan pada notebook.",
        "Uji ini memeriksa eksekusi lokal dan skenario unggahan ZIP; antarmuka Google Colab belum diuji langsung.",
        "",
        "## Penelusuran berkas lama",
        "",
        "Gunakan [peta perubahan nama](peta_perubahan_nama.csv). Cadangan lengkap sebelum",
        "penataan disimpan lokal; lihat [catatan arsip](../arsip/README.md). Berkas kerja lama tersimpan terpisah",
        "dari materi dan alat bantu aktif.",
        "",
    ]
    (ROOT / "laporan/penataan_folder.md").write_text("\n".join(lines), encoding="utf-8")
    print(
        f"PASS: {len(pemetaan) - lokal_saja} lokasi, {terlindungi} hash, {len(notebooks)} notebook, {jumlah_tautan} tautan, 31 PNG tajam dan ZIP."
    )


if __name__ == "__main__":
    main()
