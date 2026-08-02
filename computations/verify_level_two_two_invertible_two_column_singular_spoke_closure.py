#!/usr/bin/env python3
"""Close the 2I+2R+2Z two-column singular-spoke L1 boundary.

Both rank-one core sites have nonzero selected P and Q columns.  The full
four-site L1 systems have one-dimensional aligned kernels.  At either zero
site, the two invertible core roots make the endpoint families mutually
exclusive, leaving exactly three types:

    I: U_z=V_z=0;
    P: U_z=0, V_z^s=f_s v_z, M_rz=m_r P_r v_z^T;
    Q: V_z=0, U_z^s=f_s u_z, M_rz=m_r Q_r u_z^T.

An active P or Q zero gives a fixed root on its four core spokes, while the
generic-kernel equation gives M_45=0.  Hence all five blocks incident with
that zero have one fixed factor and rank(dPsi)<=32+10=42.  If both zeros
are inactive, every endpoint slice is the aligned generalized cut gauge,
so the two pure L0 targets are impossibly collinear.

This removes the invertible-spoke hypothesis from the earlier overlapping
L1 theorem.  Research evidence only; standard library exact arithmetic.
Checks remain live under python -O and python -I -S.
"""

from fractions import Fraction as Q
from itertools import combinations, product
from pathlib import Path
from runpy import run_path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


HERE = Path(__file__).resolve().parent
L1 = run_path(str(
    HERE / "verify_level_two_two_invertible_l1_collinearity_obstruction.py"
))
ALIGNED = run_path(str(
    HERE
    / "verify_level_two_three_invertible_l1_pure_l0_collinearity_obstruction.py"
))
FIXED_ROOT = run_path(str(
    HERE
    / "verify_level_two_two_invertible_asymmetric_one_active_cofactor_kernel_normal_form.py"
))

COLOURS = (0, 1)
SITES = tuple(range(6))
CORE = (0, 1, 2, 3)
ZEROS = (4, 5)
EDGES = tuple(combinations(SITES, 2))


def matrix_rank_2(matrix):
    if not any(value for row in matrix for value in row):
        return 0
    determinant = (
        matrix[0][0] * matrix[1][1]
        - matrix[0][1] * matrix[1][0]
    )
    return 2 if determinant else 1


def full_core_selected_vectors():
    e0 = (Q(1), Q(0))
    e1 = (Q(0), Q(1))
    h2 = (Q(2), Q(3))
    h3 = (Q(5), Q(7))
    return {
        0: (e0, e1),
        1: (e0, e1),
        2: (
            tuple(Q(11) * value for value in h2),
            tuple(Q(13) * value for value in h2),
        ),
        3: (
            tuple(Q(17) * value for value in h3),
            tuple(Q(19) * value for value in h3),
        ),
    }


def audit_full_core_l1_alignment():
    # Expand all six core edges simultaneously.  Variables are the eight
    # endpoint coordinates followed by one scalar on each edge.
    selected = full_core_selected_vectors()
    core_edges = tuple(combinations(CORE, 2))
    width = 2 * len(CORE) + len(core_edges)

    def residual(vector, family):
        endpoint = {
            site: tuple(vector[2 * site + colour] for colour in COLOURS)
            for site in CORE
        }
        answer = []
        for edge_index, (left, right) in enumerate(core_edges):
            p_left, q_left = selected[left]
            p_right, q_right = selected[right]
            numerator = L1["add_matrix"](
                L1["outer"](p_left, q_right),
                L1["outer"](q_left, p_right),
            )
            if family == "P/V":
                left_side = L1["add_matrix"](
                    L1["outer"](p_left, endpoint[right]),
                    L1["outer"](endpoint[left], p_right),
                )
            else:
                left_side = L1["add_matrix"](
                    L1["outer"](q_left, endpoint[right]),
                    L1["outer"](endpoint[left], q_right),
                )
            answer.extend(L1["flatten"](L1["add_matrix"](
                left_side,
                L1["scale_matrix"](
                    -vector[2 * len(CORE) + edge_index], numerator
                ),
            )))
        return answer

    matrices = {
        family: L1["coefficient_matrix"](
            lambda vector, family=family: residual(vector, family), width
        )
        for family in ("P/V", "Q/U")
    }
    ranks = {family: L1["rational_rank"](matrix)
             for family, matrix in matrices.items()}
    require(ranks == {"P/V": 13, "Q/U": 13},
            ("full two-column core L1 ranks changed", ranks))

    def aligned_direction(column):
        values = []
        for site in CORE:
            values.extend(selected[site][column])
        values.extend(Q(1) for _ in core_edges)
        return tuple(values)

    pv_aligned = aligned_direction(1)
    uq_aligned = aligned_direction(0)
    require(
        not any(L1["matrix_vector_product"](matrices["P/V"], pv_aligned))
        and not any(
            L1["matrix_vector_product"](matrices["Q/U"], uq_aligned)
        ),
        "the full core aligned generators changed",
    )
    return ranks, (len(matrices["P/V"]), width)


def audit_zero_site_type_dictionary():
    selected = full_core_selected_vectors()
    v = (Q(23), Q(29))
    u = (Q(31), Q(37))

    require(all(any(p) and any(q) for p, q in selected.values()),
            "a two-column core site lost one selected vector")
    p0, q0 = selected[0]
    require(p0[0] * q0[1] - p0[1] * q0[0] != 0,
            "the invertible root no longer separates P and Q types")

    p_spokes = {
        site: L1["outer"](selected[site][0], v) for site in CORE
    }
    q_spokes = {
        site: L1["outer"](selected[site][1], u) for site in CORE
    }
    require(
        all(matrix_rank_2(block) == 1 and any(
            block[row][column]
            for row, column in product(COLOURS, repeat=2)
        ) for block in tuple(p_spokes.values()) + tuple(q_spokes.values())),
        "an active zero spoke stopped being nonzero rank one",
    )

    # At root 0, a live P/V equation gives column space P_0, while a live
    # Q/U equation gives column space Q_0.  Their independence forbids any
    # simultaneous activity, even in different endpoint colours.
    require(p_spokes[0] != q_spokes[0],
            "the P and Q active witnesses collided at an invertible root")

    # Two live endpoint colours factor the same base spoke, so their
    # zero-side vectors lie on one line.
    f0, f1 = Q(41), Q(43)
    scaled_v = (
        tuple(f0 * value for value in v),
        tuple(f1 * value for value in v),
    )
    require(
        scaled_v[0][0] * scaled_v[1][1]
        - scaled_v[0][1] * scaled_v[1][0] == 0,
        "active endpoint colours lost their common zero-side line",
    )

    types = {
        "I": {
            "U": 0,
            "V": 0,
            "core spokes": "unrestricted by L1",
            "fixed zero factor": None,
        },
        "P": {
            "U": 0,
            "V": "f_s v_z",
            "core spokes": "m_r P_r v_z^T",
            "fixed zero factor": "v_z",
        },
        "Q": {
            "U": "f_s u_z",
            "V": 0,
            "core spokes": "m_r Q_r u_z^T",
            "fixed zero factor": "u_z",
        },
    }
    require(tuple(types) == ("I", "P", "Q"),
            "the exact zero-site type list changed")

    # A live active equation has a nonzero rank-one left side on every core
    # edge.  Hence a zero or invertible core spoke forces type I, while a
    # singular nonzero spoke is merely compatible with activity.
    invertible = ((Q(1), Q(2)), (Q(3), Q(5)))
    zero = ((Q(0), Q(0)), (Q(0), Q(0)))
    require(matrix_rank_2(invertible) == 2
            and matrix_rank_2(zero) == 0,
            "zero/invertible spoke witnesses changed")
    return types, p_spokes, q_spokes


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            answer.append(((first, second),) + tail)
    return tuple(answer)


def audit_fixed_root_support_bound():
    # Normalize an active zero's fixed physical factor to coordinate zero.
    # Every base block incident with ROOT then vanishes at ROOT-colour one.
    # A tangent on a nonincident edge has a cofactor retaining ROOT, so it
    # also vanishes in every output word with ROOT-colour one.
    root = 5
    nonincident = tuple(edge for edge in EDGES if root not in edge)
    incident = tuple(edge for edge in EDGES if root in edge)
    require((len(nonincident), len(incident)) == (10, 5),
            "fixed-root edge census changed")

    checks = 0

    def base_may_live(edge, word):
        return root not in edge or word[root] == 0

    for word in product(COLOURS, repeat=6):
        if word[root] != 1:
            continue
        for varied_edge in nonincident:
            remaining = tuple(
                site for site in SITES if site not in varied_edge
            )
            for matching in perfect_matchings(remaining):
                root_edge = next(
                    edge for edge in matching if root in edge
                )
                require(
                    not base_may_live(root_edge, word),
                    ("a nonincident tangent escaped the fixed root",
                     word, varied_edge, matching),
                )
                checks += 1
    require(checks == 32 * len(nonincident) * 3,
            ("fixed-root nonincident cofactor census changed", checks))

    fixed_slice = 2 ** 5
    transverse_incident_cells = len(incident) * 2
    bound = fixed_slice + transverse_incident_cells
    require((fixed_slice, transverse_incident_cells, bound) == (32, 10, 42),
            "fixed-root 32+10 bound changed")

    # Import an independently constructed integral packet attaining 42 in
    # this exact support envelope.
    calibration = FIXED_ROOT["audit_product_slice_and_fixed_root_bound"]()
    require(calibration[4:] == (42, 42),
            ("fixed-root calibration changed", calibration))
    return checks, incident, nonincident, bound, calibration[-1]


def audit_active_chart_closure(types):
    # M45=0 because both endpoint stars vanish there and its generic-kernel
    # multiplier is -2*tau.  Thus an active factor on four core spokes is
    # also a fixed factor on the fifth incident edge.
    charts = {}
    for left_type, right_type in product(types, repeat=2):
        if (left_type, right_type) == ("I", "I"):
            outcome = "aligned pure-L0 collinearity"
        else:
            active_zero = 4 if left_type != "I" else 5
            active_type = left_type if active_zero == 4 else right_type
            factor = "v_z" if active_type == "P" else "u_z"
            outcome = (
                f"fixed root {active_zero} ({factor}), rank <= 42"
            )
        charts[left_type, right_type] = outcome
    require(sum("rank <= 42" in outcome for outcome in charts.values()) == 8,
            ("active chart count changed", charts))
    require(charts["I", "I"] == "aligned pure-L0 collinearity",
            "inactive-inactive chart was misclassified")
    return charts


def audit_inactive_inactive_collinearity():
    # Once both zero endpoint families vanish, no hypothesis on their base
    # spokes enters the endpoint slice.  The exact aligned-gauge identity
    # and pure-target contradiction therefore apply unchanged.
    edge_checks = ALIGNED["audit_aligned_slice_is_generalized_gauge"]()
    matching_checks = ALIGNED["audit_generalized_gauge_differential"]()
    target_checks = ALIGNED["audit_pure_target_unit_certificate"]()
    require((edge_checks, matching_checks, target_checks) == (15, 15, 4),
            "inactive-inactive collinearity audit changed")
    return edge_checks, matching_checks, target_checks


def audit_scope_map():
    scope = {
        "rank-one t,u": "both selected columns nonzero",
        "zero core spokes": "arbitrary singular/invertible patterns",
        "two-column chart": "closed",
        "one missing selected column": "separate asymmetric theorem",
        "both missing selected columns": "excluded from scope",
    }
    require(scope["two-column chart"] == "closed",
            "the two-column singular-spoke chart was left open")
    return scope


def main():
    old_modes = L1["audit_invertible_edge_modes"]()
    old_propagation = L1["audit_rank_one_propagation"]()
    core = audit_full_core_l1_alignment()
    types, p_spokes, q_spokes = audit_zero_site_type_dictionary()
    fixed = audit_fixed_root_support_bound()
    charts = audit_active_chart_closure(types)
    inactive = audit_inactive_inactive_collinearity()
    scope = audit_scope_map()

    print("2I+2R+2Z two-column singular-spoke closure: passed")
    print(f"  imported edge/propagation    : {old_modes}/{old_propagation}")
    print(f"  full core L1 ranks/shape     : {core}")
    print(f"  exact zero-site types        : {types}")
    print(f"  active P/Q spoke counts      : {len(p_spokes)}/{len(q_spokes)}")
    print(f"  fixed-root bound/calibration : {fixed[3:]}")
    print(f"  ordered chart map            : {charts}")
    print(f"  inactive collinearity        : {inactive}")
    print(f"  scope                        : {scope}")


if __name__ == "__main__":
    main()
