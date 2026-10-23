from pathlib import Path
import sqlite3


class Database:
    """Responsável pela conexão e pela criação das tabelas do sistema."""

    def __init__(self, db_path="estoque_facil.db"):
        self.db_path = str(Path(db_path))
        self.initialize()

    def connect(self):
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def initialize(self):
        with self.connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS produtos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL COLLATE NOCASE UNIQUE,
                    categoria TEXT NOT NULL,
                    quantidade_atual INTEGER NOT NULL DEFAULT 0
                        CHECK (quantidade_atual >= 0),
                    ativo INTEGER NOT NULL DEFAULT 1
                        CHECK (ativo IN (0, 1))
                );

                CREATE TABLE IF NOT EXISTS movimentacoes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    produto_id INTEGER NOT NULL,
                    tipo TEXT NOT NULL CHECK (tipo IN ('ENTRADA', 'SAIDA')),
                    quantidade INTEGER NOT NULL CHECK (quantidade > 0),
                    data_hora TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    observacao TEXT,
                    FOREIGN KEY (produto_id) REFERENCES produtos(id)
                );
                """
            )
