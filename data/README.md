# Data tutorial dan arti variabel

**Data tidak perlu diunggah ke Colab.** Notebook membaca atau mengunduh berkas langsung dari GitHub.
Untuk dashboard, data yang dipakai hanya **provinsi_2021.csv**.

- **45 CSV aktif** berada di folder data/.
- **14 CSV cadangan** berada di data/cadangan/ dan belum dipakai oleh notebook saat ini.
- Arti variabel juga tersedia pada bagian **Kenali data** di setiap notebook.

[Kembali ke materi](../README.md) · [Dasar notebook](../README.md#dasar-notebook)

## Contoh berbagai format pada Sesi 0

Satu tabel makro Indonesia 2000 sampai 2025, berisi 26 baris dan tujuh kolom.
[CSV sumber](idn_makro_tahunan.csv) tetap menjadi acuan. Enam salinan berikut berada pada satu folder contoh_format/ dan semuanya dipakai dalam tutorial pembuka.
SPSS dan Stata adalah hasil konversi untuk latihan membaca berkas, bukan mikrodata survei asli. Nama kolom dan angka dipertahankan.

| Format | Berkas | Cara membaca |
|---|---|---|
| Excel | [idn_makro_tahunan.xlsx](contoh_format/idn_makro_tahunan.xlsx) | `pd.read_excel(..., sheet_name="data")` |
| SPSS | [idn_makro_tahunan.sav](contoh_format/idn_makro_tahunan.sav) | `pd.read_spss(...)` |
| Stata | [idn_makro_tahunan.dta](contoh_format/idn_makro_tahunan.dta) | `pd.read_stata(...)` |
| Teks tab/TSV | [idn_makro_tahunan.tsv](contoh_format/idn_makro_tahunan.tsv) | `pd.read_csv(..., sep="\t")` |
| JSON | [idn_makro_tahunan.json](contoh_format/idn_makro_tahunan.json) | `pd.read_json(..., orient="records")` |
| Parquet | [idn_makro_tahunan.parquet](contoh_format/idn_makro_tahunan.parquet) | `pd.read_parquet(...)` |

Definisi kolom mengikuti [kamus makro Indonesia](#idn_makro_tahunan_csv). Excel menyediakan lembar data dan sumber.
Sumber: [World Bank Indonesia](https://data.worldbank.org/country/indonesia), lisensi CC BY 4.0. Salinan CSV tutorial dipertahankan agar angka konsisten dengan Lab 6.

## Data yang dipakai tiap notebook

| Notebook | Data |
|---|---|
| [materi/01_ekonometrika/00_persiapan_colab.ipynb](../materi/01_ekonometrika/00_persiapan_colab.ipynb) | [idn_makro_tahunan.csv](#idn_makro_tahunan_csv), [provinsi_2021.csv](#provinsi_2021_csv) |
| [materi/01_ekonometrika/01_regresi_dasar.ipynb](../materi/01_ekonometrika/01_regresi_dasar.ipynb) | [uts_2.csv](#uts_2_csv), [regresi_polinom.csv](#regresi_polinom_csv) |
| [materi/01_ekonometrika/02_bentuk_fungsional.ipynb](../materi/01_ekonometrika/02_bentuk_fungsional.ipynb) | [regresi_log.csv](#regresi_log_csv), [regresi_reciprocal.csv](#regresi_reciprocal_csv), [regresi_polinom.csv](#regresi_polinom_csv), [usia_unit.csv](#usia_unit_csv) |
| [materi/01_ekonometrika/03_dummy_asumsi_klasik.ipynb](../materi/01_ekonometrika/03_dummy_asumsi_klasik.ipynb) | [latihan_dummy_1.csv](#latihan_dummy_1_csv), [latihan_dummy_2.csv](#latihan_dummy_2_csv), [contoh_did](#contoh_did), [latihan_multikolinieritas_1.csv](#latihan_multikolinieritas_1_csv), [hetero_3.csv](#hetero_3_csv), [latihan_normalitas_1.csv](#latihan_normalitas_1_csv) |
| [materi/01_ekonometrika/04_model_kategorikal.ipynb](../materi/01_ekonometrika/04_model_kategorikal.ipynb) | [spector](#spector), [logit_probit_2.csv](#logit_probit_2_csv), [kredit_default.csv](#kredit_default_csv), [multi_ordinal_2.csv](#multi_ordinal_2_csv), [multi_ordinal_1.csv](#multi_ordinal_1_csv), [tobit_data_1_rnd.csv](#tobit_data_1_rnd_csv), [poisson_data_2_restoran.csv](#poisson_data_2_restoran_csv) |
| [materi/01_ekonometrika/05_deret_waktu_kointegrasi.ipynb](../materi/01_ekonometrika/05_deret_waktu_kointegrasi.ipynb) | [ts_inflasi.csv](#ts_inflasi_csv), [ts_saham.csv](#ts_saham_csv), [ts_gdp_growth.csv](#ts_gdp_growth_csv), [ts_kurs.csv](#ts_kurs_csv), [idn_inflasi_bulanan.csv](#idn_inflasi_bulanan_csv), [konsumsi_pendapatan.csv](#konsumsi_pendapatan_csv) |
| [materi/01_ekonometrika/06_panel_garch.ipynb](../materi/01_ekonometrika/06_panel_garch.ipynb) | [panel_gdp.csv](#panel_gdp_csv), [volatilitas.csv](#volatilitas_csv) |
| [materi/02_latihan/00_persiapan_colab.ipynb](../materi/02_latihan/00_persiapan_colab.ipynb) | [idn_makro_tahunan.csv](#idn_makro_tahunan_csv), [provinsi_2021.csv](#provinsi_2021_csv) |
| [materi/02_latihan/01_regresi_dasar.ipynb](../materi/02_latihan/01_regresi_dasar.ipynb) | [uts_6.csv](#uts_6_csv), [uts_3.csv](#uts_3_csv), [uts_4.csv](#uts_4_csv) |
| [materi/02_latihan/02_bentuk_fungsional.ipynb](../materi/02_latihan/02_bentuk_fungsional.ipynb) | [regresi_log.csv](#regresi_log_csv), [pendidikan_pendapatan.csv](#pendidikan_pendapatan_csv), [usia_unit.csv](#usia_unit_csv), [jam_skor.csv](#jam_skor_csv), [uts_1.csv](#uts_1_csv) |
| [materi/02_latihan/03_dummy_asumsi_klasik.ipynb](../materi/02_latihan/03_dummy_asumsi_klasik.ipynb) | [latihan_dummy_1.csv](#latihan_dummy_1_csv), [latihan_multikolinieritas_1.csv](#latihan_multikolinieritas_1_csv), [contoh_did](#contoh_did), [hetero_2.csv](#hetero_2_csv), [latihan_normalitas_3.csv](#latihan_normalitas_3_csv), [hetero_1.csv](#hetero_1_csv) |
| [materi/02_latihan/04_model_kategorikal.ipynb](../materi/02_latihan/04_model_kategorikal.ipynb) | [spector](#spector), [kredit_default.csv](#kredit_default_csv), [logit_probit_2.csv](#logit_probit_2_csv), [multi_ordinal_1.csv](#multi_ordinal_1_csv), [poisson_data_1_klaim.csv](#poisson_data_1_klaim_csv) |
| [materi/02_latihan/05_deret_waktu_panel.ipynb](../materi/02_latihan/05_deret_waktu_panel.ipynb) | [ts_inflasi.csv](#ts_inflasi_csv), [konsumsi_pendapatan.csv](#konsumsi_pendapatan_csv), [panel_padi.csv](#panel_padi_csv), [idn_inflasi_bulanan.csv](#idn_inflasi_bulanan_csv), [ts_saham.csv](#ts_saham_csv), [ihsg_emas.csv](#ihsg_emas_csv), [panel_retail.csv](#panel_retail_csv) |
| [materi/02_latihan/06_data_indonesia.ipynb](../materi/02_latihan/06_data_indonesia.ipynb) | [ihsg_harian.csv](#ihsg_harian_csv), [asean_panel.csv](#asean_panel_csv), [idn_makro_tahunan.csv](#idn_makro_tahunan_csv), [kurs_harian.csv](#kurs_harian_csv), [idn_inflasi_bulanan.csv](#idn_inflasi_bulanan_csv), [idn_kurs_tahunan.csv](#idn_kurs_tahunan_csv), [ihsg_panjang.csv](#ihsg_panjang_csv), [provinsi_2021.csv](#provinsi_2021_csv) |
| [materi/03_regresi_housing/01_regresi_housing.ipynb](../materi/03_regresi_housing/01_regresi_housing.ipynb) | [contoh_taksi](#contoh_taksi), [housing.csv](#housing_csv) |
| [materi/04_dashboard_indonesia/01_dashboard_ekonomi.ipynb](../materi/04_dashboard_indonesia/01_dashboard_ekonomi.ipynb) | [provinsi_2021.csv](#provinsi_2021_csv) |
| [pengajar/kunci_jawaban/00_persiapan_colab.ipynb](../pengajar/kunci_jawaban/00_persiapan_colab.ipynb) | [idn_makro_tahunan.csv](#idn_makro_tahunan_csv), [provinsi_2021.csv](#provinsi_2021_csv) |
| [pengajar/kunci_jawaban/01_regresi_dasar.ipynb](../pengajar/kunci_jawaban/01_regresi_dasar.ipynb) | [uts_3.csv](#uts_3_csv), [uts_4.csv](#uts_4_csv), [uts_6.csv](#uts_6_csv) |
| [pengajar/kunci_jawaban/02_bentuk_fungsional.ipynb](../pengajar/kunci_jawaban/02_bentuk_fungsional.ipynb) | [pendidikan_pendapatan.csv](#pendidikan_pendapatan_csv), [usia_unit.csv](#usia_unit_csv), [jam_skor.csv](#jam_skor_csv), [uts_1.csv](#uts_1_csv) |
| [pengajar/kunci_jawaban/03_dummy_asumsi_klasik.ipynb](../pengajar/kunci_jawaban/03_dummy_asumsi_klasik.ipynb) | [hetero_2.csv](#hetero_2_csv), [latihan_normalitas_3.csv](#latihan_normalitas_3_csv), [hetero_1.csv](#hetero_1_csv), [contoh_did](#contoh_did) |
| [pengajar/kunci_jawaban/04_model_kategorikal.ipynb](../pengajar/kunci_jawaban/04_model_kategorikal.ipynb) | [logit_probit_2.csv](#logit_probit_2_csv), [multi_ordinal_1.csv](#multi_ordinal_1_csv), [poisson_data_1_klaim.csv](#poisson_data_1_klaim_csv), [kredit_default.csv](#kredit_default_csv) |
| [pengajar/kunci_jawaban/05_deret_waktu_panel.ipynb](../pengajar/kunci_jawaban/05_deret_waktu_panel.ipynb) | [ts_saham.csv](#ts_saham_csv), [ihsg_emas.csv](#ihsg_emas_csv), [panel_retail.csv](#panel_retail_csv), [idn_inflasi_bulanan.csv](#idn_inflasi_bulanan_csv) |
| [pengajar/kunci_jawaban/06_data_indonesia.ipynb](../pengajar/kunci_jawaban/06_data_indonesia.ipynb) | [kurs_harian.csv](#kurs_harian_csv), [ihsg_panjang.csv](#ihsg_panjang_csv), [provinsi_2021.csv](#provinsi_2021_csv), [asean_panel.csv](#asean_panel_csv) |

## Cari nama dataset

| Data | Status | Isi |
|---|---|---|
| [asean_panel.csv](#asean_panel_csv) | dipakai | Panel negara ASEAN dari World Bank |
| [contoh_did](#contoh_did) | contoh di kode | Simulasi evaluasi bantuan dan pendapatan |
| [contoh_taksi](#contoh_taksi) | contoh di kode | Contoh hitungan tarif taksi |
| [data_regresi_uts.csv](#data_regresi_uts_csv) | cadangan | Data abstrak untuk latihan spesifikasi |
| [ekspor_kurs.csv](#ekspor_kurs_csv) | cadangan | Ekspor dan nilai tukar |
| [hetero_1.csv](#hetero_1_csv) | dipakai | Iklan, tenaga penjualan, dan diskon |
| [hetero_2.csv](#hetero_2_csv) | dipakai | Pendapatan dan karakteristik pekerja |
| [hetero_3.csv](#hetero_3_csv) | dipakai | Harga dan karakteristik rumah |
| [housing.csv](#housing_csv) | dipakai | Harga rumah historis Boston |
| [idn_inflasi_bulanan.csv](#idn_inflasi_bulanan_csv) | dipakai | IHK dan inflasi Indonesia bulanan |
| [idn_kurs_tahunan.csv](#idn_kurs_tahunan_csv) | dipakai | Kurs rupiah tahunan |
| [idn_makro_tahunan.csv](#idn_makro_tahunan_csv) | dipakai | Makroekonomi Indonesia tahunan |
| [ihsg_emas.csv](#ihsg_emas_csv) | dipakai | IHSG dan harga emas simulasi |
| [ihsg_harian.csv](#ihsg_harian_csv) | dipakai | IHSG harian |
| [ihsg_panjang.csv](#ihsg_panjang_csv) | dipakai | IHSG riwayat panjang |
| [jam_skor.csv](#jam_skor_csv) | dipakai | Jam belajar dan hasil ujian |
| [konsumsi_pendapatan.csv](#konsumsi_pendapatan_csv) | dipakai | Konsumsi dan pendapatan runtun waktu |
| [kredit_default.csv](#kredit_default_csv) | dipakai | Gagal bayar kartu kredit Taiwan |
| [kurs_harian.csv](#kurs_harian_csv) | dipakai | Kurs rupiah harian |
| [latihan_dummy_1.csv](#latihan_dummy_1_csv) | dipakai | Gaji dan karakteristik pekerja |
| [latihan_dummy_2.csv](#latihan_dummy_2_csv) | dipakai | PDB, investasi, dan krisis |
| [latihan_multikolinieritas_1.csv](#latihan_multikolinieritas_1_csv) | dipakai | Harga dan ukuran rumah |
| [latihan_multikolinieritas_2.csv](#latihan_multikolinieritas_2_csv) | cadangan | Konsumsi rumah tangga |
| [latihan_normalitas_1.csv](#latihan_normalitas_1_csv) | dipakai | Harga saham dan kondisi makro |
| [latihan_normalitas_2.csv](#latihan_normalitas_2_csv) | cadangan | Hasil panen dan kondisi lahan |
| [latihan_normalitas_3.csv](#latihan_normalitas_3_csv) | dipakai | Harga dan kondisi rumah |
| [logit_probit_1.csv](#logit_probit_1_csv) | cadangan | Persetujuan kredit usaha |
| [logit_probit_2.csv](#logit_probit_2_csv) | dipakai | Kelulusan tepat waktu |
| [logit_probit_3.csv](#logit_probit_3_csv) | cadangan | Penggunaan mobile banking |
| [multi_ordinal_1.csv](#multi_ordinal_1_csv) | dipakai | Kepuasan layanan bank |
| [multi_ordinal_2.csv](#multi_ordinal_2_csv) | dipakai | Pilihan transportasi kerja |
| [multi_ordinal_3.csv](#multi_ordinal_3_csv) | cadangan | Rating risiko kredit UMKM |
| [panel_gdp.csv](#panel_gdp_csv) | dipakai | Panel PDB simulasi |
| [panel_kesehatan.csv](#panel_kesehatan_csv) | cadangan | Panel tekanan darah |
| [panel_padi.csv](#panel_padi_csv) | dipakai | Panel hasil panen padi |
| [panel_pendidikan.csv](#panel_pendidikan_csv) | cadangan | Panel hasil belajar |
| [panel_retail.csv](#panel_retail_csv) | dipakai | Panel toko ritel |
| [pendidikan_pendapatan.csv](#pendidikan_pendapatan_csv) | dipakai | Pendidikan dan pendapatan |
| [poisson_data_1_klaim.csv](#poisson_data_1_klaim_csv) | dipakai | Klaim asuransi mobil |
| [poisson_data_2_restoran.csv](#poisson_data_2_restoran_csv) | dipakai | Kunjungan pelanggan restoran |
| [poisson_data_3_cacat.csv](#poisson_data_3_cacat_csv) | cadangan | Cacat produksi |
| [provinsi_2021.csv](#provinsi_2021_csv) | dipakai | Indikator 34 provinsi tahun 2021 |
| [regresi_log.csv](#regresi_log_csv) | dipakai | Produksi, tenaga kerja, dan modal |
| [regresi_polinom.csv](#regresi_polinom_csv) | dipakai | Iklan dan penjualan |
| [regresi_reciprocal.csv](#regresi_reciprocal_csv) | dipakai | Pengalaman dan waktu produksi |
| [ritel_iklan.csv](#ritel_iklan_csv) | cadangan | Penjualan ritel dan iklan mingguan |
| [spector](#spector) | contoh di kode | Efektivitas metode pengajaran Spector |
| [tobit_data_1_rnd.csv](#tobit_data_1_rnd_csv) | dipakai | Pengeluaran penelitian dan pengembangan |
| [tobit_data_2_jamkerja.csv](#tobit_data_2_jamkerja_csv) | cadangan | Jam kerja dan keadaan keluarga |
| [tobit_data_3_asuransi.csv](#tobit_data_3_asuransi_csv) | cadangan | Pembelian premi asuransi |
| [ts_gdp_growth.csv](#ts_gdp_growth_csv) | dipakai | Pertumbuhan ekonomi simulasi |
| [ts_inflasi.csv](#ts_inflasi_csv) | dipakai | Deret harga/inflasi simulasi |
| [ts_kurs.csv](#ts_kurs_csv) | dipakai | Kurs simulasi |
| [ts_saham.csv](#ts_saham_csv) | dipakai | Harga saham simulasi |
| [usia_unit.csv](#usia_unit_csv) | dipakai | Usia dan kinerja penjual |
| [uts_1.csv](#uts_1_csv) | dipakai | Pertumbuhan ekonomi |
| [uts_2.csv](#uts_2_csv) | dipakai | Harga saham perusahaan |
| [uts_3.csv](#uts_3_csv) | dipakai | Produktivitas padi |
| [uts_4.csv](#uts_4_csv) | dipakai | Angka harapan hidup |
| [uts_5.csv](#uts_5_csv) | cadangan | Kriminalitas kota |
| [uts_6.csv](#uts_6_csv) | dipakai | Penjualan produk |
| [volatilitas.csv](#volatilitas_csv) | dipakai | Lima deret simulasi volatilitas |

## Definisi variabel

X adalah variabel penjelas, sedangkan Y adalah target. Satuan yang tidak dijelaskan sumber tidak ditebak dari besar angkanya.

<a id="asean_panel_csv"></a>

### Kenali data: Panel negara ASEAN dari World Bank

**Data:** `data/asean_panel.csv`. **Satu baris:** satu negara pada satu tahun.

| Variabel/kolom | Pengertian | Satuan atau kode | Peran |
|---|---|---|---|
| `Negara` | Kode negara ISO tiga huruf; misalnya IDN = Indonesia, MYS = Malaysia. | Kode negara | Penanda, bukan besaran ekonomi |
| `Tahun` | Tahun kalender pengamatan. | Tahun | Penanda waktu |
| `PDB_Growth` | Laju pertumbuhan tahunan PDB riil (Produk Domestik Bruto). | Persen per tahun; NY.GDP.MKTP.KD.ZG | Target pertumbuhan pada model panel |
| `Inflasi` | Kenaikan tahunan indeks harga konsumen. | Persen per tahun; FP.CPI.TOTL.ZG | Y atau X sesuai model |
| `Pengangguran` | Pengangguran sebagai bagian dari total angkatan kerja, estimasi model ILO. | Persen angkatan kerja; SL.UEM.TOTL.ZS | X: penjelas |
| `Kurs_USD` | Kurs resmi rata-rata periode: mata uang lokal untuk memperoleh satu dolar AS. | Mata uang lokal per US$1; PA.NUS.FCRF | X: penjelas |
| `FDI` | Arus masuk bersih investasi asing langsung relatif terhadap PDB. | Persen PDB; BX.KLT.DINV.WD.GD.ZS | X: penjelas |
| `Angkatan_Kerja` | Penduduk yang bekerja atau aktif mencari pekerjaan. | Orang; SL.TLF.TOTL.IN | X: penjelas |

Kurs_USD memakai mata uang negara masing-masing, sehingga IDN berarti rupiah/US$ dan MYS berarti ringgit/US$. FDI = 5 berarti 5% PDB; perubahan dari 5 ke 6 adalah 1 poin persen.

Kolom turunan berikut dibuat saat praktik; kolom ini belum ada pada CSV awal.

| Kolom turunan | Pengertian | Satuan/kode |
|---|---|---|
| `ln_angkatan_kerja` | Logaritma alami jumlah angkatan kerja. | Skala logaritma |

Sumber definisi: [rujukan data](https://databank.worldbank.org/source/world-development-indicators).

[Buka CSV](asean_panel.csv).

Dipakai pada: [06_data_indonesia](../materi/02_latihan/06_data_indonesia.ipynb), [06_data_indonesia](../pengajar/kunci_jawaban/06_data_indonesia.ipynb).

<a id="contoh_did"></a>

### Kenali data: Simulasi evaluasi bantuan dan pendapatan

**Data:** tabel contoh yang dibuat langsung di kode. **Satu baris:** satu kelompok pada satu tahun; delapan baris agregat, bukan delapan rumah tangga.

| Variabel/kolom | Pengertian | Satuan atau kode | Peran |
|---|---|---|---|
| `tahun` | Tahun pengamatan kelompok. | 2021 sampai 2024 | Penanda waktu |
| `peserta` | Penanda kelompok yang akan menerima program mulai 2023. | 1 = peserta; 0 = pembanding | X: dummy kelompok |
| `pendapatan` | Rata-rata pendapatan rumah tangga pada kelompok dan tahun tersebut. | Juta rupiah per bulan | Y: hasil yang dibandingkan |

Semua nilai adalah simulasi. Program mulai 2023. Setiap baris memiliki bobot sama untuk latihan; ini bukan hasil evaluasi PKH dan bukan dasar pengujian signifikansi statistik.

Kolom turunan berikut dibuat saat praktik; kolom ini belum ada pada CSV awal.

| Kolom turunan | Pengertian | Satuan/kode |
|---|---|---|
| `sesudah` | Penanda periode setelah program mulai. | 1 = tahun 2023 atau 2024; 0 = tahun 2021 atau 2022 |
| `interaksi` | Perkalian peserta dan sesudah; bernilai satu pada peserta setelah program. | Dummy 0 atau 1 |

Sumber: Angka ilustrasi buatan untuk pengantar DiD dalam notebook Sesi 03.

Dipakai pada: [03_dummy_asumsi_klasik](../materi/01_ekonometrika/03_dummy_asumsi_klasik.ipynb), [03_dummy_asumsi_klasik](../materi/02_latihan/03_dummy_asumsi_klasik.ipynb), [03_dummy_asumsi_klasik](../pengajar/kunci_jawaban/03_dummy_asumsi_klasik.ipynb).

<a id="contoh_taksi"></a>

### Kenali data: Contoh hitungan tarif taksi

**Data:** tabel contoh yang dibuat langsung di kode. **Satu baris:** satu jarak perjalanan yang ingin dihitung tarifnya.

| Variabel/kolom | Pengertian | Satuan atau kode | Peran |
|---|---|---|---|
| `km` | Jarak perjalanan. | Kilometer | X: penjelas |
| `taksi_standar` | Tarif awal Rp5.000 ditambah Rp4.000 untuk setiap kilometer. | Rupiah | Hasil hitungan |
| `taksi_premium` | Tarif awal Rp5.000 ditambah Rp7.500 untuk setiap kilometer. | Rupiah | Hasil hitungan |

Angka tarif hanya ilustrasi persamaan garis pada tutorial, bukan daftar tarif operator taksi saat ini.

Sumber: Contoh buatan dalam notebook Housing.

Dipakai pada: [01_regresi_housing](../materi/03_regresi_housing/01_regresi_housing.ipynb).

<a id="data_regresi_uts_csv"></a>

### Kenali data: Data abstrak untuk latihan spesifikasi

**Data:** `data/cadangan/data_regresi_uts.csv`. **Satu baris:** satu pengamatan hasil simulasi statistik.

| Variabel/kolom | Pengertian | Satuan atau kode | Peran |
|---|---|---|---|
| `Y` | Variabel respons simulasi tanpa label ekonomi khusus. | Skala simulasi | Y: target |
| `X1` | Variabel penjelas pertama pada simulasi. | Skala simulasi | X: penjelas |
| `X2` | Variabel penjelas kedua pada simulasi. | Skala simulasi | X: penjelas |
| `X3` | Variabel penjelas ketiga pada simulasi. | Skala simulasi | X: penjelas |
| `X4` | Variabel penjelas indikator pada simulasi. | Kode 0/1; makna ekonomi tidak ditetapkan | X: penjelas |
| `trend` | Tren linear berdasarkan urutan pengamatan. | Urutan mulai dari 0 | Penanda waktu |
| `error` | Komponen gangguan yang disertakan oleh pembuat simulasi. | Skala simulasi; bukan penjelas untuk prediksi data baru | Komponen simulasi |

Sumber tidak memberi konteks ekonomi untuk X1 sampai X4. Nama seperti pendapatan atau investasi tidak boleh ditambahkan tanpa dasar.

Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

[Buka CSV](cadangan/data_regresi_uts.csv).

Data cadangan: bahan tambahan pengajar, belum dibaca oleh notebook saat ini.

<a id="ekspor_kurs_csv"></a>

### Kenali data: Ekspor dan nilai tukar

**Data:** `data/cadangan/ekspor_kurs.csv`. **Satu baris:** satu kuartal berurutan pada contoh simulasi.

| Variabel/kolom | Pengertian | Satuan atau kode | Peran |
|---|---|---|---|
| `Kuartal` | Urutan periode tiga bulanan. | Nomor kuartal; tahun kalender tidak dicantumkan | Penanda waktu |
| `Ekspor_Y` | Nilai ekspor pada kuartal pengamatan. | Skala nilai ekspor tidak dirinci | Y: target |
| `Kurs_X` | Nilai tukar pada kuartal yang sama. | Pasangan mata uang/skala tidak dirinci sumber | X: penjelas |

Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

[Buka CSV](cadangan/ekspor_kurs.csv).

Data cadangan: bahan tambahan pengajar, belum dibaca oleh notebook saat ini.

<a id="hetero_1_csv"></a>

### Kenali data: Iklan, tenaga penjualan, dan diskon

**Data:** `data/hetero_1.csv`. **Satu baris:** satu pengamatan penjualan perusahaan dalam contoh.

| Variabel/kolom | Pengertian | Satuan atau kode | Peran |
|---|---|---|---|
| `Penjualan` | Banyaknya produk terjual. | Ribuan unit | Y: target |
| `Iklan` | Pengeluaran untuk iklan. | Juta rupiah | X: penjelas |
| `Salesperson` | Jumlah tenaga penjualan yang bekerja. | Orang | X: penjelas |
| `Diskon` | Rata-rata potongan harga yang diberikan. | Persen; 5,2 berarti 5,2% | X: penjelas |

Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

[Buka CSV](hetero_1.csv).

Dipakai pada: [03_dummy_asumsi_klasik](../materi/02_latihan/03_dummy_asumsi_klasik.ipynb), [03_dummy_asumsi_klasik](../pengajar/kunci_jawaban/03_dummy_asumsi_klasik.ipynb).

<a id="hetero_2_csv"></a>

### Kenali data: Pendapatan dan karakteristik pekerja

**Data:** `data/hetero_2.csv`. **Satu baris:** satu orang pada contoh latihan.

| Variabel/kolom | Pengertian | Satuan atau kode | Peran |
|---|---|---|---|
| `Pendapatan` | Pendapatan selama satu tahun. | Puluhan juta rupiah per tahun, sesuai uraian sumber | Y: target |
| `Pendidikan` | Lama pendidikan yang telah ditempuh. | Tahun | X: penjelas |
| `Pengalaman` | Lama pengalaman kerja. | Tahun | X: penjelas |
| `Usia` | Umur orang yang diamati. | Tahun | X: penjelas |

Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

[Buka CSV](hetero_2.csv).

Dipakai pada: [03_dummy_asumsi_klasik](../materi/02_latihan/03_dummy_asumsi_klasik.ipynb), [03_dummy_asumsi_klasik](../pengajar/kunci_jawaban/03_dummy_asumsi_klasik.ipynb).

<a id="hetero_3_csv"></a>

### Kenali data: Harga dan karakteristik rumah

**Data:** `data/hetero_3.csv`. **Satu baris:** satu rumah pada contoh latihan.

| Variabel/kolom | Pengertian | Satuan atau kode | Peran |
|---|---|---|---|
| `Harga` | Harga jual rumah. | Ratusan juta rupiah | Y: target |
| `Luas` | Luas bangunan rumah. | Meter persegi (m²) | X: penjelas |
| `Kamar` | Jumlah kamar tidur. | Kamar | X: penjelas |
| `Lokasi` | Skor kelayakan/kualitas lokasi rumah; bukan kode alamat. | Skor 1 sampai 10 | X: penjelas |

Kolom turunan berikut dibuat saat praktik; kolom ini belum ada pada CSV awal.

| Kolom turunan | Pengertian | Satuan/kode |
|---|---|---|
| `abs_resid` | Nilai mutlak selisih harga aktual dan prediksi untuk uji Glejser. | Sama dengan satuan Harga |

Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

[Buka CSV](hetero_3.csv).

Dipakai pada: [03_dummy_asumsi_klasik](../materi/01_ekonometrika/03_dummy_asumsi_klasik.ipynb).

<a id="housing_csv"></a>

### Kenali data: Harga rumah historis Boston

**Data:** `data/housing.csv`. **Satu baris:** satu wilayah sensus dalam data historis Boston, bukan satu rumah di Indonesia.

| Variabel/kolom | Pengertian | Satuan atau kode | Peran |
|---|---|---|---|
| `CRIM` | Tingkat kejahatan per kapita wilayah. | Tingkat per kapita | X: penjelas |
| `ZN` | Lahan hunian dengan kavling lebih dari 25.000 kaki persegi. | Persen lahan hunian | X: penjelas |
| `INDUS` | Proporsi lahan untuk bisnis nonritel di wilayah. | Persen | X: penjelas |
| `CHAS` | Apakah wilayah berbatasan dengan Sungai Charles. | 1 = ya; 0 = tidak | X: penjelas |
| `NOX` | Konsentrasi nitrogen oksida. | Bagian per 10 juta | X: penjelas |
| `RM` | Rata-rata jumlah kamar per hunian. | Kamar per hunian | X: penjelas |
| `AGE` | Hunian milik penghuni yang dibangun sebelum 1940. | Persen hunian, bukan umur rumah dalam tahun | X: penjelas |
| `DIS` | Jarak tertimbang ke lima pusat pekerjaan Boston. | Ukuran jarak tertimbang pada sumber | X: penjelas |
| `RAD` | Indeks akses ke jalan raya radial. | Indeks, bukan jarak kilometer | X: penjelas |
| `TAX` | Tarif pajak properti terhadap nilai penuh properti. | Pajak per US$10.000 nilai properti | X: penjelas |
| `PTRATIO` | Jumlah murid relatif terhadap jumlah guru di wilayah. | Murid per guru | X: penjelas |
| `BLACK` | B pada sumber historis: 1000 × (p - 0,63)²; p adalah proporsi penduduk kulit hitam. | Transformasi matematis, bukan persentase langsung | X: penjelas |
| `LSTAT` | Penduduk berstatus sosial ekonomi rendah menurut label historis sumber. | Persen penduduk | X: penjelas |
| `MEDV` | Median nilai rumah yang ditempati pemiliknya. | Ribuan dolar AS historis; 24 berarti US$24.000 | Y: target |

BLACK bukan hasil pengkodean biner dan AGE bukan usia satu rumah. Catatan keterbatasan dan bias dataset dibahas pada notebook Housing.

Sumber definisi: [rujukan data](https://lib.stat.cmu.edu/datasets/boston).

[Buka CSV](housing.csv).

Dipakai pada: [01_regresi_housing](../materi/03_regresi_housing/01_regresi_housing.ipynb).

<a id="idn_inflasi_bulanan_csv"></a>

### Kenali data: IHK dan inflasi Indonesia bulanan

**Data:** `data/idn_inflasi_bulanan.csv`. **Satu baris:** satu bulan kalender.

| Variabel/kolom | Pengertian | Satuan atau kode | Peran |
|---|---|---|---|
| `tanggal` | Bulan pengamatan; tanggal berfungsi sebagai penanda bulan. | Tanggal YYYY-MM-DD | Penanda waktu |
| `indeks` | Indeks Harga Konsumen (IHK), yaitu ukuran tingkat harga keranjang konsumsi. | Poin indeks; tahun dasar mengikuti seri sumber | Level harga |
| `inflasi_mom` | Persentase perubahan indeks dari bulan sebelumnya (month-on-month). | 100 × (indeks bulan ini / bulan lalu - 1) | Deret yang dianalisis |
| `inflasi_yoy` | Persentase perubahan indeks dari bulan yang sama setahun sebelumnya (year-on-year). | 100 × (indeks bulan ini / indeks 12 bulan lalu - 1) | Deret yang dianalisis |

indeks adalah level, sedangkan inflasi_mom dan inflasi_yoy adalah perubahan persen yang dihitung oleh skrip unduhan. Angka 2 pada kolom inflasi berarti 2%, bukan 0,02%.

Kolom turunan berikut dibuat saat praktik; kolom ini belum ada pada CSV awal.

| Kolom turunan | Pengertian | Satuan/kode |
|---|---|---|
| `era` | Label pengelompokan periode untuk ringkasan/grafik inflasi. | Kategori periode, bukan variabel inflasi baru |
| `lag_1` | Inflasi YoY pada satu bulan sebelumnya; digunakan sebagai fitur ramalan. | Persen; dibuat dengan shift(1) |
| `lag_12` | Inflasi YoY pada bulan yang sama setahun sebelumnya; digunakan sebagai fitur ramalan. | Persen; dibuat dengan shift(12) |

Sumber definisi: [rujukan data](https://fred.stlouisfed.org/series/IDNCPIALLMINMEI).

[Buka CSV](idn_inflasi_bulanan.csv).

Dipakai pada: [05_deret_waktu_kointegrasi](../materi/01_ekonometrika/05_deret_waktu_kointegrasi.ipynb), [05_deret_waktu_panel](../materi/02_latihan/05_deret_waktu_panel.ipynb), [06_data_indonesia](../materi/02_latihan/06_data_indonesia.ipynb), [05_deret_waktu_panel](../pengajar/kunci_jawaban/05_deret_waktu_panel.ipynb).

<a id="idn_kurs_tahunan_csv"></a>

### Kenali data: Kurs rupiah tahunan

**Data:** `data/idn_kurs_tahunan.csv`. **Satu baris:** satu tahun kalender.

| Variabel/kolom | Pengertian | Satuan atau kode | Peran |
|---|---|---|---|
| `tahun` | Tahun pengamatan. | Tahun | Penanda waktu |
| `kurs` | Kurs resmi rata-rata satu tahun, rupiah yang diperlukan untuk US$1. | Rupiah per dolar AS | Deret yang dianalisis |

Kurs yang meningkat berarti satu dolar membutuhkan lebih banyak rupiah, sehingga rupiah melemah terhadap dolar.

Kolom turunan berikut dibuat saat praktik; kolom ini belum ada pada CSV awal.

| Kolom turunan | Pengertian | Satuan/kode |
|---|---|---|
| `pertumbuhan` | Perubahan relatif kurs dari tahun sebelumnya, dikalikan 100. | Persen per tahun |

Sumber definisi: [rujukan data](https://data.worldbank.org/indicator/PA.NUS.FCRF).

[Buka CSV](idn_kurs_tahunan.csv).

Dipakai pada: [06_data_indonesia](../materi/02_latihan/06_data_indonesia.ipynb).

<a id="idn_makro_tahunan_csv"></a>

### Kenali data: Makroekonomi Indonesia tahunan

**Data:** `data/idn_makro_tahunan.csv`. **Satu baris:** satu tahun kalender untuk Indonesia.

| Variabel/kolom | Pengertian | Satuan atau kode | Peran |
|---|---|---|---|
| `negara` | Kode negara; IDN menunjukkan Indonesia. | Kode ISO negara | Penanda, bukan besaran ekonomi |
| `tahun` | Tahun kalender pengamatan. | Tahun | Penanda waktu |
| `PDB_Growth` | Laju pertumbuhan tahunan PDB riil (Produk Domestik Bruto). | Persen per tahun; NY.GDP.MKTP.KD.ZG | Target pertumbuhan pada model panel |
| `Inflasi` | Kenaikan tahunan indeks harga konsumen. | Persen per tahun; FP.CPI.TOTL.ZG | Y atau X sesuai model |
| `Pengangguran` | Pengangguran sebagai bagian dari total angkatan kerja, estimasi model ILO. | Persen angkatan kerja; SL.UEM.TOTL.ZS | X: penjelas |
| `Kurs_USD` | Kurs resmi rata-rata periode: mata uang lokal untuk memperoleh satu dolar AS. | Mata uang lokal per US$1; PA.NUS.FCRF | X: penjelas |
| `Angkatan_Kerja` | Penduduk yang bekerja atau aktif mencari pekerjaan. | Orang; SL.TLF.TOTL.IN | X: penjelas |

Kurs_USD untuk Indonesia bersatuan rupiah per US$1. Inflasi dan pertumbuhan adalah laju persen, bukan nilai level harga atau level PDB.

Sumber definisi: [rujukan data](https://databank.worldbank.org/source/world-development-indicators).

[Buka CSV](idn_makro_tahunan.csv).

Dipakai pada: [00_persiapan_colab](../materi/01_ekonometrika/00_persiapan_colab.ipynb), [00_persiapan_colab](../materi/02_latihan/00_persiapan_colab.ipynb), [06_data_indonesia](../materi/02_latihan/06_data_indonesia.ipynb), [00_persiapan_colab](../pengajar/kunci_jawaban/00_persiapan_colab.ipynb).

<a id="ihsg_emas_csv"></a>

### Kenali data: IHSG dan harga emas simulasi

**Data:** `data/ihsg_emas.csv`. **Satu baris:** satu bulan berurutan pada contoh simulasi.

| Variabel/kolom | Pengertian | Satuan atau kode | Peran |
|---|---|---|---|
| `Bulan` | Urutan bulan pengamatan. | Nomor bulan; tanggal kalender tidak dicantumkan | Penanda waktu |
| `IHSG_Y` | Indeks Harga Saham Gabungan dalam contoh simulasi. | Poin indeks | Y: target |
| `Emas_X` | Harga emas pada contoh simulasi. | Mata uang dan berat acuan tidak dirinci | X: penjelas |

Tabel ini adalah contoh simulasi; berbeda dari data IHSG harian unduhan Yahoo Finance.

Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

[Buka CSV](ihsg_emas.csv).

Dipakai pada: [05_deret_waktu_panel](../materi/02_latihan/05_deret_waktu_panel.ipynb), [05_deret_waktu_panel](../pengajar/kunci_jawaban/05_deret_waktu_panel.ipynb).

<a id="ihsg_harian_csv"></a>

### Kenali data: IHSG harian

**Data:** `data/ihsg_harian.csv`. **Satu baris:** satu hari perdagangan di pasar saham.

| Variabel/kolom | Pengertian | Satuan atau kode | Peran |
|---|---|---|---|
| `Date` | Tanggal hari perdagangan. | Tanggal YYYY-MM-DD | Penanda waktu |
| `Close` | Nilai penutupan Indeks Harga Saham Gabungan (IHSG). | Poin indeks | Deret yang dianalisis |
| `High` | Nilai indeks tertinggi pada hari tersebut. | Poin indeks | Informasi perdagangan |
| `Low` | Nilai indeks terendah pada hari tersebut. | Poin indeks | Informasi perdagangan |
| `Open` | Nilai indeks saat pembukaan hari perdagangan. | Poin indeks | Informasi perdagangan |
| `Volume` | Volume perdagangan yang dilaporkan penyedia data untuk ticker indeks. | Satuan pelaporan Yahoo; bukan rupiah atau poin indeks | Informasi perdagangan |

IHSG adalah indeks, sehingga Close = 6.000 berarti 6.000 poin, bukan Rp6.000. Return dihitung dari perubahan Close. Nilai Volume nol tidak otomatis menunjukkan tidak ada perdagangan; cakupan pelaporan mengikuti penyedia.

Kolom turunan berikut dibuat saat praktik; kolom ini belum ada pada CSV awal.

| Kolom turunan | Pengertian | Satuan/kode |
|---|---|---|
| `ret` | Return logaritmik harian: 100 × (ln Close hari ini - ln Close sebelumnya). | Persen log-return |

Sumber definisi: [rujukan data](https://finance.yahoo.com/quote/%5EJKSE/history/).

[Buka CSV](ihsg_harian.csv).

Dipakai pada: [06_data_indonesia](../materi/02_latihan/06_data_indonesia.ipynb).

<a id="ihsg_panjang_csv"></a>

### Kenali data: IHSG riwayat panjang

**Data:** `data/ihsg_panjang.csv`. **Satu baris:** satu hari perdagangan di pasar saham.

| Variabel/kolom | Pengertian | Satuan atau kode | Peran |
|---|---|---|---|
| `Date` | Tanggal hari perdagangan. | Tanggal YYYY-MM-DD | Penanda waktu |
| `Close` | Nilai penutupan Indeks Harga Saham Gabungan (IHSG). | Poin indeks | Deret yang dianalisis |
| `High` | Nilai indeks tertinggi pada hari tersebut. | Poin indeks | Informasi perdagangan |
| `Low` | Nilai indeks terendah pada hari tersebut. | Poin indeks | Informasi perdagangan |
| `Open` | Nilai indeks saat pembukaan hari perdagangan. | Poin indeks | Informasi perdagangan |
| `Volume` | Volume perdagangan yang dilaporkan penyedia data untuk ticker indeks. | Satuan pelaporan Yahoo; bukan rupiah atau poin indeks | Informasi perdagangan |

IHSG adalah indeks, sehingga Close = 6.000 berarti 6.000 poin, bukan Rp6.000. Return dihitung dari perubahan Close. Nilai Volume nol tidak otomatis menunjukkan tidak ada perdagangan; cakupan pelaporan mengikuti penyedia.

Kolom turunan berikut dibuat saat praktik; kolom ini belum ada pada CSV awal.

| Kolom turunan | Pengertian | Satuan/kode |
|---|---|---|
| `ret` | Return logaritmik harian: 100 × selisih log Close. | Persen log-return |

Sumber definisi: [rujukan data](https://finance.yahoo.com/quote/%5EJKSE/history/).

[Buka CSV](ihsg_panjang.csv).

Dipakai pada: [06_data_indonesia](../materi/02_latihan/06_data_indonesia.ipynb), [06_data_indonesia](../pengajar/kunci_jawaban/06_data_indonesia.ipynb).

<a id="jam_skor_csv"></a>

### Kenali data: Jam belajar dan hasil ujian

**Data:** `data/jam_skor.csv`. **Satu baris:** satu siswa/responden.

| Variabel/kolom | Pengertian | Satuan atau kode | Peran |
|---|---|---|---|
| `Jam_Belajar` | Total waktu belajar yang dicatat pada contoh. | Jam | X: penjelas |
| `Skor_Ujian` | Nilai/skor hasil ujian. | Poin skor; batas maksimum akan ditaksir dalam latihan | Y: target |

Kolom turunan berikut dibuat saat praktik; kolom ini belum ada pada CSV awal.

| Kolom turunan | Pengertian | Satuan/kode |
|---|---|---|
| `satu_per_jam` | Kebalikan jam belajar: 1 / Jam_Belajar. | Per jam |

Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

[Buka CSV](jam_skor.csv).

Dipakai pada: [02_bentuk_fungsional](../materi/02_latihan/02_bentuk_fungsional.ipynb), [02_bentuk_fungsional](../pengajar/kunci_jawaban/02_bentuk_fungsional.ipynb).

<a id="konsumsi_pendapatan_csv"></a>

### Kenali data: Konsumsi dan pendapatan runtun waktu

**Data:** `data/konsumsi_pendapatan.csv`. **Satu baris:** satu tahun berurutan pada data simulasi.

| Variabel/kolom | Pengertian | Satuan atau kode | Peran |
|---|---|---|---|
| `Tahun` | Nomor tahun dalam urutan simulasi, bukan tahun kalender. | 1, 2, 3, ... | Penanda waktu |
| `Konsumsi_Y` | Nilai konsumsi pada periode tersebut. | Skala uang tidak dirinci | Y: target |
| `Pendapatan_X` | Nilai pendapatan pada periode yang sama. | Skala uang tidak dirinci | X: penjelas |

Kolom turunan berikut dibuat saat praktik; kolom ini belum ada pada CSV awal.

| Kolom turunan | Pengertian | Satuan/kode |
|---|---|---|
| `ln_konsumsi` | Logaritma alami nilai konsumsi. | Skala logaritma |
| `ln_pendapatan` | Logaritma alami nilai pendapatan. | Skala logaritma |
| `d_konsumsi` | Selisih log konsumsi dari periode sebelumnya. | Perubahan log, belum dikalikan 100 |
| `d_pendapatan` | Selisih log pendapatan dari periode sebelumnya. | Perubahan log, belum dikalikan 100 |
| `ect` | Error Correction Term: penyimpangan dari hubungan jangka panjang pada periode sebelumnya. | Residual log periode sebelumnya |

Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

[Buka CSV](konsumsi_pendapatan.csv).

Dipakai pada: [05_deret_waktu_kointegrasi](../materi/01_ekonometrika/05_deret_waktu_kointegrasi.ipynb), [05_deret_waktu_panel](../materi/02_latihan/05_deret_waktu_panel.ipynb).

<a id="kredit_default_csv"></a>

### Kenali data: Gagal bayar kartu kredit Taiwan

**Data:** `data/kredit_default.csv`. **Satu baris:** satu nasabah dari subset 1.000 pengamatan data UCI Taiwan.

| Variabel/kolom | Pengertian | Satuan atau kode | Peran |
|---|---|---|---|
| `limit_kredit` | Batas kredit yang diberikan kepada nasabah. | Dolar Taiwan (NT$), bukan rupiah | X: penjelas |
| `jenis_kelamin` | Kategori jenis kelamin menurut pencatatan sumber. | 1 = laki-laki; 2 = perempuan | X: penjelas |
| `pendidikan` | Jenjang pendidikan menurut kode sumber. | 1 = pascasarjana; 2 = universitas; 3 = sekolah menengah; 4 = lainnya; kode lain tidak dirinci | X: penjelas |
| `status_nikah` | Status perkawinan menurut kode sumber. | 1 = menikah; 2 = lajang; 3 = lainnya; kode lain tidak dirinci | X: penjelas |
| `usia` | Umur nasabah. | Tahun | X: penjelas |
| `gagal_bayar` | Apakah nasabah mengalami gagal bayar pada periode target. | 1 = gagal bayar; 0 = tidak | Y: target |

Data ini berasal dari Taiwan, bukan Indonesia. Kode kategori tidak otomatis mempunyai jarak numerik yang bermakna; misalnya kode pendidikan 2 bukan dua kali pendidikan kode 1. Pengayaan keputusan kredit hanya memakai limit_kredit dan usia sebagai fitur; kolom kategori tidak diperlakukan sebagai angka berjarak. Biaya kesalahan adalah asumsi latihan dalam unit biaya.

Sumber definisi: [rujukan data](https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients).

[Buka CSV](kredit_default.csv).

Dipakai pada: [04_model_kategorikal](../materi/01_ekonometrika/04_model_kategorikal.ipynb), [04_model_kategorikal](../materi/02_latihan/04_model_kategorikal.ipynb), [04_model_kategorikal](../pengajar/kunci_jawaban/04_model_kategorikal.ipynb).

<a id="kurs_harian_csv"></a>

### Kenali data: Kurs rupiah harian

**Data:** `data/kurs_harian.csv`. **Satu baris:** satu tanggal tersedianya kurs acuan.

| Variabel/kolom | Pengertian | Satuan atau kode | Peran |
|---|---|---|---|
| `Tanggal` | Tanggal kurs acuan tersedia; bukan selalu setiap hari kalender. | Tanggal YYYY-MM-DD | Penanda waktu |
| `Kurs_USD_IDR` | Jumlah rupiah untuk memperoleh satu dolar AS (USD = dolar AS; IDR = rupiah). | Rupiah per US$1 | Deret yang dianalisis |

Seri diambil melalui Frankfurter dari kurs acuan ECB. Perubahan kurs adalah kolom turunan, bukan arti nilai kurs level.

Kolom turunan berikut dibuat saat praktik; kolom ini belum ada pada CSV awal.

| Kolom turunan | Pengertian | Satuan/kode |
|---|---|---|
| `ret_kurs` | Perubahan relatif kurs harian: 100 × (kurs hari ini / kurs sebelumnya - 1). | Persen; positif berarti rupiah melemah |

Sumber definisi: [rujukan data](https://www.frankfurter.dev/).

[Buka CSV](kurs_harian.csv).

Dipakai pada: [06_data_indonesia](../materi/02_latihan/06_data_indonesia.ipynb), [06_data_indonesia](../pengajar/kunci_jawaban/06_data_indonesia.ipynb).

<a id="latihan_dummy_1_csv"></a>

### Kenali data: Gaji dan karakteristik pekerja

**Data:** `data/latihan_dummy_1.csv`. **Satu baris:** satu pekerja pada contoh latihan.

| Variabel/kolom | Pengertian | Satuan atau kode | Peran |
|---|---|---|---|
| `No` | Nomor urut pekerja. | Nomor identitas | Penanda, bukan besaran ekonomi |
| `GAJI` | Besarnya gaji pekerja. | Uang; skala/periode gaji tidak dirinci | Y: target |
| `PENGALAMAN` | Lama pengalaman kerja pekerja. | Satuan waktu tidak dirinci sumber | X: penjelas |
| `GENDER` | Kategori gender yang dicatat dalam berkas. | Teks: Pria atau Wanita | X: penjelas |
| `STATUS` | Status perkawinan pekerja. | Teks: Menikah atau Lajang | X: penjelas |

Kategori teks diubah menjadi dummy 0/1 saat praktik; kelompok acuan dijelaskan pada bagian pembentukan dummy.

Kolom turunan berikut dibuat saat praktik; kolom ini belum ada pada CSV awal.

| Kolom turunan | Pengertian | Satuan/kode |
|---|---|---|
| `dummy_pria` | Indikator kategori Pria; kelompok selain Pria menjadi acuan. | 1 = Pria; 0 = selain Pria |
| `dummy_menikah` | Indikator status Menikah; kelompok selain Menikah menjadi acuan. | 1 = Menikah; 0 = selain Menikah |

Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

[Buka CSV](latihan_dummy_1.csv).

Dipakai pada: [03_dummy_asumsi_klasik](../materi/01_ekonometrika/03_dummy_asumsi_klasik.ipynb), [03_dummy_asumsi_klasik](../materi/02_latihan/03_dummy_asumsi_klasik.ipynb).

<a id="latihan_dummy_2_csv"></a>

### Kenali data: PDB, investasi, dan krisis

**Data:** `data/latihan_dummy_2.csv`. **Satu baris:** satu tahun pada contoh ekonomi simulasi.

| Variabel/kolom | Pengertian | Satuan atau kode | Peran |
|---|---|---|---|
| `Tahun` | Tahun kalender pengamatan. | Tahun | Penanda waktu |
| `PDB` | Indikator PDB yang menjadi target contoh. | Skala PDB tidak dirinci sumber | Y: target |
| `INVESTASI` | Besarnya investasi pada periode tersebut. | Skala investasi tidak dirinci sumber | X: penjelas |
| `SUKU_BUNGA` | Tingkat bunga pada periode tersebut. | Persen dalam konteks latihan | X: penjelas |
| `KRISIS` | Penanda apakah pengamatan termasuk periode krisis pada data. | 1 = krisis; 0 = bukan krisis | X: penjelas |

PDB pada nama kolom tidak otomatis berarti pertumbuhan PDB. Berkas tidak menyertakan metadata skala level/pertumbuhan; jangan menyamakannya dengan PDB_Growth World Bank.

Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

[Buka CSV](latihan_dummy_2.csv).

Dipakai pada: [03_dummy_asumsi_klasik](../materi/01_ekonometrika/03_dummy_asumsi_klasik.ipynb).

<a id="latihan_multikolinieritas_1_csv"></a>

### Kenali data: Harga dan ukuran rumah

**Data:** `data/latihan_multikolinieritas_1.csv`. **Satu baris:** satu rumah pada contoh latihan.

| Variabel/kolom | Pengertian | Satuan atau kode | Peran |
|---|---|---|---|
| `No` | Nomor rumah/pengamatan. | Nomor identitas | Penanda, bukan besaran ekonomi |
| `HARGA` | Harga jual rumah. | Uang; skala tidak dirinci | Y: target |
| `LUAS_BANGUNAN` | Luas fisik bangunan rumah. | Satuan luas tidak dirinci sumber | X: penjelas |
| `LUAS_TANAH` | Luas tanah tempat rumah berada. | Satuan luas tidak dirinci sumber | X: penjelas |
| `JML_KAMAR` | Jumlah kamar pada rumah. | Kamar | X: penjelas |

Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

[Buka CSV](latihan_multikolinieritas_1.csv).

Dipakai pada: [03_dummy_asumsi_klasik](../materi/01_ekonometrika/03_dummy_asumsi_klasik.ipynb), [03_dummy_asumsi_klasik](../materi/02_latihan/03_dummy_asumsi_klasik.ipynb).

<a id="latihan_multikolinieritas_2_csv"></a>

### Kenali data: Konsumsi rumah tangga

**Data:** `data/cadangan/latihan_multikolinieritas_2.csv`. **Satu baris:** satu rumah tangga pada contoh latihan.

| Variabel/kolom | Pengertian | Satuan atau kode | Peran |
|---|---|---|---|
| `No` | Nomor rumah tangga. | Nomor identitas | Penanda, bukan besaran ekonomi |
| `KONSUMSI` | Pengeluaran konsumsi rumah tangga. | Uang; skala/periode tidak dirinci | Y: target |
| `PENDAPATAN` | Pendapatan rumah tangga. | Uang; skala/periode tidak dirinci | X: penjelas |
| `KEKAYAAN` | Nilai kekayaan yang dimiliki rumah tangga. | Uang; skala tidak dirinci | X: penjelas |
| `JML_ANGGOTA` | Banyaknya anggota rumah tangga. | Orang | X: penjelas |

Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

[Buka CSV](cadangan/latihan_multikolinieritas_2.csv).

Data cadangan: bahan tambahan pengajar, belum dibaca oleh notebook saat ini.

<a id="latihan_normalitas_1_csv"></a>

### Kenali data: Harga saham dan kondisi makro

**Data:** `data/latihan_normalitas_1.csv`. **Satu baris:** satu pengamatan gabungan harga saham dan indikator makro.

| Variabel/kolom | Pengertian | Satuan atau kode | Peran |
|---|---|---|---|
| `Harga_Saham` | Harga penutupan saham pada pengamatan. | Uang per lembar; skala tidak dirinci | Y: target |
| `Tingkat_Suku_Bunga` | Tingkat bunga bank sentral. | Persen | X: penjelas |
| `Tingkat_Pengangguran` | Tingkat pengangguran nasional. | Persen | X: penjelas |
| `Pertumbuhan_PDB` | Laju pertumbuhan PDB kuartalan pada contoh sumber. | Persen | X: penjelas |

Berkas tidak memiliki tanggal; jangan mengarang tahun kalender dari nomor baris.

Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

[Buka CSV](latihan_normalitas_1.csv).

Dipakai pada: [03_dummy_asumsi_klasik](../materi/01_ekonometrika/03_dummy_asumsi_klasik.ipynb).

<a id="latihan_normalitas_2_csv"></a>

### Kenali data: Hasil panen dan kondisi lahan

**Data:** `data/cadangan/latihan_normalitas_2.csv`. **Satu baris:** satu pengamatan lahan pada musim tanam.

| Variabel/kolom | Pengertian | Satuan atau kode | Peran |
|---|---|---|---|
| `Hasil_Panen` | Hasil panen relatif terhadap luas lahan. | Ton per hektar | Y: target |
| `Curah_Hujan` | Akumulasi hujan selama musim tanam. | Milimeter (mm) | X: penjelas |
| `Pupuk` | Pupuk yang digunakan per luas lahan. | Kilogram per hektar | X: penjelas |
| `Sinar_Matahari` | Rata-rata lama penyinaran matahari harian. | Jam per hari | X: penjelas |

Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

[Buka CSV](cadangan/latihan_normalitas_2.csv).

Data cadangan: bahan tambahan pengajar, belum dibaca oleh notebook saat ini.

<a id="latihan_normalitas_3_csv"></a>

### Kenali data: Harga dan kondisi rumah

**Data:** `data/latihan_normalitas_3.csv`. **Satu baris:** satu rumah pada contoh latihan.

| Variabel/kolom | Pengertian | Satuan atau kode | Peran |
|---|---|---|---|
| `Harga` | Harga jual rumah pada data simulasi. | Sumber menyebut juta rupiah sekaligus simulasi dolar; skala ambigu | Y: target |
| `Luas_Bangunan` | Luas bangunan rumah. | Sumber menyebut m² sekaligus simulasi kaki persegi; skala ambigu | X: penjelas |
| `Jumlah_Kamar` | Jumlah kamar tidur. | Kamar | X: penjelas |
| `Usia_Rumah` | Lama sejak rumah dibangun. | Tahun | X: penjelas |

Sumber mencampurkan keterangan satuan untuk harga dan luas. Gunakan angka ini untuk latihan statistik; konfirmasi satuan sebelum memberi interpretasi nominal atau mengonversi luas.

Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

[Buka CSV](latihan_normalitas_3.csv).

Dipakai pada: [03_dummy_asumsi_klasik](../materi/02_latihan/03_dummy_asumsi_klasik.ipynb), [03_dummy_asumsi_klasik](../pengajar/kunci_jawaban/03_dummy_asumsi_klasik.ipynb).

<a id="logit_probit_1_csv"></a>

### Kenali data: Persetujuan kredit usaha

**Data:** `data/cadangan/logit_probit_1.csv`. **Satu baris:** satu pemohon kredit usaha.

| Variabel/kolom | Pengertian | Satuan atau kode | Peran |
|---|---|---|---|
| `APPROVE` | Hasil keputusan permohonan kredit. | 1 = disetujui; 0 = tidak disetujui | Y: target |
| `PENDAPATAN` | Pendapatan bulanan pemohon. | Juta rupiah per bulan | X: penjelas |
| `LAMA_USAHA` | Lama usaha telah berjalan. | Tahun | X: penjelas |
| `RASIO_UTANG` | Total utang relatif terhadap pendapatan pemohon. | Persen; 65 berarti 65% | X: penjelas |
| `JAMINAN` | Ketersediaan agunan/jaminan kredit. | 1 = memiliki jaminan; 0 = tidak | X: penjelas |

Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

[Buka CSV](cadangan/logit_probit_1.csv).

Data cadangan: bahan tambahan pengajar, belum dibaca oleh notebook saat ini.

<a id="logit_probit_2_csv"></a>

### Kenali data: Kelulusan tepat waktu

**Data:** `data/logit_probit_2.csv`. **Satu baris:** satu mahasiswa.

| Variabel/kolom | Pengertian | Satuan atau kode | Peran |
|---|---|---|---|
| `LULUS_TEPAT` | Apakah mahasiswa menyelesaikan studi tepat waktu. | 1 = tepat waktu; 0 = tidak tepat waktu | Y: target |
| `IPK_SEM2` | Indeks Prestasi Kumulatif sampai semester 2. | Poin IPK | X: penjelas |
| `SKS_LULUS_SEM2` | Beban studi yang telah diselesaikan sampai semester 2; SKS = Satuan Kredit Semester. | SKS | X: penjelas |
| `KEAKTIFAN_ORG` | Keaktifan mahasiswa dalam organisasi. | 1 = aktif; 0 = tidak aktif | X: penjelas |
| `BEASISWA` | Status penerimaan beasiswa. | 1 = penerima; 0 = bukan penerima | X: penjelas |

Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

[Buka CSV](logit_probit_2.csv).

Dipakai pada: [04_model_kategorikal](../materi/01_ekonometrika/04_model_kategorikal.ipynb), [04_model_kategorikal](../materi/02_latihan/04_model_kategorikal.ipynb), [04_model_kategorikal](../pengajar/kunci_jawaban/04_model_kategorikal.ipynb).

<a id="logit_probit_3_csv"></a>

### Kenali data: Penggunaan mobile banking

**Data:** `data/cadangan/logit_probit_3.csv`. **Satu baris:** satu nasabah.

| Variabel/kolom | Pengertian | Satuan atau kode | Peran |
|---|---|---|---|
| `PAKAI_MBANKING` | Apakah nasabah memakai layanan perbankan melalui aplikasi ponsel. | 1 = memakai; 0 = tidak | Y: target |
| `USIA` | Umur nasabah. | Tahun | X: penjelas |
| `TINGKAT_PENDIDIKAN` | Jenjang pendidikan nasabah. | 1 = SMA/sederajat; 2 = diploma; 3 = sarjana; 4 = pascasarjana | X: penjelas |
| `LITERASI_DIGITAL` | Skor kemampuan/pemahaman penggunaan teknologi digital. | Skor 1 sampai 10 | X: penjelas |
| `KEPERCAYAAN_KEAMANAN` | Skor kepercayaan pada keamanan layanan digital. | Skor 1 sampai 10 | X: penjelas |

Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

[Buka CSV](cadangan/logit_probit_3.csv).

Data cadangan: bahan tambahan pengajar, belum dibaca oleh notebook saat ini.

<a id="multi_ordinal_1_csv"></a>

### Kenali data: Kepuasan layanan bank

**Data:** `data/multi_ordinal_1.csv`. **Satu baris:** satu responden pengguna layanan bank.

| Variabel/kolom | Pengertian | Satuan atau kode | Peran |
|---|---|---|---|
| `Kepuasan` | Kategori kepuasan terhadap layanan, berurutan dari rendah ke tinggi. | 1 = sangat tidak puas; 2 = netral; 3 = puas | Y: target |
| `Kecepatan` | Lama menunggu pelayanan. Angka lebih besar berarti menunggu lebih lama. | Menit | X: penjelas |
| `Staf_Ramah` | Penilaian keramahan staf. | Skor 1 sampai 10 | X: penjelas |
| `Digital_App` | Frekuensi penggunaan aplikasi digital bank yang dibuat sebagai indikator. | 1 = sering memakai; 0 = jarang/tidak | X: penjelas |

Nama Kecepatan pada CSV berarti waktu tunggu, bukan skor kecepatan. Di contoh utama namanya diperjelas menjadi waktu_tunggu.

Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

[Buka CSV](multi_ordinal_1.csv).

Dipakai pada: [04_model_kategorikal](../materi/01_ekonometrika/04_model_kategorikal.ipynb), [04_model_kategorikal](../materi/02_latihan/04_model_kategorikal.ipynb), [04_model_kategorikal](../pengajar/kunci_jawaban/04_model_kategorikal.ipynb).

<a id="multi_ordinal_2_csv"></a>

### Kenali data: Pilihan transportasi kerja

**Data:** `data/multi_ordinal_2.csv`. **Satu baris:** satu pekerja/responden perjalanan ke kantor.

| Variabel/kolom | Pengertian | Satuan atau kode | Peran |
|---|---|---|---|
| `Transport` | Moda transportasi yang dipilih. | Kategori: Mobil, Motor, Umum; tidak berurutan | Y: target |
| `Waktu_Tempuh` | Lama perjalanan menuju tempat kerja. | Menit | X: penjelas |
| `Biaya` | Biaya transportasi yang dikeluarkan. | Ribu rupiah per hari | X: penjelas |
| `Jarak_KM` | Jarak rumah ke kantor. | Kilometer (km) | X: penjelas |

Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

[Buka CSV](multi_ordinal_2.csv).

Dipakai pada: [04_model_kategorikal](../materi/01_ekonometrika/04_model_kategorikal.ipynb).

<a id="multi_ordinal_3_csv"></a>

### Kenali data: Rating risiko kredit UMKM

**Data:** `data/cadangan/multi_ordinal_3.csv`. **Satu baris:** satu usaha mikro, kecil, atau menengah.

| Variabel/kolom | Pengertian | Satuan atau kode | Peran |
|---|---|---|---|
| `Rating` | Kategori risiko kredit; kode lebih besar berarti risiko lebih rendah. | 1 = tinggi; 2 = sedang; 3 = rendah | Y: target |
| `DER` | Debt to Equity Ratio: total utang dibagi ekuitas. | Rasio, bukan persen | X: penjelas |
| `Laba_Bersih` | Keuntungan setelah memperhitungkan beban perusahaan. | Juta rupiah | X: penjelas |
| `Lama_Usaha` | Lama usaha telah beroperasi. | Tahun | X: penjelas |

Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

[Buka CSV](cadangan/multi_ordinal_3.csv).

Data cadangan: bahan tambahan pengajar, belum dibaca oleh notebook saat ini.

<a id="panel_gdp_csv"></a>

### Kenali data: Panel PDB simulasi

**Data:** `data/panel_gdp.csv`. **Satu baris:** satu negara pada satu tahun.

| Variabel/kolom | Pengertian | Satuan atau kode | Peran |
|---|---|---|---|
| `CountryID` | Kode negara dalam panel simulasi. | Kode 1 sampai 10; bukan nama negara terverifikasi | Penanda, bukan besaran ekonomi |
| `Year` | Tahun kalender pada contoh. | Tahun | Penanda waktu |
| `GDP_Y` | Gross Domestic Product/PDB: besarnya output ekonomi. | Level PDB; skala mata uang tidak dicantumkan | Y: target |
| `FDI_X1` | Foreign Direct Investment: investasi asing langsung. | Level investasi; skala tidak dicantumkan | X: penjelas |
| `Labor_X2` | Labor force: besarnya angkatan kerja. | Skala jumlah tenaga kerja tidak dicantumkan | X: penjelas |

GDP_Y adalah level PDB simulasi; PDB_Growth pada data World Bank adalah pertumbuhan persen. FDI_X1 di sini tidak otomatis mempunyai satuan persen dari PDB.

Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

[Buka CSV](panel_gdp.csv).

Dipakai pada: [06_panel_garch](../materi/01_ekonometrika/06_panel_garch.ipynb).

<a id="panel_kesehatan_csv"></a>

### Kenali data: Panel tekanan darah

**Data:** `data/cadangan/panel_kesehatan.csv`. **Satu baris:** satu pasien pada satu bulan pemeriksaan.

| Variabel/kolom | Pengertian | Satuan atau kode | Peran |
|---|---|---|---|
| `PatientID` | Kode pasien yang diikuti dari waktu ke waktu. | Nomor identitas pasien | Penanda, bukan besaran ekonomi |
| `Month` | Urutan bulan pemeriksaan. | Bulan ke-1, ke-2, ... | Penanda waktu |
| `BP_Y` | Blood pressure: tekanan darah sistolik. | Satuan tekanan darah; konteks klinis memakai mmHg | Y: target |
| `Sport_X1` | Lama olahraga yang dilakukan per minggu. | Jam per minggu | X: penjelas |
| `Cal_X2` | Asupan energi makanan harian dibagi 1.000. | Ribuan kalori harian; 2,5 berarti 2.500 pada skala sumber | X: penjelas |

Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

[Buka CSV](cadangan/panel_kesehatan.csv).

Data cadangan: bahan tambahan pengajar, belum dibaca oleh notebook saat ini.

<a id="panel_padi_csv"></a>

### Kenali data: Panel hasil panen padi

**Data:** `data/panel_padi.csv`. **Satu baris:** satu petak sawah pada satu musim tanam.

| Variabel/kolom | Pengertian | Satuan atau kode | Peran |
|---|---|---|---|
| `FarmID` | Kode petak sawah yang diamati berulang. | Nomor identitas lahan | Penanda, bukan besaran ekonomi |
| `Season` | Urutan musim tanam. | Musim tanam ke-1, ke-2, ... | Penanda waktu |
| `Yield_Y` | Jumlah gabah yang dihasilkan oleh petak sawah. | Ton gabah; bukan otomatis ton per hektar | Y: target |
| `Fertilizer_X1` | Banyaknya pupuk yang digunakan. | Kilogram (kg) | X: penjelas |
| `Rainfall_X2` | Banyaknya curah hujan pada musim tanam. | Milimeter (mm) | X: penjelas |

Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

[Buka CSV](panel_padi.csv).

Dipakai pada: [05_deret_waktu_panel](../materi/02_latihan/05_deret_waktu_panel.ipynb).

<a id="panel_pendidikan_csv"></a>

### Kenali data: Panel hasil belajar

**Data:** `data/cadangan/panel_pendidikan.csv`. **Satu baris:** satu mahasiswa/siswa pada satu semester.

| Variabel/kolom | Pengertian | Satuan atau kode | Peran |
|---|---|---|---|
| `StudentID` | Kode peserta didik. | Nomor identitas | Penanda, bukan besaran ekonomi |
| `Semester` | Urutan semester pengamatan. | Semester | Penanda waktu |
| `Score_Y` | Skor/nilai belajar pada semester tersebut. | Poin skor | Y: target |
| `StudyTime_X1` | Lama waktu belajar. | Jam per minggu | X: penjelas |
| `Attend_X2` | Tingkat kehadiran dalam pembelajaran. | Persen kehadiran | X: penjelas |

Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

[Buka CSV](cadangan/panel_pendidikan.csv).

Data cadangan: bahan tambahan pengajar, belum dibaca oleh notebook saat ini.

<a id="panel_retail_csv"></a>

### Kenali data: Panel toko ritel

**Data:** `data/panel_retail.csv`. **Satu baris:** satu cabang toko pada satu bulan.

| Variabel/kolom | Pengertian | Satuan atau kode | Peran |
|---|---|---|---|
| `StoreID` | Kode cabang toko. | Nomor identitas toko | Penanda, bukan besaran ekonomi |
| `Month` | Urutan bulan dalam panel. | Bulan ke-1, ke-2, ... | Penanda waktu |
| `Sales_Y` | Besarnya penjualan toko pada bulan tersebut. | Satuan/skala tidak dirinci sumber | Y: target |
| `Ads_X1` | Biaya iklan cabang toko. | Satuan/skala tidak dirinci sumber | X: penjelas |
| `Discount_X2` | Proporsi potongan harga. | Pecahan; 0,10 berarti diskon 10% | X: penjelas |

Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

[Buka CSV](panel_retail.csv).

Dipakai pada: [05_deret_waktu_panel](../materi/02_latihan/05_deret_waktu_panel.ipynb), [05_deret_waktu_panel](../pengajar/kunci_jawaban/05_deret_waktu_panel.ipynb).

<a id="pendidikan_pendapatan_csv"></a>

### Kenali data: Pendidikan dan pendapatan

**Data:** `data/pendidikan_pendapatan.csv`. **Satu baris:** satu responden.

| Variabel/kolom | Pengertian | Satuan atau kode | Peran |
|---|---|---|---|
| `Tahun_Pendidikan` | Total lama pendidikan yang telah ditempuh. | Tahun | X: penjelas |
| `Pendapatan_Tahunan` | Pendapatan yang diterima selama satu tahun. | Juta rupiah per tahun | Y: target |

Kolom turunan berikut dibuat saat praktik; kolom ini belum ada pada CSV awal.

| Kolom turunan | Pengertian | Satuan/kode |
|---|---|---|
| `ln_pendapatan` | Logaritma alami dari Pendapatan_Tahunan. | Skala logaritma |

Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

[Buka CSV](pendidikan_pendapatan.csv).

Dipakai pada: [02_bentuk_fungsional](../materi/02_latihan/02_bentuk_fungsional.ipynb), [02_bentuk_fungsional](../pengajar/kunci_jawaban/02_bentuk_fungsional.ipynb).

<a id="poisson_data_1_klaim_csv"></a>

### Kenali data: Klaim asuransi mobil

**Data:** `data/poisson_data_1_klaim.csv`. **Satu baris:** satu pengemudi/pemegang polis yang diamati selama satu tahun.

| Variabel/kolom | Pengertian | Satuan atau kode | Peran |
|---|---|---|---|
| `JML_KLAIM` | Jumlah pengajuan klaim asuransi dalam setahun. | Klaim; bilangan bulat 0, 1, 2, ... | Y: target |
| `USIA` | Umur pengemudi. | Tahun | X: penjelas |
| `PENGALAMAN` | Lama pengalaman mengemudi. | Tahun | X: penjelas |
| `TIPE_MOBIL` | Jenis mobil menurut pengelompokan pada sumber. | 1 = sport; 0 = keluarga | X: penjelas |

Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

[Buka CSV](poisson_data_1_klaim.csv).

Dipakai pada: [04_model_kategorikal](../materi/02_latihan/04_model_kategorikal.ipynb), [04_model_kategorikal](../pengajar/kunci_jawaban/04_model_kategorikal.ipynb).

<a id="poisson_data_2_restoran_csv"></a>

### Kenali data: Kunjungan pelanggan restoran

**Data:** `data/poisson_data_2_restoran.csv`. **Satu baris:** satu interval pengamatan selama satu jam.

| Variabel/kolom | Pengertian | Satuan atau kode | Peran |
|---|---|---|---|
| `PELANGGAN` | Jumlah pelanggan yang datang pada jam pengamatan. | Orang per jam; bilangan bulat | Y: target |
| `JAM_SIBUK` | Apakah jam pengamatan termasuk jam makan siang/malam. | 1 = jam sibuk; 0 = jam lainnya | X: penjelas |
| `WEEKEND` | Apakah pengamatan berlangsung pada akhir pekan. | 1 = akhir pekan; 0 = hari kerja | X: penjelas |
| `JML_PROMO` | Jumlah program promosi yang sedang aktif. | Program promosi | X: penjelas |

Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

[Buka CSV](poisson_data_2_restoran.csv).

Dipakai pada: [04_model_kategorikal](../materi/01_ekonometrika/04_model_kategorikal.ipynb).

<a id="poisson_data_3_cacat_csv"></a>

### Kenali data: Cacat produksi

**Data:** `data/cadangan/poisson_data_3_cacat.csv`. **Satu baris:** satu batch/kelompok produksi.

| Variabel/kolom | Pengertian | Satuan atau kode | Peran |
|---|---|---|---|
| `CACAT` | Jumlah cacat produksi dalam batch. | Cacat per batch; bilangan bulat | Y: target |
| `KEC_MESIN` | Kecepatan putaran mesin. | RPM: putaran per menit | X: penjelas |
| `USIA_MESIN` | Umur mesin sejak mulai digunakan. | Bulan | X: penjelas |
| `SUHU` | Suhu ruangan ketika produksi dilakukan. | Derajat Celsius (°C) | X: penjelas |

Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

[Buka CSV](cadangan/poisson_data_3_cacat.csv).

Data cadangan: bahan tambahan pengajar, belum dibaca oleh notebook saat ini.

<a id="provinsi_2021_csv"></a>

### Kenali data: Indikator 34 provinsi tahun 2021

**Data:** `data/provinsi_2021.csv`. **Satu baris:** satu provinsi pada tahun 2021 dalam kompilasi sumber.

| Variabel/kolom | Pengertian | Satuan atau kode | Peran |
|---|---|---|---|
| `Provinsi` | Nama provinsi yang diamati. | Nama wilayah | Penanda, bukan besaran ekonomi |
| `PDRB_Kapita` | Produk Domestik Regional Bruto per penduduk, ukuran output ekonomi per kapita. | Skala sumber; dipakai sebagai ribu rupiah dalam tutorial | Y atau X sesuai model |
| `IPM` | Indeks Pembangunan Manusia yang merangkum dimensi kesehatan, pendidikan, dan taraf hidup. | Poin indeks, bukan persen | Y atau X sesuai model |
| `Pengangguran` | Tingkat Pengangguran Terbuka (TPT). | Persen angkatan kerja | X: penjelas |
| `Kemiskinan` | Penduduk yang berada di bawah garis kemiskinan. | Persen penduduk | Y: target |
| `AHH_Laki` | Angka Harapan Hidup laki-laki pada kompilasi sumber. | Tahun | Indikator pendamping |
| `AHH_Perempuan` | Angka Harapan Hidup perempuan pada kompilasi sumber. | Tahun | Indikator pendamping |
| `APS_7_12` | Angka Partisipasi Sekolah penduduk umur 7 sampai 12 tahun. | Persen penduduk kelompok umur tersebut | Indikator pendamping |
| `APS_13_15` | Angka Partisipasi Sekolah penduduk umur 13 sampai 15 tahun. | Persen penduduk kelompok umur tersebut | Indikator pendamping |
| `APS_16_18` | Angka Partisipasi Sekolah penduduk umur 16 sampai 18 tahun. | Persen penduduk kelompok umur tersebut | Indikator pendamping |
| `APS_19_23` | Angka Partisipasi Sekolah penduduk umur 19 sampai 23 tahun. | Persen penduduk kelompok umur tersebut | Indikator pendamping |
| `Perokok` | Persentase perokok pada kompilasi data provinsi. | Persen; cakupan umur mengikuti sumber | Indikator pendamping |

Berkas ini adalah kompilasi indikator, bukan tabel metadata lengkap BPS. Cakupan indikator dan skala PDRB perlu diperiksa pada sumber BPS sebelum dipakai untuk riset; barisnya mengikuti 34 provinsi pada tahun 2021.

Kolom turunan berikut dibuat saat praktik; kolom ini belum ada pada CSV awal.

| Kolom turunan | Pengertian | Satuan/kode |
|---|---|---|
| `ln_pdrb` | Logaritma alami PDRB_Kapita. | Skala logaritma |

Sumber definisi: [rujukan data](https://github.com/sainsdataid/dataset/blob/main/Data%2034%20Provinsi%202021.csv).

[Buka CSV](provinsi_2021.csv).

Dipakai pada: [00_persiapan_colab](../materi/01_ekonometrika/00_persiapan_colab.ipynb), [00_persiapan_colab](../materi/02_latihan/00_persiapan_colab.ipynb), [06_data_indonesia](../materi/02_latihan/06_data_indonesia.ipynb), [01_dashboard_ekonomi](../materi/04_dashboard_indonesia/01_dashboard_ekonomi.ipynb), [00_persiapan_colab](../pengajar/kunci_jawaban/00_persiapan_colab.ipynb), [06_data_indonesia](../pengajar/kunci_jawaban/06_data_indonesia.ipynb).

<a id="regresi_log_csv"></a>

### Kenali data: Produksi, tenaga kerja, dan modal

**Data:** `data/regresi_log.csv`. **Satu baris:** satu unit usaha/pengamatan dalam contoh produksi.

| Variabel/kolom | Pengertian | Satuan atau kode | Peran |
|---|---|---|---|
| `Observasi ke-` | Nomor urut pengamatan. | Nomor identitas | Penanda, bukan besaran ekonomi |
| `Tenaga Kerja (L)` | Input tenaga kerja untuk proses produksi (L = labor). | Jumlah tenaga kerja; cakupan waktu tidak dirinci | X: penjelas |
| `Modal (K)` | Input modal yang digunakan untuk menghasilkan barang (K = capital). | Satuan/skala tidak dirinci sumber | X: penjelas |
| `Produksi (Q)` | Jumlah hasil produksi (Q = quantity/output). | Jumlah output; unit produk tidak dirinci | Y: target |

Kolom turunan berikut dibuat saat praktik; kolom ini belum ada pada CSV awal.

| Kolom turunan | Pengertian | Satuan/kode |
|---|---|---|
| `lnQ` | Logaritma alami dari produksi Q. | Skala logaritma |
| `lnL` | Logaritma alami dari tenaga kerja L. | Skala logaritma |
| `lnK` | Logaritma alami dari modal K. | Skala logaritma |

Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

[Buka CSV](regresi_log.csv).

Dipakai pada: [02_bentuk_fungsional](../materi/01_ekonometrika/02_bentuk_fungsional.ipynb), [02_bentuk_fungsional](../materi/02_latihan/02_bentuk_fungsional.ipynb).

<a id="regresi_polinom_csv"></a>

### Kenali data: Iklan dan penjualan

**Data:** `data/regresi_polinom.csv`. **Satu baris:** satu tahun pengamatan pada contoh latihan.

| Variabel/kolom | Pengertian | Satuan atau kode | Peran |
|---|---|---|---|
| `Tahun ke-` | Urutan tahun pengamatan, bukan tahun kalender. | 1, 2, 3, dan seterusnya | Penanda waktu |
| `Biaya Iklan (X)` | Biaya yang dikeluarkan untuk memasang iklan. | Satuan/skala tidak dirinci sumber | X: penjelas |
| `Penjualan (Y)` | Besarnya penjualan yang ingin dijelaskan oleh biaya iklan. | Satuan/skala tidak dirinci sumber | Y: target |

Jangan menetapkan rupiah, juta rupiah, atau unit barang hanya dari besar angkanya; skala tersebut tidak dicantumkan pada sumber tabel.

Kolom turunan berikut dibuat saat praktik; kolom ini belum ada pada CSV awal.

| Kolom turunan | Pengertian | Satuan/kode |
|---|---|---|
| `iklan2` | Kuadrat biaya iklan: iklan × iklan; bukan biaya iklan baru. | Kuadrat satuan iklan |

Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

[Buka CSV](regresi_polinom.csv).

Dipakai pada: [01_regresi_dasar](../materi/01_ekonometrika/01_regresi_dasar.ipynb), [02_bentuk_fungsional](../materi/01_ekonometrika/02_bentuk_fungsional.ipynb).

<a id="regresi_reciprocal_csv"></a>

### Kenali data: Pengalaman dan waktu produksi

**Data:** `data/regresi_reciprocal.csv`. **Satu baris:** satu pengamatan pengalaman pekerja dan waktu produksinya.

| Variabel/kolom | Pengertian | Satuan atau kode | Peran |
|---|---|---|---|
| `Pengalaman (X)` | Lama/pengalaman melakukan pekerjaan produksi. | Satuan pengalaman tidak dirinci sumber | X: penjelas |
| `Waktu Produksi (Y)` | Waktu yang diperlukan untuk menyelesaikan produksi. | Satuan waktu tidak dirinci sumber | Y: target |

Kolom turunan berikut dibuat saat praktik; kolom ini belum ada pada CSV awal.

| Kolom turunan | Pengertian | Satuan/kode |
|---|---|---|
| `satu_per_x` | Kebalikan pengalaman: 1 / pengalaman. | Kebalikan satuan pengalaman |

Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

[Buka CSV](regresi_reciprocal.csv).

Dipakai pada: [02_bentuk_fungsional](../materi/01_ekonometrika/02_bentuk_fungsional.ipynb).

<a id="ritel_iklan_csv"></a>

### Kenali data: Penjualan ritel dan iklan mingguan

**Data:** `data/cadangan/ritel_iklan.csv`. **Satu baris:** satu minggu berurutan pada contoh.

| Variabel/kolom | Pengertian | Satuan atau kode | Peran |
|---|---|---|---|
| `Minggu` | Urutan minggu pengamatan. | Nomor minggu | Penanda waktu |
| `Penjualan_Y` | Besarnya penjualan ritel pada minggu tersebut. | Satuan/skala tidak dirinci sumber | Y: target |
| `Iklan_X` | Belanja iklan pada minggu tersebut. | Satuan/skala tidak dirinci sumber | X: penjelas |

Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

[Buka CSV](cadangan/ritel_iklan.csv).

Data cadangan: bahan tambahan pengajar, belum dibaca oleh notebook saat ini.

<a id="spector"></a>

### Kenali data: Efektivitas metode pengajaran Spector

**Data:** dataset bawaan statsmodels (`spector`). **Satu baris:** satu mahasiswa; total 32 mahasiswa pada data sumber.

| Variabel/kolom | Pengertian | Satuan atau kode | Peran |
|---|---|---|---|
| `GPA` | Grade Point Average: rata-rata prestasi akademik mahasiswa, sejenis IPK. | Poin rata-rata nilai | X: penjelas |
| `TUCE` | Skor tes pemahaman ekonomi mahasiswa. | Poin tes | X: penjelas |
| `PSI` | Keikutsertaan dalam Personalized System of Instruction, program/metode pengajaran yang diteliti. | 1 = mengikuti; 0 = tidak | X: penjelas |
| `GRADE` | Apakah nilai mahasiswa meningkat pada pengamatan program. | 1 = meningkat; 0 = tidak meningkat | Y: target |

GRADE bukan nilai huruf A/B/C dan 0 tidak berarti mahasiswa pasti gagal kuliah. Data ini dibaca dari statsmodels, sehingga tidak memiliki CSV terpisah di paket.

Sumber definisi: [rujukan data](https://www.statsmodels.org/stable/datasets/generated/spector.html).

Dipakai pada: [04_model_kategorikal](../materi/01_ekonometrika/04_model_kategorikal.ipynb), [04_model_kategorikal](../materi/02_latihan/04_model_kategorikal.ipynb).

<a id="tobit_data_1_rnd_csv"></a>

### Kenali data: Pengeluaran penelitian dan pengembangan

**Data:** `data/tobit_data_1_rnd.csv`. **Satu baris:** satu perusahaan.

| Variabel/kolom | Pengertian | Satuan atau kode | Peran |
|---|---|---|---|
| `RND` | Pengeluaran Research and Development (R&D), yaitu penelitian dan pengembangan. | Juta dolar AS; tersensor pada 0 | Y: target |
| `PROFIT` | Keuntungan perusahaan. | Juta dolar AS | X: penjelas |
| `ASET` | Total aset yang dimiliki perusahaan. | Miliar dolar AS | X: penjelas |
| `PATEN` | Jumlah paten pada tahun sebelumnya. | Paten | X: penjelas |

RND = 0 adalah nilai pengeluaran yang tercatat pada batas bawah, bukan nilai kosong. Satuan PROFIT dan ASET berbeda skala.

Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

[Buka CSV](tobit_data_1_rnd.csv).

Dipakai pada: [04_model_kategorikal](../materi/01_ekonometrika/04_model_kategorikal.ipynb).

<a id="tobit_data_2_jamkerja_csv"></a>

### Kenali data: Jam kerja dan keadaan keluarga

**Data:** `data/cadangan/tobit_data_2_jamkerja.csv`. **Satu baris:** satu responden dalam contoh penawaran tenaga kerja.

| Variabel/kolom | Pengertian | Satuan atau kode | Peran |
|---|---|---|---|
| `JAM_KERJA` | Waktu kerja yang tercatat; 0 bagi yang tidak bekerja. | Jam per minggu; tersensor pada 0 | Y: target |
| `PENDIDIKAN` | Lama pendidikan responden. | Tahun | X: penjelas |
| `ANAK_BALITA` | Jumlah anak berusia di bawah 5 tahun. | Anak | X: penjelas |
| `INCOME_SUAMI` | Pendapatan pasangan/suami dalam konteks contoh. | Juta rupiah per bulan | X: penjelas |

Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

[Buka CSV](cadangan/tobit_data_2_jamkerja.csv).

Data cadangan: bahan tambahan pengajar, belum dibaca oleh notebook saat ini.

<a id="tobit_data_3_asuransi_csv"></a>

### Kenali data: Pembelian premi asuransi

**Data:** `data/cadangan/tobit_data_3_asuransi.csv`. **Satu baris:** satu nasabah/responden.

| Variabel/kolom | Pengertian | Satuan atau kode | Peran |
|---|---|---|---|
| `PREMI` | Premi asuransi jiwa yang dibeli; 0 jika tidak membeli. | Juta rupiah per tahun; tersensor pada 0 | Y: target |
| `PENDAPATAN` | Pendapatan nasabah selama setahun. | Juta rupiah per tahun | X: penjelas |
| `USIA` | Umur nasabah. | Tahun | X: penjelas |
| `LITERASI_KEU` | Skor pengetahuan/pemahaman keuangan. | Skor 0 sampai 100 | X: penjelas |

Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

[Buka CSV](cadangan/tobit_data_3_asuransi.csv).

Data cadangan: bahan tambahan pengajar, belum dibaca oleh notebook saat ini.

<a id="ts_gdp_growth_csv"></a>

### Kenali data: Pertumbuhan ekonomi simulasi

**Data:** `data/ts_gdp_growth.csv`. **Satu baris:** satu urutan periode simulasi; bukan tanggal kalender.

| Variabel/kolom | Pengertian | Satuan atau kode | Peran |
|---|---|---|---|
| `obs` | Urutan waktu pengamatan. | 1, 2, 3, ...; frekuensi kalender tidak dirinci | Penanda waktu |
| `gdp_growth` | GDP growth: laju pertumbuhan Produk Domestik Bruto. | Persen dalam konteks pertumbuhan | Deret yang dianalisis |

Nomor obs tidak menunjukkan tanggal/bulan/tahun tertentu. Angka level dan perubahan persennya harus dibedakan.

Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

[Buka CSV](ts_gdp_growth.csv).

Dipakai pada: [05_deret_waktu_kointegrasi](../materi/01_ekonometrika/05_deret_waktu_kointegrasi.ipynb).

<a id="ts_inflasi_csv"></a>

### Kenali data: Deret harga/inflasi simulasi

**Data:** `data/ts_inflasi.csv`. **Satu baris:** satu urutan periode simulasi; bukan tanggal kalender.

| Variabel/kolom | Pengertian | Satuan atau kode | Peran |
|---|---|---|---|
| `obs` | Urutan waktu pengamatan. | 1, 2, 3, ...; frekuensi kalender tidak dirinci | Penanda waktu |
| `inflasi` | Deret level bertendensi naik, dicontohkan sebagai IHK pada sumber. | Level/indeks simulasi; bukan otomatis persen inflasi | Deret yang dianalisis |

Nomor obs tidak menunjukkan tanggal/bulan/tahun tertentu. Angka level dan perubahan persennya harus dibedakan.

Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

[Buka CSV](ts_inflasi.csv).

Dipakai pada: [05_deret_waktu_kointegrasi](../materi/01_ekonometrika/05_deret_waktu_kointegrasi.ipynb), [05_deret_waktu_panel](../materi/02_latihan/05_deret_waktu_panel.ipynb).

<a id="ts_kurs_csv"></a>

### Kenali data: Kurs simulasi

**Data:** `data/ts_kurs.csv`. **Satu baris:** satu urutan periode simulasi; bukan tanggal kalender.

| Variabel/kolom | Pengertian | Satuan atau kode | Peran |
|---|---|---|---|
| `obs` | Urutan waktu pengamatan. | 1, 2, 3, ...; frekuensi kalender tidak dirinci | Penanda waktu |
| `kurs` | Nilai tukar simulasi yang mengalami perubahan level di tengah periode. | Level kurs; pasangan mata uang tidak dirinci sumber tabel | Deret yang dianalisis |

Nomor obs tidak menunjukkan tanggal/bulan/tahun tertentu. Angka level dan perubahan persennya harus dibedakan.

Kolom turunan berikut dibuat saat praktik; kolom ini belum ada pada CSV awal.

| Kolom turunan | Pengertian | Satuan/kode |
|---|---|---|
| `pasca` | Indikator perubahan level mulai pengamatan ke-25 pada contoh. | 1 jika obs ≥ 25; 0 sebelumnya |

Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

[Buka CSV](ts_kurs.csv).

Dipakai pada: [05_deret_waktu_kointegrasi](../materi/01_ekonometrika/05_deret_waktu_kointegrasi.ipynb).

<a id="ts_saham_csv"></a>

### Kenali data: Harga saham simulasi

**Data:** `data/ts_saham.csv`. **Satu baris:** satu urutan periode simulasi; bukan tanggal kalender.

| Variabel/kolom | Pengertian | Satuan atau kode | Peran |
|---|---|---|---|
| `obs` | Urutan waktu pengamatan. | 1, 2, 3, ...; frekuensi kalender tidak dirinci | Penanda waktu |
| `saham` | Deret harga saham simulasi untuk uji stasioneritas dan peramalan. | Level harga; skala uang tidak dirinci | Deret yang dianalisis |

Nomor obs tidak menunjukkan tanggal/bulan/tahun tertentu. Angka level dan perubahan persennya harus dibedakan.

Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

[Buka CSV](ts_saham.csv).

Dipakai pada: [05_deret_waktu_kointegrasi](../materi/01_ekonometrika/05_deret_waktu_kointegrasi.ipynb), [05_deret_waktu_panel](../materi/02_latihan/05_deret_waktu_panel.ipynb), [05_deret_waktu_panel](../pengajar/kunci_jawaban/05_deret_waktu_panel.ipynb).

<a id="usia_unit_csv"></a>

### Kenali data: Usia dan kinerja penjual

**Data:** `data/usia_unit.csv`. **Satu baris:** satu tenaga penjual.

| Variabel/kolom | Pengertian | Satuan atau kode | Peran |
|---|---|---|---|
| `Usia` | Umur tenaga penjual. | Tahun | X: penjelas |
| `Unit_Terjual` | Jumlah penjualan bulanan pada contoh kinerja penjual. | Unit per bulan, berupa angka simulasi | Y: target |

Kolom turunan berikut dibuat saat praktik; kolom ini belum ada pada CSV awal.

| Kolom turunan | Pengertian | Satuan/kode |
|---|---|---|
| `usia2` | Kuadrat usia: usia × usia. | Tahun kuadrat |

Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

[Buka CSV](usia_unit.csv).

Dipakai pada: [02_bentuk_fungsional](../materi/01_ekonometrika/02_bentuk_fungsional.ipynb), [02_bentuk_fungsional](../materi/02_latihan/02_bentuk_fungsional.ipynb), [02_bentuk_fungsional](../pengajar/kunci_jawaban/02_bentuk_fungsional.ipynb).

<a id="uts_1_csv"></a>

### Kenali data: Pertumbuhan ekonomi

**Data:** `data/uts_1.csv`. **Satu baris:** satu negara pada contoh 50 negara berkembang.

| Variabel/kolom | Pengertian | Satuan atau kode | Peran |
|---|---|---|---|
| `Y_Pertumbuhan_Ekonomi` | Laju pertumbuhan kegiatan ekonomi/PDB. | Persen | Y: target |
| `X1_Investasi` | Besarnya investasi dibandingkan PDB. | Persen dari PDB | X: penjelas |
| `X2_Inflasi` | Laju kenaikan tingkat harga. | Persen | X: penjelas |
| `X3_Keterbukaan_Perdagangan` | Ukuran keterbukaan perdagangan relatif terhadap PDB. | Persen dari PDB | X: penjelas |

Rumus rinci ukuran keterbukaan tidak dicantumkan pada tabel sumber; jangan menganggapnya nilai ekspor saja.

Kolom turunan berikut dibuat saat praktik; kolom ini belum ada pada CSV awal.

| Kolom turunan | Pengertian | Satuan/kode |
|---|---|---|
| `ln_y` | Logaritma alami pertumbuhan ekonomi yang bernilai positif. | Skala logaritma |
| `ln_inv` | Logaritma alami tingkat investasi. | Skala logaritma |
| `ln_inflasi` | Logaritma alami tingkat inflasi yang bernilai positif. | Skala logaritma |
| `ln_terbuka` | Logaritma alami ukuran keterbukaan perdagangan. | Skala logaritma |

Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

[Buka CSV](uts_1.csv).

Dipakai pada: [02_bentuk_fungsional](../materi/02_latihan/02_bentuk_fungsional.ipynb), [02_bentuk_fungsional](../pengajar/kunci_jawaban/02_bentuk_fungsional.ipynb).

<a id="uts_2_csv"></a>

### Kenali data: Harga saham perusahaan

**Data:** `data/uts_2.csv`. **Satu baris:** satu perusahaan pada contoh latihan.

| Variabel/kolom | Pengertian | Satuan atau kode | Peran |
|---|---|---|---|
| `Y_Harga_Saham` | Harga satu lembar saham perusahaan. | Uang per lembar; skala mata uang tidak dirinci | Y: target |
| `X1_Pendapatan_per_Saham` | EPS (Earnings Per Share): laba per lembar saham; bukan total omzet perusahaan. | Uang per lembar; skala mata uang tidak dirinci | X: penjelas |
| `X2_Rasio_Utang_Ekuitas` | DER (Debt to Equity Ratio): total utang dibagi ekuitas perusahaan. | Rasio; 1,5 berarti utang 1,5 kali ekuitas (150%) | X: penjelas |
| `X3_Belanja_Iklan` | Jumlah pengeluaran perusahaan untuk iklan. | Uang; skala dan periode belanja tidak dirinci | X: penjelas |

Nama harga, eps, der, dan iklan adalah nama singkat dari kolom di atas. Contoh DER tidak dibaca sebagai 1,5 persen.

Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

[Buka CSV](uts_2.csv).

Dipakai pada: [01_regresi_dasar](../materi/01_ekonometrika/01_regresi_dasar.ipynb).

<a id="uts_3_csv"></a>

### Kenali data: Produktivitas padi

**Data:** `data/uts_3.csv`. **Satu baris:** satu wilayah pertanian pada contoh latihan.

| Variabel/kolom | Pengertian | Satuan atau kode | Peran |
|---|---|---|---|
| `Y_Produktivitas_Padi` | Hasil panen padi per luas lahan. | Produktivitas per hektar; skala massa tidak dirinci sumber | Y: target |
| `X1_Jumlah_Pupuk` | Banyaknya pupuk yang digunakan pada pertanian. | Jumlah pupuk; satuan/cakupan luas tidak dirinci | X: penjelas |
| `X2_Curah_Hujan` | Banyaknya hujan pada wilayah pertanian. | Satuan/periode tidak dirinci sumber | X: penjelas |
| `X3_Sinar_Matahari` | Lama penyinaran matahari yang diterima lahan. | Jam; periode akumulasi tidak dirinci | X: penjelas |

Sumber menyebut produktivitas per hektar, tetapi tidak merinci semua skala. Interpretasi dalam ton, kg, atau mm memerlukan konfirmasi metadata, bukan hanya dugaan dari angka.

Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

[Buka CSV](uts_3.csv).

Dipakai pada: [01_regresi_dasar](../materi/02_latihan/01_regresi_dasar.ipynb), [01_regresi_dasar](../pengajar/kunci_jawaban/01_regresi_dasar.ipynb).

<a id="uts_4_csv"></a>

### Kenali data: Angka harapan hidup

**Data:** `data/uts_4.csv`. **Satu baris:** satu negara pada contoh latihan.

| Variabel/kolom | Pengertian | Satuan atau kode | Peran |
|---|---|---|---|
| `Y_Angka_Harapan_Hidup` | Rata-rata lama hidup yang diharapkan menurut indikator pada contoh. | Tahun | Y: target |
| `X1_Pengeluaran_Kesehatan` | Pengeluaran kesehatan per penduduk (per kapita). | Uang per kapita; mata uang/periode tidak dirinci | X: penjelas |
| `X2_Tingkat_Imunisasi` | Persentase anak yang memperoleh imunisasi. | Persen; jenis imunisasi tidak dirinci | X: penjelas |
| `X3_Konsumsi_Kalori` | Rata-rata konsumsi energi makanan per hari. | Kalori harian; rincian satuan energi mengikuti sumber | X: penjelas |

Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

[Buka CSV](uts_4.csv).

Dipakai pada: [01_regresi_dasar](../materi/02_latihan/01_regresi_dasar.ipynb), [01_regresi_dasar](../pengajar/kunci_jawaban/01_regresi_dasar.ipynb).

<a id="uts_5_csv"></a>

### Kenali data: Kriminalitas kota

**Data:** `data/cadangan/uts_5.csv`. **Satu baris:** satu kota pada contoh latihan.

| Variabel/kolom | Pengertian | Satuan atau kode | Peran |
|---|---|---|---|
| `Y_Tingkat_Kriminalitas` | Tingkat kejadian kejahatan relatif terhadap jumlah penduduk. | Kejadian per 100.000 penduduk | Y: target |
| `X1_Tingkat_Pengangguran` | Proporsi angkatan kerja yang menganggur. | Persen | X: penjelas |
| `X2_Rata_rata_Pendidikan` | Rata-rata lama pendidikan penduduk. | Tahun | X: penjelas |
| `X3_Kepadatan_Penduduk` | Jumlah penduduk relatif terhadap luas wilayah. | Penduduk per satuan luas; unit luas tidak dirinci | X: penjelas |

Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

[Buka CSV](cadangan/uts_5.csv).

Data cadangan: bahan tambahan pengajar, belum dibaca oleh notebook saat ini.

<a id="uts_6_csv"></a>

### Kenali data: Penjualan produk

**Data:** `data/uts_6.csv`. **Satu baris:** satu pengamatan penjualan produk dalam contoh latihan.

| Variabel/kolom | Pengertian | Satuan atau kode | Peran |
|---|---|---|---|
| `Y_Penjualan_Unit` | Banyaknya produk yang terjual. | Unit produk dalam data simulasi | Y: target |
| `X1_Biaya_Iklan` | Biaya promosi/iklan untuk produk tersebut. | Uang; skala tidak dirinci | X: penjelas |
| `X2_Harga_Produk` | Harga jual produk milik perusahaan. | Uang per unit; skala tidak dirinci | X: penjelas |
| `X3_Harga_Kompetitor` | Harga produk pesaing yang menjadi pembanding. | Uang per unit; skala tidak dirinci | X: penjelas |

Harga produk sendiri dan harga kompetitor adalah dua variabel berbeda. Periode penjualan dan skala mata uang tidak dijelaskan pada sumber.

Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

[Buka CSV](uts_6.csv).

Dipakai pada: [01_regresi_dasar](../materi/02_latihan/01_regresi_dasar.ipynb), [01_regresi_dasar](../pengajar/kunci_jawaban/01_regresi_dasar.ipynb).

<a id="volatilitas_csv"></a>

### Kenali data: Lima deret simulasi volatilitas

**Data:** `data/volatilitas.csv`. **Satu baris:** satu periode simulasi dengan lima contoh deret yang berbeda.

| Variabel/kolom | Pengertian | Satuan atau kode | Peran |
|---|---|---|---|
| `Observation` | Nomor periode simulasi. | Urutan waktu, bukan tanggal kalender | Penanda waktu |
| `Kasus_1_Saham_Return` | Return/perubahan relatif harga saham pada kasus 1. | Pecahan desimal; 0,012 setara 1,2% | Deret yang dianalisis |
| `Kasus_2_Forex_Return` | Return nilai tukar/foreign exchange pada kasus 2. | Pecahan desimal | Deret yang dianalisis |
| `Kasus_3_Kripto_Return` | Return aset kripto pada kasus 3. | Pecahan desimal | Deret yang dianalisis |
| `Kasus_4_Inflasi_MoM` | Perubahan harga dari bulan sebelumnya (month-on-month) pada kasus 4. | Pecahan desimal; 0,002 setara 0,2% | Deret yang dianalisis |
| `Kasus_5_Minyak_Shock` | Guncangan/perubahan harga minyak pada kasus 5. | Skala simulasi; definisi rinci shock tidak dicantumkan | Deret yang dianalisis |

Return pecahan harus dikalikan 100 jika ingin dibaca dalam persen. Kelima kolom adalah kasus terpisah, bukan lima penjelas dalam satu regresi.

Sumber definisi: [rujukan data](https://paggalih.github.io/matkul/sem2025-01/ekonometrika/).

[Buka CSV](volatilitas.csv).

Dipakai pada: [06_panel_garch](../materi/01_ekonometrika/06_panel_garch.ipynb).
