# Multi-Panel Operations & Node Egg Management

## 1. Multi-Panel Routing
When operating environments feature multiple Pterodactyl panels (e.g. external hosting vs self-hosted console):
- Store discrete profiles in `~/.config/pterodactyl.env` with distinct URL/key pairs.
- Resolve the target panel URL and token before issuing Client API requests.
- Never assume an identifier from one panel exists on another.

## 2. Headless SSH Key Registration
Register agent SFTP access directly via the Client API rather than requesting manual dashboard input:
- Endpoint: `POST /api/client/account/ssh-keys`
- Payload: `{"name": "<key-identifier>", "public_key": "<ssh-public-key-string>"}`
- Requires standard client bearer token authorization.

## 3. Node.js Egg Startup Wildcard Traps
Standard Pterodactyl Node yolks often contain startup patterns like:
```bash
if [[ "${MAIN_FILE}" == *.js ]]; then /usr/local/bin/node "/home/container/${MAIN_FILE}" ${NODE_ARGS}; fi
```
When `eval` runs in `/entrypoint.sh` inside `/home/container`, an unquoted `*.js` glob expands to all `.js` files present in the root directory, causing `eval: syntax error in conditional expression near '...'`.

### Fix:
Simplify the server or egg startup command in the panel/DB to direct execution:
```bash
if [ -f /home/container/package.json ]; then /usr/local/bin/npm install; fi; /usr/local/bin/node /home/container/{{MAIN_FILE}} {{NODE_ARGS}}
```
