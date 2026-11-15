---
name: file-model-backup
description: Use when backing up Minecraft files or Blockbench workflows.
metadata:
  hermes:
    tags: [files, backup, minecraft, blockbench, models]
    category: productivity
---

# File and model backup

Use this class skill when a task combines filesystem organization, Minecraft/Blockbench work, or backup of reusable agent procedures.

## Procedure

1. Resolve scope before copying. Separate reusable workflow documentation from project files, model assets, textures, archives, server backups, databases, logs, credentials and generated binaries.
2. Follow the user's directory rules. Keep Minecraft and Blockbench work under `~/Minecraft/`; do not create loose backup folders in home root. Preserve active workspaces, originals, symlinks and required hidden configuration.
3. Inspect source paths and destination collisions. For moves, capture hashes, modes and symlink targets before changing paths; check active process working directories. For backups, copy only approved text/procedure files.
4. Redact operational endpoints before public backup. Exclude `.env`, tokens, passwords, private keys, databases, logs, archives and binary assets unless the user explicitly requests a private, non-public backup.
5. Keep Minecraft workflow knowledge separate from Minecraft assets. Store file-management procedures and Blockbench/modeling procedures as separate skills or topical references; never copy a whole project tree merely because it contains useful instructions.
6. Run a dry-run/count check before writing. Then copy, inspect staged paths, and verify the resulting files are readable and contain no accidental secrets. Keep source artifacts unchanged.
7. Commit locally only after checking the staged scope. Push to the configured remote and distinguish local commit success from remote push success; report the exact boundary when authentication or transport blocks push.
8. Leave a runnable backup script or command path for recurring jobs. Schedule recurring backups only after the script handles absent optional folders, skips unsafe file classes, and reports push failures without claiming remote success.

## Standing preferences

- Prefer concise Indonesian reports for this user's operational work.
- Preserve user-supplied filenames, IDs, paths and commands exactly.
- Do not deploy, publish or overwrite Minecraft assets during a documentation-backup task.
- For Blockbench work, preserve source models and distinguish editable `.bbmodel`, Java item JSON, textures and runtime compatibility evidence.

See `references/backup-scope.md` for the public-backup allowlist and verification checklist.
