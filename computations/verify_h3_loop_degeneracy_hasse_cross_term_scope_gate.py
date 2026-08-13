#!/usr/bin/env python3
"""Audit the proposed relative-degeneracy/Hasse unification.

The two loop failures really have one common target geometry.  Every Gate-I
shared loop and every maximal tau_plus omitted loop identifies two source
sites at target site 4, hence asks for the divided-power diagonal direction
2e_4.  For multi-affine factors the normalization is exact:

    D_4^[2](f g) = D_4^[1](f) D_4^[1](g).

This is a formal repeated-direction face of the prolonged Hasse-Schmidt
resolution.  It is not a column in the old literal matching/cofactor Hasse
inventory: every such coefficient is a submatching and is site-squarefree.
Nor is it by itself the required physical comparison.  Five distinct source
loop edges collapse to the same 2e_4 target coordinate, and the tau_plus
single-C4 images avoid B1,B4 entirely.  A label-decorated relative cone cell,
with matching transport and augmented readouts, is still required.

The beta=0 unit J_M=1 is not this simplicial degeneracy.  It is a genuine
nondegenerate third-cofactor/fourth-row Hasse top.  Calling it degenerate kills
it after normalization; retaining it keeps its source-descent unit, endpoint
ridge, and wrong word.  Thus a broad relative Hasse/bar family could package
all three obligations, but the ordinary normalized degeneracy operator does
not construct any of them.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations_with_replacement, product
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_hasse_coproduct_cosimplicial_totalization.py":
        "674a7503db43b8ad53d6f4ea9d7fe095f0f26629d92e4b0dd291f14bde82fa3a",
    "computations/verify_h3_cut_swap_support_tail_lift_shared_loop_gate.py":
        "db23eb4e760dd84934426a80516aad355486e947626da1849454718b512efb2d",
    "computations/verify_h3_trace_cartan_tau_plus_site_collapse_gate.py":
        "f0801bfcd5362f2fc8d9a81bf85a84b2d380fd37cbbe7db2252b352b785d5474",
    "computations/verify_h3_trace_cartan_even_repair_relative_c4_scope_gate.py":
        "645df036367a7fe60f3ce625dc37710f7e83129a84a3619005945ca6b4f0a486",
    "computations/verify_h3_cut_swap_shared_loop_repair_existing_family_gate.py":
        "bd20b6320172f846d7c4aa38ec6ebba0c0cfea4c056b8758df19d31b5ab20231",
    "computations/verify_h3_rootless_five_cycle_first_tor_multidegree_gate.py":
        "a5d9021664b904f895323c29806a825545afd16085c971dc573353bb6c11a81f",
    "computations/verify_h3_rootless_third_cofactor_bianchi_total_complex_obstruction.py":
        "ebd25f79a6fe8db936fe5601b9220f152c5349dd794bbc4e08b2095f1c1d059f",
    "computations/verify_h3_rootless_one_face_third_cofactor_comparison_vertex_gate.py":
        "37251145d805861b2d1b15b7bf37cf9f98ba30b03fbcffa1daa4fc35789efe84",
    "computations/verify_h3_source_valid_tower_first_obstruction.py":
        "ba37c966c2ef2cca2f8909a91e8ff8a8567282e68a847ac4eef75d3bb78a56ac",
    "computations/verify_h3_pure_unary_cofactor_incidence_attachment.py":
        "3295183db431e14733eceea645a28113eccd086eebbf256afaa7127cc826b8cd",
}
EXPECTED_LEDGER_SHA256 = (
    "bfa637ff164e5483f8f7649755b1c3d45a383132308e07822df2073260d01704"
)


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def normalized_boundary(simplex):
    coefficients = Counter()
    for index in range(len(simplex)):
        face = simplex[:index] + simplex[index + 1:]
        if len(set(face)) != len(face):
            continue
        coefficients[face] += (-1) ** index
    return Counter({face: coefficient for face, coefficient
                    in coefficients.items() if coefficient})


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))

    hasse = load(
        "computations/verify_h3_hasse_coproduct_cosimplicial_totalization.py",
        "loop_degeneracy_hasse",
    )
    support = load(
        "computations/verify_h3_cut_swap_support_tail_lift_shared_loop_gate.py",
        "loop_degeneracy_support",
    )
    tau = load(
        "computations/verify_h3_trace_cartan_tau_plus_site_collapse_gate.py",
        "loop_degeneracy_tau",
    )
    even_c4 = load(
        "computations/verify_h3_trace_cartan_even_repair_relative_c4_scope_gate.py",
        "loop_degeneracy_even_c4",
    )
    shared_c4 = load(
        "computations/verify_h3_cut_swap_shared_loop_repair_existing_family_gate.py",
        "loop_degeneracy_shared_c4",
    )
    literal = load(
        "computations/verify_h3_rootless_five_cycle_first_tor_multidegree_gate.py",
        "loop_degeneracy_literal",
    )
    total = load(
        "computations/verify_h3_rootless_third_cofactor_bianchi_total_complex_obstruction.py",
        "loop_degeneracy_beta_total",
    )

    # Exact divided-power normalization.  In one variable x, take f=x and
    # g=x.  D^[2](x^2)=1, while D^[1](x)D^[1](x)=1.  The ordinary second
    # derivative would be 2, so the divided-power convention is essential.
    f = (1, 0, 0)
    g = (1, 0, 0)
    order_two = (2, 0, 0)
    order_one = (1, 0, 0)
    joined = hasse.add_multiindices(f, g)
    divided_second = hasse.hasse(joined, order_two)
    cross_term = hasse.hasse(f, order_one) * hasse.hasse(g, order_one)
    require(divided_second == cross_term == 1,
            "the multi-affine second-Hasse cross term changed normalization")
    require(hasse.hasse(f, order_two) == hasse.hasse(g, order_two) == 0,
            "a multi-affine factor acquired its own second Hasse term")
    repeated_mask = 0b11
    reduced = hasse.reduced_coproduct(repeated_mask)
    require(reduced == Counter({(1, 2): 1, (2, 1): 1}),
            "the labelled two-direction Hasse coproduct changed")

    lower = support.load(
        "computations/verify_h3_complete_tangent_lower_protected_phi_reduction.py",
        "loop_degeneracy_lower",
    )
    tangent = support.load(
        "computations/verify_h3_tangent_euler_occurrence_splitter_fredholm.py",
        "loop_degeneracy_tangent",
    )
    complete = support.load(
        "computations/verify_h3_rootless_c5_complete_multidegree_source_no_go.py",
        "loop_degeneracy_complete",
    )
    base = support.load(
        "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py",
        "loop_degeneracy_base",
    )

    key = lambda label: (label[1], label[2])
    cut_012 = frozenset(map(key, lower.lower_labels(tangent, (0, 1, 2))))
    cut_024 = frozenset(map(key, lower.lower_labels(tangent, (0, 2, 4))))
    labels = tuple(sorted(cut_012 | cut_024))
    shared = tuple(sorted(cut_012 & cut_024))
    require(len(labels) == 15 and len(shared) == 3
            and {edge for _matching, edge in shared} == {(0, 2)},
            "the Gate-I shared loop labels changed")

    left, right, left_cell, _right_cell = complete.CUBIC_PAIRS[1]
    target_degree = complete.degree_add(
        base.lambda_degree(left),
        complete.cell_degree(complete.CYCLE_CELLS[left_cell]),
    )
    component = complete.component(base, target_degree)
    pure = tuple((multiplier, boundary) for word, multiplier, boundary
                 in component["columns"] if word == complete.PURE_WORD)
    graph_index = {support.graph(multiplier): index
                   for index, (multiplier, _boundary) in enumerate(pure)}
    require((left, right) == (3, 5) and len(graph_index) == 6,
            "the canonical target component changed")

    # Gate I: every successful support collapse has 0,2 -> 4, so the three
    # shared matching factors become the same target diagonal direction 2e4.
    gate_i_loop_edges = set()
    gate_i_maps = (
        (4, 2, 4, 1, 5, 3),
        (4, 2, 4, 3, 5, 1),
        (4, 5, 4, 1, 2, 3),
        (4, 5, 4, 3, 2, 1),
    )
    for values in gate_i_maps:
        require(values[0] == values[2] == 4,
                "a Gate-I collapse left the target-4 diagonal")
        for matching_index, repeated_edge in shared:
            require(repeated_edge in tangent.MATCHINGS[matching_index],
                    "a shared repeated edge left its matching")
            gate_i_loop_edges.add(repeated_edge)
    require(gate_i_loop_edges == {(0, 2)},
            "the Gate-I loop-edge set changed")

    # Tau_plus: exhaust the same equivariant maps and retain the 16 maximal
    # thirteen-label collapses.  Their double fibre is always over target 4;
    # four distinct source edges occur, all mapping to the same diagonal.
    tau_loop_edges = Counter()
    maximal_maps = 0
    omitted_records = 0
    for values in product(support.TARGET_ODD, repeat=6):
        phi = dict(enumerate(values))
        if any(phi[support.RHO[site]] != support.TARGET_S[phi[site]]
               for site in range(6)):
            continue
        images = tuple(support.collapse_graph(tangent, label, phi)
                       for label in labels)
        valid = tuple(index for index, image in enumerate(images)
                      if image in graph_index)
        if len(valid) != 13:
            continue
        maximal_maps += 1
        fibres = Counter(values)
        repeated_targets = tuple(site for site, count in fibres.items()
                                 if count == 2)
        require(repeated_targets == (4,),
                "a maximal tau_plus loop left target site 4")
        source_fibre = tuple(index for index, value in enumerate(values)
                             if value == 4)
        require(len(source_fibre) == 2,
                "the tau_plus double fibre changed size")
        loop_edge = tuple(sorted(source_fibre))
        invalid = tuple(sorted(set(range(15)) - set(valid)))
        require(len(invalid) == 2,
                "a maximal tau_plus map stopped omitting one rho pair")
        for index in invalid:
            matching_index, _repeated_edge = labels[index]
            require(loop_edge in tangent.MATCHINGS[matching_index],
                    "an omitted tau_plus matching lost the double-fibre edge")
            tau_loop_edges[loop_edge] += 1
            omitted_records += 1
    require(maximal_maps == 16 and omitted_records == 32
            and set(tau_loop_edges) == {(0, 3), (0, 5), (2, 3), (2, 5)}
            and set(tau_loop_edges.values()) == {8},
            ("the tau_plus diagonal-loop census changed", tau_loop_edges))

    # All five source loop edges above map to one target Hasse multiindex.
    # The target therefore forgets the source label; a label-decorated
    # section is extra data, not a consequence of the diagonal direction.
    all_source_loop_edges = gate_i_loop_edges | set(tau_loop_edges)
    target_diagonal = (0, 0, 0, 2, 0)  # coordinates are target sites 1,...,5
    require(len(all_source_loop_edges) == 5 and sum(target_diagonal) == 2,
            "the source-label/target-diagonal fibre changed")

    # Existing literal matching Hasse coefficients are submatchings.  Replay
    # their exact site-squarefree census: none occupies 2e4.  The universal
    # Hasse algebra admits the repeated direction formally, but its own scope
    # leaves the augmented physical comparison open.
    generators = literal.c5_generators()
    syzygies, _resolution = literal.first_tor_resolution(generators)
    literal_inventory = literal.literal_inventory_gate(syzygies)
    require(literal_inventory["complete_eight_site_Hasse_subsets_checked"]
            == 105 * 16
            and literal_inventory["literal_cofactor_site_bound"]
                == "every physical site degree is at most 1"
            and literal_inventory["inventory_match_count"] == 0,
            "the literal squarefree Hasse inventory changed")
    hasse_source = (ROOT / "computations/verify_h3_hasse_coproduct_cosimplicial_totalization.py").read_text()
    require('"remaining_comparison"' in hasse_source
            and "map this canonical multigraded source resolution to the physical"
                in hasse_source,
            "the formal-to-physical Hasse scope changed")

    # The first local C4 consequences do not silently solve the comparison.
    # Gate I has admissible target choices but no protected source binomial;
    # tau_plus has no direct B1/B4 target at all.
    shared_ledger, shared_digest = shared_c4.audit()
    require(shared_digest == shared_c4.EXPECTED_LEDGER_SHA256
            and shared_ledger["protected_base_guard"]
                ["can_cancel_r0_target_and_ainc"] is False,
            "the Gate-I C4 source-boundary guard changed")
    even_ledger, even_digest = even_c4.audit()
    require(even_digest == even_c4.EXPECTED_LEDGER_SHA256
            and even_ledger["tau_plus_local_C4_census"]
                ["all_direct_C4_targets"] == [0, 2, 3, 5]
            and even_ledger["tau_plus_local_C4_census"]
                ["direct_targets_B1_or_B4"] is False,
            "the tau_plus C4 target guard changed")

    # A simplicial degeneracy is not the same object as a repeated-direction
    # divided-power Hasse face.  In normalized chains every repeated-vertex
    # simplex and its boundary vanish.  A nondegenerate top retains all faces.
    top_strings = tuple(combinations_with_replacement(range(5), 5))
    degenerate = tuple(simplex for simplex in top_strings
                       if len(set(simplex)) != len(simplex))
    nondegenerate = tuple(simplex for simplex in top_strings
                          if len(set(simplex)) == len(simplex))
    require(len(top_strings) == 126 and len(degenerate) == 125
            and nondegenerate == ((0, 1, 2, 3, 4),)
            and all(not normalized_boundary(simplex) for simplex in degenerate)
            and len(normalized_boundary(nondegenerate[0])) == 5,
            "the normalized degeneracy/nondegenerate-top split changed")

    # Beta=0 J_M is the nondegenerate top, not the killed degeneracy.  The
    # committed physical audit records the three independent defects.
    total_ledger = total.audit()
    beta = total_ledger["third_cofactor_total_complex"]
    require(total_ledger["ledger_sha256"]
            == "493899d93b7eafd6fd520dc01795c1b7051f549421c0d3a2363c1a780a6bac0f"
            and beta["identity"].endswith("=1")
            and beta["source_labelled_bridge"]["ridge_mismatch_rank"] == 6
            and beta["source_labelled_bridge"]["primitive_omega_rank"] == 5
            and beta["descent_obstruction"]
                ["fourth_operator_on_source_equation"] == 1
            and total_ledger["endpoint_midpoint_grade"]["midpoint_hits"] == 0,
            "the beta-zero nondegenerate Hasse-top obstruction changed")

    ledger = {
        "theorem": "relative-degeneracy/Hasse cross-term scope gate",
        "pins": PINS,
        "divided_power_identity": {
            "formula": "D_4^[2](f*g)=D_4(f)*D_4(g) for multi-affine f,g",
            "coefficient": divided_second,
            "ordinary_second_derivative_coefficient": 2,
            "two_labelled_split_terms": len(reduced),
        },
        "common_loop_geometry": {
            "target_site": 4,
            "target_Hasse_multiindex": "2e_4",
            "Gate_I_source_loop_edges": [list(edge)
                                         for edge in sorted(gate_i_loop_edges)],
            "tau_plus_source_loop_edges": [list(edge)
                                            for edge in sorted(tau_loop_edges)],
            "tau_plus_maximal_maps": maximal_maps,
            "tau_plus_omitted_label_records": omitted_records,
            "distinct_source_loop_edges_over_same_target_diagonal":
                len(all_source_loop_edges),
            "structural_consequence": (
                "Gate I and tau_plus share one target divided-power diagonal, "
                "but source-edge and repeated-grade labels must remain tagged"
            ),
        },
        "inventory_verdict": {
            "formal_prolonged_Hasse_face_exists": True,
            "old_literal_matching_Hasse_column_exists": False,
            "old_literal_site_bound": 1,
            "required_target_site_multiplicity": 2,
            "physical_relative_comparison_constructed": False,
            "minimal_new_cell": (
                "a source-loop-labelled relative diagonal Hasse/mapping-cone "
                "cell over 2e_4, carrying the C4/matching transport, exact "
                "word/fine/repeated grade, labelled ordinary residue, and "
                "zero protected target/anchor rows"
            ),
        },
        "local_matching_transport": {
            "Gate_I_single_C4_has_candidate_targets": True,
            "Gate_I_protected_source_binomial_constructed": False,
            "tau_plus_single_C4_target_set": ["B0", "B2", "B3", "B5"],
            "tau_plus_single_C4_hits_B1_or_B4": False,
            "consequence": (
                "the cross term alone cannot be read as d_fixed/d_pair or "
                "d_even; an additional same-grade matching/denominator "
                "transport is essential"
            ),
        },
        "beta_zero_comparison": {
            "J_M": "nondegenerate third-cofactor/fourth-row Hasse top = 1",
            "same_second_diagonal_as_loop_repairs": False,
            "simplicial_degeneracy_would_survive_normalization": False,
            "retained_nondegenerate_top_faces": 5,
            "source_descent_unit": 1,
            "endpoint_ridge_rank": 6,
            "primitive_Omega_rank": 5,
            "correct_midpoint_word_hits": 0,
            "consequence": (
                "a master higher relative Hasse/bar family could include the "
                "beta-zero cell at a different order, but ordinary normalized "
                "degeneracy does not produce its D0 target nullhomotopy"
            ),
        },
        "answer": (
            "the proposed Hasse cross term is the correct common formal local "
            "model for the Gate-I and tau_plus loop singularities.  It is not "
            "already a physical source column and does not identify beta=0. "
            "The missing theorem is precisely a label-decorated relative "
            "Hasse comparison, not the abstract degeneracy identity"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("relative degeneracy/Hasse ledger changed", digest))
    return ledger, digest


def main():
    _ledger, digest = audit()
    print("h3 loop degeneracy/Hasse cross term: FORMAL UNIFICATION ONLY")
    print("Gate I + tau_plus loops: common target diagonal 2e_4")
    print("D^[2](fg)=D(f)D(g): exact divided-power coefficient 1")
    print("old literal Hasse inventory: site-squarefree, no 2e_4 column")
    print("needed: source-labelled relative diagonal cone + matching transport")
    print("beta=0 J_M: nondegenerate higher top, not normalized degeneracy")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
