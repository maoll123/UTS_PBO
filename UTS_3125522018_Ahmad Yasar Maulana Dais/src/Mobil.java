/**
 * Concrete Subclass Mobil yang mewarisi abstract class Kendaraan.
 * Mengimplementasikan overriding method hitungBiayaSewa dan hitungDenda
 * dengan karakteristik khusus kendaraan roda empat.
 *
 * @author Ahmad Yasar Maulana Dais (3125522018)
 */
public class Mobil extends Kendaraan {
    private int kapasitasPenumpang;
    private String tipeMobil; // SUV, MPV, Sedan, dsb.
    private double biayaAsuransiHarian; // Biaya proteksi all-risk harian
    private boolean termasukDriver; // Pilihan fasilitas supir profesional

    public Mobil(String idKendaraan, String nomorPlat, String merk, String model,
                 int tahunProduksi, double tarifSewaPerHari, int kapasitasPenumpang,
                 String tipeMobil, double biayaAsuransiHarian, boolean termasukDriver)
            throws ValidationException {
        super(idKendaraan, nomorPlat, merk, model, tahunProduksi, tarifSewaPerHari);
        setKapasitasPenumpang(kapasitasPenumpang);
        setTipeMobil(tipeMobil);
        setBiayaAsuransiHarian(biayaAsuransiHarian);
        this.termasukDriver = termasukDriver;
    }

    // ==================== GETTER & SETTER TERKONTROL ====================

    public int getKapasitasPenumpang() {
        return kapasitasPenumpang;
    }

    public void setKapasitasPenumpang(int kapasitasPenumpang) throws ValidationException {
        if (kapasitasPenumpang <= 0 || kapasitasPenumpang > 15) {
            throw new ValidationException("[Validasi Mobil] Kapasitas penumpang harus antara 1-15 orang. Input: " + kapasitasPenumpang);
        }
        this.kapasitasPenumpang = kapasitasPenumpang;
    }

    public String getTipeMobil() {
        return tipeMobil;
    }

    public void setTipeMobil(String tipeMobil) throws ValidationException {
        if (tipeMobil == null || tipeMobil.trim().isEmpty()) {
            throw new ValidationException("[Validasi Mobil] Tipe mobil tidak boleh kosong (contoh: SUV, MPV, Sedan).");
        }
        this.tipeMobil = tipeMobil.trim();
    }

    public double getBiayaAsuransiHarian() {
        return biayaAsuransiHarian;
    }

    public void setBiayaAsuransiHarian(double biayaAsuransiHarian) throws ValidationException {
        if (biayaAsuransiHarian < 0) {
            throw new ValidationException("[Validasi Mobil] Biaya asuransi harian tidak boleh negatif!");
        }
        this.biayaAsuransiHarian = biayaAsuransiHarian;
    }

    public boolean isTermasukDriver() {
        return termasukDriver;
    }

    public void setTermasukDriver(boolean termasukDriver) {
        this.termasukDriver = termasukDriver;
    }

    // ==================== POLYMORPHIC METHOD OVERRIDING ====================

    /**
     * Polymorphic Behavior pada Mobil:
     * - Biaya sewa dasar = tarif * hari
     * - Ditambah biaya wajib asuransi per hari
     * - Ditambah layanan supir (Rp 150.000/hari) jika dipilih
     * - Insentif mingguan: jika durasi >= 7 hari, diskon khusus armada mobil 10% dari tarif sewa dasar.
     */
    @Override
    public double hitungBiayaSewa(int durasiHari) {
        if (durasiHari <= 0) return 0.0;

        double sewaDasar = getTarifSewaPerHari() * durasiHari;
        double biayaAsuransi = biayaAsuransiHarian * durasiHari;
        double biayaSupir = termasukDriver ? (150_000.0 * durasiHari) : 0.0;
        double total = sewaDasar + biayaAsuransi + biayaSupir;

        // Diskon khusus paket sewa mingguan mobil
        if (durasiHari >= 7) {
            double potonganPaketMingguan = sewaDasar * 0.10;
            total -= potonganPaketMingguan;
        }

        return total;
    }

    /**
     * Polymorphic Behavior Denda Mobil:
     * Denda = (150% tarif per hari * jumlah hari terlambat) + Biaya Administrasi Relokasi Armada Rp 50.000.
     */
    @Override
    public double hitungDenda(int hariKeterlambatan) {
        if (hariKeterlambatan <= 0) return 0.0;
        double dendaHarian = (getTarifSewaPerHari() * 1.5) * hariKeterlambatan;
        double biayaAdminMobil = 50_000.0;
        return dendaHarian + biayaAdminMobil;
    }

    @Override
    public void tampilkanDetailSpesifikasi() {
        System.out.println("+------------------ SPESIFIKASI MOBIL ------------------+");
        System.out.printf("| ID Kendaraan    : %-36s |%n", getIdKendaraan());
        System.out.printf("| Model / Plat    : %-36s |%n", (getMerk() + " " + getModel() + " (" + getNomorPlat() + ")"));
        System.out.printf("| Tipe / Kursi    : %-36s |%n", (tipeMobil + " (" + kapasitasPenumpang + " Kursi)"));
        System.out.printf("| Tarif Harian    : Rp %-33s |%n", String.format("%,.0f / hari", getTarifSewaPerHari()));
        System.out.printf("| Fasilitas       : %-36s |%n", (String.format("Asuransi Rp %,.0f | %s", biayaAsuransiHarian, (termasukDriver ? "+Driver" : "Lepas Kunci"))));
        System.out.printf("| Status Unit     : %-36s |%n", (isTersedia() ? "TERSEDIA (Ready)" : "SEDANG DISEWA"));
        System.out.println("+-------------------------------------------------------+");
    }
}
