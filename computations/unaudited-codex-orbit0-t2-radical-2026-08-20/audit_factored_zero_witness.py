#!/usr/bin/env python3
"""Literal referee for the zero-incidence obstruction in the factored subideal."""

from __future__ import annotations

from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
RUST = HERE / "results_factored_p0_incidence.json"
SEED = HERE / "factored_p0_square_seed.txt"
OUT = HERE / "results_factored_zero_witness_audit.json"


CELLS = []
CELL_ID = {}
for u in range(8):
    for v in range(u + 1, 8):
        for a in range(3):
            for b in range(3):
                CELL_ID[u, v, a, b] = len(CELLS)
                CELLS.append((u, v, a, b))


def incident_columns(row: bytes):
    answer = set()
    for selected_positions in combinations(range(16), 4):
        mask = 0
        word = [None] * 8
        valid = True
        for position in selected_positions:
            cell = row[position]
            u, v, a, b = CELLS[cell]
            bits = (1 << u) | (1 << v)
            if mask & bits:
                valid = False
                break
            mask |= bits
            word[u] = a
            word[v] = b
        if not valid or mask != 255:
            continue
        if any(word[2 * pair] == word[2 * pair + 1] for pair in range(4)):
            continue
        multiplier = bytes(row[position] for position in range(16)
                           if position not in selected_positions)
        answer.add((tuple(word), multiplier))
    return answer


def main():
    rust = json.loads(RUST.read_text())
    witness = bytes.fromhex(rust["zero_incidence_witness"]["row"])
    coefficient = rust["zero_incidence_witness"]["target_coefficient"]
    seed_coefficients = {}
    for line in SEED.read_text().splitlines():
        fields = line.split()
        if fields and fields[0] == "TARGET":
            seed_coefficients[bytes.fromhex(fields[1])] = (int(fields[2]),
                                                            int(fields[3]))
    if seed_coefficients.get(witness) != (coefficient, 1) or coefficient == 0:
        raise RuntimeError("witness target coefficient did not replay")
    literal = incident_columns(witness)
    if literal:
        raise RuntimeError("zero-incidence witness has a literal factored column")

    # Must-fire control: splice one term of an alternating binary word into a
    # twelve-cell multiplier. The exact same enumerator must recover it.
    word = (1, 2, 1, 2, 1, 2, 1, 2)
    term = bytes(sorted(CELL_ID[2 * pair, 2 * pair + 1,
                                word[2 * pair], word[2 * pair + 1]]
                        for pair in range(4)))
    mutated = bytes(sorted(witness[:12] + term))
    mutation_incidence = incident_columns(mutated)
    if not mutation_incidence:
        raise RuntimeError("alternating-word source mutation failed to fire")

    result = {
        "status": "exact literal audit of factored-subideal coordinate obstruction",
        "rust_result_sha256": sha256(RUST.read_bytes()).hexdigest(),
        "seed_sha256": sha256(SEED.read_bytes()).hexdigest(),
        "witness_row": witness.hex(),
        "witness_target_coefficient": coefficient,
        "literal_four_cell_subsets_checked": 1820,
        "literal_incident_columns": len(literal),
        "source_scope": (
            "H_w times a degree-12 nonanchor multiplier, with w opposite on "
            "each of 01,23,45,67; equivalently word minimum K-degree four"
        ),
        "restricted_nonmembership": True,
        "global_scope_guard": (
            "This coordinate dual annihilates the m0^2-factored subideal J "
            "only. It does not annihilate the complete degree24/K16 source "
            "image, whose columns may leave the common-factor subspace."
        ),
        "mutation_row": mutated.hex(),
        "mutation_incident_columns": len(mutation_incidence),
        "mutation_fires": True,
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("factored zero-incidence witness: PASS")
    print("row/coefficient:", witness.hex(), coefficient)
    print("mutation incidence:", len(mutation_incidence))
    print("logical sha256:", result["logical_sha256"])


if __name__ == "__main__":
    main()
