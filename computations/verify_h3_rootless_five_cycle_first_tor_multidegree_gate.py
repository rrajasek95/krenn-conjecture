#!/usr/bin/env python3
r"""First Tor multidegree of the specialized five rootless companions.

On the five-cycle specialization of the common-q Euler cokernel, write

    (a,b,c,d,e)=(q12,q23,q34,q45,q15)

and order the five companion monomials as

    (h1,h3,h5,h2,h4)=(bd,ad,ac,ce,be).

They are the edge ideal of an odd C5.  Its five minimal first syzygies have
edge degree three.  Each multidegree is a P3+K2 physical edge set and hence
has one repeated physical site.  The unique next syzygy has degree five.

The checker proves that every literal cofactor/Hasse coefficient in the
committed matching inventory is site-squarefree, so none has a first-Tor
multidegree.  It also checks that the anchor augmentations of all first
syzygies generate only the proper diagonal ideal

    (a-b,b-c,c-d,d-e),

which remains proper after monomial localization.  Thus the first Tor can
move four of the five lambda classes but cannot give a universal primitive
anchor-normalized reduced ridge.  A new relative/source-resolution face is
required; this is not a construction of that face.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_LEDGER_SHA256 = "86f4deda314306751c6ffa0d3727ad0955f931f8dbfde1c1bea80515cc8ded0b"
PINS = {
    "computations/verify_h3_rootless_five_ridge_common_q_euler_cokernel.py":
        "caed56942bf3f74aa2942c7924200d8cfac6190665fe7f53e47bb9ccd36b5e27",
    "computations/verify_h3_direct_free_first_syzygy_multidegree_gate.py":
        "7308d9b55740644affedbda04c8085517bcc2a0881eb5a8c839fc6cdee5547e5",
    "computations/verify_h3_pure_unary_cofactor_incidence_attachment.py":
        "3295183db431e14733eceea645a28113eccd086eebbf256afaa7127cc826b8cd",
    "computations/verify_h3_full_hasse_koszul_cap_totalization.py":
        "51940ce0ac8387b68e7725508db6da1a1c055ea036335bbf19750580c69e13fb",
    "computations/verify_h3_rootless_third_cofactor_bianchi_total_complex_obstruction.py":
        "ebd25f79a6fe8db936fe5601b9220f152c5349dd794bbc4e08b2095f1c1d059f",
    "computations/verify_h3_rootless_component_iii_complete_typed_inventory.py":
        "3e2b5912f58646169547b418bb4975a27635dcd8d548a010eb4c2e265412f465",
}

ODD = (1, 2, 3, 4, 5)
MIDDLE = {1: 1, 2: 2, 3: 1, 4: 1, 5: 2}
CYCLE_EDGES = ((1, 2), (2, 3), (3, 4), (4, 5), (1, 5))
VARIABLES = ("a=q12", "b=q23", "c=q34", "d=q45", "e=q15")
GENERATOR_SITES = (1, 3, 5, 2, 4)
ZERO_MONOMIAL = (0, 0, 0, 0, 0)
FULL_MONOMIAL = (1, 1, 1, 1, 1)

Monomial = tuple[int, int, int, int, int]


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"pinned dependency changed: {relative}")


def monomial(*indices: int) -> Monomial:
    result = [0] * len(VARIABLES)
    for index in indices:
        result[index] += 1
    return tuple(result)  # type: ignore[return-value]


def add_monomials(left: Monomial, right: Monomial) -> Monomial:
    return tuple(a + b for a, b in zip(left, right, strict=True))  # type: ignore[return-value]


def subtract_monomials(left: Monomial, right: Monomial) -> Monomial:
    result = tuple(a - b for a, b in zip(left, right, strict=True))
    require(all(value >= 0 for value in result), ("negative monomial", left, right))
    return result  # type: ignore[return-value]


def lcm(left: Monomial, right: Monomial) -> Monomial:
    return tuple(max(a, b) for a, b in zip(left, right, strict=True))  # type: ignore[return-value]


def divides(left: Monomial, right: Monomial) -> bool:
    return all(a <= b for a, b in zip(left, right, strict=True))


def degree(value: Monomial) -> int:
    return sum(value)


def rank(columns) -> int:
    if not columns:
        return 0
    height = len(columns[0])
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
        if pivot_row == height:
            break
    return pivot_row


def perfect_matchings(vertices):
    vertices = tuple(sorted(vertices))
    if not vertices:
        return ((),)
    first = vertices[0]
    result = []
    for second in vertices[1:]:
        rest = tuple(site for site in vertices if site not in (first, second))
        for tail in perfect_matchings(rest):
            result.append(((first, second),) + tail)
    return tuple(result)


def site_profile(edge_indices) -> tuple[int, ...]:
    profile = {site: 0 for site in ODD}
    for index in edge_indices:
        for site in CYCLE_EDGES[index]:
            profile[site] += 1
    return tuple(profile[site] for site in ODD)


def edge_indices(value: Monomial) -> tuple[int, ...]:
    require(all(exponent in (0, 1) for exponent in value),
            ("non-squarefree cycle monomial", value))
    return tuple(index for index, exponent in enumerate(value) if exponent)


def c5_generators():
    # Cycle order is h1--h3--h5--h2--h4--h1.
    generators = (
        monomial(1, 3),  # h1 = b d
        monomial(0, 3),  # h3 = a d
        monomial(0, 2),  # h5 = a c
        monomial(2, 4),  # h2 = c e
        monomial(1, 4),  # h4 = b e
    )
    expected = (
        (0, 1, 0, 1, 0),
        (1, 0, 0, 1, 0),
        (1, 0, 1, 0, 0),
        (0, 0, 1, 0, 1),
        (0, 1, 0, 0, 1),
    )
    require(generators == expected and len(set(generators)) == 5,
            "specialized h generators changed")
    return generators


def first_tor_resolution(generators):
    syzygies = []
    records = []
    for index in range(5):
        following = (index + 1) % 5
        target = lcm(generators[index], generators[following])
        left_coefficient = subtract_monomials(target, generators[index])
        right_coefficient = subtract_monomials(target, generators[following])
        require(degree(target) == 3
                and degree(left_coefficient) == degree(right_coefficient) == 1,
                ("first Tor degree changed", index, target))
        vector = [None] * 5
        vector[index] = (1, left_coefficient)
        vector[following] = (-1, right_coefficient)

        # Literal polynomial boundary: both terms have the same target.
        require(add_monomials(left_coefficient, generators[index]) == target
                and add_monomials(right_coefficient, generators[following]) == target,
                ("S-pair boundary did not cancel", index))
        profile = site_profile(edge_indices(target))
        require(sorted(profile) == [1, 1, 1, 1, 2],
                ("first Tor lost its repeated-site profile", index, profile))
        syzygies.append({
            "index": index,
            "left": index,
            "right": following,
            "degree": target,
            "left_coefficient": left_coefficient,
            "right_coefficient": right_coefficient,
            "vector": vector,
        })
        records.append({
            "sites": [GENERATOR_SITES[index], GENERATOR_SITES[following]],
            "multidegree": list(target),
            "physical_edges": [list(CYCLE_EDGES[item])
                               for item in edge_indices(target)],
            "site_profile_1_to_5": list(profile),
            "coefficient_on_left": {
                "sign": 1, "monomial": list(left_coefficient),
            },
            "coefficient_on_right": {
                "sign": -1, "monomial": list(right_coefficient),
            },
            "lambda_pairing": {
                str(GENERATOR_SITES[index]): {
                    "sign": -1, "monomial": list(left_coefficient),
                },
                str(GENERATOR_SITES[following]): {
                    "sign": 1, "monomial": list(right_coefficient),
                },
            },
            "w_target_ores": [0, 0, 0],
        })

    # At every pair lcm, the five cubic S-pairs span the entire first
    # syzygy kernel.  The five nonadjacent Taylor pairs are reducible.
    pair_records = []
    for left, right in combinations(range(5), 2):
        target = lcm(generators[left], generators[right])
        active_generators = [index for index, value in enumerate(generators)
                             if divides(value, target)]
        active_syzygies = [item for item in syzygies
                           if divides(item["degree"], target)]
        columns = []
        for item in active_syzygies:
            column = [0] * len(active_generators)
            for generator_index, component in enumerate(item["vector"]):
                if component is None:
                    continue
                sign, coefficient = component
                require(add_monomials(
                    subtract_monomials(target, item["degree"]),
                    coefficient,
                ) == subtract_monomials(target, generators[generator_index]),
                        "lifted S-pair coefficient mismatch")
                column[active_generators.index(generator_index)] = sign
            columns.append(column)
        kernel_dimension = len(active_generators) - 1
        require(rank(columns) == kernel_dimension,
                ("minimal cubics failed to span pair-lcm kernel",
                 left, right, target, active_generators))
        adjacent = (right == left + 1) or (left == 0 and right == 4)
        require((degree(target) == 3) == adjacent,
                ("pair adjacency/degree mismatch", left, right, target))
        pair_records.append({
            "pair": [GENERATOR_SITES[left], GENERATOR_SITES[right]],
            "target_degree": degree(target),
            "active_generators": len(active_generators),
            "spanning_cubic_syzygies": len(active_syzygies),
            "minimal": adjacent,
        })

    # The unique relation among the five cubic syzygies appears first in
    # total degree abcde.  Its multiplier on s_i is FULL/deg(s_i).
    second_coefficients = [subtract_monomials(FULL_MONOMIAL, item["degree"])
                           for item in syzygies]
    module_sum: list[dict[Monomial, int]] = [dict() for _ in range(5)]
    for item, multiplier in zip(syzygies, second_coefficients, strict=True):
        for generator_index, component in enumerate(item["vector"]):
            if component is None:
                continue
            sign, coefficient = component
            term = add_monomials(multiplier, coefficient)
            module_sum[generator_index][term] = (
                module_sum[generator_index].get(term, 0) + sign
            )
    require(all(all(value == 0 for value in component.values())
                for component in module_sum),
            "degree-five second syzygy failed")

    possible_targets = set()
    for size in range(1, 6):
        for subset in combinations(range(5), size):
            target = ZERO_MONOMIAL
            for index in subset:
                target = lcm(target, syzygies[index]["degree"])
            possible_targets.add(target)
    second_betti = []
    for target in sorted(possible_targets, key=lambda value: (degree(value), value)):
        active = [item for item in syzygies if divides(item["degree"], target)]
        columns = []
        active_generators = [index for index, value in enumerate(generators)
                             if divides(value, target)]
        for item in active:
            column = [0] * len(active_generators)
            for generator_index, component in enumerate(item["vector"]):
                if component is None:
                    continue
                sign, _coefficient = component
                column[active_generators.index(generator_index)] = sign
            columns.append(column)
        kernel = len(columns) - rank(columns)
        if kernel:
            second_betti.append((target, kernel))
    require(second_betti == [(FULL_MONOMIAL, 1)],
            ("second Tor census changed", second_betti))

    return syzygies, {
        "generator_order": list(GENERATOR_SITES),
        "minimal_first_syzygies": records,
        "pair_lcm_census": pair_records,
        "first_Betti": {"edge_degree_3": 5},
        "unique_second_syzygy": {
            "multidegree": list(FULL_MONOMIAL),
            "edge_degree": 5,
            "multipliers": [list(value) for value in second_coefficients],
        },
        "minimal_resolution_degrees_for_I": "5 at degree2, 5 at degree3, 1 at degree5",
    }


def augmentation_and_diagonal_guard(syzygies, generators):
    # Sum of the two coefficients of each oriented S-pair.  These are the
    # five differences a-b, c-d, e-a, b-c, d-e in the chosen cycle order.
    augmentation_columns = []
    for item in syzygies:
        column = [0] * 5
        left_index = next(index for index, value in enumerate(item["left_coefficient"])
                          if value)
        right_index = next(index for index, value in enumerate(item["right_coefficient"])
                           if value)
        column[left_index] += 1
        column[right_index] -= 1
        augmentation_columns.append(column)
    require(rank(augmentation_columns) == 4,
            "first-syzygy augmentation ideal lost diagonal rank four")
    require(all(sum(column) == 0 for column in augmentation_columns),
            "an augmentation difference stopped vanishing on the diagonal")

    # On the valid torus point a=b=c=d=e=1 all h_v=1.  The projected ridge
    # relations are an oriented C5 incidence matrix, hence have rank four;
    # the all-ones covector remains.  Companion cancellation requires the
    # sum of formal-tail weights to be zero, while anchor incidence -1
    # requires that sum to be one.
    diagonal_ridge_columns = []
    for item in syzygies:
        column = [0] * 5
        column[item["left"]] = -1
        column[item["right"]] = 1
        diagonal_ridge_columns.append(column)
    require(rank(diagonal_ridge_columns) == 4,
            "diagonal first-Tor ridge rank changed")
    require(all(sum(column) == 0 for column in diagonal_ridge_columns),
            "diagonal aggregate stopped detecting first Tor")
    require(all(sum(generator) == 2 for generator in generators),
            "diagonal companion value stopped being one monomial")

    return {
        "first_syzygy_augmentation_rank": 4,
        "augmentation_ideal": "(a-b,b-c,c-d,d-e) in Q[a,b,c,d,e]",
        "proper_after_monomial_localization": True,
        "torus_guard_point": [1, 1, 1, 1, 1],
        "h_values_at_guard": [1, 1, 1, 1, 1],
        "ridge_relation_rank_at_guard": 4,
        "surviving_covector": "sum_v lambda_v",
        "anchor_response_conflict": (
            "response zero requires sum gamma_v=0; anchor incidence -1 "
            "requires sum gamma_v=1"
        ),
    }


def literal_inventory_gate(syzygies):
    # Every nonzero coefficient of a hafnian or one of its literal Hasse
    # derivatives is a matching or a submatching.  Enumerate the complete
    # eight-site inventory; all physical site degrees are <=1.
    subset_checks = 0
    for matching in perfect_matchings(range(8)):
        require(len(matching) == 4, "eight-site matching size changed")
        for mask in range(1 << len(matching)):
            selected = [matching[index] for index in range(len(matching))
                        if mask & (1 << index)]
            profile = [0] * 8
            for left, right in selected:
                profile[left] += 1
                profile[right] += 1
            require(max(profile, default=0) <= 1,
                    "literal Hasse coefficient repeated a physical site")
            subset_checks += 1
    require(subset_checks == 105 * 16,
            "complete eight-site Hasse subset census changed")

    first_profiles = [site_profile(edge_indices(item["degree"]))
                      for item in syzygies]
    require(all(max(profile) == 2 for profile in first_profiles),
            "first Tor acquired a matching profile")

    # The selected unary third cofactor uses three pairwise-disjoint edges
    # on six residual sites; the full Hasse top uses four on eight sites.
    six_site_matchings = perfect_matchings(range(6))
    require(len(six_site_matchings) == 15
            and all(len(set(site for edge_pair in matching for site in edge_pair)) == 6
                    for matching in six_site_matchings),
            "unary third-cofactor matching census changed")

    return {
        "complete_eight_site_Hasse_subsets_checked": subset_checks,
        "literal_cofactor_site_bound": "every physical site degree is at most 1",
        "first_Tor_physical_type": "P3+K2 on five sites",
        "first_Tor_site_profiles": [list(profile) for profile in first_profiles],
        "unary_third_cofactor_type": "3K2 on six sites",
        "full_Hasse_top_type": "4K2 on eight sites",
        "inventory_match_count": 0,
    }


def main() -> None:
    pin_dependencies()
    generators = c5_generators()
    syzygies, resolution = first_tor_resolution(generators)
    augmentation = augmentation_and_diagonal_guard(syzygies, generators)
    inventory = literal_inventory_gate(syzygies)
    ledger = {
        "pins": PINS,
        "cycle_variables": list(VARIABLES),
        "specialized_companions": {
            str(site): list(value)
            for site, value in zip(GENERATOR_SITES, generators, strict=True)
        },
        "resolution": resolution,
        "augmentation_guard": augmentation,
        "literal_inventory": inventory,
        "first_lambda_visible_degree": {
            "homological_degree": 1,
            "internal_edge_degree": 3,
            "fine_site_profile": "one selected-colour site doubled; four single",
            "readouts_of_response_canceling_S_pair": [0, 0, 0],
        },
        "verdict": (
            "the first lambda-visible Tor consists of five degree-three "
            "P3+K2 S-pairs, but no existing literal cofactor/Hasse "
            "coefficient has their repeated-site fine degree and their "
            "augmentation ideal cannot contain the anchor unit"
        ),
        "minimal_new_generator": (
            "a source-labelled relative comparison in one of the five "
            "degree-three P3+K2 fine degrees, with a primitive -1 pure-anchor "
            "face, zero w/target/ordinary-residue, and compatible degree-five "
            "odd-cycle second face"
        ),
    }
    digest = sha256(
        json.dumps(ledger, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    require(EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED", ("pin ledger digest", digest))
    require(digest == EXPECTED_LEDGER_SHA256, ("ledger digest changed", digest))
    print("h=3 rootless five-cycle first-Tor multidegree gate: PASS")
    print("minimal resolution degrees for I: 5@2, 5@3, 1@5")
    print("first Tor: five P3+K2 degrees with one doubled physical site")
    print("literal cofactor/Hasse inventory hits: 0")
    print("diagonal torus guard leaves one primitive lambda aggregate")
    print("ledger sha256:", digest)


if __name__ == "__main__":
    main()
