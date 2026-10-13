/**
 * Enum untuk mendefinisikan tingkatan loyalitas pelanggan (Customer Loyalty Tier)
 * beserta benefit persentase diskon yang berhak diperoleh.
 *
 * @author Ahmad Yasar Maulana Dais (3125522018)
 */
public enum TingkatLoyalitas {
    REGULAR(0.00, "Pelanggan Reguler"),
    GOLD(0.05, "Pelanggan Gold (Diskon 5%)"),
    PLATINUM(0.10, "Pelanggan Platinum (Diskon 10%)");

    private final double persentaseDiskon;
    private final String deskripsi;

    TingkatLoyalitas(double persentaseDiskon, String deskripsi) {
        this.persentaseDiskon = persentaseDiskon;
        this.deskripsi = deskripsi;
    }

    public double getPersentaseDiskon() {
        return persentaseDiskon;
    }

    public String getDeskripsi() {
        return deskripsi;
    }

    @Override
    public String toString() {
        return name() + " (" + (int)(persentaseDiskon * 100) + "% Diskon)";
    }
}
