# Long-running handoff

Long work is split into bounded, verifiable blocks. Every resumed session rereads
applicable instructions, confirms repository state and revalidates current
evidence. Conversation memory and handoff prose are never authority.

## Sanitized package

Persist random opaque task/objective IDs and structured references only:

- state `DONE|PARTIAL|PLANNED|BLOCKED|NOT_RUN|UNKNOWN`;
- neutral repository alias, branch, HEAD and relative ownership references;
- decision, artifact, validation and test-result references;
- deliberately unexecuted items, risk/blocker and rollback references;
- immutable cumulative limits, usage-at-start, complete block delta and usage;
- task generation, loop instances, reopen count, start and absolute deadline;
- append-only terminal history and prior checkpoint SHA-256;
- approval and generation-decision IDs, never inline records;
- relative files to reread and one exact next-action code.

Never persist a raw objective/prompt, provider summary, raw error, credential,
PII, client/production identifier, private absolute path or deterministic public
hash of user text.

## Resume rule

Current branch, HEAD, status, file and trusted-store evidence win over handoff
claims. Record divergence before editing. Counters, deadline and history never
reset because a session, agent, retry or loop changed.

A handoff cannot issue, validate, consume or replace an ApprovalRecord or a
GenerationDecisionRecord. Reopening requires the typed, atomic synthetic-store
boundary bound to the canonical digest of the prior ledger. It remains unable to
authorize real work or external side effects.
