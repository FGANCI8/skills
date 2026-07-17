---
name: renova-aura-pdf-forms-router
description: Route creation, repair, validation and delivery of fillable PDF forms to the minimum safe Renova Aura PDF skill set. Use when a PDF must preserve an approved visual identity while becoming fillable on desktop, mobile and paper, or when compatibility, saving, printing, AcroForm structure, appearance streams or auditability must be verified.
---

# Renova Aura PDF Forms Router

## Mission

Classify the real PDF task, preserve the approved source, select the minimum required PDF skills and prevent unsupported compatibility claims.

## Mandatory first read

Before acting, inspect when available:

1. project or workspace instructions;
2. the original PDF and any approved visual reference;
3. requested target viewers and devices;
4. field specifications, source documents and prior versions;
5. privacy, clinical, legal or customer-data restrictions;
6. available PDF tooling and renderer support.

Project-local instructions override this generic skill.

## Activation triggers

Use this router when the request includes:

- create a fillable or editable PDF;
- repair fields that do not work, save or print;
- preserve the same visual design while adding fields;
- support computer, Android, iPhone/iPad or printing;
- inspect AcroForm, XFA, widgets, field names or appearance streams;
- prove that values survive save, reopen and print;
- create interactive, print and synthetic test versions;
- produce manifests, hashes or an auditable delivery package.

## Routing

| Mode | Primary skill | Supporting skills |
|---|---|---|
| Create or rebuild a form | `renova-aura-fillable-pdf-architect` | compatibility auditor, delivery guardian |
| Repair an existing form | `renova-aura-fillable-pdf-architect` | compatibility auditor |
| Validate compatibility | `renova-aura-pdf-compatibility-auditor` | architect only when repair is authorized |
| Package deliverables | `renova-aura-pdf-delivery-guardian` | compatibility auditor |
| Produce a paper-only version | `renova-aura-fillable-pdf-architect` | delivery guardian |

## Non-negotiable rules

- Treat the original PDF as immutable and work on a copy.
- Preserve approved visual identity, page order, wording and content unless explicitly authorized.
- Prefer standard AcroForm fields. Do not introduce XFA, embedded JavaScript, server dependencies or proprietary plugins.
- Do not rely only on `/NeedAppearances`.
- Do not claim mobile or viewer compatibility without evidence from the named viewer or a clearly marked manual test.
- Browser, WhatsApp and e-mail previews are not proof that fields save correctly.
- Use synthetic data in tests. Never use real patient, client, financial, legal or clinical data.
- Do not state that a typed or drawn signature is an ICP-Brasil digital signature.
- Keep a printable path even when the interactive form is primary.
- Report every validation as `PASS`, `FAIL`, `NOT RUN`, `NOT VERIFIED` or `BLOCKED`.

## Required workflow

1. Preflight the original PDF.
2. Render and preserve a visual baseline.
3. Inspect form structure and field model.
4. Create or repair the form.
5. Generate field appearances.
6. Fill synthetic values programmatically.
7. Save, reopen and re-read values.
8. Render filled and print versions.
9. Compare against the baseline.
10. Package with manifest and hashes.
11. State which physical-device tests remain manual.

## Approval gates

Stop with `NEEDS_HUMAN_APPROVAL` before changing approved wording or branding, using real sensitive data, uploading to external services, replacing the PDF workflow with another product, removing audit information or declaring universal compatibility.

## Required output

Return task mode, sources inspected, selected skills, preservation constraints, compatibility targets, automated validations, manual validations, approval gates and final state: `SAFE_TO_PLAN`, `SAFE_TO_APPLY`, `SAFE_WITH_CAUTION`, `NEEDS_HUMAN_APPROVAL` or `BLOCKED`.
