# Documentação Técnica — Gerenciador de Tarefas Acadêmicas (PIT II)

**Autor:** Andrew Delfino  
**Curso:** Engenharia de Software  
**Padrão Arquitetural:** MVC (Model-View-Controller)  
**Tecnologias:** Python 3, Flask, SQLite 3, HTML5, CSS3 (Bootstrap 5), JavaScript e Pytest  

---

## 1. Revisão de Escopo e Melhoria Contínua (Kaizen)
Na transição do Projeto Integrador Transdisciplinar I (planejamento) para o PIT II (implementação e validação), o escopo foi refinado para entregar um Produto Mínimo Viável (MVP) funcional, enxuto e livre de redundâncias:
- **Separação de responsabilidades:** Adoção do padrão **MVC**, isolando o acesso ao banco de dados (`models`), o controle de rotas e regras de negócio (`controllers`) e a interface gráfica (`views`).
- **Banco de dados relacional:** Escolha do **SQLite 3** pela portabilidade, integridade referencial e facilidade de manutenção sem dependências externas complexas.
- **Qualidade de software:** Inclusão de testes unitários automatizados com **Pytest** e validação prática com 5 usuários reais (pares).

---

## 2. Modelagem UML

### 2.1. Casos de Uso Principais
- **UC01 – Cadastrar Tarefa:** O usuário informa título, disciplina, data de entrega e descrição opcional para registrar uma nova atividade.
- **UC02 – Listar e Filtrar Tarefas:** O usuário visualiza todas as tarefas ordenadas por prazo de entrega, podendo filtrar por status (`Todas`, `Pendentes` ou `Concluídas`).
- **UC03 – Editar Tarefa:** O usuário altera os dados de uma tarefa existente por meio de uma janela modal.
- **UC04 – Alterar Status:** O usuário marca uma tarefa pendente como `Concluída` ou reabre uma tarefa já concluída.
- **UC05 – Excluir Tarefa:** O usuário remove definitivamente uma tarefa após confirmar a ação em caixa de diálogo.

### 2.2. Diagrama de Classes (Camada de Domínio e Persistência)
```text
+-------------------------------------------------------+
|                     TarefaModel                       |
+-------------------------------------------------------+
| - db_path: str                                        |
+-------------------------------------------------------+
| + __init__(db_path: str)                              |
| - _conectar(): Connection                             |
| - _criar_tabela(): void                               |
| + criar(titulo, disciplina, descricao, data): void    |
| + listar(filtro_status: str): list[dict]              |
| + editar(id, titulo, disciplina, desc, data): void    |
| + alternar_status(tarefa_id: int): void               |
| + excluir(tarefa_id: int): void                       |
+-------------------------------------------------------+

Entidade representada (Tabela tarefas):
- id: int (PK)
- titulo: str
- disciplina: str
- descricao: str
- data_entrega: str (ISO AAAA-MM-DD)
- status: str ('Pendente' | 'Concluída')
```

---

## 3. Interface Humano-Computador (IHC)
O projeto da camada de apresentação (`src/views/index.html`) seguiu princípios de usabilidade e ergonomia cognitiva:
- **Clareza e simplicidade:** Formulário único no topo da página com campos rotulados e indicação explícita de obrigatoriedade (`*`).
- **Feedback imediato:** Exibição de alertas visuais (mensagens *flash* do Bootstrap) confirmando cadastro, edição, exclusão ou erro de preenchimento.
- **Prevenção de erros:** Validação de campos obrigatórios no front-end (`required`) e confirmação explícita em JavaScript antes de executar exclusões irreversíveis.
- **Consistência visual:** Uso de selos (*badges*) com cores semânticas (amarelo para `Pendente`, verde para `Concluída`) e formatação de data no padrão brasileiro (`DD/MM/AAAA`).

---

## 4. Projeto de Banco de Dados

### 4.1. Modelo Lógico (Normalizado até a 3ª Forma Normal — 3FN)
- Todos os atributos são atômicos (1FN).
- Todos os atributos não-chave dependem integralmente da chave primária `id` (2FN).
- Não há dependências transitivas entre atributos não-chave (3FN).

**Esquema Relacional:**  
`TAREFAS (id [PK], titulo, disciplina, descricao, data_entrega, status)`

### 4.2. Projeto Físico (DDL SQL)
```sql
CREATE TABLE IF NOT EXISTS tarefas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    disciplina TEXT NOT NULL,
    descricao TEXT,
    data_entrega TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'Pendente'
);
```

---

## 5. Dicionário de Dados — Tabela `tarefas`

| Atributo | Tipo de Dado | Tamanho / Domínio | Restrições | Descrição |
| :--- | :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | Inteiro positivo | `PRIMARY KEY`, `AUTOINCREMENT` | Identificador único sequencial da tarefa. |
| `titulo` | `TEXT` | String não vazia | `NOT NULL` | Título resumido da atividade acadêmica. |
| `disciplina` | `TEXT` | String não vazia | `NOT NULL` | Nome da disciplina relacionada à tarefa. |
| `descricao` | `TEXT` | Texto livre | `NULL` (Opcional) | Detalhes, observações ou links de apoio. |
| `data_entrega` | `TEXT` | Formato `AAAA-MM-DD` | `NOT NULL` | Data limite para entrega da atividade. |
| `status` | `TEXT` | `'Pendente'` ou `'Concluída'` | `NOT NULL`, `DEFAULT 'Pendente'` | Situação atual de andamento da tarefa. |

---

## 6. Verificação, Validação e Melhorias (Testes com Pares)

### 6.1. Verificação Automatizada (Testes Unitários)
Implementada em `tests/test_tarefas.py` com **Pytest**, validando o isolamento do banco de dados, inserção de registros, consulta filtrada, alternância de status e exclusão.

### 6.2. Validação com Usuários e Correções Aplicadas
| Testador | Data | O que funcionou | Falha identificada | Correção implementada |
| :--- | :--- | :--- | :--- | :--- |
| **Lucas Mendes** | 12/11/2026 | Cadastro e listagem inicial. | Formulário aceitava título preenchido apenas com espaços em branco. | Adicionado `required` no HTML e validação `.strip()` no Controller. |
| **Mariana Costa** | 13/11/2026 | Alteração de status e filtros. | Data exibida no formato americano/ISO (`AAAA-MM-DD`). | Criada função `_formatar_data_br()` para exibir `DD/MM/AAAA` na View. |
| **Gabriel Souza** | 13/11/2026 | Edição e persistência no SQLite. | Exclusão imediata ao clicar no botão, sem confirmação. | Adicionado evento `onsubmit="return confirm(...)"` no formulário de exclusão. |
| **Beatriz Lima** | 14/11/2026 | Mensagens de alerta e navegação. | Textos longos sem espaços vazavam da borda do cartão. | Aplicada classe CSS `.texto-quebra` com `word-break: break-word`. |
| **Pedro H. Silva** | 15/11/2026 | Fluxo CRUD completo pós-correções. | Nenhum erro encontrado após as melhorias aplicadas. | Versão consolidada para entrega final. |
