#!/usr/bin/env python3
"""Audit the cut-swap shadow and its first physical word obstruction.

The complete lower packet for P_024-P_012 has a striking unlabelled
factorization.  The site transposition rho=(1 4) carries the nine collision
labels of cut 012 to those of cut 024, so on the fifteen-label quotient

    lower = (rho-1) u_012.

This does not construct the protected physical comparison.  The selected
mixed word is 001122.  Cut 012 has colour histogram (2,1,0), whereas cut
024 has histogram (1,1,1).  Those histograms cannot be related by a site
permutation together with one global colour permutation preserving the GHZ
target.  In particular rho changes the word in exactly two sites.  Thus the
factorization is an occurrence/collision shadow, not a physical source bar
cell.  Its smallest possible repair has two local colour roots and still
needs a target-cancelling relative Cartan/Spencer attachment.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
from itertools import permutations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_complete_tangent_lower_protected_phi_reduction.py":
        "ea45c09a8347c312ea9721475d54a4b4f9aad21d8d51cb9d4d297aeaa99ba429",
    "computations/verify_h3_tangent_euler_occurrence_splitter_fredholm.py":
        "ba2c32a41b1d070d2af24546819e838697aba0273e85586a796ee25a27f5a950",
    "computations/verify_protected_physical_comparison_first_source_cell.py":
        "0c93a7e67f1f48d114e343a282820477fe5a86649502500c5b00ee5e560b0245",
    "computations/verify_h3_physical_cartan_source_orbit_descent.py":
        "c92667c38c57c69dff18fd7570fa154db7e1a634a83f462dfde6bd5553128a3a",
    "computations/verify_h3_residual_q_literal_mapping_cone_private_boundary_gate.py":
        "b890195a8fc0c4e90c9c9c0c03c41a95690228c81026f4c2ea1fa95908564e38",
    "computations/verify_h3_first_flat_physical_anchor_six_term_separator.py":
        "647124e7c6646727653f7377d015d4f12010f39b8398b048a4ea065eedc73968",
}
EXPECTED_LEDGER_SHA256 = "e12adf64d6bee8595a059f4ad2fb3f5b7af6b6c532a86798d9d9db0f3069ac42"


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


def transport_word(word, site_permutation, colour_permutation):
    answer = [None] * len(word)
    for old_site, colour in enumerate(word):
        answer[site_permutation[old_site]] = colour_permutation[colour]
    return tuple(answer)


def cut_histogram(word, cut):
    return tuple(word[site] for site in cut).count(0), \
        tuple(word[site] for site in cut).count(1), \
        tuple(word[site] for site in cut).count(2)


def audit() -> tuple[dict[str, object], str]:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))

    lower = load(
        "computations/verify_h3_complete_tangent_lower_protected_phi_reduction.py",
        "cut_swap_lower",
    )
    tangent = load(
        "computations/verify_h3_tangent_euler_occurrence_splitter_fredholm.py",
        "cut_swap_tangent",
    )
    literal = load(
        "computations/verify_h3_residual_q_literal_mapping_cone_private_boundary_gate.py",
        "cut_swap_literal",
    )
    anchor = load(
        "computations/verify_h3_first_flat_physical_anchor_six_term_separator.py",
        "cut_swap_anchor",
    )

    base_cut = (0, 1, 2)
    other_cut = (0, 2, 4)
    require(tangent.WORD == (0, 0, 1, 1, 2, 2),
            "the selected determinant word changed")
    require(tangent.CUTS[0] == base_cut and tangent.CUTS[5] == other_cut,
            "the marked cut pair changed")

    base_direction = lower.lower_labels(tangent, base_cut)
    other_direction = lower.lower_labels(tangent, other_cut)
    physical_key = lambda label: (label[1], label[2])
    base = frozenset(map(physical_key, base_direction))
    other = frozenset(map(physical_key, other_direction))
    labels = tuple(sorted(base | other))
    label_index = {label: index for index, label in enumerate(labels)}

    rho = (0, 4, 2, 3, 1, 5)  # literal site transposition (1 4)

    def rho_label(label):
        matching_index, repeated_edge = label
        matching = permute_matching(tangent.MATCHINGS[matching_index], rho)
        return (tangent.MATCHING_INDEX[matching],
                permute_edge(repeated_edge, rho))

    require(frozenset(map(rho_label, base)) == other,
            "rho stopped carrying the 012 collision packet to 024")
    require(frozenset(map(rho_label, labels)) == frozenset(labels),
            "rho stopped acting on the fifteen-label quotient")
    require(all(rho_label(rho_label(label)) == label for label in labels),
            "rho stopped being an involution on collision labels")

    base_vector = tuple(Q(int(label in base)) for label in labels)
    other_vector = tuple(Q(int(label in other)) for label in labels)
    rho_base_vector = [Q(0)] * len(labels)
    for label, value in zip(labels, base_vector, strict=True):
        rho_base_vector[label_index[rho_label(label)]] += value
    collision_lower = tuple(right - left for left, right in
                            zip(base_vector, other_vector, strict=True))
    require(tuple(rho_base_vector) == other_vector
            and tuple(value - base_vector[index]
                      for index, value in enumerate(rho_base_vector))
            == collision_lower,
            "the lower packet lost its (rho-1) factorization")
    require(sum(bool(value) for value in collision_lower) == 12,
            "the rho difference support changed")

    cycles = []
    remaining = set(labels)
    while remaining:
        label = min(remaining)
        image = rho_label(label)
        cycle = (label,) if image == label else (label, image)
        cycles.append(cycle)
        remaining.difference_update(cycle)
    shared = base & other
    shared_cycles = [cycle for cycle in cycles if set(cycle) <= shared]
    require(sorted(map(len, cycles)) == [1] + [2] * 7
            and sorted(map(len, shared_cycles)) == [1, 2],
            "the collision involution orbit census changed")
    moving_lower_cycles = sum(
        any(collision_lower[label_index[label]] for label in cycle)
        for cycle in cycles
    )
    require(moving_lower_cycles == 6,
            "the lower packet stopped using six anti-invariant pairs")

    # A GHZ-monomial relabelling is a site permutation followed by the same
    # colour permutation at every site.  Enumerate the full stabilizer of the
    # selected word, including the unoriented complement of the target cut.
    sites = tuple(range(6))
    colours = (0, 1, 2)
    physical_word_stabilizer = []
    cut_transports = []
    minimum_word_repair = len(tangent.WORD) + 1
    minimum_repair_count = 0
    target_cut_sets = (frozenset(other_cut),
                       frozenset(set(sites) - set(other_cut)))
    for site_permutation in permutations(sites):
        cut_image = frozenset(site_permutation[site] for site in base_cut)
        for colour_permutation in permutations(colours):
            transported = transport_word(
                tangent.WORD, site_permutation, colour_permutation)
            if transported == tangent.WORD:
                physical_word_stabilizer.append(
                    (site_permutation, colour_permutation))
                if cut_image in target_cut_sets:
                    cut_transports.append(
                        (site_permutation, colour_permutation))
            if cut_image in target_cut_sets:
                distance = sum(left != right for left, right in
                               zip(transported, tangent.WORD, strict=True))
                if distance < minimum_word_repair:
                    minimum_word_repair = distance
                    minimum_repair_count = 1
                elif distance == minimum_word_repair:
                    minimum_repair_count += 1
    require(len(physical_word_stabilizer) == 48
            and not cut_transports
            and minimum_word_repair == 2,
            "the physical word-orbit obstruction changed")

    base_histogram = cut_histogram(tangent.WORD, base_cut)
    other_histogram = cut_histogram(tangent.WORD, other_cut)
    require(sorted(base_histogram) == [0, 1, 2]
            and sorted(other_histogram) == [1, 1, 1],
            "the cut colour-histogram obstruction changed")
    rho_word = transport_word(tangent.WORD, rho, colours)
    rho_repair_sites = tuple(index for index, values in
                             enumerate(zip(rho_word, tangent.WORD,
                                           strict=True))
                             if values[0] != values[1])
    require(rho_word == (0, 2, 1, 1, 0, 2)
            and rho_repair_sites == (1, 4),
            "rho stopped requiring the two local colour repairs")

    # Two local 0<->2 repairs do not preserve the GHZ target: the pure-zero
    # target word becomes mixed.  This is precisely why an endpoint-odd or
    # relative target-cancelling Cartan cell is required.
    pure_zero = (0,) * 6
    locally_repaired_pure = list(pure_zero)
    for site in rho_repair_sites:
        locally_repaired_pure[site] = 2
    require(len(set(locally_repaired_pure)) == 2,
            "the local word repair unexpectedly preserved a pure GHZ word")

    literal_ledger, literal_digest = literal.audit()
    require(literal_digest == literal.EXPECTED_LEDGER_SHA256,
            "the literal M_v gate changed")
    mv = literal_ledger["private_pivot_no_go_and_minimal_cell"][
        "smallest_literal_mapping_cone_image"
    ]
    require(mv["D_W_target_ainc"] == [0, 0, 0, 0],
            "the required M_v image acquired anchor incidence")
    anchor_ledger = anchor.audit()
    require(anchor_ledger["pairings"]["known_relative_alpha_cell"] == 0,
            "the known alpha aggregate acquired physical anchor pairing")

    ledger = {
        "theorem": "collision cut-swap shadow and physical word-orbit obstruction",
        "collision_factorization": {
            "cut_pair": [list(base_cut), list(other_cut)],
            "site_shadow": "rho=(1 4)",
            "physical_collision_labels": len(labels),
            "rho_orbit_sizes": sorted(map(len, cycles)),
            "shared_label_orbit_sizes": sorted(map(len, shared_cycles)),
            "nonzero_lower_coefficients": sum(bool(value)
                                               for value in collision_lower),
            "nonzero_anti_invariant_orbits": moving_lower_cycles,
            "identity": "lower=(rho-1)u_012 on the collision-label quotient",
            "overlap_consequence": (
                "one shared label is rho-fixed and the other two form one "
                "rho-pair; a genuinely rho-equivariant cutwise comparison "
                "therefore satisfies all three overlap coherences"
            ),
        },
        "physical_word_obstruction": {
            "word": "001122",
            "cut_012_colour_histogram": list(base_histogram),
            "cut_024_colour_histogram": list(other_histogram),
            "GHZ_monomial_word_stabilizer_order":
                len(physical_word_stabilizer),
            "stabilizer_elements_mapping_the_unoriented_cuts":
                len(cut_transports),
            "minimum_local_word_repairs_after_any_cut_transport":
                minimum_word_repair,
            "number_of_minimal_site_global_colour_transports":
                minimum_repair_count,
            "rho_transported_word": "".join(map(str, rho_word)),
            "rho_local_repair_sites": list(rho_repair_sites),
            "verdict": (
                "rho is only an occurrence/collision shadow.  It does not "
                "define Phi=rho_* in the fixed physical word block, and a "
                "formal group-bar symbol [rho] is not a source cell"
            ),
        },
        "smallest_remaining_source_type": (
            "a source-provenant two-local-root word-change Cartan/Spencer "
            "attachment (or equivalent relative mapping-cone cell) whose "
            "target defect is cancelled, whose six anti-invariant collision "
            "pairs descend coherently, and whose canonical repeated-grade "
            "image is the literal equivariant M_v family"
        ),
        "physical_ainc_law": {
            "collision_word_is_pure": False,
            "required_M_v_ainc": mv["D_W_target_ainc"][3],
            "known_alpha_aggregate_ainc_pairing":
                anchor_ledger["pairings"]["known_relative_alpha_cell"],
            "consequence": (
                "the lower collision packet and the required M_v image are "
                "both anchor-dark by fine word/signature.  Thus ainc=0 is "
                "the separate comparison law on the lower correction, but "
                "this does not prove that the completed top-plus-lower "
                "kernel has nonzero physical pure/target anchor"
            ),
        },
        "sharp_status": (
            "the apparent one-step relabelling construction is excluded.  "
            "The three overlap equations collapse to equivariance, while "
            "the first genuinely physical datum is exactly the two-root "
            "relative word-change/M_v attachment; no such source cell is "
            "constructed here"
        ),
        "pins": PINS,
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("cut-swap word-orbit ledger changed", digest))
    return ledger, digest


def main() -> None:
    ledger, digest = audit()
    collision = ledger["collision_factorization"]
    obstruction = ledger["physical_word_obstruction"]
    print("h3 cut-swap collision/word-orbit obstruction: PASS")
    print("collision shadow:", collision["identity"])
    print("physical relabellings of 012 to 024:",
          obstruction["stabilizer_elements_mapping_the_unoriented_cuts"])
    print("minimum local word repairs:",
          obstruction["minimum_local_word_repairs_after_any_cut_transport"])
    print("remaining: two-root relative word-change / literal M_v cell")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
