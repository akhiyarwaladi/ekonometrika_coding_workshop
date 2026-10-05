"""Bangun slide pembuka workshop dengan python-pptx.

Jalankan: python scripts/make_slides.py
Output: slide-workshop.pptx (di root proyek)

Desain: latar krem, pita judul hijau tua, aksen terracotta, huruf Arial,
kode memakai Courier New. Setiap slide punya catatan pembicara.
"""

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

OUT = Path(__file__).resolve().parent.parent / "slide-workshop.pptx"

INK = RGBColor(0x22, 0x31, 0x2B)
GREEN = RGBColor(0x2F, 0x5D, 0x50)
ACCENT = RGBColor(0xC1, 0x59, 0x37)
CREAM = RGBColor(0xFA, 0xF6, 0xEF)
MUTED = RGBColor(0x6B, 0x7A, 0x72)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
FONT = "Arial"
MONO = "Courier New"

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]


def kotak(slide, kiri, atas, lebar, tinggi, warna, garis=None):
    from pptx.enum.shapes import MSO_SHAPE
    bentuk = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(kiri), Inches(atas),
                                    Inches(lebar), Inches(tinggi))
    bentuk.fill.solid()
    bentuk.fill.fore_color.rgb = warna
    if garis is None:
        bentuk.line.fill.background()
    else:
        bentuk.line.color.rgb = garis
    bentuk.shadow.inherit = False
    return bentuk


def teks(slide, isi, kiri, atas, lebar, tinggi, ukuran=16, warna=INK,
         tebal=False, rata=PP_ALIGN.LEFT, font=FONT, spasi=1.0):
    tb = slide.shapes.add_textbox(Inches(kiri), Inches(atas), Inches(lebar), Inches(tinggi))
    tf = tb.text_frame
    tf.word_wrap = True
    baris = isi if isinstance(isi, list) else [isi]
    for i, item in enumerate(baris):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = item
        p.alignment = rata
        p.line_spacing = spasi
        p.space_after = Pt(6)
        for run in p.runs:
            run.font.size = Pt(ukuran)
            run.font.color.rgb = warna
            run.font.bold = tebal
            run.font.name = font
    return tb


def catatan(slide, isi):
    slide.notes_slide.notes_text_frame.text = isi


def slide_isi(judul, poin, catatan_teks, subjudul=None):
    s = prs.slides.add_slide(BLANK)
    kotak(s, 0, 0, 13.333, 7.5, CREAM)
    kotak(s, 0, 0, 13.333, 1.15, GREEN)
    kotak(s, 0, 1.15, 13.333, 0.06, ACCENT)
    teks(s, judul, 0.55, 0.18, 12.2, 0.8, ukuran=28, warna=WHITE, tebal=True)
    if subjudul:
        teks(s, subjudul, 0.57, 1.35, 12.2, 0.5, ukuran=15, warna=MUTED)
        atas = 1.95
    else:
        atas = 1.55
    teks(s, poin, 0.65, atas, 12.0, 7.3 - atas, ukuran=17, spasi=1.12)
    catatan(s, catatan_teks)
    return s


def slide_dua_kolom(judul, kiri_judul, kiri_poin, kanan_judul, kanan_poin, catatan_teks):
    s = prs.slides.add_slide(BLANK)
    kotak(s, 0, 0, 13.333, 7.5, CREAM)
    kotak(s, 0, 0, 13.333, 1.15, GREEN)
    kotak(s, 0, 1.15, 13.333, 0.06, ACCENT)
    teks(s, judul, 0.55, 0.18, 12.2, 0.8, ukuran=28, warna=WHITE, tebal=True)

    kotak(s, 0.55, 1.55, 6.05, 5.3, WHITE)
    kotak(s, 0.55, 1.55, 6.05, 0.55, GREEN)
    teks(s, kiri_judul, 0.8, 1.62, 5.6, 0.5, ukuran=18, warna=WHITE, tebal=True)
    teks(s, kiri_poin, 0.85, 2.3, 5.5, 4.4, ukuran=15, spasi=1.1)

    kotak(s, 6.85, 1.55, 6.05, 5.3, WHITE)
    kotak(s, 6.85, 1.55, 6.05, 0.55, ACCENT)
    teks(s, kanan_judul, 7.1, 1.62, 5.6, 0.5, ukuran=18, warna=WHITE, tebal=True)
    teks(s, kanan_poin, 7.15, 2.3, 5.5, 4.4, ukuran=15, spasi=1.1)
    catatan(s, catatan_teks)
    return s


# Slide 1: judul
s = prs.slides.add_slide(BLANK)
kotak(s, 0, 0, 13.333, 7.5, GREEN)
kotak(s, 0.9, 4.55, 3.2, 0.07, ACCENT)
teks(s, "Workshop Ekonometrika", 0.9, 2.3, 11.5, 1.2, ukuran=44, warna=CREAM, tebal=True)
teks(s, "dengan Google Colab", 0.9, 3.35, 11.5, 1.0, ukuran=32, warna=CREAM)
teks(s, "Hari pertama untuk dosen, hari kedua untuk mahasiswa", 0.9, 4.85, 11.5, 0.6,
     ukuran=16, warna=WHITE)
teks(s, "Materi dan data: paggalih.github.io/matkul/sem2025-01/ekonometrika",
     0.9, 6.3, 11.5, 0.5, ukuran=13, warna=RGBColor(0xCF, 0xDD, 0xD6))
catatan(s, "Buka dengan tujuan praktis: peserta keluar dari ruangan bisa "
           "menjalankan analisis sendiri. Sebutkan bahwa semua kode sudah diuji "
           "dan data tersedia lokal, jadi tidak ada kejutan teknis.")

# Slide 2: hasil yang dicapai
slide_isi(
    "Yang dicapai dalam dua hari",
    [
        "Hari 1: alur analisis lengkap, dari regresi linear sampai data panel dan GARCH.",
        "Hari 2: praktik terbimbing, latihan mandiri per topik, ditutup proyek mini.",
        "Semua data tersedia lokal di folder data/, tanpa mengambil dari internet.",
        "Setiap notebook sudah diuji dijalankan dari atas ke bawah tanpa error.",
    ],
    "Tekankan bahwa workshop ini bukan pengantar teori, tapi latihan alur kerja. "
    "Teori tetap dibahas singkat di setiap sesi sebagai konteks.")

# Slide 3: peta dua hari
slide_dua_kolom(
    "Peta dua hari",
    "Hari 1: pengajar",
    [
        "00. Persiapan Colab dan padanan EViews",
        "01. Regresi linear dasar",
        "02. Bentuk fungsional",
        "03. Dummy dan uji asumsi klasik",
        "04. Model kategorikal",
        "05. Deret waktu dan ECM",
        "06. Data panel dan GARCH",
    ],
    "Hari 2: mahasiswa",
    [
        "Lab 0. Mulai dari nol",
        "Lab 1. Regresi dan interpretasi",
        "Lab 2. Memilih bentuk model",
        "Lab 3. Dummy dan diagnostik",
        "Lab 4. Logit, ordinal, Poisson",
        "Lab 5. Deret waktu dan panel",
        "Lab 6. Data Indonesia asli",
        "Proyek mini dan rubrik",
    ],
    "Tunjukkan bahwa hari 1 dan hari 2 memakai urutan yang sama, jadi dosen yang "
    "sudah ikut hari 1 bisa langsung membimbing di hari 2.")

# Slide 4: alat
slide_isi(
    "Alat yang dipakai",
    [
        "Google Colab: berjalan di browser, tidak perlu instalasi.",
        "pandas dan numpy: mengolah tabel dan angka.",
        "statsmodels: estimasi, p-value, dan semua uji ekonometrika.",
        "scikit-learn: prediksi, pembagian data, dan metrik klasifikasi.",
        "matplotlib dan seaborn: grafik. linearmodels dan arch: panel dan GARCH.",
    ],
    "Ingatkan bahwa linearmodels dan arch dipasang lewat satu sel %pip install yang "
    "sudah disiapkan di Sesi 6.")

# Slide 5: pembagian tugas pustaka
slide_dua_kolom(
    "statsmodels dan scikit-learn: pembagian tugas",
    "statsmodels",
    [
        "Koefisien, standard error, p-value",
        "Uji asumsi: VIF, Breusch-Pagan, Jarque-Bera",
        "ADF, kointegrasi, ARIMA, panel, GARCH",
        "Semua model ekonometrika di workshop ini",
    ],
    "scikit-learn",
    [
        "Prediksi nilai dan peluang",
        "Pembagian data latih dan uji",
        "Metrik: akurasi, presisi, recall, ROC AUC",
        "Regularisasi otomatis untuk data yang sulit",
    ],
    "Ini slide kunci untuk audiens ilmu komputer. scikit-learn tidak mengeluarkan "
    "p-value, jadi bukan pengganti statsmodels. Keduanya dipakai sesuai porsi. "
    "Contoh berdampingan ada di Sesi 4 dan Lab 4.")

# Slide 6: persiapan data
slide_isi(
    "Persiapan data (5 menit sebelum mulai)",
    [
        "Unduh paket workshop, lalu unggah data-ekonometrika.zip ke panel Files di Colab.",
        "Jalankan sel pertama di notebook: zip diekstrak otomatis ke folder data/.",
        "Semua notebook membaca data lokal, contoh: pd.read_csv(\"data/uts-2.csv\").",
        "Kalau folder data/ kosong, sel pertama akan mengingatkan untuk mengunggah zip.",
    ],
    "Lakukan ini bersama-sama di awal. Minta satu peserta berbagi layar untuk "
    "memastikan langkahnya sama. Kesalahan paling umum di workshop adalah data "
    "belum diunggah.")

# Slide 7-12: ringkasan sesi
slide_isi(
    "Sesi 1: regresi linear",
    [
        "Mulai dari scatter plot, jangan langsung ke tabel.",
        "Baca koefisien sebagai perubahan Y per satu unit X, ceteris paribus.",
        "Uji t untuk satu variabel, uji F untuk model keseluruhan.",
        "Pesan: R kuadrat tinggi bukan bukti model benar atau hubungan kausal.",
    ],
    "Demo alur: lihat data, pasang model, baca summary, prediksi. Tunjukkan juga "
    "kasus model linear yang gagal di hubungan melengkung sebagai jembatan ke Sesi 2.")

slide_isi(
    "Sesi 2: bentuk fungsional",
    [
        "Log-log untuk elastisitas, contoh fungsi produksi Cobb-Douglas.",
        "Reciprocal untuk hubungan yang punya batas atau titik jenuh.",
        "Polinomial untuk pola naik lalu turun, titik puncak dihitung dari koefisien.",
        "Aturan praktis: teori dulu, baru bandingkan R kuadrat pada Y yang sama.",
    ],
    "Pay-off dari Sesi 1: model kuadratik memperbaiki R kuadrat dari 0,007 ke 0,999 "
    "pada data iklan-penjualan. Ini momen yang bagus untuk menunjukkan kenapa "
    "bentuk fungsional penting.")

slide_isi(
    "Sesi 3: dummy dan uji asumsi klasik",
    [
        "Dummy selalu punya kategori basis. Sebut basisnya sebelum menafsirkan.",
        "Multikolinearitas lewat VIF, heteroskedastisitas lewat Breusch-Pagan dan White.",
        "Normalitas lewat Jarque-Bera, autokorelasi lewat Durbin-Watson dan Breusch-Godfrey.",
        "Obat praktis: robust SE untuk heteroskedastisitas, HAC untuk autokorelasi.",
    ],
    "Tekankan urutan: estimasi, uji, perbaiki seperlunya, baru interpretasi. "
    "Ingatkan bahwa robust SE mengubah standard error, bukan koefisien.")

slide_isi(
    "Sesi 4: model kategorikal dan terbatas",
    [
        "Logit dan probit untuk Y 0/1. Baca odds ratio dan efek marjinal, bukan koefisien mentah.",
        "Multinomial untuk kategori tanpa urutan, ordinal untuk kategori berurutan.",
        "Tobit untuk data tersensor, Poisson untuk data hitungan.",
        "Kasus perfect separation dibahas terbuka: kenapa terjadi dan bagaimana menanganinya.",
    ],
    "Ini sesi favorit audiens ilmu komputer karena dekat dengan klasifikasi. "
    "Tunjukkan bahwa efek marjinal menjawab 'berapa poin persen', jauh lebih mudah "
    "dijelaskan daripada log-odds.")

slide_isi(
    "Sesi 5: deret waktu, kointegrasi, dan ECM",
    [
        "Urutan wajib: plot data, uji ADF, selisih kalau perlu, baru model.",
        "ARIMA untuk peramalan, pilih orde dengan AIC plus prinsip parsimoni.",
        "Kointegrasi diperiksa sebelum meregresikan dua variabel yang bertren.",
        "ECM: koefisien koreksi harus negatif dan signifikan. Contoh: 70 persen koreksi per periode.",
    ],
    "Cerita pria mabuk dan anjingnya bagus untuk menjelaskan kointegrasi. Kasus "
    "IHSG-emas di latihan menunjukkan apa yang terjadi kalau ECM dipakai tanpa "
    "kointegrasi: koefisiennya terlihat signifikan tapi menyesatkan.")

slide_isi(
    "Sesi 6: data panel dan GARCH",
    [
        "Panel: pilih CEM, FEM, atau REM lewat uji Chow dan Hausman.",
        "Laporkan p-value mentah Hausman, jangan hanya menulis p < 0,05.",
        "GARCH memodelkan varians: alpha untuk guncangan baru, beta untuk persistensi.",
        "Data simulasi di workshop murni ARCH; simulasi GARCH asli disertakan sebagai pembanding.",
    ],
    "Jujur soal data simulasi: beta jatuh ke nol karena datanya memang ARCH. "
    "Bandingkan dengan simulasi GARCH asli (alpha 0,12 dan beta 0,83) supaya "
    "peserta melihat mesin estimasinya bekerja benar.")

slide_isi(
    "Lab 6: data Indonesia asli",
    [
        "IHSG sejak 1990: GARCH beta 0,82, persistensi 0,99; era krisis 1998 menyentuh IGARCH.",
        "Inflasi bulanan sejak 1968 dan kurs tahunan sejak 1967: krisis 1998 terlihat jelas, inflasi 58 persen dan rupiah melemah 244 persen.",
        "Panel 10 negara ASEAN dari World Bank dan cross-section 34 provinsi dari kompilasi BPS.",
        "Sumber data dan cara memperbaruinya ada di referensi.md dan scripts/fetch_indonesia_data.py.",
    ],
    "Ini slide penutup yang kuat: setelah dua hari memakai data simulasi, peserta "
    "melihat hasil yang sama dengan gaya buku teks pada data asli. Tekankan bahwa "
    "semua data sudah tersedia lokal, dan jalur BPS di referensi.md membuka pintu "
    "untuk data yang lebih baru.")

# Slide 13: alur hari 2
slide_isi(
    "Alur hari 2 dan aturan latihan",
    [
        "Setiap lab berisi contoh terbimbing lalu latihan mandiri di sel kosong.",
        "Kunci lengkap ada di folder kunci/. Pakai setelah mencoba sendiri.",
        "Jawaban tulis di sel komentar, bukan dihapus. Itu bukti pengerjaan.",
        "Target akhir: satu analisis lengkap sampai interpretasi, bukan sekadar kode jalan.",
    ],
    "Keliling kelas saat latihan. Kesalahan paling sering: lupa mengganti nama kolom "
    "di rumus, dan lupa menjalankan sel data sebelum sel model.")

# Slide 14: contoh kode OLS
s = prs.slides.add_slide(BLANK)
kotak(s, 0, 0, 13.333, 7.5, CREAM)
kotak(s, 0, 0, 13.333, 1.15, GREEN)
kotak(s, 0, 1.15, 13.333, 0.06, ACCENT)
teks(s, "Contoh kode: regresi dan prediksi", 0.55, 0.18, 12.2, 0.8, ukuran=28, warna=WHITE, tebal=True)
kotak(s, 0.55, 1.6, 12.2, 2.55, INK)
teks(s, [
    "import statsmodels.formula.api as smf",
    "",
    "saham = pd.read_csv(\"data/uts-2.csv\")",
    "model = smf.ols(\"Y_Harga_Saham ~ X1_Pendapatan_per_Saham\", data=saham).fit()",
    "print(model.summary())",
], 0.8, 1.75, 11.8, 2.3, ukuran=14, warna=CREAM, font=MONO, spasi=1.15)
teks(s, [
    "Koefisien ~10,4: kenaikan EPS satu unit diiringi kenaikan harga saham 10,4 unit.",
    "p-value di bawah 0,05: hubungan itu signifikan secara statistik.",
], 0.65, 4.4, 12.0, 2.0, ukuran=17)
catatan(s, "Ketik ulang kode ini di depan peserta, jangan hanya dibacakan. "
           "Tunjukkan letak koefisien dan p-value di tabel summary.")

# Slide 15: contoh kode logit
s = prs.slides.add_slide(BLANK)
kotak(s, 0, 0, 13.333, 7.5, CREAM)
kotak(s, 0, 0, 13.333, 1.15, GREEN)
kotak(s, 0, 1.15, 13.333, 0.06, ACCENT)
teks(s, "Contoh kode: logit dan efek marjinal", 0.55, 0.18, 12.2, 0.8, ukuran=28, warna=WHITE, tebal=True)
kotak(s, 0.55, 1.6, 12.2, 2.75, INK)
teks(s, [
    "import statsmodels.formula.api as smf",
    "",
    "spector = sm.datasets.spector.load_pandas().data",
    "logit = smf.logit(\"GRADE ~ GPA + TUCE + PSI\", data=spector).fit()",
    "print(logit.get_margeff().summary())",
    "from sklearn.metrics import roc_auc_score  # metrik prediksi",
], 0.8, 1.75, 11.8, 2.5, ukuran=14, warna=CREAM, font=MONO, spasi=1.15)
teks(s, [
    "Efek marjinal PSI ~0,31: peluang nilai meningkat naik sekitar 31 poin persen.",
    "Estimasi dan uji di statsmodels, metrik prediksi di scikit-learn.",
], 0.65, 4.6, 12.0, 2.0, ukuran=17)
catatan(s, "Tunjukkan perbedaan output: statsmodels memberi koefisien dan p-value, "
           "scikit-learn memberi metrik prediksi. Ini memperkuat slide pembagian tugas.")

# Slide 16: kendala umum
slide_dua_kolom(
    "Kendala umum dan solusi cepat",
    "Gejala",
    [
        "Folder data/ kosong di Colab",
        "ModuleNotFoundError linearmodels",
        "Warning perfect separation",
        "Colab terputus di tengah sesi",
    ],
    "Solusi",
    [
        "Unggah data-ekonometrika.zip, jalankan sel pertama",
        "Jalankan sel %pip install linearmodels arch -q",
        "Bukan error; bahan diskusi Sesi 4 soal data terpisah",
        "Unggah ulang data, simpan salinan notebook ke Drive",
    ],
    "Siapkan jawaban ini di ujung lidah. Sebagian besar peserta akan menemui "
    "minimal satu dari empat kendala ini.")

# Slide 17: penutup
s = prs.slides.add_slide(BLANK)
kotak(s, 0, 0, 13.333, 7.5, GREEN)
kotak(s, 0.9, 2.05, 3.2, 0.07, ACCENT)
teks(s, "Satu analisis lengkap", 0.9, 2.3, 11.5, 1.0, ukuran=34, warna=CREAM, tebal=True)
teks(s, [
    "Target workshop: dari pertanyaan, data, model, diagnostik, sampai kesimpulan.",
    "Semua kode sederhana, semua data lokal, semua sudah diuji berjalan.",
], 0.9, 3.4, 11.5, 1.6, ukuran=17, warna=WHITE, spasi=1.2)
teks(s, "Selamat mengajar.", 0.9, 5.6, 11.5, 0.6, ukuran=20, warna=CREAM, tebal=True)
catatan(s, "Tutup dengan mengarahkan peserta ke proyek mini dan rubrik. "
           "Ingatkan bahwa kunci jawaban tersedia, tapi baru dibuka setelah mencoba.")

prs.save(OUT)
print(f"OK: {OUT.name} dengan {len(prs.slides)} slide")
