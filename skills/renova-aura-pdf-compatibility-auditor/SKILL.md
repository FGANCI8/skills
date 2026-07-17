---
name: renova-aura-pdf-compatibility-auditor
description: Audit fillable PDF structure, saving, reopening, printing and viewer compatibility. Use when fields look blank, do not save, print empty, work only in one viewer, have duplicate names or orphan widgets, rely on NeedAppearances, mishandle Portuguese text, or require evidence for Adobe Acrobat, Edge, Android, iPhone/iPad or paper workflows.
---

# Renova Aura PDF Compatibility Auditor

## Mission

Prove what actually works, identify the structural or viewer failure and prevent unsupported compatibility claims.

## Evidence hierarchy

1. PDF object structure;
2. programmatic field extraction;
3. synthetic fill, save and reopen;
4. rendered appearance;
5. flattened or printed appearance;
6. desktop viewer test;
7. physical mobile viewer test.

A screenshot alone does not prove values are embedded or saved.

## Preflight inventory

Record:

- path, SHA-256, page count, dimensions, rotations and PDF version;
- encryption and permissions;
- catalog `/AcroForm` and XFA presence;
- `/NeedAppearances`;
- field count and types;
- duplicate names;
- widgets per page and rectangles;
- parent/kid hierarchy and page association;
- `/DA`, `/DR` and fonts;
- appearance streams;
- choice options and checkbox/radio states;
- read-only, hidden and no-export flags;
- non-form annotations.

## Golden validation loop

1. Render the untouched PDF.
2. Extract every field and widget.
3. Create synthetic values.
4. Fill programmatically.
5. Save to a new file.
6. Reopen it.
7. Extract values again.
8. Compare values.
9. Render the filled file.
10. Create and render a flattened or print copy.
11. Compare with the approved baseline.
12. Repeat with a second renderer when appearances differ.

## Required coverage

Test fields on the first page, an early page, a middle page, a late page and the closing/signature page.

Test short text, Portuguese accents, long text, multiline wrapping, checkbox, radio, choice field, default/blank state, save/reopen, print/flatten and tab order when a real viewer is available.

## Viewer matrix

| Viewer | Required evidence |
|---|---|
| Adobe Acrobat Reader desktop | manual open, fill, save, close, reopen and print |
| Microsoft Edge desktop | manual open, fill, save, close, reopen and print |
| Chrome desktop PDF viewer | manual test; do not assume parity with Edge |
| Adobe Acrobat Reader Android | physical device or emulator using the actual app |
| Adobe Acrobat Reader iPhone/iPad | physical device or simulator using the actual app |
| Android native viewer | test the named app; support varies |
| iOS Files/Quick Look | test the named viewer; support varies |
| WhatsApp/e-mail preview | preview only unless proven otherwise |

A library render cannot mark a named viewer as `PASS`.

## Status language

- `PASS`: tested and passed in the named environment;
- `FAIL`: tested and failed;
- `NOT RUN`: no test executed;
- `NOT VERIFIED`: evidence insufficient;
- `SUPPORTED BY STRUCTURE`: standard fields exist but viewer not tested;
- `BLOCKED`: file or environment prevents evaluation.

Never claim universal cellphone compatibility.

## Common diagnoses

### Value exists but is invisible

Inspect missing/stale appearances, invalid default appearance, missing font resource and viewer-dependent `/NeedAppearances`.

### Prints blank

Inspect printable appearance, annotation print flag, hidden/non-printing flags, viewer behavior and flattening path.

### Does not save on mobile

Inspect whether the user edited a preview instead of a PDF editor, unsupported controls, malformed hierarchy, permissions and the app's save-copy workflow.

### Checkbox/radio fails

Inspect valid appearance states, `/V`, `/AS`, widget states and duplicate names.

### Dropdown rejects a value

Inspect `/Opt` and use exact option values.

### Accents fail

Inspect form font, encoding, appearance generation, fallback font and renderer output.

## Visual regression

Render all pages before and after. Compare dimensions, count, clipping, overlap, black boxes, glyphs, field borders, page bounds, headers and footers. Pixel diff supports but does not replace structural validation.

## Privacy

Use synthetic data only. Do not upload sensitive forms to public validators. Do not expose patient, customer, legal or financial data in screenshots or logs. Add the security/data guardian for sensitive content.

## Required output

Produce structural inventory, field manifest, duplicate/orphan report, synthetic values, save/reopen results, render results, print/flatten results, viewer matrix, root causes, repair recommendation and final state: `VALIDATED`, `VALIDATED_WITH_LIMITATIONS`, `NOT VERIFIED` or `BLOCKED`.
