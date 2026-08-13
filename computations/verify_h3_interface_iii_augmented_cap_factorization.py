#!/usr/bin/env python3
r"""Factor the inactive Yw-to-W obligation through augmented Interface III.

The old physical chain r0-T already has the normalized signature

    (ridge,Eq,Yw_boundary,W,ainc,target,ores)
       = (0,1,1,1,-1,0,0).

The exact repair required by the normalized C5 base-column theorem is

    A_v=(-r_v,-Eq,0,0,0,0,0).

Therefore a source-valid, same-grade construction of A_v by the completed
root-even Interface III gives

    P_v=(r0-T)+A_v=(-r_v,0,1,1,-1,0,0),

which is precisely the physical augmented comparison column: its derived
Yw boundary and physical W readout agree.  No fourth source generator is
needed.  However W is an independent output row: a theorem which constructs
only the projection forgetting W does not imply the comparison.  The W=0
typing of A_v (equivalently W(P_v)=1) must be included in Interface III.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_shifted_filler_koszul_absorption_no_go.py":
        "37929e514e1f796725d658378b30b953d6859dfa1dcd347143c9ce80f25e6f16",
    "computations/verify_h3_rootless_normalized_c5_base_column_source_separator.py":
        "635b3e667613049817f04440401d31237db259ab7cf9948989e0da2674efb022",
    "computations/verify_h3_rootless_normalized_c5_augmented_comparison_gate.py":
        "fd6e94cd52a9f6950bf752887f9bea129373f6686b12704f6d2eaf29b7fa0dca",
    "computations/verify_h3_augmented_derived_comparison_shared_rootless_inactive_interface.py":
        "81c1bd9de57871cb334de5f3a1b4c7a3ede2a25316841c4ee0d3902a30b35341",
    "computations/verify_h3_component_iv_collision_family_normal_jet_interface.py":
        "a777687ed775c73b10129c0bee32b59f12fa3b579de39e6c4154e5ed94634651",
    "computations/verify_h3_component_iv_weighted_normal_hasse_companions.py":
        "f94b13e3d08d0f090112648f0b7a1d9b7d07ce857d6b5d979d730dc4761a8ce0",
}
EXPECTED_LEDGER_SHA256 = (
    "bcfa7eb71274c5a1601858b414b89eb2ddd2a83068910c2ee8b11ece3cdc69ae"
)

FACES = (1, 3, 5, 2, 4)
ROWS = tuple(f"ridge_{face}" for face in FACES) + (
    "Eq", "Yw_boundary", "W", "ainc", "target", "ores",
)


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def vector(**entries: int) -> tuple[int, ...]:
    require(set(entries).issubset(ROWS), ("unknown row", entries))
    return tuple(entries.get(row, 0) for row in ROWS)


def add(*columns: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(sum(column[index] for column in columns)
                 for index in range(len(ROWS)))


def scale(coefficient: int, column: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(coefficient * entry for entry in column)


def rank(columns: list[tuple[int, ...]]) -> int:
    if not columns:
        return 0
    matrix = [[Q(columns[column][row]) for column in range(len(columns))]
              for row in range(len(columns[0]))]
    pivot_row = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(pivot_row, len(matrix))
                      if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        value = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / value for entry in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            value = matrix[row][column]
            matrix[row] = [left - value * right for left, right in
                           zip(matrix[row], matrix[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def base_factorization():
    old_cap = vector(Eq=1, Yw_boundary=1, W=1, ainc=-1)
    repairs = [vector(**{f"ridge_{face}": -1, "Eq": -1})
               for face in FACES]
    physical = [add(old_cap, repair) for repair in repairs]
    expected = [vector(**{
        f"ridge_{face}": -1, "Yw_boundary": 1, "W": 1,
        "ainc": -1,
    }) for face in FACES]
    require(physical == expected,
            "r0-T plus Interface-III repair stopped giving the base columns")
    for repair in repairs:
        require(all(repair[ROWS.index(row)] == 0
                    for row in ("Yw_boundary", "W", "ainc", "target", "ores")),
                "the root-even repair acquired an augmented cap defect")
    for column in physical:
        require(column[ROWS.index("Yw_boundary")]
                == column[ROWS.index("W")] == 1,
                "derived Yw and physical W stopped agreeing")
        require(column[ROWS.index("Eq")] == 0
                and column[ROWS.index("ainc")] == -1
                and column[ROWS.index("target")] == 0
                and column[ROWS.index("ores")] == 0,
                "completed physical base typing changed")
    return old_cap, repairs, physical


def c5_propagation(physical):
    edges = []
    for index in range(5):
        edges.append(add(physical[index],
                         scale(-1, physical[(index + 1) % 5])))
    expected = []
    for index, face in enumerate(FACES):
        following = FACES[(index + 1) % 5]
        expected.append(vector(**{f"ridge_{face}": -1,
                                  f"ridge_{following}": 1}))
    require(edges == expected and add(*edges) == vector(),
            "augmented C5 propagation changed")
    require(rank(edges) == 4 and rank(edges + [physical[0]]) == 5,
            "one augmented base stopped completing the C5 edge family")
    w_covector = vector(W=1)
    require(all(sum(a * b for a, b in zip(w_covector, edge, strict=True)) == 0
                for edge in edges), "W stopped killing all collision edges")
    require(sum(a * b for a, b in zip(
        w_covector, physical[0], strict=True)) == 1,
        "W stopped detecting the augmented base")
    return edges


def projection_counterguard(repair):
    # Forget W.  Two putative repairs have identical reduced-Eq/ridge,
    # boundary, anchor, target, and residue rows, but lead to different cap
    # values after adding r0-T.  Hence W is not a consequence of the
    # projected Interface-III theorem.
    w_unit = vector(W=1)
    bad_repair = add(repair, scale(-1, w_unit))
    keep = tuple(index for index, row in enumerate(ROWS) if row != "W")
    require(tuple(repair[index] for index in keep)
            == tuple(bad_repair[index] for index in keep),
            "the W counterguard changed a protected projected row")
    old_cap = vector(Eq=1, Yw_boundary=1, W=1, ainc=-1)
    good = add(old_cap, repair)
    bad = add(old_cap, bad_repair)
    require(good[ROWS.index("Yw_boundary")] == 1
            and bad[ROWS.index("Yw_boundary")] == 1,
            "counterguard changed the derived boundary")
    require((good[ROWS.index("W")], bad[ROWS.index("W")]) == (1, 0),
            "counterguard stopped separating the physical cap row")
    return {
        "projected_rows": [ROWS[index] for index in keep],
        "good_repair_W": 0,
        "bad_same_projection_repair_W": -1,
        "completed_good_Yw_W": [1, 1],
        "completed_bad_Yw_W": [1, 0],
        "verdict": (
            "all reduced-Eq/ridge/anchor/target/residue equations leave W "
            "undetermined; W=0 on the repair is an independent augmented "
            "row condition"
        ),
    }


class Expr:
    """Integral polynomial in formal normal-Hasse coefficient labels."""

    def __init__(self, terms=()):
        if isinstance(terms, int):
            terms = {(): terms}
        elif isinstance(terms, str):
            terms = {(terms,): 1}
        self.terms = Counter({tuple(sorted(term)): coefficient
                              for term, coefficient in dict(terms).items()
                              if coefficient})

    def __add__(self, other):
        other = other if isinstance(other, Expr) else Expr(other)
        answer = Counter(self.terms)
        answer.update(other.terms)
        return Expr({term: coefficient for term, coefficient in answer.items()
                     if coefficient})

    __radd__ = __add__

    def __neg__(self):
        return Expr({term: -coefficient
                     for term, coefficient in self.terms.items()})

    def __eq__(self, other):
        other = other if isinstance(other, Expr) else Expr(other)
        return self.terms == other.terms


def jet_factorization():
    records = []
    for order in range(4):
        coefficients = [Expr(f"h_{power}") for power in range(order + 1)]
        # The existing cap family has identical Yw-boundary and W
        # convolutions.  A Rees-linear Interface-III repair is required to
        # have zero in both rows, so addition preserves equality gradewise.
        cap_yw = list(coefficients)
        cap_w = list(coefficients)
        repair_yw = [Expr() for _ in coefficients]
        repair_w = [Expr() for _ in coefficients]
        completed_yw = [left + right for left, right in
                        zip(cap_yw, repair_yw, strict=True)]
        completed_w = [left + right for left, right in
                       zip(cap_w, repair_w, strict=True)]
        require(completed_yw == completed_w == coefficients,
                ("normal-jet cap factorization changed", order))
        records.append({
            "normal_order": order,
            "convolution_terms": order + 1,
            "Yw_boundary_equals_W_gradewise": True,
            "new_cap_generator_type": False,
        })
    return records


def main() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))
    old_cap, repairs, physical = base_factorization()
    edges = c5_propagation(physical)
    counterguard = projection_counterguard(repairs[0])
    jets = jet_factorization()
    ledger = {
        "theorem": "Interface-III augmented inactive-cap factorization",
        "pins": PINS,
        "row_order": list(ROWS),
        "existing_physical_cap_chain": {
            "name": "r0-T",
            "column": list(old_cap),
            "differential": "Yw+(H0-u)e_Eq before the reduced-Eq repair",
            "fine_grade": (
                "multiply by the selected incident-cycle unit but retain its "
                "repeated P3+K2 label"
            ),
        },
        "conditional_completed_Interface_III_repairs": [
            list(repair) for repair in repairs
        ],
        "factorized_physical_images": [list(column) for column in physical],
        "identity": (
            "P_v=(r0-T)+A_v, with A_v=-r_v-e_Eq and zero "
            "Yw/W/ainc/target/ores; hence P_v has "
            "(-r_v,Eq=0,Yw=1,W=1,ainc=-1,target=ores=0)"
        ),
        "C5": {
            "edge_columns": [list(edge) for edge in edges],
            "edge_rank": 4,
            "edge_plus_one_base_rank": 5,
            "one_base_propagates_all_faces": True,
        },
        "normal_Rees_prolongation": jets,
        "sharp_projection_counterguard": counterguard,
        "theorem_count": (
            "Yw->W is not a fourth source-generator theorem after a "
            "source-valid same-grade A_v is constructed: the old r0-T cap "
            "supplies W and A_v repairs its Eq/ridge defect.  It is, however, "
            "an independent augmented output-row condition on Interface III; "
            "a projected theorem omitting W does not close the cap"
        ),
        "required_Interface_III_statement": (
            "construct the final target/residue-cancelled root-even repair "
            "A_v in the same labelled repeated grade, Rees-linearly, with "
            "W=Yw_boundary=ainc=target=ores=0; then use the existing r0-T "
            "section.  Equivalently construct P_v directly and require the "
            "single augmented equation W(P_v)=Yw(P_v)=1"
        ),
        "scope": (
            "exact conditional factorization and sharp independence guard; "
            "does not construct A_v, the raw target-bearing C_plus cell, its "
            "labelled-residue correction, or the beta=0 membership"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("Interface-III cap ledger changed", digest))
    print("h3 Interface III augmented inactive-cap factorization: PASS")
    print("P_v=(r0-T)+(-r_v-e_Eq): exact")
    print("Yw->W source-generator theorem: NO, conditional on Interface III")
    print("W augmented output-row condition: YES, independent and required")
    print("normal/Rees orders 0..3: same factorization")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
