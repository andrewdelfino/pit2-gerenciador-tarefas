# Gerenciador de Tarefas Acadêmicas (PIT II - Engenharia de Software)

Sistema web desenvolvido em **Python (Flask)** seguindo o padrão arquitetural **MVC (Model-View-Controller)** com persistência em banco de dados relacional **SQLite 3**.

## Estrutura do Projeto
- `/docs`: Documentação técnica (Diagrama de Classes UML, Modelo Relacional 3FN, Dicionário de Dados e Relatório de Testes).
- `/src`: Código-fonte separado em `models`, `views` e `controllers`.
- `/tests`: Testes automatizados utilizando `pytest`.

## Como Executar Localmente
1. Instale as dependências: `pip install -r requirements.txt`
2. Inicie a aplicação: `python src/app.py`
3. Acesse no navegador: `http://127.0.0.1:5000`
4. Para rodar os testes: `pytest`
