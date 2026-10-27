# Security verification baseline

Use only the sections relevant to the observed system. Record `NOT_VERIFIED` when evidence is unavailable.

## Current reference set

- [OWASP ASVS 5.0.0](https://github.com/OWASP/ASVS/tree/v5.0.0_release): detailed verification requirements for web applications and services.
- [OWASP Top 10:2025](https://owasp.org/Top10/2025/): awareness baseline for current web application risk categories.
- [OWASP API Security Top 10:2023](https://owasp.org/API-Security/editions/2023/en/0x11-t10/): API authorization, resource, business-flow, SSRF, inventory, and third-party consumption risks.
- [NIST SP 800-218 SSDF 1.1](https://csrc.nist.gov/pubs/sp/800/218/final): secure software development practices across the lifecycle.
- [NIST SP 800-218A](https://csrc.nist.gov/pubs/sp/800/218/a/final): additional secure development practices for generative AI and foundation-model systems.

Check official sources for newer stable versions before using numbered requirements. Pin cited ASVS identifiers with the version, such as `v5.0.0-...`.

## Architecture and threat model

- assets, actors, roles, entry points, data flows, trust boundaries;
- privileged components and external providers;
- expected abuse cases and exceptional conditions;
- prevention, detection, containment, recovery, and audit evidence.

## Identity, authentication, and session

- server-trusted identity source;
- login, enrollment, recovery, verification, MFA, OAuth callback, logout;
- session creation, rotation, revocation, expiry, cookie/token protection;
- CSRF and cross-origin behavior;
- no authentication detail that enables user enumeration;
- safe behavior for stale, missing, malformed, or conflicting identity state.

## Authorization and isolation

- deny-by-default policy;
- object, property, and function-level checks;
- role/admin/support boundaries;
- owner/tenant source and membership lifecycle;
- repository/query scoping plus database policy where applicable;
- cache, search, export, storage, background-job, and audit-log scoping;
- negative cross-scope tests with synthetic identities.

## Input, output, and files

- closed server-side schemas and bounded values;
- injection-safe database, command, template, and parser use;
- context-aware output encoding;
- upload size/type/content/storage/serving controls;
- decompression and archive limits;
- untrusted document, image, and metadata handling.

## API and integration

- endpoint/version inventory;
- authentication, authorization, signature, replay, and idempotency;
- payload, pagination, batch, time, memory, concurrency, retry, and spend limits;
- sensitive business-flow anti-automation;
- SSRF-safe outbound destinations, DNS/IP checks, protocols, and redirects;
- timeouts, response-size limits, schema validation, and safe redirects for third-party APIs;
- reconciliation for unknown external outcomes.

## Data protection and privacy

- data categories, purpose, minimization, retention, deletion, export, redaction;
- encryption in transit and at rest where required;
- key and secret ownership, rotation, revocation, and audit;
- log, analytics, prompt, AI trace, backup, and support-tool exposure;
- special handling for health, financial, legal, precise-location, and communication content.

## Supply chain and build

- dependency source, lockfile, signature/provenance where available;
- known vulnerabilities interpreted in context;
- build and lifecycle scripts;
- CI identities, permissions, secrets, artifacts, and protected release flow;
- generated files and vendored code;
- no unreviewed forceful dependency upgrades.

## Configuration and exceptional conditions

- production-safe defaults and environment separation;
- debug endpoints, headers, CORS, cookies, TLS, proxy trust, and error pages;
- fail-closed behavior for missing auth, policy, provider, environment, or rate-limit state;
- partial writes, concurrency, timeout, retry exhaustion, and rollback;
- logging and alerting for security-relevant failures without sensitive payloads.

## Verification evidence

- focused static inspection;
- unit/contract negative tests;
- isolated integration tests;
- authorized runtime/configuration evidence;
- dependency and secret scanning;
- manual abuse-case validation;
- residual `NOT_VERIFIED` areas and explicit release blockers.
