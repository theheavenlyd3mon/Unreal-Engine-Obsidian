---
title: Open-World RPG Tutorials / Transcripts (UE 5.6 / 5.7)
created: 2026-07-08
type: research/incoming
scope: Curated candidates for building open-world RPGs in UE5 — video (with transcript) and written.
version_note: Sources at UE 5.6 / 5.7 acceptable; < 5.5 rejected unless foundational framework (Lyra / GAS).
transcript_method: "YouTube automatic captions (en) confirmed retrievable via yt-dlp --write-auto-sub --sub-lang en for every video below."
---

# Open-World RPG Tutorials / Transcripts (UE 5.6 / 5.7)

Curated shortlist for our open-world RPG build. Every video candidate below was verified to have an
English transcript (YouTube automatic captions, retrievable via `yt-dlp --write-auto-sub --sub-lang en`).
Upload dates were pulled from YouTube metadata to judge UE-version relevance against the task's 5.5 cutoff.

Legend for type: `video-transcript` = YouTube video with English captions; `written` = article/docs/course page.
[UNVERIFIED] = a fact I could not directly confirm (version tag, UE feature, or transcript) and should be checked before citing.

## Ranked shortlist

| # | Title | Channel / Author | Type | Duration | Upload | UE ver. (inferred) | Topics | Relevance |
|---|-------|------------------|------|----------|--------|--------------------|--------|-----------|
| 1 | Unreal Engine 5 C++ The Ultimate Game Developer Course | Stephen Ulibarri (Udemy) | written (paid course) | — | updated for 5.7 | 5.7 (stated) | combat, AI, save, world, GAS-lite | Action-RPG-style open-world game course; explicitly "updates for 5.7". Closest to a full framework course. |
| 2 | Unreal Engine 5 RPG Tutorial Series (full playlist, #1 intro) | Gorka Games (YouTube) | video-transcript | 1h47m (#1=1m47s; playlist spans 60+ eps) | 2023-02-20 | 5.x early (pre-5.5) | quests, dialogue, locomotion, combat, vaulting, XP | Most complete UE5 RPG framework series; steps 01–13 already in our vault. Version pre-5.5 → flagged. |
| 3 | How to Create an Adventure Game in UE5 — Full Course | Gorka Games (YouTube) | video-transcript | 1h50m | 2025-09-06 | 5.5+ (recent) | traversal, combat, world, framework | Recent full-course build; strongest version currency of the free video options. |
| 4 | How to Make Open World Games in UE5 (For Beginners) — Course Preview | Nafay 3D (YouTube) | video-transcript | 54m | 2025-02-05 | 5.5+ | world-streaming, traversal, framework | Preview of a dedicated open-world course; topic fit is high for our use case. |
| 5 | Lyra Sample Game (official docs) | Epic Games (dev.epicgames.com) | written (docs) | — | current 5.8 docs | 5.0–5.8 (all branches) | GAS, modular framework, replication | FOUNDATIONAL — explicitly exempt from 5.5 cutoff. Reference architecture for RPG frameworks. |
| 6 | World Partition in Unreal Engine (official docs) | Epic Games (dev.epicgames.com) | written (docs) | — | current | 5.x | world-streaming | Canonical World Partition reference; foundational. |
| 7 | World Partition And Data Layers — UE5 Tutorial | Pitchfork Academy (YouTube) | video-transcript | 26m | 2024-03-06 | 5.x | world-streaming, data layers | Direct WP + Data Layers walkthrough; core open-world tech. |
| 8 | Creating Open World Landscapes with Partitioning & Level Streaming | Aziel Arts (YouTube) | video-transcript | 25m | 2025-04-08 | 5.5+ | world-streaming, landscapes | Recent landscape + WP/streaming build. |
| 9 | Smart Enemy AI — Part 1: Behavior Trees | Ali Elzoheiry (YouTube) | video-transcript | 45m | 2023-05-30 | 5.x | AI, behavior trees | Behavior-tree enemy AI; part of a broader UE5 AI series. |
| 10 | Smart Enemy AI — Part 4: EQS | Ali Elzoheiry (YouTube) | video-transcript | 52m | 2023-06-19 | 5.x | AI, EQS | Environment Query System for smart AI positioning. |
| 11 | Unreal Engine's Gameplay Ability System — Part 7: Multiplayer | Ali Elzoheiry (YouTube) | video-transcript | 32m | 2025-10-23 | 5.5+ | GAS, combat, multiplayer | Recent GAS series entry; combat/ability framework. |
| 12 | UE5 Quest/Dialogue Tutorial — Narrative Quick Start | reubs (YouTube) | video-transcript | 19m | 2022-04-14 | pre-5.5 | quests, dialogue | Narrative plugin quests/dialogue; version-flagged but plugin-based. |
| 13 | Dialogue System! — UE4/UE5 & C++ Action RPG, Part 60 | Shawnthebro (YouTube) | video-transcript | 21m | 2024-08-09 | 5.x | dialogue, C++, quests | C++ dialogue system inside a long Action-RPG series. |
| 14 | Narrative Inventory Quick Start Guide | Narrative Tools (YouTube) | video-transcript | 18m | 2023-12-13 | 5.x | loot/inventory | Plugin-based inventory quick start. |
| 15 | Inventory tutorial — FULL tutorial — UE5 [Blueprints] | Morrigan (YouTube) | video-transcript | 1h13m | 2025-03-24 | 5.5+ | loot/inventory | Recent full Blueprint inventory build. |
| 16 | Creating the ultimate save system — UE5 | LeafBranchGames (YouTube) | video-transcript | 51m | 2024-02-20 | 5.x | save | Save/load architecture tutorial. |
| 17 | Unreal Engine 5 Lootable Chest Blueprint Setup | D3kryption (YouTube) | video-transcript | 32m | 2024-04-11 | 5.x | loot | Loot chest interaction. |
| 18 | How to create an inventory system! — Part 14: Random loot! | NoWhere (YouTube) | video-transcript | 33m | 2024-06-25 | 5.x | loot | Random loot generation in inventory series. |

## Source URLs

1. Ulibarri course (Class Central listing): https://www.classcentral.com/index.php/course/udemy-unreal-engine-5-the-ultimate-game-developer-course-125707
   Direct Udemy: https://www.udemy.com/course/unreal-engine-5-the-ultimate-game-developer-course/
2. Gorka Games RPG playlist: https://www.youtube.com/playlist?list=PLiSlOaRBfgkcPAhYpGps16PT_9f28amXi
   Intro ep: https://www.youtube.com/watch?v=FNTyIWkv5k8
3. Gorka Adventure Full Course: https://www.youtube.com/watch?v=4r9TYrQu8QY
4. Nafay 3D Open World preview: https://www.youtube.com/watch?v=DFexPxDyDzo
5. Lyra docs: https://dev.epicgames.com/documentation/unreal-engine/lyra-sample-game-in-unreal-engine
   Lyra GAS abilities: https://dev.epicgames.com/documentation/unreal-engine/abilities-in-lyra-in-unreal-engine
6. World Partition docs: https://dev.epicgames.com/documentation/unreal-engine/world-partition-in-unreal-engine
7. Pitchfork WP+Data Layers: https://www.youtube.com/watch?v=lkjlP0Y4zvc
8. Aziel Open World Landscapes: https://www.youtube.com/watch?v=B2f6EoOXRHg
9. Ali BT Part 1: https://www.youtube.com/watch?v=-t3PbGRazKg
10. Ali EQS Part 4: https://www.youtube.com/watch?v=Oy_LojjRiWo
11. Ali GAS Part 7: https://www.youtube.com/watch?v=jDKR5nsFmvU
12. reubs Quest/Dialogue: https://www.youtube.com/watch?v=SsrHHiJeAJ8
13. Shawnthebro Dialogue C++: https://www.youtube.com/watch?v=IAVPnFx65WU
14. Narrative Inventory: https://www.youtube.com/watch?v=suMFa5K_4L8
15. Morrigan Inventory: https://www.youtube.com/watch?v=TB1eOaxwFuo
16. LeafBranch Save: https://www.youtube.com/watch?v=7gfA-QO5pA8
17. D3kryption Chest: https://www.youtube.com/watch?v=i8kUc8SUVnM
18. NoWhere Random Loot: https://www.youtube.com/watch?v=FPx02dEVL4o

## Additional candidate videos (transcript confirmed, lower shortlist priority)

- Make An Open World Map in 20 Minutes — Smart Poly — https://www.youtube.com/watch?v=6_5_GiYgCis — 22m, 2024-08-23 — world-streaming/landscapes (quick build, not framework-depth)
- How to Create an Open World in UE5 — PCG, Landmass, Water, World Partition — Gorka Games — https://www.youtube.com/watch?v=Uvce5nRrzk8 — 25m, 2023-08-08 — world-streaming [pre-5.5 flagged]
- How To Make A Massive Open World Map — Upside Tutorials — https://www.youtube.com/watch?v=nyBv0gqwJO0 — 18m, 2022-04-21 — world-streaming [pre-5.5 flagged; uses World Composition, superseded by World Partition]

## Topics deliberately under-covered (gaps to close next pass)

- Faction / reputation systems: only found Marketplace plugins / forum threads, no strong free tutorial with transcript.
  - PolishDesigner Reputation & Faction System (forum): https://forums.unrealengine.com/t/polishdesigner-reputation-faction-system/2692896 [UNVERIFIED — plugin/marketplace, not a tutorial]
  - UE4 Faction System (older video, pre-5.5, likely no transcript relevance): https://www.youtube.com/watch?v=jRxHp4EEqbs [UNVERIFIED]
- Dialogue *with branching choices + consequences*: covered partially by reubs/Shawnthebro; a dedicated modern (5.6+) branching-dialogue tutorial was not found.
- Save architecture specifically for open-world (per-cell actor state persistence): LeafBranch covers generic save; open-world-specific save (World Partition cell state) not found as a free tutorial.

## Version-relevance notes (against 5.5 cutoff)

- KEPT (foundational, exempt): Lyra docs (#5), World Partition docs (#6).
- KEPT but flagged pre-5.5: Gorka RPG Intro playlist (#2, 2023), reubs Quest/Dialogue (#12, 2022),
  Gorka PCG Open World (#extra, 2023), Upside Massive World (#extra, 2022, World Composition).
  These remain relevant as framework references but should be reviewed for 5.8 API drift.
- STRONGEST version currency (2025+): Gorka Adventure Full (#3, 2025-09), Nafay Open World (#4, 2025-02),
  Aziel Landscapes (#8, 2025-04), Ali GAS Part 7 (#11, 2025-10), Morrigan Inventory (#15, 2025-03),
  Ulibarri course (#1, 5.7 updates).

## Verification log

- Transcript availability: all 18 primary + 3 extra videos confirmed to expose English (en) automatic captions via yt-dlp --list-subs (run 2026-07-08).
- Upload dates: pulled from YouTube metadata via yt-dlp --print %(upload_date)s (run 2026-07-08).
- Lyra & World Partition doc version branches: confirmed live on dev.epicgames.com (5.0–5.8 selector present).
- Ulibarri "updates for 5.7": confirmed via Class Central course listing text.
- [UNVERIFIED] items: faction/reputation (plugin, not tutorial); UE4 faction video (age + transcript not checked).
