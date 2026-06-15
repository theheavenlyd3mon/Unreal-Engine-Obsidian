// Echoes of Ascension - starter scaffold.

using UnrealBuildTool;

public class EchoesCore : ModuleRules
{
	public EchoesCore(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

		PublicDependencyModuleNames.AddRange(new string[]
		{
			"Core",
			"CoreUObject",
			"Engine",
			"InputCore",
			// GAS
			"GameplayAbilities",
			"GameplayTags",
			"GameplayTasks",
			// AI — EchoesAIController.h includes AIController.h + holds a UBehaviorTree*,
			// and EchoesAIController.cpp calls RunBehaviorTree(). All three live in AIModule.
			// The include is in a PUBLIC header, so this must be a public dependency.
			"AIModule"
		});

		PrivateDependencyModuleNames.AddRange(new string[]
		{
			"EnhancedInput"
		});
	}
}
