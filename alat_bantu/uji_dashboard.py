"""Uji dashboard yang seluruh kodenya disimpan pada notebook penutup.

Jalankan dari folder utama: python alat_bantu/uji_dashboard.py
Tambahkan --notebook untuk menjalankan seluruh sel pada kernel baru dan menyimpan output.
AppTest memeriksa interaksi pada salinan aplikasi dan data dalam folder sementara.
"""

from pathlib import Path
from tempfile import TemporaryDirectory
import argparse
import ast
import json
import os
import shutil
import sys

import nbformat
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from streamlit.testing.v1 import AppTest
from jupyter_client import KernelManager
from nbclient import NotebookClient

from uji_notebook import periksa_sinkron

ROOT = Path(__file__).resolve().parent.parent
NOTEBOOK = ROOT / "materi/04_dashboard_indonesia/01_dashboard_ekonomi.ipynb"


def angka_metric(app, label):
    metric = next(m for m in app.metric if m.label == label)
    return float(metric.value.split()[0].rstrip("%"))


def tanpa_error(app):
    assert not app.exception, str(app.exception)


def uji_kernel(ngrok_aktif=False):
    notebook = nbformat.read(NOTEBOOK, as_version=4)
    pemeriksaan_ngrok = ""
    if ngrok_aktif:
        assert os.environ.get("NGROK_AUTHTOKEN"), "Siapkan NGROK_AUTHTOKEN di lingkungan pengujian."
        sel_ngrok = next(c for c in notebook.cells if c.cell_type == "code" and "gunakan_ngrok = False" in c.source)
        sel_ngrok.source = sel_ngrok.source.replace("gunakan_ngrok = False", "gunakan_ngrok = True")
        pemeriksaan_ngrok = (
            "assert alamat_ngrok.startswith('https://')\n"
            "headers_ngrok = {'ngrok-skip-browser-warning': 'true'}\n"
            "cek_ngrok = requests.get(alamat_ngrok + '/_stcore/health', headers=headers_ngrok, timeout=30)\n"
            "assert cek_ngrok.status_code == 200 and cek_ngrok.text.strip() == 'ok'\n"
            "halaman_ngrok = requests.get(alamat_ngrok, headers=headers_ngrok, timeout=30)\n"
            "assert halaman_ngrok.status_code == 200 and 'streamlit' in halaman_ngrok.text.lower()\n"
        )
    cleanup = (
        "if 'konfigurasi_ngrok' in globals():\n"
        "    ngrok.kill(pyngrok_config=konfigurasi_ngrok)\n"
        "if 'proses_dashboard' in globals() and proses_dashboard.poll() is None:\n"
        "    proses_dashboard.terminate()\n"
        "    proses_dashboard.wait(timeout=10)\n"
        "if 'log_dashboard' in globals():\n"
        "    log_dashboard.close()\n"
    )
    notebook.cells.append(nbformat.v4.new_code_cell(pemeriksaan_ngrok + cleanup))
    manager = KernelManager(kernel_name="python3")
    manager.kernel_spec.argv = [sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"]
    client = NotebookClient(notebook, km=manager, timeout=300, resources={"metadata": {"path": str(NOTEBOOK.parent)}})
    try:
        client.execute()
    finally:
        if manager.has_kernel and client.kc is not None:
            try:
                msg_id = client.kc.execute(cleanup)
                while True:
                    reply = client.kc.get_shell_msg(timeout=10)
                    if reply["parent_header"].get("msg_id") == msg_id:
                        break
            except Exception:
                pass
        if manager.has_kernel:
            manager.shutdown_kernel(now=True)
        if client.kc is not None:
            client.kc.stop_channels()
    notebook.cells.pop()
    code_cells = [c for c in notebook.cells if c.cell_type == "code"]
    assert all(c.execution_count is not None for c in code_cells)
    assert not [o for c in code_cells for o in c.outputs if o.output_type == "error"]
    for cell in code_cells:
        cell.source = cell.source.replace("gunakan_ngrok = True", "gunakan_ngrok = False")
        # Instalasi dan alamat pratinjau bersifat khusus untuk runtime pengujian.
        if cell.source.startswith("%pip ") or "serve_kernel_port_as_iframe" in cell.source or "gunakan_ngrok = False" in cell.source:
            cell.outputs = []
    nbformat.validate(notebook)
    nbformat.write(notebook, NOTEBOOK)
    return {"status": "PASS", "sel_kode": len(code_cells), "server_dan_healthcheck": "PASS", "proses_uji_dihentikan": True,
            "ngrok": "PASS: HTTPS, healthcheck dan halaman Streamlit melalui internet" if ngrok_aktif else "Opsional; tidak diaktifkan pada pengujian ini"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--notebook", action="store_true")
    parser.add_argument("--ngrok", action="store_true", help="Uji tautan HTTPS dengan NGROK_AUTHTOKEN dari lingkungan, lalu tutup koneksi.")
    args = parser.parse_args()
    periksa_sinkron(NOTEBOOK)
    notebook = nbformat.read(NOTEBOOK, as_version=4)
    bagian = []
    for cell in notebook.cells:
        if cell.cell_type == "code" and cell.source.startswith("%%writefile bagian_"):
            bagian.append(cell.source.split("\n", 1)[1])
    assert len(bagian) == 4
    aplikasi = "\n".join(bagian)
    pohon = ast.parse(aplikasi)
    assert not any(isinstance(n, (ast.FunctionDef, ast.For, ast.While, ast.ListComp, ast.Lambda)) for n in ast.walk(pohon))
    checks = []
    with TemporaryDirectory(prefix="uji_dashboard_") as temp:
        folder = Path(temp)
        file_app = folder / "dashboard_ekonomi.py"
        # Arahkan alamat data ke fixture lokal untuk menguji interaksi tanpa internet.
        alamat_data = "https://raw.githubusercontent.com/akhiyarwaladi/ekonometrika_coding_workshop/main/data/"
        aplikasi_lokal = aplikasi.replace(alamat_data, folder.as_posix() + "/")
        file_app.write_text(aplikasi_lokal, encoding="utf-8")
        shutil.copyfile(ROOT / "data/provinsi_2021.csv", folder / "provinsi_2021.csv")
        data = pd.read_csv(folder / "provinsi_2021.csv")
        app = AppTest.from_file(file_app, default_timeout=30).run()
        tanpa_error(app)
        assert len(app.tabs) == 3
        assert app.checkbox(key="semua_provinsi").value
        assert len(app.dataframe[-1].value) == 34
        np.testing.assert_allclose(angka_metric(app, "IPM (poin)"), data.IPM.mean(), atol=0.005)
        np.testing.assert_allclose(angka_metric(app, "Kemiskinan (%)"), data.Kemiskinan.mean(), atol=0.005)

        # Solusi OLS dihitung lewat persamaan kuadrat terkecil NumPy untuk
        # memeriksa target, pembagian sampel, dan angka evaluasi yang ditampilkan.
        X = data[["IPM", "Pengangguran"]]
        y = data.Kemiskinan
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
        koef = np.linalg.lstsq(np.column_stack([np.ones(len(X_train)), X_train]), y_train, rcond=None)[0]
        pred = np.column_stack([np.ones(len(X_test)), X_test]) @ koef
        rmse = np.sqrt(np.mean((y_test.to_numpy() - pred) ** 2))
        r2 = 1 - np.sum((y_test.to_numpy() - pred) ** 2) / np.sum((y_test.to_numpy() - y_test.mean()) ** 2)
        np.testing.assert_allclose(angka_metric(app, "RMSE uji (poin persen)"), rmse, atol=0.005)
        np.testing.assert_allclose(angka_metric(app, "R² data uji"), r2, atol=0.0005)
        checks.append("Ringkasan 34 provinsi, RMSE, dan R² sesuai perhitungan independen.")

        app.selectbox(key="indikator").set_value("IPM").run()
        app.selectbox(key="sumbu_x").set_value("Pengangguran").run()
        tanpa_error(app)
        checks.append("Pilihan indikator peringkat dan sumbu grafik dapat diubah.")

        nilai_awal = angka_metric(app, "Prediksi kemiskinan skenario")
        ipm_baru = float(X_train.IPM.max())
        pengangguran_baru = float(X_train.Pengangguran.max())
        app.slider(key="ipm_skenario").set_value(ipm_baru)
        app.slider(key="pengangguran_skenario").set_value(pengangguran_baru).run()
        tanpa_error(app)
        expected = float(np.array([1, ipm_baru, pengangguran_baru]) @ koef)
        np.testing.assert_allclose(angka_metric(app, "Prediksi kemiskinan skenario"), expected, atol=0.005)
        assert angka_metric(app, "Prediksi kemiskinan skenario") != nilai_awal
        checks.append("Slider mengubah prediksi; hasil sesuai model OLS independen.")

        for fitur in [["IPM"], ["Pengangguran"], []]:
            app.multiselect(key="fitur").set_value(fitur).run()
            tanpa_error(app)
        assert any("variabel penjelas" in item.value for item in app.info)
        app.multiselect(key="fitur").set_value(["IPM", "Pengangguran"]).run()
        checks.append("Satu atau dua X bekerja; pilihan X kosong ditangani tanpa error.")

        app.checkbox(key="semua_provinsi").set_value(False).run()
        app.multiselect(key="provinsi").set_value(["Jambi"]).run()
        tanpa_error(app)
        assert any("10 provinsi" in item.value for item in app.info)
        assert len(app.dataframe[-1].value) == 1
        assert app.dataframe[-1].value.Provinsi.iloc[0] == "Jambi"
        app.multiselect(key="provinsi").set_value([]).run()
        tanpa_error(app)
        assert any("Pilih sedikitnya satu provinsi" in item.value for item in app.info)
        checks.append("Filter Jambi, jumlah provinsi sedikit, dan pilihan kosong ditangani dengan benar.")

        app.multiselect(key="provinsi").set_value(data.Provinsi.tolist()[:10]).run()
        tanpa_error(app)
        assert len(app.dataframe[-1].value) == 10
        assert set(app.dataframe[-1].value.Provinsi) == set(data.Provinsi.tolist()[:10])
        assert any(m.label == "RMSE uji (poin persen)" for m in app.metric)
        checks.append("Model dan tabel mengikuti filter 10 provinsi yang dipilih.")

        data["IPM"] = 70.0
        data.to_csv(folder / "provinsi_2021.csv", index=False)
        app = AppTest.from_file(file_app, default_timeout=30).run()
        tanpa_error(app)
        assert any("lebih dari satu nilai" in item.value for item in app.info)
        checks.append("X konstan ditangani tanpa membentuk model yang menyesatkan.")

    report = {
        "status": "PASS", "notebook": NOTEBOOK.relative_to(ROOT).as_posix(),
        "provinsi": 34, "jumlah_bagian_aplikasi": 4,
        "rmse_uji_default": float(rmse), "r2_uji_default": float(r2), "pemeriksaan": checks,
        "batas_uji": "Interaksi Streamlit diuji dengan AppTest lokal; antarmuka Google Colab tidak dikendalikan dalam pengujian ini.",
    }
    if args.notebook or args.ngrok:
        report["kernel_notebook"] = uji_kernel(ngrok_aktif=args.ngrok)
    (ROOT / "alat_bantu/laporan/uji_dashboard.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Pengujian notebook dan dashboard ekonomi provinsi", "",
        f"Hasil AppTest: **PASS**, {len(checks)} kelompok pengujian pada data 34 provinsi tahun 2021.", "",
        f"Notebook: [{NOTEBOOK.name}](../../{NOTEBOOK.relative_to(ROOT).as_posix()}).", "",
        "## Perilaku yang diperiksa", "",
    ]
    lines += [f"- {check}" for check in checks]
    lines += ["", f"Model default pada data uji: RMSE **{rmse:.6f} poin persentase**, R² **{r2:.6f}**."]
    if args.notebook or args.ngrok:
        lines += ["", f"Seluruh **{report['kernel_notebook']['sel_kode']} sel kode** dijalankan pada kernel baru, termasuk instalasi, pembuatan berkas aplikasi, server, dan pratinjau lokal. Server uji dihentikan setelah pemeriksaan."]
        lines += ["", "Ngrok: " + report["kernel_notebook"]["ngrok"] + ". Token dan tautan sementara tidak disimpan pada laporan."]
    lines += ["", "Kode aplikasi disimpan dalam empat sel notebook; tidak memerlukan langkah terminal dari peserta.", "Pratinjau browser lokal disimpan pada [gambar simulasi](../gambar/dashboard/pratinjau_simulasi.png).", "", report["batas_uji"], ""]
    (ROOT / "alat_bantu/laporan/uji_dashboard.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"PASS: {len(checks)} kelompok pengujian dashboard; RMSE {rmse:.4f}, R² {r2:.4f}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
