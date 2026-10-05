"""Jalankan semua notebook (.py) untuk memastikan tidak ada error.

Marka sel markdown sudah berupa komentar Python, jadi file .py bisa
dieksekusi langsung setelah baris magic (%pip) diganti pass.

Jalankan: python scripts/run_notebooks.py
Log lengkap: scripts/run_output.log
"""

import contextlib
import io
import os
import sys
import traceback
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

ROOT = Path(__file__).resolve().parent.parent
os.chdir(ROOT)


def jalankan(path):
    kode = path.read_text(encoding="utf-8")
    baris = ["pass" if ln.lstrip().startswith("%") else ln for ln in kode.splitlines()]
    ns = {"__name__": "__main__", "__file__": str(path)}
    exec(compile("\n".join(baris), str(path), "exec"), ns)


def main():
    folder = [Path(f) for f in sys.argv[1:]] or [Path("hari-1-dosen"), Path("hari-2-mahasiswa")]
    files = [p for f in folder for p in sorted(f.rglob("*.py"))]
    log = io.StringIO()
    gagal = []
    for path in files:
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                jalankan(path)
            status = "PASS"
        except Exception:
            status = "FAIL"
            buf.write("\n" + traceback.format_exc())
            gagal.append(path)
        log.write(f"\n{'=' * 70}\n{status} {path}\n{'=' * 70}\n{buf.getvalue()}")
        print(f"{status} {path}")

    (Path(__file__).parent / "run_output.log").write_text(log.getvalue(), encoding="utf-8")
    print(f"\n{len(files) - len(gagal)}/{len(files)} notebook berjalan tanpa error.")
    if gagal:
        print("Gagal:")
        for p in gagal:
            print(" -", p)
    return 1 if gagal else 0


if __name__ == "__main__":
    sys.exit(main())
