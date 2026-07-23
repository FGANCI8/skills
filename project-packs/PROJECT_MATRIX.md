# Matriz de Projetos Renova Aura

## Repositórios confirmados

| Projeto | Repositório | Perfil técnico confirmado | Pacotes prioritários |
|---|---|---|---|
| Zuno Imóveis | `FGANCI8/zuno-imoveis` | Next.js 16, React 19, TypeScript, Supabase, Stripe, Leaflet, IA, Playwright | imóveis, multi-tenant, campos/endereço/mapa, leads, busca, pagamentos, release |
| PetShop Pro | `FGANCI8/petshop-pro` | Next.js 14, React 18, TypeScript, Supabase, OpenAI, Stripe, Sentry, Vitest/Playwright | tutor/pet, agenda, consentimento, dados sensíveis, IA, pagamentos, operação |
| TatameOS | `FGANCI8/TatameOS` | React/Vite/TypeScript, Firebase, Supabase, Google APIs, PWA | academia, tenant, membros, presença, conteúdo, PWA/offline, integrações Google |
| Negociação Blindada Imóvel | `FGANCI8/Negocia--o-Blindada-Im-vel` | Next.js 14, Supabase, OpenAI, PDF/Word/Excel, Playwright | documentos, patrimônio, simulações, auditoria, privacidade, IA e rastreabilidade |
| Aura Shop Agent | `FGANCI8/aura-shop-agent` | loja mobile-first, UI → Service → Repository, dados mockados, futura Supabase/WhatsApp/pagamento | catálogo, variantes, estoque, entrega, endereço, pedido, pagamento, white-label |
| Aura Clínica Automation Engine | `FGANCI8/aura-clinica-engine` | Python 3.12, FastAPI, PostgreSQL, SQLAlchemy, Alembic, Pydantic, WhatsApp, pytest | saúde, segurança, intenções, webhook, outbox, handoff, retenção, observabilidade |
| Renova Aura Vocero Lab | `FGANCI8/renova-aura-vocero-lab` | CRM WhatsApp self-hosted, pipeline, IA, laboratório de evals, Docker | CRM, mensagens, templates, delivery, tokens, knowledge base, evals, VPS |
| FalaOrça Pintor | `FGANCI8/falaorca-pintor` | Android nativo planejado/implementado por camadas, Supabase, 41 tabelas, testes pgTAP e integração | Kotlin, voz, orçamento, clientes/endereço, propostas, marketplace de profissionais, RLS |

## Repositórios que não recebem pacote de produto

- `FGANCI8/skills`: biblioteca central; recebe catálogo canônico, skills, agentes e prompts.
- `FGANCI8/NOME_DO_REPOSITORIO`: vazio; não deve receber arquivos de produto.

## Iniciativas sem repositório confirmado

Estas iniciativas devem usar um perfil derivado até possuírem repositório próprio. Não afirmar implementação.

| Iniciativa | Perfil de partida |
|---|---|
| Boi Bravo IA | Aura Shop + WhatsApp/CRM + estoque/pedido/pagamento |
| Pra Aqui Bebidas IA | Aura Shop + entrega/geolocalização + WhatsApp |
| Moda Pro IA | comércio mobile + catálogo + CRM/WhatsApp |
| Farmácia / Sistema da Farmácia | comércio regulado + estoque + endereço + privacidade + WhatsApp |
| Salão de Beleza Inteligente | agenda + profissionais + lembretes + pagamentos |
| Bares | catálogo/cardápio + pré-atendimento + pedido + WhatsApp |
| Pesqueiro IA | cadastro + campanhas + automação + sazonalidade |
| Aura Criadores IA | catálogo/marketplace + logística + conteúdo |
| KYNLI / ecossistema pet | PetShop Pro + rede social + moderação + privacidade |
| Orla 360 / Praia Pro IA | marketplace + geolocalização + logística + pagamentos |
| Clínica Mentor IA | Aura Clínica + formulários + dados sensíveis + handoff humano |
| Farmácia Popular Municipal | dados públicos/estoque + acessibilidade + LGPD + operação municipal |
| App GELLY | aplicativo local/offline + finanças privadas + backup + PIN |
| Renova Aura Lab IA e Integrações | IA/evals + conectores + segurança + custo + arquitetura experimental |
| Projeto Deus | conteúdo, eventos e comunicação; sem perfil SaaS por padrão |
| Mapa do Cemitério de São Carlos | geolocalização + dados públicos + busca + acessibilidade |

## Regra de inclusão de novos projetos

Quando surgir um repositório novo:

1. confirmar nome, raiz, branch e stack;
2. classificar domínio, dados, integrações e estágio;
3. selecionar apenas prompts/skills necessários;
4. criar `docs/renova-aura-library/PROJECT_PACK.md`;
5. criar auditoria de campos específica;
6. registrar no índice central sem copiar dados privados para repositório público.