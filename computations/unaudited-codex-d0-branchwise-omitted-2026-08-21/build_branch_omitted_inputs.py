#!/usr/bin/env python3
"""Splice exact omitted literal rows into frozen D0 branch inputs.

The input branch ideals and primes are reused verbatim.  The omitted row is
inserted immediately before the final native-F4SAT saturator; no polynomial
is truncated, reduced, or divided by an unproved factor.
"""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
BASE = HERE.parent / "unaudited-codex-d0-c0-eliminant-audit-2026-08-21"
ROWS = HERE / "d0_omitted_rows.json"
PRIMES = (1073741827, 536870909)


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def main() -> None:
    data = json.loads(ROWS.read_text())
    assert data["variables"] == ["b0", "d1", "d4"]
    manifest = {"source_rows_sha256": digest(ROWS), "inputs": []}
    for branch in (0, 1):
        for prime in PRIMES:
            source = BASE / f"d0_factor{branch}_p{prime}_resat.ms"
            lines = source.read_text().splitlines()
            assert lines[0] == "b0,d1,d4"
            assert int(lines[1]) == prime
            assert not lines[-1].rstrip().endswith(",")
            for row in data["rows"]:
                label = row["source_label"]
                target = HERE / f"d0_factor{branch}_{label}_p{prime}.ms"
                polynomial = row["polynomial"]
                # SymPy's exporter already uses msolve ^ notation.  Reject
                # the two parser hazards before creating any computation.
                assert "**" not in polynomial and "(" not in polynomial
                output = lines[:-1] + [polynomial + ",", lines[-1]]
                target.write_text("\n".join(output) + "\n")
                manifest["inputs"].append({
                    "branch": branch,
                    "prime": prime,
                    "source_label": label,
                    "base": source.name,
                    "base_sha256": digest(source),
                    "path": target.name,
                    "sha256": digest(target),
                    "row_count": len(output) - 2,
                    "omitted_row_index": len(output) - 4,
                    "saturator_index": len(output) - 3,
                })
    logical = json.dumps(manifest, sort_keys=True, separators=(",", ":"))
    manifest["logical_sha256"] = sha256(logical.encode()).hexdigest()
    path = HERE / "results_d0_branch_omitted_inputs.json"
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print("built", len(manifest["inputs"]), "inputs")
    print("logical sha256", manifest["logical_sha256"])


if __name__ == "__main__":
    main()
