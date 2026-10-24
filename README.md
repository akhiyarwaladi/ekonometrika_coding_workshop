# Workshop ekonometrika Python

Materi untuk peserta yang belum pernah coding. Semua kegiatan belajar memakai notebook `.ipynb`.
Pelatihan FEB Universitas Jambi, 26 Oktober 2026.

## Mulai dari sini

1. Klik notebook pada tabel **Pilih materi** di bawah, lalu simpan salinan ke Google Drive.
2. Jalankan sel dari atas dengan **Shift + Enter** dan koneksi internet.
3. Baca tabel **Kenali data**, amati grafik, lalu jelaskan arti hasil dengan kata sendiri.

**CSV dan ZIP tidak perlu diunggah.** Jika memakai file dari komputer, cukup unggah satu `.ipynb`.
Notebook berisi seluruh kode dan hasil. Sel latihan yang masih berupa komentar dikerjakan setelah contoh terbimbing.

[Dasar notebook](#dasar-notebook) · [Istilah](#istilah) · [Data dan arti variabel](data/README.md) · [Panduan pengajar](pengajar/README.md)

<a id="pilih-materi"></a>
## Pilih materi

Ikuti contoh, lalu latihan dengan nomor yang sama. Semua tautan notebook membuka Google Colab.

| Urutan | Topik | Contoh | Latihan |
|---|---|---|---|
| 00 | Persiapan dan grafik pertama | [00_persiapan_colab](https://colab.research.google.com/github/akhiyarwaladi/ekonometrika_coding_workshop/blob/main/materi/01_ekonometrika/00_persiapan_colab.ipynb) | [00_persiapan_colab](https://colab.research.google.com/github/akhiyarwaladi/ekonometrika_coding_workshop/blob/main/materi/02_latihan/00_persiapan_colab.ipynb) |
| 01 | Regresi dasar dan prediksi | [01_regresi_dasar](https://colab.research.google.com/github/akhiyarwaladi/ekonometrika_coding_workshop/blob/main/materi/01_ekonometrika/01_regresi_dasar.ipynb) | [01_regresi_dasar](https://colab.research.google.com/github/akhiyarwaladi/ekonometrika_coding_workshop/blob/main/materi/02_latihan/01_regresi_dasar.ipynb) |
| 02 | Bentuk fungsional | [02_bentuk_fungsional](https://colab.research.google.com/github/akhiyarwaladi/ekonometrika_coding_workshop/blob/main/materi/01_ekonometrika/02_bentuk_fungsional.ipynb) | [02_bentuk_fungsional](https://colab.research.google.com/github/akhiyarwaladi/ekonometrika_coding_workshop/blob/main/materi/02_latihan/02_bentuk_fungsional.ipynb) |
| 03 | Dummy dan asumsi klasik | [03_dummy_asumsi_klasik](https://colab.research.google.com/github/akhiyarwaladi/ekonometrika_coding_workshop/blob/main/materi/01_ekonometrika/03_dummy_asumsi_klasik.ipynb) | [03_dummy_asumsi_klasik](https://colab.research.google.com/github/akhiyarwaladi/ekonometrika_coding_workshop/blob/main/materi/02_latihan/03_dummy_asumsi_klasik.ipynb) |
| 04 | Model kategorikal | [04_model_kategorikal](https://colab.research.google.com/github/akhiyarwaladi/ekonometrika_coding_workshop/blob/main/materi/01_ekonometrika/04_model_kategorikal.ipynb) | [04_model_kategorikal](https://colab.research.google.com/github/akhiyarwaladi/ekonometrika_coding_workshop/blob/main/materi/02_latihan/04_model_kategorikal.ipynb) |
| 05 | Deret waktu dan panel | [05_deret_waktu_kointegrasi](https://colab.research.google.com/github/akhiyarwaladi/ekonometrika_coding_workshop/blob/main/materi/01_ekonometrika/05_deret_waktu_kointegrasi.ipynb) | [05_deret_waktu_panel](https://colab.research.google.com/github/akhiyarwaladi/ekonometrika_coding_workshop/blob/main/materi/02_latihan/05_deret_waktu_panel.ipynb) |
| 06 | Panel, GARCH, dan data Indonesia | [06_panel_garch](https://colab.research.google.com/github/akhiyarwaladi/ekonometrika_coding_workshop/blob/main/materi/01_ekonometrika/06_panel_garch.ipynb) | [06_data_indonesia](https://colab.research.google.com/github/akhiyarwaladi/ekonometrika_coding_workshop/blob/main/materi/02_latihan/06_data_indonesia.ipynb) |

| Praktik tambahan | Notebook |
|---|---|
| Regresi sesuai slide | [01_regresi_housing.ipynb](https://colab.research.google.com/github/akhiyarwaladi/ekonometrika_coding_workshop/blob/main/materi/03_regresi_housing/01_regresi_housing.ipynb) |
| Penutup: dashboard ekonomi | [01_dashboard_ekonomi.ipynb](https://colab.research.google.com/github/akhiyarwaladi/ekonometrika_coding_workshop/blob/main/materi/04_dashboard_indonesia/01_dashboard_ekonomi.ipynb) |

[Tugas proyek mini](materi/02_latihan/07_proyek_mini.md) dikerjakan setelah latihan.

### Dashboard dan ngrok

Gunakan satu file: `01_dashboard_ekonomi.ipynb`. Langkah 8 adalah pratinjau, langkah 9 menyediakan ngrok, langkah 10 menghentikannya.
Untuk ngrok, ubah `gunakan_ngrok` menjadi `True`, lalu jalankan langkah 9.
Token pengajar sudah diisi langsung pada sel tersebut; tidak ada permintaan input token. CSV tetap dibaca dari GitHub.

## Letak berkas

| Folder | Isi |
|---|---|
| `materi/` | 16 notebook peserta dan tugas proyek mini. |
| `data/` | 44 CSV aktif, 15 cadangan, dan satu katalog arti variabel. |
| `slide/` | Presentasi, PDF, dan 31 PNG tajam 6000 × 3375 piksel. |
| `pengajar/` | Satu panduan mengajar dan tujuh notebook kunci jawaban. |
| `alat_bantu/` | Perkakas pengelola, hasil pemeriksaan, paket opsional, serta cadangan lokal. |

**Notebook adalah sumber utama.** Grafik dibuat dan ditampilkan langsung di dalamnya; peserta tidak perlu mencari salinan script atau gambar di folder lain.

<a id="dasar-notebook"></a>
## Dasar notebook untuk pemula

### Perintah yang sering muncul

Sebelum menjalankan sel pembacaan data, baca tabel **Kenali data**.
Contohnya, `eps` berarti laba per lembar saham dan `der` adalah rasio utang
terhadap ekuitas. Pada data pendidikan, `GPA` adalah rata-rata nilai mahasiswa,
sedangkan `GRADE` berkode 1 jika nilai meningkat dan 0 jika tidak meningkat.
Definisi lengkap ada di [kamus variabel](data/README.md#definisi-variabel).

| Contoh | Cara membacanya |
|---|---|
| `import pandas as pd` | Siapkan alat untuk mengolah tabel; nama singkatnya `pd`. |
| `saham = pd.read_csv(URL_DATA + "uts_2.csv")` | Baca berkas dan simpan tabel dengan nama `saham`. |
| `saham.head()` | Tampilkan lima baris pertama tabel. |
| `saham["Y_Harga_Saham"]` | Pilih kolom harga saham. Nama kolom harus persis sama. |
| `model = LinearRegression()` | Siapkan model regresi linear. |
| `model.fit(X, y)` | Pelajari koefisien dari tabel fitur X dan kolom target y. |
| `model.predict(X_baru)` | Hitung prediksi untuk tabel fitur baru. |

`saham` dan `model` adalah nama tempat menyimpan hasil, disebut variabel.
Ini berbeda dari variabel ekonomi, misalnya harga saham dan pendapatan.
Nama dengan huruf besar dan kecil dianggap berbeda oleh Python.

### Simbol yang perlu dikenal saat bertemu

| Simbol | Contoh | Arti |
|---|---|---|
| `#` | `# Baca data` | Catatan untuk manusia, tidak dihitung. |
| `=` | `batas = 0.05` | Simpan nilai ke sebuah nama. |
| `==` | `gaji["gender"] == "Pria"` | Bandingkan apakah nilainya sama. |
| `"..."` | `"harga"` | Teks, misalnya nama kolom atau rumus. |
| `[]` | `[15, 20, 25]` | Daftar nilai; juga dipakai memilih kolom/baris. |
| `()` | `print(...)` | Tempat mengisi masukan sebuah perintah. |
| `.` | `saham.head()` | Jalankan fasilitas milik tabel/hasil tersebut. |
| `**` | `usia ** 2` | Pangkat, misalnya usia kuadrat. |
| `~` dalam rumus | `"harga ~ eps + iklan"` | Harga dijelaskan oleh EPS dan iklan. |

Pada scikit-learn, pilih variabel penjelas sebagai daftar kolom X.
`LinearRegression()` menyertakan intersep secara otomatis. Notasi `y ~ x`
masih dipakai dalam uraian persamaan dan beberapa model khusus.
Angka desimal di kode memakai titik: ketik `1.5`, bukan `1,5`.

### Contoh lengkap: baca, hitung, lihat

Jalankan sel berikut secara berurutan setelah sel persiapan data.

```python
import pandas as pd
from sklearn.linear_model import LinearRegression

URL_DATA = "https://raw.githubusercontent.com/akhiyarwaladi/ekonometrika_coding_workshop/main/data/"
saham = pd.read_csv(URL_DATA + "uts_2.csv")
saham.head()
```

Tabel harus memuat kolom `Y_Harga_Saham` dan `X1_Pendapatan_per_Saham`.
Satu baris tabel mewakili satu perusahaan pada contoh ini.

```python
X = saham[["X1_Pendapatan_per_Saham"]]
y = saham["Y_Harga_Saham"]
model = LinearRegression()
model.fit(X, y)
print("Intersep:", model.intercept_)
print("Koefisien EPS:", model.coef_[0])
print("R kuadrat pada data latih:", model.score(X, y))
```

`coef_[0]` adalah koefisien fitur pertama, yaitu EPS. Angka ini menunjukkan
perubahan prediksi harga untuk tambahan satu unit EPS. `intercept_` adalah
intersep. Koefisien belum menunjukkan sebab akibat. R² pada data latih
merangkum kecocokan; evaluasi prediksi memakai data uji yang terpisah.

P-value dan standard error dibahas pada bagian pelengkap statistik di notebook.
Nama `uji_...` menandai bagian ini, dengan X dan y yang sama seperti model utama.

```python
# Nilai di dalam [] adalah nilai EPS baru yang ingin diprediksi.
perusahaan_baru = pd.DataFrame({"X1_Pendapatan_per_Saham": [25]})
prediksi = model.predict(perusahaan_baru)
print(prediksi)
```

Hasilnya sekitar 348,1 dalam satuan harga pada data. Untuk latihan pertama,
ganti **hanya** angka `25` menjadi `20`, jalankan ulang sel prediksi, lalu
jelaskan mengapa hasilnya berubah.

`pd.DataFrame(...)` membuat tabel baru. Tanda `{}` memasangkan nama kolom
dengan daftar nilainya. Pada tahap ini cukup ikuti bentuk contoh tersebut.

### Perintah tambahan diperkenalkan saat diperlukan

| Perintah | Dipakai untuk | Muncul pada |
|---|---|---|
| `.rename(columns={...})` | Memberi nama kolom yang lebih pendek. | Sesi 1 |
| `np.log(...)` | Menghitung logaritma alami. Masukannya harus positif. | Sesi 2 |
| `.astype(int)` | Mengubah hasil perbandingan menjadi dummy 0/1. | Sesi 3 |
| `.values` dan `[1]` | Mengambil angka tabel atau hasil uji pada posisi tertentu. Posisi dimulai dari 0. | Sesi 3 |
| `.loc[kondisi, "kolom"]` | Memilih baris sesuai kondisi dan satu kolom. | Lab 6 |
| `.diff()` | Menghitung selisih dengan periode sebelumnya. | Sesi 5 |
| `.shift(1)` | Menggeser data satu periode untuk membuat lag. | Sesi 5 |
| `.dropna()` | Menghapus baris yang mempunyai nilai kosong pada kolom yang diperiksa. | Sesi 5 |
| `.set_index([...])` | Menandai unit dan waktu pada data panel. | Sesi 6 |
| `f"{nilai:.3f}"` | Menampilkan angka dengan tiga angka desimal. Tidak mengubah hasil estimasi. | Sesi 1 |

Tidak perlu menghafal tabel ini sebelum mulai. Buka kembali ketika
perintahnya muncul. Sel gaya grafik, instalasi paket, dan persiapan alamat data
cukup dijalankan sebagaimana disediakan.

### Jika hasil belum muncul

| Pesan/keadaan | Langkah yang dilakukan |
|---|---|
| Pembacaan CSV gagal | Periksa koneksi internet dan ejaan nama CSV. Jalankan kembali sel alamat data. |
| `NameError` | Nama belum dibuat atau salah ketik. Jalankan sel sebelumnya dari atas. |
| `KeyError` | Nama kolom berbeda. Tampilkan `print(saham.columns)` dan cocokkan ejaannya. |
| `SyntaxError` | Periksa tanda kutip, kurung, dan koma di sel yang diubah. |
| `ModuleNotFoundError` | Jalankan sel instalasi yang tersedia dan tunggu sampai selesai. |
| Warning konvergensi/separation | Baca catatan metode pada notebook; koefisien/p-value bisa tidak layak ditafsirkan. |
| Runtime dimulai ulang | Jalankan notebook kembali dari sel pertama. |

Jika memakai AI untuk membantu, contoh permintaannya ada di `pengajar/README.md`.
Sertakan pesan error dan sel terkait agar bantuan sesuai masalahnya.

<a id="istilah"></a>
## Istilah yang ditemui selama praktik

Istilah yang muncul di workshop, diurutkan sesuai kemunculannya. Setiap
entri menyebut tempat istilah itu diperkenalkan, supaya mudah dilacak.

### Dasar regresi (Sesi 1, Lab 0-1)

**Regresi linear**  
Cara mencari garis (atau bidang) yang paling dekat dengan data, dengan
jarak diukur sebagai kuadrat residual. Diperkenalkan di Sesi 1.

**OLS (Ordinary Least Squares)**  
Metode penaksiran regresi yang meminimalkan jumlah kuadrat residual.
Sinonim praktis dari "regresi linear" di workshop ini. Sesi 1.

**Residual**  
Selisih antara nilai aktual dan nilai prediksi model. Garis abu-abu di
gambar Sesi 1 adalah residualnya. Sesi 1.

**Koefisien**  
Angka yang menunjukkan besar hubungan satu variabel penjelas dengan Y,
dengan variabel lain dianggap tetap. Sesi 1.

**Intersep**  
Nilai Y saat semua X bernilai nol. Tidak selalu masuk akal secara
ekonomi, tapi tetap dilaporkan. Sesi 1.

**Ceteris paribus**  
"Asumsi variabel lain tidak berubah". Makna yang menempel pada setiap
koefisien regresi berganda. Sesi 1.

**R kuadrat (R2)**  
Proporsi variasi Y yang diterangkan model. Bukan bukti model benar atau
hubungan kausal. Sesi 1.

**R kuadrat terkoreksi (adjusted R2)**  
R kuadrat yang menghukum penambahan variabel yang tidak berguna. Dipakai
membandingkan model dengan jumlah variabel berbeda. Sesi 1.

**Uji t**  
Uji signifikansi satu koefisien: apakah berbeda dari nol. Sesi 1.

**Uji F**  
Uji signifikansi model secara keseluruhan. Sesi 1.

**p-value**  
Peluang mengamati hasil seekstrem ini kalau pengaruh sebenarnya nol. Di
bawah 0,05 lazim disebut signifikan. Sesi 1.

**Standard error (galat baku)**  
Ukuran ketidakpastian koefisien. Muncul di tabel output dan di rumus
robust/HAC. Sesi 1.

**Prediksi**  
Nilai Y yang dihitung untuk nilai X baru memakai model yang sudah
ditaksir. Sesi 1.

### Bentuk fungsional (Sesi 2, Lab 2)

**Elastisitas**  
Persentase perubahan Y untuk kenaikan X satu persen. Koefisien model
log-log. Sesi 2.

**Model log-log**  
Semua variabel di-log, koefisiennya elastisitas. Contoh: fungsi produksi
Cobb-Douglas. Sesi 2.

**Model lin-log dan log-lin**  
Campuran log dan linear. Log-lin dipakai untuk efek persentase (misalnya
pendidikan terhadap pendapatan). Sesi 2.

**Model reciprocal**  
Memakai 1/X sehingga efek mengecil dan mendekati batas (asimtot) saat X
membesar. Sesi 2.

**Model polinomial**  
Memakai X dan X kuadrat (kadang kubik) sehingga kurva bisa naik lalu
turun. Titik puncaknya dihitung dari koefisien. Sesi 2.

### Diagnostik (Sesi 3, Lab 3)

**Multikolinearitas**  
Korelasi tinggi antar variabel penjelas. Koefisien jadi tidak stabil
walaupun model secara keseluruhan terlihat bagus. Sesi 3.

**VIF (Variance Inflation Factor)**  
Ukuran multikolinearitas. Di atas 10 menandakan masalah serius. Sesi 3.

**Heteroskedastisitas**  
Varians residual tidak konstan. Standard error OLS jadi salah, uji t dan
F tidak valid. Sesi 3.

**Uji Breusch-Pagan dan White**  
Dua uji formal untuk heteroskedastisitas. Sesi 3.

**Robust standard error (HC3)**  
Standard error yang tahan terhadap heteroskedastisitas. Koefisien tidak
berubah, hanya ketidakpastiannya. Sesi 3.

**Autokorelasi**  
Residual berkorelasi dengan residual periode sebelumnya, khas data
deret waktu. Sesi 3.

**Durbin-Watson dan Breusch-Godfrey**  
Uji autokorelasi. DW cepat, BG lebih fleksibel. Sesi 3.

**HAC (Newey-West)**  
Standard error yang tahan terhadap autokorelasi. Sesi 3.

**Normalitas residual**  
Asumsi bahwa error berdistribusi normal, penting untuk inferensi pada
sampel kecil. Sesi 3.

**Jarque-Bera**  
Uji normalitas berbasis skewness dan kurtosis. Sesi 3.

### Variabel kategorikal (Sesi 4, Lab 4)

**Variabel dummy**  
Variabel 0/1 untuk kategori. Selalu buang satu kategori sebagai basis. Sesi 3.

**Logit dan probit**  
Model untuk Y 0/1. Logit memakai fungsi logistik, probit memakai
distribusi normal. Sesi 4.

**Odds ratio**  
exp(koefisien logit). Seberapa besar odds berubah per satu unit X. Sesi 4.

**Efek marjinal**  
Perubahan peluang (poin persen) per satu unit X. Cara paling mudah
menjelaskan hasil logit. Sesi 4.

**Multinomial logit**  
Model untuk Y dengan 3+ kategori tanpa urutan (motor, mobil, bus). Sesi 4.

**Ordinal logit/probit**  
Model untuk Y dengan kategori berurutan (buruk, cukup, baik). Memakai
ambang antar kategori. Sesi 4.

**Threshold (ambang)**  
Batas antar kategori pada model ordinal. Harus berurutan naik. Sesi 4.

**Tobit**  
Model untuk Y kontinu yang tersensor, misalnya menumpuk di nol. Sesi 4.

**Regresi Poisson**  
Model untuk Y berupa hitungan (jumlah klaim, jumlah pelanggan). Sesi 4.

**Overdispersi**  
Varians data hitungan jauh lebih besar dari rata-ratanya. Penanganannya
Negative Binomial. Sesi 4.

**Perfect separation**  
Kondisi ketika X memprediksi Y dengan benar 100 persen, sehingga logit
biasa tidak stabil. Penanganannya regularisasi atau Firth. Sesi 4.

### Deret waktu (Sesi 5, Lab 5)

**Stasioner**  
Rata-rata dan varians data konstan sepanjang waktu. Syarat utama model
deret waktu. Sesi 5.

**Uji ADF (Augmented Dickey-Fuller)**  
Uji akar unit. Hipotesis nolnya data tidak stasioner. Sesi 5.

**Selisih (differencing)**  
Mengurangi nilai periode ini dengan periode sebelumnya untuk membuat
data stasioner. Sesi 5.

**ACF dan PACF**  
Grafik korelasi antar periode untuk menebak orde AR dan MA. Sesi 5.

**ARIMA**  
Model deret waktu dengan komponen autoregresif, selisih, dan moving
average. Ordenya dipilih dengan AIC. Sesi 5.

**AIC**  
Ukuran kecocokan model yang menghukum kompleksitas. Makin kecil makin
baik. Sesi 5.

**Kointegrasi**  
Dua seri tidak stasioner yang tetap berjalan bersama dalam jangka
panjang. Syarat sahnya ECM. Sesi 5.

**ECM (Error Correction Model)**  
Model yang menggabungkan efek jangka pendek dan koreksi menuju
keseimbangan jangka panjang. Sesi 5.

**ECT (Error Correction Term)**  
Residual jangka panjang yang dipakai di ECM. Koefisiennya harus negatif
dan signifikan. Sesi 5.

**Patahan struktural (structural break)**  
Perubahan rezim yang menggeser level data, misalnya krisis 1998. Sesi 5.

### Panel dan GARCH (Sesi 6, Lab 5-6)

**Data panel**  
Data yang menggabungkan banyak unit (negara, toko) dan waktu. Sesi 6.

**CEM, FEM, REM**  
Common Effect, Fixed Effect, Random Effect. Tiga pilihan model panel.
Sesi 6.

**Uji Chow**  
Memilih antara CEM dan FEM. Sesi 6.

**Uji Hausman**  
Memilih antara FEM dan REM. Laporkan p-value mentahnya. Sesi 6.

**Volatility clustering**  
Pola "tenang mengelompok, gejolak mengelompok" di data keuangan. Sesi 6.

**ARCH dan GARCH**  
Model untuk volatilitas. Alpha mengukur reaksi guncangan baru, beta
mengukur persistensi. Sesi 6.

**Persistensi (alpha + beta)**  
Kecepatan guncangan hilang. Mendekati 1 berarti lama. Tepat 1 disebut
IGARCH. Sesi 6.

**VaR (Value at Risk)**  
Perkiraan kerugian yang hanya terlampaui pada persentase hari terburuk.
Dipakai di Lab 6. Lab 6.

**Data tersensor**  
Data yang menumpuk di batas tertentu, misalnya nol. Bukan data hilang.
Sesi 4.
