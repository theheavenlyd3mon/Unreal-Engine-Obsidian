# UE5 Gameplay Ability System (GAS) Reference

#ue5 #cpp #reference #gas #gameplay-abilities #gameplay-effects #attributes

> Comprehensive GAS reference — overview, abilities, attributes, effects, ability tasks, and networking. From Epic UE 5.8 documentation.

---

## Overview

GAS is a framework for building abilities and interactions in UE5. Designed for RPGs, action-adventure, MOBAs. Supports network replication.

**Core Components:**
1. **Ability System Component (ASC)** — Bridge between Actors and GAS
2. **Gameplay Abilities** — Define ability behavior, cost, conditions, execution
3. **Attribute Sets** — Manage floating-point stats (Health, Mana, etc.)
4. **Gameplay Effects** — Modify attributes (damage, buffs, debuffs)
5. **Gameplay Cues** — Cosmetic feedback (VFX, SFX) via tags
6. **Ability Tasks** — Async work during ability execution

---

## Ability System Component (ASC)

### Setup Pattern
```cpp
class AMyActor : public AActor, public IAbilitySystemInterface
{
    virtual UAbilitySystemComponent* GetAbilitySystemComponent() const override;

    UPROPERTY(VisibleDefaultsOnly, BlueprintReadOnly, Category = "Abilities")
    UAbilitySystemComponent* AbilitySystemComponent;
};

UAbilitySystemComponent* AMyActor::GetAbilitySystemComponent() const
{
    return AbilitySystemComponent;
}
```

### Key Rules
- **Single ASC per Actor** — multiple Actors CAN share one ASC, but an Actor cannot have multiple
- **Pawn vs PlayerState** — Store GAS data on PlayerState for persistence across respawns
- **Cross-Actor Sharing** — Pawn can use PlayerState's ASC; cache the pointer

---

## Gameplay Abilities

### Lifecycle
1. `CanActivateAbility` — Check availability (UI greying)
2. `TryActivateAbility` — Standard activation (calls CanActivate then CallActivate)
3. `CallActivateAbility` → `ActivateAbility` — Custom logic
4. `CommitAbility` — Apply cost/cooldowns
5. `EndAbility` — **MUST be called** or ability blocks forever

> **CRITICAL:** Failing to call `EndAbility` prevents future activations.

### Granting & Revoking (Server Only)
```cpp
// Grant
FGameplayAbilitySpecHandle Handle = ASC->GiveAbility(FGameplayAbilitySpec(AbilityClass));
ASC->GiveAbilityAndActivateOnce(Spec);  // Grant + one-shot

// Revoke
ASC->ClearAbility(Handle);
ASC->SetRemoveAbilityOnEnd(Handle);  // Remove after current execution
ASC->ClearAllAbilities();
```

### Tag Interactions

| Tag Variable | Purpose |
|--------------|---------|
| `Cancel Abilities With Tag` | Cancel executing abilities with matching tags |
| `Block Abilities With Tag` | Block execution of abilities with matching tags |
| `Activation Owned Tags` | Grant tags to owner while executing |
| `Activation Required Tags` | Owner must have these tags to activate |
| `Activation Blocked Tags` | Owner must NOT have these tags to activate |
| `Target Required Tags` | Target must have these tags |
| `Target Blocked Tags` | Target must NOT have these tags |

### Network Replication Policy

| Policy | Behavior |
|--------|----------|
| **Local Predicted** | Runs locally, server validates/overrides |
| **Local Only** | Runs locally only, no server replication |
| **Server Initiated** | Starts on server, propagates to clients |
| **Server Only** | Server only, data replicates normally |

### Instancing Policy

| Policy | Description | Use Case |
|--------|-------------|----------|
| **Instanced per Actor** | One instance, reused | **Default for UE 5.5+.** Good for replication, scales well |
| ~~Instanced per Execution~~ | ~~New object each run~~ | **Deprecated in UE 5.5** — use InstancedPerActor |
| ~~Non-Instanced~~ | ~~Uses CDO (no spawn)~~ | **Deprecated in UE 5.5** — use InstancedPerActor |

### Triggering via Gameplay Events
```cpp
// Send event to actor
FGameplayEventData EventData;
EventInstigator = InstigatorAbilitySystemComponent;
EventData.Target = TargetActor;
UAbilitySystemBlueprintLibrary::SendGameplayEventToActor(
    TargetActor, FGameplayTag::RequestGameplayTag("Event.Attack"), EventData);

// In ability: handle with ActivateAbilityFromEvent (not standard ActivateAbility)
```

---

## Gameplay Attributes & Attribute Sets

### Creating an Attribute Set
```cpp
UCLASS()
class MYPROJECT_API UMyAttributeSet : public UAttributeSet
{
    GENERATED_BODY()
public:
    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    FGameplayAttributeData Health;
    ATTRIBUTE_ACCESSORS(UMyAttributeSet, Health)  // Generated helpers

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    FGameplayAttributeData Mana;
    ATTRIBUTE_ACCESSORS(UMyAttributeSet, Mana)
};
```

### Helper Macros

| Macro | Generated Function | Purpose |
|-------|-------------------|---------|
| `GAMEPLAYATTRIBUTE_PROPERTY_GETTER(Set, Attr)` | `static FGameplayAttribute GetAttr()` | Reflection getter |
| `GAMEPLAYATTRIBUTE_VALUE_GETTER(Attr)` | `float GetAttr() const` | Get current value |
| `GAMEPLAYATTRIBUTE_VALUE_SETTER(Attr)` | `void SetAttr(float)` | Set value |
| `GAMEPLAYATTRIBUTE_VALUE_INITTER(Attr)` | `void InitAttr(float)` | Initialize value |

### Dual Values
- **Base Value** — Long-term, modified by Instant effects
- **Current Value** — Modified by active Duration/Infinite effects

Example: JumpHeight base=100. Effect reduces to 70% → current=70. Base increases to 110 → current=77.

### Controlling Attribute Access
```cpp
float UMyAttributeSet::GetHealth() const
{
    return FMath::Max(Health.GetCurrentValue(), 0.0f);
}

void UMyAttributeSet::SetHealth(float NewVal)
{
    NewVal = FMath::Max(NewVal, 0.0f);
    UAbilitySystemComponent* ASC = GetOwningAbilitySystemComponent();
    if (ensure(ASC))
    {
        ASC->SetNumericAttributeBase(GetHealthAttribute(), NewVal);
    }
}
```

### Interaction with Gameplay Effects
Override these in your AttributeSet:

| Function | Purpose |
|----------|---------|
| `PreAttributeChange` | Before current value changes. Clamp here. |
| `PreAttributeBaseChange` | Before base value changes. |
| `PreGameplayEffectExecute` | Before instant effect executes. |
| `PostGameplayEffectExecute` | After effect executes. React here (e.g., clamp, trigger death). |
| `PostAttributeChange` | After any attribute change. |

### Initialization from Data Table
Row type: `AttributeMetaData`. Case-sensitive naming: `AttributeSetName.AttributeName`.

```csv
---,BaseValue,MinValue,MaxValue,DerivedAttributeInfo,bCanStack
MyAttributeSet.Health,"100.000000","0.000000","150.000000","","False"
```

> MinValue/MaxValue are NOT enforced by GAS — clamp in code.

---

## Gameplay Effects

### Duration Types

| Type | Behavior |
|------|----------|
| **Instant** | Applied immediately. Modifies Base value. |
| **Has Duration** | Lasts limited time. Modifies Current value. Can be periodic. |
| **Infinite** | Persists indefinitely. Modifies Current value. |

### Terminology
- **Executed** — Instant GE, applied immediately, never enters active container
- **Applied** — General term for GE taking effect
- **Added & Executed** — Periodic effects: added to container AND executed each period

### GE Components

| Component | Purpose |
|-----------|---------|
| `UChanceToApplyGameplayEffectComponent` | Probability to apply |
| `UBlockAbilityTagsGameplayEffectComponent` | Block ability activation on target |
| `UAssetTagsGameplayEffectComponent` | Tags on the GE asset itself (don't transfer to Actors) |
| `UAdditionalEffectsGameplayEffectComponent` | Chain other GEs under conditions |
| `UTargetTagsGameplayEffectComponent` | Grant tags to receiving Actor |
| `UTargetTagRequirementsGameplayEffectComponent` | Require target tags to apply/continue |
| `URemoveOtherGameplayEffectComponent` | Remove other active GEs |
| `UCustomCanApplyGameplayEffectComponent` | Custom apply condition |
| `UImmunityGameplayEffectComponent` | Block incoming GE Specs |

### Stacking
Policy for multiple instances of same GE on target (stacking buffs, threshold building, timer resets).

### Gameplay Cues
- Cosmetic feedback (VFX, SFX) linked via tags
- Must use `GameplayCue.*` tag
- Functions: `On Active`, `While Active`, `Removed`, `Executed`
- **Do NOT use for gameplay-critical feedback** — unreliable replication
- Use Ability Tasks for replicated logic (Play Montage, etc.)

---

## Ability Tasks

### What Are They?
Async operations during ability execution. Enable abilities to span multiple frames and perform parallel work.

### Key Behavior
- Self-terminate via `EndTask()` or auto-terminate when parent Ability ends
- Stay in sync indirectly via replicated Abilities and networked variables
- Most have immediate execution pin + task-specific delayed pins

### Common Tasks
- **PlayMontageAndWait** — Play anim montage, wait for event/commit
- **WaitGameplayEvent** — Listen for gameplay event with matching tag
- **WaitDelay** — Timer-based delay
- **WaitInputPress** — Wait for player input
- **WaitTargetData** — Aiming/targeting with confirmation

### Creating Custom Ability Tasks
```cpp
UCLASS()
class UMyAbilityTask : public UAbilityTask
{
    GENERATED_BODY()
public:
    DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnTaskComplete);

    UPROPERTY(BlueprintAssignable)
    FOnTaskComplete OnComplete;

    static UMyAbilityTask* CreateTask(UGameplayAbility* Ability);
    virtual void Activate() override;
    virtual void OnDestroy(bool AbilityEnded) override;
};
```

---

## GAS Networking Summary

- ASC does NOT replicate full state — only Attributes and Tags
- **Prediction:** Abilities activate locally first, server validates
- Server may REJECT activation → requires rollback
- Non-instant GEs support rollback (preferred for tag/cue/attribute changes)
- Interact with server-owned objects through locally owned Actor (Pawn)
