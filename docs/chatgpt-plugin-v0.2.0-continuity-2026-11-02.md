# Registro de continuidade — Plugin ChatGPT Renova Aura v0.2.0 (02/11/2026)

> **Registro documental de evidências; não é alteração das skills nem autorização de deploy.** Este arquivo resume a homologação conduzida em sessão ChatGPT e em execução local Codex. O repositório público não deve conter backups de conta, URLs privadas, credenciais, capturas pessoais ou identificadores de usuários.

## Identidade e fonte

- Biblioteca fonte: `FGANCI8/skills`, `main`, commit observado `72bcd9b0855c09cf26604452faf99746642d7520` (merge da PR #8).
- Catálogo: **34 skills Renova Aura** (inclui **8 ProjectPacks**); `Core` é perfil padrão de elegibilidade, nunca `All` implícito. Fonte de perfis: `skills/renova-aura-skill-library-curator/references/profile-memberships.json`.
- Infraestrutura: `renova-aura-infrastructure-guardian` **v0.3.0** como versão da *skill*, diferente da versão do *plugin*.
- Plugin ChatGPT: identidade técnica `renova-aura-infra`, versão **0.2.0**, nome apresentado `Renova Aura`; substituiu a versão 0.1.0 **no mesmo registro** por `Enviar nova versão`.
- Extras `renova-aura-n8n-coordinator` e `Renova Aura — Segurança Global` **não** integram o conjunto das 34 e foram preservadas separadamente.
- Instalação de ChatGPT não atualiza automaticamente instalações globais no Codex e Antigravity.

## Linha do tempo das evidências

1. PR #8 / Infrastructure Guardian: homologação documental e de roteamento, incluindo execução isolada no Antigravity; merge na main; atualização global Antigravity documentada. A instalação no ChatGPT foi tratada separadamente.
2. Na conta ChatGPT, a skill Infrastructure Guardian individual já existia. Sua cópia anterior divergia da main em documentos e metadados; backups foram preservados. A manutenção arquivo a arquivo mostrou alto custo operacional.
3. Codex estudou distribuição por plugin e produziu piloto `renova-aura-infra` 0.1.0. Piloto: **17 testes locais PASS**; importação/instalação ChatGPT e uma conversa de infraestrutura foram observadas.
4. Codex consolidou 34 skills em ZIP v0.2.0, reutilizando o empacotador/validador. Após interrupção por limite de uso e retomada do checkpoint, fechou referências e preservação do ícone. Entrega final de **168 arquivos, 544823 bytes**, SHA-256 `e42796d6b3578986deb27cad5046d5305733f66a9289906d76b5bce8cae6213d`.
5. Evidências Codex (relatadas no artefato de entrega): **34/34 inventário**, **132/132 blobs-fonte**, **13 testes focados** do candidato anterior, **6/6 checks de delta final**, revisão independente local, ZIP reprodutível byte a byte, **84/84 arquivos globais monitorados** preservados. CI histórica PR #8: **45/45 PASS**, não reexecutada.
6. Tentativa de atualização automática via Computer Use ficou `BLOCKED` por política de observação da URL no navegador. Sem contorno de segurança. O proprietário realizou a atualização nativa do **mesmo plugin** pelo controle `Enviar nova versão`.
7. Capturas da UI do ChatGPT confirmaram `Nova versão enviada`, plugin exibido como `Renova Aura`, versão **0.2.0**, e contador **Habilidades 34**. As habilidades individuais existentes não foram removidas.
8. Homologação documental em conversa com plugin selecionado: 34/34 visíveis; **14/15** verificações sintéticas estáticas; uma lacuna na rota explícita Android/ProjectPacks, embora a skill exista. Controles negativos **6/6 PASS** em inspeção de contrato (não em invocação real).
9. Teste assistido `Testar no chat` para app Android/Kotlin/Compose/Room: a resposta consultou Router e Android Kotlin Engineering, repo e documentação, sem editar; resultado coerente. Isso prova aplicação **na sessão com plugin selecionado**, não invocação automática.
10. Teste em **chat novo normal, sem selecionar o plugin**, com tarefa Android: a resposta foi tecnicamente coerente e consultou fontes, mas não apresentou evidência inequívoca de seleção/leitura da skill. **AUTO_INVOKED: NOT_VERIFIED**; não classificar como PASS nem FAIL.

## Matriz atual — critérios de prova distintos

| Critério | Estado | Observação |
|---|---|---|
| Fonte canônica e PR #8 | PASS | `main` no SHA acima; CI histórico 45/45 |
| Pacote final local v0.2.0 | PASS (evidência Codex) | 34 skills; integridade, reprodução, revisão independente |
| Upload de nova versão para mesmo plugin | PASS (capturas UI) | Não criar novo plugin para substituir |
| Versão e catálogo no ChatGPT | PASS (capturas UI) | v0.2.0 e 34 habilidades visíveis |
| Leitura/uso Android em chat com plugin selecionado | PASS assistido | Sem alterações em código |
| Seleção automática em sessão nova sem plugin explícito | NOT_VERIFIED | Boa resposta técnica não prova invocação |
| Rota explícita Android no `renova-aura-router/SKILL.md` | LACUNA DOCUMENTAL | Skill pertence a ProjectPacks e tem descrição própria, mas não há linha específica na tabela |
| Roteamento funcional integral das 34 skills | NOT_RUN | Não confundir contratos estáticos com testes 34x |
| GitHub -> ChatGPT sincronização automática | NOT_PROVEN | Atualização observada foi upload manual único de ZIP |
| Outros runtimes (Codex/Antigravity) | Fora desta homologação | Não inferir atualização de instalações locais |

## Próximo ciclo — evitar retrabalho

- **Não reconstruir** o plugin nem repetir 17, 13, 6 ou 45 testes já válidos sem mudança relevante.
- Manter v0.2.0 estável; **não promover** ou alterar imediatamente por causa de um único controle estático.
- Abrir proposta isolada para linha Android/ProjectPacks no Router **somente se** necessidade de roteamento explícito for confirmada; incluir positivo/negativo, revisão e atualização de pacote por versão.
- Validar `AUTO_INVOKED` apenas quando o runtime expuser evidência de leitura/seleção; um texto tecnicamente correto sem prova é `NOT_VERIFIED`. Testes independentes de outras famílias podem ser escolhidos por risco, não por obrigação de 34 repetições.
- O registro detalhado da sessão, os ZIPs, hashes, screenshots e handoff do coordenador devem ficar no arquivo privado da Central Renova Aura. **Não colocar cópias de dados pessoais ou Drive privado neste repositório público.**
- A fonte `FGANCI8/renova-aura-docs` contém a norma de estados `RA-SKILLS-ADOPTION-001`; respeitar `DISCOVERED` vs `LOADED`, `EXECUTED` vs `AUTO_INVOKED`.
- Evidência de atualização do plugin **não substitui** PR/merge das melhorias de source; qualquer mudança em skills usa branch e gate humano.

## Decisão de continuidade

**EXECUTAR AGORA:** manter pacote 0.2.0 instalado e registrar evidência; sem novas ações no ChatGPT ou no app Android.  
**PLANEJAR:** validação futura objetiva de invocação automática e possível rota Android; revisar o adaptador ChatGPT (`RENOVA_AURA_CHATGPT_CANONICAL_ADAPTER.md`) que ainda descreve modalidades anteriores à distribuição por plugin, em uma PR própria.  
**ARQUIVAR:** empacotamento/instalação 34/34 concluídos; a homologação operacional total e o sync automático **não** foram comprovados.

Registro documenta estado observado em 02/11/2026; não declara cobertura global, produção, sincronização ou 34 execuções funcionais.
