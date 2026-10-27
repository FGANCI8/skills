# Prompts 04 — Qualidade, Release, Operação e UX

## P13 — Testes orientados a risco

```text
Não crie testes por quantidade ou cobertura superficial. Leia requisitos, fluxos críticos, código, banco, integrações, incidentes e testes existentes.

Construa uma matriz de risco com probabilidade, impacto e detectabilidade. Priorize:
- autenticação, autorização, tenant e RLS;
- criação/edição/exclusão de dados;
- cálculos e estados;
- pagamentos e side effects;
- webhooks, retries e idempotência;
- IA e extração de dados;
- dados sensíveis;
- regressões já ocorridas;
- jornada principal em mobile.

Para cada risco, escolha o nível correto: unitário, contrato, integração, banco, segurança, E2E, acessibilidade, visual, performance ou smoke. Identifique testes frágeis, duplicados, sem assert útil e que passam sem exercitar o comportamento.

Entregue suíte mínima priorizada, cenários positivos/negativos/concorrência, fixtures sintéticas, comandos, evidência esperada e critérios de bloqueio. Não use banco ou provider real sem aprovação.
```

## P14 — Release, rollout, smoke test e rollback

```text
Prepare uma avaliação de release sem publicar. Leia diff, branch, CI, build, migrations, variáveis, flags, integrações, documentação e observabilidade.

Verifique:
- escopo e requisitos aprovados;
- testes e evidências no SHA correto;
- lint/typecheck/build;
- migrations, compatibilidade e rollback;
- variáveis sem revelar valores;
- segurança e tenant isolation;
- dados de seed/demo;
- feature flag ou rollout gradual;
- backup/reconciliação quando necessário;
- smoke test de preview e produção;
- métricas e alertas;
- plano de rollback técnico e operacional;
- comunicação e suporte.

Classifique GO, CONDITIONAL_GO ou NO_GO, com motivos objetivos. Não faça deploy, merge ou migration remota. Entregue checklist executável, bloqueadores, evidências faltantes e sequência de rollback.
```

## P15 — Observabilidade e resposta a incidentes

```text
Audite se o sistema permite detectar, localizar, explicar e recuperar falhas sem expor dados sensíveis.

Mapeie jornadas e componentes críticos. Para cada um, defina:
- eventos de negócio e técnicos;
- log estruturado e campos seguros;
- correlation/request/tenant identifiers sem PII desnecessária;
- métricas de volume, sucesso, erro, latência, fila e custo;
- tracing quando justificado;
- health/readiness checks;
- alertas acionáveis e limites baseados em baseline;
- dashboards mínimos;
- retenção/redaction;
- runbook, owner e escalada;
- reconciliação e recuperação;
- evidência pós-incidente.

Analise falhas silenciosas, logs vagos, exceções engolidas, alertas ruidosos, ausência de contexto e métricas sem ação. Entregue gaps, instrumentação mínima, runbook e testes de observabilidade. Não conecte serviços de produção.
```

## P16 — Desempenho e custo operacional

```text
Meça antes de otimizar. Inspecione bundle, renderização, queries, índices, cache, imagens, jobs, integrações, IA, armazenamento e limites de providers.

Defina baselines e jornadas representativas. Avalie:
- tempo de carregamento e interação;
- chamadas e payloads;
- N+1, scans e queries lentas;
- cache e invalidação;
- processamento repetido;
- concorrência e filas;
- custo por usuário, operação ou geração de IA;
- limites, rate limits e crescimento;
- impacto em dispositivos móveis e rede ruim.

Para cada proposta, estime benefício, risco, complexidade e método de medição. Não introduza cache ou paralelismo sem estratégia de consistência. Entregue baseline, gargalos confirmados, hipóteses, experimentos, orçamento de performance/custo e critérios de regressão.
```

## P17 — UX, acessibilidade, responsividade e estados reais

```text
Audite a experiência implementada em navegador/dispositivo quando disponível. Não avalie apenas aparência estática.

Revise:
- hierarquia, linguagem e ação principal;
- onboarding e orientação;
- estados vazio, carregando, sucesso, erro, offline, expirado e permissão negada;
- formulários, labels, ajuda, máscaras, validação e preservação de dados;
- teclado, foco, leitor de tela, contraste e semântica;
- alvos de toque, navegação com uma mão e viewports reais;
- feedback de ações, confirmação e desfazer;
- tabelas, filtros e busca no celular;
- mensagens de erro acionáveis;
- localização, datas, moeda e timezone;
- consistência com design system;
- performance percebida.

Use evidências: rotas, screenshots, DOM, testes e observação no navegador. Classifique bloqueadores e melhorias. Entregue jornada, findings com localização, aceite, testes de acessibilidade/visual e menor plano de correção.
```