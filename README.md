
---

# SIGPS – Backend

**Sistema Inteligente de Gerenciamento de Prioridades em Saúde (SIGPS)**

Este repositório contém o **back-end do projeto SIGPS**, desenvolvido como **projeto acadêmico**, com foco em organização, clareza e aprendizado em equipe.

O sistema tem como objetivo **gerenciar usuários da área da saúde e aplicar priorização inteligente de atendimentos**, utilizando **Machine Learning** de forma simples e explicável.

---

## 🎯 Objetivo do Projeto

O SIGPS busca resolver um problema comum em sistemas de saúde e bem-estar:
**a falta de priorização inteligente e organizada no atendimento de pacientes**.

Este backend é responsável por:

* Gerenciar usuários e perfis (RBAC)
* Autenticação via JWT
* Disponibilizar API REST documentada (Swagger)
* Integrar um **módulo de Machine Learning** para apoiar a priorização

---

## 🧠 Uso de Machine Learning (Abordagem Acadêmica)

O projeto utiliza **Machine Learning como apoio à decisão**, não como substituição do profissional.

### Importante:

* ❌ A API **não treina modelos automaticamente**
* ✅ O treinamento é feito separadamente
* ✅ A API apenas **carrega o modelo treinado** e executa inferências

Isso garante:

* Simplicidade
* Performance
* Clareza para fins acadêmicos

---

## 🏗️ Arquitetura do Backend

```
sigps-backend/
├── app/
│   ├── main.py              # Inicialização da API
│   ├── database.py          # Conexão com MySQL
│   ├── core/                # Configurações e segurança
│   ├── models/              # Modelos do banco (SQLAlchemy)
│   ├── schemas/             # Schemas Pydantic
│   ├── routers/             # Endpoints da API
│   ├── services/            # Regras de negócio
│   └── ml/                  # Módulo de Machine Learning
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🧩 Tecnologias Utilizadas

* **Python 3.12**
* **FastAPI**
* **SQLAlchemy**
* **MySQL**
* **Docker & Docker Compose**
* **JWT (Autenticação)**
* **Scikit-learn (Machine Learning)**

---

## 🔐 Perfis de Usuário (RBAC)

O sistema trabalha com controle de acesso baseado em perfil:

* `admin` – controle total
* `gestor` – gerenciamento
* `recepcao` – operações de fila/priorização
* `paciente` – acesso limitado

Esse controle é feito via **JWT + dependências do FastAPI**.

---

## 🚀 Como Rodar o Projeto

### 1️⃣ Pré-requisitos

* Docker
* Docker Compose

---

### 2️⃣ Clonar o repositório

```bash
git clone https://github.com/seu-usuario/sigps-backend.git
cd sigps-backend
```

---

### 3️⃣ Criar o arquivo `.env`

```bash
cp .env.example .env
```

> Ajuste apenas se necessário (em geral, não precisa).

---

### 4️⃣ Subir o ambiente

```bash
docker compose up --build
```

---

### 5️⃣ Acessar a API

* Swagger (documentação):
  👉 [http://localhost:8000/docs](http://localhost:8000/docs)
* Healthcheck:
  👉 [http://localhost:8000/health](http://localhost:8000/health)

---

## 🤖 Machine Learning – Como Usar

### Treinar o modelo (manual)

```bash
docker exec -it sigps_api python -m app.ml.train
```

Isso irá gerar o arquivo:

```
app/ml/model.pkl
```

⚠️ **Esse arquivo não é versionado no Git** (boa prática).

---

### Testar inferência via API

Endpoint:

```
POST /ml/predict
```

Exemplo de payload:

```json
{
  "features": [1, 0, 0]
}
```

Resposta esperada:

```json
{
  "score": 2,
  "prioridade": "alta"
}
```

---

## 📌 Organização para a Equipe

* **Routers**: apenas recebem requisições e retornam respostas
* **Services**: contêm regras de negócio
* **ML**: isolado, simples e explicável
* **Database**: centralizado
* **Configurações**: todas via `.env`

Essa separação facilita:

* Aprendizado
* Manutenção
* Divisão de tarefas

---

## 📚 Contexto Acadêmico

Este projeto:

* Utiliza **dados simulados** para ML

* Prioriza **clareza didática e organização**


---

## 👥 Equipe

Projeto desenvolvido por alunos de **Análise e Desenvolvimento de Sistemas**, com foco em aprendizado prático, arquitetura limpa e boas práticas de backend.

Autores: 
- Josias Azevedo da Silva
- Alan Nicolas
- Matheus Akabane
- Kaio Pantoja
---

## 📄 Licença

Projeto de uso **exclusivamente acadêmico**.

