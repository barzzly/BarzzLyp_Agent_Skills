# Brand reference audit

## Extract

1. Fetch the live page HTML and every linked stylesheet/asset manifest.
2. Inspect the source repository for the actual component markup and theme branches.
3. Record exact font families/weights, body/background/surface/text tokens, border and radius values, shadow/blur, logo filenames, and responsive breakpoints.
4. Compare screenshot dimensions to target viewport; do not apply desktop geometry to mobile.

## Acceptance

- Header, logo, title, panel order, column ratio, card radius, borders, spacing, and button geometry match.
- Light and dark modes use reference tokens; no invented accent colors remain in active CSS.
- Font network requests or local `@font-face` assets resolve and computed typography uses the intended family.
- Favicon, logo, and other assets return 200 from the production URL.
- Login, empty, offline, runtime-log, and error-log states remain legible at mobile width.
- Run static checks, then render both target viewports. Compilation is not visual verification.
