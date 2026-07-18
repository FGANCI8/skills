---
name: renova-aura-observability-incident
description: Design or audit logs, metrics, traces, alerts, audit events, incident response, recovery, and operational runbooks for Renova Aura systems. Use for critical writes, webhooks, background jobs, provider integrations, production failures, or reliability improvements.
---

# Renova Aura Observability and Incident Response

## Mission

Make critical behavior explainable without leaking sensitive data. Detect meaningful failures, support diagnosis, and provide a reversible recovery path.

## Observability model

Define signals from the actual system:

- **logs** for structured event context;
- **metrics** for rates, latency, saturation, success and business-critical outcomes;
- **traces/correlation** for multi-step or distributed flows;
- **audit events** for sensitive state changes and privileged actions;
- **alerts** for conditions requiring action;
- **runbooks** for diagnosis, containment, recovery and verification.

Do not add telemetry that has no operator or decision use.

## Logging rules

Prefer structured logs with:

- event name;
- timestamp;
- request, correlation or job ID;
- safe user/owner/tenant attribution when permitted;
- module and operation;
- outcome and duration;
- sanitized error category;
- retry/attempt information;
- deployment/version context when available.

Never log raw secrets, authorization headers, full tokens, passwords, private prompts, unnecessary message bodies, clinical content, payment data or complete personal identifiers. Use redaction, hashing or bounded metadata according to project policy.

## Critical-flow instrumentation

For APIs, jobs, webhooks and external delivery, capture enough evidence to answer:

- Was the request/event accepted?
- Was validation, auth and authorization successful?
- Was a durable state change committed?
- Was the external provider called?
- What provider acknowledgement was received?
- Was delivery later confirmed, failed or left unknown?
- Was a retry attempted and why?
- Can the action be safely replayed?

Do not label queued or provider-accepted work as delivered unless the contract proves delivery.

## Metrics and SLOs

Choose a small actionable set:

- request/job success rate;
- p50/p95/p99 latency where meaningful;
- queue depth or oldest-item age;
- retry and dead-letter/unknown rate;
- webhook duplicate/replay rate;
- provider error rate;
- critical workflow completion rate;
- AI usage, latency, schema failure and cost when applicable.

Treat SLO targets without baseline as proposals, not facts.

## Alert design

An alert must include:

- condition and evaluation window;
- severity;
- expected operator action;
- link or reference to a runbook;
- noise-control strategy;
- recovery confirmation.

Avoid alerts on every individual error. Alert on user impact, sustained failure, security risk, data integrity risk or exhausted recovery capacity.

## Incident workflow

1. Confirm scope, environment and current impact.
2. Preserve evidence; do not destroy logs or unknown worktree state.
3. Contain blast radius with the safest reversible action.
4. Identify recent changes and failing dependency boundaries.
5. Distinguish code failure, configuration failure, provider failure and data corruption.
6. Recover using documented rollback, replay or manual reconciliation.
7. Verify user-facing behavior and data integrity.
8. Document timeline, root cause, contributing factors and follow-up actions.

Do not bypass auth, signatures, RLS, idempotency or safety controls to restore service.

## Recovery and replay

Before replaying or retrying, prove:

- idempotency key or deduplication strategy;
- terminal versus retryable state;
- side-effect status at the provider;
- ordering requirements;
- ownership/tenant scope;
- maximum attempts and backoff;
- operator-visible reconciliation path.

Unknown external outcome must not be blindly retried when duplication is harmful.

## Required output

- affected flow and impact;
- evidence timeline;
- signal gaps;
- containment and recovery actions;
- data integrity and security assessment;
- validations after recovery;
- root cause versus contributing factors;
- prioritized follow-up with owner and release gate;
- explicit rollback/replay instructions where safe.
