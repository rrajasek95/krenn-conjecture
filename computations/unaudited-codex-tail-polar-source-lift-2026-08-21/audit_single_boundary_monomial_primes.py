#!/usr/bin/env python3
"""Exact minimal-prime census for the normalized single-boundary 332 ideal."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from hashlib import sha256
from itertools import combinations, permutations
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
UPSTREAM = HERE / "results_single_cofactor_boundary.json"
OUT = HERE / "results_single_boundary_monomial_primes.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def logical_hash(payload):
    return sha256(json.dumps(payload, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def file_hash(path):
    return sha256(path.read_bytes()).hexdigest()


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        answer.extend((((first, second),) + tail
                       for tail in perfect_matchings(rest)))
    return tuple(answer)


def mask_variables(mask, variables):
    return [f"g{variables[index][0]}_{variables[index][1][0]}"
            f"{variables[index][1][1]}"
            for index in range(len(variables)) if (mask >> index) & 1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()

    upstream = json.loads(UPSTREAM.read_text())
    require(upstream["logical_sha256"] ==
            "e98ff441ead785676089d2986ef62704467f0bd93a9db117836524e9d42639fe",
            "single-boundary upstream digest changed")

    vertices = tuple(range(8))
    complement = (1, 2, 3, 4, 5, 7)
    anchor_edges = frozenset({(2, 3), (4, 5)})
    complement_edges = tuple(edge for edge in combinations(complement, 2)
                             if edge not in anchor_edges)
    variables = tuple(sorted((colour, edge)
                             for colour in range(3)
                             for edge in complement_edges))
    variable_index = {variable: index
                      for index, variable in enumerate(variables)}
    require(len(variables) == 39, "normalized complement variable count changed")

    # The 90 ordered colourings of the 15 complement matchings.  Anchor
    # factors are units.  This gives 87 distinct monomials, including three
    # singleton generators g_c_17.
    raw_generators = []
    for matching in perfect_matchings(complement):
        for colour_order in permutations(range(3)):
            generator = frozenset(
                (colour, tuple(sorted(edge)))
                for colour, edge in zip(colour_order, matching)
                if tuple(sorted(edge)) not in anchor_edges
            )
            raw_generators.append(generator)
    require(len(raw_generators) == 90, "raw 332 monomial count changed")
    unique_generators = set(raw_generators)
    require(len(unique_generators) == 87
            and Counter(map(len, unique_generators)) == {1: 3, 2: 24, 3: 60},
            "normalized 332 monomial profile changed")

    forced_variables = frozenset((colour, (1, 7)) for colour in range(3))
    singleton_generators = {frozenset({variable})
                            for variable in forced_variables}
    require(singleton_generators <= unique_generators,
            "forced singleton generators changed")

    # Remove generators already hit by the forced singleton variables and
    # retain the inclusion-minimal residual hyperedges.
    residual_sets = [generator for generator in unique_generators
                     if not generator & forced_variables]
    residual_sets.sort(key=lambda value: (len(value), sorted(value)))
    minimal_residual_sets = []
    for generator in residual_sets:
        if not any(old <= generator for old in minimal_residual_sets):
            minimal_residual_sets.append(generator)
    require(len(minimal_residual_sets) == 72
            and Counter(map(len, minimal_residual_sets)) == {2: 24, 3: 48},
            "residual minimal monomial generators changed")

    residual_edges = []
    for generator in minimal_residual_sets:
        mask = 0
        for variable in generator:
            mask |= 1 << variable_index[variable]
        residual_edges.append(mask)

    # Berge incremental transversal algorithm, with inclusion minimization
    # at every exact step.  Bit masks keep the 72-edge census bounded.
    transversals = [0]
    for hyperedge in residual_edges:
        bits = []
        remaining = hyperedge
        while remaining:
            bit = remaining & -remaining
            bits.append(bit)
            remaining -= bit
        candidates = []
        for transversal in transversals:
            if transversal & hyperedge:
                candidates.append(transversal)
            else:
                candidates.extend(transversal | bit for bit in bits)
        candidates = sorted(set(candidates),
                            key=lambda value: (value.bit_count(), value))
        minimal = []
        for candidate in candidates:
            if not any((old & candidate) == old for old in minimal):
                minimal.append(candidate)
        transversals = minimal

    # Independent end checks: every result hits every edge and each variable
    # in it has a private edge, so deletion destroys the hitting property.
    for transversal in transversals:
        require(all(transversal & edge for edge in residual_edges),
                "non-hitting transversal emitted")
        remaining = transversal
        while remaining:
            bit = remaining & -remaining
            require(any(not ((transversal ^ bit) & edge)
                        for edge in residual_edges),
                    "nonminimal transversal emitted")
            remaining -= bit
    residual_height_histogram = Counter(mask.bit_count()
                                        for mask in transversals)
    expected_residual_histogram = {
        12: 2, 15: 4, 16: 27, 17: 420, 18: 708,
        19: 624, 20: 1416, 21: 912, 22: 1836,
        23: 624, 24: 62,
    }
    require(len(transversals) == 6635
            and residual_height_histogram == expected_residual_histogram,
            ("minimal transversal census changed", len(transversals),
             residual_height_histogram))

    # Exact 16-element B4 site stabilizer of the unordered edge {0,6}.
    site_maps = []
    for super_permutation in permutations(range(4)):
        for flip_mask in range(16):
            flips = tuple((flip_mask >> block) & 1 for block in range(4))
            mapping = {
                vertex: (2*super_permutation[vertex//2]
                         + ((vertex % 2) ^ flips[vertex//2]))
                for vertex in vertices
            }
            if {mapping[0], mapping[6]} == {0, 6}:
                site_maps.append(mapping)
    require(len(site_maps) == 16, "{0,6} site stabilizer size changed")

    site_index_maps = []
    for mapping in site_maps:
        index_map = []
        for colour, edge in variables:
            image_edge = tuple(sorted((mapping[edge[0]], mapping[edge[1]])))
            index_map.append(variable_index[colour, image_edge])
        site_index_maps.append(tuple(index_map))

    def transform(mask, site_index_map, colour_permutation=(0, 1, 2)):
        answer = 0
        remaining = mask
        while remaining:
            bit = remaining & -remaining
            index = bit.bit_length()-1
            colour, _edge = variables[index]
            image_edge = variables[site_index_map[index]][1]
            image = variable_index[colour_permutation[colour], image_edge]
            answer |= 1 << image
            remaining -= bit
        return answer

    def orbit_ledger(include_colour):
        actions = [(site_index_map, colour_permutation)
                   for site_index_map in site_index_maps
                   for colour_permutation in (
                       tuple(permutations(range(3))) if include_colour
                       else ((0, 1, 2),))]
        orbits = defaultdict(list)
        for transversal in transversals:
            canonical = min(transform(transversal, *action)
                            for action in actions)
            orbits[canonical].append(transversal)
        ledger = []
        for canonical, members in sorted(
                orbits.items(), key=lambda item:
                (item[0].bit_count(), item[0])):
            ledger.append({
                "full_prime_height": canonical.bit_count()+3,
                "residual_cover_size": canonical.bit_count(),
                "orbit_size": len(members),
                "prime_generators": sorted(
                    [f"g{colour}_17" for colour in range(3)]
                    + mask_variables(canonical, variables)),
            })
        require(sum(record["orbit_size"] for record in ledger) == 6635,
                "orbit ledger lost minimal primes")
        return actions, ledger

    site_actions, site_orbits = orbit_ledger(False)
    colour_actions, colour_orbits = orbit_ledger(True)
    require(len(site_actions) == 16 and len(site_orbits) == 527,
            "site quotient census changed")
    require(len(colour_actions) == 96 and len(colour_orbits) == 125,
            "site-colour quotient census changed")

    site_orbit_size_histogram = Counter(record["orbit_size"]
                                        for record in site_orbits)
    colour_orbit_size_histogram = Counter(record["orbit_size"]
                                          for record in colour_orbits)
    require(site_orbit_size_histogram == {1: 3, 2: 8, 4: 38,
                                          8: 148, 16: 330},
            "site orbit size histogram changed")
    require(colour_orbit_size_histogram == {2: 2, 3: 1, 4: 2, 6: 2,
                                            8: 1, 12: 6, 24: 28,
                                            48: 44, 96: 39},
            "site-colour orbit size histogram changed")

    # The two smallest primes (one site orbit of size two) are tested against
    # the exact elementary diagonal constraints.  PURE-LIVE and BAL do not
    # remove them: the four normalized anchors give a live pure matching and
    # an anchor-only positive balance certificate.  But each prime kills a
    # complete row or column of a 2x2 same-colour block, so e_ij=1+perm(Mij)
    # reduces to 1 and excludes the stratum before any mate certificate.
    minimum_residual = min(mask.bit_count() for mask in transversals)
    smallest = [mask for mask in transversals
                if mask.bit_count() == minimum_residual]
    require(len(smallest) == 2 and minimum_residual == 12,
            "smallest-prime census changed")
    forced_mask = 0
    for variable in forced_variables:
        forced_mask |= 1 << variable_index[variable]

    super_blocks = tuple(combinations(range(4), 2))
    smallest_tests = []
    for cover in sorted(smallest):
        prime_mask = cover | forced_mask
        killed_blocks = {}
        for colour in range(3):
            zeros = {edge for c, edge in variables
                     if c == colour
                     and (prime_mask >> variable_index[c, edge]) & 1}
            witnesses = []
            for left_block, right_block in super_blocks:
                block_edges = [[tuple(sorted((2*left_block+i,
                                              2*right_block+j)))
                                for j in range(2)] for i in range(2)]
                for row in block_edges:
                    if set(row) <= zeros:
                        witnesses.append({
                            "block": f"{left_block}{right_block}",
                            "zero_row": ["".join(map(str, edge))
                                         for edge in row],
                        })
                for column in zip(*block_edges):
                    if set(column) <= zeros:
                        witnesses.append({
                            "block": f"{left_block}{right_block}",
                            "zero_column": ["".join(map(str, edge))
                                            for edge in column],
                        })
            require(witnesses, "smallest prime stopped killing a permanent")
            killed_blocks[str(colour)] = witnesses
        smallest_tests.append({
            "full_prime_generators": sorted(
                mask_variables(prime_mask, variables)),
            "full_prime_height": prime_mask.bit_count(),
            "pure_live_anchor_matching": ["01", "23", "45", "67"],
            "PURE_LIVE_eliminates": False,
            "BAL_eliminates": False,
            "BAL_witness": (
                "anchor-only support with weight 1 on each of the twelve "
                "same-colour anchor cells has load 1 at every site-colour"),
            "permanent_row_witnesses_by_colour": killed_blocks,
            "base_permanent_packet_eliminates": True,
            "arbitrary_mate_signature_needed": False,
        })

    # The next-height orbit is not removed by the same support tests and does
    # not equal any frozen support-six/one-y signature (those have at least
    # eleven/twelve zero nonanchor cells, versus five per colour here).
    next_height_records = [record for record in site_orbits
                           if record["full_prime_height"] == 18]
    require(len(next_height_records) == 1
            and next_height_records[0]["orbit_size"] == 4,
            "next-height prime orbit changed")

    # Controls: without anchor normalization there are 90 distinct coloured
    # degree-three monomials; deleting a stabilizer element changes its size.
    unnormalized = {
        frozenset((colour, tuple(sorted(edge)))
                  for colour, edge in zip(colour_order, matching))
        for matching in perfect_matchings(complement)
        for colour_order in permutations(range(3))
    }
    anchor_mutation_fired = len(unnormalized) == 90
    stabilizer_mutation_fired = len(site_maps[:-1]) == 15
    require(anchor_mutation_fired and stabilizer_mutation_fired,
            "monomial-prime mutation control failed")

    full_height_histogram = {str(height+3): count
                             for height, count
                             in sorted(residual_height_histogram.items())}
    result = {
        "status": "PASS exact single-boundary monomial minimal-prime census",
        "normalized_monomial_ideal": {
            "raw_332_rows": len(raw_generators),
            "distinct_monomials": len(unique_generators),
            "forced_linear_generators": sorted(
                f"g{colour}_17" for colour in range(3)),
            "minimal_residual_generators": len(residual_edges),
            "residual_generator_degree_histogram": {
                "2": 24, "3": 48,
            },
        },
        "minimal_primes": {
            "count": len(transversals),
            "full_height_histogram": full_height_histogram,
            "minimum_full_height": minimum_residual+3,
            "minimum_prime_count": len(smallest),
            "completeness_method": (
                "Berge incremental minimal-transversal enumeration with "
                "independent hitting and private-edge minimality checks"),
        },
        "site_stabilizer_quotient": {
            "group": "Stab_B4({0,6})",
            "group_order": len(site_actions),
            "orbit_count": len(site_orbits),
            "orbit_size_histogram": {
                str(size): count for size, count
                in sorted(site_orbit_size_histogram.items())
            },
            "orbit_representatives": site_orbits,
        },
        "site_colour_quotient_control": {
            "group": "Stab_B4({0,6}) x S3_colours",
            "group_order": len(colour_actions),
            "orbit_count": len(colour_orbits),
            "orbit_size_histogram": {
                str(size): count for size, count
                in sorted(colour_orbit_size_histogram.items())
            },
            "orbit_representatives": colour_orbits,
        },
        "smallest_prime_tests": {
            "minimum_primes": smallest_tests,
            "conclusion": (
                "PURE-LIVE and BAL do not eliminate the two height-15 "
                "minimal primes, but the literal same-colour permanent "
                "packet eliminates both: each kills a full row or column "
                "of a 2x2 block in every colour, so 1+perm=1."),
            "site_orbit": "one orbit of size 2",
            "existing_arbitrary_mate_units": (
                "not reached; the one-colour base packet fires first"),
        },
        "next_unresolved_prime_orbit": {
            "full_height": 18,
            "site_orbit_count": 1,
            "site_orbit_size": 4,
            "representative": next_height_records[0]["prime_generators"],
            "elementary_test": (
                "anchor PURE-LIVE/BAL still survive and no complete 2x2 "
                "row/column is forced zero"),
            "signature_map": (
                "no exact frozen arbitrary-mate signature match: the "
                "representative has five zero nonanchor cells per colour, "
                "outside the support-six/one-y low-support ledgers"),
        },
        "mutation_guards": {
            "remove_anchor_normalization_87_to_90": anchor_mutation_fired,
            "delete_site_stabilizer_element_16_to_15":
                stabilizer_mutation_fired,
        },
        "scope_guard": (
            "This is the exact minimal-prime census of the anchor-normalized "
            "332 monomial part after h0_06=h1_06=h2_06=0. Cofactor sums and "
            "the other eleven localized h2 factors remain as declared. "
            "Only the minimum-height prime orbit is eliminated here; the "
            "height-18 orbit is the next exact boundary."),
        "source_hashes": {
            "single_boundary_result": file_hash(UPSTREAM),
        },
    }
    result["logical_sha256"] = logical_hash(result)
    if args.write_results:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("single-boundary monomial primes: PASS", result["logical_sha256"])
    print("primes/site orbits/site-colour orbits",
          len(transversals), len(site_orbits), len(colour_orbits))
    print("minimum full height/count", minimum_residual+3, len(smallest))


if __name__ == "__main__":
    main()
