---
name: renova-aura-pdf-delivery-guardian
description: Package fillable PDF deliverables with versioning, immutable originals, interactive and print copies, synthetic filled proof, field manifests, instructions, hashes and audit reports. Use before handing a PDF form to a client, professional reviewer or project team, especially when the form contains clinical, legal, financial or personal-data decisions.
---

# Renova Aura PDF Delivery Guardian

## Mission

Deliver a PDF form as a controlled, understandable and auditable package rather than a single unverified file.

## Required package

Unless explicitly reduced, the final folder contains only:

1. original source PDF, unchanged or referenced by hash;
2. interactive editable PDF;
3. static blank print PDF;
4. synthetic filled test PDF;
5. `README_FORMULARIO.md`;
6. `form_fields_manifest.json`;
7. `VALIDATION_REPORT.md`;
8. `SHA256SUMS.txt`.

Temporary renders, scripts, caches and debug files remain outside the delivery folder.

## Naming and versioning

Use stable names containing purpose and version. Never overwrite the approved original. Record generation date, source document version or source commit, page count and field count.

## README requirements

Explain in clear Portuguese:

### Computer

- download the PDF;
- open it in a tested viewer;
- fill one test field;
- save, close and reopen;
- continue filling;
- use “Save as” for the final copy.

### Mobile

- download the file;
- open it in the named tested app;
- do not edit only inside WhatsApp or e-mail preview;
- fill one test field;
- save a copy;
- close and reopen;
- send the saved PDF rather than screenshots.

### Print

- use the validated paper size;
- confirm margins and field boxes;
- sign manually when applicable;
- scan only when the digital copy cannot be returned.

State which viewers passed and which remain `NOT VERIFIED`. Explain that typed or drawn signatures are not automatically ICP-Brasil signatures.

## Field manifest

For every field record:

- name;
- type;
- page;
- rectangle;
- label or tooltip;
- default;
- options or on-states;
- multiline;
- required;
- read-only;
- print behavior;
- purpose;
- source decision ID when applicable.

The manifest must contain no real personal data.

## Validation report

Record:

- source and output hashes;
- page and field counts;
- PDF library and version;
- renderers and versions;
- structural checks;
- synthetic fill/save/reopen and value re-extraction;
- accented-text and multiline checks;
- checkbox/radio/choice checks;
- flattened/print check;
- visual comparison;
- viewer matrix;
- manual test owner/date;
- known limitations;
- rollback path.

Use only `PASS`, `FAIL`, `NOT RUN`, `NOT VERIFIED` or `BLOCKED`.

## Synthetic proof copy

Use visibly fake data and exercise identification, accented Portuguese text, multiline text, checkbox/radio, choice field, early/middle/late decisions, closing authorization and signature area without pretending it is legally signed.

## Hashes

Generate SHA-256 for every final artifact and regenerate after every modification. Do not claim files are identical without hash evidence.

## Privacy and public/private boundary

- No real patient, client, financial, legal or clinical data.
- No credentials, tokens, private URLs or production identifiers.
- No third-party upload without explicit authorization.
- Do not publish project-specific clinical decisions in a public generic skill.
- Keep generic workflow public and project decisions local.

## Delivery gate

Do not declare `READY_FOR_DELIVERY` unless:

- the original is preserved;
- the interactive PDF passes structural checks;
- values survive save and reopen;
- filled values appear in print/flatten output;
- accented and multiline text are verified;
- the final folder is clean;
- hashes match;
- viewer claims match evidence;
- pending mobile tests are explicit.

## Required final report

Use `EXECUTAR AGORA / PLANEJAR / ARQUIVAR`. Include delivery path, files, hashes, structural/save/print results, viewer matrix, package cleanliness, manual device tests, known limitations, original version and rollback.
