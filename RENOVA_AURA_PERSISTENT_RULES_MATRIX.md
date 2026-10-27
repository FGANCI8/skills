# RENOVA AURA — MATRIZ DE REGRAS PERSISTENTES E INTEROPERABILIDADE
## Configuração Central vs. Adaptadores por Ferramenta e por Projeto

**ID:** `RA-PERSISTENT-RULES-001`  
**Data:** 27/10/2026  
**Princípio Central:** **Uma biblioteca centralizada, regras globais transversais estáveis e adaptadores leves por ferramenta e por projeto.**

---

## 1. SEPARAÇÃO RIGOROSA DE ESCOPOS

```
                           +----------------------------------------------+
                           |         BIBLIOTECA CENTRAL NO GITHUB         |
                           |       FGANCI8/skills  &  renova-aura-docs    |
                           +----------------------------------------------+
                                                  |
                     +----------------------------+----------------------------+
                     |                                                         |
         [ REGRAS GLOBAIS TRANSVERSAIS ]                         [ REGRAS DE PROJETO LOCAIS ]
       - Segurança defensiva transversal                        - Domínio de negócio (obras vs. clínica)
       - Autonomia e conectores (RA-GOV-TOOLS-001)              - Modelo de dados e tabelas locais
       - Pernada longa (RA-ENG-PL-001)                          - Paleta de cores e design system
       - Gestão de skills (RA-SKILLS-ADOPTION-001)              - Regras contratuais e precificação
       - Handoff, evidências e gates humanos                    - Stacks locais (Android vs. Next.js vs. FastAPI)
                     |                                                         |
  +------------------+------------------+                    +-----------------+-----------------+
  |                  |                  |                    |                 |                 |
Antigravity        Codex             ChatGPT              AuraServ        Aura Clínica      Zuno Imóveis
(Config Global)  (.codex/AGENTS)  (Proj. Instruct.)     (FalaOrça-Pintor)   (FastAPI)        (Next.js)
```

---

## 2. MAPEAMENTO POR FERRAMENTA

| Ferramenta | Mecanismo de Regra Global | Mecanismo de Regra de Projeto | Precedência Aplicada |
|---|---|---|---|
| **Antigravity (IDE/CLI)** | Regra Global do Usuário (`RULE[user_global]` no assistente) e `%USERPROFILE%\.gemini\config\skills` (14 skills canônicas) | `<workspace>\AGENTS.md`, `<workspace>\SECURITY.md` e `<workspace>\.agents\skills` | 1. Segurança transversal / Basal<br>2. `AGENTS.override.md` / `AGENTS.md` local<br>3. Regras globais Renova Aura |
| **OpenAI Codex** | `%USERPROFILE%\.codex\AGENTS.md` (66 linhas: Engenheiro Executor) e `%USERPROFILE%\.agents\skills` (26 skills) | `<repo_root>\AGENTS.md` | 1. Segurança transversal / Basal<br>2. `AGENTS.md` do repositório<br>3. `~/.codex/AGENTS.md` global |
| **ChatGPT** | Instruções de Projeto (Project Instructions) com `RENOVA_AURA_CHATGPT_CANONICAL_ADAPTER.md` | Leitura de `AGENTS.md` do repositório alvo via conector GitHub | 1. Decisão e aprovação do Proprietário<br>2. `AGENTS.md` do repositório alvo<br>3. Adaptador canônico ChatGPT |
| **GitHub** | Repositório central `FGANCI8/renova-aura-docs` (`main`) e `FGANCI8/skills` | Repositórios de aplicação (`falaorca-pintor`, `aura-clinica-engine`, `zuno-imoveis`) | Branch protegida `main` requer PR e aprovação humana |

---

## 3. PROIBIÇÃO DE CONTAMINAÇÃO CRUZADA

1. **Termos Comerciais:** Não incluir demãos de tinta, massa corrida ou metros quadrados em regras globais ou em projetos de clínica/imóveis.
2. **Modelos de Identidade:** O AuraServ utiliza modelo próprio; Zuno Imóveis é estritamente `owner-scoped` (sem `tenant_id`); Aura Clínica trata de sigilo médico/odontológico. Nenhuma regra de identidade pode ser forçada globalmente sobre todos os projetos.
3. **Sem Duplicação Desnecessária:** Não copiar a biblioteca completa de skills para dentro de cada pasta de projeto. Manter as skills nas localizações globais da ferramenta (`.gemini/config/skills`, `.agents/skills`) e colocar no projeto apenas adapters que contenham dados de produto.

---

## 4. CICLO DE VIDA E PERSISTÊNCIA

Ao abrir uma nova conversa ou novo terminal:
1. O agente carrega as regras globais nativamente pelo sistema.
2. O agente inspeciona o diretório de trabalho atual e lê o `AGENTS.md` do repositório.
3. As skills instaladas globalmente são descobertas pelos seus gatilhos no frontmatter.
4. O usuário **não precisa reinjetar prompts longos de contexto** a cada interação.
