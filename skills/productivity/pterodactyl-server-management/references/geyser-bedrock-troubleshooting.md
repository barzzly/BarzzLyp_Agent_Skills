# Geyser Bedrock connectivity and NetherNet / RakNet troubleshooting

- **Container Bind Address (`bedrock.address`) & Port Allocation Pitfalls**:
  - `bedrock.address` MUST ALWAYS remain `0.0.0.0` in Pterodactyl and containerized hosting. Setting public server IP causes Docker container socket bind failure or rejection of forwarded packets, rendering the server completely unreachable (`timed out`).
  - `bedrock.port` must strictly match the assigned Pterodactyl container allocation (e.g. 25562), never default `19132` or Java port `25565` unless specifically allocated. Setting an unassigned port causes immediate timeout during client auth handshake, surfacing Bedrock client error modal code **"Terracotta"** (`An error has occurred. Search help.minecraft.net for "Terracotta"`). When a user reports "Terracotta", verify `bedrock.address` is `0.0.0.0` and `bedrock.port` matches container port allocations.

- **Bedrock 1.26.60+ NetherNet Enforcement & Android Cleartext HTTP ("Terracotta")**:
  - In Minecraft Bedrock 1.26.60+, Mojang enforces NetherNet and disables legacy RakNet connection negotiation for updated clients.
  - On mobile operating systems (particularly Android 16+), OS-level `NetworkSecurityConfig` prohibits cleartext HTTP traffic to raw IP addresses. If Geyser uses built-in signaling over plain HTTP (`http://<ip>:<port>`) without TLS certificates, Android clients block the signaling request before WebRTC initialization, throwing error codeword **"Terracotta"** with diagnostic metadata `Google,M,Android,ARM64-Android 16 Error Detail: InitialConnection-...`.
  - Fix: Enable `signaling.mode: hybrid` with external NXS signaling (`endpoint: https://agent.warden.cloud`). This provisions a trusted HTTPS signaling endpoint (e.g. `https://<subdomain>.wdn.gg`). Provide Bedrock 1.26.60+ mobile players with either:
    1. 1-click web launcher URL: `https://<subdomain>.wdn.gg` (auto-triggers `minecraft://connect?serverUrl=...&serverPort=443`).
    2. Manual server entry in Bedrock: Server Address `<subdomain>.wdn.gg`, Port `443`.
  - For gameplay traffic, set `transport: both`, assign `webrtc-port` to a distinct open container UDP allocation (e.g. `18170`), and explicitly specify `advertise-addresses: ['<public_ip>:<webrtc_port>']`. This preserves legacy RakNet UDP connectivity on `<public_ip>:<raknet_port>` for older clients while enabling HTTPS-negotiated NetherNet for 1.26.60+ clients.

- **NetherNet vs. RakNet Port Allocation Requirements**:
  - NetherNet uses WebRTC over UDP for gameplay and requires an HTTP/TCP signaling server (built-in or external NXS) for connection negotiation.
  - When a server is hosted on a Pterodactyl node or shared hosting allocation where the assigned Bedrock port forwards only UDP (or filters incoming TCP on that port), setting `transport: nethernet` makes built-in signaling unreachable (`Connection timed out` from external probes). Bedrock/MCPE clients fail to receive server metadata and display the server as offline.
  - On single-port Bedrock allocations where separate TCP signaling or secondary WebRTC UDP routing is not provisioned, keep `transport: raknet` in `plugins/Geyser-<Platform>/config.yml`. RakNet runs entirely over single-port UDP.
  - If configuring dual support (`transport: both`), assign `webrtc-port` to a distinct, open secondary UDP port. Setting `webrtc-port: 0` or sharing the RakNet port causes binding failure.

- **Zero-Downtime Live Reload Procedure**:
  - Never restart the Minecraft backend or Velocity proxy server to apply Geyser network or configuration edits.
  - Send the console command `geyser reload`. Geyser gracefully disconnects any active Bedrock sessions, shuts down its network listener threads, re-reads `config.yml`, and re-binds the socket within 2–3 seconds while keeping all Java players connected and preserving server uptime.

- **Non-Destructive Remote Connectivity Verification**:
  - Test external reachability from console using `geyser connectiontest <public_ip> <bedrock_port>`. Syntax strictly requires space separation between IP and port; passing `<ip>:<port>` causes Geyser to parse the string as an invalid IPv6 literal and report false failure.
  - Confirm success in `/logs/latest.log` with `Your server is likely online and working as of 0 seconds ago!`. If the test returns `Connection timed out` under `nethernet`, check whether the hosting environment permits incoming TCP on the Bedrock port before reverting to `raknet`.
  - Verify UDP reachability directly via raw RakNet Unconnected Ping (`0x01` + timestamp + offline magic `\x00\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x124Vx` + GUID) to `<public_ip>:<bedrock_port>`. An incoming RakNet Pong (`0x1c` containing `MCPE;...`) proves the UDP listener is active and answering externally without relying on in-game client state.
  - For deep diagnostic dumps, execute `geyser dump` from console and fetch the generated raw report from `https://dump.geysermc.org/raw/<dump_id>` to inspect `netherNetInfo`, active candidate addresses, bound protocols (`bedrockProtocols`), and `connectionAttempts`.
