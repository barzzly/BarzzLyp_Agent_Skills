---
name: entity-relationship-diagrams
description: Use when designing ERDs from app requirements or examples.
version: 1.0.0
metadata:
  hermes:
    category: software-development
    tags: [ERD, database, schema, diagrams, relational-modeling]
---

# Entity-Relationship Diagrams

Design a relational model that matches the actual project, not the entities shown in a visual example. Deliver a legible diagram plus an editable source when requested.

## Procedure

1. Read the current requirements/proposal and reference image. Extract core workflows, data that must persist, confirmed facts, and proposed or future features. Use the reference for ERD notation and layout only; do not reuse its tables.
2. Model the smallest core schema first. For each entity, define PK, meaningful columns/types, FK nullability, unique constraints, and who can see sensitive data. Do not model unconfirmed optional modules as implemented facts. If assumptions are unavoidable, label them.
3. Check every relationship both ways against schema constraints: parent-to-child cardinality, whether the child FK can be NULL, whether FK UNIQUE makes a one-to-zero-or-one relation, and whether duplicated state can drift (e.g., current status plus history). Use a single source of truth or state how synchronization works.
4. Draw connectors before opaque table cards, route through gutters, and label cardinalities at both ends. Keep FK labels and types apart; ensure optional FK relationships have consistent notation in legend and line style. Check connector endpoints touch their cards, not empty space.
5. Export PDF and PNG where the user needs a sharable visual. Re-open exported PDF to confirm table names and relationship count; render PNG and inspect for clipped text, overlapping keys, crossings, and cardinality mismatch. Iterate until legible at intended viewing size.

## Pitfalls

- Keep the ERD about stored data and relationships; screens, bots, and workflows are not tables unless they introduce records that the accepted scope needs.
- Do not infer `1` mandatory parent from an optional child FK: a row with NULL references zero parents, while each non-NULL reference points to exactly one.
- Do not mark `1:1` solely because a field is named `parent_id`; require a UNIQUE constraint on that FK and decide whether the child row is optional.
- Do not claim diagram correctness from entity counts alone; validate constraints, cardinalities, and visual connector attachment against the schema.
- Keep private customer measurements/contact details out of publicly accessible entities/views by default.
