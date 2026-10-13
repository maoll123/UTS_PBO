import java.text.SimpleDateFormat;
import java.util.Date;

/**
 * Class TransaksiRental yang mengelola proses bisnis penyewaan unit.
 * Menerapkan relasi Antar-Objek (Agregasi Pelanggan dan Kendaraan),
 * kalkulasi diskon otomatis berjenjang, denda keterlambatan polimorfis,
 * serta pencetakan struk transaksi resmi.
 *
 * @author Ahmad Yasar Maulana Dais (3125522018)
 */
public class TransaksiRental {
    private String kodeTransaksi;
    private Pelanggan pelanggan; // Relasi Agregasi ke Pelanggan
    private Kendaraan kendaraan; // Relasi Agregasi/Asosiasi ke Kendaraan
    private int durasiHari;
    private int hariKeterlambatan;
    private String statusTransaksi; // "AKTIF" atau "SELESAI"
    private String tanggalTransaksi;

    // Komponen Finansial
    private double biayaSewaDasar;
    private double diskonDurasiPanjang;
    private double diskonLoyalitas;
    private double totalDenda;
    private double totalPembayaran;

    /**
     * Constructor pembuatan transaksi baru.
     * Menerapkan validasi bisnis dan inisialisasi status sewa unit.
     */
    public TransaksiRental(String kodeTransaksi, Pelanggan pelanggan, Kendaraan kendaraan, int durasiHari)
            throws ValidationException {
        if (kodeTransaksi == null || kodeTransaksi.trim().isEmpty()) {
            throw new ValidationException("[Validasi Transaksi] Kode transaksi tidak boleh kosong!");
        }
        if (pelanggan == null) {
            throw new ValidationException("[Validasi Transaksi] Data pelanggan tidak boleh null!");
        }
        if (kendaraan == null) {
            throw new ValidationException("[Validasi Transaksi] Data kendaraan tidak boleh null!");
        }
        if (durasiHari <= 0) {
            throw new ValidationException("[Validasi Transaksi] Durasi sewa minimal adalah 1 hari! Input: " + durasiHari);
        }

        // Panggil proses sewa pada kendaraan (memeriksa ketersediaan unit dan mengubah status)
        kendaraan.prosesSewa(pelanggan, durasiHari);

        this.kodeTransaksi = kodeTransaksi.trim().toUpperCase();
        this.pelanggan = pelanggan;
        this.kendaraan = kendaraan;
        this.durasiHari = durasiHari;
        this.hariKeterlambatan = 0;
        this.statusTransaksi = "AKTIF";
        this.tanggalTransaksi = new SimpleDateFormat("dd-MM-yyyy HH:mm").format(new Date());

        // Hitung estimasi biaya dasar awal via Polymorphic Call
        this.biayaSewaDasar = kendaraan.hitungBiayaSewa(durasiHari);
        hitungEstimasiDiskon();
        this.totalDenda = 0.0;
        this.totalPembayaran = (biayaSewaDasar - diskonDurasiPanjang - diskonLoyalitas);
    }

    // ==================== LOGIKA KALKULASI DISKON OTOMATIS ====================

    /**
     * Fitur Kreatif: Kalkulasi diskon otomatis berjenjang
     * - Diskon durasi sewa panjang:
     *   >= 14 hari : 15% dari biaya sewa dasar
     *   >= 7 hari  : 10% dari biaya sewa dasar
     *   >= 3 hari  : 5% dari biaya sewa dasar
     * - Diskon loyalitas pelanggan berdasarkan Membership Tier (Regular: 0%, Gold: 5%, Platinum: 10%)
     */
    private void hitungEstimasiDiskon() {
        if (durasiHari >= 14) {
            this.diskonDurasiPanjang = this.biayaSewaDasar * 0.15;
        } else if (durasiHari >= 7) {
            this.diskonDurasiPanjang = this.biayaSewaDasar * 0.10;
        } else if (durasiHari >= 3) {
            this.diskonDurasiPanjang = this.biayaSewaDasar * 0.05;
        } else {
            this.diskonDurasiPanjang = 0.0;
        }

        // Diskon loyalitas dihitung setelah potongan durasi
        double dasarSetelahDiskonDurasi = this.biayaSewaDasar - this.diskonDurasiPanjang;
        this.diskonLoyalitas = dasarSetelahDiskonDurasi * pelanggan.getTier().getPersentaseDiskon();
    }

    // ==================== PROSES PENGEMBALIAN & DENDA ====================

    /**
     * Menyelesaikan transaksi saat kendaraan dikembalikan.
     * Menghitung denda keterlambatan secara polimorfis dan menambahkan reward loyalitas ke pelanggan.
     */
    public void prosesPengembalianUnit(int hariKeterlambatan) throws ValidationException {
        if (!"AKTIF".equalsIgnoreCase(this.statusTransaksi)) {
            throw new ValidationException("[Validasi Transaksi] Transaksi " + kodeTransaksi + " sudah ditutup sebelumnya!");
        }
        if (hariKeterlambatan < 0) {
            throw new ValidationException("[Validasi Transaksi] Jumlah hari keterlambatan tidak boleh bernilai negatif!");
        }

        this.hariKeterlambatan = hariKeterlambatan;

        // Mengembalikan status unit kendaraan menjadi tersedia
        kendaraan.prosesPengembalian();

        // Polymorphic Call: Kalkulasi denda berbeda antara Mobil dan Motor
        this.totalDenda = kendaraan.hitungDenda(hariKeterlambatan);

        // Total akhir = (Biaya Dasar - Diskon) + Denda
        this.totalPembayaran = (biayaSewaDasar - diskonDurasiPanjang - diskonLoyalitas) + totalDenda;

        // Memberikan reward poin loyalitas dan potensi upgrade level pelanggan
        pelanggan.catatPenyelesaianTransaksi(this.totalPembayaran);

        this.statusTransaksi = "SELESAI";
    }

    // ==================== GETTER ====================

    public String getKodeTransaksi() {
        return kodeTransaksi;
    }

    public Pelanggan getPelanggan() {
        return pelanggan;
    }

    public Kendaraan getKendaraan() {
        return kendaraan;
    }

    public int getDurasiHari() {
        return durasiHari;
    }

    public int getHariKeterlambatan() {
        return hariKeterlambatan;
    }

    public String getStatusTransaksi() {
        return statusTransaksi;
    }

    public double getBiayaSewaDasar() {
        return biayaSewaDasar;
    }

    public double getDiskonDurasiPanjang() {
        return diskonDurasiPanjang;
    }

    public double getDiskonLoyalitas() {
        return diskonLoyalitas;
    }

    public double getTotalDenda() {
        return totalDenda;
    }

    public double getTotalPembayaran() {
        return totalPembayaran;
    }

    // ==================== FITUR KREATIF: PENCETAKAN STRUK RESMI ====================

    /**
     * Mencetak struk bukti transaksi rental resmi dengan format profesional.
     */
    public void cetakStrukRental() {
        System.out.println("+===============================================================+");
        System.out.println("|                STRUK RESMI RENTAL KENDARAAN                   |");
        System.out.println("|               PENS AUTO RENTAL - ETS PBO 2026                 |");
        System.out.println("+===============================================================+");
        System.out.printf("| No. Transaksi        : %-38s |%n", kodeTransaksi);
        System.out.printf("| Waktu Transaksi      : %-38s |%n", tanggalTransaksi);
        System.out.printf("| Status Transaksi     : %-38s |%n", statusTransaksi);
        System.out.println("+---------------------------------------------------------------+");
        System.out.println("| [DATA PENYEWA]                                                |");
        System.out.printf("| ID & Nama Pelanggan  : %-38s |%n", (pelanggan.getIdPelanggan() + " / " + pelanggan.getNama()));
        System.out.printf("| NIK Identitas        : %-38s |%n", pelanggan.getNik());
        System.out.printf("| Nomor Kontak         : %-38s |%n", pelanggan.getNomorTelepon());
        System.out.printf("| Tingkat Membership   : %-38s |%n", pelanggan.getTier().getDeskripsi());
        System.out.println("+---------------------------------------------------------------+");
        System.out.println("| [DETAIL ARMADA KENDARAAN]                                     |");
        System.out.printf("| Kendaraan            : %-38s |%n", (kendaraan.getMerk() + " " + kendaraan.getModel() + " (" + kendaraan.getNomorPlat() + ")"));
        System.out.printf("| Jenis Armada         : %-38s |%n", ("Kendaraan " + kendaraan.getClass().getSimpleName()));
        System.out.printf("| Tarif Sewa Harian    : Rp %-35s |%n", String.format("%,.0f / hari", kendaraan.getTarifSewaPerHari()));
        System.out.printf("| Durasi Sewa          : %-38s |%n", (durasiHari + " Hari"));
        System.out.println("+---------------------------------------------------------------+");
        System.out.println("| [RINCIAN BIAYA & PEMBAYARAN]                                  |");
        System.out.printf("| Subtotal Sewa Dasar  : Rp %-35s |%n", String.format("%,12.0f", biayaSewaDasar));
        System.out.printf("| Diskon Durasi Sewa   : (Rp %-34s |%n", String.format("%,11.0f)", diskonDurasiPanjang));
        System.out.printf("| Diskon Loyalty Tier  : (Rp %-34s |%n", String.format("%,11.0f)", diskonLoyalitas));
        if (hariKeterlambatan > 0) {
            System.out.printf("| Denda Keterlambatan  : Rp %-35s |%n", String.format("%,12.0f (%d Hari Telat)", totalDenda, hariKeterlambatan));
        } else {
            System.out.printf("| Denda Keterlambatan  : Rp %-35s |%n", "           0 (Tepat Waktu)");
        }
        System.out.println("+---------------------------------------------------------------+");
        System.out.printf("| TOTAL PEMBAYARAN     : Rp %-35s |%n", String.format("%,12.0f", totalPembayaran));
        System.out.printf("| Poin Diperoleh (TRX) : +%-37s |%n", ((int)(totalPembayaran / 50_000.0) + " Poin Loyalitas"));
        System.out.printf("| Akumulasi Poin Member: %-38s |%n", (pelanggan.getPoinLoyalitas() + " Poin (Tier: " + pelanggan.getTier().name() + ")"));
        System.out.println("+===============================================================+");
    }
}
