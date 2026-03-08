# SIGPS — Sistema Inteligente de Gestão e Priorização na Saúde (Backend)

Este repositório contém o **esqueleto inicial** (Boilerplate) do backend do projeto SIGPS, desenvolvido com FastAPI e SQLAlchemy. O projeto foi estruturado para ser modular, seguro e escalável.

---

## 🚀 Como Rodar o Projeto

### 1. Pré-requisitos
*   **Python 3.12** ou superior instalado.
*   **MySQL 8.0** configurado e rodando (ou via Docker).

### 2. Configuração do Ambiente
1.  **Clone o repositório** (ou acesse a pasta do projeto).
2.  **Crie um ambiente virtual:**
    ```bash
    python -m venv .venv
    ```
3.  **Ative o ambiente virtual:**
    *   No Windows: `.venv\Scripts\activate`
    *   No Linux/Mac: `source .venv/bin/activate`
4.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

### 3. Variáveis de Ambiente
O projeto utiliza um arquivo `.env` para gerenciar configurações sensíveis.
1.  Copie o arquivo de exemplo:
    ```bash
    cp .env.example .env
    ```
2.  Abra o arquivo `.env` e preencha as informações de conexão com seu banco de dados MySQL e a `SECRET_KEY`.

### 4. Migrações do Banco de Dados
O projeto utiliza o Alembic para gerenciar as tabelas. Após configurar o banco no `.env`:
1.  **Gere a migração inicial** (quando houver modelos criados):
    ```bash
    alembic revision --autogenerate -m "Initial Migration"
    ```
2.  **Aplique as migrações:**
    ```bash
    alembic upgrade head
    ```

### 5. Executando o Servidor
Com o ambiente configurado, inicie o servidor de desenvolvimento:
```bash
uvicorn app.main:app --reload
```
A API estará disponível em: `http://localhost:8000`

---

## 📖 Documentação da API
Uma vez que o servidor estiver rodando, você pode acessar a documentação interativa:
*   **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
*   **Redoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🛠️ Guia de Desenvolvimento
Para entender a lógica de negócio, a arquitetura em camadas e o passo a passo de implementação de cada funcionalidade:
*   Consulte o arquivo: **`IMPLEMENTATION_GUIDE.md`**
*   Para continuar o desenvolvimento com IA: **`PROMPT_PARA_ANTIGRAVITY.md`**

---

## 📁 Estrutura de Pastas
```text
app/
├── api/             # Endpoints e Rotas
├── core/            # Configurações globais e Segurança
├── db/              # Sessão e Base do Banco
├── models/          # Entidades SQLAlchemy
├── repositories/    # Camada de Acesso a Dados
├── schemas/         # Validações Pydantic
├── services/        # Regras de Negócio
└── utils/           # Validadores e Enums
```
