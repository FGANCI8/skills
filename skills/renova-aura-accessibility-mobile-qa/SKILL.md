---
name: renova-aura-accessibility-mobile-qa
description: Audit and verify accessibility, responsive behavior, keyboard and screen-reader operation, touch targets, text scaling, forms and real mobile states. Use when interfaces must work beyond static screenshots.
---

# Renova Aura Accessibility and Mobile QA

## Mission

Prove that critical journeys are understandable and operable across users, devices and states.

## Activate when

- mobile-first, responsive, PWA, web or Android UI is involved;
- the user asks for polish, usability or missing states;
- release requires accessibility evidence.

## Procedure

1. Identify critical routes and supported viewports/devices.
2. Inspect semantic structure, labels, focus order, keyboard, screen reader and contrast.
3. Test zoom/font scaling, orientation, touch targets, reduced motion and error announcements.
4. Verify empty, loading, error, offline, permission denied, expired and partial states.
5. Test forms, masks, validation, data preservation and recovery.
6. Check tables, filters, dialogs, menus and bottom navigation on narrow screens.
7. Record evidence with route, viewport, element and reproduction steps.

## Gates

Do not claim compliance from automated tools alone. Do not change brand or design system outside approved scope.

## Output

Journey matrix, findings by severity, WCAG/platform relevance, exact locations, acceptance criteria, manual/automated tests and correction order.

## Validation

Every critical flow must be tested with keyboard or platform accessibility path, text scaling and at least one failure state.

## Rollback

UI fixes must preserve functionality and have visual/interaction regression checks.