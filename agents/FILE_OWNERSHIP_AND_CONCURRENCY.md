# File ownership and concurrency

## Canonical claims (`RA-AOS-002`)

V1.1 accepts only repository-relative `EXACT` claims with explicit
`FILE|DIRECTORY`, owner, step, access and status. Globs are rejected rather than
interpreted differently by tools. Directory claims cover descendants; overlap
comparison is ancestral regardless of the caller-declared path type.

Normalization is fail-closed for Windows. It rejects absolute, UNC, device and
drive paths; traversal; empty/dot segments; globs; alternate streams; control
characters; reserved characters; leading spaces; trailing spaces/dots; short-
name tildes; Unicode compatibility aliases; and DOS device names such as `NUL`,
`CON`, `COM1` and `LPT1`, including names with extensions. The comparison key is
case-folded, but original validated segments are preserved for filesystem
inspection.

The repository root, every existing ancestor and the target are checked without
following symlinks. Symlinks, junctions and other reparse points fail. Existing
target type must match the declared type. Device/inode identity is compared so
hard links or filesystem aliases cannot evade a lexical intersection check.
Unknown/new preflight targets fail closed in this reference contract.

## Lifecycle and parallel preflight

Allowed lifecycle:

```text
PLANNED -> ACTIVE -> COMPLETE
PLANNED -> BLOCKED
ACTIVE  -> BLOCKED
```

`COMPLETE` and `BLOCKED` are terminal. Claim ID, path, type, access, owner, step
and dependencies are immutable. Preflight accepts `PLANNED|ACTIVE` claims,
checks target type and reparse ancestry, and blocks overlapping `WRITE/WRITE` or
`WRITE/READ` claims. `READ/READ` may coexist only without side effects.

## Diff reconciliation

Only an `ACTIVE + WRITE` claim for the exact owner and step can cover a real
diff. Reconcile every changed path, including both sides of a rename, while the
claim is still `ACTIVE`; then transition it to `COMPLETE`. `PLANNED`, `COMPLETE`,
`BLOCKED` and `READ` never authorize a mutation. Recheck reparse ancestry just
before the write and during reconciliation. Any unclaimed path, type mismatch,
alias, ownership change or reparse point produces `SCOPE_CHANGE` or
`SECURITY_BLOCK` and prevents integration.

The dependency-free checks and adversarial Windows probes live in
`agents/contract_checks.py` and `agents/tests/test_operating_contracts.py`.
