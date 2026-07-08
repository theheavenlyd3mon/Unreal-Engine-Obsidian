# Changelog

All notable changes to the UE5 Tutorial Knowledge Base will be documented in this file.

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [v1.4.0] — 2026-06-13

### Added
- **Merged PR #1** from lEWFkRAD (Jeff) — community contribution with 54 new files:
  - `UE5_Gotchas/` — 5 concept docs + MOC covering GAS replication, open-world save architecture, multiplayer-from-day-one, procedural tower generation, performance budgets
  - `Contrib/echoes-of-ascension-kit/` — full dev kit: vertical-slice spec, milestone backlog, system design, starter UE 5.7 C++ module (EchoesCore with GAS triad, async save, deterministic floor gen), eval harness, Hermes skill
  - `Articles/ue5-canonical-references.md` — stable external references (Epic docs, tranek, Lyra, benui, Tom Looman, Cedric's Network Compendium)
  - `_REVIEW_Contributed_Gotchas.md` — review notes for contributed content

### Fixed
- Modernized `UE5_Gameplay_Framework_Reference.md` per errata (PR #1 review):
  - `AttachTo()` → `SetupAttachment()` (deprecated since UE4.12)
  - Removed legacy module headers (`Engine.h`, `EnginePrivate.h`, `*Classes.h`)
  - `IMPLEMENT_PRIMARY_GAME_MODULE` — added missing `FDefaultGameModuleImpl` first arg
  - `TargetInfo` → `ReadOnlyTargetRules` with `: base(Target)`
  - Replaced obsolete INI module registration with `.uproject` Modules array + `.Target.cs` ExtraModuleNames
  - `OutExtraModuleNames` → `ExtraModuleNames`
  - `FClassFinder` → `ConstructorHelpers::FClassFinder`
- Modernized `UE5_GAS_Reference.md` per errata (PR #1 review):
  - `InstancedPerExecution` / `NonInstanced` marked deprecated in UE 5.5+
  - `InstancedPerActor` set as default instancing policy

### Sources
- PR #1 authored with Claude Code, reviewed against UE 5.7 API
- Starter code reviewed for API correctness but not yet compiled against engine (no UE install available at authoring time)

---

## [v1.3.1] — 2026-06-13

### Added
- `_MOC_ROOT.md` — Master index linking all folder MOCs
- Cross-links — `## See Also` sections added to 6 topic MOCs (GAS, CPP, AI, Data Assets, Save System, Animation)

### Fixed
- Step_by_Step_Guides numbering gap — renumbered 05–14 → 04–13

### Removed
- `_research_queue.json` — stale, all topics already written
- `Local_Models_Setup.md` — Windows setup info, not vault content

### Moved
- `_REVIEW_New_Tutorials.md` → `.archive/`

---


## [v1.3.0] — 2026-06-13

### Added
- **UE5_CPP/UE5_Cpp_Reference_Guide.md** — Comprehensive C++ reference (897 lines):
  - Epic C++ Coding Standard — naming, formatting, portable types, modern C++
  - UObject System — CDO, creation rules, GC, ticking
  - Smart Pointers — TSharedPtr/TSharedRef/TWeakPtr/TUniquePtr, thread safety
  - UFUNCTION — all specifiers, metadata, parameter specifiers
  - Metadata Specifiers — class, enum, function, property meta tags (full reference)
  - UPROPERTY — all property specifiers, bitmask patterns, data types
  - TSubclassOf — type-safe UClass pointers
  - Containers — TArray, TMap/TMultiMap, TSet with full API reference
  - Delegates & Lambdas — declaration, binding, execution, examples
  - Low-Level Memory Tracker (LLM) — setup, tags, custom tags
- **UE5_CPP/UE5_Gameplay_Framework_Reference.md** — Gameplay architecture:
  - Class hierarchy & lifecycle (GameInstance → GameMode → GameState → Controller → Pawn)
  - Constructor patterns (ObjectInitializer, ConstructorHelpers, subobjects)
  - Gameplay Modules — DLL structure, Build.cs, module registration
  - Module categories (Runtime, Editor, Developer)
- **UE5_CPP/UE5_GAS_Reference.md** — Gameplay Ability System:
  - ASC setup with IAbilitySystemInterface
  - Gameplay Abilities — lifecycle, granting/revoking, tag interactions, network replication, instancing
  - Attributes & Attribute Sets — creation, helper macros, dual values, PostGameplayEffectExecute
  - Gameplay Effects — duration types, GE components, stacking, Gameplay Cues
  - Ability Tasks — async execution, custom tasks
  - GAS networking summary (prediction, rollback)
- Updated `_MOC_UE5_CPP.md` — new "Reference Guides" section with wikilinks
- Updated `README.md` — UE5_CPP file count 5→8
## [v1.3.1] — 2026-06-13

### Added
- **`_MOC_ROOT.md`** — Master index linking all 22 folder MOCs (Learning Path → Systems → Architecture → Special)
- **`UE5_Gotchas/`** (6 files, contributed by Jeff) — "What breaks and why" notes:
  - `01_GAS_Replication_Gotchas.md` — Replication modes, ASC-on-PlayerState, Mixed-mode Owner trap, InitAbilityActorInfo timing
  - `02_OpenWorld_Save_Architecture.md` — Persistence under World Partition, GUID identity, profile-vs-run saves
  - `03_Multiplayer_From_Day_One.md` — Why retrofitting co-op is a rewrite, authority discipline
  - `04_Procedural_Tower_Generation.md` — Deterministic seeding, PCG for decoration, runtime-NavMesh gotcha
  - `05_Performance_Budget_Reality.md` — 16.6 ms budget, software vs hardware Lumen, async loading
  - `_MOC_UE5_Gotchas.md` — Map of Content
- **`Articles/ue5-canonical-references.md`** (contributed by Jeff) — Stable external references (Epic 5.7 docs, tranek GASDocumentation, vorixo Devtricks, Cedric's Network Compendium, Tom Looman, Lyra, benui)
- **Cross-links** — `## See Also` sections added to 6 topic MOCs (GAS, CPP, AI, Data Assets, Save System, Animation) linking to relevant Architecture docs

### Fixed
- **Step_by_Step_Guides numbering gap** — Renumbered files 05–14 → 04–13 to close the gap after a removed file. Updated all `episode:` frontmatter, Previous/Next wikilinks, and MOC references across 11 files.

### Removed
- `_research_queue.json` — All 14 topics already written; file was stale
- `Local_Models_Setup.md` — Windows setup info, not vault content

### Moved
- `_REVIEW_New_Tutorials.md` → `.archive/` — One-shot review artifact from v1.1.0

### Notes
- `.gitignore` already had `workspace.json` and `workspace-mobile.json` — no change needed
- `Contrib/echoes-of-ascension-kit/` from PR #1 held for separate review (game-specific dev kit)

### Sources
- UE5_Gotchas and ue5-canonical-references contributed by Jeff (PR #1), drafted on a local model (Qwen3.6-27B), fact-checked against Epic 5.7 docs
- Corrections applied during review: `UGameplayAbilityComponent` → `UAbilitySystemComponent`, invented `USaveGameComponent` → `UActorComponent`, non-existent async-load API → real `UAssetManager::GetStreamableManager().RequestAsyncLoad`
