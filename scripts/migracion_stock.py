import sqlite3

def agregar_columna_stock():
    conn = sqlite3.connect("db/escandallos.db")
    cursor = conn.cursor()

    # Verificamos si la columna ya existe
    cursor.execute("PRAGMA table_info(Ingredientes)")
    columnas = [col[1] for col in cursor.fetchall()]
    
    if "stock" not in columnas:
        cursor.execute("ALTER TABLE Ingredientes ADD COLUMN stock REAL DEFAULT 0")
        conn.commit()
        print("✅ Columna 'stock' añadida correctamente.")
    else:
        print("ℹ️ La columna 'stock' ya existe.")
    
    conn.close()

if __name__ == "__main__":
    agregar_columna_stock()
