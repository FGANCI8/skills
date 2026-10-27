# RENOVA AURA — ESCOPO E DELIMITAÇÃO DO PACOTE CANÔNICO V1.2

**ID:** `RA-PACKAGE-SCOPE-CANONICAL-V1.2`  
**Data:** 27 de Outubro de 2026  
**Versão do Pacote:** 1.2 (Revisão Corrigida para Homologação e Fechamento)  
**Repositório Base:** `FGANCI8/skills`  
**Branch Consolidada:** `consolidated/renova-aura-canonical-v1.2`  
**Status da Auditoria:** `PASS / PRONTO PARA REVISÃO HUMANA E FECHAMENTO`  

---

## 1. PROPÓSITO DO PACOTE

Este pacote (`RENOVA_AURA_CANONICAL_LIBRARY_READY_FOR_REVIEW_V2.zip`) é a distribuição de revisão e homologação independente da **Biblioteca Canônica Renova Aura Suite v1.2**, incorporando as correções apontadas na auditoria externa realizada pelo ChatGPT em 27/10/2026 sobre o pacote anterior.

O pacote foi desenhado para ser determinístico, auditável offline e 100% reproduzível em ambiente isolado.

---

## 2. ESCOPO INCLUÍDO NO PACOTE

O pacote contém exclusivamente a infraestrutura de agentes e skills da Renova Aura:

1. **34 Skills Canônicas Renova Aura (`skills/renova-aura-*`):**
   - 100% com frontmatter YAML íntegro.
   - 100% com manifesto de agente `agents/openai.yaml`.
   - 100% com cláusula basal de autoridade e segurança `RA-AUTH-BASELINE-1`.
   - Inclui a 34ª skill incorporada de PR #6: `renova-aura-infrastructure-guardian`.
   - Preserva todas as melhorias defensivas em `renova-aura-security-data-guardian` (PHP2Shell CVE-2026-109618/109619, ciclo Turnstile/reCAPTCHA, allowlist mass-assignment, 5 personas).

2. **18 Agentes Especializados (`agents/definitions/*.yaml`):**
   - 18 definições formais alinhadas ao Agent Operating System 1.1.

3. **Agent Operating System 1.1 (`agents/`):**
   - Esquemas JSON (`agent-team.schema.json`, `operating-records.schema.json`).
   - Módulos de verificação de contratos (`contract_checks.py`).
   - Protocolos (`LOOP_PROTOCOLS.md`, `FILE_OWNERSHIP_AND_CONCURRENCY.md`, `HUMAN_APPROVAL_GATES.md`, `LONG_RUNNING_HANDOFF.md`, `TEAM_ROUTING.md`, `TECHNICAL_REFERENCE.md`).
   - Templates operacionais e suíte completa de testes (`agents/tests/test_operating_contracts.py` — 41 testes).

4. **ProjectPacks (`project-packs/`):**
   - Catálogo de pacotes e matriz de projetos multi-domínio (`CATALOG.md`, `PROJECT_MATRIX.md`, `README.md`, `USAGE.md`, `VALIDATION.md`).
   - Manifesto formal de contrato (`MANIFEST.json`).
   - 4 adaptadores especializados (`project-packs/agents/`).
   - 5 cadernos de prompts universais e de canal (`project-packs/prompts/`).
   - Suíte de testes contratuais (`project-packs/tests/test_manifest_contract.py` — 4 testes).

5. **Documentação Canônica de Avaliação e Formulários (Correção P1 e P2):**
   - `RENOVA_AURA_AGENT_OS_EVALS.md` (Documento canônico contendo os contratos A01 a A30 com status `NOT_RUN` exigido pela suíte de testes).
   - `RENOVA_AURA_SKILLS_EVALS.md` (Matriz canônica de avaliações de skills).
   - `RENOVA_AURA_PDF_FORMS.md` e `RENOVA_AURA_PDF_FORMS_EVALS.md` (Especificação e avaliações de formulários preenchíveis PDF/AcroForms).
   - `RENOVA_AURA_SKILLS.md` e `RENOVA_AURA_AGENT_OS.md` (Documentos mestres de arquitetura).

6. **Governança Transversal e Adaptadores:**
   - `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` (Diretrizes permanentes transversais e regra `RA-GOV-TOOLS-001`).
   - `RENOVA_AURA_CHATGPT_CANONICAL_ADAPTER.md` (Adaptador ChatGPT v2.0 corrigido com referência à branch auditada `agent/ra-skills-base-v1` no commit `8f22a69b` e distinção dos 5 níveis operacionais).
   - `RENOVA_AURA_ACCEPTANCE_MATRIX.md`, `RENOVA_AURA_PERSISTENT_RULES_MATRIX.md`, `RENOVA_AURA_GITHUB_CANONICAL_CONSOLIDATION_PLAN.md`.
   - `RENOVA_AURA_INDEPENDENT_REVIEW.md` e `RENOVA_AURA_CODEX_PREPARATION_REPORT.md` (versão sanitizada).
   - `RENOVA_AURA_CHECKPOINT_RECUPERACAO_2026-10-27.md` (versão sanitizada).

---

## 3. ESCLARECIMENTO DE DELIMITAÇÕES E CONTRATOS (ACHADOS P2 E P3)

### A. Referências a `skills/docx`, `skills/pdf`, `skills/pptx`, `skills/xlsx` no `README.md`
- **Origem:** O arquivo `README.md` na raiz provém do repositório upstream original (`anthropics/skills`). Esse README cita pastas de demonstração de edição de documentos mantidas pela Anthropic (`skills/docx`, `skills/pdf`, `skills/pptx`, `skills/xlsx`).
- **Delimitação:** Essas pastas pertencem ao código de demonstração upstream e residem no repositório GitHub público. Elas **não integram a Biblioteca Canônica Renova Aura**, que possui sua própria suíte de formulários PDF (`renova-aura-fillable-pdf-architect`, `renova-aura-pdf-compatibility-auditor`, `renova-aura-pdf-delivery-guardian`, `renova-aura-pdf-forms-router`, `renova-aura-pdf-viewer-validation-runbook`).
- **Decisão:** O presente pacote de revisão contém estritamente as **34 skills Renova Aura**, evitando inchaço desnecessário e mantendo a contagem auditável de 34 skills. Os arquivos upstream permanecem rastreados no Git para o futuro merge geral no GitHub.

### B. Referência a `tools/` em `RENOVA_AURA_SKILLS.md`
- O texto de `RENOVA_AURA_SKILLS.md` (linha 134) define explicitamente que scripts de instalação automática global (`tools/install-renova-aura-skills-global.ps1`) pertencem à fase posterior de automação de instalação (PR E).
- Na presente fase de consolidação da biblioteca, a instalação global é formal e factualmente declarada como `NOT_RUN`. Não existem scripts de instalação não testados no pacote.

### C. Semântica de `combined_skills: 33` em `project-packs/MANIFEST.json`
- O arquivo `MANIFEST.json` do ProjectPacks define o contrato estático da versão 1.1.0-draft do subsistema ProjectPacks:
  - `base_skills: 25` (skills da PR #2)
  - `extension_skills: 8` (skills especializadas de projeto da PR #3)
  - `combined_skills: 33` (25 + 8)
- A 34ª skill (`renova-aura-infrastructure-guardian`) foi incorporada na consolidação geral v1.2 (PR #6) e pertence ao catálogo central de infraestrutura, não alterando retroativamente o contrato do manifesto histórico do ProjectPacks v1.1.
- O teste automatizado `project-packs/tests/test_manifest_contract.py` valida rigorosamente essa soma (`25 + 8 == 33`). O valor 33 foi preservado para garantir 100% de compatibilidade contratual e conformidade dos testes.

### D. Exclusão Total de Caches
- 100% dos diretórios `__pycache__` e arquivos `*.pyc` foram excluídos da rotina de empacotamento, garantindo um pacote limpo apenas com código-fonte e documentação.

### E. Escopo do Manifesto SHA-256 (`MANIFEST-SHA256.txt` — ZIP Windows vs. Checkout Git)
- **Delimitação de Escopo do Manifesto:** O arquivo `MANIFEST-SHA256.txt` foi gerado a partir dos bytes exatos dos arquivos empacotados no arquivo ZIP de distribuição Windows (`RENOVA_AURA_CANONICAL_LIBRARY_READY_FOR_REVIEW_V2.zip`), preservando as terminações de linha padrão do Windows (`CRLF`, `\r\n`). Todos os 166 arquivos contidos no ZIP conferem 100% com esse manifesto.
- **Diferenciação com Checkout Git (Normalização LF):** O Git normaliza automaticamente quebras de linha para `LF` (`\n`) no armazenamento interno do repositório (`core.autocrlf` / `.gitattributes`). Consequentemente, checkouts em sistemas Unix/Linux ou em ambientes com normalização LF produzirão hashes SHA-256 divergentes para arquivos de texto (exemplo verificado: `RENOVA_AURA_AGENT_OS_EVALS.md` possui hash CRLF `0de239b747414f011e0f91949e530c6ee273b125296a42860c75bd92fa8f4f38` no ZIP e hash LF `518313d8cc0a6c3ae0c4b385cf4fbb47f7a3471051d71c7a8514abfe818163a4` no objeto Git), embora o conteúdo textual e semântico permaneça rigorosamente idêntico.
- **Diretriz de Integridade:** O arquivo `MANIFEST-SHA256.txt` é estritamente o manifesto de integridade do arquivo ZIP de homologação e não deve ser empregado como validador de checkouts Git arbitrários em sistemas não-Windows ou com LF.
- **Integridade Canônica do Git e CI Remoto:** A integridade do repositório Git é garantida criptograficamente pela árvore de objetos do Git e validada de ponta a ponta pela execução automatizada dos 45 testes no GitHub Actions (`.github/workflows/ci.yml`).
- **Preservação de Conteúdo:** Não foram alterados arquivos para forçar igualdade artificial de hashes, preservando o manifesto original do ZIP e a normalização padrão do Git sem riscos de regressão.

---

## 4. INSTRUÇÕES DE REPRODUÇÃO ISOLADA OFFLINE

Para reproduzir os testes de forma independente a partir do ZIP em qualquer máquina com Python 3.10+:

```bash
# 1. Extrair o arquivo RENOVA_AURA_CANONICAL_LIBRARY_READY_FOR_REVIEW_V2.zip em uma pasta limpa:
unzip RENOVA_AURA_CANONICAL_LIBRARY_READY_FOR_REVIEW_V2.zip -d /tmp/renova-aura-isolated
cd /tmp/renova-aura-isolated

# 2. Executar os 41 testes de contratos do Agent OS:
python -m pytest agents/tests
# Ou via unittest:
python -m unittest discover -s agents/tests

# 3. Executar os 4 testes de contratos do ProjectPacks:
python -m pytest project-packs/tests
# Ou via unittest:
python -m unittest discover -s project-packs/tests

# Resultado esperado: 45/45 PASS.
```
