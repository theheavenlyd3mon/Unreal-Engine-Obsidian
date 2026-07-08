# Open-World RPG Framework Tutorials & Transcripts (UE 5.6 / 5.7)

Researched: 2026-07-08
Scope: tutorials/transcripts on building open-world RPGs or their underlying
       framework in Unreal Engine 5. Version note: 5.6/5.7 sources accepted;
       older than 5.5 rejected UNLESS a foundational framework doc still relevant
       (Lyra, GAS). "Upgrade to 5.8 after review" is a downstream task.

Legend:
  [V]   Verified this run (page/transcript/metadata pulled)
  [UV]  URL known from search but content not directly fetched this run
  [VERIFY]  Claim present but should be re-checked against engine 5.8
  type: video-transcript | video-course | written | plugin | sample-project

RANKING: Tier 1 = best open-world RPG framework coverage, fresh, transcript
available. Tier 2 = foundational framework docs (allowed even if pre-5.5).
Tier 3 = system-specific (some older, version caveats noted).

============================================================================
TIER 1 — Full open-world RPG framework series / courses (transcript available)
============================================================================

#1  Unreal Engine 5 RPG Tutorial Series (Gorka Games)  [V]
    Channel/Author : Gorka Games (YouTube)
    URL            : https://www.youtube.com/playlist?list=PLiSlOaRBfgkcPAhYpGps16PT_9f28amXi
    Type           : video-transcript (85 episodes; whole-series playlist)
    Duration       : ~12-48 min per episode (playlist total ~25h+)
    UE version     : UE5 (series ran 2023-02 -> 2025-02; last updated Feb 22 2025).
                     No explicit 5.6/5.7 tag; Blueprint, version-agnostic patterns. [VERIFY]
    Topics         : open-world (landscape/World Partition-style map #52/#61),
                     locomotion, combat, equipment/inventory (#14-#20),
                     AI Behavior Trees patrolling/chasing/melee (#20-#23),
                     quests + quest dialogue (#38), save/load (#80),
                     save quests + time-of-day (#81), stats/XP/levels.
    Relevance      : THE single best free, transcript-bearing open-world RPG
                     framework series. Covers most required subsystems end-to-end.
                     Verified transcripts on sampled episodes (#1, #38, #52, #61).

#2  Unreal Engine 5 C++ The Ultimate Game Developer Course (Stephen Ulibarri)  [V]
    Channel/Author : Stephen Ulibarri (Udemy)
    URL            : https://www.udemy.com/course/unreal-engine-5-the-ultimate-game-developer-course/
    Type           : video-course (paid); auto-captions exist [UV: caption quality]
    Duration       : 53h 7m (238 lectures, 22 sections)
    UE version     : 5.7 (explicit "With updates for 5.7!"; last updated 2/2026)  [V]
    Topics         : open-world system, landscapes/foliage, enemies + AI (patrol/
                     chase/attack, Motion Warping), Souls-like combat, loot/gold
                     + breakables, dungeon Level Instances, attribute/XP, C++.
    Relevance      : Most current (5.7) and most complete C++ open-world ACTION-RPG
                     course. Strong for save/loot/AI/world architecture. Paid.

#3  Unreal Dialogue System - Full Course FREE (The Game Dev Cave)  [V]
    Channel/Author : The Game Dev Cave (YouTube)
    URL            : https://www.youtube.com/watch?v=2TzMQWR8qQE
    Type           : video-transcript (free full course)
    Duration       : 1:57:28
    UE version     : UE5 (uploaded 2024-12-02)  [V]
    Topics         : dialogue, branching choices, behavior-tree-driven dialogue,
                     save integration of remembered choices.
    Relevance      : Free, recent, transcript-bearing deep dive on dialogue — a core
                     open-world RPG system the Gorka series only sketches. Verified
                     transcript shows choice/branching + save hooks.

#4  How to Make Open World Games in Unreal Engine 5 (Nafay 3D)  [V]
    Channel/Author : Nafay 3D (YouTube, course preview)
    URL            : https://www.youtube.com/watch?v=DFexPxDyDzo
    Type           : video-transcript (preview; full course paid on Udemy)
    Duration       : 54:20
    UE version     : 5.5 era ("latest version launched in 2025"; recommends latest)  [V]
    Topics         : open-world third-person game, parkour, enemy AI chase/attack,
                     timer system, health, beginner-oriented.
    Relevance      : Beginner-friendly open-world build with AI + traversal. Free
                     preview is transcript-bearing; full course is the paid path.

============================================================================
TIER 2 — Foundational framework docs / samples (allowed even if pre-5.5)
============================================================================

#5  Lyra Sample Game (Epic)  [V]
    Channel/Author : Epic Games (official docs)
    URL            : https://dev.epicgames.com/documentation/unreal-engine/lyra-sample-game-in-unreal-engine
    Type           : written (sample-project + docs, versioned 5.0-5.8)
    Duration       : n/a
    UE version     : 5.0-5.8 (docs current to 5.8)  [V]
    Topics         : modular Gameplay Feature Plugins, Experiences, GAS, inventory/
                     equipment, World Partition maps, UI/UMG, scalability.
    Relevance      : The canonical UE5 RPG/shooter framework reference. Already
                     versioned to 5.8 — ideal base to study before upgrading your info.
                     Foundational, explicitly admissible.

#6  GASDocumentation (tranek)  [V]
    Channel/Author : tranek (GitHub)
    URL            : https://github.com/tranek/GASDocumentation
    Type           : written (reference + sample project)
    Duration       : n/a
    UE version     : 5.3 (README; branches for older)  [V]  -> older than 5.5
    Topics         : Gameplay Ability System architecture, ASC, Gameplay Tags,
                     Attributes/AttributeSets, replication, GAS + multiplayer.
    Relevance      : De-facto community GAS bible (5.9k stars). Pre-5.5 but a
                     foundational architecture doc explicitly allowed by the brief.

#7  World Partition in Unreal Engine (Epic)  [V]
    Channel/Author : Epic Games (official docs)
    URL            : https://dev.epicgames.com/documentation/unreal-engine/world-partition-in-unreal-engine
    Type           : written (versioned 5.0-5.8)
    Duration       : n/a
    UE version     : 5.0-5.8  [V]
    Topics         : world streaming, grid cells, Data Layers, HLOD, One File Per
                     Actor, Open World default map, converting levels, Blueprint.
    Relevance      : Authoritative world-streaming reference for open-world maps,
                     versioned to 5.8. Pair with the Lyra WP maps.

#8  Your First 60 Minutes with Gameplay Ability System (Epic)  [UV]
    Channel/Author : Epic Games (community learning)
    URL            : https://dev.epicgames.com/community/learning/tutorials/8Xn9/unreal-engine-epic-for-indies-your-first-60-minutes-with-gameplay-ability-system
    Type           : written/tutorial
    Duration       : n/a
    UE version     : UE5 [UV: exact version not fetched]
    Topics         : GAS core concepts, practical setup.
    Relevance      : Official on-ramp to GAS before the deeper tranek doc.

#9  Behavior Tree in Unreal Engine - Quick Start Guide (Epic)  [UV]
    Channel/Author : Epic Games (official docs)
    URL            : https://dev.epicgames.com/documentation/unreal-engine/behavior-tree-in-unreal-engine---quick-start-guide
    Type           : written
    Duration       : n/a
    UE version     : UE5 [UV]
    Topics         : AI Behavior Trees, enemy chase-on-sight.
    Relevance      : Official baseline for the open-world AI requirement.

============================================================================
TIER 3 — System-specific (some older; version caveats noted)
============================================================================

#10 Starfield-style Reputation / Faction System (Ryan Laley)  [V]
    Channel/Author : Ryan Laley (YouTube live class)
    URL            : https://www.youtube.com/watch?v=ATHq1sg8-80
    Type           : video-transcript (live class)
    Duration       : 1:14:19
    UE version     : 5.2 (stated in stream)  [V]  -> older than 5.5
    Topics         : faction/reputation component, reputation as currency,
                     AI response by faction standing.
    Relevance      : Rare free, transcript-bearing faction/reputation build.
                     Pre-5.5 but conceptually version-agnostic; flagged for review.

#11 Loot System + Loot Tables (LeafBranchGames)  [V]
    Channel/Author : LeafBranchGames (YouTube)
    URL            : https://www.youtube.com/watch?v=1CE6JIkMgXc
    Type           : video-transcript
    Duration       : 41:10
    UE version     : UE4/UE5 (2022-01)  [V]  -> older than 5.5
    Topics         : loot system, loot tables via Gameplay Tags + Data Tables,
                     scalable drop logic.
    Relevance      : Solid data-driven loot pattern (Gameplay Tags + DTs). Pre-5.5;
                     pattern still valid, verify API names against 5.8.

#12 Open World Tutorial Using World Partition (Smart Poly)  [V]
    Channel/Author : Smart Poly (YouTube)
    URL            : https://www.youtube.com/watch?v=efN4bGbzr78
    Type           : video-transcript
    Duration       : 19:56
    UE version     : UE5 Early Access (2021-06)  [V]  -> significantly older
    Topics         : enabling World Partition, tiled landscapes, grid streaming,
                     runtime hash, foliage streaming.
    Relevance      : Classic WP intro. Much older than 5.5; use only for the
                     conceptual mental model, then defer to the 5.8 WP docs (#7).

#13 Implementing Quest Systems in UE5 Blueprints (Medium)  [UV]
    Channel/Author : object-oriented-worlds (Medium)
    URL            : https://medium.com/object-oriented-worlds/implementing-quest-systems-in-ue5-blueprints-47ea0ac00599
    Type           : written
    Duration       : n/a
    UE version     : UE5 [UV]
    Topics         : quest systems with structs/arrays/maps/Data Tables; integrates
                     dialogue + inventory hooks.
    Relevance      : Written companion to quest building; good for architecture notes.

#14 The Complete Guide to Save Systems in Unreal Engine 5 (Strayspark)  [UV]
    Channel/Author : strayspark.studio (blog)
    URL            : https://www.strayspark.studio/blog/complete-guide-save-systems-unreal-engine
    Type           : written
    Duration       : n/a
    UE version     : UE5 [UV]
    Topics         : what to save, serialization, async, save-file management.
    Relevance      : Broad save-architecture write-up complementing the Gorka #80/#81.

#15 Unreal Engine C++ Save System (Tom Looman)  [UV]
    Channel/Author : tomlooman.com (blog)
    URL            : https://tomlooman.com/unreal-engine-cpp-save-system/
    Type           : written
    Duration       : n/a
    UE version     : UE5 [UV]
    Topics         : C++ SaveGame system design.
    Relevance      : C++-oriented save architecture (pair with Ulibarri #2).

#16 Building an RPG with Gameplay Ability System (course)  [UV]
    Channel/Author : Epic Forums course thread
    URL            : https://forums.unrealengine.com/t/course-building-an-rpg-with-gameplay-ability-system/2654794
    Type           : written/course
    Duration       : n/a
    UE version     : UE5 [UV]
    Topics         : GAS-driven RPG core gameplay loop.
    Relevance      : Course pointer focused on GAS-as-RPG-spine.

#17 Reputation & Faction System (PolishDesigner)  [UV]
    Channel/Author : PolishDesigner (marketplace/forums)
    URL            : https://forums.unrealengine.com/t/polishdesigner-reputation-faction-system/2692896
    Type           : plugin
    Duration       : n/a
    UE version     : UE5 [UV]
    Topics         : complete reputation/faction management for RPG/open-world.
    Relevance      : Off-the-shelf system if you prefer a plugin over Ryan Laley's
                     build (#10). Verify 5.8 compatibility before adopting.

#18 GAS Basics (Umbral Studios)  [UV]
    Channel/Author : Umbral Studios (written, uses tranek)
    URL            : https://techarthub.com/the-long-shadow-of-the-gameplay-ability-system/  (umbrella; series referenced)
    Type           : written
    Duration       : n/a
    UE version     : UE5 [UV]
    Topics         : step-by-step GAS setup guided by tranek docs.
    Relevance      : Gentler on-ramp to GAS if tranek (#6) is too dense.

============================================================================
NOTES / GAPS
============================================================================
- Best free, transcript-bearing END-TO-END open-world RPG framework = Gorka Games
  series (#1). It is Blueprint-based and not explicitly version-tagged; budget time
  to reconcile its APIs with 5.8 during the upgrade review.
- Most CURRENT (5.7) complete course = Ulibarri (#2), but it is paid and C++.
- Foundational docs (Lyra #5, GAS #6, World Partition #7) are already versioned to
  5.8 / admissible as architecture references — start the 5.8 upgrade review there.
- Faction/reputation (#10, #17) and loot (#11) free videos predate 5.5; treat as
  pattern references and re-verify node/API names against 5.8.
- [UV] items were located via search but their pages were not fetched this run;
  confirm version/availability before citing in the wiki.
============================================================================
