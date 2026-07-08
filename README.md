# UE5 Tutorial Knowledge Base

An [Obsidian](https://obsidian.md) vault of extracted Unreal Engine 5 tutorials, step-by-step build guides, and architecture references — organized by source series and topic, with full wikilink cross-referencing between notes. Built for solo UE5 / RPG-action developers who want the "how" and the "why" in one place.

## What's inside

- **Tutorial Series** — full multi-episode YouTube courses transcribed into notes: `Blueprint_Fundamentals/`, `UE5_PCG_Tutorial/`, `UE5_Beginner_Tutorials/`, `UE5_7_Starter_Course/`, `Learn_to_Code_Blueprints/`.
- **Topic Folders** — single-topic deep dives, each with a `_MOC_` index: `UE5_GAS/`, `UE5_CPP/`, `UE5_AI/`, `UE5_Animation/`, `UE5_Materials/`, `UE5_Multiplayer/`, `UE5_Niagara/`, `UE5_UI/`, `UE5_Audio/`, `UE5_Optimization/`, `UE5_World_Partition/`, `UE5_Save_System/`, `UE5_Enhanced_Input/`, `UE5_Data_Assets/`.
- **Step-by-Step Guides** — `Step_by_Step_Guides/`: the best tutorials rewritten as numbered, prerequisite-ordered build steps. The most actionable entry point.
- **Architecture & Reference** — `Architecture/`: system-design patterns (inventory, quests, dialogue, save systems), a solo-RPG learning path, and stable external references in `Articles/ue5-canonical-references.md`.
- **Gotchas** — `UE5_Gotchas/`: the "what bites you" layer — GAS replication, save architecture, multiplayer, and procedural-generation pitfalls.
- **Contributed** — community dev kits, e.g. `Contrib/echoes-of-ascension-kit/` (a UE 5.8 C++ starter module + vertical-slice spec).

## Quick start

1. Open this folder as an Obsidian vault.
2. Open `_MOC_ROOT.md` for the master index.
3. Browse any `_MOC_` file to see a series or topic at a glance.
4. Follow the `← Previous` / `→ Next` links at the bottom of each note.
5. Search by tag — `#ue5`, `#rpg`, `#blueprint`, `#cpp`, `#gas`, `#pcg` …

## Conventions

Every note carries YAML frontmatter (title, source, type, tags) and a Related section. The schema is enforced by `UE5_CPP/_UE5_8_Convention_Standard.md` — read it before adding or editing notes.

## Local additions

Files carried forward from pre-sync local work that have no upstream equivalent:
- `Research/` — in-progress UE 5.8 API research and vault curation notes.
- `Local_Models_Setup.md` — local LLM / TurboHaul hardware setup reference (RTX 4070 Ti).

## Links

- Release history: [CHANGELOG.md](CHANGELOG.md)
- Vault linter: `python3 tools/vault_lint.py .`
