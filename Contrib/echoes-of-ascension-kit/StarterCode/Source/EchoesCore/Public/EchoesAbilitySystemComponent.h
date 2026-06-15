// Echoes of Ascension - starter scaffold.

#pragma once

#include "CoreMinimal.h"
#include "AbilitySystemComponent.h"
#include "GameplayTagContainer.h"
#include "Templates/SubclassOf.h"
#include "EchoesAbilitySystemComponent.generated.h"

class UGameplayAbility;

/**
 * Project ASC subclass. Adds input-tag ability activation: bind your Enhanced Input actions to
 * AbilityInputTagPressed() and abilities tagged with the matching UEchoesGameplayAbility::InputTag fire.
 */
UCLASS()
class ECHOESCORE_API UEchoesAbilitySystemComponent : public UAbilitySystemComponent
{
	GENERATED_BODY()

public:
	UEchoesAbilitySystemComponent();

	/**
	 * Grant the startup ability set once for the lifetime of this ASC (server-authoritative).
	 * The ASC lives on the (respawn-surviving) PlayerState, so the avatar pawn is re-possessed
	 * on every respawn / new run — granting on each PossessedBy would stack duplicate specs.
	 * This guards against that, so it is safe to call from PossessedBy. No-ops off the authority.
	 */
	void GrantStartupAbilities(const TArray<TSubclassOf<UGameplayAbility>>& Abilities);

	/** Try-activate every granted ability whose UEchoesGameplayAbility::InputTag equals InputTag. */
	void AbilityInputTagPressed(const FGameplayTag& InputTag);

protected:
	/** True once GrantStartupAbilities has run. Server-only bookkeeping; not replicated. */
	bool bStartupAbilitiesGranted = false;
};
