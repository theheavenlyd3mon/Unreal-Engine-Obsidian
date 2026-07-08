# UE 5.8 Upgrade Brief — API, Conventions & Changes vs 5.7

> Purpose: drive a vault-wide convention/API update from UE 5.7 → UE 5.8.
> Prepared: 2026-07-08. Source of truth: Epic's official UE 5.8 Release Notes, launch
> announcement, and release forum thread (all cited inline).
>
> Honesty note: Every API-level claim below is traced to Epic's official Upgrade Notes /
> API Change blocks in the 5.8 Release Notes. Where a specific symbol could not be
> verified against a primary source, it is flagged [UNVERIFIED].

## UE 5.8 Status

- **Released and publicly available.** UE 5.8 shipped on June 17, 2026 via the Epic Games
  Launcher, GitHub, and the Linux page. [Source: release forum announcement]
  https://forums.unrealengine.com/t/unreal-engine-5-8-released/2729274
- **Last planned major UE5 release.** Epic has stated that UE 5.8 is the final major UE5 release on
  the roadmap as they ramp up UE6; UE5 continues to receive bug-fix/regression support.
  [Source: launch announcement]
  https://www.unrealengine.com/news/unreal-engine-5-8-is-now-available
- **Official documentation exists.** Full Release Notes, a "What's New" page, and
  per-area Upgrade Notes / API Change blocks are published.
  [Source: Release Notes] https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5-8-release-notes
  [Source: What's New] https://dev.epicgames.com/documentation/unreal-engine/whats-new
- **No dedicated "5.7 → 5.8 Migration Guide" page.** The legacy UE5 Migration Guide covers
  UE4→UE5 only and has NOT been extended to sequential UE5.x upgrades. The authoritative
  migration surface for 5.8 is the **Upgrade Notes** section embedded in the Release Notes
  (every subsystem that changed carries an "Upgrade Notes" and/or "API Change" block).
  [Source: UE5 Migration Guide — still UE4→UE5 only]
  https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5-migration-guide
- **Practical upgrade reports.** Community reports describe upgrading as "fairly trivial
  unless you modified source or used experimental C++." Treat experimental/Beta systems as
  the real risk surface. [Source: Reddit upgrade thread]
  https://www.reddit.com/r/UnrealEngine5/comments/1rj6zqp/upgrading_engine_to_58/

## API Changes

Format: symbol/area | change | from-version | notes
Sources: Release Notes Upgrade Notes + API Change blocks
(https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5-8-release-notes),
referenced per-row by section.

### Build / Core / Platform macros

| Symbol / Area | Change | From | Notes |
|---|---|---|---|
| `UhtSpecifierValueType.Legacy` | Obsolete → use `UhtSpecifierValueType.None` | 5.8 | UHT specifier value enum [Build/API Change] |
| `UE_PLATFORM_*` defines | Added to mirror `PLATFORM_*`; prefer in new code | 5.8 | `PLATFORM_IOS` can be stomped by iOS framework headers → compile bugs. Opt-in migration `#if PLATFORM_*` → `#if UE_PLATFORM_*` [Foundation/Build Upgrade Notes] |
| `FSharedEventRef` | Constructor `EEventMode::ManualReset` now honored (was always AutoReset) | 5.8 | Check callsites for behavior change [Core Upgrade Notes] |
| `ExecCheckImplInternal` | Renamed → `CheckEnsureFailed` | 5.8 | Naming clarity (ensures, not checks) [Core API Change] |
| `LexToString(bool)` overload | No longer hijacks types that implicitly cast to bool | 5.8 | Missing/ambiguous `LexToString` now fails at compile time [Core API Change] |
|| `UE_LOG` family | Migration target: prefer `UE_LOGF` (UTF-8 format strings) | 5.8 | `ConvertUELog.py` ships to auto-upgrade most uses [Core Upgrade Notes]
| Intel OneAPI supported version | Bumped to 2026.0.0 | 5.8 | Build toolchain [Build New] |
| `-SkipEncryption` for IoStore | Added support | 5.8 | Build/package [Build New] |
| `TargetRules.bEnableConfigSystem` | Added (disable config loading) | 5.8 | [Core New] |
| `PluginOverride.ini` | New opt-in ini applied after plugin configs, before GFPs/Hotfixes | 5.8 | Project/Config/PluginOverrideEngine.ini [Core New] |

### Animation / Rigging (largest deprecation surface)

| Symbol / Area | Change | From | Notes |
|---|---|---|---|
| `FSmartName` family | Deprecated throughout; curve access moves to `FAnimationCurveIdentifier` + name-based APIs | 5.8 | Backing `FSmartNameContainer` payload drained on load via custom version `FUE5ReleaseStreamObjectVersion::RemovedSmartNameContainerPayload`. Skeleton.h `SmartNames_DEPRECATED`, PoseAsset.h `PoseNames_DEPRECATED`, AnimCurveTypes.h `Name_DEPRECATED` migrated [Animation Runtime API Change] |
| `USkeleton` | Removed deprecated funcs: `GetSkeletonRemapping`, `GetAssetRegistryTags`, `CollectAnimationNotifies`, `GetRawAnimationTrackIndex` | 5.6 (removed in 5.8) | "Cleaned deprecated methods" pass [Release Notes Animation] |
| `URigHierarchy::FindBone/FindControl/FindNull` + direct `Index/SubIndex/bSelected/Settings` | Deprecated in Blueprint; use `Contains(Key)`, `GetBoneType(Key)`, `GetControlSettings(Key)`, `IsSelected(Key)`, `GetIndex(Key)/GetLocalIndex(Key)` | 5.8 | Existing BP graphs keep working with deprecation warnings [Control Rig Upgrade Notes] |
| `FRigControlElement::Settings` | Direct BP access deprecated → `GetControlSettings(Key)` is migration target | 5.8 | [Release Notes Animation] |
| `GetCharacterOwner` (UMotionWarpingComponent/URootMotionModifier) | Removed (was 5.5-deprecated); replace `GetOwnerAdapter()->GetActor()/GetActorOwner()` | 5.5 | [Control Rig API Change] |
| `UMovieSceneControlRigParameterSection` | Removed non-reflected deprecated overloads (`LoadAnimSequenceIntoThisSection`, `GetControlsMask`, etc.) | 5.5–5.6 | [Control Rig API Change] |
| `PropertyAccessCompilerHandler` (class) | Deleted whole → replaced by `UAnimBlueprintExtension_PropertyAccess` | 5.0 | [Animation Runtime API Change] |
| `AnimCompressionDerivedDataPublic.h` | Deleted whole (FAsyncCompressedAnimationsManagement, GAsyncCompressedAnimationsTracker, RequestAsyncCompression, …) | 5.2 | [Animation Runtime API Change] |
| `FCompressibleAnimData::NumberOfFrames`, `ICompressedAnimData::CompressedNumberOfFrames`, `FCompressedAnimSequence::CompressedCurveNames`, free `DecompressPose` overloads | Removed | 5.0–5.3 | [Animation Runtime API Change] |
| `Persona` editor APIs (IEditableSkeleton 8 SmartName virtuals, IPersonaPreviewScene, PersonaModule, IAnimSequenceCurveEditor, etc.) | Removed non-reflected UE_DEPRECATED items | 5.0–5.6 | Full list in Upgrade Notes [Animation API Change] |
| `AnimAssetFindReplace` `RequestUIRefresh`; `AnimationEditorViewportClient` `Set/GetCustomAnimationSpeed`, `Set/GetPlaybackSpeedMode`, `GetPersonaModeManager`; `BlendSpaceAnalysis` 10 static template overloads | Removed | 5.3–5.6 | [Animation API Change] |
| `IAnimBlueprintCompilerHandler.h` + `IAnimBlueprintCompilerHandlerCollection.h` | Deleted whole (empty base classes) | 5.0 | Replaced by `UAnimBlueprintExtension_PropertyAccess` [Animation Runtime API Change] |
| LiveLink deprecated items (`ULiveLinkControllerBase::AttachedComponent`, `GetPresetSaveDir`, `FLiveLinkSourceCollection::GetSources/GetSubjects`, `FLiveLinkSubject::PreprocessFrame`, `ILiveLinkHubModule::PreinitializeLiveLinkHub/StartLiveLinkHub/ShutdownLiveLinkHub`, …) | Removed | 5.1–5.6 | [Animation Runtime API Change] |
| `a.AnimSequence.UseBinaryDDCKey` | New CVar, opt-in (default off) | 5.8 | [Animation Runtime Upgrade Notes] |

### Input / Gameplay

| Symbol / Area | Change | From | Notes |
|---|---|---|---|
| `FInputDeviceScope` | Deprecated → use `FInputDeviceRegistry` (thread-safe) | 5.8 | Set `UE_USE_LEGACY_INPUT_DEVICE_SCOPE=1` in Target.cs to keep legacy [Gameplay API Change / Input] |
| Raw Input plugin | Deprecated in favor of "Game Input for Windows" plugin | 5.8 | [Gameplay Upgrade Notes] |
| `EnhancedInput.IgnoreHeldKeysOnFlush` | New CVar (default True); will be removed later | 5.8 | Behavior fix behind flag [Gameplay Upgrade Notes] |
| `EnhancedInput.CorrectTouchBoolActionKeys` | New CVar (default on) | 5.8 | Fixes broken touch bool action keys [Gameplay Upgrade Notes] |
| `FActiveGameplayEffectHandle(int32)` | Constructor deprecated → `GetInstantExecutedHandle()` | 5.7 | `FGameplayEffectRemovalInfo` now holds pointer to owning ASC. Source: RN Framework/Gameplay API Change. |
| `FActiveGameplayEffectHandle` (ownership) | Now holds a reference to its owning `UAbilitySystemComponent` instead of a global map | 5.7 | Same change as the int32-ctor removal; enables parts of ASC to work with object migrations and multi-server proxies. Source: RN GameplayAbilitySystem Release Notes (`FActiveGameplayEffectHandle now holds a reference to its Owning AbilitySystemComponent rather than using a Global Map`). |
| `UAdditionalEffectsGameplayEffectComponent::OnApplicationGameplayEffects` | New `RemovalPolicy` (`EGameplayEffectGrantedEffectRemovalPolicy`) | 5.8 (new) | Controls lifetime of granted GEs: `GrantedEffectControlsOwnLifetime`, `RemoveGrantedEffectOnEnd`. Content validation errors if `RemoveGrantedEffectOnEnd` is used with an Instant owning GE or an Instant granted GE. Source: RN GameplayAbilitySystem Release Notes. |
| `UInputTriggerCombo` (Enhanced Input combo trigger) | Deprecated | 5.8 | Unreliable and can corrupt mapping contexts in the editor; migrate away from the combo trigger. [Source: RN Enhanced Input Release Notes — "Deprecate the combo trigger"] |
| PhysicsMover / NetworkPhysicsLiaison (Mover plugin) | Removed → use ChaosMover plugin | 5.8 | Equivalent functionality ported [Gameplay Upgrade Notes] |
| FloorQueryUtil functions | Migrate to `FFloorCheckSettings` variants | 5.8 | [Gameplay Upgrade Notes] |
| `bEnablePreferredInputAPIPreferences` (input project settings) | New flag + preferred input API list | 5.8 | [Gameplay API Change] |

### Audio / MetaSounds

| Symbol / Area | Change | From | Notes |
|---|---|---|---|
| `UFadeFunction`, `FFadeFunctionData`, `EWaveEditorFadeMode` | Deprecated → `UTransformationFadeFunction`, `UWaveformTransformationFade` | 5.8 | [WaveForm Upgrade Notes] |
| `au.EnableRelativeRenderCostVoiceLimit` | Enabled by default | 5.8 | Voice count now weighted by relative render cost (matters for MetaSounds) [MetaSounds API Change] |
| `QueueSubtitle` | Deprecated → `QueueSingleSubtitle` (+ `QueueSubtitlesFromAsset`) | 5.8 | Subtitles Beta [Audio] |
| WASAPI audio backend | Default Windows backend switched XAudio2 → `AudioMixerWasapi` module (XAudio2 opt-in fallback) | 5.8 | No dev action; XAudio2 to be removed later [Audio] |
| Convolution reverb | Now software convolution by default | 5.8 | [Audio API Change] |

### Networking / Iris

| Symbol / Area | Change | From | Notes |
|---|---|---|---|
| `ResetLifetimeConditionDebugNames`, `OnResetPersistentNetDebugNames` | Removed from Iris Net Trace API | 5.8 | Broke TailBuffer traces [Networking API Change] |
| `ESubObjectInsertionOrder::ReplicateWith` | Deprecated → specify root/parent explicitly when adding subobject | 5.8 | [Networking API Change] |
| `UE_SUPPORT_PARALLEL_IRIS` | New define (default 1); set 0 to compile out parallel-replication primitives | 5.8 | [Networking API Change] |
| Iris replication system | Production-Ready for licensees | 5.8 | RPC DoS detection re-enabled; protocol-mismatch handling improved [Framework] |

### MetaHuman

| Symbol / Area | Change | From | Notes |
|---|---|---|---|
| `FRigLogicConfiguration::CalculationType`, `::RotationOrder` | Deprecated; migrated on load to `CalculationTypePerPlatform.Default` / DNA-authored rotation | 5.8 | Code should use `CalculationTypePerPlatform.GetValueForPlatform(...)` / `Reader->GetConfig().RotationSequence` [MetaHuman Upgrade Notes] |
| `UDNA::bUseOptimizedCooking` | New opt-in (default true on UDNA) | 5.8 | Projects must re-cook [MetaHuman Upgrade Notes] |
| DNA asset layout migration | Run `ConvertLegacyDNAAssets` commandlet once per project | 5.8 | `-DryRun` / `-ReimportFromSource` supported, idempotent [MetaHuman Upgrade Notes] |
| `UDNA::DNAConfig` | New `FDNAConfig` UPROPERTY (EditAnywhere) | 5.8 | Edits destructive [MetaHuman API Change] |
| `FActiveGameplayEffectHandle`, GAS, Mover, etc. | see above rows | — | — |

### Framework / Editor / Scripting / Misc

| Symbol / Area | Change | From | Notes |
|---|---|---|---|
| `FClassInterface` | Exits experimental; `FNodeClassMetadata::DefaultInterface` now takes `FClassInterface` (replaces `FVertexInterface`); deprecated node-creation helpers removed from `IDataTypeRegistry` | 5.8 | MetaSound Node Configuration stable API [Audio] |
| `K2Node::GetBlueprint` | May now return null; `GetBlueprintChecked` added for old behavior | 5.8 | [Blueprint API Change] |
| `BlueprintGraphEditor` / `BlueprintEditorLibrary` | New Python/BP scripting APIs for editing Blueprint graphs | 5.8 | [Blueprint New] |
| Python `ufunction` packed return values | Must now pack in declared order (was reversed) | 5.8 | e.g. `return (10,"hello")` not `("hello",10)` [Scripting API Change] |
| `UAssetActionUtility` / `UActorActionUtility` `SupportedClasses` | Now required (empty ⇒ data validation error) | 5.8 | Add UObject/AActor for global actions [Scripting Upgrade Notes] |
| `TSubScriptStructOf<T>` | New (like `TSubClassOf` but for `UScriptStruct`) + editor picker | 5.8 | [Core New] |
| `MoveAssignScriptStruct` / `STRUCT_MoveAssignNative` | Added move-semantic support for `UScriptStruct` | 5.8 | [Core New] |
| `FField` virtuals `Bind()`, `PostLoad()`, `BeginDestroy()` | Deprecated & removed (never called) | 5.8 | [Core] |
| `TSet`/`TMap` compact-set swap | `bUseCompactSetAsDefault` BuildConfiguration option | 5.8 | `TCompact[Map|Set]`/`TSparse[Map|Set]` still exist; explicit forms can't be UPROPERTYs [Core] |
| Editor Gizmo System | New unified gizmo framework (Interactive Tools Framework); legacy gizmos consolidated | 5.8 | Convention change for editor tooling [Editor] |
| Slate `OnlyGameWindow` cvars / `bDebugGameWindowOnly` | Renamed → `OnlyProjectContent` / `bDebugProjectContentOnly` | 5.8 | Override `SetIsProjectContent`/`SetIsProjectContentParent`; use `EWindowType::Normal` not `GameWindow` [Slate Upgrade Notes] |
| Celestial Vault actor | Component hierarchy changed; replace existing instances | 5.8 | [World Building Upgrade Notes] |
| `R.Water.SingleLayer.ForceVelocity` | Deprecated → `R.Water.SingleLayer.VelocityOutputPass` (or project setting) | 5.8 | [Rendering Upgrade Notes] |
| `r.Lumen.HeightFog` | Default 1 (Lumen applies height fog to reflection ray hits) | 5.8 | [Lumen Upgrade Notes] |
| Subsurface Profile `r.SSProfiles.Transmission.UseLegacy=0` | Must manually reduce new `transmission distance scale` by 10 to match old behavior | 5.8 | [Materials Upgrade Notes] |
| `D3D12.ResourcesStartResident` | New read-only CVar (default Off) reduces VRAM for unreferenced resources | 5.8 | [RHI API Change] |
| Android Google Play `IsAllowedToPurchase` | Deprecated for init check → cast to `FOnlinePurchaseGooglePlay`, use `IsBillingClientConnected()` | 5.8 | [Online Subsystem Upgrade Notes] |
| Pixel Streaming `AllowedOrigins` | Set `*` to allow all, or empty for old behavior | 5.8 | [Pixel Streaming Upgrade Notes] |
| Windows `Game Input::IncludeRedistFiles=True` | Required in DefaultEngine.ini to package GameInputRedist.msi | 5.8 | [Platform/Windows Upgrade Notes] |
| Mobile "Use Half Precision" material override | Reverts to Default to preserve prior behavior (logged) | 5.8 | [Mobile Rendering Upgrade Notes] |

## Convention Changes

- **Editor Gizmo consolidation.** A single unified Editor Gizmo System (built on the
  Interactive Tools Framework) replaces multiple legacy gizmo implementations across
  viewports/tools. Tool developers should target the new framework. [Source: Editor/Gizmo]
  https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5-8-release-notes
- **Platform macro hygiene.** New `UE_PLATFORM_*` macros mirror `PLATFORM_*`; Epic
  recommends migrating conditional compilation to `UE_PLATFORM_*` to avoid iOS header
  collisions. [Source: Foundation/Build Upgrade Notes] (same URL)
- **Logging convention shift.** `UE_LOG` → `UE_LOGF` with UTF-8 format strings; Epic provides a `ConvertUELog.py` script to automate most migrations. Current notes describe this as the migration recommendation/target, not a confirmed hard deprecation; keep using `UE_LOG` where broader compatibility or uncited deprecation text is required. [Source: Core Upgrade Notes] (same URL)
- **Unified Input conventions.** Enhanced Input and Common Input/UI are unified; duplicate
  data assets are no longer needed. Prefer the new "Game Input for Windows" plugin over the
  deprecated Raw Input plugin. [Source: Framework — Unified Input]
  (same URL)
- **DDC configuration relocation.** Derived Data Cache graphs/stores are now configured in
  `[DerivedDataCacheGraphs]` / `[DerivedDataCacheStores]` Engine config sections; deprecated
  `AsyncPut`, `KeyLength`, `Verify` graph nodes. [Source: Core Upgrade Notes] (same URL)
- **Settings UI unification.** Editor Preferences, Project Settings, and plugin settings now
  share consistent styling/layout; CVar influence is visible in search. [Source: Editor
  Preferences] (same URL)
- **MetaSound API stabilization.** `FClassInterface` is now the stable public node-configuration
  surface (replaces `FVertexInterface` for `FNodeClassMetadata::DefaultInterface`).
  [Source: Audio/MetaSound] (same URL)
- **Coding-standard / naming.** `SDraggableBoxOverlay.IsDraggable`→`Draggable`,
  `RestoreFromDragBoxPosition`→`SetDragBoxPosition` deprecated to match conventions;
  `ExecCheckImplInternal`→`CheckEnsureFailed`. [Source: UI / Core API Change] (same URL)

## Breaking Changes & Migration

Ordered by likely impact for an RPG codebase standardized on UE 5.7.

1. **Animation `FSmartName` deprecation (highest surface).** Curve/skeleton code using
   `FSmartName`, `FindSmartName*`, `RetrieveSmartNameForCurve`, `Fill*Array`,
   `USkeleton::Get*AnimationTrack*` and the removed `AnimCompressionDerivedDataPublic.h`
   symbols will fail to compile. Migration: move to `FAnimationCurveIdentifier` /
   name-based APIs. Load path auto-drains legacy `FSmartNameContainer` payload; new saves
   skip it. [Source: Animation Runtime API Change] (Release Notes URL)
2. **Input: `FInputDeviceScope` → `FInputDeviceRegistry`.** Any C++ wrapping events in
   `FInputDeviceScope` must migrate; set `UE_USE_LEGACY_INPUT_DEVICE_SCOPE=1` in Target.cs for
   temporary compat. Raw Input plugin deprecated. Also: Enhanced Input **combo trigger**
   (`UInputTriggerCombo`) deprecated (unreliable, can corrupt mapping contexts) — migrate away.
   [Source: Gameplay/Input API Change + Enhanced Input Release Notes] (same URL)
3. **GAS handle construction.** `FActiveGameplayEffectHandle(int32)` ctor deprecated →
   `GetInstantExecutedHandle`; `FGameplayEffectRemovalInfo` now carries owning-ASC pointer.
   Separately, `FActiveGameplayEffectHandle` now references its owning `UAbilitySystemComponent`
   (not a global map), and `UAdditionalEffectsGameplayEffectComponent` gains
   `RemovalPolicy` (`RemoveGrantedEffectOnEnd`) for controlling granted-GE lifetime.
   [Source: Gameplay API Change / GAS Release Notes] (same URL)
4. **Mover: PhysicsMover/NetworkPhysicsLiaison removed.** Migrate to ChaosMover plugin.
   [Source: Gameplay Upgrade Notes] (same URL)
5. **Python `ufunction` return packing order reversed.** Packed tuple returns must follow
   declared order. [Source: Scripting API Change] (same URL)
6. **Blueprint local vs member variable name collision.** Now a validation error source;
   fix existing collisions manually. [Source: Blueprint Upgrade Notes] (same URL)
7. **Control Rig Blueprint deprecations.** `FindBone/FindControl/FindNull` and direct element
   struct field access deprecated in BP; use the new getter functions. [Source: Control Rig
   Upgrade Notes] (same URL)
8. **MetaHuman DNA.** Run `ConvertLegacyDNAAssets` once per project; re-cook for
   `bUseOptimizedCooking`. `FRigLogicConfiguration::CalculationType/RotationOrder` deprecated.
   [Source: MetaHuman Upgrade Notes] (same URL)
9. **Audio backend default change (Windows).** WASAPI is now default; XAudio2 opt-in. No code
   change, but audio-device behavior may differ. [Source: Audio] (same URL)
10. **Renderer defaults changed.** Lumen height-fog on by default (`r.Lumen.HeightFog 1`);
    Subsurface Profile transmission scale needs manual ×0.1 if `UseLegacy=0` was set;
    Water velocity CVar renamed. Expect visual-delTA, not compile errors.
    [Source: Lumen / Materials / Rendering Upgrade Notes] (same URL)
11. **Slate window-type conventions.** `OnlyGameWindow`→`OnlyProjectContent`;
    `EWindowType::GameWindow`→`EWindowType::Normal`; override `SetIsProjectContent*`.
    [Source: Slate Upgrade Notes] (same URL)
12. **Celestial Vault actor hierarchy changed.** Replace existing instances in levels.
    [Source: World Building Upgrade Notes] (same URL)
13. **`FSharedEventRef` ManualReset now honored.** Verify event-reset semantics at callsites.
    [Source: Core Upgrade Notes] (same URL)
14. **`LexToString(bool)` implicit-cast hijack removed.** Ambiguous overloads now fail to
    compile; add explicit `LexToString` or casts. [Source: Core API Change] (same URL)
15. **No sequential UE5.x Migration Guide.** There is no official 5.7→5.8 step-by-step page;
    rely on the Release Notes Upgrade Notes blocks + Lyra upgrade guidance.
    [Source: UE5 Migration Guide, Lyra upgrade doc]
    https://dev.epicgames.com/documentation/unreal-engine/upgrading-the-lyra-starter-game-to-the-latest-engine-release-in-unreal-engine

## New Systems

Experimental / Beta / Production-Ready status noted (relevant to RPG vault conventions):
[Source: launch announcement + Release Notes, URLs above]

- **Incremental Cooking (Beta)** + **ZenServer as cooked output store (default on)**.
- **Mass entity-system scheduler rewrite.** `MassCore` now handles off-game-thread entity
  creation, sparse/virtual fragments, and rewritten processor scheduling.
- **iOS Shader Model 6 (Experimental)** via Metal Shader Converter.
- **Windows Game Input redist packaging.** Set `Game Input::IncludeRedistFiles=True` in
  `DefaultEngine.ini` to package `GameInputRedist.msi`.
- **Mesh Terrain (Experimental)** — true 3D-mesh terrain (overhangs, caves, floating islands),
  non-destructive modifiers, fully World Partition / OFPA interoperable, PCG-compatible.
  Potential long-term replacement for heightfield Landscape.
- **Procedural Vegetation Editor / PVE (Experimental)** — grow Nanite-ready, biologically
  correct vegetation in-editor; PCG embedded subgraphs for custom artist tools.
- **PCG framework upgrades** — non-destructive manual editing atop procedural output, complex
  attribute types (arrays/structs/sets/maps), embedded subgraphs, Graph Parameters Editor.
- **MegaLights (Production-Ready)** — many dynamic shadowed area lights, reduced noise, 60fps
  console target, new debug/optimization tooling.
- **Lumen Lite (Beta)** — medium-quality GI via Irradiance Fields + Probe Occlusion; ~2× faster
  than Lumen HQ; default on current-gen handhelds, 60fps; also PC.
- **Fog Screen Space Scattering / FSSS (Experimental)** — multi-light scattering in Exponential
  Height Fog / Local Fog Volumes.
- **Substrate Toon Shading (Experimental)** — NPR/stylized shading on Substrate; Toon BSDF +
  Toon Profile asset; ramps, hatching, anisotropic specular, GI scale.
- **Control Rig Physics (Beta)** + **Control Rig Dynamics** — particle-based runtime solver
  (~5× original speed); modular/layered physics rigs.
- **Direct Mesh Controls / DMC (Experimental)** — rig controls on the skeletal mesh surface
  (facial animation).
- **Dataflow (Production-Ready)** + **Chaos Cloth Panel Editor (Production-Ready)** — node-based
  physics asset authoring; non-destructive Chaos Destruction; panel-driven cloth.
- **MetaHuman Collections (Experimental)** + **MetaHuman Crowds** — scalable crowds (tens→thousands)
  via Mass + Nanite, ISKM LOD fallback by camera distance.
- **Mesh to MetaHuman (full body conform)** + **MetaHuman Animator markerless (body+face)**.
- **Live Link Hub (Production-Ready)**, **Mocap Manager (Beta)**, **Movie Render Graph
  (Production-Ready)** + Accumulation Depth of Field, nDisplay-in-Graph.
- **Iris replication (Production-Ready)**; **Mass overhaul** (MassCore module, off-game-thread
  entity creation, sparse/virtual fragments, rewritten processor scheduling).
- **Unified Input (Enhanced + Common Input/UI)**; **Mover/ChaosMover** broad update.
- **Incremental Cooking (Beta)** + **ZenServer as cooked output store (default on)**.
- **MCP (Model Context Protocol) plugin (Experimental)** — connect LLM agents to the editor
  (assets, Blueprints, materials, meshes, levels). Relevant to your research-pipeline tooling.
- **Sandboxes (Experimental)** — isolated workspaces with selective merge back to main project.
- **X-Rite AXF materials as Substrate**, **Fast Geometry Streaming** improvements,
  **Mobile**: automated Android SDK setup, Unreal Engine Remote app, faster cook times,
  **iOS Shader Model 6 (Experimental)** via Metal Shader Converter.

## Sources

1. UE 5.8 Release (forum announcement, Jun 17 2026)
   https://forums.unrealengine.com/t/unreal-engine-5-8-released/2729274
2. Unreal Engine 5.8 is now available (launch announcement)
   https://www.unrealengine.com/news/unreal-engine-5-8-is-now-available
3. Unreal Engine 5.8 Release Notes (primary source for all API/Upgrade/New-System claims)
   https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5-8-release-notes
4. What's New | UE 5.8 Documentation
   https://dev.epicgames.com/documentation/unreal-engine/whats-new
5. Unreal Engine 5 Migration Guide (note: UE4→UE5 only, no 5.7→5.8 page)
   https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5-migration-guide
6. Upgrading the Lyra Starter Game to the latest engine release
   https://dev.epicgames.com/documentation/unreal-engine/upgrading-the-lyra-starter-game-to-the-latest-engine-release-in-unreal-engine
7. Community upgrade report (Reddit, "fairly trivial unless source/experimental C++ modified")
   https://www.reddit.com/r/UnrealEngine5/comments/1rj6zqp/upgrading_engine_to_58/
8. MetaHuman 5.8 Release Notes / Known Issues
   https://dev.epicgames.com/documentation/metahuman/metahuman-5-8-release-notes-in-unreal-engine
   https://dev.epicgames.com/documentation/metahuman/metahuman-known-issues-5-8-in-unreal-engine

### Verification gaps / caveats

- No dedicated 5.7→5.8 Migration Guide page exists; migration guidance is distributed across
  the Release Notes "Upgrade Notes" blocks (cited above). [UNVERIFIED: any 3rd-party
  migration tool beyond Lyra guidance.]
- Symbol-level removals listed under Animation are taken verbatim from Epic's Upgrade Notes;
  they reflect non-reflected, non-virtual symbols past the 2-version grace window. If your
  RPG codebase does not reference these internals directly, compile impact is limited to
  public deprecations (FSmartName, FInputDeviceScope, FActiveGameplayEffectHandle, Control
  Rig BP accessors).
- Experimental/Beta systems should NOT be treated as vault conventions yet; document them as
  "preview" until they reach Production-Ready.
