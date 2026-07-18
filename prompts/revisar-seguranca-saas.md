# Revisar segurança de aplicação ou SaaS

Faça uma auditoria de segurança somente leitura desta aplicação, orientada pelo sistema real e por fontes oficiais atuais.

Ative o roteador e selecione AppSec como proprietário em modo auditoria, adicionando especialistas somente pela superfície observada. Mapeie ativos, atores, identidade, sessões, autorização, modelo owner/tenant, APIs, banco/RLS, uploads, webhooks, agentes, integrações, segredos, dados sensíveis, supply chain, observabilidade e condições excepcionais. Procure caminhos credíveis de acesso indevido, vazamento entre escopos, prompt injection, exfiltração, fail-open, SSRF, consumo ilimitado e privilégios excessivos.

Cada achado deve ter evidência, severidade, precondição, impacto, confiança, correção mínima, teste negativo e decisão de bloqueio de release. Não modifique código ou políticas até que a remediação seja autorizada. Entregue rota, gaps, gates, testes `NOT_VERIFIED` e veredito.
