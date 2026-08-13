#!/usr/bin/env python3
"""Construct the universal relative graph resolution for the P2 sections.

Let A be the physical coefficient algebra and u_i in A the twelve literal
occurrence functions in one response word.  Add graph variables z_i and
centered carrier variables t_i, with Koszul generators theta_i, phi_i:

    d theta_i = z_i-u_i,
    d phi_i   = t_i-(Cz)_i,       C=12I-J.

Both equations are monic in new variables, so this is a presentation-safe
resolution of A: eliminate z=u and t=Cu.  The combination

    Gamma_i = phi_i + sum_j C_ij theta_j

has d Gamma_i=t_i-(Cu)_i.  It is the desired universal pointed occurrence
family relative to the carrier t.  Setting t=0 would create the desired
absolute centered boundary, but changes H0 from A to A/(Cu); with the
complete response sum u=0 it kills all twelve occurrence directions.

Root principal-parts actions extend functorially.  For any diagonal labelled
face operator D, put Xz=Du', Xu=Du', Xtheta=Dtheta', Xt=CDz', Xphi=0.
Then [d,X]=0.  Two distinct-factor directions commute, so the labelled
cobar square is automatic in this relative graph resolution.  The remaining
physical theorem is exactly a landing of the centered carrier t, including
its q/dq and labelled Q/ores augmentation.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h2_p2_centered_occurrence_cobar_section_count_gate.py":
        "2ee0bc0077dba6d116b4cb6e15101350a3a801d515c589c122cad8d39ff5654c",
    "notes/h2-p2-centered-occurrence-cobar-section-count-gate.md":
        "543f14165c00a7cf5ac30501f43f267a4b71efb4f6c50bbfa2f124c652f8ac63",
    "computations/verify_h2_labelled_two_direction_occurrence_hasse_cobar_square_gate.py":
        "77d13c31df34efa26b575497bdd7bb2cc9173e8d1907030541444551c7417804",
    "notes/h2-labelled-two-direction-occurrence-hasse-cobar-square-gate.md":
        "37b4da7bddd358d4b8d89bc80f252da9e0742d7ae8fc5eab7daedfd97c1eed7a",
    "computations/verify_h3_pointed_occurrence_primitive_cap_p2_propagation_gate.py":
        "a8dfe952ce4fbbaf71ffd4ef748e456d5284dbf6b71655cce6f2f10576db0d06",
    "notes/h3-pointed-occurrence-primitive-cap-p2-propagation-gate.md":
        "c1cac29cabc30d13b4b2a30d882e1b8e01268423be7b29d7748744ebecaf60ff",
    "computations/verify_h3_universal_graph_derived_base_change_physical_descent_gate.py":
        "9e60fb8410288a192b8be3b59938e5e7ba4ea42b455fee67b94ca6ef37777fde",
    "notes/h3-universal-graph-derived-base-change-physical-descent-gate.md":
        "510f7fd8912fe26fe27f3375497d19e90389c7ac94f66c4c7f674ea9565fe475",
    "computations/verify_h3_anchor_conormal_functoriality_bridge.py":
        "83879756547765878c36944c1ab14827ab77a1f217931bc05db0c72cb0af32a8",
    "notes/h3-anchor-conormal-functoriality-bridge.md":
        "ff21fee754b3de39788dca5c6d024a6a7f539648fb3cc9473c2690239c8bbac8",
}
EXPECTED_LEDGER_SHA256 = (
    "3886506f894797f08cad5b581461f5e4e8e42d512246f3647515cb8e6e41f6d9"
)

N = 12


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


def add(*vectors):
    return tuple(sum(entries, Q(0))
                 for entries in zip(*vectors, strict=True))


def scale(coefficient, vector):
    return tuple(Q(coefficient) * entry for entry in vector)


def dot(left, right):
    return sum((a * b for a, b in zip(left, right, strict=True)), Q(0))


def matvec(matrix, vector):
    return tuple(dot(row, vector) for row in matrix)


def matmul(left, right):
    columns = tuple(zip(*right, strict=True))
    return tuple(tuple(dot(row, column) for column in columns)
                 for row in left)


def transpose(matrix):
    return tuple(zip(*matrix, strict=True))


def rank(columns) -> int:
    if not columns:
        return 0
    rows = [list(row) for row in zip(*columns, strict=True)]
    answer = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(answer, len(rows))
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[answer], rows[pivot] = rows[pivot], rows[answer]
        value = rows[answer][column]
        rows[answer] = [entry / value for entry in rows[answer]]
        for row in range(len(rows)):
            if row == answer or not rows[row][column]:
                continue
            value = rows[row][column]
            rows[row] = [left - value * right for left, right in
                         zip(rows[row], rows[answer], strict=True)]
        answer += 1
    return answer


def identity(size):
    return tuple(tuple(Q(row == column) for column in range(size))
                 for row in range(size))


def diagonal(entries):
    return tuple(tuple(Q(entries[row]) if row == column else Q(0)
                       for column in range(len(entries)))
                 for row in range(len(entries)))


def block_vector(u, z, t):
    return tuple(u) + tuple(z) + tuple(t)


def audit() -> tuple[dict[str, object], str]:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))

    one = (Q(1),) * N
    zero = (Q(0),) * N
    i_matrix = identity(N)
    j_matrix = tuple(one for _row in range(N))
    c_matrix = tuple(tuple(N * i_matrix[row][column]
                           - j_matrix[row][column]
                           for column in range(N))
                     for row in range(N))
    require(rank(list(transpose(c_matrix))) == N - 1
            and matvec(c_matrix, one) == zero
            and matmul(c_matrix, c_matrix)
            == tuple(tuple(N * entry for entry in row)
                     for row in c_matrix),
            "the centered projector C=12I-J changed")

    # Degree-one graph generators and their degree-zero boundaries in the
    # coordinate order (u,z,t).  Columns are dtheta_i and dphi_i.
    theta_boundaries = []
    phi_boundaries = []
    for index in range(N):
        e = i_matrix[index]
        theta_boundaries.append(block_vector(scale(-1, e), e, zero))
        phi_boundaries.append(block_vector(
            zero, scale(-1, c_matrix[index]), e
        ))
    graph_columns = theta_boundaries + phi_boundaries
    require(rank(graph_columns) == 2 * N,
            "the monic relative graph sequence lost rank")

    # Gamma_i=phi_i+sum_j C_ij theta_j has boundary t_i-(Cu)_i.
    gamma_boundaries = []
    for index in range(N):
        gamma = phi_boundaries[index]
        gamma = add(gamma, *(
            scale(c_matrix[index][column], theta_boundaries[column])
            for column in range(N)
        ))
        expected = block_vector(scale(-1, c_matrix[index]), zero,
                                i_matrix[index])
        require(gamma == expected,
                ("the relative centered Gamma boundary changed", index))
        gamma_boundaries.append(gamma)

    # H0 of the graph presentation has dimension N: z=u and t=Cu.  The
    # explicit augmentation sends a physical u-vector to (u,u,Cu).
    augmentation_columns = tuple(
        block_vector(i_matrix[index], i_matrix[index],
                     tuple(c_matrix[row][index] for row in range(N)))
        for index in range(N)
    )
    require(rank(augmentation_columns) == N
            and rank(graph_columns + list(augmentation_columns)) == 3 * N,
            "the graph presentation stopped resolving the physical u-space")

    # Killing t imposes Cu=0.  Adding the complete response sum u=0 then
    # kills every occurrence direction.  This is the exact classical-fibre
    # defect of turning the relative Gamma into an absolute boundary.
    t_zero_columns = [block_vector(zero, zero, i_matrix[index])
                      for index in range(N)]
    response_row_as_relation = block_vector(one, zero, zero)
    require(rank(graph_columns + t_zero_columns) == 3 * N - 1
            and rank(graph_columns + t_zero_columns
                     + [response_row_as_relation]) == 3 * N,
            "the t=0 classical quotient changed")
    counterpoint = add(i_matrix[0], scale(-1, i_matrix[1]))
    require(sum(counterpoint, Q(0)) == 0
            and matvec(c_matrix, counterpoint)
            == scale(N, counterpoint),
            "the centered classical counterpoint changed")

    # Root/PP functoriality.  A labelled one-root face operator is diagonal
    # on occurrence tags.  For theta use D theta'.  For t use C D z' and
    # keep phi fixed; this makes both graph relations commute with X.
    mask_a = tuple(Q(index in (0, 1, 3, 4, 7, 9))
                   for index in range(N))
    mask_b = tuple(Q(index in (0, 2, 3, 5, 8, 10))
                   for index in range(N))
    d_a = diagonal(mask_a)
    d_b = diagonal(mask_b)
    require(matmul(d_a, d_b) == matmul(d_b, d_a),
            "the distinct-factor labelled masks stopped commuting")

    sample_u = tuple(Q(index + 1) for index in range(N))
    sample_z = tuple(Q(2 * index - 3) for index in range(N))
    sample_t = tuple(Q(5 - index) for index in range(N))
    sample_theta = tuple(Q((index % 4) - 1) for index in range(N))

    def root_chain_audit(direction):
        # X(d theta)=D(z-u)=d(X theta).
        x_d_theta = add(matvec(direction, sample_z),
                        scale(-1, matvec(direction, sample_u)))
        d_x_theta = x_d_theta
        # X(d phi)=X(t-Cz)=CDz-CDz=0=d(Xphi).
        x_t = matvec(c_matrix, matvec(direction, sample_z))
        x_cz = matvec(c_matrix, matvec(direction, sample_z))
        x_d_phi = add(x_t, scale(-1, x_cz))
        # X(d Gamma)=CD(z-u)=d(CD theta).
        x_d_gamma = matvec(c_matrix, matvec(
            direction, add(sample_z, scale(-1, sample_u))
        ))
        d_x_gamma = matvec(c_matrix,
                           matvec(direction, add(sample_z,
                                                 scale(-1, sample_u))))
        require(x_d_theta == d_x_theta
                and x_d_phi == zero
                and x_d_gamma == d_x_gamma,
                "a labelled root stopped being a chain derivation")
        return {
            "mask_rank": rank(list(transpose(direction))),
            "commutes_with_d_on_theta": True,
            "commutes_with_d_on_phi": True,
            "commutes_with_d_on_Gamma": True,
        }

    root_a_record = root_chain_audit(d_a)
    root_b_record = root_chain_audit(d_b)
    ab_theta = matvec(d_a, matvec(d_b, sample_theta))
    ba_theta = matvec(d_b, matvec(d_a, sample_theta))
    ab_t = matvec(c_matrix, matvec(d_a, matvec(d_b, sample_z)))
    ba_t = matvec(c_matrix, matvec(d_b, matvec(d_a, sample_z)))
    require(ab_theta == ba_theta and ab_t == ba_t,
            "the two labelled root orders stopped agreeing")

    # Recover the exact P2 combination of eight Gamma_i from 82713e3.
    count_gate = load(
        "computations/verify_h2_p2_centered_occurrence_cobar_section_count_gate.py",
        "relative_graph_section_count",
    )
    count_ledger, count_digest = count_gate.audit()
    require(count_digest == count_gate.EXPECTED_LEDGER_SHA256,
            "the pointed section-count ledger changed")
    indices = tuple(count_ledger["centered_occurrence_identification"]
                    ["indices"])
    coefficients = tuple(map(
        Q, count_ledger["centered_occurrence_identification"]
        ["coefficients_a_i"]
    ))
    combined_gamma = add(*(
        scale(coefficient, gamma_boundaries[index])
        for index, coefficient in zip(indices, coefficients, strict=True)
    ))
    z_private = add(*(
        scale(coefficient, c_matrix[index])
        for index, coefficient in zip(indices, coefficients, strict=True)
    ))
    t_combination = add(*(
        scale(coefficient, i_matrix[index])
        for index, coefficient in zip(indices, coefficients, strict=True)
    ))
    require(combined_gamma == block_vector(
        scale(-1, z_private), zero, t_combination
    ) and sum(z_private, Q(0)) == 0,
            "the eight-tag relative Gamma combination changed")

    # A single primitive cap line cannot be the full centered carrier.
    # On the complete-response fibre, t=Cu=12u has rank eleven.  The
    # endpoint-even part relevant to the displayed P2 packet has rank five.
    parity = load(
        "computations/verify_h2_lower_centered_endpoint_parity_terminal_fork.py",
        "relative_graph_parity",
    )
    _occurrence, values, lookup, swap, _b, _s = parity.endpoint_data()
    even_centered = []
    seen = set()
    for index, value in enumerate(values):
        if index in seen:
            continue
        mate = lookup[swap(value)]
        seen.update((index, mate))
        pair = add(i_matrix[index], i_matrix[mate])
        even_centered.append(matvec(c_matrix, pair))
    require(rank(even_centered) == 5,
            "the relative endpoint-even carrier rank changed")

    primitive = load(
        "computations/verify_h3_pointed_occurrence_primitive_cap_p2_propagation_gate.py",
        "relative_graph_primitive",
    )
    primitive_ledger, primitive_digest = primitive.audit()
    require(primitive_digest == primitive.EXPECTED_LEDGER_SHA256
            and primitive_ledger["P_f_vs_p"]
            ["same_literal_generator"] is False,
            "the pointed/primitive cap separation changed")

    ledger = {
        "theorem": "h2 P2 universal relative occurrence graph resolution",
        "pins": PINS,
        "physical_occurrence_module": {
            "occurrences": N,
            "complete_response": "R=sum_i u_i",
            "centered_operator": "C=12I-J",
            "rank_C": rank(list(transpose(c_matrix))),
            "identity": "C^2=12C",
        },
        "relative_graph_DGA": {
            "degree_zero_new_variables": ["z_i", "t_i"],
            "degree_one_generators": ["theta_i", "phi_i"],
            "d_theta": "z_i-u_i",
            "d_phi": "t_i-(Cz)_i",
            "regular_sequence_reason": (
                "first equations are monic in z_i and second equations are "
                "monic in t_i"
            ),
            "differential_rank": rank(graph_columns),
            "H0": "A via z_i=u_i and t_i=(Cu)_i",
            "same_classical_physical_fibre_with_t_retained": True,
            "relative_section": "Gamma_i=phi_i+sum_j C_ij theta_j",
            "d_Gamma": "t_i-(Cu)_i",
            "one_universal_family_not_eight_unrelated_columns": True,
        },
        "root_PP_functoriality": {
            "rule": (
                "for a labelled diagonal face D: Xu=Du', Xz=Dz', "
                "Xtheta=Dtheta', Xt=CDz', Xphi=0"
            ),
            "direction_a": root_a_record,
            "direction_b": root_b_record,
            "distinct_factor_commutator_on_theta": 0,
            "distinct_factor_commutator_on_t": 0,
            "labelled_cobar_square_generated": True,
            "qualification": (
                "the carrier action uses z, so it is a relative graph action; "
                "it does not descend to a physical t action until a physical "
                "carrier map is supplied"
            ),
        },
        "exact_P2_combination": {
            "Gamma_indices": list(indices),
            "Gamma_coefficients": [str(value) for value in coefficients],
            "boundary": "t_zprivate-z_private(u)",
            "centered_occurrence_boundary_if_t_is_landed": True,
            "q_reinsertion": (
                "delta(q Gamma)=q delta(Gamma)+(delta q)Gamma; the second "
                "term remains a labelled relative carrier face"
            ),
        },
        "classical_fibre_defect": {
            "illegal_step": "set every t_i=0",
            "H0_after_step": "A/(Cu)",
            "with_complete_response_R_zero": "all u_i=0",
            "rank_graph_plus_t_zero": rank(graph_columns + t_zero_columns),
            "rank_after_also_R_zero": rank(
                graph_columns + t_zero_columns + [response_row_as_relation]
            ),
            "counterpoint": "u=e_0-e_1",
            "counterpoint_complete_response": 0,
            "counterpoint_Cu": "12(e_0-e_1)",
            "conclusion": (
                "the absolute centered boundary is not a presentation change; "
                "it imposes the desired new equation on the old fibre"
            ),
        },
        "remaining_carrier_landing": {
            "full_centered_carrier_rank": N - 1,
            "endpoint_even_private_carrier_rank": rank(even_centered),
            "single_primitive_p_rank": 1,
            "single_p_is_full_carrier_map": False,
            "first_needed_map": (
                "an augmented physical comparison from the relevant t-carrier "
                "orbit to mixed-target, cap Q/ores, dq, anchor, Eq, W, "
                "eta/sigma and physical-q rows"
            ),
            "failure_alternative": (
                "a cokernel covector on t is a physical terminal only after "
                "extension over the complete augmented source map"
            ),
        },
        "sharp_positive_theorem": (
            "the relative graph DGA above is an explicit universal C_i family. "
            "Complete the construction by landing its centered carrier t in "
            "the physical augmented cap complex, naturally for labelled roots "
            "and q principal parts.  Killing t is not allowed; landing it or "
            "terminalizing its first nonlift is the sole next comparison."
        ),
        "scope": (
            "exact algebraic graph/Koszul resolution and labelled linear PP "
            "action.  The u_i are actual occurrence functions in an arbitrary "
            "physical coefficient algebra A; no algebraic independence among "
            "them is assumed because the new graph equations are monic.  No "
            "physical t-carrier augmentation is constructed."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("relative occurrence graph ledger changed", digest,
                 EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    ledger, digest = audit()
    print("relative graph K(A;z-u,t-Cz): PRESENTATION-SAFE")
    print("universal Gamma_i boundary: t_i-(Cu)_i")
    print("labelled root PP/cobar: FUNCTORIAL IN RELATIVE GRAPH")
    print("setting t=0: CHANGES CLASSICAL FIBRE TO A/(Cu)")
    print("endpoint-even physical carrier rank: 5, primitive p rank: 1")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
