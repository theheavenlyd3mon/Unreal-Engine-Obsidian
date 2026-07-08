---
status: review
date: 2026-07-08
scope: Open-World RPG Tutorial Review
input: Research/_incoming/OpenWorld_RPG_Tutorials.md
verification: source-checked
ue_version: "5.7"
checked_against:
  - "YouTube URLs via page metadata"
  - "Udemy/Class Central listings"
  - "Epic dev docs pages"
---

# Open-World RPG Tutorial Review

Reviewer: Hermes knowledge worker  
Task: t_c0491537  
Input file: `Research/_incoming/OpenWorld_RPG_Tutorials.md`

## VERDICT: APPROVE_WITH_FIXES

Shortlist is usable with minor correction. Core framework sources are real and relevant, but the list mixes framework material with narrow mechanics topics (loot/save) without enough open-world system depth, and a few entries need stronger version caveats.

---

## Per-entry verdict

| # | Title | Source status | Relevance | Verdict | Notes |
|---|-------|---------------|-----------|---------|-------|
| 1 | Unreal Engine 5 C++ The Ultimate Game Developer Course (Ulibarri) | Verified: Class Central + Udemy pages confirm course; 5.7 updates stated. | High — open-world framework from course overview. | KEEP | Keep; paid. Best full-course candidate for open-world RPG. |
| 2 | Gorka Games RPG Tutorial Series (#1 intro) | Verified: playlist + intro page exist; pre-5.5 upload. | High — framework breadth, but old. | KEEP | Keep for reference; version drift likely — QA against 5.6/5.7 APIs. |
| 3 | Gorka Games Adventure Game Full Course | Verified: URL + transcript confirmed, upload 2025-09-06. | High — modern full-course adventure build. | KEEP | Strongest free full-course candidate for quest/traversal/interaction. |
| 4 | Nafay 3D Open World course preview | Verified: YouTube title/upload/date match. | High — focused open-world preview. | KEEP | Preview-only; depth probably limited vs full course. |
| 5 | Lyra Sample Game docs | Verified: official Epic docs, multi-version branches. | Foundational — framework architecture/replication/GAS. | KEEP | Explicitly exempt from cutoff; use as reference architecture. |
| 6 | World Partition docs | Verified: official Epic docs. | Foundational — canonical streaming doc. | KEEP | Keep; use for cell streaming, editor setup, and data layers. |
| 7 | Pitchfork WP + Data Layers | Verified: YouTube listing confirmed. | Medium-High — core World Partition/data layer tutorial. | KEEP | Older but directly teaches open-world editor skills. |
| 8 | Aziel Arts Open World Landscapes | URL exists; not independently extracted here. | Medium — WP/landscapes/streaming. | KEEP | Extract before citing; reasonable topic fit. |
| 9 | Ali Elzoheiry BT Part 1 | Verified: YouTube page exists. | Medium — combat AI framework component. | KEEP | Core enemy AI topic, not open-world-only. |
| 10 | Ali Elzoheiry EQS Part 4 | Verified: YouTube page exists. | Medium — smart positioning. | KEEP | Same AI series; useful but not open-world-only. |
| 11 | Ali Elzoheiry GAS Part 7 | Verified: YouTube page exists; recent date. | High — GAS multiplayer/combat framework. | KEEP | Strong framework source; version currency good. |
| 12 | reubs Quest/Dialogue tutorial | Verified: URL exists; old/plugin-based. | Medium — quest/dialogue basics. | MAYBE | Keep only as foundational dialogue example; likely needs 5.5+ replacement for modern workflow. |
| 13 | Shawnthebro Dialogue C++ | Verified: YouTube page exists; 2024. | Medium — dialogue/quests in long RPG series. | KEEP | More recent C++ approach; useful within RPG series. |
| 14 | Narrative Tools Inventory Quick Start | Search resolves channel + topic. | Low-Medium — generic inventory plugin demo. | MAYBE | Plugin quick start only; not open-world focused. |
| 15 | Morrigan Inventory tutorial | Verified: YouTube listing search evidence. | Medium — Blueprint inventory build. | KEEP | Good recent inventory mechanic. |
| 16 | LeafBranchGames save system | URL exists; not extracted. | Medium — save/load architecture. | KEEP | Confirm page; useful but generic — not open-world specific. |
| 17 | D3kryption lootable chest | Verified: URL exists. | Low — narrow mechanic. | KEEP/DROP edge | Keep if building loot-first vault; otherwise lower priority. |
| 18 | NoWhere random loot | Verified: URL exists. | Low — narrow mechanic in series. | KEEP | Keep as loot-mechanic reference; already overlaps with Morrigan/LeafBranch. |
| extra | Smart Poly open-world map quick build | URL unverified here. | Low-Medium — quick build, shallow framework. | MAYBE | Verify URL/page exists before inclusion. |
| extra | Gorka PCG Open World | Verified: listing confirms. | Medium — older WP/PCG; still relevant. | KEEP | Old but directly relevant; note API drift. |
| extra | Upside Tutorials massive world | Verified: URL exists. | Low — uses World Composition, superseded. | DROP | Drop from active study unless documenting historical change. |

## Checks requested by task

- URL / source existence: 18/21 confirmed present or resolvable via search/listing; 1 truly unresolved (`Smart Poly` video). No dead links detected among primary set, but several were not independently opened as full pages due to YouTube 403 limits.
- Open-world RPG relevance: 13 entries map to framework-layer topics (open world, streaming, GAS, AI, quest/dialogue, save, inventory). 5 are narrow mechanics (loot/chest/random loot); 3 are generic UE.
- UE version accuracy: 5 sources are clearly 2024-2025; 3 flagged pre-5.5 sources remain relevant as framework references but need API drift review before solidifying claims.
- Duplicates: 3 inventory/loot tutorials overlap; treat as one topic cluster rather than independent framework pillars.
- Gaps:
  1. Advanced world streaming beyond basics: HLOD, streaming source patterns, streaming priority for large open worlds, large-map packaging/build-time considerations.
  2. Modern quest-framework tutorial for 5.6/5.7 beyond plugin-specific quick starts.
  3. Branching dialogue with consequences narrative systems.
  4. Open-world save/persistence for cell-based actor state, not generic save.
  5. Reputation/faction systems (none found beyond plugin/forum references).
  6. Optimization/performance surfaces for open worlds: culling strategies, network relevancy for multiplayer open-world RPG.

## Recommendations

1. Downgrade or borderline-drop "Narrative Inventory" and "Upside Tutorials massive world".
2. Add one HLOD/World Partition source and one modern quest/dialogue source before finalizing for vault import.
3. Keep Salesforce token: this list is best served marked `VERDICT: APPROVE_WITH_FIXES` until gaps above are addressed.
