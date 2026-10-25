# Proyek mini: dari pertanyaan ke kesimpulan

Pilih satu pertanyaan, jalankan analisis dalam notebook, lalu jelaskan hasilnya.
Proyek dikerjakan setelah latihan, boleh berkelompok 3 sampai 4 orang.

## Pilih satu kasus

Kasus berikut memakai data yang sudah tersedia. Mulai dari notebook rujukan;
baca tabel Kenali data untuk memahami arti setiap variabel dan satuannya.

| Kasus | Pertanyaan | Mulai dari | Hasil minimum |
|---|---|---|---|
| Ramalan inflasi | Apakah dua lag membantu meramal inflasi bulan berikutnya? | Pengayaan [Lab 05](05_deret_waktu_panel.ipynb), `data/idn_inflasi_bulanan.csv` | Pembagian berdasarkan waktu, pembanding naif, MAE/RMSE, dan grafik aktual versus ramalan. |
| Keputusan kredit | Bagaimana perubahan biaya gagal bayar mengubah pilihan ambang? | Pengayaan [Lab 04](04_model_kategorikal.ipynb), `data/kredit_default.csv` | Pilihan ambang berdasarkan validasi, matriks kebingungan, dan perbandingan biaya pada data uji. |
| Regresi harga rumah | Fitur mana yang membantu memprediksi harga pada data uji? | [Notebook Housing](../03_regresi_housing/01_regresi_housing.ipynb), `data/housing.csv` | Model sederhana dan berganda, pembanding rata-rata, RMSE, dan grafik residual. |

Data kredit berasal dari Taiwan dan Housing dari Boston; keduanya bukan data Indonesia.
Untuk kasus Indonesia, pilih inflasi. Tabel DiD delapan baris pada Sesi 03 adalah simulasi
pengantar; jangan menjadikannya bukti keberhasilan program nyata.

Arti `tanggal`, `indeks`, `inflasi_mom`, dan `inflasi_yoy` mengikuti
[kamus inflasi](../../data/README.md#idn_inflasi_bulanan_csv). Bacalah sebelum menjalankan kode.
`inflasi_yoy` bersatuan persen; angka 2 berarti 2%, bukan 0,02%.

Contoh membuka data inflasi dalam notebook:

```python
import pandas as pd

URL_DATA = "https://raw.githubusercontent.com/akhiyarwaladi/ekonometrika_coding_workshop/main/data/"
inflasi = pd.read_csv(URL_DATA + "idn_inflasi_bulanan.csv")
inflasi.head()
```

Survei sendiri juga boleh. Buat 8 sampai 12 pertanyaan, jelaskan sasaran dan cara
memilih responden, lalu kumpulkan data yang memadai untuk pertanyaan dan model.
Sampel teman sekelas tidak otomatis mewakili penduduk Indonesia.

## Langkah pengerjaan

1. **Rumuskan pertanyaan.** Satu kalimat yang sesuai dengan kasus pilihan.
   Bedakan tujuan menjelaskan hubungan, meramal, dan mengambil keputusan.
2. **Tentukan variabel.** Satu Y (dependen), dua sampai empat X
   (independen). Sebutkan satuan tiap variabel.
3. **Periksa data.** Jelaskan periode, asal, jumlah pengamatan, nilai kosong,
   dan cara menanganinya. Patokan pengolahan dipelajari dari data latihan.
4. **Eksplorasi.** Tampilkan tabel ringkasan dan satu grafik untuk setiap
   hubungan utama.
5. **Latih model.** Gunakan scikit-learn dan mulai dari rancangan sederhana
   pada notebook rujukan. Sisakan data uji; data deret waktu harus mengikuti urutan waktu.
6. **Periksa sesuai tujuan.** Untuk inferensi regresi, periksa asumsi dan
   standard error yang sesuai. Untuk prediksi, nilai data yang belum dipakai melatih.
   Untuk kredit, bedakan dua jenis kesalahan dan biaya masing-masing.
7. **Bandingkan hasil.** Gunakan pembanding sederhana. Pilih rancangan atau
   ambang pada validasi; jangan memilih berdasarkan data uji lalu melaporkan
   data yang sama sebagai pengujian independen.
8. **Tulis laporan.** Maksimal 5 halaman: pendahuluan, data dan metode,
   hasil, interpretasi, keterbatasan.

## Yang dinilai

| Aspek | Bobot | Yang dilihat |
|---|---|---|
| Pertanyaan dan desain | 20% | pertanyaan jelas, variabel masuk akal |
| Ketepatan metode | 30% | metode sesuai tujuan, pemisahan data dan pembanding tepat |
| Interpretasi | 30% | angka dibaca dalam konteks, bukan sekadar signifikan |
| Penyajian | 20% | laporan rapi, grafik berlabel, tidak ada klaim berlebihan |

## Jebakan yang sering terjadi

- Menyimpulkan sebab akibat dari data cross-section. Bilang "berhubungan
  dengan" kalau desainnya tidak memungkinkan klaim kausal.
- Membuang outlier tanpa alasan. Laporkan dan jelaskan.
- Memilih model hanya dari R kuadrat tertinggi. Teori dulu, baru angka.
- Tidak menyebut satuan saat menafsirkan koefisien.
