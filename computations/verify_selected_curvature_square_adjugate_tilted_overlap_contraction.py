#!/usr/bin/env python3
"""Exact audit of the selected-square all-label overlap contraction.

The checker works before multiplication by a common divided power.  It
verifies the connection, opposite-shore connection, normal companions,
curvature-normal split, and the transpose-adjugate contraction for three
physical labels.  It then checks every tilt J=I+E_ij, the full direct-free
specialization, and the target/residue rank obstruction at h=3.

This is a standard-library-only research checker.  All guards remain live
under ``python -O`` and ``python -I -S``.
"""

from fractions import Fraction
from hashlib import sha256
import json


Q = Fraction
ZERO = Q(0)
ONE = Q(1)
LABELS = range(3)
RESIDUAL_SITES = range(6)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def clean(poly):
    return {monomial: coefficient for monomial, coefficient in poly.items() if coefficient}


def constant(value):
    value = Q(value)
    return {} if value == 0 else {(): value}


def variable(name):
    return {(name,): ONE}


def add(*polys):
    result = {}
    for poly in polys:
        for monomial, coefficient in poly.items():
            result[monomial] = result.get(monomial, ZERO) + coefficient
    return clean(result)


def scale(value, poly):
    value = Q(value)
    return clean({monomial: value * coefficient for monomial, coefficient in poly.items()})


def subtract(left, right):
    return add(left, scale(-ONE, right))


def multiply(*polys):
    result = constant(ONE)
    for poly in polys:
        product = {}
        for left_monomial, left_coefficient in result.items():
            for right_monomial, right_coefficient in poly.items():
                monomial = tuple(sorted(left_monomial + right_monomial))
                product[monomial] = product.get(monomial, ZERO) + (
                    left_coefficient * right_coefficient
                )
        result = clean(product)
    return result


def poly_sum(terms):
    return add(*list(terms))


def set_zero(poly, names):
    names = set(names)
    return clean(
        {
            monomial: coefficient
            for monomial, coefficient in poly.items()
            if not any(name in names for name in monomial)
        }
    )


def matrix_rank(matrix):
    if not matrix:
        return 0
    work = [[Q(entry) for entry in row] for row in matrix]
    row_count = len(work)
    column_count = len(work[0])
    result = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(result, row_count) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[result], work[pivot] = work[pivot], work[result]
        pivot_value = work[result][column]
        work[result] = [entry / pivot_value for entry in work[result]]
        for row in range(row_count):
            if row == result:
                continue
            coefficient = work[row][column]
            if coefficient:
                work[row] = [
                    entry - coefficient * pivot_entry
                    for entry, pivot_entry in zip(work[row], work[result])
                ]
        result += 1
    return result


def build_symbolic_packet():
    z, y, v = variable("z"), variable("y_b"), variable("v_d")
    q_direct = variable("Q_bd")
    p = [variable(f"P_{i}b") for i in LABELS]
    s = [variable(f"S_{k}d") for k in LABELS]
    x = [variable(f"x_{i}") for i in LABELS]
    t = [variable(f"t_{k}") for k in LABELS]
    e = [variable(f"E_{i}d") for i in LABELS]
    qr = [variable(f"T_b{k}") for k in LABELS]
    cross = [[variable(f"R_{i}{k}") for k in LABELS] for i in LABELS]

    f = [add(multiply(p[i], z), multiply(x[i], y)) for i in LABELS]
    g = [
        [add(multiply(cross[i][k], z), multiply(x[i], t[k])) for k in LABELS]
        for i in LABELS
    ]
    h_opposite = add(multiply(q_direct, z), multiply(y, v))
    n_opposite = [add(multiply(s[k], z), multiply(t[k], v)) for k in LABELS]
    h_normal = [
        add(multiply(p[i], v), multiply(e[i], y), multiply(q_direct, x[i]))
        for i in LABELS
    ]
    n_normal = [
        [
            add(
                multiply(cross[i][k], v),
                multiply(e[i], t[k]),
                multiply(s[k], x[i]),
            )
            for k in LABELS
        ]
        for i in LABELS
    ]

    transition = [[None for _ in LABELS] for _ in LABELS]
    opposite = [[None for _ in LABELS] for _ in LABELS]
    curvature = [[None for _ in LABELS] for _ in LABELS]
    common = [[None for _ in LABELS] for _ in LABELS]
    for i in LABELS:
        for k in LABELS:
            transition[i][k] = subtract(multiply(p[i], t[k]), multiply(cross[i][k], y))
            opposite[i][k] = subtract(multiply(s[k], y), multiply(q_direct, t[k]))
            curvature[i][k] = subtract(
                multiply(p[i], s[k]), multiply(cross[i][k], q_direct)
            )
            common[i][k] = multiply(x[i], opposite[i][k])

            connection = subtract(
                subtract(multiply(f[i], t[k]), multiply(g[i][k], y)),
                multiply(transition[i][k], z),
            )
            require(not connection, f"connection failed at {(i, k)}")

            opposite_connection = subtract(
                subtract(multiply(n_opposite[k], y), multiply(h_opposite, t[k])),
                multiply(opposite[i][k], z),
            )
            require(not opposite_connection, f"opposite connection failed at {(i, k)}")

            # The two chart-normal differences expose D and E before any
            # common matching power is applied.  Here h=3, so h-1=2.
            h_degree = Q(3)
            pq_at_r = add(
                scale(h_degree, multiply(cross[i][k], y)),
                scale(h_degree, multiply(qr[k], x[i])),
                multiply(p[i], t[k]),
            )
            pr_at_q = add(
                scale(h_degree, multiply(p[i], t[k])),
                scale(h_degree, multiply(qr[k], x[i])),
                multiply(cross[i][k], y),
            )
            require(
                not add(
                    subtract(pq_at_r, pr_at_q),
                    scale(h_degree - 1, transition[i][k]),
                ),
                f"D normal companion failed at {(i, k)}",
            )

            qs_at_r = add(
                scale(h_degree, multiply(qr[k], v)),
                scale(h_degree, multiply(s[k], y)),
                multiply(q_direct, t[k]),
            )
            rs_at_q = add(
                scale(h_degree, multiply(qr[k], v)),
                scale(h_degree, multiply(q_direct, t[k])),
                multiply(s[k], y),
            )
            require(
                not subtract(
                    subtract(qs_at_r, rs_at_q),
                    scale(h_degree - 1, opposite[i][k]),
                ),
                f"E opposite normal companion failed at {(i, k)}",
            )

            first_half = subtract(
                subtract(
                    subtract(multiply(s[k], f[i]), multiply(q_direct, g[i][k])),
                    multiply(curvature[i][k], z),
                ),
                common[i][k],
            )
            require(not first_half, f"first normal half failed at {(i, k)}")

            second_half = add(
                subtract(
                    subtract(multiply(t[k], h_normal[i]), multiply(y, n_normal[i][k])),
                    multiply(transition[i][k], v),
                ),
                common[i][k],
            )
            require(not second_half, f"second normal half failed at {(i, k)}")

            full_normal = subtract(
                add(
                    multiply(s[k], f[i]),
                    multiply(t[k], h_normal[i]),
                    scale(-ONE, multiply(q_direct, g[i][k])),
                    scale(-ONE, multiply(y, n_normal[i][k])),
                ),
                add(multiply(transition[i][k], v), multiply(curvature[i][k], z)),
            )
            require(not full_normal, f"curvature normal failed at {(i, k)}")

    return {
        "z": z,
        "y": y,
        "v": v,
        "q_direct": q_direct,
        "p": p,
        "s": s,
        "x": x,
        "t": t,
        "cross": cross,
        "qr": qr,
        "transition": transition,
        "opposite": opposite,
        "curvature": curvature,
        "common": common,
        "f": f,
        "g": g,
        "h_normal": h_normal,
        "n_normal": n_normal,
    }


def contract(weights, entries):
    return poly_sum(
        scale(weights[i][k], entries[i][k])
        for i in LABELS
        for k in LABELS
        if weights[i][k]
    )


def matrix_unit(row, column):
    return [[ONE if (i, k) == (row, column) else ZERO for k in LABELS] for i in LABELS]


def identity():
    return [[ONE if i == k else ZERO for k in LABELS] for i in LABELS]


def matrix_add(left, right):
    return [[left[i][k] + right[i][k] for k in LABELS] for i in LABELS]


def check_contractions(packet):
    # The selected direct square has the displayed orientation
    # [[A,B],[F,U]].  Its transpose adjugate sends (y,t) to (E,D).
    a, c = 0, 1
    A = packet["p"][a]
    B = packet["cross"][a][c]
    F = packet["q_direct"]
    U = packet["s"][c]
    D = packet["transition"][a][c]
    E = packet["opposite"][a][c]
    kappa = packet["curvature"][a][c]
    y, t = packet["y"], packet["t"][c]

    require(not subtract(add(multiply(A, E), multiply(F, D)), multiply(kappa, y)),
            "first transpose-adjugate identity failed")
    require(not subtract(add(multiply(B, E), multiply(U, D)), multiply(kappa, t)),
            "second transpose-adjugate identity failed")

    # At h=3 the two normal companions expose -2D and +2E.  Dividing by
    # these fixed nonzero scalars and by kappa contracts the star channel;
    # no entry, trace, star, or internal quadratic is inverted.
    h = Q(3)
    normal_d = scale(-(h - 1), D)
    normal_e = scale(h - 1, E)
    recovered_y_numerator = add(
        scale(ONE / (h - 1), multiply(A, normal_e)),
        scale(-ONE / (h - 1), multiply(F, normal_d)),
    )
    recovered_t_numerator = add(
        scale(ONE / (h - 1), multiply(B, normal_e)),
        scale(-ONE / (h - 1), multiply(U, normal_d)),
    )
    require(not subtract(recovered_y_numerator, multiply(kappa, y)),
            "normal-companion contraction did not recover kappa*y")
    require(not subtract(recovered_t_numerator, multiply(kappa, t)),
            "normal-companion contraction did not recover kappa*t")

    # Every J=I+E_ij has the all-label contracted connection and normal.
    tilt_records = []
    for row in LABELS:
        for column in LABELS:
            J = matrix_add(identity(), matrix_unit(row, column))
            d_j = contract(J, packet["transition"])
            e_j = contract(J, packet["opposite"])
            gamma_j = contract(J, packet["curvature"])
            common_j = contract(J, packet["common"])

            first_j = poly_sum(
                scale(
                    J[i][k],
                    subtract(
                        multiply(packet["s"][k], packet["f"][i]),
                        multiply(packet["q_direct"], packet["g"][i][k]),
                    ),
                )
                for i in LABELS
                for k in LABELS
                if J[i][k]
            )
            second_j = poly_sum(
                scale(
                    J[i][k],
                    subtract(
                        multiply(packet["t"][k], packet["h_normal"][i]),
                        multiply(packet["y"], packet["n_normal"][i][k]),
                    ),
                )
                for i in LABELS
                for k in LABELS
                if J[i][k]
            )
            require(not subtract(first_j, add(multiply(gamma_j, packet["z"]), common_j)),
                    f"tilted first normal half failed for J=I+E_{row}{column}")
            require(not subtract(second_j, subtract(multiply(d_j, packet["v"]), common_j)),
                    f"tilted second normal half failed for J=I+E_{row}{column}")

            target = [J[label][label] for label in LABELS]
            expected_target = [ONE + (ONE if row == column == label else ZERO)
                               for label in LABELS]
            require(target == expected_target,
                    f"tilted diagonal target changed for J=I+E_{row}{column}")
            require(all(target), f"tilted J lost a diagonal target at {(row, column)}")
            tilt_records.append((row, column, tuple(str(value) for value in target), bool(common_j)))

            # The selected u coefficient remains the original kappa.
            line_gamma_u = contract(matrix_unit(a, c), packet["curvature"])
            require(line_gamma_u == kappa, "tilted line lost selected curvature coefficient")
            require(e_j, f"opposite-shore J contraction vanished formally at {(row, column)}")

    return kappa, tilt_records


def check_direct_free(packet):
    cross_names = {f"R_{i}{k}" for i in LABELS for k in LABELS}
    a, c = 0, 1
    A = packet["p"][a]
    F = packet["q_direct"]
    U = packet["s"][c]
    D = set_zero(packet["transition"][a][c], cross_names)
    E = set_zero(packet["opposite"][a][c], cross_names)
    kappa = set_zero(packet["curvature"][a][c], cross_names)
    common = set_zero(packet["common"][a][c], cross_names)

    require(not subtract(D, multiply(A, packet["t"][c])), "direct-free D is not A*t")
    require(not subtract(kappa, multiply(A, U)), "direct-free kappa is not A*U")
    require(not subtract(add(multiply(A, E), multiply(F, D)), multiply(kappa, packet["y"])),
            "direct-free adjugate did not recover y")
    require(not subtract(multiply(U, D), multiply(kappa, packet["t"][c])),
            "direct-free triangular contraction did not recover t")
    require(common, "direct-free middle common mode vanished identically")

    selected_normal = add(
        multiply(U, packet["f"][a]),
        multiply(packet["t"][c], packet["h_normal"][a]),
        scale(-ONE, multiply(F, set_zero(packet["g"][a][c], cross_names))),
        scale(-ONE, multiply(packet["y"], set_zero(packet["n_normal"][a][c], cross_names))),
    )
    triangular = subtract(
        selected_normal,
        add(multiply(D, packet["v"]), multiply(kappa, packet["z"])),
    )
    require(not triangular, "direct-free normal is not D*v+A*U*z")

    # The direct-free full-nine auxiliary retains the three literal
    # diagonal targets under the I contraction.
    target = tuple(identity()[label][label] for label in LABELS)
    require(target == (ONE, ONE, ONE), "direct-free diagonal target was lost")
    return bool(common), tuple(str(value) for value in target)


def check_target_and_adjacent_power_obstruction():
    # For every all-label exposed target word, all pair-chart presentations
    # have the same physical indicator.  Their differences are target-zero.
    target_checks = 0
    for i in LABELS:
        for j in LABELS:
            for k in LABELS:
                for ell in LABELS:
                    for colour in LABELS:
                        pq = int(i == j == k == ell == colour)
                        pr = int(i == k == j == ell == colour)
                        qs = int(j == ell == i == k == colour)
                        rs = int(k == ell == i == j == colour)
                        require(pq == pr == qs == rs,
                                "physical all-label target changed between charts")
                        target_checks += 1

    # At h=3 the same-power cap lock sends a physical target vector T to
    # (T, diag(Y)T).  The three anchor graph rows have no target-zero,
    # residue-nonzero combination.  Adding any number of target-zero
    # connection/normal/adjugate rows cannot change this rank fact.
    y_values = (Q(2, 3), Q(-5, 7), Q(11, 4))
    graph_rows = []
    for label in LABELS:
        row = [ZERO] * 6
        row[label] = ONE
        row[3 + label] = y_values[label]
        graph_rows.append(row)
    target_projection = [row[:3] for row in graph_rows]
    require(matrix_rank(graph_rows) == 3, "anchor graph rank changed")
    require(matrix_rank(target_projection) == 3, "target projection acquired a kernel")

    # Two chart copies have identical graphs.  Their relative differences
    # are literally zero in target and residue; the common copy survives.
    relative_rows = [
        [left - right for left, right in zip(row, row)] for row in graph_rows
    ]
    require(matrix_rank(relative_rows) == 0, "chart difference retained a cap graph")
    require(any(graph_rows[0]), "common anchor graph vanished")

    # The filtered obstruction asks for (0,-kappa*Y_c).  It is not in the
    # same-power graph span with zero target.  This is the exact reason the
    # scalar adjugate rows cannot furnish the new adjacent-power generator.
    kappa = Q(13, 5)
    colour = 1
    desired = [ZERO, ZERO, ZERO, ZERO, -kappa * y_values[colour], ZERO]
    require(desired[3 + colour] != ZERO, "desired residue sample vanished")
    require(matrix_rank(graph_rows + [desired]) == 4,
            "target-zero residue unexpectedly entered the same-power graph span")
    return target_checks, [str(value) for value in y_values]


def check_exact_missing_cross_word_rows():
    """Classify the exact full-EqSystem gaps of the two bounded guards.

    The three pure rows are target-bearing anchor graphs.  Every mixed gap
    is a one-r-site cross-word normal row, but its five-site odd word
    ``W minus {x}`` is not monochromatic, so its coefficient on every physical Y_c
    is zero.  Thus these exact extra rows can invalidate the finite guard,
    but they do not themselves supply the target-zero Y_c generator.
    """

    packets = {
        "direct_free": {
            "r": 3,
            "x": 0,
            "selected": (0, 1, 2, 0, 1, 2),
            "failures": (
                ((0, 0, 0, 0, 0, 0), 0, 0, ZERO, ONE),
                ((0, 1, 2, 1, 1, 2), 2, 2, ONE, ZERO),
                ((0, 1, 2, 2, 1, 2), 2, 1, ONE, ZERO),
                ((0, 1, 2, 2, 1, 2), 2, 2, ONE, ZERO),
                ((1, 1, 1, 1, 1, 1), 1, 1, ZERO, ONE),
                ((2, 2, 2, 2, 2, 2), 2, 2, ZERO, ONE),
            ),
        },
        "tilted": {
            "r": 1,
            "x": 0,
            "selected": (0, 1, 2, 0, 1, 2),
            "failures": (
                ((0, 0, 0, 0, 0, 0), 0, 0, ZERO, ONE),
                ((0, 0, 2, 0, 1, 2), 2, 2, Q(1, 2), ZERO),
                ((0, 2, 2, 0, 1, 2), 0, 2, Q(-3, 2), ZERO),
                ((0, 2, 2, 0, 1, 2), 2, 0, Q(1, 2), ZERO),
                ((0, 2, 2, 0, 1, 2), 2, 2, Q(-1, 4), ZERO),
                ((1, 1, 1, 1, 1, 1), 1, 1, ZERO, ONE),
                ((2, 2, 2, 2, 2, 2), 2, 2, ZERO, ONE),
            ),
        },
    }

    summary = {}
    for name, packet in packets.items():
        pure = []
        mixed = []
        for word, left, right, value, target in packet["failures"]:
            global_word = word + (left, right)
            is_pure = len(set(global_word)) == 1
            if is_pure:
                colour = global_word[0]
                require(target == ONE and left == right == colour,
                        f"{name}: pure failure is not a diagonal target")
                odd_word = tuple(
                    word[site] for site in RESIDUAL_SITES if site != packet["x"]
                )
                require(odd_word == (colour,) * 5,
                        f"{name}: pure anchor lost its Y_c word")
                pure.append((colour, str(value), str(target)))
            else:
                require(target == ZERO, f"{name}: mixed gap acquired a target")
                changed_residual_sites = tuple(
                    site
                    for site in RESIDUAL_SITES
                    if word[site] != packet["selected"][site]
                )
                require(changed_residual_sites == (packet["r"],),
                        f"{name}: mixed gap is not an r-normal cross word")
                odd_word = tuple(
                    word[site] for site in RESIDUAL_SITES if site != packet["x"]
                )
                require(len(set(odd_word)) > 1,
                        f"{name}: mixed gap unexpectedly supports a physical Y_c")
                y_coefficients = tuple(
                    int(all(label == colour for label in odd_word)) for colour in LABELS
                )
                require(y_coefficients == (0, 0, 0),
                        f"{name}: mixed cross word has nonzero odd target residue")
                mixed.append((word, left, right, str(value), odd_word))

        require(tuple(item[0] for item in pure) == (0, 1, 2),
                f"{name}: exact pure anchor list changed")
        expected_mixed = 3 if name == "direct_free" else 4
        require(len(mixed) == expected_mixed,
                f"{name}: exact mixed cross-word count changed")
        summary[name] = {"pure": pure, "mixed": mixed}

    # In the target/physical-odd readout the exact missing-row packet still
    # consists only of the three graph anchors; every mixed row reads zero.
    # Its target-zero kernel therefore has zero odd readout.
    y = (Q(3, 5), Q(-7, 4), Q(11, 6))
    pure_graphs = []
    for colour in LABELS:
        row = [ZERO] * 6
        row[colour] = ONE
        row[3 + colour] = y[colour]
        pure_graphs.append(row)
    require(matrix_rank([row[:3] for row in pure_graphs]) == 3,
            "exact missing pure anchors acquired a target-zero kernel")
    desired = [ZERO, ZERO, ZERO, ZERO, -Q(5, 2) * y[1], ZERO]
    require(matrix_rank(pure_graphs + [desired]) == 4,
            "exact missing rows generated the target-zero odd class")
    return summary


def main():
    packet = build_symbolic_packet()
    kappa, tilt_records = check_contractions(packet)
    direct_free_common, direct_free_target = check_direct_free(packet)
    target_checks, y_values = check_target_and_adjacent_power_obstruction()
    exact_missing = check_exact_missing_cross_word_rows()
    record = {
        "labels": 3,
        "tilts": len(tilt_records),
        "tilt_records": tilt_records,
        "selected_kappa_terms": len(kappa),
        "direct_free_common_nonzero": direct_free_common,
        "direct_free_target": direct_free_target,
        "all_label_target_checks": target_checks,
        "same_power_y_values": y_values,
        "exact_missing": exact_missing,
    }
    digest = sha256(
        json.dumps(record, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    print("selected-square all-label adjugate overlap contraction: PASS")
    print("all 9 tilts and the direct-free specialization audited")
    print("absolute diagonal targets retained; relative target/residue graphs cancel")
    print("new adjacent-power generator: not supplied by selected adjugate rows")
    print("sha256:", digest)


if __name__ == "__main__":
    main()
