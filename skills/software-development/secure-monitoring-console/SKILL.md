---
name: secure-monitoring-console
description: Use when building secure read-only monitoring consoles.
---

# Secure Monitoring Console

Use for authenticated, read-only monitoring consoles for bots and services.

## Always-on rules

- Treat supplied live URLs, repositories, screenshots, fonts, logos, and CSS as source of truth; inspect them before writing UI.
- Match reference composition before styling details: shell, panel split, card geometry, spacing, typography, and responsive behavior. For dedicated utility consoles (e.g. log monitoring), collapse the workspace into a single primary card rather than retaining irrelevant multi-step wizard sidebars.
- In light-mode themes, audit every text element and nested span (such as `h1 span`, kicker, badges, active tabs) against the light background. Never leave inherited `#fff` or faint grays un-overridden on white surfaces; enforce high-contrast dark values (`#09090b`, `#18181b`).
- Order static asset serving before SPA fallback: register `express.static()` ahead of dynamic routes and catch-alls (`app.get('*')`), and generate both binary `/favicon.ico` and high-res PNG with cache-busting queries so browsers do not receive HTML and drop the icon.
- Reuse exact brand assets. Never replace a real logo with placeholder letters or invent accent colors absent from the reference.
- Keep monitor consoles read-only by default; expose start/stop/restart only when explicitly requested, and never expose shell, RCON, or arbitrary command actions. When controls are added, rename stale read-only copy, protect each action with authenticated session + CSRF validation, and integrate actions cleanly into the card header rather than reviving wizard sidebars.
- Resolve CLI/daemon binaries dynamically or provide fallback paths (`which pm2` or `~/.npm-global/bin/pm2`); never assume system `/usr/bin/` paths for Node-installed tooling, and pass process manager environment variables (`PM2_HOME`).
- Never use browser-native dialogs (`alert`, `confirm`, `prompt`) for interaction feedback. Build custom styled toast notifications or inline banners matching the theme with loading, success, and error states.
- Put authentication, session secrets, API keys, and environment values outside Git. Use separate secrets for console login, service webhooks, and service-to-service bridges.
- Keep the console backend bound to localhost behind the reverse proxy; apply secure cookies, CSRF protection for state-changing routes, rate limits, CSP, frame denial, and explicit input validation.
- Make logs and status useful for scanning: current state, process identity, memory/CPU or equivalent telemetry, separate runtime/error streams, and a clear stale/offline state.
- Do not claim visual fidelity from compilation alone. Verify exact production HTML/assets, response status, asset status, process status, and target viewport rendering.

## Procedure

1. Read the reference implementation and live production CSS/HTML. Extract fonts, weights, palette, border/radius scale, shadows, logo assets, light/dark behavior, and desktop/mobile layout.
2. Inspect the existing console server, frontend, reverse-proxy configuration, process manager, environment files, and current production response before editing.
3. Define the monitor boundary. List allowed read endpoints and explicitly remove or reject operational controls not requested.
4. Build the shared shell and reference-matched layout first. Use CSS grid for desktop panel composition and a deliberate mobile collapse; keep labels visible above inputs. Map reference panels to product purpose: do not copy a converter's numbered workflow into a monitoring console when status, controls, and log streams are the real tasks.
5. Implement security at trust boundaries: authenticate before status/log reads, validate query parameters, redact secrets from logs, use constant-time secret comparison where applicable, and return generic auth errors.
6. Add a tight verification loop before deployment: `node --check` for Node files, project build/typecheck, `git diff --check`, authenticated status/log probe, unauthenticated rejection probe, and production HTTP/asset checks.
7. Deploy with the existing PM2/Nginx strategy, save process state, verify the exact public URL and each asset path with `curl -sSI`, then check process status and recent logs. Serve static assets before SPA/fallback routes; otherwise an image URL can return HTML with HTTP 200 and still show a broken-image icon.
8. Compare desktop and mobile renders against the reference. Correct structure, typography, color, card shape, and overflow; do not stop at a successful build.
9. Commit only intended source/assets. Exclude `.env`, temporary screenshots, prompts, logs, raw reference folders, and generated secrets.

## Pitfalls

- Inspect the actual reference repository and live CSS instead of trusting a previous description; visual tokens drift and stale assumptions create wrong fonts/colors.
- Do not add blue, lime, gradients, or decorative metrics because they look useful; a reference-driven UI must prove each accent from the source.
- Do not use a text letter as a logo when a supplied asset exists; brand recognition fails first on mobile where the mark is small.
- Do not expose a webhook or manual bridge without an independent secret and payload validation; a public transaction endpoint becomes a fake-donation vector.
- Do not deploy frontend changes without restarting the serving process when it serves static HTML from memory or a built artifact; production can otherwise keep old markup. Check image response `content-type: image/*`, not only page HTTP 200, because fallback HTML is a common branding failure.
- Verify a state-changing integration by reading its exact persisted result, not merely by accepting HTTP 200; successful transport does not prove storage or UI visibility.
- Do not hardcode `/usr/bin/pm2` when spawning process manager actions; Node/PM2 is frequently located in user-scoped npm prefixes (e.g. `~/.npm-global/bin/pm2`), throwing silent ENOENT errors without `PM2_HOME` in env.
- Never use default `alert()` popups for async action feedback; browsers show generic host headers and poor UX. Use structured in-page toast notifications with explicit loading and error states.
- Do not enforce excessive client-side input restrictions (such as HTML `minlength="20"`) or arbitrary length minimums in server authentication logic that exceed standard operator passwords; validate against the configured environment secret directly, otherwise users with valid 10–16 character passwords will be blocked by native browser validation.

## References

- `references/brand-reference-audit.md` — repeatable reference extraction and visual acceptance checklist.
- `references/secure-bridge.md` — authenticated service-to-service bridge pattern for manual events and webhooks.
