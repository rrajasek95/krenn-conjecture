#!/usr/bin/env python3
"""Replay the published rate and design packages against their saved receipts."""

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PACKAGES = (
    "useful-consequences-2026-09-26",
    "universal-rate-gate-2026-09-26",
    "rate-boundary-gate-2026-09-26",
    "complex-rate-bound-2026-09-26",
    "quantitative-proof-identities-2026-09-26",
    "general-complex-rate-2026-09-26",
    "rate-sharpness-followup-2026-09-26",
    "rate-design-frontier-2026-09-26",
    "method-utility-2026-09-26",
    "boundary-structure-2026-09-26",
    "higher-order-2026-09-26",
    "critical-cone-2026-09-26",
    "critical-extension-search-2026-09-26",
    "w-state-two-root-2026-09-26",
    "w-state-local-optimum-2026-09-26",
    "site-balancing-2026-09-26",
    "balanced-frontier-2026-09-27",
    "full-support-jets-2026-09-27",
    "w-ground-cancellation-2026-09-27",
    "flat-core-rigidity-2026-09-27",
    "flat-support-structure-2026-09-27",
    "w-all-even-local-optimum-2026-09-27",
    "four-arm-ghz-boundary-2026-09-27",
    "four-core-attachments-2026-09-27",
    "w-universal-factor-two-2026-09-27",
    "w-cofactor-rigidity-2026-09-27",
    "triangle-ghz-onset-2026-09-27",
    "three-arm-ghz-onset-2026-09-27",
    "two-arm-ghz-onset-2026-09-27",
    "w-balanced-cancellation-2026-09-27",
    "w-equal-split-legendre-2026-09-27",
    "w-two-group-reduction-2026-09-27",
    "transverse-two-arm-ghz-2026-09-27",
    "coherent-two-arm-ghz-2026-09-27",
    "single-invertible-edge-ghz-2026-09-27",
    "binary-adjugate-ghz-2026-09-27",
    "balanced-response-ghz-2026-09-27",
    "cofactor-graph-frontier-2026-09-27",
    "full-support-ghz-onset-2026-09-27",
    "ghz-star-fidelity-gap-2026-09-27",
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check_path_hashes(value, package, checked):
    """Check path-keyed hashes; mathematical fingerprints stay with each verifier."""
    if isinstance(value, dict):
        for key, item in value.items():
            if isinstance(item, str) and re.fullmatch(r"[0-9a-f]{64}", item):
                if key.startswith(("computations/", "notes/", "proofs/", "certification/")):
                    path = ROOT / key
                elif key == "verify.py":
                    path = package / key
                elif key == "quantitative-proof-identities-2026-09-26.md":
                    path = ROOT / "notes" / key
                else:
                    path = None
                if path is not None:
                    require(path.is_file(), f"Missing hash dependency: {path}")
                    require(hashlib.sha256(path.read_bytes()).hexdigest() == item,
                            f"Hash mismatch: {path.relative_to(ROOT)}")
                    checked.add(str(path.relative_to(ROOT)))
            check_path_hashes(item, package, checked)
    elif isinstance(value, list):
        for item in value:
            check_path_hashes(item, package, checked)


def main():
    checked = set()
    for name in PACKAGES:
        package = ROOT / "computations" / name
        receipts = [package / file for file in ("results.json", "verification.json")
                    if (package / file).is_file()]
        require(len(receipts) == 1, f"Expected one saved receipt in {package}")
        expected = json.loads(receipts[0].read_text())
        check_path_hashes(expected, package, checked)
        dependency_file = package / "dependencies.json"
        if dependency_file.exists():
            check_path_hashes(json.loads(dependency_file.read_text()), package, checked)
        for options in ([], ["-O"]):
            command = [sys.executable, "-B", *options, str(package / "verify.py")]
            result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
            require(result.returncode == 0,
                    f"{name} {' '.join(options)} failed:\n{result.stderr}\n{result.stdout}")
            actual = json.loads(result.stdout)
            require(actual == expected,
                    f"{name} {' '.join(options)} differs from {receipts[0].name}")
        print(f"PASS: {name} (normal and -O; saved receipt matched)", flush=True)
    print(f"PASS: {len(PACKAGES)} packages; {2 * len(PACKAGES)} replays; "
          f"{len(checked)} distinct file hashes checked.")
    print("Evidence: written research and exact supporting checks; independent audit pending.")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, json.JSONDecodeError) as error:
        sys.exit(f"FAIL: {error}")
