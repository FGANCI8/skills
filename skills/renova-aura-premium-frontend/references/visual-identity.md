# Renova Aura visual identity fallback

Use this reference only when a project has no approved visual identity. Project-local tokens and brand decisions take precedence.

## Character

`quiet precision + warm intelligence + luminous depth`

The interface should feel calm, technically credible, human, and deliberately composed. Premium means fewer, better decisions.

## Semantic color starting point

These values are a portable starting point, not a mandate:

| Role | Dark surface | Light surface | Purpose |
|---|---|---|---|
| canvas | `#07111F` | `#F6F8FB` | page background |
| surface | `#0D1B2A` | `#FFFFFF` | primary container |
| surface-raised | `#13243A` | `#EEF3F8` | raised or selected region |
| text | `#F8FAFC` | `#0F172A` | primary content |
| text-muted | `#9FB0C3` | `#526277` | secondary content |
| border | `#26384D` | `#D9E2EC` | structure |
| aura | `#2DD4BF` | `#0F8F83` | primary action and focus |
| signal | `#60A5FA` | `#2563EB` | information and links |
| warmth | `#F6C76E` | `#9A6508` | limited highlight |
| danger | `#FB7185` | `#C81E3A` | destructive/error state |

Verify contrast in the actual composition. Never use raw palette values as a substitute for semantic roles.

## Typography

- Preserve the project font if it is licensed, loaded, and coherent.
- If no type system exists, prefer a restrained sans-serif with strong Brazilian Portuguese coverage and a system fallback.
- Use weight, size, line height, and spacing before adding color.
- Keep body copy comfortable and data labels compact without becoming faint.
- Reserve display treatment for one focal level per screen.

## Shape and depth

- Use a small radius scale such as `8 / 12 / 16 / 24` and assign each value a role.
- Prefer 1 px borders and soft directional shadow to opaque floating slabs.
- Use translucency only when background context remains legible.
- Keep accent glow local to one focal element; never surround every card.

## Motion

- Use motion to show entry, continuity, hierarchy, or completion.
- Keep routine transitions approximately 140-220 ms unless the existing system differs.
- Prefer opacity and transform over layout-thrashing properties.
- Respect reduced-motion preferences and preserve meaning without animation.

## Composition

- Give the primary action the strongest local contrast.
- Use asymmetry only when it strengthens focus.
- Let sections breathe; do not fill empty space with decorative modules.
- Keep marketing and authenticated surfaces recognizably related without forcing identical density.
- Separate founder/admin, operator, and customer contexts through information architecture as well as styling.

## Anti-patterns

- purple-blue gradient as the only brand signal;
- glassmorphism on every surface;
- excessive pills and rounded rectangles;
- decorative charts without decisions attached;
- tiny muted labels that fail contrast;
- icon-only critical actions;
- motion that delays work;
- a polished shell concealing mock, incomplete, or read-only behavior.
