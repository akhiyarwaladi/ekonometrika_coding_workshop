"""Konversi file .py format persen (jupytext style) ke .ipynb untuk Colab.

Marka sel:
    # %% [markdown]  -> sel markdown (baris komentar '# ' dilepas)
    # %%             -> sel kode

Jalankan: python alat_bantu/konversi_notebook.py [folder atau file ...]
Tanpa argumen: seluruh materi dan kunci jawaban. Output lama akan dikosongkan.
"""

import json
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SUMBER = ROOT / "alat_bantu/sumber_notebook"


def sumber_notebook(notebook):
    return SUMBER / Path(notebook).resolve().relative_to(ROOT).with_suffix(".py")


def notebook_dari_sumber(sumber):
    return ROOT / Path(sumber).resolve().relative_to(SUMBER).with_suffix(".ipynb")


def parse_sel(teks):
    """Pecah isi .py jadi daftar (tipe, baris)."""
    sel = []
    tipe, buf = None, []

    def tutup():
        if tipe is not None:
            sel.append((tipe, buf[:]))

    for baris in teks.splitlines():
        if baris.startswith("# %% [markdown]"):
            tutup()
            buf.clear()
            tipe = "markdown"
        elif baris.startswith("# %%"):
            tutup()
            buf.clear()
            tipe = "code"
        elif tipe is not None:
            buf.append(baris)
    tutup()
    return sel


def ke_sumber(tipe, baris):
    if tipe == "markdown":
        isi = []
        for b in baris:
            if b.startswith("# "):
                isi.append(b[2:])
            elif b.strip() == "#":
                isi.append("")
            else:
                isi.append(b)
        return [x + "\n" for x in isi]
    return [x + "\n" for x in baris]


def konversi(path):
    sel = parse_sel(path.read_text(encoding="utf-8"))
    cells = []
    for numero, (tipe, baris) in enumerate(sel):
        if not baris or all(not b.strip() for b in baris):
            continue
        src = ke_sumber(tipe, baris)
        cell_id = hashlib.sha256(f"{path.stem}:{numero}".encode()).hexdigest()[:12]
        if tipe == "markdown":
            cells.append(
                {"cell_type": "markdown", "id": cell_id, "metadata": {}, "source": src}
            )
        else:
            cells.append(
                {
                    "cell_type": "code",
                    "id": cell_id,
                    "execution_count": None,
                    "metadata": {},
                    "outputs": [],
                    "source": src,
                }
            )
    nb = {
        "cells": cells,
        "metadata": {
            "colab": {"provenance": [], "toc_visible": True},
            "kernelspec": {"display_name": "Python 3", "name": "python3"},
            "language_info": {"name": "python"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    out = notebook_dari_sumber(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{path} -> {out.name} ({len(cells)} sel)")


def main():
    target = [Path(a).resolve() for a in sys.argv[1:]] or [SUMBER]
    for item in target:
        if not item.is_relative_to(SUMBER):
            item = sumber_notebook(item)
            if item.suffix == ".py" and not item.exists():
                item = item.with_suffix("")
        paths = (
            sorted(item.rglob("*.py")) if item.is_dir() else [item.with_suffix(".py")]
        )
        for path in paths:
            konversi(path)


if __name__ == "__main__":
    main()
