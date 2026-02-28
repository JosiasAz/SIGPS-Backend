# Guia de Fluxo e Regras do Sistema SIGPS

Este documento explica de forma simples e detalhada como o SIGPS funciona na prática, quem são seus usuários e como a Inteligência Artificial toma as decisões.

---

## 1. Os Perfis do Sistema (Quem é quem?)

Existem **5 tipos** de "chaves" (perfis) que determinam o que uma pessoa pode ver ou fazer no sistema:

### 🅰️ Admin (O Administrador)
*   **Quem é:** O responsável técnico ou diretor da unidade.
*   **O que faz:** Tem poder total. Gerencia todos os usuários e parâmetros do sistema.

### 👤 Gestor (O Gerente)
*   **Quem é:** O coordenador clínico ou administrador.
*   **O que faz:** Monitora o fluxo de pacientes, intervém na fila se necessário e acompanha o **Dashboard** analítico.

### 🏥 Paciente (O Usuário do Serviço)
*   **Quem é:** A pessoa que busca atendimento.
*   **O que faz:** Realiza seu próprio cadastro, escolhe especialistas e entra na **Lista de Espera**.

### 🩺 Especialista (O Profissional de Saúde)
*   **Quem é:** Médicos, psicólogos, nutricionistas, etc.
*   **O que faz:** Gerencia seu perfil público e sua própria agenda de horários.

### 👁️ Visualizador (Acesso de Leitura)
*   **Quem é:** Um auditor ou estagiário.
*   **O que faz:** Apenas visualiza relatórios e dashboards, sem permissão para alterações.

---

## 2. A Inteligência Artificial (Nossa ML)

A grande diferença do SIGPS é que ele não atende apenas por "ordem de chegada". Ele utiliza **Priorização Inteligente**.

### Como a IA toma decisões:
Nosso modelo de Machine Learning analisa critérios para definir uma nota de 0 a 100:
1.  **Perfil Clínico e Social:** Idade e vulnerabilidade socioeconômica (renda vs gastos).
2.  **Urgência Declarada:** O motivo do atendimento e a urgência apontada pelo paciente.
3.  **Sugestão de Horário:** Ao invés de o paciente procurar um horário, a IA pode sugerir o profissional mais adequado e livre mais rapidamente.

---

## 3. Fluxos Principais

### A. Agendamento Automático (O "Match" da Saúde)
1.  **Solicitação:** O paciente pede um horário via modo automático.
2.  **Sugestão:** A IA encontra o melhor especialista e horário disponível.
3.  **Confirmação:** O sistema reserva o horário, mas ele só é oficializado quando o **paciente clica em "Confirmar"**. Isso evita faltas e horários presos.

### B. Entrada na Fila (Self-Service)
1.  **Check-in:** O paciente faz a entrada na fila pelo celular/totem.
2.  **Score Instantâneo:** O backend calcula a prioridade segundos depois da entrada.
3.  **Ordenação Dinâmica:** A lista dos profissionais se reordena automaticamente. Quem é mais urgente sempre "sobe" na lista.

---

## 4. Segurança e Sessão (O Login Seguro)

O SIGPS usa tecnologia de ponta para proteger os dados:
*   **Tokens de Acesso:** São como crachás digitais que expiram rapidamente para sua segurança.
*   **Refresh Tokens:** Permitem que você continue logado no app sem precisar digitar a senha toda hora, mas podem ser cancelados remotamente pelo Admin se você perder o celular (**Logout Global**).

---

## 5. Regras Críticas

*   **Privacidade:** Um paciente nunca consegue ver os dados de outro paciente.
*   **Humanização:** Embora a IA sugira, o humano (gestor) sempre tem a palavra final para ajustes manuais na fila em casos excepcionais.
*   **Transparência:** Todas as ações críticas (como mudar a prioridade de alguém) são gravadas em logs de auditoria.

---
**SIGPS — Tecnologia a serviço da vida.**
