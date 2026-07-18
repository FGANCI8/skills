# Technical reference and decisions

Pesquisa confirmada em 2026-07-17, somente em documentação oficial ou fonte primária. Versões são snapshots e devem ser verificadas novamente antes de integração real.

| Fonte | Versão/data | Padrão útil | Usar quando | Não usar quando | Custo | Decisão Renova Aura |
|---|---|---|---|---|---|---|
| [OpenAI Agents SDK Python](https://pypi.org/project/openai-agents/) | 0.18.2, 2026-07-11 | agents, tools, handoffs, guardrails, sessions, tracing, HITL | runtime agentic leve e controlado | workflow determinístico basta | médio | extra opcional; provider real desabilitado |
| [OpenAI multi-agent](https://openai.github.io/openai-agents-python/multi_agent/) | docs atuais | manager/agents-as-tools e handoffs | especialistas limitados com integrador | um especialista resolve | médio-alto | manager como padrão; handoff seletivo |
| [OpenAI handoffs](https://openai.github.io/openai-agents-python/handoffs/) | docs atuais | transferência tipada e filtrada para especialista | especialista precisa assumir a etapa | integrador deve manter a resposta final | médio | usar somente com contrato de handoff |
| [OpenAI agents](https://openai.github.io/openai-agents-python/agents/) | docs atuais | `output_type` e saídas estruturadas | rota, plano ou avaliação precisa ser validada | texto livre é suficiente | baixo-médio | Pydantic no runtime de referência |
| [OpenAI running agents](https://openai.github.io/openai-agents-python/running_agents/) | docs atuais | loop e `max_turns` | problema aberto com feedback | consulta simples | variável | limite explícito obrigatório |
| [OpenAI sessions](https://openai.github.io/openai-agents-python/sessions/) | docs atuais | estado entre turns e retomada | contexto conversacional precisa persistir | handoff em arquivo basta | médio | não persistir dado sensível por padrão |
| [OpenAI guardrails](https://openai.github.io/openai-agents-python/guardrails/) | docs atuais | validação de entrada e saída | boundary agentic precisa falhar cedo | substituir auth ou gate humano | médio | defesa adicional, nunca autorização |
| [OpenAI HITL](https://openai.github.io/openai-agents-python/human_in_the_loop/) | docs atuais | pausa, serialização e retomada | ação sensível exige decisão | ação segura/read-only | médio | gate fora do agente |
| [OpenAI tracing](https://openai.github.io/openai-agents-python/tracing/) | docs atuais | traces de run, tools e handoffs | depuração/evals sanitizados | dado sensível sem política | médio | sensitive data `false` por padrão |
| [OpenAI agent evals](https://developers.openai.com/api/docs/guides/agent-evals) | docs atuais | datasets, trace grading e avaliação reproduzível do workflow | comportamento agentic variável | um exemplo manual isolado | médio-alto | matriz sintética local agora; eval real somente em rodada separada |
| [OpenAI sandbox agents](https://openai.github.io/openai-agents-python/sandbox/guide/) | beta | workspace isolado | código não confiável com contenção | produção sem defesa adicional | alto | não usar como único controle |
| [Anthropic Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) | 2024-12-19 | workflow versus agente | escolher autonomia proporcional | complexidade por moda | variável | começar simples |
| [Anthropic multi-agent research](https://www.anthropic.com/engineering/multi-agent-research-system) | 2025-06-13 | orchestrator-workers e paralelo | pesquisa breadth-first | código com estado compartilhado | alto | paralelo somente independente |
| [Anthropic context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | 2025-09-29 | compaction, notas e subagentes | contexto longo | copiar contexto inteiro | médio | síntese e artefatos persistentes |
| [Anthropic Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) | 2025-10-16 | progressive disclosure | processo público reutilizável | fatos privados de projeto | baixo-médio | base da biblioteca |
| [Anthropic long-running harness](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) | 2025-11-26 | progresso incremental e handoff | trabalho excede sessão | tarefa curta | alto | ledger e checkpoint obrigatórios |
| [Anthropic agent evals](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) | 2026-01-09 | outcome, traces e trials | validar comportamento variável | um exemplo manual | médio-alto | matriz sintética e repetível |
| [Anthropic harness design](https://www.anthropic.com/engineering/harness-design-long-running-apps) | 2026-03-24 | planner-generator-evaluator | produto complexo e alto valor | manutenção comum | muito alto | modo premium, não padrão |
| [LangGraph workflows/agents](https://docs.langchain.com/oss/python/langgraph/workflows-agents) | 1.2.2 em 2026-05-26 | execução stateful e durable | retomada entre processos é requisito | estado simples basta | alto | não instalar por padrão |
| [LangGraph interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts) | docs atuais | HITL durável | pausa/reentrada complexa | side effect não idempotente antes do interrupt | alto | avaliar só com necessidade comprovada |
| [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/) | 5.0.0, 2025-05-30 | requisitos verificáveis | controles detalhados | alegar compliance por checklist | médio | baseline versionada |
| [OWASP Top 10](https://owasp.org/Top10/2025/0x00_2025-Introduction/) | edição 2025 | awareness de riscos web | priorização | substituir ASVS/threat model | baixo | contexto, não prova |
| [OWASP API Top 10](https://owasp.org/API-Security/editions/2023/en/0x00-header/) | edição 2023 | auth, recursos, fluxos, SSRF | APIs e ferramentas | aplicação sem API | médio | cobertura mínima de API |
| [NIST SP 800-218](https://csrc.nist.gov/pubs/sp/800/218/final) | SSDF 1.1, final 2022-02-03 | ciclo de software seguro | governança SDLC | alegar certificação | médio | baseline estável; 1.2 draft não substitui |
| [NIST SP 800-218A](https://csrc.nist.gov/pubs/sp/800/218/a/final) | final 2024-07-26 | práticas SSDF para IA | agentes/modelos/dados | software sem IA | médio | complemento obrigatório para IA |

## Decisões

1. Núcleo agnóstico de fornecedor e roteamento natural-language-first.
2. Workflow determinístico ou agente único por padrão.
3. Manager + specialists como tools quando um integrador deve reter controle.
4. Handoff somente quando a especialidade precisa assumir a próxima etapa.
5. Structured outputs para rota, plano, avaliação e handoff.
6. Máximo de três rodadas, timeout, orçamento, limite de ferramentas e stop reason.
7. HITL, least privilege, redaction e evals são requisitos.
8. Agents SDK é a primeira opção futura; LangGraph apenas para durabilidade comprovada.
9. Nenhuma dependência ou chamada real é necessária para validar a referência mock.
