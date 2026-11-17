from datetime import datetime
from flask import Blueprint, flash, redirect, render_template, request, url_for
from models.tarefa_model import TarefaModel

tarefa_bp = Blueprint("tarefas", __name__)
model = TarefaModel()


def _formatar_data_br(data_iso):
    try:
        return datetime.strptime(data_iso, "%Y-%m-%d").strftime("%d/%m/%Y")
    except ValueError:
        return data_iso


@tarefa_bp.route("/", methods=["GET"])
def index():
    filtro = request.args.get("status", "Todos")
    tarefas = model.listar(filtro)
    for t in tarefas:
        t["data_formatada"] = _formatar_data_br(t["data_entrega"])
    return render_template("index.html", tarefas=tarefas, filtro=filtro)


@tarefa_bp.route("/criar", methods=["POST"])
def criar():
    titulo = request.form.get("titulo", "")
    disciplina = request.form.get("disciplina", "")
    descricao = request.form.get("descricao", "")
    data_entrega = request.form.get("data_entrega", "")

    if not titulo.strip() or not disciplina.strip() or not data_entrega:
        flash("Preencha todos os campos obrigatórios corretamente.", "danger")
        return redirect(url_for("tarefas.index"))

    model.criar(titulo, disciplina, descricao, data_entrega)
    flash("Tarefa cadastrada com sucesso!", "success")
    return redirect(url_for("tarefas.index"))


@tarefa_bp.route("/editar/<int:tarefa_id>", methods=["POST"])
def editar(tarefa_id):
    titulo = request.form.get("titulo", "")
    disciplina = request.form.get("disciplina", "")
    descricao = request.form.get("descricao", "")
    data_entrega = request.form.get("data_entrega", "")

    if not titulo.strip() or not disciplina.strip() or not data_entrega:
        flash("Os campos obrigatórios não podem ficar em branco.", "danger")
        return redirect(url_for("tarefas.index"))

    model.editar(tarefa_id, titulo, disciplina, descricao, data_entrega)
    flash("Tarefa atualizada!", "info")
    return redirect(url_for("tarefas.index"))


@tarefa_bp.route("/status/<int:tarefa_id>", methods=["POST"])
def alternar_status(tarefa_id):
    model.alternar_status(tarefa_id)
    return redirect(url_for("tarefas.index"))


@tarefa_bp.route("/excluir/<int:tarefa_id>", methods=["POST"])
def excluir(tarefa_id):
    model.excluir(tarefa_id)
    flash("Tarefa excluída.", "warning")
    return redirect(url_for("tarefas.index"))
