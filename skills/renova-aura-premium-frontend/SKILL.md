---
name: renova-aura-premium-frontend
description: Define, implement, or review the premium Renova Aura visual identity for web application interfaces. Use when a user asks for a premium, elegant, modern, trustworthy, distinctive, polished, responsive, or brand-consistent front end; when creating landing pages, dashboards, forms, onboarding, or authenticated product surfaces; or when converting visual references into reusable tokens and components. Preserve project-local brand rules and use renova-aura-ux-design-system for flow ownership.
---

# Renova Aura Premium Frontend

## Mission

Create calm, distinctive, high-trust interfaces whose polish comes from hierarchy, proportion, typography, material restraint, and complete states rather than decorative excess.

## Responsibility boundary

Own visual identity, composition, tokens, component expression, and visual verification.

- Route journey, information architecture, copy clarity, and state semantics to `renova-aura-ux-design-system`.
- Route code architecture and server/client boundaries to `renova-aura-engineering-guardian`.
- Add `renova-aura-quality-release` when code changes.
- Preserve an established project design system unless a redesign is explicitly authorized.

## Evidence first

Inspect project-local instructions, existing tokens, typography, components, screenshots, target routes, real data states, device constraints, and reference provenance. Classify references as approved brand, inspiration, legacy, demo, or unknown.

Do not copy a third-party product identity. Extract reusable visual principles and adapt them to the product.

## Identity direction

Use the detailed fallback system in [references/visual-identity.md](references/visual-identity.md) only when the project has no approved identity. The Renova Aura signature is:

- deep neutral foundations with luminous but restrained accents;
- generous negative space and decisive hierarchy;
- crisp typography with warm, human microcopy;
- layered surfaces with borders and light, not heavy glass effects;
- one dominant action per region;
- subtle motion that explains state;
- honest labels for demo, preview, read-only, automated, or legacy behavior.

Avoid generic purple SaaS gradients, excessive glow, interchangeable card grids, random radii, decorative charts, stock-dashboard density, and animation without informational value.

## Workflow

1. Identify the user, task, surface, product truth, and approved references.
2. Inventory current tokens and reusable primitives.
3. Establish a visual thesis in one sentence.
4. Define or map semantic tokens before styling screens.
5. Compose the critical path at mobile and desktop widths.
6. Implement complete loading, empty, partial, error, denied, success, and destructive states.
7. Validate accessibility, content stress, motion preferences, and interaction feedback.
8. Compare rendered screenshots against the approved reference and product truth.
9. Send desktop and mobile evidence to an independent visual evaluator with an objective rubric.
10. Correct concrete findings in a bounded loop of at most three rounds.
11. Report literal checks and remaining visual debt.

## Premium quality bar

- Typography has a clear display, section, body, label, and data hierarchy.
- Spacing follows a small deliberate scale.
- Color communicates role and status; it does not compensate for weak hierarchy.
- Cards group meaningful units and do not become the default wrapper for everything.
- Tables, charts, and metrics expose context, units, freshness, and empty states.
- Forms keep labels visible, errors actionable, and touch targets usable.
- Focus, hover, active, disabled, loading, and success states belong to the same visual language.
- Mobile is recomposed, not merely compressed.
- Contrast and interaction targets are evaluated against WCAG 2.2 AA where applicable.

## Visual verification

Validate representative small, medium, and large viewports. Use realistic long Brazilian Portuguese, reduced motion, keyboard navigation, zoom, loading, empty, error, and permission-denied cases. Record screenshots only when they contain no secrets or personal data.

Do not claim pixel parity, accessibility, performance, or responsiveness without the corresponding evidence.

The visual author cannot be the sole evaluator. The evaluator must report viewport, criterion, observed divergence, priority, and concrete correction rather than generic praise.

## Required output

Return:

- visual thesis and reference status;
- existing tokens/components preserved;
- semantic token or component decisions;
- changed files, when authorized;
- mobile, desktop, accessibility, content-stress, and screenshot evidence;
- honest product-state labels;
- residual gaps and rollback;
- final status: `VISUAL_DIRECTION`, `READY_TO_IMPLEMENT`, `VALIDATED_WITH_LIMITATIONS`, `NEEDS_HUMAN_APPROVAL`, or `BLOCKED`.
