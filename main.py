from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from pathlib import Path
import serial
import time
app = FastAPI()

# Permitir peticiones desde tu frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = Path("libros.db")

# Inicializar DB y tabla
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS libros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT,
            autor TEXT,
            contenido TEXT,
            traducido TEXT,
            estado INTEGER
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# --- Endpoints ---

# GET: obtener todos los libros
@app.get("/libros")
def get_libros():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM libros")
    rows = c.fetchall()
    conn.close()
    return [
        {"id": r[0], "titulo": r[1], "autor": r[2], "contenido": r[3], "traducido": r[4], "estado": r[5]}
        for r in rows
    ]

# POST: agregar un libro
@app.post("/libros")
def add_libro(libro: dict):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO libros (titulo, autor, contenido, traducido, estado) VALUES (?, ?, ?, ?, ?)",
        (
            libro.get("titulo"),
            libro.get("autor"),
            libro.get("contenido"),
            libro.get("traducido"),
            libro.get("estado", 1)
        )
    )
    conn.commit()
    libro_id = c.lastrowid
    conn.close()
    return {"success": True, "id": libro_id}

# PUT: actualizar un libro
@app.put("/libros/{libro_id}")
def update_libro(libro_id: int, libro: dict):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """
        UPDATE libros
        SET titulo=?, autor=?, contenido=?, traducido=?, estado=?
        WHERE id=?
        """,
        (
            libro.get("titulo"),
            libro.get("autor"),
            libro.get("contenido"),
            libro.get("traducido"),
            libro.get("estado", 1),
            libro_id,   # <- se usa el id de la URL
        )
    )
    if c.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    conn.commit()
    conn.close()
    return {"success": True}


# DELETE: eliminar un libro
@app.delete("/libros")
def delete_libro(libro: dict):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM libros WHERE id=?", (libro.get("id"),))
    if c.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    conn.commit()
    conn.close()
    return {"success": True}
# GET: obtener un libro por ID
@app.get("/libros/{libro_id}")
def get_libro(libro_id: int):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM libros WHERE id=?", (libro_id,))
    row = c.fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return {
        "id": row[0],
        "titulo": row[1],
        "autor": row[2],
        "contenido": row[3],
        "traducido": row[4],
        "estado": row[5],
    }
# GET: obtener libros traducidos
@app.post("/imprimir")
async def imprimir_bloque(bloque: dict):
    """
    Recibe un bloque de 30 filas, espera 5 segundos y responde.
    """
    print("📥 Recibido bloque:", bloque)

    # Simula tiempo de impresiónhhhh
    time.sleep(5)

    return {"status": "ok", "mensaje": "Bloque impreso correctamente"}

###no moeleses
#otra voz