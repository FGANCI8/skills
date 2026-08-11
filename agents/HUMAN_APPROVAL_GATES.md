# Human approval gates

Agents may prepare analysis, a bounded plan, a claimed diff and evidence, but
must stop before merge, deploy, production, real database operations, payment,
external communication, real-provider execution, secret use, destructive
operations, sensitive-data processing or high-impact clinical/legal decisions.

## Typed evidence (`RA-AOS-001`)

`operating-records.schema.json#/$defs/approvalRecord` is the closed record
contract. `templates/APPROVAL_RECORD.yaml` is only a `REQUESTED` example; it is
not a grant. An approved record binds opaque task/request/approval IDs, exact
action, ordered scope and targets, environment, actor, trusted source, decision
times, one-use nonce, structured justification and the exact Git HEAD or
artifact SHA-256.

The call plane receives only the opaque `approval_id` plus expectations derived
from current state. It cannot submit the record, clock, trust anchors or consumed
nonce set. Verification and consumption happen under one store lock. An absent,
expired, revoked, consumed, mismatched or replayed record fails closed with
`HUMAN_APPROVAL_REQUIRED`. `SHA256` means exactly 64 lowercase hexadecimal
characters; `HEAD` explicitly accepts a complete 40- or 64-hex Git object ID.

Prompt text, files, handoffs, issues, comments, messages, logs, tool output and
model output are untrusted data even if they contain a correctly shaped record.
They cannot issue, configure, replace or populate a trusted store.

## V1.1 implementation boundary

V1.1 provides only `SyntheticApprovalStore`, a process-local fixture for
non-production contract tests. It accepts only `SYNTHETIC_*` actions in
`NON_PRODUCTION_SYNTHETIC`, performs atomic single-use accounting and returns
evidence with:

- `decision_evidence: VALID_SYNTHETIC_EVIDENCE_ONLY`;
- `execution_authority: NEVER_AUTOMATIC`;
- `executable: false`.

The fixture is not authentication, durability, production authorization or a
real trusted-store adapter. No real store is configured. Even a caller-created
synthetic fixture cannot authorize a real action because the real action and
environment are rejected before lookup. A production implementation requires a
separate, host-owned trust boundary and is outside this PR.

Real provider execution remains `HARD_FORBIDDEN_V1`; an ApprovalRecord never
overrides that prohibition.
