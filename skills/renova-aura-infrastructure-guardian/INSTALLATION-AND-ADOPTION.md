# Instalação, persistência e adoção — candidata v0.3.0

Evolução revisada do pacote v0.2; não é cópia byte a byte. Status: candidata, pendente de aprovação final. A preparação da branch/PR não a promove a canônica.

## Três níveis diferentes
1. **Canônica**: versão aprovada, versionada em fonte GitHub autorizada; alterações passam por revisão.
2. **Persistente**: cópia instalada no diretório de skills do perfil Codex, sobrevive ao encerramento da sessão; GitHub continua sendo a fonte de atualização, não há sincronização automática.
3. **Transversal**: projetos e outros agentes conseguem localizar/acionar a skill; depende de instruções de encaminhamento e suporte do ambiente. Não equivale a ativação automática em toda ferramenta.

## Estratégia de instalação
- Antes de escrever, Codex identifica diretório real de skills do usuário e convenções suportadas; não presumir `~/.agents/skills` nem `~/.codex/skills` sem verificar.
- Inventariar skills existentes e procurar sobreposição com guardians de segurança, infra ou banco.
- Preservar instalações existentes; criar salvaguarda se houver conflito de nome; nunca sobrescrever sem autorização.
- Instalar candidata localmente apenas após validação estática; usar branch/PR no GitHub para revisão antes de publicar como canônica.
- Em projetos consumidores, adotar encaminhamento mínimo e idempotente em `AGENTS.md` ou mecanismo equivalente, sem copiar o conteúdo integral e sem alterar projetos não autorizados.
- Se o repositório central for privado, validar acesso dos agentes; caso não haja, fornecer fallback seguro de leitura local, nunca expor segredos.

## Codex e outras ferramentas

A documentação oficial atual indica `$HOME/.agents/skills` para skills do usuário: https://learn.chatgpt.com/docs/build-skills . Conferir o perfil efetivo e o catálogo do executável instalado; não duplicar a mesma skill em múltiplas raízes. O pacote usa `SKILL.md` com `name`, `description` e metadados de versão/status, referências relativas e `agents/openai.yaml`. Não modifica `config.toml`, MCPs ou outras skills. Descoberta implícita permanece permitida por padrão; aprovação canônica é um gate separado.

Validar nova instância do app-server (`skills/list`, recarga) e uma sessão nova do Codex lendo o caminho global. Uma listagem prova descoberta; uma execução de análise com a skill prova uso somente naquele cenário. Não equivale a reinício visual da IDE, a fontes privadas acessíveis em todo agente ou a testes de infraestrutura de produção.

Para Claude, Gemini, Antigravity ou outra IDE, conferir o suporte local a skills/instruções, permissões e descoberta reais. Preparar um apontamento equivalente e testar uma tarefa relevante e outra irrelevante em cada ferramenta antes de declarar adoção.

## Encaminhamento mínimo proposto

Aplicar somente no projeto autorizado, após ler suas instruções e revisar o diff:

> Para decisões de infraestrutura, banco, hospedagem, automações por código, capacidade, custos, backups ou VPS, após aprovação da candidata, usar `$renova-aura-infrastructure-guardian` quando disponível. Consultar as fontes canônicas indicadas nela; preservar regras e gates locais. Se skill ou fontes estiverem inacessíveis, registrar `BLOCKED` para conclusões dependentes. Instalação global não prova adoção nesta ferramenta. Não acionar em tarefas irrelevantes.

O router existente não é alterado por esta instalação. Sua futura integração deve acrescentar apenas uma rota de infraestrutura e preservar Security/Database Guardian como responsáveis nas respectivas áreas; testar antes de aplicar. Ausência de um adaptador por projeto continua sendo pendência, mesmo que o catálogo global encontre a skill.

## Rollback local

Registrar hashes antes/depois e o manifesto dos arquivos instalados. Como a instalação é aditiva, a reversão consiste em retirar apenas esta pasta da raiz de descoberta para uma quarentena fora de `skills`, preservando conteúdo e hashes, e conferir o catálogo numa nova sessão. Não remover diretórios existentes, restaurar backups por wildcard ou usar reset/clean. Atualizações futuras exigem comparação e autorização para substituir conteúdo divergente.

## Testes de aceitação
- `SKILL.md` com frontmatter válido, nome e descrição consistentes.
- Referências relativas existentes, sem segredos nem URLs de acesso temporário.
- Evals: 8 cenários com resultado esperado; executar com skill ativa e sem skill (controle), registrar evidências, resultados PASS/FAIL/NOT_RUN.
- Disparos: tarefas de banco, VPS, custos, automações por código e recuperação devem carregar skill; tarefas alheias não devem acioná-la indiscriminadamente.
- Nenhuma compra, deploy, alteração de produção ou edição em massa sem autorização específica.
- Verificar instalação após reinício de sessão e leitura de uma skill em um projeto consumidor de teste.

## Aprovação final
A candidata não deve ser chamada de canônica ativa antes de aprovação do proprietário, publicação versionada e testes reais. Registrar commit, branch, instalação, cobertura de projetos e lacunas.
