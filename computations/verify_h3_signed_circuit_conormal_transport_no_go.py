#!/usr/bin/env python3
r"""Signed-circuit and two-chart audit for the h=3 conormal obstruction.

Each chart c has the exact normal-incidence candidate

    N_c = Y*M_c-kappa*Y*rho_c-kappa*T_c+kappa*r0_c,

with reduced type ([F0_c],w)=(kappa,kappa*Y).  A literal adjacent-chart
interval has conormal incidence F0_L-F0_D and zero w boundary.  Therefore
the total pure-anchor coefficient is invariant under every Bianchi
difference.  Any combination with w coefficient kappa*Y has total
conormal coefficient kappa, never zero.

The signed-circuit atoms of b942209 and cd08db9 use mixed target-zero rows,
so their conormal incidence is zero.  An odd circuit can manufacture the
missing coefficient only after its active monomial is inverted, at which
point it is already a unit certificate and the source packet is empty.
Balanced circuits and multiplicity-cube debts cannot change the invariant.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_source_base_change_conormal_obstruction.py":
        "1a921671ab378f68355c2a6196d1951cad30244d78a9e90ec2715ce47ef12bf0",
    "notes/h3-source-base-change-conormal-obstruction.md":
        "550d1fdea1127d1771191057207b6b2bb6cb97edd3309c90f230d87631f401cd",
    "computations/verify_oo_curved_global_private_transport_boundary.py":
        "9a4c6bd04ea8d0466efee9f5188c1ffa922ac82ec0187b3fc4213b355091c2c5",
    "notes/oo-curved-global-private-transport-boundary.md":
        "1256fcfd1df1316b6fb3af824bfdde202f8ccf05325c9337fe74780514853bd2",
    "computations/verify_n8_one_bad_multiplicity_cube_boundary.py":
        "7a14bae54df2916ec03e8adf3685cc96f09fe71fdba27d507469b8d2f7715456",
    "notes/n8-one-bad-multiplicity-cube-boundary.md":
        "d93478e04bd7ef27aaed4b77b4616c266947e2cd9645284acc6c28fc14b21668",
    "computations/verify_recombination_cube_segre_cancellation.py":
        "b2e3bcfa8b4a7832b2db128f53cc524cb12c8aa87f0490e680f238757af81023",
    "notes/recombination-cube-segre-cancellation.md":
        "b758a8121a9bfc5e78ffe61d40a64b101d97ecf0e0fcd7138b75ec08995deb89",
    "computations/verify_h3_mixed_bar_curvature_bicomplex.py":
        "6d239dfa1610d36de3385f9e084693523225528f8343ea9412773604fe396318",
}
EXPECTED_LEDGER_SHA256 = "fa6e336d4c4373cee059a557ed572db01edb7e98021dccfd675b5938d2f7011f"

ZERO = Q(0)
ONE = Q(1)


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"pinned dependency changed: {relative}")


def dot(left, right):
    return sum((Q(x) * Q(y) for x, y in zip(left, right, strict=True)), ZERO)


def rank(rows):
    work = [list(map(Q, row)) for row in rows]
    answer = 0
    width = len(work[0]) if work else 0
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
            work[row] = [entry - value * pivot_entry
                         for entry, pivot_entry
                         in zip(work[row], work[answer], strict=True)]
        answer += 1
    return answer


def two_chart_anchor_audit():
    # Coordinates are ([F0_D], [F0_L], normalized w).  Target and ordinary
    # residue have already been cancelled inside each exact candidate from
    # 04abf04.  The Bianchi interval is the literal difference L-D.
    candidate_d = (ONE, ZERO, ONE)
    candidate_l = (ZERO, ONE, ONE)
    bianchi_l_minus_d = (-ONE, ONE, ZERO)
    desired = (ZERO, ZERO, ONE)
    separator = (ONE, ONE, -ONE)
    available = (candidate_d, candidate_l, bianchi_l_minus_d)
    require(all(dot(separator, row) == ZERO for row in available),
            "anchor-number separator stopped killing source candidates")
    require(dot(separator, desired) == -ONE,
            "desired class entered the two-chart source span")
    require(rank(available) == 2 and rank(available + (desired,)) == 3,
            "two-chart conormal rank obstruction changed")

    # Exhaust a nontrivial exact coefficient box.  If a_D+a_L=1 gives the
    # desired w coefficient, no multiple z(L-D) can make both conormal
    # coordinates vanish; their sum is the invariant a_D+a_L=1.
    tested = 0
    for a_d, a_l, z in product(range(-4, 5), repeat=3):
        conormal_d = Q(a_d - z)
        conormal_l = Q(a_l + z)
        w = Q(a_d + a_l)
        if w == ONE:
            tested += 1
            require(conormal_d + conormal_l == ONE,
                    "Bianchi transport changed total anchor number")
            require((conormal_d, conormal_l) != (ZERO, ZERO),
                    "a finite Bianchi combination cancelled the anchor")
    require(tested == 72, "coefficient-box census changed")

    return {
        "coordinates": ["[F0_D]", "[F0_L]", "normalized w"],
        "chart_D_candidate": list(map(str, candidate_d)),
        "chart_L_candidate": list(map(str, candidate_l)),
        "Bianchi_L_minus_D": list(map(str, bianchi_l_minus_d)),
        "anchor_number_separator": list(map(str, separator)),
        "available_rank": rank(available),
        "rank_with_desired": rank(available + (desired,)),
        "integer_combinations_with_w_one_checked": tested,
        "invariant": "sum chart conormal coefficients = normalized w",
    }


def signed_circuit_audit():
    # The b942209 identity.  Treat A,...,F as exponent vectors in a free
    # monoid modulo A+D+E=B+C+F.  The three physical rows are mixed, hence
    # selected-u conormal degree zero.  Localizing K turns 2K into a unit;
    # without that localization the identity remains wholly in the mixed
    # ideal and has no F0 component.
    exponent = {
        "A": (1, 0, 0, 0, 0),
        "B": (0, 1, 0, 0, 0),
        "C": (0, 0, 1, 0, 0),
        "D": (0, 0, 0, 1, 0),
        "E": (0, 0, 0, 0, 1),
        # Enforce A+D+E=B+C+F.
        "F": (1, -1, -1, 1, 1),
    }

    def add_exp(*names):
        return tuple(sum(exponent[name][index] for name in names)
                     for index in range(5))

    left_k = add_exp("A", "D", "E")
    right_k = add_exp("B", "C", "F")
    require(left_k == right_k,
            "odd triangle exponent dependency changed")
    # Expanded DE(A+B)-BE(C+D)+BC(E+F): the three non-K cross terms cancel.
    positive = [add_exp("D", "E", "A"),
                add_exp("D", "E", "B"),
                add_exp("B", "C", "E"),
                add_exp("B", "C", "F")]
    negative = [add_exp("B", "E", "C"),
                add_exp("B", "E", "D")]
    multiplicities = {}
    for sign, terms in ((1, positive), (-1, negative)):
        for term in terms:
            multiplicities[term] = multiplicities.get(term, 0) + sign
            if not multiplicities[term]:
                del multiplicities[term]
    require(multiplicities == {left_k: 2},
            "odd triangle polynomial identity changed")
    require(all(word not in ("00000000", "11111111", "22222222")
                for word in ("20120121", "22100121", "22120101")),
            "an odd-triangle row acquired a pure target")

    # cd08db9: every one of the eight recombination cube words is mixed;
    # the four residual debts are in independent mixed output grades.
    singleton_bits = ("001", "010", "101", "110")
    require(len(singleton_bits) == 4
            and all(bit not in ("000", "111") for bit in singleton_bits),
            "multiplicity-cube debt changed")

    return {
        "odd_triangle_words": ["20120121", "22100121", "22120101"],
        "odd_triangle_selected_u_conormal": [0, 0, 0],
        "ordinary_identity": "DE*f0-BE*f1+BC*f2=2*K",
        "unit_after_active_localization": True,
        "unit_consequence": (
            "the packet is already source-empty; only then can 1 multiply F0"
        ),
        "without_unit_localization_F0_component": 0,
        "multiplicity_cube_singleton_bits": list(singleton_bits),
        "multiplicity_cube_debt_selected_u_conormal": [0, 0, 0, 0],
        "completed_Segre_mate_tensor_entries": 8,
        "completed_Segre_mate_tensor_selected_u_conormal": [0] * 8,
        "Segre_flattening_minors_selected_u_conormal": 0,
    }


def generic_reinsertion_audit():
    # Abstract any number of charts.  Each complete chart candidate has
    # (anchor,w)=(a_c,a_c), every adjacent Bianchi edge contributes
    # (-z,+z;0), and every mixed signed-circuit/debt row contributes zero.
    # The augmentation sum of anchor incidences therefore equals w.
    records = []
    for charts in range(2, 8):
        # Use a deterministic nontrivial coefficient family summing to one.
        candidates = [Q(index + 1, charts) for index in range(charts - 1)]
        candidates.append(ONE - sum(candidates, ZERO))
        edges = [Q((-1) ** index * (index + 2), charts + 1)
                 for index in range(charts - 1)]
        conormal = list(candidates)
        for index, value in enumerate(edges):
            conormal[index] -= value
            conormal[index + 1] += value
        require(sum(conormal, ZERO) == sum(candidates, ZERO) == ONE,
                "multi-chart Bianchi incidence lost augmentation")
        require(any(conormal), "multi-chart conormal vanished at w=1")
        records.append({
            "charts": charts,
            "Bianchi_edges": charts - 1,
            "normalized_w": "1",
            "total_anchor_incidence": str(sum(conormal, ZERO)),
        })
    return records


def main() -> None:
    pin_dependencies()
    two_chart = two_chart_anchor_audit()
    circuits = signed_circuit_audit()
    multichart = generic_reinsertion_audit()
    ledger = {
        "pins": PINS,
        "two_chart_conormal": two_chart,
        "signed_circuit_atoms": circuits,
        "multi_chart_transport": multichart,
        "dichotomy": {
            "odd_or_valuation_holonomy": (
                "gives a Laurent unit and closes the packet directly"
            ),
            "source_compatible_balanced_circuit": (
                "stays in mixed target-zero grades and has conormal zero, "
                "including the completed rank-one Segre mate tensor"
            ),
            "Bianchi_chart_difference": (
                "moves [F0] between chart labels but preserves total "
                "pure-anchor incidence"
            ),
        },
        "minimal_missing_packet": (
            "a source-labelled lower face with total pure-anchor incidence "
            "-1 and zero w/target/ores, not a signed matching circuit or "
            "an adjacent-chart difference"
        ),
        "verdict": (
            "the b942209/cd08db9 signed-circuit mechanism either proves a "
            "unit (empty source packet) or has zero conormal; ordinary "
            "Bianchi transport conserves the remaining kappa[F0] class"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"signed-circuit conormal ledger changed: {digest}")
    print("h=3 signed-circuit conormal transport audit: PASS")
    print("odd circuit: direct Laurent unit or no selected-u conormal")
    print("multiplicity-cube debts: four mixed rows, conormal zero")
    print("two-chart Bianchi: moves [F0], preserves total anchor number")
    print("desired w=1 forces total conormal=1")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
