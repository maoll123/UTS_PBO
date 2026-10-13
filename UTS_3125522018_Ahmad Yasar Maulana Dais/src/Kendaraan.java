/**
 * Abstract Superclass Kendaraan yang merepresentasikan armada rental.
 * Mengimplementasikan interface DapatDisewa dan menerapkan prinsip Enkapsulasi,
 * Abstraksi, serta Business Rule Validation.
 *
 * @author Ahmad Yasar Maulana Dais (3125522018)
 */
public abstract class Kendaraan implements DapatDisewa {
    // Encapsulation: atribut utama berakses private
    private String idKendaraan;
    private String nomorPlat;
    private String merk;
    private String model;
    private int tahunProduksi;
    private double tarifSewaPerHari;
    private boolean tersedia;

    /**
     * Constructor lengkap dengan validasi integritas data awal.
     */
    public Kendaraan(String idKendaraan, String nomorPlat, String merk, String model,
                     int tahunProduksi, double tarifSewaPerHari) throws ValidationException {
        setIdKendaraan(idKendaraan);
        setNomorPlat(nomorPlat);
        setMerk(merk);
        setModel(model);
        setTahunProduksi(tahunProduksi);
        setTarifSewaPerHari(tarifSewaPerHari); // Business Rule 1: tarif > 0
        this.tersedia = true; // Status awal unit baru masuk armada selalu tersedia
    }

    // ==================== GETTER & SETTER TERKONTROL ====================

    public String getIdKendaraan() {
        return idKendaraan;
    }

    public void setIdKendaraan(String idKendaraan) throws ValidationException {
        if (idKendaraan == null || idKendaraan.trim().isEmpty()) {
            throw new ValidationException("[Validasi Error] ID Kendaraan tidak boleh kosong!");
        }
        this.idKendaraan = idKendaraan.trim().toUpperCase();
    }

    public String getNomorPlat() {
        return nomorPlat;
    }

    public void setNomorPlat(String nomorPlat) throws ValidationException {
        if (nomorPlat == null || nomorPlat.trim().isEmpty()) {
            throw new ValidationException("[Validasi Error] Nomor plat kendaraan tidak boleh kosong!");
        }
        this.nomorPlat = nomorPlat.trim().toUpperCase();
    }

    public String getMerk() {
        return merk;
    }

    public void setMerk(String merk) throws ValidationException {
        if (merk == null || merk.trim().isEmpty()) {
            throw new ValidationException("[Validasi Error] Merk kendaraan tidak boleh kosong!");
        }
        this.merk = merk.trim();
    }

    public String getModel() {
        return model;
    }

    public void setModel(String model) throws ValidationException {
        if (model == null || model.trim().isEmpty()) {
            throw new ValidationException("[Validasi Error] Model kendaraan tidak boleh kosong!");
        }
        this.model = model.trim();
    }

    public int getTahunProduksi() {
        return tahunProduksi;
    }

    public void setTahunProduksi(int tahunProduksi) throws ValidationException {
        if (tahunProduksi < 2000 || tahunProduksi > 2027) {
            throw new ValidationException("[Validasi Error] Tahun produksi harus antara 2000 hingga 2027. Input: " + tahunProduksi);
        }
        this.tahunProduksi = tahunProduksi;
    }

    public double getTarifSewaPerHari() {
        return tarifSewaPerHari;
    }

    /**
     * Business Rule Validation: Tarif sewa harian harus bernilai positif (> 0).
     */
    public void setTarifSewaPerHari(double tarifSewaPerHari) throws ValidationException {
        if (tarifSewaPerHari <= 0) {
            throw new ValidationException("[Validasi Error] Tarif sewa per hari harus lebih besar dari Rp 0! Input: Rp " + tarifSewaPerHari);
        }
        this.tarifSewaPerHari = tarifSewaPerHari;
    }

    @Override
    public boolean isTersedia() {
        return tersedia;
    }

    protected void setTersedia(boolean tersedia) {
        this.tersedia = tersedia;
    }

    // ==================== IMPLEMENTASI DAPATDISEWA ====================

    /**
     * Business Rule Validation: Memeriksa ketersediaan unit dan durasi sewa sebelum proses sewa.
     */
    @Override
    public void prosesSewa(Pelanggan pelanggan, int durasiHari) throws ValidationException {
        if (!this.tersedia) {
            throw new ValidationException("[Validasi Unit] Unit " + merk + " " + model + " (" + nomorPlat + 
                                           ") saat ini sedang disewa dan TIDAK TERSEDIA!");
        }
        if (durasiHari <= 0) {
            throw new ValidationException("[Validasi Durasi] Durasi sewa minimal harus 1 hari! Input: " + durasiHari);
        }
        this.tersedia = false;
    }

    @Override
    public void prosesPengembalian() {
        this.tersedia = true;
    }

    // ==================== ABSTRACT METHODS (POLYMORPHISM) ====================

    /**
     * Method abstrak yang wajib di-override oleh masing-masing subclass
     * dengan logika kalkulasi biaya yang spesifik.
     */
    @Override
    public abstract double hitungBiayaSewa(int durasiHari);

    /**
     * Method abstrak untuk kalkulasi denda keterlambatan per hari.
     */
    @Override
    public abstract double hitungDenda(int hariKeterlambatan);

    /**
     * Menampilkan spesifikasi lengkap kendaraan secara polymorphic.
     */
    public abstract void tampilkanDetailSpesifikasi();

    @Override
    public String toString() {
        return String.format("[%s] %s %s (%s) | Tarif: Rp %,.0f/hari | Status: %s",
                idKendaraan, merk, model, nomorPlat, tarifSewaPerHari, (tersedia ? "TERSEDIA" : "DISEWA"));
    }
}
