# Guia de Fluxo e Regras do Sistema SIGPS

Este documento explica de forma simples e detalhada como o SIGPS funciona na prática, quem são seus usuários e como a Inteligência Artificial toma as decisões.

---

## 1. Os Perfis do Sistema (Quem é quem?)

Existem 4 tipos de "chaves" (perfis) que determinam o que uma pessoa pode ver ou fazer no sistema:

### 🅰️ Admin (O Administrador)
*   **Quem é:** O responsável técnico ou diretor da unidade.
*   **O que faz:** Tem poder total. É o único que pode **treinar a Inteligência Artificial** com novos dados.
*   **Como ser um:** Ao criar a conta no `/auth/registrar`, deve-se enviar o campo `"perfil": "admin"`.

### 👤 Gestor (O Gerente)
*   **Quem é:** O coordenador clínico ou administrador do hospital.
*   **O que faz:** Gerencia a equipe (cadastra e edita Médicos/Especialistas), organiza as especialidades e acompanha o **Dashboard** com estatísticas em tempo real.
*   **Como ser um:** No cadastro, envie `"perfil": "gestor"`.

### 🏥 Paciente (O Usuário do Serviço)
*   **Quem é:** A pessoa que busca atendimento.
*   **O que faz:** Realiza seu próprio cadastro, insere seus dados socioeconômicos e faz o **check-in na fila**. Ele pode escolher um médico específico ou entrar na fila geral.
*   **Como ser um:** No cadastro, envie `"perfil": "paciente"`.

### 👁️ Visualizador (Acesso de Leitura)
*   **Quem é:** Um auditor ou estagiário.
*   **O que faz:** Apenas visualiza as listas, sem permissão para alterar nada ou entrar na fila.

---

## 2. A Inteligência Artificial (Nossa ML)

A grande diferença do SIGPS é que ele não atende por "ordem de chegada" simplesmente. Ele atende por **Urgência Social e Clínica**.

### As Regras da IA:
A nossa ML (Regressão Logística) analisa três pilares principais para dar uma nota de 0 a 100 para o paciente:
1.  **Idade:** Pessoas idosas recebem uma pontuação maior automaticamente.
2.  **Renda vs. Gastos:** A IA calcula o "Comprometimento de Renda". Se o paciente gasta muito do que ganha com sobrevivência, a IA entende que ele está em situação de vulnerabilidade e aumenta sua prioridade.
3.  **Score Automático:** Você não precisa pedir para a IA calcular. No momento em que o paciente entra na fila, o sistema faz o cálculo "por baixo dos panos" e já o coloca na posição correta.

---

## 3. Fluxo do Sistema (O Caminho do Usuário)

### Caso de Uso 1: O Paciente Crítico (Autoatendimento)
*   **Ação:** João (Paciente, 70 anos, baixa renda) cria sua conta e clica em "Entrar na Fila".
*   **O que acontece:** O sistema detecta que João é idoso e tem baixa renda. A IA gera um score de 95.
*   **Resultado:** João passa na frente de outros 10 pacientes que chegaram antes dele, mas que têm 20 anos e alta renda.

### Caso de Uso 2: O Gestor Organizando a Casa
*   **Ação:** O Gestor percebe que a fila de "Cardiologia" está muito grande.
*   **O que acontece:** Ele acessa o Dashboard, vê os números e decide cadastrar um novo Médico Especialista para ajudar na demanda.
*   **Resultado:** O sistema passa a oferecer esse novo médico como opção de transbordo para os pacientes.

### Caso de Uso 3: O Admin Atualizando o Cérebro
*   **Ação:** O Admin percebe que os critérios de prioridade mudaram (ex: nova lei de saúde).
*   **O que acontece:** Ele envia novos dados de exemplo e chama a função de "Treinar Modelo" no `/ia/treinar`.
*   **Resultado:** A partir desse instante, a IA passa a seguir as novas regras de priorização para todos os novos pacientes.

---

## 4. Como as coisas acontecem (Resumo por escrito)

1.  **Ingresso:** O usuário faz seu **Cadastro** e **Login**. Ele recebe um token JWT (seu crachá).
2.  **Preparação:** O perfil `paciente` preenche seus dados socioeconômicos.
3.  **Ação de Fila:** O `paciente` solicita entrada na fila. 
    - O sistema busca os dados do paciente.
    - O sistema pergunta para a ML: "Qual a nota desse paciente?".
    - A ML responde (ex: 85).
    - O paciente é salvo na fila com o `score_ml = 0.85`.
4.  **Espera Inteligente:** A lista de espera que os médicos veem está sempre ordenada do maior score para o menor.
5.  **Atendimento:** O médico chama o paciente do topo. O status da fila muda para "Atendido" e o ciclo se fecha.

---
**Este fluxo garante que o SIGPS seja um sistema justo, rápido e sem necessidade de balcão de recepção humano.**
