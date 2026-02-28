# SIGPS — System Intelligent de Gestão e Priorização na Saúde

O **SIGPS** é um ecossistema inteligente voltado para a gestão de clínicas, consultórios e profissionais autônomos de saúde e bem-estar. Este repositório contém o **Backend**, construído com uma arquitetura moderna e escalável utilizando **FastAPI** e **Machine Learning**.

---

## 🚀 Como Iniciar do Zero

### 1. Pré-requisitos
*   **Python 3.10+** (Recomendado 3.12)
*   **MySQL 8.x** (Local ou via Docker)
*   **Docker & Docker Compose** (Opcional, mas recomendado)

### 2. Configuração do Ambiente Local
Siga estes passos para rodar o projeto sem Docker:

1.  **Clonar o Repositório:**
    ```bash
    git clone https://github.com/JosiasAz/SIGPS-Backend.git
    cd sigps-backend
    ```

2.  **Criar e Ativar Ambiente Virtual:**
    ```bash
    python -m venv .venv
    # Windows:
    .venv\Scripts\activate
    # Linux/Mac:
    source .venv/bin/activate
    ```

3.  **Instalar Dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar Variáveis de Ambiente:**
    Crie um arquivo `.env` na raiz do projeto (use o `.env.example` como base):
    ```env
    APP_ENV=dev
    DATABASE_URL=mysql+pymysql://user:password@localhost:3306/sigps
    JWT_SECRET=sua_chave_secreta_aqui
    JWT_ALG=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=1440
    REFRESH_TOKEN_EXPIRE_DAYS=7
    ```

5.  **Iniciar o Servidor:**
    ```bash
    uvicorn app.main:app --reload
    ```
    Acesse em: `http://localhost:8000/docs`

### 3. Configuração via Docker (Recomendado)
Se você tem Docker instalado, basta rodar:
```bash
docker-compose up --build
```
Isso subirá a API e o banco de dados MySQL automaticamente em uma rede isolada.

---

## 📂 Estrutura do Projeto

```text
sigps-backend/
├── app/
│   ├── core/           # Configurações globais, segurança e padrões de resposta
│   ├── database/       # Modelos (SQLAlchemy) e conexão com banco
│   ├── ml/             # Motor de Machine Learning (Priorização e Inferência)
│   ├── routers/        # Controladores da API segmentados por módulos
│   ├── schemas/        # Validação de dados e serialização (Pydantic)
│   ├── services/       # Lógica de negócio complexa (opcional)
│   └── main.py         # Ponto de entrada da aplicação FastAPI
├── data/
│   └── models/         # Diretório para armazenamento dos arquivos .pkl (IA)
├── .env                # Variáveis de ambiente sensíveis
├── docker-compose.yml  # Orquestração de containers
├── Dockerfile          # Definição da imagem Docker
└── requirements.txt    # Dependências do Python
```

---

## 🛠️ Módulos e Regras de Negócio

### 1. Autenticação e RBAC (`/auth`)
Utilizamos **JWT Stateless** com um sistema de **Access e Refresh Tokens**.
*   **Perfis (RBAC):** `paciente`, `especialista`, `admin`, `gestor`, `visualizador`.
*   **Logout:** Invalida o Refresh Token no banco de dados.

### 2. Especialistas (`/especialistas`)
*   Listagem pública com filtros inteligentes (especialidade, modalidade, localização).
*   Gestão de perfil próprio e bloqueio de horários na agenda.

### 3. Agendamentos (`/agendamentos`)
*   **Modo Manual:** Paciente escolhe livremente o slot.
*   **Modo Automático (IA):** O sistema sugere o melhor slot com base nas preferências.
*   **Regra Crítica:** Agendamentos sugeridos pela IA ficam em estado pendente até a **confirmação final do paciente**.

### 4. Lista de Espera Inteligente (`/fila`)
*   Ao entrar na fila, o módulo de **Machine Learning** é acionado.
*   O cálculo de prioridade leva em conta: urgência, vulnerabilidade socioeconômica e perfil clínico.
*   Permite intervenção manual de gestores para ajustes excepcionais.

---

## 🧠 Módulo de Machine Learning
O SIGPS utiliza modelos baseados em **Scikit-learn** carregados diretamente em memória para alta performance.
*   **Ação:** O score é gerado instantes após a requisição.
*   **Inputs:** Idade, Renda, Gastos (ou urgência declarada).
*   **Output:** Score numérico que determina a ordenação dinâmica da fila.

---

## 📡 Padrões de Resposta da API
Todas as respostas seguem o formato:

```json
{
  "success": true,
  "data": { ... },
  "message": "Operação realizada"
}
```

Em caso de erro:
```json
{
  "success": false,
  "error": {
    "code": "ERRO_VAL_01",
    "message": "Descrição detalhada do erro"
  }
}
```

---

## 👥 Equipe e Autores
Projeto desenvolvido com foco acadêmico e profissional em arquitetura de software e inteligência artificial aplicada à saúde.

*   **Josias Azevedo da Silva** (JosiasAz)
*   **Equipe SIGPS**

---

## 📄 Licença e Uso
Este projeto é de cunho acadêmico/profissional. Proibida reprodução para fins comerciais sem autorização.
SIGPS não realiza diagnósticos médicos e não atua em situações de emergência.
