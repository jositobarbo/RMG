import sqlite3
from pathlib import Path

DB_PATH = Path("db/escandallos.db")

def insertar_ingrediente(nombre, unidad, coste_unitario):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO Ingredientes (nombre, unidad, coste_unitario)
        VALUES (?, ?, ?)
    """, (nombre, unidad, coste_unitario))
    
    conn.commit()
    conn.close()
    print(f"Ingrediente '{nombre}' añadido correctamente.")

def actualizar_precio_ingrediente(nombre_ingrediente, nuevo_precio):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE Ingredientes
        SET coste_unitario = ?
        WHERE nombre = ?
    """, (nuevo_precio, nombre_ingrediente))

    if cursor.rowcount == 0:
        print(f"❌ Ingrediente '{nombre_ingrediente}' no encontrado.")
    else:
        print(f"🔄 Precio del ingrediente '{nombre_ingrediente}' actualizado a {nuevo_precio:.2f} €")

    conn.commit()
    conn.close()

