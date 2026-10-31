# Temporary Event Multipliers & Economy Boosts

Procedures for granting temporary server-wide experience and economy sell multipliers via LuckPerms without restarting servers.

## 1. Standard Boost Multipliers

When configuring periodic or weekend event multipliers across Noesantara networks:
- **AuraSkills XP Boost (+50%)**: Permission node `auraskills.multiplier.50`
- **ShopGUIPlus Sell Boost (1.5x / +50%)**: Permission node `shopguiplus.pricemodifiers.farming_event_50`

Both permissions should be granted to the baseline group (`default`) scoped to the target server context (`server=noerpg`).

## 2. Dispatching Live Multiplier Commands

Dispatch temporary permission commands via console or Pterodactyl Client API (`POST /api/client/servers/{server_id}/command`):

```sh
# Set AuraSkills multiplier
lp group default permission settemp auraskills.multiplier.50 true <duration> server=noerpg

# Set ShopGUIPlus sell multiplier
lp group default permission settemp shopguiplus.pricemodifiers.farming_event_50 true <duration> server=noerpg
```

### Duration Calculation
Compute the duration from the current target timezone (`Asia/Jakarta` / WIB) to the specified end time (e.g., `10:00 AM WIB` the following day):
- Example: If dispatched at 17:50 WIB to expire at 10:00 WIB next day, duration is `16h10m`.
- LuckPerms parses standard time notation: `<N>h<M>m` or `<N>d`.

## 3. Multi-Server Synchronization & Database Verification

- Because LuckPerms uses SQL messaging (`messaging-service: sql`), commands dispatched on Velocity or backend servers propagate to all connected servers in the network automatically.
- To verify active temporary permissions and exact expiration timestamps directly from the database:
  ```sql
  SELECT name, permission, value, server, contexts, FROM_UNIXTIME(expiry) AS expires_at 
  FROM luckperms_group_permissions 
  WHERE permission LIKE '%multiplier%' OR permission LIKE '%farming_event%';
  ```

## 4. Zero-Restart Lifecycle
LuckPerms automatically evicts expired temporary permission nodes at runtime when the timer elapses. Do not schedule server restarts to remove event boosts; permission removal is completely zero-downtime.
