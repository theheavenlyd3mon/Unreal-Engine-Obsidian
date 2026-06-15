#!/usr/bin/env python3
"""Lint this Obsidian vault for link and metadata drift.

Standard-library only. Intended checks:
- required root index exists
- broken or ambiguous Obsidian wikilinks
- duplicate note stems/titles that make wikilinks ambiguous
- warning-only metadata/MOC hygiene checks
"""

from __future__ import annotations

import argparse
import os
import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

WIKILINK_RE = re.compile(r"(?<!!)\[\[([^\[\]\n]+)\]\]")
MD_LINK_RE = re.compile(r"(?<!!)\[[^\]\n]+\]\(([^)]+)\)")
HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*$")
TITLE_RE = re.compile(r"^title:\s*[\"']?(.+?)[\"']?\s*$", re.MULTILINE)

SKIP_DIRS = {
    ".git",
    ".obsidian",
    ".archive",
    "__pycache__",
}
META_NAMES = {
    "README.md",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
}
ROOT_REQUIRED = "_MOC_ROOT.md"


@dataclass(frozen=True)
class Note:
    path: Path
    rel: str
    stem: str
    title: str | None
    headings: frozenset[str]
    has_frontmatter: bool
    is_moc: bool
    is_meta: bool


@dataclass(frozen=True)
class Finding:
    severity: str
    path: str
    message: str

    def key(self) -> str:
        return f"{self.severity}\t{self.path}\t{self.message}"


def iter_markdown(root: Path) -> Iterable[Path]:
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for filename in filenames:
            if filename.endswith(".md"):
                yield Path(dirpath) / filename


def slug_heading(text: str) -> str:
    """Approximate Obsidian/GitHub heading slug matching for existence checks."""
    text = text.strip().lower()
    text = re.sub(r"[`*_~]", "", text)
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"\s+", "-", text)
    return text.strip("-")


def parse_frontmatter(text: str) -> tuple[bool, str | None]:
    if not text.startswith("---\n"):
        return False, None
    end = text.find("\n---", 4)
    if end == -1:
        return False, None
    block = text[4:end]
    match = TITLE_RE.search(block)
    return True, match.group(1).strip() if match else None


def parse_note(root: Path, path: Path) -> Note:
    text = path.read_text(encoding="utf-8", errors="replace")
    has_frontmatter, title = parse_frontmatter(text)
    headings = frozenset(slug_heading(m.group(1)) for m in HEADING_RE.finditer(text))
    rel = path.relative_to(root).as_posix()
    name = path.name
    is_moc = name.startswith("_MOC") or path.stem.startswith("_MOC")
    is_meta = name in META_NAMES or name.startswith("_REVIEW")
    return Note(
        path=path,
        rel=rel,
        stem=path.stem,
        title=title,
        headings=headings,
        has_frontmatter=has_frontmatter,
        is_moc=is_moc,
        is_meta=is_meta,
    )


def normalize_target(raw: str) -> tuple[str, str | None]:
    target = raw.split("|", 1)[0].strip()
    target = target.split("^", 1)[0].strip()  # block refs: validate page only
    heading = None
    if "#" in target:
        target, heading = target.split("#", 1)
        heading = heading.strip() or None
    target = target.strip()
    if target.endswith(".md"):
        target = target[:-3]
    return target, heading


def build_indexes(notes: list[Note]) -> tuple[dict[str, list[Note]], dict[str, list[Note]]]:
    by_stem: dict[str, list[Note]] = defaultdict(list)
    by_title: dict[str, list[Note]] = defaultdict(list)
    for note in notes:
        by_stem[note.stem].append(note)
        by_stem[note.stem.lower()].append(note)
        if note.title:
            by_title[note.title].append(note)
            by_title[note.title.lower()].append(note)
    return by_stem, by_title


def resolve_wikilink(target: str, by_stem: dict[str, list[Note]], by_title: dict[str, list[Note]]) -> list[Note]:
    matches: list[Note] = []
    candidates = [target, target.lower()]
    if "/" in target:
        # Obsidian allows path-ish links. Resolve by path stem without extension.
        path_stem = target.rstrip("/").split("/")[-1]
        candidates.extend([path_stem, path_stem.lower()])
    for key in candidates:
        matches.extend(by_stem.get(key, []))
        matches.extend(by_title.get(key, []))
    # de-dupe while preserving order
    seen: set[str] = set()
    out: list[Note] = []
    for note in matches:
        if note.rel not in seen:
            out.append(note)
            seen.add(note.rel)
    return out


def lint(root: Path) -> list[Finding]:
    notes = [parse_note(root, path) for path in sorted(iter_markdown(root))]
    by_stem, by_title = build_indexes(notes)
    findings: list[Finding] = []

    if not (root / ROOT_REQUIRED).exists():
        findings.append(Finding("ERROR", ROOT_REQUIRED, "required root MOC is missing"))

    # Duplicate stems/titles are warnings unless a link actually becomes ambiguous.
    for stem, matches in sorted(by_stem.items()):
        if stem.lower() != stem:
            continue
        unique = {n.rel for n in matches}
        if len(unique) > 1:
            findings.append(
                Finding("WARN", "<vault>", f"duplicate note stem '{stem}': " + ", ".join(sorted(unique)))
            )
    for title, matches in sorted(by_title.items()):
        if title.lower() != title:
            continue
        unique = {n.rel for n in matches}
        if len(unique) > 1:
            findings.append(
                Finding("WARN", "<vault>", f"duplicate frontmatter title '{title}': " + ", ".join(sorted(unique)))
            )

    for note in notes:
        text = note.path.read_text(encoding="utf-8", errors="replace")
        if not note.has_frontmatter and not note.is_meta:
            findings.append(Finding("WARN", note.rel, "missing YAML frontmatter"))

        for match in WIKILINK_RE.finditer(text):
            raw = match.group(1)
            target, heading = normalize_target(raw)
            if not target:
                continue
            matches = resolve_wikilink(target, by_stem, by_title)
            if not matches:
                findings.append(Finding("ERROR", note.rel, f"broken wikilink [[{raw}]]"))
                continue
            if len(matches) > 1:
                findings.append(
                    Finding(
                        "ERROR",
                        note.rel,
                        f"ambiguous wikilink [[{raw}]] -> " + ", ".join(n.rel for n in matches),
                    )
                )
                continue
            if heading:
                wanted = slug_heading(heading)
                if wanted and wanted not in matches[0].headings:
                    findings.append(
                        Finding("WARN", note.rel, f"wikilink heading not found [[{raw}]] -> {matches[0].rel}")
                    )

        for match in MD_LINK_RE.finditer(text):
            href = match.group(1).strip()
            if not href or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", href) or href.startswith("#"):
                continue
            path_part = href.split("#", 1)[0].replace("%20", " ")
            if not path_part:
                continue
            target_path = (note.path.parent / path_part).resolve()
            try:
                target_path.relative_to(root.resolve())
            except ValueError:
                continue
            if not target_path.exists():
                findings.append(Finding("WARN", note.rel, f"local Markdown link target not found: {href}"))

    # Warn about content files not reachable from any MOC. Warning-only because some notes are intentionally standalone.
    linked_from_mocs: set[str] = set()
    moc_notes = [n for n in notes if n.is_moc]
    for moc in moc_notes:
        text = moc.path.read_text(encoding="utf-8", errors="replace")
        for match in WIKILINK_RE.finditer(text):
            target, _ = normalize_target(match.group(1))
            for resolved in resolve_wikilink(target, by_stem, by_title):
                linked_from_mocs.add(resolved.rel)
    for note in notes:
        if note.is_moc or note.is_meta:
            continue
        if note.rel not in linked_from_mocs:
            findings.append(Finding("WARN", note.rel, "not linked from any _MOC_ file"))

    return findings


def load_baseline(path: Path | None) -> set[str]:
    if not path or not path.exists():
        return set()
    return {
        line.rstrip("\n")
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }


def write_baseline(path: Path, findings: list[Finding]) -> None:
    keys = sorted(f.key() for f in findings)
    path.write_text(
        "# vault_lint baseline. Existing findings listed here do not fail CI; new ERRORs still do.\n"
        + "\n".join(keys)
        + ("\n" if keys else ""),
        encoding="utf-8",
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Lint an Obsidian Markdown vault.")
    parser.add_argument("root", nargs="?", default=".", help="vault root directory")
    parser.add_argument(
        "--baseline",
        default=".vault_lint_baseline",
        help="baseline file for existing findings (default: .vault_lint_baseline)",
    )
    parser.add_argument(
        "--update-baseline",
        action="store_true",
        help="write the current findings to the baseline file and exit",
    )
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    findings = lint(root)
    baseline_path = (root / args.baseline).resolve() if args.baseline else None

    if args.update_baseline:
        if not baseline_path:
            raise SystemExit("--update-baseline requires --baseline")
        write_baseline(baseline_path, findings)
        print(f"Wrote baseline: {baseline_path.relative_to(root)} ({len(findings)} finding(s))")
        return 0

    baseline = load_baseline(baseline_path)
    active_findings = [f for f in findings if f.key() not in baseline]
    suppressed = len(findings) - len(active_findings)
    errors = [f for f in active_findings if f.severity == "ERROR"]
    warnings = [f for f in active_findings if f.severity == "WARN"]

    for finding in active_findings:
        print(f"{finding.severity}: {finding.path}: {finding.message}")

    if suppressed:
        print(f"\nSuppressed {suppressed} baseline finding(s).")
    print(f"Vault lint: {len(errors)} new error(s), {len(warnings)} new warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
