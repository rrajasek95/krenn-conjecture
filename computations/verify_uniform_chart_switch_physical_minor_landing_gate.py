#!/usr/bin/env python3
"""Test the relative switch carriers in the physical response algebra.

For one h=3 lower packet write its fixed term F and the two four-cycle
companions C1,C2.  The complete response/target coefficient is

    H=F+C1+C2,

while the physical switch carriers are the matching-exchange binomials

    t1=C1-F,  t2=C2-F.

The change of coordinates (F,C1,C2) -> (H,t1,t2) has determinant 3.
Therefore over the characteristic-zero theorem field, t1,t2 are coordinates
on the conditional lower zero fibre H=0: every nonzero complete lower packet
is switch-bright.  Conversely, H=t1=t2=0 forces all three terms to vanish.

Each t is a literal quadratic binomial in the underlying edge/endpoint
cells, but it is not a physical Plucker/Segre relation.  In the C4 packet it
would impose a decomposability relation on arbitrary q cells; in C2+ it
mixes Dq with ps; in P2 it mixes sq terms from different sites.  Explicit
physical assignments make H=0 and t nonzero in all three types.  The complete
GHZ row thus detects/reduces the carrier but does not nullhomotope it.

Uniformly, if all switch contrasts are dark, every companion equals its
canonical parent and P=(2h-3)F.  If the complete lower packet P is supplied
as a source-valid zero row in that exact word/head/fine/repeated grade, this
reduces to F=0 and is a well-founded response-order descent.  The parent
GHZ value equation alone does not make an arbitrary Hasse coefficient P
zero.  A bright contrast enters the pinned C2+/C4/P2 carrier alternative.
This is a positive coefficient landing, not yet an augmented physical source
boundary or terminal.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_chart_cross_companion_relative_switch_dga_gate.py":
        "e0a8251128174d50b450b3bf85ce0a6870af00d4ab5565e7849fc3c8644c31c6",
    "notes/uniform-chart-cross-companion-relative-switch-dga-gate.md":
        "2b9fbe0c648cadc5913e57e4b6d678205c7f7fbc66f57e58e371f9ad10ef2cb8",
    "computations/verify_h3_universal_occurrence_shear_physical_toric_lift_gate.py":
        "ca5ede5e7a2cc11bf9f62bdcca8349813c3585b401ea614b8622fa40e63c7609",
    "notes/h3-universal-occurrence-shear-physical-toric-lift-gate.md":
        "9764018dcccd47e774c285c4bff51ca095fa219e879c8d4a2a7cd51394da5d7e",
    "computations/verify_h3_pure_trapped_h2_c2_c4_p2_descent_reduction.py":
        "026eb42fac96e2c21e6466f51322a18d45d975bcf5f48e0dc33f9cfa740d8d41",
    "notes/h3-pure-trapped-h2-c2-c4-p2-descent-reduction.md":
        "699a9debf8de2646249f949e80312baa58251a1f36639bed249d40e2dc74b2ea",
}
EXPECTED_LEDGER_SHA256 = (
    "ce836892431a8a06b2f2056c5dcfd0652df424fb238263017ceb28c000e47304"
)

Monomial = tuple[str, ...]
Polynomial = dict[Monomial, Q]


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


def rank(rows: tuple[tuple[Q, ...], ...]) -> int:
    work = [list(map(Q, row)) for row in rows]
    if not work:
        return 0
    answer = 0
    width = len(work[0])
    require(all(len(row) == width for row in work), "rank width")
    for column in range(width):
        pivot = next((row for row in range(answer, len(work))
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[answer], work[pivot] = work[pivot], work[answer]
        value = work[answer][column]
        work[answer] = [entry / value for entry in work[answer]]
        for row in range(len(work)):
            if row == answer or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[answer], strict=True)]
        answer += 1
    return answer


def determinant3(matrix: tuple[tuple[Q, ...], ...]) -> Q:
    a, b, c = matrix
    return (a[0] * (b[1] * c[2] - b[2] * c[1])
            - a[1] * (b[0] * c[2] - b[2] * c[0])
            + a[2] * (b[0] * c[1] - b[1] * c[0]))


def monomial(*factors: str) -> Monomial:
    return tuple(sorted(factors))


def add(*polynomials: Polynomial) -> Polynomial:
    answer: dict[Monomial, Q] = {}
    for polynomial in polynomials:
        for term, value in polynomial.items():
            answer[term] = answer.get(term, Q(0)) + value
    return {term: value for term, value in answer.items() if value}


def scale(value: int | Q, polynomial: Polynomial) -> Polynomial:
    return {term: Q(value) * coefficient
            for term, coefficient in polynomial.items()
            if Q(value) * coefficient}


def evaluate(polynomial: Polynomial, values: dict[str, Q | int]) -> Q:
    return sum((coefficient
                * Q(1 if not term else 1)
                * product(Q(values.get(factor, 0)) for factor in term)
                for term, coefficient in polynomial.items()), Q(0))


def product(values) -> Q:
    answer = Q(1)
    for value in values:
        answer *= Q(value)
    return answer


def packet_data() -> dict[str, tuple[tuple[Polynomial, Polynomial, Polynomial],
                                     dict[str, int]]]:
    return {
        "C4": (
            (
                {monomial("q01", "q23"): Q(1)},
                {monomial("q02", "q13"): Q(1)},
                {monomial("q03", "q12"): Q(1)},
            ),
            {
                "q01": 1, "q23": 1,
                "q02": -1, "q13": 1,
                "q03": 0, "q12": 1,
            },
        ),
        "C2plus": (
            (
                {monomial("D", "q23"): Q(1)},
                {monomial("p2", "s3"): Q(1)},
                {monomial("p3", "s2"): Q(1)},
            ),
            {
                "D": 1, "q23": 1,
                "p2": -1, "s3": 1,
                "p3": 0, "s2": 1,
            },
        ),
        "P2": (
            (
                {monomial("s1", "q23"): Q(1)},
                {monomial("s2", "q13"): Q(1)},
                {monomial("s3", "q12"): Q(1)},
            ),
            {
                "s1": 1, "q23": 1,
                "s2": -1, "q13": 1,
                "s3": 0, "q12": 1,
            },
        ),
    }


def local_packet_audit() -> dict[str, object]:
    # Rows of the coordinate change (F,C1,C2) -> (H,t1,t2).
    transform = (
        tuple(map(Q, (1, 1, 1))),
        tuple(map(Q, (-1, 1, 0))),
        tuple(map(Q, (-1, 0, 1))),
    )
    require(determinant3(transform) == 3 and rank(transform) == 3,
            (determinant3(transform), rank(transform)))
    even_dual = tuple(map(Q, (2, -1, -1)))
    odd_dual = tuple(map(Q, (0, 1, -1)))
    complete = transform[0]
    require(sum(a * b for a, b in zip(even_dual, complete, strict=True)) == 0
            and sum(a * b for a, b in
                    zip(odd_dual, complete, strict=True)) == 0
            and rank((complete, even_dual, odd_dual)) == 3,
            "the even/odd quotient basis changed")

    records = {}
    for name, (terms, assignment) in packet_data().items():
        f, c1, c2 = terms
        h_row = add(f, c1, c2)
        t1 = add(c1, scale(-1, f))
        t2 = add(c2, scale(-1, f))
        t_even = add(t1, t2)
        t_odd = add(t1, scale(-1, t2))
        require(len(set(f).intersection(c1)) == 0
                and len(set(f).intersection(c2)) == 0,
                (name, f, c1, c2))
        values = tuple(evaluate(term, assignment) for term in terms)
        readouts = (
            evaluate(h_row, assignment),
            evaluate(t1, assignment),
            evaluate(t2, assignment),
        )
        require(values == (Q(1), Q(-1), Q(0))
                and readouts == (Q(0), Q(-2), Q(-1)),
                (name, values, readouts))
        require(evaluate(t_even, assignment) == -3
                and evaluate(t_odd, assignment) == -1,
                (name, evaluate(t_even, assignment),
                 evaluate(t_odd, assignment)))

        # Distinct monomials make both exchange binomials nonzero physical
        # polynomials.  A literal toric identity would have identical factor
        # multisets on its two sides, as in the pinned occurrence-minor gate.
        require(t1 and t2 and len(t1) == len(t2) == 2,
                (name, t1, t2))
        records[name] = {
            "F": [list(term) for term in f],
            "C1": [list(term) for term in c1],
            "C2": [list(term) for term in c2],
            "complete_row": "H=F+C1+C2",
            "switch_carriers": ["t1=C1-F", "t2=C2-F"],
            "physical_zero_row_counterguard": {
                "term_values_F_C1_C2": [str(value) for value in values],
                "H": str(readouts[0]),
                "t1": str(readouts[1]),
                "t2": str(readouts[2]),
            },
            "exchange_binomial_is_literal_polynomial": True,
            "exchange_binomial_is_identity": False,
        }

    return {
        "coordinate_transform": [
            [str(value) for value in row] for row in transform
        ],
        "determinant": str(determinant3(transform)),
        "characteristic_zero_inverse": (
            "F=(H-t1-t2)/3, C1=(H+2t1-t2)/3, "
            "C2=(H-t1+2t2)/3"
        ),
        "on_H_zero": {
            "t1_t2_are_coordinates": True,
            "t1=t2=0": "F=C1=C2=0",
            "T=t1+t2": "-3F",
        },
        "complete_row_annihilator": {
            "endpoint_even": [2, -1, -1],
            "endpoint_odd": [0, 1, -1],
            "rank": 2,
        },
        "literal_packet_guards": records,
    }


def pinned_and_uniform_audit() -> dict[str, object]:
    switch = load(
        "computations/verify_uniform_chart_cross_companion_relative_switch_dga_gate.py",
        "physical_minor_switch_pin",
    )
    switch_ledger, switch_digest = switch.audit()
    require(switch_digest == switch.EXPECTED_LEDGER_SHA256,
            switch_digest)

    toric = load(
        "computations/verify_h3_universal_occurrence_shear_physical_toric_lift_gate.py",
        "physical_minor_toric_pin",
    )
    toric_ledger, toric_digest = toric.audit()
    require(toric_digest == toric.EXPECTED_LEDGER_SHA256,
            toric_digest)
    toric_gate = toric_ledger["physical_toric_conormal"]
    require(toric_gate["strict_physical_p_s_q_lift"] is False
            and toric_gate["literal_relation"]
                == "u_Ay*u_Bx-u_Ax*u_By=0",
            toric_gate)

    lower = load(
        "computations/verify_h3_pure_trapped_h2_c2_c4_p2_descent_reduction.py",
        "physical_minor_lower_pin",
    )
    lower_ledger, lower_digest = lower.audit()
    require(lower_digest == lower.EXPECTED_LEDGER_SHA256
            and lower_ledger["input"]
                ["pure_trapped_types"] == ["C2plus", "C4", "P2"],
            lower_ledger)

    reductions = []
    for order in switch_ledger["orders_exhaustively_audited"]:
        h = order["h"]
        fixed = order["fixed_chart_occurrences"]
        companions = order["cross_chart_companions"]
        degree = order["companions_per_fixed_parent"]
        parent_values = tuple(Q(index + 1) for index in range(fixed))
        fixed_sum = sum(parent_values, Q(0))
        # Switch-dark means every child equals its parent.
        full_sum = sum((Q(degree + 1) * value for value in parent_values),
                       Q(0))
        require(companions == degree * fixed
                and full_sum == Q(2 * h - 3) * fixed_sum,
                (h, fixed, companions, degree, full_sum, fixed_sum))
        reductions.append({
            "h": h,
            "switch_dark_identity": f"P={2 * h - 3}F",
            "consequence_on_P_zero": "F=0 in characteristic zero",
            "fixed_packet_order": h - 2,
            "if_fixed_edge_zero": "the entire switch-dark packet is zero",
            "otherwise": "the lower hafnian/response coefficient is zero",
            "physical_hypothesis": (
                "P=0 is an admitted source-valid complete lower row in the "
                "same word/head/fine/repeated grade"
            ),
        })
    return {
        "switch_DGA_ledger": switch_digest,
        "physical_toric_lift_ledger": toric_digest,
        "lower_packet_descent_ledger": lower_digest,
        "toric_relation_kind": (
            "quadratic in occurrence coordinates with identical physical "
            "factor multiset on both sides"
        ),
        "switch_relation_kind": (
            "linear in occurrence coordinates / quadratic in edge cells, "
            "with distinct physical factor multisets"
        ),
        "same_physical_relation": False,
        "uniform_switch_dark_reductions": reductions,
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "uniform chart switch physical minor landing gate",
        "pins": PINS,
        "h3_literal_physical_packets": local_packet_audit(),
        "pinned_and_uniform_scope": pinned_and_uniform_audit(),
        "verdict": (
            "The relative switch variables have a canonical physical value "
            "t_c=u_c-u_parent, a matching-exchange binomial.  This is not a "
            "vanishing Plucker/Segre relation and the complete GHZ row does "
            "not make it a boundary.  At h=3 the invertible transform "
            "(F,C1,C2)<->(H,t1,t2) proves the conditional positive alternative: "
            "on a source-valid complete lower zero row, every nonzero "
            "C2plus/C4/P2 packet is switch-bright.  The "
            "displayed physical assignments realize H=0 with nonzero t in "
            "all three packet types.  Uniformly, switch-darkness gives "
            "P=(2h-3)F.  It strictly lowers response order only after P=0 "
            "has been constructed as an exact source row in that grade."
        ),
        "physical_landing_alternative": {
            "switch_bright": (
                "a literal occurrence-asymmetric carrier enters the pinned "
                "Cplus/P2 or relative-C4 landing problem, with its retained labels"
            ),
            "switch_dark": (
                "conditional on a source-valid P=0 row, reduce to the lower "
                "fixed packet; otherwise retain P as the restriction/algebraization gate"
            ),
            "accepted_augmented_terminal": False,
        },
        "first_literal_guard": (
            "the rank-two quotient of the three term packet by H, with even "
            "dual (2,-1,-1) and odd dual (0,1,-1).  It is a complete local "
            "coefficient guard, not a full unary/anchor/q/ridge source point"
        ),
        "physical_zero_row_scope": {
            "parent_GHZ_value_equation_implies_arbitrary_Hasse_P_zero": False,
            "needed_row": (
                "complete lower response/target coefficient P in the actual "
                "word, endpoint head, fine and repeated grade"
            ),
            "target_normalization": (
                "in a mixed response word its GHZ target value is zero; in a "
                "pure target word retain the normalized target coordinate, "
                "so descent is affine unless that target is separately cancelled"
            ),
            "all_t_dark_across_words_suffices_without_rows": False,
            "all_t_dark_plus_complete_lower_rows": (
                "wordwise/headwise strict order descent, compatible with common-edge PP recursion"
            ),
            "unary_rows": (
                "do not follow from the coefficient identity; their product-"
                "rule/reinsertion faces must be transported by the same source map"
            ),
        },
        "shortest_positive_theorem": (
            "land one switch-bright physical binomial in the augmented "
            "Cplus/P2 or same-grade relative-C4 source map.  No extra Segre "
            "identity is available; if every binomial is dark, construct the "
            "complete lower zero row and then use the conditional order descent"
        ),
        "scope": (
            "exact h3 physical coefficient polynomials and uniform matching "
            "recursion; no physical nullhomotopy or terminal promotion"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    require(EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN",
            ("freeze EXPECTED_LEDGER_SHA256", digest))
    print("physical t_c=u_c-u_parent: LITERAL MATCHING-EXCHANGE BINOMIAL")
    print("t_c is a vanishing Plucker/Segre relation: NO")
    print("h3 H=0: nonzero packet implies switch-bright")
    print("all-h switch-dark: P=(2h-3)F")
    print("strict physical descent: CONDITIONAL ON SAME-GRADE LOWER ZERO ROW")
    print("augmented Cplus/P2 or relative-C4 landing: STILL REQUIRED")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
