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

## Noesantara inner-page consistency

- Match Minigames headers to Leaderboard/Gallery: `container max-w-6xl mx-auto px-4 pt-8`, heading `text-3xl md:text-5xl font-heading font-extrabold tracking-tight`, header gap `mb-6 md:mb-10`, subtitle `text-sm md:text-base` with 20px/24px line heights and 4px top margin. Do not add a network eyebrow or extra navbar-offset padding; App already lays out navigation.
- Compare computed title coordinates and typography at desktop/mobile; broad `.mg-page p` CSS can override subtitle line height even when utility classes match.

## Noesantara localization

- Use existing `useAppSettings` ID/EN language setting for minigames, including login/setup, wallet snapshots, transfer statuses, validation, accessibility labels, and game rules. Avoid em dashes in user-facing copy; use periods or colons. Keep command names, arguments, account identifiers, numeric mutation payloads, and security gates unchanged.
- Verify language changes preserve form inputs and pending transaction intent. Format display numbers/dates by locale, not command arguments. Unknown backend errors must remain visible rather than disappear behind generic translations.

## Transfer history viewport

- Show the newest two transfer records, retaining older fetched records inside a keyboard-focusable vertical scroll list. For variable status instructions and ID/EN wrapping, size viewport from the first two row heights with ResizeObserver instead of fixed pixels or truncating records. Observe only those rows and disconnect on cleanup; no polling required. Bring browser tab to front before resize assertions because background ResizeObserver delivery can pause.

## Minigames lobby balance

- Use equal-width, equal-height desktop overview columns; move long transfer form into a separate full-width section with equal internal columns instead of stretching one sidebar. Stack on mobile and verify no horizontal overflow.
- Put amount input and submit button in a shared CSS grid row; helper text belongs below controls. Independent column flex layouts with margin-top:auto misalign actions when copy wraps. Measure input/button top and bottom coordinates.
- Do not interpret pending session data as a disabled service. Show unavailability only after explicit successful status=false, keep mutation gates fail-closed, and avoid legacy hardcoded explanations that misstate the live service state.
- When removing verbose asset attribution, retain a concise discoverable credit/license link and complete attribution file; avoid silently dropping CC BY requirements.
- Run generated wallet and login browser suites on separate fresh documents; both override global fetch/timers and overlap causes false polling failures. Wait for CSS to load before recording layout geometry.

## Noe FisherMan arcade presentation

- Treat fishing as an animated tap arcade, not a static illustration beside questionnaire cards. Keep rod cast, bobber/bite, tap ripples, reel progress, catch lift, and escape feedback inside one visible water arena; preserve private server-authoritative money and challenge protocol.
- Keep challenge targets visible and interactive during casting/bite decoration; animation must not consume mandatory memory/timing windows or hide mobile controls below the scene. Verify actual moving transforms at multiple times and reduced-motion behavior, not keyframe declarations alone.
- Scroll the whole fishing arena below sticky navigation, not only its challenge subtree; measure rod top and last target bottom in the full production shell. Verify arena foreground/background after Vite build because standalone component harnesses can miss inherited white-on-white text and CSS cascade differences.
- Settle decorative cast/tug state with a cleaned-up timer fallback; reduced-motion disables animationend, so animation events alone can leave stale phases.

## Pre-flight

1. Inspect reference CSS/HTML or screenshot.
2. Verify exact font families and weights.
3. Confirm palette has no unrequested accent colors.
4. Check desktop and mobile structure.
5. Add loading, empty, error, and focus states where relevant.
6. Keep secrets outside Git.
7. Verify production response and primary interaction.
