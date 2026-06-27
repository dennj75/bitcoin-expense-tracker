import sqlite3

# O il percorso esatto del tuo database (es. "beesy.db")
DB_PATH = "database.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Eliminiamo definitivamente la transazione incriminata
cursor.execute("DELETE FROM transazioni WHERE id = 441")
conn.commit()

print(f"Transazioni eliminate: {cursor.rowcount}")
conn.close()
print("Riga 441 eliminata con successo!")