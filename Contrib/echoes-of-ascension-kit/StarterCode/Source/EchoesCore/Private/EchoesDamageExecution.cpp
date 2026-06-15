// Echoes of Ascension - starter scaffold.

#include "EchoesDamageExecution.h"
#include "EchoesAttributeSet.h"
#include "EchoesGameplayTags.h"
#include "AbilitySystemComponent.h"

// Canonical GAS capture pattern: snapshot the source's AttackPower.
struct FEchoesDamageStatics
{
	DECLARE_ATTRIBUTE_CAPTUREDEF(AttackPower);

	FEchoesDamageStatics()
	{
		DEFINE_ATTRIBUTE_CAPTUREDEF(UEchoesAttributeSet, AttackPower, Source, false);
	}
};

static const FEchoesDamageStatics& DamageStatics()
{
	static FEchoesDamageStatics Statics;
	return Statics;
}

UEchoesDamageExecution::UEchoesDamageExecution()
{
	RelevantAttributesToCapture.Add(DamageStatics().AttackPowerDef);
}

void UEchoesDamageExecution::Execute_Implementation(const FGameplayEffectCustomExecutionParameters& ExecutionParams,
	FGameplayEffectCustomExecutionOutput& OutExecutionOutput) const
{
	const FGameplayEffectSpec& Spec = ExecutionParams.GetOwningSpec();

	FAggregatorEvaluateParameters EvalParams;
	EvalParams.SourceTags = Spec.CapturedSourceTags.GetAggregatedTags();
	EvalParams.TargetTags = Spec.CapturedTargetTags.GetAggregatedTags();

	float AttackPower = 0.f;
	ExecutionParams.AttemptCalculateCapturedAttributeMagnitude(DamageStatics().AttackPowerDef, EvalParams, AttackPower);
	float Damage = FMath::Max(AttackPower, 0.f);

	// Optional flat bonus passed via SetByCaller. WarnIfNotFound=false → returns 0 when absent,
	// so we don't need to probe the spec's internal magnitude map by name.
	Damage += Spec.GetSetByCallerMagnitude(EchoesTags::Data_Damage, /*WarnIfNotFound=*/false, /*Default=*/0.f);

	OutExecutionOutput.AddOutputModifier(
		FGameplayModifierEvaluatedData(UEchoesAttributeSet::GetDamageAttribute(), EGameplayModOp::Additive, Damage));
}
