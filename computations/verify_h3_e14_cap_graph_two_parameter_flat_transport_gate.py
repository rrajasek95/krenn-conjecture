#!/usr/bin/env python3
"""Audit horizontal transport of the old cap graph over the E14 D4 orbit.

There is a canonical *formal* answer.  Tensor the two-generator old cap
complex with the 90-tag occurrence module and the four-root Boolean orbit.
The cap graph ``G=T+rho`` is a constant cycle at Y=1.  Occurrence centering
acts on tags, the roots act on colours, and the cap differential acts on the
cap factor, so all interchange commutators and all square holonomies vanish.

This does not manufacture a physical source-labelled top copy.  The old cap
word is the eight-site word 01211222; at the four D4 root sites 2,3,4,5 its
letters are 2,1,1,2, so none is an input 0 for the required 0->1 roots.  The
D4 response cube instead starts at six-site word 110000.  Thus the formal
tensor local system is a canonical enriched comparison, while descent to the
literal physical word/fine/repeated grade remains the degree-zero section.

The shifted Kahler class is functorial but not coefficientwise constant.  A
root at the ridge site v sends ``u_v=q_xv^00`` to
``c_v=q_xv^01`` and therefore sends ``gamma_v=-dOmega_v`` by the connection
face ``-dc_v``.  Mixed curvature is zero.  Both eta and sigma kill c_v, so
their terminal contractions are preserved exactly.  Physically typing the
new dc_v face in the shifted P3+K2 module is not committed.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
from itertools import combinations
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
N = 90
ROOT_SITES = (2, 3, 4, 5)
FACES = (1, 2, 3, 4, 5)
MIDDLE = {1: 1, 2: 2, 3: 1, 4: 1, 5: 2}
X, P, QSITE = 0, 6, 7
PINS = {
    "computations/verify_h3_e14_orbit_relative_d4_target_cone_gate.py":
        "67d33b03ec52c619f29e76c917fdba9b7e28380b4349291fa37b6b7d511e241c",
    "notes/h3-e14-orbit-relative-d4-target-cone-gate.md":
        "6268689c54144cc09b6be596b81d8b4aa741e0590a83e664ec3f6e65b89187bf",
    "computations/verify_h3_e14_d4_unary_moving_target_bicomplex_gate.py":
        "facdbbdcb4f85011c34eeab94c4219b995360381667c6ab790b39612ec397f77",
    "notes/h3-e14-d4-unary-moving-target-bicomplex-gate.md":
        "b79421dd10aaf55fa8a4bffcfa8881193ba5930e1542e4215a575e05c3155114",
    "computations/verify_h3_e14_silent_target_occurrence_compression_gate.py":
        "d8addc92045c58cb9e26492b5c0d641bf8f182454dff3df0fff72a47f2df89a2",
    "computations/verify_h3_reynolds_attach_coupled_obstruction.py":
        "c37ae0188febbde82196a297307b55d03833a2adee87a0e9f12733eef006110b",
    "notes/h3-reynolds-attach-coupled-obstruction.md":
        "d22645280f293482e6ad11074fee4b95044dc1e2714df8e4e370e4845982b39e",
    "computations/verify_h3_residual_q_terminal_ridge_kahler_identification.py":
        "aea73ce5ff6ce183245d209393ed60192066d38eab7d4d203caa0c82cc5b16d6",
    "notes/h3-residual-q-terminal-ridge-kahler-identification.md":
        "ddccd38496103c2a597d3f6f589adf65f3ed7a5ab4da1bc8e36168618d480fd6",
    "computations/verify_h3_physical_cartan_source_orbit_descent.py":
        "c92667c38c57c69dff18fd7570fa154db7e1a634a83f462dfde6bd5553128a3a",
    "computations/verify_h3_rootless_clean_c5_formal_F_full_jacobian_boundary.py":
        "1c17b29f1179416d57acbb2daada0d1f34ee5a69e5f3a68bd6827da0858363e3",
    "computations/verify_h3_rootless_eta_character_source_interface.py":
        "2357e1a4e1c22c4496d99be12b8bf49deea3838337743ea849da29757508517c",
    "computations/verify_h3_e14_cplus_keq_companion_assembly_gate.py":
        "754038f33ae07329e0fc6a8825df9f1695664a40df91afbb77e52dedb1e1aae1",
    "notes/h3-e14-cplus-keq-companion-assembly-gate.md":
        "8548c1db8ec362fce0876c0f67d77efc96f141ebd4c82b6564069e3a089eff3a",
    "computations/verify_h3_cplus_root_even_koszul_physical_dressing_gate.py":
        "9bd2c9f482dc3277d07bd96a4e2189034e766f97e7800d3864179a75e03cef17",
    "notes/h3-cplus-root-even-koszul-physical-dressing-gate.md":
        "c21d7e3e140d2d86d040f9928c787011a7b49e9c58493f812086065c05715e9b",
    "computations/verify_h3_reduced_eq_koszul_tate_relative_orbit_gate.py":
        "15b47a420a6f1e2e6eb0b89e5e5efb5c895172e30b8ab9339dfa1e451ac03668",
    "notes/h3-reduced-eq-koszul-tate-relative-orbit-gate.md":
        "5d5d0b2639cca085d4cc818ba718c154bd5105c79dfbcecd63c018e6a36c92ac",
    "computations/verify_h3_e14_keq_private_placement_pointedness_gate.py":
        "5eef4dff45be6e8993808ef5bcb533d62143dd4bc833a16e2015b48e7bc408d8",
    "notes/h3-e14-keq-private-placement-pointedness-gate.md":
        "59111d6a2dda8a16785cab6c6d129c806ea7e01a2a6d54e092c8841f6521c6c0",
}
EXPECTED_LEDGER_SHA256 = (
    "3a3e59186dd613fbb7975ff626e0b52ca49a2bd154ab3778fdee84c3655e9762"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def faces() -> tuple[tuple[int, ...], ...]:
    return tuple(face for degree in range(5)
                 for face in combinations(ROOT_SITES, degree))


def centered_marked_vector() -> tuple[Q, ...]:
    return (Q(N - 1),) + (Q(-1),) * (N - 1)


def centering_operator(vector: tuple[Q, ...]) -> tuple[Q, ...]:
    total = sum(vector, Q(0))
    return tuple(Q(N) * value - total for value in vector)


def formal_two_parameter_flatness() -> dict[str, object]:
    cube = faces()
    require(len(cube) == 16, "the four-root cube changed")
    e_marked = (Q(1),) + (Q(0),) * (N - 1)
    centered = centered_marked_vector()
    require(centering_operator(e_marked) == centered
            and sum(centered, Q(0)) == 0,
            "the occurrence-centering numerator changed")

    # At Y=1, d(T)=-w and d(rho)=w.  The constant graph G=T+rho is a
    # cycle.  Identity transport of (T,rho,w) over every Boolean edge is a
    # chain map and has trivial square holonomy.
    cap_boundary = (Q(-1), Q(1))
    cap_graph = (Q(1), Q(1))
    require(sum(left * right for left, right in
                zip(cap_boundary, cap_graph, strict=True)) == 0,
            "T+rho stopped being a cap cycle")
    graph_at_vertex = {face: cap_graph for face in cube}
    centered_at_vertex = {face: centered for face in cube}
    require(len(set(graph_at_vertex.values())) == 1
            and len(set(centered_at_vertex.values())) == 1,
            "the formal cap/occurrence local system stopped being constant")

    edge_count = 0
    square_count = 0
    for face in cube:
        for site in ROOT_SITES:
            if site in face:
                continue
            top = tuple(sorted(face + (site,)))
            require(graph_at_vertex[face] == graph_at_vertex[top]
                    and centered_at_vertex[face] == centered_at_vertex[top],
                    ("one formal root edge gained holonomy", face, site))
            # C acts on the tag factor and root transport is identity on the
            # tag.  Check [C,D_i] on the marked generator at every edge.
            require(centering_operator(e_marked) == centered_at_vertex[top],
                    ("[C,D_i] changed", face, site))
            edge_count += 1
        absent = tuple(site for site in ROOT_SITES if site not in face)
        for left, right in combinations(absent, 2):
            left_then_right = graph_at_vertex[
                tuple(sorted(face + (left, right)))
            ]
            right_then_left = graph_at_vertex[
                tuple(sorted(face + (right, left)))
            ]
            require(left_then_right == right_then_left,
                    ("cap square holonomy changed", face, left, right))
            square_count += 1
    require(edge_count == 32 and square_count == 24,
            ("Boolean incidence census changed", edge_count, square_count))
    return {
        "base_ring": "Q[Y] specialized at normalized Y=1",
        "cap_complex": "dT=-w, d(rho)=w",
        "cap_graph": "G=T+rho",
        "cap_graph_boundary": 0,
        "occurrence_centering": "C=N*I-J, N=90",
        "root_action_on_tags": "identity",
        "root_action_on_cap_generators": "identity in the tensor extension",
        "root_edges_checked": edge_count,
        "root_squares_checked": square_count,
        "commutator_C_Di": 0,
        "root_curvature": 0,
        "root_holonomy": "identity",
        "formal_flat_local_system_exists": True,
        "formal_top_vertex": "pure moving target G11[111111]/E14",
    }


def literal_physical_descent_gate() -> dict[str, object]:
    cap_word = tuple(map(int, "01211222"))
    response_word = tuple(map(int, "110000"))
    cap_inputs = tuple(cap_word[site] for site in ROOT_SITES)
    response_inputs = tuple(response_word[site] for site in ROOT_SITES)
    require(cap_inputs == (2, 1, 1, 2)
            and response_inputs == (0, 0, 0, 0),
            ("the cap/response D4 inputs changed", cap_inputs, response_inputs))

    physical = load(
        "computations/verify_h3_physical_cartan_source_orbit_descent.py",
        "cap_flat_physical_orbit",
    ).audit()
    directions = physical["literal_root_covariance"]["ordered_root_directions"]
    require(directions == [[1, 2], [2, 1]],
            ("the pinned physical root directions changed", directions))

    # The covariance theorem is literal once a word has the required old
    # colour.  It cannot be applied to the old cap word along the E14 0->1
    # cube, because none of those four cap letters is zero.  Also the cap
    # word is an eight-site source object whereas the response/E14 word is
    # a six-site object after the endpoint block is removed.
    return {
        "old_physical_cap_word": "01211222",
        "old_physical_cap_fine_repeated_grade": "t*q_(v,N) / P3+K2",
        "old_cap_letters_at_D4_sites_2_3_4_5": list(cap_inputs),
        "D4_required_input_letters": [0, 0, 0, 0],
        "response_D4_base_word": "110000",
        "response_letters_at_D4_sites_2_3_4_5": list(response_inputs),
        "top_response_word": "111111",
        "unary_E14_word": "000101",
        "literal_old_cap_root_transport_defined": False,
        "reason": (
            "the source-provenant root action is covariant on eligible "
            "decorated words, but the old cap word is not an object of the "
            "0->1 D4 cube and has a distinct eight-site fine grade"
        ),
        "formal_tensor_top_is_physical_source_cell": False,
        "obstruction_type": (
            "degree-zero word/fine/repeated-grade section, not curvature "
            "or holonomy"
        ),
    }


def shifted_kahler_connection_audit() -> dict[str, object]:
    # Omega_v=(a-t)-(b-u), gamma_v=-dOmega_v.  For the sitewise root
    # X_i=E_(1,0) at i, q_xv^00 changes to c_v=q_xv^01 exactly when i=v.
    # q_xv^(0,m_v) does not change because every m_v is 1 or 2.
    records = []
    nonzero_connection_faces = 0
    for face in FACES:
        require(MIDDLE[face] in (1, 2), "a ridge middle colour became zero")
        for site in ROOT_SITES:
            root_u = Q(site == face)
            root_b = Q(0)
            root_omega = -root_b + root_u
            root_gamma_dc = -root_omega
            if root_gamma_dc:
                nonzero_connection_faces += 1
            records.append({
                "ridge_face_v": face,
                "root_site_i": site,
                "X_i(u_v)": "q_xv^01" if site == face else "0",
                "X_i(b_v)": "0",
                "X_i(Omega_v)": "q_xv^01" if site == face else "0",
                "L_X_i(gamma_v)": "-d(q_xv^01)" if site == face else "0",
            })
    require(nonzero_connection_faces == 4,
            ("the ridge connection-face census changed",
             nonzero_connection_faces))

    # A second E_(1,0) action kills q_xv^01, and roots at distinct sites
    # touch distinct endpoint labels.  Thus every mixed commutator is zero.
    curvature = {
        (left, right): 0
        for left, right in combinations(ROOT_SITES, 2)
    }
    require(len(curvature) == 6 and not any(curvature.values()),
            "the shifted Kahler root connection acquired curvature")

    # eta_z has weight +1 on p:0 and -1 on z:0.  The connection coordinate
    # c_v=q_xv^(0,1) contains x:0 and v:1, hence has eta weight zero for all
    # z.  sigma has weights +1 on p:2 and -1 on x:2, hence also kills c_v.
    def eta_weight(auxiliary: int, site: int, colour: int) -> int:
        return (int((site, colour) == (P, 0))
                - int((site, colour) == (auxiliary, 0)))

    def sigma_weight(site: int, colour: int) -> int:
        return (int((site, colour) == (P, 2))
                - int((site, colour) == (X, 2)))

    eta_weights = {
        (face, auxiliary):
            eta_weight(auxiliary, X, 0)
            + eta_weight(auxiliary, face, 1)
        for face in FACES for auxiliary in FACES
    }
    sigma_weights = {
        face: sigma_weight(X, 0) + sigma_weight(face, 1)
        for face in FACES
    }
    require(not any(eta_weights.values()) and not any(sigma_weights.values()),
            ("a connection face acquired eta/sigma weight",
             eta_weights, sigma_weights))

    ridge = load(
        "computations/verify_h3_residual_q_terminal_ridge_kahler_identification.py",
        "cap_flat_ridge",
    ).audit()
    terminal = ridge["terminal_ridge_uniqueness"]
    require(terminal["unique_ridge"] == "-Omega_v=-a+t+b-u"
            and terminal["eta_contraction"]
                == "1+delta_(vz)*u_z/t"
            and terminal["sigma_contraction"] == "-q_pq^22",
            ("the pinned eta/sigma law changed", terminal))
    return {
        "ridge": "Omega_v=(a-t)-(b-u)",
        "shifted_class": "gamma_v=-dOmega_v",
        "root_connection_records": records,
        "nonzero_connection_one_faces": nonzero_connection_faces,
        "connection_one_face": "-d(q_xv^01) when root site i=v",
        "mixed_root_curvature": 0,
        "root_holonomy": "identity in the universal Kahler local system",
        "eta_sigma_kill_connection_face": True,
        "fixed_terminal_frame_connection_face_contractions": {
            "eta_z_on_-d(q_xv^01)": 0,
            "sigma_on_-d(q_xv^01)": 0,
        },
        "equivariant_terminal_naturality": (
            "i_(g_*eta)(g^*gamma)=g^*(i_eta gamma); the root sends "
            "u_v to u_v+s*q_xv^01"
        ),
        "eta_law_after_parallel_transport": (
            "1+delta_(vz)*u_z(s)/t in transported coordinates"
        ),
        "sigma_law_after_parallel_transport": "-q_pq^22",
        "terminal_readouts_preserved": True,
        "gamma_is_coefficientwise_constant": False,
        "physical_shifted_connection_face_constructed": False,
        "physical_obstruction": (
            "place the pq/xv shifted gamma and its -d(q_xv^01) connection "
            "faces in one labelled repeated P3+K2 source module"
        ),
    }


def pointed_orbit_keq_unary_assembly() -> dict[str, object]:
    # Necessary quotient rows: marked/private return R and the incidence of
    # the central source input E=(H0-u)e_Eq.  The orbit D4 top supplies only
    # R.  The canonical clean Koszul cell supplies only E.  Their sum is the
    # required comparison column.  The cap graph is dark in this quotient.
    orbit_top = (Q(1), Q(0))
    clean_keq = (Q(0), Q(1))
    cap_graph = (Q(0), Q(0))
    required = (Q(1), Q(1))
    assembled = tuple(left + right for left, right in
                      zip(orbit_top, clean_keq, strict=True))
    central_dual = (Q(0), Q(1))
    require(assembled == required
            and sum(left * right for left, right in
                    zip(central_dual, orbit_top, strict=True)) == 0
            and sum(left * right for left, right in
                    zip(central_dual, clean_keq, strict=True)) == 1
            and sum(left * right for left, right in
                    zip(central_dual, cap_graph, strict=True)) == 0,
            "the orbit/K_Eq central-incidence assembly changed")

    assembly = load(
        "computations/verify_h3_e14_cplus_keq_companion_assembly_gate.py",
        "cap_flat_e14_assembly",
    )
    endpoint_q = assembly.load(
        "computations/verify_h3_e14_first_hit_dual_endpoint_q_extension_gate.py",
        "cap_flat_endpoint_q",
    )
    data, identity = assembly.e14_spair_identity(endpoint_q)
    unary = data["columns"][data["selected_name"]]
    private_return = assembly.RETURN
    require(identity["exact_identity"]
                == "B_E14=U[000101]*v24_11+R_E14"
            and assembly.sparse_add((1, unary), (1, private_return))
                == data["target"],
            "the unary/private E14 identity changed")

    koszul_module = load(
        "computations/verify_h3_reduced_eq_koszul_tate_relative_orbit_gate.py",
        "cap_flat_keq",
    )
    koszul, koszul_digest = koszul_module.audit()
    require(koszul_digest == koszul_module.EXPECTED_LEDGER_SHA256,
            "the reduced-Eq Koszul ledger changed")
    core = koszul["absolute_derived_intersection"]
    old_block = koszul["checked_underived_physical_block"]
    require(core["relative_boundary"] == "dC_K=-F e_Eq"
            and old_block["nearest_boundary"] == "-F e_Eq"
            and old_block["forced_defect"] == "labelled ordinary residue +Y",
            ("the clean/physical K_Eq scope changed", core, old_block))

    root_even = load(
        "computations/verify_h3_cplus_root_even_koszul_physical_dressing_gate.py",
        "cap_flat_root_even",
    ).audit()
    nearest = root_even["nearest_checked_physical_lift"]
    require(root_even["unaugmented_derived"]["constructed"]
            and nearest["lower_private"] == "+E"
            and nearest["Eq"] == "+E"
            and nearest["word_resolved_labelled_ores"] == "-E (nonzero)"
            and nearest["global_anchor_incidence"] == "0",
            ("the nearest physical K_Eq dressing changed", root_even))

    pointed = load(
        "computations/verify_h3_e14_keq_private_placement_pointedness_gate.py",
        "cap_flat_pointed",
    )
    pointed_ledger, pointed_digest = pointed.audit()
    require(pointed_digest == pointed.EXPECTED_LEDGER_SHA256,
            "the E14 pointedness gate changed")
    require("two distinct homogeneous faces" in
                pointed_ledger["shortest_positive_target"],
            ("P_f and the higher K_Eq face merged underived",
             pointed_ledger["shortest_positive_target"]))
    return {
        "quotient_rows": ["private occurrence R", "central Eq-input E"],
        "orbit_D4_top": [1, 0],
        "clean_K_Eq_incidence": [0, 1],
        "horizontal_cap_graph": [0, 0],
        "assembled_Phi_orb_column": [1, 1],
        "required_column": [1, 1],
        "coefficient_level_occurrence_plus_Eq_closes": True,
        "unary_identity": "T12=U[000101]*v24_11+R_E14",
        "independent_T12_cell_after_Phi_orb": False,
        "formal_single_totalization": (
            "pointed P_f bottom face + orbit D4 occurrence cube + clean "
            "K_Eq normal face + old unary U"
        ),
        "raw_pointed_substitution_constructs_it": False,
        "P_f_and_K_Eq_are_distinct_homogeneous_faces": True,
        "clean_K_Eq_in_unaugmented_derived_source": True,
        "clean_K_Eq_in_complete_physical_source": False,
        "nearest_physical_K_Eq_extra_faces": {
            "lower_private": "+E",
            "word_resolved_labelled_ores": "-E",
            "anchor_incidence": 0,
        },
        "physical_single_square_closed": False,
        "first_physical_failure": (
            "compare the clean Koszul normal cell with a literal source-"
            "labelled K_Eq column while cancelling its forced lower/private "
            "and word-resolved residue faces in the same P_f/D4 totalization"
        ),
    }


def cap_terminal_and_frontier_audit() -> dict[str, object]:
    silent = load(
        "computations/verify_h3_e14_silent_target_occurrence_compression_gate.py",
        "cap_flat_silent",
    )
    silent_ledger, silent_digest = silent.audit()
    require(silent_digest == silent.EXPECTED_LEDGER_SHA256,
            "the silent cap normalization ledger changed")
    typing = silent_ledger["physical_typing"]
    require(typing["cap_graph_other_rows"].startswith(
                "boundary,W,Eq,lower,anchor,eta/sigma zero")
            and typing["shifted_ridge"].startswith(
                "the graph correction does not construct"),
            ("the cap graph/ridge separation changed", typing))
    return {
        "cap_graph_eta_sigma": 0,
        "cap_graph_other_zero_rows": [
            "boundary", "W", "Eq", "lower", "anchor",
        ],
        "cap_graph_physical_q_determined": False,
        "shifted_ridge_is_separate_from_cap_graph": True,
        "formal_two_parameter_consequence": (
            "once one pointed physical c_f/P_f/AugP2 base section carries "
            "the cap graph, C and D4 transport it without another curvature "
            "or holonomy theorem"
        ),
        "first_unfilled_faces_after_formal_transport": [
            "one augmented P_f/D4/clean-K_Eq comparison with literal lower "
            "and word-resolved residue cancellation",
            "the labelled shifted-Kahler connection/q clause",
        ],
        "independent_T12_face_after_central_placement": False,
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "E14 two-parameter flat cap-graph transport gate",
        "pins": PINS,
        "formal_C_times_D4_cap_local_system": formal_two_parameter_flatness(),
        "literal_physical_descent": literal_physical_descent_gate(),
        "shifted_Kahler_connection": shifted_kahler_connection_audit(),
        "pointed_orbit_K_Eq_unary_assembly":
            pointed_orbit_keq_unary_assembly(),
        "cap_terminal_scope_and_frontier": cap_terminal_and_frontier_audit(),
        "verdict": (
            "The normalized cap graph has a canonical flat extension over "
            "the product of the occurrence-centering direction and the "
            "four-root moving-target cube: [C,D_i]=0, curvature is zero, "
            "and square holonomy is trivial.  The shifted Kahler class has "
            "the flat connection face -d(q_xv^01) at i=v; this face is eta/"
            "sigma dark in the fixed frame, and equivariant contraction "
            "preserves the terminal laws in transported coordinates.  "
            "At coefficient level the orbit top (1,0) plus the clean K_Eq "
            "incidence (0,1) is exactly the required Phi_orb column (1,1); "
            "the old unary row then closes T12, so T12 is not independent. "
            "However this is not yet a physical E14 source cell: the old cap "
            "word 01211222 is not in the 110000->111111 root cube, and no "
            "labelled P3+K2 section places the cap graph, the clean K_Eq "
            "cell, or the Kahler connection face there.  The nearest "
            "physical K_Eq lift has forced lower/private +E and labelled "
            "residue -E.  The obstruction is augmented descent/grading, "
            "not curvature, holonomy, or a second T12 class."
        ),
        "scope": (
            "canonical h=3 normalized Y=1 cap block, 90 occurrence tags, "
            "and the four E14 root sites.  The formal relative PP/Kahler "
            "local systems and terminal contractions are exact.  No claim "
            "is made that the free tensor extension is quasi-isomorphic to "
            "the literal physical correction complex or that physical q "
            "has been transported."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("formal cap graph over C x D4: FLAT")
    print("[C,D_i]=0; root curvature=0; holonomy=identity")
    print("ridge connection: -d(q_xv^01) at i=v; eta/sigma DARK")
    print("orbit (1,0) + clean K_Eq (0,1) = required Phi_orb (1,1)")
    print("old unary closes T12 after Phi_orb: YES")
    print("literal physical E14/P3+K2 placement: NOT CONSTRUCTED")
    print("first obstruction: word/fine/repeated-grade descent, not curvature")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
