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
- For light-theme UI redesigns, enforce strict dark typography (`#1A1A1A` / `text-foreground`); never render light or white text directly over light cards or subtle background panels.
- When referencing dashboard or transaction screenshots, map summary counters to a dedicated horizontal metric strip, and pair desktop tabular records with an equivalent stacked-card layout for mobile viewports so horizontal scrolling is not forced.
- When displaying player or game statistics seen in reference UI, wire them directly to live database tables (e.g. LuckPerms, economy balance, point cache) instead of hardcoding static zero-values.
- When the user directs "tanpa emoji" (no emojis), strip both unicode emojis and decorative SVG pictograms (such as tickets, trophies, or exit glyphs) from buttons, badges, and stat headers; non-technical users read icons as emojis. Enforce pure typography with clean text labels.
- Never let bottom dashboard cards butt tightly against the site footer; maintain generous container bottom padding (`pb-28 md:pb-36`) for visual breathing room.
- Avoid two-tone split-colored header banners behind player avatars that cut across the image with negative margins; use cohesive single-card containers with uniform backgrounds and padding.
- When organizing multi-mode gaming networks, provide top-level server gamemode selector tabs (`ECO RPG`, `PVP SL`, `RP REBEL`) above stats and leaderboards for consistent navigation and segregated live data.
- When displaying rank badges in gaming profiles or dashboards, use the official pixelated in-game prefix badge texture (e.g. from Nexo `iconrank` assets) rendered with `imageRendering: 'pixelated'` directly inside the dedicated Rank metric container; keep the player nickname line clean without duplicate badges or text labels crowding it.
- Action buttons or portfolio links on character cards belong in the content column directly below description copy; never position them overlapping character feet or illustration artwork.
- Interactive elements inside draggable tracks: When buttons or links sit inside swipeable/draggable carousel tracks, parent `onMouseDown` and `onTouchStart` drag listeners will intercept clicks and activate `pointer-events-none` before child click events fire. Always guard drag container handlers with `if ((e.target as HTMLElement).closest("a, button")) return;`, add `onMouseDown` and `onTouchStart` `stopPropagation` on child elements, and provide an explicit fallback click handler (`window.open(..., '_blank')`).
- Maintenance & warning banners: Use clean dark/neutral borders (`border-2 border-[#1A1A1A]`) instead of dated or loud yellow/gold borders. Vertically center warning/alert icons (`items-center`) with the accompanying copy rather than forcing top alignment with `items-start mt-1`.
- Social media share banners (OpenGraph / WhatsApp / Discord): Messaging platforms like WhatsApp favor square (1:1) previews. Always replace legacy branding in root public assets, provide both square (`og-image.png`) and landscape (`og-banner.png` 1200x630) variants, and append cache-busting version params (`?v=...`) to `og:image`, `og:image:secure_url`, and `twitter:image` across static HTML and dynamic SEO components to bust crawler caches immediately.
- Static asset replacement and browser cache busting: When overwriting existing image or media files with the same filename (e.g., `ecorpg.webp`), client browsers will aggressively serve stale cached assets from disk cache. Append a cache-buster query parameter (e.g. `image: '/gamemodes/ecorpg.webp?v=3'`) or change the subfolder path in code so returning users immediately receive the updated graphic without requiring a manual hard reload.
- Preserve asset semantics: map supplied background art only to the background slot and supplied logo/title art only to the logo slot; inspect the component's separate image constants before editing because swapping the whole hero asset can make a logo fill the page background. When the request says “replace the logo,” change only the logo constant and leave background constant untouched; when it says “replace hero/background,” change only the background constant.
- Treat an explicitly named local asset path as authoritative. Compare source and deployed files by SHA-256, inspect the rendered element's `currentSrc` and bounding box in a live browser, and verify the visible slot—not only the URL or HTTP 200—before claiming the replacement is active. Keep favicon, app/logo, hero-logo, background, and OG assets separate; changing one must not silently overwrite another.
- When a user specifies a visual correction such as “blue glow,” search the owning component for the exact effect token and remove the old color before adding the new one; verify the built CSS or rendered computed style so stale utility classes do not survive.
- Fit supplied logo art without distortion: read dimensions, keep `object-contain` for transparent/title images, and verify the live hero at desktop and mobile widths; use `object-cover` only for true background artwork. Do not compensate for a mis-sized logo by moving the whole hero content; resize the image slot first, then verify composition.
- Floating Liquid Glass Navbar vs. Scroll Morphing: Avoid morphing scroll transitions that resize full-width navbars into floating capsules on scroll. Width jumping, height shifts, and text color flipping feel jerky and unappealing. Implement the navbar directly as a permanent floating liquid glass capsule (`rounded-full`, fixed height `h-14 md:h-16`, translucent frosted surface `bg-[#FEFEFE]/85 backdrop-blur-2xl`, subtle specular border `border-white/60 ring-1 ring-black/5`) with crisp dark typography (`#1A1A1A`) and zero scroll transition.
- Trust Device & Client Session Expiry: When implementing client-side trusted device sessions (e.g. 1-hour window), persist `loginAt: Date.now()` in storage alongside user identity. Combine an `onRehydrateStorage` check with a periodic interval watchdog (30s) and window `focus` listener to automatically invalidate expired sessions and clear carts without requiring user-initiated action.
- Donator Leaderboard & Transaction Ingestion: When ingesting transaction logs from channels, parse both bot embeds and plain-text codeblocks from human admins; never assume logs only come as rich embeds. For couple purchases, split totals equally (50/50) while preserving leading dots on Bedrock usernames. Once transactions are fully stored in the database, use the database as the sole authoritative source of truth — never additively sum database records on top of static historical arrays, which results in double-counting total revenue and donor ranks.
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
