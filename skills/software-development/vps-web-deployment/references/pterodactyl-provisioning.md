# Pterodactyl Panel and Wings provisioning

## Same-host IPv4 renumbering

- Stage the confirmed new address alongside the old one. Use a free source-policy table and rule for the new gateway; verify source-bound public egress, then test inbound SSH independently before retiring the old address/default route. Local HTTPS and a wildcard SSH listener do not prove remote reachability. Validate merged Netplan with `netplan generate`; do not start stopped workloads to test a network change.
- For in-place allocation changes, preserve node, allocation IDs, ports and server assignments. Snapshot the scoped rows, check for destination collisions, update transactionally and compare the exact mapping before commit.

## Choose addressing before installation

1. Distinguish the Panel URL, Wings API endpoint, and game allocations. Players can connect to an IPv4 allocation even when Wings uses a DNS hostname; do not remove Wings TLS to satisfy an IPv4 game-address request.
2. For an HTTPS Panel, provide a browser-trusted HTTPS Wings endpoint: browsers connect directly for console WebSockets and block insecure HTTP as mixed content. A raw IP endpoint needs a trusted certificate covering that IP and a working renewal method; do not claim IP certificates are impossible or suggest self-signed certificates as an equivalent replacement.
3. For the simple direct-TLS setup, create a node hostname A record pointing to the node IP, keep it DNS only, select Use SSL Connection and Not Behind Proxy, and use daemon TCP 8080 plus SFTP TCP 2022. SFTP is separate from host SSH; do not reuse port 22. Do not switch Behind Proxy on merely because the Panel itself uses Cloudflare.
4. Inspect `free -m`, `df -m /var/lib`, and `ss -ltnp` before choosing node limits and ports. Set memory/disk in MiB, leave headroom for OS, Panel, Docker images and logs, and use over-allocation 0 unless deliberately requested. Do not copy another VPS's capacity values.

## Install and bootstrap configuration

1. If using the community installer, verify its current README at https://github.com/pterodactyl-installer/pterodactyl-installer and identify it as unofficial. Run from a root shell, not `sudo bash <(...)` with ambiguous shell privilege handling. The documented entrypoint is `bash <(curl -fsSL https://pterodactyl-installer.se)`; choose Panel or Wings as needed. DNS verification and certificate issuance are prerequisites, not proof Wings is configured.
2. Create the node in Panel Admin > Nodes. Match FQDN, TLS mode, daemon and SFTP ports to the intended endpoint. Anonymous telemetry is optional; explain the choice without treating consent as required.
3. Open the node's Configuration tab and Generate Token. Run the complete generated configure command on the node; use the actual node ID and Panel URL, never guess them. Keep the token out of chat and durable notes.
4. Alternatively, save the exact node YAML from Panel into `/etc/pterodactyl/config.yml` after `mkdir -p /etc/pterodactyl`; set `chmod 600 /etc/pterodactyl/config.yml`. Preserve token fields and certificate paths without printing their contents.
5. Confirm the config exists before running Wings: `test -s /etc/pterodactyl/config.yml`. Installation alone does not create node credentials. A missing configuration error calls for bootstrap above, not reinstalling Wings or inventing a YAML token.

## Test foreground, then hand off to systemd

1. On a new node with no active Wings service, run `wings --debug`. Loading config, fetching server configs from Panel, then HTTPS and SFTP listeners without a fatal error indicate foreground startup. `total_configs=0` is normal before any game server is created.
2. Explain before launching that Wings remains in foreground: an idle-looking terminal is normal, and typed `clear` is not a shell command while Wings owns the terminal. Press Ctrl+C once after a successful check to return to the shell.
3. Run `systemctl enable --now wings`, then `systemctl status wings --no-pager`. Verify `systemctl is-active wings` and `systemctl is-enabled wings`; foreground logs do not prove service persistence. Do not start a second debug instance over a running service because it competes for ports.
4. Verify HTTPS certificate/endpoint reachability and the Panel's node connection separately. An unauthenticated Wings HTTP 401 may prove TLS/API reachability but does not prove authenticated Panel access. If needed inspect `journalctl -u wings -n 100 --no-pager`, redacting secrets.
5. Permit the chosen API and SFTP TCP ports through applicable host/provider firewalls without resetting existing rules. Keep direct-TLS node DNS only; Cloudflare proxying requires a separate supported-port/TLS plan and does not proxy normal SFTP.
6. Add game allocations under Node > Allocation using the actual interface IP (private interface IP behind NAT, with provider forwarding as needed) and requested game ports. Do not use loopback for player-facing allocations. Add protocol-specific firewall access separately.

## Credential handling

- If a generated `ptla_...` application/auto-deploy token is pasted into chat, treat it as exposed and revoke that exact credential in Panel after bootstrap. Do not repeat or store it.
- Distinguish the bootstrap/application token from node authentication stored in `config.yml`; revoking the former does not justify resetting the latter. If node credentials themselves are exposed, rotate them deliberately and synchronize Wings configuration.
- Do not claim revocation, service startup, or Panel connectivity succeeded without observing the corresponding result. Report user-supplied foreground output as foreground evidence only.
