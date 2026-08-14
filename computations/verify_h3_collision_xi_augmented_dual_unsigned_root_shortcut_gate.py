#!/usr/bin/env python3
"""Extend the collision dual and audit the unsigned-root shortcut.

There are two complementary calculations.

1.  The parent-labelled Xi_01/30 dual extends over the strongest
    presentation-safe top and first-PP relative graphs.  Before a physical
    PP-to-cap word/fine/repeated bridge is supplied, every cap value is zero,
    and therefore target, Eq, q, anchor, ores, W and ridge are all zero.  A
    first positive bridge to cap corner B0 raises rank by one.  The dual
    extends uniquely over the known cap/Cartan packet with

      B0=1/30, target0=W0=-1/30, ores0=ridge=1/30,

    and Eq=q=anchor=0.  In general the formula is

      target_j=W_j=-mu_j, ores_j=mu_j,
      ridge=-sum_j alpha_j mu_j, Eq=q=anchor=0.

2.  A complete unsigned vertex root 0->S has symmetric 45-term first
    derivative, so granting the symmetric collision cell bypasses Xi.  The
    opposite-root composition on the complete response is not one fixed
    A+B family: it is exactly twice the sum of all 90 matchings not using
    edge 0S.  Likewise the second root gives twice the 90-match aggregate
    avoiding 1S.  The desired fixed-window A+B and A+C packets each raise
    rank independently.  Thus the shortcut moves the first obstruction from
    collision-standard degree to a squarefree occurrence projector; it does
    not remove the source-labelled placement problem.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "notes/h3-fullword-collision-sector-parent-inventory-gate.md":
        "04968b23ff618ad4262f6a40ebc5190bc4dd449930bc58c7fcb6beeee1795169",
    "notes/h3-collision-parent-split-relative-bar-terminal-gate.md":
        "292f3b50956e29fae3436489b7c566c8599e79498272f334c94c297d3752bbfe",
    "notes/h3-o2-augmented-terminal-cap-cartan-extension-gate.md":
        "e9c0cf3c76cbe4c8061574d2b977bf1189a1fa299ef17ae1d2e463c08a313429",
    "notes/h3-hyperbolic-collision-fixed-window-matching-routing-gate.md":
        "9ee72f85c69d08b8998f7061a52be2450a9f6e3bb843b8951777961471e16f2a",
    "notes/uniform-hyperbolic-collision-standard-representation-gate.md":
        "f926c48750c9788ced0308ce93b224c50b2cbe34fc23efdb7f958d915bb594fa",
    "notes/h3-fixed-window-centered-k22-physical-routing-gate.md":
        "73147addd04f69ea5a6a21e408dbd7030cd449f0cebbe46bb35caa2c32d6c189",
}
EXPECTED_LEDGER_SHA256 = (
    "2aebec770a0d1b394e56977b7097e2152dd34b3a1060a0b35ef13ce68ed79328"
)


P, S, ZERO, ONE, TWO, THREE, FOUR, FIVE = range(8)
VERTICES = tuple(range(8))
ALPHA = (Q(-1), Q(1), Q(1), Q(-1))


Edge = tuple[int, int]
Matching = tuple[Edge, ...]
Polynomial = Counter[Matching]


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def edge(left: int, right: int) -> Edge:
    require(left != right, ("loop", left))
    return (left, right) if left < right else (right, left)


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            yield tuple(sorted((edge(first, second),) + tail))


MATCHINGS = tuple(perfect_matchings(VERTICES))
RESPONSE = Counter({matching: Q(1) for matching in MATCHINGS})


def clean(polynomial: Polynomial) -> Polynomial:
    return Counter({key: value for key, value in polynomial.items() if value})


def add_polynomials(*polynomials: Polynomial) -> Polynomial:
    answer: Polynomial = Counter()
    for polynomial in polynomials:
        answer.update(polynomial)
    return clean(answer)


def scale_polynomial(coefficient: int | Q,
                     polynomial: Polynomial) -> Polynomial:
    return clean(Counter({key: Q(coefficient) * value
                          for key, value in polynomial.items()}))


def unsigned_root(polynomial: Polynomial, missing: int,
                  doubled: int) -> Polynomial:
    """The complete vertex transvection missing -> doubled, all plus signs."""
    answer: Polynomial = Counter()
    forbidden = edge(missing, doubled)
    for monomial, coefficient in polynomial.items():
        for position, source in enumerate(monomial):
            if missing not in source or source == forbidden:
                continue
            other = source[0] if source[1] == missing else source[1]
            target = edge(doubled, other)
            output = list(monomial)
            output[position] = target
            answer[tuple(sorted(output))] += coefficient
    return clean(answer)


def vector_on(order: tuple[Matching, ...], polynomial: Polynomial
              ) -> tuple[Q, ...]:
    return tuple(Q(polynomial[value]) for value in order)


def dot(left, right) -> Q:
    require(len(left) == len(right), "dot width")
    return sum((Q(a) * Q(b)
                for a, b in zip(left, right, strict=True)), Q(0))


def add(*vectors):
    require(vectors and len({len(vector) for vector in vectors}) == 1,
            "add width")
    return tuple(sum(entries, Q(0)) for entries in zip(*vectors, strict=True))


def scale(coefficient, vector):
    return tuple(Q(coefficient) * Q(value) for value in vector)


def rank(columns) -> int:
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank height")
    rows = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(height)]
    answer = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(answer, height)
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[answer], rows[pivot] = rows[pivot], rows[answer]
        value = rows[answer][column]
        rows[answer] = [entry / value for entry in rows[answer]]
        for row in range(height):
            if row == answer or not rows[row][column]:
                continue
            value = rows[row][column]
            rows[row] = [left - value * right for left, right in
                         zip(rows[row], rows[answer], strict=True)]
        answer += 1
    return answer


def augmented_relative_xi_audit() -> dict[str, object]:
    # Coordinate families: 90 collision parents c_i and retained top
    # carriers t_i; four first-PP face/carrier pairs for each of the 30
    # active root occurrences; then the literal known cap/Cartan block.
    labels = []
    labels.extend(f"c{i}" for i in range(90))
    labels.extend(f"t{i}" for i in range(90))
    labels.extend(f"f{i}:{face}" for i in range(30) for face in range(4))
    labels.extend(f"s{i}:{face}" for i in range(30) for face in range(4))
    labels.extend(f"B{j}" for j in range(4))
    labels.extend(f"Eq{j}" for j in range(4))
    labels.extend(("q", "ainc"))
    labels.extend(f"target{j}" for j in range(4))
    labels.extend(f"W{j}" for j in range(4))
    labels.extend(f"ores{j}" for j in range(4))
    labels.append("ridge")
    index = {label: position for position, label in enumerate(labels)}
    require(len(index) == len(labels) == 443, "augmented coordinate count")

    def vector(**entries) -> tuple[Q, ...]:
        unknown = set(entries) - set(index)
        require(not unknown, ("unknown coordinates", unknown))
        answer = [Q(0)] * len(labels)
        for label, value in entries.items():
            answer[index[label]] += Q(value)
        return tuple(answer)

    root_weights = (Q(1),) * 15 + (Q(-1),) * 15 + (Q(0),) * 60
    columns = []
    for occurrence in range(90):
        columns.append((
            f"top_graph:{occurrence}",
            vector(**{f"c{occurrence}": 1, f"t{occurrence}": -1}),
        ))
    for occurrence in range(30):
        for face in range(4):
            columns.append((
                f"PP_graph:{occurrence}:{face}",
                vector(**{f"f{occurrence}:{face}": 1,
                          f"s{occurrence}:{face}": -1}),
            ))
    columns.append((
        "parent_even_collision",
        vector(**{f"c{i}": 1 for i in range(90)}),
    ))

    # Known r0,T,rho,K cap/Cartan packet.
    for corner in range(4):
        columns.extend((
            (f"r0_{corner}", vector(**{
                f"B{corner}": 1, f"Eq{corner}": 1,
                f"target{corner}": 1, "ainc": -1,
            })),
            (f"T_{corner}", vector(**{
                f"W{corner}": -1, f"target{corner}": 1,
            })),
            (f"rho_{corner}", vector(**{
                f"W{corner}": 1, f"ores{corner}": 1,
            })),
        ))
    columns.append(("K", vector(**{
        **{f"ores{j}": ALPHA[j] for j in range(4)}, "ridge": 1,
    })))

    detector_entries = {}
    for occurrence, weight in enumerate(root_weights):
        detector_entries[f"c{occurrence}"] = weight / 30
        detector_entries[f"t{occurrence}"] = weight / 30
        if occurrence < 30:
            for face in range(4):
                detector_entries[f"f{occurrence}:{face}"] = weight / 30
                detector_entries[f"s{occurrence}:{face}"] = weight / 30
    detector_zero_cap = vector(**detector_entries)
    column_values = tuple(value for _name, value in columns)
    require(all(dot(detector_zero_cap, value) == 0
                for value in column_values),
            "Xi dual failed on the relative/known augmented block")
    xi_top = vector(**{f"c{i}": root_weights[i] for i in range(90)})
    xi_carrier = vector(**{f"t{i}": root_weights[i] for i in range(90)})
    require(dot(detector_zero_cap, xi_top) == 1
            and dot(detector_zero_cap, xi_carrier) == 1,
            "Xi normalization changed")

    base_rank = rank(column_values)
    require(base_rank == 224,
            ("relative plus cap rank changed", base_rank))

    # The first literal positive carrier has value 1/30.  A word/fine/
    # repeated PP-to-cap bridge to B0 is therefore detected by the zero-cap
    # extension and raises rank.  Once present, set mu_0=1/30 and use the
    # exact cap/Cartan formula; the resulting augmented dual kills it.
    bridge = vector(**{"s0:0": 1, "B0": -1})
    require(dot(detector_zero_cap, bridge) == Q(1, 30)
            and rank(column_values + (bridge,)) == base_rank + 1,
            "the first PP-to-cap bridge stopped raising rank")

    mu = (Q(1, 30), Q(0), Q(0), Q(0))
    extended_entries = dict(detector_entries)
    for corner in range(4):
        extended_entries[f"B{corner}"] = mu[corner]
        extended_entries[f"target{corner}"] = -mu[corner]
        extended_entries[f"W{corner}"] = -mu[corner]
        extended_entries[f"ores{corner}"] = mu[corner]
    extended_entries["ridge"] = -dot(ALPHA, mu)
    detector_after_bridge = vector(**extended_entries)
    require(all(dot(detector_after_bridge, value) == 0
                for value in column_values + (bridge,))
            and dot(detector_after_bridge, xi_top) == 1,
            "cap/Cartan extension did not absorb the first bridge")

    # An absolute landing of the entire retained Xi carrier is different:
    # it has value one and is exactly the class-killing arm.
    require(dot(detector_zero_cap, xi_carrier) == 1
            and rank(column_values + (xi_carrier,)) == base_rank + 1,
            "absolute Xi-carrier landing criterion changed")

    return {
        "coordinates": len(labels),
        "relative_columns": {
            "top_graphs": 90,
            "first_PP_graphs": 120,
            "parent_even_collision": 1,
            "known_cap_Cartan": 13,
            "rank": base_rank,
        },
        "Xi_dual_before_collection": "Xi_01/30",
        "forced_values_before_cross_grade_bridge": {
            "collision_and_top_carrier": "+/-1/30 on 15+15 occurrences",
            "each_of_four_PP_face_and_carrier_copies":
                "+/-1/30 on each active parent occurrence",
            "target": 0, "Eq": 0, "q": 0, "anchor_ainc": 0,
            "ores": 0, "W": 0, "ridge": 0,
        },
        "first_cross_grade_rank_raiser": {
            "type": (
                "source-labelled forward DSQ P3+K2 PP-to-AugP2/cap "
                "word/fine/repeated bridge"
            ),
            "sample_boundary": "s_(positive parent,face)-B0",
            "old_dual_value": "1/30",
            "rank_before_after": [base_rank, base_rank + 1],
        },
        "forced_values_after_sample_positive_bridge": {
            "mu": ["1/30", "0", "0", "0"],
            "target": ["-1/30", "0", "0", "0"],
            "Eq": ["0", "0", "0", "0"],
            "q": "0", "anchor_ainc": "0",
            "ores": ["1/30", "0", "0", "0"],
            "W": ["-1/30", "0", "0", "0"],
            "ridge": "1/30",
        },
        "general_cap_Cartan_extension": {
            "target_j": "-mu_j", "Eq_j": "0", "q": "0",
            "anchor_ainc": "0", "ores_j": "mu_j",
            "W_j": "-mu_j",
            "ridge": "-sum_j (-1,1,1,-1)_j mu_j",
        },
        "absolute_killer": (
            "an absolute occurrence-labelled Xi anti-carrier landing has "
            "dual value one; a relative PP-to-cap graph only transports "
            "the dual and is absorbed by the displayed augmented values"
        ),
    }


def selected_packet(local_left: Matching, local_right: Matching) -> Polynomial:
    tails = tuple(perfect_matchings((TWO, THREE, FOUR, FIVE)))
    answer: Polynomial = Counter()
    for local in (local_left, local_right):
        for tail in tails:
            answer[tuple(sorted(local + tail))] += 1
    require(len(answer) == 6 and set(answer.values()) == {Q(1)},
            "selected switch packet changed")
    return answer


def unsigned_root_shortcut_audit() -> dict[str, object]:
    require(len(MATCHINGS) == 105, "K8 matching count changed")
    D = edge(P, S)
    Q01 = edge(ZERO, ONE)
    A = (D, Q01)
    B = tuple(sorted((edge(P, ZERO), edge(S, ONE))))
    C = tuple(sorted((edge(P, ONE), edge(S, ZERO))))

    first_0 = unsigned_root(RESPONSE, ZERO, S)
    first_1 = unsigned_root(RESPONSE, ONE, S)
    require(len(first_0) == len(first_1) == 45
            and set(first_0.values()) == set(first_1.values()) == {Q(2)},
            "an unsigned first root stopped being the symmetric collision")

    second_0 = unsigned_root(first_0, S, ZERO)
    second_1 = unsigned_root(first_1, S, ONE)
    expected_0 = Counter({matching: Q(2) for matching in MATCHINGS
                          if edge(ZERO, S) not in matching})
    expected_1 = Counter({matching: Q(2) for matching in MATCHINGS
                          if edge(ONE, S) not in matching})
    require(second_0 == expected_0 and second_1 == expected_1
            and len(second_0) == len(second_1) == 90,
            "unsigned second-order aggregate changed")

    # Literal one-tail return: A -> A+B and A -> A+C.  This is exactly the
    # shore-gauged sign required by the fixed-window theorem.
    tail = ((TWO, THREE), (FOUR, FIVE))
    a_tail = Counter({tuple(sorted(A + tail)): Q(1)})
    return_ab = unsigned_root(unsigned_root(a_tail, ZERO, S), S, ZERO)
    return_ac = unsigned_root(unsigned_root(a_tail, ONE, S), S, ONE)
    expected_ab_one = Counter({tuple(sorted(A + tail)): Q(1),
                               tuple(sorted(B + tail)): Q(1)})
    expected_ac_one = Counter({tuple(sorted(A + tail)): Q(1),
                               tuple(sorted(C + tail)): Q(1)})
    require(return_ab == expected_ab_one and return_ac == expected_ac_one,
            "unsigned local returns stopped being A+B and A+C")

    fixed_ab = selected_packet(A, B)
    fixed_ac = selected_packet(A, C)
    gauged_l = add_polynomials(fixed_ab, fixed_ac)
    order = tuple(sorted(MATCHINGS))
    h = vector_on(order, RESPONSE)
    u0 = vector_on(order, second_0)
    u1 = vector_on(order, second_1)
    fab = vector_on(order, fixed_ab)
    fac = vector_on(order, fixed_ac)
    lg = vector_on(order, gauged_l)
    base = (h, u0, u1)
    require(rank(base) == 3
            and rank(base + (fab,)) == 4
            and rank(base + (fac,)) == 4
            and rank(base + (fab, fac)) == 5
            and rank(base + (fab, fac, lg)) == 5
            and lg == add(fab, fac),
            "unsigned aggregate/fixed-window ranks changed")

    # The two aggregate roots and H are constant on the three categories
    # N=no S0/S1, D0=contains S0, D1=contains S1.  Center within these
    # categories to obtain literal normalized occurrence detectors.
    support_a = set(tuple(sorted(A + t))
                    for t in perfect_matchings((TWO, THREE, FOUR, FIVE)))
    support_b = set(tuple(sorted(B + t))
                    for t in perfect_matchings((TWO, THREE, FOUR, FIVE)))
    support_c = set(tuple(sorted(C + t))
                    for t in perfect_matchings((TWO, THREE, FOUR, FIVE)))
    lambda_ab = []
    lambda_ac_after_ab = []
    lambda_l = []
    categories = Counter()
    for matching in order:
        has_s0 = edge(S, ZERO) in matching
        has_s1 = edge(S, ONE) in matching
        require(not (has_s0 and has_s1), "matching used S twice")
        category = "D0" if has_s0 else "D1" if has_s1 else "N"
        categories[category] += 1

        if matching in support_a:
            lambda_ab.append(Q(1, 6))
            lambda_l.append(Q(1, 12))
        elif category == "N":
            lambda_ab.append(Q(-1, 144))
            lambda_l.append(Q(-1, 288))
        elif matching in support_b:
            lambda_ab.append(Q(1, 6))
            lambda_l.append(Q(1, 12))
        elif category == "D1":
            lambda_ab.append(Q(-1, 24))
            lambda_l.append(Q(-1, 48))
        elif matching in support_c:
            lambda_ab.append(Q(0))
            lambda_l.append(Q(1, 12))
        else:
            lambda_ab.append(Q(0))
            lambda_l.append(Q(-1, 48))

        if matching in support_c:
            lambda_ac_after_ab.append(Q(1, 3))
        elif category == "D0":
            lambda_ac_after_ab.append(Q(-1, 12))
        else:
            lambda_ac_after_ab.append(Q(0))

    lambda_ab = tuple(lambda_ab)
    lambda_ac_after_ab = tuple(lambda_ac_after_ab)
    lambda_l = tuple(lambda_l)
    require(categories == Counter({"N": 75, "D0": 15, "D1": 15}),
            ("unsigned matching categories changed", categories))
    require(all(dot(lambda_ab, value) == 0 for value in base)
            and dot(lambda_ab, fab) == 1,
            "first fixed-window switch detector changed")
    require(all(dot(lambda_ac_after_ab, value) == 0
                for value in base + (fab,))
            and dot(lambda_ac_after_ab, fac) == 1,
            "second fixed-window switch detector changed")
    require(all(dot(lambda_l, value) == 0 for value in base)
            and dot(lambda_l, lg) == 1,
            "combined shore-gauged detector changed")

    # The signed standard collision dual is centered, hence kills both
    # symmetric unsigned first derivatives.  The shortcut is real at first
    # order, but its second-order aggregate is the new occurrence debt.
    compressed_pair_weights = []
    neighbours = tuple(vertex for vertex in VERTICES
                       if vertex not in (ZERO, S))
    for left, right in combinations(neighbours, 2):
        compressed_pair_weights.append(
            Q(int(left == P or right == P)
              - int(left == ONE or right == ONE))
        )
    require(Counter(compressed_pair_weights)
            == Counter({Q(1): 4, Q(-1): 4, Q(0): 7})
            and sum(compressed_pair_weights, Q(0)) == 0,
            "signed collision standard character changed")

    return {
        "unsigned_first_roots": {
            "0_to_S": "symmetric missing-0/doubled-S row: 45 terms * 2",
            "1_to_S": "symmetric missing-1/doubled-S row: 45 terms * 2",
            "signed_Xi_dual_value": 0,
            "consequence_if_symmetric_collision_cells_are_granted": (
                "the signed 24-term first-order obstruction is bypassed"
            ),
        },
        "shore_gauged_local_returns": {
            "0_S_square_on_A": "A+B",
            "1_S_square_on_A": "A+C",
            "sign_is_the_required_physical_shore_gauge": True,
        },
        "complete_second_order": {
            "0_S_square": "2*(RESPONSE - response block containing edge 0S)",
            "1_S_square": "2*(RESPONSE - response block containing edge 1S)",
            "terms_each": 90,
            "coefficient_each": 2,
            "selected_fixed_window_terms_each": 6,
        },
        "exact_ranks": {
            "complete_response_plus_two_unsigned_aggregates": 3,
            "after_one_fixed_window_switch": 4,
            "after_both_fixed_window_switches": 5,
            "after_shore_gauged_L_equals_AB_plus_AC": 5,
        },
        "normalized_detectors": {
            "first_A_plus_B_mod_aggregates": {
                "selected_A_and_B": "1/6",
                "other_N": "-1/144",
                "other_D1": "-1/24",
                "D0": "0",
            },
            "A_plus_C_after_A_plus_B": {
                "selected_C": "1/3", "other_D0": "-1/12",
                "elsewhere": "0",
            },
            "shore_gauged_2A_plus_B_plus_C": {
                "selected_A_B_C": "1/12",
                "other_N": "-1/288",
                "other_D0_D1": "-1/48",
            },
        },
        "first_new_family_after_unsigned_shortcut": (
            "a squarefree occurrence/window projector splitting the three "
            "A/B (respectively A/C) tail orbits out of the 45 orbit sums in "
            "the unsigned second-order aggregate, with the same word/fine/"
            "repeated labels and its PP/reinsertion plus augmented readouts"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "h3 collision Xi augmented dual and unsigned-root shortcut gate",
        "pins": PINS,
        "relative_Xi_augmented_extension": augmented_relative_xi_audit(),
        "unsigned_vertex_root_shortcut": unsigned_root_shortcut_audit(),
        "verdict": (
            "The Xi_01/30 dual extends through all 90 top graphs, all 120 "
            "parent-labelled first-PP graphs, and every known response/cap/"
            "Cartan column.  Tag separation initially forces target, Eq, q, "
            "anchor, ores, W and ridge all to zero.  The first cross-grade "
            "rank raiser is the missing forward-DSQ PP-to-cap bridge; after "
            "such a relative bridge the known packet forces target=W=-mu, "
            "ores=mu, ridge=-alpha.mu and Eq=q=anchor=0, so the dual still "
            "extends.  An absolute Xi-carrier landing is the actual killer. "
            "Complete unsigned roots genuinely bypass Xi at first order and "
            "give the correct shore-gauged local returns A+B and A+C.  On "
            "the complete response, however, their second order is the 90-"
            "term aggregate 2*(response minus the 0S/1S edge block), not the "
            "six-term fixed-window switch.  Extracting each selected switch "
            "raises rank and requires a new squarefree occurrence projector."
        ),
        "scope": (
            "exact canonical h=3 rational presentation.  The Xi part is a "
            "presentation-safe relative/known-augmentation theorem, not an "
            "exhaustion of unknown full-source columns.  The unsigned part "
            "uses the complete 105-matching response and proves the exact "
            "second-order aggregate; it does not construct the required "
            "fixed-window occurrence projector or its physical augmented "
            "landing."
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
    print("Xi/30 through relative top+120 PP+known augmentation: EXTENDS")
    print("initial target/Eq/q/anchor/ores/W/ridge: ALL ZERO")
    print("first cross-grade rank raiser: FORWARD DSQ PP-TO-CAP BRIDGE")
    print("unsigned first root: SYMMETRIC COLLISION, Xi BYPASSED")
    print("unsigned second order: 2*(RESPONSE - 0S/1S EDGE BLOCK)")
    print("fixed-window A+B and A+C: TWO INDEPENDENT OCCURRENCE RAISERS")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
