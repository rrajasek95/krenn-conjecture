#!/usr/bin/env python3
"""Refute common-edge realization of the minimal dirty outside signature.

For one physical pair p,q, a perfect matching uses either pq or sends p and
q to two residual sites.  Thus its capped response has only boundary degrees
0 and 2.  More sharply, every coefficient slice of the degree-two response
is a sum of two rank-one 3x3 matrices and has determinant zero.

The abstract guard of 00a1d52 asks for C2=-s*x with direct block I_3 and a
nonzero x.  At any live cell of x this would identify a rank-at-most-two
response slice with -I_3.  It also asks for a nonzero C6, which a physical
two-site cap cannot have.  For the guard's literal mixed one-factor x, the
actual pair-cap formula has zero projection to every pure residual word for
arbitrary star matrices, contradicting the three normalized pure rows.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
from itertools import combinations, permutations, product
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_essential_outside_derivative_dirty_cap_guard.py":
        "f64710b518f6da07a5596f67c45c58595dd0cd66a239202b3c46b4772b90b075",
    "notes/2026-08-14-essential-outside-derivative-dirty-cap-guard.md":
        "0c0a18f5300c724b1cbcf9e73396f08a37fb0e8159a47a54c58d6e90a4a66fb7",
    "notes/clean-pair-cap-exact-descent-target.md":
        "90f49ac4fde9b793409d9081977e7a7135ebd76c1b5df5d699387d142c2b9b75",
    "computations/verify_clean_pair_cap_exact_descent_symbolic.py":
        "d6507c2afa341ce5c15056feddf92b9a171e2a5c80652617b595c7c7cf35acf5",
}
EXPECTED_LEDGER_SHA256 = (
    "38b836999bda8978c7dfb85bdf9678bedb713292c5cb7a60c35596986bc2eb4e"
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
                ("pinned dirty-signature input changed", relative,
                 actual, expected))


def perfect_matchings(vertices):
    vertices = tuple(sorted(vertices))
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            yield tuple(sorted(((first, second),) + tail))


def boundary_degree_audit() -> dict[str, object]:
    vertices = tuple(range(8))
    cap_sites = frozenset((0, 1))
    histogram = {}
    direct = 0
    crossed = 0
    for matching in perfect_matchings(vertices):
        degree = sum(bool(set(edge) & cap_sites)
                     and not set(edge) <= cap_sites
                     for edge in matching)
        histogram[degree] = histogram.get(degree, 0) + 1
        if (0, 1) in matching:
            require(degree == 0, matching)
            direct += 1
        else:
            require(degree == 2, matching)
            crossed += 1
    require(histogram == {0: 15, 2: 90}
            and (direct, crossed) == (15, 90),
            (histogram, direct, crossed))
    return {
        "vertices": 8,
        "physical_cap_pair": "01",
        "perfect_matchings": direct + crossed,
        "boundary_degree_histogram": histogram,
        "physical_signature_layers": ["C0=s", "C2=r"],
        "identically_zero_layers": ["C4", "C6"],
        "first_guard_failure": (
            "the abstract nonzero C6 cannot be a two-site physical cap layer"
        ),
    }


def polynomial_add(*polynomials):
    answer = {}
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            answer[monomial] = answer.get(monomial, 0) + coefficient
            if not answer[monomial]:
                del answer[monomial]
    return answer


def polynomial_multiply(left, right):
    answer = {}
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            monomial = tuple(sorted(left_monomial + right_monomial))
            answer[monomial] = answer.get(monomial, 0) \
                + left_coefficient * right_coefficient
            if not answer[monomial]:
                del answer[monomial]
    return answer


def polynomial_scale(scalar, polynomial):
    return {monomial: scalar * coefficient
            for monomial, coefficient in polynomial.items()
            if scalar * coefficient}


def variable(name):
    return {(name,): 1}


def determinant(matrix):
    answer = {}
    for permutation in permutations(range(3)):
        inversions = sum(permutation[left] > permutation[right]
                         for left in range(3)
                         for right in range(left + 1, 3))
        term = {(): 1}
        for row, column in enumerate(permutation):
            term = polynomial_multiply(term, matrix[row][column])
        answer = polynomial_add(
            answer, polynomial_scale(-1 if inversions % 2 else 1, term)
        )
    return answer


def second_response_rank_identity() -> dict[str, object]:
    # A physical response coefficient at residual decorated cell ab;alpha,beta
    # has cap matrix
    #   M_ij=P_a(i,alpha)Q_b(j,beta)+P_b(i,beta)Q_a(j,alpha),
    # hence M=u*v^T+x*y^T.  Its determinant vanishes identically.
    u = tuple(variable(f"u{index}") for index in range(3))
    v = tuple(variable(f"v{index}") for index in range(3))
    x = tuple(variable(f"x{index}") for index in range(3))
    y = tuple(variable(f"y{index}") for index in range(3))
    matrix = tuple(tuple(polynomial_add(
        polynomial_multiply(u[row], v[column]),
        polynomial_multiply(x[row], y[column]),
    ) for column in range(3)) for row in range(3))
    determinant_polynomial = determinant(matrix)
    require(not determinant_polynomial, determinant_polynomial)

    identity = tuple(tuple(Q(int(row == column)) for column in range(3))
                     for row in range(3))
    identity_determinant = (
        identity[0][0] * identity[1][1] * identity[2][2]
    )
    require(identity_determinant == 1, identity)
    return {
        "physical_slice": "u*v^T+x*y^T",
        "symbolic_determinant_terms_after_cancellation": 0,
        "uniform_identity": (
            "det R_ab[alpha,beta]=0 for every residual decorated cell"
        ),
        "guard_required_slice": "-I_3 at each of 01;01,23;20,45;12",
        "guard_required_determinant": -1,
        "general_consequence": (
            "if r(K)=-s(K)*x and direct block D represents s, then "
            "x_ab(alpha,beta)^3*det(D)=0 cellwise"
        ),
        "guard_values": {"x_cell": 1, "det_direct_I3": 1},
        "realization_possible": False,
    }


def matrix_add(left, right):
    return tuple(tuple(a + b for a, b in zip(left_row, right_row, strict=True))
                 for left_row, right_row in zip(left, right, strict=True))


def outer(left, right):
    return tuple(tuple(a * b for b in right) for a in left)


def rational_matrix_rank(matrix) -> int:
    rows = [list(map(Q, row)) for row in matrix]
    rank_value = 0
    for column in range(len(rows[0])):
        pivot = next((row for row in range(rank_value, len(rows))
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[rank_value], rows[pivot] = rows[pivot], rows[rank_value]
        scale_value = rows[rank_value][column]
        rows[rank_value] = [entry / scale_value
                            for entry in rows[rank_value]]
        for row in range(len(rows)):
            if row == rank_value or not rows[row][column]:
                continue
            scale_value = rows[row][column]
            rows[row] = [entry - scale_value * pivot_entry
                         for entry, pivot_entry in
                         zip(rows[row], rows[rank_value], strict=True)]
        rank_value += 1
    return rank_value


def response(p_vectors, q_vectors, left, right):
    return matrix_add(
        outer(p_vectors[left], q_vectors[right]),
        outer(p_vectors[right], q_vectors[left]),
    )


def low_direct_rank_classification() -> dict[str, object]:
    zero = (Q(0), Q(0), Q(0))
    e0 = (Q(1), Q(0), Q(0))
    e1 = (Q(0), Q(1), Q(0))

    # Rank two is sharp for one edge.  The live response has independent
    # p- and q-spans.  Any third site cross-zero to both endpoints must have
    # p_c=q_c=0, so there cannot be a second live x edge.
    p_rank2 = (e0, e1, zero)
    q_rank2 = (e1, e0, zero)
    rank2_response = response(p_rank2, q_rank2, 0, 1)
    require(rational_matrix_rank(rank2_response) == 2
            and response(p_rank2, q_rank2, 0, 2)
            == response(p_rank2, q_rank2, 1, 2)
            == (zero, zero, zero),
            (rank2_response, p_rank2, q_rank2))

    # Rank one is sharp for two disjoint edges.  This is the exceptional
    # balanced normal form p1=lambda*p0, q1=lambda*q0.  Every outside site c
    # cross-zero to 0,1 is p_c=a_c*d, q_c=-a_c*e/(2lambda), so responses
    # among outside sites are -a_c*a_d/lambda times the same rank-one D.
    half = Q(1, 2)
    p_rank1 = (e0, e0, e0, tuple(-entry for entry in e0))
    q_rank1 = (tuple(half * entry for entry in e0),
               tuple(half * entry for entry in e0),
               tuple(-half * entry for entry in e0),
               tuple(half * entry for entry in e0))
    first_rank1 = response(p_rank1, q_rank1, 0, 1)
    second_rank1 = response(p_rank1, q_rank1, 2, 3)
    cross_rank1 = tuple(response(p_rank1, q_rank1, left, right)
                        for left in (0, 1) for right in (2, 3))
    require(rational_matrix_rank(first_rank1) == 1
            and first_rank1 == second_rank1
            and all(matrix == (zero, zero, zero) for matrix in cross_rank1),
            (first_rank1, second_rank1, cross_rank1))

    # A proposed third disjoint live edge uses two further nonzero parameters
    # a4,a5.  Since the second edge already has a2,a3 nonzero, every cross
    # coefficient -a_i*a_j/lambda is nonzero in a field.  In particular
    # B_24 cannot vanish.  This is the terminal support contradiction.
    parameters = {2: Q(1), 3: Q(-1), 4: Q(2), 5: Q(-3)}
    scalar_responses = {
        (left, right): -parameters[left] * parameters[right]
        for left in parameters for right in parameters if left < right
    }
    require(scalar_responses[(2, 3)]
            and scalar_responses[(4, 5)]
            and scalar_responses[(2, 4)], scalar_responses)

    return {
        "rank_3": {
            "maximum_live_x_edges": 0,
            "reason": "one response slice has rank at most two",
        },
        "rank_2": {
            "maximum_live_x_edges": 1,
            "sharp_one_edge_example_rank":
                rational_matrix_rank(rank2_response),
            "proof": (
                "a live rank-two B_ab makes p_a,p_b and q_a,q_b "
                "independent; B_ac=B_bc=0 then forces p_c=q_c=0"
            ),
        },
        "rank_1": {
            "maximum_live_x_edges": 2,
            "sharp_two_edge_example_ranks": [
                rational_matrix_rank(first_rank1),
                rational_matrix_rank(second_rank1),
            ],
            "exceptional_normal_form": (
                "p_c=a_c*d, q_c=-a_c*e/(2*lambda), "
                "B_cd=-(a_c*a_d/lambda)D"
            ),
            "three_edge_contradiction": (
                "B_23 and B_45 nonzero make a2,a3,a4,a5 nonzero, "
                "so the required cross-zero B_24 is nonzero"
            ),
        },
        "rank_0": {
            "maximum_live_x_edges_under_r_equals_minus_sx": "irrelevant",
            "reason": "s(K)=<K,D> is identically zero, so activity fails",
        },
        "three_disjoint_guard_edges_realizable_at_any_direct_rank": False,
        "field_scope": "characteristic zero (rank-one normal form uses 1/2)",
    }


def pure_row_unit_audit(guard) -> dict[str, object]:
    # Use the guard's literal internal x.  A physical pair cap has top tensor
    # s*x^3/6+r*x^2/2 for an arbitrary degree-two response r.  Enumerate every
    # one-cell monomial of a generic r and verify that no product with x^2 is
    # pure.  This retains all 135 response coordinates rather than imposing
    # the dirty C2 formula.
    x = guard.add(
        guard.decorated_edge(0, 1, 0, 1),
        guard.decorated_edge(2, 3, 2, 0),
        guard.decorated_edge(4, 5, 1, 2),
    )
    x_squared = guard.power(x, 2)
    x_cubed = guard.power(x, 3)
    require(x_cubed == {(0, 1, 2, 0, 1, 2): Q(6)}, x_cubed)

    response_coordinates = 0
    nonzero_products = 0
    full_words = set()
    for left, right in combinations(range(6), 2):
        for left_colour, right_colour in product(range(3), repeat=2):
            response_coordinates += 1
            monomial = guard.decorated_edge(
                left, right, left_colour, right_colour
            )
            contribution = guard.multiply(monomial, x_squared)
            if contribution:
                nonzero_products += 1
            for word in contribution:
                if -1 not in word:
                    full_words.add(word)
                    require(len(set(word)) > 1,
                            ("generic r*x^2 reached a pure word", word,
                             left, right, left_colour, right_colour))
    require(response_coordinates == 135
            and nonzero_products == 27
            and len(full_words) == 25,
            (response_coordinates, nonzero_products, len(full_words)))
    require(all(len(set(word)) > 1 for word in x_cubed), x_cubed)

    # At diagonal cap coordinate K_bb, contraction of the full GHZ target is
    # X_b, while the physical pair formula has pure coefficient zero for
    # arbitrary stars/response r.  These are three literal normalized pure
    # row contradictions 0=1.
    units = []
    for colour in range(3):
        units.append({
            "cap_covector": f"K_{colour}{colour}",
            "original_word": str(colour) * 8,
            "residual_word": str(colour) * 6,
            "physical_pair_cap_coefficient": 0,
            "GHZ_target_coefficient": 1,
            "equation": "0=1",
            "classification": "normalized pure source unit",
        })
    return {
        "internal_x": "01;01+23;20+45;12",
        "x_squared_terms": len(x_squared),
        "x_cubed": {"012012": 6},
        "generic_second_response_coordinates": response_coordinates,
        "nonzero_r_times_x_squared_cell_products": nonzero_products,
        "distinct_full_words_from_r_times_x_squared": len(full_words),
        "pure_words_from_physical_pair_cap": 0,
        "mixed_words_only": True,
        "terminal_units": tuple(units),
        "outcome": "source unit before any active-clean search",
    }


def exact_realization_verdict() -> dict[str, object]:
    return {
        "realization": "REFUTED",
        "obstruction_order": [
            "two-site boundary grading forces C4=C6=0",
            "second Hasse slice determinant det(u*v^T+x*y^T)=0",
            "full physical pair-cap top has no pure word for the guard x",
        ],
        "first_nonlinear_common_edge_identity": (
            "det R_ab[alpha,beta]=0; the dirty guard demands determinant -1"
        ),
        "terminal_alternative": (
            "the full GHZ contraction produces three normalized pure units; "
            "no active clean K is needed"
        ),
        "uniform_scope": (
            "the determinant no-go applies to any rank-three direct block "
            "and any nonzero x cell in a proposed identity r=-s*x"
        ),
        "remaining_outside_problem": (
            "general physical essential outside states need not satisfy the "
            "dirty normal form r=-s*x; after excluding this guard, one still "
            "must classify the actual rank-at-most-two response variety"
        ),
    }


def audit() -> dict[str, object]:
    pin_dependencies()
    guard = load(
        "computations/verify_uniform_essential_outside_derivative_dirty_cap_guard.py",
        "common_edge_dirty_guard",
    )
    # Re-run the abstract guard before refuting its common-edge realization.
    abstract = guard.full_ghz_compatible_guard()
    require(abstract["outside_column_rank"] == 3
            and abstract["every_clean_covector_inactive"], abstract)
    return {
        "theorem": "minimal dirty outside signature common-edge realization no-go",
        "pins": PINS,
        "two_site_boundary_grading": boundary_degree_audit(),
        "second_Hasse_rank_identity": second_response_rank_identity(),
        "direct_rank_classification": low_direct_rank_classification(),
        "full_GHZ_pure_row_test": pure_row_unit_audit(guard),
        "verdict": exact_realization_verdict(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("structural", "full", "exhaustive"),
                        default="structural")
    arguments = parser.parse_args()
    ledger = {"mode_independent": True, "audit": audit()}
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger changed", digest, EXPECTED_LEDGER_SHA256))
    print("N8 common-edge dirty-signature realization: PASS")
    print("mode", arguments.mode)
    print("realization: REFUTED")
    print("first nonlinear identity: every second-response slice has det 0")
    print("guard requires det(-I3)=-1")
    print("terminal: three normalized pure source units")
    print("sha256:", digest)


if __name__ == "__main__":
    main()
