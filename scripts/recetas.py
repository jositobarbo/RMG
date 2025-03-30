import sqlite3
from pathlib import Path

DB_PATH = Path("db/escandallos.db")

def insertar_receta(nombre, margen_objetivo):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO Recetas (nombre, margen_objetivo)
        VALUES (?, ?)
    """, (nombre, margen_objetivo))
    
    conn.commit()
    receta_id = cursor.lastrowid  # ID de la receta recién creada
    conn.close()
    print(f"Receta '{nombre}' creada con ID {receta_id}")
    return receta_id

def asociar_ingrediente_a_receta(receta_id, ingrediente_id, cantidad):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO RecetaIngredientes (receta_id, ingrediente_id, cantidad)
        VALUES (?, ?, ?)
    """, (receta_id, ingrediente_id, cantidad))

    conn.commit()
    conn.close()
    print(f"Ingrediente ID {ingrediente_id} asociado a receta ID {receta_id} con cantidad {cantidad}")

def calcular_precio_receta(receta_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Obtener ingredientes y cantidades de la receta
    cursor.execute("""
        SELECT i.nombre, ri.cantidad, i.coste_unitario
        FROM RecetaIngredientes ri
        JOIN Ingredientes i ON ri.ingrediente_id = i.id
        WHERE ri.receta_id = ?
    """, (receta_id,))
    ingredientes = cursor.fetchall()

    coste_total = 0
    print(f"\n🧾 Ingredientes para receta ID {receta_id}:\n")

    for nombre, cantidad, coste_unitario in ingredientes:
        coste = cantidad * coste_unitario
        print(f"- {nombre}: {cantidad} × {coste_unitario:.2f} € = {coste:.2f} €")
        coste_total += coste

    # Obtener el margen objetivo de la receta
    cursor.execute("""
        SELECT nombre, margen_objetivo
        FROM Recetas
        WHERE id = ?
    """, (receta_id,))
    receta = cursor.fetchone()
    nombre_receta, margen = receta

    precio_sugerido = coste_total / (1 - margen)

    print(f"\n🔍 Coste total: {coste_total:.2f} €")
    print(f"📈 Margen objetivo: {margen*100:.0f}%")
    print(f"💰 Precio sugerido: {precio_sugerido:.2f} €\n")

    conn.close()
    return precio_sugerido

def listar_recetas():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id, nombre FROM Recetas")
    recetas = cursor.fetchall()

    print("\n📋 Recetas registradas:\n")
    for r in recetas:
        print(f"ID: {r[0]} → {r[1]}")

    conn.close()

def obtener_id_receta_por_nombre(nombre_receta):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM Recetas WHERE nombre = ?", (nombre_receta,))
    resultado = cursor.fetchone()

    conn.close()

    if resultado:
        return resultado[0]
    else:
        print(f"❌ Receta '{nombre_receta}' no encontrada.")
        return None

def obtener_escandallo_completo(receta_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT i.nombre, ri.cantidad, i.unidad, i.coste_unitario, (ri.cantidad * i.coste_unitario) AS coste
        FROM RecetaIngredientes ri
        JOIN Ingredientes i ON ri.ingrediente_id = i.id
        WHERE ri.receta_id = ?
    """, (receta_id,))
    ingredientes = cursor.fetchall()

    # Total coste receta
    total_coste = sum([fila[4] for fila in ingredientes])

    # Margen y nombre receta
    cursor.execute("SELECT nombre, margen_objetivo FROM Recetas WHERE id = ?", (receta_id,))
    receta = cursor.fetchone()
    nombre_receta, margen = receta

    conn.close()

    return {
        "receta": nombre_receta,
        "margen": margen,
        "coste_total": total_coste,
        "ingredientes": ingredientes,
        "precio_sugerido": total_coste / (1 - margen) if margen < 1 else 0
    }
