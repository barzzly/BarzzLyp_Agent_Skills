---
name: 9router-model-sync
description: Sync 9Router models into Claude Code settings.json.
---

# 9Router → Claude Code model sync

Use when syncing the 9Router/airouter model list into `~/.claude/settings.json`,
or auditing which router models actually answer.

9Router Proxy fronts several upstream providers and exposes an OpenAI-compatible
API. Set its private endpoint through `HERMES_CUSTOM_AIROUTER_BASE_URL`; do not
commit the endpoint or credentials. Claude Code consumes it via
`ANTHROPIC_BASE_URL` in `~/.claude/settings.json`.

## `/v1/models` is not the usable list

`GET /v1/models` returns ~500 IDs — the union of everything the upstreams
*advertise*, not what is registered locally. Calling an unregistered ID fails:

```
{"error":{"message":"[<provider-uuid>/<model>] [403]: No credit rate configured
 for <model>. Ask the operator to set its price first.","code":"credit_rate_missing"}}
```

The real list is the per-provider "Available Models" section at
`/dashboard/providers` → click a provider card. Use `/v1/models` only to spot
new candidates, never as the settings source.

## Reading the dashboard

Login wall: `/dashboard/` 308→`/dashboard`, which redirects to `/login` with a
single `input[type=password]` and one `button`. Ask the user for the password —
the page prints "Default password is 123456" as a hint; never try it unprompted.

Provider cards are `div` with class containing `bg-surface`, text starting with
the provider name. Click the LAST match — the outermost card is a grid wrapper
containing all provider names, and clicking it does nothing.

Registered IDs appear after the `Import from /models` marker (custom
OpenAI/Anthropic-compatible providers) or after `Disable All` (OAuth/free-tier
providers). Split `document.body.innerText` on those markers and regex the
provider prefix.

The browser session sometimes drops to `about:blank` between `browser_exec`
calls — re-check `location.href` and re-login rather than assuming state.

## Probing: two traps

1. **Small `max_tokens` fails reasoning models.** With `max_tokens: 32`,
   thinking models burn the whole budget on reasoning tokens and return
   `content: ""` with `finish_reason: "max_tokens"` — they look dead but work.
   Use `max_tokens: 4096`.
2. **HTTP 200 can carry an error sentence as content.** Retired upstream models
   answer `"Gemini 3.5 Flash is no longer available. Please switch to ..."` with
   `finish_reason: "stop"`. Match dead markers (`no longer available`,
   `not available`, `deprecated`) against the content and fail those.

Ask a question with a checkable answer ("What is 2+2? Answer with the number
only.") so an error sentence cannot pass as a valid reply.

Providers showing `0 connections` (e.g. OpenCode Free) return empty content on
every call — exclude them even though the dashboard lists models.

## Script

`scripts/build_claude_settings.py` holds the REGISTERED map + TIER map, probes in
parallel (6 workers), backs up to `~/.claude/backups/settings.json.<epoch>.bak`,
then rewrites only `availableModels`, `modelPicker`, and `model`. Everything else
in settings.json (env, plugins, permissions, theme) survives because the script
loads and re-dumps the existing dict.

`modelPicker.options[].behavesAs` must be a real Anthropic model name
(`claude-opus-5`, `claude-sonnet-5`, `claude-haiku-4-5-20251001`) — it sets the
capability profile Claude Code assumes. Set `replaceBuiltInOptions: true` so the
picker shows only router models.

Verify with the real CLI, not just HTTP:
`claude --print --model "<id>" "reply with one word: READY"`.

## Sharing settings.json

`env.ANTHROPIC_AUTH_TOKEN` is a live `sk-` key. Write a separate sanitized copy
with the token replaced before sending the file over chat; never send the real
one.
