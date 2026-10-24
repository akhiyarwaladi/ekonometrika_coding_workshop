"""Verifikasi notebook per sel, dengan ruang variabel baru untuk tiap file.

Jalankan: python alat_bantu/uji_notebook.py [folder atau file ...] [--dari-zip]
--dari-zip mengekstrak paket ke folder sementara dan mengarahkan URL data ke salinan lokal.
--dari-folder-notebook memakai folder masing-masing notebook sebagai folder kerja.
Sel %pip dilewati; pasang requirements.txt sebelum menjalankan pemeriksaan.
Log mencatat output teks, ekspresi terakhir, warning statistik, dan traceback.
Pemeriksaan ini tidak menggantikan uji tampilan serta koneksi Google Colab.
"""

import ast
import contextlib
import io
import json
import os
import shlex
import sys
import tempfile
import traceback
import warnings
from pathlib import Path
from zipfile import ZipFile

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from konversi_notebook import ke_sumber, parse_sel, sumber_notebook

ROOT = Path(__file__).resolve().parent.parent


def tutup_grafik(*args, **kwargs):
    plt.close("all")


plt.show = tutup_grafik


def jalankan_sel(sumber, label, ruang):
    baris = sumber.splitlines()
    if baris and baris[0].startswith("%%writefile "):
        argumen = shlex.split(baris[0])[1:]
        mode = "a" if "-a" in argumen else "w"
        tujuan = Path(argumen[-1]).resolve()
        assert tujuan.is_relative_to(Path.cwd().resolve()), tujuan
        with tujuan.open(mode, encoding="utf-8") as file:
            file.write("\n".join(baris[1:]) + "\n")
        print(f"Berkas aplikasi disimpan: {tujuan.name}")
        return
    # Perintah instalasi milik IPython; paket diuji lewat impor pada sel berikutnya.
    kode = "\n".join("pass" if s.lstrip().startswith("%pip ") else s for s in baris)
    pohon = ast.parse(kode, filename=label)
    akhir = None
    if pohon.body and isinstance(pohon.body[-1], ast.Expr):
        akhir = pohon.body.pop().value
    exec(compile(pohon, label, "exec"), ruang)
    if akhir is not None:
        nilai = eval(compile(ast.Expression(akhir), label, "eval"), ruang)
        if nilai is not None:
            print(repr(nilai))


def jalankan(path, workdir, data_lokal=False):
    nb = json.loads(path.read_text(encoding="utf-8"))
    ruang = {"__name__": "__main__", "__file__": str(path)}
    # Entri kosong mengikuti perubahan folder kerja seperti pada kernel Jupyter.
    sys_path_awal = sys.path[:]
    sys.path.insert(0, "")
    sys.modules.pop("alat_bantu.metode_lanjutan", None)
    sys.modules.pop("alat_bantu", None)
    sys.modules.pop("metode_lanjutan", None)
    semula = Path.cwd()
    os.chdir(workdir)
    try:
        for numero, sel in enumerate(nb["cells"], 1):
            if sel["cell_type"] == "code":
                sumber = "".join(sel["source"])
                if data_lokal:
                    sumber = sumber.replace(
                        "https://raw.githubusercontent.com/akhiyarwaladi/ekonometrika_coding_workshop/main/data/",
                        (workdir / "data").resolve().as_posix() + "/",
                    )
                    sumber = sumber.replace(
                        "https://raw.githubusercontent.com/akhiyarwaladi/ekonometrika_coding_workshop/main/alat_bantu/metode_lanjutan.py",
                        (workdir / "alat_bantu/metode_lanjutan.py").resolve().as_uri(),
                    )
                jalankan_sel(sumber, f"{path.name}:sel-{numero}", ruang)
        hasil = periksa_pemodelan(ruang)
        print("Pemeriksaan model:", hasil)
    finally:
        konfigurasi = ruang.get("konfigurasi_ngrok")
        if konfigurasi is not None:
            ruang["ngrok"].kill(pyngrok_config=konfigurasi)
        proses = ruang.get("proses_dashboard")
        if proses is not None and proses.poll() is None:
            proses.terminate()
            proses.wait(timeout=10)
        if "log_dashboard" in ruang:
            ruang["log_dashboard"].close()
        os.chdir(semula)
        sys.path[:] = sys_path_awal
        plt.close("all")


def periksa_pemodelan(ruang):
    """Pastikan model utama benar-benar scikit-learn dan inferensinya setara."""
    import numpy as np
    import pandas as pd
    from sklearn.linear_model import (
        LinearRegression,
        LogisticRegression,
        PoissonRegressor,
    )

    jumlah_model = 0
    jumlah_banding = 0
    objek = set()
    for nama, model in list(ruang.items()):
        if isinstance(model, (LinearRegression, LogisticRegression, PoissonRegressor)):
            if id(model) not in objek:
                jumlah_model += 1
                objek.add(id(model))
            assert np.isfinite(model.coef_).all(), nama
            assert np.isfinite(model.intercept_).all(), nama
        if not nama.startswith("uji_"):
            continue
        dasar = nama[4:]
        utama = ruang.get(dasar)
        X = ruang.get("X_" + dasar)
        if X is None or not hasattr(model, "predict"):
            continue
        if isinstance(utama, LinearRegression):
            np.testing.assert_allclose(
                utama.predict(X), model.predict(), rtol=1e-7, atol=1e-6
            )
        elif isinstance(utama, LogisticRegression):
            np.testing.assert_allclose(
                utama.predict_proba(X)[:, 1], model.predict(), rtol=1e-5, atol=3e-5
            )
        elif isinstance(utama, PoissonRegressor):
            np.testing.assert_allclose(
                utama.predict(X), model.predict(), rtol=1e-6, atol=1e-6
            )
        else:
            continue
        assert model.nobs == len(X), nama
        y = ruang["y_" + dasar]
        assert X.index.equals(y.index), nama
        koefisien = ruang.get("koefisien_" + dasar)
        if isinstance(koefisien, pd.Series):
            assert set(koefisien.index) == set(model.params.index), nama
        jumlah_banding += 1
    if "peluang" in ruang and "model_mn" in ruang:
        peluang = ruang["peluang"]
        np.testing.assert_allclose(peluang.sum(axis=1), 1)
        assert peluang.columns.to_list() == ruang["model_mn"].classes_.tolist()
    return {
        "model_scikit_learn": jumlah_model,
        "perbandingan_inferensi": jumlah_banding,
    }


def periksa_sinkron(path):
    sumber = sumber_notebook(path)
    sel_py = []
    for tipe, baris in parse_sel(sumber.read_text(encoding="utf-8")):
        if any(b.strip() for b in baris):
            sel_py.append((tipe, "".join(ke_sumber(tipe, baris))))
    nb = json.loads(path.read_text(encoding="utf-8"))
    sel_nb = [(s["cell_type"], "".join(s["source"])) for s in nb["cells"]]
    if sel_py != sel_nb:
        raise ValueError(
            "Python dan notebook berbeda. Jalankan alat_bantu/konversi_notebook.py."
        )
    ids = [s["id"] for s in nb["cells"]]
    if len(ids) != len(set(ids)):
        raise ValueError("ID sel notebook tidak unik.")
    # Batas keterbacaan untuk materi peserta; perkakas pengajar dikecualikan.
    sulit = (
        ast.FunctionDef,
        ast.AsyncFunctionDef,
        ast.ClassDef,
        ast.Lambda,
        ast.ListComp,
        ast.DictComp,
        ast.SetComp,
        ast.GeneratorExp,
        ast.For,
        ast.While,
        ast.IfExp,
        ast.MatMult,
    )
    for sel in nb["cells"]:
        if sel["cell_type"] != "code":
            continue
        kode = "\n".join(
            "pass" if s.lstrip().startswith(("%pip ", "%%writefile ")) else s
            for s in "".join(sel["source"]).splitlines()
        )
        if any(isinstance(n, sulit) for n in ast.walk(ast.parse(kode))):
            raise ValueError("Ada sintaks tingkat lanjut pada sel materi peserta.")
        for node in ast.walk(ast.parse(kode)):
            if not isinstance(node, ast.Assign) or not isinstance(node.value, ast.Call):
                continue
            fit = node.value.func
            if not isinstance(fit, ast.Attribute) or fit.attr not in (
                "fit",
                "fit_regularized",
            ):
                continue
            estimator = fit.value
            if not isinstance(estimator, ast.Call) or not isinstance(
                estimator.func, ast.Attribute
            ):
                continue
            jenis = estimator.func
            if not isinstance(jenis.value, ast.Name):
                continue
            inferensi = (
                jenis.value.id == "smf" and jenis.attr in ("ols", "logit", "poisson")
            ) or (
                jenis.value.id == "sm"
                and jenis.attr in ("OLS", "Logit", "MNLogit", "Poisson")
            )
            if inferensi and not node.targets[0].id.startswith("uji_"):
                raise ValueError(
                    "Estimator yang tersedia di scikit-learn harus menjadi model utama; statsmodels diberi nama uji_."
                )


def main():
    zip_only = "--dari-zip" in sys.argv
    dari_folder = "--dari-folder-notebook" in sys.argv
    opsi = {"--dari-zip", "--dari-folder-notebook"}
    argumen = [a for a in sys.argv[1:] if a not in opsi]
    target = [Path(a).resolve() for a in argumen] or [
        ROOT / "materi",
        ROOT / "pengajar/kunci_jawaban",
    ]
    files = []
    for item in target:
        files.extend(
            sorted(item.rglob("*.ipynb"))
            if item.is_dir()
            else [item.with_suffix(".ipynb")]
        )
    if not files:
        raise ValueError("Tidak ada notebook pada lokasi yang dipilih.")
    log = io.StringIO()
    gagal = []
    for path in files:
        buf = io.StringIO()
        pesan = []
        try:
            periksa_sinkron(path)
            with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
                with warnings.catch_warnings(record=True) as pesan:
                    warnings.simplefilter("always")
                    if zip_only:
                        with tempfile.TemporaryDirectory(
                            prefix="ekonometrika-"
                        ) as folder:
                            tempat = Path(folder)
                            with ZipFile(ROOT / "alat_bantu/paket/data_tutorial.zip") as paket:
                                paket.extractall(tempat)
                            jalankan(path, tempat, data_lokal=True)
                    else:
                        jalankan(path, path.parent if dari_folder else ROOT)
            status = "PASS"
        except Exception:
            status = "FAIL"
            buf.write("\n" + traceback.format_exc())
            gagal.append(path)
        for peringatan in pesan:
            buf.write(f"WARNING {peringatan.category.__name__}: {peringatan.message}\n")
        log.write(f"\n{status} {path.relative_to(ROOT)}\n{buf.getvalue()}")
        print(f"{status} {path.relative_to(ROOT)} ({len(pesan)} warning)", flush=True)
    mode = "zip" if zip_only else "folder_notebook" if dari_folder else "lokal"
    laporan = ROOT / "alat_bantu/laporan"
    laporan.mkdir(exist_ok=True)
    (laporan / f"uji_notebook_{mode}.log").write_text(log.getvalue(), encoding="utf-8")
    (laporan / f"uji_notebook_{mode}.json").write_text(
        json.dumps(
            {
                "mode": mode,
                "jumlah": len(files),
                "lulus": len(files) - len(gagal),
                "gagal": [p.relative_to(ROOT).as_posix() for p in gagal],
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"\n{len(files) - len(gagal)}/{len(files)} notebook berjalan tanpa error.")
    print(
        "Mode:",
        "salinan ZIP dengan URL data diarahkan ke folder lokal" if zip_only else mode,
    )
    return 1 if gagal else 0


if __name__ == "__main__":
    sys.exit(main())
