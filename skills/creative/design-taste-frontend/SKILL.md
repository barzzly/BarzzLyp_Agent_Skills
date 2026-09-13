---
name: design-taste-frontend
description: Use when designing frontend UI. Apply anti-slop checks.
---

# Design Taste Frontend

Apply this skill for frontend UI work. Read brief and references first. State one-line design read before coding when implementation follows.

## Core rules

- Infer page kind, audience, vibe, references, existing assets, and constraints before choosing style.
- Use one coherent visual system. Lock palette, type, radius scale, spacing rhythm, and interaction posture.
- Do not default to AI-purple gradients, centered hero layouts, generic glass cards, arbitrary metrics, or decorative icon grids.
- Commit to correct surface: Monitor, Operate, Compare, Configure, Decide/Learn, Explore, or Command/Inspect.
- Dashboards and consoles prioritize scanning, state clarity, density, and action hierarchy over marketing composition.
- Use CSS grid over flex percentage math. Use `min-height: 100dvh`, responsive breakpoints, focus states, reduced-motion handling, and 44px mobile hit targets.
- Label inputs above fields. Keep helper and error text explicit. Never use placeholder text as only label.
- Audit button and form contrast at WCAG AA. Keep desktop CTA labels on one line. Avoid duplicate CTA intent.
- Use cards only where elevation communicates hierarchy. Keep one corner-radius rule unless documented component rules require exceptions.
- Use existing type and brand assets before inventing replacements. Self-host production fonts where practical.
- Verify build/static checks and render target viewports when visual fidelity matters. Do not call visual work matched from compilation alone.

## Verified MEG Converter-style reference tokens

For a dark monitor console matching `https://megconverter.barzzly.com/`:

- Body: `Inter`, weights 400/500/600/700.
- Labels, metadata, logs: `JetBrains Mono`, weights 400/500.
- Background `#000`; topbar `#09090b`; surface `#18181b`; active surface `#27272a`.
- Borders `#3f3f46`, `#52525b`, `#71717a`; primary text `#fafafa` / `#f4f4f5`.
- Muted text `#a1a1aa` / `#71717a`; success `#34d399`.
- Primary buttons white `#fff` with black text. Secondary controls `#18181b` with `#3f3f46` border. No blue or lime unless reference explicitly contains them.
- Use 7px–12px radii, subtle borders, restrained blur, dashed work areas, and no neon glow.

## Pre-flight

1. Inspect reference CSS/HTML or screenshot.
2. Verify exact font families and weights.
3. Confirm palette has no unrequested accent colors.
4. Check desktop and mobile structure.
5. Add loading, empty, error, and focus states where relevant.
6. Keep secrets outside Git.
7. Verify production response and primary interaction.
