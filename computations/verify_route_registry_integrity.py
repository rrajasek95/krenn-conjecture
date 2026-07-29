#!/usr/bin/env python3
"""Mechanical integrity audit for notes/route-registry.md."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "notes" / "route-registry.md"


def local_markdown_targets(text: str) -> list[Path]:
    targets: list[Path] = []
    for raw in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
        target = raw.split("#", 1)[0]
        if not target or "://" in target or target.startswith("mailto:"):
            continue
        targets.append((REGISTRY.parent / target).resolve())
    return targets


def backticked_artifact_targets(text: str) -> list[Path]:
    targets: list[Path] = []
    for raw in re.findall(r"`([^`]+)`", text):
        if raw.startswith(("notes/", "proofs/", "computations/")):
            targets.append((ROOT / raw).resolve())
    return targets


def top_route_ids(lines: list[str]) -> list[str]:
    ids: list[str] = []
    in_table = False
    for line in lines:
        if line.startswith("| Route |"):
            in_table = True
            continue
        if not in_table:
            continue
        if not line.startswith("|"):
            break
        fields = [field.strip() for field in line.strip().strip("|").split("|")]
        if fields and fields[0] and set(fields[0]) != {"-"}:
            ids.append(fields[0])
    return ids


def main() -> None:
    text = REGISTRY.read_text()
    lines = text.splitlines()
    markdown_targets = local_markdown_targets(text)
    artifact_targets = backticked_artifact_targets(text)
    missing = sorted(
        {path for path in markdown_targets + artifact_targets if not path.exists()}
    )
    assert not missing, "missing registry targets:\n" + "\n".join(map(str, missing))

    route_ids = top_route_ids(lines)
    duplicates = sorted(key for key, count in Counter(route_ids).items() if count > 1)
    assert not duplicates, f"duplicate top-level route identifiers: {duplicates}"

    print("route registry integrity: PASS")
    print(f"top-level route identifiers: {len(route_ids)} (all unique)")
    print(f"Markdown links checked: {len(markdown_targets)}")
    print(f"backticked artifact paths checked: {len(artifact_targets)}")


if __name__ == "__main__":
    main()
