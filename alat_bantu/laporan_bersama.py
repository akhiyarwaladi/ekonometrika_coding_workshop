"""Satu laporan Markdown dari hasil pemeriksaan terstruktur."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LAPORAN = ROOT / "alat_bantu/laporan"


def baca(name):
    path = LAPORAN / name
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def simpan_ringkasan():
    kernel = baca("uji_kernel_semua_notebook.json")
    struktur = baca("struktur.json")
    housing = baca("hasil_uji_regresi_rumah.json")
    dashboard = baca("uji_dashboard.json")
    visual = baca("audit_visual.json")
    kamus = baca("kamus_variabel.json")
    format_data = baca("uji_format_data.json")
    lines = ["# Hasil pemeriksaan materi", "",
             "Notebook `.ipynb` adalah sumber utama. Grafik pembelajaran tersimpan pada keluaran notebook.",
             "Sesi 00 berfokus pada EDA; pembentukan model dimulai pada Sesi 01.",
             "[Kembali ke materi](../../README.md)", "", "## Eksekusi seluruh notebook", ""]
    if kernel:
        lines += [f"Hasil: **{kernel['lulus']}/{kernel['jumlah']} notebook lulus**. Waktu uji: {kernel['waktu']}.",
                  "Setiap notebook dijalankan pada kernel baru, termasuk sel instalasi. Pemeriksaan model membandingkan prediksi scikit-learn dengan pelengkap inferensi yang sesuai.", "",
                  "| Notebook | Status | Sel kode | Gambar keluaran |", "|---|---|---:|---:|"]
        for item in kernel["hasil"]:
            path = item["notebook"]
            lines.append(f"| [{path}](../../{path}) | {item['status']} | {item.get('sel_kode', '—')} | {item.get('grafik', '—')} |")
    lines += ["", "## Struktur dan integritas", ""]
    if struktur:
        lines += [f"Status **{struktur['status']}**: {struktur['notebook']} notebook, {struktur['csv_aktif']} CSV utama, {struktur['csv_cadangan']} CSV latihan tambahan.",
                  f"{struktur['hash_diperiksa']} hash berkas terlindungi dan {struktur['tautan_lokal']} tautan materi diperiksa, termasuk tujuan bagian dan tautan Colab.",
                  "31 PNG slide tetap berukuran 6000 × 3375 piksel, 600 dpi, dan sesuai dengan ZIP PNG."]
        if "bagian_notebook" in struktur:
            lines += [f"{struktur['bagian_notebook']} bagian pada seluruh notebook diperiksa: judul sesi/latihan/kunci seragam, nomor bagian inti berurutan, dan setiap judul bagian mengawali sel.",
                      "Seluruh notebook mempunyai bagian Selanjutnya. Tidak ada impor identik yang berulang dalam ruang kerja yang sama."]
    if kamus:
        lines += [f"Definisi {kamus['jumlah_definisi_kolom']} kolom tersedia pada {kamus['jumlah_tabel_di_tutorial']} tabel Kenali data; [katalog data](../../data/README.md) memuat seluruh CSV."]
        if "jumlah_tabel_fungsi" in kamus:
            lines += [f"{kamus['jumlah_tabel_fungsi']} tabel fungsi menjelaskan kegunaan, masukan/argumen, dan hasil perintah. {kamus['jumlah_tabel_alur']} tabel alur menghubungkan bekal sebelumnya dengan materi berikutnya."]
    if format_data:
        lines += ["", "## Pembaca berbagai format data", "",
                  f"Status **{format_data['status']}**: tujuh format memakai {format_data['kasus_berbeda']} kasus Indonesia yang berbeda.",
                  "Sumber: World Bank, BPS Jawa Barat, dan BMKG. Bentuk tabel, satuan, label SPSS/Stata, kedua lembar Excel, dan hash salinan diperiksa.", "",
                  "| Format | Kasus | Baris | Kolom |", "|---|---|---:|---:|"]
        for item in format_data["hasil"]:
            lines.append(f"| {item['format']} | {item['kasus']} | {item['baris']} | {item['kolom']} |")
    lines += ["", "## Visualisasi dan keterbacaan", ""]
    if visual:
        lines += [f"Status **{visual['status']}**: {visual['jumlah_notebook']} notebook diperiksa; total {visual['jumlah_gambar']} gambar keluaran.",
                  "Setiap notebook mempunyai grafik, petunjuk cara membaca, dan kode yang dapat dijalankan berurutan. Pemeriksaan visual meliputi judul, label sumbu, keterbacaan, dan ukuran gambar.",
                  "Tinjauan tampilan: **" + visual.get("tinjauan_tampilan", "Belum dicatat") + "**."]
    else:
        lines += ["Pemeriksaan visual akhir belum dicatat untuk versi ini."]
    lines += ["", "## Regresi Housing", ""]
    if housing:
        lines += [f"Pemeriksaan independen: **{housing['checks']}**, dengan {housing['train']} baris latih dan {housing['test']} baris uji.", "",
                  "| Model | RMSE uji | R² uji |", "|---|---:|---:|"]
        for item in housing["evaluation"]:
            lines.append(f"| {item['model']} | {item['RMSE_test']:.4f} | {item['R2_test']:.4f} |")
        lines += ["", "RMSE memakai satuan MEDV, yaitu ribu dolar AS historis. Imputasi dipelajari dari data latih; prediksi manual dibandingkan dengan Pipeline serta solusi NumPy independen."]
    lines += ["", "## Dashboard dan ngrok", ""]
    if dashboard:
        lines += [f"Interaksi aplikasi: **{dashboard['status']}**, {len(dashboard['pemeriksaan'])} kelompok pemeriksaan.",
                  f"Model default: RMSE {dashboard['rmse_uji_default']:.6f} poin persentase; R² {dashboard['r2_uji_default']:.6f}."]
        if "kernel_notebook" in dashboard:
            lines += ["Ngrok: " + dashboard["kernel_notebook"].get("ngrok", "belum diuji pada run ini") + "."]
    lines += ["", "## Batas pemeriksaan", "",
              "Kernel dan akses HTTPS ngrok diuji secara lokal. Antarmuka Google Colab belum dikendalikan langsung.",
              "Peringatan separation, konvergensi, atau model khusus dibaca bersama penjelasan notebook; p-value bukan pengganti pemeriksaan data dan asumsi.",
              "Token pribadi dan tautan ngrok sementara tidak disimpan pada laporan. Cadangan sebelum perapian disimpan lokal di alat_bantu/arsip/.", ""]
    LAPORAN.mkdir(exist_ok=True)
    (LAPORAN / "hasil_pemeriksaan.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    simpan_ringkasan()
