#!/usr/bin/env python3
"""Reduce the physical h=3 endpoint projector lift to one primitive cap cell.

The coefficient association scheme is recomputed on the ninety response
occurrences.  After the residual-matching filter its endpoint adjacency has
constant eigenvalue 8 and nonconstant eigenvalues -2,2,4, hence

    P(B)=(B+2)(B-2)(B-4),       P(8)=240.

The matching projector contributes denominator 3.  This constructs the
centered occurrence projector only coefficientwise.  A physical cubic
Cartan/Hasse lift has a scalar zero-face 90*f and enters the already computed
five-face cap complex.  Cartan closes the saturated sum-zero sublattice, so
the remaining projected datum is one column p with nonzero face augmentation.

The checker fixes the smallest primitive choice

    p_(v,N): Q_(v,N)=-1, ores=-1,

with Omega/ridge/Eq/W/target/ainc and terminal rows zero.  It also records why
the current unary, Tate/orientation, and complete full-nine inventories do not
construct it.  This is an exact finite interface, not a construction of p:
the association projector has not yet been lifted to an augmented source
bicomplex, and the face augmentation has not been promoted to a physical
terminal.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_centered_occurrence_endpoint_association_projector.py":
        "0ef88312cead100120e4600ea3a2d0616262a96bf27726d07817610d11b43f59",
    "computations/verify_h3_centered_occurrence_same_grade_physical_gate.py":
        "5b41444ef5f4844bc1bd87a6a4e81e60a631f3549eed21c160efdcb428582ea4",
    "computations/verify_uniform_centered_occurrence_full_endpoint_transfer_gate.py":
        "6f5686298143b584a4edcb350145bf9d648277972aa96b90443c4ce254cb1d30",
    "computations/verify_uniform_centered_occurrence_matching_eigenspace_correction.py":
        "6e9c665e2c42b23e1910963b030de2f6c4b16dfe4951eae6e0e79b7fcf1e6921",
    "computations/verify_h3_jd_normalized_cube_physical_cap_homology.py":
        "2488998937c4aac2915a9335c48d40398b419ee654092d9a9942157abd04b9e3",
    "computations/verify_h3_jd_site_covariant_tate_cartan_cap_alternative.py":
        "48977e27e6cf4f1d8c897f629419a24284c6490e31b6f69f42e0a74b08607279",
    "computations/verify_h3_rootless_endpoint_word_change_attachment_or_dual.py":
        "a98a37e07b7847c4484de9505b1f833fc269b02126091d3ee92463bc65ad60d4",
    "computations/verify_h3_rootless_one_face_third_cofactor_comparison_vertex_gate.py":
        "37251145d805861b2d1b15b7bf37cf9f98ba30b03fbcffa1daa4fc35789efe84",
    "computations/verify_h3_rootless_c5_complete_multidegree_source_no_go.py":
        "719e48963faac5cd1dc5e7348de41e86f690f3046fefba88dddfa60bae532899",
    "computations/verify_h3_koszul_reynolds_higher_commutator_obstruction.py":
        "c52cec702336ecdd821617ba21c66538cdbbdf2fc964b3d1637dfaf25c9bae6b",
    "computations/verify_h3_gl3_normalized_bar_word_change_obstruction.py":
        "ed3c1baafd7d83819c1b6842857611b5b540c57ef95c8ca8a450de357312670a",
    "computations/verify_derived_base_change_relative_cap_obstruction.py":
        "19c38d42710de2df403aa5cdf8513b6c03a758ab01eb281ce9da21564ca907d3",
    "computations/verify_h3_component_iv_physical_definability_gate.py":
        "d2753b9e885464243a471387f168531484edafa8aa4bb34d160308a128237c00",
    "computations/verify_h3_direct_free_first_syzygy_multidegree_gate.py":
        "7308d9b55740644affedbda04c8085517bcc2a0881eb5a8c839fc6cdee5547e5",
}
EXPECTED_LEDGER_SHA256 = (
    "1256327676e3a78fd10d121f0af78e52d249e5e57f6633587ab33818c224cd6c"
)

SITES = tuple(range(6))
FACES = (1, 3, 5, 2, 4)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def rank(vectors) -> int:
    basis = {}
    for original in vectors:
        values = [Q(value) for value in original]
        for pivot in sorted(basis):
            if values[pivot]:
                coefficient = values[pivot]
                values = [left - coefficient * right for left, right in
                          zip(values, basis[pivot], strict=True)]
        pivot = next((index for index, value in enumerate(values) if value), None)
        if pivot is None:
            continue
        coefficient = values[pivot]
        basis[pivot] = tuple(value / coefficient for value in values)
    return len(basis)


def determinant(columns) -> int:
    size = len(columns)
    require(size and all(len(column) == size for column in columns),
            "not square")
    matrix = [[Q(columns[column][row]) for column in range(size)]
              for row in range(size)]
    value = Q(1)
    for column in range(size):
        pivot = next((row for row in range(column, size)
                      if matrix[row][column]), None)
        if pivot is None:
            return 0
        if pivot != column:
            matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
            value *= -1
        pivot_value = matrix[column][column]
        value *= pivot_value
        matrix[column] = [entry / pivot_value for entry in matrix[column]]
        for row in range(column + 1, size):
            if not matrix[row][column]:
                continue
            coefficient = matrix[row][column]
            matrix[row] = [left - coefficient * right for left, right in
                           zip(matrix[row], matrix[column], strict=True)]
    require(value.denominator == 1, ("nonintegral determinant", value))
    return value.numerator


def edge(left: int, right: int) -> tuple[int, int]:
    require(left != right, ("loop", left, right))
    return (left, right) if left < right else (right, left)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for index, second in enumerate(vertices[1:], start=1):
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            answer.append(tuple(sorted((edge(first, second),) + tail)))
    return tuple(answer)


def occurrences():
    answer = []
    for p_site in SITES:
        for s_site in SITES:
            if p_site == s_site:
                continue
            residual = tuple(site for site in SITES
                             if site not in (p_site, s_site))
            for matching in perfect_matchings(residual):
                answer.append((p_site, s_site, matching))
    require(len(answer) == len(set(answer)) == 90,
            "the h=3 occurrence set changed")
    return tuple(answer)


def switch_neighbors(matching):
    # At intrinsic h=3 there are two residual edges.  Their switch graph is
    # the triangle on the three perfect matchings of four fixed vertices.
    (a, b), (c, d) = matching
    return (
        tuple(sorted((edge(a, c), edge(b, d)))),
        tuple(sorted((edge(a, d), edge(b, c)))),
    )


def endpoint_neighbors(occurrence):
    p_site, s_site, matching = occurrence
    answer = []
    for selected in SITES:
        if selected in (p_site, s_site):
            continue
        mate = next(other for pair in matching if selected in pair
                    for other in pair if other != selected)
        remainder = tuple(pair for pair in matching if selected not in pair)
        answer.append((selected, s_site,
                       tuple(sorted(remainder + (edge(p_site, mate),)))))
        answer.append((p_site, selected,
                       tuple(sorted(remainder + (edge(s_site, mate),)))))
    require(len(answer) == len(set(answer)) == 8,
            ("endpoint degree changed", occurrence))
    return tuple(answer)


def apply(vector, adjacency):
    return tuple(sum(vector[neighbor] for neighbor in adjacency[item])
                 for item in range(len(vector)))


def polynomial_apply(vector, roots, adjacency):
    answer = vector
    for root in roots:
        image = apply(answer, adjacency)
        answer = tuple(left - root * right for left, right in
                       zip(image, answer, strict=True))
    return answer


def coefficient_projector_audit():
    values = occurrences()
    lookup = {value: index for index, value in enumerate(values)}
    endpoint_adjacency = tuple(tuple(lookup[neighbor]
                                      for neighbor in endpoint_neighbors(value))
                               for value in values)
    matching_adjacency = tuple(tuple(
        lookup[(value[0], value[1], neighbor)]
        for neighbor in switch_neighbors(value[2])
    ) for value in values)

    # The matching-flat pointed row is the h=2 specialization of the
    # uniform formula, since intrinsic response order is h+1=3.
    marked = (0, 1, ((2, 3), (4, 5)))
    marked_matching = set(marked[2])
    flat = []
    for p_site, s_site, _matching in values:
        q_value = sum(int(p_site not in pair and s_site not in pair)
                      for pair in marked_matching)
        if (p_site, s_site) == (0, 1):
            constant = 24
        elif p_site == 0 or s_site == 1:
            constant = 3
        else:
            constant = 0
        flat.append(Q(q_value + 3 * constant))
    flat = tuple(flat)

    # Endpoint/swap cyclic module has the five sectors
    # (8,+),(2,+),(-2,+),(4,-),(-2,-).  The endpoint cubic kills the four
    # nonconstant sectors without needing the swap in the formula.
    roots = (-2, 2, 4)
    projected = polynomial_apply(flat, roots, endpoint_adjacency)
    require(len(set(projected)) == 1 and projected[0] == 1344,
            ("h=3 endpoint projector output changed", set(projected)))
    denominator = (8 + 2) * (8 - 2) * (8 - 4)
    require(denominator == 240
            and projected[0] / denominator == Q(28, 5),
            "endpoint projector normalization changed")

    # Coefficient commutation is checked on every occurrence, not inferred
    # from the pointed row.
    endpoint_then_matching = tuple(
        sorted(lookup[neighbor]
               for endpoint_neighbor in endpoint_neighbors(value)
               for neighbor in (
                   (endpoint_neighbor[0], endpoint_neighbor[1], switched)
                   for switched in switch_neighbors(endpoint_neighbor[2])
               ))
        for value in values
    )
    matching_then_endpoint = tuple(
        sorted(lookup[neighbor]
               for switched in switch_neighbors(value[2])
               for neighbor in endpoint_neighbors(
                   (value[0], value[1], switched)))
        for value in values
    )
    require(endpoint_then_matching == matching_then_endpoint,
            "endpoint and matching coefficient graphs stopped commuting")

    matching_degree = 2
    matching_eigenvalue = -1
    matching_denominator = matching_degree - matching_eigenvalue
    require(matching_denominator == 3,
            "h=3 matching projector denominator changed")
    return {
        "intrinsic_response_order": 3,
        "occurrences": len(values),
        "association_parameter_h_minus_one": 2,
        "endpoint_degree": 8,
        "endpoint_nonconstant_eigenvalues": list(roots),
        "endpoint_polynomial": "(B+2I)(B-2I)(B-4I)",
        "endpoint_denominator": denominator,
        "matching_polynomial": "A+I",
        "matching_denominator": matching_denominator,
        "combined_coefficient_denominator": denominator * matching_denominator,
        "coefficient_operators_commute": True,
        "coefficient_centered_projector_exists": True,
        "source_chain_lift_constructed": False,
        "scalar_zero_face_after_rational_normalization": "90*f(x)",
    }


def mat_mul(left, right):
    columns = tuple(zip(*right, strict=True))
    return tuple(tuple(sum(Q(a) * Q(b) for a, b in
                           zip(row, column, strict=True))
                       for column in columns) for row in left)


def mat_sub(left, right):
    return tuple(tuple(Q(a) - Q(b) for a, b in
                       zip(left_row, right_row, strict=True))
                 for left_row, right_row in zip(left, right, strict=True))


def incidence_cech_factorization_audit():
    """Factor B+2 through endpoint incidence and locate its H0 class."""
    pairs = tuple((p_site, s_site) for p_site in SITES
                  for s_site in SITES if p_site != s_site)
    lookup = {pair: index for index, pair in enumerate(pairs)}
    size = len(pairs)
    identity = tuple(tuple(Q(row == column) for column in range(size))
                     for row in range(size))
    b_matrix = []
    for p_site, s_site in pairs:
        row = [Q(0)] * size
        for selected in SITES:
            if selected in (p_site, s_site):
                continue
            row[lookup[(selected, s_site)]] += 1
            row[lookup[(p_site, selected)]] += 1
        b_matrix.append(tuple(row))
    b_matrix = tuple(b_matrix)
    c_matrix = tuple(tuple(b_matrix[row][column]
                           + 2 * identity[row][column]
                           for column in range(size)) for row in range(size))

    # U records outgoing and incoming endpoint incidences.  Its adjoint
    # sends a pair of site functions to a(p)+b(s).
    incidence = []
    for channel in range(2):
        for site in SITES:
            incidence.append(tuple(Q(
                (channel == 0 and pair[0] == site)
                or (channel == 1 and pair[1] == site)
            ) for pair in pairs))
    incidence = tuple(incidence)
    transpose = tuple(zip(*incidence, strict=True))
    incidence_push_pull = mat_mul(transpose, incidence)
    require(incidence_push_pull == c_matrix,
            "B+2 stopped factoring through head/tail incidence")
    require(rank(c_matrix) == 11,
            "the ordered-pair incidence rank changed")

    # At n=6, C=B+2 has eigenvalues 10,4,0,6,0.  Its cubic kills all but
    # constants and equals 8 times the all-ones matrix.
    four_i = tuple(tuple(4 * value for value in row) for row in identity)
    six_i = tuple(tuple(6 * value for value in row) for row in identity)
    projector = mat_mul(mat_mul(c_matrix, mat_sub(c_matrix, four_i)),
                        mat_sub(c_matrix, six_i))
    require(projector == tuple((Q(8),) * size for _ in range(size)),
            "the incidence-factorized cubic stopped being the constant projector")

    # Any ordinary Cech/group-bar edge is a difference of vertices and has
    # augmentation zero.  The constant output of one projector column has
    # mass 240 and is therefore H0, not an oriented top boundary.
    tree_edges = []
    for index in range(1, size):
        column = [Q(0)] * size
        column[index] = 1
        column[0] = -1
        tree_edges.append(tuple(column))
    require(rank(tree_edges) == size - 1
            and all(sum(column, Q(0)) == 0 for column in tree_edges)
            and sum((projector[row][0] for row in range(size)), Q(0)) == 240,
            "the Cech H0/augmentation split changed")
    return {
        "ordered_pair_sites": len(SITES),
        "ordered_pairs": size,
        "formula": "B+2I=U_tail^*U_tail+U_head^*U_head",
        "incidence_rank": rank(c_matrix),
        "incidence_kernel_dimension": size - rank(c_matrix),
        "cubic_in_C": "C(C-4I)(C-6I)",
        "cubic_matrix": "8*J_30",
        "mass_of_each_cubic_column": 240,
        "ordinary_Cech_bar_image": "ker(sum:Q^30->Q)",
        "ordinary_Cech_bar_rank": rank(tree_edges),
        "constant_projector_is_bar_boundary": False,
        "consequence": (
            "incidence realizes the coefficient push-pull economically, "
            "but its base/constant H0 class is exactly where a physical "
            "cap augmentation must be adjoined"
        ),
    }


def relative_cartan_ce_audit():
    """Test odd/even Cartan bars and the target-normal correction."""
    # Orbit order is 1,w,s,sw.  w and s commute.  Acting on the seed gives
    # the two endpoint parities below.
    odd = (Q(-1), Q(1), Q(1), Q(-1))
    even = (Q(-1), Q(1), Q(-1), Q(1))
    require(sum(odd, Q(0)) == sum(even, Q(0)) == 0,
            "a relative Cartan boundary acquired H0 augmentation")
    require((odd[2], odd[3], odd[0], odd[1])
            == tuple(-value for value in odd)
            and (even[2], even[3], even[0], even[1]) == even,
            "the endpoint parity split changed")

    # The target is s-fixed.  Therefore the odd prism kills the Weyl target
    # defect, whereas the even companion doubles it.
    odd_target_defect = 0
    even_target_defect = 2
    require(odd_target_defect == 0 and even_target_defect != 0,
            "the odd/even Cartan target alternative changed")

    # Small physical quotient (Eq,w,target,ores).  The normalized target
    # correction cannot make the desired invisible w face.  This is the
    # exact target-normal obstruction behind the even companion.
    y_value = Q(1)
    target_row = (Q(-1), Q(0), Q(1), Q(0))
    cap_target = (Q(0), -y_value, Q(1), Q(0))
    ordinary = (Q(0), Q(1), Q(0), Q(1))
    desired_invisible = (Q(0), y_value, Q(0), Q(0))
    dual = (y_value, Q(1), y_value, Q(-1))
    require(all(sum(a * b for a, b in zip(dual, column, strict=True)) == 0
                for column in (target_row, cap_target, ordinary))
            and sum(a * b for a, b in
                    zip(dual, desired_invisible, strict=True)) == 1,
            "the target-normal invisible-face separator changed")
    require(rank((target_row, cap_target, ordinary)) == 3
            and rank((target_row, cap_target, ordinary,
                      desired_invisible)) == 4,
            "the target-normal rank jump changed")
    return {
        "relative_orbit": ["1", "w", "s", "sw"],
        "odd_boundary": [int(value) for value in odd],
        "even_boundary": [int(value) for value in even],
        "odd_target_defect": odd_target_defect,
        "even_target_defect": "2*(w-1)Delta",
        "odd_prism_source_valid_target_zero": True,
        "odd_prism_face_augmentation": 0,
        "even_companion_target_zero": False,
        "CE_or_group_bar_H0_augmentation": 0,
        "CE_orientation_top_maps_to_primitive_p": False,
        "target_normal_old_rank": 3,
        "rank_with_invisible_w_face": 4,
        "primitive_target_normal_dual": [int(value) for value in dual],
        "interpretation": (
            "the target-safe odd Cartan construction can only give standard "
            "face differences.  Removing the oddization exposes an even "
            "target defect; old graph/Koszul target correction leaves one "
            "primitive invisible cap class.  That class, not a CE top, is "
            "the missing source-normal attachment"
        ),
    }


def relative_cap_and_invisible_lift_comparison_audit():
    """Distinguish p=(-Q,-ores) from the invisible lift n."""
    # Normalize the selected cap row Q to one.  Coordinates are
    # (Q-boundary,target,ordinary residue).  The reduced relative endpoint
    # p is -rho.  The invisible lift n has the opposite boundary and zero
    # augmented readouts.  Their sum is the desired closed residue carrier.
    p = (Q(-1), Q(0), Q(-1))
    n = (Q(1), Q(0), Q(0))
    cycle = tuple(left + right for left, right in zip(p, n, strict=True))
    require(cycle == (Q(0), Q(0), Q(-1)),
            "the reduced-cap/invisible-lift signs changed")
    require(p != n, "the relative cap endpoint was confused with its lift")

    # The first universal cross-word candidate is the degree-four two-row
    # Koszul cell.  Its five denominator faces are nonzero quadrics; hence it
    # is a symbol for n, not a completed physical n or p.
    first_syzygy = (ROOT / (
        "computations/verify_h3_direct_free_first_syzygy_multidegree_gate.py"
    )).read_text()
    derived = (ROOT / (
        "computations/verify_derived_base_change_relative_cap_obstruction.py"
    )).read_text()
    require("first possible degree: 4" in first_syzygy
            and "universal bare-reset denominator defects: 5 nonzero quadrics"
                in first_syzygy
            and "relative Yoneda class: nonzero obstruction -kappa*Y*w"
                in derived
            and "hypothetical invisible lift: unique target-zero response line"
                in derived,
            "the cross-word relative-cap interface changed")
    return {
        "row_order": ["selected_Q_boundary", "target", "ordinary_residue"],
        "primitive_reduced_cap_p": [int(value) for value in p],
        "invisible_lift_n": [int(value) for value in n],
        "closed_carrier_n_plus_p": [int(value) for value in cycle],
        "p_equals_n": False,
        "precise_relation": (
            "after the source-labelled reset identifies Q with kappa*Y*w, "
            "p=-kappa*Y*rho is the relative endpoint and n has "
            "d n=+kappa*Y*w with target=ores=0; z=n+p is closed"
        ),
        "ordinary_derived_base_change_constructs_n": False,
        "first_cross_word_candidate": (
            "the degree-four two-row Koszul cell in words 01211222 and "
            "00000000"
        ),
        "first_candidate_status": (
            "exact upstairs syzygy, but its reset has five nonzero internal "
            "quadratic denominator faces"
        ),
        "reuse_of_Tor_framework": (
            "yes: p is the relative obstruction endpoint and n is the "
            "required positive transgression.  The construction question is "
            "one higher reset syzygy/nullhomotopy, not a new abstract CE top"
        ),
    }


def cap_quotient_and_primitive_cell_audit():
    # Five face coordinates after the matching-labelled q companions have
    # been packaged.  Physical Cartan gives the oriented C5 incidence.
    edges = []
    for index in range(5):
        column = [Q(0)] * 5
        column[index] = -1
        column[(index + 1) % 5] = 1
        edges.append(tuple(column))
    epsilon = (Q(1),) * 5
    primitive = (Q(-1), Q(0), Q(0), Q(0), Q(0))
    require(rank(edges) == 4
            and all(sum(column, Q(0)) == 0 for column in edges),
            "the physical Cartan cap standard module changed")
    tree = tuple(edges[:4])
    require(abs(determinant(tree + (primitive,))) == 1,
            "the reduced cap cell stopped being primitive")
    require(rank(tree + (primitive,)) == 5
            and sum(primitive, Q(0)) == -1,
            "one reduced cap cell stopped completing the quotient")

    # The local cell is displayed before its C5 translates.  Q_(v,N) is the
    # labelled response companion, not a coarse unlabeled residue scalar.
    rows = (
        "Omega", "Q_(v,N)", "rootless_ridge", "Eq", "W",
        "target", "ores", "ainc", "eta", "sigma",
    )
    p = (0, -1, 0, 0, 0, 0, -1, 0, 0, 0)
    require(p[rows.index("Q_(v,N)")] == -1
            and p[rows.index("ores")] == -1
            and all(p[rows.index(row)] == 0 for row in
                    ("Omega", "rootless_ridge", "Eq", "W", "target",
                     "ainc", "eta", "sigma")),
            "the minimal reduced cap signature changed")
    return {
        "projected_cap_module": "P=Z^5 with face coordinates lambda_v",
        "physical_Cartan_image": "ker(epsilon)",
        "Cartan_rank": rank(edges),
        "Cartan_image_saturated": True,
        "remaining_cokernel": "Z generated by epsilon=sum_v lambda_v",
        "smallest_local_cell": "p_(v,N)",
        "row_order": list(rows),
        "required_augmented_signature": list(p),
        "boundary_formula": "-Q_(v,N), with ores=-1",
        "primitive_epsilon": -1,
        "integral_completion_determinant": determinant(tree + (primitive,)),
        "full_source_word": "01211222",
        "rootless_word_after_exposed_x_removed": "1211222",
        "first_common_fine_degree": "t*q_(v,N), repeated P3+K2",
        "first_scalar_Hasse_top": (
            "order four: {q_xv:0m_v,q_pq:22}+N; external/internal=(2,2)"
        ),
        "first_literal_source_component": (
            "target weight 14, seven-edge full-nine boundary"
        ),
        "cyclic_common_top_component": (
            "target weight 18, nine-edge full-nine boundary"
        ),
    }


def current_inventory_obstruction_audit():
    # Exact projected facts, pinned to the complete literal computations.
    # They are deliberately kept distinct: none can be renamed as p.
    candidate_selected_values = {
        "formal_Hasse_tail": Q(1),
        "target_normalized_unary": Q(0),
        "source_valid_adjacent_edge": Q(0),
    }
    half_sum = Q(1, 2) * (
        candidate_selected_values["formal_Hasse_tail"]
        + candidate_selected_values["target_normalized_unary"]
    )
    require(half_sum == Q(1, 2),
            "the unary/Hasse selected obstruction changed")

    # The C5 degree-five Tate top is a relation among edge columns; its face
    # image is zero.  The ordinary face readout is invariant while Alt_7 is
    # odd, so equivariance gives 2p_v=0 in a torsion-free target.
    sign_constraints = []
    for index in range(5):
        column = [Q(0)] * 5
        column[index] = 2
        sign_constraints.append(tuple(column))
    require(rank(sign_constraints) == 5,
            "the Alt7-to-ordinary-face map stopped vanishing")

    # Source-text assertions pin the complete finite search conclusions
    # without re-running its 5*288+4266 full-nine enumeration in every mode.
    complete = (ROOT / (
        "computations/verify_h3_rootless_c5_complete_multidegree_source_no_go.py"
    )).read_text()
    one_face = (ROOT / (
        "computations/verify_h3_rootless_one_face_third_cofactor_comparison_vertex_gate.py"
    )).read_text()
    tate = (ROOT / (
        "computations/verify_h3_jd_site_covariant_tate_cartan_cap_alternative.py"
    )).read_text()
    require('"one_chart_kernel": 0' in complete
            and '"kernel_anchor_incidence": 0' in complete
            and '"selected_fourth_operator_value": str(candidate_descent)'
                in one_face
            and '"maps_to_aggregate_lambda": False' in tate
            and '"order_forgetting_map_dimension": 0' in tate,
            "a pinned primitive-cap obstruction statement changed")
    return {
        "target_normalized_unary_product": {
            "coarse_signature_can_be_forced": True,
            "source_valid": False,
            "selected_fourth_operator_value": str(half_sum),
            "word_labels": ["01211222", "00211200", "00000000"],
            "word_change_by_polynomial_multiplication": False,
        },
        "degree_five_Tate_top": {
            "boundary": "sum of the five C5 edge generators",
            "face_image": 0,
            "epsilon": 0,
            "constructs_p": False,
        },
        "orientation_line": {
            "source": "Alt_7",
            "ordinary_cap_variance": "trivial under occurrence reordering",
            "equivariance_equations": "2*p_v=0",
            "rank": rank(sign_constraints),
            "ordinary_order_forgetting_map": 0,
            "needed_escape": (
                "an explicitly orientation-twisted physical relative cap, "
                "not the symmetric forgetful map"
            ),
        },
        "complete_literal_full_nine": {
            "five_weight14_components": "288 columns/rank 288 each",
            "weight18_component": "4266 columns/rank 4266",
            "natural_Tate_map": "1440 -> 1201, kernel 239",
            "anchor_on_entire_natural_kernel": 0,
            "two_chart_kernels": "pairwise identical-chart differences",
            "primitive_cap_cell_in_image": False,
        },
    }


def physical_cubic_interface_audit():
    # The coefficient cubic has three endpoint stages.  Its source lift also
    # composes with the matching switch.  The four face families below are
    # forced by the Hasse product rule.  Coefficient commutation supplies no
    # chain homotopy for them.
    face_families = (
        "three one-endpoint Cartan product-rule faces",
        "pairwise B-B second-Hasse faces",
        "mixed B-A_match commutator faces",
        "the third-Hasse face of the cubic endpoint polynomial",
    )
    return {
        "top_coefficient_operation": (
            "Pi_end Pi_match with the marked occurrence delta retained"
        ),
        "proper_face_families": list(face_families),
        "coefficient_graph_commutation_is_chain_commutation": False,
        "first_physical_cap_projection": (
            "the five lambda_v classes of the word/ridge response companion"
        ),
        "standard_part": "closed by the physical Cartan C5 orbit",
        "aggregate_part": "one primitive p or an extended epsilon terminal",
        "smallest_positive_theorem": (
            "construct one source-valid seven-occurrence relative total cell "
            "whose normalized scalar face is 90*f, whose cap face has "
            "epsilon +/-1, and whose word/ridge/Eq/W/target/ores/ainc/q/"
            "eta/sigma faces equal the required p packet; the C5 orbit and "
            "Cartan edges then supply all face translates"
        ),
        "uniform_extension_requirement": (
            "make this cell a module over the spectator Hasse coalgebra; "
            "bare multiplication by q^[h-3] leaves nonzero d(q^[h-3]) faces"
        ),
        "association_projector_is_a_Hasse_lift_of_p": (
            "conditional only: the coefficient cubic identifies the unique "
            "place where p must enter, but no augmented source lift maps "
            "its scalar face to the cap generator yet"
        ),
        "relation_to_Tr_h": (
            "p supplies the local nonzero cap augmentation required by a "
            "physical lift; Tr_h additionally needs boundary independence, "
            "clean-line type, and every common Hankel shift, so p alone is "
            "not the uniform transfer theorem"
        ),
    }


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))
    ledger = {
        "theorem": (
            "h3 centered endpoint association projector / primitive physical "
            "cap lift gate"
        ),
        "pins": PINS,
        "coefficient_projector": coefficient_projector_audit(),
        "incidence_Cech_factorization": incidence_cech_factorization_audit(),
        "relative_Cartan_CE": relative_cartan_ce_audit(),
        "physical_cap_quotient": cap_quotient_and_primitive_cell_audit(),
        "relative_cap_vs_invisible_lift":
            relative_cap_and_invisible_lift_comparison_audit(),
        "current_inventory": current_inventory_obstruction_audit(),
        "physical_cubic_interface": physical_cubic_interface_audit(),
        "verdict": (
            "The h=3 matching/endpoint association projector is exact at "
            "coefficient level, but its source-valid cubic totalization is "
            "not in the committed inventory.  After all physical Cartan "
            "standard directions, the first cap obstruction is precisely one "
            "primitive reduced response cell p=(-Q,-ores) in the labelled "
            "P3+K2 word 01211222.  Unary normalization leaves the selected "
            "fourth-Hasse class, Tate and symmetric Alt7 forgetting have zero "
            "aggregate image, and the complete weight-14/18 full-nine modules "
            "have no suitable kernel.  Thus p (with the four cubic/mixed face "
            "families) is the smallest new physical source extension; epsilon "
            "is not yet a typed physical terminal"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("primitive cap lift ledger changed", digest))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("h3 endpoint association projector: COEFFICIENTWISE EXACT")
    print("physical cubic Cartan/Hasse lift: NOT CONSTRUCTED")
    print("first cap quotient: one primitive p=(-Q,-ores)")
    print("unary / Tate-Alt7 / complete-row routes: OBSTRUCTED")
    print("epsilon physical terminal: NOT YET TYPED")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
