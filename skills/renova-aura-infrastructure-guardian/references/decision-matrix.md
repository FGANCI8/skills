# Matriz de decisão

| Necessidade | Primeira avaliação | Quando reconsiderar |
|---|---|---|
| SaaS transacional | Supabase/PostgreSQL gerenciado | Gargalos medidos, requisitos específicos, TCO superior |
| Reservas simultâneas | Constraints e transações PostgreSQL; teste de corrida | Schema/status exige outra estratégia de serialização |
| Android offline | SQLite/Room + sincronização opcional | Conflitos multi-dispositivo ou volume comprovado |
| Geolocalização | PostGIS | Limites medidos, índice inadequado, carga extrema |
| IA/busca vetorial | pgvector no PostgreSQL | Volume/latência/custo justificam motor dedicado |
| Arquivos de mídia | Object storage + metadados SQL | Compliance, retenção ou tráfego exigem arquitetura diferente |
| Agendamento leve | Supabase Cron/Edge Functions ou Cloudflare Cron | Duração, memória ou rede ultrapassam limites |
| Jobs de engenharia | GitHub Actions | Necessidade de disponibilidade de produção/baixa latência |
| Jobs contínuos | Workers Python/filas; VPS se necessário | Comparar PaaS/serviço gerenciado antes de VPS |
| Cache/fila | Banco e jobs existentes primeiro | Volume, retries, throughput e SLO exigem serviço próprio |

## Comparação obrigatória
Anotar custo inicial e de renovação, região/latência, consumo, egress, backup, recuperação, monitoramento, atualização de segurança, isolamento, lock-in e esforço de operação. Nunca usar somente preço promocional.

## Gatilhos
- Excedeu limites reais documentados, mesmo após otimização.
- Requisito de duração, GPU, rede, processo persistente ou compliance não atendido.
- RTO/RPO ou recuperação testada insuficiente.
- Crescimento de clientes ou dados que altera custo e SLO.
