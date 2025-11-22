#!/usr/bin/env python3
"""
STEP E: End-to-end test per verificare isolamento dati utente.
Crea 2 utenti, aggiunge transazioni diverse, verifica che ogni utente vede solo le proprie.
"""

import os
import sys
from werkzeug.security import generate_password_hash

# Importa le funzioni dal progetto
from db.db_utils import (
    inizializza_db,
    crea_utente,
    get_user_by_username,
    salva_su_db,
    salva_su_db_lightning,
    salva_su_db_onchain,
    leggi_transazioni_da_db,
    leggi_transazioni_da_db_lightning,
    leggi_transazioni_da_db_onchain,
    elimina_transazione_da_db,
)

def test_multiuser_isolation():
    """Testa l'isolamento dati tra utenti."""
    print("=" * 70)
    print("[STEP E] Test Multi-User Data Isolation")
    print("=" * 70)
    
    # 1. Inizializza DB
    print("\n[1] Inizializzando database...")
    inizializza_db()
    print("[OK] Database inizializzato")
    
    # 2. Crea due utenti
    print("\n[2] Creando utenti...")
    user1_pass = generate_password_hash("password123")
    user2_pass = generate_password_hash("password456")
    
    user1_id = crea_utente("alice", "alice@example.com", user1_pass)
    user2_id = crea_utente("bob", "bob@example.com", user2_pass)
    print(f"[OK] Utente 1 (alice) creato con ID: {user1_id}")
    print(f"[OK] Utente 2 (bob) creato con ID: {user2_id}")
    
    # 3. Aggiungi transazioni EUR per alice
    print("\n[3] Aggiungendo transazioni EUR per alice...")
    salva_su_db(user1_id, "2025-11-01", "Stipendio", "Entrate", "Stipendio", 1500.00, None, None)
    salva_su_db(user1_id, "2025-11-05", "Spesa alimentari", "Alimentari", "Supermercato", 50.00, None, None)
    print(f"[OK] 2 transazioni EUR aggiunte per alice")
    
    # 4. Aggiungi transazioni EUR per bob (diverse)
    print("\n[4] Aggiungendo transazioni EUR per bob...")
    salva_su_db(user2_id, "2025-11-02", "Stipendio", "Entrate", "Stipendio", 2000.00, None, None)
    salva_su_db(user2_id, "2025-11-06", "Affitto", "Abitazione", "Affitto/Mutuo", 800.00, None, None)
    print(f"[OK] 2 transazioni EUR aggiunte per bob")
    
    # 5. Aggiungi transazioni Lightning
    print("\n[5] Aggiungendo transazioni Lightning...")
    salva_su_db_lightning(user1_id, "2025-11-01", "wallet_alice", "Ricevuta sats", "Ricevuta", "Altro", 10000, 5.00, 38900.00)
    salva_su_db_lightning(user2_id, "2025-11-02", "wallet_bob", "Pagamento sats", "Pagamento", "Altro", 5000, 2.50, 38900.00)
    print(f"[OK] Transazioni Lightning aggiunte")
    
    # 6. Aggiungi transazioni On-chain
    print("\n[6] Aggiungendo transazioni On-chain...")
    salva_su_db_onchain(user1_id, "2025-11-01", "alice_address", "BTC ricevuto", "Ricevuta", "Altro", "txid_alice_1", 0.05, 0.0001, 1945.00, 38900.00)
    salva_su_db_onchain(user2_id, "2025-11-02", "bob_address", "BTC inviato", "Pagamento", "Altro", "txid_bob_1", 0.1, 0.0002, 3890.00, 38900.00)
    print(f"[OK] Transazioni On-chain aggiunte")
    
    # 7. VERIFICA: alice legge solo le sue transazioni EUR
    print("\n[7] VERIFICA - alice legge transazioni EUR...")
    alice_eur = leggi_transazioni_da_db(user1_id)
    print(f"   Alice vede {len(alice_eur)} transazioni EUR")
    for t in alice_eur:
        print(f"   - {t[1]} | {t[2]} | EUR {t[5]:.2f}")
    assert len(alice_eur) == 2, f"[FAIL] alice deve avere 2 transazioni, ne ha {len(alice_eur)}"
    assert all(t[5] == 1500.00 or t[5] == 50.00 for t in alice_eur), "[FAIL] Dati alice corrotti"
    print(f"[OK] alice vede solo le sue 2 transazioni EUR")
    
    # 8. VERIFICA: bob legge solo le sue transazioni EUR
    print("\n[8] VERIFICA - bob legge transazioni EUR...")
    bob_eur = leggi_transazioni_da_db(user2_id)
    print(f"   Bob vede {len(bob_eur)} transazioni EUR")
    for t in bob_eur:
        print(f"   - {t[1]} | {t[2]} | EUR {t[5]:.2f}")
    assert len(bob_eur) == 2, f"[FAIL] bob deve avere 2 transazioni, ne ha {len(bob_eur)}"
    assert all(t[5] == 2000.00 or t[5] == 800.00 for t in bob_eur), "[FAIL] Dati bob corrotti"
    print(f"[OK] bob vede solo le sue 2 transazioni EUR")
    
    # 9. VERIFICA: alice legge solo le sue Lightning
    print("\n[9] VERIFICA - alice legge transazioni Lightning...")
    alice_lightning = leggi_transazioni_da_db_lightning(user1_id)
    print(f"   Alice vede {len(alice_lightning)} transazioni Lightning")
    assert len(alice_lightning) == 1, f"[FAIL] alice deve avere 1 tx lightning, ne ha {len(alice_lightning)}"
    assert alice_lightning[0][6] == 10000, "[FAIL] Satoshi di alice non corretti"
    print(f"[OK] alice vede solo la sua 1 transazione Lightning (10000 sats)")
    
    # 10. VERIFICA: bob legge solo le sue Lightning
    print("\n[10] VERIFICA - bob legge transazioni Lightning...")
    bob_lightning = leggi_transazioni_da_db_lightning(user2_id)
    print(f"   Bob vede {len(bob_lightning)} transazioni Lightning")
    assert len(bob_lightning) == 1, f"[FAIL] bob deve avere 1 tx lightning, ne ha {len(bob_lightning)}"
    assert bob_lightning[0][6] == 5000, "[FAIL] Satoshi di bob non corretti"
    print(f"[OK] bob vede solo la sua 1 transazione Lightning (5000 sats)")
    
    # 11. VERIFICA: alice legge solo le sue On-chain
    print("\n[11] VERIFICA - alice legge transazioni On-chain...")
    alice_onchain = leggi_transazioni_da_db_onchain(user1_id)
    print(f"   Alice vede {len(alice_onchain)} transazioni On-chain")
    assert len(alice_onchain) == 1, f"[FAIL] alice deve avere 1 tx onchain, ne ha {len(alice_onchain)}"
    assert alice_onchain[0][7] == 0.05, "[FAIL] BTC di alice non corretti"
    print(f"[OK] alice vede solo la sua 1 transazione On-chain (0.05 BTC)")
    
    # 12. VERIFICA: bob legge solo le sue On-chain
    print("\n[12] VERIFICA - bob legge transazioni On-chain...")
    bob_onchain = leggi_transazioni_da_db_onchain(user2_id)
    print(f"   Bob vede {len(bob_onchain)} transazioni On-chain")
    assert len(bob_onchain) == 1, f"[FAIL] bob deve avere 1 tx onchain, ne ha {len(bob_onchain)}"
    assert bob_onchain[0][7] == 0.1, "[FAIL] BTC di bob non corretti"
    print(f"[OK] bob vede solo la sua 1 transazione On-chain (0.1 BTC)")
    
    # 13. TEST: Prova a eliminare transazione di alice con user_id di bob (deve fallire)
    print("\n[13] TEST SECURITY - bob prova a eliminare transazione di alice...")
    alice_tx_id = alice_eur[0][0]
    try:
        elimina_transazione_da_db(alice_tx_id, user2_id)  # bob prova a cancellare tx di alice
        print("[FAIL] SECURITY BREACH: bob e' riuscito a cancellare transazione di alice!")
        sys.exit(1)
    except PermissionError as e:
        print(f"[OK] Accesso negato (corretto): {e}")
    
    # Verifica che la transazione e' ancora li'
    alice_eur_after = leggi_transazioni_da_db(user1_id)
    assert len(alice_eur_after) == 2, "[FAIL] Transazione alice non dovrebbe essere stata cancellata"
    print(f"[OK] Transazione alice ancora intatta (non eliminata)")
    
    # 14. Elimina correttamente la transazione di alice con user_id di alice
    print("\n[14] TEST - alice elimina correttamente la sua transazione...")
    elimina_transazione_da_db(alice_tx_id, user1_id)
    alice_eur_final = leggi_transazioni_da_db(user1_id)
    assert len(alice_eur_final) == 1, f"[FAIL] alice deve avere 1 tx dopo eliminazione, ne ha {len(alice_eur_final)}"
    print(f"[OK] Transazione alice eliminata correttamente")
    
    print("\n" + "=" * 70)
    print("[PASS] TUTTI I TEST PASSATI - ISOLAMENTO DATI VERIFICATO")
    print("=" * 70)

if __name__ == "__main__":
    # Elimina DB vecchio per partire pulito
    db_path = "transazioni.db"
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"[CLEANUP] Database precedente eliminato")
    
    try:
        test_multiuser_isolation()
    except AssertionError as e:
        print(f"\n[FAIL] TEST FALLITO: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[FAIL] ERRORE: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
