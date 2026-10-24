# Menggunakan AI sebagai pendamping analisis

Bagian ini mendampingi praktik ekonometrika dalam pelatihan 26 Oktober
2026. Gunakan layanan AI yang tersedia bagi peserta. Tidak diperlukan
API key atau kode untuk menghubungkan notebook ke layanan AI.

Hasil numerik berasal dari kode yang dijalankan di notebook. Jawaban AI
dibandingkan kembali dengan data, rumus model, dan output tersebut.

## Latihan terbimbing, sekitar 30 sampai 40 menit

1. Jalankan contoh regresi harga saham di Sesi 1 hingga tabel hasil muncul.
2. Minta AI menjelaskan satu sel kode dengan prompt pertama di bawah.
3. Minta penjelasan satu koefisien menggunakan output aktual.
4. Ubah satu nilai prediksi, jalankan ulang, lalu bandingkan penjelasannya.
5. Simpan sel yang dipakai, hasilnya, dan kesimpulan dengan kata sendiri.

Pengajar mendemokan satu contoh sebelum peserta mencoba. Teks di dalam
kurung siku pada prompt perlu diisi oleh peserta; itu bukan kode Python.

## Memahami kode yang sudah disiapkan

```text
Saya belajar ekonometrika dan belum pernah coding.
Jelaskan kode berikut satu baris setiap kali, dengan bahasa Indonesia.
Sebutkan data masuk, hasil yang disimpan, dan bagian yang boleh saya ubah.
Gunakan nama variabel yang sama. Jangan menambahkan fungsi buatan sendiri,
perulangan, atau perhitungan matriks.

Kode:
[tempel satu sel kode dari notebook]
```

Periksa bahwa penjelasan memakai nama kolom yang benar dan menjelaskan
apa yang dilakukan `fit()`, bukan mengarang hasil regresi.

## Meminta contoh perubahan model

```text
Tabel saya bernama saham. Kolom yang tersedia:
Y_Harga_Saham, X1_Pendapatan_per_Saham, X2_Rasio_Utang_Ekuitas,
X3_Belanja_Iklan. Data ini adalah simulasi untuk belajar.

Buat regresi OLS harga saham pada ketiga variabel penjelas dengan
scikit-learn. Tulis langkah berurutan: tentukan tabel X dan target y, buat LinearRegression, jalankan fit,
lalu tampilkan coef_, intercept_, dan R². Tambahkan komentar pendek dalam bahasa Indonesia.
Jangan memakai fungsi buatan sendiri atau mengambil data baru dari internet.
Jangan menuliskan angka hasil sebelum kode dijalankan.
```

Jalankan usulan dalam sel baru. Cocokkan rumus dengan pertanyaan penelitian,
lalu bandingkan hasil dengan model berganda yang sudah tersedia di Sesi 1.

## Memahami output aktual

```text
Berikut output regresi yang sudah saya jalankan:
[tempel baris koefisien, p-value, N, dan R-squared]

Y adalah [nama dan satuan]. X adalah [nama dan satuan].
Jenis data: [cross-section/deret waktu/panel], sumber: [sumber data].
Jelaskan arah, besaran, dan ketidakpastian hubungan untuk satu X.
Gunakan taraf uji 5%. Bedakan hubungan statistik dari sebab akibat.
Jika informasi belum cukup, sebutkan yang kurang. Jangan mengarang angka.
```

Sebelum memakai jawabannya, cocokkan tanda dan besaran koefisien, satuan,
p-value, kategori basis jika ada dummy, serta model yang sedang dibaca.
Untuk HC3/HAC, pastikan p-value yang dibaca berasal dari hasil koreksi.

## Memahami error tanpa mengganti seluruh notebook

```text
Saya menjalankan notebook ekonometrika di Google Colab.
Sel yang error:
[tempel sel terkait]
Pesan error lengkap:
[tempel pesan error]
Nama kolom dari print(saham.columns):
[tempel hasilnya; sesuaikan nama tabel bila bukan saham]

Jelaskan penyebabnya dengan bahasa sederhana dan usulkan perubahan sekecil
mungkin. Pertahankan pertanyaan penelitian dan rumus model. Jelaskan
setiap baris yang berubah. Jangan memasang paket tambahan jika tidak perlu.
```

Jika masalahnya `NameError`, jalankan lebih dulu sel sebelumnya. Jika
masalahnya konvergensi, jangan sekadar meminta AI menyembunyikan warning.
Periksa kelayakan estimator dan catatan metode di notebook.

## Lembar jawaban peserta

Catat lima hal berikut dalam sel teks di akhir latihan:

1. Pertanyaan ekonomi dan variabel yang dipakai.
2. Prompt yang diajukan kepada AI.
3. Kode akhir yang benar-benar dijalankan.
4. Angka penting dari output dan penjelasannya.
5. Saran AI yang diperbaiki atau tidak dipakai, beserta alasannya.

Gunakan data latihan yang dibagikan. Untuk data penelitian pribadi,
bagikan struktur kolom atau contoh yang sudah dianonimkan jika perlu
bantuan; jangan menempelkan identitas responden atau kredensial akses.
