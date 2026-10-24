# Pola pemodelan dengan scikit-learn

Tutorial memakai scikit-learn sebagai pustaka utama untuk regresi linear,
logit, multinomial, dan Poisson. Setiap contoh mengikuti urutan yang sama:
pilih fitur X, pilih target y, buat model, jalankan `fit`, lalu `predict`.

```python
import pandas as pd
from sklearn.linear_model import LinearRegression

URL_DATA = "https://raw.githubusercontent.com/akhiyarwaladi/ekonometrika_coding_workshop/main/data/"
saham = pd.read_csv(URL_DATA + "uts_2.csv")
X = saham[["X1_Pendapatan_per_Saham"]]
y = saham["Y_Harga_Saham"]
model = LinearRegression()
model.fit(X, y)

print("Intersep:", model.intercept_)
print("Koefisien EPS:", model.coef_[0])
```

Jalankan contoh dengan koneksi internet. Dalam notebook,
sel persiapan menetapkan alamat data GitHub. `X` memakai dua pasang kurung siku
karena harus berbentuk tabel, termasuk ketika fiturnya hanya satu.
`y` memakai satu pasang kurung siku karena berupa satu kolom.

## Perintah yang dipakai

| Perintah | Arti |
|---|---|
| `model.fit(X, y)` | Pelajari koefisien dari data latihan. |
| `model.coef_` | Koefisien sesuai urutan kolom X. |
| `model.intercept_` | Intersep model. |
| `model.predict(X_baru)` | Nilai prediksi regresi atau label kelas klasifikasi. |
| `model.predict_proba(X_baru)` | Peluang setiap kelas; urutannya mengikuti `model.classes_`. |
| `model.score(X, y)` | R² untuk LinearRegression; akurasi untuk LogisticRegression. |

Jangan menyamakan `score` antarjenis model. Pada PoissonRegressor, `score`
adalah deviance explained (D²). Untuk evaluasi yang jelas, gunakan fungsi metrik
yang sesuai tujuan, seperti RMSE dan R² untuk regresi, atau akurasi dan ROC AUC
untuk klasifikasi. Nilai pada data latih harus dibedakan dari nilai pada data uji.

Nama `X_model1` atau `X_model_cd` mempertahankan tabel fitur milik masing-masing
model. Hal ini mencegah tertukarnya kolom saat satu notebook memuat beberapa model.
`koefisien_model1` adalah pandas Series yang memberi label pada `model1.coef_`,
dengan satu baris tambahan untuk intersep. Nama model tidak diberi atribut buatan.

## Pilihan model

| Kebutuhan | Estimator utama |
|---|---|
| Regresi linear sederhana, berganda, log, dummy, reciprocal, polinomial | `LinearRegression` setelah menyiapkan kolom yang diperlukan. |
| Pembanding yang selalu menebak rata-rata | `DummyRegressor(strategy="mean")`. |
| Logit biner dan multinomial | `LogisticRegression`. |
| Hitungan dengan log-link | `PoissonRegressor(alpha=0)` untuk contoh tanpa penalti. |

`LinearRegression` menggunakan metode OLS. Logit tanpa penalti memakai
`LogisticRegression(penalty=None)` pada versi scikit-learn 1.6.1 yang digunakan
untuk pengujian. Contoh dengan separation memakai regularisasi; koefisiennya
tidak otomatis sama dengan koefisien model tanpa penalti. Poisson juga diberi
`alpha=0` agar perbandingan dengan inferensi Poisson tanpa penalti setara.

## Pelengkap inferensi

P-value, standard error, interval kepercayaan koefisien, serta beberapa uji
ekonometrika belum disediakan langsung oleh estimator tersebut. Bagian ini
memakai statsmodels dengan nama `uji_...`, berdasarkan sampel, X, dan y yang sama.
Model scikit-learn tetap digunakan untuk koefisien dan prediksi utama.

Contoh regresi mempertahankan baris yang lengkap untuk kolom model melalui
`dropna()`. Ini menyamakan observasi estimasi dengan pelengkap inferensinya.
Pada Housing, data kosong ditangani dengan imputer yang hanya dilatih pada train.

Untuk logit, tabel standard error dan efek marjinal berasal dari estimasi
tanpa penalti pada pelengkap inferensi. Jangan menempelkan p-value tersebut pada
koefisien model yang menggunakan regularisasi. Hasil dua optimasi numerik dapat
berbeda sedikit meskipun tujuannya sama; pemeriksaan memakai toleransi numerik.

## Model khusus

Probit, ordinal, Tobit, Negative Binomial, ARIMA, panel, dan GARCH memerlukan
pustaka khusus pada materi ini. Judul atau catatan bagian menjelaskan alasannya.
Ordinal tetap mempertahankan urutan kategori; multinomial biasa tidak digunakan
sebagai pengganti diam-diam. Data panel tetap memperhitungkan unit dan waktu.

Dokumentasi: [LinearRegression](https://scikit-learn.org/1.6/modules/generated/sklearn.linear_model.LinearRegression.html),
[LogisticRegression](https://scikit-learn.org/1.6/modules/generated/sklearn.linear_model.LogisticRegression.html),
[PoissonRegressor](https://scikit-learn.org/1.6/modules/generated/sklearn.linear_model.PoissonRegressor.html).

Kembali ke [daftar materi](../../panduan/daftar_materi.md).
