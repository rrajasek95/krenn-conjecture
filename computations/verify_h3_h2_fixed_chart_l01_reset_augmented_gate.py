#!/usr/bin/env python3
"""Obstruct the first fixed-chart reset and pin its augmented landing.

The full-site H2 coefficient action contracts the centered direction tags,
but a fixed pointed chart retains the scalar proper face

    L01=(2Dq01-p0s1-p1s0) H2345.

This checker asks whether L01 can be cancelled by a lower, source-valid
constant logarithmic Euler correction in the same complete K8 response
polynomial.  Every such correction is an edge-weight row on the 105 perfect
matchings.  That row space has rank 21; L01 raises it to 22.  A literal
12-occurrence covector kills every edge-weight row and the complete response
row, but reads one on L01.  Thus the fixed-chart reset cannot be completed by
any constant coordinate Euler, site/type Euler, or response-row correction.

The presentation-safe graph cone retains the obstruction as a scalar graph
coordinate.  A genuinely physical reset must place that coordinate in the
same word/fine/H2 grade with protected q/anchor/target/ridge rows.  Once it is
placed, the pinned cap/Cartan theorem supplies the exact filler-or-augmented-
terminal alternative.  The coefficient calculation does not itself supply
that placement.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_response_h2_full_site_tag_contraction.py":
        "9cebd563781fa90c4e1203799fdd8a5a505c0b78992ff2535c313b8ce414213f",
    "notes/uniform-response-h2-full-site-tag-contraction.md":
        "a59f65bff094ffdff10e7500c36d9e21bc0c8e0688881537541a5407a14c6354",
    "computations/verify_h3_h2_full_site_chart_swap_pointed_scalar_guard.py":
        "bc35781e0f57bbd1202711e2dc818417d76fa87c69e33d3d4b01540e06865557",
    "notes/h3-h2-full-site-chart-swap-pointed-scalar-guard.md":
        "77771f8eee2a4bbaeb5a9575961efb9c7728833e28bca86d33102806aeffa6c2",
    "computations/verify_h3_h2_c4_trivial_tag_euler_scalar_face_gate.py":
        "47378f8ce904021bb802e0e4fd59de1591f0cd7333e1fcbc645e62cf40deb499",
    "notes/h3-h2-c4-trivial-tag-euler-scalar-face-gate.md":
        "3d16b7a1b77030eaaa5ba3fc342b927a7ee750db2c4f8091868591acc261477f",
    "computations/verify_h3_active_coloop_redistribution_second_hasse_face_classification.py":
        "b03c096eb5bc4e6307cafa966f3d66d8c087e78bb8793c8448eec33f51e7e76a",
    "notes/h3-active-coloop-redistribution-second-hasse-face-classification.md":
        "985737011ea321c70096a89ea2a719db207c304d947ff4899133b39e14c46276",
    "computations/verify_h3_o2_augmented_terminal_cap_cartan_extension_gate.py":
        "8a9bfe47c934658d1b10ad42f283d6a017c27125bcb98615882e4bacd975f1eb",
    "notes/h3-o2-augmented-terminal-cap-cartan-extension-gate.md":
        "e9c0cf3c76cbe4c8061574d2b977bf1189a1fa299ef17ae1d2e463c08a313429",
}
EXPECTED_LEDGER_SHA256 = "94f11da21af93ef6d07b68b6d4d42c3362e4095360798b1decb4aecdacf5e6fe"


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def rank(rows) -> int:
    work = [list(map(Q, row)) for row in rows]
    if not work:
        return 0
    pivot_row = 0
    for column in range(len(work[0])):
        pivot = next((row for row in range(pivot_row, len(work))
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right
                         in zip(work[row], work[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def dot(left, right):
    return sum((Q(a) * Q(b)
                for a, b in zip(left, right, strict=True)), Q(0))


def scalar_vector(classification, response_terms):
    q = classification.q
    p = classification.p
    s = classification.s
    direction_pairs = (
        frozenset((classification.D, q(0, 1))),
        frozenset((p(0), s(1))),
        frozenset((p(1), s(0))),
    )
    weights = (Q(2), Q(-1), Q(-1))
    answer = []
    for monomial in response_terms:
        hits = [weight for pair, weight
                in zip(direction_pairs, weights, strict=True)
                if pair.issubset(monomial)]
        require(len(hits) <= 1,
                ("one matching contained two direction pairs", monomial))
        answer.append(hits[0] if hits else Q(0))
    require(Counter(answer) == Counter({Q(0): 96, Q(2): 3, Q(-1): 6}),
            ("the L01 coefficient profile changed", Counter(answer)))
    return tuple(answer)


def literal_dual_records(classification):
    q = classification.q
    p = classification.p
    s = classification.s
    d = classification.D
    # The signs are normalized so the covector reads one on L01.  Every
    # monomial is a literal response occurrence/perfect matching of K8.
    return (
        (Q(1, 3), tuple(sorted((d, q(0, 1), q(2, 3), q(4, 5))))),
        (Q(-1, 3), tuple(sorted((d, q(0, 3), q(1, 4), q(2, 5))))),
        (Q(-1, 3), tuple(sorted((d, q(0, 5), q(1, 2), q(3, 4))))),
        (Q(1, 3), tuple(sorted((d, q(0, 5), q(1, 4), q(2, 3))))),
        (Q(-1, 3), tuple(sorted((p(0), q(2, 3), q(4, 5), s(1))))),
        (Q(1, 3), tuple(sorted((p(0), q(2, 5), q(3, 4), s(1))))),
        (Q(-1, 3), tuple(sorted((p(0), q(1, 3), q(4, 5), s(2))))),
        (Q(1, 3), tuple(sorted((p(0), q(1, 2), q(4, 5), s(3))))),
        (Q(-1, 3), tuple(sorted((p(1), q(2, 3), q(4, 5), s(0))))),
        (Q(1, 3), tuple(sorted((p(1), q(0, 3), q(4, 5), s(2))))),
        (Q(1, 3), tuple(sorted((p(2), q(1, 3), q(4, 5), s(0))))),
        (Q(-1, 3), tuple(sorted((p(2), q(0, 1), q(4, 5), s(3))))),
    )


def audit_logarithmic_reset_obstruction(classification):
    _target, response_terms = classification.source_monomials()
    response_terms = tuple(response_terms)
    variables = tuple(sorted(
        {variable for monomial in response_terms for variable in monomial},
        key=repr,
    ))
    require(len(response_terms) == 105 and len(variables) == 28,
            (len(response_terms), len(variables)))
    incidence = tuple(tuple(Q(variable in monomial)
                            for monomial in response_terms)
                      for variable in variables)
    l01 = scalar_vector(classification, response_terms)
    complete = (Q(1),) * len(response_terms)
    require(rank(incidence) == 21
            and rank(incidence + (complete,)) == 21
            and rank(incidence + (l01,)) == 22,
            "the fixed-chart logarithmic obstruction rank changed")

    term_index = {monomial: index
                  for index, monomial in enumerate(response_terms)}
    dual = [Q(0)] * len(response_terms)
    records = literal_dual_records(classification)
    for coefficient, monomial in records:
        require(monomial in term_index,
                ("a dual occurrence left the response", monomial))
        dual[term_index[monomial]] = coefficient
    dual = tuple(dual)
    require(sum(value != 0 for value in dual) == 12
            and all(dot(dual, row) == 0 for row in incidence)
            and dot(dual, complete) == 0
            and dot(dual, l01) == 1,
            "the primitive 12-occurrence reset dual changed")

    # Three local direction coordinates A,B,C.  Raw chart folding adds
    # B-A and C-A, reducing the response quotient from dimension two to zero.
    # The graph cone instead keeps u1,u2 and the relations B-A-u1,
    # C-A-u2; it retains dimension two and identifies v=2A-B-C=-u1-u2.
    response_row = (Q(1), Q(1), Q(1))
    raw_ab = (Q(-1), Q(1), Q(0))
    raw_ac = (Q(-1), Q(0), Q(1))
    graph_rows = (
        (Q(1), Q(1), Q(1), Q(0), Q(0)),
        (Q(-1), Q(1), Q(0), Q(-1), Q(0)),
        (Q(-1), Q(0), Q(1), Q(0), Q(-1)),
    )
    require(3 - rank((response_row,)) == 2
            and 3 - rank((response_row, raw_ab, raw_ac)) == 0
            and 5 - rank(graph_rows) == 2,
            "the pointed graph-cone dimension changed")
    v = (Q(2), Q(-1), Q(-1), Q(0), Q(0))
    u = (Q(0), Q(0), Q(0), Q(1), Q(1))
    require(tuple(v[index] + u[index] for index in range(5))
            == tuple(-graph_rows[1][index] - graph_rows[2][index]
                     for index in range(5)),
            "the v=-(u1+u2) graph identity changed")

    return {
        "complete_response_occurrences": len(response_terms),
        "physical_coefficient_variables": len(variables),
        "constant_logarithmic_Euler_rank": rank(incidence),
        "rank_after_complete_response_row": rank(incidence + (complete,)),
        "rank_after_L01": rank(incidence + (l01,)),
        "L01_in_logarithmic_Euler_plus_response_span": False,
        "primitive_dual": {
            "support": len(records),
            "coefficients": [str(coefficient)
                             for coefficient, _monomial in records],
            "literal_occurrences": [repr(monomial)
                                    for _coefficient, monomial in records],
            "kills_every_coordinate_Euler_row": True,
            "kills_complete_response_row": True,
            "reads_L01": "1",
            "occurrence_augmentation": "0",
        },
        "source_validity_consequence": (
            "no constant logarithmic coordinate Euler correction, including "
            "every site/type Euler specialization, cancels the L01 proper "
            "face while retaining its H2 symbol in the fixed chart"
        ),
        "presentation_safe_graph_cone": {
            "relations": ["B-A-u1", "C-A-u2"],
            "response_quotient_dimension": 2,
            "raw_folded_quotient_dimension": 0,
            "graph_cone_quotient_dimension": 2,
            "retained_scalar": "L01=-(u1+u2)*H2345",
            "fixed_fibre_warning": (
                "setting u1=u2=0 imposes A=B=C and is exactly the invalid "
                "raw chart fold; the graph cone organizes but does not "
                "construct a physical reset"
            ),
        },
    }


def audit_scalar_and_target(scalar_gate):
    ledger, digest = scalar_gate.audit()
    require(digest == scalar_gate.EXPECTED_LEDGER_SHA256,
            "the L01 scalar theorem changed")
    literal = ledger["literal_product_rule"]
    require(literal["target_augmentation"] == "0"
            and literal["response_row_countermodel"]["response_value"] == "0"
            and literal["response_row_countermodel"]["scalar_face_value"] == "3",
            "the L01 scalar/target counterguard changed")
    return {
        "target_augmentation": 0,
        "pointed_scalar_counterguard": literal["response_row_countermodel"],
        "distinction": (
            "target-zero is not pointed-scalar-zero: at the displayed "
            "response-row point R=0 but L01=3.  A source-valid graph reset "
            "must retain a scalar coordinate u01 with u01(x)=L01(x), rather "
            "than declaring its value zero"
        ),
    }


def audit_augmented_fork(terminal):
    ledger, digest = terminal.audit()
    require(digest == terminal.EXPECTED_LEDGER_SHA256,
            "the augmented cap/Cartan theorem changed")
    extension = ledger["explicit_local_dual_extension"]
    fork = ledger["post_placement_dichotomy"]
    require(extension["extension_formula"] == {
        "q": 0, "ainc": 0, "Eq_j": 0,
        "target_j": "-mu_j", "W_j": "-mu_j",
        "ores_j": "mu_j", "ridge": "-sum alpha_j mu_j",
    } and fork["third_branch"] is False,
            ("the augmented reset landing changed", extension, fork))
    return {
        "required_physical_reset_output": (
            "one source column whose local face is L01 in the same literal "
            "word/fine/repeated/H2 direction grade and whose q, ainc, target, "
            "Eq and shifted-ridge faces are protected zero (with every other "
            "declared augmented face retained)"
        ),
        "coefficient_rows_do_not_type": [
            "physical q", "ainc/anchor", "Eq", "shifted ridge", "W",
            "ordinary residue", "eta/sigma",
        ],
        "after_same_grade_placement": fork["exact_alternative"],
        "terminal_dual_extension": extension["extension_formula"],
        "interpretation": (
            "q and anchor need no dual correction; target/W/ordinary residue "
            "cancel the cap rows and ridge cancels the Cartan remainder.  "
            "This proves exhaustivity after placement, not placement itself"
        ),
    }


def audit():
    pin_dependencies()
    classification = load(
        "computations/verify_h3_active_coloop_redistribution_second_hasse_face_classification.py",
        "fixed_chart_l01_classification",
    )
    scalar_gate = load(
        "computations/verify_h3_h2_c4_trivial_tag_euler_scalar_face_gate.py",
        "fixed_chart_l01_scalar",
    )
    terminal = load(
        "computations/verify_h3_o2_augmented_terminal_cap_cartan_extension_gate.py",
        "fixed_chart_l01_terminal",
    )
    ledger = {
        "theorem": "h3 H2 fixed-chart L01 reset/augmented obstruction",
        "pins": PINS,
        "logarithmic_reset_obstruction":
            audit_logarithmic_reset_obstruction(classification),
        "scalar_target_typing": audit_scalar_and_target(scalar_gate),
        "augmented_q_anchor_ridge_fork": audit_augmented_fork(terminal),
        "exact_frontier": (
            "construct the fixed-chart source-labelled graph/reset column "
            "with first proper face L01 and protected augmented rows, or "
            "place L01 in the exhaustive same-grade physical map and apply "
            "the pinned filler/terminal alternative.  Full-site covariance "
            "and every constant logarithmic Euler correction are exhausted"
        ),
        "scope": (
            "exact uncoloured canonical h=3 K8 response algebra and exact "
            "conditional augmented promotion.  The 12-occurrence covector "
            "is not called a physical terminal before same-grade q/anchor/"
            "ridge placement, and non-diagonal higher Spencer corrections "
            "outside the tested logarithmic/source-row span are not excluded"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("fixed-chart L01 reset ledger changed", digest,
                 EXPECTED_LEDGER_SHA256))
    print("fixed-chart logarithmic reset: OBSTRUCTED (rank 21 -> 22)")
    print("primitive L01 covector: 12 literal occurrences, augmentation zero")
    print("target zero but pointed scalar may be 3")
    print("after same-grade q/anchor/ridge placement: FILLER OR TERMINAL")
    print("ledger_sha256=" + digest)
    return ledger


if __name__ == "__main__":
    audit()
