// Echoes of Ascension - starter scaffold.

#include "EchoesCharacter.h"
#include "AbilitySystemComponent.h"
#include "EchoesAbilitySystemComponent.h"
#include "EchoesPlayerState.h"
#include "GameplayEffect.h"
#include "Abilities/GameplayAbility.h"

AEchoesCharacter::AEchoesCharacter()
{
}

UAbilitySystemComponent* AEchoesCharacter::GetAbilitySystemComponent() const
{
	if (const AEchoesPlayerState* PS = GetPlayerState<AEchoesPlayerState>())
	{
		return PS->GetAbilitySystemComponent();
	}
	return nullptr;
}

void AEchoesCharacter::PossessedBy(AController* NewController)
{
	Super::PossessedBy(NewController);

	// SERVER: the PlayerState exists by now.
	if (AEchoesPlayerState* PS = GetPlayerState<AEchoesPlayerState>())
	{
		InitAbilityActorInfoFor(PS, this);
		GiveDefaultAbilities();
		InitDefaultAttributes();
	}
}

void AEchoesCharacter::OnRep_PlayerState()
{
	Super::OnRep_PlayerState();

	// OWNING CLIENT: the PlayerState has just replicated down. Init here so the local client
	// gets its ability actor info (needed for prediction).
	if (AEchoesPlayerState* PS = GetPlayerState<AEchoesPlayerState>())
	{
		InitAbilityActorInfoFor(PS, this);
	}
}

void AEchoesCharacter::GiveDefaultAbilities()
{
	if (!HasAuthority())
	{
		return;
	}

	// Delegate to the ASC so the grant is idempotent. The ASC lives on the PlayerState and
	// survives respawn, so this runs again for every new avatar pawn — a naive GiveAbility loop
	// here would stack duplicate specs across runs. See UE5_Gotchas/01.
	if (UEchoesAbilitySystemComponent* ASC = Cast<UEchoesAbilitySystemComponent>(GetAbilitySystemComponent()))
	{
		ASC->GrantStartupAbilities(DefaultAbilities);
	}
}

void AEchoesCharacter::InitDefaultAttributes()
{
	if (!HasAuthority() || !DefaultAttributesEffect)
	{
		return;
	}

	UAbilitySystemComponent* ASC = GetAbilitySystemComponent();
	if (!ASC)
	{
		return;
	}

	FGameplayEffectContextHandle Context = ASC->MakeEffectContext();
	Context.AddSourceObject(this);

	// Level 1 — the init effect sets flat starting values; scale later if you add leveling.
	const FGameplayEffectSpecHandle SpecHandle = ASC->MakeOutgoingSpec(DefaultAttributesEffect, 1.f, Context);
	if (SpecHandle.IsValid())
	{
		ASC->ApplyGameplayEffectSpecToSelf(*SpecHandle.Data.Get());
	}
}

void AEchoesCharacter::InitAbilityActorInfoFor(AActor* InOwnerActor, AActor* InAvatarActor)
{
	if (UAbilitySystemComponent* ASC = GetAbilitySystemComponent())
	{
		ASC->InitAbilityActorInfo(InOwnerActor, InAvatarActor);
	}
}
