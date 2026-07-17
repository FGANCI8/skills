# Renova Aura skills inventory

Snapshot inicial: 2026-07-17. Este relatório é intencionalmente sanitizado para publicação. Caminhos privados, nomes de clientes, regras específicas de produtos e conteúdo proprietário permanecem no registro local ignorado pelo Git.

## Escopo inspecionado

- diretório global `%USERPROFILE%\.agents\skills`;
- padrões de backup `skills-backup-*` e `skills-backup-pdf-*`;
- workspace mestre e histórico da branch da draft PR;
- árvore de nomes de nove repositórios acessíveis, sem clone indiscriminado;
- oito raízes locais conhecidas, sem alteração de aplicações;
- catálogo, roteadores, skills, avaliações e instaladores da biblioteca.

O snapshot remoto encontrou três repositórios públicos e seis privados. A inspeção privada foi limitada a caminhos e documentos necessários para reconhecer processos genéricos.

## Skills globais antes da curadoria

| Pasta | Arquivos | Bytes | SHA-256 de `SKILL.md` | Função provável | Qualidade inicial | Duplicidade/conflito | Decisão |
|---|---:|---:|---|---|---|---|---|
| `renova-aura-fillable-pdf-architect` | 1 | 5.015 | `3B8C114765C0B414F0877D8173729C524FF5D2808FA0E7FE1CCF57AC8D2BAD5F` | autoria/reparo AcroForm | forte, sem metadados de interface | idêntica à branch | manter e completar pacote |
| `renova-aura-pdf-compatibility-auditor` | 1 | 6.456 | `5E0A8BA20E101982E64F47F3517BAF134BA7E7AB3A8960C902291C882BD48AF6` | auditoria de compatibilidade PDF | forte, sem metadados de interface | idêntica à branch | manter e completar pacote |
| `renova-aura-pdf-delivery-guardian` | 1 | 4.279 | `B9731CC7DCA9799FEF2E56ED446C83CAD4413E530E76494FF9FD1F515293B143` | entrega auditável de PDF | forte, sem metadados de interface | idêntica à branch | manter e completar pacote |
| `renova-aura-pdf-forms-router` | 1 | 5.106 | `D735E8AD7C7EF8ECD4BC42B951135BC303C269F9D75DF143ECDBD938ADF02942` | roteamento de PDF | forte, sem metadados de interface | idêntica à branch | manter e completar pacote |
| `renova-aura-pdf-viewer-validation-runbook` | 1 | 7.197 | `D3B11C6FD2B2C16DC993103DFB58A4489F54EDA7C6233DDD9F6784318BA09BB0` | validação manual de visualizador | forte, sem metadados de interface | idêntica à branch | manter e completar pacote |
| `renova-aura-saas-architect` | 1 | 1.463 | `C4221463CDC23A2C4DF6AC3CA3B9BC785FE3907F912FFD019C5007D06187408C` | arquitetura SaaS | válida, curta e ampla demais | global-only; sobrepunha roteador/engenharia/segurança | reescrever, delimitar e versionar |

Datas iniciais: a skill SaaS foi modificada em 2026-04-24; a suíte PDF em 2026-07-17. Não havia arquivos auxiliares nem backups compatíveis no início da execução.

## GitHub oficial

- repositório: `FGANCI8/skills`, público;
- `main` inicial: `ca1e7dc13c0ab5e2dfaa6de71991cd951b8f1cf2`;
- branch auditada: `agent/renova-aura-project-skills-v1`;
- HEAD inicial: `4d31c23834d06fc359d5bc4b36fb674f606e499c`;
- divergência inicial: 0 commits atrás, 32 à frente de `main`;
- draft PR #1 aberta, sem checks reportados e sem autorização de merge.

## Achados de duplicidade e conflito

1. As cinco skills PDF globais eram cópias exatas da branch; restauração de backup não era necessária.
2. A skill SaaS existia somente no diretório global e concentrava arquitetura, segurança, release e execução em um gatilho amplo.
3. O maior corpus local tinha 302 prompts. Havia uma duplicidade byte a byte limitada a sete pequenos arquivos de índice e forte sobreposição semântica entre roteadores, orquestradores e guardians.
4. Dois corpora de projeto compartilhavam 166 caminhos equivalentes, mas nenhum blob era idêntico; fusão automática seria insegura.
5. O instalador PDF sobrescrevia destinos sem dry-run, comparação, backup ou rollback.
6. A skill de UX existente cobria fluxo e acessibilidade, mas não definia uma identidade premium Renova Aura.
7. As skills não possuíam `agents/openai.yaml`, reduzindo descoberta e uso por linguagem natural em clientes compatíveis.

## Mapa canônico após curadoria

| Responsabilidade | Proprietário canônico |
|---|---|
| entrada em português normal | `renova-aura-router` |
| inventário, deduplicação, instalação e publicação | `renova-aura-skill-library-curator` |
| desenho de prompts e conteúdo de skills | `renova-aura-prompt-source-designer` |
| decisão de arquitetura do sistema | `renova-aura-saas-architect` |
| implementação e refatoração | `renova-aura-engineering-guardian` |
| segurança de aplicação, SaaS e dados | `renova-aura-security-data-guardian` |
| jornada, estados e acessibilidade | `renova-aura-ux-design-system` |
| identidade visual premium | `renova-aura-premium-frontend` |
| validação, release e rollback | `renova-aura-quality-release` |
| PDFs preenchíveis | `renova-aura-pdf-forms-router` e especialistas da suíte |

## Política de instalação

Somente skills com processo genérico, conteúdo público seguro, nome/descrição válidos, referências resolvidas, metadados de interface, avaliações e ausência de conflito canônico podem ser `GLOBAL_APPROVED`.

Adaptadores, schemas, decisões comerciais, comandos exclusivos, regras clínicas/jurídicas, integrações privadas e prompts com fatos de produto permanecem `PROJECT_ADAPTER` ou `PRIVATE_REFERENCE`.

O instalador oficial executa comparação, bloqueia divergência sem `-Replace`, cria backup com timestamp, usa cópia temporária, compara hashes e não instala adaptadores de projeto.

## Resultado da instalação global

- manifesto aprovado: 19 skills gerais, incluindo a suíte PDF;
- novas instalações: 13;
- substituições com backup: 6;
- backup: `%USERPROFILE%\.agents\skills-backup-20260717-184753`;
- correção de encoding de duas interfaces, com backup adicional em `%USERPROFILE%\.agents\skills-backup-20260717-184907`;
- verificação idempotente: 19 `UNCHANGED` na segunda execução;
- diretórios temporários residuais: 0;
- adaptadores de projeto instalados: 0.
