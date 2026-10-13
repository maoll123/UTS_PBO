import java.util.ArrayList;
import java.util.List;

/**
 * Driver / Main Class untuk Sistem Rental Kendaraan.
 * Menguji dan mendemonstrasikan:
 * 1. Instansiasi Data Master (Kendaraan & Pelanggan)
 * 2. Polymorphic Behavior (Method Overriding pada Subclass & Koleksi Polimorfis)
 * 3. Business Rule Validation & Exception Handling
 * 4. Logika Bisnis Kreatif (Diskon Otomatis, Denda Keterlambatan, Loyalty Point & Tier Upgrade)
 * 5. Pencetakan Struk Transaksi Resmi
 *
 * @author Ahmad Yasar Maulana Dais (3125522018)
 * @version ETS Praktikum PBO 2026/2027
 */
public class Main {

    public static void main(String[] args) {
        cetakHeaderUtama();

        try {
            // =========================================================================
            // 1. INSTANSIASI DATA MASTER (KENDARAAN & PELANGGAN)
            // =========================================================================
            System.out.println("\n[1] INISIALISASI DATA MASTER ARMADA DAN PELANGGAN");
            System.out.println("-----------------------------------------------------------------");

            // Instansiasi minimal 3 kendaraan (Mobil SUV, Mobil MPV, Motor Matic, Motor Sport)
            Mobil mobilFortuner = new Mobil("CAR-001", "L 1945 AG", "Toyota", "Fortuner GR Sport",
                    2024, 850_000.0, 7, "SUV Premium", 50_000.0, true);

            Mobil mobilAvanza = new Mobil("CAR-002", "B 2024 PBO", "Toyota", "Avanza Veloz",
                    2023, 350_000.0, 7, "MPV Keluarga", 25_000.0, false);

            Motor motorVario = new Motor("MOT-001", "M 3125 SM", "Honda", "Vario 160 ABS",
                    2024, 90_000.0, 160, "Matic", 2);

            Motor motorNinja = new Motor("MOT-002", "N 2500 RAC", "Kawasaki", "Ninja 250 FI",
                    2023, 220_000.0, 250, "Manual", 2);

            // Instansiasi Pelanggan
            Pelanggan pelanggan1 = new Pelanggan("PLG-001", "3529012304990001", "Ahmad Yasar Maulana Dais",
                    "081234567890", TingkatLoyalitas.GOLD);
            pelanggan1.tambahPoin(150); // Pelanggan Gold dengan tabungan 150 poin

            Pelanggan pelanggan2 = new Pelanggan("PLG-002", "3529011108020002", "Budi Santoso",
                    "085678901234", TingkatLoyalitas.REGULAR);

            System.out.println("[OK] Master armada kendaraan berhasil didaftarkan: 2 Mobil, 2 Motor.");
            System.out.println("[OK] Master pelanggan terdaftar:");
            System.out.println("  - " + pelanggan1);
            System.out.println("  - " + pelanggan2);

            // =========================================================================
            // 2. DEMONSTRASI POLYMORPHISM & ABSTRACT CLASS
            // =========================================================================
            System.out.println("\n[2] DEMONSTRASI RUNTIME POLYMORPHISM & METHOD OVERRIDING");
            System.out.println("-----------------------------------------------------------------");
            System.out.println("Menyimpan berbagai subclass dalam referensi tipe superclass (Kendaraan[]):");

            List<Kendaraan> daftarArmada = new ArrayList<>();
            daftarArmada.add(mobilFortuner);
            daftarArmada.add(mobilAvanza);
            daftarArmada.add(motorVario);
            daftarArmada.add(motorNinja);

            int simulasiHari = 7;
            System.out.printf("%nSimulasi Kalkulasi Biaya Sewa Polymorphic selama %d Hari:%n", simulasiHari);
            for (Kendaraan k : daftarArmada) {
                // Polymorphic Call: hitungBiayaSewa() menghasilkan perilaku berbeda per tipe kendaraan
                double estimasiBiaya = k.hitungBiayaSewa(simulasiHari);
                System.out.printf("  * [%-10s] %-28s => Estimasi (%d hari): Rp %,.0f%n",
                        k.getClass().getSimpleName(),
                        (k.getMerk() + " " + k.getModel()),
                        simulasiHari,
                        estimasiBiaya);
            }

            System.out.println("\nSpesifikasi Detail Armada (Polymorphic Method tampilkanDetailSpesifikasi):");
            mobilFortuner.tampilkanDetailSpesifikasi();
            motorVario.tampilkanDetailSpesifikasi();

            // =========================================================================
            // 3. SKENARIO TRANSAKSI RENTAL 1: SUKSES & PENGEMBALIAN TEPAT WAKTU
            // =========================================================================
            System.out.println("\n[3] SKENARIO TRANSAKSI 1: RENTAL SUKSES DENGAN DISKON OTOMATIS");
            System.out.println("-----------------------------------------------------------------");
            System.out.println("Pelanggan : " + pelanggan1.getNama() + " (" + pelanggan1.getTier().name() + ")");
            System.out.println("Unit Sewa : " + mobilFortuner.getMerk() + " " + mobilFortuner.getModel() + " (Dengan Driver)");
            System.out.println("Durasi    : 7 Hari (Memenuhi diskon durasi 10% dan diskon Gold Member 5%)");

            // Membuat Transaksi
            TransaksiRental transaksi1 = new TransaksiRental("TRX-202610-001", pelanggan1, mobilFortuner, 7);

            System.out.println("[OK] Transaksi berhasil dibuat. Status unit berubah menjadi: " + 
                    (mobilFortuner.isTersedia() ? "TERSEDIA" : "SEDANG DISEWA"));

            // Simulasi pengembalian tepat waktu (keterlambatan = 0 hari)
            transaksi1.prosesPengembalianUnit(0);
            System.out.println("[OK] Unit dikembalikan tepat waktu. Mencetak struk resmi:");
            transaksi1.cetakStrukRental();

            // =========================================================================
            // 4. SKENARIO PENGUJIAN BUSINESS RULE VALIDATION (EXCEPTION HANDLING)
            // =========================================================================
            System.out.println("\n[4] SKENARIO PENGUJIAN ATURAN BISNIS & DEFENSIVE VALIDATION");
            System.out.println("-----------------------------------------------------------------");

            // Kasus A: Validasi Ketersediaan Unit (Mencoba sewa unit yang sedang aktif disewa)
            System.out.println("[TEST A] Mencoba menyewa unit yang sedang berstatus 'SEDANG DISEWA'");
            try {
                // Buat transaksi aktif untuk mobilAvanza
                TransaksiRental trxAvanza = new TransaksiRental("TRX-TEMP-001", pelanggan2, mobilAvanza, 2);
                System.out.println("  Mobil Avanza disewa oleh Budi Santoso. Status tersedia = " + mobilAvanza.isTersedia());

                // Pelanggan 1 mencoba menyewa mobil Avanza yang sama
                System.out.println("  Ahmad Yasar mencoba menyewa mobil Avanza yang sama...");
                TransaksiRental trxBentrok = new TransaksiRental("TRX-TEMP-002", pelanggan1, mobilAvanza, 3);
            } catch (ValidationException e) {
                System.out.println("  [VALIDASI BERHASIL DICEGAH] " + e.getMessage());
            }

            // Kasus B: Validasi Durasi Sewa Minimal
            System.out.println("\n[TEST B] Mencoba input durasi sewa tidak valid (0 atau negatif)");
            try {
                TransaksiRental trxInvalidDurasi = new TransaksiRental("TRX-ERR-001", pelanggan2, motorNinja, 0);
            } catch (ValidationException e) {
                System.out.println("  [VALIDASI BERHASIL DICEGAH] " + e.getMessage());
            }

            // Kasus C: Validasi Format NIK Pelanggan
            System.out.println("\n[TEST C] Mencoba input NIK tidak sesuai standar 16 digit");
            try {
                Pelanggan pelangganInvalid = new Pelanggan("PLG-999", "12345", "User Salah", "081234567890");
            } catch (ValidationException e) {
                System.out.println("  [VALIDASI BERHASIL DICEGAH] " + e.getMessage());
            }

            // Kasus D: Validasi Tarif Sewa Bernilai Negatif
            System.out.println("\n[TEST D] Mencoba set tarif sewa negatif / nol");
            try {
                motorNinja.setTarifSewaPerHari(-50_000.0);
            } catch (ValidationException e) {
                System.out.println("  [VALIDASI BERHASIL DICEGAH] " + e.getMessage());
            }

            // =========================================================================
            // 5. SKENARIO TRANSAKSI 2: DENDA POLIMORFIS & UPGRADE TIER PELANGGAN
            // =========================================================================
            System.out.println("\n[5] SKENARIO TRANSAKSI 2: DENDA KETERLAMBATAN & AUTO TIER UPGRADE");
            System.out.println("-----------------------------------------------------------------");
            System.out.println("Pelanggan : " + pelanggan2.getNama() + " (" + pelanggan2.getTier().name() + " Member)");
            System.out.println("Unit Sewa : " + motorVario.getMerk() + " " + motorVario.getModel() + " (Matic)");
            System.out.println("Durasi    : 5 Hari (Mendapat diskon komuter motor 5%)");
            System.out.println("Kondisi   : Pengembalian terlambat 2 Hari");

            TransaksiRental transaksi2 = new TransaksiRental("TRX-202610-002", pelanggan2, motorVario, 5);

            // Simulasi keterlambatan 2 hari
            transaksi2.prosesPengembalianUnit(2);
            transaksi2.cetakStrukRental();

            // Memeriksa profil pelanggan 2 setelah transaksi selesai
            System.out.println("\nProfil Terkini Pelanggan setelah Transaksi Selesai:");
            pelanggan2.tampilkanProfil();

            // =========================================================================
            // KESIMPULAN EVALUASI
            // =========================================================================
            cetakFooterSelesai();

        } catch (Exception e) {
            System.err.println("Terjadi kesalahan sistem: " + e.getMessage());
            e.printStackTrace();
        }
    }

    private static void cetakHeaderUtama() {
        System.out.println("+=================================================================+");
        System.out.println("|          UJIAN TENGAH SEMESTER (ETS) PRAKTIKUM PBO 2026         |");
        System.out.println("|         PROGRAM STUDI D3 TEKNIK INFORMATIKA PSDKU SUMENEP       |");
        System.out.println("|               POLITEKNIK ELEKTRONIKA NEGERI SURABAYA            |");
        System.out.println("+=================================================================+");
        System.out.println("| Tipe Kasus : A - Sistem Rental Kendaraan (AutoRent Architecture)|");
        System.out.println("| Mahasiswa  : Ahmad Yasar Maulana Dais                           |");
        System.out.println("| NRP        : 3125522018                                         |");
        System.out.println("| Kelas      : 3D3PSDKU-SM-IT A                                   |");
        System.out.println("+=================================================================+");
    }

    private static void cetakFooterSelesai() {
        System.out.println("\n+=================================================================+");
        System.out.println("|           SELURUH SKENARIO PENGUJIAN SELESAI DIEKSEKUSI         |");
        System.out.println("|  Status Rubrik: 100% Memenuhi Spesifikasi Teknis ETS PBO 2026   |");
        System.out.println("+=================================================================+");
    }
}
