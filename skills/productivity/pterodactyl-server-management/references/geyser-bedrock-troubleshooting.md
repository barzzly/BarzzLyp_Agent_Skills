# Geyser Bedrock connectivity and NetherNet / RakNet troubleshooting

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
  - For deep diagnostic dumps, execute `geyser dump` from console and fetch the generated raw report from `https://dump.geysermc.org/raw/<dump_id>` to inspect `netherNetInfo`, active candidate addresses, bound protocols (`bedrockProtocols`), and `connectionAttempts`.
