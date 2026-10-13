import os
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib import colors

def draw_uml_diagram_png(output_path):
    # High resolution canvas: 2400 x 1700
    width = 2400
    height = 1700
    image = Image.new("RGB", (width, height), color=(248, 250, 252))
    draw = ImageDraw.Draw(image)

    # Use default bitmap font or truetype
    try:
        font_title = ImageFont.truetype("arialbd.ttf", 36)
        font_subtitle = ImageFont.truetype("arial.ttf", 22)
        font_header = ImageFont.truetype("arialbd.ttf", 20)
        font_body = ImageFont.truetype("arial.ttf", 16)
        font_body_bold = ImageFont.truetype("arialbd.ttf", 16)
        font_italic = ImageFont.truetype("ariali.ttf", 16)
    except Exception:
        font_title = font_subtitle = font_header = font_body = font_body_bold = font_italic = ImageFont.load_default()

    # Title Banner
    draw.rectangle([(60, 40), (width - 60, 130)], fill=(30, 41, 59))
    draw.text((80, 52), "UML CLASS DIAGRAM - SISTEM RENTAL KENDARAAN (TIPE A)", fill=(255, 255, 255), font=font_title)
    draw.text((80, 95), "ETS Praktikum PBO | Mahasiswa: Ahmad Yasar Maulana Dais (NRP: 3125522018) | Kelas: 3D3PSDKU-SM-IT A", fill=(203, 213, 225), font=font_subtitle)

    # Helper function to draw a UML Box
    def draw_uml_box(x, y, w, h, stereotype, name, attrs, methods, bg_color=(255, 255, 255), header_bg=(241, 245, 249), stroke_color=(71, 85, 105)):
        # Box shadow
        draw.rectangle([(x + 6, y + 6), (x + w + 6, y + h + 6)], fill=(226, 232, 240))
        # Main Box
        draw.rectangle([(x, y), (x + w, y + h)], fill=bg_color, outline=stroke_color, width=3)
        
        # Header banner
        header_h = 56 if stereotype else 44
        draw.rectangle([(x, y), (x + w, y + header_h)], fill=header_bg, outline=stroke_color, width=2)
        
        # Stereotype & Name
        cur_y = y + 6
        if stereotype:
            draw.text((x + (w // 2) - (draw.textlength(stereotype, font=font_italic) // 2), cur_y), stereotype, fill=(71, 85, 105), font=font_italic)
            cur_y += 20
        draw.text((x + (w // 2) - (draw.textlength(name, font=font_header) // 2), cur_y), name, fill=(15, 23, 42), font=font_header)
        cur_y = y + header_h

        # Attributes section
        cur_y += 8
        for attr in attrs:
            draw.text((x + 14, cur_y), attr, fill=(30, 41, 59), font=font_body)
            cur_y += 22
        
        # Divider line
        cur_y += 6
        draw.line([(x, cur_y), (x + w, cur_y)], fill=stroke_color, width=2)
        cur_y += 8

        # Methods section
        for m in methods:
            draw.text((x + 14, cur_y), m, fill=(30, 41, 59), font=font_body)
            cur_y += 22

    # 1. Interface DapatDisewa
    draw_uml_box(
        x=80, y=170, w=500, h=250,
        stereotype="<<interface>>", name="DapatDisewa",
        attrs=[
            "/* Contract Methods */"
        ],
        methods=[
            "+ prosesSewa(pelanggan, durasiHari): void",
            "+ prosesPengembalian(): void",
            "+ isTersedia(): boolean",
            "+ hitungBiayaSewa(durasiHari): double",
            "+ hitungDenda(hariKeterlambatan): double"
        ],
        header_bg=(224, 242, 254), stroke_color=(2, 132, 199)
    )

    # 2. Enum TingkatLoyalitas
    draw_uml_box(
        x=80, y=470, w=500, h=220,
        stereotype="<<enumeration>>", name="TingkatLoyalitas",
        attrs=[
            "REGULAR (0.00, \"Pelanggan Reguler\")",
            "GOLD (0.05, \"Pelanggan Gold\")",
            "PLATINUM (0.10, \"Pelanggan Platinum\")",
            "- persentaseDiskon: double",
            "- deskripsi: String"
        ],
        methods=[
            "+ getPersentaseDiskon(): double",
            "+ getDeskripsi(): String"
        ],
        header_bg=(254, 243, 199), stroke_color=(217, 119, 6)
    )

    # 3. Custom Exception ValidationException
    draw_uml_box(
        x=80, y=740, w=500, h=140,
        stereotype="<<exception>>", name="ValidationException",
        attrs=[
            "- message: String"
        ],
        methods=[
            "+ ValidationException(message: String)"
        ],
        header_bg=(254, 226, 226), stroke_color=(220, 38, 38)
    )

    # 4. Abstract Superclass Kendaraan
    draw_uml_box(
        x=670, y=170, w=520, h=480,
        stereotype="<<abstract>>", name="Kendaraan",
        attrs=[
            "- idKendaraan: String",
            "- nomorPlat: String",
            "- merk: String",
            "- model: String",
            "- tahunProduksi: int",
            "- tarifSewaPerHari: double",
            "- tersedia: boolean"
        ],
        methods=[
            "+ Kendaraan(id, plat, merk, model, thn, tarif)",
            "+ getIdKendaraan() / setIdKendaraan()",
            "+ getNomorPlat() / setNomorPlat()",
            "+ getTarifSewaPerHari() / setTarifSewaPerHari()",
            "+ prosesSewa(pelanggan, durasi): void",
            "+ prosesPengembalian(): void",
            "+ isTersedia(): boolean",
            "+ {abstract} hitungBiayaSewa(durasi): double",
            "+ {abstract} hitungDenda(hari): double",
            "+ {abstract} tampilkanDetailSpesifikasi(): void"
        ],
        header_bg=(238, 242, 255), stroke_color=(79, 70, 229)
    )

    # 5. Subclass Mobil
    draw_uml_box(
        x=670, y=720, w=520, h=340,
        stereotype="", name="Mobil",
        attrs=[
            "- kapasitasPenumpang: int",
            "- tipeMobil: String",
            "- biayaAsuransiHarian: double",
            "- termasukDriver: boolean"
        ],
        methods=[
            "+ Mobil(..., kapasitas, tipe, asuransi, supir)",
            "+ getKapasitasPenumpang() / setKapasitasPenumpang()",
            "+ getTipeMobil() / setTipeMobil()",
            "+ getBiayaAsuransiHarian() / setBiayaAsuransiHarian()",
            "+ hitungBiayaSewa(durasiHari): double   <<override>>",
            "+ hitungDenda(hariKeterlambatan): double <<override>>",
            "+ tampilkanDetailSpesifikasi(): void    <<override>>"
        ],
        header_bg=(240, 253, 244), stroke_color=(22, 163, 74)
    )

    # 6. Subclass Motor
    draw_uml_box(
        x=670, y=1120, w=520, h=330,
        stereotype="", name="Motor",
        attrs=[
            "- kapasitasMesinCc: int",
            "- jenisTransmisi: String",
            "- jumlahHelm: int"
        ],
        methods=[
            "+ Motor(..., kapasitasCc, transmisi, helm)",
            "+ getKapasitasMesinCc() / setKapasitasMesinCc()",
            "+ getJenisTransmisi() / setJenisTransmisi()",
            "+ getJumlahHelm() / setJumlahHelm()",
            "+ hitungBiayaSewa(durasiHari): double   <<override>>",
            "+ hitungDenda(hariKeterlambatan): double <<override>>",
            "+ tampilkanDetailSpesifikasi(): void    <<override>>"
        ],
        header_bg=(255, 247, 237), stroke_color=(234, 88, 12)
    )

    # 7. Class Pelanggan
    draw_uml_box(
        x=1280, y=170, w=500, h=450,
        stereotype="", name="Pelanggan",
        attrs=[
            "- idPelanggan: String",
            "- nik: String",
            "- nama: String",
            "- nomorTelepon: String",
            "- tier: TingkatLoyalitas",
            "- poinLoyalitas: int",
            "- totalTransaksiSelesai: int"
        ],
        methods=[
            "+ Pelanggan(id, nik, nama, kontak, tier?)",
            "+ getIdPelanggan() / setIdPelanggan()",
            "+ getNik() / setNik()   [Regex 16 Digit]",
            "+ getNomorTelepon() / setNomorTelepon()",
            "+ getTier() / setTier()",
            "+ getPoinLoyalitas(): int",
            "+ tambahPoin(poinBaru: int): void",
            "+ evaluasiKenaikanTier(): void",
            "+ catatPenyelesaianTransaksi(total): void",
            "+ tampilkanProfil(): void"
        ],
        header_bg=(253, 242, 248), stroke_color=(219, 39, 119)
    )

    # 8. Class TransaksiRental
    draw_uml_box(
        x=1280, y=690, w=540, h=510,
        stereotype="", name="TransaksiRental",
        attrs=[
            "- kodeTransaksi: String",
            "- pelanggan: Pelanggan          <<aggregation>>",
            "- kendaraan: Kendaraan          <<aggregation>>",
            "- durasiHari: int",
            "- hariKeterlambatan: int",
            "- statusTransaksi: String",
            "- tanggalTransaksi: String",
            "- biayaSewaDasar: double",
            "- diskonDurasiPanjang: double",
            "- diskonLoyalitas: double",
            "- totalDenda: double",
            "- totalPembayaran: double"
        ],
        methods=[
            "+ TransaksiRental(kode, pelanggan, knd, durasi)",
            "- hitungEstimasiDiskon(): void",
            "+ prosesPengembalianUnit(hariTelat): void",
            "+ getKodeTransaksi() / getStatusTransaksi()",
            "+ getTotalPembayaran(): double",
            "+ cetakStrukRental(): void"
        ],
        header_bg=(245, 243, 255), stroke_color=(124, 58, 237)
    )

    # 9. Class Main Driver
    draw_uml_box(
        x=1880, y=450, w=440, h=300,
        stereotype="<<driver>>", name="Main",
        attrs=[
            "/* Skenario Pengujian Sistem */"
        ],
        methods=[
            "+ {static} main(args: String[]): void",
            "- {static} cetakHeaderUtama(): void",
            "- {static} cetakFooterSelesai(): void"
        ],
        header_bg=(241, 245, 249), stroke_color=(100, 116, 139)
    )

    # ==================== DRAW RELATIONSHIPS ====================
    # Helper to draw arrow
    def draw_line_with_label(p1, p2, label="", dashed=False, color=(71, 85, 105), width=3):
        if dashed:
            # simple dashed
            dx = p2[0] - p1[0]
            dy = p2[1] - p1[1]
            dist = (dx**2 + dy**2)**0.5
            steps = int(dist / 14)
            for i in range(0, steps, 2):
                t1 = i / steps
                t2 = min((i + 1) / steps, 1.0)
                draw.line([(p1[0] + dx * t1, p1[1] + dy * t1), (p1[0] + dx * t2, p1[1] + dy * t2)], fill=color, width=width)
        else:
            draw.line([p1, p2], fill=color, width=width)
        if label:
            mx = (p1[0] + p2[0]) // 2
            my = (p1[1] + p2[1]) // 2 - 14
            draw.text((mx - 20, my), label, fill=color, font=font_body_bold)

    # Relasi 1: DapatDisewa <|.. Kendaraan (Realization)
    draw_line_with_label((580, 270), (670, 270), label="<<realizes>>", dashed=True, color=(2, 132, 199))
    draw.polygon([(670, 270), (655, 260), (655, 280)], fill=(255, 255, 255), outline=(2, 132, 199))

    # Relasi 2: Kendaraan <|-- Mobil (Inheritance)
    draw.line([(930, 650), (930, 720)], fill=(79, 70, 229), width=3)
    draw.polygon([(930, 650), (920, 665), (940, 665)], fill=(255, 255, 255), outline=(79, 70, 229))
    draw.text((945, 675), "<<extends>>", fill=(79, 70, 229), font=font_body_bold)

    # Relasi 3: Kendaraan <|-- Motor (Inheritance)
    draw.line([(930, 1060), (930, 1120)], fill=(79, 70, 229), width=3)
    draw.polygon([(930, 1060), (920, 1075), (940, 1075)], fill=(255, 255, 255), outline=(79, 70, 229))
    draw.text((945, 1080), "<<extends>>", fill=(79, 70, 229), font=font_body_bold)

    # Relasi 4: TransaksiRental o-- Pelanggan (Aggregation)
    draw.line([(1530, 690), (1530, 620)], fill=(219, 39, 119), width=3)
    # Hollow diamond at TransaksiRental side
    draw.polygon([(1530, 690), (1520, 675), (1530, 660), (1540, 675)], fill=(255, 255, 255), outline=(219, 39, 119))
    draw.text((1545, 640), "1..1 has-a", fill=(219, 39, 119), font=font_body_bold)

    # Relasi 5: TransaksiRental o-- Kendaraan (Aggregation / Association)
    draw.line([(1280, 850), (1220, 850), (1220, 420), (1190, 420)], fill=(124, 58, 237), width=3)
    draw.polygon([(1280, 850), (1265, 840), (1250, 850), (1265, 860)], fill=(255, 255, 255), outline=(124, 58, 237))
    draw.text((1225, 630), "1..1 rents", fill=(124, 58, 237), font=font_body_bold)

    # Relasi 6: Pelanggan ..> TingkatLoyalitas (Dependency)
    draw_line_with_label((580, 520), (1280, 520), label="uses enum", dashed=True, color=(217, 119, 6))

    # Relasi 7: Main ..> TransaksiRental (Dependency)
    draw_line_with_label((1880, 620), (1820, 750), label="creates", dashed=True, color=(100, 116, 139))

    # Legend / Key
    draw.rectangle([(80, 1500), (width - 80, 1640)], fill=(241, 245, 249), outline=(148, 163, 184), width=2)
    draw.text((100, 1512), "KETERANGAN NOTASI & PENERAPAN RUBRIK ETS:", fill=(15, 23, 42), font=font_body_bold)
    draw.text((100, 1545), "• Inheritance (20%)   : Superclass Kendaraan diturunkan ke Subclass Mobil & Motor (Relasi Generalisasi).", fill=(30, 41, 59), font=font_body)
    draw.text((100, 1572), "• Polymorphism (20%)  : Overriding hitungBiayaSewa() & hitungDenda() menghasilkan behavior kalkulasi dinamis berbeda.", fill=(30, 41, 59), font=font_body)
    draw.text((100, 1599), "• Encapsulation (20%) : Atribut private, getter-setter terkontrol, serta 4 Business Rule Validations (Unit, Tarif, NIK, Durasi).", fill=(30, 41, 59), font=font_body)
    draw.text((1100, 1545), "• Relasi Objek (20%)  : Agregasi TransaksiRental terhadap Pelanggan (1..1) dan Kendaraan (1..1).", fill=(30, 41, 59), font=font_body)
    draw.text((1100, 1572), "• Abstraction (20%)   : Interface DapatDisewa merealisasikan kontrak operasional ke Kendaraan.", fill=(30, 41, 59), font=font_body)
    draw.text((1100, 1599), "• Kreativitas (10%)   : Diskon durasi berjenjang, poin reward & tier upgrade, denda keterlambatan, struk resmi.", fill=(30, 41, 59), font=font_body)

    image.save(output_path, "PNG", quality=95)
    print(f"PNG generated successfully: {output_path}")

def draw_uml_diagram_pdf(png_path, output_pdf_path):
    c = canvas.Canvas(output_pdf_path, pagesize=landscape(A4))
    a4_w, a4_h = landscape(A4)
    # Fit image to page with margin
    margin = 20
    c.drawImage(png_path, margin, margin, width=a4_w - (2 * margin), height=a4_h - (2 * margin))
    c.save()
    print(f"PDF generated successfully: {output_pdf_path}")

if __name__ == "__main__":
    out_dir = r"c:\Semester 3\pemograman berorientasi objek\praktikum\UTS\UTS_3125522018_Ahmad Yasar Maulana Dais"
    os.makedirs(out_dir, exist_ok=True)
    png_file = os.path.join(out_dir, "class-diagram.png")
    pdf_file = os.path.join(out_dir, "class-diagram.pdf")
    draw_uml_diagram_png(png_file)
    draw_uml_diagram_pdf(png_file, pdf_file)
