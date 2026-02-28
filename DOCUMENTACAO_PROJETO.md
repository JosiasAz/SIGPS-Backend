# SIGPS — Documentação Técnica do Sistema

Esta documentação detalha a arquitetura, padrões e decisões de design implementadas no SIGPS Backend.

---

## 1. Arquitetura do Sistema

O SIGPS é construído sobre o framework **FastAPI**, utilizando **SQLAlchemy (1.4/2.0 style)** como ORM para comunicação com o banco de dados **MySQL**.

### Camadas:
1.  **Core (`app/core/`)**: Contém a espinha dorsal do sistema.
    *   `config.py`: Gestão de variáveis de ambiente usando Pydantic Settings.
    *   `security.py`: Lógica de hashing de senhas (Bcrypt) e gestão de tokens JWT.
    *   `responses.py`: Utilitário para garantir que toda resposta da API seja consistente.
2.  **Database (`app/database/`)**:
    *   `db.py`: Configuração do Engine e Session local.
    *   `models.py`: Definição das tabelas do MySQL. Implementado com relacionamentos recursivos e cascatas de deleção.
3.  **Schemas (`app/schemas/`)**:
    *   Utiliza Pydantic para validação de entrada e serialização de saída (DTPs).
4.  **Routers (`app/routers/`)**:
    *   Implementação dos endpoints REST. Cada roteador é protegido por dependências de segurança (`deps.py`) que validam o perfil do usuário (RBAC).
5.  **ML (`app/ml/`)**:
    *   Módulo desacoplado para inferência de Machine Learning.
    *   `model.py`: Carrega modelos `.pkl` e fornece funções de previsão.

---

## 2. Padrões de Segurança (RBAC & JWT)

O sistema implementa **RBAC (Role-Based Access Control)** com 5 níveis:
1.  **Paciente**: Acesso a agendamentos próprios e filtros de especialistas.
2.  **Especialista**: Gestão da própria agenda e perfil.
3.  **Gestor**: Monitoria de fluxo e intervenção na fila.
4.  **Admin**: Gestão de usuários internos e parâmetros do sistema.
5.  **Visualizador**: Acesso somente leitura para auditoria e dashboards.

### Gestão de Sessão:
*   **Access Token**: 24h de validade (configurável).
*   **Refresh Token**: 7 dias de validade, armazenado no banco para permitir o "Force Logout" (revogação).

---

## 3. Lógica de Agendamento Automático com IA

O fluxo de agendamento automático é um diferencial do SIGPS:
1.  O paciente solicita uma sugestão (`POST /agendamentos/automatico`).
2.  O sistema processa as preferências e sugere um profissional.
3.  Um registro de agendamento é criado com status `sugestao` e `confirmado = False`.
4.  O agendamento só é efetivado quando o paciente chama `POST /agendamentos/confirmar/{id}`.

---

## 4. Priorização de Fila Inteligente

A priorização não é apenas por ordem de chegada:
*   **Acionamento**: Ao criar uma entrada na fila (`POST /fila/entrar`).
*   **Motor de Score**: O motor de ML calcula um peso baseado no perfil cadastrado do paciente.
*   **Ordenação**: O endpoint `GET /fila` retorna os pacientes ordenados de forma decrescente pelo score de prioridade.

---

## 5. Implementação de Resposta Padrão

Para facilitar a integração com o Frontend, utilizamos o `standard_response`:
*   **Sucesso**: Status HTTP 200-201.
*   **Erro**: Status HTTP 400-500, com objeto `error` contendo código interno para facilitar a tradução no Front.

```python
# Exemplo de erro retornado
{
    "success": false,
    "error": {
        "code": "HTTP_401",
        "message": "Token expirado"
    }
}
```

---

## 6. Guia para Novos Desenvolvedores (Do Zero ao Primeiro Endpoint)

1.  **Modelo**: Declare a nova tabela em `app/database/models.py`.
2.  **Schema**: Crie os modelos Pydantic em `app/schemas/`.
3.  **Router**: Crie um novo arquivo em `app/routers/` e registre-o no `app/main.py`.
4.  **Segurança**: Use `Depends(exigir_perfis(...))` para proteger o endpoint.
5.  **Resposta**: Utilize sempre a função `standard_response`.

---
*Documentação atualizada em: 28 de Fevereiro de 2026*
