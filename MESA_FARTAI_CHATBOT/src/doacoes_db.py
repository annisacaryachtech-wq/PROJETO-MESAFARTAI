import sqlite3
from pathlib import Path

CAMINHO = Path(__file__).resolve().parent.parent / 'mesafartai_ac4.db'

def conectar():
    return sqlite3.connect(CAMINHO)

def iniciar():
    with conectar() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS doacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            alimento TEXT NOT NULL,
            quantidade_kg REAL NOT NULL,
            validade TEXT NOT NULL,
            urgencia TEXT NOT NULL,
            ong_destino TEXT NOT NULL
        )""")

def registrar(alimento, quantidade_kg, validade, urgencia, ong_destino):
    if not alimento or quantidade_kg <= 0 or not ong_destino:
        raise ValueError('Doação inválida')
    with conectar() as conn:
        cursor = conn.execute("""INSERT INTO doacoes
            (alimento, quantidade_kg, validade, urgencia, ong_destino)
            VALUES (?, ?, ?, ?, ?)""", (alimento, quantidade_kg, validade, urgencia, ong_destino))
        conn.commit()
        return cursor.lastrowid

def resumo():
    with conectar() as conn:
        total = conn.execute('SELECT COALESCE(SUM(quantidade_kg), 0) FROM doacoes').fetchone()[0]
        linhas = conn.execute('SELECT id, alimento, quantidade_kg, validade, urgencia, ong_destino FROM doacoes ORDER BY id DESC').fetchall()
    return total, linhas
