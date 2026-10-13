import os
import sys
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, Preformatted, Image as RLImage
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

sys.stdout.reconfigure(encoding='utf-8')

# ==============================================================================
# DOCX HELPER FUNCTIONS
# ==============================================================================
def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_table_borders(table, color="D3D3D3", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:insideV w:val="none"/>'
        f'  <w:left w:val="none"/>'
        f'  <w:right w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def set_box_borders(cell, color="003366", sz="8"):
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'  <w:top w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:left w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:bottom w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:right w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)

# ==============================================================================
# REPORTLAB NUMBERED CANVAS FOR PDF
# ==============================================================================
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_header_footer(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#003366"))
        
        # Header (Only on pages > 1)
        if self._pageNumber > 1:
            self.drawString(40, 11 * 72 - 32, "Laporan ETS Praktikum PBO — Tipe A: Rental Kendaraan | Ahmad Yasar M. D. (3125522018)")
            self.setStrokeColor(colors.HexColor("#003366"))
            self.setLineWidth(0.5)
            self.line(40, 11 * 72 - 36, 8.5 * 72 - 40, 11 * 72 - 36)
        
        # Footer
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#666666"))
        self.drawString(40, 26, "D3 Teknik Informatika - PENS PSDKU Sumenep (2026) | AutoRent Architecture")
        page_text = f"Halaman {self._pageNumber} dari {page_count}"
        self.drawRightString(8.5 * 72 - 40, 26, page_text)
        self.setStrokeColor(colors.HexColor("#D0D0D0"))
        self.setLineWidth(0.5)
        self.line(40, 36, 8.5 * 72 - 40, 36)
        
        self.restoreState()

# ==============================================================================
# 1. BUILD DOCX REPORT
# ==============================================================================
def generate_docx_report(docx_path, img_path):
    doc = Document()

    # Page Margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Styles
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(10.5)
    normal_style.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(4)

    # Header / Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(2)
    run_t1 = p_title.add_run("LAPORAN RESMI UJIAN TENGAH SEMESTER (ETS)\n")
    run_t1.font.size = Pt(14)
    run_t1.bold = True
    run_t1.font.color.rgb = RGBColor(0x00, 0x33, 0x66)

    run_t2 = p_title.add_run("PRAKTIKUM PEMROGRAMAN BERORIENTASI OBYEK\n")
    run_t2.font.size = Pt(13)
    run_t2.bold = True
    run_t2.font.color.rgb = RGBColor(0x00, 0x55, 0x99)

    run_t3 = p_title.add_run("STUDI KASUS TIPE A: SISTEM RENTAL KENDARAAN (AUTORENT ARCHITECTURE)")
    run_t3.font.size = Pt(11)
    run_t3.bold = True
    run_t3.font.color.rgb = RGBColor(0x44, 0x44, 0x44)

    # Info Box Metadata Mahasiswa
    t_info = doc.add_table(rows=5, cols=2)
    t_info.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_info, color="003366", sz="6", val="single")

    meta_data = [
        ("Nama Mahasiswa", "Ahmad Yasar Maulana Dais"),
        ("Nomor Registrasi Pokok (NRP)", "3125522018"),
        ("Kelas / Program Studi", "3D3PSDKU-SM-IT A / D3 Teknik Informatika"),
        ("Dosen Pengampu", "Nirwana Haidar Hari, S.Pd., M.Kom."),
        ("Institusi & Waktu Pelaksanaan", "PENS Kampus PSDKU Sumenep | Semester Genap 2026/2027")
    ]
    for i, (k, v) in enumerate(meta_data):
        cell_k, cell_v = t_info.cell(i, 0), t_info.cell(i, 1)
        cell_k.text = k
        cell_v.text = v
        cell_k.paragraphs[0].runs[0].bold = True
        cell_k.paragraphs[0].runs[0].font.size = Pt(9.5)
        cell_v.paragraphs[0].runs[0].font.size = Pt(9.5)
        cell_k.width = Inches(2.5)
        cell_v.width = Inches(4.0)
        set_cell_background(cell_k, "F0F4F8")
        set_cell_background(cell_v, "FFFFFF")
        set_cell_margins(cell_k, top=60, bottom=60, left=100, right=100)
        set_cell_margins(cell_v, top=60, bottom=60, left=100, right=100)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # -------------------------------------------------------------
    # BAB I: PENDAHULUAN & ANALISIS MASALAH
    # -------------------------------------------------------------
    h1 = doc.add_heading("BAB I: DESKRIPSI & ANALISIS MASALAH", level=1)
    h1.runs[0].font.color.rgb = RGBColor(0x00, 0x33, 0x66)
    
    p = doc.add_paragraph(
        "Sistem Rental Kendaraan merupakan aplikasi manajemen armada dan transaksi persewaan yang dituntut "
        "memiliki integritas data tinggi, perhitungan biaya fleksibel, serta validasi operasional yang ketat. "
        "Dalam proyek ETS ini, sistem dirancang dengan pendekatan Pemrograman Berorientasi Objek murni yang "
        "memenuhi seluruh rubrik penilaian melalui 9 komponen kelas modular."
    )

    doc.add_heading("Tabel Evaluasi Pemenuhan Rubrik ETS (100% Bobot)", level=2)
    t_rubrik = doc.add_table(rows=7, cols=4)
    t_rubrik.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_rubrik, color="B0C4DE", sz="4", val="single")

    rubrik_headers = ["Komponen Penilaian", "Bobot", "Ketentuan Soal", "Implementasi Nyata"]
    for j, h in enumerate(rubrik_headers):
        c = t_rubrik.cell(0, j)
        c.text = h
        c.paragraphs[0].runs[0].bold = True
        c.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        set_cell_background(c, "003366")
        set_cell_margins(c, top=80, bottom=80, left=100, right=100)

    rubrik_rows = [
        ("Analisis & Class Diagram", "20%", "Arsitektur rapi, modular, UML lengkap", "9 kelas/interface/enum terintegrasi rapi dengan relasi lengkap (PDF & PNG)."),
        ("Encapsulation & Validation", "20%", "Atribut private, min 2 business rules, min 2 relasi", "Semua atribut private; 4 business rules (Unit, Tarif, NIK, Durasi); Relasi Agregasi."),
        ("Inheritance & Abstract Class", "20%", "Min 1 superclass abstract + 2 subclass", "Kendaraan (abstract superclass) diwariskan ke Mobil dan Motor."),
        ("Polymorphism & Interface", "20%", "Min 1 interface, min 1 method overriding kalkulasi", "Interface DapatDisewa; Overriding hitungBiayaSewa() dan hitungDenda() berbeda tiap subclass."),
        ("Program Berjalan & Pengujian", "10%", "Min 3 master data, skenario transaksi & validasi", "Main driver menguji 4 kendaraan, 2 pelanggan, skenario rental, denda, dan 4 test case error."),
        ("Kreativitas Solusi", "10%", "Fitur bisnis orisinal bernilai tambah", "Sistem Loyalty Tier & Auto Upgrade, Diskon Durasi Bertingkat, Struk Nota Monospaced ASCII.")
    ]

    for i, row in enumerate(rubrik_rows, start=1):
        for j, val in enumerate(row):
            c = t_rubrik.cell(i, j)
            c.text = val
            c.paragraphs[0].runs[0].font.size = Pt(9)
            if j == 1:
                c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
                c.paragraphs[0].runs[0].bold = True
            set_cell_background(c, "F8FAFC" if i % 2 == 0 else "FFFFFF")
            set_cell_margins(c, top=60, bottom=60, left=80, right=80)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # -------------------------------------------------------------
    # BAB II: PERANCANGAN CLASS DIAGRAM
    # -------------------------------------------------------------
    h2 = doc.add_heading("BAB II: PERANCANGAN CLASS DIAGRAM & ARSITEKTUR", level=1)
    h2.runs[0].font.color.rgb = RGBColor(0x00, 0x33, 0x66)

    doc.add_paragraph(
        "Arsitektur dirancang menggunakan 9 kelas terpisah guna menjamin Single Responsibility Principle (SRP) "
        "dan Separation of Concerns. Gambar diagram kelas berikut menyajikan struktur inheritance, realization, "
        "dan relasi agregasi:"
    )

    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture(img_path, width=Inches(6.5))
        p_cap = doc.add_paragraph("Gambar 2.1 UML Class Diagram Sistem Rental Kendaraan (AutoRent Architecture)")
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.runs[0].font.size = Pt(9)
        p_cap.runs[0].italic = True

    doc.add_heading("Penjelasan Relasi Antar-Objek", level=2)
    doc.add_paragraph(
        "1. Realization (DapatDisewa <|.. Kendaraan): Kendaraan mengimplementasikan interface DapatDisewa sebagai "
        "kontrak operasional penyewaan dan pengembalian unit.\n"
        "2. Generalization/Inheritance (Kendaraan <|-- Mobil, Kendaraan <|-- Motor): Superclass Kendaraan menurunkan "
        "atribut identitas dan tarif dasar kepada subclass Mobil dan Motor.\n"
        "3. Aggregation (TransaksiRental o-- Pelanggan): Relasi Agregasi menunjukkan Pelanggan dapat eksis mandiri "
        "tanpa terikat siklus hidup transaksi tunggal, sehingga histori dan poin reward pelanggan tetap terpelihara.\n"
        "4. Aggregation (TransaksiRental o-- Kendaraan): Transaksi menghubungkan unit kendaraan yang disewa; unit "
        "dapat disewa berulang kali oleh transaksi berbeda setelah dikembalikan."
    )

    # -------------------------------------------------------------
    # BAB III: IMPLEMENTASI FITUR & KONSEP OOP
    # -------------------------------------------------------------
    h3 = doc.add_heading("BAB III: IMPLEMENTASI KONSEP OOP & LOGIKA BISNIS", level=1)
    h3.runs[0].font.color.rgb = RGBColor(0x00, 0x33, 0x66)

    doc.add_heading("1. Encapsulation & 4 Business Rule Validations", level=2)
    doc.add_paragraph(
        "Seluruh atribut pada setiap kelas dideklarasikan private dan hanya dapat diakses melalui method getter-setter. "
        "Validasi defensif diimplementasikan langsung pada konstruktor dan setter:\n"
        "• Validasi 1 (Tarif Sewa Harian > 0): Mencegah penetapan harga gratis atau bernilai negatif.\n"
        "• Validasi 2 (Ketersediaan Unit): Unit yang sedang berstatus 'SEDANG DISEWA' tidak dapat disewa oleh transaksi lain.\n"
        "• Validasi 3 (Format NIK 16 Digit): NIK pelanggan diverifikasi menggunakan regular expression ^\\d{16}$.\n"
        "• Validasi 4 (Durasi Sewa Minimal): Durasi sewa wajib bernilai minimal 1 hari, input <= 0 memicu ValidationException."
    )

    doc.add_heading("2. Polymorphism: Kalkulasi Biaya dan Denda Berbeda", level=2)
    doc.add_paragraph(
        "Polymorphism diwujudkan melalui overriding abstract method hitungBiayaSewa() dan hitungDenda() pada kelas turunan:\n"
        "• Mobil: Menghitung tarif harian + biaya asuransi all-risk + opsi driver harian (Rp 150.000/hari). "
        "Sewa >= 7 hari mendapatkan diskon paket mingguan mobil 10%. Denda mobil = (150% tarif * hari) + biaya relokasi Rp 50.000.\n"
        "• Motor: Menghitung tarif harian + surcharge pemeliharaan CVT matic (Rp 15.000 flat). "
        "Sewa >= 5 hari mendapatkan diskon komuter motor 5%. Denda motor = 120% tarif * hari telat."
    )

    doc.add_heading("3. Fitur Kreatif Tambahan", level=2)
    doc.add_paragraph(
        "• Customer Loyalty Tier & Auto Upgrade: Pelanggan mendapatkan 1 poin per kelipatan pembayaran Rp 50.000. "
        "Sistem secara dinamis menaikkan tier membership dari Regular -> Gold (>= 100 poin) -> Platinum (>= 300 poin).\n"
        "• Tiered Duration Discount: Diskon durasi panjang otomatis (3-6 hari: 5%, 7-13 hari: 10%, >=14 hari: 15%) "
        "yang diakumulasikan secara bertingkat dengan diskon membership pelanggan.\n"
        "• Professional Monospaced ASCII Receipt: Pencetakan bukti sewa berformat tabel konsol presisi 65 karakter "
        "yang kompatibel di berbagai IDE dan command line tanpa karakter cacat."
    )

    # -------------------------------------------------------------
    # BAB IV: PANDUAN DEMO 3 MENIT
    # -------------------------------------------------------------
    h4 = doc.add_heading("BAB IV: PANDUAN DEMO PRESENTASI 3 MENIT", level=1)
    h4.runs[0].font.color.rgb = RGBColor(0x00, 0x33, 0x66)

    doc.add_paragraph(
        "Poin presentasi terstruktur untuk menjawab 3 pertanyaan kunci dosen saat sesi evaluasi lisan:"
    )

    p_q1 = doc.add_paragraph()
    p_q1.add_run("1. Mengapa saya merancang class seperti ini?\n").bold = True
    p_q1.add_run(
        "\"Arsitektur ini memisahkan tanggung jawab secara modular (Separation of Concerns). "
        "Superclass Kendaraan menyatukan atribut umum armada guna menghindari redundansi kode (DRY principle). "
        "Subclass Mobil dan Motor mengisolasi atribut spesifik masing-masing. Relasi Agregasi dipilih pada "
        "TransaksiRental dan Pelanggan karena pelanggan adalah entitas independen yang histori poinnya "
        "tetap eksis meskipun transaksi telah selesai.\""
    )

    p_q2 = doc.add_paragraph()
    p_q2.add_run("2. Di mana polymorphism terjadi?\n").bold = True
    p_q2.add_run(
        "\"Polymorphism terjadi pada dua titik: pertama, method overriding hitungBiayaSewa() dan hitungDenda() "
        "pada Mobil dan Motor yang menghasilkan rumus kalkulasi dinamis berbeda. Kedua, dynamic dispatch pada "
        "Main.java, di mana seluruh armada disimpan dalam koleksi polymorphic List<Kendaraan> dan JVM secara otomatis "
        "mengeksekusi kalkulasi subclass yang tepat pada runtime tanpa pengecekan instanceof manual.\""
    )

    p_q3 = doc.add_paragraph()
    p_q3.add_run("3. Apa fitur kreatif yang saya tambahkan?\n").bold = True
    p_q3.add_run(
        "\"Tiga fitur orisinal bernilai bisnis: (1) Sistem Tingkat Loyalitas Dinamis dengan perolehan poin transaksi "
        "dan auto-upgrade tier, (2) Kalkulasi Diskon Sewa Otomatis berjenjang untuk sewa jangka panjang, dan "
        "(3) Pencetakan Struk Resmi Monospaced ASCII yang menampilkan transparansi breakdown biaya.\""
    )

    # -------------------------------------------------------------
    # BAB V: KESIMPULAN
    # -------------------------------------------------------------
    h5 = doc.add_heading("BAB V: KESIMPULAN", level=1)
    h5.runs[0].font.color.rgb = RGBColor(0x00, 0x33, 0x66)
    doc.add_paragraph(
        "Program Sistem Rental Kendaraan telah berhasil direalisasikan dan diverifikasi 100% bebas error kompilasi. "
        "Semua prinsip OOP (Class & Object, Encapsulation, Validation, Relationship, Inheritance, Polymorphism, "
        "Abstract Class, dan Interface) terimplementasikan secara komprehensif dan siap dipertanggungjawabkan pada evaluasi ETS PBO."
    )

    doc.save(docx_path)
    print(f"DOCX Report created successfully: {docx_path}")

# ==============================================================================
# 2. BUILD PDF REPORT
# ==============================================================================
def generate_pdf_report(pdf_path, img_path):
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=48,
        bottomMargin=48
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#003366'),
        alignment=1, # Center
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor('#005599'),
        alignment=1,
        spaceAfter=10
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#003366'),
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#005599'),
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#222222'),
        spaceAfter=4
    )

    bullet_style = ParagraphStyle(
        'DocBullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#222222'),
        leftIndent=12,
        spaceAfter=3
    )

    table_header_style = ParagraphStyle(
        'TH',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white,
        alignment=1
    )

    table_cell_style = ParagraphStyle(
        'TC',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor('#222222')
    )

    table_cell_bold = ParagraphStyle(
        'TCB',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor('#003366'),
        alignment=1
    )

    story = []

    # Title Banner
    story.append(Paragraph("LAPORAN RESMI UJIAN TENGAH SEMESTER (ETS) PRAKTIKUM PBO", title_style))
    story.append(Paragraph("STUDI KASUS TIPE A: SISTEM RENTAL KENDARAAN (AUTORENT ARCHITECTURE)", subtitle_style))

    # Meta Table
    meta_data = [
        [Paragraph("<b>Nama Mahasiswa</b>", table_cell_style), Paragraph("Ahmad Yasar Maulana Dais", table_cell_style)],
        [Paragraph("<b>NRP / Kelas</b>", table_cell_style), Paragraph("3125522018 / 3D3PSDKU-SM-IT A (D3 Teknik Informatika)", table_cell_style)],
        [Paragraph("<b>Dosen Pengampu</b>", table_cell_style), Paragraph("Nirwana Haidar Hari, S.Pd., M.Kom.", table_cell_style)],
        [Paragraph("<b>Institusi & Waktu</b>", table_cell_style), Paragraph("PENS Kampus PSDKU Sumenep | Semester Genap 2026/2027", table_cell_style)],
    ]
    t_meta = Table(meta_data, colWidths=[130, 400])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#F0F4F8')),
        ('BACKGROUND', (1,0), (1,-1), colors.white),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#003366')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D0D7DE')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 8))

    # BAB I
    story.append(Paragraph("BAB I: ANALISIS MASALAH & PEMENUHAN RUBRIK PENILAIAN ETS (100%)", h1_style))
    story.append(Paragraph(
        "Sistem Rental Kendaraan (Tipe A) dirancang menggunakan pendekatan Object-Oriented Programming (OOP) "
        "komprehensif untuk mengelola siklus operasional armada dan transaksi pelanggan. Seluruh rubrik penilaian "
        "dipenuhi secara ketat melalui arsitektur 9 berkas program yang saling terintegrasi:",
        body_style
    ))

    rubrik_data = [
        [Paragraph("Komponen Rubrik", table_header_style), Paragraph("Bobot", table_header_style), Paragraph("Persyaratan Minimal Soal", table_header_style), Paragraph("Implementasi pada Sistem AutoRent", table_header_style)],
        [Paragraph("Analisis & Class Diagram", table_cell_style), Paragraph("20%", table_cell_bold), Paragraph("Arsitektur rapi, min. 5 class", table_cell_style), Paragraph("9 kelas/komponen modular, diagram UML lengkap (PDF & PNG).", table_cell_style)],
        [Paragraph("Encapsulation & Validation", table_cell_style), Paragraph("20%", table_cell_bold), Paragraph("Atribut private, min. 2 validasi & 2 relasi", table_cell_style), Paragraph("Semua atribut private; 4 business rules (Unit, Tarif, NIK, Durasi); 2 Agregasi.", table_cell_style)],
        [Paragraph("Inheritance & Abstract Class", table_cell_style), Paragraph("20%", table_cell_bold), Paragraph("Min. 1 abstract class + 2 subclass", table_cell_style), Paragraph("Kendaraan (abstract) diwariskan ke Mobil dan Motor.", table_cell_style)],
        [Paragraph("Polymorphism & Interface", table_cell_style), Paragraph("20%", table_cell_bold), Paragraph("Min. 1 interface + overriding kalkulasi", table_cell_style), Paragraph("Interface DapatDisewa; Overriding hitungBiayaSewa() & hitungDenda().", table_cell_style)],
        [Paragraph("Pengujian & Driver Main", table_cell_style), Paragraph("10%", table_cell_bold), Paragraph("Min. 3 objek master, skenario sewa & validasi", table_cell_style), Paragraph("Main driver menguji 4 kendaraan, 2 pelanggan, 4 test case validasi.", table_cell_style)],
        [Paragraph("Kreativitas Solusi", table_cell_style), Paragraph("10%", table_cell_bold), Paragraph("Fitur orisinal dengan logika bisnis nyata", table_cell_style), Paragraph("Loyalty Tier dinamis, diskon durasi bertingkat, struk ASCII monospaced.", table_cell_style)]
    ]
    t_rub = Table(rubrik_data, colWidths=[110, 40, 160, 220])
    t_rub.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#003366')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#003366')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D0D7DE')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_rub)
    story.append(Spacer(1, 8))

    # BAB II
    story.append(Paragraph("BAB II: PERANCANGAN CLASS DIAGRAM & DEKOMPOSISI KELAS", h1_style))
    story.append(Paragraph(
        "Sistem didekomposisi ke dalam 9 kelas independen guna mematuhi prinsip Single Responsibility (SRP): "
        "<b>DapatDisewa</b> (Interface), <b>TingkatLoyalitas</b> (Enum), <b>ValidationException</b> (Exception), "
        "<b>Kendaraan</b> (Abstract Superclass), <b>Mobil</b> & <b>Motor</b> (Concrete Subclasses), <b>Pelanggan</b> (Entity), "
        "<b>TransaksiRental</b> (Transaction Service), dan <b>Main</b> (Driver Test):",
        body_style
    ))

    if os.path.exists(img_path):
        story.append(RLImage(img_path, width=7.2*inch, height=4.8*inch))
        story.append(Paragraph("<i>Gambar 2.1 Perancangan UML Class Diagram Lengkap Sistem Rental Kendaraan</i>", ParagraphStyle('Cap', parent=body_style, alignment=1, fontSize=7.5)))

    story.append(Spacer(1, 6))

    # BAB III
    story.append(Paragraph("BAB III: IMPLEMENTASI KONSEP OOP & BUSINESS RULES", h1_style))
    story.append(Paragraph("<b>1. Encapsulation & 4 Business Rule Validations:</b>", h2_style))
    story.append(Paragraph("• <b>Validasi Tarif (> 0):</b> Mencegah input tarif bernilai nol atau negatif (setTarifSewaPerHari).", bullet_style))
    story.append(Paragraph("• <b>Validasi Ketersediaan Unit:</b> Mencegah mobil/motor disewa ganda jika status unit false (prosesSewa).", bullet_style))
    story.append(Paragraph("• <b>Validasi NIK 16 Digit:</b> Memastikan identitas penyewa valid menggunakan regex ^\\d{16}$.", bullet_style))
    story.append(Paragraph("• <b>Validasi Durasi Minimal:</b> Durasi sewa minimal harus 1 hari, input <= 0 melempar ValidationException.", bullet_style))

    story.append(Paragraph("<b>2. Polymorphism (Method Overriding & Dynamic Dispatch):</b>", h2_style))
    story.append(Paragraph("• <b>Kalkulasi Biaya Sewa:</b> Subclass Mobil memperhitungkan asuransi harian, biaya driver opsional, dan diskon mingguan 10% (>=7 hari). Subclass Motor memperhitungkan biaya perawatan CVT matic dan diskon commuter 5% (>=5 hari).", bullet_style))
    story.append(Paragraph("• <b>Kalkulasi Denda Keterlambatan:</b> Subclass Mobil menerapkan denda 150% tarif per hari plus biaya reposisi Rp 50.000. Subclass Motor menerapkan denda 120% tarif per hari.", bullet_style))
    story.append(Paragraph("• <b>Polymorphic Collection:</b> Seluruh objek armada disimpan dalam <code>List&lt;Kendaraan&gt;</code> dan dipanggil secara seragam di runtime tanpa pengecekan tipe manual.", bullet_style))

    story.append(Paragraph("<b>3. Fitur Kreatif & Logika Bisnis Orisinal:</b>", h2_style))
    story.append(Paragraph("• <b>Sistem Loyalty Tier Dinamis:</b> Reward poin (1 poin / Rp 50.000) dengan kenaikan otomatis ke GOLD (>= 100 poin) dan PLATINUM (>= 300 poin).", bullet_style))
    story.append(Paragraph("• <b>Diskon Durasi Bertingkat:</b> Potongan otomatis sewa durasi panjang (3-6 hari: 5%, 7-13 hari: 10%, >=14 hari: 15%) yang diakumulasikan dengan diskon member.", bullet_style))
    story.append(Paragraph("• <b>Pencetakan Struk Resmi ASCII:</b> Menghasilkan nota faktur rental monospaced profesional yang rapi di berbagai konsol terminal.", bullet_style))

    story.append(Spacer(1, 6))

    # BAB IV
    story.append(Paragraph("BAB IV: PANDUAN DEMO PRESENTASI 3 MENIT (JAWABAN DOSEN)", h1_style))
    demo_points = [
        ("1. Mengapa merancang class seperti ini?",
         "Arsitektur dirancang modular berdasarkan Separation of Concerns. Superclass Kendaraan menyatukan atribut umum armada untuk mencegah duplikasi kode (DRY principle). Subclass Mobil dan Motor mengisolasi atribut unik masing-masing. Relasi Agregasi diterapkan antara TransaksiRental dan Pelanggan karena pelanggan adalah entitas independen yang histori poinnya tetap tersimpan meskipun transaksi telah selesai."),
        ("2. Di mana polymorphism terjadi?",
         "Polymorphism terjadi pada dua level: pertama, overriding method hitungBiayaSewa() dan hitungDenda() pada Mobil dan Motor yang menghasilkan kalkulasi biaya dan sanksi denda berbeda. Kedua, dynamic dispatch pada perulangan koleksi List<Kendaraan> di Main.java yang mengeksekusi method spesifik masing-masing objek secara dinamis."),
        ("3. Apa fitur kreatif yang ditambahkan?",
         "Tiga fitur bisnis orisinal: (1) Sistem Loyalty Tier dinamis dengan poin reward dan auto-upgrade status keanggotaan, (2) Diskon Durasi Bertingkat otomatis untuk sewa jangka panjang, dan (3) Cetak Struk Resmi Monospaced ASCII yang menampilkan transparansi breakdown biaya.")
    ]
    for q, ans in demo_points:
        story.append(Paragraph(f"<b>{q}</b>", h2_style))
        story.append(Paragraph(f"<i>Jawaban:</i> \"{ans}\"", body_style))

    story.append(Spacer(1, 6))

    # BAB V
    story.append(Paragraph("BAB V: KESIMPULAN", h1_style))
    story.append(Paragraph(
        "Sistem Rental Kendaraan (AutoRent Architecture) telah teruji memenuhi 100% rubrik penilaian ETS Praktikum PBO. "
        "Seluruh berkas siap dijalankan langsung di NetBeans, IntelliJ IDEA, maupun Command Line Terminal.",
        body_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF Report created successfully: {pdf_path}")

if __name__ == "__main__":
    out_dir = r"c:\Semester 3\pemograman berorientasi objek\praktikum\UTS\UTS_3125522018_Ahmad Yasar Maulana Dais"
    uts_parent = r"c:\Semester 3\pemograman berorientasi objek\praktikum\UTS"
    img = os.path.join(out_dir, "class-diagram.png")

    docx_file = os.path.join(out_dir, "Laporan_ETS_Praktikum_PBO_Ahmad_Yasar_Maulana_Dais.docx")
    pdf_file = os.path.join(out_dir, "Laporan_ETS_Praktikum_PBO_Ahmad_Yasar_Maulana_Dais.pdf")

    generate_docx_report(docx_file, img)
    generate_pdf_report(pdf_file, img)

    # Also copy to parent UTS folder for easy access
    import shutil
    shutil.copy2(docx_file, os.path.join(uts_parent, "Laporan_ETS_Praktikum_PBO_Ahmad_Yasar_Maulana_Dais.docx"))
    shutil.copy2(pdf_file, os.path.join(uts_parent, "Laporan_ETS_Praktikum_PBO_Ahmad_Yasar_Maulana_Dais.pdf"))
    print("Reports copied to UTS root folder as well!")
