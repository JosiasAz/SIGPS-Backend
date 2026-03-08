# 🏥 SIGPS — A Bíblia do Backend (Guia Definitivo de Implementação)

Este documento é um roteiro técnico exaustivo para reconstruir o backend do sistema **SIGPS** do zero até o estado de 100% funcional. Ele detalha não apenas "o quê" fazer, mas a lógica exata por trás de cada linha e camada.

---

## � 1. Estrutura do Projeto e Organização
A arquitetura segue o padrão **Clean Architecture** com **Repository Pattern**:
- `app/api/v1/`: Controladores (Endpoints). Eles apenas recebem a requisição e chamam o serviço.
- `app/core/`: O "cérebro" da infraestrutura (segurança, configurações, permissões).
- `app/db/`: Conexão e orquestração do banco de dados.
- `app/models/`: Tabelas do banco de dados (SQLAlchemy).
- `app/schemas/`: Contratos de dados (Pydantic) para validação e serialização.
- `app/services/`: Lógica de negócio pesada. Onde os serviços conversam entre si.
- `app/repositories/`: Isolamento do SQL/ORM.
- `app/utils/`: Ferramentas auxiliares (validadores, enums).

---

## 🛠️ 2. Implementação Passo a Passo

### Etapa 1: Infraestrutura e Segurança (`app/core/`)
Antes de criar rotas, o sistema de proteção deve estar pronto:
1.  **`config.py`**: Use `pydantic-settings` para carregar o `.env`. O backend depende de: `SECRET_KEY`, `DATABASE_URL` e `ALGORITHM`.
2.  **`security.py`**:
    - Função `get_password_hash`: Usa `passlib[bcrypt]` para transformar "senha123" em um hash seguro.
    - Função `create_access_token`: Gera o JWT.
3.  **`permissions.py` (O Guardião)**: 
    - Implemente a classe `RoleChecker`. Ela deve receber uma lista de roles (ex: `['admin', 'gestor']`) e verificar se o `token` do usuário atual contém um desses perfis. Se não tiver, retorna `403 Forbidden`.

### Etapa 2: O Coração de Dados (`app/models/` & `app/db/`)
O banco de dados deve refletir as seguintes entidades e regras:
1.  **`User`**: O núcleo. Campos: `email`, `password_hash`, `role` (enum), `is_active`.
2.  **`Patient`**: Dados pessoais. FK para `User`.
3.  **`Specialist`**: Campos: `registro_profissional`, `bio`, `modality` (Presencial/Online). **Campo crítico:** `status` (Enum: PENDENTE, ATIVO, SUSPENSO).
4.  **`Schedule`**: A agenda. Campos: `specialist_id`, `data`, `hora_inicio`, `is_available` (Default: True).
5.  **`Appointment`**: O agendamento. Une `Patient`, `Specialist` e `Schedule`.

> [!IMPORTANT]
> No arquivo `app/db/base_models.py`, você **deve** importar todos os arquivos da pasta `models`. O Alembic usa esse arquivo como mapa para criar as tabelas automaticamente.

### Etapa 3: Lógica de Negócio "Inteligente" (`app/services/`)
É aqui que o sistema deixa de ser um "site comum" e vira o SIGPS:

**1. Lógica de Agendamento (`AppointmentService`):**
- Quando um paciente tenta agendar:
  - Verificar se o `ScheduleID` realmente pertence àquele especialista.
  - Verificar se `is_available` ainda é `True`.
  - Criar o registro de `Appointment`.
  - **Mudar `is_available` para `False`** imediatamente. Isso evita que duas pessoas marquem o mesmo horário ao mesmo tempo.

**2. Lógica de Aprovação de Especialista (`AdminService`):**
- Especialistas novos entram como `is_active = False` e `status = PENDENTE`.
- Criar um endpoint `/admin/approve/{specialist_id}`.
- Ao aprovar, o serviço muda o status para `ATIVO` e o `is_active` do `User` para `True`. Só então o especialista pode ser listado no site.

**3. Dashboard (`DashboardService`):**
- Realize contagens usando `sqlalchemy.func.count`.
- O dashboard deve retornar: Total de pacientes, atendimentos realizados hoje e taxa de cancelamento.

---

## 📜 3. Definição Detalhada de Endpoints (API V1)

### Autenticação (`/auth`)
- `POST /login`: Recebe email/senha, valida e retorna o JWT.
- `GET /me`: Retorna os dados do usuário logado (usando o Token).

### Usuários (`/users`)
- `POST /`: Cadastro inicial. Se for especialista, cria o perfil pendente.
- `GET /`: Lista de usuários (Apenas Admin/Gestor).

### Pacientes (`/patients`)
- `GET /me`: Ver minhas consultas e histórico de saúde.
- `PUT /me`: Atualizar meus dados.

### Especialistas (`/specialists`)
- `GET /`: Listar especialistas **ATIVOS**.
- `POST /schedules`: Especialista cria seus horários de atendimento.

### Consultas (`/appointments`)
- `POST /`: Paciente realiza o agendamento (Gatilha a lógica de reserva).
- `PATCH /{id}/cancel`: Libera o horário na agenda automaticamente.

---

## ⚡ 4. Guia de Migrações e Inicialização
1.  **Primeira Migração**: 
    - `alembic revision --autogenerate -m "Initial schema"`
    - `alembic upgrade head`
2.  **Seed (`app/db/init_db.py`)**: 
    - Implemente uma função que verifica se o email `admin@sigps.com.br` existe. Se não, cria o usuário Admin inicial. Sem isso, você ficará trancado fora do sistema.

---

## 🛡️ 5. Regras de Ouro para o Desenvolvedor
- **Nunca use `os.getenv` nas rotas**: Chame sempre o objeto `settings` do `app.core.config`.
- **Tratamento de Erros**: Use `raise HTTPException(status_code=400, detail="Mensagem personalizada")`. Nunca deixe o servidor retornar erro 500 sem tratamento.
- **Validadores de CPF**: Implemente o cálculo matemático real de validação de CPF para evitar lixo no banco de dados.
- **Comentários**: Mantenha todos os comentários em português para consistência da equipe.

---

## 🏁 Conclusão
Seguindo este roteiro, o backend será robusto, auditável e seguro. A separação em camadas garante que se amanhã você quiser trocar o banco de dados MySQL para PostgreSQL, precisará mexer apenas na camada de infraestrutura, sem tocar na lógica de negócio.
