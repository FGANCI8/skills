# Renova Aura — ProjectPacks

`ProjectPacks` é uma camada especializada do Renova Aura Agent OS 1.1. Ela complementa a biblioteca-base com:

- auditoria de requisitos, campos e dados ausentes;
- rastreabilidade entre jornada, tela, formulário, API, banco, integração e relatório;
- detecção de contratos incompletos entre módulos;
- seleção de prompts por estágio do projeto;
- pacotes específicos por produto e tecnologia;
- quatro project adapters para contextos que exigem responsabilidade distinta.

O conjunto contém cinco arquivos de prompts com 23 IDs (`P01`–`P17` e `T01`–`T06`), oito extension skills no profile `ProjectPacks` e quatro project adapters. A biblioteca combinada permanece em 25 skills basais + 8 extensions, sem sobreposição, totalizando 33 IDs únicos.

## Regra central

Não executar todos os prompts, skills, agentes ou adapters em todos os projetos. O roteador/orquestrador escolhe o menor conjunto necessário para a tarefa, o risco e o estágio comprovados.

## Estrutura

- `CATALOG.md`: catálogo completo e gatilhos.
- `USAGE.md`: como pedir em português normal.
- `PROJECT_MATRIX.md`: mapa de projetos GitHub e iniciativas planejadas.
- `prompts/`: prompts-fonte completos, agrupados por finalidade.
- `agents/`: quatro project adapters, fora do registry canônico de agentes.
- `../skills/renova-aura-*/`: skills executáveis e verificáveis.
- `MANIFEST.json`: inventário estrutural e versão do conjunto.

## Relação com Agent OS 1.1

O Agent OS permanece a fonte central de autoridade, routing, ownership, revisão e gates. Seu registry contém 18 agentes canônicos e exatamente um accountable integrator (`technical-director-orchestrator`). Os quatro project adapters:

- `requirements-completeness-analyst`;
- `data-contract-integration-reviewer`;
- `android-kotlin-engineer`;
- `messaging-reliability-engineer`.

não fazem parte desses 18 agentes. As oito extension skills também não se tornam agentes. `ProjectPacks` não cria um segundo Agent OS, outro accountable integrator ou autoridade paralela.

Todos permanecem subordinados a `RA-AUTH-BASELINE-1`. Instruções locais podem restringir a autoridade basal, nunca ampliá-la. Handoffs transmitem estado e evidência; não concedem autoridade, não reabrem gates e não autorizam merge, push ou deploy. Revisão por IA não substitui autorização humana.

## Modos de uso

1. **Diagnóstico somente leitura**: inventaria e classifica lacunas sem alterar aplicação.
2. **Planejamento**: produz PRD, SPEC, contratos, backlog e aceite.
3. **Implementação controlada**: somente após evidência, escopo e gates definidos.
4. **Revisão**: compara implementação com requisitos e evidências.
5. **Operação**: release, observabilidade, incidente e rollback.

## Segurança

- Ler o repositório, instruções locais, memória e configurações antes de orientar mudanças.
- Não usar documentação como prova de implementação.
- Não acessar ou publicar secrets, PII ou dados reais.
- Não executar deploy, migration remota, mensagem real, pagamento, merge ou alteração de produção sem aprovação explícita e verificável.
- Manter tenant isolation, RLS/RBAC, LGPD, validação no servidor, idempotência, índices, logs, testes e rollback.
- Respeitar a tool policy canônica: default deny, escrita somente com claim explícito, rede externa negada, provider real proibido no V1.1 e produção negada.
- Submeter merge, deploy, produção, autenticação/autorização, RLS/tenant, dados sensíveis, providers reais, pagamento e ações irreversíveis aos gates humanos do Agent OS.

## Status

`LOCAL_DRAFT_PRE_PUBLICATION`

No manifesto, `version: 1.1.0-draft` identifica o conteúdo do conjunto e `schema_version: 1.1.0` identifica o formato estrutural. Draft não significa release, merge, publicação final, instalação, descoberta, runtime ou produção. Destino, licença e distribuição permanecem em `PENDING_PUBLICATION_GOVERNANCE_DECISION`.
