# Workshop Ekonometrika dengan Google Colab

Materi workshop 2 hari berbasis Python untuk mata kuliah Ekonometrika.
Hari pertama untuk dosen dan pengajar, hari kedua latihan terbimbing untuk
mahasiswa.

Data dan kasus diambil dari halaman kuliah Ekonometrika
(https://paggalih.github.io/matkul/sem2025-01/ekonometrika/), ditambah
beberapa contoh dari dataset bawaan statsmodels. Semua data disimpan lokal
di folder `data/`, jadi notebook tidak perlu internet untuk membacanya.

Pustaka yang dipakai: pandas, statsmodels (estimasi dan inferensi,
termasuk semua uji ekonometrika), scikit-learn (metrik prediksi dan
klasifikasi), matplotlib dan seaborn (grafik), linearmodels (data panel),
arch (GARCH). Pembagian tugas statsmodels dan scikit-learn dijelaskan di
Sesi 0 dan diperagakan berdampingan di Sesi 4.

## Benang merah

Materi disusun sebagai satu cerita, bukan kumpulan topik lepas:

1. Sesi 1 mulai dari regresi linear dan sengaja menunjukkan kegagalannya
   pada hubungan melengkung.
2. Sesi 2 memilih bentuk fungsional yang tepat.
3. Sesi 3 memeriksa apakah model layak dipercaya (asumsi klasik).
4. Sesi 4 mengganti jenis variabel Y: kategori, hitungan, tersensor.
5. Sesi 5 menambah dimensi waktu: stasioneritas, kointegrasi, ECM.
6. Sesi 6 menutup dengan data panel dan pemodelan volatilitas (GARCH).
7. Hari 2 mengulang alur yang sama sebagai latihan (Lab 0 sampai 5), lalu
   menutup dengan data Indonesia asli (Lab 6) dan proyek mini.

Setiap notebook membuka dengan blok "Posisi dalam alur workshop" dan
menutup dengan "Selanjutnya", jadi pembaca selalu tahu dari mana dan ke
mana arah materinya. Istilah teknis dikumpulkan di `glosarium.md` beserta
sesi tempat istilah itu muncul pertama kali.

Di tengah setiap sesi ada checkpoint "Coba sendiri" berisi tugas singkat
5 menit dengan jawaban yang bisa dibuka lewat tombol "Lihat jawaban".
Totalnya 21 checkpoint, tersebar dari Sesi 0 sampai Lab 6. Tujuannya
supaya peserta aktif mencoba sendiri, bukan hanya menonton demo.

## Struktur folder

```
ekonometrika/
  README.md
  glosarium.md              istilah penting dan sesi tempat munculnya
  referensi.md              sumber belajar lanjutan dan sumber data Indonesia
  data/                     58 file CSV
  data-ekonometrika.zip     paket data untuk diunggah ke Colab
  visualisasi/              17 gambar hasil tutorial (siap dipakai di slide)
  slide-workshop.pptx       slide pembuka, lengkap dengan catatan pembicara
  hari-1-dosen/             materi hari 1 (untuk dosen)
    00_persiapan_colab.py ... 06_panel_garch.py
    panduan_fasilitator.md
    kunci_latihan.md
  hari-2-mahasiswa/         materi hari 2 (untuk mahasiswa)
    lab0_setup.py ... lab6_data_indonesia.py
    proyek_mini.md
    kunci/                  solusi semua lab
  scripts/                  alat bantu (bukan bahan ajar)
    make_inline_data.py     membuat CSV dari data inline Pertemuan 3 dan 12-15
    fetch_indonesia_data.py mengunduh data Indonesia asli (butuh internet)
    py_to_ipynb.py          konversi .py ke .ipynb untuk Colab
    run_notebooks.py        menjalankan semua notebook untuk uji error
    make_slides.py          membuat ulang slide-workshop.pptx
    make_visualizations.py  membuat ulang semua gambar di visualisasi/
```

## Cara pakai di Google Colab

1. Unduh paket ini, lalu unggah notebook `.ipynb` yang diinginkan ke
   Colab (File > Upload notebook).
2. Unggah `data-ekonometrika.zip` lewat panel Files di kiri Colab.
3. Jalankan sel pertama. Zip akan diekstrak otomatis ke folder `data/`.
4. Lanjutkan dari atas ke bawah dengan `Shift + Enter`.

Di sesi 6 ada sel `%pip install linearmodels arch -q` yang butuh internet.
Jalankan sekali saat masih ada koneksi.

## Cara pakai di komputer sendiri

1. Ekstrak seluruh paket.
2. Buka file `.py` di VS Code atau editor lain yang mengenali format
   sel `# %%`, atau konversi ke `.ipynb` dengan:

```bash
python scripts/py_to_ipynb.py
```

3. Pastikan folder `data/` berada di sebelah notebook, lalu jalankan.

## Isi materi hari 1 (dosen)

| File | Isi |
|---|---|
| `00_persiapan_colab.py` | Colab, cara baca data, padanan perintah EViews |
| `01_regresi_dasar.py` | OLS, uji t dan F, R kuadrat, prediksi |
| `02_bentuk_fungsional.py` | log-log, reciprocal, polinomial |
| `03_dummy_asumsi_klasik.py` | dummy, VIF, Breusch-Pagan, Jarque-Bera, autokorelasi |
| `04_model_kategorikal.py` | logit, probit, multinomial, ordinal, tobit, poisson |
| `05_deret_waktu_kointegrasi.py` | ADF, ARIMA, kointegrasi, ECM |
| `06_panel_garch.py` | CEM/FEM/REM, uji Chow dan Hausman, GARCH(1,1) |
| `panduan_fasilitator.md` | rencana dua hari, poin mengajar, rencana cadangan |
| `kunci_latihan.md` | jawaban latihan hari 1 |

## Isi materi hari 2 (mahasiswa)

| File | Isi |
|---|---|
| `lab0_setup.py` | mulai dari nol, regresi pertama |
| `lab1_regresi_dasar.py` | regresi berganda dan prediksi |
| `lab2_bentuk_fungsional.py` | memilih bentuk model |
| `lab3_dummy_dan_asumsi.py` | dummy, VIF, heteroskedastisitas, normalitas |
| `lab4_kategorikal.py` | logit, ordinal, poisson |
| `lab5_deret_waktu_panel.py` | ADF, ARIMA, kointegrasi, panel |
| `lab6_data_indonesia.py` | GARCH IHSG, panel ASEAN, makro Indonesia asli |
| `proyek_mini.md` | tugas akhir dan rubrik |
| `kunci/` | solusi lengkap semua lab |

## Memeriksa ulang seluruh materi

Semua notebook diuji dengan menjalankannya dari atas ke bawah:

```bash
python scripts/run_notebooks.py
```

Log lengkap tersimpan di `scripts/run_output.log`. Hasil terakhir:
21 dari 21 notebook berjalan tanpa error.

## Galeri visualisasi

Folder `visualisasi/` berisi 17 gambar hasil analisis di tutorial, digambar
dengan gaya yang seragam (palet hijau tua, terracotta, emas): scatter
regresi dengan garis OLS, kurva reciprocal dan polinomial, diagram VIF,
uji heteroskedastisitas dan normalitas, efek marjinal logit, ramalan
ARIMA, perbandingan koefisien panel, GARCH IHSG asli, krisis inflasi
1998, dan cross-section provinsi. File `visualisasi/gallery.png` memuat
semuanya dalam satu lembar untuk evaluasi cepat.

Buat ulang dengan `python scripts/make_visualizations.py`. Notebook juga
memakai palet yang sama, jadi grafik di kelas dan gambar di folder ini
konsisten.

## Slide pembuka

`slide-workshop.pptx` berisi 18 slide untuk membuka workshop: peta dua
hari, pembagian tugas statsmodels dan scikit-learn, ringkasan tiap sesi,
contoh kode, dan kendala umum. Setiap slide punya catatan pembicara.
Buat ulang dengan `python scripts/make_slides.py`.

## Catatan data

- 32 CSV berasal langsung dari repositori halaman kuliah (regresi-log,
  hetero-1 sampai 3, uts-1 sampai 6, dan seterusnya).
- 17 CSV lain dibuat dari tabel inline Pertemuan 3 dan 12-15 yang tidak
  tersedia sebagai file unduhan di halaman kuliah (`ts-*`, `panel-*`,
  `volatilitas.csv`, `pendidikan-pendapatan.csv`, `usia-unit.csv`,
  `jam-skor.csv`). Script pembuatnya ada di `scripts/make_inline_data.py`.
- 9 CSV adalah data asli dari sumber terbuka, delapan di antaranya
  Indonesia, dipakai di Lab 6 dan latihannya:

  | File | Isi | Sumber |
  |---|---|---|
  | `ihsg-harian.csv` | IHSG harian 2019 sampai 2026 | Yahoo Finance |
  | `ihsg-panjang.csv` | IHSG harian 1990 sampai 2026 | Yahoo Finance |
  | `kurs-harian.csv` | Kurs USD/IDR harian 2019 sampai 2026 | ECB via Frankfurter |
  | `idn-kurs-tahunan.csv` | Kurs tahunan 1967 sampai 2025, memuat krisis 1998 | World Bank |
  | `idn-inflasi-bulanan.csv` | Inflasi bulanan 1968 sampai 2025 | BPS via OECD/FRED |
  | `idn-makro-tahunan.csv` | Inflasi, PDB, pengangguran, kurs 2000 sampai 2025 | World Bank |
  | `asean-panel.csv` | Panel 10 negara ASEAN 2000 sampai 2025 | World Bank |
  | `provinsi-2021.csv` | 34 provinsi: PDRB, IPM, kemiskinan, dll | kompilasi BPS |
  | `kredit-default.csv` | 1.000 nasabah kartu kredit, bahan latihan logit | UCI (Taiwan) |

  Perbarui dengan `python scripts/fetch_indonesia_data.py` (butuh internet,
  dan `xlrd` untuk data kredit default).
- Sebagian besar data kursus adalah simulasi dengan konteks Indonesia.
  Kalau butuh data asli untuk tugas atau skripsi, mulai dari Lab 6 dan
  `referensi.md` bagian sumber data Indonesia.
- Beberapa data simulasi punya perilaku khusus yang dibahas terbuka di
  notebook: logit dengan perfect separation, GARCH murni ARCH, dan
  threshold ordinal yang tidak berurutan. Ini justru bahan diskusi yang
  bagus, bukan alasan untuk menyembunyikan data.
- Sebagian CSV cadangan (misalnya `uts-5.csv`, `panel-kesehatan.csv`,
  `tobit_data_2_jamkerja.csv`) tidak dipakai di jalur utama. Daftar
  lengkap dan saran latihannya ada di `hari-1-dosen/panduan_fasilitator.md`.
