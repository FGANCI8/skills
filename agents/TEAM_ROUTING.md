# Team routing

## Decisão inicial

1. Ler instruções locais e evidência.
2. Se o caminho for determinístico, usar workflow comum.
3. Se um especialista for suficiente, usar `SINGLE_SPECIALIST`.
4. Adicionar revisor apenas pelo risco ou subjetividade.
5. Usar orquestrador somente com dependências, vários domínios, paralelo, loop ou duração longa.

## Pedidos naturais

| Pedido | Modo e equipe mínima |
|---|---|
| “Faça esta correção pequena.” | especialista do domínio |
| “Construa esta funcionalidade completa.” | diretor; produto/arquitetura se necessário; autores full-stack; qualidade; revisor |
| “Faça front e back.” | pipeline frontend/backend; banco somente se houver mudança de dados; revisor |
| “Crie uma tela premium.” | autor visual + avaliador visual independente |
| “Faça o backend.” | backend/API + segurança se houver auth/dados + qualidade |
| “Crie um projeto Python.” | Python + qualidade + revisor proporcional |
| “Revise banco ou migration.” | banco/dados + AppSec + revisor; gate humano |
| “Revise a segurança.” | AppSec em modo auditoria; sem edição por padrão |
| “Descubra e corrija o bug.” | investigador do domínio; qualidade; revisor para risco médio+ |
| “Crie uma automação/agente de IA.” | IA/automação + AppSec + observabilidade + qualidade |
| “Use vários agentes/cada um faz uma parte.” | diretor valida se as partes são realmente independentes |
| “Trabalhe em loop até ficar bom.” | evaluator-optimizer, rubrica e máximo de três rodadas |
| “Continue por várias etapas.” | long-running incremental + documentação/handoff |
| “Prepare release.” | qualidade + plataforma + AppSec conforme risco; nunca merge/deploy automático |
| “Investigue incidente.” | incidente + AppSec; congelar mudanças não essenciais |

## Precedência

Privacidade e autorização > segurança e isolamento > integridade operacional > arquitetura e produto > domínio > UX/visual/conveniência. Um especialista ausente não é substituído por outro fingindo a capacidade; usar fallback seguro ou `MISSING_EVIDENCE`.
