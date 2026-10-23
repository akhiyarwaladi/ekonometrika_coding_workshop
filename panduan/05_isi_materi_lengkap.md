# Pelatihan Ekonometrika berbasis AI dan Coding

Materi untuk kegiatan Program Studi Ekonomi Pembangunan, FEB Universitas
Jambi, Senin **26 Oktober 2026**, mulai **08.30 WIB**, di Ruang Gedung
Hexagonal Lantai 2 Universitas Jambi. Acuan: surat undangan nomor
4186/DST/UN21.5/DL.17/2026 tertanggal 21 Oktober 2026.

Undangan menetapkan satu tanggal kegiatan dan tidak merinci jam selesai
atau pembagian peserta. Paket dua hari di bawah adalah bahan lengkap untuk
pendalaman. Folder `materi/01_ekonometrika` memuat contoh dan `materi/02_latihan` memuat
latihan. Pembagian ini membantu memilih bahan sesuai waktu yang tersedia.

## Jalur peserta tanpa latar belakang coding

Mulai dari [panduan pemula](01_panduan_pemula.md), lalu buka
`materi/01_ekonometrika/00_persiapan_colab.ipynb`. Peserta menjalankan contoh,
mengubah satu bagian, dan menjelaskan hasilnya. Tidak perlu menulis program
dari halaman kosong.

| Urutan untuk kegiatan satu hari | Bahan | Hasil yang dituju |
|---|---|---|
| Persiapan | Panduan pemula dan Sesi 0 | Bisa menjalankan sel dan membaca tabel. |
| Regresi | Sesi 1 | Bisa membaca koefisien, p-value, dan prediksi. |
| Bentuk model | Contoh utama Sesi 2 | Bisa membedakan unit, persen, dan pola lengkung. |
| Pemeriksaan model | Contoh dummy, VIF, dan HC3 di Sesi 3 | Bisa menjelaskan basis dummy dan alasan koreksi SE. |
| Pendampingan AI | [Panduan praktik AI](02_panduan_ai.md) | Bisa memeriksa kode dan interpretasi yang disarankan AI. |
| Praktik peserta | Lab 1 dan kuncinya | Menghasilkan satu analisis yang dapat dijelaskan sendiri. |

Model kategorikal, deret waktu, panel, GARCH, dan kasus Indonesia lengkap
tetap tersedia untuk sesi lanjutan. Usulan pembagian waktu satu hari ada
di `pengajar/panduan_fasilitator.md`; waktunya bukan rundown resmi.

## Paket pendalaman dua hari

Materi workshop 2 hari berbasis Python untuk mata kuliah Ekonometrika.
Hari pertama untuk dosen dan pengajar, hari kedua latihan terbimbing untuk
mahasiswa.

Data dan kasus diambil dari halaman kuliah Ekonometrika
(https://paggalih.github.io/matkul/sem2025-01/ekonometrika/), ditambah
beberapa contoh dari dataset bawaan statsmodels. Semua data disimpan lokal
di folder `data/`, jadi pembacaan CSV tidak mengunduh data lagi. Google
Colab dan pemasangan paket tetap memerlukan koneksi internet.

Pustaka yang dipakai: pandas (tabel), scikit-learn (model linear, logit,
multinomial, Poisson, prediksi, dan evaluasi), statsmodels (pelengkap inferensi,
uji diagnostik, serta model khusus), matplotlib dan seaborn (grafik), linearmodels (data panel),
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
mana arah materinya. Istilah teknis dikumpulkan di `panduan/03_glosarium.md` beserta
sesi tempat istilah itu muncul pertama kali.

Di tengah setiap sesi ada checkpoint "Coba sendiri" berisi tugas singkat
5 menit dengan jawaban yang bisa dibuka lewat tombol "Lihat jawaban".
Totalnya 21 checkpoint, tersebar dari Sesi 0 sampai Lab 6. Tujuannya
supaya peserta aktif mencoba sendiri, bukan hanya menonton demo.

## Struktur folder

[Struktur folder terbaru](../README.md#letak-berkas) dan
[daftar seluruh notebook](00_daftar_materi.md) menjadi acuan lokasi berkas.

## Cara pakai di Google Colab

1. Unduh paket ini, lalu unggah notebook `.ipynb` yang diinginkan ke
   Colab (File > Upload notebook).
2. Unggah `data_tutorial.zip` dari folder `paket/` lewat panel Files di kiri Colab.
3. Jalankan sel pertama. Zip akan diekstrak otomatis ke folder `data/`.
4. Lanjutkan dari atas ke bawah dengan `Shift + Enter`.

Notebook yang memakai panel/GARCH menyediakan sel instalasi dengan versi
`linearmodels==7.1` dan `arch==8.0.0`. Jalankan saat runtime baru, tunggu
selesai, lalu lanjutkan. Uji Hausman memakai fasilitas linearmodels 7.1.
Data dan alat bantu ikut disiapkan dari paket ZIP yang sama.

## Cara pakai di komputer sendiri

1. Ekstrak seluruh paket.
2. Buka file `.py` di VS Code atau editor lain yang mengenali format
   sel `# %%`, atau konversi ke `.ipynb` dengan:

```bash
python alat_bantu/konversi_notebook.py
```

3. Pasang paket dengan `python -m pip install -r requirements.txt`.
4. Pertahankan susunan folder proyek. Sel persiapan menemukan folder data
   dari folder utama atau dari folder notebook masing-masing. Buka versi
   `.ipynb` untuk menjalankan sel `%pip`. Berkas `.py` adalah sumber dengan
   penanda sel, sehingga tidak dijalankan langsung lewat `python nama.py`.

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
| `pengajar/panduan_fasilitator.md` | rencana dua hari, poin mengajar, rencana cadangan |
| `pengajar/kunci_jawaban/catatan_latihan.md` | jawaban latihan hari 1 |

## Isi materi hari 2 (mahasiswa)

| File | Isi |
|---|---|
| `00_persiapan_colab.py` | mulai dari nol, regresi pertama |
| `01_regresi_dasar.py` | regresi berganda dan prediksi |
| `02_bentuk_fungsional.py` | memilih bentuk model |
| `03_dummy_asumsi_klasik.py` | dummy, VIF, heteroskedastisitas, normalitas |
| `04_model_kategorikal.py` | logit, ordinal, poisson |
| `05_deret_waktu_panel.py` | ADF, ARIMA, kointegrasi, panel |
| `06_data_indonesia.py` | GARCH IHSG, panel ASEAN, makro Indonesia asli |
| `07_proyek_mini.md` | tugas akhir dan rubrik |
| `pengajar/kunci_jawaban/` | solusi lengkap semua lab |

## Memeriksa ulang seluruh materi

Setelah mengedit sumber `.py`, buat ulang notebook dan paket data:

```bash
python alat_bantu/konversi_notebook.py
python alat_bantu/kemas_data.py
python alat_bantu/uji_notebook.py
python alat_bantu/uji_notebook.py --dari-zip
```

Pemeriksaan menjalankan sel kode `.ipynb` dari atas ke bawah, termasuk
ekspresi tabel di akhir sel, dan memastikan isinya sama dengan sumber
`.py`. Opsi `--dari-zip` memberi setiap notebook folder kosong yang hanya
berisi ZIP, sehingga tidak meminjam data atau variabel notebook lain.
Sel instalasi dilewati pada uji lokal karena paket sudah dipasang.
Log output dan warning statistik tersimpan di `laporan/uji_notebook_lokal.log`.
Latihan yang masih berupa komentar tetap dikerjakan peserta; kuncinya
diuji sebagai notebook tersendiri. Uji lokal belum menggantikan gladi
bersih antarmuka Google Colab sebelum acara.

Kode utama ditulis berurutan, tanpa fungsi buatan sendiri, comprehension,
perulangan bersarang, atau operasi matriks manual. Estimasi Tobit dan
penanganan demonstrasi separation tersedia terbuka di `alat_bantu/metode_lanjutan.py`.
Perkakas pengajar di `alat_bantu/` tidak perlu dipelajari peserta.

## Galeri visualisasi

Folder `gambar/ekonometrika/` berisi 17 gambar hasil analisis di tutorial, digambar
dengan gaya yang seragam (palet hijau tua, terracotta, emas): scatter
regresi dengan garis OLS, kurva reciprocal dan polinomial, diagram VIF,
uji heteroskedastisitas dan normalitas, efek marjinal logit, ramalan
ARIMA, perbandingan koefisien panel, GARCH IHSG asli, krisis inflasi
1998, dan cross-section provinsi. File `gambar/ekonometrika/galeri.png` memuat
semuanya dalam satu lembar untuk evaluasi cepat.

Buat ulang dengan `python alat_bantu/buat_gambar.py`. Notebook juga
memakai palet yang sama, jadi grafik di kelas dan gambar di folder ini
konsisten.

## Slide pembuka

`slide/01_pengantar_workshop.pptx` berisi 18 slide untuk membuka workshop: peta dua
hari, pembagian tugas statsmodels dan scikit-learn, ringkasan tiap sesi,
contoh kode, dan kendala umum. Setiap slide punya catatan pembicara.
Buat ulang dengan `python alat_bantu/buat_slide.py`.

## Catatan data

- 32 CSV berasal langsung dari repositori halaman kuliah (`regresi_log.csv`,
  `hetero_1.csv` sampai `hetero_3.csv`, `uts_1.csv` sampai `uts_6.csv`, dan seterusnya).
- 17 CSV lain dibuat dari tabel inline Pertemuan 3 dan 12-15 yang tidak
  tersedia sebagai file unduhan di halaman kuliah (`ts_*`, `panel_*`,
  `volatilitas.csv`, `pendidikan_pendapatan.csv`, `usia_unit.csv`,
  `jam_skor.csv`). Script pembuatnya ada di `alat_bantu/buat_data_simulasi.py`.
- 9 CSV adalah data asli dari sumber terbuka, delapan di antaranya
  Indonesia, dipakai di Lab 6 dan latihannya:

  | File | Isi | Sumber |
  |---|---|---|
  | `ihsg_harian.csv` | IHSG harian 2019 sampai 2026 | Yahoo Finance |
  | `ihsg_panjang.csv` | IHSG harian 1990 sampai 2026 | Yahoo Finance |
  | `kurs_harian.csv` | Kurs USD/IDR harian 2019 sampai 2026 | ECB via Frankfurter |
  | `idn_kurs_tahunan.csv` | Kurs tahunan 1967 sampai 2025, memuat krisis 1998 | World Bank |
  | `idn_inflasi_bulanan.csv` | Inflasi bulanan 1968 sampai 2025 | BPS via OECD/FRED |
  | `idn_makro_tahunan.csv` | Inflasi, PDB, pengangguran, kurs 2000 sampai 2025 | World Bank |
  | `asean_panel.csv` | Panel 10 negara ASEAN 2000 sampai 2025 | World Bank |
  | `provinsi_2021.csv` | 34 provinsi: PDRB, IPM, kemiskinan, dll | kompilasi BPS |
  | `kredit_default.csv` | 1.000 nasabah kartu kredit, bahan latihan logit | UCI (Taiwan) |

  Perbarui dengan `python alat_bantu/unduh_data_indonesia.py` (butuh internet,
  dan `xlrd` untuk data kredit default).
- Sebagian besar data kursus adalah simulasi dengan konteks Indonesia.
  Kalau butuh data asli untuk tugas atau skripsi, mulai dari Lab 6 dan
  `panduan/04_referensi.md` bagian sumber data Indonesia.
- Beberapa data simulasi punya perilaku khusus yang dibahas terbuka di
  notebook: logit dengan perfect separation dan GARCH yang menaksir beta
  dekat nol. Parameter ambang ordinal pada summary perlu ditransformasi
  sebelum dibaca sebagai batas kategori. Hal-hal ini menjadi bahan diskusi yang
  bagus, bukan alasan untuk menyembunyikan data.
- Sebagian CSV cadangan (misalnya `uts_5.csv`, `panel_kesehatan.csv`,
  `tobit_data_2_jamkerja.csv`) tidak dipakai di jalur utama. Daftar
  lengkap dan saran latihannya ada di `pengajar/panduan_fasilitator.md`.

## Praktik regresi Housing

[Notebook Housing](../materi/03_regresi_housing/01_regresi_housing.ipynb)
melengkapi contoh ekonometrika dengan supervised learning sesuai
[slide regresi](../slide/02_regresi_machine_learning.pdf). Data tambahan
`data/housing.csv` memuat 506 baris dan 14 kolom; total paket menjadi 59 CSV.
Notebook mencakup pembagian train/test, imputasi berdasarkan train, regresi
sederhana dan berganda, VIF, RMSE, R², prediksi baru, serta validasi
underfitting/overfitting. Hasil uji ada di [laporan Housing](../laporan/uji_regresi_housing.md).
