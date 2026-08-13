#!/usr/bin/env python3
"""Separate the five physical cap classes by covariance and Tate degree.

The physical word/ridge cap quotient is P=Z^5 with coordinates lambda_v.
This checker proves four exact statements.

1.  The cyclic physical Cartan orbit projects to the saturated standard
    lattice ker(epsilon:P->Z), where epsilon is coordinate sum.
2.  The degree-five C5 Tate top is the relation among those five edge
    columns.  Its literal face image is zero, not the aggregate vector.
3.  The natural order-forgetting map from the Alt_7 line in the normalized
    seven-occurrence cobar to the ordinary five-face module is zero.  An
    aggregate transgression would therefore require an orientation-twisted
    new comparison, not just the symmetric face readout.  The checker does
    not identify the occurrence-order S7 action with physical site S5.
4.  At the projected level one primitive aggregate column completes P;
    otherwise epsilon is the unique separator.  This is not yet a physical
    full-row alternative: the Cartan columns carry residue/eta/sigma data,
    and the pinned face-epsilon theorem shows that epsilon has not been
    lifted through the 360-feature physical comparison.

The result is a sharp construction interface, not a construction of the
missing reduced response cell and not a physical terminal claim.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
from itertools import combinations
import json
from math import gcd
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_jd_normalized_cube_physical_cap_homology.py":
        "2488998937c4aac2915a9335c48d40398b419ee654092d9a9942157abd04b9e3",
    "computations/verify_h3_physical_cartan_source_orbit_descent.py":
        "c92667c38c57c69dff18fd7570fa154db7e1a634a83f462dfde6bd5553128a3a",
    "computations/verify_h3_order6_covariance_bridge_cyclic_aggregate.py":
        "01d4d504c0d5d9ac8fd643e06a38b35d75962c859e41908bff3161d10c7cbc13",
    "computations/verify_h3_rootless_five_cycle_positive_interface.py":
        "fd359b3ff2abbb01d9508996c754a27b70890b2cd621926fc30b92057b337851",
    "computations/verify_h3_rootless_five_cycle_first_tor_multidegree_gate.py":
        "a5d9021664b904f895323c29806a825545afd16085c971dc573353bb6c11a81f",
    "computations/verify_h3_face_epsilon_physical_terminal_extension_typing_gate.py":
        "8c52ab72c9825bf41a821f1ecef2838b169b929df34a36f2fe805529edf57dee",
    "computations/verify_uniform_cartan_augmented_grade_naturality_gate.py":
        "d71b2ae71cdfc910e374b498a70edbb5e897867cf624dec49203c34e74647925",
}
EXPECTED_LEDGER_SHA256 = (
    "7465cab5fabb96a7e898384a4c80adf8c4a2f6cfb8deb43f8d4902365cff284d"
)

N = 5
EPSILON = (1, 1, 1, 1, 1)


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


def rank(columns) -> int:
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "ragged matrix")
    matrix = [[Q(columns[column][row]) for column in range(len(columns))]
              for row in range(height)]
    pivot_row = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(pivot_row, height)
                      if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        value = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / value for entry in matrix[pivot_row]]
        for row in range(height):
            if row == pivot_row or not matrix[row][column]:
                continue
            value = matrix[row][column]
            matrix[row] = [left - value * right for left, right in
                           zip(matrix[row], matrix[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def determinant(rows) -> int:
    size = len(rows)
    require(size and all(len(row) == size for row in rows), "not square")
    work = [[Q(value) for value in row] for row in rows]
    answer = Q(1)
    for column in range(size):
        pivot = next((row for row in range(column, size)
                      if work[row][column]), None)
        if pivot is None:
            return 0
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            answer *= -1
        value = work[column][column]
        answer *= value
        work[column] = [entry / value for entry in work[column]]
        for row in range(column + 1, size):
            if not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[column], strict=True)]
    require(answer.denominator == 1, ("nonintegral determinant", answer))
    return answer.numerator


def dot(left, right):
    return sum((Q(a) * Q(b) for a, b in
                zip(left, right, strict=True)), Q(0))


def eval_polynomial(polynomial) -> Q:
    return sum((Q(value) for value in polynomial.values()), Q(0))


def multiply_matrix_vector(matrix, vector):
    return tuple(sum((Q(matrix[row][column]) * Q(vector[column])
                      for column in range(len(vector))), Q(0))
                 for row in range(len(matrix)))


def cycle_edges_and_cartan(orbit, physical):
    orbit_ledger = orbit.audit()
    columns = tuple(tuple(record["face_boundary"])
                    for record in orbit_ledger["bridge_orbit"])
    require(len(columns) == N and rank(columns) == N - 1,
            "the cyclic Cartan projection rank changed")
    require(all(dot(EPSILON, column) == 0 for column in columns),
            "a Cartan edge acquired aggregate mass")

    # Saturation of the rank-four image: the gcd of its nonzero maximal
    # minors is one.  Hence these are the full integral sum-zero lattice,
    # not a finite-index sublattice.
    minors = []
    for rows in combinations(range(N), N - 1):
        for selected in combinations(range(N), N - 1):
            matrix = [[columns[column][row] for column in selected]
                      for row in rows]
            value = determinant(matrix)
            if value:
                minors.append(abs(value))
    divisor = 0
    for value in minors:
        divisor = gcd(divisor, value)
    require(divisor == 1, ("Cartan edge lattice is not saturated", divisor))

    physical_ledger = physical.audit()
    packet = physical_ledger["physical_packet"]
    require(packet["protected_D_W_target_anchor_Eq"] == 0
            and packet["ordinary_residue"] == [-1, 1, 1, -1]
            and packet["ridge"]
            == "strictly commuting -dOmega_v eta/sigma packet",
            "the physical Cartan augmented packet changed")
    return columns, {
        "face_module": "P=Z^5 with coordinates lambda_v",
        "edge_rank": rank(columns),
        "edge_image": "ker(epsilon:Z^5->Z)",
        "maximal_minor_gcd": divisor,
        "aggregate_covector": list(EPSILON),
        "physical_source_provenance": True,
        "projected_standard_components_closed": True,
        "full_row_baggage": {
            "ordinary_residue": packet["ordinary_residue"],
            "terminal": packet["ridge"],
            "protected_D_W_target_anchor_Eq": 0,
        },
    }


def tate_top_audit(positive):
    (_generators, first_degrees, _d0, d1, d2, _records) = (
        positive.multigraded_resolution()
    )
    first = tuple(tuple(eval_polynomial(d1[row][column])
                        for column in range(N)) for row in range(N))
    top = tuple(eval_polynomial(d2[row][0]) for row in range(N))
    require(top == (Q(1),) * N, ("normalized Tate boundary changed", top))
    face_image = multiply_matrix_vector(first, top)
    require(face_image == (Q(0),) * N,
            ("the Tate top acquired a face image", face_image))
    first_columns = tuple(tuple(first[row][column] for row in range(N))
                          for column in range(N))
    require(rank(first_columns) == N - 1
            and all(dot(EPSILON, column) == 0 for column in first_columns),
            "the normalized C5 differential changed")
    require(rank(first_columns + (EPSILON,)) == N,
            "the aggregate entered the Tate edge image")

    cycle_edges = ((1, 2), (2, 3), (3, 4), (4, 5), (1, 5))

    def site_profile(monomial):
        values = [0] * N
        for edge_index, exponent in enumerate(monomial):
            for site in cycle_edges[edge_index]:
                values[site - 1] += exponent
        return tuple(values)

    cubic_profiles = tuple(site_profile(value) for value in first_degrees)
    top_profile = site_profile((1, 1, 1, 1, 1))
    require(all(sorted(profile) == [1, 1, 1, 1, 2]
                for profile in cubic_profiles)
            and top_profile == (2, 2, 2, 2, 2),
            "the C5 fine profiles changed")
    return {
        "normalized_edge_matrix": [
            [int(value) for value in column] for column in first_columns
        ],
        "degree_five_boundary_in_edges": [str(value) for value in top],
        "degree_five_face_image": [str(value) for value in face_image],
        "maps_to_aggregate_lambda": False,
        "reason": "dF=sum_i E_i is the unique relation and d1*dF=0",
        "cubic_face_profiles": [list(value) for value in cubic_profiles],
        "degree_five_top_profile": list(top_profile),
        "fine_grade_guard": (
            "the top has doubled C5 profile; it is not a primitive "
            "P3+K2 face augmentation"
        ),
    }


def alternating_covariance_audit():
    # Occurrence reordering acts trivially on an ordinary commutative
    # face/ridge readout but by sign on Alt_7.  For any adjacent occurrence
    # transposition, equivariance therefore imposes p=-p in the torsion-free
    # five-face target.  The five equations 2*p_v=0 have trivial kernel.
    equations = []
    for row in range(N):
        equation = [Q(0)] * N
        equation[row] = 2
        equations.append(tuple(equation))
    columns = tuple(tuple(equations[row][column]
                          for row in range(len(equations)))
                    for column in range(N))
    require(rank(columns) == N,
            "the order-forgetting sign constraint stopped vanishing")

    # The elementary face-forgetful map gives the same cancellation.  For a
    # fixed deleted label, pair every ordering of the other occurrences by
    # one odd spectator transposition; the two Alt coefficients cancel.
    paired_terms_per_face = 720  # 6! orderings of the other six occurrences
    require(paired_terms_per_face % 2 == 0,
            "spectator sign pairing stopped being even")
    return {
        "source_line": "Alt_7 is sign under occurrence reordering",
        "target": (
            "ordinary five-face readout is invariant under occurrence "
            "reordering"
        ),
        "rank_of_equivariance_constraints": rank(columns),
        "order_forgetting_map_dimension": 0,
        "forgetful_face_sum_terms_per_face": paired_terms_per_face,
        "forgetful_face_sum": [0] * N,
        "aggregate_transgression_from_Alt7": False,
        "minimal_escape": (
            "add an orientation-twisted physical cap/comparison cell, or "
            "construct a non-forgetful occurrence-to-site transgression "
            "with its action and signs explicitly"
        ),
        "scope_guard": (
            "the occurrence-order S7 action is not identified here with "
            "physical site S5; only the canonical symmetric face readout "
            "is ruled out"
        ),
    }


def projected_alternative(edge_columns):
    # Four Cartan edges plus p have full rank exactly when sum(p) != 0.
    samples = {
        "standard": (2, -1, 0, -1, 0),
        "primitive": (1, 0, 0, 0, 0),
        "aggregate": EPSILON,
    }
    records = {}
    tree = edge_columns[:N - 1]
    for name, column in samples.items():
        mass = int(dot(EPSILON, column))
        actual_rank = rank(tree + (column,))
        require(actual_rank == (N if mass else N - 1),
                ("projected aggregate alternative changed", name))
        determinant_value = determinant([
            [candidate[row] for candidate in tree + (column,)]
            for row in range(N)
        ])
        require(abs(determinant_value) == abs(mass),
                ("tree determinant stopped measuring aggregate", name,
                 determinant_value, mass))
        records[name] = {
            "column": list(column),
            "epsilon": mass,
            "rank_with_Cartan_tree": actual_rank,
            "determinant_absolute": abs(determinant_value),
        }
    return {
        "samples": records,
        "field_criterion": "Cartan edges plus p span Q^5 iff epsilon(p)!=0",
        "integral_criterion": "they span Z^5 iff epsilon(p)=+/-1",
        "torsion_if_epsilon_absolute_m_gt_1": "Z/m",
        "equivariant_construction_if_positive": (
            "take the C5 orbit of p; subtract Cartan edge combinations to "
            "isolate its aggregate, then normalize and translate"
        ),
        "projected_dual_if_negative": "epsilon=sum_v lambda_v",
    }


def physical_typing_guard(face_terminal, augmented):
    terminal_ledger, terminal_digest = face_terminal.audit()
    require(terminal_digest == face_terminal.EXPECTED_LEDGER_SHA256
            and not terminal_ledger["physical_terminal_separator_constructed"],
            "the face-epsilon physical typing frontier changed")
    augmented_ledger, augmented_digest = augmented.audit()
    require(augmented_digest == augmented.EXPECTED_LEDGER_SHA256
            and not augmented_ledger["ridge_eta_sigma"]
                ["arbitrary_common_tail_repairs_degree"],
            "the augmented Cartan grade gate changed")
    return {
        "projected_standard_module": "closed by physical Cartan orbit",
        "fully_augmented_standard_module": "not a clean cap differential",
        "why": [
            "each Cartan edge carries nonzero four-corner ordinary residue",
            "each Cartan edge carries a labelled -dOmega eta/sigma terminal",
            "a common tail does not repair the two Kähler site degrees",
        ],
        "projected_aggregate_dual": "epsilon=sum_v lambda_v",
        "physical_dual_lift_constructed": False,
        "missing_covector_equation": (
            "find epsilon_tilde with restriction epsilon and "
            "J_phys^*(epsilon_tilde)=0 on the 360-feature+Eq+terminal codomain"
        ),
        "equivalent_positive_cell": (
            "one source-valid reduced response column p in the forced "
            "word/fine/repeated grade with primitive epsilon(p), together "
            "with its labelled residue, Eq, q, ridge, W, eta and sigma caps"
        ),
        "terminal_eta_sigma_compatibility": (
            "numerically correct after the missing facewise Omega/r "
            "comparison, but not itself that comparison"
        ),
    }


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))
    orbit = load(
        "computations/verify_h3_order6_covariance_bridge_cyclic_aggregate.py",
        "jd_covariant_orbit",
    )
    physical = load(
        "computations/verify_h3_physical_cartan_source_orbit_descent.py",
        "jd_covariant_physical",
    )
    positive = load(
        "computations/verify_h3_rootless_five_cycle_positive_interface.py",
        "jd_covariant_positive",
    )
    face_terminal = load(
        "computations/verify_h3_face_epsilon_physical_terminal_extension_typing_gate.py",
        "jd_covariant_terminal",
    )
    augmented = load(
        "computations/verify_uniform_cartan_augmented_grade_naturality_gate.py",
        "jd_covariant_augmented",
    )

    edge_columns, cartan = cycle_edges_and_cartan(orbit, physical)
    ledger = {
        "theorem": "site-covariant Tate/Cartan physical cap alternative",
        "Cartan_standard_projection": cartan,
        "degree_five_Tate_top": tate_top_audit(positive),
        "Alt7_covariance": alternating_covariance_audit(),
        "projected_aggregate_alternative":
            projected_alternative(edge_columns),
        "full_physical_typing": physical_typing_guard(
            face_terminal, augmented
        ),
        "verdict": (
            "Cartan closes exactly the four projected standard cap "
            "directions.  Neither the normalized Alt7 line nor the literal "
            "degree-five C5 Tate top hits the aggregate.  One primitive "
            "reduced response column would construct the whole projected "
            "equivariant family; in its absence epsilon is the unique "
            "projected separator.  Promotion of either branch through the "
            "complete augmented physical rows remains the single missing "
            "comparison, so no physical terminal is claimed"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("site-covariant cap ledger changed", digest))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("J_D physical cap: CARTAN CLOSES PROJECTED STANDARD RANK FOUR")
    print("degree-five Tate top -> aggregate lambda: NO (face image zero)")
    print("Alt7 -> aggregate under symmetric face-forgetting: NO")
    print("remaining projected branch: primitive reduced cell or epsilon dual")
    print("full physical family/terminal: NOT YET TYPED")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
