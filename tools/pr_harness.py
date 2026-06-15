#!/usr/bin/env python3
"""Local PR harness for this Obsidian vault.

Default behavior is local-only: inspect, validate, and draft. It never pushes or
opens a PR unless the publish subcommand is called with explicit review approval.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import subprocess
import sys
from pathlib import Path

VALID_VERIFICATION = {
    "unverified",
    "tutorial-derived",
    "source-checked",
    "static-reviewed",
    "compile-tested",
    "editor-tested",
    "playtested",
}

REPO_ROOT = Path(__file__).resolve().parents[1]
DRAFT_PATH = REPO_ROOT / ".pr_draft.md"


def run(cmd: list[str], check: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=REPO_ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=check)


def git_output(*args: str) -> str:
    return run(["git", *args], check=True).stdout.strip()


def changed_files(base: str | None = None) -> list[str]:
    if base:
        proc = run(["git", "rev-parse", "--verify", base])
        if proc.returncode == 0:
            out = git_output("diff", "--name-only", f"{base}...HEAD")
            return sorted(line for line in out.splitlines() if line)
    out = git_output("diff", "--name-only", "HEAD")
    staged = git_output("diff", "--cached", "--name-only")
    files = sorted({line for line in (out + "\n" + staged).splitlines() if line})
    return files


def origin_owner() -> str | None:
    url = git_output("remote", "get-url", "origin")
    match = re.search(r"github\.com[:/]([^/]+)/", url)
    return match.group(1) if match else None


def validate_verification_labels(files: list[str]) -> list[str]:
    problems: list[str] = []
    label_re = re.compile(r"status:\s*([^\n#]+)")
    for rel in files:
        path = REPO_ROOT / rel
        if not path.exists() or path.suffix != ".md":
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if "verification:" not in text:
            # Templates and top-level meta docs can be unlabelled.
            if rel.startswith("templates/") or Path(rel).name in {"README.md", "CHANGELOG.md", "AGENTS.md"}:
                continue
            problems.append(f"WARN {rel}: no verification block")
            continue
        match = label_re.search(text)
        if not match:
            problems.append(f"WARN {rel}: verification block has no status")
            continue
        status = match.group(1).strip().strip('"\'')
        if status not in VALID_VERIFICATION:
            problems.append(f"ERROR {rel}: invalid verification status '{status}'")
    return problems


def check() -> int:
    exit_code = 0
    outputs: list[str] = []

    lint = REPO_ROOT / "tools" / "vault_lint.py"
    if lint.exists():
        proc = run([sys.executable, str(lint), "."])
        outputs.append("$ python3 tools/vault_lint.py .\n" + proc.stdout.rstrip())
        if proc.returncode != 0:
            exit_code = proc.returncode
    else:
        outputs.append("SKIP vault_lint.py not found")

    files = changed_files("upstream/main") or changed_files("main")
    label_findings = validate_verification_labels(files)
    if label_findings:
        outputs.append("$ verification label check\n" + "\n".join(label_findings))
        if any(line.startswith("ERROR") for line in label_findings):
            exit_code = 1
    else:
        outputs.append("$ verification label check\nOK")

    for block in outputs:
        print(block)
        print()
    return exit_code


def draft(title: str, base: str) -> int:
    branch = git_output("branch", "--show-current")
    status = git_output("status", "--short") or "clean"
    files = changed_files("upstream/main") or changed_files("main")
    diffstat = git_output("diff", "--stat", base + "...HEAD") if run(["git", "rev-parse", "--verify", base], False).returncode == 0 else git_output("diff", "--stat")

    check_proc = run([sys.executable, str(Path(__file__).resolve()), "check"])
    body = f"""# PR Draft — {title}

Generated: {dt.datetime.now().isoformat(timespec='seconds')}

## Upload guard

Do not push or open this PR until the human reviewer approves.

## Branch

`{branch}`

## Suggested title

{title}

## Summary

- 

## Why

- 

## Changed files

{chr(10).join(f'- `{f}`' for f in files) if files else '- No uncommitted changed files detected.'}

## Diffstat

```text
{diffstat or 'No committed diffstat against base; review local diff.'}
```

## Local status

```text
{status}
```

## Verification

```text
{check_proc.stdout.rstrip()}
```

## Risks / limits

- No Unreal Engine build verification unless explicitly stated above.
- Existing findings may be suppressed by `.vault_lint_baseline`; new errors should not be introduced.

## Publish commands after review only

```bash
# after human approval only
python3 tools/pr_harness.py publish --title {title!r} --base {base} --i-reviewed-this
```
"""
    DRAFT_PATH.write_text(body, encoding="utf-8")
    print(f"Wrote {DRAFT_PATH.relative_to(REPO_ROOT)}")
    return check_proc.returncode


def publish(title: str, base: str, reviewed: bool, repo: str | None = None) -> int:
    if not reviewed:
        print("Refusing to upload: pass --i-reviewed-this after human review.", file=sys.stderr)
        return 2
    branch = git_output("branch", "--show-current")
    if not DRAFT_PATH.exists():
        print("Refusing to upload: .pr_draft.md is missing. Run draft first.", file=sys.stderr)
        return 2
    check_code = check()
    if check_code != 0:
        print("Refusing to upload: local checks failed.", file=sys.stderr)
        return check_code
    print("Uploading branch and opening PR...")
    run(["git", "push", "-u", "origin", branch], check=True)
    head_owner = origin_owner()
    head = f"{head_owner}:{branch}" if head_owner else branch
    cmd = [
        "gh", "pr", "create",
        "--base", base,
        "--head", head,
        "--title", title,
        "--body-file", str(DRAFT_PATH),
    ]
    if repo:
        cmd[3:3] = ["--repo", repo]
    run(cmd, check=True)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Prepare local PR drafts for the UE5 Obsidian vault.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("check", help="run local vault and metadata checks")

    draft_p = sub.add_parser("draft", help="write .pr_draft.md without uploading")
    draft_p.add_argument("--title", required=True)
    draft_p.add_argument("--base", default="main")

    pub_p = sub.add_parser("publish", help="push/open PR after explicit human approval")
    pub_p.add_argument("--title", required=True)
    pub_p.add_argument("--base", default="main")
    pub_p.add_argument("--i-reviewed-this", action="store_true")
    pub_p.add_argument("--repo", help="target GitHub repo, e.g. owner/name")

    args = parser.parse_args(argv)
    if args.cmd == "check":
        return check()
    if args.cmd == "draft":
        return draft(args.title, args.base)
    if args.cmd == "publish":
        return publish(args.title, args.base, args.i_reviewed_this, args.repo)
    raise AssertionError(args.cmd)


if __name__ == "__main__":
    raise SystemExit(main())
