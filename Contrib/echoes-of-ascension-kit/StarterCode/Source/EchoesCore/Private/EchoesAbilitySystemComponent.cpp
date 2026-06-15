// Echoes of Ascension - starter scaffold.

#include "EchoesAbilitySystemComponent.h"
#include "EchoesGameplayAbility.h"
#include "Abilities/GameplayAbility.h"

UEchoesAbilitySystemComponent::UEchoesAbilitySystemComponent()
{
}

void UEchoesAbilitySystemComponent::GrantStartupAbilities(const TArray<TSubclassOf<UGameplayAbility>>& Abilities)
{
	// Server-authoritative. GiveAbility already no-ops off the authority, but guard explicitly
	// to make the intent clear and avoid any client-side churn.
	if (!IsOwnerActorAuthoritative())
	{
		return;
	}

	// Idempotency: the ASC is on the PlayerState and survives respawn, so PossessedBy fires for
	// each new avatar pawn. Grant the startup set only once, or specs accumulate across runs.
	if (bStartupAbilitiesGranted)
	{
		return;
	}

	for (const TSubclassOf<UGameplayAbility>& AbilityClass : Abilities)
	{
		if (AbilityClass)
		{
			GiveAbility(FGameplayAbilitySpec(AbilityClass, 1));
		}
	}

	bStartupAbilitiesGranted = true;
}

void UEchoesAbilitySystemComponent::AbilityInputTagPressed(const FGameplayTag& InputTag)
{
	if (!InputTag.IsValid())
	{
		return;
	}

	// Collect first, then activate — TryActivateAbility can mutate the activatable list.
	TArray<FGameplayAbilitySpecHandle> ToActivate;
	for (const FGameplayAbilitySpec& Spec : GetActivatableAbilities())
	{
		if (const UEchoesGameplayAbility* Ability = Cast<UEchoesGameplayAbility>(Spec.Ability))
		{
			if (Ability->InputTag == InputTag)
			{
				ToActivate.Add(Spec.Handle);
			}
		}
	}

	for (const FGameplayAbilitySpecHandle& Handle : ToActivate)
	{
		TryActivateAbility(Handle);
	}
}
