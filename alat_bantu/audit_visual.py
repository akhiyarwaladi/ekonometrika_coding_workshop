"""Periksa gambar notebook dan buat lembar tinjauan lokal tanpa menambah bahan peserta."""
import argparse
import base64
import io
import json
from pathlib import Path

import nbformat
from PIL import Image, ImageDraw, ImageFont

from laporan_bersama import simpan_ringkasan

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "alat_bantu/arsip/penyempurnaan_pemula/tinjauan_visual"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selesai-ditinjau", action="store_true", help="Catat setelah seluruh lembar benar-benar ditinjau.")
    args = parser.parse_args()
    paths = sorted((ROOT / "materi").rglob("*.ipynb")) + sorted((ROOT / "pengajar/kunci_jawaban").glob("*.ipynb"))
    OUT.mkdir(parents=True, exist_ok=True)
    items, notebooks, issues = [], [], []
    for path in paths:
        nb = nbformat.read(path, as_version=4)
        nbformat.validate(nb)
        count = 0
        for i, cell in enumerate(nb.cells):
            if cell.cell_type != "code":
                continue
            assert cell.execution_count is not None, (path, i)
            assert not [o for o in cell.outputs if o.output_type == "error"], (path, i)
            for o in cell.outputs:
                data = o.get("data", {})
                if "image/png" not in data:
                    continue
                picture = Image.open(io.BytesIO(base64.b64decode(data["image/png"]))).convert("RGB")
                assert picture.width >= 400 and picture.height >= 250, (path, i, picture.size)
                count += 1
                if not (i + 1 < len(nb.cells) and nb.cells[i + 1].cell_type == "markdown" and any(t in nb.cells[i + 1].source.lower() for t in ["baca grafik", "cara membaca"])):
                    issues.append({"notebook": path.relative_to(ROOT).as_posix(), "sel": i, "masalah": "Petunjuk membaca belum langsung sesudah grafik."})
                items.append((f"{path.parent.name}/{path.stem} | grafik {count}", picture))
        assert count > 0, path
        notebooks.append({"notebook": path.relative_to(ROOT).as_posix(), "gambar": count})
    font_path = Path("C:/Windows/Fonts/arial.ttf")
    font = ImageFont.truetype(str(font_path), 18) if font_path.exists() else ImageFont.load_default()
    sheets = []
    for start in range(0, len(items), 6):
        page = Image.new("RGB", (1800, 1650), "#eeeeee")
        draw = ImageDraw.Draw(page)
        for j, (label, picture) in enumerate(items[start:start + 6]):
            x, y = (j % 2) * 900, (j // 2) * 550
            draw.text((x + 12, y + 10), label, fill="black", font=font)
            copy = picture.copy()
            copy.thumbnail((880, 510))
            page.paste(copy, (x + (900 - copy.width) // 2, y + 38 + (510 - copy.height) // 2))
        target = OUT / f"lembar_{start // 6 + 1:02d}.png"
        page.save(target)
        sheets.append(target.relative_to(ROOT).as_posix())
    report = {"status": "PASS" if not issues else "PERLU PERBAIKAN", "jumlah_notebook": len(paths),
              "jumlah_gambar": len(items), "tinjauan_tampilan": "PASS" if args.selesai_ditinjau else "Belum dicatat",
              "notebook": notebooks, "masalah": issues, "lembar_lokal": sheets}
    (ROOT / "alat_bantu/laporan/audit_visual.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    simpan_ringkasan()
    print(f"{report['status']}: {len(paths)} notebook, {len(items)} gambar, {len(sheets)} lembar tinjauan lokal.")
    for item in issues:
        print(item)
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
