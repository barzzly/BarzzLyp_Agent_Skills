# API-first server diagnosis

- Use configured Client API credentials before browser access. Browser Cloudflare failure does not prove API failure.
- If urllib/default routing stalls, use `curl -4 --connect-timeout 8 --max-time 25 -A 'Mozilla/5.0'` with Bearer authentication. Never print credentials.
- Match proxy backend aliases against live server allocations, not screenshot labels.
- Paginate file listings beyond 250 entries before concluding JAR absence. Data folders do not prove loaded plugins.
- Read startup logs for actual software/version, not panel egg labels.
- Preserve exact Via protocol direction. Observed NBT conversion failure does not prove corrupt world, duplicate Via installation, outdated plugin, or specific block type. Diagnose before updating or deleting blocks.
