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

## Catálogo

| Skill | Uso principal |
|---|---|
| `renova-aura-router` | Classificar a tarefa e selecionar o menor conjunto seguro de skills |
| `renova-aura-agent-orchestrator` | Coordenar equipe, dependências, ownership, loops e handoffs limitados |
| `renova-aura-project-bootstrap` | Iniciar ou recuperar um projeto sem apagar trabalho existente |
| `renova-aura-product-spec` | Converter ideia em problema validado, MVP, PRD, SPEC e aceite |
| `renova-aura-saas-architect` | Decidir arquitetura, limites, identidade e evolução do sistema |
| `renova-aura-engineering-guardian` | Preservar arquitetura, contratos, baixo acoplamento e evidência |
| `renova-aura-backend-api-engineer` | Projetar serviços, APIs, webhooks, filas, validação e idempotência |
| `renova-aura-database-reliability` | Proteger schema, migrations, constraints, RLS, consultas e rollback |
| `renova-aura-python-engineering` | Criar Python tipado, seguro, testável e empacotado |
| `renova-aura-performance-engineering` | Medir e melhorar desempenho com baseline comparável |
| `renova-aura-independent-reviewer` | Revisar diffs e evidências sem autoaprovação |
| `renova-aura-security-data-guardian` | Proteger autenticação, autorização, isolamento, LGPD, segredos e banco |
| `renova-aura-ux-design-system` | Criar interfaces coerentes, responsivas, acessíveis e verificáveis |
| `renova-aura-premium-frontend` | Aplicar identidade visual premium, contida, distinta e honesta |
| `renova-aura-ai-integration-guardian` | Projetar IA com schemas, evals, custos, fallback e revisão humana |
| `renova-aura-quality-release` | Planejar testes, CI, release, deploy, rollback e critérios de bloqueio |
| `renova-aura-observability-incident` | Definir logs, métricas, alertas, resposta a incidentes e recuperação |
| `renova-aura-prompt-source-designer` | Criar prompts-fonte claros, modulares, versionáveis e avaliáveis |
| `renova-aura-project-handoff` | Atualizar documentação, estado real, próximos passos e continuidade |
| `renova-aura-skill-library-curator` | Inventariar, deduplicar, validar, instalar e publicar a biblioteca |
| `renova-aura-pdf-forms-router` | Classificar criação, reparo, validação e entrega de PDFs preenchíveis |
| `renova-aura-fillable-pdf-architect` | Criar ou reconstruir AcroForm preservando o visual e a versão para impressão |
| `renova-aura-pdf-compatibility-auditor` | Verificar estrutura, salvamento, reabertura, impressão e compatibilidade por visualizador |
| `renova-aura-pdf-viewer-validation-runbook` | Executar validação manual e rastreável em visualizadores e dispositivos declarados |
| `renova-aura-pdf-delivery-guardian` | Empacotar PDF interativo, impressão, teste sintético, manifesto, relatório e hashes |

## Agent Operating System V1

- 18 agentes declarativos em `agents/definitions/`;
- 9 modos de orquestração;
- 7 protocolos de loop, com máximo padrão de 3 rodadas;
- 9 motivos terminais padronizados;
- um integrador final e avaliadores independentes;
- ownership exclusivo por arquivo;
- templates persistentes para handoff, ledger, decisões, arquivos e avaliações;
- referência Python mock, sem chave, rede ou side effects.

Consulte `RENOVA_AURA_AGENT_OS.md`, `agents/README.md` e `RENOVA_AURA_AGENT_OS_EVALS.md`.

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

Executar primeiro o dry-run:

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
