import sqlite3

def agregar_columna_usuario():
    conn = sqlite3.connect("db/escandallos.db")
    cursor = conn.cursor()
    
    try:
        cursor.execute("ALTER TABLE Recetas ADD COLUMN usuario TEXT")
        print("✅ Columna 'usuario' añadida correctamente.")
    except sqlite3.OperationalError:
        print("ℹ️ La columna 'usuario' ya existe.")
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    agregar_columna_usuario()
