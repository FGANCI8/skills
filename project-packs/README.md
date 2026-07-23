# Renova Aura — Biblioteca Operacional de Prompts, Skills e Agentes

Esta camada complementa a biblioteca-base da Renova Aura com o que faltava para transformar governança em resultado de produto:

- auditoria de requisitos, campos e dados ausentes;
- rastreabilidade entre jornada, tela, formulário, API, banco, integração e relatório;
- detecção de contratos incompletos entre módulos;
- seleção de prompts por estágio do projeto;
- pacotes específicos por produto e tecnologia;
- papéis especializados apenas quando há responsabilidade distinta.

## Regra central

Não executar todos os prompts em todos os projetos. O usuário informa o projeto, a dor e o estágio; o agente lê o repositório e seleciona o menor conjunto necessário.

## Estrutura

- `CATALOG.md`: catálogo completo e gatilhos.
- `USAGE.md`: como pedir em português normal.
- `PROJECT_MATRIX.md`: mapa de projetos GitHub e iniciativas planejadas.
- `prompts/`: prompts-fonte completos, agrupados por finalidade.
- `agents/`: papéis adicionais que não duplicam os agentes já existentes.
- `../skills/renova-aura-*/`: skills executáveis e verificáveis.

## Relação com a biblioteca-base

Esta branch parte de `agent/ra-skills-base-v1` e depende das 25 skills basais existentes. Ela não substitui:

- `renova-aura-router`;
- `renova-aura-product-spec`;
- `renova-aura-security-data-guardian`;
- `renova-aura-database-reliability`;
- `renova-aura-quality-release`;
- `renova-aura-observability-incident`;
- demais skills já catalogadas.

As novas skills tratam lacunas específicas que não estavam cobertas como comportamento próprio.

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

## Status

Esta camada é documentação e contratos de execução em branch draft. Presença no GitHub não comprova instalação, descoberta, ativação ou compatibilidade com uma ferramenta específica. Cada projeto deve validar localmente seu adaptador e suas skills.