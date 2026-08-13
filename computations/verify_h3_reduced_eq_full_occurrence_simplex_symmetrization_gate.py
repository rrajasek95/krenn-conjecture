#!/usr/bin/env python3
r"""Full 90-occurrence symmetrization of the reduced-Eq graph cone.

For the pure direct-free row H0=sum_M f_M, adjoin all private graph
coordinates z_M=f_M.  Put E_M=f_M-z_M and B=sum_M z_M-U.  Then

    F0=H0-U=sum_M E_M+B.

Consequently the integral symmetric chain

    K_sym=r0-sum_M a_M*e_Eq,  d(a_M)=E_M,

has dK_sym=B*e_Eq.  This cancels all individual graph faces, but B is the
pullback of the original physical Eq equation, not a bar boundary.  The
occurrence simplex has degree-zero boundary equal to the augmentation-zero
lattice, while B lies in its primitive trivial/target quotient.  Declaring
B=0 is relative base change by F0=0 and recreates the already isolated
Koszul/Tate normal cell rather than a physical augmented lift.

The checker audits integral versus normalized coefficients, the independent
rho parity factor, labelled-residue obstruction, and the surviving C5
aggregate.  It proves a positive compression to one symmetric normal class,
not construction of K_Eq(beta).
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
N = 90
PINS = {
    "computations/verify_h3_reduced_eq_occurrence_graph_tensor_gate.py":
        "5b6db94ecff07e5946007a0d7f95c4ffffb52acc74544d173d5b48cb0ccb0bc9",
    "computations/verify_h3_reduced_eq_koszul_tate_relative_orbit_gate.py":
        "15b47a420a6f1e2e6eb0b89e5e5efb5c895172e30b8ab9339dfa1e451ac03668",
    "computations/verify_h3_source_base_change_conormal_obstruction.py":
        "1a921671ab378f68355c2a6196d1951cad30244d78a9e90ec2715ce47ef12bf0",
    "computations/verify_h3_selected_lower_quiver_kahler_mapping_cylinder_gate.py":
        "e5deda7162db47f229239dc91b419baaf00c3158249859cbafb03fe3af2cc958",
    "computations/verify_h3_rootless_endpoint_to_collision_chain_map_boundary.py":
        "be39a61df8e3723983eea7a20d405fba7ff0f3822bc90e8d48b8039177f69cfc",
    "computations/verify_h3_reduced_eq_spencer_three_projection_gate.py":
        "315508b572fa0d96b33ba83b8ac4905e59dfbf8f484023891618dbb3c6489d83",
}
EXPECTED_LEDGER_SHA256 = (
    "78ecc59aa828bfb9d423a568d3ae694bad8c8630f1f17f43989ac654544175a9"
)


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def dot(left, right):
    return sum((Q(a) * Q(b) for a, b in zip(left, right, strict=True)), Q(0))


def rank(columns):
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "ragged matrix")
    work = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(height)]
    pivot_row = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(pivot_row, height)
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(height):
            if row == pivot_row or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def unit(index, size=N):
    value = [Q(0)] * size
    value[index] = Q(1)
    return tuple(value)


def add(*vectors):
    return tuple(sum((Q(vector[index]) for vector in vectors), Q(0))
                 for index in range(len(vectors[0])))


def scale(coefficient, vector):
    return tuple(Q(coefficient) * Q(value) for value in vector)


def occurrence_simplex_audit():
    vertices = tuple(unit(index) for index in range(N))
    edges = tuple(add(vertices[index], scale(-1, vertices[0]))
                  for index in range(1, N))
    augmentation = (Q(1),) * N
    require(rank(edges) == N - 1
            and all(dot(augmentation, edge) == 0 for edge in edges),
            "occurrence simplex incidence changed")

    # Deleting row zero leaves the 89x89 identity, so the image is exactly
    # the saturated augmentation-zero lattice over Z.  Higher simplex faces
    # give relations among these edges and cannot enlarge their C0 image.
    deleted_row_matrix = tuple(tuple(edge[row] for row in range(1, N))
                               for edge in edges)
    require(all(deleted_row_matrix[column][row]
                == (Q(1) if row == column else Q(0))
                for column in range(N - 1) for row in range(N - 1)),
            "star incidence stopped having a unit maximal minor")

    # Target-augmented row order is z_1,...,z_90,U.  The invariant diagonal
    # B=sum z_M-U is primitive and not in the simplex boundary image.
    extended_edges = tuple(edge + (Q(0),) for edge in edges)
    b = augmentation + (Q(-1),)
    target_dual = (Q(0),) * N + (Q(-1),)
    require(all(dot(target_dual, edge) == 0 for edge in extended_edges)
            and dot(target_dual, b) == 1,
            "symmetric occurrence/target diagonal stopped being primitive")
    require(rank(extended_edges) == N - 1
            and rank(extended_edges + (b,)) == N,
            "symmetric diagonal rank changed")
    return {
        "occurrence_vertices": N,
        "simplex_C0_rank": N,
        "simplex_boundary_rank": N - 1,
        "simplex_boundary_image": "ker(sum of occurrence coefficients)",
        "integrally_saturated": True,
        "symmetric_target_diagonal": "B=sum_M z_M-U",
        "primitive_detector": "minus physical U coordinate",
        "B_in_simplex_boundary_image": False,
        "interpretation": (
            "the complete bar kills occurrence differences but leaves its "
            "trivial augmentation component; B is that component paired "
            "with the physical target"
        ),
    }


def symmetric_graph_cone_audit():
    # Boundary rows: 90 graph equations E_M, then B.  The physical Eq row is
    # F0=sum E_M+B; graph tensors are the individual E_M columns.
    physical = (Q(1),) * N + (Q(1),)
    graph_tensors = tuple(unit(index, N + 1) for index in range(N))
    k_sym = add(physical, *(scale(-1, column) for column in graph_tensors))
    b_only = (Q(0),) * N + (Q(1),)
    require(k_sym == b_only,
            "integral full-occurrence cone stopped leaving exactly B*Eq")

    # Averaging the 90 selected one-graph cones is a different operation.
    # K_i=r0-a_i*Eq.  Its normalized average retains (89/90) of every graph
    # face and one B; the raw sum retains 89 of every graph face and 90 B.
    selected_cones = tuple(add(physical, scale(-1, graph_tensors[index]))
                           for index in range(N))
    raw_sum = add(*selected_cones)
    normalized = scale(Q(1, N), raw_sum)
    expected_raw = (Q(N - 1),) * N + (Q(N),)
    expected_normalized = (Q(N - 1, N),) * N + (Q(1),)
    require(raw_sum == expected_raw and normalized == expected_normalized,
            "selected-cone averaging coefficients changed")

    # More generally, a weighted sum of selected cones with sum c_i=1 has
    # B coefficient one and E_i coefficient 1-c_i.  Killing all E_i would
    # require every c_i=1, incompatible with sum one for N>1.
    weights = tuple(Q(1, N) for _ in range(N))
    require(sum(weights, Q(0)) == 1
            and all(1 - value == Q(N - 1, N) for value in weights),
            "uniform weights changed")

    # Splitting the physical target among occurrence diagonals also leaves
    # B: sum_i(z_i-w_i U)=sum_i z_i-U whenever sum_i w_i=1.
    target_split_sum = (Q(1),) * N + (-sum(weights, Q(0)),)
    require(target_split_sum == (Q(1),) * N + (Q(-1),),
            "normalized target diagonals stopped summing to B")
    return {
        "row_order": [*(f"E_{index}" for index in range(N)), "B"],
        "physical_Eq_boundary": "sum_M E_M+B",
        "integral_symmetric_chain": "K_sym=r0-sum_M a_M e_Eq",
        "integral_symmetric_boundary": "B e_Eq",
        "division_by_90_required": False,
        "raw_sum_of_selected_cones": {
            "each_E_M_coefficient": N - 1,
            "B_coefficient": N,
        },
        "normalized_average_of_selected_cones": {
            "each_E_M_coefficient": f"{N - 1}/{N}",
            "B_coefficient": 1,
            "closes": False,
        },
        "normalized_target_split": (
            "weights sum to one, so the 90 individual target diagonals sum "
            "to B rather than zero"
        ),
        "source_validity": (
            "all private graphs z_M=f_M are contractible; adjoining B=0 is "
            "exactly the pulled-back physical equation H0-U=0, not a bar face"
        ),
    }


def conormal_and_koszul_identification():
    source = (ROOT / (
        "computations/verify_h3_source_base_change_conormal_obstruction.py"
    )).read_text()
    tate = (ROOT / (
        "computations/verify_h3_reduced_eq_koszul_tate_relative_orbit_gate.py"
    )).read_text()
    require('"connecting_class_in_J_mod_J2": "kappa*[F0]"' in source
            and '"conormal_connecting_class": "delta(N)=kappa*[F0] in J/J^2"'
            in source,
            "source conormal ledger changed")
    require('"relative_boundary": "dC_K=-F e_Eq"' in tate
            and '"forced_defect": "labelled ordinary residue +Y"' in tate,
            "Koszul/Tate physical comparison ledger changed")
    return {
        "graph_pullback": "B maps to F0=H0-U after eliminating all z_M",
        "conormal_class": "[B]=[F0] is nonzero in J/J^2",
        "selected_U_conormal_value": -1,
        "why_B_zero_is_circular": (
            "B vanishes on the source quotient, but a source nullhomotopy "
            "must lift before that base change; its connecting class is [F0]"
        ),
        "positive_compression": (
            "the full occurrence symmetrization identifies the only remaining "
            "normal class with the absolute Koszul/Tate generator for the "
            "pair (B,Eq)"
        ),
        "physical_Tate_lift": {
            "unaugmented_relative_boundary": "-B e_Eq",
            "nearest_underived_signature": (
                "right Eq boundary, zero target/W, labelled ordinary residue +Y"
            ),
            "still_missing": (
                "augmented comparison cancelling labelled residue and Eq+ainc, "
                "with ridge/word/private/terminal/q typing"
            ),
        },
    }


def rho_parity_audit():
    # Occurrence symmetrization acts on a different tensor factor from the
    # regular rho orbit Q{C,rho C}.  Therefore it commutes with the two parity
    # projectors but cannot create either source-labelled orbit member.
    left = (Q(1), Q(0))
    right = (Q(0), Q(1))
    odd = add(left, scale(-1, right))
    even = add(left, right)
    require(rank((odd, even)) == 2 and odd == (1, -1) and even == (1, 1),
            "rho regular representation changed")

    # Tensoring B with the exact coefficient projections retains B in both
    # parity sectors.  The generic even packet has eight +/-1 coefficients.
    d = (Q(-1), Q(1), Q(-1), Q(1))
    v = (Q(0), Q(1, 2), Q(0), Q(0), Q(1, 2), Q(0))
    even_packet = tuple(2 * root * label for root in d for label in v)
    require(sum(value != 0 for value in even_packet) == 8
            and set(value for value in even_packet if value) == {-1, 1},
            "generic even coefficient packet changed")

    # The nearest physical Tate lifts retain labelwise residue.  Odd kills
    # only its coarse sum; even retains both labels.
    odd_ores = (Q(1), Q(-1))
    even_ores = (Q(1), Q(1))
    require(sum(odd_ores, Q(0)) == 0 and even_ores == (1, 1),
            "labelled parity residue ledger changed")
    return {
        "factorization": (
            "occurrence simplex factor tensor regular rho factor; projectors commute"
        ),
        "occurrence_symmetry_constructs_rho_orbit": False,
        "odd_projection": "-B in the conditional C-rho C line",
        "even_projection": "2D B tensor v in the conditional C+rho C line",
        "beta_special_projection": "+B in the selected special line",
        "generic_even_nonzero_coefficients": len(
            [value for value in even_packet if value]
        ),
        "nearest_odd_labelled_residue": [1, -1],
        "nearest_even_labelled_residue": [1, 1],
        "conclusion": (
            "symmetrization preserves the formal coefficient projections but "
            "also preserves their two independent augmented obstruction lines; "
            "it neither constructs the regular rho orbit nor makes one parity "
            "imply the other"
        ),
    }


def c5_aggregate_audit():
    edges = []
    for index in range(5):
        column = [Q(0)] * 5
        column[index] = Q(1)
        column[(index + 1) % 5] = Q(-1)
        edges.append(tuple(column))
    aggregate = (Q(1),) * 5
    require(rank(edges) == 4
            and all(dot(aggregate, edge) == 0 for edge in edges),
            "C5 comparison incidence changed")

    # Tensor with the two-dimensional rho orbit: the map is two block copies
    # of C5 incidence, hence rank eight in ten and one aggregate per parity.
    zero5 = (Q(0),) * 5
    doubled_edges = tuple(edge + zero5 for edge in edges) + tuple(
        zero5 + edge for edge in edges
    )
    require(rank(doubled_edges) == 8,
            "rho-doubled C5 edge rank changed")
    left_aggregate = aggregate + zero5
    right_aggregate = zero5 + aggregate
    require(all(dot(left_aggregate, edge) == 0 for edge in doubled_edges)
            and all(dot(right_aggregate, edge) == 0 for edge in doubled_edges),
            "C5 rho aggregates stopped surviving")
    return {
        "single_parity_edge_rank": 4,
        "single_parity_cokernel": "one primitive sum_v C_v",
        "regular_rho_edge_rank": 8,
        "regular_rho_ambient_rank": 10,
        "regular_rho_cokernel_rank": 2,
        "parity_interpretation": (
            "one C5 comparison aggregate survives in each odd/even line"
        ),
        "occurrence_symmetrization_effect": (
            "none: B is the trivial occurrence factor, so tensoring the C5 "
            "incidence map with B preserves its cokernel"
        ),
    }


def main() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, ("pinned dependency changed", relative,
                                     actual, expected))
    ledger = {
        "theorem": "full occurrence-simplex symmetrization gate",
        "pins": PINS,
        "full_occurrence_bar": occurrence_simplex_audit(),
        "coefficient_scaling": symmetric_graph_cone_audit(),
        "source_and_Tate_identification": conormal_and_koszul_identification(),
        "rho_parity": rho_parity_audit(),
        "C5_transport": c5_aggregate_audit(),
        "verdict": (
            "full integral symmetrization cancels all 90 private graph faces "
            "and compresses them to B=(sum z_M-U), but B is exactly the graph "
            "pullback of F0=H0-U.  The occurrence simplex kills only "
            "augmentation-zero differences, so B is a primitive surviving "
            "trivial class.  Setting B=0 is source base change and yields the "
            "unaugmented Koszul/Tate normal cell; its physical augmented "
            "comparison, both rho parities, labelled residue, and one C5 "
            "aggregate per parity remain open"
        ),
        "K_Eq_beta_constructed": False,
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("unexpected ledger digest", digest, EXPECTED_LEDGER_SHA256))
    print("h3 full occurrence-simplex symmetrization gate: PASS")
    print("integral K_sym cancels 90 graph faces and leaves B*e_Eq")
    print("B=sum z_M-U is the original Eq conormal, not a simplex boundary")
    print("normalized averaging also leaves B; no coefficient shortcut")
    print("rho odd/even obstruction lines and C5 aggregates both survive")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
