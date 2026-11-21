---
name: pterodactyl-cross-node-database
description: "Use when Pterodactyl servers connect to remote MariaDB."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [pterodactyl, docker, mariadb, firewall, networking, cross-node]
---

# Pterodactyl Cross-Node Database Networking

Use when Minecraft/Pterodactyl servers on one node connect to MariaDB hosted in a Pterodactyl database container on another node.

## Always-on rules

- Confirm database container port before changing firewall: public `host_port` and container `listen_port` are separate values.
- Prefer one explicit mapping: `DB_PUBLIC_IP:19160 -> MariaDB_CONTAINER:3306`; do not make MariaDB listen on the public port merely to hide a mapping mistake.
- Restrict Docker-published database ports in `DOCKER-USER`, not only UFW, because Docker NAT can bypass UFW filtering.
- Whitelist confirmed node egress IPs only; never infer egress from a server allocation or proxy/backend IP.
- Allow TCP `19160` on database host only when mapping targets container port `3306`; do not expose container port `3306` directly to the Internet.
- Read back Docker port mapping, MariaDB listen socket, `DOCKER-USER` rules, and Pterodactyl allocation before changing application configs.
- Test from each real source node with `nc -vz DB_PUBLIC_IP 19160`, then test application authentication with the actual database/user; an open TCP port does not prove SQL access.
- Preserve database credentials; redact them from commands, logs, and reports.

## Procedure

1. **Inventory both ends**
   - Record database server public IP, Pterodactyl database server ID, host allocation port, container MariaDB port, and source server IDs.
   - Record each source node's public egress IP from that node itself, using `curl -4 https://api.ipify.org` or the provider's node-level network check. Do not use a backend allocation as a substitute.

2. **Validate port mapping**
   - On the database node, inspect the container's published ports and network:
     ```bash
     docker ps --format '{{.Names}} {{.Ports}}'
     docker inspect <db-container> --format '{{json .NetworkSettings.Ports}}'
     ```
   - Inside the MariaDB container, verify the actual listener:
     ```bash
     ss -lntp
     mariadb-admin ping -h 127.0.0.1 -P 3306
     ```
   - Expected shape:
     ```text
     103.42.116.72:19160 -> container:3306
     ```

3. **Apply narrow firewall rules**
   - Add `DOCKER-USER` rules before broad accepts, allowing only confirmed egress IPs to TCP 19160 and dropping other sources to that published port:
     ```bash
     iptables -I DOCKER-USER 1 -p tcp -s 185.207.166.85 -d 103.42.116.72 --dport 19160 -j ACCEPT
     iptables -I DOCKER-USER 2 -p tcp -s 185.207.166.76 -d 103.42.116.72 --dport 19160 -j ACCEPT
     iptables -I DOCKER-USER 3 -p tcp -d 103.42.116.72 --dport 19160 -j DROP
     ```
   - Persist rules using the host's firewall persistence mechanism. Verify ordering and counters after a test connection.
   - Keep UFW/firewall rules consistent, but do not treat UFW alone as sufficient for Docker-published ports.

4. **Test source-to-database path**
   - From each source node/container:
     ```bash
     nc -vz -w 5 103.42.116.72 19160
     mysql --protocol=tcp -h 103.42.116.72 -P 19160 -u '<user>' -p'<redacted>' -e 'SELECT 1' '<database>'
     ```
   - Use the same host/port/user/database in plugin configs only after this test passes.

5. **Verify application state**
   - Restart one named application at a time.
   - Read logs for a successful Hikari/MySQL connection and absence of `Communications link failure`, `Connection refused`, or `Connect timed out`.
   - Read back server status and database connection after restart.

## Decision table

| Observation | Meaning | Action |
|---|---|---|
| Host port 19160 maps to container 19160, MariaDB listens on 3306 | Mapping is wrong | Change mapping to host 19160 -> container 3306, then recreate/restart database container if required |
| Host `nc` works, source-node `nc` times out | Routing/firewall/egress problem | Confirm source egress and inspect DOCKER-USER/provider firewall |
| Source `nc` works, SQL login fails | User/database/grant problem | Fix MariaDB grants or credentials; do not widen firewall |
| SQL login works, plugin still fails | Plugin config or startup state problem | Inspect exact plugin config and restart only that server |
| Public port open from unrelated source | Whitelist missing or ordered incorrectly | Insert DOCKER-USER drop/allow rules and verify counters |

## Pitfalls

- Do not whitelist `185.207.166.85` or `185.207.166.76` merely because they appear as game-server allocations; they are valid source IPs only after egress testing confirms them.
- Do not allow `3306` publicly when MariaDB is containerized; the published host port is the controlled boundary.
- Do not change every plugin to a new endpoint before proving the network path; otherwise config edits obscure whether the failure is routing, mapping, grants, or credentials.
- Do not report firewall work as complete from a successful rule command; verify with source-node TCP and SQL probes plus application logs.
- Do not expose full command output when it contains passwords; use redacted config excerpts and boolean connection results.
