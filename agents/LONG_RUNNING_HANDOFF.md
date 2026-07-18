# Long-running handoff

Trabalho longo é dividido em blocos pequenos, verificáveis e reversíveis. Cada sessão reabre o repositório, relê instruções, confirma Git e revalida a evidência; não confia apenas na memória da conversa.

## Pacote mínimo

- objetivo e aceite versionados;
- estado `DONE|PARTIAL|PLANNED|BLOCKED|NOT_RUN|UNKNOWN`;
- repositório, branch e HEAD confirmados;
- arquivos alterados e ownership;
- decisões e alternativas;
- comandos e resultados literais;
- itens deliberadamente não executados;
- riscos, bloqueios e aprovação necessária;
- rollback;
- limite/contexto restante;
- arquivos que a próxima sessão deve ler;
- próximo bloco exato e sua validação.

## Registros

Use os templates de handoff, task ledger, decision log, file ownership, evaluation log e session summary. Referencie artefatos grandes por caminho e hash; não copie segredos, prompts privados ou payloads.

## Regra de retomada

Se branch, HEAD, status, arquivo ou decisão divergir do handoff, o estado atual vence e a divergência é registrada antes de editar.
