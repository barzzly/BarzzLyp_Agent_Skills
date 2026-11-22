# GHAST target acquisition

Inspect fresh spawn logs before blaming rotation. MythicMobs can reject `AITargetSelectors: [0 clear, 1 players]` for GHAST: `AI pathfinder players is not valid for mob type GHAST`. Scripted pursuit and attacks using `@target` then lack an acquired player.

Replace unsupported selector with bounded nearest-player `setTarget` metaskill timer. Exclude CREATIVE and SPECTATOR through TargetConditions; preserve threat table, stats and existing pursuit. Add a target look timer after fixing acquisition.

Back up exact live mob/skill files, compare before writes, read back bytes, assert scope and inspect fresh reload errors. Do not claim movement fixed from YAML/reload alone. Sample position/rotation in real encounter or obtain player confirmation. Do not spawn mass tests or reset active dungeon runs.
