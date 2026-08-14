#!/usr/bin/env python3
"""Audit the complete K8 Euler occurrence selector and its source descent.

Let H be the 105-term hafnian of the complete graph K8 and let f be one
perfect matching.  The four commuting logarithmic coordinate derivations

    E_e=x_e*d/dx_e,       e in f,

have product E_f(H)=m_f.  This checker constructs the entire four-cube and
the squarefree Spencer/Hasse packet

    d r[U] = sum_(S subset U) E_S(H-u) e[U-S].

The cube is flat: all 24 squares commute, all 24 paths to the top agree,
and the cubical cellular totalization has the ranks of a contractible
four-cube.  It is not a physical operation on the fixed source fibre.  The
first singleton packet already contains the nonzero normal H_e, which is
not in (H-u); the top diagonal-projection defect is m_f.  Thus the top is a
relative Spencer/KS carrier, not the pointed conormal P_f.

The final rank calculation distinguishes the full-K8 centered occurrence
normal c_f=105 dz_f-dZ from B=dZ-du and P_f=dz_f-du.  They have rank three.
Only after pulling back to du=0 and quotienting B do their shadows become
proportional, which forgets exactly the global pointed normalization needed
for a physical P_f cell.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "notes/h3-full-hasse-cone-d4-descent-obstruction.md":
        "2f13dbd315211b39da1a2b8026b40bb31c09bf6de0631cd3dc896689126ee2c7",
    "notes/h3-universal-response-deformation-e14-orbit-ks-gate.md":
        "d9032c365e8fd8fb5baf320dcc5adac8832c023119fb7d4df69d02cce3d5878f",
    "notes/h3-centered-pointed-face-existing-conormal-cap-terminal-gate.md":
        "9f41f22cc232beefca120c770c5815faa2aff0b80c738069cfd18a5c3557fa17",
    "notes/h3-jd-hasse-bianchi-totalization-uniform-spectator-gate.md":
        "8704921ca24946c17703ea1f8f2c92f557d5028c7e44c9fb18faa2c99420bf52",
}
EXPECTED_LEDGER_SHA256 = (
    "e54d9752e616c692bbdd2c55c8081f7b9cb7e18282c6a68d099016787fd0cd87"
)

SITES = tuple(range(8))
TARGET = ("u",)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def edge(left: int, right: int) -> tuple[int, int]:
    require(left != right, ("loop", left, right))
    return (left, right) if left < right else (right, left)


def perfect_matchings(vertices):
    vertices = tuple(sorted(vertices))
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position, second in enumerate(vertices[1:], start=1):
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            answer.append(tuple(sorted((edge(first, second),) + tail)))
    return tuple(answer)


def subsets(values):
    values = tuple(values)
    return tuple(item for size in range(len(values) + 1)
                 for item in combinations(values, size))


def add(*polynomials):
    answer = {}
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            answer[monomial] = answer.get(monomial, Q(0)) + Q(coefficient)
    return {monomial: coefficient for monomial, coefficient in answer.items()
            if coefficient}


def scale(coefficient, polynomial):
    coefficient = Q(coefficient)
    return {monomial: coefficient * Q(value)
            for monomial, value in polynomial.items()
            if coefficient * Q(value)}


def euler(polynomial, selected_edge):
    """Apply x_e*d/dx_e; every matching monomial is squarefree."""
    return {
        monomial: coefficient
        for monomial, coefficient in polynomial.items()
        if monomial != TARGET and selected_edge in monomial
    }


def euler_subset(polynomial, directions, selected):
    answer = polynomial
    for index in selected:
        answer = euler(answer, directions[index])
    return answer


def ordinary_derivative(polynomial, selected_edge):
    answer = {}
    for monomial, coefficient in polynomial.items():
        if monomial == TARGET or selected_edge not in monomial:
            continue
        residual = list(monomial)
        residual.remove(selected_edge)
        residual = tuple(residual)
        answer[residual] = answer.get(residual, Q(0)) + coefficient
    return answer


def derivative_subset(polynomial, directions, selected):
    answer = polynomial
    for index in selected:
        answer = ordinary_derivative(answer, directions[index])
    return answer


def vector_rank(columns) -> int:
    if not columns:
        return 0
    rows = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(len(columns[0]))]
    pivot_row = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(pivot_row, len(rows))
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        value = rows[pivot_row][column]
        rows[pivot_row] = [entry / value for entry in rows[pivot_row]]
        for row in range(len(rows)):
            if row == pivot_row or not rows[row][column]:
                continue
            value = rows[row][column]
            rows[row] = [left - value * right for left, right in
                         zip(rows[row], rows[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def polynomial_rank(polynomials, basis) -> int:
    return vector_rank(tuple(tuple(polynomial.get(item, Q(0))
                                   for item in basis)
                             for polynomial in polynomials))


def dot(left, right):
    return sum((Q(a) * Q(b) for a, b in
                zip(left, right, strict=True)), Q(0))


def cube_cells(dimension: int, degree: int):
    """Oriented cubical cells (free coordinates, fixed 0/1 assignment)."""
    answer = []
    for free in combinations(range(dimension), degree):
        complement = tuple(index for index in range(dimension)
                           if index not in free)
        for bits in product((0, 1), repeat=len(complement)):
            answer.append((free, tuple(zip(complement, bits, strict=True))))
    return tuple(answer)


def cubical_boundary(cell):
    free, fixed = cell
    fixed = dict(fixed)
    answer = {}
    for position, direction in enumerate(free):
        smaller_free = tuple(item for item in free if item != direction)
        sign = Q(-1 if position % 2 else 1)
        for endpoint, endpoint_sign in ((1, Q(1)), (0, Q(-1))):
            assignment = dict(fixed)
            assignment[direction] = endpoint
            target = (smaller_free, tuple(sorted(assignment.items())))
            answer[target] = answer.get(target, Q(0)) + sign * endpoint_sign
    return {target: coefficient for target, coefficient in answer.items()
            if coefficient}


def cubical_totalization_audit():
    cells = tuple(cube_cells(4, degree) for degree in range(5))
    dimensions = [len(items) for items in cells]
    require(dimensions == [16, 32, 24, 8, 1], dimensions)
    boundaries = []
    ranks = []
    for degree in range(1, 5):
        target_lookup = {cell: index for index, cell in
                         enumerate(cells[degree - 1])}
        columns = []
        for cell in cells[degree]:
            column = [Q(0)] * len(cells[degree - 1])
            for target, coefficient in cubical_boundary(cell).items():
                column[target_lookup[target]] = coefficient
            columns.append(tuple(column))
        boundaries.append(tuple(columns))
        ranks.append(vector_rank(tuple(columns)))
    require(ranks == [15, 17, 7, 1], ranks)

    for degree in range(2, 5):
        lower = cells[degree - 2]
        lower_lookup = {cell: index for index, cell in enumerate(lower)}
        for cell in cells[degree]:
            twice = [Q(0)] * len(lower)
            for middle, first_coefficient in cubical_boundary(cell).items():
                for target, second_coefficient in cubical_boundary(middle).items():
                    twice[lower_lookup[target]] += (
                        first_coefficient * second_coefficient
                    )
            require(not any(twice), ("cubical boundary squared", degree, cell))
    return {
        "cell_dimensions_C0_to_C4": dimensions,
        "boundary_ranks_d1_to_d4": ranks,
        "homology": {"H0": 1, "positive": 0},
        "contractible_augmented_four_cube": True,
        "cellular_d_squared": 0,
    }


def hasse_packet(polynomial, directions, selected):
    """Boundary of the squarefree Hasse row r[selected]."""
    selected = tuple(sorted(selected))
    packet = {}
    for derived in subsets(selected):
        jet = tuple(item for item in selected if item not in derived)
        packet[jet] = euler_subset(polynomial, directions, derived)
    return {jet: coefficient for jet, coefficient in packet.items()
            if coefficient}


def prolong_packet(packet, directions, direction):
    """Product-rule prolongation J_i(p e[V])=E_i(p)e[V]+p e[V+i]."""
    answer = {}
    for jet, coefficient in packet.items():
        require(direction not in jet, ("repeated Hasse direction", direction))
        answer[jet] = add(answer.get(jet, {}),
                          euler(coefficient, directions[direction]))
        raised = tuple(sorted(jet + (direction,)))
        answer[raised] = add(answer.get(raised, {}), coefficient)
    return {jet: coefficient for jet, coefficient in answer.items()
            if coefficient}


def selector_and_hasse_audit():
    matchings = perfect_matchings(SITES)
    require(len(matchings) == len(set(matchings)) == 105,
            "the complete K8 matching count changed")
    h = {matching: Q(1) for matching in matchings}
    f = tuple((2 * index, 2 * index + 1) for index in range(4))
    require(f in h, ("selected perfect matching missing", f))
    directions = f
    source_equation = add(h, {TARGET: Q(-1)})
    all_subsets = subsets(range(4))

    expected_support_by_order = {0: 105, 1: 15, 2: 3, 3: 1, 4: 1}
    support = {}
    for selected in all_subsets:
        image = euler_subset(h, directions, selected)
        support[selected] = len(image)
        require(len(image) == expected_support_by_order[len(selected)],
                ("Euler support changed", selected, len(image)))
        for direction in selected:
            require(euler(image, directions[direction]) == image,
                    ("Euler idempotence changed", selected, direction))

    top = euler_subset(h, directions, range(4))
    selected_monomial = {f: Q(1)}
    require(top == selected_monomial, ("top failed to select m_f", top))
    third_faces = tuple(euler_subset(h, directions, selected)
                        for selected in combinations(range(4), 3))
    require(all(image == selected_monomial for image in third_faces),
            "three fixed matching edges stopped forcing the fourth")

    directed_edges = 0
    for selected in all_subsets:
        for direction in range(4):
            if direction in selected:
                continue
            image = euler_subset(source_equation, directions, selected)
            target = euler_subset(
                source_equation, directions,
                tuple(sorted(selected + (direction,))))
            require(euler(image, directions[direction]) == target,
                    ("cube edge changed", selected, direction))
            directed_edges += 1
    require(directed_edges == 32, directed_edges)

    squares = 0
    for left, right in combinations(range(4), 2):
        residual = tuple(index for index in range(4)
                         if index not in (left, right))
        for base in subsets(residual):
            image = euler_subset(source_equation, directions, base)
            lr = euler(euler(image, directions[left]), directions[right])
            rl = euler(euler(image, directions[right]), directions[left])
            require(lr == rl, ("Euler square curvature", base, left, right))
            squares += 1
    require(squares == 24, squares)

    path_tops = []
    top_packets = []
    for order in permutations(range(4)):
        image = source_equation
        packet = {(): source_equation}
        for direction in order:
            image = euler(image, directions[direction])
            packet = prolong_packet(packet, directions, direction)
        path_tops.append(image)
        top_packets.append(packet)
    direct_top_packet = hasse_packet(source_equation, directions, range(4))
    require(all(image == selected_monomial for image in path_tops)
            and all(packet == direct_top_packet for packet in top_packets),
            "the 24 Hasse paths stopped agreeing")
    require(len(direct_top_packet) == 16
            and direct_top_packet[()] == selected_monomial
            and direct_top_packet[tuple(range(4))] == source_equation,
            "the top 16-face Hasse packet changed")

    all_packets = {selected: hasse_packet(source_equation, directions, selected)
                   for selected in all_subsets}
    require(sum(len(packet) for packet in all_packets.values()) == 81,
            "the full squarefree Hasse packet stopped having 3^4 faces")
    first_faces = tuple(all_packets[(direction,)][()]
                        for direction in range(4))
    require(all(len(face) == 15 for face in first_faces),
            "the first Euler normal stopped being a 15-term partial hafnian")

    # The pure derivative D4 has the same Boolean shape but a different top:
    # it removes all four matching variables and returns the unit.  The Euler
    # cube retains m_f, and its fourth coefficient step is redundant.
    pure_d4_top = derivative_subset(h, directions, range(4))
    require(pure_d4_top == {(): Q(1)}, pure_d4_top)

    return {
        "hafnian": "H=Haf(K8)",
        "hafnian_terms": len(h),
        "selected_matching": [list(item) for item in f],
        "operator": "product_(e in f) (x_e d/dx_e)",
        "support_by_selected_edge_count": expected_support_by_order,
        "selector_identity": "E_f(H)=m_f",
        "order_three_already_selects_m_f": True,
        "order_four_new_coefficient_information": False,
        "cube_vertices": len(all_subsets),
        "cube_directed_edges": directed_edges,
        "cube_squares": squares,
        "square_curvature": 0,
        "paths_from_bottom_to_top": len(path_tops),
        "all_path_composites": "m_f",
        "hasse_row_generators": len(all_packets),
        "hasse_boundary_module_terms": sum(
            len(packet) for packet in all_packets.values()),
        "top_hasse_boundary_terms": len(direct_top_packet),
        "top_scalar_face": "m_f",
        "first_scalar_faces": {
            "number": len(first_faces),
            "terms_each": sorted({len(face) for face in first_faces}),
            "description": "H_e=sum of the 15 matchings containing e",
        },
        "pure_derivative_D4_top": "1",
        "Euler_D4_top": "m_f",
    }, h, f, directions, source_equation, all_packets


def fixed_fibre_descent_audit(h, f, directions, source_equation, packets):
    basis = tuple(sorted(h)) + (TARGET,)
    nonmembership_ranks = {}
    for selected in subsets(range(4)):
        if not selected:
            continue
        normal = euler_subset(source_equation, directions, selected)
        rank = polynomial_rank((source_equation, normal), basis)
        require(rank == 2, ("a positive Euler face entered (H-u)", selected))
        nonmembership_ranks["".join(map(str, selected))] = rank

    # In the homogeneous ring deg(u)=4, membership of another degree-four
    # polynomial in the principal ideal (H-u) would force scalar
    # proportionality.  The exact rank-two calculation rules this out for
    # all fifteen positive faces.  The same support argument works on H=0.
    zero_target_ranks = []
    h_basis = tuple(sorted(h))
    for selected in subsets(range(4)):
        if not selected:
            continue
        normal = euler_subset(h, directions, selected)
        zero_target_ranks.append(polynomial_rank((h, normal), h_basis))
    require(set(zero_target_ranks) == {2}, zero_target_ranks)

    # Audit the literal normalized fibre H=1 as well.  If a nonzero H_e
    # belonged to (H-1), comparison of highest degrees in the polynomial
    # domain would force the quotient to be constant; its constant term
    # would then force that constant to vanish.  The rank/support check
    # supplies the exact nonzero endpoint of this argument.
    normalized_equation = add(h, {(): Q(-1)})
    normalized_basis = tuple(sorted(h)) + ((),)
    normalized_ranks = []
    for selected in subsets(range(4)):
        if not selected:
            continue
        normal = euler_subset(normalized_equation, directions, selected)
        normalized_ranks.append(polynomial_rank(
            (normalized_equation, normal), normalized_basis))
    require(set(normalized_ranks) == {2}, normalized_ranks)

    singleton_defects = tuple(packets[(direction,)][()]
                              for direction in range(4))
    top_defect = packets[tuple(range(4))][()]
    require(all(len(item) == 15 for item in singleton_defects)
            and top_defect == {f: Q(1)},
            "the diagonal Spencer projection defect changed")

    return {
        "fixed_source_equation": "F=H-u",
        "tangent_descent_condition": "E_e(F) in (F)",
        "positive_face_pair_ranks_with_F": nonmembership_ranks,
        "all_positive_faces_outside_source_ideal": True,
        "zero_target_equation_H_same_verdict": True,
        "normalized_pure_target_equation_H_minus_1_same_verdict": True,
        "first_nonphysical_packet": "d r[e]=F e[e]+H_e e[empty]",
        "first_nonphysical_face_terms": 15,
        "first_diagonal_projection_defect": "H_e e[empty]",
        "top_diagonal_projection_defect": "m_f e[empty]",
        "formal_two_face_curvature": 0,
        "interpretation": (
            "the formal connection is flat, but its normal one-form is "
            "already nonzero; flatness does not imply tangency to the fibre"
        ),
        "product_operator_descends_to_fixed_source_quotient": False,
    }


def pointed_occurrence_audit():
    # Coordinates are (dz_f,dZ,du), where Z is the sum of all 105 complete
    # K8 occurrence coordinates.  B is the complete response normal, c is
    # the centered occurrence normal, and P is the old pointed conormal.
    n = Q(105)
    raw = (Q(1), Q(0), Q(0))
    total = (Q(0), Q(1), Q(0))
    target = (Q(0), Q(0), Q(1))
    symmetric = (Q(0), Q(1), Q(-1))
    centered = (n, Q(-1), Q(0))
    pointed = (Q(1), Q(0), Q(-1))
    scale_tangent = (Q(1), Q(1), Q(1))

    require(tuple(n * value for value in raw)
            == tuple(left + right for left, right in
                     zip(centered, total, strict=True)),
            "raw/centered occurrence decomposition changed")
    require(tuple(centered[index] + symmetric[index] for index in range(3))
            == tuple(n * pointed[index] + (n - 1) * target[index]
                     for index in range(3)),
            "centered/pointed/global-target relation changed")
    require(vector_rank((symmetric, pointed)) == 2
            and vector_rank((symmetric, pointed, centered)) == 3,
            "the full-K8 pointed conormal rank changed")
    require(dot(symmetric, scale_tangent) == 0
            and dot(pointed, scale_tangent) == 0
            and dot(centered, scale_tangent) == 104,
            "the full-K8 scale tangent certificate changed")

    # Pulling back to du=0 gives B=dZ; quotienting by B leaves only dz_f.
    # In that information-losing quotient c=105 dz_f and P=dz_f.
    centered_strict_fixed_quotient = (n,)
    pointed_strict_fixed_quotient = (Q(1),)
    require(centered_strict_fixed_quotient
            == tuple(n * value for value in pointed_strict_fixed_quotient),
            "the strict fixed-fibre shadow changed")

    return {
        "coordinate_order": ["dz_f", "dZ", "du"],
        "complete_K8_occurrences": int(n),
        "raw_Euler_top": [1, 0, 0],
        "complete_response_normal_B": [0, 1, -1],
        "centered_c_f": [105, -1, 0],
        "pointed_P_f": [1, 0, -1],
        "rank_B_Pf_then_cf": [2, 3],
        "common_scale_tangent": [1, 1, 1],
        "tangent_values": {"B": 0, "P_f": 0, "c_f": 104},
        "exact_relation": "c_f+B=105 P_f+104 du",
        "relative_KS_class": "raw occurrence minus response mean = c_f/105",
        "strict_du_zero_B_quotient": "c_f=105 P_f",
        "strict_fixed_fibre_shadow_coincides": True,
        "strict_shadow_constructs_global_pointed_cell": False,
        "reason": (
            "the pullback kills the independent global-target scale detected "
            "by (1,1,1); source-valid P_f must retain the -du face"
        ),
    }


def audit():
    pins = {}
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, ("pinned source artifact changed",
                                     relative, actual, expected))
        pins[relative] = actual

    selector, h, f, directions, source_equation, packets = (
        selector_and_hasse_audit()
    )
    return {
        "theorem": "complete K8 squarefree Euler cube fixed-fibre gate",
        "pins": pins,
        "selector_and_hasse_cube": selector,
        "cubical_cellular_totalization": cubical_totalization_audit(),
        "fixed_fibre_descent": fixed_fibre_descent_audit(
            h, f, directions, source_equation, packets),
        "occurrence_pointed_comparison": pointed_occurrence_audit(),
        "D4_comparison": {
            "common_structure": (
                "both have a full Boolean Hasse packet and require every "
                "proper product-rule face"
            ),
            "pure_fourth_derivative": "partial_f H=1",
            "fourth_Euler_composite": "E_f H=m_f",
            "old_D4_diagonal_defect": "(H0-u)e0 for its special cycle",
            "Euler_row_diagonal_defect": "m_f e0 at the top, H_e e0 first",
            "same_physical_cell": False,
            "reason": (
                "the old D4 uses a direct-free mixed/pure two-row target "
                "cone; this exact audit uses the 105-term complete pure K8 "
                "row and supplies neither the moving target nor its -du face"
            ),
        },
        "verdict": {
            "order_four_Euler_cube_is_formally_flat": True,
            "order_four_Euler_cube_is_physical_P_f": False,
            "best_exact_interpretation": (
                "a relative occurrence Spencer/KS carrier with top m_f"
            ),
            "first_missing_physical_input": (
                "a source-labelled singleton lift of each 15-term H_e normal, "
                "coherently totalized with the global target/anchor -du face"
            ),
        },
        "scope": {
            "exact_complete_object": (
                "the 105-term complete K8 hafnian and its pure target "
                "normalization H-u"
            ),
            "all_16_Hasse_rows_checked": True,
            "all_32_edges_checked": True,
            "all_24_squares_checked": True,
            "all_3_pow_4_product_rule_faces_checked": True,
            "literal_normalized_pure_target_H_equals_1_checked": True,
            "other_pure_colour_targets_checked": False,
            "full_3_pow_8_word_system_checked": False,
            "full_GHZ_source_tensor_constructed": False,
            "logical_force": (
                "failure to preserve even H-u rules out the uncorrected "
                "Euler cube as an endomorphism of any fuller source quotient; "
                "it does not rule out a new relative physical correction"
            ),
        },
    }


def main() -> None:
    ledger = audit()
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("K8 Euler cube ledger changed", digest))
    print("complete K8 squarefree Euler cube: PASS")
    print("E_f Haf(K8)=m_f; 16 vertices, 32 edges, 24 flat squares")
    print("first fixed-fibre defect: 15-term H_e; top defect: m_f")
    print("order-four Euler cube: RELATIVE KS CARRIER, NOT PHYSICAL P_f")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
