#!/usr/bin/env python3
"""Exact occurrence-lift/Fitting independence counterguard.

The occurrence resolution L_r retains one common carrier line, makes every
centered occurrence exact, and lifts every restriction/insertion
correspondence functorially.  Tensoring it with the pinned based-loop moment
complex preserves all this occurrence structure while preserving the
nonzero exceptional clean class.  Thus a complete occurrence lift alone
does not imply the uniform Fitting wedge.

This is a logical filtered-DGM counterguard, not a decorated matching
source.  The accompanying note states the precise physical scope.
"""

from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import combinations
from math import factorial
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "notes/uniform-centered-occurrence-endpoint-association-projector.md":
        "6be3edc16be3b429f517fe007886fd3289281f8e8acdde1f13ebebf2a20bb836",
    "computations/verify_uniform_centered_occurrence_endpoint_association_projector.py":
        "0ef88312cead100120e4600ea3a2d0616262a96bf27726d07817610d11b43f59",
    "notes/uniform-centered-occurrence-restriction-insertion-gate.md":
        "c3161b740606a19d1fb238921986a6ab3b9c2f9cec9d7bc9a9410059f8c213da",
    "computations/verify_uniform_centered_occurrence_restriction_insertion_gate.py":
        "cb328adc1f23b38f6f9f9305635ddbaef888178633f8db91c205fdfbdca1ff34",
    "notes/scalar-unit-moment-transgression-source-lift-based-loop-torsor.md":
        "8df4b715775194282542cf1ea057b8305223744504687e5e480c4c262fcecd4a",
    "computations/verify_scalar_unit_moment_transgression_source_lift_based_loop_torsor.py":
        "4bff53e1568a74cfe262fac185558aa14337fe1a2e31e6c46141645e78e8e839",
    "notes/scalar-unit-carrier-moment-tower-hilbert-cauchy.md":
        "c9a58db12d8959a3b498c3e6b0ae54aeb49224476fb02d264d21d77d8a230855",
    "computations/verify_scalar_unit_carrier_moment_tower_hilbert_cauchy.py":
        "b1674da530c0af1790780bb19fadc7622117b373ece3e9a0845cbb532870e3f3",
}


Q = Fraction
Edge = tuple[int, int]
Matching = tuple[Edge, ...]
Occurrence = tuple[int, int, Matching]


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def edge(left, right):
    require(left != right, "loop")
    return (left, right) if left < right else (right, left)


@lru_cache(maxsize=None)
def perfect_matchings(vertices):
    if not vertices:
        return ((),)
    first = vertices[0]
    result = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            result.append(tuple(sorted((edge(first, second),) + tail)))
    return tuple(result)


def occurrences(vertices):
    result = []
    for p_site in vertices:
        for s_site in vertices:
            if p_site == s_site:
                continue
            residual = tuple(site for site in vertices
                             if site not in (p_site, s_site))
            for matching in perfect_matchings(residual):
                result.append((p_site, s_site, matching))
    require(len(result) == len(set(result)), "duplicate occurrence")
    return tuple(result)


def odd_double_factorial(value):
    result = 1
    for factor in range(value, 0, -2):
        result *= factor
    return result


def occurrence_count(order):
    return 2 * order * (2 * order - 1) * odd_double_factorial(2 * order - 3)


def average(vector):
    return sum(vector, Q(0)) / len(vector)


def differential(vector):
    """d_r x=(x,-avg_r x) in L_r."""
    return tuple(vector), -average(vector)


def projection(degree_zero):
    """p_r(o,a)=avg_r(o)+a."""
    vector, carrier = degree_zero
    return average(vector) + carrier


def inclusion(scalar, width):
    return (tuple(Q(0) for _ in range(width)), Q(scalar))


def homotopy(degree_zero):
    """s_r(o,a)=o."""
    return degree_zero[0]


def lift_map(matrix_columns, induced_scalar):
    """Return degree-one and degree-zero actions of T^#.

    matrix_columns are the images of source occurrence basis vectors.
    T^#(o,a)=(To, c*a+c*avg(o)-avg(To)).
    """
    source_width = len(matrix_columns)
    target_width = len(matrix_columns[0])

    def top(vector):
        require(len(vector) == source_width, "top source width")
        return tuple(sum((vector[column] * matrix_columns[column][row]
                          for column in range(source_width)), Q(0))
                     for row in range(target_width))

    def degree_zero(degree_zero_vector):
        vector, carrier = degree_zero_vector
        image = top(vector)
        corrected = (Q(induced_scalar) * carrier
                     + Q(induced_scalar) * average(vector)
                     - average(image))
        return image, corrected

    return top, degree_zero


def restriction_matrix(source, lower, selected):
    lower_index = {occurrence: index for index, occurrence in enumerate(lower)}
    columns = []
    for p_site, s_site, matching in source:
        column = [Q(0)] * len(lower)
        if selected in matching:
            image = (p_site, s_site,
                     tuple(candidate for candidate in matching
                           if candidate != selected))
            column[lower_index[image]] = Q(1)
        columns.append(tuple(column))
    return tuple(columns)


def insertion_matrix(source, lower, selected):
    source_index = {occurrence: index for index, occurrence in enumerate(source)}
    columns = []
    for p_site, s_site, matching in lower:
        image = (p_site, s_site, tuple(sorted(matching + (selected,))))
        column = [Q(0)] * len(source)
        column[source_index[image]] = Q(1)
        columns.append(tuple(column))
    return tuple(columns)


def apply_matrix(columns, vector):
    return tuple(sum((vector[column] * columns[column][row]
                      for column in range(len(columns))), Q(0))
                 for row in range(len(columns[0])))


def add_vectors(*vectors):
    return tuple(sum((vector[index] for vector in vectors), Q(0))
                 for index in range(len(vectors[0])))


def scale_vector(vector, scalar):
    return tuple(Q(scalar) * entry for entry in vector)


def audit_occurrence_resolution(order):
    vertices = tuple(range(2 * order))
    source = occurrences(vertices)
    require(len(source) == occurrence_count(order), "occurrence count")
    width = len(source)

    # Exact deformation retract L_r -> k.
    probes = (
        tuple(Q(int(index == 0)) for index in range(width)),
        tuple(Q((index % 5) - 2) for index in range(width)),
        tuple(Q(1) for _ in range(width)),
    )
    for vector in probes:
        for carrier in (Q(-3), Q(0), Q(5, 2)):
            degree_zero = (vector, carrier)
            require(projection(differential(homotopy(degree_zero))) == 0,
                    "p*d*s stopped vanishing")
            right = inclusion(projection(degree_zero), width)
            left = differential(homotopy(degree_zero))
            recovered = (add_vectors(left[0], right[0]), left[1] + right[1])
            require(recovered == degree_zero, "ds+ip != id")

    marked = source[0]
    centered = tuple(Q(len(source) if item == marked else 0) - 1
                     for item in source)
    require(average(centered) == 0, "centered augmentation")
    require(differential(centered) == (centered, Q(0)),
            "centered class not an exact physical cell")

    # Every residual restriction and reinsertion has a canonical augmented
    # chain lift.  The normalized carrier scalars are 1 and 1/alpha.
    residual_edges = tuple(edge(left, right)
                           for left, right in combinations(vertices, 2))
    alpha = Q(order * (2 * order - 1), order - 1)
    for selected in residual_edges:
        complement = tuple(site for site in vertices if site not in selected)
        lower = occurrences(complement)
        d_columns = restriction_matrix(source, lower, selected)
        i_columns = insertion_matrix(source, lower, selected)

        d_top, d_zero = lift_map(d_columns, Q(1))
        i_top, i_zero = lift_map(i_columns, Q(1, 1) / alpha)

        for vector in probes[:2]:
            top_image = d_top(vector)
            require(d_zero(differential(vector))
                    == differential(top_image), "D_e^# not a chain map")
        lower_probe = tuple(Q((index % 3) - 1) for index in range(len(lower)))
        inserted = i_top(lower_probe)
        require(i_zero(differential(lower_probe))
                == differential(inserted), "I_e^# not a chain map")

    # Each occurrence contains exactly r-1 residual matching edges, so the
    # top Euler sum is (r-1)id.  The normalized carrier scalar has the same
    # sum because |E(K_2r)|/alpha=r-1.  By the displayed canonical lift
    # formula, the whole augmented sum is therefore (r-1)id.
    require(len(residual_edges) / alpha == order - 1,
            "augmented Euler carrier scalar")

    return {
        "order": order,
        "occurrences": width,
        "centered_exact": True,
        "deformation_retract_to_common_carrier": True,
        "restriction_carrier_scalar": "1",
        "insertion_carrier_scalar": str(Q(1, 1) / alpha),
        "augmented_euler": f"sum I_e^# D_e^#={order - 1} id",
    }


def exact_rank(columns):
    require(columns, "rank without columns")
    rows = len(columns[0])
    matrix = [[Q(columns[column][row]) for column in range(len(columns))]
              for row in range(rows)]
    pivot_row = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(pivot_row, rows)
                      if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        value = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / value for entry in matrix[pivot_row]]
        for row in range(rows):
            if row == pivot_row or not matrix[row][column]:
                continue
            multiple = matrix[row][column]
            matrix[row] = [entry - multiple * pivot_entry
                           for entry, pivot_entry
                           in zip(matrix[row], matrix[pivot_row])]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def multiply_q(vector, degree):
    output = [Q(0)] * (degree + 2)
    for r_degree, coefficient in enumerate(vector):
        output[r_degree] += (degree + 1 - r_degree) * coefficient
    return output


def multiply_r(vector, degree):
    output = [Q(0)] * (degree + 2)
    for r_degree, coefficient in enumerate(vector):
        output[r_degree + 1] += (r_degree + 1) * coefficient
    return output


def carrier(h, moment):
    n = h - 2
    h_s = [Q(1, moment + ell + 1) for ell in range(n + 1)]
    return [left - 2 * right for left, right
            in zip(multiply_r(h_s, n), multiply_q(h_s, n))]


def clean_vector(h):
    return [Q(int(index >= 2)) for index in range(h + 1)]


def target_vector(h):
    return [Q(int(index <= 1)) for index in range(h + 1)]


def polynomial_multiply(left, right):
    output = [Q(0)] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            output[i + j] += a * b
    return output


def polynomial_derivative(poly, order=1):
    output = list(poly)
    for _ in range(order):
        output = [Q(index) * output[index]
                  for index in range(1, len(output))]
    return output or [Q(0)]


def integral(poly, weight=0):
    return sum((coefficient / Q(index + weight + 1)
                for index, coefficient in enumerate(poly)), Q(0))


def eta(index):
    seed = polynomial_multiply(
        [Q(0)] * index + [Q(1)],
        [Q((-1) ** power * factorial(index),
           factorial(power) * factorial(index - power))
         for power in range(index + 1)],
    )
    return polynomial_derivative(seed, index - 1)


def audit_moment_independence(h):
    c_zero = carrier(h, 0)
    boundary_columns = [
        clean_vector(h),
        multiply_q(c_zero, h - 1),
        multiply_r(c_zero, h - 1),
    ]
    target = target_vector(h)
    require(exact_rank(boundary_columns)
            < exact_rank(boundary_columns + [target]),
            f"h={h}: c0 unexpectedly killed the exceptional target")

    moment_count = 1 if h == 3 else h - 3
    residue_matrix = []
    for moment in range(1, moment_count + 1):
        row = []
        for loop_index in range(1, moment_count + 1):
            loop_derivative = polynomial_derivative(eta(loop_index))
            row.append(integral(loop_derivative, weight=moment))
        residue_matrix.append(row)
    residue_columns = [
        [residue_matrix[row][column] for row in range(moment_count)]
        for column in range(moment_count)
    ]
    require(exact_rank(residue_columns) == moment_count,
            f"h={h}: based-loop residues lost rank")
    require(all(integral(polynomial_derivative(eta(index)), weight=0) == 0
                for index in range(1, moment_count + 1)),
            f"h={h}: a based loop changed the common H0 carrier")

    return {
        "h": h,
        "c0_exact_but_target_survives": True,
        "required_higher_moments": moment_count,
        "based_loop_residue_rank": moment_count,
    }


def shift_form(form, shift, total_degree):
    output = [Q(0)] * (total_degree + 1)
    for v_degree, coefficient in enumerate(form):
        output[v_degree + shift] += coefficient
    return output


def audit_pure_axis_fitting(h):
    """The two carrier-valued clean tails u^h and v^h have full Macaulay rank."""
    u_axis = [Q(0)] * (h + 1)
    v_axis = [Q(0)] * (h + 1)
    u_axis[0] = Q(1)
    v_axis[h] = Q(1)
    columns = []
    for form in (u_axis, v_axis):
        for shift in range(h):
            columns.append(shift_form(form, shift, 2 * h - 1))
    rank = exact_rank(columns)
    require(rank == 2 * h, f"h={h}: pure-axis Macaulay rank {rank}")
    return {
        "h": h,
        "clean_forms": ["u^h", "v^h"],
        "carrier_copies": 2,
        "macaulay_rank": rank,
        "top_fitting_wedge_nonzero": True,
    }


def audit():
    pin_dependencies()
    occurrence_records = [audit_occurrence_resolution(order)
                          for order in (2, 3, 4)]
    moment_records = [audit_moment_independence(h) for h in range(3, 13)]
    fitting_records = [audit_pure_axis_fitting(h) for h in range(3, 13)]
    ledger = {
        "theorem": "uniform occurrence-lift/Fitting independence gate",
        "pins": PINS,
        "occurrence_resolution": occurrence_records,
        "moment_torsor": moment_records,
        "carrier_valued_pure_axis_fitting": fitting_records,
        "tensor_product_counterguard": {
            "construction": "Q_(r,h)=L_r tensor C_h",
            "occurrence_factor": (
                "L_r deformation retracts naturally to one common carrier; "
                "all centered classes and zero-induced faces are exact"
            ),
            "clean_factor": (
                "C_h has c0 exact, the full leading coefficientwise lift, "
                "and nonzero exceptional class x_h"
            ),
            "clean_tail_factor": (
                "two independent common-carrier word copies carry u^h and "
                "v^h; centered occurrence directions are exact in each "
                "copy, while the 2h Macaulay shifts have full rank"
            ),
            "homology": (
                "p_r tensor id and i_r tensor id exhibit Q_(r,h) as a "
                "deformation retract of C_h; x_h therefore remains nonzero"
            ),
            "cross_pair_naturality": (
                "every D_e^# and normalized I_e^# acts on L_r and identity "
                "on C_h, so it commutes strictly with q,r, the clean tail, "
                "and the common carrier"
            ),
            "physical_source_constructed": False,
        },
        "verdict": (
            "Even a chain-level centered occurrence lift with exact "
            "restriction/insertion, a common constant carrier, and all "
            "contractible occurrence faces does not force the Fitting "
            "wedge.  The independent based-loop torsor preserves c0 and "
            "every occurrence square while changing the weighted moments "
            "needed to kill x_h.  A positive theorem must additionally "
            "construct a clean-parameter horizontal one-form/zero-residue "
            "map from the occurrence lift to the whole clean family."
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    require(digest == "391378f30f3913be5d2cb8f0af74ef5e91bd851478461138ad44d54318bac4a2",
            ("occurrence/Fitting independence ledger changed", digest))
    return ledger, digest


def main():
    _ledger, digest = audit()
    print("uniform occurrence-lift/Fitting independence gate: PASS")
    print("centered occurrence and every D/I square: exact in L_r")
    print("common H0 and all occurrence faces do not kill higher moment torsor")
    print("Fitting wedge still needs horizontal clean-parameter zero residue")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
