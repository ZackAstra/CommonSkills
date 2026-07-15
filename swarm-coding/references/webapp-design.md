# Webapp Design Reference

Use this reference when a webapp, website, landing page, portfolio, dashboard, browser game, or interactive page is being built. The designer's job is to decide structure, visual direction, content hierarchy, interactions, responsive behavior, template fit, and asset needs before implementation starts.

## Design Output

For any user-facing web deliverable, create at least:

- `design/design.md`: global design system or compact design brief, typography, color, spacing, animation language, dependencies, shared components, page/section list, template mapping when relevant, and asset manifest.

For non-trivial or multi-page sites, also create:

- `design/home.md`: home or landing page details.
- `design/<page>.md`: one file per additional page or major route.

For small one-page or template-driven apps, one `design/design.md` is enough, but it must still be explicit enough for implementation workers to avoid inventing structure.

## Global Design Contents

Include:

- Product/site concept and target user.
- Template choice and rationale when using a bundled template.
- Mapping from requested content to template sections/config fields when using a configurable template.
- Page list with route, purpose, and ownership suggestion.
- Color palette with exact values and usage roles.
- Typography with font names, weights, sizes, and hierarchy.
- Layout rules: max widths, grid behavior, section rhythm, breakpoints, and mobile behavior.
- Shared components: header/nav, footer, cards, buttons, forms, modals, empty/loading/error states.
- Interaction language: hover, active, focus, transitions, scroll behavior, keyboard affordances.
- Dependencies that implementation likely needs.
- Asset manifest when custom images, videos, SVGs, icons, 3D models, or textures are needed.

For template-driven sites, also include:

- Exact config objects or source files that content workers should edit.
- Section order and which template sections should be hidden, reused, or renamed.
- Stable asset filenames and dimensions before asset workers start.
- A short note on what the scaffold step should preserve from the template.

## Per-Page Design Contents

For every page, specify:

- Route and page purpose.
- Section-by-section layout.
- Realistic copy and data, not placeholders unless the user asks for placeholders.
- Component names or responsibilities when other workers depend on them.
- Responsive behavior for mobile/tablet/desktop.
- Interactions and state changes.
- Animation details with concrete triggers and parameters.
- Assets used by filename.

## Asset Manifest

List every generated or sourced asset with:

- Filename, e.g. `hero-bg.png`.
- Type: image, SVG, video, model, texture, audio, or data.
- Intended page/section.
- Dimensions or aspect ratio.
- Prompt or sourcing instructions.
- Fallback behavior if the asset cannot be generated or fetched.

Implementation should reference public assets as `/filename.ext` when they live under `public/` in a Vite-style app.

## Visual Standards

Design for the application's domain. Operational SaaS tools should be dense, clear, and repeatable. Games and immersive experiences can be more expressive. Landing pages should make the brand, product, venue, person, or object obvious in the first viewport.

Prefer real visual assets or generated bitmap images when the site depends on a product, place, person, game state, or inspectable object. Do not rely on decorative gradient blobs or abstract SVG hero art when an actual image would carry the subject better.

Use familiar controls:

- Icons for toolbar actions.
- Swatches for color.
- Segmented controls for modes.
- Toggles/checkboxes for binary settings.
- Sliders/steppers/inputs for numeric values.
- Tabs for views.
- Menus for option sets.

Keep cards for repeated items, framed tools, and modals. Avoid nested cards and page sections styled as floating cards.

## Animation Guidance

Use motion to clarify hierarchy and state changes. Specify exact values:

- Entrance: opacity, transform distance, duration, easing, stagger.
- Scroll: trigger point, pinned distance, progress mapping, cleanup/fallback.
- Hover/tap: transform, color, elevation, cursor, focus state.
- Loading: skeleton, progress, retry, empty state.

Performance guardrails:

- Avoid animating layout properties like `top`, `left`, `width`, or `height`.
- Prefer transform and opacity.
- Limit simultaneous heavy effects in one viewport.
- Use one major WebGL/shader/canvas effect per section at most.
- Provide reduced-motion behavior for essential experiences.
