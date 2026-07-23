---
name: renova-aura-whatsapp-automation-reliability
description: Audit and design reliable WhatsApp and messaging workflows, including webhook verification, deduplication, ordering, outbox, templates, delivery states, handoff, opt-in, token security and reconciliation. Use for Meta WhatsApp, CRM or message automation boundaries.
---

# Renova Aura WhatsApp Automation Reliability

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

## Prohibited

No real message, provider connection, token access, broadcast, template submission or production webhook mutation without explicit verified approval.

## Output

Sequence diagram, state model, failure matrix, security gaps, test plan, observability, runbook and staged correction.

## Validation

Cover duplicate inbound, repeated status, out-of-order delivery, expired window, invalid signature, provider timeout and human handoff.

## Rollback

Any follow-up must permit disabling automation and returning safely to human/manual operation without losing conversation state.