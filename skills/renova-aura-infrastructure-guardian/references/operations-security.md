# Segurança e operação

## Preflight
Verificar propriedade dos dados, classificação de sensibilidade, segregação por tenant, RLS, autenticação, autorização, tokens e segredos, acessos administrativos, política de backup e teste real de restore.

Usar dados sintéticos em testes. Minimizar coleta e retenção; não incluir dados pessoais, clínicos, áudios reais, tokens ou identificadores operacionais em logs, commits, relatórios públicos ou prompts de fornecedores. Nunca colocar service-role no cliente. Preferir integração nativa, OAuth, conector/MCP e injeção protegida antes de chave manual. Acesso a dados reais e envio a provedores exigem autorização própria.

Backup do banco e cópia dos objetos de storage são coberturas distintas; verificar ambos e testar restauração antes de alegar recuperabilidade. Backup, recuperação de desastre e alta disponibilidade não são equivalentes.

## Automação por código
Garantir autenticação de webhooks, idempotência, retry com backoff, deduplicação, observabilidade, timeouts e proteção contra execução dupla. Agendamentos não substituem filas quando a entrega deve ser garantida. Tratar timezone e falhas parciais.

## PostgreSQL e concorrência
Não fazer `SELECT disponibilidade` seguido de `INSERT` sem barreira atômica. Examinar exclusion constraints em intervalos, status que bloqueiam datas, check-out exclusivo, locks e isolamento; usar testes simultâneos e validar resultado único. Avaliar efeitos de transações longas, deadlocks e retries.

Testar duas conexões independentes para o mesmo recurso e intervalo, idempotência, intervalos adjacentes, cancelamento e tenants diferentes. Confirmar exatamente uma reserva conflitante aceita; não tratar esse roteiro como teste de banco realizado. Nunca reescrever migration já publicada, aplicar DDL em ambiente compartilhado ou enfraquecer RLS para passar no teste.

## VPS Linux
Se autorizada, aplicar SSH com chaves, MFA onde suportado, firewall, portas mínimas, TLS, updates, backups externos e restauração, logs, monitoramento, limites de recursos, isolamento de serviços, controle de segredos e plano de incidente. Não expor banco ou painéis administrativos sem necessidade.

## Gates
Sem autorização específica: não comprar, não alterar DNS, não migrar banco, não tocar em dados reais, não fazer deploy/merge, não expor credenciais. Registrar evidência e status.
