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
- For Noesantara embeds, keep footer branding to `Noesantara Network` and use Discord's native timestamp (`setTimestamp()` / ISO `timestamp`) as the only date display; Discord renders it as “Today” and automatically changes to the date on later days. Do not duplicate a formatted date inside the footer. Do not use `Official Store` in embed footers.
- When users ask to restore or match an existing panel, treat the current Discord message as the source of truth: inspect its description, emoji IDs, button labels/URLs, mention content, footer, and image fields before rebuilding; product catalog data alone is not enough.
- Use the fixed blue Noesantara logo URL `https://store.noesantara.id/logo-no-backround.png` as footer `icon_url`; never fall back to bot avatar when branding requires the Noesantara logo.
- When refreshing an existing panel, preserve its established visual language: exact emoji, list layout, buttons, `@everyone`, and footer branding. Apply the requested casing consistently to product labels in overview, select options, and detail embeds (not just one visible row); preserve product IDs, option values, prices and copy unrelated to the request. Inspect the previous builder/source and live message before rebuilding; never invent a plain replacement from product data.
- For user-facing reward/pass embeds, omit internal mechanics (permission nodes like `lp user ...`, internal activation commands, and database flags) unless requested; present player-facing guidance instead (e.g. `• **Cara Pakai:** Ketik \`/command\` di ingame`).
- In Indonesian copy for Noesantara bot, write `ingame` without hyphen (never `in-game`). Use dedicated animated guild emojis (such as `<a:goldencoinspin:1258157813746897000>` for Coin Pass) in titles.
- Existing Discord messages do not change retroactively. For text/option changes or retroactively fixing already-sent log/panel embeds across guild channels, query candidate channels via Discord REST (`GET /channels/{id}/messages`), identify the exact bot-authored embeds, and PATCH them in place (`PATCH /channels/{id}/messages/{id}`) without deleting messages or sending duplicate notifications. When asked to delete an old panel and send a new message, delete only that specific panel. Never delete every recent bot message: other panels may share the channel.
- Keep secrets in `.env`; never print tokens, API keys, or webhook keys in logs or reports.
- Prefer the smallest centralized change over repeating footer/timestamp code in every command.

## Procedure

1. Locate every embed producer before editing. Include command files, interaction handlers, webhook servers, donation loggers, and panel builders.
2. Add one centralized embed metadata helper or a single serialization boundary. Apply organization footer and native send timestamp at final serialization so future commands and webhook paths cannot bypass branding. Do not add a second human-readable date to footer: Discord's native timestamp already renders relative day label and rolls over to calendar date automatically.
3. Preserve the fixed Noesantara logo in the final footer object; replace stale organization text rather than appending a second footer. Use `Asia/Jakarta` time and an ISO timestamp for Discord's native timestamp. Remove panel-specific decorative images when requested, but keep footer logo independent from embed body images. For raw payload embeds, explicitly include footer, icon, timestamp, components, and allowed mention fields because they bypass `EmbedBuilder` serialization hooks.
4. Run syntax checks across all changed JavaScript:
   ```bash
   node --check index.js
   for f in commands/*.js donation-logger.js webhook-server.js items-handler.js rank-handler.js; do node --check "$f" || exit 1; done
   ```
5. When adding or modifying slash commands, register guild commands with `node deploy.js` so Discord updates the command definitions immediately without waiting for global cache propagation.
6. For temporary Discord role assignments (e.g. 7-day passes), track grant and expiration timestamps in a persistent JSON store; check and remove expired roles on bot startup and via a periodic `setInterval` (e.g. 60s). Never use in-memory `setTimeout` alone. For stackable/queued passes, store an array of discrete pass records (`status: 'active' | 'remaining' | 'expired'`, `channelId`, `messageId`); never key the store by `userId` alone, because repeat purchases overwrite active passes and drop message tracking. When an active pass exists for the same player and user, mark the new pass `remaining` and defer RCON execution until promotion. On expiration, patch the old embed to `expired`, promote the next `remaining` pass to `active`, execute its RCON, patch its embed, and revoke the Discord role only when zero active passes remain for that user.
7. For in-game RCON commands triggered by Discord interactions, strip leading `/` from console commands, ensure `rcon.end()` runs in a `finally` block to prevent lingering socket connections, and append executed actions to `rcon-log.txt`.
8. Run one serialization self-check that constructs an `EmbedBuilder` and asserts footer text is exactly `Noesantara Network` and native timestamp exists. Avoid starting a second bot instance because its webhook port can collide with PM2.
9. Restart only intended PM2 process and verify liveness:
   ```bash
   pm2 restart <bot-name> --update-env
   sleep 3
   pm2 describe <bot-name>
   pm2 logs <bot-name> --lines 30 --nostream
   ```
   Require `status: online`, `unstable restarts: 0`, and a ready log before reporting success.
10. For panel refreshes, keep channel IDs in one small sender script, target only requested channels, delete only bot-authored messages, send item/rank/coin payloads, and avoid starting a second long-lived bot process. Build Coins from the existing panel convention or source-of-truth product builder, including its coin emoji/list/description and `Webstore Noesantara` link; omit only the body image when requested while retaining footer logo. Add `content: '|| @everyone ||'` when the panel convention requires a visible everyone mention, then verify it through the API. Never replace a rich existing panel with a minimal placeholder just because the catalog is available.
11. Check source for stale branding and inspect `git diff --check`. Report changed scope, runtime status, message IDs verified, and that unrelated human messages were preserved.

## RCON migration

- Resolve ambiguous ECO RPG labels against exact old/new panel server identifiers before changing the bot. Match target RCON allocation and active `server.properties` password; preserve other bot env keys and back up `.env` with owner-only permissions.
- Inspect PM2 RCON override key names without printing secrets. If no overrides exist and bot loads dotenv, restart only intended bot without `--update-env`; verify a fresh Discord ready log and `unstable_restarts: 0`.
- Recheck target power state immediately before final verification; earlier offline state may have changed. When running, use bot's installed `rcon-client` to authenticate and send read-only `list`, then close connection. TCP reachability alone does not prove password authentication. Never start a second Discord bot instance for this check.

## Pitfalls

- Do not rely on in-memory `setTimeout` for temporary Discord role assignments; PM2 reloads and process restarts discard in-memory timers, permanently orphaning expired roles on users. Use a persistent JSON store with a startup and interval check.
- Do not key temporary pass stores by `userId` alone when passes can stack; repeat commands will overwrite active entries, discard earlier queue timers, and orphan Discord message IDs needed for retroactive status patches.
- Do not leave RCON client sockets open or unhandled on exceptions; always place `rcon.end()` inside a `finally` block to prevent socket exhaustion.
- Do not prefix console commands with `/` in Minecraft RCON; console dispatchers expect bare command names and will fail or behave unpredictably.
- Do not forget to run `node deploy.js` when adding or modifying slash commands; Discord does not register new commands in the guild until `applicationGuildCommands` is updated.
- Do not add footer logic only to a shop panel when the requirement covers every embed; donation, announcement, moderation, utility, webhook, and future embeds use separate construction paths.
- Do not run `node index.js` as a verification probe while PM2 bot is online; the real webhook listener already owns its port and the probe exits with `EADDRINUSE`.
- Do not claim a PM2 restart succeeded from exit code alone; read process status and recent logs because a crash-loop can briefly report a successful restart.
- Do not use a second `setFooter()` after a centralized serialization hook unless intentionally preserving only the icon; Discord allows one footer object, so later calls replace earlier text.
- Do not claim old Discord embeds cannot be updated when retrofitting embed text or branding; query the relevant channels via Discord REST and PATCH each target bot-authored message in place rather than re-sending duplicates.
- For ephemeral catalog previews, inventory the supplied archive first, reject unsafe ZIP paths, and map each screenshot to a numbered/labelled option without claiming that screenshots prove the number of in-game skin variants. Prefer verified public HTTPS images over attachments: mobile clients may retain file-backed replies after dismissal. Add the select menu to the detail embed, route its custom ID through both the central interaction dispatcher and the detail handler, validate selected values against a fixed allowlist before building the image URL, and update the existing ephemeral reply rather than sending another message. Keep an existing kit preview menu working when adding pet previews. If an attachment is unavoidable, pass `files` and `attachments: []` on `interaction.update` to replace the prior preview. Test the initial reply, every selection/image URL, invalid values, and the old menu without starting a second bot; verify HTTP content type for all images, then restart only the targeted PM2 bot and check status.
- If a public catalog panel needs only text/option changes, fetch its exact bot-authored message and PATCH it in place through Discord REST; read back ID, description, options, mention content and URL button. This avoids duplicate panel messages or fresh `@everyone` notifications.
