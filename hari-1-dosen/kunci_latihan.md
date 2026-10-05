# Kunci Latihan Hari 1 (Dosen)

Semua angka di bawah dihasilkan dari data di folder `data/`. Jalankan
notebooknya sendiri untuk memverifikasi; hasilnya harus sama.

## Sesi 0

1. `data/uts-4.csv` berisi 50 baris dan 4 kolom.
2. Rata-rata `Y_Angka_Harapan_Hidup` = 76,95. Rata-rata
   `X2_Tingkat_Imunisasi` = 91,86.

## Sesi 1: regresi dasar

1. Model padi: hanya curah hujan yang signifikan (koefisien 0,0029,
   p = 0,0000). Pupuk (p = 0,69) dan sinar matahari (p = 0,48) tidak
   signifikan. R kuadrat 0,988.
2. Prediksi produktivitas pada pupuk 160, hujan 1900, sinar 230 = 7,624.
3. Uji gabungan pupuk dan sinar matahari: p = 0,766, jauh di atas 0,05.
   Keduanya tidak signifikan bersama-sama.

Catatan: pola padi menarik untuk diskusi. Curah hujan mendominasi, pupuk
tidak terlihat efeknya. Di data nyata, ini bisa jadi tanda rentang pupuk
terlalu sempit atau ada faktor lain.

## Sesi 2: bentuk fungsional

1. Reciprocal pengalaman dan waktu produksi: batas asimtot = 4,98
   (dibaca dari intersep). Prediksi untuk pengalaman 6 bulan = 13,32.
2. Usia dan kinerja: adj R kuadrat linear 0,268, kuadratik 0,999.
   Tambahan `usia2` sangat sepadan. Titik puncak 39,46 tahun.
3. Uji skala Cobb-Douglas: p-value = 2,3e-26, tolak skala tetap. Jumlah
   elastisitas 1,47, artinya increasing returns to scale.

## Sesi 3: dummy dan asumsi klasik

1. VIF `latihan-multikolinieritas-2.csv`: pendapatan 59,65, kekayaan
   54,90, jumlah anggota 2,59. Koefisien pendapatan bergeser dari 0,696
   (dengan kekayaan) ke 0,503 (tanpa kekayaan). Pergeseran sebesar itu
   adalah gejala khas multikolinearitas; pilih salah satu variabel yang
   paling sesuai teori.
2. Heteroskedastisitas `hetero-2.csv`: Breusch-Pagan p = 0,0025 (ada
   masalah), White p = 0,0638 (tidak menolak pada 5%). Setelah robust SE,
   p-value pendidikan naik dari 0,0089 ke 0,0286. Tetap signifikan, tapi
   lebih lemah.
3. `hetero-1.csv`: BP p = 0,997 dan White p = 0,542. Tidak ada bukti
   heteroskedastis. Dugaan di soal tidak didukung data.
4. Normalitas `latihan-normalitas-3.csv`: Jarque-Bera = 3,19 dengan
   p = 0,203. Residual normal.

## Sesi 4: model kategorikal

1. Logit kelulusan (`logit-probit-2.csv`): data terpisah sempurna, MLE
   polos tidak stabil. Tiga jalan keluar yang bisa dibandingkan:
   - statsmodels `fit_regularized` (alpha = 0,5): IPK +15,10, SKS -1,23,
     keaktifan organisasi -0,12, beasiswa 0,00.
   - scikit-learn `LogisticRegression` bawaan (regularisasi L2 otomatis):
     koefisien berhingga tanpa pengaturan, tapi besarannya bergantung
     skala variabel.
   - Kesimpulan untuk diajarkan: regularisasi menstabilkan estimasi;
     p-value tidak tersedia di kedua versi regularisasi. Jelaskan
     penyebabnya (separation), bukan sekadar "koefisiennya aneh".
2. Ordinal `multi-ordinal-1.csv` dengan probit: waktu tunggu -7,18,
   keramahan staf +10,80, aplikasi digital +6,24, threshold -1,60 dan
   4,06 (berurutan, aman). Tanda sama dengan versi logit, hanya skalanya
   lebih kecil (rasio khas logit terhadap probit sekitar 1,6).
3. `multi-ordinal-3.csv` sebagai bahan diskusi: threshold yang keluar
   adalah 9,36 lalu 4,92, tidak berurutan. Gejala khas data simulasi yang
   nyaris terpisah sempurna. Tindakan yang bisa disebut: gabungkan
   kategori, pakai multinomial, atau tambah variasi data. Koefisiennya
   jangan dikutip mentah.
4. scikit-learn dengan `test_size=0,3`: akurasi berubah cukup banyak saat
   `random_state` diganti. Dengan 32 observasi, sampel uji hanya sekitar
   10 orang, jadi satu orang saja yang berpindah prediksi sudah
   menggeser akurasi 10 poin persen. Pesan: metrik pada sampel kecil
   tidak stabil, laporkan beberapa pembagian data.
5. Poisson klaim (`poisson_data_1_klaim.csv`): IRR usia 1,023 (p = 0,91),
   pengalaman 0,784 (p = 0,35), tipe mobil 1,410 (p = 0,42). Tidak ada
   yang signifikan. Overdispersi 0,141 (aman), AIC Poisson 80,9 lebih
   kecil dari NB 82,9. Kesimpulan jujur: data ini tidak menunjukkan efek
   yang bisa dibedakan dari nol.

## Sesi 5: deret waktu

1. IHSG dan emas: p kointegrasi = 0,494, tidak terkointegrasi. ECM tidak
   layak dipakai. Kalau tetap dijalankan, koefisien ECT memang terlihat
   signifikan, tapi itu menyesatkan persis karena syarat kointegrasi
   tidak dipenuhi. Pelajaran: urutan uji tidak boleh dilompati.
2. Ramalan inflasi ARIMA(1,1,0): 137,59; 138,36; 139,13; 139,88; 140,62.
   Ramalan dengan d = 0 akan tertarik ke rata-rata, tidak masuk akal
   untuk indeks yang bertren. Pakai d = 1.
3. ADF pada kurs gagal karena uji itu mengasumsikan satu proses
   stasioner, sedangkan kurs berpindah level (patahan struktural). Solusi:
   dummy periode atau uji Chow.

## Sesi 6: panel dan GARCH

1. Retail: koefisien diskon di CEM -157,07 (signifikan), di FEM -1,94
   (p = 0,956). Di CEM, koefisien itu mencampur perbedaan antar toko
   dengan efek diskon sesungguhnya. Uji Chow menolak CEM (p = 0,0000).
   Hausman p = 1,0 (REM tidak tertolak); apa pun pilihannya, kesimpulan
   tentang diskon sama: tidak signifikan setelah efek toko dikontrol.
2. GARCH(2,1): AIC 208,69, lebih besar dari GARCH(1,1) 206,69. Tambahan
   orde tidak sepadan.
3. Data nyata: jawaban berbeda-beda, tergantung periode. Yang dicek:
   apakah beta akhirnya besar (persistensi nyata) berbeda dengan data
   simulasi yang murni ARCH.
