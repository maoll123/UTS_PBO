/**
 * Interface kontrak operasional untuk entitas yang dapat disewakan dalam sistem.
 * Mendefinisikan method standar untuk siklus sewa, pengembalian, status ketersediaan,
 * kalkulasi biaya sewa, dan kalkulasi denda.
 *
 * @author Ahmad Yasar Maulana Dais (3125522018)
 */
public interface DapatDisewa {

    /**
     * Memproses reservasi/sewa unit kepada pelanggan tertentu.
     *
     * @param pelanggan objek penyewa
     * @param durasiHari lama sewa dalam satuan hari
     * @throws ValidationException jika unit tidak tersedia atau parameter tidak valid
     */
    void prosesSewa(Pelanggan pelanggan, int durasiHari) throws ValidationException;

    /**
     * Memproses pengembalian unit agar statusnya kembali tersedia.
     */
    void prosesPengembalian();

    /**
     * Mengecek apakah unit saat ini siap dan tersedia untuk disewa.
     *
     * @return true jika unit tersedia, false jika sedang disewa/perawatan
     */
    boolean isTersedia();

    /**
     * Menghitung total biaya sewa berdasarkan durasi hari (polymorphic).
     *
     * @param durasiHari durasi sewa dalam hari
     * @return total biaya sewa sebelum diskon transaksi
     */
    double hitungBiayaSewa(int durasiHari);

    /**
     * Menghitung denda keterlambatan pengembalian unit (polymorphic).
     *
     * @param hariKeterlambatan jumlah hari lewat batas waktu
     * @return total nominal denda
     */
    double hitungDenda(int hariKeterlambatan);
}
