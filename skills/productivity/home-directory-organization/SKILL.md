---
name: home-directory-organization
description: Use when tidying loose files in a home directory.
metadata:
  hermes:
    tags: [files, organization, filesystem, housekeeping]
    category: productivity
---

# Home directory organization

## User preference and scope
- Keep ordinary loose files out of the home directory root; group them by type and, where useful, subject. Use Pictures/, Scripts/, Configs/ and Documents/ rather than one unsorted dump folder.
- Preserve hidden shell/application configuration in its expected location. Explain this exception briefly; moving .bashrc, .profile or application dotfiles can break startup and authentication.
- Leave existing project folders, active workspaces, symlinks and running-task paths unchanged unless explicitly asked to reorganize those too. A request to tidy home is not permission to recursively flatten projects.

## Procedure
1. Resolve the requested home to an absolute path. Inventory immediate children with `Path(root).iterdir()`, recording name, file/directory/symlink type and size. Do not start with a recursive search of the whole home: cache and dependency trees obscure the handful of loose files that matter.
2. Read loose scripts and inspect filenames before categorizing. Avoid printing credential-bearing configuration or opening sensitive screenshots merely to classify them. Group images under Pictures/Images, Pictures/Generated or Pictures/Screenshots/<subject>; scripts under Scripts/<purpose>; exported config under Configs/<application>; documents under Documents/<purpose>. Prefer suitable existing directories.
3. Build an explicit source-to-destination mapping for every ordinary root file. Check destination collisions, symlinks, available access and source presence before moving anything. Inspect relevant scheduler/service references and script output paths; do not run a settings-generation script as a relocation test because it may invoke paid APIs or modify live configuration.
4. Save a local move manifest under Documents/FileOrganization before the first move. Include original path, destination and SHA-256. Move without overwriting, retain metadata, and compare destination hash with the original. Keep the manifest local: it records operational paths, not reusable skill content. If a move fails, stop and report completed entries rather than deleting or guessing a rollback.
5. Update known hardcoded output paths in relocated scripts with `patch` so future execution does not recreate root clutter. Change only relocation-related paths. Validate syntax and target assignments with AST/static checks; record post-edit hashes separately from original move hashes. Test execution only when its side effects are safe and relevant.
6. Re-inventory immediate root children. Assert every mapped file exists at its destination and no ordinary loose files remain. Report hidden configuration exceptions and any skipped files accurately. Check active worker liveness when reorganization occurred alongside a long-running task.
7. Finish with moved count, category folders, remaining exceptions and verification status. Do not replay individual moves or expose sensitive filenames unnecessarily.

## Verification
- Every source accounted for in the manifest; no destination overwritten.
- All moved bytes hash-match before intentional path edits.
- Updated scripts reference existing organized output directories.
- Ordinary root file count reaches zero, excluding explicitly preserved configuration.
- Existing projects and active workspaces remain at their original paths.
