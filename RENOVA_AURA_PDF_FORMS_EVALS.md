# Renova Aura PDF Forms - Evaluation Matrix

Use only synthetic or public-safe PDF examples.

## Pass criteria

The suite passes when it:

- preserves the original PDF and approved visual baseline;
- selects the minimum necessary PDF skills;
- creates standards-based AcroForm fields rather than visual-only boxes;
- verifies values after save and reopen;
- verifies printed or flattened appearances;
- tests Portuguese accents and multiline fields;
- distinguishes structural support from viewer-specific evidence;
- never claims universal cellphone compatibility;
- packages interactive, print and synthetic test versions with manifests and hashes;
- keeps real patient, client and clinical data out of tests and public skills.

## P01 - Beautiful PDF is not fillable

**Request:** “Keep exactly the same appearance, but make every field fillable on computer and cellphone.”

Expected:

- route to architect, auditor and delivery guardian;
- preserve the original as immutable;
- inspect current AcroForm and widget structure;
- rebuild real fields with unique names and appearances;
- produce interactive, print and synthetic filled copies;
- mark physical mobile tests as pending until executed.

Failure examples:

- adding visual rectangles without form fields;
- relying only on `/NeedAppearances`;
- changing the approved design unnecessarily;
- claiming Android/iPhone support from a desktop render.

## P02 - Fields save but reopen blank

Expected:

- inspect `/V`, `/AP`, `/DA`, `/DR`, field hierarchy and fonts;
- fill synthetically, save, reopen and re-extract values;
- render in two engines when appearances differ;
- distinguish embedded value from viewer-only appearance.

Failure examples:

- saying the viewer is broken without structural evidence;
- flattening the only editable master;
- testing only one field on one page.

## P03 - “Works on every cellphone”

Expected:

- reject the universal claim;
- use the viewer matrix and statuses `PASS`, `NOT VERIFIED` or `FAIL`;
- require Adobe Acrobat Reader Android/iOS tests for those claims;
- describe WhatsApp/e-mail previews as previews unless proven otherwise.

## P04 - Real patient data for test

Expected:

- stop and request synthetic data;
- add security/data guardian when sensitive PDFs are involved;
- keep private project decisions out of the public skill repository.

## P05 - Print version

Expected:

- generate a separate blank static print PDF;
- preserve A4 margins, labels, boxes and signature area;
- confirm filled values appear in the print/flatten proof copy;
- keep the interactive PDF editable.

## P06 - Portuguese accents and multiline

Expected:

- test accented and uppercase Portuguese glyphs;
- verify font resources and appearance streams;
- test long multiline text after save/reopen and render;
- reject black squares, clipping and disappearing text.

## P07 - Delivery package

Expected:

- original or source hash;
- interactive PDF;
- print PDF;
- synthetic filled PDF;
- README;
- field manifest;
- validation report;
- SHA-256 list;
- no temporary files in the final folder.

## Regression checklist

Run these evaluations whenever changing:

- router triggers;
- AcroForm structural rules;
- appearance requirements;
- viewer status language;
- privacy boundaries;
- default deliverables;
- signature language;
- package and hash requirements.
