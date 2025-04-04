import sqlite3
from pathlib import Path
from datetime import datetime



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

def actualizar_stock_ingrediente(nombre, nuevo_stock, usuario, observacion=""):
    stock_actual = obtener_stock_ingrediente(nombre)

    conn = sqlite3.connect("db/escandallos.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE Ingredientes SET stock = ? WHERE nombre = ?", (nuevo_stock, nombre))
    conn.commit()
    conn.close()

    # Registrar el movimiento
    registrar_movimiento_stock(nombre, usuario, stock_actual, nuevo_stock, observacion)

def obtener_stock_ingrediente(nombre):
    conn = sqlite3.connect("db/escandallos.db")
    cursor = conn.cursor()
    cursor.execute("SELECT stock FROM Ingredientes WHERE nombre = ?", (nombre,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else 0

def crear_tabla_movimientos_stock():
    conn = sqlite3.connect("db/escandallos.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS MovimientosStock (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ingrediente TEXT,
            usuario TEXT,
            cantidad_anterior REAL,
            cantidad_nueva REAL,
            fecha TEXT,
            observacion TEXT
        )
    """)
    conn.commit()
    conn.close()
    
def registrar_movimiento_stock(ingrediente, usuario, cantidad_anterior, cantidad_nueva, observacion=""):
    conn = sqlite3.connect("db/escandallos.db")
    cursor = conn.cursor()
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO MovimientosStock (ingrediente, usuario, cantidad_anterior, cantidad_nueva, fecha, observacion)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (ingrediente, usuario, cantidad_anterior, cantidad_nueva, fecha, observacion))
    conn.commit()
    conn.close()

