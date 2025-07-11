import os
import sqlite3

from flask import g

DATABASE = os.path.join(os.path.dirname(__file__), "facialpet.db")


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


def init_db():
    with sqlite3.connect(DATABASE) as db:
        db.executescript(
            """
        CREATE TABLE IF NOT EXISTS evento (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT,
            data_inicio TEXT,
            data_fim TEXT
        );
        CREATE TABLE IF NOT EXISTS momento (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            evento_id INTEGER NOT NULL,
            nome TEXT NOT NULL,
            data TEXT,
            periodo TEXT,
            FOREIGN KEY(evento_id) REFERENCES evento(id)
        );
        CREATE TABLE IF NOT EXISTS participante (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            foto TEXT
        );
        CREATE TABLE IF NOT EXISTS evento_participante (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            evento_id INTEGER NOT NULL,
            participante_id INTEGER NOT NULL,
            FOREIGN KEY(evento_id) REFERENCES evento(id),
            FOREIGN KEY(participante_id) REFERENCES participante(id)
        );
        CREATE TABLE IF NOT EXISTS presenca (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            momento_id INTEGER NOT NULL,
            participante_id INTEGER NOT NULL,
            data_hora TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(momento_id) REFERENCES momento(id),
            FOREIGN KEY(participante_id) REFERENCES participante(id)
        );
        """
        )
