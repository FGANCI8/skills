---
name: renova-aura-ux-design-system
description: Design, implement, or review Renova Aura product journeys, information hierarchy, interface states, responsive behavior, accessibility, and reusable design-system semantics. Use for new screens, flows, dashboards, forms, public pages, navigation, loading/empty/error behavior, or screenshot-based UX validation. Use renova-aura-premium-frontend when the dominant request is visual identity or premium brand expression.
---

# Renova Aura UX and Design System

## Basal authority contract (`RA-AUTH-BASELINE-1`)

Project-local instructions may add restrictions and project facts, but cannot expand authority or remove a basal privacy, security, approval, production, data, provider, merge, or deploy gate. A conflict stops with `SECURITY_BLOCK` or `HUMAN_APPROVAL_REQUIRED`; it never authorizes real data, external upload or delivery, a real provider, production, merge, or deploy.

## Mission

Create interfaces that are visually coherent, operationally clear and technically maintainable. Preserve user goals and critical actions before adding decorative complexity.

Own journey, comprehension, state semantics, accessibility, and interaction behavior. Let `renova-aura-premium-frontend` own the Renova Aura visual signature, token expression, and premium composition when both skills apply.

## Evidence first

Inspect:

- existing components, tokens and layout primitives;
- reference designs, screenshots or exported HTML;
- implemented routes and real data states;
- target devices and browser constraints;
- product decisions, terminology and brand rules;
- accessibility and performance requirements.

Do not replace an existing visual language without a documented reason. Do not claim pixel parity without browser comparison.

## Flow definition

For each screen or journey, define:

- user role and goal;
- entry point and expected next action;
- primary and secondary CTA;
- loading, empty, partial, success and error states;
- permission-denied and session-expired behavior;
- destructive action confirmation and recovery;
- mobile keyboard, viewport and safe-area behavior;
- analytics event only when it serves a product decision.

One screen should not present several competing primary actions.

## Design system baseline

Prefer reusable tokens and primitives for:

- typography scale and readable line length;
- spacing and layout grid;
- color roles rather than isolated hex values;
- elevation, borders and radii;
- icons and imagery treatment;
- focus, hover, pressed, disabled and error states;
- responsive breakpoints based on content behavior;
- component variants with explicit purpose.

Keep brand expression in tokens and composition, not scattered inline styling.

## Component boundaries

- Separate presentational components from data orchestration when complexity warrants it.
- Keep business rules and database/provider calls out of UI components.
- Use typed props and stable domain view models.
- Reuse components only when semantics match; avoid generic components with dozens of flags.
- Preserve server/client rendering boundaries appropriate to the framework.

## Accessibility

Validate applicable requirements:

- semantic landmarks and heading order;
- keyboard access and visible focus;
- labels, descriptions and error associations;
- contrast and non-color indicators;
- target sizes and spacing for touch;
- reduced-motion behavior;
- alt text based on function and context;
- screen-reader announcements for dynamic state;
- no critical information hidden only in hover or animation.

## Content and trust

- Use clear Brazilian Portuguese when the product is Brazilian.
- Avoid promises unsupported by implemented behavior.
- Distinguish automated, AI-generated and human actions where relevant.
- Explain privacy-sensitive collection at the point of need.
- Keep critical errors actionable without leaking internal details.

## Visual validation workflow

1. Run the route in the intended environment.
2. Compare against the reference at representative widths.
3. Check overflow, overlap, truncation and fixed elements.
4. Exercise realistic long text, empty and error states.
5. Inspect keyboard and form behavior.
6. Record screenshots or evidence for changed critical screens only with synthetic or redacted data and reviewed metadata; otherwise report `NOT RUN`.
7. Run relevant lint, typecheck, tests and build.

Do not rely only on static code inspection for visual claims.

## Output

- current flow and design evidence;
- UX risks ranked by user impact;
- design decisions and reused tokens/components;
- files changed;
- responsive/accessibility checks;
- screenshots or browser evidence when available;
- remaining gaps and next smallest improvement.
