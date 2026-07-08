# UE5 C++ Reference Guide

#ue5 #cpp #reference #coding-standard #gas #containers #delegates

> Comprehensive C++ reference for Unreal Engine 5.8. Pulled from official Epic documentation. Covers coding standard, UObject system, reflection macros, containers, delegates, smart pointers, and memory tracking.

---

## 1. Epic C++ Coding Standard

### Naming Conventions (PascalCase, no underscores)

| Prefix | Usage                    | Example              |
|--------|--------------------------|----------------------|
| T      | Template classes          | TAttribute           |
| U      | UObject subclasses        | UActorComponent      |
| A      | AActor subclasses         | AActor               |
| S      | SWidget subclasses        | SCompoundWidget      |
| I      | Abstract interfaces       | IAnalyticsProvider   |
| C      | Concept-alike structs     | CStaticClassProvider |
| E      | Enums                     | EColorBits           |
| b      | Boolean variables         | bPendingDestruction  |
| F      | Most other classes/structs| FSkin                |

**Functions:**
- Bool-returning functions ask questions: `IsVisible()`, `HasAuthority()`
- Procedures use strong verb + Object: `DestroyActor()`, `InitializeComponent()`
- Prefix `Out` for reference params modified by function

**Macros:** `UE_` prefix, ALL_CAPS with underscores

### Class Organization
```cpp
UCLASS()
class MYPROJECT_API AMyActor : public AActor
{
    GENERATED_BODY()
public:
    AMyActor();
protected:
    virtual void BeginPlay() override;
private:
    // internal helpers
};
```
Order: public → protected → private.

### Portable Types (explicit sizing)
- `uint8`/`int8` (1 byte), `uint16`/`int16` (2 bytes)
- `uint32`/`int32` (4 bytes), `uint64`/`int64` (8 bytes)
- `float` (4 bytes), `double` (8 bytes)
- Never assume size of `bool`, `TCHAR`, or `PTRINT`

### Standard Library Usage
- USE: `<atomic>`, `<type_traits>`, `<initializer_list>`, `<cmath>`, `std::numeric_limits`
- AVOID: Standard containers/strings (except in interop code)
- Prefer UE containers (TArray, TMap, TSet) for consistency

### Modern C++ (C++20 default)
**Supported:**
- `static_assert`, `override`/`final`, `nullptr`
- Range-based for loops (preferred)
- Strongly-typed enums with `ENUM_CLASS_FLAGS()` macro
- Move semantics (`MoveTemp` for explicit moves)

**Limited use:**
- `auto`: Only for lambdas, verbose iterators, or template contexts
- Lambdas: Keep short, explicit captures, document complex ones

**Avoid:**
- C-style `NULL` (use `nullptr`)
- Structured bindings (variadic `auto`)
- Compiler-specific features without preprocessor guards

### Formatting
- Braces on new lines ALWAYS (even single-line functions)
- Always use braces for if/else blocks
- Tabs (4 spaces), not spaces
```cpp
if (bHaveUnrealLicense)
{
    InsertYourGameHere();
}
else
{
    CallMarkRein();
}
```

### Const Correctness
- Be const-correct: const parameters, methods, and iteration
- Never use `const` on return types (inhibits move semantics)
```cpp
void SomeMutatingOperation(FThing& OutResult, const TArray<Int32>& InArray)
{
    // InArray will not be modified here, but OutResult probably will be
}
```

### Namespaces
- New APIs: Use `UE::` namespace (e.g., `UE::Audio::`)
- Implementation details: `Private` namespace (e.g., `UE::Audio::Private::`)
- No `using` declarations in global scope
- Macros cannot live in namespaces (use `UE_` prefix)

### Include Guards
- Use `#pragma once`
- Minimize header dependencies (forward declare when possible)
- Include specific headers, not umbrella headers

### Inclusive Word Choice
| Old Term | Alternatives                     |
|----------|----------------------------------|
| Blacklist | deny list, block list, exclude list |
| Whitelist | allow list, include list, trust list |
| Master   | primary, source, controller, template |
| Slave    | secondary, replica, agent, worker |

---

## 2. Programming with C++ — Architecture Overview

### Key Sections
- **Gameplay Classes** — Create via standard C++ syntax, compile with VS/XCode, changes reflected in editor
- **Reflection System** — UCLASS/UPROPERTY/UFUNCTION macros for editor integration and GC
- **Containers** — TArray, TMap, TSet (UE-specific collections)
- **Gameplay Architecture** — Object/Actor hierarchy with boilerplate for interactive experiences
- **Delegates** — Generic, type-safe function binding system

### Related Sub-Pages
- Reflection System: UPROPERTY specifiers, GC, serialization
- Containers: TArray, TMap, TSet usage and performance
- Gameplay Architecture: AActor, APawn, ACharacter hierarchy
- Delegates: Function binding and event systems

---

## 3. Delegates & Lambda Functions

### What Are Delegates?
Type-safe function pointers that can bind to member functions on arbitrary objects. Safe to copy. Pass by reference (value allocates heap memory).

### Three Types
1. **Single** — One binding at a time
2. **Multicast** — Multiple bindings, all execute
3. **Dynamic** — UObject-based, serializable, Blueprint-compatible

### Declaration Macros

| Function Signature              | Macro                                          |
|---------------------------------|------------------------------------------------|
| `void Function()`               | `DECLARE_DELEGATE(DelegateName)`               |
| `void Function(Param1)`         | `DECLARE_DELEGATE_OneParam(DName, P1Type)`     |
| `void Function(P1, P2)`         | `DECLARE_DELEGATE_TwoParams(DName, P1Type, P2Type)` |
| `<Ret> Function()`              | `DECLARE_DELEGATE_RetVal(RetType, DName)`      |
| `<Ret> Function(P1)`            | `DECLARE_DELEGATE_RetVal_OneParam(Ret, DName, P1Type)` |
| `<Ret> Function(P1, P2)`        | `DECLARE_DELEGATE_RetVal_TwoParams(Ret, DName, P1Type, P2Type)` |

**Dynamic variants:** `DECLARE_DYNAMIC_DELEGATE...`, `DECLARE_DYNAMIC_MULTICAST_DELEGATE...`
**UDELEGATE macro** for Blueprint specifiers:
```cpp
UDELEGATE(BlueprintAuthorityOnly)
DECLARE_DYNAMIC_MULTICAST_DELEGATE_FourParams(
    FInstigatedAnyDamageSignature,
    float, Damage,
    const UDamageType*, DamageType,
    AActor*, DamagedActor,
    AActor*, DamageCauser);
```

**Placement:** Global scope, namespace, or class declaration. NEVER inside function bodies.

### Binding Functions

| Function    | Description                                                      |
|-------------|------------------------------------------------------------------|
| `Bind`      | Binds to an existing delegate object                             |
| `BindStatic`| Raw C++ pointer global function delegate                         |
| `BindRaw`   | Raw C++ pointer delegate. Unsafe if target deleted.              |
| `BindLambda`| Functor/lambda binding                                           |
| `BindSP`    | Shared pointer member function. Weak reference. Use ExecuteIfBound. |
| `BindUObject`| UObject member function. Weak reference. Use ExecuteIfBound.    |
| `UnBind`    | Unbinds this delegate                                            |

### Payload Data
Pass extra variables at bind-time, invoked with the delegate:
```cpp
MyDelegate.BindRaw(&MyFunction, true, 20);  // bool + int32 payload
```
Supported by all types EXCEPT "dynamic".

### Execution

| Function          | Description                                          |
|-------------------|------------------------------------------------------|
| `Execute`         | Execute WITHOUT checking bindings (unsafe)           |
| `ExecuteIfBound`  | Check then execute (safe for void functions)         |
| `IsBound`         | Check if bound (use before Execute)                  |

### Complete Example
```cpp
// 1. Declare delegate type
DECLARE_DELEGATE_OneParam(FStringDelegate, FString);

// 2. Class that holds the delegate
class FMyClass
{
    FStringDelegate WriteToLogDelegate;
};

// 3. Create target object
TSharedRef<FLogWriter> LogWriter(new FLogWriter());

// 4. Bind (SP = shared pointer, use BindUObject for UObject)
WriteToLogDelegate.BindSP(LogWriter, &FLogWriter::WriteToLog);

// 5. Execute
WriteToLogDelegate.Execute(TEXT("Delegates are great!"));

// 6. Safe execution
WriteToLogDelegate.ExecuteIfBound(TEXT("Only executes if bound!"));
```

### Key Gotchas
- Always check `IsBound()` before `Execute()` — unbound delegates scribble memory
- `ExecuteIfBound` is safe for void functions but beware output params
- `BindRaw` is unsafe if target is deleted — prefer `BindSP` or `BindUObject`
- Delegates pass by reference, not value (heap allocation)
- Dynamic delegates don't support payload data

---

## 4. UObject System

### Core Concept
All engine objects derive from `UObject`. Classes must use the `UCLASS` macro to integrate with the reflection system.

### Class Default Object (CDO)
- Each `UCLASS` has a CDO — a default "template" object created by the constructor, never modified after
- `GetClass()` returns the `UCLASS` metadata descriptor
- Only UPROPERTY/UFUNCTION tagged members are included in reflection

### UObject Creation — CRITICAL RULES
1. **No constructor arguments** — initialized via default constructor at engine startup
2. **Constructors must be lightweight** — set only default values and subobjects
3. **Always use engine APIs:**
   - `NewObject<T>()` — flexible runtime creation
   - `CreateDefaultSubobject<T>()` — for components/subobjects at startup
4. **Never use `new` or `delete`** — memory managed by GC. Manual management causes corruption

### Minimal Header
```cpp
#pragma once
#include "Object.h"
#include "MyObject.generated.h"  // MUST be last include

UCLASS()
class MYPROJECT_API UMyObject : public UObject
{
    GENERATED_BODY()
};
```

### Ticking
- Actors & ActorComponents can tick if enabled
- UObjects do NOT tick by default — inherit `FTickableGameObject` and implement `Tick()`

### Garbage Collection
- Objects collected when no strong references exist (UPROPERTY pointers, TStrongObjectPtr)
- Weak pointers do NOT keep objects alive
- `MarkAsGarbage()` replaces deprecated `MarkPendingKill()` — sets pointers to NULL, collected next GC pass
- GC runs between frames — manually clear pointers for perf-critical code
- `IsValid()` checks for null/garbage — prefer manual pointer management where possible

---

## 5. Smart Pointers (Non-UObject)

> **NOT for UObject systems** — UObjects have their own memory tracking via GC.

| Type | Class | Behavior |
|------|-------|----------|
| Shared Pointer | `TSharedPtr` | Owns object, can be null. Deletes when no shared refs remain. |
| Shared Reference | `TSharedRef` | Must always be non-null. Guarantees safe dereferencing. |
| Weak Pointer | `TWeakPtr` | Does NOT own object. Breaks reference cycles. Can become null. |
| Unique Pointer | `TUniquePtr` | Sole owner. Cannot share. Auto-deletes on scope exit. Compile error on copy. |

### Helper Classes & Functions

| Helper | Description |
|--------|-------------|
| `TSharedFromThis` | Derive from this to get `AsShared()` / `SharedThis()` for TSharedRef to `this`. Don't call from constructors. |
| `MakeShared` | Single allocation (most efficient). Requires public constructor. |
| `MakeShareable` | Two allocations. Works with private constructors. |
| `StaticCastSharedRef` / `StaticCastSharedPtr` | Static downcasting (no RTTI dynamic cast). |
| `ConstCastSharedRef` / `ConstCastSharedPtr` | Remove const from smart pointer. |

### TSharedFromThis Example
```cpp
class FMyBaseClass : public TSharedFromThis<FMyBaseClass>
{
    void RegisterAsBaseClass(FRegistryObject* Registry)
    {
        TSharedRef<FMyBaseClass> ThisRef = AsShared();
        Registry->Register(ThisRef);
    }
};

class FMyDerivedClass : public FMyBaseClass
{
    void Register(FRegistryObject* Registry) override
    {
        TSharedRef<FMyDerivedClass> ThisRef = SharedThis(this);
        Registry->Register(ThisRef);  // Implicit upcast
    }
};
```

### Thread Safety
Default: thread-unsafe. For multi-threaded access:
```cpp
TSharedPtr<T, ESPMode::ThreadSafe>
TSharedRef<T, ESPMode::ThreadSafe>
TWeakPtr<T, ESPMode::ThreadSafe>
TSharedFromThis<T, ESPMode::ThreadSafe>
```
Reads/copies are thread-safe. Writes/resets must be synchronized.

---

## 6. UFUNCTION — Function Specifiers

### Core Specifiers

| Specifier | Effect |
|-----------|--------|
| `BlueprintCallable` | Executable in Blueprint graphs |
| `BlueprintPure` | Side-effect free. Const functions are pure by default |
| `BlueprintImplementableEvent` | Implemented entirely in Blueprints |
| `BlueprintNativeEvent` | Blueprint override with C++ default. Generates `FunctionName_Implementation` |
| `Client` / `Server` | Executes on client/server only. Generates `_Implementation` |
| `NetMulticast` | Executes on server and all clients |
| `Reliable` / `Unreliable` | Network replication guarantee |
| `Exec` | Callable from in-game console |
| `CallInEditor` | Button in editor Details panel |
| `WithValidation` | Generates `_Validate` function gating execution |
| `SealedEvent` | Prevents overriding in subclasses |

### Metadata Specifiers (Editor Only)

| Meta Tag | Effect |
|----------|--------|
| `Category="Parent\|Child"` | Organizes functions in Blueprint menus |
| `DisplayName="Node Name"` | Overrides generated node name |
| `ToolTip="Description"` | Custom tooltip |
| `AdvancedDisplay=N` | Parameters after Nth hidden as advanced |
| `DeprecatedFunction` | Marks function as obsolete |
| `DevelopmentOnly` | Only runs in Development builds |
| `WorldContext="Param"` | Identifies world context parameter |

### Parameter Specifiers

| Specifier | Description |
|-----------|-------------|
| `Out` | Reference parameter modified by function |
| `Optional` | Parameter optional for caller |

### Making Pure Functions Not Pure
```cpp
UFUNCTION(BlueprintPure=false)
float NotActuallyPure() const;
```

---

## 7. Metadata Specifiers — Full Reference

### Class Metadata

| Meta Tag | Effect |
|----------|--------|
| `BlueprintSpawnableComponent` | Can be spawned by Blueprint |
| `BlueprintThreadSafe` | Callable on non-game threads (animation BPs) |
| `ChildCannotTick` | Prevents Blueprint subclasses from ticking |
| `ChildCanTick` | Allows Blueprint subclasses to override tick flag |
| `DeprecatedNode` | Behavior tree node deprecated |
| `DeprecationMessage="Text"` | Custom deprecation warning |
| `DisplayName="Name"` | Overrides Blueprint node name |
| `ExposedAsyncProxy` | Exposes proxy in Async Task nodes |
| `IsBlueprintBase="true/false"` | Acceptable base for Blueprints |
| `KismetHideOverrides="Event1,Event2"` | Blueprint events that cannot be overridden |
| `RestrictedToClasses="Class1,Class2"` | Restricts Blueprint function library usage |
| `ShortToolTip="Text"` | Short tooltip for Parent Class Picker |
| `ToolTip="Text"` | Overrides auto-generated tooltip |

### Enum Metadata

| Meta Tag | Effect |
|----------|--------|
| `Bitflags` | Enum usable as flags by integer UPROPERTY with `Bitmask` |
| `Experimental` | Labels type as experimental |

**Individual Enum Value UMeta:**
| UMeta Tag | Effect |
|-----------|--------|
| `DisplayName="Name"` | Overrides display name |
| `Hidden` | Hides value from Editor |
| `ToolTip="Text"` | Overrides tooltip |

### Function Metadata (Extended)

| Meta Tag | Effect |
|----------|--------|
| `ArrayParm="Param1,Param2"` | Call Array Function node; params treated as wildcard arrays |
| `AutoCreateRefTerm="Param1"` | Auto-creates default for ref params if pins disconnected |
| `BlueprintAutocast` | Auto cast node for static BlueprintPure functions |
| `BlueprintInternalUseOnly` | Internal implementation, never directly exposed |
| `BlueprintProtected` | Can only be called on owning Object |
| `CallableWithoutWorldContext` | Works even without GetWorld |
| `CommutativeAssociativeBinaryOperator` | Commutative binary operator node |
| `CompactNodeTitle="Name"` | Compact display name in Blueprint |
| `CustomStructureParam="Param1"` | Custom struct input pin |
| `DefaultToSelf` | Default value is "self" (owning object) |
| `HidePin="Param"` | Hides specified pin |
| `HideSelfPin` | Hides self pin |
| `InternalUseParam="Param"` | Parameter for internal use only |
| `Key="Value"` | Arbitrary key-value metadata |
| `Latent` | Latent action node |
| `LatentInfo="Param"` | Latent info parameter |
| `MaterialParameterCollectionFunction` | Material parameter collection function |
| `NativeBreak="Module.Class.Function"` | Custom Break Struct node |
| `NativeMake="Module.Class.Function"` | Custom Make Struct node |
| `NoGetter` | No "get" node generated (Sparse Class Data only) |
| `NoSetter` | No "set" node generated |
| `ShortTooltip="Text"` | Short tooltip |
| `ToolTip="Text"` | Full tooltip |
| `VectorParameter="Param"` | Vector parameter node |

### Property Metadata (Extended)

| Meta Tag | Effect |
|----------|--------|
| `AllowAbstract="true/false"` | Show abstract classes in Class picker |
| `AllowedClasses="Class1,Class2"` | Asset types for Asset picker |
| `AllowPreserveRatio` | Ratio lock for FVector properties |
| `ArrayClamp="ArrayProp"` | Clamp values to array length |
| `AssetBundles` | Bundle names for Primary Data Assets |
| `BlueprintBaseOnly` | Only Blueprint Classes in Class picker |
| `ClampMin="N"` / `ClampMax="N"` | Value range limits |
| `ConfigHierarchyEditable` | Serialized to config, settable anywhere in hierarchy |
| `ContentDir` | Slate-style directory picker in Content folder |
| `DisplayAfter="PropName"` | Show after named property |
| `DisplayName="Name"` | Override display name |
| `DisplayPriority="N"` | Sort order (1 = highest) |
| `EditCondition="BoolProp"` | Conditional editing. Supports `!` inversion and full expressions |
| `EditFixedOrder` | Prevents array element reordering by dragging |
| `ExposeOnSpawn="true"` | Expose on Spawn Actor node |
| `FilePathFilter="FileType"` | File picker filter (e.g., "uasset", "umap") |
| `HideAlphaChannel` | Hide Alpha for FColor/FLinearColor |
| `InlineEditConditionToggle` | Boolean shown inline as toggle, not own row |
| `LongPackageName` | Convert path to long package name |
| `MakeEditWidget` | Expose Transform/Rotator as movable viewport widget |

---

## 8. UPROPERTY — Property Specifiers

### Declaration
```cpp
UPROPERTY([specifier, ...], [meta(key=value, ...)])
Type VariableName;
```

### Core Data Types
| Type | Size | Notes |
|------|------|-------|
| `uint8`/`int8` | 1 byte | |
| `uint16`/`int16` | 2 bytes | |
| `uint32`/`int32` | 4 bytes | |
| `uint64`/`int64` | 8 bytes | |
| `float` | 4 bytes | |
| `double` | 8 bytes | |
| `FString` | dynamic | Mutable string |
| `FName` | fixed | Immutable, case-insensitive, global table. Fast pass-by-value |
| `FText` | fixed | Localization-ready |

### Boolean Types
```cpp
uint32 bIsHungry : 1;  // bitfield
bool bIsThirsty;        // standard bool
```

### Bitmask Properties
```cpp
// Generic flags
UPROPERTY(EditAnywhere, Meta = (Bitmask))
int32 BasicBits;

// Named flags from UENUM
UENUM(Meta = (Bitflags))
enum class EColorBits { ECB_Red, ECB_Green, ECB_Blue };

UPROPERTY(EditAnywhere, Meta = (Bitmask, BitmaskEnum = "EColorBits"))
int32 ColorFlags;

// Alternate: ENUM_CLASS_FLAGS with explicit values
UENUM(Meta = (Bitflags, UseEnumValuesAsMaskValuesInEditor = "true"))
enum class EColorBits { ECB_Red = 0x01, ECB_Green = 0x02, ECB_Blue = 0x04 };
ENUM_CLASS_FLAGS(EColorBits);
```

### Property Specifiers

| Specifier | Effect |
|-----------|--------|
| `EditAnywhere` | Editable on archetypes and instances. Incompatible with Visible* |
| `EditDefaultsOnly` | Editable only on archetypes |
| `EditInstanceOnly` | Editable only on instances |
| `EditFixedSize` | Prevents array length changes in editor |
| `VisibleAnywhere` | Visible but not editable. Incompatible with Edit* |
| `VisibleDefaultsOnly` | Visible only on archetypes |
| `VisibleInstanceOnly` | Visible only on instances |
| `BlueprintReadWrite` | Read/write from Blueprint |
| `BlueprintReadOnly` | Read-only from Blueprint |
| `BlueprintGetter=Func` | Custom accessor. Implies BlueprintReadOnly if no Setter |
| `BlueprintSetter=Func` | Custom mutator. Implies BlueprintReadWrite |
| `Category="Cat\|Sub"` | Blueprint editor category |
| `Config` | Saved to .ini file. Implies BlueprintReadOnly |
| `GlobalConfig` | Like Config but cannot override in subclass |
| `Transient` | Not saved/loaded. Zero-filled at load |
| `Replicated` | Network replication |
| `ReplicatedUsing=Func` | Replication with callback |
| `NotReplicated` | Skip replication (struct members only) |
| `SaveGame` | Include in save system |
| `Interp` | Driven by Sequencer track |
| `Instanced` | Unique copy per instance. Implies EditInline + Export |
| `NoClear` | Prevents setting to none in editor |
| `DuplicateTransient` | Reset to default on duplication |
| `AdvancedDisplay` | Hidden in advanced dropdown |
| `SimpleDisplay` | Visible without opening Advanced section |
| `Native` | C++ handles serialization and GC |
| `NoExport` | Not in auto-generated class declaration |
| `NonPIEDuplicateTransient` | Reset on duplication except PIE |
| `NonTransactional` | Not in undo/redo history |
| `Export` | Export full subobject on copy/paste |
| `RepRetry` | Retry replication if struct fails to send |
| `AssetRegistrySearchable` | Auto-added to Asset Registry |

### Bitmask in UFUNCTION Parameters
```cpp
UFUNCTION(BlueprintCallable)
void MyFunction(UPARAM(meta=(Bitmask, BitmaskEnum="EColorBits")) int32 ColorFlagsParam);
```

---

## 9. Typed Object Pointer Properties — TSubclassOf

### What Is TSubclassOf?
Template class providing UClass type safety. Restricts the editor's class picker to only show classes derived from the specified type.

### Without vs With TSubclassOf
```cpp
// BAD: Any UClass can be chosen
UPROPERTY(EditDefaultsOnly, Category=Damage)
UClass* DamageType;

// GOOD: Only UDamageType subclasses shown
UPROPERTY(EditDefaultsOnly, Category=Damage)
TSubclassOf<UDamageType> DamageType;
```

### Type Safety
```cpp
UClass* ClassA = UDamageType::StaticClass();

TSubclassOf<UDamageType> ClassB;
ClassB = ClassA;  // Runtime check — ok if compatible

TSubclassOf<UDamageType_Lava> ClassC;
ClassB = ClassC;  // Compile-time check — type error
```

- Up-casting: implicit (like raw pointers)
- Down-casting: `StaticCastSharedPtr` (no RTTI dynamic cast)
- Generic UClass assignment: runtime check, nullptr on failure

---

## 10. TArray — Dynamic Array Container

### Core Concept
UE's primary sequential container. Fast, memory-efficient, safe. Value type — deep copies on assignment, owns its elements.

```cpp
TArray<int32> IntArray;
```

### Population
```cpp
TArray<FString> Arr;
Arr.Init(TEXT("Vanilla"), 5);        // 5 copies of "Vanilla"
Arr.Add(TEXT("Chocolate"));          // Copy/move in
Arr.Emplace(TEXT("Strawberry"));     // Construct in-place (prefer over Add)
Arr.Append(OtherArray);              // Add all from another array
Arr.AddUnique(TEXT("Vanilla"));      // Only if not already present
Arr.Insert(TEXT("Mint"), 0);         // At specific index
Arr.SetNum(10);                      // Resize (default-construct new, remove excess)
```

### Iteration
```cpp
for (auto& Elem : Arr) { ... }                    // Range-for
for (int32 i = 0; i < Arr.Num(); ++i) { ... }     // Index-based
auto It = Arr.CreateIterator();                    // Iterator
auto ConstIt = Arr.CreateConstIterator();          // Read-only iterator
```

### Sorting
```cpp
Arr.Sort();                                        // Default operator<
Arr.Sort([](const FString& A, const FString& B) { return A.Len() < B.Len(); }); // Custom
Arr.HeapSort();                                    // Heap sort (unstable)
Arr.StableSort();                                  // Stable merge sort
```

### Queries
| Function | Description |
|----------|-------------|
| `Num()` | Element count |
| `GetData()` | Raw pointer to data |
| `operator[]` | Access by index (asserts on invalid) |
| `IsValidIndex(i)` | Bounds check |
| `Find(Value)` / `FindLast(Value)` | Write index, return bool. Or return index directly |
| `IndexOfByKey(Key)` | Find by arbitrary key type |
| `FindByKey(Key)` / `FindByPredicate(Pred)` | Return pointer or nullptr |
| `FilterByPredicate(Pred)` | Returns new TArray of matches |
| `Contains(Value)` / `ContainsByPredicate(Pred)` | Existence check |
| `Last()` / `Top()` | Access from end |

### Removal
| Function | Behavior |
|----------|----------|
| `Remove(Value)` | Remove ALL matches (shifts elements) |
| `RemoveSingle(Value)` | Remove first match only |
| `RemoveAt(Index)` | Remove at index (shifts) |
| `RemoveAll(Pred)` | Remove all matching predicate |
| `RemoveSwap(Value)` | Fast removal, NO order preservation |
| `RemoveAtSwap(Index)` | Fast removal at index, NO order preservation |
| `Empty()` | Remove all elements |

### Heap Operations
Root at index 0. Children of N: `2N+1`, `2N+2`.
```cpp
Arr.Heapify();          // Convert to heap
Arr.HeapPush(Elem);     // Add + re-heapify
Arr.HeapPop(Elem);      // Remove root (returns copy)
Arr.HeapPopDiscard();   // Remove root (no return)
Arr.HeapRemoveAt(i);    // Remove at index + re-heapify
Arr.HeapTop();          // Inspect root
```

### Slack Management
```cpp
Arr.Reserve(100);       // Preallocate for 100 elements
Arr.Shrink();           // Deallocate trailing slack
Arr.Compact();          // Consolidate active elements
Arr.Empty(0);           // Remove all + deallocate
```

### Operators
- `operator=` / copy ctor: deep copy
- `operator+=`: concatenate
- `MoveTemp()`: move semantics (source emptied)
- `operator==` / `operator!=`: element-wise comparison

---

## 11. TMap / TMultiMap — Key-Value Containers

### Overview
Hash-based containers storing `TPair<KeyType, ValueType>`.
- **TMap**: Unique keys. Adding duplicate key replaces value.
- **TMultiMap**: Multiple values per key.

### Requirements
- Key type must support `GetTypeHash()` and `operator==`
- **Unstable iteration order** — changes after modifications
- Elements NOT contiguous in memory
- Backed by sparse array

### Declaration & Population
```cpp
TMap<int32, FString> FruitMap;
FruitMap.Add(5, TEXT("Banana"));
FruitMap.Add(2, TEXT("Grapefruit"));
FruitMap.Add(2, TEXT("Pear"));      // Replaces value for key 2
FruitMap.Emplace(3, TEXT("Orange")); // Construct in-place

TMap<int32, FString> OtherMap;
OtherMap.Emplace(5, TEXT("Mango"));
FruitMap.Append(OtherMap);           // Moves all, empties OtherMap
```

### Iteration
```cpp
for (auto& Elem : FruitMap)
{
    // Elem.Key, Elem.Value
}

for (auto It = FruitMap.CreateConstIterator(); It; ++It)
{
    // It.Key(), It.Value()
}
```

### Queries
| Function | Description | Notes |
|----------|-------------|-------|
| `Num()` | Element count | |
| `Contains(Key)` | Key exists? | |
| `operator[]` | Value by key | **Asserts if key not found** |
| `Find(Key)` | Pointer to value or nullptr | Single lookup, efficient |
| `FindOrAdd(Key)` | Reference (adds default if missing) | May invalidate references |
| `FindRef(Key)` | Copy of value or default | Safe for const maps |
| `FindKey(Value)` | Reverse lookup (key pointer) | **Linear time, slow** |

### Removal
```cpp
FruitMap.Remove(Key);                    // Returns count removed (0 or 1)
FruitMap.FindAndRemoveChecked(Key);     // Returns value, asserts if missing
FruitMap.RemoveAndCopyValue(Key, Out);  // Copies value to Out, returns bool
FruitMap.Empty();                        // Remove all
```

### Sorting
```cpp
FruitMap.KeySort([](int32 A, int32 B) { return A > B; });
FruitMap.ValueSort([](const FString& A, const FString& B) { return A < B; });
```
Sorting only affects iteration order until next modification.

### Memory Management
```cpp
FruitMap.Reserve(10);    // Preallocate
FruitMap.Compact();      // Consolidate active elements
FruitMap.Shrink();       // Remove trailing slack
FruitMap.Empty(0);       // Remove all + deallocate
```

### Custom KeyFuncs
For types without `operator==`/`GetTypeHash`:
```cpp
template <typename ValueType>
struct TMyKeyFuncs : public BaseKeyFuncs<TPair<FMyStruct, ValueType>, FString>
{
    static const FString& GetSetKey(const TPair<FMyStruct, ValueType>& Element) { return Element.Key.UniqueID; }
    static bool Matches(const FString& A, const FString& B) { return A == B; }
    static uint32 GetKeyHash(const FString& Key) { return GetTypeHash(Key); }
};
```

---

## 12. TSet — Unique Element Container

### Overview
Fast, unordered container for unique elements where the element IS the key. Constant-time add/find/remove.

### Requirements
- Element type must support `operator==` and `GetTypeHash`
- **Unstable iteration order**
- Elements may be fragmented; pointers can be invalidated on reallocation

### Declaration & Population
```cpp
TSet<FString> FruitSet;
FruitSet.Add(TEXT("Apple"));
FruitSet.Add(TEXT("Banana"));
FruitSet.Emplace(TEXT("Pear"));
FruitSet.Add(TEXT("Banana"));  // Replaces existing, count stays 3

TSet<FString> SecondSet;
SecondSet.Add(TEXT("Kiwi"));
FruitSet.Append(SecondSet);
```

### Iteration
```cpp
for (const FString& Elem : FruitSet) { /*...*/ }
auto It = FruitSet.CreateConstIterator();
```

### Queries
| Function | Description |
|----------|-------------|
| `Num()` | Element count |
| `Contains(Value)` | Existence check |
| `Find(Value)` | Pointer to element or nullptr. Prefer over Contains+operator[] |
| `Index(Value)` | Returns FSetElementId (indices NOT stable) |
| `Array()` | Returns TArray copy of all elements |

### Removal
```cpp
FruitSet.Remove(Value);    // Returns count removed
FruitSet.Empty(0);         // Remove all, deallocate
FruitSet.Reset();          // Remove all, keep max slack
```

### Sorting
```cpp
FruitSet.Sort([](const FString& A, const FString& B) { return A < B; });
// Sorted order maintained until next modification
```

### Memory Management
```cpp
FruitSet.Reserve(100);     // Preallocate
FruitSet.Compact();        // Consolidate active elements
FruitSet.Shrink();         // Deallocate trailing slack
```

### Custom KeyFuncs
```cpp
struct MyKeyFuncs : public TDefaultKeyFuncs<MyElementType>
{
    typedef /* Key passing type */ KeyInitType;
    typedef /* Element passing type */ ElementInitType;
    static KeyInitType GetSetKey(ElementInitType Element);
    static bool Matches(KeyInitType A, KeyInitType B);
    static uint32 GetKeyHash(KeyInitType Key);
};
TSet<MyElementType, MyKeyFuncs> MySet;
```
**Rule:** Do not modify keys in ways that change `Matches` or `GetKeyHash` results.

---

## 13. Low-Level Memory Tracker (LLM)

### Overview
Profiling tool tracking ALL memory allocations using scoped-tag system. Complete, non-overlapping account of Engine + OS memory.

### Two Trackers
- **Default Tracker**: Higher-level. Tracks `FMemory::Malloc` (Engine allocations). Stats: `stat LLM`, `stat LLMFULL`
- **Platform Tracker**: Lower-level. Tracks all OS allocations. Stats: `stat LLMPlatform`
- Default Tracker stats are a subset of Platform Tracker

### Setup
| Command Line | Description |
|-------------|-------------|
| `-LLM` | Enable LLM |
| `-LLMCSV` | Write tag values to CSV every 5s. Auto-enables `-LLM` |
| `-llmtagsets=Assets` | (Experimental) Per-asset allocation |
| `-llmtagsets=AssetClasses` | (Experimental) Per-UObject class allocation |

| Console Command | Description |
|----------------|-------------|
| `stat LLM` | Summary (engine stats grouped) |
| `stat LLMFULL` | All stats in detail |
| `stat LLMPlatform` | OS-allocated memory |
| `stat LLMOverhead` | LLM's own memory usage |

### Key Built-in Tags
| Tag | Description |
|-----|-------------|
| `UObject` | All UObject-derived classes and serialized data |
| `EngineMisc` | Low-level untracked engine memory |
| `TaskGraphTasksMisc` | Task graph tasks without own category |
| `StaticMesh` | UStaticMesh class and properties (not mesh data) |

### Custom Tags
```cpp
// Header
LLM_DECLARE_TAG(MyTestTag);

// Source
LLM_DEFINE_TAG(MyTestTag);

// Usage — scope-based
void AMyActor::SomeFunction()
{
    LLM_SCOPE_BYTAG(MyTestTag);
    MyLargeBuffer.Reset(new uint8[1024*1024*1024]);
}
```

### Build Configs
- **Development**: Full LLM support
- **Test**: No on-screen stats, but writes CSV files
- **Shipping**: LLM completely compiled out
- Overhead: 100MB+ — use large memory mode on consoles

### Technical Details
- 21-byte overhead per allocation (pointer + hash + size + tag + index)
- Tags applied via stack macros: `LLM_SCOPE(Tag)` (Default) / `LLM_PLATFORM_SCOPE(Tag)` (Platform)
- Frame deltas tracked per-thread, summed at frame end
- Uses dedicated `LLMAlloc`/`LLMFree` to avoid recursive tracking
