# Backup scope

## Public reusable procedures

Allow:

- Skill Markdown describing file organization, backup boundaries, Blockbench import/export, model validation, packaging and verification.
- Sanitized scripts that operate on those procedures without embedded credentials or private endpoints.
- Small manifests or documentation that contain no private runtime state.

## Exclude by default

Exclude:

- Minecraft projects, server worlds, plugin data, player data, databases and server backups.
- `.bbmodel` assets, textures, resource-pack ZIPs, JARs, generated binaries and media.
- `.env` files, API keys, access tokens, passwords, SSH keys, OAuth files and private endpoints.
- Runtime logs, caches, temporary downloads and session transcripts.

## Verification

- Run a dry-run first and report file counts.
- Inspect staged paths before commit; reject paths outside the intended skill/workflow scope.
- Scan text for credential-like values and redact known operational endpoints.
- Confirm local commit exists separately from remote push.
- If push fails, report local-only state and never claim GitHub backup completed.
