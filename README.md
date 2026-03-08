# SIGPS -- Backend

**Sistema Inteligente de Gestão e Priorização na Saúde (SIGPS)**

Este repositório contém o **backend da plataforma SIGPS**, responsável
pela API REST, autenticação, gerenciamento de usuários, especialistas e
agendamentos.

O SIGPS é uma plataforma desenvolvida como **Trabalho de Conclusão de
Curso (TCC)** em Análise e Desenvolvimento de Sistemas.

O sistema conecta **pacientes e profissionais da área de saúde e
bem‑estar**, permitindo agendamentos inteligentes, organização de
agendas e priorização de atendimentos.

⚠️ O SIGPS **não é um sistema hospitalar** e **não realiza diagnósticos
médicos**.

------------------------------------------------------------------------

# 🎯 Missão

> Conectar pacientes aos profissionais certos, no momento certo, com
> inteligência e eficiência.

------------------------------------------------------------------------

# 🧠 Arquitetura do Projeto

O sistema SIGPS é dividido em **três repositórios principais**.

    SIGPS
    ├── sigps-frontend   → Interface web (Angular)
    ├── sigps-backend    → API REST (FastAPI)
    └── sigps-ml         → Machine Learning (priorização inteligente)

### Responsabilidades

**Frontend** - Interface do usuário - Comunicação com a API

**Backend** - Autenticação e segurança - Gerenciamento de usuários -
Gerenciamento de especialistas - Gerenciamento de agendamentos - Regras
de negócio

**Machine Learning** - Treinamento do modelo - Geração do modelo
`.pkl` - Algoritmo de priorização

------------------------------------------------------------------------

# 👥 Perfis do Sistema

O SIGPS possui **5 perfis de acesso**:

  Perfil         Tipo
  -------------- ---------
  Paciente       Externo
  Especialista   Externo
  Admin          Interno
  Gestor         Interno
  Visualizador   Interno

------------------------------------------------------------------------

# 📅 Fluxo de Agendamento

Existem dois modos de agendamento.

## Agendamento Manual

1.  Paciente busca especialista
2.  Escolhe profissional
3.  Seleciona horário disponível
4.  Confirma agendamento

------------------------------------------------------------------------

## Agendamento Assistido por IA

Quando o paciente não escolhe um especialista específico, o sistema
pode:

-   sugerir o horário mais próximo
-   sugerir especialistas disponíveis
-   sugerir modalidade presencial ou online

A decisão final **sempre é confirmada pelo paciente**.

------------------------------------------------------------------------

# 🤖 Machine Learning

O módulo de Machine Learning está em um repositório separado:

    SIGPS-Machine-Learning

Ele é responsável por:

-   treinamento do modelo
-   geração do arquivo de modelo
-   priorização inteligente de atendimentos

O backend **não realiza treinamento**.

Ele apenas **consome os resultados produzidos pelo módulo de ML**.

------------------------------------------------------------------------

# 🏗️ Estrutura do Backend

    sigps-backend/
    │
    ├── app/
    │   ├── main.py
    │   ├── database.py
    │
    │   ├── core/
    │   │   ├── config.py
    │   │   └── security.py
    │
    │   ├── models/
    │   │   ├── user.py
    │   │   ├── specialist.py
    │   │   └── appointment.py
    │
    │   ├── schemas/
    │   │   ├── user_schema.py
    │   │   └── appointment_schema.py
    │
    │   ├── routers/
    │   │   ├── auth_router.py
    │   │   ├── users_router.py
    │   │   └── appointments_router.py
    │
    │   └── services/
    │       ├── user_service.py
    │       └── appointment_service.py
    │
    ├── docker-compose.yml
    ├── Dockerfile
    ├── requirements.txt
    ├── .env.example
    └── README.md

------------------------------------------------------------------------

# 🧩 Tecnologias Utilizadas

  Tecnologia    Uso
  ------------- -----------------
  Python 3.12   Linguagem
  FastAPI       API REST
  SQLAlchemy    ORM
  MySQL         Banco de dados
  Docker        Containerização
  JWT           Autenticação
  Nginx         Proxy reverso

------------------------------------------------------------------------

# 🔐 Segurança

O sistema implementa:

-   Autenticação **JWT**
-   Controle de acesso **RBAC**
-   Senhas com **bcrypt**
-   HTTPS
-   Variáveis sensíveis via `.env`

------------------------------------------------------------------------

# 🚀 Executando o Backend

## Pré‑requisitos

-   Docker
-   Docker Compose

------------------------------------------------------------------------

## Clonar repositório

``` bash
git clone https://github.com/seu-usuario/sigps-backend.git
cd sigps-backend
```

------------------------------------------------------------------------

## Criar arquivo `.env`

``` bash
cp .env.example .env
```

------------------------------------------------------------------------

## Subir ambiente

``` bash
docker compose up --build
```

------------------------------------------------------------------------

## Acessar API

Swagger:

    http://localhost:8000/docs

Healthcheck:

    http://localhost:8000/health

------------------------------------------------------------------------

# 🧑‍💻 Metodologia

O projeto utiliza **Scrum** com sprints quinzenais gerenciadas via
**Asana**.

------------------------------------------------------------------------

# 👥 Equipe

  Membro            Papel
  ----------------- --------------------------
  Josias Azevedo    Scrum Master · Fullstack
  Alan Nicolas      Product Owner · Backend
  Matheus Akabane   QA
  Kaio Pantoja      Frontend
  Olliver Aquino    Frontend

------------------------------------------------------------------------

# 📄 Licença

Projeto de uso **exclusivamente acadêmico**.
