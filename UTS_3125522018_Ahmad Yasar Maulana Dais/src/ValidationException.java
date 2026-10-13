/**
 * Exception khusus untuk menangani pelanggaran aturan bisnis (business rules)
 * pada sistem rental kendaraan.
 *
 * @author Ahmad Yasar Maulana Dais (3125522018)
 */
public class ValidationException extends Exception {
    public ValidationException(String message) {
        super(message);
    }
}
