"""Jalankan notebook Housing di kernel baru dan simpan hasil serta laporan.

Jalankan dari folder proyek: python alat_bantu/uji_regresi_housing.py
Paket tambahan untuk pemeriksaan: nbclient, nbformat, dan ipykernel.
"""

from pathlib import Path
import ast
import hashlib
import json
import os
import sys
import textwrap

import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager
from konversi_notebook import ke_sumber, parse_sel

ROOT = Path(__file__).resolve().parent.parent
NOTEBOOK = ROOT / "materi/03_regresi_housing/01_regresi_housing.ipynb"
DATA = ROOT / "data/housing.csv"

CHECK = r"""
import json
import sklearn
import statsmodels

# Pasangan observasi tetap benar setelah pembagian, imputasi, dan korelasi.
assert X_train_bersih.index.equals(y_train.index)
assert X_test_bersih.index.equals(y_test.index)
assert data_train["MEDV"].equals(y_train.rename("MEDV"))
assert len(data_train) == len(X_train) == 404
assert len(X_test) == 102
assert set(X_train.index).isdisjoint(X_test.index)
assert set(X_train.index) | set(X_test.index) == set(data.index)
assert "MEDV" not in X_train.columns
assert data_train.isna().sum().sum() == 0

# Imputer menggunakan median train dan pipeline konsisten dengan versi manual.
np.testing.assert_allclose(pengisi_kosong.statistics_, X_train.median().to_numpy())
np.testing.assert_allclose(prediksi_otomatis, prediksi_berganda)
np.testing.assert_allclose(model_otomatis.predict(data_baru), prediksi_baru)
assert np.isfinite(prediksi_baru).all()
assert data_baru["CRIM"].isna().sum() == 1
assert data_baru_bersih.isna().sum().sum() == 0
assert "RAD" not in X_train_ringkas.columns and "TAX" in X_train_ringkas.columns

# Periksa OLS secara independen dengan penyelesaian least squares NumPy.
desain_train = np.column_stack([np.ones(len(X_train_bersih)), X_train_bersih.to_numpy()])
desain_test = np.column_stack([np.ones(len(X_test_bersih)), X_test_bersih.to_numpy()])
beta_lstsq = np.linalg.lstsq(desain_train, y_train.to_numpy(), rcond=None)[0]
np.testing.assert_allclose(desain_test @ beta_lstsq, prediksi_berganda, atol=1e-8)

# Periksa definisi metrik dan batas pemisahan validasi.
error_manual = y_test.to_numpy() - prediksi_berganda
rmse_manual = np.sqrt(np.mean(error_manual ** 2))
r2_manual = 1 - np.sum(error_manual ** 2) / np.sum((y_test.to_numpy() - y_test.mean()) ** 2)
np.testing.assert_allclose(rmse_manual, rmse_berganda)
np.testing.assert_allclose(r2_manual, r2_berganda)
assert set(RM_latih.index).isdisjoint(RM_validasi.index)
assert set(RM_latih.index).isdisjoint(X_test.index)
assert set(RM_validasi.index).isdisjoint(X_test.index)
assert set(RM_latih.index) | set(RM_validasi.index) == set(X_train.index)
assert rmse_train_lentur < rmse_train_kuadrat
assert rmse_validasi_lentur > rmse_validasi_kuadrat

print(json.dumps({
    "rows": len(data),
    "columns": len(data.columns),
    "missing": int(data.isna().sum().sum()),
    "duplicates": int(data.duplicated().sum()),
    "train": len(X_train),
    "test": len(X_test),
    "evaluation": evaluasi.to_dict(orient="records"),
    "complexity": perbandingan_kompleksitas.to_dict(orient="records"),
    "new_predictions": prediksi_baru.tolist(),
    "pandas": pd.__version__,
    "numpy": np.__version__,
    "sklearn": sklearn.__version__,
    "statsmodels": statsmodels.__version__,
    "checks": "PASS"
}, indent=2))
"""


def main():
    original_hash = hashlib.sha256(DATA.read_bytes()).hexdigest()
    nb = nbformat.read(NOTEBOOK, as_version=4)
    source_cells = [
        (kind, "".join(ke_sumber(kind, lines)))
        for kind, lines in parse_sel(
            NOTEBOOK.with_suffix(".py").read_text(encoding="utf-8")
        )
        if any(line.strip() for line in lines)
    ]
    assert len(source_cells) == len(nb.cells)
    for cell, (kind, source) in zip(nb.cells, source_cells):
        assert cell.cell_type == kind and cell.source.strip() == source.strip()
        cell.source = source
    code_cells = [c for c in nb.cells if c.cell_type == "code"]
    difficult = (
        ast.For,
        ast.While,
        ast.FunctionDef,
        ast.ClassDef,
        ast.Lambda,
        ast.ListComp,
        ast.DictComp,
        ast.SetComp,
        ast.GeneratorExp,
        ast.MatMult,
    )
    for cell in code_cells:
        assert not any(
            isinstance(n, difficult) for n in ast.walk(ast.parse(cell.source))
        )
    # Sel pemeriksaan tidak disimpan ke materi peserta.
    nb.cells.append(nbformat.v4.new_code_cell(textwrap.dedent(CHECK).strip()))
    os.environ["MPLBACKEND"] = "module://matplotlib_inline.backend_inline"
    manager = KernelManager(kernel_name="python3")
    manager.kernel_spec.argv = [
        sys.executable,
        "-m",
        "ipykernel_launcher",
        "-f",
        "{connection_file}",
    ]
    client = NotebookClient(
        nb,
        timeout=180,
        resources={"metadata": {"path": str(NOTEBOOK.parent)}},
        km=manager,
    )
    try:
        client.execute()
    finally:
        if manager.has_kernel:
            manager.shutdown_kernel(now=True)
        if client.kc is not None:
            client.kc.stop_channels()
    check_cell = nb.cells.pop()
    check_text = "".join(
        o.get("text", "") for o in check_cell.outputs if o.output_type == "stream"
    )
    results = json.loads(check_text)
    assert hashlib.sha256(DATA.read_bytes()).hexdigest() == original_hash
    errors = [
        o
        for c in nb.cells
        if c.cell_type == "code"
        for o in c.outputs
        if o.output_type == "error"
    ]
    assert not errors
    pictures = [
        o.data["image/png"]
        for c in nb.cells
        if c.cell_type == "code"
        for o in c.outputs
        if o.output_type in ("display_data", "execute_result") and "image/png" in o.data
    ]
    assert len(pictures) == 6, len(pictures)
    nbformat.validate(nb)
    nbformat.write(nb, NOTEBOOK)

    temp = ROOT / "gambar/regresi_housing"
    temp.mkdir(parents=True, exist_ok=True)
    (ROOT / "laporan/hasil_uji_regresi_housing.json").write_text(
        json.dumps(results, indent=2), encoding="utf-8"
    )
    import base64

    for i, picture in enumerate(pictures, 1):
        (temp / f"grafik_{i:02d}.png").write_bytes(base64.b64decode(picture))
    lines = [
        "# Hasil pemeriksaan notebook Regression (I)",
        "",
        "Notebook: [01_regresi_housing.ipynb](../materi/03_regresi_housing/01_regresi_housing.ipynb).",
        "Data: [housing.csv](../data/housing.csv), dibaca lokal tanpa Google Drive atau unduhan tambahan.",
        "Folder kerja awal: folder notebook sendiri; sel persiapan menemukan folder data proyek.",
        f"Status: **{len(code_cells)}/{len(code_cells)} sel kode berjalan pada kernel baru tanpa error.**",
        f"Notebook berisi {len(nb.cells)} sel dan {len(pictures)} grafik; seluruh output tersimpan.",
        "",
        "## Data dan pembagian",
        "",
        f"- {results['rows']} baris, {results['columns']} kolom; {results['missing']} nilai kosong, {results['duplicates']} duplikat.",
        f"- {results['train']} baris train dan {results['test']} baris test, random_state=42.",
        "- CSV tidak diubah; SHA-256: `" + original_hash + "`.",
        "",
        "## Evaluasi test",
        "",
        "| Model | RMSE test | R² test |",
        "|---|---:|---:|",
    ]
    for record in results["evaluation"]:
        lines.append(
            f"| {record['model']} | {record['RMSE_test']:.4f} | {record['R2_test']:.4f} |"
        )
    lines.extend(
        [
            "",
            "RMSE memakai satuan MEDV (ribuan dolar AS historis). Mengurangi VIF dengan",
            "mengeluarkan RAD tidak otomatis memperbaiki prediksi pada test ini.",
            "",
            "## Pemeriksaan yang lulus",
            "",
            "- Indeks fitur dan target konsisten; penggabungan untuk korelasi tidak menambah baris/kekosongan.",
            "- Train dan test terpisah; target tidak masuk ke fitur.",
            "- Median imputasi berasal dari train; prediksi baru tetap berhingga ketika CRIM kosong.",
            "- Prediksi pipeline sama dengan proses manual.",
            "- Prediksi regresi berganda sesuai penyelesaian least squares NumPy independen.",
            "- RMSE dan R² sesuai perhitungan rumus manual.",
            "- Contoh polinomial memakai validasi dari train, tidak memakai test untuk memilih derajat.",
            "- Kode peserta tidak memakai fungsi buatan sendiri, perulangan, comprehension, atau operasi matriks manual.",
            "- Format notebook valid dan seluruh sel berisi output eksekusi terbaru.",
            "",
            "## Lingkungan uji",
            "",
            f"Python {sys.version.split()[0]}, pandas {results['pandas']}, NumPy {results['numpy']},",
            f"scikit-learn {results['sklearn']}, statsmodels {results['statsmodels']}.",
            "",
            "Ini pemeriksaan eksekusi lokal, bukan pengujian antarmuka Google Colab.",
        ]
    )
    (ROOT / "laporan/uji_regresi_housing.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )
    print(json.dumps(results, indent=2))
    print(
        f"PASS: {len(code_cells)} sel kode, {len(pictures)} grafik, semua pemeriksaan lulus."
    )


if __name__ == "__main__":
    main()
