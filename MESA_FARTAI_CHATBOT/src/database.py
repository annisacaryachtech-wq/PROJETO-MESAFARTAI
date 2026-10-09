import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "mesafartai.db"


def conectar():
    return sqlite3.connect(DB_PATH)


def inicializar_banco():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            tipo TEXT CHECK(tipo IN ('DOADOR', 'ONG')) NOT NULL,
            cep TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            telefone TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS doacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doador_id INTEGER NOT NULL,
            descricao_alimento TEXT NOT NULL,
            quantidade REAL NOT NULL,
            unidade TEXT NOT NULL,
            data_validade TEXT,
            status TEXT DEFAULT 'DISPONIVEL',
            FOREIGN KEY (doador_id) REFERENCES usuarios(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doacao_id INTEGER,
            ong_id INTEGER,
            distancia_km REAL,
            data_match TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (doacao_id) REFERENCES doacoes(id),
            FOREIGN KEY (ong_id) REFERENCES usuarios(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS atendimentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mensagem TEXT NOT NULL,
            intencao TEXT,
            confianca REAL,
            resposta TEXT,
            data_atendimento TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM usuarios")
    quantidade = cursor.fetchone()[0]

    if quantidade == 0:
        dados = [
            ("ONG Prato Quente", "ONG", "06700-000", -23.612, -46.781, "11999990001"),
            ("Abrigo Esperança", "ONG", "06705-000", -23.625, -46.795, "11999990002"),
            ("Supermercado Silva", "DOADOR", "06701-000", -23.615, -46.785, "11999990003"),
            ("Restaurante Sabor", "DOADOR", "06703-000", -23.618, -46.789, "11999990004"),
        ]

        cursor.executemany("""
            INSERT INTO usuarios
            (nome, tipo, cep, latitude, longitude, telefone)
            VALUES (?, ?, ?, ?, ?, ?)
        """, dados)

    conn.commit()
    conn.close()


def listar_ongs():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nome, cep, latitude, longitude, telefone
        FROM usuarios
        WHERE tipo = 'ONG'
    """)

    colunas = ["id", "nome", "cep", "latitude", "longitude", "telefone"]
    resultado = [dict(zip(colunas, linha)) for linha in cursor.fetchall()]

    conn.close()
    return resultado


def listar_doadores():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nome, cep, latitude, longitude, telefone
        FROM usuarios
        WHERE tipo = 'DOADOR'
    """)

    colunas = ["id", "nome", "cep", "latitude", "longitude", "telefone"]
    resultado = [dict(zip(colunas, linha)) for linha in cursor.fetchall()]

    conn.close()
    return resultado


def inserir_doacao(doador_id, alimento, quantidade, unidade, prazo):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO doacoes
        (doador_id, descricao_alimento, quantidade, unidade, data_validade)
        VALUES (?, ?, ?, ?, ?)
    """, (doador_id, alimento, quantidade, unidade, prazo))

    doacao_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return doacao_id


def registrar_match(doacao_id, ong_id, distancia):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO matches (doacao_id, ong_id, distancia_km)
        VALUES (?, ?, ?)
    """, (doacao_id, ong_id, distancia))

    conn.commit()
    conn.close()


def registrar_atendimento(mensagem, intencao, confianca, resposta):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO atendimentos
        (mensagem, intencao, confianca, resposta)
        VALUES (?, ?, ?, ?)
    """, (mensagem, intencao, confianca, resposta))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    inicializar_banco()
    print(f'Banco "{DB_PATH.name}" inicializado com sucesso!')
