---
name: discord-bot-operations
description: "Use when changing Discord bot embeds or PM2 deployment."
version: 1.0.0
license: Apache-2.0
platforms: [linux]
metadata:
  hermes:
    tags: [discord, bot, embeds, webhooks, pm2, nodejs]
    category: social-media
---

# Discord Bot Operations

## Standing rules

- Keep embed branding consistent across commands, panels, webhooks, and logger-generated messages; do not patch only the command named by the user when the requirement is global.
- For Noesantara embeds, use footer format `Noesantara Network • MM/DD/YYYY, hh:mm AM/PM` with `Asia/Jakarta` time, matching Discord's displayed `en-US` format. Do not use `Official Store` in embed footers.
- When users ask to restore or match an existing panel, treat the current Discord message as the source of truth: inspect its description, emoji IDs, button labels/URLs, mention content, footer, and image fields before rebuilding; product catalog data alone is not enough.
- Use the fixed blue Noesantara logo URL `https://store.noesantara.id/logo-no-backround.png` as footer `icon_url`; never fall back to bot avatar when branding requires the Noesantara logo.
- When refreshing an existing panel, preserve its established visual language: exact emoji, list layout, wording, buttons, `@everyone`, and footer branding. Do not invent a plain replacement from product data; inspect the previous builder/source first. If prior source is unavailable, inspect recent Discord messages before rebuilding and copy their structure.
- Existing Discord messages do not change retroactively; when asked to resend panels, fetch each target channel, delete only bot-authored panel messages, send rebuilt payloads, then read messages back through Discord API and verify footer text, footer icon, and image presence.
- Keep secrets in `.env`; never print tokens, API keys, or webhook keys in logs or reports.
- Prefer the smallest centralized change over repeating footer/timestamp code in every command.

## Procedure

1. Locate every embed producer before editing. Include command files, interaction handlers, webhook servers, donation loggers, and panel builders.
2. Add one centralized embed metadata helper or a single serialization boundary. Apply organization footer and send time at final serialization so future commands and webhook paths cannot bypass branding. Build the displayed date manually or with `formatToParts` when punctuation must be exact; `Intl.DateTimeFormat('en-US').format()` commonly inserts a comma.
3. Preserve the fixed Noesantara logo in the final footer object; replace stale organization text rather than appending a second footer. Use `Asia/Jakarta` time and an ISO timestamp for Discord's native timestamp. Remove panel-specific decorative images when requested, but keep footer logo independent from embed body images. For raw payload embeds, explicitly include footer, icon, timestamp, components, and allowed mention fields because they bypass `EmbedBuilder` serialization hooks.
4. Run syntax checks across all changed JavaScript:
   ```bash
   node --check index.js
   for f in commands/*.js donation-logger.js webhook-server.js items-handler.js rank-handler.js; do node --check "$f" || exit 1; done
   ```
5. Run one serialization self-check that constructs an `EmbedBuilder` and asserts footer starts with `Noesantara Network • ` and timestamp exists. Avoid starting a second bot instance because its webhook port can collide with PM2.
6. Restart only intended PM2 process and verify liveness:
   ```bash
   pm2 restart <bot-name> --update-env
   sleep 3
   pm2 describe <bot-name>
   pm2 logs <bot-name> --lines 30 --nostream
   ```
   Require `status: online`, `unstable restarts: 0`, and a ready log before reporting success.
7. For panel refreshes, keep channel IDs in one small sender script, target only requested channels, delete only bot-authored messages, send item/rank/coin payloads, and avoid starting a second long-lived bot process. Build Coins from the existing panel convention or source-of-truth product builder, including its coin emoji/list/description and `Webstore Noesantara` link; omit only the body image when requested while retaining footer logo. Add `content: '|| @everyone ||'` when the panel convention requires a visible everyone mention, then verify it through the API. Never replace a rich existing panel with a minimal placeholder just because the catalog is available.
8. Check source for stale branding and inspect `git diff --check`. Report changed scope, runtime status, message IDs verified, and that unrelated human messages were preserved.

## Pitfalls

- Do not add footer logic only to a shop panel when the requirement covers every embed; donation, announcement, moderation, utility, webhook, and future embeds use separate construction paths.
- Do not run `node index.js` as a verification probe while PM2 bot is online; the real webhook listener already owns its port and the probe exits with `EADDRINUSE`.
- Do not claim a PM2 restart succeeded from exit code alone; read process status and recent logs because a crash-loop can briefly report a successful restart.
- Do not use a second `setFooter()` after a centralized serialization hook unless intentionally preserving only the icon; Discord allows one footer object, so later calls replace earlier text.
- Do not promise old Discord embeds will update; editing history requires a separate migration and message-fetch policy.
