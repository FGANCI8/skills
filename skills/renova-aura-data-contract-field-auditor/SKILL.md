---
name: renova-aura-data-contract-field-auditor
description: Trace every material field and relationship across UI, validation, API, service, database, search, integration, reporting and lifecycle to find missing, inconsistent, excessive or unusable data contracts. Use when a product may be missing fields or an integration depends on incomplete data.
---

# Renova Aura Data Contract and Field Auditor

## Mission

Prevent flows that look complete in the interface but cannot persist, search, integrate, report or operate correctly.

## Activate when

- the user suspects a missing field;
- an address, map, payment, message, document, order or report fails downstream;
- UI/types/API/schema use different names or types;
- a new provider or feature needs existing data.

## Sources

Read forms, labels, masks, types, schemas, server validation, APIs, services, repositories, migrations, RLS, indexes, providers, exports, analytics and tests.

## Procedure

1. Identify entities, relations and critical journeys.
2. Build a canonical field ledger with purpose, source, type, format, nullability, requiredness, enum/unit/timezone, sensitivity, owner/tenant and lifecycle.
3. Trace origin → capture → normalize → validate → authorize → persist → query/edit → search/filter → integrate → report/export → retain/delete.
4. Detect missing, orphan, duplicated, renamed, conflicting, over-collected and derived-without-source fields.
5. Inspect relationship contracts and technical identifiers only when justified.
6. Apply data minimization; a field without legitimate purpose is a finding, not an automatic addition.

## Required findings

Classify `BLOCKER`, `HIGH`, `MEDIUM`, `LOW` or `NOT_NEEDED`. Include evidence, affected layers, impact, canonical contract and tests.

## Gates

No migration, schema change, real data query or external provider call in audit mode. Auth, tenant, RLS, health, financial and legal fields require security/privacy review.

## Output

Entity inventory, field-by-layer matrix, missing/excess fields, naming/type mismatches, integration gaps, proposed contract, affected files/tables, test matrix and staged plan.

## Validation

Every blocker must show the broken journey and at least two affected layers. Every recommended field must have purpose, consumer and retention rationale.

## Rollback

Read-only by default. Any later implementation must use reversible migrations, compatibility strategy and rollback plan.