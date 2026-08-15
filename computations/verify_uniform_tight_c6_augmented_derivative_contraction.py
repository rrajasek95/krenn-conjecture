#!/usr/bin/env python3
"""Uniform tight-cut contraction criterion and the sharp C6 audit.

On a physically tight cut, the complete matching tensor is jointly linear in
the live cut cells.  If a forced escape derivative lies in the span of the
live cap derivatives, its coefficient can be absorbed into those cap cells
and the escape cell deleted.  If it does not, a nonzero pure projection makes
it a literal active outside channel; a private mixed projection is a unit.

This checker audits the exact affine deletion branch, the complete 729-row
C6 escape matrices for all twelve minimal escapes, and the exact K4 GHZ
sharpness control.  The two committed derivative theorems are byte-pinned.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_tight_cut_minimal_derivative_independence_gate.py":
        "69c0a995092c4cad6ffadbd82f00332ff27719b24b1f73d23583ac28245c14d2",
    "notes/2026-08-14-tight-cut-minimal-physical-derivative-independence.md":
        "35cda28bf307f5d33e7ba0dd562b1b841fdba4007f0f3e4392b2f51a8a03558f",
    "computations/verify_uniform_c6_seven_cell_escape_physical_derivative_rank.py":
        "f78a90212c71800bb6ccb67edafc36199f0caabc53a251ea89333f81cf46ed86",
    "notes/2026-08-14-c6-seven-cell-escape-physical-derivative-rank.md":
        "c5cfc7ce47f6426fda393e82d1d01d14f5242959be185e67c56bedc726fd6210",
}
EXPECTED_LEDGER_SHA256 = (
    "99e2c0b7f8e67de0ca3b2b5038ec23437959968831b84154c6995c36ddbc0399"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned derivative theorem changed", relative,
                 actual, expected))


def nonzero_coordinates(module, vector):
    return tuple((module.word_name(module.WORDS[index]), str(value))
                 for index, value in enumerate(vector) if value)


def exact_dependent_cut_deletion(tight) -> dict[str, object]:
    # A genuine physical K4 local channel with two distinct tight-cut cells
    # having the same complete derivative.  Its tensor is e_0000, with
    # coefficients 2 and -1 on the two occurrences.
    cell_a = (tight.edge(0, 1), 0, 0)
    cell_b = (tight.edge(0, 2), 0, 0)
    support = {
        cell_a: Q(2),
        (tight.edge(2, 3), 0, 0): Q(1),
        cell_b: Q(-1),
        (tight.edge(1, 3), 0, 0): Q(1),
    }
    tensor = tight.matching_tensor(support)
    derivative_a = tight.derivative_tensor(support, cell_a)
    derivative_b = tight.derivative_tensor(support, cell_b)
    pure_zero = tight.WORDS.index((0, 0, 0, 0))
    require(tuple((index, value) for index, value in enumerate(tensor)
                  if value) == ((pure_zero, Q(1)),), tensor)
    require(derivative_a == derivative_b
            and tight.matrix_rank((derivative_a, derivative_b)) == 1,
            (derivative_a, derivative_b))

    # D_b=D_a.  Absorb q_b into q_a: q'_a=2+(-1)=1, q'_b=0.
    reduced = dict(support)
    reduced[cell_a] = support[cell_a] + support[cell_b]
    reduced.pop(cell_b)
    require(reduced[cell_a] == 1
            and tight.matching_tensor(reduced) == tensor,
            (reduced, tight.matching_tensor(reduced), tensor))
    return {
        "vertices": 4,
        "tight_shore": [0],
        "cut_cells": ["01;00", "02;00"],
        "complete_rows": len(tight.WORDS),
        "derivative_relation": "D_(02;00)-D_(01;00)=0",
        "old_cut_rank": 1,
        "affine_move": "q01'=q01+q02=1; q02'=0",
        "tensor_before_after": "e_0000",
        "deleted_occupied_cells": 1,
        "all_physical_rows_preserved": True,
    }


def c6_complete_augmented_span(c6) -> dict[str, object]:
    base = c6.seven_cell_base()
    cap_cells = tuple(c6.cell(c6.CAP, colour) for colour in c6.COLOURS)
    pure_words = tuple((colour,) * c6.N for colour in c6.COLOURS)
    pure_indices = tuple(c6.WORDS.index(word) for word in pure_words)
    mixed_indices = tuple(index for index, word in enumerate(c6.WORDS)
                          if len(set(word)) > 1)
    require(len(pure_indices) == 3 and len(mixed_indices) == 726,
            (pure_indices, len(mixed_indices)))

    records = []
    outside_cells = set()
    for matching in (item for item in c6.MATCHINGS if c6.CAP not in item):
        support, _missing = c6.augment_by_escape(base, matching)

        # The one-vertex shore {3} is physically tight.  Its live cells are
        # the three cap colours and the unique edge of the escape incident 3.
        escape_edge = next(endpoints for endpoints in matching
                           if 3 in endpoints)
        escape_cell = c6.cell(escape_edge, 1)
        live_cut_cells = tuple(sorted(
            selected for selected in support if 3 in selected[0]
        ))
        require(set(live_cut_cells) == set(cap_cells) | {escape_cell}
                and len(live_cut_cells) == 4,
                (matching, live_cut_cells, cap_cells, escape_cell))
        outside_cells.add(escape_cell)

        cap_derivatives = tuple(c6.derivative_tensor(support, selected)
                                for selected in cap_cells)
        escape_derivative = c6.derivative_tensor(support, escape_cell)
        cap_rank = c6.matrix_rank(cap_derivatives)
        augmented_rank = c6.matrix_rank(cap_derivatives
                                         + (escape_derivative,))
        pure_projection = tuple(escape_derivative[index]
                                for index in pure_indices)
        mixed_projection = tuple(escape_derivative[index]
                                 for index in mixed_indices)
        require(cap_rank == 0 and augmented_rank == 1,
                (matching, cap_rank, augmented_rank))
        require(pure_projection in ((Q(0), Q(1), Q(0)),
                                    (Q(0), Q(-1), Q(0)))
                and not any(mixed_projection),
                (matching, pure_projection,
                 nonzero_coordinates(c6, escape_derivative)))
        require(support[escape_cell] * pure_projection[1] == 1,
                (matching, escape_cell, support[escape_cell], pure_projection))

        # The active pure derivative coordinate is a single literal matching
        # cofactor, not a cancellation aggregate.
        pure_word = (1,) * c6.N
        derivative_occurrences = []
        for fine in c6.MATCHINGS:
            cells = c6.occurrence_cells(fine, pure_word)
            if escape_cell not in cells:
                continue
            remaining = tuple(item for item in cells
                              if item != escape_cell)
            if all(item in support for item in remaining):
                derivative_occurrences.append((
                    c6.matching_name(fine),
                    c6.product_value(support[item] for item in remaining),
                ))
        require(derivative_occurrences == [
            (c6.matching_name(matching), pure_projection[1])
        ], (matching, derivative_occurrences, pure_projection))

        tensor = c6.matching_tensor(support)
        deleted = dict(support)
        for selected in cap_cells:
            deleted.pop(selected)
        require(c6.matching_tensor(deleted) == tensor,
                (matching, nonzero_coordinates(c6, tensor),
                 nonzero_coordinates(c6, c6.matching_tensor(deleted))))

        records.append({
            "escape_fine": c6.matching_name(matching),
            "tight_cut_cell": (
                f"{escape_cell[0][0]}{escape_cell[0][1]};11"
            ),
            "tight_cut_cell_weight": str(support[escape_cell]),
            "complete_row_count": len(c6.WORDS),
            "pure_row_count": len(pure_indices),
            "mixed_row_count": len(mixed_indices),
            "cap_span_rank": cap_rank,
            "rank_with_escape": augmented_rank,
            "escape_pure_projection": tuple(map(str, pure_projection)),
            "escape_mixed_support": 0,
            "weighted_pure_one_value": "1",
            "literal_derivative_occurrence": derivative_occurrences[0][0],
            "classification": "active outside tight-cut channel",
            "killed_cap_cells_delete": True,
        })

    require(len(records) == 12 and len(outside_cells) == 4,
            (len(records), outside_cells))
    return {
        "vertices": c6.N,
        "tight_shore": [3],
        "cap": "34",
        "physical_output_space_dimension": len(c6.WORDS),
        "pure_rows": [c6.word_name(word) for word in pure_words],
        "mixed_rows": len(mixed_indices),
        "forced_residual_equation": "H=1-1=0",
        "complete_cap_derivative_span_rank": 0,
        "complete_augmented_rank": 1,
        "escape_cases": len(records),
        "distinct_outside_cut_cells": tuple(sorted(
            f"{item[0][0]}{item[0][1]};11" for item in outside_cells
        )),
        "records": tuple(records),
        "uniform_classification": (
            "all twelve escapes lie outside the cap span and have one "
            "literal pure-one cofactor occurrence; all mixed derivative "
            "coordinates vanish"
        ),
        "exact_support_move": (
            "the three zero cap columns delete; the escape does not"
        ),
    }


def exact_full_ghz_sharpness(tight) -> dict[str, object]:
    # The committed K4 source is the smallest nontrivial exact full-GHZ
    # control.  Every cut state is independent but exposes a private pure
    # channel, so it realizes the outside branch rather than refuting the
    # contraction criterion.
    support = {}
    for colour, matching in enumerate(tight.ONE_FACTORS):
        for endpoints in matching:
            support[(endpoints, colour, colour)] = Q(1)
    tensor = tight.matching_tensor(support)
    require(tensor == tight.target_tensor(), "K4 exact target changed")
    cut_cells = tuple((tight.edge(0, colour + 1), colour, colour)
                      for colour in tight.COLOURS)
    derivatives = tuple(tight.derivative_tensor(support, selected)
                        for selected in cut_cells)
    require(tight.matrix_rank(derivatives) == 3, derivatives)
    records = []
    for colour, derivative in enumerate(derivatives):
        others = tuple(item for index, item in enumerate(derivatives)
                       if index != colour)
        pure_index = tight.WORDS.index((colour,) * 4)
        require(tight.matrix_rank(others) == 2
                and tight.matrix_rank(others + (derivative,)) == 3
                and derivative[pure_index] == 1
                and all(not item[pure_index] for item in others),
                (colour, derivative, others))
        records.append({
            "cut_cell": f"0{colour + 1};{colour}{colour}",
            "rank_other_with_selected": [2, 3],
            "private_pure_word": str(colour) * 4,
            "classification": "essential active outside channel",
        })
    return {
        "full_GHZ_source": True,
        "vertices": 4,
        "all_words_checked": len(tight.WORDS),
        "tight_shore": [0],
        "derivative_rank": 3,
        "records": tuple(records),
        "guard_to_forced_deletion": True,
        "guard_to_span_or_active_trichotomy": False,
        "verdict": (
            "the smallest exact full target makes independent derivatives "
            "essential, but each has a literal private pure witness"
        ),
    }


def uniform_criterion() -> dict[str, object]:
    return {
        "setup": (
            "on a tight cut J, Delta=sum_(j in J) q_j D_j in the complete "
            "physical word space; every D_j is independent of all q_i"
        ),
        "forced_escape_selection": (
            "if the outside contribution to pure word b^N is nonzero, "
            "some live outside j has q_j*(D_j)_(b^N) nonzero"
        ),
        "span_branch": (
            "if D_j=sum_(c in C) a_c D_c for live cap cells C, set "
            "q'_j=0 and q'_c=q_c+q_j*a_c; every pure and mixed row is "
            "unchanged and occupied support strictly decreases"
        ),
        "outside_branch": (
            "if D_j is not in span(D_C), its nonzero pure projection is a "
            "literal active outside derivative channel; a private nonzero "
            "mixed occurrence is instead a source unit"
        ),
        "minimal_source_consequence": (
            "the span branch is impossible in a support-minimal source, so "
            "forced escape mass must use physically independent outside "
            "channels; any zero/dependent live cap column deletes"
        ),
        "scope_guard": (
            "this deletes endpoint-decorated cells at fixed N, not two "
            "sites; active outside does not yet mean active clean cap "
            "without a private/common-cofactor landing theorem"
        ),
    }


def audit() -> dict[str, object]:
    pin_dependencies()
    tight = load(
        "computations/verify_uniform_tight_cut_minimal_derivative_independence_gate.py",
        "tight_c6_augmented_tight",
    )
    c6 = load(
        "computations/verify_uniform_c6_seven_cell_escape_physical_derivative_rank.py",
        "tight_c6_augmented_c6",
    )
    return {
        "theorem": "uniform tight-cut augmented derivative contraction criterion",
        "pins": PINS,
        "criterion": uniform_criterion(),
        "exact_dependent_span_branch": exact_dependent_cut_deletion(tight),
        "complete_C6_augmented_span": c6_complete_augmented_span(c6),
        "smallest_exact_full_GHZ_sharpness": exact_full_ghz_sharpness(tight),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("structural", "full", "exhaustive"),
                        default="structural")
    arguments = parser.parse_args()
    ledger = {"mode_independent": True, "audit": audit()}
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger changed", digest, EXPECTED_LEDGER_SHA256))
    print("uniform tight-C6 augmented derivative contraction: PASS")
    print("mode", arguments.mode)
    print("C6 cap span / augmented rank", 0, 1)
    print("all 12 C6 escapes: literal active outside channel")
    print("dependent span branch: exact occupied-cell deletion")
    print("sha256:", digest)


if __name__ == "__main__":
    main()
