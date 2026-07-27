import sqlite3
import os
from utils.security import decrypt_master_key, encrypt_data, decrypt_data

# Mock di una classe User minimal per si    mulare Flask-Login


class DummyUser:
    def __init__(self, id_user, username, auth_type, encrypted_master_key):
        self.id = id_user
        self.username = username
        self.auth_type = auth_type
        self.encrypted_master_key = encrypted_master_key


def test_sblocco_master_key():
    print("=" * 50)
    print("🔐 TEST DI VERIFICA MASTER KEY & CRITTOGRAFIA")
    print("=" * 50)

    # 1. Chiediamo le credenziali di test da terminale
    username_input = input(
        "Inserisci lo username dell'utente da testare (es. dennj75): ").strip()
    password_input = input(
        f"Inserisci la password di {username_input}: ").strip()

    # 2. Connessione al DB di sviluppo in sola lettura/consultazione
    db_path = os.path.join(os.path.dirname(__file__), 'database_dev.db')
    if not os.path.exists(db_path):
        db_path = 'database.db'  # Fallback se il nome file è diverso

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, username, auth_type, encrypted_master_key FROM users WHERE username = ?", (username_input,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        print(f"❌ Utente '{username_input}' non trovato nel DB ({db_path})!")
        return

    user = DummyUser(
        id_user=row['id'],
        username=row['username'],
        auth_type=row['auth_type'],
        encrypted_master_key=row['encrypted_master_key']
    )

    print(f"\n📊 Dati estratti dal DB per user ID {user.id}:")
    print(f"   - Auth Type: {user.auth_type}")
    print(
        f"   - Encrypted MK: {user.encrypted_master_key[:25]}..." if user.encrypted_master_key else "   - Encrypted MK: NESSUNA (NULL)")

    if not user.encrypted_master_key:
        print("\n⚠️ Questo utente non ha ancora una Master Key salvata nel DB.")
        return

    # 3. Tentativo di Decrittazione Master Key
    print("\n🔑 1. Tentativo di decifrare la Master Key dalla password...")
    master_key_reale = decrypt_master_key(user, password_input)

    if master_key_reale:
        print(f"✅ SUCCESS! Master Key decifrata con successo!")
        print(
            f"   🔑 Key (Base64): {master_key_reale[:15]}... (Lunghezza: {len(master_key_reale)} caratteri)")
    else:
        print("❌ FALLIMENTO: Impossibile decifrare la Master Key. La password o il salt non corrispondono!")
        return

    # 4. Test di Cifratura/Decifratura Dati con la Master Key estratta
    print("\n🧪 2. Test Cifratura/Decifratura con la Master Key estratta...")
    testo_segreto_originale = "Beesy Test Payload: 1000 Satoshi & 50.00 EUR"

    # Cifriamo
    testo_cifrato = encrypt_data(testo_segreto_originale, master_key_reale)
    print(f"   🔒 Testo Cifrato: {testo_cifrato[:30]}...")

    # Decifriamo
    testo_decifrato = decrypt_data(testo_cifrato, master_key_reale)
    print(f"   🔓 Testo Decifrato: '{testo_decifrato}'")

    if testo_decifrato == testo_segreto_originale:
        print("\n🎉 ESITO TOTALE: PERFETTO! La Master Key funziona al 100%!")
    else:
        print("\n⚠️ ERRORE: Il testo decifrato non coincide con quello originale.")


if __name__ == "__main__":
    test_sblocco_master_key()
