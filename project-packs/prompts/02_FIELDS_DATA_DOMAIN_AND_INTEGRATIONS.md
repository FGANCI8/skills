# Prompts 02 — Campos, Dados, Domínio e Integrações

## P05 — Auditoria de cobertura de campos, dados e integrações

```text
Você está auditando o repositório real deste projeto da Renova Aura para descobrir campos, dados, relações ou contratos que estejam faltando, inconsistentes, duplicados ou sem uso. Este é um diagnóstico somente leitura.

Antes de responder, leia instruções locais, memória, PRD/SPEC, formulários, componentes, schemas de validação, tipos, APIs, serviços, repositories, migrations, tabelas, RLS/RBAC, integrações, relatórios, exports e testes.

Não use somente os exemplos do usuário. Descubra o domínio completo.

Para cada entidade e jornada crítica:
1. Liste os campos necessários para identificar, operar, buscar, filtrar, relacionar, auditar e integrar o registro.
2. Rastreie cada campo ponta a ponta: origem → captura → normalização → validação no servidor → autorização → persistência → leitura → edição → busca/filtro → integração → relatório/exportação → retenção/exclusão.
3. Registre nome em cada camada, tipo, formato, obrigatoriedade, default, enum, unidade, timezone, precisão, nullability, unicidade, índice, foreign key, ownership/tenant, sensibilidade e fonte da verdade.
4. Procure campos presentes na UI e ausentes no banco; presentes no banco e nunca capturados; enviados por API e ignorados; derivados sem regra; duplicados com nomes diferentes; obrigatórios somente no cliente; armazenados sem finalidade; e campos necessários para integrações futuras já assumidas pelo produto.
5. Analise relações e não apenas colunas: endereço↔geocodificação, usuário↔organização, item↔preço, pedido↔pagamento, contato↔consentimento, mensagem↔delivery, documento↔versão, evento↔idempotency key.
6. Verifique campos técnicos: created_at, updated_at, created_by, version, status, reason, source, external_id, correlation_id, idempotency_key, audit metadata e soft delete, somente quando o domínio justificar.
7. Não recomende coletar dado sem necessidade. Aplique minimização de dados e LGPD.

Classifique cada achado:
- BLOCKER: fluxo ou integração não funciona;
- HIGH: risco de dado errado, vazamento, duplicação ou operação manual crítica;
- MEDIUM: perda de qualidade, busca, relatório ou manutenção;
- LOW: melhoria futura;
- NOT_NEEDED: campo sugerido, mas sem finalidade legítima.

Entregue:
- entidades e jornadas auditadas;
- matriz campo por camada;
- campos ausentes e campos excessivos;
- divergências de nome/tipo/obrigatoriedade;
- integrações quebradas ou incompletas;
- impacto e evidência por achado;
- proposta de contrato canônico;
- arquivos/tabelas afetados;
- testes necessários;
- plano em EXECUTAR AGORA / PLANEJAR / ARQUIVAR.

Não altere banco, migration, aplicação ou produção nesta etapa.
```

## P06 — Regras de domínio, invariantes e estados impossíveis

```text
Inspecione o projeto e identifique as regras que precisam permanecer verdadeiras independentemente de tela, API, automação ou agente de IA.

Para cada entidade e processo, determine:
- estados permitidos e transições;
- pré-condições e pós-condições;
- cálculos, unidades, arredondamentos e datas;
- ownership, papéis e tenant;
- unicidade e concorrência;
- relações obrigatórias;
- ações reversíveis e irreversíveis;
- eventos que podem ocorrer uma única vez;
- situações proibidas;
- regras atualmente apenas na UI;
- regras conflitantes entre documentação, código e banco.

Transforme regras em invariantes testáveis. Indique onde cada uma deve ser aplicada: constraint, transaction, service, schema de servidor, policy/RLS, state machine ou teste. Não mova regra para banco ou código sem justificar fronteira e rollback.

Entregue catálogo de invariantes, estados impossíveis encontrados, risco, evidência, owner técnico e matriz de testes positivos, negativos e de concorrência.
```

## P07 — Banco, schema, migrations e integridade

```text
Faça uma auditoria somente leitura do banco e do contrato de dados. Leia migrations em ordem, schema atual, ORM/types, queries, seeds, RLS/policies, testes e documentação.

Verifique:
- alinhamento schema↔código↔documentação;
- primary/foreign keys e comportamento de delete/update;
- nullability, defaults, checks, enums e unicidade;
- tenant_id/owner e isolamento;
- índices para filtros, joins, ordenação e unicidade;
- timestamps, timezone e versionamento;
- valores monetários e unidades;
- migrations idempotentes, ordem, lock, backfill e rollback;
- concorrência, transações e race conditions;
- soft delete, retenção, anonimização e auditoria;
- dados derivados e fonte da verdade;
- service role ou bypass indevido;
- testes de RLS e acesso negativo.

Não execute migration remota nem use banco real. Entregue gaps por severidade, queries/migrations afetadas, estratégia segura, testes locais, plano de rollback e itens que precisam de aprovação humana.
```

## P08 — APIs, webhooks, filas e idempotência

```text
Audite todas as fronteiras assíncronas e integrações externas deste projeto.

Para cada endpoint, webhook, job, fila, outbox ou provider, registre:
- produtor e consumidor;
- autenticação, assinatura e replay protection;
- schema e versionamento;
- external_id, correlation_id e idempotency_key;
- ordem de eventos e deduplicação;
- timeout, retry, backoff e limite;
- resposta parcial e compensação;
- estados de delivery;
- persistência antes/depois do side effect;
- dead letter ou reconciliação;
- observabilidade e redaction;
- rate limit e abuso;
- comportamento quando provider está indisponível;
- teste sem chamada real.

Procure efeitos duplicados, acknowledge precoce, retry não seguro, eventos ignorados, falha silenciosa, payload não validado, status conflituoso e dependência de memória local.

Entregue diagrama de sequência, contratos, gaps, estratégia de idempotência, testes de duplicação/ordem/falha, runbook de reconciliação e plano mínimo de correção. Não envie mensagens nem conecte providers reais.
```