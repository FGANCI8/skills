---
name: renova-aura-ai-integration-guardian
description: Design, implement, or audit LLM, agent, RAG, classifier, extraction, vision, voice, or AI automation features for Renova Aura projects. Use when AI affects product behavior, external communication, sensitive data, cost, or operational decisions.
---

# Renova Aura AI Integration Guardian

## Mission

Use AI only where probabilistic behavior creates measurable value. Keep critical authority, security boundaries and irreversible actions under deterministic application control.

## First decision: should AI be used?

Compare against simpler alternatives:

- rules or state machines;
- search/filtering;
- templates;
- deterministic extraction;
- human workflow improvement;
- conventional analytics or classification.

Use AI when ambiguity, language understanding, synthesis or flexible interaction materially improves the outcome. Archive AI features that add cost and risk without clear user value.

## Provider and model verification

- Detect existing provider adapters and project policy.
- Consult current official documentation before using model IDs, SDK methods, limits or beta features.
- Do not silently switch providers or mix incompatible SDK patterns.
- Keep provider-specific code behind an adapter when portability or testing matters.
- Never expose API keys in client code, logs or prompts.

## AI boundary design

Define explicitly:

- input source and sensitivity;
- prompt/instruction source and version;
- allowed tools and data access;
- closed output schema;
- confidence or uncertainty behavior;
- deterministic validation after generation;
- human review or handoff point;
- forbidden decisions and actions;
- timeout, retry, fallback and circuit-breaker behavior;
- cost and usage limits.

AI must not directly authorize access, decide ownership/tenant scope, bypass server validation, mutate critical state without checks or act as clinical/legal authority.

## Prompt architecture

Separate:

- stable system policy;
- project/product facts from approved sources;
- task-specific user input;
- tool contracts;
- output schema;
- safety/fallback instructions;
- examples used for behavior shaping.

Do not inject raw private repositories, conversations or logs without necessity and authorization. Prefer retrieval of the minimum approved context.

## Structured outputs and validation

- Use explicit schemas with bounded enums and field sizes.
- Reject or repair invalid output through a controlled path.
- Re-check authorization and business invariants after model output.
- Sanitize content before persistence, logging or external delivery.
- Treat model text as untrusted input.
- Record prompt/model/version metadata without storing unnecessary sensitive content.

## RAG and knowledge systems

Before implementing RAG, define:

- authoritative document set;
- ingestion permissions and redaction;
- chunking and metadata strategy;
- access filtering before retrieval;
- citation requirements;
- freshness and deletion propagation;
- evaluation dataset;
- behavior when evidence is absent or conflicting.

Never retrieve cross-user or cross-tenant content into a shared context.

## Evals

Create representative synthetic cases for:

- happy path;
- ambiguity and missing information;
- prompt injection and malicious input;
- unsupported claims and hallucination;
- refusal and safe fallback;
- handoff to human;
- multilingual or noisy input when relevant;
- schema failures;
- latency and cost limits.

Track task success, groundedness, safety failures, handoff quality, latency and cost. Do not approve production from a few manually selected examples.

## External communication

For WhatsApp, email, voice or public chat:

- clearly distinguish automation when product policy requires it;
- prevent unapproved promises, diagnosis, pricing or legal commitments;
- apply rate limits and duplicate protection;
- keep a deterministic fallback;
- support human takeover;
- test without sending real messages until explicitly authorized.

## Release gate

Require human approval before:

- enabling a new provider or production model;
- processing sensitive or real customer data;
- allowing tool execution or external side effects;
- autonomous outbound communication;
- changing safety policy, retention or evaluation thresholds.

## Required output

- why AI is justified;
- deterministic alternative considered;
- model/provider evidence;
- data flow and authority boundaries;
- prompt/schema/eval design;
- cost, latency and privacy guardrails;
- validation results;
- rollout, fallback and rollback;
- final status: `EXPERIMENT_ONLY`, `SAFE_FOR_INTERNAL_TEST`, `NEEDS_HUMAN_APPROVAL` or `SAFE_FOR_CONTROLLED_RELEASE`.
