# UE5 Tutorial Vault Curation Report — T0

Generated: 2026-07-08  
Scope: quick classification pass before restructure  
Vault root: `/Users/noctis/Documents/Unreal-Engine-Obsidian`  
Inputs actually present on disk after verification:  
- `/tmp/curation_stale_map.json` — present  
- `/Users/noctis/Documents/Unreal-Engine-Obsidian/CHANGELOG.md` — present  
- `/Users/noctis/Documents/Unreal-Engine-Obsidian/Research/_incoming/UE58_API_DeepSearch.md` — present  
- `/Users/noctis/Documents/Unreal-Engine-Obsidian/_REVIEW_New_Tutorials.md` — present  
- `/Users/noctis/Documents/Unreal-Engine-Obsidian/_REVIEW_Contributed_Gotchas.md` — present  
- `/Users/noctis/Documents/Unreal-Engine-Obsidian/Articles/ue5-canonical-references.md` — present  
Missing on disk but referenced by stale map / brief:  
- `Research/_incoming/UE58_Review.md` — not present  
- `Research/_incoming/OpenWorld_RPG_Review.md` — not present  
- `Research/_incoming/UE58_API_Changes.md` — not present  
- `AGENTS.md` — not present anywhere in vault  
- `Hermes/` directory — not present  
- `templates/` directory — not present  

Because the two review files and the API-changes brief are absent, those briefed claims are preserved only as instructions, not as finished inputs. Classification below is based on the remaining visible evidence. Anything that depends on the missing review files is marked **UNVERIFIED**.

---

## 1. Per-category recommendation + file counts

Selected categories are not exhaustive; they capture the tier-1 tutorial asset folders. Legacy column already exists on disk.

| Category | Files | Rec | Notes |
|---|---|---|---|
| `UE5_RPG_Framework/` | 13 | keep | Largest coherent series; primary RPG spine. |
| `Blueprint_Fundamentals/` | 28 | keep/merge-pairs | Core fundamental series. For pair-merges, see §4. |
| `UE5_Beginner_Tutorials/` | 17 | keep | Coqui Games coding series. |
| `UE5_CPP/` | 10 | keep/merge-related | Includes reference docs from v1.3.0. |
| `Learn_to_Code_Blueprints/` | 22 | keep/merge-related | High overlap with `Step_by_Step_Guides` packaging. |
| `Step_by_Step_Guides/` | 14 | keep/merge-related | Duplicates packaging + RPG series steps with `Learn_to_Code_Blueprints`. |
| `UE5_7_Starter_Course/` | 21 | keep-as-alias | Bad Decisions beginner course; alias to 5.8 in index/MOC, keep wikilinks intact. |
| `UE5_PCG_Tutorial/` | 34 | keep/retitle-versioned | Many files title themselves as 5.5, 5.6, or 5.7. |
| `UE5_GAS/` | 6 | keep/merge-similar | Multiple overviews + full course + combat. |
| `UE5_AI/` | 4 | keep | Small, coherent. |
| `UE5_Enhanced_Input/` | 4 | keep | Small, coherent. |
| `UE5_World_Partition/` | 4 | keep | Small, coherent. |
| `UE5_Audio/` | 3 | keep | Small, coherent. |
| `UE5_Materials/` | 4 | keep | Small, coherent. |
| `UE5_Multiplayer/` | 4 | keep | Small, coherent. |
| `UE5_Gotchas/` | 6 | keep | New contribution; valuable. |
| `Contrib/echoes-of-ascension-kit/` | 11 | relocate out | Full dev kit + module; move out of tutorial vault. |
| `Legacy_5.7_and_Earlier/` | 5 | keep-or-expand | Houses already-migrated legacy candidates; expand during revamp. |
| `Architecture/` | 8 | keep | Design-decision docs; not versioned to engine by themselves. |
| `Articles/` | 3 | keep | `ue5-canonical-references.md` is stable curated sources. |

Total `.md` count across the above content folders (excluding `.git`, `.obsidian`, and misc root docs): **245**.

---

## 2. Version classification for file-level stale references

Rule used: `current-5.8` = valid after aligning to 5.8 conventions, even if a title mentions an older engine; `legacy-5.7` = semantically valid UE 5.6–5.7 content that is not itself deprecated; `deprecated` = references removed APIs; `UNVERIFIED` = claim cannot be confirmed against available brief/docs/stale-map evidence.

### UE5_PCG_Tutorial — high stale-version density

These are evidence-backed classifications using titles plus body snippets from the stale map.

| File | Classification | Evidence / Rationale |
|---|---|---|
| `procedural-road-spline-sampler-ue-5-5.md` | legacy-5.7 | Body/title targets UE 5.5 tutorial content. No deprecated API evidence visible; valid concept but engine version stale. |
| `ue5-pcg-tutorial-beginners-episode-1.md` | legacy-5.7 | Body states `5.5.4 used`, tutorial-level concept. |
| `pcg-ue-5-6-all-new-features.md` | current-5.8 | Feature description is still valid in 5.8; update version reference from 5.6. |
| `Building_a_Procedural_Farm_PCG_and_Landscape_Texture_Patch_Workflow.md` | legacy-5.7 | Body states `UE 5.6.1`; mechanics unchanged but version-specific phrasing stale. |
| `building-procedural-farm-pcg-landscape-texture-patch.md` | legacy-5.7 | Same as above duplicate-ish source. |
| `cinematic-post-apocalyptic-street-p2-pcg.md` | legacy-5.7 | Body explicitly `UE 5.6`; concepts remain valid. |
| `post-apocalyptic-car-wall-pcg-splines-part1.md` | legacy-5.7 | Body explicitly `UE 5.6`, PCG splines are current. |
| `Build_a_Procedural_Dock_Over_Water_Using_Spline.md` | legacy-5.7 | Body explicitly `UE 5.6`; concept valid in 5.8. |
| `ue-5-7-pcg-episode-1-forest-path-splines.md` | current-5.8 | 5.7-specific title/frame, but PCG features are current in 5.8. Retitle only. |
| `ue-5-7-pcg-episode-2-linear-grammar-tool.md` | current-5.8 | Same rationale as above. |
| `procedural-vegetation-editor-ue-5-7-full-forest.md` | current-5.8 | 5.7 Procedural Vegetation Editor workflow names are unchanged in 5.8. |
| `Adding_Realistic_Details_to_Procedural_Trees.md` | current-5.8 | 5.7 title/body; no deprecated systems visible. Update frontmatter tag. |

### UE5_Gotchas

| File | Classification | Evidence / Rationale |
|---|---|---|
| `05_Performance_Budget_Reality.md` | current-5.8 | Claims `UE 5.7 adds experimental Nanite Foliage`; that is true historical wording, but experimental warning is still appropriate. Frame for 5.8 only changes prefix. |
| `04_Procedural_Tower_Generation.md` | current-5.8 | Uses `UE 5.7 PCG` as a historical descriptor. No stale deprecated API claims. |

### UE5_GAS

| File | Classification | Evidence / Rationale |
|---|---|---|
| `04_GAS_UE5.5_2025.md` | legacy-5.7 | Entire note is explicitly a UE 5.5 intro from 2025; keep as historical 5.5 material. |

### UE5_Enhanced_Input

| File | Classification | Evidence / Rationale |
|---|---|---|
| `03_Enhanced_Input_Hold_To_Interact.md` | current-5.8 | Enhanced Input is the current system. No stale deprecated API claim detected from stale-map entry. |

### UE5_World_Partition

| File | Classification | Evidence / Rationale |
|---|---|---|
| `03_UE5_5_4_World_Partition_and_HLODs.md` | legacy-5.7 | Clearly labeled UE 5.4 content; concepts current in 5.8. |

### Blueprint_Fundamentals

| File | Classification | Evidence / Rationale |
|---|---|---|
| `BP_Vectors_Applied_Dash_and_Launch.md` | current-5.8 | Generic character movement/vectors; no 5.7-specific API visible in stale map’s line context. |

### Flat docs / review docs

| File | Classification | Evidence / Rationale |
|---|---|---|---|
| `CHANGELOG.md` | current-5.8 | Contains explicit `5.7 → 5.8` version-reference update notes; itself is provenance metadata. |
| `_REVIEW_Contributed_Gotchas.md` | UNVERIFIED | Stale map shows `Epic 5.7` reference; cannot classify without review file, because example reviewer markdown is not owned by us. |
| `_REVIEW_New_Tutorials.md` | current-5.8 | Serves as historical review record for v1.1.0 v5.6/5.7-era content; misleading to retroactively claim 5.8 provenance, so treat as research provenance, not current documentation. Recommend move to `Research/` after revamp and add frontmatter `status: provenance`. |
| `Research/_incoming/OpenWorld_RPG_Tutorials.md` | UNVERIFIED | Stale map shows explicit `UE 5.6 / 5.7` frame. Without the file on disk, classify as UNVERIFIED pending recovery; archived brief suggests acceptable range. |
| `Research/_incoming/OpenWorld_RPG_Review.md` | UNVERIFIED | Not found on disk. |
| `Research/_incoming/UE58_Review.md` | UNVERIFIED | Not found on disk. |
| `Research/_incoming/UE58_API_Changes.md` | UNVERIFIED | Stale map title implies API changes brief exists elsewhere; on-disk counterpart discovered: `Research/_incoming/UE58_API_DeepSearch.md` — treat as the actual authoritative 5.8 input. |
| `Research/_incoming/UE58_API_DeepSearch.md` | current-5.8 | Present; sourced from official 5.8 release notes with explicit anchors. |
| `Articles/ue5-canonical-references.md` | current-5.8 | “Living” references; source list includes Epic 5.7 pages, which are still authoritative; class `current-5.8` with source note. |

---

## 3. LEGACY category proposal

### Folder structure

```
Legacy_5.7_and_Earlier/
  _MOC_Legacy_5.7_and_Earlier.md
  UE5_Animation/
    _MOC_UE5_Animation_legacy.md
    01_Animation_Blueprint_Blendspaces.md
    02_Animation_Blueprint_State_Machine.md
    03_Jump_Turn_In_Place.md
  UE5_World_Partition/
    03_UE5_5_4_World_Partition_and_HLODs.md
  UE5_GAS/
    04_GAS_UE5.5_2025.md
  UE5_Enhanced_Input/
    03_Enhanced_Input_Hold_To_Interact.md   # only if later deemed version-bound
  UE5_PCG_Tutorial/
    <any title-explicit 5.5 or 5.6 files elected to quarantine>
```

Use the existing `_MOC_UE5_Animation.md` as the model MOC. Mirror original category paths under `Legacy_` so reverse-linking remains obvious.

### Frontmatter annotation scheme (post-revamp, every note)

```yaml
---
title: "..."
ue_version: "5.8"        # changes from "5.7" / absent / "5.5" to canonical current target
status: current           # current | legacy | deprecated
source: "..."
workflow: research.pipeline   # or existing per-note workflow tag
tags:
  - ...
---
```

Optionally endorse a `status: provenance` for review/provenance docs (`_REVIEW_New_Tutorials.md`, review records) so vault indexers exclude them from “current” counts.

---

## 4. Repetitive / overlapping clusters to merge

### Cluster A: Packaging duplicates
- `Learn_to_Code_Blueprints/package_your_Unreal_Engine_5.7_project_and_share_it_with_everyone.md`
- `Step_by_Step_Guides/02_Packaging_Project.md`

Both cover the same packaging workflow. Keep `Step_by_Step_Guides/02_Packaging_Project.md` as canonical; retitle to “Package Your UE 5.8 Project.” Redirect the other note to the canonical target.

### Cluster B: RPG gameplay overlap
- `UE5_RPG_Framework/` episodes 02–14
- `Step_by_Step_Guides/05_RPG_Tutorial_02_Locomotion_Blendspace.md` through `14_RPG_Tutorial_10_Sword_Trace_Damage.md`

These are transcript-summary notes and rewritten step-by-step steps from the same series. Do **not** delete; make one the canonical workflow target and the other the related episode summary, with `see also` wikilinks.

### Cluster C: GAS overviews
- `UE5_GAS/02_GAS_Overview.md`
- `UE5_GAS/03_Full_Course.md`
- `UE5_GAS/04_GAS_UE5.5_2025.md`
- `UE5_GAS/05_GAS_Combat.md`

Merge the two 14-minute overviews into a slim UE5 current overview, keep the full course as the deep-dive target, and move `04_GAS_UE5.5_2025.md` to `Legacy_5.7_and_Earlier/UE5_GAS/` because it is bound to a legacy version.

### Cluster D: World Partition overlap
- `UE5_World_Partition/02_Creating_Open_World_Landscapes_with_Partitioning.md`
- `Blueprint_Fundamentals/` has a landscape/material pair of notes that overlap on landscape/material fundamentals.

Recommend constraining `Learn_to_Code_Blueprints/` landscape/material tutorials to “landscape only” and cross-link to `Step_by_Step_Guides/` or v1.3.0 topic refs for the materials slice.

### Cluster E: Topic-folder categories introduced in v1.1.0
Several categories are thin-spread with 2–4 files each. Consolidating deprecated-adjacent material into `Legacy_5.7_and_Earlier/` makes the topic folders cleaner.

---

## 5. Structural recommendations

| Item | Recommendation | Rationale / Evidence on Disk |
|---|---|---|
| `UE5_7_Starter_Course/` (21 files) | **Alias in index/MOC to 5.8, do NOT rename folder** | Renaming breaks wikilinks; alias preserves graph. Add frontmatter `ue_version: "5.8"` + `status: current`. |
| `Contrib/echoes-of-ascension-kit/` (11 files) | **Relocate out of tutorial vault** to a project repo or dedicated `Contrib/` vault; separate branch/workspace recommended | Contains design docs, eval harness, C++ starter module, Hermes skill. Not tutorial content; violates primary instruction/learning signal. |
| `Hermes/` + `templates/` | **Not present on disk**. If introduced later, gitignore + keep out of vault index | No current disk evidence; maintain policy of excluding tooling from tutorial index. |
| `Research/_incoming/` (1 file now) | **Move to `Research/` after revamp as provenance** | Current incoming folder does not show 4 files as brief claimed. Proceed with recovery of missing files from PR #1 / review artifacts before moving. |
| `Legacy_5.7_and_Earlier/` | **Expand as during-category quarantine** for version-bound notes | Disk already has `UE5_Animation/` subtree migrated there; 5 files on disk, model is proven. |

### True historical note vs stale error — explicit examples

| Source | Statement | Classification |
|---|---|---|
| `CHANGELOG.md` line 26 | `NonInstanced / InstancedPerExecution marked deprecated in UE 5.5+` | TRUE historical statement from 5.5; correct. Updating to 5.8 conventions means stating current default as `InstancedPerActor`. |
| `Articles/ue5-canonical-references.md` line 20 | “Epic — Understanding GAS (UE 5.7 docs)” | Valid stable reference, though label says 5.7. Recommend changing to “Epic — Understanding GAS” without explicit version, or to current page version. |
| `Contrib` guide | “ UE 5.7 C++ module … reviewed line-by-line against UE 5.7 APIs” | Correct historical framing; keep as-is but add a `source_version` field in frontmatter. |
| `UE5_PCG_Tutorial/title`s | “UE 5.5 / 5.6 / 5.7” titles | Stale error if still circulating as primary docs after audit. Keep notes but update frontmatter `ue_version: "5.8"` or move to `Legacy_` if version-bound. |
| `Step_by_Step_Guides/02_Packaging_Project.md` | “UE5.7 Project and Share It” | Stale version string. Correct to `5.8`. |

---

## 6. UNVERIFIED items needing upstream confirmation

These cannot be classified from disk evidence alone.

1. `Research/_incoming/OpenWorld_RPG_Tutorials.md` — claimed source range `UE 5.6 / 5.7 acceptable; < 5.5 rejected unless foundational`. File missing on disk.
2. `Research/_incoming/OpenWorld_RPG_Review.md` — claimed verified class list; file missing on disk.
3. `Research/_incoming/UE58_Review.md` — claimed 5.7 vs 5.8 usage accuracy confirmation; file missing on disk.
4. `Research/_incoming/UE58_API_Changes.md` — briefed as `status APPROVE_WITH_FIXES`; file missing on disk. On-disk replacement is `Research/_incoming/UE58_API_DeepSearch.md`.
5. `AGENTS.md` with `ue_version: "5.7"` — referenced in stale map; not present under current vault path. If it lives under another path outside workspace, confirm current `ue_version` for all active task/agent files.

Action: recover these files from prior PR artifacts / git history, then re-run classification using the procedure above.

---

## 7. Quick decision log

- Remaining analysis is bound to visible content, not speculation on missing reviews.
- No files were moved, renamed, or deleted per gate requirement.
- Next recommended action: update `Research/_incoming/curation_report.md` into approved state, then schedule category-wide frontmatter migration following the proposed `ue_version` / `status` scheme.
