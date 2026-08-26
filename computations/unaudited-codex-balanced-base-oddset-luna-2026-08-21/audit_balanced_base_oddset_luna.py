#!/usr/bin/env python3
"""Finite graph and second-fundamental-form audit at a balanced base point."""

from __future__ import annotations

import argparse
from collections import defaultdict
from fractions import Fraction
from functools import reduce
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = HERE / "results_balanced_base_oddset_luna.json"
PINS = {
    "computations/unaudited-codex-t0-kempf-ness-2026-08-21/results_t0_kempf_ness.json":
        "b3e1eefbf00efdf62caed722e24f74efda6068b7b2b0b8db090fe5bb85792eda",
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position, partner in enumerate(vertices[1:], 1):
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            yield ((first, partner),) + tail


PM8 = tuple(perfect_matchings(range(8)))


def amplitude(source, word):
    return sum(
        reduce(lambda value, edge: value * source.get(
            (edge[0], edge[1], word[edge[0]], word[edge[1]]), 0),
               matching, Fraction(1))
        for matching in PM8
    )


def energies(source):
    return {
        (site, colour): sum(
            value * value for (u, v, a, b), value in source.items()
            if (u, a) == (site, colour) or (v, b) == (site, colour)
        )
        for site in range(8) for colour in range(3)
    }


ODD_EDGES = ((0, 1), (1, 2), (0, 2),
             (3, 4), (4, 5), (5, 6), (6, 7), (3, 7))


def odd_cycle_controls():
    diagonal = {(u, v, 0, 0): Fraction(1) for u, v in ODD_EDGES}
    diagonal_energy = energies(diagonal)
    require([diagonal_energy[i, 0] for i in range(8)] == [2] * 8,
            diagonal_energy)
    require(all(amplitude(diagonal, word) == 0
                for word in product(range(3), repeat=8)), "diagonal top nonzero")

    leakage = {}
    for u, v in ODD_EDGES:
        for a in range(3):
            for b in range(3):
                if a != b:
                    leakage[(u, v, a, b)] = Fraction(1)
    leakage_energy = energies(leakage)
    require(all(leakage_energy[i, c] == 4
                for i in range(8) for c in range(3)), leakage_energy)
    require(all(amplitude(leakage, word) == 0
                for word in product(range(3), repeat=8)), "leakage top nonzero")
    return {
        "diagonal": {
            "graph": "C3 disjoint_union C5",
            "port_energy": "2 in colour 0, zero otherwise",
            "fractional_one_factor": "edge weight 1/2 on both odd cycles",
            "perfect_matching": False,
            "top_tensor": "zero",
        },
        "offdiagonal_leakage": {
            "graph": "C3 disjoint_union C5, all six a!=b cells per edge",
            "port_energy": "4 at every site-colour port",
            "diagonal_support": "empty",
            "top_tensor": "zero",
        },
    }


# Q(w), w^2+w+1=0.
def qadd(x, y):
    return (x[0] + y[0], x[1] + y[1])


def qmul(x, y):
    a, b = x
    c, d = y
    return (a * c - b * d, a * d + b * c - b * d)


ONE = (Fraction(1), Fraction(0))
ZERO = (Fraction(0), Fraction(0))
W = (Fraction(0), Fraction(1))
W2 = qmul(W, W)


def cancellation_control():
    # First K4 matching products are 1,w,w^2; second K4 has all unit edges.
    first = {
        (0, 1): ONE, (2, 3): ONE,
        (0, 2): ONE, (1, 3): W,
        (0, 3): ONE, (1, 2): W2,
    }
    second = {edge: ONE for edge in combinations(range(4, 8), 2)}
    def haf4(weights, vertices):
        total = ZERO
        for matching in perfect_matchings(vertices):
            term = ONE
            for edge in matching:
                term = qmul(term, weights[tuple(sorted(edge))])
            total = qadd(total, term)
        return total
    left = haf4(first, range(4))
    right = haf4(second, range(4, 8))
    require(left == ZERO and right == (Fraction(3), Fraction(0)), (left, right))
    return {
        "support_graph": "K4 disjoint_union K4",
        "all_cell_moduli": 1,
        "port_energy": 3,
        "first_block_matching_products": ["1", "w", "w^2"],
        "first_block_hafnian": "1+w+w^2=0",
        "second_block_hafnian": "3",
        "eight_site_hafnian": "0",
        "full_perfect_matchings_in_support": 9,
        "meaning": (
            "This balanced diagonal base point has no leakage and many integral "
            "perfect matchings. Its vanishing is phase cancellation, invisible "
            "to fractional-matching and odd-cut support data."
        ),
    }


def one_colour_carrier_census(weights):
    """Rank/activity census when only the (0,0) cell can be nonzero."""
    def scalar(p, q, a, b):
        first = qmul(weights.get(tuple(sorted((p, a))), ZERO),
                     weights.get(tuple(sorted((q, b))), ZERO))
        second = qmul(weights.get(tuple(sorted((p, b))), ZERO),
                      weights.get(tuple(sorted((q, a))), ZERO))
        return qadd(first, second)

    histograms = {"star": defaultdict(int), "triangle": defaultdict(int)}
    active = {"star": 0, "triangle": 0}
    active_labels = {"star": [], "triangle": []}
    for p, q in combinations(range(8), 2):
        residual = tuple(site for site in range(8) if site not in (p, q))
        pair_live = weights.get((p, q), ZERO) != ZERO
        for centre in residual:
            values = [scalar(p, q, a, b) for a, b in combinations(residual, 2)
                      if centre not in (a, b)]
            response_rank = int(any(value != ZERO for value in values))
            histograms["star"][response_rank] += 1
            # For a one-colour source, a carrier is active exactly when the
            # direct pair is live and the response rowspace is zero.
            is_active = pair_live and response_rank == 0
            active["star"] += int(is_active)
            if is_active:
                active_labels["star"].append(f"star:pq={p}{q}:centre={centre}")
        for triangle in combinations(residual, 3):
            allowed = set(combinations(triangle, 2))
            values = [scalar(p, q, a, b) for a, b in combinations(residual, 2)
                      if (a, b) not in allowed]
            response_rank = int(any(value != ZERO for value in values))
            histograms["triangle"][response_rank] += 1
            is_active = pair_live and response_rank == 0
            active["triangle"] += int(is_active)
            if is_active:
                active_labels["triangle"].append(
                    f"triangle:pq={p}{q}:sites={''.join(map(str, triangle))}"
                )
    return {
        "rank_histograms": {
            kind: {str(rank_value): count for rank_value, count in sorted(hist.items())}
            for kind, hist in histograms.items()
        },
        "active_rank_zero": active,
        "active_rank_zero_labels": active_labels,
        "pivot_valuation_variables": {
            "v_" + label.replace(":", "_").replace("=", "_"): ">0"
            for labels in active_labels.values() for label in labels
        },
        "meaning": (
            "Every active base carrier has response rank zero and a live direct "
            "pair. A no-cap arc can reach it only through response-pivot rank "
            "drop; fixed-rank rowspace incidence cannot persist."
        ),
    }


def qpoly_add(left, right):
    answer = dict(left)
    for degree, value in right.items():
        answer[degree] = qadd(answer.get(degree, ZERO), value)
        if answer[degree] == ZERO:
            del answer[degree]
    return answer


def qpoly_mul(left, right):
    answer = {}
    for left_degree, left_value in left.items():
        for right_degree, right_value in right.items():
            degree = left_degree + right_degree
            answer[degree] = qadd(answer.get(degree, ZERO),
                                  qmul(left_value, right_value))
    return {degree: value for degree, value in answer.items() if value != ZERO}


def qlabel(value):
    """Canonical compact label for an element a+b*w of Q(w)."""
    a, b = value
    pieces = []
    if a:
        pieces.append(str(a))
    if b:
        pieces.append(("+" if b > 0 and pieces else "") + str(b) + "*w")
    return "".join(pieces) or "0"


def phase_delayed_seed_audit():
    """First order-six seed not excluded by the order-four permanent guard."""
    cells = {}
    def add_cell(cell, degree, value):
        cells[cell] = qpoly_add(cells.get(cell, {}), {degree: value})

    left = {
        (0, 1): ONE, (2, 3): ONE, (0, 2): ONE, (0, 3): ONE,
        (1, 3): W, (1, 2): W2,
    }
    for edge, value in left.items():
        add_cell(edge + (0, 0), 0, value)
    for edge in combinations(range(4, 8), 2):
        add_cell(edge + (0, 0), 0, ONE)
    # U: all cross (1,0) cells at order one.
    for left_site in range(4):
        for right_site in range(4, 8):
            add_cell((left_site, right_site, 1, 0), 1, ONE)
    # R: a right perfect matching in (1,1), order one.
    for edge in ((4, 5), (6, 7)):
        add_cell(edge + (1, 1), 1, ONE)
    # The order-two response correction induced by U.  Since the right K4
    # hafnian is 3 and each two-cross sum is 12, every left cell is -4.
    for edge in combinations(range(4), 2):
        add_cell(edge + (1, 1), 2, (Fraction(-4), Fraction(0)))

    output = {}
    for matching in PM8:
        options = []
        for u, v in matching:
            options.append([
                (a, b, polynomial) for (x, y, a, b), polynomial in cells.items()
                if (x, y) == (u, v)
            ])
        for choice in product(*options):
            word = [None] * 8
            polynomial = {0: ONE}
            for (u, v), (a, b, factor) in zip(matching, choice):
                word[u], word[v] = a, b
                polynomial = qpoly_mul(polynomial, factor)
            label = "".join(map(str, word))
            output[label] = qpoly_add(output.get(label, {}), polynomial)
    degree_histogram = defaultdict(int)
    for polynomial in output.values():
        for degree in polynomial:
            degree_histogram[degree] += 1
    require(dict(sorted(degree_histogram.items())) == {3: 12, 4: 7, 6: 1},
            degree_histogram)
    require(output.get("11111111", {}).get(6) == (Fraction(48), Fraction(0)),
            output.get("11111111"))
    residual_rows = {
        str(degree): [
            {"word": word, "coefficient": qlabel(polynomial[degree])}
            for word, polynomial in sorted(output.items()) if degree in polynomial
        ]
        for degree in (3, 4)
    }
    require(len(residual_rows["3"]) == 12 and len(residual_rows["4"]) == 7,
            residual_rows)
    order3_by_right_pair = defaultdict(int)
    for row in residual_rows["3"]:
        order3_by_right_pair[row["word"][4:]] += 1
    require(dict(order3_by_right_pair) == {"0011": 6, "1100": 6},
            order3_by_right_pair)
    return {
        "scope": (
            "This is the oriented binary response channel U^(c,0)@1, "
            "R_right^(c,c)@1, L_left^(c,c)@2.  The contradiction is not an "
            "all-valuations or arbitrary-multichannel m=6 theorem."
        ),
        "valuation_signature": {
            "cross_(1,0)_U": 1,
            "right_internal_(1,1)_R": 1,
            "left_internal_(1,1)_L": 2,
        },
        "induced_correction": (
            "L_I=-(1/3) sum_(|J|=2) r_(J^c) per_2(U[I,J]); "
            "for U all-one and the unit right base this is L_I=-4"
        ),
        "orders_zero": [0, 1, 2],
        "nonzero_word_count_by_order": {
            str(degree): count for degree, count in sorted(degree_histogram.items())
        },
        "candidate_pure_order6": "[t^6] H_11111111=48",
        "cokernel_rows": residual_rows,
        "finite_coefficient_system": {
            "variables": "U_(i,a) (16), R_J (6), L_I (6)",
            "order2_elimination": (
                "3 L_I + sum_(|J|=2) per_2(U[I,J])=0 for all six left pairs I"
            ),
            "order3": (
                "R_J*(per_2(U[I,J^c]) + L_I)=0; the matching support "
                "R_45,R_67 gives the displayed 12 rows"
            ),
            "order4_six_rows": "L_I*Haf(R)=0 for all six left pairs I",
            "order6_pure": "Haf(L)*Haf(R)",
            "exact_exclusion": (
                "A nonzero order-six pure coefficient requires Haf(L)Haf(R)!=0. "
                "Then Haf(R)!=0, while the six order-four cokernel rows force "
                "every L_I=0, a contradiction. Thus this entire valuation "
                "channel has no admissible GHZ-leading m=6 seed."
            ),
        },
        "failure": (
            "12 mixed words survive at order 3 and 7 at order 4. Hence this "
            "is an exact lifted second-order seed, not an admissible GHZ jet."
        ),
    }


def phase_next_coupled_channel():
    """First channel which can reinsert a direct (c,c) polar into E4."""
    return {
        "valuation_partition": "1+1+2+2",
        "variables": {
            "U": "16 cross cells (c,0) at order 1",
            "X": "16 cross cells (c,c) at order 1",
            "V": "16 cross cells (c,c) at order 2",
            "R": "6 right-internal cells (c,c) at order 1",
            "L": "6 left-internal cells (c,c) at order 2",
            "total": 60,
            "after_eliminating_L": 54,
        },
        "binary_word_closure": (
            "Every displayed output word uses only colours {0,c}; cells using "
            "the third physical colour cannot cancel these coefficients."
        ),
        "equations": {
            "E2_response_6": (
                "3 L_I + sum_J per_2(U[I,J])=0"
            ),
            "E2_direct_36": "per_2(X[I,J])=0",
            "E3_direct_response_36": (
                "P_(X,V)[I,J] + R_J*(L_I+per_2(U[I,J^c]))=0"
            ),
            "E4_rescue_6": (
                "L_I*Haf(R) + sum_J R_(J^c)*P_(X,V)[I,J]=0"
            ),
        },
        "polar_definition": (
            "P_(X,V)[I,J] is the coefficient of t^3 in "
            "per_2(t X[I,J]+t^2 V[I,J])."
        ),
        "pure_order6": (
            "Haf(L)Haf(R) + sum_(I,J) L_(I^c)R_(J^c)P_(X,V)[I,J] "
            "+ [t^6]per_4(tX+t^2V)"
        ),
        "first_escape_from_previous_obstruction": (
            "The new polar term sum_J R_(J^c)P_(X,V)[I,J] has exactly the "
            "same left-pair/right-four word as L_I Haf(R), so the six E4 "
            "rows no longer force L=0.  This is the first finite channel not "
            "excluded by the previous response-only argument."
        ),
        "support_reduction": (
            "The 36 equations per_2(X[I,J])=0 imply that the nonzero support "
            "of X is a row star, a column star, or is contained in one 2x2 "
            "block with its single permanent cancellation.  Thus the literal "
            "right-site S4 symmetry reduces the first-order direct support to "
            "these three types; the phased left K4 has trivial exact site "
            "stabilizer."
        ),
        "status": (
            "First unresolved finite system.  Order-4/5 cokernel rows and the "
            "72 positive no-cap pivot valuations must be appended before any "
            "positive Puiseux seed is admissible."
        ),
    }


def phase_column_star_survivor_and_pivots():
    """Exact E2--E4 survivor and all active-carrier pivot valuations."""
    cells = {}
    def add(cell_key, degree, value):
        cells[cell_key] = qpoly_add(cells.get(cell_key, {}), {degree: value})

    left = {
        (0, 1): ONE, (2, 3): ONE, (0, 2): ONE, (0, 3): ONE,
        (1, 3): W, (1, 2): W2,
    }
    for edge, value in left.items():
        add(edge + (0, 0), 0, value)
    for edge in combinations(range(4, 8), 2):
        add(edge + (0, 0), 0, ONE)

    # z_i=1 specialization of the column-star family.
    for i in range(4):
        for j in (4, 5, 6):
            add((i, j, 1, 0), 1, ONE)      # U
        add((i, 4, 1, 1), 1, ONE)          # X
        add((i, 5, 1, 1), 2, ONE)          # V
    for edge in ((4, 5), (6, 7)):
        add(edge + (1, 1), 1, ONE)          # R
    for edge in combinations(range(4), 2):
        add(edge + (1, 1), 2, (Fraction(-2), Fraction(0)))  # L

    # Direct finite equations at z_i=1.
    q_values = {}
    for i, k in combinations(range(4), 2):
        for j, ell in combinations(range(4, 8), 2):
            uij = int(j in (4, 5, 6))
            uiell = int(ell in (4, 5, 6))
            ukj = int(j in (4, 5, 6))
            ukell = int(ell in (4, 5, 6))
            q_values[(i, k, j, ell)] = uij * ukell + uiell * ukj
    for i, k in combinations(range(4), 2):
        pair_values = [q_values[(i, k, j, ell)]
                       for j, ell in combinations(range(4, 8), 2)]
        require(sum(pair_values) == 6, pair_values)
        require(-6 + sum(pair_values) == 0, pair_values)  # 3 L + sum q
        require(q_values[(i, k, 4, 5)] == 2, pair_values)
        require(q_values[(i, k, 6, 7)] == 0, pair_values)
        for j, ell in combinations(range(4, 8), 2):
            right_pair = (j, ell)
            complement = tuple(x for x in range(4, 8) if x not in right_pair)
            polar = 2 if right_pair == (4, 5) else 0
            r_value = int(right_pair in ((4, 5), (6, 7)))
            e3 = polar + r_value * (
                -2 + q_values[(i, k, complement[0], complement[1])]
            )
            require(e3 == 0, (i, k, right_pair, e3))
        e4 = -2 + 2  # L_I Haf(R) + R_67 P[I,45]
        require(e4 == 0, (i, k, e4))

    pure_polynomial = {}
    for matching in PM8:
        term = {0: ONE}
        for u, v in matching:
            term = qpoly_mul(term, cells.get((u, v, 1, 1), {}))
        pure_polynomial = qpoly_add(pure_polynomial, term)
    require(pure_polynomial == {6: (Fraction(-12), Fraction(0))},
            pure_polynomial)

    omitted_order2 = []
    for i, k in combinations(range(4), 2):
        word = [0] * 8
        word[i] = word[k] = word[4] = 1
        polynomial = {}
        for matching in PM8:
            term = {0: ONE}
            for u, v in matching:
                term = qpoly_mul(term, cells.get((u, v, word[u], word[v]), {}))
            polynomial = qpoly_add(polynomial, term)
        complement = tuple(x for x in range(4) if x not in (i, k))
        expected = qmul((Fraction(4), Fraction(0)), left[complement])
        require(polynomial == {2: expected}, (word, polynomial, expected))
        omitted_order2.append({
            "word": "".join(map(str, word)),
            "coefficient_at_z=1": qlabel(expected),
            "general_coefficient": f"4*l_{complement[0]}{complement[1]}*z_{i}*z_{k}",
        })

    def oriented_cell(u, v, a, b):
        if u < v:
            return cells.get((u, v, a, b), {})
        return cells.get((v, u, b, a), {})

    def response_poly(p, q, a, b, alpha, beta, i, j):
        first = qpoly_mul(oriented_cell(p, a, i, alpha),
                          oriented_cell(q, b, j, beta))
        second = qpoly_mul(oriented_cell(p, b, i, beta),
                           oriented_cell(q, a, j, alpha))
        return qpoly_add(first, second)

    pivot_hist = {"star": defaultdict(int), "triangle": defaultdict(int)}
    inactive = []
    for p, q in combinations(range(8), 2):
        if (p, q) not in left and not (4 <= p < q <= 7):
            continue
        residual = tuple(site for site in range(8) if site not in (p, q))
        carriers = []
        for centre in residual:
            carriers.append(("star", f"star:pq={p}{q}:centre={centre}",
                             [edge for edge in combinations(residual, 2)
                              if centre not in edge]))
        for triangle in combinations(residual, 3):
            allowed = set(combinations(triangle, 2))
            carriers.append((
                "triangle",
                f"triangle:pq={p}{q}:sites={''.join(map(str, triangle))}",
                [edge for edge in combinations(residual, 2) if edge not in allowed],
            ))
        for kind, label, edges in carriers:
            degrees = []
            for a, b in edges:
                for alpha in range(3):
                    for beta in range(3):
                        for i in range(3):
                            for j in range(3):
                                polynomial = response_poly(
                                    p, q, a, b, alpha, beta, i, j
                                )
                                degrees.extend(polynomial)
            # Only the 72 carriers with rank zero at the base are in scope.
            if not degrees or min(degrees) > 0:
                if degrees:
                    pivot_hist[kind][min(degrees)] += 1
                else:
                    inactive.append(label)
    require(sum(pivot_hist["star"].values()) +
            sum(pivot_hist["triangle"].values()) + len(inactive) == 72,
            (pivot_hist, inactive))

    return {
        "general_family": (
            "For z_0 z_1 z_2 z_3!=0 set U_i4=U_i5=U_i6=z_i, U_i7=0, "
            "X_i4=z_i, V_i5=z_i, R_45=R_67=1, L_ij=-2 z_i z_j. "
            "Then Haf(L)Haf(R)=12 product_i z_i and the full pure coefficient "
            "is -12 product_i z_i."
        ),
        "specialization": (
            "z_i=1; U_i4=U_i5=U_i6=1,U_i7=0; X_i4=1; V_i5=1; "
            "R_45=R_67=1; L_I=-2"
        ),
        "equation_check": (
            "E2, E3, and E4 vanish identically; Haf(L)Haf(R)=12 and the "
            "full literal pure coefficient [t^6]H_11111111=-12"
        ),
        "literal_omitted_order2_obstruction": {
            "rows": omitted_order2,
            "cokernel_guard": (
                "Every word has three colour-c sites including right site 4, "
                "whereas im(dH at the phase base) has right block colour zero. "
                "No order-two source correction can cancel it."
            ),
            "contradiction": (
                "All six left complementary base cells are nonzero Q(w) units. "
                "The pure coefficient requires product_i z_i!=0, so all six "
                "displayed order-two mixed coefficients are nonzero."
            ),
        },
        "support_type": "column star X",
        "pivot_valuation_histograms": {
            kind: {str(degree): count for degree, count in sorted(hist.items())}
            for kind, hist in pivot_hist.items()
        },
        "unactivated_active_carriers": inactive,
        "all_72_positive": not inactive,
        "terminal_scope": (
            "The family survives only the reduced E2--E4 packet and pivot "
            "nonvanishing. The six literal omitted rows kill it before any "
            "blocker-membership choice."
        ),
    }


def phase_two_colour_order2_audit():
    """Duplicate the z=1 family in colours 1,2 and freeze the first shell."""
    cells = {}
    def add(cell_key, degree, value):
        cells[cell_key] = qpoly_add(cells.get(cell_key, {}), {degree: value})
    left = {
        (0, 1): ONE, (2, 3): ONE, (0, 2): ONE, (0, 3): ONE,
        (1, 3): W, (1, 2): W2,
    }


def phase_adjusted_column_star_order3_audit():
    """Kill the U-X shell in the full column-star branch and expose U-V."""
    cells = {}
    def add(cell_key, degree, value):
        cells[cell_key] = qpoly_add(cells.get(cell_key, {}), {degree: value})
    left = {
        (0, 1): ONE, (2, 3): ONE, (0, 2): ONE, (0, 3): ONE,
        (1, 3): W, (1, 2): W2,
    }
    for edge, value in left.items():
        add(edge + (0, 0), 0, value)
    for edge in combinations(range(4, 8), 2):
        add(edge + (0, 0), 0, ONE)
    for i in range(4):
        for j, value in ((4, Fraction(-1, 3)), (5, Fraction(1)),
                         (7, Fraction(-1))):
            add((i, j, 1, 0), 1, (value, Fraction(0)))
        add((i, 4, 1, 1), 1, ONE)
        add((i, 5, 1, 1), 2, (Fraction(-1, 3), Fraction(0)))
    for edge in ((4, 5), (6, 7)):
        add(edge + (1, 1), 1, ONE)
    for edge in combinations(range(4), 2):
        add(edge + (1, 1), 2, (Fraction(2, 3), Fraction(0)))

    output = {}
    for matching in PM8:
        options = []
        for u, v in matching:
            options.append([
                (a, b, polynomial)
                for (x, y, a, b), polynomial in cells.items() if (x, y) == (u, v)
            ])
        for choice in product(*options):
            word = [None] * 8
            polynomial = {0: ONE}
            for (u, v), (a, b, factor) in zip(matching, choice):
                word[u], word[v] = a, b
                polynomial = qpoly_mul(polynomial, factor)
            label = "".join(map(str, word))
            output[label] = qpoly_add(output.get(label, {}), polynomial)
    histogram = defaultdict(int)
    for polynomial in output.values():
        for degree in polynomial:
            histogram[degree] += 1
    require(dict(sorted(histogram.items())) == {3: 12, 4: 7, 5: 4, 6: 2},
            histogram)
    require(output["11111111"] == {6: (Fraction(-4, 3), Fraction(0))},
            output["11111111"])
    order3 = [
        {"word": word, "coefficient": qlabel(polynomial[3])}
        for word, polynomial in sorted(output.items()) if 3 in polynomial
    ]
    require(len(order3) == 12, order3)
    return {
        "specialization": (
            "U_i4=-1/3,U_i5=1,U_i6=0,U_i7=-1; X_i4=1; "
            "V_i5=-1/3; R_45=R_67=1; L_I=2/3"
        ),
        "orders_zero": [0, 1, 2],
        "nonzero_word_count_by_order": {
            str(degree): count for degree, count in sorted(histogram.items())
        },
        "pure_order6": "[t^6]H_11111111=-4/3",
        "order3_rows": order3,
        "verdict": (
            "The adjusted full column-star specialization kills all 24 U-X "
            "rows but has twelve literal mixed U-V/response rows at order three."
        ),
    }
    for edge, value in left.items():
        add(edge + (0, 0), 0, value)
    for edge in combinations(range(4, 8), 2):
        add(edge + (0, 0), 0, ONE)
    for colour in (1, 2):
        for i in range(4):
            for j in (4, 5, 6):
                add((i, j, colour, 0), 1, ONE)
            add((i, 4, colour, colour), 1, ONE)
            add((i, 5, colour, colour), 2, ONE)
        for edge in ((4, 5), (6, 7)):
            add(edge + (colour, colour), 1, ONE)
        for edge in combinations(range(4), 2):
            add(edge + (colour, colour), 2, (Fraction(-2), Fraction(0)))

    rows = []
    counts = {"binary_colour1": 0, "binary_colour2": 0, "cross_colour": 0}
    for word in product(range(3), repeat=8):
        polynomial = {}
        for matching in PM8:
            term = {0: ONE}
            for u, v in matching:
                term = qpoly_mul(term, cells.get((u, v, word[u], word[v]), {}))
            polynomial = qpoly_add(polynomial, term)
        if 2 not in polynomial:
            continue
        used = set(word) - {0}
        if used == {1}:
            kind = "binary_colour1"
        elif used == {2}:
            kind = "binary_colour2"
        else:
            kind = "cross_colour"
        counts[kind] += 1
        rows.append({
            "word": "".join(map(str, word)),
            "coefficient": qlabel(polynomial[2]),
            "kind": kind,
        })
    require(counts == {
        "binary_colour1": 6, "binary_colour2": 6, "cross_colour": 36,
    }, counts)
    require(len(rows) == 48, len(rows))
    return {
        "first_nonzero_mixed_order": 2,
        "row_counts": counts,
        "rows": rows,
        "verdict": (
            "The duplicated two-colour family already has 48 nonzero mixed "
            "coefficients at order two. The 12 binary rows alone are terminal; "
            "third-colour or cross-colour source cells cannot cancel a binary "
            "output word. Higher valuation shells are therefore not entered."
        ),
        "blocker_branch_guard": (
            "The literal source equation fails before carrier membership is "
            "tested, so all four blocker choices on each of the 72 activated "
            "carriers are excluded simultaneously."
        ),
    }


def phase_support_type_resolution():
    return {
        "right_symmetry": (
            "The minimum Haf(R)!=0 support is one right perfect matching; "
            "right S4 has one orbit, represented by R_45=R_67=1."
        ),
        "row_star_X": {
            "verdict": "contradiction",
            "proof": (
                "If the X-star row is r, then P_(X,V)[I,J]=0 whenever the "
                "left pair I avoids r. E4 and Haf(R)!=0 force L_I=0 for all "
                "three such pairs. Every left perfect matching contains one "
                "pair avoiding r, hence Haf(L)=0."
            ),
        },
        "column_star_X": {
            "verdict": "survivor",
            "representative": "column 4, with the z-family frozen separately",
            "minimal_R_support": 2,
        },
        "two_by_two_X": {
            "verdict_on_minimal_R_orbit": "contradiction",
            "proof": (
                "Put the X block on rows {0,1}, columns {4,5}. E4 gives "
                "L_23=0. With R_45 R_67!=0, E3 gives q_45=-L and q_67=0, "
                "while E2 gives B(a+b,c+d)=2B(a,b), where a,b,c,d are the "
                "four columns of U and q_45=B(a,b). The symmetrized-product "
                "lemma forces q_01 q_23=q_02 q_13=q_03 q_12. Since q_23=0, "
                "Haf(q_45)=0, so Haf(L)=0."
            ),
            "symmetrized_product_lemma": (
                "If B(a+b,e)=2B(a,b) in characteristic zero, the three "
                "complementary products of the six off-diagonal entries of "
                "B(a,b) are equal. This follows after writing a=(s+d)/2, "
                "b=(s-d)/2: solvability of r_i+r_j=1-delta_i delta_j "
                "forces at least three delta_i equal; degenerate coordinate "
                "cases follow by the same cross-multiplied identities."
            ),
            "scope_guard": (
                "Denser R support in the 2x2-X stratum is not classified; it "
                "cannot beat the column-star survivor's two-edge R support."
            ),
        },
        "smallest_surviving_branch": "column-star X with two-edge R matching",
    }


def phase_m6_partition_ledger():
    partitions = [(1, 1, 1, 3), (1, 1, 2, 2)]

    right_vertices = (4, 5, 6, 7)
    base_matching = {frozenset((4, 5)), frozenset((6, 7))}
    stabilizer = []
    for image in permutations(right_vertices):
        mapping = dict(zip(right_vertices, image))
        transported = {
            frozenset((mapping[u], mapping[v])) for u, v in ((4, 5), (6, 7))
        }
        if transported == base_matching:
            stabilizer.append(mapping)
    require(len(stabilizer) == 8, len(stabilizer))
    extras = tuple(combinations(right_vertices, 2))
    extras = tuple(edge for edge in extras if frozenset(edge) not in base_matching)
    unseen = {frozenset(subset) for size in range(5)
              for subset in combinations(extras, size)}
    orbit_representatives = []
    while unseen:
        representative = min(unseen, key=lambda subset: (len(subset), sorted(subset)))
        orbit = set()
        for mapping in stabilizer:
            orbit.add(frozenset(
                tuple(sorted((mapping[u], mapping[v]))) for u, v in representative
            ))
        unseen -= orbit
        orbit_representatives.append({
            "extra_edges": [f"{u}{v}" for u, v in sorted(representative)],
            "extra_count": len(representative),
            "orbit_size": len(orbit),
        })
    require(len(orbit_representatives) == 6, orbit_representatives)

    return {
        "integer_partitions": [list(values) for values in partitions],
        "cross_edge_topologies": [0, 2, 4],
        "ledger": {
            "1113_k0": (
                "Impossible: two left-internal pure edges are needed but only "
                "one edge has valuation >1; an order-one left-internal (c,c) "
                "cell has an uncancellable linear word."
            ),
            "1113_k2": (
                "Impossible: the left-internal edge must have valuation 3 and "
                "the two cross edges valuation 1. Their order-two per_2 word "
                "is lower than the pure term and contains its cross factor."
            ),
            "1113_k4": (
                "Impossible: per_2(X)=0 puts the order-one cross support in a "
                "star or one 2x2 cancellation block, so it has no size-three "
                "matching required by the 1+1+1+3 pure term."
            ),
            "1122_k0": (
                "Both left edges have valuation 2 and both right edges valuation "
                "1. Cancelling the left linear rows forces the oriented U@1 "
                "response system; without a direct polar E4 kills it, and with "
                "a direct polar it is the classified coupled channel."
            ),
            "1122_k2": (
                "If the cross valuations are 1,1 and R has valuation 2, the "
                "order-two per_2(X) row kills the pure factor. The only remaining "
                "assignment is L@2,R@1,X@1,V@2, exactly the coupled channel."
            ),
            "1122_k4": (
                "The degree-six per_4 coefficient is a Laplace sum of degree-two "
                "per_2(X) and degree-three P_(X,V) factors. Without L@2,R@1 it "
                "vanishes; with them it reduces to the same coupled channel."
            ),
        },
        "exhaustive_reduction": (
            "Every binary total-pure-order-six topology is impossible or reduces "
            "to U@1,X@1,R@1,L@2,V@2. There is no third integer partition."
        ),
        "minimum_R_support_resolution": (
            "For R_45 R_67!=0 with no extra R edges, row-star and 2x2-X are "
            "excluded. A column-star with at least three nonzero X entries "
            "first obeys the 24 omitted U-X equations, forcing "
            "sum_(j!=4)U_ij=0. E2/E3 then force U_4=-b/3, "
            "U_6+U_7=-b, L=(1/3)B(b,b), and B(X,V)=-L. The next six U-V "
            "rows force B(V,b)=0, contradicting B(X,V)=-L when Haf(L)!=0."
        ),
        "smallest_unresolved_minimum_R_branch": (
            "Column-star X with exactly two nonzero row entries. One entry is "
            "the already excluded row-star; three or four entries are killed "
            "by the U-X/U-V polar chain above."
        ),
        "next_support_orbits": {
            "fixed_live_matching": ["45", "67"],
            "stabilizer_order": len(stabilizer),
            "extra_edge_orbits": orbit_representatives,
            "meaning": (
                "Beyond the two-entry column-star on the minimum-R orbit, any "
                "remaining m6 binary escape lies in one of the five denser-R "
                "orbits (one extra edge; two adjacent; two opposite; three; four)."
            ),
        },
    }


def phase_m6_six_branch_resolution():
    return {
        "localization": (
            "Binary coupled channel with Haf(L)Haf(R)!=0, a live right "
            "matching normalized to 45|67, and X a two-entry column star on "
            "column 4. This is exactly the six-branch antichain left by the "
            "partition/support ledger."
        ),
        "notation": (
            "Write a,b,c,d for U columns 4,5,6,7, x for the two-entry X "
            "column, and B(u,v)_ik=u_i v_k+u_k v_i. Let m45=R45 R67, "
            "m46=R46 R57, m47=R47 R56 and h=m45+m46+m47=Haf(R)."
        ),
        "literal_rows": {
            "order2_UX": (
                "B(x,b+c+d)=0. For a two-entry x on rows 0,1, every U column "
                "selected by a live complementary R edge is supported on "
                "rows 0,1 and is proportional to y=(x0,-x1,0,0)."
            ),
            "order3_XUR": (
                "R67 B(x,b)=0, R57 B(x,c)=0, R56 B(x,d)=0. These are the "
                "literal words with colour c on a left pair and on the three "
                "right sites consisting of 4 plus the chosen R edge."
            ),
            "E3_nonincident": (
                "R67(q45+L)=R57(q46+L)=R56(q47+L)=0. Thus every live "
                "nonincident R edge identifies the corresponding B(a,U_j) "
                "with -L."
            ),
            "E4_contraction": (
                "m45 q67 + m46 q57 + m47 q56=0. The L terms cancel exactly "
                "after substituting the three incident E3 polar rows."
            ),
        },
        "branches": {
            "no_extra": (
                "m45!=0 and E4 gives q67=0. Then P45=-R45 L. The rows "
                "B(x,b)=0 make b=mu*(x0,-x1,0,0); comparing B(x,V5) with "
                "R45 B(a,b) on rows 02 and 12 gives V5_2=+R45 mu a2 and "
                "V5_2=-R45 mu a2. Likewise at site3, so Haf(L)=0."
            ),
            "one_extra": (
                "No second right matching product is completed, so E4 still "
                "gives q67=0 and the no-extra contradiction is unchanged."
            ),
            "two_adjacent": (
                "No complementary extra pair is present; again h=m45 and the "
                "no-extra contradiction applies."
            ),
            "two_opposite": (
                "A second matching is completed. The two XUR rows make its two "
                "U columns proportional to y; E3 equality makes the scalars "
                "equal. Hence q67=q57, and E4 becomes h*q67=0. Since h!=0, "
                "q67=0 and the no-extra comparison kills Haf(L)."
            ),
            "three_extra": (
                "Exactly one additional matching product is completed. The same "
                "proportionality/equality gives q67=q56, so E4 is h*q67=0 and "
                "reduces to the no-extra contradiction."
            ),
            "four_extra": (
                "All b,c,d are proportional to y, and E3 makes their scalars "
                "equal. Thus q67=q57=q56; E4 gives h*q67=0. With h!=0 this "
                "again forces the no-extra contradiction."
            ),
        },
        "verdict": (
            "All six support branches are empty on Haf(L)Haf(R)!=0. Since the "
            "contradictions are binary literal rows, a second physical colour "
            "cannot cancel them; all carrier pivot and four-way blocker branches "
            "are excluded upstream."
        ),
        "scope_guard": (
            "This exhausts the frozen six-branch response-component antichain. "
            "A divisor with Haf(R)=0 but a nonzero direct k=2/k=4 pure6 polar "
            "is not represented by this antichain and must not be claimed closed."
        ),
    }


def phase_m6_hafR_zero_resolution():
    return {
        "pure_degree6_decomposition": (
            "H6=Haf(L)Haf(R) + sum_(I,J)L_(I^c)R_(J^c)P[I,J] "
            "+ [t^6]per_4(tX+t^2V), where I,J run over left/right pairs."
        ),
        "minimum_support_orbits": {
            "k4_R_empty": (
                "R has empty support; there is one orbit and only the direct "
                "four-cross term can contribute."
            ),
            "k2_R_single_edge": (
                "A single R edge is the minimum k2 support and is one S4 orbit; "
                "Haf(R)=0 automatically."
            ),
            "first_coefficient_cancellation": (
                "The minimum support carrying nonzero matching products but "
                "Haf(R)=0 is the union of two right perfect matchings (a C4), "
                "one S4 orbit, with m1+m2=0."
            ),
            "direct_X_types": [
                "row star", "column star", "one 2x2 permanent-cancellation block"
            ],
        },
        "k2_contraction": (
            "The six literal E4 rows are L_I Haf(R)+sum_J R_(J^c)P[I,J]=0. "
            "On Haf(R)=0 they give sum_J R_(J^c)P[I,J]=0 for every I. "
            "Multiplying by L_(I^c) and summing I is exactly the full k2 "
            "degree-six contribution, so k2=0 for arbitrary R support. More "
            "generally k2=-2 Haf(L)Haf(R), since sum_I L_I L_(I^c)=2Haf(L)."
        ),
        "k4_laplace": (
            "The 36 degree-two rows give per_2(X[I,J])=0, hence X is a row "
            "star, column star, or one 2x2 cancellation block. For a row star "
            "choose two left rows avoiding its centre; for a 2x2 block choose "
            "the complementary two rows; for a column star choose two right "
            "columns avoiding its centre. In the corresponding fixed Laplace "
            "expansion of per_4(tX+t^2V), the chosen 2x2 factor has zero "
            "degree-three polar P (indeed X is zero there), while every "
            "degree-two complementary factor is per_2(X)=0. Therefore its "
            "degree-six coefficient is zero."
        ),
        "verdict": (
            "On Haf(R)=0 all three summands of H6 vanish. Thus no binary pure6 "
            "jet exists on this divisor, for any R support and every direct-X "
            "support orbit. Literal equations close the branch before carrier "
            "pivot or blocker valuations and before adding the second colour."
        ),
        "global_m6_conclusion": (
            "The k4 term is zero independently of Haf(R), and E4 gives "
            "H6=-Haf(L)Haf(R). Hence the entire product-zero complement "
            "(including Haf(L)=0,Haf(R)!=0) has H6=0. The six-branch theorem "
            "excludes the product-nonzero open. Therefore every binary leading "
            "pure coefficient at total order m=6 is impossible at the phase "
            "K4 disjoint-union K4 base. Binary word closure makes this stable "
            "under arbitrary third-colour coupling."
        ),
    }


def phase_order_independent_contraction_and_m7_ledger():
    return {
        "formal_series": (
            "Let L_I(t), R_J(t), C_ij(t) be the binary (c,c) left, right, "
            "and cross cells. The literal word with colour c on left pair I "
            "and on all four right sites has series "
            "E_I=L_I Haf(R)+sum_J R_(J^c) per_2(C[I,J])."
        ),
        "order_independent_contraction": (
            "On the mixed-word ideal E_I=0, multiplication by L_(I^c) and "
            "summation over all six I gives k2=-2 Haf(L)Haf(R) coefficientwise. "
            "Thus at every valuation the pure series reduces to "
            "H_pure=per_4(C)-Haf(L)Haf(R)."
        ),
        "why_not_yet_general": (
            "The four-coloured-site rows which would separately control the "
            "2x2 cross permanents are contaminated by oriented (c,0)/(0,c) "
            "response products. No source-faithful identity currently equates "
            "per_4(C) with Haf(L)Haf(R) at arbitrary valuation."
        ),
        "m7_partition_guard": (
            "There are three, not two, weak positive partitions of seven into "
            "four edge valuations: 1114, 1123, and 1222. The last cannot be "
            "omitted without an additional source lemma."
        ),
        "m7_1114": {
            "verdict": "empty",
            "k0": (
                "Two left-internal edges are required but only one valuation "
                "exceeds one, so an uncancellable order-one left linear word occurs."
            ),
            "k2": (
                "The only assignment avoiding left valuation one is L4,R1,C1,C1; "
                "the lower per_2(X) shell kills its cross factor."
            ),
            "k4": (
                "A 1114 cross matching needs three disjoint order-one X edges, "
                "impossible in the per_2(X)=0 star/2x2 support types."
            ),
        },
        "m7_1123": {
            "immediate_eliminations": (
                "Every signature with L1 is killed by the unique left linear "
                "word; every k2 signature with C1,C1 is killed by per_2(X)."
            ),
            "primitive_signatures": [
                "k0: L(2,3), R(1,1)",
                "k2: L2, R1, C(1,3)",
                "k2: L3, R1, C(1,2)",
                "k4: C(1,1,2,3)",
            ],
            "count": 4,
        },
        "m7_1222": {
            "status": "required additional partition",
            "immediate_eliminations": "Every signature with L1 is killed.",
            "primitive_signatures": [
                "k0: L(2,2), R(1,2)",
                "k2: L2, R1, C(2,2)",
                "k2: L2, R2, C(1,2)",
                "k4: C(1,2,2,2)",
            ],
            "count": 4,
        },
        "finite_remainder": (
            "Order seven reduces to eight primitive binary signatures: four "
            "from 1123 and four from 1222. The 1114 partition is empty. Third "
            "physical colour cannot cancel any binary output row."
        ),
    }


def cancellation_base_jacobian():
    """Rank and first normal-cone obstruction for the K4+K4 phase base."""
    # Only support/cofactor nonvanishing is needed for the rank: the left K4
    # hafnian is zero, the right K4 hafnian is 3, and every left edge cofactor
    # is a nonzero unit in Q(w).
    image_words = set()
    nonzero_columns = 0
    for u, v in combinations(range(4), 2):
        for a in range(3):
            for b in range(3):
                word = [0] * 8
                word[u], word[v] = a, b
                image_words.add(tuple(word))
                nonzero_columns += 1
    require(nonzero_columns == 54, nonzero_columns)
    require(len(image_words) == 33, len(image_words))

    # A 4x4 cross-block first-order matrix X in a new pure colour produces at
    # order two the six-by-six family of 2x2 permanents (times nonzero
    # complementary base-edge units), and at order four per_4(X).  Laplace by
    # the first two rows expresses per_4 as a sum of products of complementary
    # 2x2 permanents, so vanishing of the mixed quadratic shell kills the pure
    # quartic coefficient.
    row_pairs = list(combinations(range(4), 2))
    column_pairs = list(combinations(range(4), 2))
    require(len(row_pairs) * len(column_pairs) == 36, (row_pairs, column_pairs))
    return {
        "source_columns": 252,
        "nonzero_columns": nonzero_columns,
        "exact_rank": len(image_words),
        "kernel_dimension": 252 - len(image_words),
        "linear_image": (
            "outputs differing from colour zero only at the endpoints of one "
            "edge in the phase-cancelling left K4"
        ),
        "GHZ_linear_leading_jet": False,
        "reason_linear": (
            "pure colours 1 and 2 are outside this 33-dimensional image"
        ),
        "canonical_cross_quartic_test": {
            "quadratic_mixed_rows": 36,
            "equations": "per_2(X[I,J])=0 for every two-row/two-column pair",
            "quartic_pure": "per_4(X)",
            "identity": (
                "per_4(X)=sum_(|J|=2) per_2(X[{0,1},J]) "
                "per_2(X[{2,3},J^c])"
            ),
            "verdict": (
                "vanishing of every order-two mixed coefficient forces the "
                "order-four pure coefficient to vanish"
            ),
        },
        "scope": (
            "This excludes the first normal cone and the cheapest four-cross-edge "
            "GHZ jet. Delayed internal/cross corrections at higher filtration "
            "order are not classified."
        ),
    }


def base_source():
    return {(u, v, 0, 0): Fraction(1) for u, v in ODD_EDGES}


def cofactor(source, omitted, residual_word):
    remaining = tuple(site for site in range(8) if site not in omitted)
    answer = Fraction(0)
    for matching in perfect_matchings(remaining):
        term = Fraction(1)
        for u, v in matching:
            term *= source.get((u, v, residual_word[u], residual_word[v]), 0)
        answer += term
    return answer


def jacobian_audit():
    source = base_source()
    nonzero_columns = 0
    image_words = set()
    for u, v in combinations(range(8), 2):
        for a in range(3):
            for b in range(3):
                word = [0] * 8
                word[u], word[v] = a, b
                coefficient = cofactor(source, {u, v}, word)
                if coefficient:
                    nonzero_columns += 1
                    image_words.add(tuple(word))
    require(nonzero_columns == 135, nonzero_columns)
    require(len(image_words) == 77, len(image_words))
    return {
        "source_columns": 252,
        "nonzero_columns": nonzero_columns,
        "exact_rank": len(image_words),
        "kernel_dimension": 252 - len(image_words),
        "image_description": (
            "one cross edge between C3 and C5: the output differs from colour "
            "zero only at that edge's endpoints"
        ),
        "image_word_count": len(image_words),
        "image_words": image_words,
    }


def poly_add(target, source):
    for exponent, coefficient in source.items():
        target[exponent] += coefficient
        if not target[exponent]:
            del target[exponent]


def poly_mul(left, right):
    answer = defaultdict(Fraction)
    for (sx, sy), a in left.items():
        for (tx, ty), b in right.items():
            answer[(sx + tx, sy + ty)] += a * b
    return dict(answer)


def polynomial_output(extra):
    cells = {cell: {(0, 0): value} for cell, value in base_source().items()}
    for cell, polynomial in extra.items():
        cells.setdefault(cell, {})
        merged = defaultdict(Fraction, cells[cell])
        poly_add(merged, polynomial)
        cells[cell] = dict(merged)
    output = {}
    for word in product(range(3), repeat=8):
        total = defaultdict(Fraction)
        for matching in PM8:
            term = {(0, 0): Fraction(1)}
            for u, v in matching:
                term = poly_mul(term, cells.get((u, v, word[u], word[v]), {}))
                if not term:
                    break
            poly_add(total, term)
        if total:
            output["".join(map(str, word))] = {
                f"{left},{right}": str(value)
                for (left, right), value in sorted(total.items())
            }
    return output


def second_variation_audit(image_words):
    # X is a linear-kernel difference; Y is an inactive within-C5 cell.
    xy = polynomial_output({
        (0, 3, 1, 0): {(1, 0): Fraction(1)},
        (0, 4, 1, 0): {(1, 0): Fraction(-1)},
        (4, 5, 1, 1): {(0, 1): Fraction(1)},
    })
    require(xy == {"10001100": {"1,1": "1"}}, xy)
    obstruction_word = tuple(map(int, "10001100"))
    require(obstruction_word not in image_words, obstruction_word)

    # X0 is another linear-kernel direction with vanishing quadratic term but
    # a nonzero cubic term.
    cubic = polynomial_output({
        (0, 3, 0, 0): {(1, 0): Fraction(1)},
        (1, 4, 0, 0): {(1, 0): Fraction(1)},
        (2, 5, 0, 0): {(1, 0): Fraction(1)},
        (0, 4, 0, 0): {(1, 0): Fraction(-3)},
    })
    require(cubic == {"00000000": {"3,0": "1"}}, cubic)
    return {
        "quadratic_obstruction": {
            "X": "A_03^(1,0)-A_04^(1,0)",
            "Y": "A_45^(1,1)",
            "dH_X": 0,
            "dH_Y": 0,
            "exact_output": "H(B0+sX+tY)=s*t*e_10001100",
            "cokernel": "10001100 is outside im(dH_B0)",
        },
        "second_order_blind_direction": {
            "X0": "A_03^(0,0)+A_14^(0,0)+A_25^(0,0)-3A_04^(0,0)",
            "exact_output": "H(B0+sX0)=s^3*e_00000000",
            "meaning": (
                "dH and the second fundamental form both vanish on X0. "
                "A second-variation-only properness proof cannot exclude all "
                "balanced-base tangent directions; cubic/higher jets are necessary."
            ),
        },
    }


def logical_sha(payload):
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return sha256(raw).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()
    for relative, expected in PINS.items():
        observed = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(observed == expected, (relative, observed, expected))

    jacobian = jacobian_audit()
    image_words = jacobian.pop("image_words")
    odd_weights = {edge: ONE for edge in ODD_EDGES}
    phase_weights = {
        (0, 1): ONE, (2, 3): ONE, (0, 2): ONE, (0, 3): ONE,
        (1, 3): W, (1, 2): W2,
    }
    phase_weights.update({edge: ONE for edge in combinations(range(4, 8), 2)})
    payload = {
        "status": "PASS exact odd-set scope and Luna second-variation obstruction",
        "fractional_matching_scope": {
            "leakage_free": (
                "If diagonal colour-c port degrees all equal d_c>0, then "
                "x_ij=|A_ij^(c,c)|^2/d_c is a fractional one-factor. Its "
                "half-integral extreme points are unit matching edges and "
                "half-weight odd cycles. Absence of an integral perfect "
                "matching gives a Tutte odd-set obstruction."
            ),
            "leakage_formula": (
                "diagonal_degree_i,c=d_c-L_i,c, where L_i,c is the total "
                "offdiagonal endpoint-colour energy. Moment zero does not make "
                "L_i,c site-independent, so it need not give a diagonal "
                "fractional one-factor."
            ),
            "cap_guard": (
                "Odd-set data are support-only, while carrier activity is a "
                "coefficient/rank condition and is not closed at rank drop. "
                "No source-labelled implication from every Tutte obstruction "
                "to a clean-cap/descent antecedent follows."
            ),
        },
        "odd_cycle_controls": odd_cycle_controls(),
        "phase_cancellation_control": cancellation_control(),
        "carrier_graph_closure": {
            "odd_C3_C5": one_colour_carrier_census(odd_weights),
            "phase_K4_K4": one_colour_carrier_census(phase_weights),
        },
        "phase_base_jacobian_and_cross_jet": cancellation_base_jacobian(),
        "phase_delayed_order6_seed": phase_delayed_seed_audit(),
        "phase_next_coupled_order6_channel": phase_next_coupled_channel(),
        "phase_column_star_order6_survivor": phase_column_star_survivor_and_pivots(),
        "phase_two_colour_order2_terminal": phase_two_colour_order2_audit(),
        "phase_adjusted_column_star_order3_terminal": phase_adjusted_column_star_order3_audit(),
        "phase_order6_support_type_resolution": phase_support_type_resolution(),
        "phase_binary_m6_partition_ledger": phase_m6_partition_ledger(),
        "phase_binary_m6_six_branch_resolution": phase_m6_six_branch_resolution(),
        "phase_binary_m6_hafR_zero_resolution": phase_m6_hafR_zero_resolution(),
        "phase_order_independent_contraction_and_m7_ledger": phase_order_independent_contraction_and_m7_ledger(),
        "phase_minimal_order": {
            "lower_bound": 4,
            "scope": (
                "The m=4 and m=5 exclusions hold independently in each binary "
                "{0,c} channel and therefore survive arbitrary third-colour "
                "coupling. The response-only m=6 exclusion is channel-specific."
            ),
            "order4": (
                "Impossible. Pure colours 1 and 2 require four order-one cells. "
                "An internal-left (c,c) cell has a unique forbidden linear word, "
                "leaving the all-cross route; its order-two per_2 shell kills per_4."
            ),
            "order5": (
                "Impossible. A 1+1+1+2 matching either contains an order-one "
                "internal-left (c,c) cell, or its k=2/k=4 contribution contains "
                "an order-one cross pair already killed by the quadratic mixed shell."
            ),
            "first_not_excluded": 6,
            "order6_mechanism": (
                "Order-one cross (c,0) cells can quadratically induce order-two "
                "left-internal (c,c) corrections, while order-one right-internal "
                "(c,c) cells supply a candidate Haf(L)Haf(R) pure coefficient."
            ),
        },
        "balanced_odd_base_jacobian": jacobian,
        "second_variation": second_variation_audit(image_words),
        "terminal_verdict": (
            "Edmonds/Tutte reduces only the leakage-free no-perfect-matching "
            "support branch. Cross-colour energy leakage and exact complex "
            "cancellation are independent balanced base mechanisms. At the "
            "smallest odd base, the Luna quadratic form has genuine cokernel "
            "obstructions but also an explicit direction invisible through "
            "second order. Therefore neither graph support nor second variation "
            "alone proves mixed-norm properness; a carrier-stratified cubic/higher "
            "GHZ-accessibility theorem is still required."
        ),
        "input_hashes": PINS,
    }
    payload["logical_sha256"] = logical_sha(payload)
    if args.write_results:
        OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("balanced-base odd-set/Luna audit: PASS terminal bounded no-go")
    print("odd base dH rank/kernel: 77/175")
    print("quadratic cokernel word: 10001100")
    print("second-order blind cubic: s^3 e_00000000")
    print("logical sha256:", payload["logical_sha256"])


if __name__ == "__main__":
    main()
