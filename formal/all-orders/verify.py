#!/usr/bin/env python3
"""Build the integrated modules and audit their Lean kernel dependencies."""

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tomllib

ROOT = Path(__file__).resolve().parent
ALLOWED = {"propext", "Classical.choice", "Quot.sound"}


def without_comments(source: str) -> str:
    """Remove Lean's line comments and nested block comments before scanning."""
    result = []
    depth = 0
    i = 0
    while i < len(source):
        if source.startswith("/-", i):
            depth += 1
            i += 2
        elif depth and source.startswith("-/", i):
            depth -= 1
            i += 2
        elif depth:
            if source[i] == "\n":
                result.append("\n")
            i += 1
        elif source.startswith("--", i):
            i = source.find("\n", i)
            if i < 0:
                break
        else:
            result.append(source[i])
            i += 1
    return "".join(result)


def run(*args: str) -> str:
    result = subprocess.run(args, cwd=ROOT, text=True, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    if result.returncode:
        print(result.stdout, end="")
        raise RuntimeError(f"Command failed ({result.returncode}): {' '.join(args)}")
    return result.stdout


def audit(output: str, source: str) -> list[str]:
    expected = re.findall(r"^#print axioms (\S+)$", source, re.MULTILINE)
    if not expected or len(set(expected)) != len(expected):
        raise RuntimeError("Axiom audit must name distinct declarations")
    for name in expected:
        match = re.search(r"'" + re.escape(name) +
                          r"' depends on axioms:\s*\[([^\]]*)\]", output)
        if match:
            axioms = {a.strip() for a in match[1].split(",") if a.strip()}
            if unexpected := axioms - ALLOWED:
                raise RuntimeError(f"Unexpected axioms for {name}: {sorted(unexpected)}")
        elif f"'{name}' does not depend on any axioms" not in output:
            raise RuntimeError(f"Missing axiom report for {name}")
    return expected


def main() -> None:
    config = tomllib.loads((ROOT / "lakefile.toml").read_text())
    modules = config["defaultTargets"]
    sources = [f"{name}.lean" for name in modules] + ["CheckAxioms.lean"]
    for name in sources:
        source = without_comments((ROOT / name).read_text())
        if re.search(r"\bsorry\b|\badmit\b|^\s*(?:axiom|unsafe)\b", source, re.MULTILINE):
            raise RuntimeError(f"Unaccepted proof construct in {name}")
    print(run("lake", "--wfail", "build"), end="")
    output = run("lake", "env", "lean", "-DwarningAsError=true", "CheckAxioms.lean")
    declarations = audit(output, (ROOT / "CheckAxioms.lean").read_text())
    (ROOT / "axioms.txt").write_text(output)
    metadata = {
        "status": "PASS",
        "toolchain": run("lake", "env", "lean", "--version").strip(),
        "mathlib_tag": "v4.33.1",
        "mathlib_revision": "0df444a360eaa60ab8c11dca51a86af692955474",
        "build_command": "lake --wfail build",
        "build_exit_code": 0,
        "axiom_command": "lake env lean -DwarningAsError=true CheckAxioms.lean",
        "axiom_exit_code": 0,
        "declarations_checked": len(declarations),
        "checked_declarations": declarations,
        "allowed_axioms": sorted(ALLOWED),
        "integrated_modules": modules,
        "source_hashes": {
            name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
            for name in sources + ["lakefile.toml", "lake-manifest.json", "lean-toolchain"]
        },
        "scope": (
            "Physical quotient/divided-power bridge, O(2) invariant-ring theorem, "
            "finite Wick covariance, conditional endpoint and response algebra, "
            "complete graph obstruction and conditional weighted contradiction. "
            "The full conjecture and physical-source-to-endpoint identities are not formalized."
        ),
    }
    (ROOT / "verification.json").write_text(json.dumps(metadata, indent=2) + "\n")
    print(f"PASS: {len(modules)} integrated modules; {len(declarations)} declarations axiom-checked.")


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, OSError) as error:
        (ROOT / "verification.json").write_text(json.dumps({
            "status": "FAIL", "error": str(error)
        }, indent=2) + "\n")
        print(error, file=sys.stderr)
        sys.exit(1)
