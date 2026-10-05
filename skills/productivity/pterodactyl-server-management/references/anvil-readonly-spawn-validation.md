# Read-only Anvil spawn validation

- Open region files only with `rb`; keep scripts/results outside Minecraft world. Do not start Paper to inspect offline terrain.
- Locate chunk using floor division, especially negative coordinates: region `(cx//32,cz//32)`, header index `(cx%32)+32*(cz%32)`. Header entry's upper 24 bits give 4096-byte sector offset. Chunk payload contains 4-byte length, compression byte, compressed NBT.
- Modern section block states use palette and padded packed longs: bits `max(4,(palette_count-1).bit_length())`, entries per long `64//bits`, index `(y%16)*256+(z%16)*16+x%16`. Mask shifted signed longs. Reject unsupported formats rather than silently guessing.
- For modern overworld height -64, 9-bit WORLD_SURFACE padded heightmap stores first free Y plus 64. Use only to find candidate surface; validate real blocks afterward. Older versions/dimensions need their own height and packing rules.
- Accept conservative full-block allowlist, reject waterlogged ground, partial collision blocks, leaves, gravity blocks and hazards. Require flat full-block 3x3 floor and 3 air layers. Boss candidates need 5x5 floor and 4 air layers. Position at block center X/Z, integer foot Y.
- Dense sampling near warp should use 2-block spacing across explicit chunk bounds; sparse chunk-center sampling misses most custom-build paths.
- Heightmap selection can choose roofs. Report elevated candidates separately; block safety does not prove walking access, gameplay suitability, or creature-specific hitbox clearance.
- Reopen/redecode selected locations and assert footprint plus headroom. Hash region before/after validation to check snapshot stability. Save all candidates and selected counts as JSON; count/dedupe programmatically.
