# File ownership and concurrency

## Registro obrigatório

Antes de qualquer escrita paralela, preencher `templates/FILE_OWNERSHIP.yaml` com caminho relativo normalizado, proprietário, modo `read|write`, etapa, dependências e status. Caminho absoluto, UNC, `..`, drive e glob amplo são proibidos.

## Regras

- Um caminho tem um único escritor ativo.
- Leitores podem coexistir, desde que não executem side effects.
- O proprietário pode escrever somente os arquivos atribuídos.
- Contratos compartilhados exigem um proprietário e consumidores aguardam a versão integrada.
- Migrations são sempre sequenciais.
- Schema e código dependente não avançam em paralelo sem contrato versionado e aprovado.
- O integrador não aceita patches fora da atribuição.

## Paralelo permitido

- pesquisa oficial em fontes independentes;
- inventários e auditorias somente leitura;
- arquivos completamente distintos sem contrato comum;
- avaliações independentes do mesmo artefato, sem edição.

## Conflito

Ao detectar dois escritores, contrato incompatível ou escopo novo: interromper as escritas, preservar ambos os artefatos, registrar `SCOPE_CHANGE` ou `ENVIRONMENT_BLOCK`, escolher um proprietário e replanejar em sequência. Não resolver por merge automático.
