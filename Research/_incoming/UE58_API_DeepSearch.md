# UE 5.8 API & Convention Deep Search — Confirmed Facts, Deprecations, and Unverified Items

Generated: 2026-07-08
Scope: 6-point bounded deep search of the UE 5.8 API / convention surface.
Primary source: Unreal Engine 5.8 Release Notes (official Epic Developer Community)
  https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5-8-release-notes?lang=en-US

> NOTE ON PRIOR BRIEF: The task brief referenced an existing file
> `Research/_incoming/UE58_API_Changes.md` (status APPROVE_WITH_FIXES) to "build on".
> That file does NOT exist in this workspace (verified by directory listing). This
> document was therefore produced from scratch against the official 5.8 Release Notes
> rather than amending a prior draft. If the prior brief lives elsewhere, re-run with
> the correct path. Every factual claim below carries a source anchor.

---

## 1. CONFIRMED 5.8 FACTS

### 1.1 Incremental Cooking (Beta) + ZenServer as Cooked Output Store [POINT 1]

Source: UE 5.8 Release Notes, "Developer Iteration" > "Incremental Cooking (Beta)" and
"Zenserver as Cooked Output Store"
https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5-8-release-notes?lang=en-US#incrementalcooking(beta)
https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5-8-release-notes?lang=en-US#zenserverascookedoutputstore

- Incremental Cooking "continues as a beta feature for UE 5.8." Improvements to
  determinism further reduce the need to recook unmodified assets, notably with DDC and
  structured data variations. [Release Notes, Incremental Cooking (Beta)]
- Mechanism: "Cook processes automatically analyze asset changes against output stored
  in Zen Server and only cook new updates made to your project's assets. This works
  across all native engine assets including Blueprints and World Partition tiles."
  [Release Notes, Incremental Cooking (Beta)]
- "Zenserver as Cooked Output Store is now enabled by default." This also enables
  Zenserver Streaming being used automatically by workflows in Unreal Editor when
  launching the game/client on devices; staging container files (pak / iostore) remains
  available and supported for non-iteration workflows. [Release Notes, Zenserver as
  Cooked Output Store]
- Remote behavior: "To ensure this functions with remote devices, Zenserver responds to
  remote requests, but only if they supply a pre-generated key for authorization."
  [Release Notes, Zenserver as Cooked Output Store]
- Backward-compat: "Existing projects that have the use of Zen store disabled in their
  project settings will not use Zenserver as a cooked output store. They will need to
  manually change the setting in the project settings to enable it." [Release Notes,
  Zenserver as Cooked Output Store]
- Config note: professional builds should set `LimitProcessLifetime=false` in the
  `Zen.AutoLaunch` section of `DefaultEngine.ini` so Zenserver is not starting/stopping
  frequently. The `AllowRemoteNetworkService` config key was renamed to
  `RemoteNetworkService` and now takes values `None` / (others) instead of true/false.
  [Release Notes, Zenserver as Cooked Output Store]

### 1.2 Mass entity-system scheduler rewrite [POINT 2]

Source: UE 5.8 Release Notes, "Mass" section
https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5-8-release-notes?lang=en-US#mass-2

- "Mass, our data-oriented entity system, gets a major overhaul." [Release Notes, Mass]
- "Mass Signals are now part of the core engine, and entities can be created off the
  game thread thanks to archetype-based, lock-free scheduling." [Release Notes, Mass]
- "A new sparse/virtual fragment system reduces memory use and allows optional fragments
  and tags to be added or removed without triggering costly archetype changes."
  [Release Notes, Mass]
- "We completely overhauled Mass processor execution and dependency resolution to better
  take advantage of multi-core CPUs, resulting in safer and faster execution on modern
  hardware. This is supported by more granular scheduling and thread-safe observer
  notifications." [Release Notes, Mass]
- "A new MassCore module further simplifies adoption by separating the core entity system
  from the broader MassGameplay stack." [Release Notes, Mass]
- Additional tested detail: "Mass Gameplay Debug: Made AssignDebugVisProcessor editor
  only..."; "Mass Entity: Add observer support for shared fragments and swaptag."
  [Release Notes, Mass / changelog lines]
  Reference doc: https://dev.epicgames.com/documentation/unreal-engine/mass-entity-in-unreal-engine

### 1.3 iOS Shader Model 6 via Metal Shader Converter [POINT 3]

Source: UE 5.8 Release Notes, "iOS Shader Model 6 (Experimental)"
https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5-8-release-notes?lang=en-US#ios,tvos,andipados

- "In Unreal Engine 5.8, we add experimental Shader Model 6 (SM6) support on iOS,
  integrating Apple's Metal Shader Converter library to unlock advanced GPU features on
  Apple Silicon." [Release Notes, iOS Shader Model 6 (Experimental)]
- Delivered in 5.8:
  - A dedicated iOS SM6 shader platform variant alongside the existing Metal paths
  - Wave intrinsics (SIMD-group operations) for more efficient GPU compute algorithms
  - Native 16-bit (FP16) shader types to improve ALU throughput on Apple Silicon
  [Release Notes, iOS Shader Model 6 (Experimental)]
- "Support targets A15 and newer Apple Silicon and ships as experimental, with the
  existing Metal rendering paths preserved for broader device coverage. Validation of
  SM6-gated rendering features such as improved deferred techniques and higher-quality
  compute paths is underway and will land in subsequent releases." [Release Notes, iOS
  Shader Model 6 (Experimental)]
- Supporting platform note: "Shader Model 6 (SM6) requires iOS26+ with an Apple A17Pro or
  better device. This support is in Beta, and we do not recommend it for production at
  this time." [Release Notes, Platform > iOS/tvOS/iPadOS requirements]

### 1.4 Windows Game Input redistributable packaging (IncludeRedistFiles) [POINT 4]

Source: UE 5.8 Release Notes, "Windows" section
https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5-8-release-notes?lang=en-US#windows

- "You can now set `Game Input::IncludeRedistFiles=True` in your project's
  `DefaultEngine.ini` to have `BootstrapPackagedGame` run a `GameInputRedist.msi`
  installer! You should set this for any packaged game using the Game Input for Windows
  plugin." [Release Notes, Windows — exact sentence]
- Context (Game Input plugin hardening, same release): the Raw Input plugin is deprecated
  in favor of the newer Game Input experimental plugin; a "preferred input API" engine
  setting lets projects roll out from older input APIs (e.g. XInput) to GameInput; and
  `FInputDeviceScope` is deprecated in favor of the new thread-safe `FInputDeviceRegistry`.
  [Release Notes, Game Input / Input sections]

### 1.5 UE_LOG deprecation claim — CORRECTED [POINT 5]

Source: UE 5.8 Release Notes, "Upgrade Notes" > "Foundation" > "Core" (API Change / Upgrade Notes)
https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5-8-release-notes?lang=en-US#core-2

FINDING: UE_LOG is NOT deprecated in 5.8. It is named as a future migration TARGET. The
exact Release Notes sentence is:

> "These replace UE_LOG which will eventually be deprecated. Please convert UE_LOG to
> UE_LOGF. The release contains ConvertUELog.py to safely upgrade most uses."
> [Release Notes, Upgrade Notes > Foundation > Core]

Interpretation:
- UE_LOG remains fully usable in 5.8 (the new UE_LOGF/structured logging is the
  replacement going forward, but deprecation has not yet happened).
- The Release Notes elsewhere note an internal change: "Converted UE_LOG to use log
  records internally. This adds file, line, and context to every UE_LOG even though they
  are inherently unstructured." [Release Notes, Core/Foundation changelog] — this is an
  implementation detail, not a deprecation.
- Migration path if/when you adopt it now: convert `UE_LOG` -> `UE_LOGF`; an automated
  helper `ConvertUELog.py` ships with the release to upgrade most call sites.

CONCLUSION: Any prior claim that "UE_LOG is deprecated in 5.8" is INCORRECT. Correct
statement: UE_LOG is slated for eventual deprecation and UE_LOGF is the recommended
replacement, but UE_LOG is not deprecated in 5.8.

### 1.6 Not-in-5.8 / deprecated-in-5.8 list [POINT 6]

See Section 2 (Deprecated/Removed list). All entries carry a source anchor and, where
Epic documents one, a migration path.

---

## 2. DEPRECATED / REMOVED IN 5.8 (vs 5.7) — WITH SOURCE + MIGRATION PATH

All entries sourced from the UE 5.8 Release Notes. Format: item — source anchor —
migration path (where documented).

### 2.1 Input
- Raw Input plugin — DEPRECATED in favor of the new "Game Input for Windows" plugin.
  [Release Notes, Upgrade Notes > Gameplay/Input; also "Deprecate the Raw Input plugin
  in favor of the newer Game Input experimental plugin"] Migration: move to Game Input
  for Windows plugin.
- Enhanced Input "combo trigger" — DEPRECATED. "This trigger type is unreliable and can
  cause mapping contexts to be corrupted in the editor." Migration: not specified; avoid
  the combo trigger type. [Release Notes, Enhanced Input]
- `FInputDeviceScope` — DEPRECATED in favor of `FInputDeviceRegistry` (thread-safe).
  Migration: replace `FInputDeviceScope` usage with `FInputDeviceRegistry`.
  [Release Notes, Input]

### 2.2 Core / Foundation
- `UE_LOG` — flagged for eventual deprecation (NOT deprecated in 5.8). Migration:
  `UE_LOG` -> `UE_LOGF`, via `ConvertUELog.py`. (See §1.5.) [Release Notes, Core]
- `FCoreDelegates::OnPostEngineInit` — DEPRECATED in favor of
  `FCoreDelegates::GetOnPostEngineInit()`. Migration: call the getter form.
  [Release Notes, Core]
- `PLATFORM_ENABLE_POPCNT_INTRINSIC` and `FPlatformMisc::HasNonoptionalCPUFeatures()` /
  `FPlatformMisc::NeedsNonoptionalCPUFeaturesCheck()` — DEPRECATED. [Release Notes, Core]
- `r.SkipRedundantTransformUpdate` feature and associated API — DEPRECATED and disabled.
  [Release Notes, Rendering/Core] Migration: remove reliance on it.
- UE4-API DDC functionality — DEPRECATED (no longer supported). [Release Notes, Core]
- `FPrimitiveSceneProxy`: several deprecated APIs REMOVED; `OnDetachLight` deprecated.
  REMOVED: `WritesVirtualTexture`, `GetNaniteResourceInfo`,
  `UpdateInstances_RenderThread`, `GetDistanceFieldInstanceData`. [Release Notes, Core]
- `GetLastTickGameTime` — DEPRECATED (confusing). [Release Notes, Gameplay]
- `FClassInterface` (etc.) — `FNodeClassMetadata::DefaultInterface` now accepts
  `FClassInterface` directly (replacing `FVertexInterface`); deprecated input/output node
  creation helpers REMOVED from `IDataTypeRegistry`. [Release Notes, MetaSound/Animation]
- `CheckEnsureFailed` — `ExecCheckImplInternal` RENAMED to `CheckEnsureFailed` (applies to
  ensures, not checks). [Release Notes, Core]

### 2.3 Animation / Rig
- `FRigControlElement::Settings` direct Blueprint access — DEPRECATED (adds deprecated
  UPROPERTY so existing BP graphs still compile with warnings). Migration:
  `GetControlSettings(Key)` BlueprintCallable is the migration target. [Release Notes,
  Control Rig]
- Removed 5.6-deprecated PoseSearch methods. [Release Notes, Animation]
- PoseSearch `BP_GetCurveValue` / `BP_GetWorldRotation` / `BP_GetWorldVelocity` /
  `BP_GetWorldPosition` (on Curve/Heading/Velocity/Position channels) — DEPRECATED in
  favor of the `...FromContext` variants. [Release Notes, Animation]
- Removed deprecated functions in `USkeleton`: `GetSkeletonRemapping`,
  `GetAssetRegistryTags`, `CollectAnimationNotifies`, `GetRawAnimationTrackIndex`.
  [Release Notes, Animation]
- "Cleaned deprecated methods" from UAF, RigVM, Motion Warping, MLDeformer, animation
  runtime (up to 5.6). [Release Notes, Animation]
- Animation: non-reflected `UE_DEPRECATED` items (5.3–5.6) REMOVED, e.g.
  `AnimAssetFindReplace::RequestUIRefresh`, several `AnimationEditorViewportClient`
  accessors (`SetCustomAnimationSpeed`, `GetCustomAnimationSpeed`,
  `SetPlaybackSpeedMode`, `GetPlaybackSpeedMode`, `GetPersonaModeManager`). [Release Notes,
  Upgrade Notes > Animation]

### 2.4 Rendering / RHI
- Path Tracing: `EnableBackfaceCulling` cvar REMOVED; defaults to on. [Release Notes,
  Path Tracer]
- Unreal Editor rendering on Intel-based Macs — REMOVED. "Removed rendering support for
  Intel-based Macs. Any processes using the Unreal Editor that don't require rendering
  (such as cooking) are still available on Intel-based Macs." [Release Notes, Mac]

### 2.5 Platform / Mobile (Android / iOS / XR)
- "Android Graphics Debugger" entry in Project Settings → Platforms → Android → Graphics
  Debugger — DEPRECATED (the tools it referred to are deprecated/no longer available).
  [Release Notes, Android]
- OpenXR: `PackageForOculusMobile` REMOVED (replaced by `bPackageForMetaQuest` more than
  two UE versions ago). [Release Notes, XR/OpenXR]
- Windows Mixed Reality Bindings — REMOVED (from VR Template). [Release Notes, VR/XR]

### 2.6 Worldbuilding / Geometry
- LightWeightInstances code — marked DEPRECATED. [Release Notes, Worldbuilding]
- Experimental light gizmo plugin — REMOVED ("no longer good representations...").
  [Release Notes, Geometry/Level Design]
- Experimental gizmo option removed from level editor viewport (rehomed to gizmo settings
  and profiles). [Release Notes, Geometry/Level Design]

### 2.7 Simulation / Physics / Cloth
- Cloth: "Deprecated anything related to extracting collision data from cloth simulations
  directly (e.g., `FClothingSimulationInstance::AppendSimulationData`,
  `USkeletalMeshComponent::FindClothCollisions`)." [Release Notes, Cloth]
- Chaos Flesh: `StaticMesh` property on the Chaos Flesh asset — DEPRECATED. [Release Notes,
  Simulation]

### 2.8 Media / Compositing
- `UCompositePassColorGrade` — RENAMED to `UCompositePassColorGrading`. [Release Notes,
  Compositing]

### 2.9 Audio / Subtitles
- `QueueSubtitle` — DEPRECATED; replaced by new `QueueSingleSubtitle` Blueprint/C++
  function (companion `QueueSubtitlesFromAsset` queues all lines in one call). [Release
  Notes, Audio/Subtitles]

### 2.10 NNE / AI
- `NNERuntimeORTDml` NPU inference — projects must migrate to GPU or RDG paths. After
  upgrade, `GetRuntime("NNERuntimeORTDml")` will never return a proxy implementing
  `INNERuntimeNPU`; `CanCreateModelNPU`/`CreateModelNPU` no longer callable. Migration:
  use GPU or RDG execution paths of the same runtime. [Release Notes, Upgrade Notes > AI/ML]
- IREE runtime/tools upgraded to 3.11.0: compiled model artifacts from prior IREE version
  not guaranteed ABI-compatible. Migration: clear compiled-model cache and re-cook.
  [Release Notes, Upgrade Notes > AI/ML]

---

## 3. UNVERIFIED / NOT RESOLVED

The following could not be confirmed against the official 5.8 Release Notes within this
bounded search and are EXCLUDED from the confirmed list per the "no guessing" rule.

- U3.1 Any specific API signatures of `UE_LOGF` (the structured-logging replacement). The
  Release Notes name it and ship `ConvertUELog.py`, but the exact macro signature /
  structured-field API was not extracted here. UNVERIFIED.
- U3.2 The full enumerated set of `RemoteNetworkService` accepted values beyond `None`
  (Release Notes shows `None` as an example and says it "instead uses the following
  values" but the complete enum/string list was not captured in the truncated view).
  UNVERIFIED.
- U3.3 Performance benchmarks / numeric speedups for the Mass scheduler rewrite (e.g. "X%
  faster"). The Release Notes describe qualitative improvements ("safer and faster
  execution on modern hardware") but no headline numeric figure for the scheduler itself
  was quoted. (Note: an unrelated "5x runtime performance improvement" figure applies to
  Control Rig Dynamics, not Mass.) UNVERIFIED.
- U3.4 The prior brief `UE58_API_Changes.md` (referenced by the task as APPROVE_WITH_FIXES)
  could not be located in this workspace; the claimed list of "gaps" it contained could
  not be cross-checked. UNVERIFIED — see header note.

---

## 4. SOURCES

[1] Unreal Engine 5.8 Release Notes (primary, canonical). All factual anchors above cite
    this document unless otherwise noted.
    https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5-8-release-notes?lang=en-US
    Key section anchors used:
      - #incrementalcooking(beta)  (Incremental Cooking Beta)
      - #zenserverascookedoutputstore  (ZenServer as Cooked Output Store)
      - #mass-2  (Mass overhaul / scheduler)
      - #ios,tvos,andipados  (iOS Shader Model 6 Experimental)
      - #windows  (Game Input IncludeRedistFiles)
      - #core-2  (Core: UE_LOG -> UE_LOGF, FCoreDelegates, FPrimitiveSceneProxy removals)

[2] MassEntity documentation (referenced by Release Notes for further detail)
    https://dev.epicgames.com/documentation/unreal-engine/mass-entity-in-unreal-engine

[3] Using the Windows Metal Shader Compiler for iOS (background on MSC workflow)
    https://dev.epicgames.com/documentation/unreal-engine/using-the-windows-metal-shader-compiler-for-ios-in-unreal-engine

Confidence: HIGH for all Section 1 + Section 2 claims (directly quoted from official
Release Notes). Section 3 items are explicitly UNVERIFIED and excluded from confirmed list.
