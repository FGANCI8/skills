# Renova Aura PDF Forms Skill Suite

Suíte pública e reutilizável para criar, reparar, validar e entregar formulários PDF preenchíveis sem perder o visual aprovado.

## Skills

| Skill | Responsabilidade |
|---|---|
| `renova-aura-pdf-forms-router` | Classifica a tarefa e seleciona o menor conjunto seguro |
| `renova-aura-fillable-pdf-architect` | Cria ou reconstrói AcroForm, campos, fontes, aparências e versão impressa |
| `renova-aura-pdf-compatibility-auditor` | Testa estrutura, salvamento, reabertura, impressão e compatibilidade por visualizador |
| `renova-aura-pdf-delivery-guardian` | Empacota versão interativa, impressão, teste sintético, manifesto, relatório e hashes |

## Ordem recomendada

1. roteador;
2. arquiteto, quando houver criação ou reparo;
3. auditor de compatibilidade;
4. guardião de entrega.

## Regra central

Nunca declarar compatibilidade universal. Informar exatamente o que foi testado e usar `NOT VERIFIED` para visualizadores ou aparelhos sem evidência.

## Instalação global no Codex

Copiar as quatro pastas de skills para:

`%USERPROFILE%\.agents\skills`

## Instalação por projeto

Copiar as quatro pastas para:

`PASTA_DO_PROJETO\.agents\skills`

## Fronteira público/privado

Esta suíte contém somente processo genérico. PDFs de clientes, regras clínicas, dados pessoais, textos jurídicos específicos e decisões operacionais devem permanecer no projeto privado correspondente.
