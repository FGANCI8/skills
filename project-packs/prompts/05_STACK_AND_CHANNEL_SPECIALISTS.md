# Prompts 05 — Tecnologia e Canais

## T01 — Next.js, React e Supabase

```text
Audite este projeto Next.js/React/Supabase com base na versão realmente instalada. Leia App Router, server/client boundaries, route handlers/server actions, middleware, schemas, Supabase clients, migrations, RLS, storage, cache, tests e deploy config.

Verifique:
- separação server/client e exposição de secrets;
- autenticação SSR, refresh e proteção de rotas;
- autorização no servidor e RLS;
- tenant_id/owner em todas as consultas;
- validação Zod ou equivalente no servidor;
- cache/revalidation e vazamento entre usuários;
- formulários, optimistic updates e concorrência;
- uploads e URLs assinadas;
- errors/loading/not-found;
- bundle, imagens e performance;
- migrations, types gerados e schema drift;
- Playwright/testes de RLS;
- Vercel/env/preview sem alterar produção.

Entregue fatos, gaps, arquivos, testes, menor plano e rollback. Não faça deploy ou migration remota.
```

## T02 — Python, FastAPI, PostgreSQL e automações

```text
Audite este projeto Python/FastAPI/PostgreSQL pela configuração e versões locais. Leia pyproject/requirements, app, schemas Pydantic, services, repositories, SQLAlchemy, Alembic, jobs, Docker, logging e testes.

Verifique:
- typing e validação nas fronteiras;
- async/sync correto e lifecycle de sessão;
- transactions e concorrência;
- migrations e schema drift;
- configuração por ambiente e secrets;
- exceptions sanitizadas;
- idempotência, retries, timeout e jobs;
- health/readiness;
- logging estruturado e redaction;
- isolamento de testes e banco test-only;
- segurança de webhooks;
- packaging, lint, compile e CI.

Para automações, simule falha no meio, duplicação, reprocessamento, provider indisponível e mensagem fora de ordem. Entregue gaps, testes e plano. Não conecte banco ou provider real.
```

## T03 — Android nativo, Kotlin e Jetpack Compose

```text
Audite o aplicativo Android real. Leia Gradle/version catalog, módulos, manifest, Compose, navigation, ViewModels, domain/use cases, repositories, Room/DataStore, network, WorkManager, DI, permissions, tests e configuração de build.

Verifique:
- arquitetura e direção de dependências;
- estado imutável, eventos únicos e lifecycle;
- rotação, process death e restauração;
- navegação e argumentos tipados;
- offline-first, cache, sincronização e conflitos;
- permissões e armazenamento seguro;
- autenticação e tokens;
- networking, timeout, retry e idempotência;
- Compose recomposition e performance;
- acessibilidade, TalkBack, font scaling e touch targets;
- strings/localização;
- build variants, signing e secrets;
- unit, instrumentation, Compose UI e screenshot tests.

Não assuma que o preview web equivale ao Android. Entregue matriz tela↔estado↔dados↔backend, gaps, testes e plano incremental. Não publique na Play Store.
```

## T04 — WhatsApp, CRM e automação de mensagens

```text
Audite o fluxo WhatsApp/CRM sem enviar mensagens reais. Leia webhook, assinatura, normalização de telefone, contatos, conversas, mensagens, templates, janela de atendimento, outbox, status, handoff, pipeline, opt-in, retries e logs.

Verifique:
- handshake e assinatura;
- deduplicação por event/message id;
- ordem e reentrega;
- persistência antes do side effect;
- sent/delivered/read/failed separados;
- janela de 24 horas e templates aprovados;
- opt-in/opt-out;
- normalização internacional;
- anexos e tipos não suportados;
- handoff humano e bloqueio da IA;
- múltiplos tenants/números;
- token rotation e redaction;
- rate limit, timeout e reconciliação;
- sandbox e testes sem Meta real.

Entregue diagrama, gaps, testes de duplicação/falha, runbook e plano. Não conecte Meta nem envie mensagem.
```

## T05 — Voz, transcrição e extração estruturada

```text
Audite a jornada de voz da captura à ação. Leia gravação, permissões, formatos, upload, STT, prompt/schema, normalização, confirmação, persistência, edição e testes.

Avalie:
- ruído, sotaques, fala rápida, números, medidas, moeda, nomes e endereços;
- duração, tamanho e formatos;
- perda de rede e retomada;
- consentimento e retenção do áudio;
- precisão por campo e não apenas texto geral;
- campos ausentes, ambíguos ou contraditórios;
- confiança e confirmação pelo usuário;
- correção manual antes de side effect;
- prompt injection por áudio;
- custo, latência e fallback para formulário;
- dataset sintético/consentido e evals de regressão.

Entregue contrato de saída, matriz campo↔métrica, casos de teste, limites e critérios de aprovação. Não envie áudio real a provider.
```

## T06 — PDF, formulários e documentos

```text
Audite o ciclo completo de documentos: origem, parsing, campos, geração, preenchimento, salvamento, reabertura, assinatura quando aplicável, impressão, envio e retenção.

Verifique:
- formato e versão;
- nomes, tipos, obrigatoriedade e ordem dos campos;
- correspondência campo↔modelo↔banco;
- documentos grandes, corruptos, protegidos e maliciosos;
- macros/conteúdo ativo;
- extração de texto/tabelas;
- validação e revisão humana;
- compatibilidade de visualizadores;
- dados sensíveis e redaction;
- hashes, versão e audit trail;
- fallback para impressão;
- testes em desktop e celular.

Não use dados reais, não compartilhe externamente sem aprovação e não trate OCR como primeira opção. Entregue gaps, matriz de campos, testes e pacote de validação.
```