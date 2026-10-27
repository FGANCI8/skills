# Prompts 01 — Produto, Requisitos e Prontidão

## P01 — Diagnóstico de produto, MVP e corte de escopo

```text
Você está dentro do repositório real deste produto da Renova Aura. Antes de recomendar ou alterar algo, leia as instruções locais, memória viva, README, PRD/SPEC, rotas, schema, integrações, testes, backlog e estado Git disponíveis.

Missão: determinar se o produto está resolvendo um problema real com o menor escopo útil, seguro e operável. Não trate quantidade de telas ou arquivos como progresso.

1. Identifique com evidências: usuário, operador, comprador, problema, alternativa atual, proposta de valor, estágio e fluxo crítico.
2. Compare documentação, código, configuração, banco e testes. Código e comportamento testado vencem documentação antiga.
3. Inventarie funcionalidades existentes, incompletas, somente documentadas, duplicadas e sem usuário claro.
4. Classifique cada item em EXECUTAR AGORA, PLANEJAR, ARQUIVAR ou DO_NOT_BUILD.
5. Defina o menor fluxo ponta a ponta que prova valor, incluindo entrada, validação, persistência, saída, erro, retomada e suporte.
6. Identifique dependências comerciais e operacionais: onboarding, dados iniciais, permissões, suporte, métricas, custo e manutenção.
7. Proponha MVP, não objetivos, métricas e critérios de aceite observáveis.
8. Não implemente nesta etapa. Não faça deploy, migration, merge ou acesso a dados reais.

Entregue: fatos, hipóteses, lacunas, decisões recomendadas, mapa do fluxo crítico, escopo MVP, itens adiados, riscos, backlog vertical e próximo micropasso.
```

## P02 — Rastreabilidade de requisitos e critérios de aceite

```text
Audite a rastreabilidade completa deste projeto. Leia repositório, instruções, memória, PRD, SPEC, issues, migrations, APIs, telas e testes.

Para cada requisito material, construa uma matriz:
- ID e descrição;
- fonte e data;
- usuário/ator;
- jornada e tela/endpoint/evento;
- regra de domínio;
- campos de entrada e saída;
- arquivo/módulo responsável;
- tabela/coluna ou armazenamento;
- autorização e tenant ownership;
- teste existente;
- evidência literal;
- status: IMPLEMENTADO, PARCIAL, DOCUMENTADO_APENAS, AUSENTE, CONFLITANTE ou OBSOLETO.

Procure requisitos sem implementação, implementação sem requisito, testes sem requisito, requisitos sem teste, nomes divergentes e critérios vagos. Transforme “funciona”, “seguro”, “rápido” e “responsivo” em resultados mensuráveis.

Não altere produto. Entregue matriz priorizada, falhas bloqueantes, critérios de aceite corrigidos, arquivos afetados e prompt técnico para o menor próximo conjunto de correções.
```

## P03 — Jornada, estados, erros e recuperação

```text
Mapeie a jornada real do usuário e do operador, não apenas o fluxo feliz. Inspecione rotas, componentes, serviços, banco, máquinas de estado, mensagens, formulários, permissões e testes.

Para cada jornada crítica, registre:
- ponto de entrada e pré-condições;
- passos e decisões;
- estados persistidos;
- estados vazios, carregando, sucesso, erro, parcial, cancelado, expirado e bloqueado;
- validações no cliente e no servidor;
- falha de rede/provider;
- retry, retomada e idempotência;
- permissão negada e tenant incorreto;
- confirmação antes de ação irreversível;
- acessibilidade e uso móvel;
- suporte/handoff humano;
- analytics e evidência de conclusão.

Identifique becos sem saída, loops, telas sem retorno, dados perdidos ao voltar, estados impossíveis, mensagens vagas e ações sem confirmação. Classifique gravidade e proponha correções mínimas por jornada.

Entregue mapa de estados, tabela de exceções, gaps, critérios de aceite e testes recomendados. Não implemente sem escopo aprovado.
```

## P04 — Prontidão comercial e operacional

```text
Avalie se este produto está pronto para ser demonstrado, vendido, implantado e sustentado. Não confunda build verde com prontidão comercial.

Inspecione produto, documentação, configuração, dados de demonstração, onboarding, permissões, cobrança, suporte, observabilidade, termos, privacidade, backup, métricas e rollback.

Avalie:
- proposta de valor e público;
- demonstração reproduzível;
- onboarding e configuração inicial;
- papéis, limites e tenant isolation;
- dados de exemplo seguros;
- plano/limites/custos;
- suporte e handoff;
- métricas de ativação, uso, resultado e qualidade;
- dependências externas e contingência;
- documentação de operação;
- release, rollback e incidente;
- privacidade, retenção e exclusão;
- capacidade de implantar o segundo cliente sem copiar manualmente dados do primeiro.

Classifique cada dimensão como READY, PARTIAL, NOT_READY, NOT_APPLICABLE ou NOT_VERIFIED. Entregue bloqueadores, plano de 30 dias por prioridade, critérios de go/no-go e o que não deve ser vendido ainda.
```