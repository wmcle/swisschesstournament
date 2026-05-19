# SP26 - Swiss Chess Tournament Manager

Um gerenciador de torneios de xadrez moderno, inspirado no clássico **Swiss Perfect 98**. O SP26 permite organizar e administrar torneios no sistema suíço com uma interface simples, rápida e responsiva.

## 🚀 Recursos Principais

- **Gestão de Jogadores**: Adição, edição, exclusão e visualização rápida de jogadores com seus respectivos ratings e pontuações.
- **Emparceiramentos (Sistema Suíço)**: Geração automática das rodadas usando as regras do sistema suíço.
- **Registro de Resultados**: Atribuição simplificada dos resultados das partidas (1-0, 0-1, 1/2-1/2, e Byes).
- **Classificação Geral**: Tabela atualizada automaticamente a cada rodada com a classificação em tempo real dos participantes.

## 🛠️ Tecnologias Utilizadas

- **Python 3**: Linguagem base do projeto.
- **[Flet](https://flet.dev/)**: Framework UI moderno baseado em Flutter, utilizado para a construção da interface gráfica (Desktop/Web).
- **SQLite**: Banco de dados leve e embutido para salvar e persistir as informações do torneio localmente (`tournament.db`).

## ⚙️ Como Executar o Projeto

1. Certifique-se de ter o Python instalado na sua máquina (versão 3.8 ou superior).
2. Clone o repositório ou baixe o projeto.
3. Crie e ative um ambiente virtual (recomendado):
   ```bash
   python -m venv .venv
   
   # No macOS/Linux:
   source .venv/bin/activate
   
   # No Windows:
   .venv\Scripts\activate
   ```
4. Instale as dependências (Flet):
   ```bash
   pip install flet
   ```
5. Inicie a aplicação:
   ```bash
   python main.py
   ```

## 📝 Estrutura do Projeto

- `main.py`: Ponto de entrada da aplicação e definição da Interface de Usuário.
- `db.py`: Funções para manipulação do banco de dados SQLite (CRUD de jogadores e registro de partidas).
- `engine.py`: Motor lógico responsável pela realização dos emparceiramentos entre os jogadores.
- `tournament.db`: Banco de dados gerado automaticamente na primeira execução do sistema.

## 📄 Licença

Este projeto está sob licença (ver arquivo `LICENSE` para mais detalhes).