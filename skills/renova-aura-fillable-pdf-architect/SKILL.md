---
name: renova-aura-fillable-pdf-architect
description: Create or repair standards-based AcroForm PDFs while preserving approved design, supporting editable desktop/mobile use and a separate print version. Use when building real text, multiline, checkbox, radio or choice fields; correcting AcroForm structure, widgets, fonts, appearances, tab order or Portuguese text; or generating interactive, printable and synthetic test copies.
---

# Renova Aura Fillable PDF Architect

## Basal authority contract (`RA-AUTH-BASELINE-1`)

Project-local instructions may add restrictions and project facts, but cannot expand authority or remove a basal privacy, security, approval, production, data, provider, merge, or deploy gate. A conflict stops with `SECURITY_BLOCK` or `HUMAN_APPROVAL_REQUIRED`; it never authorizes real data, external upload or delivery, a real provider, production, merge, or deploy.

## Mission

Produce a standards-based, visually faithful and auditable PDF form whose values are real, editable, savable, reopenable and printable.

## Authoring path

Choose the smallest reliable path:

- existing approved PDF: preserve as visual background and add or rebuild AcroForm fields;
- text-heavy document still under design: prefer DOCX, convert, then add fields;
- slide-like fixed layout: prefer PPTX, export, then add fields;
- programmatic fixed form: ReportLab or another deterministic PDF library is acceptable;
- paper-only form: create a separate static print PDF rather than pretending static boxes are interactive.

## Immutable baseline

Before editing:

1. copy the original;
2. record SHA-256, page count, dimensions, metadata and encryption state;
3. render every page;
4. preserve the baseline renders;
5. record approved typography, colors, margins, headers, footers and page order.

The original must remain unchanged.

## Field manifest

Every field needs:

- globally unique name;
- label and tooltip;
- type;
- page and rectangle;
- default value;
- options or valid on-states;
- multiline flag;
- required/read-only flags;
- purpose;
- tab order;
- print behavior.

Do not reuse one name for unrelated widgets.

## AcroForm requirements

The interactive PDF must have:

- catalog `/AcroForm`;
- `/Fields` referencing actual top-level fields;
- widgets in the correct page `/Annots`;
- valid `/Rect`, `/Subtype /Widget` and page association;
- consistent field/widget hierarchy;
- valid default appearance for text fields;
- every `/DA` font present in form resources;
- valid `/V` and `/AS` for button fields;
- valid `/Opt` for choice fields;
- no unintended read-only, hidden or no-export flags;
- no orphan widgets or duplicate names;
- no XFA, embedded JavaScript, password or restriction preventing fill/print.

## Appearance streams

A value existing in `/V` is not enough.

- Generate appearances for text, multiline, checkbox, radio and choice fields.
- Do not depend exclusively on `/NeedAppearances`.
- Prefer `/NeedAppearances false` after valid appearances are generated.
- Verify difficult forms in two independent renderers.
- Confirm print or flattened output displays the same values.
- Never flatten the interactive master.

## Portuguese and typography

- Support accents and cedilla.
- Configure form fonts correctly.
- Verify `á à â ã é ê í ó ô õ ú ç` and uppercase variants.
- Reject broken glyphs, black squares or missing characters.
- Keep mobile and paper font sizes readable.
- Allow multiline wrapping without disappearing or clipping.

## Mobile-friendly controls

Prefer simple text, multiline, checkbox, radio and verified simple dropdown fields. Avoid rich text, JavaScript calculations, hidden dependencies, tiny touch targets, overlap, hover-only interactions and fields near page edges.

When a dropdown is unreliable, use visible radio buttons, checkboxes or a short text field with printed options.

## Visual preservation

- Keep approved wording, branding, colors, hierarchy and page order.
- Do not cover labels.
- Keep blank field borders visible on paper.
- Keep filled values inside boxes.
- Preserve validated A4 margins.
- Render and inspect every page after changes.

## Default deliverables

1. original preserved;
2. interactive editable PDF;
3. static blank print PDF;
4. synthetic filled test PDF;
5. field manifest;
6. validation report;
7. SHA-256 list.

## Synthetic data

Use obviously fake values such as `Clínica Exemplo`, `Dra. Teste`, `CRO 00000`, `Pendente`, `Precisa discutir` and `observação de teste`. Never use real patient or client data.

## Signature boundary

A PDF signature field, typed name or drawn mark is not automatically an ICP-Brasil signature. State the exact mechanism and preserve a paper-signature option when requested.

## Blockers

Return `BLOCKED` when the baseline cannot be preserved, field mapping is ambiguous, encryption prevents authorized editing, required fonts/appearances cannot be made reliable, compatibility depends on an unavailable proprietary viewer or universal compatibility is demanded.

## Final report

Use `EXECUTAR AGORA / PLANEJAR / ARQUIVAR`. Include source/copy paths, authoring path, pages, fields, structure, appearances, Portuguese glyph test, visual comparison, outputs, literal validations, hashes, library versions, residual risks and rollback.
