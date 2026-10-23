# Matriz de aceitação — protocolo v0.3.0

| ID | Verificação | Esperado | Estado inicial |
|---|---|---|---|
| A01 | Estrutura YAML/Markdown | Válida e sem referências quebradas | NOT_RUN |
| A02 | Conflito com skills existentes | Nenhuma sobreposição não resolvida | NOT_RUN |
| A03 | n8n não adotado | Recomendar automação por código | NOT_RUN |
| A04 | Upgrade Supabase | Não sugerir compra sem evidência | NOT_RUN |
| A05 | Reserva concorrente | Requer proteção atômica e teste | NOT_RUN |
| A06 | Dados clínicos | Aplicar gates e LGPD | NOT_RUN |
| A07 | Persistência local | Skill carrega após nova sessão | NOT_RUN |
| A08 | Adoção transversal | Referências reais por projeto | NOT_RUN |
| A09 | Atualização do Drive | Readback e histórico, sem alegações falsas | NOT_RUN |
| A10 | Não acionamento indevido | Tarefa alheia não carrega skill | NOT_RUN |

Status deve ser preenchido apenas após evidência verificável.

O estado inicial acima é um template, não um relatório de execução. Registrar resultados datados no relatório da rodada, incluindo versão/hash do pacote, modelo/CLI, prompts e trace. Comportamento esperado numa resposta não comprova transação concorrente, restore, implantação, leitura atual do Drive ou ativação em outras IDEs.
