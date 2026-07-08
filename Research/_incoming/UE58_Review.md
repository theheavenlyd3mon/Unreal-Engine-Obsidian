# UE 5.8 Brief Review
Reviewed: 2026-07-08  
Input: `/Users/noctis/Unreal-Engine-Obsidian/Research/_incoming/UE58_API_Changes.md`  
Cross-check: `UE5_CPP/UE5_GAS_Reference.md`, `UE5_CPP/UE5_Gameplay_Framework_Reference.md`, `UE5_Cpp_Reference_Guide.md`

## VERDICT
APPROVE_WITH_FIXES

## Summary
The brief is vault-ready in shape and sourcing discipline. Most API/convention claims map cleanly to Epic’s official UE 5.8 Release Notes and the cited references; I do not see fabricated symbols. The remaining issues are missing specificity, not bad faith.

## Findings

### Accuracy / source coverage (mostly good | minor precision gaps)
- Corroborated from Epic 5.8 Release Notes snippets:
  - `FInputDeviceScope` deprecation → `FInputDeviceRegistry`, legacy compat define.
  - PhysicsMover/NetworkPhysicsLiaison removal → ChaosMover.
  - `UAdditionalEffectsGameplayEffectComponent` `RemovalPolicy` / content-validation rules.
  - `FActiveGameplayEffectHandle` attaching to owning ASC rather than global map.
  - `ConvertLegacyDNAAssets` commandlet and `bUseOptimizedCooking`.
  - MegaLights PR, Lumen Lite Beta, Substrate Toon Shading Experimental, FSSS Experimental.
  - `LexToString(bool)` implicit bool-cast fix and `FSharedEventRef` constructor/mode fix.
- Needs-more:
  - “UE_PLATFORM_*” row is directionally correct, but I do not see the exact snippet confirming `UE_PLATFORM_*` addition is present in all forms or that `UE_LOG` is functionally deprecated. The brief says “Deprecated” — that is a strong word; downgrade to “Discouraged/migration target” until a direct RN sentence is attached.

### Version compatibility
- Claims are correctly bucketed; 5.7 vs 5.8 usage is mostly accurate.
- Flag: “Last planned major UE5 release” wording is unverified inside the Release Notes page I spot-checked; the launch announcement citation exists, but the Release Notes page does not repeat it. Keep it, but tighten phrasing to “Epic has stated” rather than treat as documented migration truth.

### Gaps
- No explicit mention of:
  - Incremental Cooking Beta + ZenServer default cook store behavior.
  - Mass entity-system scheduler rewrite.
  - iOS Shader Model 6 via Metal Shader Converter.
  - Windows Game Input redist packaging (`IncludeRedistFiles`).
- These should be added under “New Systems / Platform notes” or flagged explicitly as missing.

### Fabrication risk
- Low. No made-up symbols observed. The UNVERIFIED marker is used appropriately.

### Vault consistency
- Existing vault references are written from 5.x-era docs; they do not yet include 5.8 APIs. The brief is consistent with them and helps future-proof upgrades — it does not contradict the current GAS/Gameplay Framework reference.

## Required corrections / additions
1. Soften the `UE_LOG` deprecation claim; make it “migration recommendation” unless a 5.8-specific sentence is added.
2. Add missing new-system bullets noted above or mark as `[UNVERIFIED: not covered]` if source is not attached.
3. Tighten the “last planned UE5 release” sentence to attribute it to the launch announcement only.

## Post-change checklist before approve removal
- [ ] Every deprecation claim has an exact RN sentence or anchor.
- [ ] New Systems section covers at least Cooking/OS builds/Mobile/RPG-relevant systems.
- [ ] Vault MOC update note added when this gets approved.
