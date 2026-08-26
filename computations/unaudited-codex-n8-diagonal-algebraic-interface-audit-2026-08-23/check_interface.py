#!/usr/bin/env python3
"""Read-only audit of the certified N8-DIAGONAL algebraic interface.

This deliberately does not solve an ideal.  It checks what proof objects are
actually frozen, measures the 87 orbit CNF/DRAT packet, and guards against
confusing the nearby N=6 degree-18 diagonal-quotient calculation with N=8.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CERT = ROOT / "computations/certificates/n8_diagonal"
ORBITS = CERT / "orbits"


def require(condition: bool, detail: str) -> None:
    if not condition:
        raise RuntimeError(detail)


def cnf_header(path: Path) -> tuple[int, int]:
    with path.open(encoding="ascii") as stream:
        for line in stream:
            if line.startswith("p cnf "):
                _, _, variables, clauses = line.split()
                return int(variables), int(clauses)
    raise RuntimeError(f"missing CNF header: {path}")


def nonempty_lines(path: Path) -> int:
    with path.open("rb") as stream:
        return sum(bool(line.strip()) for line in stream)


def main() -> None:
    cnfs = sorted(ORBITS.glob("n8k4_*.cnf"))
    drats = sorted(ORBITS.glob("n8k4_*.drat"))
    require(len(cnfs) == 87, f"expected 87 orbit CNFs, got {len(cnfs)}")
    require(len(drats) == 87, f"expected 87 orbit DRATs, got {len(drats)}")

    cnf_indices = {p.stem.removeprefix("n8k4_") for p in cnfs}
    drat_indices = {p.stem.removeprefix("n8k4_") for p in drats}
    require(cnf_indices == drat_indices == {str(i) for i in range(87)},
            "orbit certificate indices do not match 0..86")

    headers = [cnf_header(path) for path in cnfs]
    proof_lines = [nonempty_lines(path) for path in drats]
    proof_bytes = [path.stat().st_size for path in drats]

    all_files = [path for path in CERT.rglob("*") if path.is_file()]
    suffixes: dict[str, int] = {}
    for path in all_files:
        suffixes[path.suffix or "<none>"] = suffixes.get(path.suffix or "<none>", 0) + 1

    # The frozen package is propositional/replay material.  These filename
    # guards are not a proof of nonexistence by themselves; the REPORT couples
    # them to a source audit of the encoder and certified proof document.
    algebraic_suffixes = {".sing", ".syz", ".gb", ".mpl", ".mtx"}
    require(not algebraic_suffixes.intersection(suffixes),
            f"unexpected algebraic payload suffix: {algebraic_suffixes.intersection(suffixes)}")
    suspicious = [
        str(path.relative_to(CERT))
        for path in all_files
        if any(token in path.name.lower()
               for token in ("multiplier", "nullstell", "syzygy", "macaulay"))
    ]
    require(not suspicious, f"possible multiplier payload needs manual audit: {suspicious}")

    encoder = (ROOT / "computations/verify_eight_site_diagonal_obstruction.py").read_text()
    require('`p(c, S)` is the Boolean' in encoder,
            "certified encoder no longer documents p(c,S) as Boolean")
    require('"haf(t^c | S) != 0"' in encoder,
            "certified encoder polarity changed")

    proof = (ROOT / "proofs/eight-site-diagonal-obstruction.md").read_text()
    require("The `N = 8` Groebner corroboration does not exist." in proof.replace("Gröbner", "Groebner"),
            "certified proof no longer records the absent N=8 algebraic corroboration")
    require("timed out" in proof[proof.find("The `N = 8` Gröbner corroboration"):],
            "certified proof no longer records the N=8 timeout")

    n6 = (ROOT / "computations/test_diagonal_power2.py").read_text()
    require("diagonal n=6,q=3" in n6,
            "nearby degree-18 calculation is no longer explicitly N=6")
    require("degree-18" in n6, "nearby N=6 degree marker missing")

    result = {
        "verdict": "NO_FROZEN_N8_SOURCE_MULTIPLIERS",
        "proof_system": "Boolean CNF plus DRAT on hafnian nonvanishing atoms",
        "orbit_packet": {
            "cnfs": len(cnfs),
            "drats": len(drats),
            "variables_per_cnf": sorted({v for v, _ in headers}),
            "clauses": {
                "min": min(c for _, c in headers),
                "max": max(c for _, c in headers),
                "total": sum(c for _, c in headers),
            },
            "drat_nonempty_lines": {
                "min": min(proof_lines),
                "max": max(proof_lines),
                "total": sum(proof_lines),
            },
            "drat_bytes": {
                "min": min(proof_bytes),
                "max": max(proof_bytes),
                "total": sum(proof_bytes),
            },
        },
        "certificate_tree_suffix_counts": dict(sorted(suffixes.items())),
        "n8_source_multiplier_degree": None,
        "n8_source_multiplier_support": None,
        "nearby_degree18_scope": "N=6 diagonal quotient only",
        "cheap_export": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
