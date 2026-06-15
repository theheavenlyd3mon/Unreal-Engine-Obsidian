---
title: "GAS Replication & Architecture Gotchas"
created: 2026-06-13
updated: 2026-06-13
type: concept
tags: [unreal-engine, gas, gameplay-ability-system, replication, multiplayer, c++, gotchas]
composes: []
composed_by: []
topics: [unreal-engine, game-development, rpg, gas]
workflow: developing
confidence: high
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/understanding-the-unreal-engine-gameplay-ability-system", "https://github.com/tranek/GASDocumentation", "https://vorixo.github.io/devtricks/gas/", "https://gascompanion.github.io/asc-on-player-state/"]
---

# GAS Replication & Architecture Gotchas

The stuff the GAS tutorials skip — the decisions that make it "work in single-player, break in co-op." Tutorials show you how to grant an ability; almost none cover ownership semantics, init timing, or replication modes, and those are exactly what bite an RPG with planned co-op.

## Overview

GAS is network-aware by design, but it assumes you set up ownership correctly. The two questions that decide everything: **who owns the AbilitySystemComponent (ASC)**, and **who is allowed to see what**. Get these wrong and you get attribute "ghosts," missing cues on other clients, or abilities that never initialize on the owning client.

## Replication Modes: pick by role

The ASC has three replication modes. Set it once (`SetReplicationMode`) and choose by the entity's network role:

- **Full** — replicates active GameplayEffects (durations, stacks) to **everyone**.
  - Use for: single-player, and AI enemies in MP where every client needs full effect detail.
- **Mixed** (the player-hero standard for co-op) — GameplayEffects replicate to the **owning client only**; GameplayTags and GameplayCues replicate to everyone.
  - Use for: player-controlled heroes in MP. Other players still see your cues (VFX) and can read your tags (e.g. `State.Stunned`), but don't get your full effect list. Less bandwidth, no "attribute peeking."
- **Minimal** — GameplayEffects replicate to **no one** (server-only); tags/cues still go out via the ASC.
  - Use for: AI minions in MP where clients don't need the effect detail.

## The Mixed-mode Owner trap (top bug)

Mixed mode requires that the ASC **OwnerActor's `Owner` is the Controller**.

- `PlayerState`'s `Owner` **is** the Controller by default → if your ASC lives on the PlayerState, this just works.
- A `Character`/`Pawn`'s `Owner` is **not** the Controller by default → if your ASC lives on the Character and you use Mixed mode, you must set it:

```cpp
// In ACharacter::PossessedBy(AController* NewController) — server side
Super::PossessedBy(NewController);
SetOwner(NewController);   // AActor::SetOwner — makes Owner->GetOwner() resolve to the Controller
```

Symptom when you forget: cues/tags replicate fine, but the owning client never receives its own GameplayEffects, so cooldowns/buffs look broken only on the client.

## ASC placement: PlayerState vs Pawn

```text
+------------------------+        +------------------------+
|      PlayerState       |        |     Character/Pawn     |
|   (OwnerActor of ASC)  |        |   (AvatarActor)        |
|  - survives respawn    |        |  - destroyed on death  |
|  - holds ASC + Attrs   |  --->  |  - the body abilities   |
|  - replicated to all   |        |    act through         |
+------------------------+        +------------------------+
        OwnerActor = PlayerState,  AvatarActor = Pawn
```

- **Players → ASC on `PlayerState`.** Rule: *anything that respawns must have `OwnerActor != AvatarActor`* so the ASC is **not** destroyed with the body. Attributes, active effects, and cooldowns persist across death without save/restore gymnastics.
- **AI / minions → ASC on the `Pawn`/`Character`.** They don't respawn (or are pooled), so co-locating ASC with the mesh is simpler.

## PlayerState NetUpdateFrequency

`PlayerState` is a low-priority actor by default (~1–10 Hz). With the ASC on it, that throttles attribute/ability replication — health bars jump, ability state lags.

```cpp
// In APlayerState subclass constructor or BeginPlay (UE 5.x uses the setter)
SetNetUpdateFrequency(100.f);
```

## InitAbilityActorInfo timing (the "client has no abilities" bug)

Abilities/attributes are bound when `InitAbilityActorInfo(OwnerActor, AvatarActor)` runs. With ASC on PlayerState you must call it in **two** places, because the server and the owning client learn about the PlayerState at different times:

```cpp
// SERVER: the controller possesses the pawn
void AMyCharacter::PossessedBy(AController* NewController)
{
    Super::PossessedBy(NewController);
    if (AMyPlayerState* PS = GetPlayerState<AMyPlayerState>())
        PS->GetAbilitySystemComponent()->InitAbilityActorInfo(PS, this);
}

// OWNING CLIENT: PlayerState replicates down after the pawn
void AMyCharacter::OnRep_PlayerState()
{
    Super::OnRep_PlayerState();
    if (AMyPlayerState* PS = GetPlayerState<AMyPlayerState>())
        PS->GetAbilitySystemComponent()->InitAbilityActorInfo(PS, this);
}
```

Init in `BeginPlay` instead and the client's `PlayerState` is often still null → no abilities, no attributes, silent failure.

## Grant startup abilities once (the respawn duplicate-grant trap)

Initializing `AbilityActorInfo` on **every** `PossessedBy` is correct (above). The trap is doing the same with the *grant*. Because the ASC lives on the respawn-surviving `PlayerState`, a new avatar pawn is possessed on every respawn / new run, so a `GiveAbility` loop in `PossessedBy` runs **again** and stacks duplicate `FGameplayAbilitySpec`s on the same ASC. Cooldowns/charges then misbehave and input-tag activation can fire the "same" ability twice.

Grant from the ASC and guard it, so the call is idempotent no matter how often `PossessedBy` fires:

```cpp
// In your ASC subclass — granted once for the ASC's lifetime, server-authoritative.
void UMyAbilitySystemComponent::GrantStartupAbilities(const TArray<TSubclassOf<UGameplayAbility>>& Abilities)
{
    if (!IsOwnerActorAuthoritative() || bStartupAbilitiesGranted)
        return;
    for (const TSubclassOf<UGameplayAbility>& Ability : Abilities)
        if (Ability)
            GiveAbility(FGameplayAbilitySpec(Ability, 1));
    bStartupAbilitiesGranted = true;   // bool member on the ASC; not replicated
}
```

Symptom when you forget: abilities work on first spawn, then after a death/respawn the player has 2× (then 3×…) of each granted ability. Note attribute init is the *opposite* case — re-applying `GE_InitStats` on respawn is usually what you want (full health on a fresh body), so guard the **grant**, not the attribute seed. The starter `EchoesAbilitySystemComponent` ships this guard.

## AttributeSet: creation, replication, init

- **Create** the AttributeSet with `CreateDefaultSubobject` on the ASC's owner (the PlayerState for players). Owning an AttributeSet is what registers its attributes with the ASC.
- **Replicate attributes** inside the AttributeSet's `GetLifetimeReplicatedProps`, one macro per attribute:

```cpp
void UMyAttributeSet::GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& Out) const
{
    Super::GetLifetimeReplicatedProps(Out);
    DOREPLIFETIME_CONDITION_NOTIFY(UMyAttributeSet, Health,    COND_None, REPNOTIFY_Always);
    DOREPLIFETIME_CONDITION_NOTIFY(UMyAttributeSet, MaxHealth, COND_None, REPNOTIFY_Always);
}

// and a RepNotify per attribute that calls the GAS helper:
void UMyAttributeSet::OnRep_Health(const FGameplayAttributeData& Old)
{
    GAMEPLAYATTRIBUTE_REPNOTIFY(UMyAttributeSet, Health, Old);
}
```

`REPNOTIFY_Always` matters: by default a RepNotify is skipped if the value looks unchanged, which breaks attribute reconciliation. The ASC's **replication mode** (Mixed/Full/Minimal) governs *who* gets effect data — you don't gate the AttributeSet itself with `COND_OwnerOnly`.

- **Initialize values** by applying an instant `GameplayEffect` (e.g. `GE_InitStats`, often backed by a CurveTable/DataTable), **never** by hardcoding in C++. Server-authoritative init flows through replication for free.

## Math goes in GameplayEffects, not Tick

All gameplay math — damage, healing, stat scaling — belongs in **Modifier Magnitude Calculations** (`UGameplayModMagnitudeCalculation`) or **Execution Calculations** (`UGameplayEffectExecutionCalculation`). Tick-driven mutation isn't predicted, isn't authoritative, and desyncs. GEs are the source of truth.

## Work *with* prediction, not around it

GAS has built-in client-side prediction: `TryActivateAbility` → prediction key → server validates → reconcile. Don't bypass it by mutating attributes directly from a button press; you'll get rubber-banding and rollback artifacts. Let the ability/effect pipeline own the state change.

## Echoes of Ascension mapping

- **Aether Mastery skills** → `UGameplayAbility` (elemental affinities = ability tags; hybrid builds = tag-gated ability grants).
- **Attributes / stats behind Aetheric Renown gates** → `UAttributeSet`, initialized via GE, replicated as above.
- **Echoes bound to gear/skills** → `UGameplayEffect` applied on equip and removed on unequip, with `FGameplayTag`s for synergy checks.
- Because the Tower is the planned co-op space, build all hero abilities in **Mixed** mode from the start — see [[03_Multiplayer_From_Day_One]].

---

- → Next: [[02_OpenWorld_Save_Architecture]]
- 📚 Series: [[_MOC_UE5_Gotchas]]
- 🔗 Related: [[unreal-engine-gameplay-ability-system]] · [[GASDocumentation]]
