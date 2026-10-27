# Prompts 03 — Arquitetura, Segurança, IA e Privacidade

## P09 — Arquitetura, fronteiras e baixo acoplamento

```text
Analise a arquitetura implementada deste projeto. Leia estrutura, imports, rotas, serviços, repositories, adapters, banco, configurações, testes e documentação. Não proponha uma arquitetura ideal abstrata sem comparar com o código real.

Mapeie:
- módulos e responsabilidades;
- dependências e direção das chamadas;
- contratos de entrada/saída;
- regras de domínio e onde vivem;
- acesso a dados e providers;
- fronteiras de tenant, autenticação e autorização;
- side effects;
- pontos de acoplamento, duplicação e ciclos;
- módulos muito grandes ou sem owner;
- abstrações prematuras e camadas decorativas.

Classifique cada problema por impacto e custo. Prefira o menor diff que restaure um contrato claro. Não sugira microserviços, eventos, filas ou novas dependências sem necessidade comprovada.

Entregue arquitetura atual, fatos versus intenção documentada, riscos, decisões propostas, ADRs necessários, sequência incremental, testes de contrato e rollback.
```

## P10 — Segurança, tenant isolation, RBAC/RLS e LGPD

```text
Execute auditoria defensiva e somente leitura. Inspecione autenticação, sessão, autorização, papéis, ownership, tenant_id, RLS/policies, rotas administrativas, uploads, APIs, server actions, service role, logs, secrets, cache, exports e testes.

Modele atores e ativos. Teste mentalmente e, quando houver ambiente local seguro, por testes negativos:
- usuário anônimo;
- usuário de outro tenant;
- membro com papel insuficiente;
- objeto sem owner;
- ID previsível/IDOR;
- mass assignment;
- bypass por service role;
- filtro de tenant apenas na UI;
- upload malicioso;
- webhook forjado/replay;
- logs com PII ou token;
- prompt injection e exfiltração por IA;
- exportação ou exclusão sem autorização;
- cache compartilhado entre usuários.

Para cada achado, informe evidência, exploração possível sem executar dano, impacto, correção, teste de regressão e gate humano. Preserve minimização, finalidade, retenção, acesso, correção, portabilidade e exclusão da LGPD.

Não acesse secrets, banco real ou dados pessoais. Não altere produção. Entregue threat model, matriz de autorização, gaps, testes e plano priorizado.
```

## P11 — Integração de IA, evals, fallback e revisão humana

```text
Avalie uma funcionalidade de IA existente ou planejada neste projeto. Primeiro determine se IA é necessária; compare regra determinística, busca, formulário, classificação tradicional e intervenção humana.

Inspecione prompts, schemas, ferramentas, retrieval, dados, providers, custos, logs, testes e UX.

Defina:
- tarefa e decisão permitida;
- entradas, fontes autorizadas e dados proibidos;
- saída estruturada e validação no servidor;
- casos em que o modelo deve recusar, pedir confirmação ou escalar;
- dataset de evals representativo, adversarial e de regressão;
- métricas: precisão por campo, completude, groundedness, taxa de fallback, segurança, latência e custo;
- prompt injection, tool abuse, hallucination e data leakage;
- versionamento de prompt/modelo;
- timeout, retry e provider fallback;
- human-in-the-loop;
- observabilidade com redaction;
- comportamento sem IA.

Nunca trate uma demonstração como prova. Não envie dados reais a provider. Entregue decisão usar/não usar IA, contrato, eval plan, critérios de aprovação, fallback, custo estimado como hipótese e próximos passos.
```

## P12 — Privacidade, retenção, auditoria e exclusão

```text
Mapeie o ciclo de vida dos dados deste projeto: coleta, finalidade, base/consentimento quando aplicável, armazenamento, acesso, uso, compartilhamento, logs, backup, retenção, anonimização, exportação e exclusão.

Para cada categoria de dado, registre:
- entidade e campos;
- sensibilidade;
- titular e controlador operacional;
- finalidade;
- origem;
- quem acessa e por qual papel/tenant;
- onde é replicado;
- prazo e gatilho de retenção;
- procedimento de correção/exportação/exclusão;
- exceções legais ou operacionais a confirmar;
- evidência e testes.

Procure dados sem finalidade, PII em logs, retenção infinita, backup não considerado, exclusão que quebra auditoria, consentimento não versionado, compartilhamento não registrado e ambientes de teste com dados reais.

Não ofereça parecer jurídico. Separe requisito técnico, hipótese legal a validar e recomendação de produto. Entregue matriz, gaps, minimização, plano de retenção/redaction e testes.
```