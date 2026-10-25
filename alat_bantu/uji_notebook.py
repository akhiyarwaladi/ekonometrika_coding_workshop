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

import nbformat

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
                        (workdir / "data").resolve().as_uri() + "/",
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
    pengayaan = []
    if "bantuan_did" in ruang:
        d = ruang["bantuan_did"]
        assert len(d) == 8 and not d.duplicated(["tahun", "peserta"]).any()
        assert (d["sesudah"] == (d["tahun"] >= 2023)).all()
        assert (d["interaksi"] == d["peserta"] * d["sesudah"]).all()
        # Verifikasi lewat aljabar matriks, terpisah dari tabel empat rata-rata.
        desain = np.column_stack([np.ones(len(d)), d[["peserta", "sesudah", "interaksi"]]])
        assert np.linalg.matrix_rank(desain) == 4
        koef = np.linalg.lstsq(desain, d["pendapatan"], rcond=None)[0]
        np.testing.assert_allclose(koef[-1], 0.3, atol=1e-12)
        np.testing.assert_allclose(ruang["dampak_did"], koef[-1], atol=1e-12)
        np.testing.assert_allclose(ruang["model_did"].coef_, koef[1:], atol=1e-12)
        gap = ruang["rata_tahunan_did"][1] - ruang["tanpa_program_did"]
        np.testing.assert_allclose(gap.loc[2021:2022], 0, atol=1e-12)
        np.testing.assert_allclose(gap.loc[2023:2024], 0.3, atol=1e-12)
        if "did_satu_tahun" in ruang:
            np.testing.assert_allclose(ruang["did_satu_tahun"], 0.3, atol=1e-12)
        pengayaan.append("did: hitungan manual, koefisien, dan pembanding simulasi")
    if "model_kredit" in ruang:
        sets = [set(ruang[n].index) for n in ("kredit_latih", "kredit_validasi", "kredit_uji")]
        assert [len(s) for s in sets] == [600, 200, 200]
        assert not (sets[0] & sets[1] or sets[0] & sets[2] or sets[1] & sets[2])
        assert set.union(*sets) == set(ruang["kredit"].index)
        skala = ruang["skala_kredit"]
        assert skala.n_samples_seen_ == 600
        np.testing.assert_allclose(skala.mean_, ruang["X_latih_kredit"].mean())
        ulang = LogisticRegression(max_iter=1000).fit(
            skala.transform(ruang["X_latih_kredit"]), ruang["y_latih_kredit"]
        )
        np.testing.assert_allclose(ulang.coef_, ruang["model_kredit"].coef_)
        assert ruang["model_kredit"].classes_.tolist() == [0, 1]
        y_valid = ruang["y_validasi_kredit"].to_numpy()
        biaya_valid = []
        for ambang in (0.2, 0.5):
            pred = ulang.predict_proba(skala.transform(ruang["X_validasi_kredit"]))[:, 1] >= ambang
            biaya_valid.append(int(((y_valid == 0) & pred).sum() + 5 * ((y_valid == 1) & ~pred).sum()))
        np.testing.assert_array_equal(ruang["biaya_validasi_kredit"]["biaya"], biaya_valid)
        assert ruang["ambang_terpilih_kredit"] == (0.2, 0.5)[int(np.argmin(biaya_valid))]
        y_uji = ruang["y_uji_kredit"].to_numpy()
        peluang_uji = ulang.predict_proba(skala.transform(ruang["X_uji_kredit"]))[:, 1]
        np.testing.assert_allclose(peluang_uji, ruang["peluang_uji_kredit"])
        pred_uji = peluang_uji >= ruang["ambang_terpilih_kredit"]
        biaya_uji = int(((y_uji == 0) & pred_uji).sum() + 5 * ((y_uji == 1) & ~pred_uji).sum())
        np.testing.assert_array_equal(ruang["kelas_uji_kredit"], pred_uji)
        np.testing.assert_array_equal(ruang["hasil_uji_kredit"]["biaya_uji"], [5 * y_uji.sum(), (y_uji == 0).sum(), biaya_uji])
        pengayaan.append("kredit: pemisahan sampel, skala latihan, biaya, dan ambang validasi")
    if "model_ramalan" in ruang:
        d = ruang["inflasi_ramalan"]
        assert d.index.is_unique and d.index.is_monotonic_increasing
        assert pd.infer_freq(d.index) == "MS"
        np.testing.assert_allclose(d["lag_1"].iloc[1:], d["inflasi_yoy"].shift(1).iloc[1:])
        np.testing.assert_allclose(d["lag_12"].iloc[12:], d["inflasi_yoy"].shift(12).iloc[12:])
        latih, uji = ruang["latih_ramalan"], ruang["uji_ramalan"]
        assert len(latih) == 168 and len(uji) == 16
        assert latih.index.max() < uji.index.min()
        assert latih.index.max() == pd.Timestamp("2023-12-01")
        assert uji.index.min() == pd.Timestamp("2024-01-01")
        assert uji.index.max() == pd.Timestamp("2025-04-01")
        X, y = ruang["X_latih_ramalan"], ruang["y_latih_ramalan"]
        tahun_validasi, galat_cv = [], []
        for a, b in ruang["pembagian_waktu_ramalan"].split(X):
            assert X.index[a].max() < X.index[b].min() < uji.index.min()
            assert len(b) == 12
            tahun_validasi.append(X.index[b][0].year)
            m = LinearRegression().fit(X.iloc[a], y.iloc[a])
            galat_cv.append(np.abs(y.iloc[b].to_numpy() - m.predict(X.iloc[b])).mean())
        np.testing.assert_array_equal(ruang["hasil_validasi_ramalan"]["tahun_validasi"], tahun_validasi)
        np.testing.assert_allclose(ruang["mae_validasi_ramalan"], galat_cv)
        # Model uji harus sama dengan estimasi dari data sampai 2023 saja.
        akhir = LinearRegression().fit(X, y)
        np.testing.assert_allclose(akhir.coef_, ruang["model_ramalan"].coef_)
        pred = akhir.predict(ruang["X_uji_ramalan"])
        np.testing.assert_allclose(pred, ruang["prediksi_uji_ramalan"])
        np.testing.assert_allclose(ruang["prediksi_naif_ramalan"], uji["lag_1"])
        galat = np.column_stack([uji["inflasi_yoy"] - uji["lag_1"], uji["inflasi_yoy"] - pred])
        np.testing.assert_allclose(ruang["hasil_uji_ramalan"]["MAE_poin_persentase"], np.abs(galat).mean(axis=0))
        np.testing.assert_allclose(ruang["hasil_uji_ramalan"]["RMSE_poin_persentase"], np.sqrt((galat ** 2).mean(axis=0)))
        pengayaan.append("ramalan: lag masa lalu, validasi waktu, dan metrik uji akhir")
    return {
        "model_scikit_learn": jumlah_model,
        "perbandingan_inferensi": jumlah_banding,
        "pengayaan_terverifikasi": pengayaan,
    }


def periksa_notebook(path):
    nbformat.validate(nbformat.read(path, as_version=4))
    nb = json.loads(path.read_text(encoding="utf-8"))
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
        for node in ast.walk(ast.parse(kode)):
            if isinstance(node, ast.ImportFrom) and node.module == "pathlib":
                raise ValueError("Materi peserta memakai alamat data langsung dan pembacaan berkas biasa, tanpa pathlib.")
            if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) and node.value.id == "os" and node.attr in {"environ", "getenv"}:
                raise ValueError("Pengaturan tutorial tidak menggunakan variabel lingkungan.")
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "Path":
                raise ValueError("Path() tidak dipakai pada kode peserta.")
        if path.stem == "00_persiapan_colab":
            for node in ast.walk(ast.parse(kode)):
                if isinstance(node, ast.Attribute) and node.attr in {"fit", "predict", "predict_proba", "score"}:
                    raise ValueError("Sesi 00 hanya EDA; pemodelan dimulai pada Sesi 01.")
                if isinstance(node, ast.ImportFrom) and (node.module or "").split(".")[0] in {"sklearn", "statsmodels", "linearmodels", "arch"}:
                    raise ValueError("Pustaka pemodelan belum digunakan pada Sesi 00.")
                if isinstance(node, ast.Import) and any(a.name.split(".")[0] in {"sklearn", "statsmodels", "linearmodels", "arch"} for a in node.names):
                    raise ValueError("Pustaka pemodelan belum digunakan pada Sesi 00.")
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
            periksa_notebook(path)
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
    (laporan / "uji_kode.log").write_text(log.getvalue(), encoding="utf-8")
    (laporan / "uji_kode.json").write_text(
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
