"""Buat ulang salinan data offline opsional dari CSV aktif di folder data/.

Jalankan setelah mengubah CSV atau metode_lanjutan.py:
    python alat_bantu/kemas_data.py
"""

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parent.parent


def main():
    berkas = sorted((ROOT / "data").glob("*.csv"))
    berkas.append(ROOT / "alat_bantu" / "metode_lanjutan.py")
    tujuan = ROOT / "alat_bantu/paket" / "data_tutorial.zip"
    tujuan.parent.mkdir(parents=True, exist_ok=True)
    sementara = tujuan.with_suffix(".tmp")
    with ZipFile(sementara, "w", compression=ZIP_DEFLATED) as paket:
        for path in berkas:
            paket.write(path, path.relative_to(ROOT).as_posix())
    sementara.replace(tujuan)
    print(f"{tujuan.name}: {len(berkas) - 1} CSV dan metode_lanjutan.py")


if __name__ == "__main__":
    main()
