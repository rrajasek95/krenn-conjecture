#!/usr/bin/env python3
"""Exact cokernel of site bars and paired Cartan/Weyl prisms.

There are two different modules which must not be conflated.

* In the formal permutation module on individual occurrences, the boundary
  of the group-action graph is the augmentation ideal on every orbit.
* A complete physical source row is the orbit sum in the matching factor.
  Site bars and endpoint-odd Cartan/Weyl prisms made from that row therefore
  remain in the trivial matching representation.  They cannot split a
  proper matching component.

The second statement leaves an explicit cokernel.  For matching occurrences
X, a site-placement orbit A, and a local Weyl orbit B, complete paired prisms
span

    1_X tensor I_A tensor I_B.

Adding every target-preserving complete site bar enlarges this only to

    1_X tensor I_A tensor k[B].

The checker verifies the ranks, the trivial/Segre marginal excess, the
smallest 2x2x2 counterguards, and the complete matching-orbit assertions at
orders six and eight.
"""

from __future__ import annotations

from collections import Counter, deque
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_physical_cartan_source_prism.py":
        "4f23c4645574d619fac4667eba50567435b2f85ff2583b5b3708a565de400cca",
    "computations/verify_uniform_cartan_critical_component_placement_gate.py":
        "68c56c1a9144dd92fa803962697de60b78b58a125191450f1af1abcd1befe2a1",
    "computations/verify_uniform_hybrid_to_pure_cartan_rectangle_cancellation.py":
        "4edfead0410149e871d396fb0d29f232b5e7c73e91f61691a499b96827633244",
    "computations/verify_oo_dark_potential_source_promotion_counterguard.py":
        "76bdd6c8ce19cc466995b235bade9114d7d2779b74bfcd25eea703c2d1de3db2",
}
EXPECTED_LEDGER_SHA256 = (
    "04b066649d09c0412d6aaeb319583288d408592d516791bcc32b7a765563b25a"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def vector(width, entries):
    answer = [Fraction(0) for _ in range(width)]
    for index, coefficient in entries.items():
        answer[index] += Fraction(coefficient)
    return tuple(answer)


def add(*vectors):
    require(vectors, "cannot add an empty vector family")
    return tuple(sum(values, Fraction(0)) for values in zip(*vectors))


def scale(coefficient, values):
    return tuple(Fraction(coefficient) * value for value in values)


def rank(vectors):
    """Exact row rank over Q."""
    basis = {}
    for original in vectors:
        values = [Fraction(value) for value in original]
        for pivot in sorted(basis):
            if values[pivot]:
                coefficient = values[pivot]
                row = basis[pivot]
                values = [left - coefficient * right
                          for left, right in zip(values, row)]
        pivot = next((index for index, value in enumerate(values) if value),
                     None)
        if pivot is None:
            continue
        coefficient = values[pivot]
        basis[pivot] = tuple(value / coefficient for value in values)
    return len(basis)


def index3(x, a, b, a_size, b_size):
    return (x * a_size + a) * b_size + b


def basis3(x, a, b, x_size, a_size, b_size):
    return vector(x_size * a_size * b_size,
                  {index3(x, a, b, a_size, b_size): 1})


def complete_fibre(a, b, x_size, a_size, b_size):
    return add(*(basis3(x, a, b, x_size, a_size, b_size)
                 for x in range(x_size)))


def adjacent_differences(size):
    return tuple((index, index + 1) for index in range(size - 1))


def audit_tensor_cokernel(x_size, a_size, b_size):
    """Rank the complete physical images in k[X] tensor k[A] tensor k[B]."""
    require(min(x_size, a_size, b_size) >= 2,
            "the audit expects three nontrivial factors")
    width = x_size * a_size * b_size

    paired = []
    for a0, a1 in adjacent_differences(a_size):
        for b0, b1 in adjacent_differences(b_size):
            paired.append(add(
                complete_fibre(a1, b1, x_size, a_size, b_size),
                scale(-1, complete_fibre(a1, b0, x_size, a_size, b_size)),
                scale(-1, complete_fibre(a0, b1, x_size, a_size, b_size)),
                complete_fibre(a0, b0, x_size, a_size, b_size),
            ))

    complete_site = []
    for a0, a1 in adjacent_differences(a_size):
        for b in range(b_size):
            complete_site.append(add(
                complete_fibre(a1, b, x_size, a_size, b_size),
                scale(-1, complete_fibre(a0, b, x_size, a_size, b_size)),
            ))

    occurrence_local = []
    for x0, x1 in adjacent_differences(x_size):
        for a in range(a_size):
            for b in range(b_size):
                occurrence_local.append(add(
                    basis3(x1, a, b, x_size, a_size, b_size),
                    scale(-1, basis3(x0, a, b,
                                     x_size, a_size, b_size)),
                ))

    pure_weyl = []
    for x in range(x_size):
        for a in range(a_size):
            for b0, b1 in adjacent_differences(b_size):
                pure_weyl.append(add(
                    basis3(x, a, b1, x_size, a_size, b_size),
                    scale(-1, basis3(x, a, b0,
                                     x_size, a_size, b_size)),
                ))

    paired_rank = rank(paired)
    site_rank = rank(complete_site)
    formal_occurrence_rank = rank(occurrence_local)
    augmented_physical_rank = rank(complete_site + paired)
    formal_without_weyl_rank = rank(
        occurrence_local + complete_site + paired)
    exhaustive_rank = rank(
        occurrence_local + complete_site + paired + pure_weyl)

    require(paired_rank == (a_size - 1) * (b_size - 1),
            "the complete paired-prism rank changed")
    require(site_rank == (a_size - 1) * b_size,
            "the complete site-bar rank changed")
    require(formal_occurrence_rank == (x_size - 1) * a_size * b_size,
            "the occurrence-local bar rank changed")
    require(augmented_physical_rank == site_rank,
            "paired prisms enlarged the already complete site-bar image")
    require(formal_without_weyl_rank
            == (x_size - 1) * a_size * b_size
               + (a_size - 1) * b_size,
            "the formal occurrence/site sum changed")
    require(exhaustive_rank == width - 1,
            "occurrence, site, and pure Weyl bars missed augmentation zero")

    return {
        "shape": [x_size, a_size, b_size],
        "ambient_dimension": width,
        "total_augmentation_kernel_dimension": width - 1,
        "complete_paired_prism_rank": paired_rank,
        "paired_zero_augmentation_cokernel_dimension": (
            width - 1 - paired_rank),
        "paired_matching_cut_dimension": (
            (x_size - 1) * a_size * b_size),
        "paired_segre_excess_dimension": a_size + b_size - 2,
        "complete_site_bar_rank": site_rank,
        "site_plus_paired_rank": augmented_physical_rank,
        "site_plus_paired_zero_augmentation_cokernel_dimension": (
            width - 1 - augmented_physical_rank),
        "site_plus_paired_matching_cut_dimension": (
            (x_size - 1) * a_size * b_size),
        "site_plus_paired_weyl_marginal_dimension": b_size - 1,
        "formal_occurrence_bar_rank": formal_occurrence_rank,
        "formal_without_pure_weyl_rank": formal_without_weyl_rank,
        "formal_without_pure_weyl_cokernel_dimension": b_size - 1,
        "all_three_bar_families_rank": exhaustive_rank,
    }


def audit_smallest_counterguard():
    x_size = a_size = b_size = 2
    physical_site = []
    paired = []
    for b in range(2):
        physical_site.append(add(
            complete_fibre(1, b, 2, 2, 2),
            scale(-1, complete_fibre(0, b, 2, 2, 2)),
        ))
    paired.append(add(physical_site[1], scale(-1, physical_site[0])))

    matching_cut = add(
        basis3(0, 0, 0, 2, 2, 2),
        scale(-1, basis3(1, 0, 0, 2, 2, 2)),
    )
    site_marginal = physical_site[0]
    weyl_marginal = add(
        complete_fibre(0, 0, 2, 2, 2),
        complete_fibre(1, 0, 2, 2, 2),
        scale(-1, complete_fibre(0, 1, 2, 2, 2)),
        scale(-1, complete_fibre(1, 1, 2, 2, 2)),
    )
    trivial = add(*(basis3(x, a, b, 2, 2, 2)
                    for x in range(2)
                    for a in range(2)
                    for b in range(2)))

    require(sum(matching_cut) == 0 and sum(site_marginal) == 0
            and sum(weyl_marginal) == 0,
            "a zero-augmentation counterguard changed")
    require(rank(physical_site + paired + [matching_cut])
            == rank(physical_site + paired) + 1,
            "the matching cut entered the complete physical image")
    require(rank(paired + [site_marginal]) == rank(paired) + 1,
            "the site marginal entered the paired-prism image")
    require(rank(physical_site + paired + [weyl_marginal])
            == rank(physical_site + paired) + 1,
            "the pure Weyl marginal entered the site/prism image")
    require(sum(trivial) == 8,
            "the global trivial class lost its augmentation")

    return {
        "shape": [2, 2, 2],
        "matching_cut_total_augmentation": 0,
        "matching_cut_in_complete_site_plus_prism_image": False,
        "site_marginal_in_paired_prism_image": False,
        "weyl_marginal_in_complete_site_plus_prism_image": False,
        "global_trivial_augmentation": int(sum(trivial)),
    }


def edge(left, right):
    return tuple(sorted((left, right)))


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    left = vertices[0]
    for index in range(1, len(vertices)):
        right = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            yield tuple(sorted((edge(left, right),) + tail))


def swap_site(site, first, second):
    if site == first:
        return second
    if site == second:
        return first
    return site


def swap_matching(matching, first, second):
    return tuple(sorted(
        edge(swap_site(left, first, second),
             swap_site(right, first, second))
        for left, right in matching))


def audit_matching_orbit(size):
    matchings = tuple(perfect_matchings(range(size)))
    lookup = {matching: index for index, matching in enumerate(matchings)}
    generators = tuple((site, site + 1) for site in range(size - 1))
    adjacency = [set() for _ in matchings]
    fixed_actions = 0
    for first, second in generators:
        image = [swap_matching(matching, first, second)
                 for matching in matchings]
        require(Counter(image) == Counter(matchings),
                "a site transposition stopped permuting matchings")
        for index, changed in enumerate(image):
            target = lookup[changed]
            adjacency[index].add(target)
            adjacency[target].add(index)
            if target == index:
                fixed_actions += 1

    seen = {0}
    queue = deque([0])
    tree_edges = 0
    while queue:
        source = queue.popleft()
        for target in adjacency[source]:
            if target in seen:
                continue
            seen.add(target)
            queue.append(target)
            tree_edges += 1
    require(len(seen) == len(matchings),
            "the matching permutation graph stopped being transitive")
    require(tree_edges == len(matchings) - 1,
            "the connected orbit lost its spanning-tree incidence rank")

    # A complete matching row has constant occurrence profile.  Every
    # centered proper-component selector is orthogonal to it.
    component_size = max(1, len(matchings) // 3)
    centered = [len(matchings) if index < component_size else 0
                for index in range(len(matchings))]
    centered = [value - component_size for value in centered]
    require(sum(centered) == 0 and any(centered),
            "the proper component cut did not center")
    complete = [1 for _ in matchings]
    require(sum(left * right for left, right in zip(centered, complete)) == 0,
            "a centered component detector saw the complete row")

    return {
        "order": size,
        "matching_occurrences": len(matchings),
        "adjacent_site_generators": len(generators),
        "fixed_generator_actions": fixed_actions,
        "orbit_components": 1,
        "formal_occurrence_bar_rank": tree_edges,
        "complete_row_occurrence_rank": 1,
        "proper_component_centered_detector_nonzero": True,
        "detector_on_every_constant_occurrence_profile": 0,
    }


def apply_operator(values, permutation):
    answer = [Fraction(0) for _ in values]
    for source, coefficient in enumerate(values):
        answer[permutation[source]] += coefficient
    return tuple(answer)


def audit_complete_prism_profile(x_size):
    """A complete prism is matching-constant; the fixed-word one cancels."""
    a_size = b_size = 2
    width = x_size * a_size * b_size
    site_asymmetric = []
    site_fixed_word = []
    weyl = []
    for x in range(x_size):
        for a in range(2):
            for b in range(2):
                source = index3(x, a, b, 2, 2)
                site_asymmetric.append(index3((x + 1) % x_size,
                                               1 - a, b, 2, 2))
                site_fixed_word.append(index3((x + 1) % x_size,
                                               a, b, 2, 2))
                weyl.append(index3(x, a, 1 - b, 2, 2))
    require(sorted(site_asymmetric) == list(range(width))
            and sorted(site_fixed_word) == list(range(width))
            and sorted(weyl) == list(range(width)),
            "a prism operator stopped being a permutation")

    complete = complete_fibre(0, 0, x_size, 2, 2)
    weyl_difference = add(apply_operator(complete, weyl), scale(-1, complete))
    asymmetric = add(
        weyl_difference,
        scale(-1, apply_operator(weyl_difference, site_asymmetric)),
    )
    fixed_word = add(
        weyl_difference,
        scale(-1, apply_operator(weyl_difference, site_fixed_word)),
    )
    expected = add(
        complete_fibre(0, 1, x_size, 2, 2),
        scale(-1, complete_fibre(0, 0, x_size, 2, 2)),
        scale(-1, complete_fibre(1, 1, x_size, 2, 2)),
        complete_fibre(1, 0, x_size, 2, 2),
    )
    require(asymmetric == expected and any(asymmetric),
            "the asymmetric complete prism lost its word rectangle")
    require(not any(fixed_word),
            "the fixed-word complete prism stopped cancelling")

    for a in range(2):
        for b in range(2):
            fibre = [asymmetric[index3(x, a, b, 2, 2)]
                     for x in range(x_size)]
            require(len(set(fibre)) == 1,
                    "the complete prism acquired a matching-centered part")

    return {
        "matching_occurrences": x_size,
        "asymmetric_word_rectangle_nonzero": True,
        "asymmetric_matching_centered_projection_rank": 0,
        "fixed_word_complete_boundary_rank": 0,
        "corner_coefficients_by_site_weyl_bits": [-1, 1, 1, -1],
    }


def main():
    pin_dependencies()
    ledger = {
        "pins": PINS,
        "matching_orbits": [audit_matching_orbit(size) for size in (6, 8)],
        "tensor_cokernels": [
            audit_tensor_cokernel(x_size, a_size, b_size)
            for x_size, a_size, b_size in ((2, 2, 2), (3, 3, 2), (4, 3, 4))
        ],
        "smallest_counterguard": audit_smallest_counterguard(),
        "complete_prism_profiles": [
            audit_complete_prism_profile(x_size) for x_size in (3, 5)
        ],
        "formal_orbit_theorem": (
            "on every connected occurrence orbit, occurrence-local group "
            "bars span exactly the orbitwise augmentation kernel"
        ),
        "physical_complete_row_theorem": (
            "known complete site bars and paired Cartan/Weyl prisms remain "
            "in the trivial matching representation; paired prisms span "
            "1_X tensor I_A tensor I_B, and all complete site bars enlarge "
            "this only to 1_X tensor I_A tensor k[B]"
        ),
        "zero_augmentation_cokernel": (
            "after all complete site bars, the residual is every matching-"
            "centered component cut plus the pure Weyl marginal; paired "
            "prisms alone additionally leave both Segre marginals"
        ),
        "conditional_splitter": (
            "zero augmentation is the full boundary image only after "
            "occurrence-local site bars and target-preserving pure Weyl "
            "bars are both source-provenant"
        ),
        "proof_frontier": (
            "Cartan placement gives a nonzero projection of a complete "
            "prism, not a component-supported source boundary.  A dark "
            "residual cannot be removed by group averaging unless its "
            "matching-centered and pure-Weyl marginal classes vanish or a "
            "new physical component projector/complement primitive is built"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256:
        require(digest == EXPECTED_LEDGER_SHA256,
                f"ledger digest changed: {digest}")
    print(json.dumps(ledger, indent=2, sort_keys=True))
    print("ledger_sha256", digest)


if __name__ == "__main__":
    main()
