---
title: "UE5 Canonical References — Stable Authoritative Sources"
source: "curated"
type: "reference"
series: "Articles"
tags: [ue5, reference, gas, multiplayer, save-system, performance, canonical, index]
created: 2026-06-13
---

# UE5 Canonical References

Stable, authoritative external references for solo RPG development — chosen because they don't rot the way one-off videos do. Unlike the vault's `youtube-summary` notes (which capture a specific tutorial), these are living docs, reference repos, and engine documentation worth bookmarking for the life of the project.

Each entry notes **why it matters for an open-world RPG with GAS + a procedural co-op tower** (the *Echoes of Ascension* stack).

## Gameplay Ability System (GAS)

| Resource | URL | Why |
|----------|-----|-----|
| Epic — Understanding GAS (UE 5.8+) | `https://dev.epicgames.com/documentation/en-us/unreal-engine/understanding-the-unreal-engine-gameplay-ability-system` | The official, version-current reference. Start here for terminology. |
| tranek — GASDocumentation | `https://github.com/tranek/GASDocumentation` | The community bible for GAS. Replication modes, prediction, the whole mental model. Already referenced in [[GASDocumentation]]. |
| vorixo — Devtricks (GAS) | `https://vorixo.github.io/devtricks/gas/` and `/gas-replication-proxy/` | "The truth of GAS" + advanced network optimization. Deep, correct, replication-focused. |
| GAS Companion — ASC on PlayerState | `https://gascompanion.github.io/asc-on-player-state/` | The clearest write-up of the OwnerActor/AvatarActor + respawn rule. See [[01_GAS_Replication_Gotchas]]. |
| Stephen Ulibarri (Druid Mechanics) — GAS course | Udemy (paid) | The most thorough video course on building an RPG with GAS in C++. Worth the money if going deep on combat. |

## Multiplayer / Networking

| Resource | URL | Why |
|----------|-----|-----|
| Cedric "eXi" Neukirchen — Multiplayer Network Compendium | `https://cedric-neukirchen.net/docs/category/multiplayer-network-compendium/` | The canonical free intro to UE networking: authority, ownership, RPCs, replication. Updated for UE5. Required reading before co-op — see [[03_Multiplayer_From_Day_One]]. |
| Epic — Networking & Multiplayer | `https://dev.epicgames.com/documentation/en-us/unreal-engine/networking-and-multiplayer-in-unreal-engine` | Official networking docs; the authority on RPC/replication specifics. |

## Open World / World Partition / Save

| Resource | URL | Why |
|----------|-----|-----|
| Epic — World Partition (UE 5.8+) | `https://dev.epicgames.com/documentation/en-us/unreal-engine/world-partition-in-unreal-engine` | Official WP reference: grid, streaming, data layers, HLODs. |
| Sam Bloomberg — World Partition Internals | `https://xbloom.io/2025/10/24/unreals-world-partition-internals/` | How WP actually works under the hood (actor descriptors, streaming generation). Invaluable when persistence gets weird. |
| Tom Looman — UE C++ Save System | `https://tomlooman.com/unreal-engine-cpp-save-system/` | The canonical `UPROPERTY(SaveGame)` + proxy-archive save pattern used in [[02_OpenWorld_Save_Architecture]]. |
| Epic — Level Streaming Persistence plugin | Built-in engine plugin | Automates persistence for World Partition levels. Underused; evaluate before hand-rolling. |

## Procedural Generation (PCG)

| Resource | URL | Why |
|----------|-----|-----|
| Epic — PCG Framework (UE 5.8+) | `https://dev.epicgames.com/documentation/en-us/unreal-engine/procedural-content-generation-overview` | PCG reached maturity in UE 5.7/5.8. Use for decoration; see [[04_Procedural_Tower_Generation]]. |

## C++ / Architecture / Reference Projects

| Resource | URL | Why |
|----------|-----|-----|
| Tom Looman — ActionRoguelike | `https://github.com/tomlooman/ActionRoguelike` | Clean, modern UE5 C++ project — a "known-good" baseline to compare your (or an LLM's) code against. Already in [[open-source-ue5-game-references]]. |
| Tom Looman — Stanford UE C++ course | `https://tomlooman.com/unrealengine-cpp/` | The reference C++ course; pairs with ActionRoguelike. |
| Epic — Lyra Starter Game | Epic Games Launcher / Fab (free sample) | Epic's modern reference project: GAS, Enhanced Input, modular gameplay, common UI. The single best "how Epic does it" sample. |
| benui — UMG / UPROPERTY specifiers | `https://benui.ca/` | The definitive reference for `UPROPERTY`/`UFUNCTION` specifiers and UMG. Bookmark the specifier tables. |

## Performance

| Resource | URL | Why |
|----------|-----|-----|
| Epic — Lumen GI & Reflections | `https://dev.epicgames.com/documentation/en-us/unreal-engine/lumen-global-illumination-and-reflections-in-unreal-engine` | Software vs hardware Lumen cost model — decide early. See [[05_Performance_Budget_Reality]]. |
| Epic — Nanite Virtualized Geometry | `https://dev.epicgames.com/documentation/en-us/unreal-engine/nanite-virtualized-geometry-in-unreal-engine` | Where Nanite pays off and where it doesn't (foliage caveats). |

## Community

- **Unreal Source / Unreal Slackers** (Discord) — the largest UE community; `#cpp`, `#gas`, and `#multiplayer` channels are faster than Answerhub for "why is my replication broken."
- **Epic Developer Community Forums** — `https://forums.unrealengine.com/` — official release notes, announcements, and the multiplayer/GAS subforums.

---

- 📚 Series: [[_MOC_UE5_Gotchas]]
- 🔗 Related: [[open-source-ue5-game-references]] · [[GASDocumentation]] · [[unreal-engine-solo-rpg-learning-path]]
