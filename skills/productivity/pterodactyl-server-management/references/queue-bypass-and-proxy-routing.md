# Proxy Queue Bypass and Direct Server Routing

When bypassing queueing plugins (like ajQueue) for specific backend servers (such as `noerp` or event servers) without restarting proxies or lobbies:

## 1. DeluxeHub Server Selector Menus
- File: `plugins/DeluxeHub/menus/serverselector.yml`
- Action: Replace `[COMMAND] queue <server>` with `[PROXY] <server>`.
  - DeluxeHub's `[PROXY]` action (and legacy `[BUNGEE]`) dispatches a native BungeeCord `ConnectOther` plugin message to transfer the clicking player directly to the target server.
- Hot-reload command: `deluxehub reload` (loads updated menu YAML in milliseconds).

## 2. FancyNpcs Server Selectors
- File: `plugins/FancyNpcs/npcs.yml`
- Action: In the target NPC's `actions.ANY_CLICK`, replace `action: player_command` / `value: queue <server>` with:
  ```yaml
  action: send_to_server
  value: <server>
  ```
  - `SendToServerAction` uses BungeeCord `Connect` plugin messaging natively, avoiding console queue command spam.
- Hot-reload command: `fancynpcs reload`.

## 3. Velocity ajQueue Configuration
- File: `plugins/ajqueue/config.yml` on Velocity proxy.
- Action: Add the target backend server to the `send-instantly` list:
  ```yaml
  send-instantly:
    - "lobbys"
    - "noerpg"
    - "<server>"
  ```
  - This ensures any player who types `/queue <server>` or `/server <server>` is sent instantly without entering a wait queue.
- Hot-reload command: `ajqueue reload` on Velocity proxy console.
