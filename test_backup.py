import json
import os
import sqlite3
from utils.security import decrypt_master_key, decrypt_data


class DummyUser:
    def __init__(self, id_user, username, auth_type, encrypted_master_key):
        self.id = id_user
        self.username = username
        self.auth_type = auth_type
        self.encrypted_master_key = encrypted_master_key


def test_decripta_backup():
    print("=" * 60)
    print("📦 TEST DECRIPTAZIONE FILE DI BACKUP REALE")
    print("=" * 60)

    # 1. Chiediamo il percorso del file scaricato
    file_path = input(
        "\n1️⃣ Trascina qui il file di backup scaricato (o scrivi il percorso): ").strip().strip("'\"")

    if not os.path.exists(file_path):
        print(f"❌ File non trovato: {file_path}")
        return

    # 2. Chiediamo le credenziali
    username_input = input(
        "2️⃣ Inserisci lo username dell'utente del backup: ").strip()
    password_input = input(
        f"3️⃣ Inserisci la password (o firma) di {username_input}: ").strip()

    # 3. Leggiamo il DB per recuperare la Master Key cifrata dell'utente
    db_path = os.path.join(os.path.dirname(__file__), 'database_dev.db')
    if not os.path.exists(db_path):
        db_path = 'database.db'

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, username, auth_type, encrypted_master_key FROM users WHERE username = ?", (username_input,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        print(f"❌ Utente '{username_input}' non trovato nel database!")
        return

    user = DummyUser(
        id_user=row['id'],
        username=row['username'],
        auth_type=row['auth_type'],
        encrypted_master_key=row['encrypted_master_key']
    )

    # 4. Sblocchiamo la Master Key
    print("\n🔑 Recupero e sblocco della Master Key...")
    master_key = decrypt_master_key(user, password_input)

    if not master_key:
        print("❌ Impossibile sbloccare la Master Key. Password o utente errati!")
        return

    print("✅ Master Key sbloccata con successo!")

    # 5. Leggiamo il contenuto del file di backup
    with open(file_path, 'r', encoding='utf-8') as f:
        contenuto_file = f.read().strip()

    print("\n🔓 Tentativo di decifratura del backup...")

    # Verifichiamo se il file è un JSON cifrato o testo grezzo cifrato
    testo_da_decifrare = contenuto_file
    try:
        # Se il backup ha una struttura JSON con campo 'data' o 'payload'
        json_parsed = json.loads(contenuto_file)
        if isinstance(json_parsed, dict) and 'data' in json_parsed:
            testo_da_decifrare = json_parsed['data']
        elif isinstance(json_parsed, dict) and 'payload' in json_parsed:
            testo_da_decifrare = json_parsed['payload']
    except json.JSONDecodeError:
        pass  # Il file è direttamente la stringa cifrata Fernet

    # Decifriamo con la Master Key
    dati_decifrati = decrypt_data(testo_da_decifrare, master_key)

    if dati_decifrati:
        print("\n🎉 SUCCESS! Il file di backup è stato DECRITTATO con successo!")
        print("=" * 60)
        print("📄 ANTEPRIMA DEI DATI REALI CONTENUTI NEL BACKUP:")
        print("=" * 60)

        try:
            # Se i dati decifrati sono un JSON, stampiamoli belli formattati
            struttura_json = json.loads(dati_decifrati)
            print(json.dumps(struttura_json, indent=4,
                  ensure_ascii=False)[:1000])
            if len(dati_decifrati) > 1000:
                print("\n... [Contenuto troncato per leggibilità] ...")
        except json.JSONDecodeError:
            print(dati_decifrati[:1000])

        print("\n✅ Il sistema di ripristino/backup di Beesy è SOLIDO e VERIFICATO!")
    else:
        print("❌ ERRORE: La Master Key sbloccata non è riuscita a decifrare questo file.")
        print("   Possibili cause: il backup è stato creato con un'altra chiave o il file è corrotto.")


if __name__ == "__main__":
    test_decripta_backup()
