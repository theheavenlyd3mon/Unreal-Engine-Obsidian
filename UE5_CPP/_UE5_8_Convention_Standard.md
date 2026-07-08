# UE 5.8 Convention Standard

> Status: `current`
> ue_version: `5.8`
> Last updated: 2026-07-08
> Primary source: [UE 5.8 Release Notes](https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5-8-release-notes?lang=en-US)

## 1. Purpose

This document is the single source of truth for the UE 5.8 convention revamp. It defines:
- the current 5.8 API/convention surface to treat as authoritative
- items deprecated or removed in 5.8
- the corrected UE_LOG guidance
- a reusable frontmatter/annotation template for revamped notes

Every claim below cites its source or is explicitly marked `UNVERIFIED`.

## 2. Authoritative 5.8 API / Convention Surface

### 2.1 Incremental Cooking + ZenServer cooked output store
- Incremental Cooking continues in beta for UE 5.8. [Release Notes, Developer Iteration]
- ZenServer as Cooked Output Store is enabled by default. [Release Notes, Developer Iteration]
- For remote devices, ZenServer requires a pre-generated authorization key. [Release Notes, Developer Iteration]
- Projects that had Zen store disabled will continue to use the old behavior until they enable the setting manually. [Release Notes, Developer Iteration]
- In `DefaultEngine.ini`, set `Zen.AutoLaunch|LimitProcessLifetime=false` so ZenServer is not restarted frequently. [Release Notes, Developer Iteration]
- Input config continuation: the `AllowRemoteNetworkService` config key was renamed to `RemoteNetworkService` and uses `None` / other values instead of true/false. [Release Notes, Developer Iteration]

### 2.2 Mass entity system overhaul
- Mass Signals are now core-engine, with archetype-based lock-free scheduling; entity creation off the game thread is supported. [Release Notes, Mass]
- A new sparse/virtual fragment system reduces memory use and supports optional fragments/tags without costly archetype changes. [Release Notes, Mass]
- Processor execution and dependency resolution were rewritten for better multi-core CPU usage, with thread-safe observer notifications. [Release Notes, Mass]
- `MassCore` is introduced as a separate module to reduce adoption surface vs the broader `MassGameplay` stack. [Release Notes, Mass]
- Mass Gameplay Debug: `AssignDebugVisProcessor` is editor-only. [Release Notes, Mass]

### 2.3 iOS Shader Model 6 (experimental)
- UE 5.8 adds experimental Shader Model 6 on iOS via Apple's Metal Shader Converter. [Release Notes, iOS/tvOS/iPadOS]
- Supported features: wave intrinsics and native 16-bit (FP16) shader types. [Release Notes, iOS/tvOS/iPadOS]
- Supported devices: A15 and newer Apple Silicon. [Release Notes, iOS/tvOS/iPadOS]
- Production use is not recommended; existing Metal paths remain for broader device coverage. [Release Notes, iOS/tvOS/iPadOS]

### 2.4 Windows GameInput packaging
- DefaultEngine.ini: `Game Input::IncludeRedistFiles=True` enables `GameInputRedist.msi` installation during `BootstrapPackagedGame`. [Release Notes, Windows]
- This is recommended for any packaged project using the Game Input for Windows plugin. [Release Notes, Windows]

### 2.5 UE_LOG status
- UE_LOG is **not deprecated** in 5.8. [Release Notes, Core]
- UE 5.8 release notes state: `UE_LOG ... will eventually be deprecated`; the migration target is `UE_LOGF`. [Release Notes, Core]
- `ConvertUELog.py` ships with the release to automate conversion. [Release Notes, Core]
- Implementation note: UE_LOG was internally converted to log records in 5.8 for richer context, but this does not imply deprecation. [Release Notes, Core]

## 3. DEPRECATED / NOT-IN-5.8 / REMOVED ITEMS

Use this section to decide legacy quarantine. Every entry cites a source; if no migration path is documented by Epic, that item is marked explicitly.

### 3.1 Input
- Raw Input plugin deprecated in favor of Game Input for Windows. Migration: use Game Input for Windows. [Release Notes, Gameplay/Input]
- Enhanced Input combo trigger deprecated; can corrupt mapping contexts in the editor. Migration: avoid combo trigger type; Epic does not document a replacement trigger. UNVERIFIED alternative. [Release Notes, Enhanced Input]
- `FInputDeviceScope` deprecated in favor of thread-safe `FInputDeviceRegistry`. [Release Notes, Input]

### 3.2 Core / Foundation
- `UE_LOG` is not deprecated in 5.8; see §2.5 for migration guidance. DO NOT list as removed here. [Release Notes, Core]
- `FCoreDelegates::OnPostEngineInit` deprecated in favor of `FCoreDelegates::GetOnPostEngineInit()`. [Release Notes, Core]
- `PLATFORM_ENABLE_POPCNT_INTRINSIC` and `FPlatformMisc::HasNonoptionalCPUFeatures()` / `NeedsNonoptionalCPUFeaturesCheck()` deprecated. [Release Notes, Core]
- `r.SkipRedundantTransformUpdate` and associated API deprecated and disabled. [Release Notes, Rendering/Core]
- UE4-style DDC functionality deprecated/no longer supported. [Release Notes, Core]
- `FPrimitiveSceneProxy` deprecated APIs removed or marked deprecated:
  - removed: `WritesVirtualTexture`, `GetNaniteResourceInfo`, `UpdateInstances_RenderThread`, `GetDistanceFieldInstanceData`
  - deprecated: `OnDetachLight`
  [Release Notes, Core]
- `GetLastTickGameTime` deprecated because of confusing semantics. [Release Notes, Gameplay]
- `FNodeClassMetadata::DefaultInterface` accepts `FClassInterface` directly; previous `FVertexInterface` input-output node creation helpers removed from `IDataTypeRegistry`. [Release Notes, MetaSound/Animation]
- `CheckEnsureFailed` renaming note: `ExecCheckImplInternal` renamed to `CheckEnsureFailed` for ensure behavior. [Release Notes, Core]

### 3.3 Animation / Control Rig / Rig VM
- `FRigControlElement::Settings` direct Blueprint access deprecated. Migration: use `GetControlSettings(Key)`. [Release Notes, Control Rig]
- 5.6-deprecated PoseSearch methods removed. [Release Notes, Animation]
- PoseSearch channel helpers deprecated in favor of `...FromContext` variants:
  - `BP_GetCurveValue`
  - `BP_GetWorldRotation`
  - `BP_GetWorldVelocity`
  - `BP_GetWorldPosition`
  [Release Notes, Animation]
- Removed deprecated `USkeleton` functions:
  - `GetSkeletonRemapping`
  - `GetAssetRegistryTags`
  - `CollectAnimationNotifies`
  - `GetRawAnimationTrackIndex`
  [Release Notes, Animation]
- Non-reflected `UE_DEPRECATED` items removed from UAF, RigVM, Motion Warping, MLDeformer, and animation runtime up to 5.6-deprecated symbols. [Release Notes, Animation]

### 3.4 Rendering / RHI / Platform
- Path Tracer `EnableBackfaceCulling` cvar removed; backface culling now defaults to on. [Release Notes, Path Tracer]
- Unreal Editor rendering support removed for Intel-based Macs. Non-rendering processes like cooking still run on Intel-based Macs. [Release Notes, Mac]

### 3.5 Platform / Mobile / XR
- Android Graphics Debugger entry in Project Settings deprecated because the referenced tools are deprecated/unavailable. [Release Notes, Android]
- OpenXR `PackageForOculusMobile` removed long ago; replaced by `bPackageForMetaQuest` in previous versions. [Release Notes, XR/OpenXR]
- Windows Mixed Reality Bindings removed from VR Template. [Release Notes, VR/XR]

### 3.6 Worldbuilding / Geometry
- LightWeightInstances code deprecated. [Release Notes, Worldbuilding]
- Experimental light gizmo plugin removed. [Release Notes, Geometry/Level Design]
- Experimental gizmo option removed from level editor viewport; migrated to gizmo settings/profiles. [Release Notes, Geometry/Level Design]

### 3.7 Simulation / Physics / Cloth
- Cloth direct collision extraction deprecated:
  - `FClothingSimulationInstance::AppendSimulationData`
  - `USkeletalMeshComponent::FindClothCollisions`
  [Release Notes, Cloth]
- Chaos Flesh: `StaticMesh` property on the Chaos Flesh asset deprecated. [Release Notes, Simulation]

### 3.8 Media / Compositing
- `UCompositePassColorGrade` renamed to `UCompositePassColorGrading`. [Release Notes, Compositing]

### 3.9 Audio / Subtitles
- `QueueSubtitle` deprecated. Migration: use `QueueSingleSubtitle`; `QueueSubtitlesFromAsset` queues all lines in one call. [Release Notes, Audio/Subtitles]

### 3.10 NNE / AI
- `NNERuntimeORTDml` NPU inference path: after upgrade `GetRuntime("NNERuntimeORTDml")` will not return an `INNERuntimeNPU` proxy; `CanCreateModelNPU` / `CreateModelNPU` are not callable. Migration: use GPU or RDG execution paths. [Release Notes, AI/ML]
- IREE runtime/tools upgraded to 3.11.0; rewarm compiled-model cache after upgrade. [Release Notes, AI/ML]

## 4. Frontmatter / Annotation Template (CANONICAL — single source of truth)

All revamped notes use this exact schema. Do not rename fields. This supersedes the T0 curation proposal (§3) and any per-note variants already written (e.g. `verified` / `ue_version_source` on `Learn_to_Code_Blueprints/_MOC`).

```yaml
---
ue_version: "5.8"            # canonical target; change from 5.7 / absent / 5.5
status: current | legacy | deprecated
category: <notes|notes-legacy|tutorials|...>
source: "<path or URL to evidence: Release Notes section / official doc / derived-from: canonical standard note>"
revamped_at: YYYY-MM-DD
# --- optional, only for legacy / deprecated notes ---
deprecated_symbols: []       # removed/deprecated symbols named in the note
migration_hint: ""           # one-line pointer to the 5.8 replacement
historical_notes: []         # version-bound context worth keeping
---
```

Field reconciliation (so existing notes line up without a rewrite):
- `source_check` (T1b draft) and `ue_version_source` (LTCB MOC) → both renamed to `source`.
- `verified` (LTCB MOC) → dropped; provenance lives in `source`.
- `category` + `revamped_at` (T1b draft) → added to every note.
- `deprecated_symbols`, `migration_hint`, `historical_notes` (LTCB MOC) → retained as optional fields.

Annotation rules for each value of `status`:
- `current`: the note describes behavior supported in 5.8.
- `legacy`: behavior accepted in 5.8 but superseded; say why in the note body and link the replacement when known.
- `deprecated`: the API/pattern is deprecated in 5.8; add a `>` block in the note body quoting the exact migration guidance from §3 so a later worker can upgrade without re-reading the standard.

## 5. Unverified / Missing-Inputs Note

This document was generated from `/Users/noctis/Documents/Unreal-Engine-Obsidian/Research/_incoming/UE58_API_DeepSearch.md`. The other task-inputs referenced by the kanban task are not present in the workspace:
- `Research/_incoming/UE58_API_Changes.md`
- `Research/_incoming/UE58_Review.md`

If those files are located later, re-open this document and add `UNVERIFIED` resolutions as sourced facts before treating any gap as settled.

## 6. Summary for Revamp Workers

For a normal category revamp:
1. Read this doc and the current Release Notes section for the relevant subsystem.
2. Apply the frontmatter template from §4 to every note.
3. Set `status=current` unless §3 or your subsystem section includes your exact item.
4. If quarantining, move the note to a `legacy` subfolder and set `status=legacy`; link back to the canonical replacement evidence.
5. If your item is deprecated in 5.8, set `status=deprecated` and include the exact migration quote in the body.
