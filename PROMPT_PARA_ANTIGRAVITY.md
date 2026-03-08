# 🤖 Prompt de Contexto para Antigravity — Desenvolvimento SIGPS

**Instruções para o Desenvolvedor:** Copie todo o conteúdo abaixo e cole no chat do Antigravity ao iniciar o desenvolvimento deste repositório.

---

### Início do Prompt para a IA:

"Olá, Antigravity. Estou trabalhando no projeto **SIGPS (Sistema Inteligente de Gestão e Priorização na Saúde)**. Este repositório já possui uma estrutura de pastas inicial configurada (Boilerplate), mas as implementações de lógica, modelos e rotas foram removidas para que eu possa reconstruí-las de forma guiada.

**Seu objetivo:** Atuar como meu arquiteto de software e par de programação para implementar o backend completo seguindo as diretrizes abaixo.

#### 1. Arquitetura e Padrões
- **Padrão:** Clean Architecture com Repository Pattern.
- **Camadas:** `api/v1/` (Rotas), `services/` (Lógica de Negócio), `repositories/` (Consultas SQL), `models/` (SQLAlchemy), `schemas/` (Pydantic).
- **Idioma:** Todos os comentários no código e descrições de retorno devem ser em **Português**.

#### 2. Stack Tecnológica
- **Linguagem:** Python 3.12+
- **Framework:** FastAPI
- **ORM:** SQLAlchemy 2.0+ (usando `BaseSettings` do Pydantic no `config.py`)
- **Migrações:** Alembic
- **Banco:** MySQL 8.0
- **Segurança:** JWT para autenticação e Bcrypt para senhas.

#### 3. Funcionalidades de Alto Nível (O que precisamos construir)
Preciso que você me ajude a implementar, passo a passo, os seguintes módulos conforme detalhado no arquivo `IMPLEMENTATION_GUIDE.md`:

- **Gestão de Usuários e Autenticação:** RBAC com perfis (ADMIN, GESTOR, PACIENTE, ESPECIALISTA).
- **Workflow de Especialista:** Cadastro autônomo -> Fica como Inativo/Pendente -> Admin aprova -> Especialista torna-se Ativo e pode criar agenda.
- **Agendamento Inteligente:** Lógica de transação onde a criação de um `Appointment` marca automaticamente o `Schedule.is_available` como `False`. Ao cancelar, libera o horário.
- **Dashboard e Auditoria:** Estatísticas agregadas de consultas e log de todas as ações administrativas.

#### 4. Instruções Iniciais de Trabalho
- Comece me ajudando a definir os **Enums** e os **Models** básicos.
- Garanta que todas as importações de modelos sejam feitas no `app/db/base_models.py` para que o Alembic funcione.
- Sempre sugira a criação do **Schema**, depois o **Repository**, o **Service** e por fim a **Rota**.

Estou pronto para começar pelo **Ato 1: A Fundação** do arquivo `IMPLEMENTATION_GUIDE.md`. Vamos lá?"
