# FAWE oversized persisted clipboard

For `Error loading clipboard from disk` with `Size exceeds Integer.MAX_VALUE`, inspect exact player's UUID `.bd` in live FAWE clipboard directory. FAWE 2.15.4 `DiskOptimizedClipboard.init()` maps whole file; file above 2147483647 bytes cannot load.

Confirm size and matching login trace before repair. Recheck size/mtime, then quarantine only that file outside clipboard directory using same-filesystem rename. Preserve original data without multi-GB copy, world edits or global setting changes. Read back source absence, backup size/header and unchanged power state. Do not restart by default. Player relog remains separate runtime verification; clean log without new login does not prove recovery.
