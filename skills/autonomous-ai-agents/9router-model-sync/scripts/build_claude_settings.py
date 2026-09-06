#!/usr/bin/env python3
"""Verify each provider-registered model on 9Router actually answers, then write
~/.claude/settings.json with only the working ones.

Model list = what is REGISTERED in the dashboard provider cards (not the ~500
pass-through IDs advertised by /v1/models). Refresh REGISTERED by visiting
/dashboard/providers and reading each provider's "Available Models" section.
"""
import concurrent.futures as cf
import json
import os
import shutil
import subprocess
import time

BASE = os.environ.get("HERMES_CUSTOM_AIROUTER_BASE_URL", "http://127.0.0.1:20128/v1") + "/chat/completions"
KEY = os.environ["HERMES_CUSTOM_AIROUTER_BARZZLY_COM_API_KEY"]
SETTINGS = os.path.expanduser("~/.claude/settings.json")
BACKUP_DIR = os.path.expanduser("~/.claude/backups")

# Registered per provider card in dashboard -> /dashboard/providers
REGISTERED = {
    "GripRouter": ["Grip/gpt-5.6-luna"],
    "OnList": [
        "OnList/openai/gpt-5.6-sol",
        "OnList/openai/gpt-5.6-terra",
        "OnList/openai/gpt-5.6-luna",
        "OnList/anthropic/claude-sonnet-5",
    ],
    "XKiro Free": [
        "XKiro/deepseek/deepseek-v4-pro",
        "XKiro/deepseek/deepseek-v4-flash",
    ],
    "JustDoWork Free": [
        "JustDoWork/claude-opus-5-thinking",
        "JustDoWork/claude-opus-4-8-thinking",
    ],
    # Antigravity: gemini-3.5-* and gemini-3-flash-agent excluded - upstream
    # returns "Gemini 3.5 Flash is no longer available" (HTTP 200 w/ error text).
    "Antigravity": [
        "ag/gemini-3.8-flash-high", "ag/gemini-3.8-flash-medium",
        "ag/gemini-3.8-flash-low", "ag/gemini-3.8-flash",
        "ag/gemini-3.7-flash-high", "ag/gemini-3.7-flash-medium",
        "ag/gemini-3.7-flash-low", "ag/gemini-3.6-flash-high",
        "ag/gemini-3.6-flash-medium", "ag/gemini-3.6-flash-low",
        "ag/gemini-3-flash", "ag/gemini-pro-agent",
        "ag/gemini-3.1-pro-low", "ag/claude-sonnet-4-6",
        "ag/claude-opus-4-6-thinking", "ag/gpt-oss-120b-medium",
    ],
    # OpenCode Free omitted: 0 connections, every call returns empty content.
}

# Capability tier for Claude Code's behavesAs mapping.
OPUS, SONNET, HAIKU = "claude-opus-5", "claude-sonnet-5", "claude-haiku-4-5-20251001"
TIER = {
    "Grip/gpt-5.6-luna": OPUS,
    "OnList/openai/gpt-5.6-sol": OPUS,
    "OnList/openai/gpt-5.6-terra": OPUS,
    "OnList/openai/gpt-5.6-luna": OPUS,
    "OnList/anthropic/claude-sonnet-5": SONNET,
    "XKiro/deepseek/deepseek-v4-pro": OPUS,
    "XKiro/deepseek/deepseek-v4-flash": SONNET,
    "JustDoWork/claude-opus-5-thinking": OPUS,
    "JustDoWork/claude-opus-4-8-thinking": OPUS,
    "ag/gemini-3.8-flash-high": OPUS,
    "ag/gemini-3.8-flash-medium": SONNET,
    "ag/gemini-3.8-flash-low": HAIKU,
    "ag/gemini-3.8-flash": SONNET,
    "ag/gemini-3.7-flash-high": OPUS,
    "ag/gemini-3.7-flash-medium": SONNET,
    "ag/gemini-3.7-flash-low": HAIKU,
    "ag/gemini-3.6-flash-high": OPUS,
    "ag/gemini-3.6-flash-medium": SONNET,
    "ag/gemini-3.6-flash-low": HAIKU,
    "ag/gemini-3-flash": SONNET,
    "ag/gemini-pro-agent": OPUS,
    "ag/gemini-3.1-pro-low": HAIKU,
    "ag/claude-sonnet-4-6": SONNET,
    "ag/claude-opus-4-6-thinking": OPUS,
    "ag/gpt-oss-120b-medium": SONNET,
}

# Upstream can return HTTP 200 with an error sentence as the content. Treat as fail.
DEAD_MARKERS = ("no longer available", "not available", "deprecated")


def probe(model: str):
    """Return (model, ok, detail). Budget must be generous: reasoning models
    spend the whole allowance on thinking tokens and look 'empty' otherwise."""
    payload = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": "What is 2+2? Answer with the number only."}],
        "max_tokens": 4096,
        "stream": False,
    })
    try:
        r = subprocess.run(
            ["curl", "-s", "--max-time", "180", "-X", "POST", BASE,
             "-H", f"Authorization: Bearer {KEY}",
             "-H", "Content-Type: application/json",
             "-d", payload],
            capture_output=True, text=True, timeout=200,
        )
    except subprocess.TimeoutExpired:
        return model, False, "timeout"
    body = r.stdout.strip()
    if not body:
        return model, False, "empty response"
    if body.startswith("data:"):
        return model, True, "stream ok"
    try:
        d = json.loads(body)
    except json.JSONDecodeError:
        return model, False, f"unparseable: {body[:90]}"
    if "error" in d:
        return model, False, str(d["error"].get("message", d["error"]))[:110]
    try:
        ch = d["choices"][0]
        content = (ch["message"].get("content") or "").strip()
        reason = ch.get("finish_reason")
    except (KeyError, IndexError):
        return model, False, f"odd shape: {body[:90]}"
    if any(m in content.lower() for m in DEAD_MARKERS):
        return model, False, f"dead upstream: {content[:60]}"
    if not content:
        return model, False, f"no content (finish={reason})"
    return model, True, f"{content[:30]} (finish={reason})"


all_models = [m for lst in REGISTERED.values() for m in lst]
print(f"probing {len(all_models)} registered models...\n")

results = {}
with cf.ThreadPoolExecutor(max_workers=6) as ex:
    for model, ok, detail in ex.map(probe, all_models):
        results[model] = (ok, detail)

working, broken = [], []
for prov, lst in REGISTERED.items():
    print(f"[{prov}]")
    for m in lst:
        ok, detail = results[m]
        print(f"  {'PASS' if ok else 'FAIL'}  {m:42} {detail}")
        (working if ok else broken).append(m)
    print()

# --- write settings -------------------------------------------------------
with open(SETTINGS) as f:
    cfg = json.load(f)
os.makedirs(BACKUP_DIR, exist_ok=True)
shutil.copy2(SETTINGS, os.path.join(BACKUP_DIR, f"settings.json.{int(time.time())}.bak"))

cfg["availableModels"] = working
cfg["modelPicker"] = {
    "options": [{"model": m, "behavesAs": TIER[m]} for m in working],
    "replaceBuiltInOptions": True,
}
if cfg.get("model") not in working and working:
    cfg["model"] = working[0]

with open(SETTINGS, "w") as f:
    json.dump(cfg, f, indent=2)
    f.write("\n")

# sanitized copy for sharing over chat - never send the live token
share = json.loads(json.dumps(cfg))
share["env"]["ANTHROPIC_AUTH_TOKEN"] = "<REDACTED - kept in local ~/.claude/settings.json>"
share_path = os.path.expanduser("~/claude-settings-shared.json")
with open(share_path, "w") as f:
    json.dump(share, f, indent=2)
    f.write("\n")

print(f"working: {len(working)}   broken: {len(broken)}")
if broken:
    print("excluded:", ", ".join(broken))
print(f"default model: {cfg['model']}")
print(f"share file: {share_path}")

assert len(cfg["availableModels"]) == len(cfg["modelPicker"]["options"])
assert all(o["behavesAs"] in (OPUS, SONNET, HAIKU) for o in cfg["modelPicker"]["options"])
assert cfg["env"]["ANTHROPIC_AUTH_TOKEN"].startswith("sk-")
print("checks: OK")
