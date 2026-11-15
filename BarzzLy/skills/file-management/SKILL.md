---
name: file-management
description: Use when managing or backing up BarzzLy files and Blockbench models. Inspect paths, preserve project originals, exclude private/binary assets, and verify copies.
metadata:
  hermes:
    tags: [files, organization, backup, minecraft, blockbench, models]
    category: productivity
---

# BarzzLy file and model workflow

## File management
- Follow `/home/barzzly/DIRECTORY_RULES.md` as the single source of truth for paths. Keep Minecraft, Blockbench and game-server artifacts under `/home/barzzly/Minecraft/`; do not create work folders directly under home root.
- Inspect existing folders and project context before creating or moving anything. Prefer the smallest change; preserve active workspaces, originals, symlinks and required hidden configuration.
- Before reorganizing a directory, inventory files, check destination collisions, capture SHA-256/modes/symlink targets, and check active process working directories. Move only with a clear mapping; verify destination hashes afterward.
- Keep temporary downloads, test outputs and intermediate exports in the relevant `Minecraft/maintenance/` or project workspace; remove only artifacts owned by the completed task.

## Blockbench/model creation
- Start with a derivative copy; hash and preserve source models/assets. Use the actual Blockbench editor/codecs and export real `.bbmodel` or requested Minecraft format, not placeholder scripts.
- Identify target format and consumer first: Generic/ModelEngine animations are not vanilla Java item animations. Preserve IDs, hierarchy, textures, UVs and animation behavior unless asked to change them.
- Make one targeted improvement at a time. Validate native import/export roundtrip and compare element/group/texture/animation counts and relevant transforms. Render front, side, quarter and thumbnail views; inspect framing, silhouette, texture readability and clipping before calling a model finished.
- Package only requested deliverables. Reopen ZIPs, run CRC checks, compare entry counts, verify embedded texture bytes against external PNGs, and ensure documented paths exist in the archive.
- Separate structural validation, rendered visual review and live Minecraft compatibility. Never claim runtime proof from a valid `.bbmodel` or ZIP alone.

## Automated backup scope
- Back up only reusable workflow/skill documentation: path/file-management procedures and how to create, inspect, verify and package models.
- Keep Minecraft project folders and runtime files separate from skill backup. Do not copy model/project assets, textures, archives, server backups, databases, credentials, private keys, `.env` files, logs or generated binaries into the public skills repository.
- Copy the Blockbench modeling workflow separately to `Minecraft/skills/blockbench-modeling-workshop/`; keep its procedures distinct from ordinary Minecraft asset/project files.
- Redact operational endpoints before public backup; verify `git status`, staged paths and push result. Never commit the user’s projects merely because they live under `Minecraft/` or `BarzzLy/`.
