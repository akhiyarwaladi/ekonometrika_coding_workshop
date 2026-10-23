# Referensi dan Bahan Belajar Lanjutan

## Dokumentasi untuk contoh kode yang disederhanakan

- [Regresi dan OLS scikit-learn](https://scikit-learn.org/1.6/modules/generated/sklearn.linear_model.LinearRegression.html):
  estimator utama regresi linear, dengan pola X, y, fit, predict.
- [Logit dan multinomial scikit-learn](https://scikit-learn.org/1.6/modules/generated/sklearn.linear_model.LogisticRegression.html):
  `predict_proba()` menghitung peluang; urutan kolom mengikuti `classes_`.
- [Poisson scikit-learn](https://scikit-learn.org/1.6/modules/generated/sklearn.linear_model.PoissonRegressor.html):
  `alpha=0` untuk contoh tanpa penalti.
- [Contoh regresi ordinal statsmodels](https://www.statsmodels.org/stable/examples/notebooks/generated/ordinal_regression.html):
  parameter ambang di summary perlu ditransformasi untuk memperoleh batas asli.
- [Efek marjinal statsmodels](https://www.statsmodels.org/stable/generated/statsmodels.discrete.discrete_model.DiscreteResults.get_margeff.html):
  `at="overall"` menghitung rata-rata efek; `dummy=True` menangani perubahan 0 ke 1.
- [Hausman pada linearmodels 7.1](https://bashtage.github.io/linearmodels/panel/panel/linearmodels.panel.results.RandomEffectsResults.hausman.html):
  uji klasik memakai kovarians unadjusted. Workshop menetapkan `sigmamore=True`
  agar kedua kovarians memakai estimasi varians galat REM yang sama.

## Rujukan pendalaman

Kumpulan sumber yang bisa dipakai untuk memperdalam workshop ini. Setiap
entri punya catatan singkat: berguna untuk apa dan menutup sesi yang mana.

## Buku dan kursus yang mengikuti alur kuliah

**Gujarati, Econometrics by Example (2nd edition).**
Buku ini yang paling dekat dengan RPS mata kuliah: urutan babnya hampir
sama (bab diagnostik regresi, logit dan probit, multinomial, ordinal,
data terbatas, count data, deret waktu, kointegrasi, ARCH/GARCH, panel,
survival analysis). Kalau ingin versi cetak untuk perbandingan EViews,
ini rujukan utamanya. Contoh dan datanya bisa dibandingkan langsung
dengan notebook Sesi 3 sampai 6.

**Heiss dan Brunner, Using Python for Introductory Econometrics (edisi
2024, gratis).**
PDF lengkap: https://www.urfie.net/downloads/PDF/UPfIE_web.pdf
Buku ini menerjemahkan Wooldridge, Introductory Econometrics ke Python
bab per bab. Cocok untuk dosen yang ingin memperdalam dasar teoretis yang
di workshop ini sengaja dipadatkan. Bagus untuk Sesi 1 dan 2.

**Kevin Sheppard, Python for Econometrics (catatan kuliah, gratis).**
PDF: https://bashtage.github.io/kevinsheppard.com/files/teaching/python/notes/python_introduction_2020.pdf
Penulis yang sama dengan paket `linearmodels`. Isinya lebih teknis:
struktur data, optimisasi, hingga contoh ekonometrika keuangan. Bagus
untuk Sesi 5 dan 6, dan untuk siapa pun yang ingin memahami isi paket
`linearmodels` lebih dalam.

**metricsAI: Econometrics with Python and AI.**
https://quarcs-lab.github.io/metricsai/
Buku pendamping Cameron (2022) dengan notebook Colab untuk 17 bab. Unik
karena memakai `pyfixest` (port dari paket fixest di R) untuk estimasi
dan pelaporan. Berguna kalau ingin membandingkan gaya statsmodels dengan
gaya fixest untuk model efek tetap dan standard error klaster. Untuk
Sesi 3 dan 6.

**QuantEcon, Linear Regression in Python.**
https://python.quantecon.org/ols.html
Catatan yang sangat rapi dari Sargent dan Stachurski. Contohnya memakai
data Acemoglu dan memasukkan instrumental variables dengan `linearmodels`.
Berguna sebagai bacaan lanjutan setelah Sesi 1, terutama untuk IV/2SLS
yang belum masuk workshop.

**Python for Econometrics (Universitas Göttingen).**
https://pyecon.org/down/pyecon.pdf
Catatan kuliah yang menekankan alur kerja Jupyter dan latihan bertingkat.
Bisa dijadikan sumber soal tambahan untuk mahasiswa yang ingin berlatih
lebih banyak.

**Computational Methods for Economists using Python (Richard W. Evans).**
https://opensourceecon.github.io/CompMethods
Jupyter Book gratis tentang metode komputasi ekonomi: optimisasi,
dinamika, dan simulasi. Berguna setelah workshop untuk membuka jalan ke
model struktural dan komputasi.

## Kausalitas dan topik lanjutan

**Causal Inference for the Brave and True (Matheus Facure).**
https://matheusfacure.github.io/python-causality-handbook/landing-page.html
Buku daring gratis yang membahas causal inference dengan Python:
potential outcomes, diff-in-diff, instrumental variables, propensity
score, hingga double machine learning. Cocok disebut sebagai "bab
berikutnya" setelah mahasiswa paham bahwa koefisien OLS bukan otomatis
kausal.

## Dokumentasi pustaka

| Pustaka | Tautan | Catatan |
|---|---|---|
| statsmodels | https://www.statsmodels.org | Inferensi, diagnostik, dan model khusus |
| linearmodels | https://bashtage.github.io/linearmodels/ | Panel, IV, sistem persamaan |
| arch | https://arch.readthedocs.io | ARCH/GARCH, uji efek ARCH |
| scikit-learn | https://scikit-learn.org | Pemodelan utama, koefisien, prediksi, dan evaluasi |
| yfinance | https://github.com/ranaroussi/yfinance | Data pasar termasuk IHSG (^JKSE) |
| STADATA | https://github.com/bps-statistics/stadata | Pembungkus Python untuk WebAPI BPS |

## Sumber data Indonesia

**1. World Bank Open Data (dipakai di Lab 6).**
API tanpa kunci: `https://api.worldbank.org/v2/country/IDN/indicator/<kode>?format=json`
Script `alat_bantu/unduh_data_indonesia.py` memakai jalur ini untuk data
makro Indonesia tahunan dan panel ASEAN. Cocok untuk data lintas negara
dan deret waktu panjang.

**2. BPS WebAPI (untuk data resmi Indonesia yang lebih baru).**
Dokumentasi: https://webapi.bps.go.id/documentation/
Perlu kunci gratis dari portal developer BPS. Paket `stadata`
menyederhanakan pemakaiannya:

```python
# %pip install stadata -q
import stadata

client = stadata.Client("ISI_TOKEN_BPS")
# Contoh: lihat daftar tabel dinamis untuk domain nasional
client.list_dynamic_table(domain="0000")
```

Berguna untuk data bulanan (inflasi, ekspor impor, kunjungan wisata) yang
tidak tersedia di World Bank. Catatan jujur: kunci API tidak bisa
dibagikan di repositori, jadi setiap pengguna mendaftar sendiri.

**3. Yahoo Finance via yfinance (dipakai di Lab 6).**
IHSG harian tersedia dengan kode `^JKSE`. Saham individual Indonesia
memakai kode `KODE.JK`, misalnya `BBCA.JK`. Cocok untuk GARCH, event
study sederhana, dan analisis return.

**4. Frankfurter (kurs ECB, dipakai di Lab 6).**
API tanpa kunci: `https://api.frankfurter.app/2019-01-01..2026-09-30?from=USD&to=IDR`
Kurs referensi harian USD/IDR. Untuk kurs resmi BI (JISDOR), belum ada
API gratis; unduh manual dari situs BI.

**5. FRED (OECD Main Economic Indicators), untuk inflasi bulanan.**
CSV tanpa kunci:
`https://fred.stlouisfed.org/graph/fredgraph.csv?id=IDNCPIALLMINMEI`
Indeks harga konsumen bulanan Indonesia sejak 1968, dipakai di Lab 6
bagian krisis. Nilainya sudah dicek: inflasi tahunan 1998 sekitar 58
persen, sesuai angka BPS. Cocok untuk analisis rezim inflasi dan patahan
struktural.

**6. Data provinsi dan mikro.**
- Data 34 provinsi 2021 (dipakai di Lab 6): kompilasi indikator BPS di
  https://github.com/sainsdataid/dataset. Nilai sudah dicek terhadap
  angka BPS, misalnya PDRB per kapita DKI Jakarta 274,7 juta.
- Alternatif dengan DOI dan lisensi CC-BY: Zenodo record 20372479, data
  38 provinsi 2024 di https://zenodo.org/records/20372479.
- Data kredit default (1.000 baris, bahan latihan logit di
  `data/kredit_default.csv`): UCI Machine Learning Repository,
  https://archive.ics.uci.edu/dataset/350. Data asli kartu kredit
  Taiwan 2005, bukan Indonesia, tapi berguna karena tidak ada masalah
  perfect separation seperti data simulasi kuliah.
- Untuk mikrodata resmi (Susenas, Sakernas), ajukan lewat
  https://silastik.bps.go.id.

**7. Portal lain untuk eksplorasi.**
- data.go.id: portal data terbuka pemerintah, banyak tabel per daerah.
- bps.go.id: publikasi dan tabel statis yang bisa diunduh manual.
- bi.go.id: BI Rate, JISDOR, uang beredar (unduh manual).
- ojk.go.id: statistik perbankan dan industri keuangan (unduh manual).

## Bagaimana sumber ini meningkatkan tutorial

- Sesi 1 dan 2: buku UPfIE memberi turunan rumus dan latihan tambahan
  yang tidak muat di workshop.
- Sesi 3: metricsAI dan Gujarati memberi contoh diagnostik dengan data
  nyata dari buku teks.
- Sesi 4: Gujarati membahas kasus kategorikal dengan konteks ekonomi yang
  lebih lengkap.
- Sesi 5 dan 6: dokumentasi arch dan linearmodels menjawab pertanyaan
  teknis lanjutan (orde GARCH, efek tetap dua arah, klaster).
- Lab 6: data asli Indonesia sudah terpasang (IHSG sejak 1990, inflasi
  bulanan sejak 1968, kurs tahunan sejak 1967, panel ASEAN, dan 34
  provinsi), dan jalur BPS membuka pintu ke data mikro dan bulanan untuk
  proyek mini atau skripsi.
- Proyek mini: semua sumber data di atas bisa dipakai. Untuk survei
  sendiri, alur Google Form ke Colab tetap yang paling cepat.
