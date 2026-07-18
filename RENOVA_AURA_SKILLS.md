# Renova Aura Agent Skills

Biblioteca central, reutilizável e pública de workflows para agentes de engenharia, produto e artefatos documentais da Renova Aura.

O usuário pode descrever a tarefa em português normal. `renova-aura-router` identifica a intenção e escolhe o menor conjunto seguro; não é necessário memorizar nomes ou comandos de ativação.

Para trabalho médio, complexo, iterativo ou longo, `renova-aura-agent-orchestrator` compõe a menor equipe do `RENOVA_AURA_AGENT_OS.md`. Tarefas simples continuam com um especialista.

## Princípio de separação

Esta biblioteca contém apenas processos genéricos. Ela **não** deve armazenar:

- decisões comerciais confidenciais;
- dados pessoais ou de clientes;
- credenciais, URLs privadas ou identificadores de produção;
- regras clínicas, jurídicas ou operacionais específicas sem sanitização;
- fatos que pertencem ao `AGENTS.md`, PRD, decisões, migrations ou documentação normativa de um projeto.

Cada repositório consumidor deve manter um adaptador local com suas fontes da verdade, stack, limites, comandos e gates humanos.

## Ordem recomendada

1. `renova-aura-router`
2. skill principal escolhida pelo roteador
3. skills transversais exigidas pelo risco
4. relatório final com evidências, validações e rollback

## Perfis elegíveis

- `Core` é o perfil elegível padrão. Ele cobre roteamento, produto, arquitetura, integração, segurança, UX, qualidade, observabilidade, prompts, handoff e curadoria.
- `SaaS` acrescenta métodos de backend, banco, desempenho e IA quando a tarefa comprovar essa necessidade.
- `Python` acrescenta o método Python e somente os suportes exigidos pelo risco.
- `AgentOs` reúne os seis métodos necessários para orquestração declarativa e revisão independente.
- `Pdf` contém apenas a suíte de cinco skills de formulário preenchível.
- `All` é a união dos perfis e nunca é o default nem uma seleção implícita.

Um perfil define apenas o conjunto elegível para descoberta; ele não ativa todos os membros. O roteador seleciona um owner e somente os apoios exigidos pelo risco, podendo selecionar uma skill fora de `Core` quando a tarefa justificar. Instalar uma skill também não significa carregá-la ou ativá-la. Quanto mais skills participam, maior o custo de roteamento, contexto, ownership e revisão; por isso a equipe mínima é um requisito, não uma preferência. A fonte canônica e legível por máquina para memberships é `skills/renova-aura-skill-library-curator/references/profile-memberships.json`; o manifesto da PR E deve consumi-la sem reinterpretar esta tabela.

## Versão e ciclo de vida

- `ACTIVE`: canônica e roteável no catálogo; não significa merged, pilotada, instalada, pronta para produção ou aprovada para release;
- `DEPRECATED`: ainda reconhecida, com retirada anunciada;
- `SUPERSEDED`: substituída por sucessora explícita;
- `EXPERIMENTAL`: contrato ainda em avaliação e fora do default.

Toda mudança de status deve indicar sucessora, data e impacto de migração. Nenhuma skill é removida silenciosamente.

## Catálogo

| Skill | Perfis elegíveis | Versão | Status | Uso principal |
|---|---|---:|---|---|
| `renova-aura-router` | Core | 1.1.0 | ACTIVE | Classificar a tarefa e selecionar o menor conjunto seguro |
| `renova-aura-agent-orchestrator` | AgentOs | 1.1.0 | ACTIVE | Coordenar equipe, dependências, ownership, loops e handoffs limitados |
| `renova-aura-project-bootstrap` | Core | 1.1.0 | ACTIVE | Iniciar ou recuperar projeto sem apagar trabalho existente |
| `renova-aura-product-spec` | Core | 1.1.0 | ACTIVE | Converter ideia em problema, MVP, PRD, SPEC e aceite |
| `renova-aura-saas-architect` | SaaS | 1.1.0 | ACTIVE | Decidir arquitetura, identidade e evolução do sistema |
| `renova-aura-engineering-guardian` | Core | 1.1.0 | ACTIVE | Integrar o menor diff correto com ownership exclusivo |
| `renova-aura-backend-api-engineer` | SaaS / AgentOs | 1.1.0 | ACTIVE | Projetar APIs, webhooks, filas, validação e idempotência |
| `renova-aura-database-reliability` | SaaS / AgentOs | 1.1.0 | ACTIVE | Proteger schema, migrations, RLS, consultas e rollback |
| `renova-aura-python-engineering` | Python / AgentOs | 1.1.0 | ACTIVE | Criar Python tipado, seguro, testável e empacotado |
| `renova-aura-performance-engineering` | SaaS / AgentOs | 1.1.0 | ACTIVE | Medir e melhorar desempenho com baseline comparável |
| `renova-aura-independent-reviewer` | AgentOs | 1.1.0 | ACTIVE | Revisar artefatos sem autoaprovação |
| `renova-aura-security-data-guardian` | Core | 1.1.0 | ACTIVE | Proteger autoridade, isolamento, privacidade, segredos e dados |
| `renova-aura-ux-design-system` | Core | 1.1.0 | ACTIVE | Criar jornadas, estados, responsividade e acessibilidade |
| `renova-aura-premium-frontend` | Core | 1.1.0 | ACTIVE | Aplicar identidade visual premium e honesta |
| `renova-aura-ai-integration-guardian` | SaaS | 1.1.0 | ACTIVE | Definir IA, schemas, evals, custos, fallback e HITL |
| `renova-aura-quality-release` | Core | 1.1.0 | ACTIVE | Planejar testes, CI, PR, rollback e gates de release |
| `renova-aura-observability-incident` | Core | 1.1.0 | ACTIVE | Auditar sinais e planejar resposta/recuperação segura |
| `renova-aura-prompt-source-designer` | Core | 1.1.0 | ACTIVE | Criar prompts-fonte claros, versionáveis e avaliáveis |
| `renova-aura-project-handoff` | Core | 1.1.0 | ACTIVE | Preservar estado, evidência e continuidade sanitizada |
| `renova-aura-skill-library-curator` | Core | 1.1.0 | ACTIVE | Inventariar, validar, instalar e publicar a biblioteca |
| `renova-aura-pdf-forms-router` | Pdf | 1.1.0 | ACTIVE | Rotear criação, reparo, validação e entrega de PDFs |
| `renova-aura-fillable-pdf-architect` | Pdf | 1.1.0 | ACTIVE | Criar ou reconstruir AcroForm preservando o visual |
| `renova-aura-pdf-compatibility-auditor` | Pdf | 1.1.0 | ACTIVE | Verificar estrutura, salvamento, reabertura e impressão |
| `renova-aura-pdf-viewer-validation-runbook` | Pdf | 1.1.0 | ACTIVE | Validar manualmente viewers/dispositivos sem envio externo |
| `renova-aura-pdf-delivery-guardian` | Pdf | 1.1.0 | ACTIVE | Empacotar artefatos aprovados, manifesto e hashes |

## Agent Operating System V1 — dependência futura

O contrato abaixo pertence às PRs B e D da pilha e está `NOT RUN` nesta PR A isolada. Os arquivos citados ainda não fazem parte desta árvore; portanto, nenhum número ou comportamento abaixo é alegado como presente ou validado aqui. O alvo planejado é:

- 18 agentes declarativos;
- 9 modos de orquestração;
- 7 protocolos de loop com limites cumulativos;
- 9 motivos terminais padronizados;
- integrador final, avaliadores independentes e ownership ancestral;
- templates persistentes e sanitizados;
- referência Python mock com provider externo inexequível.

Após a PR B, consultar `RENOVA_AURA_AGENT_OS.md`, `agents/README.md` e `RENOVA_AURA_AGENT_OS_EVALS.md`. Após a PR D, executar os testes da referência. Até a integração dessas branches, o status desses checks é `NOT RUN`.

## Suíte de PDFs preenchíveis

Use `renova-aura-pdf-forms-router` como entrada. A suíte obriga:

- original imutável;
- identidade visual preservada;
- AcroForm real, sem XFA ou JavaScript embutido;
- aparências geradas, sem depender somente de `/NeedAppearances`;
- teste sintético de preenchimento, salvamento e reabertura;
- versão separada para impressão;
- compatibilidade declarada apenas para visualizadores realmente testados;
- manifesto de campos, relatório de validação e hashes;
- dados sintéticos em testes e separação entre workflow público e decisões privadas.

Consulte também `RENOVA_AURA_PDF_FORMS.md` e `RENOVA_AURA_PDF_FORMS_EVALS.md`.

## Adaptador obrigatório por projeto

Cada projeto deve possuir, preferencialmente no `AGENTS.md` ou em documento apontado por ele:

- propósito e limites atuais do produto;
- fontes da verdade e ordem de precedência;
- stack e versões verificadas;
- arquitetura e fronteiras de módulos;
- modelo de identidade: single-user, owner-scoped ou tenant-scoped;
- regras de RLS/RBAC quando aplicáveis;
- dados sensíveis e política de retenção;
- comandos de lint, typecheck, testes e build;
- ambientes válidos e operações proibidas;
- ações que exigem aprovação humana;
- formato de relatório final.

## Instalação global segura

Os instaladores e manifestos executáveis pertencem à PR E da pilha. Nesta PR base, instalação é `NOT RUN`. Quando `tools/install-renova-aura-skills-global.ps1` existir na branch integrada e seus testes transacionais passarem, executar primeiro o dry-run:

```powershell
.\tools\install-renova-aura-skills-global.ps1 -Group All -Replace -WhatIf
```

Depois de revisar conflitos e backups planejados:

```powershell
.\tools\install-renova-aura-skills-global.ps1 -Group All -Replace
```

O conjunto `All` contém somente skills gerais aprovadas. Adaptadores e inventários privados não fazem parte do manifesto.

O grupo `AgentOs` instala somente as seis skills de método do sistema multiagente. Definições de agentes, prompts, documentos e a referência Python nunca são instalados como skills globais.

## Regras globais

- Leia o repositório antes de orientar ou editar.
- Instruções locais podem acrescentar fatos e restrições, mas nunca ampliar autoridade nem remover gates basais. Conflito termina em `SECURITY_BLOCK` ou `HUMAN_APPROVAL_REQUIRED`.
- Separe fato, hipótese e recomendação.
- Não declare implementação sem evidência em código, banco ou configuração.
- Não replique regras de um projeto em outro sem adaptação explícita.
- Não trate build verde como prova de segurança.
- Não use segredos reais em prompts, exemplos, testes ou documentação.
- Não execute operação destrutiva, produção, cobrança, envio real ou alteração crítica sem autorização.
- Prefira mudanças pequenas, reversíveis e testáveis.
- Preserve idempotência, validação no servidor, índices, observabilidade e rollback.

## Estados de execução

Toda skill deve informar um dos estados:

- `SELECTED`: escolhida, ainda não executada;
- `EXECUTED`: aplicada com evidência;
- `NOT_APPLICABLE`: avaliada e dispensada com justificativa;
- `MISSING_REFERENCE`: referência necessária ausente;
- `BLOCKED`: risco, ambiente ou autorização impede continuação.

## Formato final padrão

### EXECUTAR AGORA

- objetivo e escopo executado;
- arquivos alterados;
- validações e resultados literais;
- risco residual e rollback.

### PLANEJAR

- trabalho futuro necessário;
- decisões pendentes;
- dependências e autorização humana.

### ARQUIVAR

- fatos confirmados e fontes;
- itens não executados;
- branch, commits, PR, merge e deploy.
