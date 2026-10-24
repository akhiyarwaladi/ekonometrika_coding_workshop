"""Periksa 31 PNG tajam dan buat alat_bantu/paket/png_regresi_tajam.zip.

Jalankan dari folder utama: python alat_bantu/kemas_png.py
ZIP hanya berisi halaman_01.png sampai halaman_31.png.
"""

from pathlib import Path
from zipfile import ZIP_STORED, ZipFile

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent


def kemas_png():
    gambar = sorted((ROOT / "slide/png_regresi_tajam").glob("*.png"))
    if len(gambar) != 31:
        raise ValueError("Folder PNG tajam harus memuat tepat 31 gambar.")

    for nomor, path in enumerate(gambar, 1):
        if path.name != f"halaman_{nomor:02d}.png":
            raise ValueError(f"Nama PNG tidak sesuai urutan: {path.name}")
        with Image.open(path) as png:
            if png.size != (6000, 3375) or png.mode != "RGB":
                raise ValueError(f"Ukuran atau mode warna tidak sesuai: {path.name}")
            if abs(png.info.get("dpi", (0, 0))[0] - 600) >= 1:
                raise ValueError(f"Metadata dpi tidak sesuai: {path.name}")
            png.verify()

    tujuan = ROOT / "alat_bantu/paket/png_regresi_tajam.zip"
    tujuan.parent.mkdir(parents=True, exist_ok=True)
    sementara = tujuan.with_suffix(".tmp")
    with ZipFile(sementara, "w", compression=ZIP_STORED) as paket:
        for path in gambar:
            paket.write(path, path.name)
    sementara.replace(tujuan)
    print(f"{tujuan.name}: 31 PNG, masing-masing 6000 x 3375 piksel dan 600 dpi.")
    return tujuan


if __name__ == "__main__":
    kemas_png()
