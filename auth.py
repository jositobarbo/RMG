import sqlite3
import hashlib

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

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def registrar_usuario(username, password):
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    hashed = hash_password(password)
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
    hashed = hash_password(password)
    cursor.execute("SELECT password FROM usuarios WHERE username = ?", (username,))
    data = cursor.fetchone()
    conn.close()
    return data is not None and data[0] == hashed

def obtener_todos_los_usuarios():
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM usuarios")
    usuarios = cursor.fetchall()
    conn.close()
    return [u[0] for u in usuarios]

def cambiar_contrasena(username, nueva_contrasena):
    hashed = hash_password(nueva_contrasena)
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE usuarios SET password = ? WHERE username = ?", (hashed, username))
    conn.commit()
    conn.close()

def eliminar_usuario(username):
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios WHERE username = ?", (username,))
    conn.commit()
    conn.close()
