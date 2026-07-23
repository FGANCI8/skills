# Catálogo Mestre — Renova Aura

## Prompts universais

| ID | Prompt | Use quando | Resultado |
|---|---|---|---|
| P01 | Diagnóstico de produto, MVP e corte de escopo | há muitas ideias, telas ou funcionalidades | manter, simplificar, adiar, arquivar e não construir |
| P02 | Rastreabilidade de requisitos e aceite | requisitos não estão ligados ao código e aos testes | matriz requisito → fluxo → arquivo → teste → evidência |
| P03 | Jornada, estados e exceções | o fluxo feliz existe, mas erros e retomadas estão nebulosos | mapa de estados, vazios, erros, cancelamentos e recuperação |
| P04 | Prontidão comercial e operacional | o produto funciona, mas ainda não está vendável ou operável | gaps de onboarding, suporte, métricas, limites e implantação |
| P05 | Cobertura de campos, dados e integrações | suspeita de campo ausente ou dado que não chega ao destino | inventário de campos e contratos ponta a ponta |
| P06 | Regras de domínio e invariantes | regras estão espalhadas em UI, banco e automações | catálogo de invariantes, estados válidos e validações no servidor |
| P07 | Banco, schema, migrations e integridade | há tabelas, migrations ou RLS em evolução | gaps de schema, constraints, índices, ownership e rollback |
| P08 | APIs, webhooks, filas e idempotência | integrações podem duplicar, falhar ou chegar fora de ordem | contratos, retry, timeout, deduplicação e reconciliação |
| P09 | Arquitetura, fronteiras e acoplamento | módulos cresceram sem limites claros | mapa de dependências, contratos e menor refatoração segura |
| P10 | Segurança, tenant isolation, RBAC/RLS e LGPD | há autenticação, dados pessoais ou multi-tenant | ameaças, testes negativos, gates e plano de correção |
| P11 | IA, evals, fallback e revisão humana | existe ou será criada uma função com modelo de IA | dataset, métricas, riscos, custo, latência e fallback |
| P12 | Privacidade, retenção, auditoria e exclusão | há PII, dados sensíveis ou obrigação de trilha | ciclo de vida dos dados e evidência de conformidade |
| P13 | Testes orientados a risco | há testes, mas não se sabe se protegem o essencial | matriz de risco e suíte mínima útil |
| P14 | Release, rollout e rollback | a mudança está perto de publicação | checklist, bloqueios, smoke test e retorno seguro |
| P15 | Observabilidade e incidentes | falhas são difíceis de localizar | eventos, logs, métricas, alertas e runbook |
| P16 | Desempenho e custo | o produto pode ficar lento ou caro | baseline, gargalos, orçamento e critérios de regressão |
| P17 | UX, acessibilidade e mobile | telas existem, mas podem estar incompletas ou difíceis | auditoria de jornada, estados, responsividade e acessibilidade |

## Prompts por tecnologia ou canal

| ID | Prompt | Projetos principais |
|---|---|---|
| T01 | Next.js/React/Supabase | Zuno, PetShop Pro, Negociação Blindada, Aura Shop |
| T02 | Python/FastAPI/Postgres | Aura Clínica Engine e automações Python |
| T03 | Android/Kotlin/Compose | FalaOrça Android e futuros aplicativos nativos |
| T04 | WhatsApp/CRM/webhooks | Vocero, Aura Clínica, FalaOrça, Aura Shop, Zuno |
| T05 | Voz, transcrição e extração estruturada | FalaOrça e produtos de orçamento/lead por voz |
| T06 | PDF, formulários e documentos | Negociação Blindada, clínica, propostas e matrizes preenchíveis |

## Novas skills desta camada

| Skill | Responsabilidade exclusiva |
|---|---|
| `renova-aura-requirements-completeness-auditor` | provar cobertura dos requisitos e detectar omissões |
| `renova-aura-data-contract-field-auditor` | rastrear cada campo da origem ao armazenamento, uso e saída |
| `renova-aura-workflow-integration-auditor` | validar contratos entre módulos, providers e eventos |
| `renova-aura-domain-invariant-guardian` | identificar e proteger regras de domínio e estados impossíveis |
| `renova-aura-android-kotlin-engineering` | arquitetura e qualidade específicas de Android/Kotlin |
| `renova-aura-whatsapp-automation-reliability` | confiabilidade de webhooks, outbox, janela, templates e handoff |
| `renova-aura-voice-ai-evaluation` | qualidade de áudio, STT, extração, confirmação e evals |
| `renova-aura-accessibility-mobile-qa` | acessibilidade, teclado, leitor de tela, toque e viewports reais |

## Novos papéis de agente

| Agente | Quando existe função distinta |
|---|---|
| Requirements Completeness Analyst | inventário e rastreabilidade de requisitos |
| Data Contract Integration Reviewer | contratos de campos, APIs, banco e integrações |
| Android Kotlin Engineer | aplicativo Android nativo |
| Messaging Reliability Engineer | WhatsApp, webhooks, outbox e entrega |

## Ordem recomendada por estágio

- **Ideia/protótipo:** P01 → P03 → P05 → P17.
- **Arquitetura em definição:** P02 → P05 → P06 → P09 → P10.
- **Banco/backend em construção:** P05 → P06 → P07 → P08 → P13.
- **IA/voz:** P05 → P08 → P11 → T05 → P13.
- **Pré-release:** P02 → P10 → P13 → P14 → P15.
- **Operação:** P15 → P16 → P12 → revisão periódica de P05.

O roteador deve reduzir essa sequência ao conjunto mínimo necessário para a solicitação real.