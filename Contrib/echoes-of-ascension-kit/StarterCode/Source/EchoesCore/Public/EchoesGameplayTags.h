// Echoes of Ascension - starter scaffold.

#pragma once

#include "NativeGameplayTags.h"

// Native gameplay tags, resolved at startup. Reference as EchoesTags::InputTag_Attack etc.
//
// Note: no ECHOESCORE_API export macro here. UE_DECLARE_GAMEPLAY_TAG_EXTERN expands to
// `extern FNativeGameplayTag <Tag>;` — prefixing it with the module API macro emits
// `__declspec(dllexport) extern ...` (declspec before the storage-class specifier, which
// MSVC flags, promoted to an error under UE's warnings-as-errors), and would be asymmetric
// with the unmarked UE_DEFINE_GAMEPLAY_TAG in the .cpp. These tags are referenced within
// EchoesCore, so no export is needed; this matches Epic's native-tag idiom (Lyra).
namespace EchoesTags
{
	UE_DECLARE_GAMEPLAY_TAG_EXTERN(InputTag_Attack);
	UE_DECLARE_GAMEPLAY_TAG_EXTERN(InputTag_Ability1);
	UE_DECLARE_GAMEPLAY_TAG_EXTERN(InputTag_Dash);
	UE_DECLARE_GAMEPLAY_TAG_EXTERN(Ability_Attack);
	UE_DECLARE_GAMEPLAY_TAG_EXTERN(Ability_Dash);
	UE_DECLARE_GAMEPLAY_TAG_EXTERN(Cooldown_Dash);
	UE_DECLARE_GAMEPLAY_TAG_EXTERN(Data_Damage);
	UE_DECLARE_GAMEPLAY_TAG_EXTERN(State_Dead);
}
