# Documentação Técnica — Gerenciador de Tarefas Acadêmicas

## 1. Diagrama de Classes (UML)
- **Classe `Tarefa`**:
  - `- id: int` (Identificador único)
  - `- titulo: str` (Título obrigatório da tarefa)
  - `- disciplina: str` (Nome da disciplina)
  - `- descricao: str` (Detalhes opcionais)
  - `- data_entrega: str` (Data no formato ISO `AAAA-MM-DD`)
  - `- status: str` (`Pendente` ou `Concluída`)
  - `+ criar()`, `+ listar()`, `+ editar()`, `+ alterar_status()`, `+ excluir()`

## 2. Projeto Lógico e Físico (3ª Forma Normal)
```sql
CREATE TABLE IF NOT EXISTS tarefas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    disciplina TEXT NOT NULL,
    descricao TEXT,
    data_entrega TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'Pendente'
);
