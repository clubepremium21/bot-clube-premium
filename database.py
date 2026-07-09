import sqlite3

BANCO = "dados.db"


def conectar():
    return sqlite3.connect(BANCO)


def criar_banco():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        telegram_id INTEGER UNIQUE,

        nome TEXT,

        usuario TEXT,

        plano TEXT,

        status TEXT,

        data_pagamento TEXT,

        vencimento TEXT

    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS comprovantes(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        telegram_id INTEGER,

        file_id TEXT,

        data_envio TEXT,

        status TEXT
    )
    """)

    conn.commit()
    conn.close()


def cadastrar_cliente(telegram_id, nome, usuario):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR IGNORE INTO clientes
    (telegram_id,nome,usuario,status)

    VALUES(?,?,?,?)
    """, (telegram_id, nome, usuario, "NOVO"))

    conn.commit()
    conn.close()


def atualizar_plano(telegram_id, plano):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""

    UPDATE clientes

    SET plano=?

    WHERE telegram_id=?

    """, (plano, telegram_id))

    conn.commit()
    conn.close()


def salvar_comprovante(telegram_id, file_id, data):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO comprovantes

    (telegram_id,file_id,data_envio,status)

    VALUES(?,?,?,?)

    """, (telegram_id, file_id, data, "AGUARDANDO"))

    conn.commit()
    conn.close()


def alterar_status(telegram_id, status):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""

    UPDATE clientes

    SET status=?

    WHERE telegram_id=?

    """, (status, telegram_id))

    conn.commit()
    conn.close()


def buscar_cliente(telegram_id):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""

    SELECT *

    FROM clientes

    WHERE telegram_id=?

    """, (telegram_id,))

    cliente = cursor.fetchone()

    conn.close()

    return cliente


def listar_clientes():

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""

    SELECT *

    FROM clientes

    """)

    clientes = cursor.fetchall()

    conn.close()

    return clientes
