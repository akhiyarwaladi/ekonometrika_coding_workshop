"""Buat PDF dengan teks vektor dan 31 PNG 6K untuk slide regresi.

Jalankan dari folder utama: python alat_bantu/ekspor_slide_tajam.py
PDF/PNG sumber tidak ditimpa. Blok kode, tabel kecil, dan rumus dibangun ulang.
Contoh evaluasi halaman 27-28 disesuaikan dengan notebook Housing yang diuji.
"""

from pathlib import Path
from io import BytesIO
import ast
import hashlib
import json
import re

import fitz
import numpy as np
import pandas as pd
from PIL import Image
from pygments import lex
from pygments.lexers import PythonLexer
from pygments.token import Token
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

from kemas_png import kemas_png

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "slide/02_regresi_machine_learning.pdf"
PDF_OUT = ROOT / "slide/03_regresi_machine_learning_tajam.pdf"
PNG_OUT = ROOT / "slide/png_regresi_tajam"
PNG_LAMA = ROOT / "alat_bantu/arsip/slide/png_regresi_300_dpi"
DPI = 600
BG = (247 / 255, 247 / 255, 247 / 255)

FONT_DIR = Path("C:/Windows/Fonts")
pdfmetrics.registerFont(TTFont("Kode", str(FONT_DIR / "consola.ttf")))
pdfmetrics.registerFont(TTFont("Teks", str(FONT_DIR / "arial.ttf")))
pdfmetrics.registerFont(TTFont("Tebal", str(FONT_DIR / "arialbd.ttf")))

CODE = {
    20: """from sklearn.model_selection import train_test_split

feature = data.drop(columns='Curah_Hujan')
target = data[['Curah_Hujan']]

feature_train, feature_test, target_train, target_test = train_test_split(
    feature, target, test_size=0.20, random_state=42
)
""",
    21: """from sklearn.linear_model import LinearRegression

# Tentukan model yang akan digunakan
linreg = LinearRegression()

# Train model
linreg.fit(feature_train, target_train)
""",
    24: """from statsmodels.stats.outliers_influence import variance_inflation_factor as vif
from statsmodels.tools.tools import add_constant

X_vif = add_constant(X_train)

vif_df = pd.DataFrame([vif(X_vif.values, i)
    for i in range(X_vif.shape[1])],
    index=X_vif.columns).reset_index()
vif_df.columns = ['feature', 'vif_score']
vif_df = vif_df.loc[vif_df.feature != 'const']
vif_df
""",
    25: """plt.figure(figsize=(10, 7))
sns.heatmap(
    df.corr(), annot=True, fmt='.2f'
)
""",
    27: """from sklearn.metrics import r2_score
prediksi_ringkas = model_ringkas.predict(X_test_ringkas)
r2_score(y_test, prediksi_ringkas)
""",
    28: """import numpy as np
from sklearn.metrics import mean_squared_error
prediksi_ringkas = model_ringkas.predict(X_test_ringkas)
rmse = np.sqrt(mean_squared_error(y_test, prediksi_ringkas))
rmse
""",
}


def white_rect(x0, y0, x1, y1):
    return f"{x0 / 720:.10f} {1 - y1 / 405:.10f} {(x1 - x0) / 720:.10f} {(y1 - y0) / 405:.10f} re f\n"


def white_polygon(points):
    ops = [
        f"{x / 720:.10f} {1 - y / 405:.10f} " + ("m" if i == 0 else "l")
        for i, (x, y) in enumerate(points)
    ]
    return "\n".join(ops) + "\nh f\n"


def mask_for(number):
    mask = "\nq\n1 1 1 rg\n"
    if number == 1:
        mask += (
            white_rect(0, 0, 720, 34)
            + white_rect(660, 0, 720, 47)
            + white_rect(0, 386, 720, 405)
        )
    elif number == 31:
        mask += (
            white_rect(0, 0, 720, 44)
            + white_rect(0, 372, 720, 405)
            + white_rect(0, 364, 175, 405)
        )
    elif number in {2, 3, 7, 10, 16, 26}:
        mask += white_rect(0, 0, 720, 44) + white_rect(0, 360, 720, 405)
        mask += white_polygon([(0, 285), (150, 405), (0, 405)])
    else:
        mask += white_rect(0, 0, 720, 44) + white_polygon(
            [(565, 0), (720, 0), (720, 125)]
        )
        mask += white_rect(0, 358, 720, 405)
    return mask + "Q\n"


def hide_image(doc, page, xref):
    names = [im[7] for im in page.get_images(full=True) if im[0] == xref]
    assert names, (page.number + 1, xref)
    count = 0
    for stream in page.get_contents():
        data = doc.xref_stream(stream)
        for name in names:
            data, n = re.subn(rb"/" + re.escape(name.encode()) + rb"\s+Do\b", b"", data)
            count += n
        doc.update_stream(stream, data)
    assert count, (page.number + 1, xref)


def paint(page, rect, draw):
    rect = fitz.Rect(rect)
    memory = BytesIO()
    c = canvas.Canvas(memory, pagesize=(rect.width, rect.height), pageCompression=1)
    draw(c, rect.width, rect.height)
    c.save()
    fragment = fitz.open(stream=memory.getvalue(), filetype="pdf")
    page.show_pdf_page(rect, fragment, 0, keep_proportion=False)
    fragment.close()


def token_color(token):
    if token in Token.Comment:
        return (0.10, 0.43, 0.12)
    if token in Token.Keyword or token in Token.Name.Namespace:
        return (0.48, 0.04, 0.65)
    if token in Token.Literal.String:
        return (0.65, 0.12, 0.14)
    if token in Token.Literal.Number:
        return (0.03, 0.28, 0.62)
    return (0.06, 0.07, 0.08)


def draw_code(c, width, height, code, output=None, max_size=11):
    margin = 5
    code = code.strip("\n")
    lines = code.splitlines()
    widest = max(pdfmetrics.stringWidth(line, "Kode", 1) for line in lines)
    rows = len(lines) + (2 if output is not None else 0)
    size = min(
        max_size, (width - 2 * margin) / widest, (height - 2 * margin) / (rows * 1.3)
    )
    assert size >= 6.5, (size, code)
    c.setFillColorRGB(*BG)
    c.rect(0, 0, width, height, stroke=0, fill=1)
    y = height - margin - size
    for line in lines:
        x = margin
        for token, text in lex(line, PythonLexer()):
            text = text.rstrip("\n")
            if not text:
                continue
            c.setFillColorRGB(*token_color(token))
            c.setFont("Kode", size)
            c.drawString(x, y, text)
            x += pdfmetrics.stringWidth(text, "Kode", size)
        y -= size * 1.3
    if output is not None:
        c.setFillColorRGB(1, 1, 1)
        c.rect(0, 0, width, y + size * 0.9, stroke=0, fill=1)
        c.setFillColorRGB(0.06, 0.07, 0.08)
        c.setFont("Kode", size)
        c.drawString(margin, y - size * 0.3, output)


def draw_table(c, width, height, headers, rows, proportions, highlights=()):
    row_h = height / (len(rows) + 1)
    col_widths = [width * f for f in proportions]
    size = min(11, row_h * 0.45)
    for r, values in enumerate([headers] + rows):
        top = height - r * row_h
        c.setFillColorRGB(*(BG if r % 2 else (1, 1, 1)))
        c.rect(0, top - row_h, width, row_h, stroke=0, fill=1)
        c.setFont("Tebal" if r == 0 else "Teks", size)
        c.setFillColorRGB(0.05, 0.06, 0.07)
        x = 0
        for value, col_w in zip(values, col_widths):
            assert (
                pdfmetrics.stringWidth(str(value), "Tebal" if r == 0 else "Teks", size)
                < col_w - 2
            ), (value, col_w, size)
            c.drawCentredString(x + col_w / 2, top - row_h * 0.66, str(value))
            x += col_w
    c.setStrokeColorRGB(0.75, 0.78, 0.80)
    c.setLineWidth(0.4)
    c.line(0, height - row_h, width, height - row_h)
    for row in highlights:
        c.setStrokeColorRGB(0.12, 0.23, 0.37)
        c.setLineWidth(1.3)
        c.rect(
            sum(col_widths[:-1]),
            height - (row + 2) * row_h,
            col_widths[-1],
            row_h,
            stroke=1,
            fill=0,
        )


def draw_math(page, rect, formula):
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_agg import FigureCanvasAgg

    fig = Figure(figsize=(6, 1.4))
    FigureCanvasAgg(fig)
    fig.text(0.5, 0.5, formula, fontsize=24, ha="center", va="center")
    memory = BytesIO()
    fig.savefig(
        memory, format="pdf", transparent=True, bbox_inches="tight", pad_inches=0.015
    )
    fragment = fitz.open(stream=memory.getvalue(), filetype="pdf")
    page.show_pdf_page(fitz.Rect(rect), fragment, 0, keep_proportion=True)
    fragment.close()


def repair_arrows(page):
    arrows = []
    for block in page.get_text("rawdict")["blocks"]:
        for line in block.get("lines", []):
            for span in line["spans"]:
                for char in span["chars"]:
                    if char["c"] == "🡪":
                        arrows.append(fitz.Rect(char["bbox"]))
    for rect in arrows:
        page.add_redact_annot(rect, fill=BG)
    if arrows:
        page.apply_redactions(images=0, graphics=0, text=0)
    for rect in arrows:
        x0, x1 = rect.x0 + 0.5, rect.x1 - 0.5
        y = (rect.y0 + rect.y1) / 2
        page.draw_line((x0, y), (x1, y), color=(0, 0, 0), width=0.8)
        page.draw_line((x1 - 2.5, y - 2.1), (x1, y), color=(0, 0, 0), width=0.8)
        page.draw_line((x1 - 2.5, y + 2.1), (x1, y), color=(0, 0, 0), width=0.8)


def sample_metrics():
    data = pd.read_csv(ROOT / "data/harga_rumah_boston.csv")
    X = data.drop(columns=["MEDV", "RAD"])
    X_train, X_test_ringkas, y_train, y_test = train_test_split(
        X, data["MEDV"], test_size=0.20, random_state=42
    )
    model_ringkas = LinearRegression().fit(X_train, y_train)
    predicted = model_ringkas.predict(X_test_ringkas)
    return {
        "r2": r2_score(y_test, predicted),
        "rmse": np.sqrt(mean_squared_error(y_test, predicted)),
    }, locals()


def metric_page(page, number, metrics):
    # Hilangkan teks lama dari badan halaman, sambil mempertahankan judul vektor.
    page.add_redact_annot(fitz.Rect(74, 77, 710, 358), fill=BG)
    page.apply_redactions(images=0, graphics=0, text=0)

    def body(c, w, h):
        def text(y, value, size=12.5, bold=False):
            c.setFillColorRGB(0.07, 0.08, 0.08)
            c.setFont("Tebal" if bold else "Teks", size)
            c.drawString(4, h - y - size, value)

        if number == 27:
            text(
                2,
                "R² mengukur proporsi variasi target yang dijelaskan model pada data yang dinilai.",
                13,
            )
            text(32, "- R² = 1: seluruh variasi target pada data tersebut terjelaskan.")
            text(
                52,
                "- R² = 0: setara dengan selalu memprediksi rata-rata target pada data tersebut.",
            )
            text(
                72,
                "- R² dapat negatif jika hasilnya lebih buruk daripada pembanding rata-rata.",
            )
            text(103, "Contoh Housing: model tanpa RAD, pada data test", 11.5, True)
            c.saveState()
            c.translate(0, h - 134 - 96)
            draw_code(c, w - 5, 96, CODE[27], f"{metrics['r2']:.16f}", 11.5)
            c.restoreState()
            text(
                238,
                f"Pada test ini, sekitar {metrics['r2'] * 100:.2f}% variasi MEDV terjelaskan oleh model.",
                11.5,
            )
            text(256, "R² tidak dibaca sebagai persentase prediksi yang benar.", 11.5)
        else:
            text(
                2,
                "Evaluasi dilakukan pada data test yang tidak digunakan untuk fit model.",
                13,
            )
            text(87, "Contoh Housing: model tanpa RAD, pada data test", 11.5, True)
            c.saveState()
            c.translate(0, h - 112 - 105)
            draw_code(c, w - 5, 105, CODE[28], f"{metrics['rmse']:.15f}", 10.5)
            c.restoreState()
            text(
                229,
                f"RMSE = {metrics['rmse']:.3f} dalam satuan MEDV (ribuan dolar AS historis).",
                11.5,
            )
            text(247, "Ini ukuran besar error prediksi secara keseluruhan.", 11.5)
            text(261, "RMSE tidak langsung membentuk interval prediksi ± RMSE.", 11.5)

    paint(page, (78, 79, 704, 356), body)
    if number == 28:
        draw_math(
            page,
            (83, 115, 370, 157),
            r"$RMSE=\sqrt{\frac{1}{n}\sum_{i=1}^{n}(y_i-\hat{y}_i)^2}$",
        )


def main():
    PNG_OUT.mkdir(parents=True, exist_ok=True)
    source_hash = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    originals = {
        p.name: hashlib.sha256(p.read_bytes()).hexdigest()
        for p in PNG_LAMA.glob("*.png")
    }
    doc = fitz.open(SOURCE)
    assert len(doc) == 31
    image_rects = {
        (i + 1, im["xref"]): fitz.Rect(im["bbox"])
        for i, page in enumerate(doc)
        for im in page.get_image_info(xrefs=True)
    }
    for i, page in enumerate(doc):
        refs = page.get_contents()
        assert len(refs) == 1
        data = doc.xref_stream(refs[0])
        match = re.search(rb"/Image\d+\s+Do", data)
        assert match
        doc.update_stream(
            refs[0],
            data[: match.end()] + mask_for(i + 1).encode("ascii") + data[match.end() :],
        )

    # Ganti screenshot kode dengan teks berwarna yang tetap berupa vektor.
    for number, xref in [(20, 203), (21, 210), (24, 232), (25, 242)]:
        page = doc[number - 1]
        rect = image_rects[(number, xref)]
        hide_image(doc, page, xref)
        if number == 24:
            rect.x1 = 538
        paint(page, rect, lambda c, w, h, n=number: draw_code(c, w, h, CODE[n]))

    tables = [
        (
            19,
            196,
            ["", "Temperature", "Curah_Hujan"],
            [
                [i, a, b]
                for i, (a, b) in enumerate(
                    [(35, 85), (32, 70), (33, 75), (35, 80), (36, 85)]
                )
            ],
            [0.13, 0.43, 0.44],
            (),
        ),
        (
            21,
            211,
            ["", "feature", "coefficient"],
            [[0, "intercept", "2.3842"], [1, "Temperature", "1.2835"]],
            [0.11, 0.49, 0.40],
            (),
        ),
        (
            24,
            233,
            ["", "feature", "vif_score"],
            [
                [i + 1, n, v]
                for i, (n, v) in enumerate(
                    [
                        ("CRIM", "1.682416"),
                        ("ZN", "2.273766"),
                        ("INDUS", "4.241354"),
                        ("CHAS", "1.089018"),
                        ("NOX", "4.452894"),
                        ("RM", "2.085863"),
                        ("AGE", "3.163989"),
                        ("DIS", "4.033996"),
                        ("RAD", "7.100781"),
                        ("TAX", "9.157594"),
                        ("PTRATIO", "1.814771"),
                        ("B", "1.333589"),
                        ("LSTAT", "3.108827"),
                    ]
                )
            ],
            [0.13, 0.40, 0.47],
            (8, 9),
        ),
    ]
    for number, xref, headers, rows, proportions, highlights in tables:
        page = doc[number - 1]
        rect = image_rects[(number, xref)]
        hide_image(doc, page, xref)
        if number == 24:
            # Penanda biru lama adalah objek vektor terpisah dari screenshot tabel.
            page.draw_rect(
                fitz.Rect(rect.x0 - 1, rect.y0 - 1, rect.x1 + 4, rect.y1 + 1),
                fill=(1, 1, 1),
                color=None,
            )
        paint(
            page,
            rect,
            lambda c, w, h, hs=headers, rs=rows, ps=proportions, hi=highlights: draw_table(
                c, w, h, hs, rs, ps, hi
            ),
        )

    formulas = [
        (13, 129, r"$\min\left\{\sum_{i=1}^{n}(y_i-\hat{y}_i)^2\right\}$"),
        (14, 143, r"$Y=\beta_0+\beta_1X_1+\epsilon$"),
        (23, 225, r"$VIF_i=\frac{1}{1-R_i^2}$"),
    ]
    for number, xref, formula in formulas:
        page = doc[number - 1]
        hide_image(doc, page, xref)
        if number == 13:
            # PDF asal menumpuk dua gambar rumus; hilangkan keduanya.
            hide_image(doc, page, 128)
        rect = image_rects[(number, xref)]
        if number == 14:
            rect = fitz.Rect(250, 121, 440, 145)
        draw_math(page, rect, formula)
    repair_arrows(doc[22])

    metrics, namespace = sample_metrics()
    for code in CODE.values():
        ast.parse(code)
    # Verifikasi dua contoh metrik memakai objek model dari perhitungan yang sama.
    for number, key in [(27, "r2"), (28, "rmse")]:
        exec(CODE[number], namespace)
        value = (
            r2_score(namespace["y_test"], namespace["prediksi_ringkas"])
            if number == 27
            else namespace["rmse"]
        )
        np.testing.assert_allclose(value, metrics[key])
    for number, xrefs in [(27, [255]), (28, [262, 263])]:
        for xref in xrefs:
            hide_image(doc, doc[number - 1], xref)
        metric_page(doc[number - 1], number, metrics)

    doc.set_metadata(
        {
            "title": "Supervised Learning - Regression (I): versi tajam",
            "subject": "Kode dan tabel vektor; header/footer putih; metrik Housing terverifikasi",
            "creator": "Ekspor tutorial ekonometrika",
        }
    )
    doc.save(PDF_OUT, garbage=4, deflate=True)
    doc.close()
    doc = fitz.open(PDF_OUT)
    for i, page in enumerate(doc):
        output = PNG_OUT / f"halaman_{i+1:02d}.png"
        pix = page.get_pixmap(dpi=DPI, alpha=False, colorspace=fitz.csRGB)
        assert (pix.width, pix.height) == (6000, 3375)
        pix.save(output)
        with Image.open(output) as picture:
            assert picture.info["dpi"][0] > 599
            picture.verify()
        print(f"{output.name}: 6000 x 3375", flush=True)
    assert len(list(PNG_OUT.glob("*.png"))) == 31
    zip_out = kemas_png()
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == source_hash
    assert originals == {
        p.name: hashlib.sha256(p.read_bytes()).hexdigest()
        for p in PNG_LAMA.glob("*.png")
    }
    manifest = {
        "pdf_sumber": SOURCE.relative_to(ROOT).as_posix(),
        "sha256_sumber": source_hash,
        "pdf_tajam": PDF_OUT.relative_to(ROOT).as_posix(),
        "folder_png": PNG_OUT.relative_to(ROOT).as_posix(),
        "zip_png": zip_out.relative_to(ROOT).as_posix(),
        "halaman": 31,
        "piksel": [6000, 3375],
        "dpi": DPI,
        "halaman_kode_vektor": list(CODE),
        "halaman_tabel_vektor": [19, 21, 24],
        "halaman_rumus_vektor": [13, 14, 23, 28],
        "metrik_housing_tanpa_RAD": metrics,
        "sumber_dan_png_lama_tetap": True,
    }
    (ROOT / "alat_bantu/laporan/ekspor_slide_tajam.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )
    print(
        "PASS: 31 PNG 6K dan ZIP; kode vektor; sumber dan PNG lama tidak berubah.",
        flush=True,
    )


if __name__ == "__main__":
    main()
