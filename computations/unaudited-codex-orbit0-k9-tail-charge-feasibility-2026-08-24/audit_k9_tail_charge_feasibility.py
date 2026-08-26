#!/usr/bin/env python3
"""Exact bounded charge audit for the omitted degrees >=9 sparse-R8 tail.

This deliberately does not canonicalize or retain row orbits.  The cycle
functional is H-invariant, so it can be paired with each literal matching
output before quotient collection.  The resulting scalar is exactly the
pairing with the quotient/orbit-mass ledger.
"""

from __future__ import annotations

import hashlib
import json
import argparse
from collections import Counter
from itertools import combinations
from pathlib import Path
from time import perf_counter


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "computations/unaudited-codex-orbit0-t2-radical-2026-08-20"
DUAL_BASE = ROOT / "computations/unaudited-codex-orbit0-k16-weighted-dafsa-2026-08-23"
SEED = BASE / "sparse_r8_k9_tail_terms.txt"
TAIL = BASE / "results_sparse_r8_k9_tail.json"
SEED_META = BASE / "results_anchor_times_e9_cutoff10_seed.json"
DUAL = DUAL_BASE / "k16_cycle_partition_dual.tsv"
DEFAULT_OUT = Path(__file__).with_name("results_k9_tail_charge_feasibility.json")

PINS = {
    SEED: "b572b774d3d50d2618aa2d79338681fcf80542bf19ddd6e319037f9432aab74b",
    TAIL: "6b85cca58d6da26f426404eb785b2d9bf7858a4c758a651e1e9aa66729b08132",
    SEED_META: "8106f094ba796f124f80213d019420a9df469a8ced8e72b4d37a493b6da23ba9",
    DUAL: "fea91d03250128fa6ea99252659ddd2b46329a9318916a19d6dae0ecfb69dd84",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def perfect_matchings(vertices: tuple[int, ...] = tuple(range(8))):
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for i in range(1, len(vertices)):
        v = vertices[i]
        rest = vertices[1:i] + vertices[i + 1 :]
        for tail in perfect_matchings(rest):
            yield ((u, v),) + tail


EDGES = tuple(combinations(range(8), 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
MATCHINGS = tuple(perfect_matchings())
require(len(MATCHINGS) == 105, "perfect-matching count changed")


def cell_id(u: int, v: int, a: int, b: int) -> int:
    if u > v:
        u, v, a, b = v, u, b, a
    return 9 * EDGE_INDEX[(u, v)] + 3 * a + b


CELL_PORTS = []
for u, v in EDGES:
    for a in range(3):
        for b in range(3):
            CELL_PORTS.append((3 * u + a, 3 * v + b))
require(len(CELL_PORTS) == 252, "cell universe changed")


def matching_cells(word: tuple[int, ...], matching) -> tuple[int, ...]:
    return tuple(cell_id(u, v, word[u], word[v]) for u, v in matching)


def cycle_partition(cells: tuple[int, ...]) -> tuple[int, ...]:
    adjacency = [[] for _ in range(24)]
    for cell in cells:
        u, v = CELL_PORTS[cell]
        adjacency[u].append(v)
        adjacency[v].append(u)
    require(all(len(neighbours) == 2 for neighbours in adjacency), "non-2-regular literal row")
    seen = set()
    parts = []
    for start in range(24):
        if start in seen:
            continue
        stack = [start]
        size = 0
        while stack:
            u = stack.pop()
            if u in seen:
                continue
            seen.add(u)
            size += 1
            stack.extend(adjacency[u])
        parts.append(size)
    return tuple(sorted(parts))


def parse_inputs():
    for path, expected in PINS.items():
        require(sha256(path) == expected, f"input SHA changed: {path}")

    dual = {}
    lines = DUAL.read_text().splitlines()
    require(lines[0] == "cycle_partition\tinteger_coefficient", "dual header changed")
    for line in lines[1:]:
        partition, coefficient = line.split("\t")
        dual[tuple(map(int, partition.split(",")))] = int(coefficient)
    require(len(dual) == 77, "dual table is not the frozen 77-functional")

    anchors = None
    terms = []
    action_count = 0
    lines = SEED.read_text().splitlines()
    require(lines[0] == "KRENN_SPARSE_R8_K9_TAIL_TERMS_V1", "seed magic changed")
    for line in lines[1:]:
        fields = line.split()
        if fields[0] == "ANCHORS":
            anchors = tuple(bytes.fromhex(fields[1]))
        elif fields[0] == "ACTION":
            action_count += 1
        elif fields[0] == "TERM":
            require(len(fields) == 7, "term schema changed")
            terms.append(
                {
                    "index": int(fields[1]),
                    "coefficient": int(fields[2]),
                    "word": tuple(map(int, fields[3])),
                    "multiplier": tuple(bytes.fromhex(fields[4])),
                    "source_column": int(fields[5]),
                    "role": fields[6],
                }
            )
        else:
            raise RuntimeError(f"unknown seed record: {fields[0]}")
    require(anchors is not None and len(anchors) == 12, "anchor packet changed")
    require(action_count == 2304, "H action count changed")
    require(len(terms) == 9607, "source term count changed")
    require([term["index"] for term in terms] == list(range(9607)), "term indices changed")
    return anchors, terms, dual


def audit():
    begun = perf_counter()
    anchors, terms, dual = parse_inputs()
    anchor_set = set(anchors)

    pure = []
    for colour in range(3):
        word = (colour,) * 8
        pure.append(tuple(matching_cells(word, matching) for matching in MATCHINGS))

    target_charge = Counter()
    target_emissions = Counter()
    target_partitions = {degree: Counter() for degree in range(9, 13)}
    for row0 in pure[0]:
        for row1 in pure[1]:
            for row2 in pure[2]:
                row = row0 + row1 + row2
                degree = sum(cell not in anchor_set for cell in row)
                if degree < 9:
                    continue
                require(degree <= 12, "target degree exceeded 12")
                partition = cycle_partition(anchors + row)
                target_charge[degree] += dual.get(partition, 0)
                target_emissions[degree] += 1
                target_partitions[degree][partition] += 1

    source_charge = Counter()
    source_emissions = Counter()
    source_firing_terms = {degree: set() for degree in range(9, 13)}
    source_partitions = {degree: Counter() for degree in range(9, 13)}
    for term in terms:
        multiplier = term["multiplier"]
        multiplier_degree = sum(cell not in anchor_set for cell in multiplier)
        for matching in MATCHINGS:
            selected = matching_cells(term["word"], matching)
            degree = multiplier_degree + sum(cell not in anchor_set for cell in selected)
            if degree < 9:
                continue
            require(degree <= 12, "source degree exceeded 12")
            partition = cycle_partition(anchors + multiplier + selected)
            coefficient = term["coefficient"]
            source_charge[degree] += coefficient * dual.get(partition, 0)
            source_emissions[degree] += 1
            source_firing_terms[degree].add(term["index"])
            source_partitions[degree][partition] += coefficient

    tail_charge = {degree: target_charge[degree] - source_charge[degree] for degree in range(9, 13)}
    tail = json.loads(TAIL.read_text())
    seed_meta = json.loads(SEED_META.read_text())
    require(seed_meta["tail_file_sha256"] == PINS[TAIL], "seed metadata tail pin changed")
    require(seed_meta["stabilizer_order"] == 2304, "seed metadata stabilizer changed")
    require(seed_meta["target_row_orbits"] == len(tail["tail"]), "seed metadata tail count changed")
    require(target_emissions[9] == tail["target_literal_emissions"], "K9 target emission replay mismatch")
    require(source_emissions[9] == tail["source_literal_emissions"], "K9 source emission replay mismatch")
    require(len(source_firing_terms[9]) == tail["source_firing_terms"], "K9 firing-term replay mismatch")
    require(tail_charge[9] == -18_809_856, "independent K9 charge replay mismatch")
    require(sum(tail_charge.values()) == -4_564_224, "full omitted-tail charge mismatch")

    # Independently pair the retained, already H-collected K9 quotient ledger.
    # This guards the representation bridge used above: its integer values are
    # orbit masses, not one representative coefficient per labelled row.
    quotient_k9_charge = 0
    quotient_k9_rows = 0
    for row_hex, coefficient in tail["tail"]:
        row = tuple(bytes.fromhex(row_hex))
        require(len(row) == 12, "K9 quotient row width changed")
        require(sum(cell not in anchor_set for cell in row) == 9, "quotient row left K9")
        quotient_k9_charge += int(coefficient) * dual.get(cycle_partition(anchors + row), 0)
        quotient_k9_rows += 1
    require(quotient_k9_rows == tail["tail_row_orbits"] == 49_988, "K9 quotient census changed")
    require(quotient_k9_charge == tail_charge[9], "literal/quotient K9 pairing mismatch")

    result = {
        "status": "PASS_EXACT_BOUNDED_K9_THROUGH_K12_LITERAL_CHARGE",
        "scope": "charge-only feasibility for a*(T-S) in omitted K-degrees 9..12; no row reduction or broad continuation",
        "representation_semantics": {
            "tail_values": "canonical H-coinvariant orbit masses (labelled emissions are summed into natural representatives)",
            "source_coefficients": "coefficients of quotient source columns; an H-Reynolds lift has the same quotient coordinate",
            "charge_pairing": "the 77 cycle functional is H-invariant, so literal pre-collection pairing equals orbit-mass pairing",
        },
        "identity": {
            "tail": "R_tail=(H0*H1*H2)-S9607 in K-degrees 9..12",
            "telescope": "a+E0*E1*E2 is an explicit source combination",
            "consequence": "lambda(-R_tail*E0*E1*E2)=lambda(a*R_tail)",
        },
        "counts": {
            "source_terms": len(terms),
            "source_actions_in_seed": 2304,
            "perfect_matchings_per_H_word": len(MATCHINGS),
            "target_literal_emissions": {str(k): target_emissions[k] for k in range(9, 13)},
            "source_literal_emissions": {str(k): source_emissions[k] for k in range(9, 13)},
            "source_firing_terms": {str(k): len(source_firing_terms[k]) for k in range(9, 13)},
        },
        "charges": {
            "target": {str(k): target_charge[k] for k in range(9, 13)},
            "source": {str(k): source_charge[k] for k in range(9, 13)},
            "tail_target_minus_source": {str(k): tail_charge[k] for k in range(9, 13)},
            "K10_through_K12_subtotal": sum(tail_charge[k] for k in range(10, 13)),
            "K9_through_K12_total": sum(tail_charge.values()),
            "expected_missing_correction_charge": -4_564_224,
            "retained_K9_quotient_pairing": quotient_k9_charge,
        },
        "partition_support": {
            "target": {str(k): len(target_partitions[k]) for k in range(9, 13)},
            "source_weighted_nonzero": {
                str(k): sum(value != 0 for value in source_partitions[k].values()) for k in range(9, 13)
            },
        },
        "pins": {str(path.relative_to(ROOT)): digest for path, digest in PINS.items()},
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    result["elapsed_seconds"] = perf_counter() - begun
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    result = audit()
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
