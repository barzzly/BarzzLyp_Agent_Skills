# Simple Voice Chat Tuning and Proxy Diagnostics

## Architecture Overview
In a multi-server Minecraft network with Velocity and Paper/Leaf backends:
- **Velocity Proxy**: Runs `voicechat-velocity-<ver>.jar` (`plugins/voicechat/voicechat-proxy.properties`). Listens on a single public UDP port (e.g., `12002`). Sniffs secret exchange packets on Minecraft plugin messaging channels (`voicechat:secret`, `voicechat:request_secret`) and maintains an ephemeral `VoiceProxyBridge` per player forwarding UDP packets to the backend server.
- **Backend Server**: Runs `voicechat-bukkit-<ver>.jar` (`plugins/voicechat/voicechat-server.properties`). Listens on an allocated UDP port (e.g., `12000`). Manages voice distance, groups, voice chat state, and client secret generation.

## Root Causes of Spontaneous Disconnections

### 1. Aggressive Keepalive Timeout (10 Seconds)
- In `voicechat-server.properties`, `keep_alive=1000` (1000 ms).
- Timeout duration is hardcoded as `timeout = keepAlive * 10L = 10,000 ms (10 seconds)`.
- Over international routes or mobile data (e.g., Indonesia to Singapore), UDP route jitter and brief packet loss bursts exceeding 10 seconds trigger `Player <uuid> timed out`.

### 2. Broken Mid-Session In-Place Reconnect
- When the backend server declares a timeout, it sends a new `SecretPacket` via plugin messaging to force a reconnect.
- Velocity's `VoiceProxySniffer` catches the secret and closes the active `VoiceProxyBridge`.
- When the client mod attempts re-authentication, Velocity assigns a new ephemeral UDP port for the bridge.
- The client mod frequently fails to cleanly close its initial UDP socket thread mid-session without a server disconnect/relog. As a result, authentication succeeds (`Successfully authenticated player`), but the follow-up connection check (`ConnectionCheckPacket`) fails validation, leaving the player permanently stuck in a "Voice chat disconnected" state. In-game commands like `/resetvoice` fail for this exact reason.

## Proven Remedies & Zero-Restart Maintenance

### 1. Increase Keepalive Buffer
- Raise `keep_alive` in `plugins/voicechat/voicechat-server.properties` from `1000` to `3000` (or `4000`).
- This increases timeout tolerance to 30–40 seconds, preventing 99% of transient UDP drops from triggering an accidental disconnect.

### 2. Hot-Reloading Voice Proxy on Velocity (Zero Downtime)
- Never restart Velocity or backend servers solely to refresh voice proxy state.
- Issue `velocity reload` from the Velocity console.
- SimpleVoiceChat catches `ProxyReloadEvent` and invokes `reloadVoiceProxyServer()`, tearing down and rebinding the UDP proxy server and flushing all bridge states cleanly in-memory.

### 3. Connection Verification via Console
- Verify Velocity-to-backend UDP routing directly from Velocity console:
  ```text
  voicechatproxy ping <server_name> <backend_voice_port>
  ```
  Example:
  ```text
  voicechatproxy ping noerp 12000
  ```
- Confirms packet delivery, round-trip latency, and firewall/NAT status without needing player testing.
