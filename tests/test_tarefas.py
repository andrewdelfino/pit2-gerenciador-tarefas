import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from models.tarefa_model import TarefaModel


def test_criar_e_listar_tarefa(tmp_path):
    db_teste = tmp_path / "teste.db"
    model = TarefaModel(str(db_teste))

    model.criar("Entregar PIT II", "Engenharia de Software", "Subir no GitHub", "2026-11-20")
    tarefas = model.listar()

    assert len(tarefas) == 1
    assert tarefas[0]["titulo"] == "Entregar PIT II"
    assert tarefas[0]["status"] == "Pendente"


def test_alternar_status_e_excluir(tmp_path):
    db_teste = tmp_path / "teste.db"
    model = TarefaModel(str(db_teste))

    model.criar("Estudar Pytest", "Qualidade de Software", "", "2026-11-22")
    tarefa_id = model.listar()[0]["id"]

    model.alternar_status(tarefa_id)
    assert model.listar()[0]["status"] == "Concluída"

    model.excluir(tarefa_id)
    assert len(model.listar()) == 0
