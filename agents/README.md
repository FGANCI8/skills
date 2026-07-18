# Renova Aura agents

Esta pasta define a equipe do Agent Operating System. Agentes são papéis operacionais; skills são métodos reutilizáveis. Um agente pode compor várias skills, e uma skill pode atender vários agentes.

## Fontes canônicas

- `renova-aura-team.yaml`: registro, limites, modos e gates.
- `agent-team.schema.json`: contrato validável da equipe e de cada agente.
- `definitions/*.yaml`: 18 definições individuais.
- `AGENT_CATALOG.md`: visão humana do catálogo.
- `TEAM_ROUTING.md`: seleção por linguagem natural.
- `FILE_OWNERSHIP_AND_CONCURRENCY.md`: propriedade e paralelo.
- `LOOP_PROTOCOLS.md`: loops e stop reasons.
- `HUMAN_APPROVAL_GATES.md`: ações que param para decisão humana.
- `LONG_RUNNING_HANDOFF.md`: continuidade entre sessões.
- `TECHNICAL_REFERENCE.md`: pesquisa oficial e decisões.
- `templates/`: handoff, ledger, decisões, ownership, avaliações e resumo.

As pastas `skills/*/agents/openai.yaml` são metadados de interface das skills; não substituem estas definições.

## Regra de execução

O roteador escolhe a skill principal. O orquestrador entra somente quando uma tarefa média, complexa, iterativa ou longa exige coordenação. Especialistas devolvem artefatos estruturados ao integrador; não publicam, mesclam ou fazem deploy por conta própria.

## Validação

`ValidationPython` exige Python 3.11+ com PyYAML. `ReferencePython` exige Python 3.11+ com Pydantic 2. Quando um único interpretador possui as duas dependências:

```powershell
$python = "python"
& .\tools\test-renova-aura-agent-os.ps1 -ValidationPython $python -ReferencePython $python
```

Quando as dependências estão em runtimes isolados, informe cada executável sem instalar pacotes no ambiente global:

```powershell
$yamlPython = "<python 3.11+ com PyYAML>"
$pydanticPython = "<python 3.11+ com Pydantic 2>"
& .\tools\test-renova-aura-agent-os.ps1 -ValidationPython $yamlPython -ReferencePython $pydanticPython
```

O wrapper executa schema/catálogo, `compileall`, lint interno e testes mock sem rede. Executa Ruff somente quando a dependência já existe; caso contrário registra literalmente `NOT RUN (dependency unavailable)`. O scan público de segredos, caminhos e dados pessoais é heurístico e complementa, mas não substitui, revisão humana do diff.
