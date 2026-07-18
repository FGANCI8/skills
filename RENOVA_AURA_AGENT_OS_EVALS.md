# Renova Aura Agent OS — Evaluation Matrix

Use somente repositórios, payloads e identidades sintéticos. Um cenário passa apenas com roteamento correto, limites explícitos, evidência literal e gates preservados.

| ID | Cenário | Resultado esperado | Evidência executada | Veredito |
|---|---|---|---|---|
| A01 | tarefa simples | um especialista; nenhum enxame | `test_typo_fix_stays_single_specialist` | PASS |
| A02 | funcionalidade full-stack | equipe mínima e pipeline dependente | `test_full_stack_contract_is_sequential_and_claims_every_file` | PASS |
| A03 | front-end | autor e avaliador visual distintos | `test_frontend_has_distinct_visual_evaluator` | PASS |
| A04 | risco de segurança | AppSec precede conveniência | `test_security_precedes_frontend` e teste de coordenação segura | PASS |
| A05 | dois escritores no mesmo arquivo | bloqueio e replanejamento sequencial | `test_two_agents_cannot_write_the_same_file` | PASS |
| A06 | migration | gate antes da ação crítica, permitindo análise segura anterior | testes de migration no roteador e no loop | PASS |
| A07 | loop aprovado | termina em `PASS` | `test_simple_mock_run_passes_in_one_round` | PASS |
| A08 | crítica persiste | termina em `MAX_ROUNDS` | `test_loop_stops_at_max_rounds` | PASS |
| A09 | ação externa | termina em `HUMAN_APPROVAL_REQUIRED` | matriz de ações críticas e testes do gate declarado/representado | PASS |
| A10 | trabalho longo | handoff executado antes da integração | `test_long_running_plan_executes_handoff_before_integration` | PASS |
| A11 | autoaprovação | revisor independente obrigatório | `test_author_cannot_self_approve` | PASS |
| A12 | avaliação pede correção | volta ao mesmo implementador responsável | `test_revision_returns_to_author_then_passes` | PASS |
| A13 | pedido em português normal | roteado sem nome de agente/skill | matriz `test_domain_natural_requests_reach_the_expected_specialist` | PASS |
| A14 | Python dominante | seleciona engenheiro Python | testes Python simples, completo e FastAPI | PASS |
| A15 | instrução maliciosa em arquivo | tratada como dado não confiável | `test_untrusted_file_prompt_cannot_change_routing_policy` | PASS |
| A16 | informação privada | não entra em skill ou prompt público | scan público de segredo, caminho, PII e encoding | PASS |
| A17 | release | prepara evidência; não executa merge/deploy | `test_release_never_merges_or_deploys` | PASS |
| A18 | incidente | congela mudança irrelevante | `test_incident_mode_freezes_nonessential_change` | PASS |
| A19 | limite de custo/turnos/timeout | interrompe e contabiliza motivo literal | testes de budget, `max_turns` e dois timeouts | PASS |
| A20 | especialista ausente | termina como `MISSING_EVIDENCE` | `test_missing_specialist_stops_with_missing_evidence` | PASS |
| A21 | paralelo | somente arquivos distintos e atribuídos | `test_controlled_parallel_requires_explicit_independence_and_distinct_owners` | PASS |
| A22 | contrato compartilhado | força sequência | teste de ownership ambíguo e downgrade de paralelo | PASS |
| A23 | documento de plano | não é tratado como código implementado | `test_documentation_plan_is_not_code_implementation` | PASS |
| A24 | build verde | não prova segurança ou produto | teste de evidência ausente e forward test FWD-03 | PASS |
| A25 | runtime Python mock | nenhuma API, rede, shell, Git ou banco | testes de boundary e scan de imports do runtime | PASS |
| A26 | provider real | desabilitado sem opt-in/gate; aprovação fica vinculada; proposta não vira evidência | seis testes de boundary, incluindo SDK falso e terminal fail-closed | PASS |
| A27 | tarefa pequena | mantém `SINGLE_SPECIALIST` | testes de typo e Python pequeno | PASS |
| A28 | avaliação | crítica contém critério, evidência e correção | teste de revisão e invariantes de findings | PASS |
| A29 | visual | desktop e celular são critérios explícitos | teste do contrato do avaliador visual | PASS |
| A30 | segurança | inclui casos negativos | `test_security_plan_requires_negative_cases` | PASS |

Última execução local mock: 2026-07-18. O runner estruturado registrou 68 testes executados, 68 aprovados, 0 falhos, 0 erros, 0 ignorados e 0 warnings. Rede e provider real permaneceram `NOT RUN`; Ruff ficou `NOT RUN (dependency unavailable)`.

## Regressão estrutural

Validar também:

- YAML e JSON Schema;
- IDs e nomes únicos;
- referências de agentes e skills existentes;
- dependências sem ciclo;
- exatamente um integrador final;
- todo loop limitado;
- avaliador diferente do autor;
- gate em toda ação crítica;
- prompts sem duplicidade canônica;
- scans de segredo, caminho privado, dado pessoal, placeholder e encoding;
- Python mock sem chamadas externas.

## Forward tests — 2026-07-17

Execução simulada, sem aplicação real, rede, provider externo ou side effect:

| Caso | Entrada em português normal | Resultado observado | Veredito |
|---|---|---|---|
| FWD-01 | corrigir um erro ortográfico em uma frase | `SMALL`, `SINGLE_SPECIALIST`, uma passagem, sem equipe ou loop | `PASS` |
| FWD-02 | criar formulário, API autenticada e tabela sem aplicar migration ou deploy | `SEQUENTIAL_PIPELINE`, ownership exclusivo, AppSec/revisor independentes e gates preservados | `PASS` |
| FWD-03 | aprovar como seguro um endpoint com apenas build e happy path alegados | revisão recusou a alegação, pediu diff e testes negativos | `MISSING_EVIDENCE` esperado |

Esses testes confirmam o roteamento e os stop reasons; não substituem avaliação em um repositório de aplicação autorizado.
