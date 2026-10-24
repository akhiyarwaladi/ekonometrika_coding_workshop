"""Jalankan semua notebook pada kernel Jupyter baru, simpan output untuk mengajar.

Jalankan: python alat_bantu/uji_semua_notebook.py
Menguji sel instalasi %pip juga. Butuh nbclient, nbformat, dan ipykernel.
Setiap notebook dimulai dari foldernya sendiri, dengan ruang variabel baru.
"""

from pathlib import Path
from datetime import datetime
import inspect
from importlib.metadata import version
import json
import os
import sys
import traceback

import nbformat
from laporan_bersama import simpan_ringkasan
from nbclient import NotebookClient
from jupyter_client import KernelManager
from uji_notebook import periksa_notebook, periksa_pemodelan

ROOT = Path(__file__).resolve().parent.parent


def main():
    paths = sorted((ROOT / "materi").rglob("*.ipynb")) + sorted(
        (ROOT / "pengajar/kunci_jawaban").glob("*.ipynb")
    )
    if sys.argv[1:]:
        paths = [Path(name).resolve() for name in sys.argv[1:]]
        assert all(p.exists() and p.suffix == ".ipynb" for p in paths)
    hasil = []
    os.environ["MPLBACKEND"] = "module://matplotlib_inline.backend_inline"
    for path in paths:
        item = {"notebook": path.relative_to(ROOT).as_posix(), "waktu_uji": datetime.now().isoformat(timespec="seconds")}
        try:
            periksa_notebook(path)
            nb = nbformat.read(path, as_version=4)
            # Sel pemeriksaan dilepas sebelum menyimpan bahan peserta.
            pemeriksaan = inspect.getsource(periksa_pemodelan)
            pemeriksaan += (
                "\nimport json\nprint(json.dumps(periksa_pemodelan(globals())))"
            )
            if path.parent.name == "04_dashboard_indonesia":
                pemeriksaan += (
                    "\nif 'konfigurasi_ngrok' in globals():"
                    "\n    ngrok.kill(pyngrok_config=konfigurasi_ngrok)"
                    "\nif 'proses_dashboard' in globals() and proses_dashboard.poll() is None:"
                    "\n    proses_dashboard.terminate()"
                    "\n    proses_dashboard.wait(timeout=10)"
                    "\nlog_dashboard.close()"
                )
            nb.cells.append(nbformat.v4.new_code_cell(pemeriksaan))
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
                timeout=240,
                km=manager,
                resources={"metadata": {"path": str(path.parent)}},
            )
            try:
                client.execute()
            finally:
                if manager.has_kernel:
                    manager.shutdown_kernel(now=True)
                if client.kc is not None:
                    client.kc.stop_channels()
            check = nb.cells.pop()
            text = "".join(
                o.get("text", "") for o in check.outputs if o.output_type == "stream"
            )
            item.update(json.loads(text))
            code = [c for c in nb.cells if c.cell_type == "code"]
            assert all(c.execution_count is not None for c in code)
            assert not [o for c in code for o in c.outputs if o.output_type == "error"]
            pictures = [
                o
                for c in code
                for o in c.outputs
                if o.output_type in ("display_data", "execute_result")
                and "image/png" in o.data
            ]
            nbformat.validate(nb)
            nbformat.write(nb, path)
            item.update(status="PASS", sel_kode=len(code), grafik=len(pictures))
        except Exception:
            item.update(status="FAIL", error=traceback.format_exc())
        hasil.append(item)
        print(item["status"], item["notebook"], flush=True)
    laporan = ROOT / "alat_bantu/laporan"
    jumlah_dijalankan = len(paths)
    if sys.argv[1:] and (laporan / "uji_kernel_semua_notebook.json").exists():
        sebelumnya = json.loads((laporan / "uji_kernel_semua_notebook.json").read_text(encoding="utf-8"))
        gabungan = {item["notebook"]: item for item in sebelumnya["hasil"]}
        gabungan.update({item["notebook"]: item for item in hasil})
        hasil = [gabungan[name] for name in sorted(gabungan)]
    ringkasan = {
        "waktu": datetime.now().isoformat(timespec="seconds"),
        "python": sys.version.split()[0],
        "paket": {
            nama: version(nama)
            for nama in (
                "numpy",
                "pandas",
                "statsmodels",
                "scikit-learn",
                "linearmodels",
                "arch",
            )
        },
        "jumlah": len(hasil),
        "jumlah_dijalankan_terakhir": jumlah_dijalankan,
        "lulus": sum(i["status"] == "PASS" for i in hasil),
        "hasil": hasil,
    }
    (laporan / "uji_kernel_semua_notebook.json").write_text(
        json.dumps(ringkasan, indent=2), encoding="utf-8"
    )
    simpan_ringkasan()
    print(f"{ringkasan['lulus']}/{len(hasil)} notebook lulus; {jumlah_dijalankan} dijalankan pada pemeriksaan terakhir.", flush=True)
    return 0 if ringkasan["lulus"] == len(hasil) else 1


if __name__ == "__main__":
    sys.exit(main())
