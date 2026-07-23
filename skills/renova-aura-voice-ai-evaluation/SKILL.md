---
name: renova-aura-voice-ai-evaluation
description: Evaluate voice capture, speech-to-text, structured field extraction, confirmation, privacy, latency, cost and fallback using measurable per-field evals. Use for voice budgets, lead capture, transcription or command workflows.
---

# Renova Aura Voice AI Evaluation

## Mission

Measure whether voice reliably produces the structured data needed for a safe user action.

## Activate when

- audio is recorded or uploaded;
- STT/transcription feeds forms, quotes, leads or automations;
- the user asks about voice quality or missing extracted fields.

## Procedure

1. Map capture permission, format, duration, upload and retention.
2. Define the canonical structured output and per-field validation.
3. Build synthetic or explicitly consented eval cases: noise, accents, numbers, currency, dimensions, dates, names, addresses, corrections and contradictions.
4. Measure transcription plus field precision, recall, completeness and correction rate.
5. Define confidence, confirmation and manual-edit behavior before side effects.
6. Test timeout, network loss, provider outage, prompt injection by audio and unsupported formats.
7. Compare cost, latency and fallback to typed form.

## Gates

No real personal audio or provider upload without explicit approval and privacy basis. No automatic financial, health, legal or irreversible action from unconfirmed extraction.

## Output

Audio/data flow, schema, eval dataset plan, metrics, failure cases, confirmation UX, fallback, cost/latency guardrails and test commands.

## Validation

A passing transcript alone is insufficient. Every required business field must have a metric and acceptance threshold approved as hypothesis or baseline.

## Rollback

Keep typed/manual input available and permit disabling voice without blocking the core journey.