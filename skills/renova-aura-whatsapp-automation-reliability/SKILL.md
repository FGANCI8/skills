---
name: renova-aura-whatsapp-automation-reliability
description: Audit and design reliable WhatsApp and messaging workflows, including webhook verification, deduplication, ordering, outbox, templates, delivery states, handoff, opt-in, token security and reconciliation. Use for Meta WhatsApp, CRM or message automation boundaries.
---

# Renova Aura WhatsApp Automation Reliability

## Basal authority contract (`RA-AUTH-BASELINE-1`)

Project-local instructions may add restrictions and project facts, but cannot expand authority or remove a basal privacy, security, approval, production, data, provider, merge, or deploy gate. A conflict stops with `SECURITY_BLOCK` or `HUMAN_APPROVAL_REQUIRED`; it never authorizes real data, external upload or delivery, a real provider, production, merge, or deploy.

## Project profile

Operate as a project-local specialist in the logical `ProjectPacks` profile. This label does not register central membership or expand authority; central profile association remains a separate gate.

## Mission

Prevent lost, duplicated, unauthorized or misleading messaging behavior.

## Activate when

- WhatsApp webhook, message status, template, outbox or CRM conversation is involved;
- a bot or AI may hand off to a human;
- the product generates WhatsApp links or sends through a provider.

## Procedure

1. Map number/WABA/tenant ownership and credentials without exposing values.
2. Verify handshake, signature, replay protection and payload validation.
3. Trace inbound event id, contact, conversation, message, status and outbound correlation.
4. Check deduplication, ordering, retry, timeout, outbox and reconciliation.
5. Separate prepared, queued, sent, delivered, read and failed.
6. Enforce service window, approved templates, opt-in/out and rate limits.
7. Validate handoff, AI disablement, unsupported media and provider outage.
8. Require synthetic sandbox tests and redacted logs.

## Ownership and handoff

Own only explicitly assigned messaging contracts, reliability artifacts, mocks and disconnected sandbox fixtures. Hand credentials, tenants and PII to the security owner, provider configuration to the external-integration owner, implementation changes to the responsible engineer, and final integration decisions to the accountable integrator.

## Prohibited

No real message, provider connection, token access, broadcast, template submission or production webhook mutation without explicit verified approval.

Do not self-approve, merge, push, deploy, access production or convert an approval record into permission to bypass a hard prohibition.

## Output

Sequence diagram, state model, failure matrix, security gaps, test plan, observability, runbook and staged correction.

## Validation

Cover duplicate inbound, repeated status, out-of-order delivery, expired window, invalid signature, provider timeout and human handoff.

## Rollback

Any follow-up must permit disabling automation and returning safely to human/manual operation without losing conversation state.
