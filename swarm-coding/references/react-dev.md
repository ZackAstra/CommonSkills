# React Implementation Reference

Use this reference for React, Vite, Tailwind, shadcn/ui, animation, canvas, and WebGL implementation workers.

## Setup Principles

- Use the existing project stack when editing an existing app.
- For greenfield apps, scaffold from the public registry at runtime. Do not copy baked `node_modules`.
- Commit the scaffold before page workers branch from it.
- Treat each git worktree as its own install target. `node_modules` is untracked and does not follow branches or merges.
- Keep package installs minimal and justified by the design.
- After installing dependencies, run the package manager's build/typecheck command before handing work back.
- If build/typecheck reports `Cannot find module '<pkg>'`, inspect the importing file and `package.json`, install the missing package with the active package manager, and commit both `package.json` and the lockfile.

## TypeScript

Use type-only imports for types when `verbatimModuleSyntax` is enabled:

```tsx
import type { ReactNode } from 'react';
import { useEffect, useMemo } from 'react';
```

For Framer Motion easing arrays, use tuple assertions:

```tsx
const ease = [0.16, 1, 0.3, 1] as [number, number, number, number];
```

Keep component props explicit, avoid `any`, and keep shared types in a location agreed by the scaffold contract.

## Routing And Assets

For static Vite builds, prefer `HashRouter` unless the deployment environment provides route fallback. Keep route definitions centralized unless a worker is explicitly assigned routing.

For assets in `public/`, reference with root paths:

```tsx
<img src="/hero-bg.png" alt="..." />
```

Keep `tsconfig` path aliases and Vite aliases in sync. If aliases are absent, use relative imports rather than inventing aliases.

## Tailwind And shadcn/ui

- Enumerate Tailwind classes explicitly; avoid dynamic string interpolation that Tailwind cannot scan.
- Put global styles in Tailwind layers, usually `@layer base`.
- Do not add broad global resets that duplicate Tailwind Preflight.
- Use shadcn/ui components for common UI density and accessibility when available.
- Keep design tokens in one place: Tailwind config, CSS variables, or the repo's existing token system.

## Layout Stability

- Prefer `min-h-[100dvh]` over `h-screen` for mobile viewport stability.
- Give animated reveal containers explicit dimensions or constraints.
- Ensure text fits inside buttons, cards, sidebars, and compact panels at mobile and desktop widths.
- Set fixed or responsive dimensions for boards, grids, toolbars, counters, and tiles so hover or loading states do not shift layout.

## Icons And Controls

Use the app's existing icon library, or `lucide-react` when available. Do not use emoji as icon replacements unless the product explicitly calls for them. Add accessible labels or tooltips for icon-only controls.

## Animation

Use Framer Motion for UI interactions and layout transitions. Use GSAP for scroll-driven storytelling or canvas-heavy sequences. Keep the two isolated in separate components when both are present.

Avoid `useState` for high-frequency animation values. Use refs, motion values, CSS transitions, GSAP timelines, or React Three Fiber frame loops.

Animate transform and opacity. Avoid animating layout properties unless there is a measured reason.

## Canvas And WebGL

For Three.js in React, prefer React Three Fiber with `@react-three/fiber`, `@react-three/drei`, and `@react-three/postprocessing` when those dependencies are already approved or needed by the design.

Rules:

- Lazy-load heavy WebGL sections with `React.lazy` and `Suspense`.
- Pause or reduce frame work when the section is outside the viewport.
- Precompute random particle positions with refs or memoized arrays.
- Keep original particle positions separate from interactive displacement.
- Set canvas sizing reliably at mount time, using inline style when needed.

## Worker Discipline

Read the scaffold before implementing pages:

```bash
sed -n '1,220p' src/App.tsx
sed -n '1,220p' src/index.css
find src/components -maxdepth 2 -type f | sort
```

Only edit assigned files. If the design requires changing shared components, stop and report the needed change instead of unilaterally editing shared code from a page branch.

Before finishing, run the narrowest useful validation command, then the broader build if feasible:

```bash
test -d node_modules || npm install --no-audit --no-fund
npm run build
```
