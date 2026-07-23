# Como usar sem decorar nomes

Fernando não precisa memorizar IDs, skills ou agentes. Basta pedir em português normal.

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

O agente deve localizar o pacote do projeto, ler o repositório e selecionar o menor conjunto de prompts e skills.

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