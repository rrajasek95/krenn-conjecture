#!/usr/bin/env python3
"""Construct the nonzero cut-swap tail and isolate its shared-loop defect.

For the canonical faces-(3,5) repeated P3+K2 component, the exact physical
automorphism group that preserves the fine degree and direct-free pair has
one nontrivial odd-site action s=(2 5).  Enumerating every equivariant
one-double-fibre map from the six collision sites to the five odd sites gives
four maps on the twelve nonzero labels.  Their signed images are

    +/- 2 (B_0+B_2-B_3-B_5).

After the rational normalization 1/2 this is one of the literal 360-feature
alpha aggregates in M_v=-O_alpha+K.  None of the four maps extends to all
fifteen collision labels: every shared label contains the repeated edge 02,
and every successful map identifies 0 and 2 at target site 4, producing the
forbidden loop 44.  The shared packet is one fixed rho label plus one rho
pair, so a full comparison needs exactly two additional equivariant image
choices in a diagonal/loop-resolution source cell.

This is a construction on the signed twelve-label lower packet and a no-go
only for the natural one-double-fibre site-collapse class.  It is not a
no-go for an arbitrary relative linear comparison.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from itertools import permutations, product
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_cut_swap_odd_prism_kdu_typing_gate.py":
        "a1c7868bee94baf12f0f4915305bb1e21cdc3f6732ccec9adf3d68768d3d90b0",
    "computations/verify_h3_complete_tangent_lower_protected_phi_reduction.py":
        "ea45c09a8347c312ea9721475d54a4b4f9aad21d8d51cb9d4d297aeaa99ba429",
    "computations/verify_h3_cut_swap_collision_word_orbit_obstruction.py":
        "d7281084a0fc084e6d951f527daf92c92faefebec183a83d6cfa33e055596c77",
    "computations/verify_h3_rootless_c5_complete_multidegree_source_no_go.py":
        "719e48963faac5cd1dc5e7348de41e86f690f3046fefba88dddfa60bae532899",
    "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py":
        "190171b72493e661dedb8e7aa369a9b72f1a71e14487632df2841ca7eeb19bf4",
    "computations/verify_h3_residual_q_literal_mapping_cone_private_boundary_gate.py":
        "b890195a8fc0c4e90c9c9c0c03c41a95690228c81026f4c2ea1fa95908564e38",
    "computations/verify_h3_literal_mv_cap_cartan_composition.py":
        "8e54a161402499c638dcba6177069fc3bb37648fb37c3546955310a56889744e",
}
EXPECTED_LEDGER_SHA256 = (
    "8c255624f436b4685df302b0237855fc3b1156731235a322f5c07bc40828fefb"
)

RHO = (0, 4, 2, 3, 1, 5)
TARGET_S = {1: 1, 2: 5, 3: 3, 4: 4, 5: 2}
TARGET_ODD = tuple(TARGET_S)


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


def permute_edge(edge, permutation):
    return tuple(sorted(permutation[site] for site in edge))


def permute_matching(matching, permutation):
    return tuple(sorted(permute_edge(edge, permutation) for edge in matching))


def transform_degree(degree, site_permutation, colour_permutation):
    answer = [0] * len(degree)
    for site in range(8):
        for colour in range(3):
            answer[3 * site_permutation[site] + colour_permutation[colour]] = (
                degree[3 * site + colour]
            )
    return tuple(answer)


def transform_multiplier(base, multiplier, site_permutation,
                         colour_permutation):
    return tuple(sorted(
        base.edge(site_permutation[left], site_permutation[right],
                  colour_permutation[left_colour],
                  colour_permutation[right_colour])
        for left, right, left_colour, right_colour in multiplier
    ))


def graph(multiplier):
    return tuple(sorted((left, right) for left, right, _lc, _rc in multiplier))


def rho_label(tangent, label):
    matching_index, repeated_edge = label
    matching = permute_matching(tangent.MATCHINGS[matching_index], RHO)
    return (tangent.MATCHING_INDEX[matching],
            permute_edge(repeated_edge, RHO))


def collapse_graph(tangent, label, phi):
    matching_index, _repeated_edge = label
    edges = []
    for left, right in tangent.MATCHINGS[matching_index]:
        image = tuple(sorted((phi[left], phi[right])))
        if image[0] == image[1]:
            return None
        edges.append(image)
    return tuple(sorted(edges))


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))

    lower = load(
        "computations/verify_h3_complete_tangent_lower_protected_phi_reduction.py",
        "support_tail_lower",
    )
    tangent = load(
        "computations/verify_h3_tangent_euler_occurrence_splitter_fredholm.py",
        "support_tail_tangent",
    )
    complete = load(
        "computations/verify_h3_rootless_c5_complete_multidegree_source_no_go.py",
        "support_tail_complete",
    )
    base = load(
        "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py",
        "support_tail_base",
    )
    literal = load(
        "computations/verify_h3_residual_q_literal_mapping_cone_private_boundary_gate.py",
        "support_tail_literal",
    )
    mv = load(
        "computations/verify_h3_literal_mv_cap_cartan_composition.py",
        "support_tail_mv",
    )

    # The physical lower module and its signed twelve-label cut difference.
    key = lambda label: (label[1], label[2])
    base_labels = frozenset(map(key, lower.lower_labels(tangent, (0, 1, 2))))
    other_labels = frozenset(map(key, lower.lower_labels(tangent, (0, 2, 4))))
    all_labels = tuple(sorted(base_labels | other_labels))
    shared_labels = tuple(sorted(base_labels & other_labels))
    support_labels = tuple(sorted(base_labels ^ other_labels))
    lower_vector = {
        label: Q(int(label in other_labels) - int(label in base_labels))
        for label in all_labels
    }
    lower_vector = {label: value for label, value in lower_vector.items()
                    if value}
    require(len(all_labels) == 15 and len(shared_labels) == 3
            and len(support_labels) == len(lower_vector) == 12,
            "the 15/3/12 lower packet changed")
    require({edge for _matching, edge in shared_labels} == {(0, 2)},
            "the shared packet stopped being the repeated-02 packet")
    require(all(lower_vector[rho_label(tangent, label)] == -value
                for label, value in lower_vector.items()),
            "the signed lower stopped being rho-odd")

    # Canonical h=3 repeated component (faces 3,5), with its six pure
    # multiplier columns and literal 90-feature boundaries.
    left, right, left_cell, _right_cell = complete.CUBIC_PAIRS[1]
    require((left, right) == (3, 5), "the canonical repeated component moved")
    target_degree = complete.degree_add(
        base.lambda_degree(left),
        complete.cell_degree(complete.CYCLE_CELLS[left_cell]),
    )
    component = complete.component(base, target_degree)
    pure = tuple((multiplier, boundary) for word, multiplier, boundary
                 in component["columns"] if word == complete.PURE_WORD)
    require(len(component["columns"]) == 288 and len(pure) == 6,
            "the canonical complete component changed size")
    pure_graphs = tuple(graph(multiplier) for multiplier, _boundary in pure)
    graph_index = {value: index for index, value in enumerate(pure_graphs)}
    require(len(graph_index) == 6, "pure multiplier graphs collided")

    # Exhaust the physical fine-grade automorphisms.  The endpoint swap is
    # invisible on the pure multipliers; the unique nontrivial odd action is
    # s=(2 5), inducing (0 5)(2 3) on the six pure columns.
    pure_multiplier_set = frozenset(multiplier for multiplier, _boundary in pure)
    automorphisms = []
    for site_permutation in permutations(range(8)):
        if frozenset(site_permutation[site]
                     for site in base.DIRECT_FREE_PAIR) != base.DIRECT_FREE_PAIR:
            continue
        for colour_permutation in permutations(range(3)):
            if transform_degree(target_degree, site_permutation,
                                colour_permutation) != target_degree:
                continue
            transformed = frozenset(transform_multiplier(
                base, multiplier, site_permutation, colour_permutation
            ) for multiplier in pure_multiplier_set)
            if transformed != pure_multiplier_set:
                continue
            induced = tuple(next(index for index, (candidate, _row)
                                 in enumerate(pure)
                                 if candidate == transform_multiplier(
                                     base, multiplier, site_permutation,
                                     colour_permutation))
                            for multiplier, _row in pure)
            automorphisms.append((site_permutation, colour_permutation,
                                  induced))
    require(len(automorphisms) == 4,
            ("the canonical physical automorphism group changed",
             len(automorphisms)))
    require({colour for _site, colour, _induced in automorphisms}
            == {tuple(range(3))},
            "a nontrivial global colour action entered the canonical grade")
    odd_actions = {tuple(site[odd] for odd in TARGET_ODD)
                   for site, _colour, _induced in automorphisms}
    require(odd_actions == {(1, 2, 3, 4, 5), (1, 5, 3, 4, 2)},
            ("the odd-site symmetry changed", odd_actions))
    induced_actions = {induced for _site, _colour, induced in automorphisms}
    require(induced_actions == {
        (0, 1, 2, 3, 4, 5), (5, 1, 3, 2, 4, 0)
    }, ("the pure multiplier action changed", induced_actions))

    # Exhaust every one-double-fibre six-to-five site-collapse map that
    # intertwines rho with s.  Four maps lift all twelve nonzero labels;
    # none lifts the complete physical U15 module.
    good_support = []
    good_all = []
    for values in product(TARGET_ODD, repeat=6):
        if sorted(Counter(values).values()) != [1, 1, 1, 1, 2]:
            continue
        phi = dict(enumerate(values))
        if any(phi[RHO[site]] != TARGET_S[phi[site]] for site in range(6)):
            continue
        images = {label: collapse_graph(tangent, label, phi)
                  for label in all_labels}
        support_ok = all(images[label] in graph_index
                         for label in support_labels)
        all_ok = all(images[label] in graph_index for label in all_labels)
        if support_ok:
            signed = [Q(0)] * len(pure)
            for label, coefficient in lower_vector.items():
                signed[graph_index[images[label]]] += coefficient
            good_support.append((values, tuple(signed), images))
        if all_ok:
            good_all.append(values)
    expected_maps = {
        (4, 2, 4, 1, 5, 3),
        (4, 2, 4, 3, 5, 1),
        (4, 5, 4, 1, 2, 3),
        (4, 5, 4, 3, 2, 1),
    }
    require({values for values, _signed, _images in good_support}
            == expected_maps and not good_all,
            ("the equivariant site-collapse census changed",
             [entry[0] for entry in good_support], good_all))
    target_alpha = (Q(1), Q(0), Q(1), Q(-1), Q(0), Q(-1))
    require({signed for _values, signed, _images in good_support}
            == {tuple(2 * value for value in target_alpha),
                tuple(-2 * value for value in target_alpha)},
            "the signed support image changed")

    # The rationally normalized image is literally a 360-feature alpha
    # aggregate: order (5,0,2,3) with alpha=(-,+,+,-).
    boundary = defaultdict(Q)
    for coefficient, (_multiplier, row) in zip(target_alpha, pure, strict=True):
        for feature in row:
            boundary[feature] += coefficient
    boundary = {feature: value for feature, value in boundary.items() if value}
    selected_indices = (5, 0, 2, 3)
    expected_boundary = defaultdict(Q)
    for coefficient, index in zip(literal.ALPHA, selected_indices, strict=True):
        for feature in pure[index][1]:
            expected_boundary[feature] += coefficient
    expected_boundary = {feature: value for feature, value
                         in expected_boundary.items() if value}
    require(boundary == expected_boundary and len(boundary) == 360,
            "the normalized support lift stopped being the literal M_v aggregate")
    require(sum(target_alpha) == 0,
            "the support lift acquired a pure target/ainc coefficient")
    require(tuple(target_alpha[index] for index in (5, 1, 3, 2, 4, 0))
            == tuple(-value for value in target_alpha),
            "the target alpha aggregate stopped being s-odd")
    require(mv.EXPECTED_LEDGER_SHA256
            == "84904cfd9f434eb8ff36548a0b2e0b2e68b8ec562c6559a89acdefb94500eb64",
            "the exact output-side M_v theorem changed")

    # Every successful collapse identifies 0 and 2 at site 4.  Therefore
    # all three shared labels produce a loop 44.  They cannot be set to zero:
    # forgetting the repeated edge sends them to three distinct unit
    # occurrence coordinates.  Their rho action has orbit sizes 1 and 2.
    loop_records = set()
    for values, _signed, _images in good_support:
        require(values[0] == values[2] == 4,
                "a successful support map stopped collapsing 02 to 44")
        phi = dict(enumerate(values))
        for matching_index, repeated_edge in shared_labels:
            repeated_image = tuple(sorted(
                (phi[repeated_edge[0]], phi[repeated_edge[1]])))
            matching = tangent.MATCHINGS[matching_index]
            other_images = tuple(sorted(
                tuple(sorted((phi[left], phi[right])))
                for left, right in matching if (left, right) != repeated_edge
            ))
            loop_records.add((repeated_image, other_images))
            require(repeated_image == (4, 4),
                    "a shared repeated edge stopped becoming loop 44")
    shared_orbits = []
    remaining = set(shared_labels)
    while remaining:
        seed = min(remaining)
        orbit = {seed, rho_label(tangent, seed)}
        require(orbit <= set(shared_labels),
                "rho moved a shared label outside the shared packet")
        shared_orbits.append(tuple(sorted(orbit)))
        remaining -= orbit
    require(sorted(map(len, shared_orbits)) == [1, 2]
            and len({matching for matching, _edge in shared_labels}) == 3,
            "the minimal shared-loop orbit/occurrence count changed")

    ledger = {
        "theorem": "cut-swap support tail lift and shared-loop gate",
        "pins": PINS,
        "canonical_component": {
            "faces": [left, right],
            "complete_columns": len(component["columns"]),
            "pure_multipliers": len(pure),
            "pure_graphs": [list(map(list, value)) for value in pure_graphs],
            "physical_grade_automorphisms": len(automorphisms),
            "nontrivial_odd_site_action": "s=(2 5)",
            "induced_pure_action": "(0 5)(2 3), with 1 and 4 fixed",
        },
        "positive_support_construction": {
            "U15_labels": len(all_labels),
            "shared_labels": len(shared_labels),
            "signed_support_labels": len(support_labels),
            "rho_equivariant_one_double_fibre_maps": [
                list(values) for values in sorted(expected_maps)
            ],
            "signed_pushforwards": [
                "2*(B0+B2-B3-B5)", "-2*(B0+B2-B3-B5)"
            ],
            "rational_normalization": "1/2",
            "normalized_alpha": [int(value) for value in target_alpha],
            "literal_corner_order": list(selected_indices),
            "literal_alpha": [int(value) for value in literal.ALPHA],
            "literal_boundary_support": len(boundary),
            "rho_target_parity": "rho/s-odd",
            "protected_rows": (
                "sum(alpha)=0 cancels pure r0 target and ainc; the r0 tail "
                "has no W/D rows; Eq retains alpha.  Adding the already "
                "physical Cartan K gives the exact normalized M_v ridge"
            ),
        },
        "sharp_site_collapse_obstruction": {
            "maps_lifting_all_15_labels": len(good_all),
            "shared_repeated_edge": "02",
            "forced_image": "44",
            "possible_other_edge_images": [
                [list(edge) for edge in record[1]]
                for record in sorted(loop_records)
            ],
            "reason": (
                "44 is a coefficient loop, absent from the physical edge "
                "algebra and from all six pure multiplier graphs"
            ),
            "zero_extension_is_not_a_chain_map": (
                "forgetting the repeated edge sends the three shared labels "
                "to three distinct unit matching coordinates"
            ),
            "rho_orbit_sizes": sorted(map(len, shared_orbits)),
            "smallest_missing_interface": (
                "two equivariant image choices: one for the rho-fixed shared "
                "label and one for a representative of the shared rho-pair; "
                "these require a diagonal/loop-resolution relative source cell"
            ),
        },
        "frontier": (
            "the desired map is constructed on the only nonzero signed "
            "twelve-label lower packet and lands exactly on the 360-feature "
            "M_v aggregate.  Gate I is reduced to resolving the three shared "
            "labels in two rho orbits"
        ),
        "nonclaims": [
            "no full physical tau on U15 is constructed",
            "the no-go covers one-double-fibre site-collapse maps only",
            "the shared labels are not discarded merely because their signed lower coefficients vanish",
            "no general-Y or inactive-grade extension is claimed",
        ],
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("support-tail/shared-loop ledger changed", digest))
    return ledger, digest


def main():
    ledger, digest = audit()
    print("h3 cut-swap support tail: CONSTRUCTED ON SIGNED 12-LABEL PACKET")
    print("normalized image: B0+B2-B3-B5; literal support=360")
    print("full U15 site-collapse maps: 0")
    print("remaining shared-loop repair: 3 labels / 2 rho orbits")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
