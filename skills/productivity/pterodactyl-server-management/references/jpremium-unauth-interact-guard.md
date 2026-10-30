# JPremium Unauthorized Interact & Server Transfer Exploit Mitigation

## Problem & Vulnerability Root Cause
1. **Proxy Level (Velocity):**
   In `/plugins/jpremium/configuration.yml`, if `limboServerNames: []` is empty:
   `JPremiumVelocity.ServerPreConnectEvent` checks:
   `if (targetServer != null && !limbo.isEmpty())`
   Because `limbo.isEmpty()` is true, the denial check is skipped. Any unauthenticated cracked player can be transferred to backend servers (e.g., `noerpg`, `noerp`) via BungeeCord plugin messages (`Connect`), ajQueue, or commands without ever typing `/login` or `/register`.

2. **Backend/Lobby Level (Paper):**
   - **FancyNpcs Bypass:** FancyNpcs uses packet-level interception (PacketEvents) to capture player interactions with virtual NPCs. Bukkit's standard `PlayerInteractEntityEvent` does not protect virtual NPCs.
   - **Hotbar / Menu Bypass:** Players clicking custom menu items (e.g. DeluxeHub server selector) trigger `PlayerInteractEvent` and `InventoryClickEvent`. If not cancelled at `LOWEST` priority before authentication, players can open server menus and trigger `/queue` or bungee transfers.

## Remediation Workflow

### 1. Velocity Proxy Configuration
- In `/plugins/jpremium/configuration.yml`:
  ```yaml
  limboServerNames: [lobby]
  mainServerNames: [lobby]
  ```
- When configured, JPremium strictly enforces that players with `!user.isLogged()` can NEVER transition out of `lobby` to any backend server.

### 2. Dedicated Lobby Auth Guard Plugin (`NoeAuthGuard`)
- Hook `de.oliver.fancynpcs.api.events.NpcInteractEvent` at `EventPriority.LOWEST`.
- Hook `PlayerInteractEvent`, `PlayerInteractEntityEvent`, `PlayerInteractAtEntityEvent`, `InventoryOpenEvent`, `InventoryClickEvent`, `PlayerDropItemEvent`, and `PlayerSwapHandItemsEvent`.
- Hook `PlayerCommandPreprocessEvent`: enforce strict whitelist (`/login`, `/l`, `/register`, `/reg`, `/r`, `/requestpasswordrecovery`, `/confirmpasswordrecovery`). All other commands (including `/queue`, `/server`, `/help`) are cancelled.

## Key Implementation Pitfalls & Gotchas

1. **Floodgate / Bedrock Players Never Enter Passwords:**
   In crossplay setups, Bedrock players authenticate via Floodgate and never run `/login`. Any custom auth guard must immediately exempt Bedrock players (`player.getName().startsWith(".")` or `FloodgateApi.getInstance().isFloodgatePlayer(uuid)`). Failing to exempt Bedrock players traps them in the lobby with false login prompts.

2. **JPremium Bukkit User Lookup Reflection:**
   Calling `com.jakub.jpremium.a$a.a(player)` merely invokes `new a$a(player.getUniqueId())` — an uninitialized dummy instance where `.b()` (the state enum) is `null`. To read live auth state, reflect into the `Backend` plugin instance field `e` (`private com.jakub.jpremium.a e;`) and query `e.a(uuid).get().b().a()`.

3. **PlaceholderAPI Expansion Unregistration on `/reload`:**
   Running `/reload` on Spigot/Paper unregisters external PlaceholderAPI expansions. If JPremium's expansion is dropped, `%jpremium_state%` evaluates to the unparsed literal string `"%jpremium_state%"`. Never rely exclusively on PlaceholderAPI; always combine with live reflection into JPremium's user map, and re-register `com.jakub.jpremium.c.a(jprem, map)` on guard plugin enable.
