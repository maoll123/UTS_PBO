/**
 * Concrete Subclass Motor yang mewarisi abstract class Kendaraan.
 * Mengimplementasikan overriding method hitungBiayaSewa dan hitungDenda
 * dengan karakteristik khusus kendaraan roda dua.
 *
 * @author Ahmad Yasar Maulana Dais (3125522018)
 */
public class Motor extends Kendaraan {
    private int kapasitasMesinCc;
    private String jenisTransmisi; // "Matic" atau "Manual"
    private int jumlahHelm; // Fasilitas helm gratis (default 2)

    public Motor(String idKendaraan, String nomorPlat, String merk, String model,
                 int tahunProduksi, double tarifSewaPerHari, int kapasitasMesinCc,
                 String jenisTransmisi, int jumlahHelm) throws ValidationException {
        super(idKendaraan, nomorPlat, merk, model, tahunProduksi, tarifSewaPerHari);
        setKapasitasMesinCc(kapasitasMesinCc);
        setJenisTransmisi(jenisTransmisi);
        setJumlahHelm(jumlahHelm);
    }

    // ==================== GETTER & SETTER TERKONTROL ====================

    public int getKapasitasMesinCc() {
        return kapasitasMesinCc;
    }

    public void setKapasitasMesinCc(int kapasitasMesinCc) throws ValidationException {
        if (kapasitasMesinCc < 50 || kapasitasMesinCc > 1500) {
            throw new ValidationException("[Validasi Motor] Kapasitas mesin harus antara 50 - 1500 CC. Input: " + kapasitasMesinCc);
        }
        this.kapasitasMesinCc = kapasitasMesinCc;
    }

    public String getJenisTransmisi() {
        return jenisTransmisi;
    }

    public void setJenisTransmisi(String jenisTransmisi) throws ValidationException {
        if (jenisTransmisi == null || (!jenisTransmisi.equalsIgnoreCase("Matic") && !jenisTransmisi.equalsIgnoreCase("Manual"))) {
            throw new ValidationException("[Validasi Motor] Transmisi motor harus 'Matic' atau 'Manual'. Input: " + jenisTransmisi);
        }
        this.jenisTransmisi = jenisTransmisi.substring(0, 1).toUpperCase() + jenisTransmisi.substring(1).toLowerCase();
    }

    public int getJumlahHelm() {
        return jumlahHelm;
    }

    public void setJumlahHelm(int jumlahHelm) throws ValidationException {
        if (jumlahHelm < 1) {
            throw new ValidationException("[Validasi Motor] Fasilitas helm minimal 1 unit untuk keamanan berkendara.");
        }
        this.jumlahHelm = jumlahHelm;
    }

    // ==================== POLYMORPHIC METHOD OVERRIDING ====================

    /**
     * Polymorphic Behavior pada Motor:
     * - Biaya sewa dasar = tarif * hari
     * - Tambahan biaya pemeliharaan berkala CVT Rp 15.000 jika transmisi Matic
     * - Insentif komuter: jika durasi >= 5 hari, diskon komuter motor 5% dari tarif dasar.
     */
    @Override
    public double hitungBiayaSewa(int durasiHari) {
        if (durasiHari <= 0) return 0.0;

        double sewaDasar = getTarifSewaPerHari() * durasiHari;
        double biayaCvtMatic = jenisTransmisi.equalsIgnoreCase("Matic") ? 15_000.0 : 0.0;
        double total = sewaDasar + biayaCvtMatic;

        // Diskon hemat sewa komuter roda dua (>= 5 hari)
        if (durasiHari >= 5) {
            double potonganKomuter = sewaDasar * 0.05;
            total -= potonganKomuter;
        }

        return total;
    }

    /**
     * Polymorphic Behavior Denda Motor:
     * Denda = 120% tarif per hari * jumlah hari terlambat (tanpa biaya administrasi relokasi).
     */
    @Override
    public double hitungDenda(int hariKeterlambatan) {
        if (hariKeterlambatan <= 0) return 0.0;
        return (getTarifSewaPerHari() * 1.20) * hariKeterlambatan;
    }

    @Override
    public void tampilkanDetailSpesifikasi() {
        System.out.println("+------------------ SPESIFIKASI MOTOR ------------------+");
        System.out.printf("| ID Kendaraan    : %-36s |%n", getIdKendaraan());
        System.out.printf("| Model / Plat    : %-36s |%n", (getMerk() + " " + getModel() + " (" + getNomorPlat() + ")"));
        System.out.printf("| Mesin / Trans   : %-36s |%n", (kapasitasMesinCc + " CC | Transmisi " + jenisTransmisi));
        System.out.printf("| Tarif Harian    : Rp %-33s |%n", String.format("%,.0f / hari", getTarifSewaPerHari()));
        System.out.printf("| Fasilitas       : %-36s |%n", ("Termasuk " + jumlahHelm + " Helm SNI + Jas Hujan"));
        System.out.printf("| Status Unit     : %-36s |%n", (isTersedia() ? "TERSEDIA (Ready)" : "SEDANG DISEWA"));
        System.out.println("+-------------------------------------------------------+");
    }
}
