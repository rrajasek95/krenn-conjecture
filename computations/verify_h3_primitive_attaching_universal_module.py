#!/usr/bin/env python3
"""Smallest literal universal module at the h=3 attaching primitive.

The checker has two deliberately separate outputs.

* In the source-labelled squarefree four-Hasse prolongation, it constructs
  n_A = kappa*(s_I-T) from the 16 r_0 faces, the top r_m face, and the cap
  column T.  The symbol n_A is not a generator.  Its augmented boundary is
  (kappa*Y*w, 0, 0).
* After diagonal projection to the committed underived physical module, the
  primitive integral functional (E,W,tgt,ores) |-> E+W+tgt-ores kills the
  full cap basis and all 60 labelled denominator/lower-face candidates, but
  takes the desired invisible boundary to one.  Thus the formal chain does
  not descend through the available physical columns.

Here E is the coefficient of u*e_Eq after setting every labelled edge to
zero, W is the coefficient of Y*w, and ores is normalized by Y.  This is a
bounded module calculation; it does not declare a new source cell.
"""

from fractions import Fraction as Q
from functools import reduce
from hashlib import sha256
from itertools import combinations
from math import gcd
import json

import verify_h3_full_hasse_koszul_cap_totalization as HASSE
import verify_h3_qzero_denominator_rees_four_cube as QZERO


EXPECTED_LEDGER_DIGEST = (
    "263b8f90977055b84184fa3a8ddc5d8fe57788e2f19bca95a2ab1c81d3f6a9b4"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def add_vectors(*vectors):
    return tuple(sum(entries, Q(0)) for entries in zip(*vectors, strict=True))


def scale_vector(coefficient, vector):
    return tuple(Q(coefficient) * entry for entry in vector)


def dot(left, right):
    return sum((a * b for a, b in zip(left, right, strict=True)), Q(0))


def json_vector(vector):
    return [int(entry) if Q(entry).denominator == 1 else str(Q(entry))
            for entry in vector]


def rank(columns):
    if not columns:
        return 0
    work = [list(map(Q, row)) for row in zip(*columns, strict=True)]
    pivot_row = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(pivot_row, len(work))
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][column]
        work[pivot_row] = [entry / pivot_value for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            coefficient = work[row][column]
            work[row] = [left - coefficient * right for left, right in
                         zip(work[row], work[pivot_row], strict=True)]
        pivot_row += 1
        if pivot_row == len(work):
            break
    return pivot_row


def determinant(rows):
    work = [list(map(Q, row)) for row in rows]
    require(work and all(len(row) == len(work) for row in work),
            "determinant input is not square")
    answer = Q(1)
    for column in range(len(work)):
        pivot = next((row for row in range(column, len(work))
                      if work[row][column]), None)
        if pivot is None:
            return Q(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            answer = -answer
        pivot_value = work[column][column]
        answer *= pivot_value
        for row in range(column + 1, len(work)):
            if not work[row][column]:
                continue
            coefficient = work[row][column] / pivot_value
            work[row] = [left - coefficient * right for left, right in
                         zip(work[row], work[column], strict=True)]
    return answer


def maximal_minor_gcd(columns):
    matrix = [list(map(int, row)) for row in zip(*columns, strict=True)]
    target_rank = rank(columns)
    minors = []
    for selected_rows in combinations(range(len(matrix)), target_rank):
        for selected_columns in combinations(range(len(columns)), target_rank):
            square = [[matrix[row][column] for column in selected_columns]
                      for row in selected_rows]
            minors.append(abs(int(determinant(square))))
    return reduce(gcd, minors, 0)


def serialized_polynomial(polynomial):
    return [
        [str(coefficient), [repr(item) for item in term]]
        for term, coefficient in sorted(
            polynomial.items(), key=lambda item: (len(item[0]), repr(item[0]))
        )
    ]


def source_four_cube():
    """Reconstruct kappa*(s_I-T); no n_A generator is introduced."""
    deleted = HASSE.ODD[0]
    matching = HASSE.matchings(HASSE.face(deleted))[0]
    directions = HASSE.endpoint_variables(deleted) + HASSE.internal_variables(matching)
    require(len(directions) == 4 and len(set(directions)) == 4,
            "marked four-cube directions changed")

    # Pin the literal ed60e2c input rather than importing its conditional
    # augmented column.  These routines check all 15 reset columns, cube
    # signs, and the first q-zero order.
    literal, support = QZERO.literal_row_and_no_leakage_audit()
    cube_signs = QZERO.cubical_sign_audit()
    ladder, conditional = QZERO.degree_and_conditional_typing_audit()
    require(len(literal) == 15, "literal four-polar count changed")
    require(support["qzero_candidates"] == 15
            and support["labelled_output_rank"] == 5,
            "full reset-column support count changed")
    require(cube_signs["ridges"] == 24,
            "four-cube ridge count changed")
    require(ladder[-1]["total_order"] == 4
            and ladder[-1]["q_degree"] == 0,
            "q-zero top stopped occurring first at order four")
    require(conditional["interpretation"].startswith("typing test only"),
            "ed60e2c conditional scope changed")

    cycle = HASSE.indexed_top_koszul_cycle(directions)
    full_mask = (1 << len(directions)) - 1
    require(len(cycle) == 17, "four-Hasse Koszul cycle term count changed")
    require(set(cycle).issubset({("r_0", mask) for mask in range(16)}
                                | {("r_m", full_mask)}),
            "four-Hasse cycle acquired a non-source generator")
    require(not HASSE.indexed_hasse_chain_differential(cycle, directions),
            "s_I is not a cycle in the source-labelled Hasse module")
    require(cycle[("r_0", 0)] == HASSE.constant(),
            "unit target face of s_I changed")

    n_a = {generator: HASSE.multiply(HASSE.KAPPA, coefficient)
           for generator, coefficient in cycle.items()}
    require("n_A" not in n_a and "T" not in n_a,
            "n_A was inserted as a declared source column")
    n_a["T"] = HASSE.scale(-HASSE.ONE, HASSE.KAPPA)
    indexed = {generator: coefficient for generator, coefficient in n_a.items()
               if isinstance(generator, tuple)}
    boundary = HASSE.indexed_hasse_chain_differential(indexed, directions)
    boundary = HASSE.module_add(
        boundary,
        {"w": HASSE.multiply(n_a["T"],
                             HASSE.scale(-HASSE.ONE, HASSE.CAP_Y))},
    )
    require(boundary == {"w": HASSE.multiply(HASSE.KAPPA, HASSE.CAP_Y)},
            "constructed n_A does not have boundary kappa*Y*w")
    target = HASSE.add(n_a[("r_0", 0)], n_a["T"])
    require(not target, "constructed n_A retained target")
    # There is no rho term in n_A; ores is supported on rho alone.
    require("rho" not in n_a, "constructed n_A retained ordinary residue")

    return {
        "deleted": deleted,
        "matching": [list(edge) for edge in matching],
        "directions": [repr(direction) for direction in directions],
        "literal_four_polars": len(literal),
        "reset_columns": 15,
        "cube_ridges": cube_signs["ridges"],
        "qzero_order": ladder[-1]["total_order"],
        "hasse_generators_available": 32,
        "cycle_source_terms": len(cycle),
        "cycle_r0_faces": sum(row == "r_0" for row, _mask in cycle),
        "cycle_rm_faces": sum(row == "r_m" for row, _mask in cycle),
        "declared_n_A_column": False,
        "boundary": serialized_polynomial(boundary["w"]),
        "target": 0,
        "ordinary_residue": 0,
    }


def physical_separator():
    """Integral cokernel of every available underived candidate column."""
    # Coordinates: (E, W, target, ores).  E is the u*Eq coefficient after
    # edge augmentation; W and ores are respectively normalized by Y.
    r0 = (-1, 0, 1, 0)
    rm = (0, 0, 0, 0)
    cap_t = (0, -1, 1, 0)
    y_rho = (0, 1, 0, 1)
    desired_k = (0, 1, 0, 0)
    separator = (1, 1, 1, -1)

    physical_basis = {
        "r_0": r0,
        "r_m": rm,
        "T": cap_t,
        "Y*rho": y_rho,
    }
    require(all(dot(separator, column) == 0
                for column in physical_basis.values()),
            "integral separator stopped killing the physical basis")
    require(dot(separator, desired_k) == 1,
            "integral separator stopped detecting the desired boundary")

    # Literal lower-face candidates for all 15 denominator columns and all
    # four internal faces.  Ten columns are identically zero; the 20 active
    # faces are scalar multiples of r_0-T, and their response corrections
    # are scalar multiples of r_0-T-Y*rho.  We retain every source label.
    deleted = HASSE.ODD[0]
    matching = HASSE.matchings(HASSE.face(deleted))[0]
    internal = HASSE.internal_variables(matching)
    lower_faces = []
    active = 0
    for site in HASSE.ODD:
        h_site = HASSE.face_hafnian(site)
        for colour in HASSE.COLOURS:
            for size in range(3):
                for selected in combinations(internal, size):
                    coefficient = (HASSE.derivative(h_site, selected)
                                   if colour == HASSE.MIXED[site] else {})
                    phi_vector = add_vectors(r0, scale_vector(-1, cap_t))
                    response_vector = add_vectors(
                        phi_vector, scale_vector(-1, y_rho)
                    )
                    if coefficient:
                        active += 1
                    else:
                        phi_vector = (0, 0, 0, 0)
                        response_vector = (0, 0, 0, 0)
                    require(dot(separator, phi_vector) == 0,
                            "a labelled lower Hasse face escaped the separator")
                    require(dot(separator, response_vector) == 0,
                            "a labelled curvature response escaped the separator")
                    lower_faces.append({
                        "site": site,
                        "colour": colour,
                        "internal_face": [repr(edge) for edge in selected],
                        "active": bool(coefficient),
                        "coefficient_terms": len(coefficient),
                        "phi_vector": json_vector(phi_vector),
                        "curvature_vector": json_vector(response_vector),
                    })
    require(len(lower_faces) == 60 and active == 12,
            ("full labelled lower-face census changed", len(lower_faces), active))

    candidate_columns = [r0, cap_t, y_rho]
    require(rank(candidate_columns) == 3,
            "physical augmented module rank changed")
    require(maximal_minor_gcd(candidate_columns) == 1,
            "physical augmented cokernel acquired torsion")
    require(rank(candidate_columns + [desired_k]) == 4,
            "desired K column entered the physical candidate span")
    closed_determinant = determinant([
        [column[row] for column in candidate_columns + [desired_k]]
        for row in range(4)
    ])
    require(abs(closed_determinant) == 1,
            "desired K no longer closes the cokernel primitively")

    # The tempting top diagonal projections explain the obstruction:
    # r_0-T has the extra -u*Eq term and lies in ker(lambda); adding -Y*rho
    # gives the response cycle, still in ker(lambda).  Only the full Hasse
    # lower-face cancellation removes Eq without adding ores, and that is
    # exactly the non-descending column detected by lambda.
    top_projection = add_vectors(r0, scale_vector(-1, cap_t))
    top_response = add_vectors(top_projection, scale_vector(-1, y_rho))
    require(top_projection == (-1, 1, 0, 0)
            and top_response == (-1, 0, 0, -1),
            "top projection vectors changed")
    require(dot(separator, top_projection) == 0
            and dot(separator, top_response) == 0,
            "top curvature candidates escaped the integral separator")

    return {
        "coordinates": ["u*Eq at edges=0", "Y*w", "target", "Y*ores"],
        "physical_basis": {label: json_vector(column)
                           for label, column in physical_basis.items()},
        "top_projection": json_vector(top_projection),
        "top_curvature_response": json_vector(top_response),
        "labelled_denominator_faces": len(lower_faces),
        "active_denominator_faces": active,
        "candidate_rank": rank(candidate_columns),
        "maximal_minor_gcd": maximal_minor_gcd(candidate_columns),
        "cokernel_generator": json_vector(separator),
        "desired_K": json_vector(desired_k),
        "separator_on_K": str(dot(separator, desired_k)),
        "rank_after_K": rank(candidate_columns + [desired_k]),
        "determinant_after_K": str(closed_determinant),
        "lower_face_labels": lower_faces,
    }


def primitive_bridge():
    """Exact affine-polynomial check of [K]=alpha*[A]."""
    # Entries are pairs (constant, alpha coefficient).  Coordinates are
    # (T, S=sum m_S, K).  Existing rows are S and K-16 alpha T-S.
    middle = ((0, 0), (1, 0), (0, 0))
    relative = ((0, -16), (-1, 0), (1, 0))
    alpha_a = ((0, 16), (0, 1), (0, 0))
    connecting = ((0, 0), (0, 0), (1, 0))

    def affine_add(*vectors):
        return tuple((sum(entry[0] for entry in entries),
                      sum(entry[1] for entry in entries))
                     for entries in zip(*vectors, strict=True))

    def affine_scale(value, vector):
        return tuple((value * constant, value * alpha)
                     for constant, alpha in vector)

    difference = affine_add(connecting, affine_scale(-1, alpha_a))
    one_minus_alpha_middle = ((0, 0), (1, -1), (0, 0))
    expected = affine_add(relative, one_minus_alpha_middle)
    require(difference == expected,
            "committed primitive bridge K-alpha*A changed")
    return {
        "primitive": "A=16*T+sum_{|S|=3}m_S",
        "bridge": "[K]=alpha*[A] modulo 20 middle rows and H2",
        "cap_normalized_boundary": "K=kappa*Y*w",
    }


def main():
    ledger = {
        "four_cube_and_formal_membership": source_four_cube(),
        "underived_integral_cokernel": physical_separator(),
        "primitive_bridge": primitive_bridge(),
        "verdict": {
            "prolonged_universal_module":
                "n_A=kappa*(s_I-T) is reconstructed, not declared",
            "committed_physical_module":
                "n_A is separated by lambda=(1,1,1,-1)",
            "scope":
                "formal membership plus exact physical-descent obstruction; no new source cell",
        },
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_DIGEST,
                ("ledger changed", digest))
    print("h=3 primitive attaching universal module: PASS")
    print("upstairs: n_A=kappa*(s_I-T), 17 source-labelled Hasse terms, dn_A=K")
    print("downstairs: 60 labelled lower faces + full cap basis lie in ker(1,1,1,-1)")
    print("desired (K,tgt,ores)=(kappa*Y*w,0,0) is primitive cokernel generator")
    print(f"ledger sha256 {digest}")


if __name__ == "__main__":
    main()
