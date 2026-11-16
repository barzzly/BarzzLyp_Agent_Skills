# Google Drive ZIP transfers

- Resolve destination from live panel inventory; preserve power state and keep archive unextracted when requested.
- For public large Drive files, request `https://drive.usercontent.google.com/download?id=<ID>&export=download`, parse the virus-warning download form, and use its exact hidden parameters (including `confirm` and `uuid`). Probe a four-byte range: require ZIP magic and record total size from Content-Range.
- Direct Wings `/files/pull` can return success while saving a Google warning HTML page as `.zip`. Read back size and magic; never treat HTTP 204 as archive delivery. Remove only the verified failed artifact after staging the real archive.
- Prefer `aria2c -x 8 -s 8 -c --file-allocation=none` locally when node pull receives HTML. Confirm local exact size and ZIP central directory before upload.
- Stage SFTP upload as `.zip.part`; avoid overwriting an existing real archive. Wings can reject `sftp -B 262144` with `Outbound message too long 262166`; use standard `-B 32768` with higher `-R` concurrency instead. Resume partial transfer with `reput`.
- Verify exact remote size and content before promoting staged archive. Preserve server files, do not extract or restart. Remove local staging after successful verification unless retention requested.
