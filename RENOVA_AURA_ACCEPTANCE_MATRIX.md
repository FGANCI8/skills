# RENOVA AURA — MATRIZ DE CRITÉRIOS DE ACEITE E ESTADO REAL
## Avaliação de Prontidão da Infraestrutura Canônica de IA

**Data:** 27/10/2026 (Atualizado com Consolidação Concluída)  
**Responsável Técnico:** Agente Coordenador / Executor Técnico Antigravity  
**Empresa:** Renova Aura  
**Estados Permitidos:** `PASS`, `PARTIAL`, `BLOCKED`, `NOT_RUN`, `NOT_APPLICABLE`

---

## 1. MATRIZ CONSOLIDADA DE PRONTIDÃO OPERACIONAL

| Ambiente | Instalado | Descoberto | Utilizado | Persistente | Seguro | Veredito Geral |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Antigravity (IDE/CLI)** | **PASS**<br>(14 skills prioritárias em `%USERPROFILE%\.gemini\config\skills`) | **PASS**<br>(Reconhecidas nativamente pelo assistente) | **PASS**<br>(Testado empiricamente via subagente em sessão cega) | **PASS**<br>(Configuração global na pasta persistente da IDE) | **PASS**<br>(Zero Docker executado; fail-closed ativo) | **PASS** |
| **OpenAI Codex** | **PASS**<br>(26 skills instaladas em `%USERPROFILE%\.agents\skills`) | **PASS**<br>(Validado estaticamente por parser offline) | **NOT_RUN**<br>(`CLI_BINARY_NOT_IN_PATH`: binário CLI não exposto em PATH no terminal; créditos 100% preservados) | **PASS**<br>(`%USERPROFILE%\.codex\AGENTS.md` e regras globais ativas) | **PASS**<br>(Zero segredos; frontmatter e arquivos verificados) | **PARTIAL**<br>(Pronto localmente; runtime via IDE do usuário) |
| **ChatGPT** | **PASS**<br>(Via Conector GitHub para repositórios centrais) | **PASS**<br>(Consulta comprovada aos repositórios no GitHub) | **PASS**<br>(Histórico de consultas diretas a `FGANCI8/renova-aura-docs`) | **PASS**<br>(Adaptador formal `RA-CHATGPT-ADAPTER-001` v2.0 com 4 modalidades entregue) | **PASS**<br>(Zero segredos; testes desacoplados) | **PASS**<br>(Adaptador pronto para uso pelo proprietário) |
| **GitHub** | **PASS**<br>(Repositório `FGANCI8/skills` e `renova-aura-docs` mapeados) | **PASS**<br>(6 PRs reconciliadas na branch `consolidated/renova-aura-canonical-v1.2`) | **PASS**<br>(Suíte canônica de 21 testes com 100% PASS; commit `cace5ae`) | **PASS**<br>(Branch local consolidada com ancestralidade completa) | **PASS**<br>(Zero push/merge não autorizado executado) | **PASS**<br>(Pronto para revisão humana e push autorizado) |

---

## 2. DISCRIMINAÇÃO TRANSPARENTE DA REALIDADE OPERACIONAL

### 1. O QUE FUNCIONA HOJE (OPERACIONAL IMEDIATO)
- **Biblioteca Canônica Consolidada:** 34 skills unificadas na branch `consolidated/renova-aura-canonical-v1.2` (commit `cace5ae`), todas com o contrato basal `RA-AUTH-BASELINE-1`.
- **Segurança Preservada:** `renova-aura-security-data-guardian` unificada em 236 linhas, mantendo mitigações 2026 (CVE-2026-109618/109619 PHP2Shell, lifecycle Turnstile/reCAPTCHA, allowlist mass-assignment, 5 personas) e o contrato basal `RA-AUTH-BASELINE-1`.
- **34ª Skill Incorporada:** `renova-aura-infrastructure-guardian` (da PR #6) incorporada com testes, referências e contrato basal.
- **Governança Integrada:** `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` connector-first ativos na raiz.
- **Antigravity:** As 14 skills canônicas da Renova Aura estão ativas e sendo descobertas e utilizadas sem necessidade de citar seus nomes.
- **Isolamento Multiprojeto:** Comprovado que `Aura Clínica` (Python/FastAPI/Saúde) e `Zuno Imóveis` (Next.js/Imobiliário) mantêm suas arquiteturas e regras sem contaminação pelas regras de pintura/obras do `AuraServ`.
- **Suíte de Testes Canônica:** 21 testes determinísticos executados com 100% PASS (0 falhas).

### 2. O QUE JÁ ESTÁ CONFIGURADO E PREPARADO
- **OpenAI Codex:** Todas as 26 skills estão no disco (`%USERPROFILE%\.agents\skills`), com metadados `agents/openai.yaml`, frontmatters íntegros e hashes consistentes. O arquivo `%USERPROFILE%\.codex\AGENTS.md` está ativo com a governança Renova Aura.
- **ChatGPT:** O documento `RENOVA_AURA_CHATGPT_CANONICAL_ADAPTER.md` v2.0 está finalizado, com modalidades A (Gerais), B (Projetos), C (GitHub), D (Novos), com testes desacoplados.
- **GitHub:** O plano de consolidação das 6 PRs está montado, commitado na branch local `consolidated/renova-aura-canonical-v1.2` (`cace5ae`) sem quebrar o histórico.

### 3. O QUE DEPENDE DE AUTORIZAÇÃO HUMANA
- **Push e Abertura de PR de Consolidação no GitHub:** Conforme regra de segurança transversal, nenhuma escrita remota em `FGANCI8/skills` foi realizada. O proprietário precisa autorizar o comando `git push origin consolidated/renova-aura-canonical-v1.2` e a abertura da PR unificada direcionada à `main`.
- **Instruções de Projeto do ChatGPT:** O proprietário deve colar o conteúdo das modalidades A ou B de `RENOVA_AURA_CHATGPT_CANONICAL_ADAPTER.md` nas Instruções Personalizadas ou Instruções de Projeto no ChatGPT.
