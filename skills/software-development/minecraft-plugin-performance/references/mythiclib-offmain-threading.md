# MythicLib & Off-Main Event Threading Collisions

## Problem
In Paper 1.20+ with Moonrise/TickThread safety enforcement, plugins executing world mutations (entity spawning, lightning strikes, exp drops, block modifications) off the main thread throw:
`[ca.spottedleaf.moonrise.common.util.TickThread] Thread failed main thread check: Cannot add entity off-main`

When MythicMobs evaluates skill target conditions asynchronously (`lumine-fscheduler` / `Craft Scheduler Thread`), MythicLib with `interaction_rules.enabled: true` checks PvP/PvE rules by calling `EntityManager.canInteract()`, which fires fake Bukkit damage/interact events asynchronously.

Downstream event listeners (such as AdvancedEnchantments listening to `AttackTrigger` / `DefenseTrigger`) catch these fake events on the async thread and attempt to spawn entities (`GUARD`), strike lightning, or mutate `ItemStack` data components concurrently.

## Symptoms
1. Repeated thousands of lines of `Thread failed main thread check: Cannot add entity off-main` in server logs.
2. Packet encoding failures on Netty threads: `EncoderException: Failed to encode packet 'clientbound/minecraft:container_set_content'` caused by concurrent item component mutations.
3. Proxy connection timeouts on Velocity/BungeeCord: players kicked with `kicked from server: disconnect.timeout` or `read timed out` as backend main/Netty threads stall.

## Zero-Downtime Fix (No Restart Required)

### Step 1: Disable MythicLib Interaction Rules (For Non-PvP Worlds)
1. Inspect `plugins/MythicLib/config.yml`.
2. Disable interaction rules:
   ```yaml
   interaction_rules:
     enabled: false
   ```
   *Note: Interaction rules are toggled off by default in MythicLib; party/guild PvP checks are typically handled independently by BetterTeams or WorldGuard.*
3. Write file via Pterodactyl API (`POST /files/write?file=plugins%2FMythicLib%2Fconfig.yml`).
4. Read back the exact lines to confirm change landed.
5. Reload MythicLib and MythicMobs runtime:
   - Console command: `ml reload` (reloads MythicLib config)
   - Console command: `mm reload` (reloads MythicMobs skill engine)
6. Verify console output confirms `MythicLib reloaded successfully` and `[MythicMobs] Mythic has finished reloading!`.

### Step 2: Fix AdvancedEnchantments `WAIT:1` (For PvP Worlds, e.g. Nether)
- **PvP World Pitfall:** In worlds where PvP is globally active (`world.getPVP() == true`, such as `world_nether`), MythicLib's `EntityManager.canInteract()` unconditionally fires `DamageCheckEvent` (subclass of `EntityDamageByEntityEvent`) on the async thread even when `interaction_rules.enabled: false`.
- **Root Fix in AE:** Prefix entity-mutating effects (`GUARD:`, `EXP:`, `LIGHTNING`) with `- WAIT:1` in `plugins/AdvancedEnchantments/enchantments.yml` for all triggered enchants (especially `type: DEFENSE`, `type: DEFENSE_MOB`, or `type: ATTACK`, e.g. `xpgain`, `guardians`, `spirits`, `undeadruse`, `explosivedemise`).
- **Mechanism:** In AdvancedEnchantments, `WAIT:1` delays effect execution by 1 tick via Bukkit's synchronous main thread scheduler (`SchedulerUtils.runTask`), moving `world.spawn()` / `strikeLightning()` safely onto the main thread regardless of which thread fired the damage check.
- **Reload:** Execute console command `ae reload`.
- **Verification:** Confirm zero subsequent `Cannot add entity off-main` errors across all worlds in `logs/latest.log`.
