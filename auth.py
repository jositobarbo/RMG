import sqlite3
import bcrypt

def crear_tabla_usuarios():
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            username TEXT PRIMARY KEY,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

def registrar_usuario(username, password):
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    try:
        cursor.execute("INSERT INTO usuarios (username, password) VALUES (?, ?)", (username, hashed))
        conn.commit()
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()
    return True

def verificar_usuario(username, password):
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM usuarios WHERE username = ?", (username,))
    data = cursor.fetchone()
    conn.close()
    if data:
        return bcrypt.checkpw(password.encode(), data[0])
    return False
