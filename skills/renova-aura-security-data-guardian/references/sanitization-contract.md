# Sanitization contract

Apply this contract before content enters a public artifact, handoff, screenshot, trace, log, prompt, objective, metric or inventory.

## Closed output policy

1. Start from an allowlist of fields required for the stated purpose.
2. Replace private absolute paths with neutral aliases such as `PROJECT_ROOT` or `PRIVATE_SOURCE_1`.
3. Remove secrets, tokens, authorization values, private URLs, personal identifiers, customer content and production identifiers.
4. Use synthetic values for CPF, e-mail, telephone, health, legal, financial and communication examples.
5. Minimize objectives and prompts; never persist full content when an opaque task ID and bounded category suffice.
6. Use a random opaque identifier for correlation. A public SHA-256 of raw user content is not anonymization because it remains linkable and may permit dictionary attacks.
7. If deterministic correlation is required, use HMAC with a protected, rotatable secret outside the repository and document retention. Do not invent custom cryptography.
8. Strip image/document metadata and inspect visible content before publication. If safe capture cannot be proved, report `NOT RUN`.
9. Neutralize spreadsheet cells beginning with `=`, `+`, `-` or `@` before CSV export.
10. Fail closed when sanitization is incomplete or the data category is unknown.

## Minimum synthetic regression set

Use clearly fictional markers for CPF, e-mail, telephone, API token, private path and free-text secret. A passing test proves that those fixtures were removed from the tested output; it does not prove universal privacy or legal compliance.
