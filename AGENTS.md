# Agent Contribution Guide

This repository is an Obsidian vault for Unreal Engine 5 learning and RPG development. Agents should treat it as a structured knowledge base, not a generic notes dump.

## Hard Rules

- Do not claim `compile-tested`, `editor-tested`, or `playtested` unless that exact verification was actually performed.
- Do not add or modify Unreal Engine starter code unless you can state the UE version, target, toolchain, and verification level.
- Prefer Epic docs, engine source, Lyra, tranek GASDocumentation, and canonical references over blogs or AI memory.
- Keep changes small and reviewable. Do not rewrite broad tutorial content unless the PR is explicitly scoped to that rewrite.
- Update the relevant `_MOC_*.md` when adding a durable note that should be discoverable.
- Run `python3 tools/vault_lint.py .` before drafting a PR when the linter exists.
- Do not push branches or open PRs unless the human reviewer explicitly approves upload.

## Verification Labels

Use these labels consistently in frontmatter or a `## Verification` section:

- `unverified` — draft or unsourced claim; should not be presented as authoritative.
- `tutorial-derived` — extracted from a tutorial/video; source should be cited.
- `source-checked` — checked against official docs, engine source, Lyra, tranek, or another canonical source.
- `static-reviewed` — code/config reviewed without running Unreal Engine.
- `compile-tested` — compiled against a named UE version/target/toolchain.
- `editor-tested` — opened/exercised in the Unreal Editor.
- `playtested` — exercised in a runtime/PIE scenario with expected behavior observed.

Recommended metadata:

```yaml
verification:
  status: source-checked
  ue_version: "5.7"
  toolchain: ""
  checked_against:
    - "Epic docs URL or source path"
  last_checked: "YYYY-MM-DD"
```

## AI-Friendly Feature Shape

When adding examples, prefer complete feature shapes over isolated snippets:

- Purpose
- Files involved
- Lifecycle / initialization order
- Minimal implementation outline
- Failure modes
- Verification status
- Source/provenance
- Links to relevant MOCs and gotchas

This makes the vault easier for AI agents to retrieve and use without flattening confidence levels.

## Local PR Harness

Use the local harness to prepare reviewable PRs without uploading:

```bash
python3 tools/pr_harness.py draft --title "Add feature-shape template"
```

The harness writes `.pr_draft.md` with the branch, diffstat, changed files, suggested PR body, and verification output. Upload is intentionally opt-in and guarded.
