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
1. **Velocity Proxy Configuration:**
   - In `/plugins/jpremium/configuration.yml`:
     ```yaml
     limboServerNames: [lobby]
     mainServerNames: [lobby]
     ```
   - When configured, JPremium strictly enforces that players with `!user.isLogged()` can NEVER transition out of `lobby` to any backend server.

2. **Dedicated Lobby Auth Guard Plugin (`NoeAuthGuard`):**
   - Hook `de.oliver.fancynpcs.api.events.NpcInteractEvent` at `EventPriority.LOWEST`:
     Check authentication via JPremium state (`com.jakub.jpremium.a.a.a(player).b().a()`) or `%jpremium_state%` (`PREMIUM` or `LOGGED`).
     If unauthorized, `event.setCancelled(true)` and send warning message + alert sound.
   - Hook `PlayerInteractEvent`, `PlayerInteractEntityEvent`, `PlayerInteractAtEntityEvent`, `InventoryOpenEvent`, `InventoryClickEvent`, `PlayerDropItemEvent`, and `PlayerSwapHandItemsEvent`:
     Cancel all interactions for players who are not authenticated.
   - Hook `PlayerCommandPreprocessEvent`:
     Enforce strict whitelist: `/login`, `/l`, `/register`, `/reg`, `/r`, `/requestpasswordrecovery`, `/confirmpasswordrecovery`. All other commands (including `/queue`, `/server`, `/help`) are cancelled.
