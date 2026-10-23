# Proyek Mini: dari Pertanyaan ke Kesimpulan

Proyek ini meniru alur UAS di halaman kuliah: tentukan topik, kumpulkan
data, olah dengan regresi, lalu simpulkan. Batas waktu: dikerjakan setelah
hari kedua, boleh kelompok 3 sampai 4 orang.

## Pilihan sumber data

**Opsi A: survei sendiri (seperti UAS).** Buat Google Form dengan 8 sampai
12 pertanyaan, sebarkan ke teman sekelas, target minimal 50 responden.
Skala Likert 1 sampai 5 boleh dipakai, tapi satu variabel dependen harus
angka kontinu atau 0/1 supaya modelnya jelas.

**Opsi B: data terbuka.** Contoh sumber yang bisa dipakai:

- World Bank Open Data (data.worldbank.org): indikator ekonomi negara.
- BPS (bps.go.id): data Indonesia per provinsi atau per waktu.
- Kaggle dan GitHub dataset: cek lisensinya.

Contoh mengambil data World Bank langsung di Colab (butuh internet):

```python
# %pip install wbdata -q
import wbdata

# PDB per kapita dan inflasi untuk Indonesia, Malaysia, Thailand
indikator = {
    "NY.GDP.PCAP.CD": "gdp_per_kapita",
    "FP.CPI.TOTL.ZG": "inflasi",
}
data = wbdata.get_dataframe(indikator, country=["IDN", "MYS", "THA"])
data = data.reset_index()
data.head()
```

Kalau situsnya tidak bisa diakses saat kelas, pakai Opsi A.

## Langkah pengerjaan

1. **Rumuskan pertanyaan.** Satu kalimat, misalnya: "Apakah harga
   berpengaruh terhadap jumlah pembelian?" Tulis juga dugaan arahnya.
2. **Tentukan variabel.** Satu Y (dependen), dua sampai empat X
   (independen). Sebutkan satuan tiap variabel.
3. **Kumpulkan data.** Pastikan tidak ada kolom kosong. Kalau ada, jelaskan
   cara menanganinya.
4. **Eksplorasi.** Tampilkan tabel ringkasan dan satu grafik untuk setiap
   hubungan utama.
5. **Estimasi model.** Mulai dari OLS. Kalau Y kategorikal, pakai logit.
6. **Uji asumsi.** Multikolinearitas (VIF), heteroskedastisitas
   (Breusch-Pagan), normalitas residual, dan autokorelasi kalau data
   deret waktu.
7. **Perbaiki kalau perlu.** Robust standard error untuk
   heteroskedastisitas, HAC untuk autokorelasi.
8. **Tulis laporan.** Maksimal 5 halaman: pendahuluan, data dan metode,
   hasil, interpretasi, keterbatasan.

## Yang dinilai

| Aspek | Bobot | Yang dilihat |
|---|---|---|
| Pertanyaan dan desain | 20% | pertanyaan jelas, variabel masuk akal |
| Ketepatan metode | 30% | model sesuai jenis Y, asumsi diuji |
| Interpretasi | 30% | angka dibaca dalam konteks, bukan sekadar signifikan |
| Penyajian | 20% | laporan rapi, grafik berlabel, tidak ada klaim berlebihan |

## Jebakan yang sering terjadi

- Menyimpulkan sebab akibat dari data cross-section. Bilang "berhubungan
  dengan" kalau desainnya tidak memungkinkan klaim kausal.
- Membuang outlier tanpa alasan. Laporkan dan jelaskan.
- Memilih model hanya dari R kuadrat tertinggi. Teori dulu, baru angka.
- Tidak menyebut satuan saat menafsirkan koefisien.
