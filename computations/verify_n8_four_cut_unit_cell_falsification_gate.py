#!/usr/bin/env python3
"""Exact N=8 one-cell falsification gate for four adjacent five-cuts.

This checker starts from the independently audited three-cut countermodel,
adds its two-source mixed-word repair, and adds two diagonal cells which
restore the missing colour-zero pure coefficient.  The resulting integral
source has all three pure coefficients equal to one and three active complete
five-cut quotient identities, but it is not GHZ because eight mixed
coefficients survive.

Every one of the 252 endpoint-colour coordinates is then changed by +1 and
-1, including occupied coordinates.  For each of the 504 exact mutations we
rebuild the full matching tensor, both odd crossing sectors on every cut, and
the five-site cofactor-insertion spaces over Q.  The falsification event is a
mutation which preserves all three pure anchors and the original active cut
triple while making one of the other three adjacent cuts active and complete.

No such mutation exists.  This is deliberately only a signed-unit one-cell
barrier around one source; it is not a four-cut theorem and not a proof of
Krenn's conjecture.
"""

from __future__ import annotations

import importlib.util
from fractions import Fraction
from pathlib import Path


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load_three_cut_verifier():
    path = Path(__file__).with_name(
        "verify_three_adjacent_five_cut_complete_quotient_countermodel.py"
    )
    spec = importlib.util.spec_from_file_location("three_cut_source", path)
    require(spec is not None and spec.loader is not None, "cannot load source verifier")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


THREE_CUTS = (2, 3, 4)
FOURTH_CUT_CANDIDATES = (0, 1, 5)
PURE_WORDS = tuple((colour,) * 8 for colour in range(3))
ANCHOR_REPAIR = (
    (2, 3, 0, 0, 1),
    (6, 7, 0, 0, 1),
)

EXPECTED_BASE_TENSOR = {
    (0, 0, 0, 0, 0, 0, 0, 0): Fraction(1),
    (0, 0, 0, 0, 0, 0, 1, 2): Fraction(-1),
    (0, 0, 2, 1, 0, 0, 0, 0): Fraction(1),
    (1, 1, 1, 1, 1, 0, 0, 0): Fraction(1),
    (1, 1, 1, 1, 1, 0, 1, 2): Fraction(-1),
    (1, 1, 1, 1, 1, 1, 1, 1): Fraction(1),
    (1, 2, 1, 2, 0, 0, 0, 0): Fraction(1),
    (1, 2, 1, 2, 0, 0, 1, 2): Fraction(-1),
    (2, 2, 0, 2, 2, 0, 0, 0): Fraction(1),
    (2, 2, 0, 2, 2, 0, 1, 2): Fraction(-1),
    (2, 2, 2, 2, 2, 2, 2, 2): Fraction(1),
}

EXPECTED_BASE_CUTS = {
    0: (False, 3, (False, False, False), 14),
    1: (False, 3, (False, False, False), 14),
    2: (True, 1, (True, False, True), 14),
    3: (True, 1, (True, True, False), 14),
    4: (True, 2, (True, False, False), 14),
    5: (False, 1, (False, True, True), 15),
}


def copy_cells(cells):
    return {edge: list(entries) for edge, entries in cells.items()}


def active_complete(record) -> bool:
    # For an odd 3|5 cut the literal matching expansion has only T1 and T3.
    # one_cross_factors checks T1 in the insertion cylinder; full checks
    # T3-Delta in it.  Positive defect makes the quotient target-active.
    return bool(
        record["one_cross_factors"] and record["full"] and record["defect"] > 0
    )


def pure_tuple(module, tensor):
    return tuple(tensor.get(word, Fraction(0)) for word in PURE_WORDS)


def build_base(module):
    cells = module.cells_from_mask()
    module.add_sources(cells, module.REPAIR_SOURCES)
    module.add_sources(cells, ANCHOR_REPAIR)
    return cells


def audit_base(module, cells) -> None:
    tensor = module.matching_tensor(module.B, cells)
    require(tensor == EXPECTED_BASE_TENSOR, "anchored base tensor changed")
    require(pure_tuple(module, tensor) == (1, 1, 1), "pure anchors are not all one")
    mixed_count = sum(len(set(word)) > 1 for word in tensor)
    require(mixed_count == 8, "anchored base mixed-debt count changed")

    for z in module.S:
        record = module.cut_record(z, cells)
        observed = (
            bool(record["full"]),
            int(record["defect"]),
            tuple(record["constant_members"]),
            int(record["rank"]),
        )
        require(observed == EXPECTED_BASE_CUTS[z], f"base cut {z} changed")
        require(record["one_cross_factors"], f"base T1 factorization failed at cut {z}")


def audit_signed_unit_mutations(module, base):
    counts = {
        "tested": 0,
        "anchor_preserving": 0,
        "triple_preserving": 0,
        "fourth_cut_extensions": 0,
    }
    preserving_coordinates = set()

    for u in range(8):
        for v in range(u + 1, 8):
            for colour_u in range(3):
                for colour_v in range(3):
                    coordinate = (u, v, colour_u, colour_v)
                    for increment in (-1, 1):
                        counts["tested"] += 1
                        cells = copy_cells(base)
                        module.add_sources(cells, ((*coordinate, increment),))

                        tensor = module.matching_tensor(module.B, cells)
                        if pure_tuple(module, tensor) != (1, 1, 1):
                            continue
                        counts["anchor_preserving"] += 1

                        if not all(
                            active_complete(module.cut_record(z, cells))
                            for z in THREE_CUTS
                        ):
                            continue
                        counts["triple_preserving"] += 1
                        preserving_coordinates.add((coordinate, increment))

                        for z in FOURTH_CUT_CANDIDATES:
                            if active_complete(module.cut_record(z, cells)):
                                counts["fourth_cut_extensions"] += 1
                                raise RuntimeError(
                                    "four-cut falsifier found: "
                                    f"coordinate={coordinate}, increment={increment}, cut={z}"
                                )

    require(counts["tested"] == 504, "signed-unit mutation census is incomplete")
    require(
        counts["anchor_preserving"] == 478,
        "anchor-preserving mutation count changed",
    )
    require(
        counts["triple_preserving"] == 34,
        "three-cut-preserving mutation count changed",
    )
    require(len(preserving_coordinates) == 34, "mutation ledger contains duplicates")
    require(
        counts["fourth_cut_extensions"] == 0,
        "a fourth-cut extension escaped fail-fast handling",
    )
    return counts


def main() -> None:
    module = load_three_cut_verifier()
    base = build_base(module)
    audit_base(module, base)
    counts = audit_signed_unit_mutations(module, base)

    print("N=8 anchored four-cut signed-unit falsification gate: PASS")
    print("base pure tuple: (1, 1, 1); mixed debts: 8")
    print("active complete cuts on base: z=2,3,4; failed cuts: z=0,1,5")
    print(
        "mutations: "
        f"tested={counts['tested']}, "
        f"anchor-preserving={counts['anchor_preserving']}, "
        f"triple-preserving={counts['triple_preserving']}, "
        f"fourth-cut extensions={counts['fourth_cut_extensions']}"
    )
    print("verdict: no signed-unit one-cell repair reaches a fourth active cut")


if __name__ == "__main__":
    main()
