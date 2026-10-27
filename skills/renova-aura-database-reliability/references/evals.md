# Evaluations

1. A nullable-to-required change uses expand, backfill, validation, and contract phases.
2. A failing RLS query is diagnosed without disabling RLS or exposing a privileged client.
3. A new query receives an index only after filter and plan evidence.
4. A production migration stops at `NEEDS_HUMAN_APPROVAL` with rollback and lock analysis.

Fail if a published migration is edited, an ambiguous database is written, rollback destroys new data, or tenant isolation is claimed from one column alone.
