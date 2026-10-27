# Como usar sem decorar nomes

O usuário não precisa memorizar IDs, skills ou agentes. Basta pedir em português normal.

## Formato mínimo

Diga três coisas quando souber:

1. projeto;
2. problema ou objetivo;
3. se quer somente analisar, planejar ou implementar.

Exemplos:

- “No Zuno, veja se estão faltando campos para endereço, mapa, busca e contato.”
- “No FalaOrça, revise se o orçamento por voz entrega todos os dados necessários para proposta, banco e WhatsApp.”
- “Na Aura Clínica, veja se o webhook pode duplicar mensagem ou perder handoff.”
- “No Aura Shop, confira o que falta para sair de dados mockados e receber pedido real.”
- “No PetShop Pro, faça uma revisão de dados do tutor, pet, agenda, consentimento e pagamento.”

O roteador/orquestrador do Agent OS 1.1 deve localizar o pacote do projeto, ler as instruções locais e selecionar o menor conjunto de agentes, skills, project adapters e prompts.

## Fluxo dentro do Agent OS 1.1

1. O pedido chega em linguagem natural.
2. O roteador escolhe um owner e somente os apoios exigidos pela tarefa e pelo risco.
3. O agente usa as skills adequadas; o profile `ProjectPacks` torna oito extension skills elegíveis, mas não ativa todas.
4. Um dos quatro project adapters entra somente quando o contexto do projeto exigir. Adapters não fazem parte dos 18 agentes canônicos.
5. Um dos 23 prompts (`P01`–`P17` ou `T01`–`T06`) pode fornecer instrução padronizada.
6. Handoffs transmitem estado e evidência, sem conceder autoridade, reabrir gate ou autorizar merge, push ou deploy.
7. Quando o contrato exigir, um avaliador independente revisa sem autoaprovar.
8. O humano decide ações críticas.

O accountable integrator canônico continua sendo `technical-director-orchestrator`. `ProjectPacks` não cria um segundo Agent OS nem autoridade paralela, e revisão de IA não substitui decisão humana.

## Adaptação pelo estágio

Antes de executar, classifique:

- `DISCOVERY`: ideia, pesquisa ou protótipo;
- `SPEC`: requisitos e contratos;
- `BUILD`: implementação em andamento;
- `HARDEN`: segurança, testes e confiabilidade;
- `RELEASE`: preparação de publicação;
- `OPERATE`: produção, incidentes e evolução.

O mesmo prompt muda de profundidade:

- em `DISCOVERY`, aponta perguntas e hipóteses;
- em `SPEC`, produz contratos e aceite;
- em `BUILD`, compara código e requisitos;
- em `HARDEN`, procura falhas e testes negativos;
- em `RELEASE`, exige evidência e rollback;
- em `OPERATE`, usa métricas, logs e incidentes reais sanitizados.

## Resposta obrigatória

A resposta deve separar:

- `FATO CONFIRMADO`;
- `HIPÓTESE`;
- `RECOMENDAÇÃO`;
- `INFORMAÇÃO AUSENTE`;
- `DOCUMENTAÇÃO POSSIVELMENTE DESATUALIZADA`.

E terminar em:

- `EXECUTAR AGORA`;
- `PLANEJAR`;
- `ARQUIVAR`.

Quando houver próximo passo seguro, entregar um prompt técnico copiável.

## Regra para implementação

Nenhum prompt desta biblioteca autoriza automaticamente:

- migration remota;
- banco real;
- deploy;
- merge ou push;
- envio de WhatsApp ou e-mail;
- pagamento;
- exclusão;
- uso de secrets;
- processamento de dados pessoais reais.

O agente pode inspecionar, especificar, testar localmente e preparar mudanças reversíveis dentro do escopo autorizado.

As permissões continuam subordinadas a `RA-AUTH-BASELINE-1` e à tool policy do Agent OS: default deny, escrita apenas com claim explícito, rede externa negada, provider real proibido no V1.1 e produção negada. Instruções locais podem restringir, mas não ampliar esses limites.

Merge, deploy, produção, autenticação/autorização, RLS/tenant, dados sensíveis, provider real, pagamento e ações irreversíveis exigem os gates humanos canônicos. Esta documentação está em `LOCAL_DRAFT_PRE_PUBLICATION`; destino, licença e distribuição permanecem em `PENDING_PUBLICATION_GOVERNANCE_DECISION`.
