# UE5 Gameplay Framework Reference

#ue5 #cpp #reference #gameplay-framework #actors #modules

> Core gameplay architecture — class hierarchy, lifecycle, modules, and constructors. From Epic UE 5.8 documentation.

---

## Class Hierarchy & Lifecycle

1. **Game Instance** — Instantiated on engine launch, persists across levels. Manages save games, subsystems. NOT replicated.
2. **Game Mode** — Instantiated per level. Server-only. Sets rules, spawns Game State and Player States.
3. **Game State** — Global game data (scores, objectives, player list). REPLICATED.
4. **Player State** — Per-player data (health, ammo). REPLICATED.
5. **Controller** — Non-physical manager for logic and input.
   - **Player Controller** — Human input
   - **AI Controller** — Behavior trees, navigation
6. **Pawn** — Physical actor in world (collision, mesh, movement).
   - **Character** — Specialized Pawn with advanced movement (walk, jump, swim, fly)

**Key Relationships:**
- Game Instance is longest-lived
- Game Mode owns rules, spawns primary structures
- Controllers POSSESS Pawns to act in the world

---

## Core Class Reference

| Class | Description |
|-------|-------------|
| **Actor** | Base spawnable object in a level. Can be replicated. |
| **Actor Component** | Building blocks of Actors (movement, rendering, etc.) |
| **Pawn** | Base for player/AI-controlled actors |
| **Character** | Pawn with advanced movement component |
| **Controller** | Non-physical actor that possesses a Pawn |
| **Game Mode** | Gameplay rules for a session (server-only) |
| **Game Instance** | Persists across map loads |
| **Game State** | Global replicated data |
| **Player State** | Per-player replicated data |
| **Gameplay Statics** | Static utility (sounds, spawning, damage) |
| **HUD** | Overlay elements on viewport |
| **Camera** | Player's point of view |

---

## Naming Conventions

| Prefix | Meaning |
|--------|---------|
| `A` | Actors — spawnable, placed in world |
| `U` | Non-spawnable Objects — must belong to an Actor (Components) |

---

## Class Header Structure

```cpp
#pragma once
#include "ClassName.generated.h"  // MUST be last include

UCLASS([specifiers], [meta(key=value)])
class MYPROJECT_API AClassName : public AParentName
{
    GENERATED_BODY()
public:
    AClassName();
};
```

### Key Class Specifiers

| Specifier | Effect |
|-----------|--------|
| `Abstract` | Prevents placing in levels. Use for base classes. |
| `Blueprintable` | Allows Blueprint subclassing |
| `Config=Name` | Enables .ini config storage |
| `Placeable` | Can be placed in levels/Blueprints |
| `Transient` | Never saved to disk |

---

## Constructor Patterns

### Basic Constructor
```cpp
AMyActor::AMyActor()
{
    // Set CDO defaults only
}
```

### With ObjectInitializer (override parent subobjects)
```cpp
AMyActor::AMyActor(const FObjectInitializer& ObjectInitializer)
    : Super(ObjectInitializer)
{
    // Set CDO defaults
}
```

### Asset References (one-time load)
```cpp
struct FConstructorStatics
{
    ConstructorHelpers::FObjectFinder<UStaticMesh> MeshAsset;
    FConstructorStatics()
        : MeshAsset(TEXT("StaticMesh'/Game/Path/To/Asset'"))
    {}
};
static FConstructorStatics ConstructorStatics;
StaticMesh = ConstructorStatics.MeshAsset.Object;
```

### Class References
```cpp
// Method 1: FClassFinder
static ConstructorHelpers::FClassFinder<UNavigationMeshBase> ClassFinder(
    TEXT("class'Engine.NavigationMeshBase'"));
if (ClassFinder.Succeeded()) { NavMeshClass = ClassFinder.Class; }

// Method 2: Direct (simpler)
NavMeshClass = UNavigationMeshBase::StaticClass();
```

### Creating Subobjects
```cpp
AMyActor::AMyActor()
{
    WindSource = CreateDefaultSubobject<UWindPointSourceComponent>(TEXT("WindSource"));
    RootComponent = WindSource;

    DisplaySphere = CreateDefaultSubobject<UDrawSphereComponent>(TEXT("DisplaySphere"));
    DisplaySphere->SetupAttachment(RootComponent);
}
```
Store pointers in UPROPERTY for GC.

---

## Gameplay Modules

Modules are DLLs containerizing related classes. Each game needs at least one primary module.

### Directory Structure
```
[GameName]/Source/[ModuleName]/Public/    // .h files
[GameName]/Source/[ModuleName]/Private/   // .cpp files
[GameName]/Source/[ModuleName]/           // *.Build.cs
```

### Module Files

**Header (.h):**
```cpp
#include "CoreMinimal.h"
// Per-file includes as needed, e.g.:
// #include "GameFramework/Actor.h"
// UHT discovers classes automatically — no module-wide headers needed
```

**Source (.cpp):**
```cpp
#include "<ModuleName>.h"
IMPLEMENT_PRIMARY_GAME_MODULE(FDefaultGameModuleImpl, <ModuleName>, "<GameName>");
// Additional modules: IMPLEMENT_GAME_MODULE instead
```

**Build.cs:**
```csharp
using UnrealBuildTool;
public class <ModuleName> : ModuleRules
{
    public <ModuleName>(ReadOnlyTargetRules Target) : base(Target)
    {
        PublicDependencyModuleNames.AddRange(
            new string[] { "Core", "Engine" });
        PrivateDependencyModuleNames.AddRange(
            new string[] { "RenderCore" });
    }
}
```

### Module Registration (UE 5.7)
Register modules in two places:

**`.uproject`** — `Modules` array:
```json
"Modules": [
    { "Name": "<ModuleName>", "Type": "Runtime", "LoadingPhase": "Default" }
]
```

**`*.Target.cs`** — `ExtraModuleNames`:
```csharp
ExtraModuleNames.AddRange(new string[] { "<ModuleName>" });
```

### Multiple Modules
- Better link times, faster iteration
- More DLL exports/interfaces, increased complexity
- Add to `Target.cs` in `ExtraModuleNames` array
- Only ONE uses `IMPLEMENT_PRIMARY_GAME_MODULE`

---

## Module Categories

| Category | Availability | Purpose |
|----------|-------------|---------|
| **Runtime** | Every build | Core engine (Core, CoreUObject, Engine, Renderer, Physics) |
| **Editor** | Editor builds only | Editor UI, tooling (UnrealEd, BlueprintGraph, Sequencer) |
| **Developer** | Dev/Debug only | Profiling, automation, debug tools |

Plugins are collections of modules — must be enabled in .uproject or Plugins Editor.
