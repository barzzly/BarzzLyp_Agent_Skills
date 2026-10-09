---
name: test-driven-development
description: "TDD: enforce RED-GREEN-REFACTOR, tests before code."
version: 1.1.0
author: Hermes Agent (adapted from obra/superpowers)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [testing, tdd, development, quality, red-green-refactor]
    related_skills: [systematic-debugging, subagent-driven-development]
---

# Test-Driven Development (TDD)

## Overview

Write the test first. Watch it fail. Write minimal code to pass.

**Core principle:** If you didn't watch the test fail, you don't know if it tests the right thing.

**Violating the letter of the rules is violating the spirit of the rules.**

## When to Use

**Always:**
- New features
- Bug fixes
- Refactoring
- Behavior changes

**Exceptions (ask the user first):**
- Throwaway prototypes
- Generated code
- Configuration files

Thinking "skip TDD just this once"? Stop. That's rationalization.

## The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Write code before the test? Delete it. Start over.

**No exceptions:**
- Don't keep it as "reference"
- Don't "adapt" it while writing tests
- Don't look at it
- Delete means delete

Implement fresh from tests. Period.

## Red-Green-Refactor Cycle

### RED — Write Failing Test

Write one minimal test showing what should happen.

**Good test:**
```python
def test_retries_failed_operations_3_times():
    attempts = 0
    def operation():
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise Exception('fail')
        return 'success'

    result = retry_operation(operation)

    assert result == 'success'
    assert attempts == 3
```
Clear name, tests real behavior, one thing.

**Bad test:**
```python
def test_retry_works():
    mock = MagicMock()
    mock.side_effect = [Exception(), Exception(), 'success']
    result = retry_operation(mock)
    assert result == 'success'  # What about retry count? Timing?
```
Vague name, tests mock not real code.

**Requirements:**
- One behavior per test
- Clear descriptive name ("and" in name? Split it)
- Real code, not mocks (unless truly unavoidable)
- Name describes behavior, not implementation

### Verify RED — Watch It Fail

**MANDATORY. Never skip.**

```bash
# Use terminal tool to run the specific test
pytest tests/test_feature.py::test_specific_behavior -v
```

Confirm:
- Test fails (not errors from typos)
- Failure message is expected
- Fails because the feature is missing

**Test passes immediately?** You're testing existing behavior. Fix the test.

**Test errors?** Fix the error, re-run until it fails correctly.

### GREEN — Minimal Code

Write the simplest code to pass the test. Nothing more.

**Good:**
```python
def add(a, b):
    return a + b  # Nothing extra
```

**Bad:**
```python
def add(a, b):
    result = a + b
    logging.info(f"Adding {a} + {b} = {result}")  # Extra!
    return result
```

Don't add features, refactor other code, or "improve" beyond the test.

**Cheating is OK in GREEN:**
- Hardcode return values
- Copy-paste
- Duplicate code
- Skip edge cases

We'll fix it in REFACTOR.

### Verify GREEN — Watch It Pass

**MANDATORY.**

```bash
# Run the specific test
pytest tests/test_feature.py::test_specific_behavior -v

# Then run ALL tests to check for regressions
pytest tests/ -q
```

Confirm:
- Test passes
- Other tests still pass
- Output pristine (no errors, warnings)

**Test fails?** Fix the code, not the test.

**Other tests fail?** Fix regressions now.

### REFACTOR — Clean Up

After green only:
- Remove duplication
- Improve names
- Extract helpers
- Simplify expressions

Keep tests green throughout. Don't add behavior.

**If tests fail during refactor:** Undo immediately. Take smaller steps.

### Repeat

Next failing test for next behavior. One cycle at a time.

## Avoid Horizontal Slices

Do **not** write all tests first and then all implementation. That is horizontal slicing: RED becomes "write a pile of imagined tests" and GREEN becomes "make the pile pass." It produces brittle tests because the tests are designed before the implementation has taught you what behavior and interface actually matter.

Use vertical tracer bullets instead:

```text
WRONG:
  RED:   test1, test2, test3, test4
  GREEN: impl1, impl2, impl3, impl4

RIGHT:
  RED→GREEN: test1→impl1
  RED→GREEN: test2→impl2
  RED→GREEN: test3→impl3
```

A tracer bullet is one end-to-end behavior slice. It proves the path works, teaches you about the interface, and keeps each next test grounded in what you just learned.

## Why Order Matters

**"I'll write tests after to verify it works"**

Tests written after code pass immediately. Passing immediately proves nothing:
- Might test the wrong thing
- Might test implementation, not behavior
- Might miss edge cases you forgot
- You never saw it catch the bug

Test-first forces you to see the test fail, proving it actually tests something.

**"I already manually tested all the edge cases"**

Manual testing is ad-hoc. You think you tested everything but:
- No record of what you tested
- Can't re-run when code changes
- Easy to forget cases under pressure
- "It worked when I tried it" ≠ comprehensive

Automated tests are systematic. They run the same way every time.

**"Deleting X hours of work is wasteful"**

Sunk cost fallacy. The time is already gone. Your choice now:
- Delete and rewrite with TDD (high confidence)
- Keep it and add tests after (low confidence, likely bugs)

The "waste" is keeping code you can't trust.

**"TDD is dogmatic, being pragmatic means adapting"**

TDD IS pragmatic:
- Finds bugs before commit (faster than debugging after)
- Prevents regressions (tests catch breaks immediately)
- Documents behavior (tests show how to use code)
- Enables refactoring (change freely, tests catch breaks)

"Pragmatic" shortcuts = debugging in production = slower.

**"Tests after achieve the same goals — it's spirit not ritual"**

No. Tests-after answer "What does this do?" Tests-first answer "What should this do?"

Tests-after are biased by your implementation. You test what you built, not what's required. Tests-first force edge case discovery before implementing.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks. Test takes 30 seconds. |
| "I'll test after" | Tests passing immediately prove nothing. |
| "Tests after achieve same goals" | Tests-after = "what does this do?" Tests-first = "what should this do?" |
| "Already manually tested" | Ad-hoc ≠ systematic. No record, can't re-run. |
| "Deleting X hours is wasteful" | Sunk cost fallacy. Keeping unverified code is technical debt. |
| "Keep as reference, write tests first" | You'll adapt it. That's testing after. Delete means delete. |
| "Need to explore first" | Fine. Throw away exploration, start with TDD. |
| "Test hard = design unclear" | Listen to the test. Hard to test = hard to use. |
| "TDD will slow me down" | TDD faster than debugging. Pragmatic = test-first. |
| "Manual test faster" | Manual doesn't prove edge cases. You'll re-test every change. |
| "Existing code has no tests" | You're improving it. Add tests for the code you touch. |

## Red Flags — STOP and Start Over

If you catch yourself doing any of these, delete the code and restart with TDD:

- Code before test
- Test after implementation
- Test passes immediately on first run
- Can't explain why test failed
- Tests added "later"
- Rationalizing "just this once"
- "I already manually tested it"
- "Tests after achieve the same purpose"
- "Keep as reference" or "adapt existing code"
- "Already spent X hours, deleting is wasteful"
- "TDD is dogmatic, I'm being pragmatic"
- "This is different because..."

**All of these mean: Delete code. Start over with TDD.**

## Verification Checklist

Before marking work complete:

- [ ] Every new function/method has a test
- [ ] Watched each test fail before implementing
- [ ] Each test failed for expected reason (feature missing, not typo)
- [ ] Wrote minimal code to pass each test
- [ ] All tests pass
- [ ] Output pristine (no errors, warnings)
- [ ] Tests use real code (mocks only if unavoidable)
- [ ] Edge cases and errors covered

Can't check all boxes? You skipped TDD. Start over.

## When Stuck

| Problem | Solution |
|---------|----------|
| Don't know how to test | Write the wished-for API. Write the assertion first. Ask the user. |
| Test too complicated | Design too complicated. Simplify the interface. |
| Must mock everything | Code too coupled. Use dependency injection. |
| Test setup huge | Extract helpers. Still complex? Simplify the design. |

## Hermes Agent Integration

### Running Tests

Use the `terminal` tool to run tests at each step:

```python
# RED — verify failure
terminal("pytest tests/test_feature.py::test_name -v")

# GREEN — verify pass
terminal("pytest tests/test_feature.py::test_name -v")

# Full suite — verify no regressions
terminal("pytest tests/ -q")
```

### With delegate_task

When dispatching subagents for implementation, enforce TDD in the goal:

```python
delegate_task(
    goal="Implement [feature] using strict TDD",
    context="""
    Follow test-driven-development skill:
    1. Write failing test FIRST
    2. Run test to verify it fails
    3. Write minimal code to pass
    4. Run test to verify it passes
    5. Refactor if needed
    6. Commit

    Project test command: pytest tests/ -q
    Project structure: [describe relevant files]
    """,
    toolsets=['terminal', 'file']
)
```

### With systematic-debugging

Bug found? Write failing test reproducing it. Follow TDD cycle. The test proves the fix and prevents regression.

Never fix bugs without a test.

## Node Crypto and Round-Rollover Tests

- For history-dependent demo rules, test the actual HTTP rollover as well as the sampler; a passing helper test does not prove production calls it.
- When deterministic tests must replace Node crypto entropy, restore the original function and call `syncBuiltinESMExports()` after both replacement and restoration. Keep overrides inside isolated test processes; never add production override endpoints.
- Test both sides of streak thresholds, interruption by a qualifying result, reset behavior, and maximum output. Remove stale UI claims of independent outcomes when rules depend on history.

## Durable Wallet Game Checks

- Run money tests against a separate loopback MariaDB instance and randomized disposable databases; never load deployment `.env` or seed real player accounts.
- Audit every suite connection, including read-only sampler tests that select the system `mysql` schema. When disposable schemas are mandatory, change only a staged test copy to a random owned schema, preserve assertions, restore the copy before build, and verify schema lists before/after. Include shared display tests when counting frontend coverage.
- For release snapshots sharing installed `node_modules`, run `npm run check -- --incremental false` when tsBuildInfoFile points inside that symlink; this prevents verification from rewriting shared compiler cache. Hash live dist and source before/after, and build only inside a unique staging directory.
- Test concurrent same-wallet operations before integrating games: `INSERT IGNORE` followed by `SELECT ... FOR UPDATE` can deadlock shared-lock upgrades; an exclusive duplicate-key update avoids that upgrade pattern.
- Lock own wallet before singleton game room and never lock other wallets during rollover; loss settlement needs only game-entry changes because stakes were debited already.
- Read authoritative DB time after acquiring game locks; queued cashouts must not settle using stale request-arrival timestamps.
- Inject SQL trigger failures after wallet changes to prove entry, ledger, and balance roll back together; read persisted results from a separate Node process to verify restart durability.
- Treat an idempotent ledger hit without its matching game entry as corruption and fail closed, rather than creating a free stake.

## React pages without a DOM test dependency

- Build standalone SSR harnesses with esbuild `jsx: 'automatic'`; project JSX config may otherwise emit `React.createElement` without a React binding. Put generated CJS inside project-local temporary folders (or supply project module resolution), since `/tmp` outputs with external packages cannot find project React. Keep React Query provider and hooks on the same CJS export to avoid duplicate contexts. Distinguish harness failures from production regressions.

- When a formerly public helper starts rejecting authorization failures, search every caller, including legacy modals and raw-fetch duplicates. Test private failures independently from public-profile loading, and render account switches before effects run to catch stale private rows. Report active callers outside assigned ownership rather than silently widening edits.

- Use installed esbuild with CSS loader `empty`, external React packages, and `react-dom/server` to assert rendered access gates and form states without adding a test framework; wrap wouter pages with `Router` and `ssrPath` to avoid browser-location errors.
- Seed React Query caches by account UUID when checking private history; test that an unrelated account cache never renders after account changes.
- Treat `navigator.onLine === false` as offline, not a falsy value; Node exposes `navigator` without browser connectivity state.
- Test feature flags with missing, false, and true values; high-risk actions must require explicit server enablement.

- Run generated browser checks in a real browser; successful esbuild bundling does not execute assertions. Serve oversized bundles from a loopback-only artifact server and load a script element rather than sending megabytes through CDP IPC. Record actual assertion results separately from Node test totals.
- Check challenge expiration again when asynchronous approvals arrive, against both stored challenge deadline and response deadline; polling can cross expiry after request start. Hold stale nickname/status/challenge responses and release them after replacement to verify newer form state survives.

## MariaDB Wallet Concurrency Checks

- Run money-state tests against a disposable database on a dedicated loopback MariaDB instance when production credentials cannot create isolated databases; never point fixture resets or global settings at a shared production server.
- Test more concurrent requests than pool capacity. Never acquire another connection from the same pool while holding business transaction locks; reserve persistent auth backoff first, and clear only its own attempt token after verification.
- Reproduce same-wallet lock upgrade races with many parallel valid writes. `INSERT IGNORE` followed by `SELECT FOR UPDATE` can deadlock; an idempotent duplicate-key UPDATE obtains the exclusive row lock directly.
- Separate transport HMAC timestamp from observed presence timestamp. Test older online snapshots arriving after offline snapshots, and historical result retries after snapshot TTL; neither may refresh online balance.

## Express wallet boundary checks

- Exercise case and trailing-slash variants of every feature-gated endpoint. Express default routing can match `/Transfers/` while an exact `req.path` gate checks only `/transfers`; attach guard directly to routes or enforce canonical strict routing, and assert no wallet/DB entry while disabled.
- Put small wallet parsers ahead of large generic upload parsers; checking `rawBody.length` after a 50MB global parse does not bound allocation. Preserve exact raw bytes for HMAC and test unsupported types and routing variants.
- Recheck expiration after locking reads and after asynchronous PIN verification/hash or account-binding waits, immediately before issuing credentials or approving challenges. Pre-lock `Date.now()` SQL parameters can expire while queued.

## Session/challenge race regression checks

- Hold controlled transport responses while exercising real fetch helper and React Query; release old success and old 401 responses after logout, revoke, login/account switch, and session expiry. Assert both cached identity and next mutation's CSRF header, not merely request rejection.
- Cancel queries synchronously before replacing auth caches; also guard post-JSON side effects with generations because transports can complete despite abort. Keep challenge UI derived from session cache so an absent challenge clears it, and reject approvals whose code no longer matches.
- Bound locally retired challenge codes through expiry; local memory cancellation does not revoke server cookies or survive a full document reload. Use a server cancellation endpoint if persistent cancellation becomes required.

## Durable provider receipt protocol checks

- Agree provider wire contract before implementing backend proof validation; storage brand guesses or integer-only balance assumptions can break a correct provider. Parse bounded canonical decimal strings with scaled BigInt, bind operation/player/attempt/kind/amount, and distinguish trusted bridge attestation from independent storage proof.
- Require an explicit durable provider capability plus fresh accepted advertisement for new claims; recheck after queued wallet acquisition. Let proven historical settlement remain independent of new-transfer enablement and live presence. Never infer a durable failed/fenced operation from provider exceptions.
- Test additive migrations on populated old schemas, repeat them, and assert money remains unchanged; CREATE TABLE IF NOT EXISTS alone does not upgrade columns. Make schema readiness probe required columns.
- Measure successful HTTP operations beyond pool capacity with p50/p95/max, exact success/error counts, and ledger cardinality; never report rejection throughput as settlement capacity.

## Best-effort Vault transfer checks

- Test fsynced intent before calling Vault, preserve last observed integer balance for restart UNKNOWN, and replay exact persisted attempts/results without requiring an online player. A local fsync does not prove Essentials async persistence; never label Vault receipts durable.
- Treat any failure, exception, nonfinite result, response mismatch, or wrong decimal delta after a Vault invocation as UNKNOWN; only pre-invocation fences can be FAILED. Keep UNKNOWN player locks after backend acknowledgment and never auto-reverse.
- Test provider disable/name changes, signed-auth loss, delayed main-thread callbacks, shutdown, and mismatched confirmations before live plugin integration. Supply explicit main-thread and transport hooks so offline checks can exercise the real engine without real wallets.

- Hold an already-started Vault callback beyond the worker deadline until UNKNOWN is durably acknowledged; then release exact success and require same-attempt durable upgrade, fresh acknowledgment, and exact restart replay without another Vault call. Also close while it is held: stop transport/new work, retain journal until completion, and report a permanently hung provider as unresolved shutdown rather than discarding its result.

## Offline Journal Stress

- Snapshot production source and harness into a dedicated artifact tree before compiling; hash both plus cached dependency JARs, and compare original source hashes after execution. Never borrow mutable plugin build outputs during parallel work.
- Test cross-process exclusion both directly and after a rejected same-JVM duplicate open. Closing a second descriptor for a locked inode can release process-associated OS locks even while Java still considers its original FileLock valid.
- Replay identical provider success after acknowledgment and assert acknowledgment remains durable; separately require fresh acknowledgment when UNKNOWN upgrades to newly proven SUCCESS.
- Verify journal startup with actual `strace -f -yy` fsync paths before first record write; inject EIO at each directory fsync and require startup rejection before claim/intent. Force existing ancestors too: a failed earlier startup can leave directories present but not durably linked. State clearly that syscall ordering and Runtime.halt do not simulate disk power loss.
- Separate complete temporary-record recovery liveness from corruption fail-closed safety. Preserve staged files and exact failure traces; a disabled journal is not proof of lost money or duplicate settlement.
- Keep seeded model counts, named scenario counts, reached assertions, source hashes, and real child exit codes machine-readable. Runtime.halt tests process death, not actual disk power loss.

## Password Transfer Authentication Races

- Key password-bearing wallet UI by account UUID plus session CSRF identity so expiry, revocation, and account replacement discard secrets, eye visibility, and retry intent together. Guard async completions with both mount lifetime and current query-cache identity; release held responses before React commits replacement to catch stale private-cache writes that unmount guards alone miss.

- Test password transfers through real login cookies against a disposable MariaDB schema; pause real Argon2 verification to replace password hashes or expire sessions, then assert balances, transfer rows, and ledger remain unchanged.
- Keep automatic pending-transfer refunds inside the authenticated transfer transaction; otherwise an expired session can mutate balances before the final authorization check. Recheck expiry after row-lock waits before refund or new hold writes.
- Avoid range `FOR UPDATE` scans followed by inserts on the same transfer index: adjacent accounts can deadlock on next-key gaps. Discover bounded candidate IDs without locks, then lock each primary key and revalidate status under the already-held wallet lock. Verify successful requests beyond pool capacity, not merely rejection throughput.

## Password Reset Database Races

- Hold account locks before challenge locks across both new password and legacy approval/completion routes; test each legacy route racing reset, because mixed lock order can deadlock even when new-flow concurrency passes.
- Split UUID/name identity checks into unique-index point reads instead of an OR locking query; inspect InnoDB deadlock output when independent account requests lock unrelated rows.
- Test expiry after revocation waits, not only after hashing; roll back password, session/device deletion, and challenge approval together when the final deadline check fails.
- Exercise concurrent distinct reset codes for one account and independent accounts beyond pool capacity; add indexes for challenge revocation predicates and preserve single-use winners.

## Best-effort bridge settlement checks

- Pin provider identity on each transfer row before claim; test provider switches and feature disablement between creation, claim, and historical settlement. Additive migrations must assign legacy rows their prior provider without rewriting populated provider fields on repeated upgrades.
- Distinguish timed-out review with NULL outcome from explicitly reported UNKNOWN. Test delayed signed non-invocation failures after timeout, but never let UNKNOWN become failed/refunded; provider exceptions after invocation remain ambiguous.
- Derive pre-invocation failure reason allowlists from actual engine wire output, not invented receipt fields. Document that HMAC authenticates engine assertions and cannot prove unchanged Essentials/Vault disk durability.

## Single-command deposit verification

- Keep native single-command deposit on the existing authenticated prepare/claim/journal/mutate path. Test RED on missing dispatch and player feedback separately; preserve legacy withdrawal and provider-specific commands.
- Run insufficient-funds checks before deliberately losing settlement acknowledgments: unacknowledged journals correctly fence subsequent transfers. Compare unchanged balance with the actual pre-command Vault reading, not a decimal literal; official providers can expose binary floating-point conversion differences.
- Stop and join isolated transfer workers before deleting fixture directories; asynchronous journal initialization/close can race recursive cleanup even after plugin disable returns. Create foreign-owner fixture accounts before assigning transfer UUIDs; preserve database foreign-key constraints.

## Game Router Boundary Checks

- Mount bounded JSON/admission ingress before global upload parsers for every money-game API prefix, not only wallet auth. Exercise production mount statements with case/trailing-slash, chunked, and unsupported-type requests; assert oversized bodies never reach global parsers.
- Retain admission until game transactions settle after HTTP disconnect; hold room locks, abort eight admitted requests, and require immediate rejection of further work. Middleware-only retention ends before downstream async game handlers finish.
- Revalidate HTTP session identity under transaction locks after wallet and room waits; test logout during queued join and expiry during queued cashout with unchanged ledger/balance. Keep direct trusted service fixtures distinct from browser identity.

## Uncertain frontend transfer retries

- Keep original request ID, amount, and direction through every ambiguous retry response, including auth/throttle 4xx and malformed 200. A later rejection cannot disprove an earlier commit. Resolve only a validated same-ID own-transfer response; history lists without request IDs cannot safely correlate intent.
- Replay frozen intent despite balance/presence preflight changes caused by its prior hold; enforce full preflight for new intent. Compose default transport deadline with caller cancellation and cover body reads, preserving explicit abort reasons.
- Guard game success, errors, and finally writes with both session-cache identity and effect/mutation generation. Key authenticated subtrees by UUID plus CSRF; an alive boolean alone fails cleanup/setup replay.
- When SSR tests bundle pages as CJS, obtain React Query provider from the same CJS export. Mixing ESM provider and CJS hook creates separate contexts and false missing-provider failures.

## Storefront session and history checks

- Before retiring game routes, trace shared account sessions and purchase-history verification links. Keep a non-game verification page and narrowly allow auth/password bridge endpoints; block economy APIs before parsers with case/trailing-slash coverage, including GET handlers that settle or expire money. Never remove financial tables as feature cleanup.
- For Node SSR checks of TSX pages, set esbuild `jsx: 'automatic'` and create temporary bundles beneath the staged project so external dependencies resolve through its node_modules; clean them after each run.

- Test session insertion/invalidation failures with SQL triggers on disposable MariaDB, and require no cookie before commit. Freeze time across two logins to catch identical JWTs; add random `jti` without changing existing session schema.
- Test both authentication and history query identity semantics. A matching-account middleware cannot close IDOR when downstream SQL expands Java `Foo` into Bedrock `.Foo`; keep leading dots significant and test actual returned rows after route integration.

## Storefront RCON Payment Checks

- Reproduce mysql2 FOUND_ROWS races against disposable MariaDB using more parallel callbacks/status/admin retries than pool capacity; change claim predicate before remote invocation rather than treating unchanged matched rows as claim wins.
- Persist per-item intent before RCON and fence unknown/processing forever until independent reconciliation. Test intent, acknowledgment, and final-order DB failures; never call database fencing exactly-once remote delivery.
- Quarantine every pre-migration undelivered invoice, including pending discounted ranks, because new checkout validation cannot repair historical ownership proof. Test repeated additive migration without changing amounts.
- Bind provider reference/order and exact gross created invoice amount on callback/detail; distinguish customer fees from merchant net receipts using provider documentation. Keep manual fulfillment pending and exact dotted player identities separate in authenticated history HTTP tests.

- For explicit manual fulfillment, assert one atomic terminal write across status, delivered flag, state and timestamp; then reject downgrades using each terminal marker independently. Test mixed carts with unchanged acknowledged journals, a held active remote claim, SQL-trigger write failure, and bridge INSERT defaults. Keep processing/review fenced rather than treating manual approval as an uncertainty bypass.

## Admin CSRF rotation checks

- Reproduce retired-admin authorization with a valid JWT and matching active DB row; require both identities to equal current configured admin exactly. Test health-check and delegated private-history gates too.
- Test session-bound CSRF with two real logins and replay the first CSRF against the second auth cookie. Replace plain CSRF fixtures with issued login tokens so persistence/logout fault tests still reach their intended DB operation.
- Exercise production and development cookie modes against disposable DB schemas. Assert __Host- cookie issue/clear attributes, production rejection of legacy cookies, and client preference for host cookies while preserving login-response store behavior.

## Private skill-game settlement checks

- Test locked foreign primary keys before using `WHERE id=? AND owner=? FOR UPDATE`; InnoDB may wait on the foreign row before filtering owner. Discover ownership without a locking read, then lock only verified own primary keys under own-wallet serialization.
- Test speed-derived rewards through actual persisted settlement, not only a helper. Subtract accumulated mandatory reveal/earliest-valid timing waits from DB elapsed time, compare fast and slow valid completions, and require identical skill weight when only forced reveal duration changes.
- Use `RTRIM` on CHAR inputs in indexed MariaDB generated columns when padding SQL modes make the expression non-deterministic; exercise the migration on the real disposable server rather than assuming MySQL compatibility.

## Private skill-based fishing games

- Bound economy tuning against perfect automated play, not assumed human failures; publish base multipliers/odds and compute maximum expected gross payout with integer rounding. Browser-visible memory puzzles are automatable, not proof of cheating-resistant play.
- Derive skill rewards from locked server time minus accumulated mandatory reveal/timing waits; never randomize weight when requirements tie it to completion speed. Test fast/slow completions and forced-wait neutrality independently.
- Exercise every rarity through actual browser controls against disposable DB fixtures. Prime and foreground the browser before creating time-sensitive fixtures; navigation delay can consume a valid timing window and falsely suggest broken gameplay. Store each batch durably, aggregate latest results by rarity, and assert seven unique completed tiers.
- Persist both cast intent and current action choice across reload. Clear a first definitive rejection only when no earlier ambiguous attempt exists; unrelated successful state/history reads must not clear an unresolved same-step action.
- Preserve hidden-card positions after selecting first card, retaining disabled empty slot across steps. Hide cached faces locally at reveal deadline as well as in subsequent server payloads; step count alone does not make higher rarity harder.

## Animated game frontend checks

- Keep animation phases cosmetic: CSS animationend may never fire under reduced motion, so add a cleaned-up bounded phase fallback without delaying challenge availability or altering authoritative clocks.
- Foreground browser before measuring running CSS transforms; background throttling can leave transforms unchanged despite a running animation. Assert computed transforms, pointer-down feedback before response, accepted-step progress, and reduced-motion completion separately.
- Scroll the whole playable arena below sticky navigation, not only its nested challenge. Measure rod top and every target bottom at mobile dimensions; test against production CSS as well as isolated fixture CSS. Scope clue-list selectors to `ol` when protocol sections share their class names.

## Testing Anti-Patterns

- **Testing mock behavior instead of real behavior** — mocks should verify interactions, not replace the system under test
- **Testing implementation details** — test behavior/results, not internal method calls
- **Happy path only** — always test edge cases, errors, and boundaries
- **Brittle tests** — tests should verify behavior, not structure; refactoring shouldn't break them

## Final Rule

```
Production code → test exists and failed first
Otherwise → not TDD
```

No exceptions without the user's explicit permission.
