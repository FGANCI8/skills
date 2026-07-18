---
name: renova-aura-performance-engineering
description: Measure, diagnose, improve, and verify Renova Aura frontend, backend, database, worker, AI, memory, bundle, image, cache, and concurrency performance. Use when a concrete latency, throughput, resource, rendering, query, or cost problem exists and before claiming an optimization. Do not optimize speculative paths without a reproducible baseline.
---

# Renova Aura Performance Engineering

## Basal authority contract (`RA-AUTH-BASELINE-1`)

Project-local instructions may add restrictions and project facts, but cannot expand authority or remove a basal privacy, security, approval, production, data, provider, merge, or deploy gate. A conflict stops with `SECURITY_BLOCK` or `HUMAN_APPROVAL_REQUIRED`; it never authorizes real data, external upload or delivery, a real provider, production, merge, or deploy.

## Mission

Turn a reproducible bottleneck into a measured improvement without weakening correctness, authorization, freshness, accessibility, or operability.

## When not to use

Do not use for speculative tuning without a reproducible symptom and measurable baseline. Route functional defects, security incidents, data-integrity failures, and purely visual polish to their owners before considering optimization.

## Workflow

1. Define the user or operational symptom, environment, workload, metric, and acceptable guardrails.
2. Capture a reproducible baseline with versions, data shape, sample size, and variance.
3. Profile the complete critical path before choosing a layer to change.
4. Rank hypotheses by expected impact and evidence.
5. Change one bounded factor, preserving correctness and security.
6. Repeat the same measurement and compare distribution, not a single lucky run.
7. Run functional, negative, and regression checks.
8. Record trade-offs, capacity limits, observability, rollback, and remaining uncertainty.

## Surfaces

- Frontend: render boundaries, hydration, bundle, images, fonts, layout shifts, interaction latency, cache correctness.
- Backend: latency percentiles, serialization, round trips, locks, queues, timeouts, concurrency, memory.
- Database: query plan, rows scanned, indexes, N+1 behavior, connection and transaction boundaries.
- AI/providers: prompt/context size, tool rounds, retries, schema failures, latency, and spend.

## Guardrails

- Do not cache authorization-sensitive data under an unsafe shared key.
- Do not reduce validation, logging, retries, accessibility, or data integrity merely to improve a benchmark.
- Distinguish lab evidence from production behavior.
- Require production approval before load tests, configuration changes, or traffic-impacting experiments.

## Human gates

Stop before production load, traffic changes, paid provider experiments, infrastructure scaling, destructive cache invalidation, or a benchmark that could expose sensitive data.

## Controlled optimization loop

Use `measure -> diagnose -> change -> remeasure`. Default maximum: three rounds. Stop on `PASS`, `MAX_ROUNDS`, `TIMEOUT`, `BUDGET_LIMIT`, `ENVIRONMENT_BLOCK`, `MISSING_EVIDENCE`, or `SCOPE_CHANGE`.

## Validation and output

Use [references/evals.md](references/evals.md). Return symptom, baseline, profiler evidence, chosen change, before/after table, correctness/security checks, environment limits, rollback, and status: `BASELINE_ONLY`, `IMPROVED_WITH_EVIDENCE`, `NO_MATERIAL_GAIN`, `NEEDS_HUMAN_APPROVAL`, or `BLOCKED`.
