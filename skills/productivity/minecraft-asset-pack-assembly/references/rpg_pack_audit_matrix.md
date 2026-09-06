# RPG Pack Multi-Plugin Audit Matrix & Static Validation Rules

Comprehensive verification rules for high-end Minecraft RPG weapon and asset packs integrating MMOItems, MythicLib, MythicMobs, ItemsAdder, and ModelEngine.

## 1. The 4-Way Cross-Validation Pipeline

Every RPG weapon definition must resolve cleanly across four plugin domains:

```
[MMOItems item/*.yml]
       │
       ├── (material + custom-model-data) ──► [ItemsAdder contents/**/configs/**/*.yml]
       │                                            └── (resource.material + model_id)
       │
       └── (ability.type) ──► [MythicLib skill/*.yml]
                                     │
                                     └── (mythicmobs-skill-id) ──► [MythicMobs skills/**/*.yml]
```

### Validation Checklist:
1. **Model & Material Parity:**
   - MMOItems `base.custom-model-data` (float or int) must match ItemsAdder `resource.model_id` (integer).
   - MMOItems `base.material` must identically match ItemsAdder `resource.material` (e.g. `STONE_SWORD`). A mismatch causes fallback missing-texture rendering.
2. **Ability Wiring Integrity:**
   - MMOItems `ability.<slot>.type` must match a top-level key in MythicLib skill YAML.
   - MythicLib `mythicmobs-skill-id` must match a top-level skill name in MythicMobs YAML.
   - Flag any unresolved skill nodes as runtime invocation failures.

---

## 2. Cooldown Pitfalls & Thresholds

| Config Location | Correct Syntax | Buggy Antipattern | Consequence |
|---|---|---|---|
| **MMOItems `ability`** | `cooldown: 3.5` | `skillcooldown: 3.5` | MMOItems ignores `skillcooldown`, defaults to `0.0s`, causing 20x/sec spam. |
| **MythicMobs `Skills`** | `Cooldown: 3.5` | `Cooldown: <modifier.skillcooldown>` | MythicMobs evaluates unparsed placeholder as `0.0`, flooding server packets. |
| **Aura-Gated Combos** | `cooldown: 0.2` | `cooldown: 0.0` or `< 0.05` | Rapid click spam desyncs client swing animation and drops item visibility. |

---

## 3. Aura-Driven FSM Combo Patterns
In MythicMobs, combo chains use Auras as state registers. Ensure proper cascading delays:
- Step 1 checks `hasaurastacks{stacks=1} false` and `hasaurastacks{stacks=2} false`, then applies Aura with `delay=1` tick.
- Step 2 checks `hasaurastacks{stacks=1} true`.
- Step 3 (Finisher) checks `hasaurastacks{stacks=2} true` and calls `removeaura`.
- Without `delay=1` or mutually exclusive stack conditions, all 3 steps fire in the same tick.

---

## 4. Automated Pack Health Calculation
When building pack inspectors or linters:
- Start score at 100%.
- Deduct 15% per missing model / material mismatch.
- Deduct 10% per unparsed cooldown placeholder or zero-cooldown click ability.
- Deduct 5% per unresolved helper sound or particle metaskill.

---

## 5. Combat Simulation & Packet Load Thresholds
Static YAML validation alone fails to catch DPS runaway and packet flood bugs:
- **Simulation Duration:** Benchmark rotations over 100 seconds (2,000 ticks at 20 TPS).
- **Packet Rate Limits:** Keep ability + VFX packet events under 25 events/second per player. Rates above 30 events/sec create severe client-side frame drops and server network queue lag.
- **DPS Parity:** Clamp sustained single-target DPS across class tiers (e.g. Tier 1: 15-25 DPS, Tier 2: 25-35 DPS, Tier 3: 35-50 DPS). Flag abilities with cooldowns < 0.1s that artificially spike DPS to 100+.

---

## 6. Multi-Phase Boss State Engine Standards
When designing boss encounters with HP thresholds (e.g. 60% and 25% HP phases):
- **Phase Locking:** Always lock phase transitions using persistent Auras (`duration=999999`) combined with inverted aura checks (`?!hasaura{auraName=Boss_P2}`) to prevent cutscenes or enrage buffs from firing on every damaged tick.
- **ThreatTable Wiring:** Set `Modules: ThreatTable: true` and align AI targeters:
  ```yaml
  AITargetSelectors:
    - clear
    - threat
    - players
  ```
- **Safe Bullet Hell Projectiles:** Projectile barrages must use `bulletType=DISPLAY` instead of ARMOR_STAND and mandate bounded lifetimes (`md=40` to `60` ticks) to prevent entity accumulation.
