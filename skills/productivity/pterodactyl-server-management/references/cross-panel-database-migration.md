# Cross-panel database and endpoint migration

Use this workflow when moving named Pterodactyl servers between panels or nodes.

1. Read panel URLs from integration env. Do not guess hostnames. Validate Client API tokens with `/api/client/account` and `/api/client`; if a Python request intermittently returns 403, retry with `curl`, `Accept: application/vnd.pterodactyl.v1+json`, and a normal User-Agent before declaring access invalid.
2. Inventory only explicitly named servers. Similar names do not expand scope: bot, HC, event, and unrelated servers stay untouched unless named.
3. Inspect target allocations and server files before edits. Search text configs for old IPs/domains, but exclude jars, databases, generated assets, logs, and backup copies.
4. Inspect the database container first: Docker network membership, container DNS name, internal listening port, exposed host ports, database names, and usable credentials. When servers share `pterodactyl_nw`, prefer database-container DNS plus internal MariaDB port; host allocation ports are not automatically database ports.
5. Never replace every `localhost` mechanically. Some values are intentional local settings, comments, templates, or unrelated plugin sections. Change only verified database connection fields.
6. Back up each file immediately before editing, using a topical suffix such as `.before-db-fix`; never expose passwords or tokens in output.
7. Match runtime to egg: Velocity uses Velocity, Paper uses Paper, and Node.js bots use Node.js. Keep completion words scoped to the matching egg/server; do not alter global egg settings to fix one server.
8. Validate endpoint values and old-endpoint absence. Restart one named server at a time, preserve prior power state unless migration requires a stop, and verify logs for actual database connection success. Config inspection alone does not prove connectivity.
9. Read back allocation descriptions and server state after writes. HTTP 204 or a successful write call alone is not proof.

Common checks:

```bash
curl -sS -H 'Authorization: Bearer …' \
  -H 'Accept: Application/vnd.pterodactyl.v1+json' \
  https://panel.example/api/client/account

sudo docker inspect <db-container>
sudo docker exec <db-container> ss -lntp
sudo docker logs --tail 100 <db-container>
```
