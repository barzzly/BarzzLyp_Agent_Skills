---
name: screenshot-driven-web-redesign
description: Use when rebuilding web UI from supplied screenshots.
---

# Screenshot-Driven Web Redesign

## Always-on rules

- Treat supplied screenshots, local fonts, logos, and palettes as source of truth. Do not substitute a generic interpretation.
- When a live reference URL is supplied, inspect its HTML and loaded CSS/assets directly with `web_extract` or `curl` before implementing; record exact font families, weights, color tokens, radii, borders, and shadows. Never infer a brand palette from a prior project or add accents absent from the reference.
- Match composition before decoration: page order, shell geometry, alignment, section proportions, card structure, spacing rhythm, and typography hierarchy come before polish.
- Inspect every supplied reference before editing. Distinguish mobile and desktop references by dimensions and map each to its target viewport.
- Preserve business logic, routes, API calls, auth, data states, and accessibility unless the brief explicitly changes them.
- Missing imagery gets a deliberate local placeholder that preserves exact geometry; never leave an image-dependent region collapsed.
- When replacing an old visual system, delete obsolete tokens, asset imports, theme branches, and dead CSS instead of layering overrides.
- One successful build is not visual verification. Render target viewports, compare against references, issue concrete corrections, and repeat until major composition differences are gone.

## Procedure

1. **Inventory references and implementation**
   - List every screenshot, logo, font, palette, and existing page/component involved.
   - Read image dimensions to classify mobile/desktop targets.
   - Inspect current route files, shared shell, global CSS/tokens, and asset imports.

2. **Extract a reference specification**
   - Extract exact page order, header/footer geometry, column/grid counts, alignment, card shapes, typography roles, palette values, imagery aspect ratios, and responsive transitions.
   - For live references, preserve the distinction between dark-mode base colors (`#000`, `#09090b`, `#18181b`, `#27272a`, `#3f3f46`, `#52525b`), neutral text (`#fafafa`, `#f4f4f5`, `#a1a1aa`, `#71717a`), and semantic success colors; do not invent blue/lime accents unless reference CSS proves they exist.
   - Use exact supplied values where visible. Mark unavailable imagery as placeholder, not invented content.

3. **Delegate as one bounded implementation task when Claude Code is requested**
   - Give one self-contained task with reference paths, exact asset constraints, preservation rules, forbidden files, and acceptance commands.
   - For custom-routed models, override both CLI model and invocation settings, then verify actual routing when structured output exposes it.
   - Keep image-heavy context local. Ask Claude Code to inspect files from disk; do not pipe binary screenshots or a giant accumulated conversation into stdin because request payloads can exceed gateway limits.
   - Prefer a fresh print-mode session for one-shot implementation. Use interactive tmux only when iterative steering is required.

4. **Implement shared visual language first**
   - Install supplied fonts with `@font-face`, centralize exact palette/tokens, then rebuild shared header/footer/background.
   - Rebuild page markup to match screenshot composition. Avoid cosmetic-only recoloring of an incorrect structure.
   - Use local fallbacks for remote player/media assets and keep required URL templates literal.

5. **Run static verification**
   - Run project typecheck/lint and production build.
   - Run `git diff --check`.
   - Search active source for forbidden old asset names, obsolete palette/theme terms, stale remote image endpoints, and removed theme branches.
   - Inspect diff scope to ensure secrets, environment files, migrations, and deployment configuration were not touched unless requested.

6. **Render and compare**
   - Start preview on a free port after checking listeners.
   - Capture each referenced route at its matching viewport dimensions.
   - Compare screenshot-to-render for composition, spacing, type scale, palette, imagery bounds, responsive behavior, overflow, and interaction states.
   - Convert differences into specific correction instructions such as “hero image begins too low by about one nav height” rather than “make it more similar.”
   - Repeat implementation and comparison until no major structural mismatch remains.

7. **Deploy only after acceptance gates**
   - Re-run check/build after final corrections.
   - Commit only intended source/assets; never include raw reference folders, temporary prompts, logs, or `.env`.
   - Push, watch CI/deploy to completion, then verify production HTTP response and exact target page.
   - Stop temporary preview servers and tunnels after production verification.

## Pitfalls

- Never report percentage progress from elapsed time alone; derive it from completed artifacts, changed files, and remaining gates because long agent runs may spend most time inspecting or retrying.
- Never call a redesign “matched” based only on agent self-report and successful compilation; compilation proves syntax, not visual fidelity.
- Keep temporary delegation prompts outside the repository or explicitly exclude them from commits, because untracked orchestration files pollute project status.
- If a model provider is unavailable, use only a user-approved fallback model and preserve the same acceptance criteria; do not lower fidelity to finish faster.
