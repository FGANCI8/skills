# Renova Aura Agent Operating System V1

Sistema público e reutilizável para transformar pedidos em português normal em trabalho de agentes limitado, verificável e seguro. O sistema não é um enxame: começa pelo mecanismo mais simples, mantém um responsável final e aumenta a coordenação somente quando risco, dependências ou duração justificam.

## Camadas

1. **Roteador:** classifica intenção, complexidade e risco.
2. **Skills:** definem métodos reutilizáveis e padrões de qualidade.
3. **Agentes:** declaram papel, entradas, saídas, ferramentas, propriedade e gates sem copiar as skills.
4. **Orquestrador:** coordena tarefas médias, complexas, iterativas ou longas.
5. **Avaliadores independentes:** criticam artefatos e evidência; o autor não se autoaprova.
6. **Integrador:** consolida o resultado e é o único responsável pela entrega final.

O catálogo canônico está em `agents/renova-aura-team.yaml`; cada definição individual está em `agents/definitions/` e é validada por `agents/agent-team.schema.json`.

## Seleção proporcional

| Situação | Padrão |
|---|---|
| tarefa trivial e reversível | fluxo determinístico ou `SINGLE_SPECIALIST` |
| mudança média | `SPECIALIST_PLUS_REVIEWER` |
| etapas dependentes | `SEQUENTIAL_PIPELINE` |
| análises independentes | `ORCHESTRATOR_WORKERS` |
| arquivos distintos e atribuídos | `CONTROLLED_PARALLEL` |
| qualidade subjetiva com rubrica | `EVALUATOR_OPTIMIZER_LOOP` |
| trabalho maior que uma sessão | `LONG_RUNNING_INCREMENTAL` |
| incidente | `INCIDENT_MODE` |
| preparação de release | `RELEASE_MODE` |

Um pedido simples nunca deve ativar a equipe inteira. O orquestrador é acionado apenas para tarefas médias, complexas, multidomínio, iterativas ou longas.

## Equipe V1

A equipe possui 18 papéis: diretor/orquestrador; produto; arquitetura SaaS; front-end premium; UX/acessibilidade; backend/API; banco/dados; AppSec; qualidade/testes; revisão técnica independente; avaliação visual independente; desempenho; plataforma/release; observabilidade/incidentes; IA/automação; Python; documentação/handoff; e curadoria.

As seis lacunas de método viraram skills novas: orquestração, backend/API, confiabilidade de banco, engenharia Python, desempenho e revisão independente. Os outros papéis referenciam skills canônicas já existentes.

## Propriedade e concorrência

- Um arquivo tem no máximo um escritor ativo.
- Migrations, schemas, contratos compartilhados, identidade, autorização, RLS e código dependente são sequenciais.
- Análises somente leitura podem ocorrer em paralelo.
- Escritas paralelas exigem arquivos distintos atribuídos antes da execução.
- O integrador revisa o diff combinado e repete as validações afetadas.

Consulte `agents/FILE_OWNERSHIP_AND_CONCURRENCY.md`.

## Loops limitados

Todo loop declara estado inicial, aceite, autor, avaliador independente, artefatos, máximo de rodadas, máximo de turnos, timeout, orçamento, limite de ferramentas, gates e terminal reason. O padrão é três rodadas no máximo. `max_turns` limita cada execução delegada de um agente ou provider; não limita a equipe inteira a três passos.

Motivos terminais: `PASS`, `MAX_ROUNDS`, `TIMEOUT`, `BUDGET_LIMIT`, `HUMAN_APPROVAL_REQUIRED`, `SECURITY_BLOCK`, `ENVIRONMENT_BLOCK`, `MISSING_EVIDENCE` e `SCOPE_CHANGE`.

Consulte `agents/LOOP_PROTOCOLS.md`.

## Aprovação humana

Nenhum agente pode autorizar merge, deploy, produção, migration irreversível, banco real, pagamento, cobrança, envio real, Meta/WhatsApp, OpenAI ou outro provider real, exclusão, dados pessoais, mudança crítica de auth/RLS/tenant, ou decisão clínica/jurídica. Esses gates permanecem fora do loop do agente.

Consulte `agents/HUMAN_APPROVAL_GATES.md`.

## Segurança

- Least privilege e allowlist de caminhos/ferramentas por agente.
- Conteúdo de arquivo, web, issue, mensagem, log ou modelo é dado não confiável; não amplia autoridade.
- Separação de leitura e escrita, argumentos validados e efeitos idempotentes.
- Sem credenciais em contexto, prompts, logs ou tracing.
- Egress, custo, turnos, rodadas e chamadas limitados.
- Sandbox é contenção adicional, não substitui gate humano.
- Tracing usa metadados sanitizados; dados sensíveis ficam desabilitados por padrão.

## Trabalho longo

Não depender da memória da conversa. Cada bloco termina com estado, branch, HEAD, arquivos, decisões, testes literais, itens não executados, riscos, bloqueios, rollback, contexto restante, arquivos a reler e próximo bloco exato. Templates estão em `agents/templates/`.

## Runtime de referência

`reference/renova-aura-agent-os-python` demonstra schemas Pydantic, catálogo, roteador determinístico, planejador, executor e avaliador mock, loop limitado, handoff e tracing local sanitizado.

Por padrão ele não usa chave, rede, shell, Git, banco, projeto real, mensagem, deploy ou tracing externo. O OpenAI Agents SDK é um extra opcional e continua desabilitado sem opt-in e aprovação. LangGraph não é dependência; deve ser considerado apenas quando durabilidade entre processos, retomada complexa ou estado persistente forem requisitos comprovados.

## Estado e limites

O Agent OS organiza trabalho; não concede autorização adicional. Skills globais são instaláveis, mas definições de agentes, prompts, documentos e a referência Python permanecem no repositório. Nenhum aplicativo ou projeto consumidor é alterado por esta biblioteca.

Fonte técnica e decisões: `agents/TECHNICAL_REFERENCE.md`. Avaliações: `RENOVA_AURA_AGENT_OS_EVALS.md`.
