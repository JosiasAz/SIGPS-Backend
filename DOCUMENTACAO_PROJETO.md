# Documentação Completa do Projeto SIGPS

## 1. Visão Geral
O **SIGPS (Sistema Inteligente de Gerenciamento de Prioridades em Saúde)** é uma plataforma de backend projetada para o **autoatendimento inteligente**. Diferente de sistemas tradicionais, o SIGPS elimina a necessidade de triagem manual por recepcionistas, permitindo que o fluxo de atendimento seja guiado de ponta a ponta por **Inteligência Artificial (Machine Learning)**.

---

## 2. O Problema vs. A Solução
*   **O Problema:** Filas de espera baseadas na ordem de chegada e dependência de triagem humana, que pode ser lenta e subjetiva.
*   **A Solução:** Um sistema **Self-Service**. O paciente realiza seu cadastro e entrada na fila. No exato momento da entrada, a IA analisa o perfil socioeconômico e clínico do paciente e define sua posição prioritária em tempo real.

---

## 3. Principais Funcionalidades

### 🔐 3.1. Gestão de Acesso e Segurança (Autenticação)
*   **Autenticação JWT:** Login seguro para pacientes e gestores via `/auth/login`.
*   **RBAC (Controle Baseado em Perfis):**
    *   `admin`: Controle total e manutenção do modelo de IA via `/ia/treinar`.
    *   `gestor`: Supervisão de especialistas e painéis.
    *   `paciente`: Perfil de autoatendimento para realizar entrada na fila e acompanhar posição.

### 👥 3.2. Autoatendimento de Pacientes
*   **Cadastro Socioeconômico:** O paciente fornece dados como idade, renda e gastos, essenciais para a análise de vulnerabilidade pela IA.
*   **Especialistas e Especialidades:** Acesso à lista de médicos via `/especialistas`.

### 📅 3.3. Fila Inteligente Automática
*   **Entrada Sem Intervenção:** Ao entrar na fila via `/fila`, o sistema não aguarda uma triagem humana.
*   **Cálculo Instantâneo de IA:** O backend chama o motor de Machine Learning no momento da criação da entrada na fila, preenchendo o score de prioridade automaticamente.
*   **Organização Dinâmica:** A fila se reordena instantaneamente para garantir que os mais urgentes sejam chamados primeiro.

### 🧠 3.4. Inteligência Artificial (IA)
*   **Modelo:** Regressão Logística (Scikit-learn).
*   **Automação:** Fornece a inteligência necessária para que o sistema funcione sem funcionários de recepção.
*   **Explicação:** O score de urgência é calculado cruzando a idade do paciente com o impacto financeiro de sua renda, priorizando quem tem maior risco social.

---

## 4. Arquitetura Técnica
*   `app/routers/fila.py`: Integra diretamente a chamada à IA (`prever_prioridade`) durante a criação da entrada na fila.
*   `app/database/models.py`: Modelos em Português (Paciente, Especialista, Agendamento, etc.).
*   `app/routers/deps.py`: Permissões ajustadas para que o perfil `paciente` possa operar suas próprias solicitações de fila.

---

## 5. Fluxo de Uso "Zero Recepção"
1.  **Login do Paciente:** O usuário entra no sistema com seu perfil de `paciente`.
2.  **Registro de Dados:** Se for o primeiro acesso, o paciente preenche seus dados socioeconômicos.
3.  **Entrada na Fila:** O paciente clica para entrar na fila (com ou sem médico preferencial).
4.  **Processamento em Backstage:** O SIGPS chama a IA, gera o score e coloca o paciente na posição correta da fila.
5.  **Notificação/Atendimento:** O profissional disponível visualiza a fila (organizada por prioridade) e chama o próximo paciente.

---

## 6. Stack Tecnológica
*   **Linguagem:** Python 3.12
*   **Framework:** FastAPI
*   **Banco de Dados:** MySQL / SQLAlchemy
*   **IA:** Scikit-Learn, NumPy
*   **Container:** Docker & Docker Compose
*   **Documentação Automática:** Swagger (OpenAPI) em `/docs`

---

## 7. Próximos Passos (Roadmap)
*   [x] Tradução completa do backend para Português (PT-BR).
*   [ ] Notificações via WhatsApp/E-mail para pacientes chamados.
*   [ ] Front-end em React/Next.js para visualização do Painel.

---
**Documento gerado para registro técnico do projeto SIGPS.**
