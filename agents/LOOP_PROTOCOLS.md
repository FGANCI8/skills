# Controlled loop protocols

| Loop | Sequência | Avaliador |
|---|---|---|
| implementação | planejar → bloco pequeno → testar → revisar → corrigir | revisor técnico |
| front-end premium | implementar → renderizar → avaliar desktop/móvel → corrigir | avaliador visual |
| segurança | threat model → auditar → corrigir → negativas → reauditar | AppSec independente |
| qualidade | testar → analisar falha → correção mínima → regressão | qualidade/revisor |
| desempenho | medir → diagnosticar → otimizar → medir | performance + revisor |
| agente/automação | schema → mock → avaliar → ajustar → reavaliar | IA + AppSec/qualidade |
| documentação/handoff | comparar com estado → corrigir divergência → validar retomada | documentação/revisor |

## Contrato comum

Cada instância registra objetivo, estado inicial, critério de aprovação/rubrica, autor, avaliador diferente, artefatos, máximo de rodadas, timeout, orçamento, limite de ferramentas, side effects permitidos, gates, aprovação humana aplicável, motivo de bloqueio e stop reason.

Padrão: três rodadas. Não usar `while true`, `max_turns=None` ou instrução equivalente sem limite. Uma rodada que não produz crítica concreta ou ganho mensurável não justifica continuação.

## Terminação

`PASS`, `MAX_ROUNDS`, `TIMEOUT`, `BUDGET_LIMIT`, `HUMAN_APPROVAL_REQUIRED`, `SECURITY_BLOCK`, `ENVIRONMENT_BLOCK`, `MISSING_EVIDENCE` ou `SCOPE_CHANGE`.

Depois de um terminal reason, somente uma nova autorização ou mudança de evidência inicia outro trabalho.
