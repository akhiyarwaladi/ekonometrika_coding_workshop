# Data yang dipakai setiap notebook

**Untuk dashboard, hanya `provinsi_2021.csv` yang dipakai.**

Seluruh notebook membaca CSV langsung dari GitHub dengan koneksi internet.
Peserta cukup membuka `.ipynb` dan menjalankan sel dari atas.

```python
import pandas as pd

URL_DATA = "https://raw.githubusercontent.com/akhiyarwaladi/ekonometrika_coding_workshop/main/data/"
data = pd.read_csv(URL_DATA + "provinsi_2021.csv")
```

`URL_DATA` adalah alamat folder; nama CSV menentukan tabel yang dibaca.
Nama file dalam tabel berikut sama persis dengan yang tertulis di notebook.

## Pilih notebook, lalu lihat datanya

| Notebook | Data yang dipakai |
|---|---|
| [materi/01_ekonometrika/00_persiapan_colab.ipynb](../materi/01_ekonometrika/00_persiapan_colab.ipynb) | [regresi_polinom.csv](../data/regresi_polinom.csv), [uts_4.csv](../data/uts_4.csv) |
| [materi/01_ekonometrika/01_regresi_dasar.ipynb](../materi/01_ekonometrika/01_regresi_dasar.ipynb) | [uts_2.csv](../data/uts_2.csv), [regresi_polinom.csv](../data/regresi_polinom.csv) |
| [materi/01_ekonometrika/02_bentuk_fungsional.ipynb](../materi/01_ekonometrika/02_bentuk_fungsional.ipynb) | [regresi_log.csv](../data/regresi_log.csv), [regresi_reciprocal.csv](../data/regresi_reciprocal.csv), [regresi_polinom.csv](../data/regresi_polinom.csv), [usia_unit.csv](../data/usia_unit.csv) |
| [materi/01_ekonometrika/03_dummy_asumsi_klasik.ipynb](../materi/01_ekonometrika/03_dummy_asumsi_klasik.ipynb) | [latihan_dummy_1.csv](../data/latihan_dummy_1.csv), [latihan_dummy_2.csv](../data/latihan_dummy_2.csv), [latihan_multikolinieritas_1.csv](../data/latihan_multikolinieritas_1.csv), [hetero_3.csv](../data/hetero_3.csv), [latihan_normalitas_1.csv](../data/latihan_normalitas_1.csv) |
| [materi/01_ekonometrika/04_model_kategorikal.ipynb](../materi/01_ekonometrika/04_model_kategorikal.ipynb) | Spector (bawaan statsmodels), [logit_probit_2.csv](../data/logit_probit_2.csv), [multi_ordinal_2.csv](../data/multi_ordinal_2.csv), [multi_ordinal_1.csv](../data/multi_ordinal_1.csv), [tobit_data_1_rnd.csv](../data/tobit_data_1_rnd.csv), [poisson_data_2_restoran.csv](../data/poisson_data_2_restoran.csv) |
| [materi/01_ekonometrika/05_deret_waktu_kointegrasi.ipynb](../materi/01_ekonometrika/05_deret_waktu_kointegrasi.ipynb) | [ts_inflasi.csv](../data/ts_inflasi.csv), [ts_saham.csv](../data/ts_saham.csv), [ts_gdp_growth.csv](../data/ts_gdp_growth.csv), [ts_kurs.csv](../data/ts_kurs.csv), [konsumsi_pendapatan.csv](../data/konsumsi_pendapatan.csv) |
| [materi/01_ekonometrika/06_panel_garch.ipynb](../materi/01_ekonometrika/06_panel_garch.ipynb) | [panel_gdp.csv](../data/panel_gdp.csv), [volatilitas.csv](../data/volatilitas.csv) |
| [materi/02_latihan/00_persiapan_colab.ipynb](../materi/02_latihan/00_persiapan_colab.ipynb) | [uts_2.csv](../data/uts_2.csv), [uts_4.csv](../data/uts_4.csv) |
| [materi/02_latihan/01_regresi_dasar.ipynb](../materi/02_latihan/01_regresi_dasar.ipynb) | [uts_6.csv](../data/uts_6.csv), [uts_3.csv](../data/uts_3.csv), [uts_4.csv](../data/uts_4.csv) |
| [materi/02_latihan/02_bentuk_fungsional.ipynb](../materi/02_latihan/02_bentuk_fungsional.ipynb) | [regresi_log.csv](../data/regresi_log.csv), [pendidikan_pendapatan.csv](../data/pendidikan_pendapatan.csv), [usia_unit.csv](../data/usia_unit.csv), [jam_skor.csv](../data/jam_skor.csv), [uts_1.csv](../data/uts_1.csv) |
| [materi/02_latihan/03_dummy_asumsi_klasik.ipynb](../materi/02_latihan/03_dummy_asumsi_klasik.ipynb) | [latihan_dummy_1.csv](../data/latihan_dummy_1.csv), [latihan_multikolinieritas_1.csv](../data/latihan_multikolinieritas_1.csv), [hetero_2.csv](../data/hetero_2.csv), [latihan_normalitas_3.csv](../data/latihan_normalitas_3.csv), [hetero_1.csv](../data/hetero_1.csv) |
| [materi/02_latihan/04_model_kategorikal.ipynb](../materi/02_latihan/04_model_kategorikal.ipynb) | Spector (bawaan statsmodels), [logit_probit_2.csv](../data/logit_probit_2.csv), [multi_ordinal_1.csv](../data/multi_ordinal_1.csv), [poisson_data_1_klaim.csv](../data/poisson_data_1_klaim.csv) |
| [materi/02_latihan/05_deret_waktu_panel.ipynb](../materi/02_latihan/05_deret_waktu_panel.ipynb) | [ts_inflasi.csv](../data/ts_inflasi.csv), [konsumsi_pendapatan.csv](../data/konsumsi_pendapatan.csv), [panel_padi.csv](../data/panel_padi.csv), [ts_saham.csv](../data/ts_saham.csv), [ihsg_emas.csv](../data/ihsg_emas.csv), [panel_retail.csv](../data/panel_retail.csv) |
| [materi/02_latihan/06_data_indonesia.ipynb](../materi/02_latihan/06_data_indonesia.ipynb) | [ihsg_harian.csv](../data/ihsg_harian.csv), [asean_panel.csv](../data/asean_panel.csv), [idn_makro_tahunan.csv](../data/idn_makro_tahunan.csv), [kurs_harian.csv](../data/kurs_harian.csv), [idn_inflasi_bulanan.csv](../data/idn_inflasi_bulanan.csv), [idn_kurs_tahunan.csv](../data/idn_kurs_tahunan.csv), [ihsg_panjang.csv](../data/ihsg_panjang.csv), [provinsi_2021.csv](../data/provinsi_2021.csv) |
| [materi/03_regresi_housing/01_regresi_housing.ipynb](../materi/03_regresi_housing/01_regresi_housing.ipynb) | contoh taksi (dibuat di kode), [housing.csv](../data/housing.csv) |
| [materi/04_dashboard_indonesia/01_dashboard_ekonomi.ipynb](../materi/04_dashboard_indonesia/01_dashboard_ekonomi.ipynb) | [provinsi_2021.csv](../data/provinsi_2021.csv) |
| [pengajar/kunci_jawaban/00_persiapan_colab.ipynb](../pengajar/kunci_jawaban/00_persiapan_colab.ipynb) | [uts_4.csv](../data/uts_4.csv) |
| [pengajar/kunci_jawaban/01_regresi_dasar.ipynb](../pengajar/kunci_jawaban/01_regresi_dasar.ipynb) | [uts_3.csv](../data/uts_3.csv), [uts_4.csv](../data/uts_4.csv), [uts_6.csv](../data/uts_6.csv) |
| [pengajar/kunci_jawaban/02_bentuk_fungsional.ipynb](../pengajar/kunci_jawaban/02_bentuk_fungsional.ipynb) | [pendidikan_pendapatan.csv](../data/pendidikan_pendapatan.csv), [usia_unit.csv](../data/usia_unit.csv), [jam_skor.csv](../data/jam_skor.csv), [uts_1.csv](../data/uts_1.csv) |
| [pengajar/kunci_jawaban/03_dummy_asumsi_klasik.ipynb](../pengajar/kunci_jawaban/03_dummy_asumsi_klasik.ipynb) | [hetero_2.csv](../data/hetero_2.csv), [latihan_normalitas_3.csv](../data/latihan_normalitas_3.csv), [hetero_1.csv](../data/hetero_1.csv) |
| [pengajar/kunci_jawaban/04_model_kategorikal.ipynb](../pengajar/kunci_jawaban/04_model_kategorikal.ipynb) | [logit_probit_2.csv](../data/logit_probit_2.csv), [multi_ordinal_1.csv](../data/multi_ordinal_1.csv), [poisson_data_1_klaim.csv](../data/poisson_data_1_klaim.csv) |
| [pengajar/kunci_jawaban/05_deret_waktu_panel.ipynb](../pengajar/kunci_jawaban/05_deret_waktu_panel.ipynb) | [ts_saham.csv](../data/ts_saham.csv), [ihsg_emas.csv](../data/ihsg_emas.csv), [panel_retail.csv](../data/panel_retail.csv) |
| [pengajar/kunci_jawaban/06_data_indonesia.ipynb](../pengajar/kunci_jawaban/06_data_indonesia.ipynb) | [kurs_harian.csv](../data/kurs_harian.csv), [ihsg_panjang.csv](../data/ihsg_panjang.csv), [provinsi_2021.csv](../data/provinsi_2021.csv), [asean_panel.csv](../data/asean_panel.csv) |

## Arti folder data

- `data/`: **44 CSV aktif**, digunakan oleh contoh, latihan, atau kunci jawaban di atas.
- `data/cadangan/`: **15 CSV cadangan**, belum dibaca oleh 23 notebook saat ini; bahan tambahan bagi pengajar.
- `laporan/peta_perubahan_nama.csv`: catatan pengelolaan nama berkas, bukan data untuk pemodelan.

[Daftar CSV aktif](../data/README.md) · [Daftar cadangan](../data/cadangan/README.md) · [Definisi variabel](07_kamus_variabel.md)

## Salinan offline opsional

[data_tutorial.zip](../paket/data_tutorial.zip) ada di **`paket/data_tutorial.zip`**.
Isinya 44 CSV aktif dan satu modul pendukung. ZIP ini merupakan salinan untuk pengajar;
alur notebook peserta menggunakan alamat GitHub di atas.
