#!/usr/bin/env python3
"""Independent literal-row referee for the k=4 cycle c=0 family.

The point formulas are imported from the producer artifact, but every packet
row and the pure Hafnian are rebuilt through the support-stratum lane's raw
row map.  This deliberately does not import the producer's equations.
"""

from __future__ import annotations

from hashlib import sha256
import importlib.util
from itertools import permutations, product
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FAMILY_PATH = (ROOT / "computations" /
               "unaudited-codex-n8-dangerous-chart-bridge-2026-08-20" /
               "audit_branch0_cycle_czero_component.py")
INTERFACE_PATH = HERE / "build_support_strata_interface.py"
OUT = HERE / "results_cycle_boundary_family_referee.json"
EDGES = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


FAMILY = load("n8_cycle_boundary_family_producer", FAMILY_PATH)
INTERFACE = load("n8_cycle_boundary_raw_referee", INTERFACE_PATH)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def act_mask(mask, switches, permutation):
    """Transport a six-edge term/branch mask under switches and S4."""
    answer = 0
    for edge, (left, right) in enumerate(EDGES):
        selected = (mask >> edge) & 1
        # A switch at exactly one endpoint exchanges diagonal/offdiagonal.
        selected ^= switches[left] ^ switches[right]
        target = tuple(sorted((permutation[left], permutation[right])))
        answer |= selected << EDGE_INDEX[target]
    return answer


def main():
    values = FAMILY.point()
    equations, hafnian = INTERFACE.PROBE.equations((0,) * 6)
    labels = list(INTERFACE.raw_labels())
    require(len(equations) == len(labels) == 22,
            "literal packet row count changed")

    evaluated = tuple(FAMILY.evaluate(row, values) for row in equations)
    h_value = FAMILY.evaluate(hafnian, values)
    require(not any(evaluated), "a raw referee packet row is nonzero")
    require(h_value == FAMILY.as_l(4), "the raw referee Hafnian is not 4")

    blocks = tuple(values[4 * edge:4 * edge + 4] for edge in range(6))
    support = (1, 2, 3, 4)
    c_numerators = tuple(
        FAMILY.ONE + blocks[edge][0] * blocks[edge][3]
        for edge in support
    )
    require(c_numerators == (FAMILY.ZERO,) * 4,
            "a selected c numerator is not identically zero")
    require(tuple(blocks[edge][2] for edge in support)
            == (FAMILY.ZERO,) * 4,
            "a selected literal c entry is not zero")
    require(all(blocks[edge][0] and blocks[edge][1] and blocks[edge][3]
                for edge in support),
            "a selected a/b/d factor is generically zero")

    # Independent orbit routing: switching a support-six aligned chart with
    # branch mask 51 reaches branch0 and term mask33 in sixteen group actions.
    actions = [
        (switches, permutation)
        for switches in product((0, 1), repeat=4)
        for permutation in permutations(range(4))
        if act_mask(51, switches, permutation) == 0
        and act_mask(63, switches, permutation) == 33
    ]
    require(len(actions) == 16, "aligned boundary orbit routing changed")

    mutated = list(values)
    mutated[0] = mutated[0] - 2 * (FAMILY.RR + 2) * FAMILY.T_INV
    mutation_values = tuple(FAMILY.evaluate(row, mutated)
                            for row in equations)
    require(any(mutation_values), "hostile source mutation did not fire")

    result = {
        "status": "UNAUDITED independent raw-row cycle-boundary referee",
        "producer_formula_path": str(FAMILY_PATH.relative_to(ROOT)),
        "independent_raw_map_path": str(INTERFACE_PATH.relative_to(ROOT)),
        "defect_support_edge_indices": list(support),
        "literal_source_labels": labels,
        "literal_zero_row_count": len(evaluated),
        "pure_H": h_value.encode(),
        "selected_c_numerators_zero": len(c_numerators),
        "selected_literal_c_entries_zero": len(support),
        "aligned_boundary_routing": {
            "from_branch_term": [51, 63],
            "to_branch_term": [0, 33],
            "action_count": len(actions),
        },
        "hostile_mutation_nonzero_row_count": sum(bool(row)
                                                   for row in mutation_values),
        "conclusion": (
            "The explicit H-live k4-cycle family lies entirely on the four "
            "c_e=0 faces and routes to a previously closed aligned chart."
        ),
        "scope_guard": (
            "This verifies the displayed boundary family only; it neither "
            "classifies all cycle components nor proves the c-nonzero "
            "interior empty."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("branch0 k4-cycle boundary referee: PASS")
    print("rows / H / mutation:", len(evaluated), h_value.encode(),
          result["hostile_mutation_nonzero_row_count"])
    print("aligned routing actions:", len(actions))
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
