# Glosarium

Istilah yang muncul di workshop, diurutkan sesuai kemunculannya. Setiap
entri menyebut tempat istilah itu diperkenalkan, supaya mudah dilacak.

## Dasar regresi (Sesi 1, Lab 0-1)

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

## Bentuk fungsional (Sesi 2, Lab 2)

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

## Diagnostik (Sesi 3, Lab 3)

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

## Variabel kategorikal (Sesi 4, Lab 4)

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

## Deret waktu (Sesi 5, Lab 5)

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

## Panel dan GARCH (Sesi 6, Lab 5-6)

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
