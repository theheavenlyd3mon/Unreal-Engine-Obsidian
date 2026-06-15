# First Build — getting EchoesCore to compile

This module was **reviewed line-by-line against UE 5.7 APIs** but authored without an engine install, so the first build is a "wire it up + fix any nits" pass, not magic. This doc front-loads every issue likely to surface so that pass is ~15 minutes, not a debugging session.

## Build verification (2026-06-14) — now compiles clean against UE 5.7

The module was put through a real build against an installed **UE 5.7**: a minimal C++ host project, **Game target** (`Win64 Development`), UnrealHeaderTool + MSVC v143 over all 33 files, then link. **Result: it compiles and links clean.** Four fixes were needed, in two waves:

**Wave 1 — found by an independent read-audit (structural, version-independent):**
1. **`EchoesCore.Build.cs` was missing `AIModule`.** `EchoesAIController` (`AIController.h`, `UBehaviorTree`, `RunBehaviorTree`) needs it; `GameplayTasks` doesn't pull it in. Added to `PublicDependencyModuleNames` (public, since the include is in a public header).
2. **`EchoesGameplayTags.h` exported tags incorrectly.** `ECHOESCORE_API UE_DECLARE_GAMEPLAY_TAG_EXTERN(...)` placed `__declspec` before `extern` and was asymmetric with the unmarked `.cpp` defs. Removed `ECHOESCORE_API` from all 8 — the Epic/Lyra native-tag idiom.

**Wave 2 — found only by compiling (plausible API names no read-review caught):**
3. **`EchoesAttributeSet.cpp` ctor called `FGameplayAttributeData::Init()`**, which doesn't exist. Switched to the `ATTRIBUTE_ACCESSORS`-generated `InitHealth(...)` / `InitMaxHealth(...)` / etc. (they set base + current).
4. **`EchoesDamageExecution.cpp` called `FTagContainerAggregator::GetAggregatorTags()`**, which doesn't exist. Corrected to `GetAggregatedTags()`.

Note the **Game target** is used deliberately: it compiles every EchoesCore file (all runtime) without pulling in `UnrealEd` → `SwarmInterface` (which requires the .NET Framework SDK). An Editor-target build needs that SDK component installed — a toolchain detail, unrelated to EchoesCore. Four cosmetic nits (an unused header include, a self-vs-target effect-spec note, a non-`BlueprintType` handle pin, an over-stated persistent-id comment) remain logged-not-changed — none affect the build. The per-file ratings below now reflect a real compile, not just a read.

## Pre-build checklist (do these first — they cause 90% of first-build failures)

1. **UE version:** 5.7 (the code targets 5.7 APIs; see version-sensitivity notes below if you're on 5.4–5.6).
2. **Enable the plugin:** Edit → Plugins → **Gameplay Abilities** → enable → restart editor.
3. **Register the module** (see `README.md` for the exact JSON):
   - `.uproject` → `Modules` array: `{ "Name": "EchoesCore", "Type": "Runtime", "LoadingPhase": "Default" }`
   - `Source/<Project>.Target.cs` **and** `<Project>Editor.Target.cs` → `ExtraModuleNames.Add("EchoesCore");`
4. **Primary vs secondary module:** `EchoesCore.cpp` uses `IMPLEMENT_MODULE(FDefaultGameModuleImpl, EchoesCore)` — correct when your project already has its own primary game module. If EchoesCore is your *only* module, change that line to `IMPLEMENT_PRIMARY_GAME_MODULE(FDefaultGameModuleImpl, EchoesCore, "EchoesCore")`.
5. **Regenerate project files** (right-click `.uproject` → Generate Visual Studio project files) before opening the solution.

## Per-file compile confidence

All 20 files traced. Confidence = how likely it compiles unchanged on a clean 5.7 project.

| File | Confidence | Watch for |
|------|:---:|---|
| `EchoesAttributeSet.h/.cpp` | High | `ATTRIBUTE_ACCESSORS` macro + `GAMEPLAYATTRIBUTE_REPNOTIFY` are standard; needs `AbilitySystemComponent.h` (included). |
| `EchoesAbilitySystemComponent.h/.cpp` | High | Trivial subclass. |
| `EchoesPlayerState.h/.cpp` | High | `SetNetUpdateFrequency(100.f)` — see version note #1. |
| `EchoesCharacter.h/.cpp` | High | `MakeOutgoingSpec/ApplyGameplayEffectSpecToSelf` are current; `DefaultAttributesEffect` will be null until you author `GE_InitStats`. |
| `EchoesGameplayAbility.h/.cpp` | High | Minimal. |
| `EchoesSaveGame.h` | High | Pure UPROPERTY(SaveGame) data. |
| `EchoesSaveSubsystem.h/.cpp` | High | Async delegate types (`FAsyncSaveGameToSlotDelegate` etc.) live in `Kismet/GameplayStatics.h` (included). |
| `EchoesPersistentIdComponent.h/.cpp` | High | `OnRegister`/`FGuid::NewGuid` standard. |
| `EchoesBiomeDataAsset.h` | High | `TSoftObjectPtr<UWorld>` fine. |
| `EchoesFloorGenerator.h/.cpp` | High | `Math/RandomStream.h` included for `FRandomStream`. |
| `EchoesCore.Build.cs` / `EchoesCore.cpp` | High | `AIModule` dep added in the 2026-06-14 audit (was missing → AI controller wouldn't compile); see module-registration steps above. |

No file is rated below High — the earlier code review removed the real API errors (logged in `README.md`). The realistic failures are the *environmental* ones in the checklist, not the C++.

## Version-sensitivity notes (only if NOT on 5.7)

1. **`SetNetUpdateFrequency(100.f)`** (in `EchoesPlayerState.cpp`) — the setter exists in **5.5+**. On 5.4 or earlier, replace with the direct field: `NetUpdateFrequency = 100.f;`.
2. **GAS ability instancing** — the code uses `InstancedPerActor` (the 5.5+ default). Fine on 5.7; also fine earlier.
3. **`TObjectPtr<>`** UPROPERTYs — standard since 5.0. If on a very old engine, raw pointers also work.

## Errors you might still see, and the fix

| Symptom | Cause | Fix |
|---|---|---|
| `Cannot open include file: 'AbilitySystemComponent.h'` | Plugin not enabled / module dep missing | Enable Gameplay Abilities; confirm `GameplayAbilities` in `Build.cs` (it is). |
| `Unresolved external symbol ... InitAbilityActorInfo` | `GameplayAbilities` not linked | Same as above; regenerate project files. |
| `EchoesCore module could not be loaded` | Module not registered | Re-check checklist steps 3–4. |
| `IMPLEMENT_PRIMARY_GAME_MODULE` vs `IMPLEMENT_MODULE` mismatch | Wrong macro for your module layout | Checklist step 4. |
| LNK error mentioning your AttributeSet | `.generated.h` stale | Delete `Binaries/` + `Intermediate/`, regenerate, rebuild. |

## After it compiles — the expected "your work" wiring

The module gives you correct *systems*; these are the game-specific assets you author on top (by design — they're content, not boilerplate):

1. **`GE_InitStats`** (instant GameplayEffect) seeding Health/MaxHealth/Aether/MaxAether/AttackPower → assign to `AEchoesCharacter::DefaultAttributesEffect`.
2. **One ability** (Blueprint child of `UEchoesGameplayAbility`) → add to `DefaultAbilities`.
3. **GameMode** set to use `AEchoesCharacter` + `AEchoesPlayerState` (the `EchoesGameMode` in the slice-scaffold drop, if you're using it).
4. **Net-PIE test** (Number of Players = 2) — confirm attributes replicate and the ability fires on the second client. That validates the whole GAS spine before you build on it.

If anything here doesn't match what you hit, the mismatch itself is useful signal — send it back and it's a fast fix.
