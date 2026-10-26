# Simple Voice Chat Proxy Networking & Timeout Diagnostics

Procedures for diagnosing and stabilizing Simple Voice Chat (SVC) in Velocity proxy + Paper/Leaf backend networks hosted on Pterodactyl.

## 1. Architecture & Port Mapping

In a Minecraft proxy environment:
- **Velocity Proxy (`voicechat-velocity`)**:
  - Acts as the public UDP gateway. Clients connect ONLY to the proxy's public IP and UDP port (`voicechat-proxy.properties`: `port` and `voice_host`).
  - Sniffs `voicechat:secret` and `voicechat:request_secret` Minecraft plugin messaging channels.
  - Dynamically creates a per-player UDP bridge (`VoiceProxyBridge`) relaying audio packets to the backend server's internal UDP allocation.
- **Backend Servers (`voicechat-bukkit`)**:
  - Each backend server binds its own distinct UDP allocation (`voicechat-server.properties`: `port=<port>`).
  - When proxy plugin is installed on Velocity, the backend `voice_host` property is ignored for proxy-routed clients.
  - Proxy routes packets based on `[servers]` mapping in `velocity.toml` and sniffed backend port.

## 2. Root Cause: Unexpected Mid-Game Disconnections

### A. Aggressive UDP Timeout (10-Second Threshold)
- In `plugins/voicechat/voicechat-server.properties`, the default is `keep_alive=1000` (1000 ms).
- Simple Voice Chat's internal timeout evaluation is:
  ```java
  if (timestamp - connection.getLastKeepAliveResponse() >= Voicechat.SERVER_CONFIG.keepAlive.get() * 10L) {
      Voicechat.LOGGER.info("Player {} timed out", connection.getPlayerUUID());
  ```
- `keep_alive=1000` yields a **strict 10-second timeout** (`1000ms * 10`).
- Over mobile networks or home fiber with international routing (e.g. Indonesia to Singapore VPS), UDP jitter spikes or brief packet drops >10s are common.
- As soon as 10s passes without a KeepAlive packet, the server forces a disconnect and triggers a session reconnect.

### B. The Mid-Game Reconnect Failure (Stuck "Voice chat disconnected")
- When the backend server detects timeout, it sends a new `SecretPacket` to the client over Minecraft TCP networking.
- Velocity's `VoiceProxySniffer` intercepts the packet and interrupts the active bridge (`disconnectBridge`).
- When the client attempts to re-authenticate with the new secret, Velocity creates a new bridge with a new ephemeral UDP port.
- However, client-side mod threads often retain the previous socket state without a full server switch/rejoin, causing `ConnectionCheckPacket` validation to fail after authentication (`Successfully authenticated` logged, but `Successfully validated connection` never completes).
- **In-game reset commands** (like custom `/resetvoice`) suffer from this exact same failure mechanism. The only client workaround without server-side fixes is reconnecting to the server.

## 3. Stabilization Procedure (Zero-Downtime)

### Step 1: Increase Keep-Alive Tolerance on Backend
Edit `plugins/voicechat/voicechat-server.properties` on each backend server:
```properties
keep_alive=3000
```
- A setting of `3000` increases the timeout threshold to **30 seconds** (`3000ms * 10`), tolerating temporary UDP jitter and packet loss without triggering disconnects.
- This value is transmitted to the client inside `SecretPacket` upon login/switch and controls both client and server timeout loops.

### Step 2: Hot-Reload Proxy Voice Gateway Without Restart
Velocity supports live reloading of the voice proxy server:
1. Dispatch via Velocity console or Pterodactyl API (`POST /api/client/servers/{velocity_id}/command`):
   ```sh
   velocity reload
   ```
2. Velocity fires `ProxyReloadEvent`, triggering `reloadVoiceProxyServer()` in `SimpleVoiceChatVelocity`:
   - It interrupts and flushes stale player bridges.
   - It re-binds and restarts the UDP `VoiceProxyServer` socket cleanly.
   - Zero downtime: players are not kicked from the proxy or backend servers.

### Step 3: Verify Proxy-to-Backend UDP Latency
Test UDP packet transport between Velocity and backend servers directly from the Velocity console:
```sh
voicechatproxy ping <server_name> <voice_chat_port>
```
Example:
```sh
voicechatproxy ping noerp 12000
```
Check `logs/latest.log` on Velocity:
- Expect: `Received response from server '<name>' in 0-1 ms`.
- If packets time out, verify backend port allocation and firewall rules on Pterodactyl.
