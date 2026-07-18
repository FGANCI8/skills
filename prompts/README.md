# Renova Aura reusable prompts

Use estes prompts como entradas em português normal. O usuário não precisa saber nomes de skills ou agentes: o roteador inspeciona o projeto, escolhe a menor equipe, define gates e exige relatório com evidências.

## Construção e manutenção

| Necessidade | Prompt |
|---|---|
| mudança pequena e delimitada | `planejar-e-implementar.md` |
| funcionalidade completa | `construir-funcionalidade-completa.md` |
| backend/API | `criar-backend.md` |
| projeto Python | `criar-projeto-python.md` |
| corrigir bug | `corrigir-bug.md` |
| refatorar | `refatorar.md` |
| desempenho | `melhorar-desempenho.md` |

## Produto, interface e dados

| Necessidade | Prompt |
|---|---|
| front-end premium | `polir-frontend-premium.md` |
| banco/schema/migration em auditoria | `revisar-banco.md` |
| segurança de aplicação/SaaS | `revisar-seguranca-saas.md` |

## IA, operações e equipe

| Necessidade | Prompt |
|---|---|
| automação segura | `criar-automacao.md` |
| agente de IA em mock | `criar-agente-ia.md` |
| equipe multiagente | `formar-equipe-multiagente.md` |
| loop limitado de qualidade | `executar-loop-qualidade.md` |
| revisão independente | `revisao-independente.md` |
| preparar release sem merge/deploy | `preparar-release.md` |
| investigar incidente | `investigar-incidente.md` |
| continuar trabalho longo | `continuar-trabalho.md` |

## Biblioteca e orientação

| Necessidade | Prompt |
|---|---|
| entender repositório sem alterar | `auditar-projeto.md` |
| organizar skills e prompts | `organizar-biblioteca.md` |

## Regras comuns

Instruções locais, decisões, código, migrations, testes e configuração permanecem fontes da verdade. Substitua placeholders apenas por contexto seguro. Nunca cole credenciais, dados pessoais/clientes, payloads privados ou caminhos de produção.

Prompts não concedem autorização para merge, deploy, banco real, migration, pagamento, mensagem, provider real, exclusão ou mudança crítica de segurança. Cada execução deve reportar rota, ownership, arquivos, resultados literais, gaps, gates, risco e rollback.
