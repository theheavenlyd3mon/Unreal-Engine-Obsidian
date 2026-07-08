# Local LLM Models — TurboHaul Setup

## Hardware
- **GPU:** NVIDIA RTX 4070 Ti (12 GB VRAM)
- **Server:** TurboHaul v0.3.0 — Docker container on port 11401
- **Config:** `C:\Users\Hermes\southpaw-turbohaul\turbohaul-custom.yaml`

## Active Models

### Carnice 35B-A3B MoE (APEX MTP)
- **Role:** Coding, tool calling, daily work
- **Base:** Qwen3.6 MoE 35B-A3B (3B active params)
- **File:** `Carnice-Qwen3.6-MoE-35B-A3B-APEX-MTP-I-Mini.gguf` (13.3 GB)
- **Context:** 262,144 tokens (256k)
- **KV Cache:** turbo3 (compressed)
- **Speed:** ~20-25 tok/s generation
- **Hermes tag:** `turbohaul-carnice`
- **Used by:** abilities, blender-coder, designer, threejs-coder, ue5-coder

### Darwin Apex 36B MoE (APEX I-Mini)
- **Role:** Reasoning, architecture, STEM, design decisions
- **Base:** Darwin 36B Opus evolutionary-merge fine-tune
- **File:** `Darwin-36B-Opus-APEX-I-Mini.gguf` (12.5 GB)
- **Context:** 262,144 tokens (256k)
- **KV Cache:** turbo3 (compressed)
- **Speed:** ~25 tok/s generation
- **Hermes tag:** `turbohaul-darwin`
- **Used by:** arch, worldbuilder

## Server Flags (Both Models)
```
--n-gpu-layers 99
--cpu-moe true          # Expert layers on CPU RAM (fits 12GB GPU)
--flash-attn on
--cache-type-k turbo3
--cache-type-v turbo3
--no-context-shift
--cache-reuse 256
--parallel 1
```

## Key Config Changes
- `safety_enabled: false` — Safety gate doesn't account for `cpu_moe`, counts full model body as GPU memory
- `grace_seconds: 10` — Quick model swaps (was 1800s/30min)
- `discover_models: false` — Avoids `/v1/models` 404 on TurboHaul

## Model Swap Behavior
- Cold load (different model): ~40-60s from disk
- Warm inherit (same model, within grace): instant
- Idle hold: 3600s (1 hour) after last request

## Inactive Models (in TurboHaul, not actively used)
| Model | Size | Context | Notes |
|-------|------|---------|-------|
| DeepSeek-V4-Flash-MTP | 9.1 GB | 40k | Distilled daily driver |
| Qwen3-14B | 9.8 GB | 48k | Creative writing |
| MN-Violet-Lotus-12B | 9.4 GB | 48k | NPC dialogue |
| Qwopus 3.5 9B | 9.1 GB | 48k | Coding (MTP) |

## Profile → Model Mapping
| Profile | Default Model | Purpose |
|---------|--------------|---------|
| ue5-coder | carnice-35b-moe | UE5 C++ implementation |
| abilities | carnice-35b-moe | GAS ability specs |
| blender-coder | carnice-35b-moe | Blender scripting |
| designer | carnice-35b-moe | Visual/UI design |
| threejs-coder | carnice-35b-moe | Three.js prototyping |
| arch | darwin-36b-moe | System architecture |
| worldbuilder | darwin-36b-moe | Lore & narrative |
