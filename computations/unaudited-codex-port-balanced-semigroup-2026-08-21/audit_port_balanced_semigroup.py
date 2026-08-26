#!/usr/bin/env python3
"""Exact low-degree port-balanced invariant-semigroup screen at N=8.

The calculation is distinct from Hilbert--Mumford support geometry.  It
classifies the semigroup box needed by H0*H1*H2 and the two completed N=8
source-cycle invariants, computes the complete degree-4 and degree-8 Hilbert
basis counts (with B4 x S3 orbit counts), and stops at an exact degree-12
explosion guard before attempting an unusable SAGBI export.
"""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from math import ceil, comb, gcd
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
REES = (ROOT / "computations" /
    "unaudited-codex-ghz-rees-boundary-2026-08-21" /
    "results_ghz_rees_boundary.json")
ONE_HOT_GUARD = ROOT / "computations" / \
    "verify_one_hot_source_cycle_invariant_separator.py"
CYCLE_DUAL_GUARD = ROOT / "computations" / \
    "verify_n8_full_source_cycle_product_membership.py"
PURE_DUAL_GUARD = ROOT / "computations" / \
    "verify_n8_full_source_degree6_exact_dual.py"
OUT = HERE / "results_port_balanced_semigroup.json"
EXPECTED_REES_LOGICAL = \
    "14c9e1df0cab33d75041d5d13ff4acc3544ab873b52c898164f22928aa2e936e"

SITES = tuple(range(8))
COLOURS = tuple(range(3))
EDGES = tuple(combinations(SITES, 2))
PAIRING = ((0, 1), (2, 3), (4, 5), (6, 7))


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def logical_sha(payload):
    return sha256(json.dumps(payload, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def file_sha(path):
    return sha256(path.read_bytes()).hexdigest()


def double_factorial(odd):
    if odd <= 0:
        return 1
    answer = 1
    for value in range(1, odd+1, 2):
        answer *= value
    return answer


@lru_cache(maxsize=None)
def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position, second in enumerate(vertices[1:], 1):
        rest = vertices[1:position]+vertices[position+1:]
        edge = (first, second) if first < second else (second, first)
        for tail in perfect_matchings(rest):
            answer.append(tuple(sorted((edge,)+tail)))
    return tuple(answer)


PHYSICAL_MATCHINGS = perfect_matchings(SITES)
require(len(PHYSICAL_MATCHINGS) == 105, "K8 matching count changed")


def b4_actions():
    actions = set()
    for block_permutation in permutations(range(4)):
        for flips in product((0, 1), repeat=4):
            actions.add(tuple(
                2*block_permutation[site//2]
                + ((site % 2) ^ flips[site//2])
                for site in SITES))
    require(len(actions) == 384, "B4 order changed")
    return tuple(sorted(actions))


B4 = b4_actions()
S3 = tuple(permutations(COLOURS))


def transform_edge(edge, action):
    return tuple(sorted((action[edge[0]], action[edge[1]])))


def transform_matching(matching, action):
    return tuple(sorted(transform_edge(edge, action) for edge in matching))


def orbit_partition(items, transforms):
    remaining = set(items)
    records = []
    while remaining:
        representative = min(remaining)
        orbit = {transform(representative) for transform in transforms}
        require(orbit <= remaining, ("orbit overlap", representative))
        remaining -= orbit
        records.append((representative, len(orbit)))
    return records


def degree4_orbits():
    transforms = tuple(lambda matching, action=action:
                       transform_matching(matching, action)
                       for action in B4)
    return orbit_partition(PHYSICAL_MATCHINGS, transforms)


def cycles(vertices):
    vertices = tuple(sorted(vertices))
    first = vertices[0]
    answer = set()
    for tail in permutations(vertices[1:]):
        order = (first,)+tail
        edges = tuple(sorted(tuple(sorted((order[index],
                                           order[(index+1) % len(order)])))
                             for index in range(len(order))))
        answer.add(edges)
    return tuple(sorted(answer))


def degree8_single_colour_hilbert_elements():
    """2-regular multigraphs with odd components: 3+5 or 3+3+2."""
    elements = set()
    sites = set(SITES)
    for triangle_sites in combinations(SITES, 3):
        rest = tuple(sorted(sites-set(triangle_sites)))
        for left in cycles(triangle_sites):
            for right in cycles(rest):
                elements.add(tuple(sorted(left+right)))
    for doubled_edge in EDGES:
        rest = tuple(sorted(sites-set(doubled_edge)))
        first = rest[0]
        for other_two in combinations(rest[1:], 2):
            triangle = tuple(sorted((first,)+other_two))
            complement = tuple(sorted(set(rest)-set(triangle)))
            left = cycles(triangle)[0]
            right = cycles(complement)[0]
            elements.add(tuple(sorted((doubled_edge, doubled_edge)+left+right)))
    require(len(elements) == 952, ("degree8 single-colour count", len(elements)))
    return tuple(sorted(elements))


def degree8_single_colour_orbits(elements):
    transforms = tuple(
        lambda monomial, action=action: tuple(sorted(
            transform_edge(edge, action) for edge in monomial))
        for action in B4)
    return orbit_partition(elements, transforms)


def port_permutation(site_action, swap_colours):
    return tuple(8*((colour ^ swap_colours)) + site_action[site]
                 for colour in range(2) for site in SITES)


def fixed_allowed_matchings(permutation, same_colour_only):
    """Count invariant perfect matchings on two colour layers exactly."""
    def allowed(left, right):
        left_colour, left_site = divmod(left, 8)
        right_colour, right_site = divmod(right, 8)
        return left_site != right_site and (
            not same_colour_only or left_colour == right_colour)

    @lru_cache(maxsize=None)
    def edge_orbit(left, right):
        edge = tuple(sorted((left, right)))
        orbit = []
        seen = set()
        while edge not in seen:
            seen.add(edge)
            orbit.append(edge)
            edge = tuple(sorted((permutation[edge[0]],
                                 permutation[edge[1]])))
        require(edge == orbit[0], "edge action did not return to seed")
        return tuple(orbit)

    @lru_cache(maxsize=None)
    def count(remaining):
        if not remaining:
            return 1
        left = (remaining & -remaining).bit_length()-1
        answer = 0
        candidates = remaining & ~(1 << left)
        while candidates:
            low = candidates & -candidates
            right = low.bit_length()-1
            candidates -= low
            if not allowed(left, right):
                continue
            orbit = edge_orbit(left, right)
            used = 0
            valid = True
            for u, v in orbit:
                if not allowed(u, v) or (used & ((1 << u) | (1 << v))):
                    valid = False
                    break
                used |= (1 << u) | (1 << v)
            if valid and used & remaining == used:
                answer += count(remaining ^ used)
        return answer

    return count((1 << 16)-1)


def degree8_two_colour_burnside():
    fixed_all = []
    fixed_decomposable = []
    for action in B4:
        for swap in (0, 1):
            permutation = port_permutation(action, swap)
            fixed_all.append(fixed_allowed_matchings(permutation, False))
            fixed_decomposable.append(fixed_allowed_matchings(permutation, True))
    require(fixed_all[0] >= 0, "Burnside ledger empty")
    # The action order is 384*2, the stabilizer of an unordered used-colour
    # pair in B4 x S3.  Subtracting same-colour pairs leaves the connected
    # two-colour (hence indecomposable) Hilbert elements.
    numerator = sum(left-right for left, right
                    in zip(fixed_all, fixed_decomposable))
    require(numerator % 768 == 0, "two-colour Burnside sum not integral")
    return {
        "orbit_count": numerator//768,
        "fixed_sum": numerator,
        "fixed_all_histogram": dict(sorted(Counter(fixed_all).items())),
        "fixed_decomposable_histogram": dict(sorted(
            Counter(fixed_decomposable).items())),
    }


BOUNDARY_CELLS = {
    ((0, 1), 0, 0), ((0, 3), 1, 1), ((0, 7), 2, 2),
    ((1, 4), 2, 2), ((1, 6), 1, 1), ((2, 3), 2, 2),
    ((2, 4), 1, 1), ((2, 5), 0, 0), ((3, 4), 0, 0),
    ((5, 6), 2, 2), ((5, 7), 1, 1), ((6, 7), 0, 0),
}
CELL_BY_EDGE = {edge: (left, right)
                for edge, left, right in BOUNDARY_CELLS}
MIXED_SEEDS = (
    (tuple(map(int, "12012000")),
     ((0, 3), (1, 4), (2, 5), (6, 7))),
    (tuple(map(int, "21000012")),
     ((0, 7), (1, 6), (2, 5), (3, 4))),
)


def canonical_cell(edge, left, right):
    if edge[0] < edge[1]:
        return edge[0], edge[1], left, right
    return edge[1], edge[0], right, left


def transform_monomial(monomial, site_action, colour_action):
    answer = []
    for u, v, left, right in monomial:
        image_u, image_v = site_action[u], site_action[v]
        answer.append(canonical_cell((image_u, image_v),
                                     colour_action[left],
                                     colour_action[right]))
    return tuple(sorted(answer))


def colour_component_shape(matching, word):
    adjacency = {colour: set() for colour in COLOURS}
    for u, v in matching:
        left, right = word[u], word[v]
        if left != right:
            adjacency[left].add(right)
            adjacency[right].add(left)
    seen = set()
    sizes = []
    for colour in COLOURS:
        if colour in seen:
            continue
        stack = [colour]
        seen.add(colour)
        size = 0
        while stack:
            current = stack.pop()
            size += 1
            for neighbour in adjacency[current]:
                if neighbour not in seen:
                    seen.add(neighbour)
                    stack.append(neighbour)
        sizes.append(size)
    return tuple(sorted(sizes, reverse=True))


def completed_cycle_ledger():
    records = []
    monomials = set()
    type_counts = Counter()
    for word, supported_matching in MIXED_SEEDS:
        q_cells = []
        for edge in sorted(set(CELL_BY_EDGE)-set(supported_matching)):
            left, right = CELL_BY_EDGE[edge]
            q_cells.append(canonical_cell(edge, left, right))
        require(len(q_cells) == 8, "completed-cycle complement degree changed")
        local_counts = Counter()
        for matching in PHYSICAL_MATCHINGS:
            h_cells = [canonical_cell(edge, word[edge[0]], word[edge[1]])
                       for edge in matching]
            monomial = tuple(sorted(q_cells+h_cells))
            require(len(monomial) == len(set(monomial)) == 12,
                    ("completed monomial is not squarefree", word, matching))
            shape = colour_component_shape(matching, word)
            local_counts[shape] += 1
            type_counts[shape] += 1
            monomials.add(monomial)
        require(local_counts == {(3,): 72, (2, 1): 30,
                                 (1, 1, 1): 3},
                ("completed-cycle factor census changed", word, local_counts))
        records.append({
            "word": "".join(map(str, word)),
            "H_terms": 105,
            "three_pure_degree4_factors": local_counts[(1, 1, 1)],
            "degree8_mixed_Hilbert_times_pure": local_counts[(2, 1)],
            "primitive_degree12_Hilbert_terms": local_counts[(3,)],
        })
    # The full twelve-edge boundary product occurs once in each completed
    # invariant, so the two 105-term supports overlap in exactly one monomial.
    require(len(monomials) == 209 and type_counts == {
        (3,): 144, (2, 1): 60, (1, 1, 1): 6},
        ("completed union census changed", len(monomials), type_counts))

    actions = tuple((site_action, colour_action)
                    for site_action in B4 for colour_action in S3)
    canonical = {}
    for monomial in monomials:
        representative = min(transform_monomial(monomial, *action)
                             for action in actions)
        canonical[monomial] = representative
    orbit_types = Counter()
    for representative in set(canonical.values()):
        sample = next(monomial for monomial, owner in canonical.items()
                      if owner == representative)
        # Recover the factor type from colour connectivity of the monomial.
        adjacency = {colour: set() for colour in COLOURS}
        for _, _, left, right in sample:
            if left != right:
                adjacency[left].add(right)
                adjacency[right].add(left)
        seen, sizes = set(), []
        for colour in COLOURS:
            if colour in seen:
                continue
            stack, size = [colour], 0
            seen.add(colour)
            while stack:
                current = stack.pop()
                size += 1
                for neighbour in adjacency[current]:
                    if neighbour not in seen:
                        seen.add(neighbour)
                        stack.append(neighbour)
            sizes.append(size)
        orbit_types[tuple(sorted(sizes, reverse=True))] += 1
    return records, type_counts, len(set(canonical.values())), orbit_types


def main():
    rees = json.loads(REES.read_text())
    require(rees["logical_sha256"] == EXPECTED_REES_LOGICAL,
            "GHZ Rees boundary digest changed")
    expected_guards = {
        ONE_HOT_GUARD:
            "5b4a51bae2d66f6d2ed9977d7209e67ecc9e4ae3435b1b37c10b04f15156d441",
        CYCLE_DUAL_GUARD:
            "ee16eca557e04a8b2eedce34e57cfd5a8b9c05acc16813a4ba0925ab5967c834",
        PURE_DUAL_GUARD:
            "48974f1a62bfbf297ce25fc6ffd3aa1bef9925238d9da627b84512925d242251",
    }
    for path, expected in expected_guards.items():
        require(file_sha(path) == expected, ("guard script changed", str(path)))

    d4_orbits = degree4_orbits()
    require(sum(size for _, size in d4_orbits) == 105,
            "degree4 orbit coverage changed")
    d8_single = degree8_single_colour_hilbert_elements()
    d8_single_orbits = degree8_single_colour_orbits(d8_single)
    require(sum(size for _, size in d8_single_orbits) == len(d8_single),
            "degree8 single-colour orbit coverage changed")

    # Exact labelled counts before the more expensive orbit calculation.
    two_colour_all = sum((-1)**chosen*comb(8, chosen)
                         * double_factorial(15-2*chosen)
                         for chosen in range(9))
    two_colour_decomposable = 105**2
    two_colour_hilbert = two_colour_all-two_colour_decomposable
    require((two_colour_all, two_colour_hilbert) == (1190672, 1179647),
            "degree8 two-colour count changed")
    d8_two_burnside = degree8_two_colour_burnside()

    # In the k=(1,1,1) box, monomials are perfect matchings on 24 ports
    # avoiding the three within-site port pairs.  Inclusion-exclusion chooses
    # at most one forbidden edge at each physical site.
    degree12_all = sum((-1)**chosen*comb(8, chosen)*(3**chosen)
                       * double_factorial(23-2*chosen)
                       for chosen in range(9))
    degree12_three_pure = 105**3
    degree12_pair_plus_pure = 3*105*two_colour_hilbert
    degree12_connected_hilbert = (
        degree12_all-degree12_three_pure-degree12_pair_plus_pure)
    require((degree12_all, degree12_connected_hilbert) ==
            (108990418320, 108617671890),
            "degree12 connected count changed")

    completed, completed_types, completed_orbits, completed_orbit_types = \
        completed_cycle_ledger()

    payload = {
        "status": "PASS exact low-degree port-balanced semigroup explosion screen",
        "torus_and_semigroup": {
            "source_variables": 252,
            "port_characters": 24,
            "normalization_relations": 3,
            "effective_torus_rank": 21,
            "semigroup": (
                "S={m in N^252 : deg_(i,c)(m)=k_c independent of site i "
                "for c=0,1,2}."),
            "ordinary_degree_formula": "deg(m)=4*(k_0+k_1+k_2)",
            "invariant_ring": "Q[S]",
        },
        "hilbert_basis_through_degree8": {
            "degree4": {
                "description": "one same-colour perfect matching, k=e_c",
                "labelled_elements": 3*105,
                "B4_times_S3_orbits": len(d4_orbits),
                "orbit_size_histogram_one_colour": dict(sorted(
                    Counter(size for _, size in d4_orbits).items())),
                "one_colour_representatives": [
                    {"matching": [list(edge) for edge in representative],
                     "orbit_size": size}
                    for representative, size in d4_orbits],
            },
            "degree8_k_2_0_0": {
                "description": (
                    "one-colour 2-regular multigraph with an odd cycle; "
                    "component types 3+5 or 3+3+2 (the 2-cycle is doubled)"),
                "labelled_per_used_colour": len(d8_single),
                "labelled_all_colours": 3*len(d8_single),
                "B4_times_S3_orbits": len(d8_single_orbits),
                "orbit_size_histogram_one_colour": dict(sorted(
                    Counter(size for _, size in d8_single_orbits).items())),
            },
            "degree8_k_1_1_0": {
                "description": (
                    "perfect matching on two eight-port colour layers, "
                    "avoiding same-site edges and containing a cross-colour edge"),
                "labelled_per_unordered_colour_pair": two_colour_hilbert,
                "labelled_all_colour_pairs": 3*two_colour_hilbert,
                "B4_times_S3_orbits": d8_two_burnside["orbit_count"],
                "Burnside_fixed_sum": d8_two_burnside["fixed_sum"],
            },
            "complete_through_degree8": True,
        },
        "degree12_explosion_guard": {
            "box": "k=(1,1,1), exactly the box containing H0*H1*H2 and completed cycles",
            "all_labelled_balanced_monomials": degree12_all,
            "decomposable_as_three_pure_matchings": degree12_three_pure,
            "decomposable_as_degree8_mixed_times_pure":
                degree12_pair_plus_pure,
            "connected_colour_graph_Hilbert_elements":
                degree12_connected_hilbert,
            "B4_times_S3_orbit_lower_bound":
                ceil(degree12_connected_hilbert/(384*6)),
            "orbit_enumeration_started": False,
            "stop_reason": (
                "More than 108 billion primitive degree-12 generators and "
                "at least 47 million symmetry orbits occur in the target box, "
                "before any radical or power calculation."),
        },
        "target_and_cycle_factorization": {
            "pure_product": {
                "polynomial": "H0*H1*H2",
                "ordinary_degree": 12,
                "port_degree": [1, 1, 1],
                "monomial_count": 105**3,
                "factorization": (
                    "Every monomial is exactly a product of three degree-4 "
                    "Hilbert generators, one pure matching in each colour."),
            },
            "completed_cycle_invariants": completed,
            "two_invariant_union_term_factor_counts": {
                "three_degree4_pure": completed_types[(1, 1, 1)],
                "degree8_mixed_times_degree4_pure": completed_types[(2, 1)],
                "primitive_degree12": completed_types[(3,)],
            },
            "term_occurrences": 210,
            "distinct_terms": 209,
            "shared_term": "the full twelve-cell boundary product P_G",
            "B4_times_S3_term_orbits": completed_orbits,
            "term_orbits_by_factor_type": {
                "three_degree4_pure": completed_orbit_types[(1, 1, 1)],
                "degree8_mixed_times_degree4_pure":
                    completed_orbit_types[(2, 1)],
                "primitive_degree12": completed_orbit_types[(3,)],
            },
            "one_hot_separator_guard": (
                "Each Q_M*H_word is invariant, equals one on the Laurent "
                "boundary orbit, and vanishes on the exact GHZ fiber."),
        },
        "quotient_membership_verdict": {
            "mixed_ideal": "I_mix=(H_w : w mixed), a torus-stable semi-invariant ideal",
            "invariant_contraction": "J=I_mix intersect Q[S]",
            "lossless_for_invariant_target": (
                "Because the torus is linearly reductive in characteristic "
                "zero, invariant weight projection shows P^r in I_mix iff "
                "P^r in J for invariant P."),
            "exponent_one_guards": [
                "H0*H1*H2 is not in I_mix (exact rational degree-12 dual).",
                "The boundary support product P_G is not in I_mix (exact rational cycle dual)."],
            "smaller_radical_or_target_power_problem_obtained": False,
            "reason": (
                "The quotient is logically lossless but its minimal "
                "degree-12 target box already has 108,617,671,890 primitive "
                "monomials. The two completed cycles cover only 144 of them."),
            "new_power_bound": None,
            "recommended_replacement": (
                "Do not export the Hilbert/SAGBI basis. Work on a localized "
                "twelve-cell boundary chart or search for a small invariant "
                "subalgebra selected by additional source identities/no-cap "
                "minors; any useful quotient needs more than port balance."),
        },
        "pinned_guards": {
            "GHZ_Rees_boundary_logical_sha256": EXPECTED_REES_LOGICAL,
            "one_hot_cycle_separator_script_sha256":
                "5b4a51bae2d66f6d2ed9977d7209e67ecc9e4ae3435b1b37c10b04f15156d441",
            "cycle_product_exponent_one_script_sha256":
                "ee16eca557e04a8b2eedce34e57cfd5a8b9c05acc16813a4ba0925ab5967c834",
            "pure_product_exponent_one_ledger_sha256":
                "1bf53cd05fb701865505054161a50d44730002435c636ef477005ad94e5af941",
        },
    }
    payload["logical_sha256"] = logical_sha(payload)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True)+"\n")
    print(json.dumps({
        "logical_sha256": payload["logical_sha256"],
        "degree4_orbits": len(d4_orbits),
        "degree8_single_colour_orbits": len(d8_single_orbits),
        "degree8_two_colour_orbits": d8_two_burnside["orbit_count"],
        "degree12_connected_Hilbert_elements": degree12_connected_hilbert,
        "completed_cycle_term_orbits": completed_orbits,
        "smaller_power_problem": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
