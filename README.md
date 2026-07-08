# UE5 Tutorial Knowledge Base

An Obsidian vault containing extracted summaries, transcripts, step-by-step guides, and architecture references for Unreal Engine 5 RPG development. Organized by topic with full cross-linking between files.

## What's In Here

### Tutorial Series (Original)

| Folder | Source | What It Covers |
|--------|--------|----------------|
| `Blueprint_Fundamentals/` | Ask A Dev (19 classes) | Visual scripting from zero — variables, events, loops, UI, interfaces |
| `UE5_Beginner_Tutorials/` | Coqui Games (16 episodes) | C++/Blueprint coding — classes, functions, interfaces, components |
| `UE5_7_Starter_Course/` | Bad Decisions Studio (20 parts) | Engine basics — modeling, lighting, materials, animation, rendering |
| `UE5_PCG_Tutorial/` | PolyBoost (20 tutorials) | Procedural generation — forests, farms, roads, landscapes, cities |
| `Learn_to_Code_Blueprints/` | UNF Games (21 videos) | World building — landscapes, water, foliage, materials, optimization |

### Topic Folders (Added in v1.1.0)

|| Folder | Files | What It Covers |
|--------|-------|----------------|
| `UE5_GAS/` | 6 | Gameplay Ability System — abilities, effects, attributes, combat |
| `UE5_CPP/` | 10 | C++ for UE5 — coding standard, UObject, containers, delegates, gameplay framework, GAS (3 new reference guides in v1.3.0: 897-line C++ reference, gameplay framework, full GAS breakdown) |
| `UE5_Data_Assets/` | 4 | Data Assets & Data Tables — UDataAsset, PrimaryDataAsset, DataTables |
| `UE5_AI/` | 4 | AI — Behavior Trees, Blackboards, AI Perception |
| `UE5_Niagara/` | 4 | Niagara particles — emitters, VFX, mesh particles |
| `UE5_UI/` | 4 | UI / UMG — menus, HUD, Canvas Panel, best practices |
| `UE5_Enhanced_Input/` | 4 | Enhanced Input — Input Actions, Mapping Contexts, triggers |
| `UE5_Save_System/` | 4 | Save/Load — SaveGame objects, structs, checkpoints, autosave |
| `UE5_Animation/` | 4 | Animation — Animation Blueprints, State Machines, Blend Spaces |
| `UE5_Optimization/` | 4 | Optimization — profiling, Unreal Insights, GPU tips |
| `UE5_World_Partition/` | 4 | World Partition — grid system, HLODs, landscape streaming |
| `UE5_Audio/` | 3 | Audio — MetaSounds, attenuation, Blueprint integration |
| `UE5_Materials/` | 4 | Materials — glass, layered materials, parallax occlusion |
| `UE5_Multiplayer/` | 4 | Multiplayer — replication, RPCs, RepNotify |
| `UE5_Gotchas/` | 6 | What breaks and why — GAS replication traps, save architecture, multiplayer-from-day-one pitfalls, procedural generation gotchas, performance budget reality |
| `UE5_OpenWorld_RPG/` | 22 | Open-world RPG framework notes, curated tutorials, RPG build sequences |
| `Step_by_Step_Guides/` | 14 | Numbered step-by-step build guides |
| `Individual_Videos/` | 4 | One-off tutorials that don't belong to a series |
| `Articles/` | 3 | Written content (non-video) |

### Architecture (Added in v1.2.0)

| File | What It Covers |
|------|----------------|
| `unreal-engine-rpg-systems.md` | Inventory, quests, dialogue, save system architecture patterns |
| `unreal-engine-solo-rpg-learning-path.md` | Priority-ordered learning plan for solo RPG dev |
| `unreal-engine-gameplay-ability-system.md` | GAS overview with RPG system mapping |
| `unreal-engine-blueprint-hybrid-workflow.md` | C++/Blueprint split strategy — "C++ writes the verbs, Blueprints fill in the nouns" |
| `unreal-engine-cpp-foundations.md` | UObject system, reflection, garbage collection |
| `GASDocumentation.md` | Pointer to tranek's GAS documentation (324KB community reference) |
| `open-source-ue5-game-references.md` | ActionRoguelike and Alis as code architecture references |

### Contributed Content (Added in v1.4.0, maintained in v1.5.0)

| Folder | What's In It |
|--------|-------------|
| `UE5_Gotchas/` | 5 concept docs + MOC — GAS replication, save architecture, multiplayer, procedural gen, performance budgets. The "what bites you" layer. |
| `Contrib/echoes-of-ascension-kit/` | Community dev kit: vertical-slice spec, milestone backlog, system design, errata, starter UE 5.8 C++ module (EchoesCore), eval harness, Hermes skill |
| `Articles/ue5-canonical-references.md` | Stable external references that don't rot — Epic docs, tranek, Lyra, benui, etc. |
| `_REVIEW_Contributed_Gotchas.md` | Review notes for the contributed gotchas |
### Gotchas (Added in v1.3.1, contributed by Jeff)

|| Folder | Files | What It Covers |
|--------|-------|----------------|
| `UE5_Gotchas/` | 6 | What breaks and why — GAS replication traps, open-world save architecture, multiplayer-from-day-one pitfalls, procedural generation gotchas, performance budget reality |

### Special Folders

| Folder | What's In It |
|--------|-------------|
| `Step_by_Step_Guides/` | The best tutorials rewritten as numbered steps with prerequisites. Start here if you want to build something. |
| `Individual_Videos/` | One-off tutorials that don't belong to a series |
| `Articles/` | Written content (non-video) |
| `UE5_OpenWorld_RPG/` | Curated open-world RPG framework notes, tutorial shortlist, and RPG build integration references |

## File Structure

Every file has:
- **YAML frontmatter** — title, source URL, video ID, type, series, episode number, tags
- **Tutorial content** — transcript, summary, or step-by-step instructions
- **Related section** — wikilinks to previous/next episodes and the series index

Each folder has a `_MOC_` file (Map of Content) that links to every file in that series.

## How To Use

1. **Open this folder as an Obsidian vault**
2. **Start here** — open `_MOC_ROOT.md` for the master index
3. **Browse by series** — open any `_MOC_` file to see all episodes listed
4. **Navigate episodes** — click the `← Previous` and `→ Next` links at the bottom of each file
5. **Search by topic** — use Obsidian's search with tags (`#ue5`, `#rpg`, `#blueprint`, `#pcg`, etc.)
6. **Graph view** — shows how episodes connect to each other across series
7. **Start building** — `Step_by_Step_Guides/` has the most actionable content
8. **Design decisions** — `Architecture/` has the "why" behind the "what"
9. **What breaks** — `UE5_Gotchas/` has the traps tutorials skip

## Tags

- `#ue5` — Everything (every file has this)
- `#rpg` — RPG Framework series (combat, AI, quests)
- `#blueprint` — Blueprint/visual scripting tutorials
- `#cpp` — C++ tutorials
- `#gas` — Gameplay Ability System
- `#pcg` — Procedural content generation
- `#beginner` — Beginner-friendly content
- `#guide` — Step-by-step instructions
- `#moc` — Map of Content index files
- `#combat`, `#ai`, `#ui`, `#animation`, `#niagara`, `#materials` — Topic-specific tags
- `#gotchas`, `#architecture` — Architecture and "what breaks" docs

## Vault Checks

Run the local vault linter before opening PRs that add, rename, or reorganize notes:

```bash
python3 tools/vault_lint.py .
```

The linter uses only the Python standard library. It checks for required root indexes, broken or ambiguous Obsidian wikilinks, duplicate note names/titles, and warning-only metadata/MOC hygiene issues. Existing vault findings can be recorded in `.vault_lint_baseline`; CI suppresses those but still fails on new broken/ambiguous wikilinks.

To refresh the baseline after intentionally fixing or accepting findings:

```bash
python3 tools/vault_lint.py . --update-baseline
```

## Local PR Harness

Use the local harness to prepare reviewable PRs without uploading:

```bash
python3 tools/pr_harness.py check
python3 tools/pr_harness.py draft --title "Add feature-shape template"
```

The harness writes `.pr_draft.md` with branch, changed files, diffstat, local status, and verification output. Upload is intentionally opt-in and guarded:

```bash
# after human review only
python3 tools/pr_harness.py publish --title "Add feature-shape template" --repo theheavenlyd3mon/Unreal-Engine-Obsidian --i-reviewed-this
```

## Versions

See [CHANGELOG.md](CHANGELOG.md) for release history.
