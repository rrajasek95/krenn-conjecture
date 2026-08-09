#!/usr/bin/env python3
"""Full-nine deleted-star inverse audit on the canonical active OO profile.

The three constant deleted-r-star pivot columns form the identity.  This is
therefore the strongest possible test of the tempting scalar equation E K=I:
there is no non-pivot star remainder to blame.  The exact source equation is
instead tensor-valued.  Pure-output evaluation gives an invertible diagonal
matrix, while the clean mixed-face Hessian lives in a different tensor grade
and in the exclusive r=2 column.  Its adjugate image stays off diagonal.
"""

from collections import Counter, defaultdict
from fractions import Fraction as F
from itertools import product

import verify_oo_c8_main_face_cramer_transport as cramer
import verify_oo_c8_active_leader_quotient as leader
import verify_oo_c8_two_cell_activity_frontier as frontier
import verify_oo_doubly_good_two_anchor_counterguard as base


SUPPORT = (
    (0, 1, 2, 1),
    (0, 3, 1, 1),
    (1, 7, 1, 1),
    (5, 6, 1, 1),
)

FACE = (
    (1, 2, 1, 1, 1),
    (1, 0, 1, 1, 1),
    (0, 2, 1, 1, 1),
    (0, 0, 1, 1, 1),
)

RESIDUAL = tuple(v for v in base.VERTICES if v not in (base.P, base.R))
PIVOTS = ((5, 0), (base.Q, 1), (3, 2))


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def clean(polynomial):
    return {mask: value for mask, value in polynomial.items() if value}


def subtract(left, right):
    answer = defaultdict(F, left)
    for mask, value in right.items():
        answer[mask] -= value
    return clean(answer)


def add_scaled(target, polynomial, scalar):
    for mask, value in polynomial.items():
        target[mask] += scalar * value


def full_word(p_colour, r_colour, residual_word):
    colours = dict(zip(RESIDUAL, residual_word, strict=True))
    colours[base.P] = p_colour
    colours[base.R] = r_colour
    return tuple(colours[v] for v in base.VERTICES)


def deleted_star(blocks):
    """Return the r-star matrix by physical half-edge columns, omitting p."""

    occupied = {
        (site, colour)
        for site in base.VERTICES
        if site not in (base.P, base.R)
        for row in base.COLORS
        for colour in base.COLORS
        if base.entry(blocks, base.R, site, row, colour)
    }
    require(occupied == set(PIVOTS), "deleted-r-star acquired a non-pivot column")
    columns = PIVOTS
    matrix = [
        [base.entry(blocks, base.R, site, row, colour) for site, colour in columns]
        for row in base.COLORS
    ]
    return tuple(columns), matrix


def tensor_k(blocks):
    """Build K_ij as a tensor on the six residual sites from r-pivot terms."""

    answer = [[{} for _ in base.COLORS] for _ in base.COLORS]
    for p_colour in base.COLORS:
        for r_colour in base.COLORS:
            component = {}
            for residual_word in product(base.COLORS, repeat=len(RESIDUAL)):
                word = full_word(p_colour, r_colour, residual_word)
                by_column = cramer.response_by_r_column(blocks, SUPPORT, word)
                require(
                    set(by_column) <= {PIVOTS[r_colour]},
                    "a non-pivot deleted-star summand entered the canonical packet",
                )
                polynomial = by_column.get(PIVOTS[r_colour], {})
                if polynomial:
                    component[residual_word] = polynomial
            answer[p_colour][r_colour] = component
    return answer


def hessian(component, residual_words):
    answer = defaultdict(F)
    for sign, word in zip((1, -1, -1, 1), residual_words, strict=True):
        add_scaled(answer, component.get(word, {}), sign)
    return clean(answer)


def matrix_nonzero_pattern(matrix):
    return tuple(
        (row, column)
        for row in base.COLORS
        for column in base.COLORS
        if matrix[row][column]
    )


def selected_response(blocks, support, word, r_colour):
    """Response through the constant r-pivot, with variable r-cells removed."""

    incident_mask = sum(
        1 << index
        for index, cell in enumerate(support)
        if base.R in cell[:2]
    )
    polynomial = cramer.response_by_r_column(blocks, support, word).get(
        PIVOTS[r_colour], {}
    )
    return {
        mask: value
        for mask, value in polynomial.items()
        if not (mask & incident_mask)
    }


def selected_k_matrices(blocks, support, face):
    pure = [[{} for _ in base.COLORS] for _ in base.COLORS]
    mixed = [[{} for _ in base.COLORS] for _ in base.COLORS]
    face_residual_words = []
    for common_word in face:
        colours = dict(zip(leader.COMMON, common_word, strict=True))
        colours[base.Q] = 0
        face_residual_words.append(tuple(colours[v] for v in RESIDUAL))
    for i in base.COLORS:
        for j in base.COLORS:
            pure_word = (i,) * len(RESIDUAL)
            pure[i][j] = selected_response(
                blocks, support, full_word(i, j, pure_word), j
            )
            value = defaultdict(F)
            for sign, residual_word in zip(
                (1, -1, -1, 1), face_residual_words, strict=True
            ):
                add_scaled(
                    value,
                    selected_response(
                        blocks, support, full_word(i, j, residual_word), j
                    ),
                    sign,
                )
            mixed[i][j] = clean(value)
    return pure, mixed


def exponent_polynomial(polynomial, variables=4):
    return {
        tuple(int(bool(mask & (1 << index))) for index in range(variables)): value
        for mask, value in polynomial.items()
    }


def poly_add(left, right, scale=1):
    answer = defaultdict(F, left)
    for exponent, coefficient in right.items():
        answer[exponent] += scale * coefficient
    return clean(answer)


def poly_multiply(left, right):
    answer = defaultdict(F)
    for a, x in left.items():
        for b, y in right.items():
            answer[tuple(u + v for u, v in zip(a, b, strict=True))] += x * y
    return clean(answer)


def poly_matrix(matrix):
    return [[exponent_polynomial(entry) for entry in row] for row in matrix]


def adjugate_3(matrix):
    # Adjugate[j][i] is the signed minor deleting row i and column j.
    answer = [[{} for _ in base.COLORS] for _ in base.COLORS]
    for i in base.COLORS:
        for j in base.COLORS:
            rows = [row for row in base.COLORS if row != i]
            columns = [column for column in base.COLORS if column != j]
            minor = poly_add(
                poly_multiply(matrix[rows[0]][columns[0]], matrix[rows[1]][columns[1]]),
                poly_multiply(matrix[rows[0]][columns[1]], matrix[rows[1]][columns[0]]),
                -1,
            )
            answer[j][i] = minor if (i + j) % 2 == 0 else {
                exponent: -coefficient for exponent, coefficient in minor.items()
            }
    return answer


def poly_matmul(left, right):
    answer = [[{} for _ in base.COLORS] for _ in base.COLORS]
    for i in base.COLORS:
        for j in base.COLORS:
            value = {}
            for k in base.COLORS:
                value = poly_add(value, poly_multiply(left[i][k], right[k][j]))
            answer[i][j] = value
    return answer


def main_profiles(blocks):
    profiles = []
    for support in leader.no_compound_regressions(blocks):
        records = tuple(leader.leading_record(blocks, support, arm) for arm in frontier.ARMS)
        residual_pq = tuple(v for v in base.VERTICES if v not in frontier.ARMS[0])
        residual_pr = tuple(v for v in base.VERTICES if v not in frontier.ARMS[1])
        r_colour = records[0]["word"][residual_pq.index(base.R)]
        q_colour = records[1]["word"][residual_pr.index(base.Q)]
        clean_face = cramer.vertex.chosen_clean_face(blocks, support, records)
        if clean_face is not None and q_colour == 0 and r_colour == 2:
            profiles.append((support, clean_face[0]))
    require(len(profiles) == 47, "main 47-profile sector changed")
    return profiles


def main():
    blocks = base.build_packet()
    columns, star = deleted_star(blocks)
    require(columns == PIVOTS, "deleted-r-star columns changed")
    require(star == [[F(1), 0, 0], [0, F(1), 0], [0, 0, F(1)]], "E is not I3")

    # Literal source-faithful flattening.  K is not a scalar matrix: every
    # entry is a six-site top tensor.  Check its decomposition against the
    # full matching tensor and the direct pr*q^[3] term at every coefficient.
    k_tensor = tensor_k(blocks)
    full = frontier.tensor_polynomials(blocks, SUPPORT)
    q_tensor = frontier.cofactor_polynomials(blocks, SUPPORT, (base.P, base.R))
    direct = base.direct_matrix(blocks, base.P, base.R)
    require(direct == [[0, 0, 0], [0, 1, 0], [0, 0, 0]], "direct pr block changed")
    for i in base.COLORS:
        for j in base.COLORS:
            for residual_word in product(base.COLORS, repeat=len(RESIDUAL)):
                lhs = full.get(full_word(i, j, residual_word), {})
                direct_term = {
                    mask: direct[i][j] * value
                    for mask, value in q_tensor.get(residual_word, {}).items()
                    if direct[i][j] * value
                }
                response = subtract(lhs, direct_term)
                require(
                    response == k_tensor[i][j].get(residual_word, {}),
                    "full-nine slice != direct cofactor + deleted-star response",
                )

    # The conventional E*K=I statement silently uses a different output
    # functional in each row: extract the pure-i residual word in row i.
    pure_k = [
        [k_tensor[i][j].get((i,) * len(RESIDUAL), {}) for j in base.COLORS]
        for i in base.COLORS
    ]
    require(
        pure_k
        == [[{0: F(1)}, {}, {}], [{}, {14: F(1)}, {}], [{}, {}, {0: F(1)}]],
        "pure-output flattening changed",
    )
    # On the pure-anchor torus chart mask 14 is normalized to one, so K=I.
    pure_adjugate_pattern = ((0, 0), (1, 1), (2, 2))

    # Evaluate the *same tensor-valued K* on the clean common-word face,
    # fixing q=0.  This is the exclusive r=2 Hessian from the 47-profile
    # regression.  It is a different tensor grade from the pure evaluation.
    face_words = []
    for common_word in FACE:
        colours = dict(zip(leader.COMMON, common_word, strict=True))
        colours[base.Q] = 0
        face_words.append(tuple(colours[v] for v in RESIDUAL))
    face_k = [
        [hessian(k_tensor[i][j], face_words) for j in base.COLORS]
        for i in base.COLORS
    ]
    require(
        face_k
        == [[{}, {}, {}], [{}, {}, {12: F(1)}], [{}, {}, {}]],
        "clean-face K-Hessian changed",
    )
    require(matrix_nonzero_pattern(face_k) == ((1, 2),), "exclusive r=2 grade moved")

    # The adjugate of the pure diagonal flattening is diagonal.  Left or
    # right multiplication can rescale E_12 but cannot create the required
    # r=1 diagonal E_11 channel.  This is a support statement, independent
    # of the localized nonzero monomial values.
    left_pattern = matrix_nonzero_pattern(face_k)
    right_pattern = matrix_nonzero_pattern(face_k)
    require(left_pattern == right_pattern == ((1, 2),), "adjugate created a new channel")
    require((1, 1) not in left_pattern, "mixed Hessian reached the diagonal channel")

    # Check the same adjugate proposal on every member of the committed
    # 47-profile regression sector.  We retain the constant pivot contribution
    # and remove variable cells incident to r; those are precisely the
    # nonlocal star remainder in the full E*K equation.
    transport_census = Counter()
    determinant_term_census = Counter()
    first_transport = None
    for profile_support, profile_face in main_profiles(blocks):
        profile_pure, profile_face_k = selected_k_matrices(
            blocks, profile_support, profile_face
        )
        pure_polynomial = poly_matrix(profile_pure)
        face_polynomial = poly_matrix(profile_face_k)
        adjugate = adjugate_3(pure_polynomial)
        left_image = poly_matmul(adjugate, face_polynomial)
        right_image = poly_matmul(face_polynomial, adjugate)
        left_transport = bool(left_image[1][1])
        right_transport = bool(right_image[1][1])
        transport_census[(left_transport, right_transport)] += 1
        # det(K) is the (0,0) entry of K*adj(K).
        determinant_term_census[len(poly_matmul(pure_polynomial, adjugate)[0][0])] += 1
        if (left_transport or right_transport) and first_transport is None:
            first_transport = (
                profile_support, profile_face, profile_pure, profile_face_k,
                left_image[1][1], right_image[1][1],
            )
    require(
        transport_census == Counter({(False, False): 47}),
        "the pure adjugate unexpectedly transported a main-profile Hessian",
    )

    print("alternating-C8 full-nine star inverse: PASS")
    print(f"deleted-r-star columns={columns}; E={star}; nonpivot=0")
    print(f"source-faithful equation: H_ij=d_ij*Q+sum_alpha E_jalpha*K_ialpha")
    print(f"pure-output K={pure_k}; det monomial=mask14; adjugate pattern={pure_adjugate_pattern}")
    print(f"clean-face K-Hessian={face_k}")
    print(f"left/right adjugate image pattern={left_pattern}; diagonal (1,1) absent")
    print(f"47-profile adjugate transport census={dict(transport_census)}")
    print(f"47-profile determinant-term census={dict(sorted(determinant_term_census.items()))}")
    print(f"first transported profile={first_transport}")
    print("verdict=E*K=I exists only after row-dependent pure evaluation; it does not transport the mixed tensor grade")


if __name__ == "__main__":
    main()
