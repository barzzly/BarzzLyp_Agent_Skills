---
name: web-preview-tunneling
description: Use when sharing a local web app or testing on mobile.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [tunnel, cloudflared, mobile, preview, web, responsive, cdp]
    category: web
---

# Web Preview Tunneling & Mobile Verification

Expose local web servers running on headless environments or remote servers to public HTTPS URLs for testing on physical mobile devices, and verify mobile responsive layout autonomously before sharing.

## Quick Start

```bash
# 1. Ensure standalone cloudflared binary is available
curl -fsSL https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -o ~/.local/bin/cloudflared && chmod +x ~/.local/bin/cloudflared

# 2. Launch background quick tunnel (no account or login required)
# Pattern: cloudflared tunnel --url http://127.0.0.1:<PORT>
```

Read stdout for the generated `https://<subdomain>.trycloudflare.com` URL.

## Workflow

### Step 1: Start Local Server & Verify Endpoint

1. Verify the web application is built or running locally (e.g. `dist/` directory via `python3 -m http.server <PORT>` or Vite dev server).
2. Confirm health locally first with `curl -I http://127.0.0.1:<PORT>` before exposing publicly.

### Step 2: Establish Quick Public Tunnel

1. Prefer `cloudflared` quick tunnels over npm-based tunnel packages (`untun`, `localtunnel`) — standalone binary requires zero runtime dependencies and avoids node ESM packaging errors or interstitial visitor verification pages.
2. Avoid raw SSH reverse tunnels (`localhost.run`, `serveo.net`) in background commands; they may hang waiting for interactive SSH host key approval or terminal allocation.
3. Start the tunnel in the background with watch pattern `notify=['trycloudflare.com']`.
4. Inspect process logs via `process_manage(action='log', session_id=...)` once connected to extract the public HTTPS URL.

### Step 3: Headless Mobile Viewport Verification

Before handing the URL to the user, verify mobile layout via Chrome DevTools Protocol (CDP):

1. Set viewport to standard mobile dimensions (375x812, device scale factor 2):
   ```python
   cdp('Emulation.setDeviceMetricsOverride', width=375, height=812, deviceScaleFactor=2, mobile=True)
   goto_url('http://127.0.0.1:<PORT>')
   wait_for_load()
   shot = capture_screenshot()
   ```
2. Analyze the capture with `vision_analyze` checking for mobile layout pitfalls:
   - **Stacked Action Buttons:** Call-to-action buttons must stack vertically full-width (`flex-col sm:flex-row w-full sm:w-auto`) on viewports < 480px; horizontal rows cramp text and cause tap collisions.
   - **Touch Target Padding:** Interactive controls (hamburger toggle, buttons, icon links) must meet the minimum 44x44px tap target (`w-11 h-11`). Icons and buttons in stacked footers should have explicit padding hitboxes rather than bare SVG glyphs.
   - **Pill & Badge Wrapping:** Status badges must allow flexible text wrapping or scale down (`text-[11px] sm:text-xs`) to prevent orphan words or container overflow on 360–390px screens.

### Step 4: Teardown & Security Invariant

Temporary tunnels expose internal ports to the public internet without an authentication layer.

1. Keep track of background process IDs.
2. When the user signals testing is finished ("matiin tunnel", "stop preview", or task completion):
   - Terminate running background tasks via `process_manage(action='kill', session_id=...)`.
   - Terminate any temporary local HTTP preview server.
   - Run fallback cleanup `pkill -f cloudflared 2>/dev/null` and confirm with `ps aux | grep -E 'cloudflared|<PORT>'` to guarantee no orphaned tunnels remain.
