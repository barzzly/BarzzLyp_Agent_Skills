# Headless Minecraft testing and chat control

## 1. Establish scope and baseline

Use one non-OP bot for a bounded live smoke test. Confirm proxy allocation and backend alias through panel API and proxy config. Java login does not test Geyser/Floodgate; a single idle bot does not test player capacity. Keep credentials private in the project directory.

Save timestamped CPU/RAM samples before, during, and after the session. Request backend `list`, `tps`, and `mspt` where supported; read their actual responses from logs. Do not assign TPS to Velocity. Report sample count, duration, player count, units, failures, and untested gameplay separately from latency. Persist data before long waits so interrupted work remains reportable.

## 2. Prepare authentication and controls before connecting

Inspect the installed auth plugin's registration syntax, confirmation setting, password pattern, and CAPTCHA configuration. JPremium may permit lobby spawn but silently block `/server` before authentication. Its password-length rejection can describe only the minimum even when the maximum was exceeded.

For a new test account, generate a password matching the configured constraints, store mode 0600, and register normally. Reuse that password for login; never regenerate it after successful registration. Do not guess existing credentials, disable auth, or remove a whitelist to complete a smoke test. Redact registration/login payloads from local command logs.

Create the stdin control handler, sanitized event log, graceful quit, and finite session timer before launching. Keep at most one connected bot. Register plugin-dependent methods such as `chatAddPattern` after `login`, because Mineflayer injects these asynchronously. Guard early shutdown when `bot.quit` is not yet available, falling back to the protocol client's `end` method. Run `node --check` and small parser assertions before starting.

## 3. Verify backend transfer and resource-pack behavior

Send `/server <alias>` only after auth succeeds. Confirm the exact bot's backend connection in proxy/backend logs and updated world/position or chunk data; not every transfer produces another Mineflayer `spawn` event. Command-send logs alone are insufficient.

If transfer stalls during configuration, inspect the installed resource-pack handler before changing server settings. Some implementations of `denyResourcePack` send both UUID and UUID-less replies; modern serialization then fails. When that mechanism is confirmed, replace only the client handler rather than changing server resource-pack policy.

For a deliberately headless protocol test, the verified handler shape is:

```js
const bot = mineflayer.createBot({ ...options, plugins: { resource_pack: false } })
bot._client.on('add_resource_pack', data => {
  for (const result of [3, 0]) {
    bot._client.write('resource_pack_receive', { uuid: data.uuid, result })
  }
})
```

This simulates accepted/loaded status to complete protocol negotiation; it does not download, apply, render, or validate the pack. Disclose this limitation explicitly. Use a real client for pack-loading or visual acceptance testing. Match packet names and fields to the installed protocol version.

## 4. Prove chat identity and delivery

Capture `messagestr` with channel and sender metadata; exclude repetitive action bars from chat-review output. Prefer authoritative sender UUID. Custom chat plugins may omit it, so inspect real rendered messages and cross-check server logs before trusting a fallback parser.

Use anchored server-format parsing with separate username/message captures. For a server format ending in `TestOwner ➼ message`, a restricted parser can resemble `/^[^➼\r\n]*\s(TestOwner) ➼ (.*)$/`; adapt to observed format and escape dynamic names. Test genuine owner messages and another player's message containing `TestOwner ➼ /ping`. Do not treat display-name matching as authenticated identity for privileged operations.

Verify outgoing messages by reading back server/client chat, not by successful `bot.chat()` return. If a moderation filter rejects the text, mark delivery failed; do not claim the player saw it or attempt filter evasion.

## 5. Separate scripted actions from AI participation

For scripted smoke-test control, allowlist exact low-risk commands and arguments, reject multiline or chained input, rate-limit, and suppress duplicate handling from overlapping chat events. When the user explicitly requests a player-action AI, do not mistake a tiny fixed command list for the deliverable: provide natural-language AI tool selection, ordinary owner-requested player commands, movement/navigation and interaction tools, and report unimplemented mechanics. Retain explicit boundaries for host access, credential/account operations, privileges, and high-impact actions; do not silently promote the bot to OP. Gate commands that move away from the target backend by current test scope. A recognized owner message proves capture only: require one live command and its server-side result before claiming automatic execution works.

For an AI-participation request, a real model-to-chat/action bridge is an additional acceptance criterion, not implied by logging or regex parsing. Do not describe an unimplemented bridge as active. Player messages remain scoped inputs, never system instructions, shell source, or permission to expose secrets. Limit any future bridge to explicit gameplay actions and require trusted-channel approval for destructive, privilege, security, or host operations.

### AI bridge acceptance and boundaries

Use actual model tool calls with bounded conversation history and serialize requests. Set `stream: false` explicitly when parsing Chat Completions JSON; some compatible routers default to SSE. Keep model credentials outside prompts and logs. Validate final replies as well as tool arguments: `bot.chat` executes leading-slash text, so reject leading slash and control/newline characters on EVERY ordinary chat output. Only a separate command tool may dispatch validated commands. Include `/ask <bounded text>` if help-question execution is requested; prose/bracket parsing belongs to the model, not the command validator.

Feed observed server feedback back to the model and distinguish sent, accepted, permission denied, and unknown results. Test a labelled operator model request separately from genuine owner chat; verify both actual command dispatch and returned chat in server logs. Never claim an operator harness proved owner-message routing. Check fresh model errors and backend state before announcing readiness.

### Player-action extensions

For navigation load Mineflayer pathfinder and explicitly disable automatic digging, towers, doors, and scaffold placement unless specifically required. Resolve owner from currently visible entities, not merely the chat/tab list; cross-world/vanished players may chat while absent from the bot's perception. Stop must clear controls, path goals and digging immediately, not wait behind an AI API call. Bound follow/action lifetimes.

For digging/placing require exact finite integer block coordinates, reach and visibility checks, user-authorized gameplay context, and cancellation timeout. Do not gate Indonesian natural-language mining behind English keywords: requests such as `ambil snow ini 10 biji drop ke gw` already authorize the mining/collection/drop workflow. Once ordinary gameplay is authorized, do not ask permission again; add nearby-block perception so the model can resolve targets itself. Attribute local validator failures to the bot, never falsely to server protection. Never substitute an arbitrary block ahead when coordinates are absent. Mineflayer digging can optimistically set local block state to air; do not call that authoritative server verification. Inspect the current window before clicking and invalidate inspection on window/slot changes. Validate namespaced commands against the canonical command root; `/minecraft:op` must not bypass an `op` block.

## 6. Report runtime honestly

Use a background PTY with stdin for operator-driven sessions and a finite lifetime. Verify current process plus fresh keepalives/backend state before saying online. State which functions remain automatic while the agent is not taking a turn; log capture does not mean an AI is continuously reading and replying. Treat old-process completion notices separately from the active session, and report only changed conclusions.
