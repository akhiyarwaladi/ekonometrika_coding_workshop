# Mulai di sini: ekonometrika tanpa pengalaman coding

Panduan ini dipakai sebelum membuka notebook pertama. Targetnya adalah
membaca data, menjalankan model, dan menjelaskan hasilnya dengan kata sendiri.
Anda cukup mengubah contoh yang sudah tersedia.

## Berkas yang dibuka peserta

1. [Buka notebook persiapan di Colab](https://colab.research.google.com/github/akhiyarwaladi/ekonometrika_coding_workshop/blob/main/materi/01_ekonometrika/00_persiapan_colab.ipynb)
   dan simpan salinan ke Google Drive. Tautan untuk sesi berikutnya ada pada
   [daftar materi](00_daftar_materi.md).
2. Jalankan kotak kode alamat data dengan `Shift + Enter`. Gunakan koneksi internet.
3. Setelah tulisan **Alamat data siap** muncul, jalankan kotak berikutnya.
4. `pd.read_csv(URL_DATA + "nama_file.csv")` membaca tabel langsung dari GitHub.

[Peta pemakaian data](08_peta_pemakaian_data.md) menunjukkan nama CSV untuk setiap notebook.
Untuk dashboard penutup, hanya `provinsi_2021.csv` yang dipakai.

Jika sudah mempunyai berkas `.ipynb` di komputer, notebook juga bisa dibuka
melalui **File > Upload notebook**. Urutan pengerjaannya tetap sama.

Notebook adalah lembar kerja yang berisi penjelasan, kotak kode (sel), dan
hasil. Penjelasan dibaca; sel kode dijalankan. Angka dalam kurung siku di
kiri sel menunjukkan bahwa sel pernah dijalankan. Simpan salinan notebook
ke Drive agar jawaban latihan tidak hilang.

`URL_DATA` menyimpan alamat folder CSV di GitHub. Nama file di dalam `read_csv`
memilih tabel yang akan dibaca. Pada materi kategorikal, sel persiapan juga mengambil
modul untuk contoh Tobit dan logit khusus. Jalankan sel persiapan apa adanya.
Notebook baru mempunyai ruang variabel sendiri: jalankan kembali dari atas setiap membuka notebook lain.

## Perintah yang sering muncul

Sebelum menjalankan sel pembacaan data, baca tabel **Kenali data**.
Contohnya, `eps` berarti laba per lembar saham dan `der` adalah rasio utang
terhadap ekuitas. Pada data pendidikan, `GPA` adalah rata-rata nilai mahasiswa,
sedangkan `GRADE` berkode 1 jika nilai meningkat dan 0 jika tidak meningkat.
Definisi lengkap ada di [kamus variabel](07_kamus_variabel.md).

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

## Simbol yang perlu dikenal saat bertemu

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

## Contoh lengkap: baca, hitung, lihat

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

## Perintah tambahan diperkenalkan saat diperlukan

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

## Jika hasil belum muncul

| Pesan/keadaan | Langkah yang dilakukan |
|---|---|
| Pembacaan CSV gagal | Periksa koneksi internet dan ejaan nama CSV. Jalankan kembali sel alamat data. |
| `NameError` | Nama belum dibuat atau salah ketik. Jalankan sel sebelumnya dari atas. |
| `KeyError` | Nama kolom berbeda. Tampilkan `print(saham.columns)` dan cocokkan ejaannya. |
| `SyntaxError` | Periksa tanda kutip, kurung, dan koma di sel yang diubah. |
| `ModuleNotFoundError` | Jalankan sel instalasi yang tersedia dan tunggu sampai selesai. |
| Warning konvergensi/separation | Baca catatan metode pada notebook; koefisien/p-value bisa tidak layak ditafsirkan. |
| Runtime dimulai ulang | Jalankan notebook kembali dari sel pertama. |

Jika memakai AI untuk membantu, contoh permintaannya ada di `panduan/02_panduan_ai.md`.
Sertakan pesan error dan sel terkait agar bantuan sesuai masalahnya.

## Menjalankan di komputer sendiri

Buka notebook `.ipynb` di Jupyter atau VS Code dengan kernel Python yang
sudah dipasangi paket dari `requirements.txt`. Data dibaca dari alamat GitHub
yang sama seperti di Colab; gunakan koneksi internet.
Jalankan semua sel dari atas setiap memulai kernel baru.
