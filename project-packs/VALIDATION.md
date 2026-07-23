# Validação — Biblioteca de Pacotes por Projeto

## Escopo validado nesta entrega

- branch central criada a partir de `agent/ra-skills-base-v1`;
- PR draft aberta sem merge;
- catálogo com 23 prompts;
- oito skills novas com `SKILL.md` e frontmatter mínimo;
- quatro definições YAML de agentes;
- manifesto JSON;
- matriz dos oito repositórios confirmados;
- dois arquivos locais criados e relidos em cada repositório;
- estrutura do Google Drive criada e relida: pasta mestre, oito pastas de projeto, três documentos centrais e oito documentos de projeto.

## Validações executadas

| Verificação | Resultado |
|---|---|
| PR central existe e permanece draft | PASS |
| Lista de arquivos da PR foi relida pelo conector GitHub | PASS |
| Catálogo central foi relido em UTF-8 | PASS |
| Skill `renova-aura-data-contract-field-auditor` foi relida com frontmatter | PASS |
| `PROJECT_PACK.md` em oito repositórios | PASS |
| `FIELD_DATA_INTEGRATION_AUDIT.md` em oito repositórios | PASS |
| Branch correta do Vocero (`renova-aura/base-hardening`) | PASS |
| Pasta raiz e nove subpastas no Drive | PASS |
| Três documentos na pasta mestre do Drive | PASS |
| Um documento dentro de cada pasta de produto no Drive | PASS |
| Ausência intencional de pacote no repositório vazio | PASS |

## Validações não executadas

- instalação global ou local das skills em Codex, Antigravity, Claude Code ou Gemini CLI;
- descoberta automática das novas skills por qualquer agente;
- ativação comportamental em sessão nova;
- evals automatizados dos 23 prompts;
- execução dos prompts contra código de produto;
- build, testes ou migrations dos produtos;
- merge da PR central;
- deploy ou provider real.

Esses itens permanecem `NOT RUN`. A presença de arquivos não deve ser descrita como skill instalada, descoberta ou funcional em uma ferramenta específica.

## Status honesto

`PARTIAL_NOT_CLAIMED`

A biblioteca e os adaptadores documentais estão salvos, organizados e relidos. A instalação/descoberta/ativação das skills depende de execução local controlada por projeto e ferramenta.

## Próximo smoke test recomendado

Em um único projeto piloto, iniciar sessão nova e solicitar:

> Leia as instruções locais e `docs/renova-aura-library/PROJECT_PACK.md`. Execute somente em leitura a auditoria descrita em `FIELD_DATA_INTEGRATION_AUDIT.md`. Informe arquivos lidos, entidades auditadas, blockers, evidências e o que permaneceu NOT VERIFIED. Não altere aplicação, banco, providers ou produção.

Resultado esperado: o agente seleciona o pacote correto, lê o repositório e produz uma matriz baseada em evidências sem realizar mudanças.

## Rollback

- Central: fechar a PR draft e apagar a branch somente após decisão humana.
- Projetos: reverter exclusivamente os commits que adicionaram `docs/renova-aura-library/`.
- Drive: remover a pasta raiz criada nesta entrega somente após confirmar que o GitHub continua como fonte canônica.
