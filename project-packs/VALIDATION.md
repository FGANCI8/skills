# Validação — Biblioteca de Pacotes por Projeto

## Contrato do manifesto

No `MANIFEST.json`, `version` identifica a versão do conteúdo do conjunto
`ProjectPacks`. O valor atual, `1.1.0-draft`, indica que o pacote permanece em
estado draft e não representa release ou publicação final.

`schema_version` identifica a versão estrutural do formato do manifesto. O
formato atual é `1.1.0`. Mudanças estruturais incompatíveis — como remover ou
renomear uma propriedade, mudar seu significado contratual ou alterar seu tipo
de maneira incompatível — exigem uma nova versão de `schema_version`. Mudanças
puramente aditivas só podem manter a versão quando o contrato vigente permitir
explicitamente a extensão.

O formato 1.1 substituiu `agents` por `project_adapters`, substituiu as
contagens `new_skills` e `new_agents`, separou explicitamente base skills,
extension skills, canonical agents e project adapters, e declarou o profile
`ProjectPacks`.

## CURRENT LOCAL VALIDATION

O estado técnico local reconciliado usa Agent OS 1.1, 18 agentes canônicos, um accountable integrator, quatro project adapters fora do registry canônico, oito extension skills no profile `ProjectPacks` e 23 prompts. A biblioteca combinada contém 25 skills basais + 8 extensions, sem sobreposição, totalizando 33 IDs únicos.

| Verificação local | Resultado | Natureza da evidência |
|---|---|---|
| Suite Agent OS e contratos dos adapters | `41/41 PASS` | executada localmente no head técnico congelado durante a revisão final pré-publicação |
| Contrato do manifesto | `4/4 PASS` | executado localmente com `unittest` e standard library |
| Inventário e profile | `25 + 8 = 33`, overlap `0`, `ProjectPacks = 8` | reconciliação mecânica dos registros centrais |
| Revisão UTF-8 do delta técnico | `37/37 PASS` | revisão focal do delta congelado anterior a este patch narrativo |
| `git diff --check` do delta técnico | `PASS` | executado na revisão final pré-publicação |

Esses resultados provam somente os contratos e artefatos indicados. Não provam instalação, descoberta, comportamento funcional, runtime integrado, publicação ou produção.

## HISTORICAL / PRIOR EVIDENCE

Evidências anteriores permanecem úteis como histórico, sem serem apresentadas como execução atual:

- validação estrutural das oito extension skills: `8/8 PASS` obtido no C3 (`c98ec89374967d910af83563c06c893d89f3aebf`) e reutilizado porque os oito blobs `SKILL.md` continuam idênticos; não foi integralmente reproduzido nesta revisão;
- validação dos oito `agents/openai.yaml`: `8/8 PASS` obtido no mesmo C3 e reutilizado porque os oito blobs de metadata continuam idênticos; não foi integralmente reproduzido nesta revisão;
- branch original criada a partir de `agent/ra-skills-base-v1` e PR mantida em draft;
- catálogo original com 23 prompts e matriz dos oito repositórios confirmados;
- `PROJECT_PACK.md` e `FIELD_DATA_INTEGRATION_AUDIT.md` criados e relidos nos oito repositórios;
- branch do Vocero verificada como `renova-aura/base-hardening`;
- estrutura histórica do Google Drive relida, com pasta mestre, oito pastas de projeto, três documentos centrais e oito documentos de projeto;
- ausência intencional de pacote no repositório vazio.

Essas verificações históricas não alegam estado atual do GitHub, Drive ou repositórios externos e não substituem uma revalidação específica quando necessária.

Uma reexecução adversarial do `quick_validate.py` no ambiente Windows padrão resultou em `7/8`: a leitura sem encoding explícito encontrou `UnicodeDecodeError` sob CP1252. Essa é uma limitação não bloqueante do validador/ambiente para futuro hardening; os 16 blobs permanecem idênticos ao C3 e não há evidência de corrupção das skills.

## NOT_RUN

- remote CI (`NO_REMOTE_CI`);
- instalação ou descoberta global das skills;
- ativação comportamental em sessão nova;
- evals funcionais dos 23 prompts e cenários A01–A30;
- execução dos prompts contra código de produto;
- runtime integrado;
- build, testes ou migrations dos produtos;
- provider real, deploy ou produção;
- push dos commits locais, retarget, merge da PR ou atualização de `main`.

Esses itens permanecem `NOT_RUN`. A presença de arquivos nunca deve ser descrita como instalação, descoberta, execução funcional ou autorização.

## Estado atual

`LOCAL_DRAFT_PRE_PUBLICATION`

O draft não representa release, merge, publicação final ou produção. Destino, licença e distribuição permanecem em `PENDING_PUBLICATION_GOVERNANCE_DECISION`.

## Próximo smoke test recomendado

Em um único projeto piloto, iniciar sessão nova e solicitar:

> Leia as instruções locais e `docs/renova-aura-library/PROJECT_PACK.md`. Execute somente em leitura a auditoria descrita em `FIELD_DATA_INTEGRATION_AUDIT.md`. Informe arquivos lidos, entidades auditadas, blockers, evidências e o que permaneceu NOT VERIFIED. Não altere aplicação, banco, providers ou produção.

Resultado esperado: o agente seleciona o pacote correto, lê o repositório e produz uma matriz baseada em evidências sem realizar mudanças.

## Rollback

- Reverter somente o commit ou patch documental correspondente, preservando prompts, manifesto, adapters, skills, testes e registros centrais.
- Qualquer fechamento de PR, remoção de branch, alteração externa ou exclusão de conteúdo continua sujeito a gate humano separado.
