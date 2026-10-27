# RENOVA AURA — PLANO CANÔNICO DE CONSOLIDAÇÃO DO GITHUB
## Estratégia de Unificação da Biblioteca de Skills (`FGANCI8/skills`)

**ID:** `RA-GITHUB-CONSOLIDATION-001`  
**Data:** 27/10/2026 (Atualizado com Consolidação Concluída)  
**Repositório Alvo:** `https://github.com/FGANCI8/skills`  
**Branch Canônica Local Pronta:** `consolidated/renova-aura-canonical-v1.2`  
**HEAD Local:** `cace5ae`  
**Governança:** `https://github.com/FGANCI8/renova-aura-docs`  
**Estado de Autorização:** CONSOLIDAÇÃO LOCAL CONCLUÍDA E TESTADA; **PUSH, MERGE, REBASE REMOTO OU ALTERAÇÃO DE MAIN BLOQUEADOS AGUARDANDO DECISÃO HUMANA DO PROPRIETÁRIO**.

---

## 1. RESUMO EXECUTIVO DO DIAGNÓSTICO DAS PULL REQUESTS

No repositório central `FGANCI8/skills`, a branch `origin/main` é um fork do repositório upstream (Anthropic skills) e ainda não contém os artefatos da Renova Aura. O trabalho técnico encontra-se distribuído em seis Pull Requests históricas, agora 100% reconciliadas e unificadas na branch local `consolidated/renova-aura-canonical-v1.2`:

| PR | Branch de Origem | Branch Base | Título / Escopo | Status na Consolidação Local |
|---|---|---|---|---|
| **#1** | `agent/renova-aura-project-skills-v1` | `main` | Add Renova Aura reusable project and PDF skill system (158 arquivos) | **TOTALMENTE ABSORVIDA E SUPERSEDIDA** pelas PRs modulares. Nenhuma instrução ou teste foi perdido. |
| **#2** | `agent/ra-skills-base-v1` | `main` | Renova Aura V1.1 A: biblioteca base e skills (65 arquivos) | **INCORPORADA**. 25 skills basais, `RENOVA_AURA_SKILLS.md`, `spec/`, `template/` e contrato basal `RA-AUTH-BASELINE-1`. |
| **#3** | `agent/ra-project-prompt-packs-v1` | `agent/ra-skills-base-v1` | Renova Aura V1.1 C: prompt packs, completeness audits and project adapters | **INCORPORADA**. 8 extension skills, 4 project adapters, 23 prompts (`P01`–`P17`, `T01`–`T06`) e documentação alinhada. |
| **#4** | `agent/ra-agent-os-v1` | `agent/ra-skills-base-v1` | Renova Aura V1.1 B: Agent OS e agentes (43 arquivos) | **INCORPORADA**. 18 agentes canônicos, templates operacionais, `TASK_LEDGER.yaml` e suíte de contratos. |
| **#5** | `docs/adopt-ra-gov-tools-001-20261022` | `main` | docs(agents): adotar governança canônica RA-GOV-TOOLS-001 | **INCORPORADA**. `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` adicionados na raiz da branch consolidada. |
| **#6** | `codex/infrastructure-guardian-v0.3` | `main` | feat(skills): Infrastructure Guardian v0.3.0 candidata | **INCORPORADA**. 34ª skill (`skills/renova-aura-infrastructure-guardian/`) adicionada com contrato `RA-AUTH-BASELINE-1`. |

---

## 2. ESTADO REAL DA CANDIDATA CONSOLIDADA

- **Branch Local:** `consolidated/renova-aura-canonical-v1.2`
- **Commit SHA:** `cace5ae`
- **Total de Skills:** Exatamente 34 skills canônicas em `skills/` (todas com `SKILL.md`, `agents/openai.yaml` e `RA-AUTH-BASELINE-1`).
- **Segurança Preservada:** `renova-aura-security-data-guardian` unificada em 236 linhas, mantendo mitigações 2026 (CVE-2026-109618/109619 PHP2Shell, lifecycle Turnstile/reCAPTCHA, allowlist mass-assignment, 5 personas) e o contrato basal `RA-AUTH-BASELINE-1`.
- **Governança Integrada:** `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` connector-first ativos na raiz.
- **Suíte de Testes:** 21/21 testes determinísticos executados com **100% PASS**.
- **Sanitização:** Zero segredos detectados em código ou documentação.

---

## 3. PROCEDIMENTO PARA PUBLICAÇÃO NO GITHUB (EXIGE AUTORIZAÇÃO HUMANA)

Quando o proprietário autorizar a publicação remota:

```powershell
# 1. Enviar a branch consolidada para o GitHub (SEM forçar e SEM alterar main diretamente)
git push origin consolidated/renova-aura-canonical-v1.2

# 2. Abrir Pull Request no GitHub:
#    Base: main
#    Compare: consolidated/renova-aura-canonical-v1.2
#    Título: "feat(canonical): Renova Aura Canonical Suite v1.2 (34 skills, Agent OS 1.1, ProjectPacks, Governance)"

# 3. Após revisão humana e merge da PR consolidada na main:
#    Fechar PRs #1, #2, #3, #4, #5 e #6 com nota:
#    "Superseded by canonical consolidation PR #X (consolidated/renova-aura-canonical-v1.2)"
```
*(Nota: Nenhuma etapa de push remoto foi executada neste momento).*
