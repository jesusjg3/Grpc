import sqlite3
from contextlib import closing

DB_NAME = 'libros.db'

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS libros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                autor TEXT NOT NULL,
                anio_publicacion INTEGER NOT NULL
            )
        ''')

def crear_libro(nombre, autor, anio_publicacion):
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.execute(
            'INSERT INTO libros (nombre, autor, anio_publicacion) VALUES (?, ?, ?)',
            (nombre, autor, anio_publicacion)
        )
        return cur.lastrowid

def obtener_libro(libro_id):
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.execute('SELECT id, nombre, autor, anio_publicacion FROM libros WHERE id = ?', (libro_id,))
        return cur.fetchone()

def actualizar_libro(libro_id, nombre, autor, anio_publicacion):
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.execute(
            'UPDATE libros SET nombre = ?, autor = ?, anio_publicacion = ? WHERE id = ?',
            (nombre, autor, anio_publicacion, libro_id)
        )
        return cur.rowcount

def eliminar_libro(libro_id):
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.execute('DELETE FROM libros WHERE id = ?', (libro_id,))
        return cur.rowcount

def listar_libros():
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.execute('SELECT id, nombre, autor, anio_publicacion FROM libros')
        return cur.fetchall()

# Inicializar la base de datos al importar
init_db()
