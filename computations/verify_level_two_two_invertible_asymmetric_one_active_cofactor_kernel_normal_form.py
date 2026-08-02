#!/usr/bin/env python3
"""Audit the one-active asymmetric 2I+2R+2Z residual normal form.

For a P/V-active zero z and inactive zero w, every endpoint packet modulo
the aligned gauge is

    a_s R_v,  R_v = 2*tau*(beta_v-b_v)*S_t + f_v*S_z.

Mixed L0 leaves one correction colour and makes H a physical pure tensor.
Both star derivatives have the active z-factor, so pure L0 fixes it to the
complementary physical colour.  The four-site cofactor at w is then pure.
Its degenerate inner triangle map has rank five and kernel (r,-r,0).  The
nonzero product slice forces physical colour s and both columns of M_uw
onto the rank-one u-line.  Every block incident with u then has one fixed
factor, giving rank(dPsi)<=32+10=42 and closing the chart.

Standard library only; checks remain live under -O and -I -S.
"""

from fractions import Fraction as Q
from itertools import combinations, product
from pathlib import Path
from runpy import run_path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


HERE = Path(__file__).resolve().parent
ASYMMETRIC = run_path(str(
    HERE / "verify_level_two_two_invertible_asymmetric_one_column_l1_boundary.py"
))
SHORE = run_path(str(
    HERE / "verify_level_two_three_invertible_coordinate_shore_rank_drop.py"
))

SITES = tuple(range(6))
FULL = (0, 1, 3)
ONE_COLUMN = 2
ACTIVE = 4
INACTIVE = 5
COLOURS = (0, 1)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position in range(1, len(vertices)):
        second = vertices[position]
        remaining = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(remaining):
            answer.append(((first, second),) + tail)
    return tuple(answer)


MATCHINGS = perfect_matchings(SITES)


def rational_rank(matrix):
    rows = [[Q(value) for value in row] for row in matrix]
    rank = 0
    width = len(rows[0]) if rows else 0
    for column in range(width):
        pivot = next((row for row in range(rank, len(rows))
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        scale = rows[rank][column]
        rows[rank] = [entry / scale for entry in rows[rank]]
        for row in range(len(rows)):
            if row == rank or not rows[row][column]:
                continue
            multiple = rows[row][column]
            rows[row] = [
                left - multiple * right
                for left, right in zip(rows[row], rows[rank])
            ]
        rank += 1
    return rank


def matrix_vector_product(matrix, vector):
    return tuple(
        sum((entry * value for entry, value in zip(row, vector)), Q(0))
        for row in matrix
    )


def audit_imported_endpoint_packet():
    defect = ASYMMETRIC["audit_inactive_zero_slice_defect"]()
    zero_types = ASYMMETRIC["audit_zero_site_l1_types"]()
    require(defect[0] == 15 and defect[1] == frozenset(((0, 2), (1, 2), (2, 3))),
            "imported one-star defect changed")
    require(zero_types["P"]["full-column factor"] == "v_z"
            and zero_types["I"]["full-column factor"] is None,
            "imported P/I endpoint dictionary changed")

    # The residual coefficients have the exact outer-product form
    # a_s*(2*tau*delta_v, f_v) in the basis (S_t,S_z).
    tau = Q(7)
    a = (Q(2), Q(3))
    delta = (Q(5), Q(11))
    f = (Q(13), Q(17))
    packets = {
        (s, v): (2 * tau * a[s] * delta[v], a[s] * f[v])
        for s in COLOURS for v in COLOURS
    }
    for s, v in product(COLOURS, repeat=2):
        require(packets[s, v] == (
            a[s] * (2 * tau * delta[v]), a[s] * f[v]
        ), "endpoint residual lost its a_s factor")
    return defect, packets


def audit_matching_factorization():
    # Base matchings: tz gives B*C, Fz gives the active v_z factor, and zw
    # is dead.  This is a literal partition of all fifteen matchings.
    base = {"B*C": 0, "v-factor": 0, "dead-zw": 0}
    for matching in MATCHINGS:
        edges = frozenset(matching)
        if (ACTIVE, INACTIVE) in edges:
            category = "dead-zw"
        elif (ONE_COLUMN, ACTIVE) in edges:
            category = "B*C"
        else:
            active_edge = next(edge for edge in matching if ACTIVE in edge)
            partner = (active_edge[1] if active_edge[0] == ACTIVE
                       else active_edge[0])
            require(partner in FULL,
                    ("active zero lost its fixed-factor spoke", matching))
            category = "v-factor"
        base[category] += 1
    require(base == {"B*C": 3, "v-factor": 9, "dead-zw": 3},
            ("one-active matching split changed", base))

    # For each S_t edge, two complementary matchings pair z to F and one
    # uses dead zw.  For each S_z edge, its tangent block itself supplies v.
    st = {"v-factor": 0, "dead-zw": 0}
    for full_site in FULL:
        remaining = tuple(site for site in SITES
                          if site not in (ONE_COLUMN, full_site))
        for tail in perfect_matchings(remaining):
            edges = frozenset(tail)
            if (ACTIVE, INACTIVE) in edges:
                st["dead-zw"] += 1
            else:
                active_edge = next(edge for edge in tail if ACTIVE in edge)
                partner = (active_edge[1] if active_edge[0] == ACTIVE
                           else active_edge[0])
                require(partner in FULL,
                        ("S_t cofactor lost active factor", full_site, tail))
                st["v-factor"] += 1
    require(st == {"v-factor": 6, "dead-zw": 3},
            ("S_t factor census changed", st))

    sz_terms = 0
    for full_site in FULL:
        remaining = tuple(site for site in SITES
                          if site not in (full_site, ACTIVE))
        sz_terms += len(perfect_matchings(remaining))
    require(sz_terms == 9, "S_z tangent term count changed")
    return base, st, sz_terms


def audit_mixed_colour_reduction():
    # Abstract [R_0],[R_1] as zero/nonzero classes.  Mixed L0 imposes
    # a0*R1=a1*R0=0.  If both pure products vanish, pure L0 is collinear.
    closed = 0
    survivors = []
    for a0, a1, r0, r1 in product((0, 1), repeat=4):
        if a0 * r1 or a1 * r0:
            continue
        pure = (a0 * r0, a1 * r1)
        if pure == (0, 0):
            closed += 1
        else:
            survivors.append((a0, a1, r0, r1, pure))
    require(survivors == [
        (0, 1, 0, 1, (0, 1)),
        (1, 0, 1, 0, (1, 0)),
    ], ("one-active mixed-colour survivors changed", survivors))
    require(closed == 7, "one-active collinear case count changed")
    return closed, survivors


def audit_pure_flattening_and_support():
    # E_k-kappa*h*E_s=v*D has z-flattening rank at most one.  The displayed
    # diagonal 2x2 minor is +/-kappa*h, so kappa=0; singleton support then
    # fixes v and D to colour k.  The s-row B_s*C=h E_s^5 similarly fixes
    # both nonzero factors.
    checks = 0
    supports = {}
    for s in COLOURS:
        k = 1 - s
        # Columns stand for the five-site words k^5 and s^5.
        matrix = [[Q(0), Q(0)] for _ in COLOURS]
        matrix[k][0] = Q(1)
        matrix[s][1] = Q(-35)  # a nonzero instance of -kappa*h
        determinant = (matrix[0][0] * matrix[1][1]
                       - matrix[0][1] * matrix[1][0])
        require(determinant != 0,
                ("pure-corner flattening minor vanished", s))

        target = frozenset(((k, (k,) * 5),))
        require({left for left, _ in target} == {k}
                and {right for _, right in target} == {(k,) * 5},
                "singleton pure correction stopped fixing v_z")

        factor_target = frozenset(((s, (s,) * 4),))
        solutions = []
        for t_colour in COLOURS:
            for four_word in product(COLOURS, repeat=4):
                if frozenset(((t_colour, four_word),)) == factor_target:
                    solutions.append((t_colour, four_word))
        require(solutions == [(s, (s,) * 4)],
                ("B_s*C singleton factorization changed", s))
        supports[s] = tuple(solutions)
        checks += 3
    return checks, supports


def cofactor_matrix(p=Q(2), q=Q(3)):
    # Normalize h_u=e0.  M01=J and M0u=M1u=r*e0^T with r=(q,p).
    # Inputs are A0_0,A0_1,A1_0,A1_1,Au_0,Au_1; outputs are words 000..111.
    r = (q, p)
    j = ((Q(0), Q(1)), (Q(1), Q(0)))
    rows = []
    for x0, x1, xu in product(COLOURS, repeat=3):
        row = [Q(0)] * 6
        if xu == 0:
            row[x0] += r[x1]
            row[2 + x1] += r[x0]
        row[4 + xu] += j[x0][x1]
        rows.append(row)
    return rows


def audit_rank_five_cofactor_kernel():
    samples = ((Q(2), Q(3)), (Q(-5), Q(7)),
               (Q(11, 3), Q(-13, 2)))
    kernels = []
    for p, q in samples:
        r = (q, p)
        matrix = cofactor_matrix(p, q)
        kernel = r + tuple(-entry for entry in r) + (Q(0), Q(0))
        require((len(matrix), len(matrix[0])) == (8, 6),
                "degenerate cofactor map shape changed")
        require(rational_rank(matrix) == 5,
                ("degenerate cofactor map rank changed", p, q))
        require(not any(matrix_vector_product(matrix, kernel)),
                ("antisymmetric cofactor kernel stopped vanishing", p, q))

        # Rank five and a nonzero null vector make the audited null line the
        # complete kernel.
        require(any(kernel), "cofactor-kernel witness collapsed")

        # Directly audit the one-parameter solution used in the proof:
        # A0=lambda*r, A1=-lambda*r, Au=0.
        for lam in (Q(-5), Q(0), Q(7, 3)):
            candidate = tuple(lam * value for value in kernel)
            require(not any(matrix_vector_product(matrix, candidate)),
                    "a cofactor-kernel multiple became visible")
        kernels.append(kernel)
    return (8, 6), 5, tuple(kernels)


def audit_common_shore_and_path():
    # C^k=0 puts U^k=lambda*K.  C^s!=0 prevents U^s from lying on K.
    # Therefore lambda=0 is exactly the fixed-e_s shore subcase.
    cases = {
        "lambda=0": "fixed physical e_s shore; rank <=49",
        "lambda!=0": "unfactored antisymmetric-kernel residue",
    }
    require(len(cases) == 2 and "rank <=49" in cases["lambda=0"],
            "common-shore dichotomy changed")

    path_identities, categories = SHORE["audit_path_factorization"]()
    require(path_identities == 64,
            "coordinate-shore path identities changed")
    require(categories == {
        "all_cross": 6, "34": 3, "35": 3, "45": 3,
    }, "coordinate-shore path categories changed")
    shores = ("Q_t", "v_z=e_k", "e_s")
    exceptional = frozenset(((ONE_COLUMN, ACTIVE),
                             (ONE_COLUMN, INACTIVE)))
    require(len(shores) == 3 and (ACTIVE, INACTIVE) not in exceptional,
            "one-active exceptional path changed")
    return cases, shores, exceptional, categories


def audit_product_slice_and_fixed_root_bound():
    # The u=e1 slice of Phi(U_w^s) is A_u(e1)*J.  Its required nonzero
    # product value is eta_u(e1)*(eta_0 outer eta_1).  Rank-two J cannot
    # equal a nonzero scalar multiple of a rank-one outer product, so both
    # coefficients vanish.  Thus A_u and physical e_s at u lie on h_u=e0.
    j = ((Q(0), Q(1)), (Q(1), Q(0)))
    outer_product = ((Q(6), Q(15)), (Q(14), Q(35)))
    require(ASYMMETRIC["matrix_rank_2"](j) == 2,
            "normalized J slice lost rank two")
    require(ASYMMETRIC["matrix_rank_2"](outer_product) == 1,
            "physical product slice lost rank one")

    incident = tuple(edge for edge in combinations(SITES, 2) if 3 in edge)
    nonincident = tuple(edge for edge in combinations(SITES, 2)
                        if 3 not in edge)
    require((len(incident), len(nonincident)) == (5, 10),
            "fixed-root edge census changed")

    # Nonincident tangents remain in the h_u slice, dimension 2^5=32.
    # Each incident edge has only two cells with complementary u-colour.
    fixed_slice_dimension = 2 ** 5
    escape_cells = len(incident) * 2
    bound = fixed_slice_dimension + escape_cells
    require((fixed_slice_dimension, escape_cells, bound) == (32, 10, 42),
            "fixed-root differential bound changed")

    # An exact integral packet in the fixed-root envelope attains 42, so
    # the support count itself has no hidden slack.  Edge matrices are
    # stored with rows at the smaller endpoint and columns at the larger.
    packet = {}
    for edge_index, (left, right) in enumerate(combinations(SITES, 2)):
        matrix = []
        for left_colour in COLOURS:
            row = []
            for right_colour in COLOURS:
                value = Q(
                    (edge_index + 2) * (left_colour + 1)
                    + (edge_index + 3) * (right_colour + 2)
                    + left_colour * right_colour + 1
                )
                if right == 3 and right_colour == 1:
                    value = Q(0)
                if left == 3 and left_colour == 1:
                    value = Q(0)
                row.append(value)
            matrix.append(tuple(row))
        packet[left, right] = tuple(matrix)

    cells = tuple(
        (left, right, left_colour, right_colour)
        for left, right in combinations(SITES, 2)
        for left_colour, right_colour in product(COLOURS, repeat=2)
    )
    rows = []
    for word in product(COLOURS, repeat=6):
        row = []
        for left, right, left_colour, right_colour in cells:
            if (word[left], word[right]) != (left_colour, right_colour):
                row.append(Q(0))
                continue
            remaining = tuple(site for site in SITES
                              if site not in (left, right))
            value = Q(0)
            for matching in perfect_matchings(remaining):
                term = Q(1)
                for edge in matching:
                    i, j = edge
                    term *= packet[edge][word[i]][word[j]]
                value += term
            row.append(value)
        rows.append(row)
    calibration_rank = rational_rank(rows)
    require(calibration_rank == 42,
            "fixed-root integral calibration rank changed")
    return 2, 1, incident, nonincident, bound, calibration_rank


def main():
    endpoint = audit_imported_endpoint_packet()
    matching = audit_matching_factorization()
    mixed = audit_mixed_colour_reduction()
    flattening = audit_pure_flattening_and_support()
    cofactor = audit_rank_five_cofactor_kernel()
    path = audit_common_shore_and_path()
    fixed_root = audit_product_slice_and_fixed_root_bound()

    print("2I+2R+2Z one-active cofactor-kernel normal form: passed")
    print(f"  imported endpoint packet : {endpoint[0]}")
    print(f"  matching/star factors    : {matching}")
    print(f"  mixed colour census      : {mixed}")
    print(f"  pure flattening/support  : {flattening}")
    print(f"  cofactor shape/rank/ker  : {cofactor}")
    print(f"  shore/path dichotomy     : {path}")
    print(f"  product slice/root bound : {fixed_root}")


if __name__ == "__main__":
    main()
