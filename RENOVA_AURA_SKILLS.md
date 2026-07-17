# Renova Aura Agent Skills

Biblioteca central, reutilizável e pública de workflows para agentes de engenharia e produto da Renova Aura.

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
| `renova-aura-project-bootstrap` | Iniciar ou recuperar um projeto sem apagar trabalho existente |
| `renova-aura-product-spec` | Converter ideia em problema validado, MVP, PRD, SPEC e aceite |
| `renova-aura-engineering-guardian` | Preservar arquitetura, contratos, baixo acoplamento e evidência |
| `renova-aura-security-data-guardian` | Proteger autenticação, autorização, isolamento, LGPD, segredos e banco |
| `renova-aura-ux-design-system` | Criar interfaces coerentes, responsivas, acessíveis e verificáveis |
| `renova-aura-ai-integration-guardian` | Projetar IA com schemas, evals, custos, fallback e revisão humana |
| `renova-aura-quality-release` | Planejar testes, CI, release, deploy, rollback e critérios de bloqueio |
| `renova-aura-observability-incident` | Definir logs, métricas, alertas, resposta a incidentes e recuperação |
| `renova-aura-prompt-source-designer` | Criar prompts-fonte claros, modulares, versionáveis e avaliáveis |
| `renova-aura-project-handoff` | Atualizar documentação, estado real, próximos passos e continuidade |

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
