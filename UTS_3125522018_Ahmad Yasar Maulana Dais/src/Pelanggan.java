/**
 * Class Pelanggan yang merepresentasikan data master penyewa.
 * Mengimplementasikan Enkapsulasi murni, validasi NIK & kontak,
 * serta sistem klasifikasi loyalitas dinamis (Loyalty Points & Tier System).
 *
 * @author Ahmad Yasar Maulana Dais (3125522018)
 */
public class Pelanggan {
    private String idPelanggan;
    private String nik;
    private String nama;
    private String nomorTelepon;
    private TingkatLoyalitas tier;
    private int poinLoyalitas;
    private int totalTransaksiSelesai;

    public Pelanggan(String idPelanggan, String nik, String nama, String nomorTelepon) throws ValidationException {
        setIdPelanggan(idPelanggan);
        setNik(nik); // Business Rule 3: Validasi NIK 16 digit
        setNama(nama);
        setNomorTelepon(nomorTelepon); // Business Rule: Validasi kontak
        this.tier = TingkatLoyalitas.REGULAR;
        this.poinLoyalitas = 0;
        this.totalTransaksiSelesai = 0;
    }

    public Pelanggan(String idPelanggan, String nik, String nama, String nomorTelepon, TingkatLoyalitas tier)
            throws ValidationException {
        this(idPelanggan, nik, nama, nomorTelepon);
        this.tier = (tier != null) ? tier : TingkatLoyalitas.REGULAR;
    }

    // ==================== GETTER & SETTER TERKONTROL ====================

    public String getIdPelanggan() {
        return idPelanggan;
    }

    public void setIdPelanggan(String idPelanggan) throws ValidationException {
        if (idPelanggan == null || idPelanggan.trim().isEmpty()) {
            throw new ValidationException("[Validasi Pelanggan] ID Pelanggan tidak boleh kosong!");
        }
        this.idPelanggan = idPelanggan.trim().toUpperCase();
    }

    public String getNik() {
        return nik;
    }

    /**
     * Business Rule Validation: NIK harus berupa 16 digit angka resmi KTP.
     */
    public void setNik(String nik) throws ValidationException {
        if (nik == null || !nik.matches("\\d{16}")) {
            throw new ValidationException("[Validasi Identitas] NIK harus tepat 16 digit angka numerik! Input: " + nik);
        }
        this.nik = nik;
    }

    public String getNama() {
        return nama;
    }

    public void setNama(String nama) throws ValidationException {
        if (nama == null || nama.trim().isEmpty()) {
            throw new ValidationException("[Validasi Pelanggan] Nama pelanggan tidak boleh kosong!");
        }
        this.nama = nama.trim();
    }

    public String getNomorTelepon() {
        return nomorTelepon;
    }

    /**
     * Business Rule Validation: Nomor telepon harus berformat angka dengan panjang 10-15 digit.
     */
    public void setNomorTelepon(String nomorTelepon) throws ValidationException {
        if (nomorTelepon == null || !nomorTelepon.matches("\\d{10,15}")) {
            throw new ValidationException("[Validasi Kontak] Nomor telepon harus bernilai angka 10-15 digit! Input: " + nomorTelepon);
        }
        this.nomorTelepon = nomorTelepon;
    }

    public TingkatLoyalitas getTier() {
        return tier;
    }

    public void setTier(TingkatLoyalitas tier) {
        if (tier != null) {
            this.tier = tier;
        }
    }

    public int getPoinLoyalitas() {
        return poinLoyalitas;
    }

    public int getTotalTransaksiSelesai() {
        return totalTransaksiSelesai;
    }

    // ==================== FITUR KREATIF: SISTEM LOYALITAS DINAMIS ====================

    /**
     * Menambahkan poin loyalitas dan mengecek kelayakan upgrade tier pelanggan.
     */
    public void tambahPoin(int poinBaru) {
        if (poinBaru > 0) {
            this.poinLoyalitas += poinBaru;
            evaluasiKenaikanTier();
        }
    }

    /**
     * Evaluasi otomatis kenaikan tingkat loyalitas pelanggan:
     * - PLATINUM : Poin >= 300 atau Transaksi Selesai >= 5
     * - GOLD     : Poin >= 100 atau Transaksi Selesai >= 2
     * - REGULAR  : Default
     */
    public void evaluasiKenaikanTier() {
        TingkatLoyalitas tierLama = this.tier;

        if (this.poinLoyalitas >= 300 || this.totalTransaksiSelesai >= 5) {
            this.tier = TingkatLoyalitas.PLATINUM;
        } else if (this.poinLoyalitas >= 100 || this.totalTransaksiSelesai >= 2) {
            this.tier = TingkatLoyalitas.GOLD;
        }

        if (this.tier != tierLama) {
            System.out.printf("  [LOYALTY UPGRADE] Pelanggan %s berhasil naik level: %s -> %s!%n",
                    this.nama, tierLama.name(), this.tier.name());
        }
    }

    /**
     * Mencatat penyelesaian transaksi rental:
     * Menghitung reward poin (1 poin tiap kelipatan nominal Rp 50.000) dan mengupdate riwayat.
     */
    public void catatPenyelesaianTransaksi(double totalPembayaran) {
        this.totalTransaksiSelesai++;
        int poinDidapat = (int) (totalPembayaran / 50_000.0);
        tambahPoin(poinDidapat);
    }

    public void tampilkanProfil() {
        System.out.println("+------------------ PROFIL PELANGGAN -------------------+");
        System.out.printf("| ID / Nama       : %-37s |%n", (idPelanggan + " - " + nama));
        System.out.printf("| NIK             : %-37s |%n", nik);
        System.out.printf("| No. Kontak      : %-37s |%n", nomorTelepon);
        System.out.printf("| Membership Tier : %-37s |%n", tier.getDeskripsi());
        System.out.printf("| Poin Loyalitas  : %-37s |%n", (poinLoyalitas + " Poin (Total Order: " + totalTransaksiSelesai + ")"));
        System.out.println("+-------------------------------------------------------+");
    }

    @Override
    public String toString() {
        return String.format("[%s] %s (NIK: %s) | Tier: %s | Poin: %d",
                idPelanggan, nama, nik, tier.name(), poinLoyalitas);
    }
}
