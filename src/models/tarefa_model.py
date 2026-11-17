import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DB = os.path.join(BASE_DIR, "..", "tarefas.db")


class TarefaModel:
    def __init__(self, db_path=DEFAULT_DB):
        self.db_path = db_path
        self._criar_tabela()

    def _conectar(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _criar_tabela(self):
        with self._conectar() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS tarefas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL,
                    disciplina TEXT NOT NULL,
                    descricao TEXT,
                    data_entrega TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'Pendente'
                )
            """)

    def criar(self, titulo, disciplina, descricao, data_entrega):
        with self._conectar() as conn:
            conn.execute(
                "INSERT INTO tarefas (titulo, disciplina, descricao, data_entrega) VALUES (?, ?, ?, ?)",
                (titulo.strip(), disciplina.strip(), descricao.strip(), data_entrega),
            )

    def listar(self, filtro_status="Todos"):
        with self._conectar() as conn:
            if filtro_status in ("Pendente", "Concluída"):
                cursor = conn.execute(
                    "SELECT * FROM tarefas WHERE status = ? ORDER BY data_entrega ASC",
                    (filtro_status,),
                )
            else:
                cursor = conn.execute("SELECT * FROM tarefas ORDER BY data_entrega ASC")
            return [dict(row) for row in cursor.fetchall()]

    def editar(self, tarefa_id, titulo, disciplina, descricao, data_entrega):
        with self._conectar() as conn:
            conn.execute(
                """UPDATE tarefas
                   SET titulo = ?, disciplina = ?, descricao = ?, data_entrega = ?
                   WHERE id = ?""",
                (titulo.strip(), disciplina.strip(), descricao.strip(), data_entrega, tarefa_id),
            )

    def alternar_status(self, tarefa_id):
        with self._conectar() as conn:
            row = conn.execute("SELECT status FROM tarefas WHERE id = ?", (tarefa_id,)).fetchone()
            if row:
                novo_status = "Concluída" if row["status"] == "Pendente" else "Pendente"
                conn.execute("UPDATE tarefas SET status = ? WHERE id = ?", (novo_status, tarefa_id))

    def excluir(self, tarefa_id):
        with self._conectar() as conn:
            conn.execute("DELETE FROM tarefas WHERE id = ?", (tarefa_id,))
