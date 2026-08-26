#!/usr/bin/env python3
"""Exact quotient-rank and pure-matching-skeleton audit at N=8.

This lane is deliberately independent of the blocker-compressor code.  It
reconstructs the endpoint-ordered response maps from the raw source blocks,
projects the literal X4 slice identities to C*/W_C, and then extracts the
support consequence of the top quotient stratum.

The support consequence is globalized by an exhaustive S8 x S3 orbit census
of the 105^3 choices of one live perfect matching in each pure colour.
"""

from __future__ import annotations

from array import array
from collections import Counter, deque
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import sys


sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SITES = tuple(range(8))
COLORS = tuple(range(3))
EDGES = tuple(combinations(SITES, 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
W40_PATH = ROOT / "computations/unaudited-x4general-w40-2026-08-20/results_t3.json"
W25_PATH = (ROOT / "computations/unaudited-x3core-w25-2026-08-15"
            / "OBJECT_W25-F8_n8_allblocked_X3.json")
PINS = {
    W40_PATH: "30ad242d62b5cb905858842ce4e8255b105862dc21a65c73c080557fa8c1617f",
    W25_PATH: "46d6e207e392deaa7e0bfc4221c7f5cc6735f11a2a14cc388292ca6850dd33f6",
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


@lru_cache(maxsize=None)
def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position, second in enumerate(vertices[1:]):
        remaining = vertices[1:position + 1] + vertices[position + 2:]
        edge = (min(first, second), max(first, second))
        for tail in perfect_matchings(remaining):
            answer.append((edge,) + tail)
    return tuple(answer)


MATCHINGS = tuple(tuple(sorted(matching)) for matching in perfect_matchings(SITES))
MATCHING_INDEX = {matching: index for index, matching in enumerate(MATCHINGS)}
require(len(MATCHINGS) == 105 and len(MATCHING_INDEX) == 105,
        "perfect-matching census")


def parse_source(payload):
    source = {}
    for key, matrix in payload.items():
        u, v = (int(piece.strip())
                for piece in key.strip().strip("()").split(","))
        require(u < v, key)
        source[u, v] = tuple(tuple(Fraction(str(value)) for value in row)
                                   for row in matrix)
    require(set(source) == set(EDGES), "source block set")
    return source


def load_sources():
    for path, expected in PINS.items():
        require(digest(path) == expected, (path, "digest changed"))
    w40 = json.loads(W40_PATH.read_text())["engine_audit"]["witness_B_integral"]["source"]
    w25 = json.loads(W25_PATH.read_text())["blocks"]
    return parse_source(w40), parse_source(w25)


def cell(source, u, v, a, b):
    if u < v:
        return source[u, v][a][b]
    return source[v, u][b][a]


def hafnian(source, word, vertices):
    value = Fraction(0)
    for matching in perfect_matchings(tuple(vertices)):
        term = Fraction(1)
        for u, v in matching:
            term *= cell(source, u, v, word[u], word[v])
            if not term:
                break
        value += term
    return value


def rref(rows, width=9):
    matrix = [list(map(Fraction, row)) for row in rows if any(row)]
    pivots = []
    pivot_row = 0
    for column in range(width):
        pivot = next((row for row in range(pivot_row, len(matrix))
                      if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scale = matrix[pivot_row][column]
        matrix[pivot_row] = [value / scale for value in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            scale = matrix[row][column]
            matrix[row] = [value - scale * pivot_value
                           for value, pivot_value
                           in zip(matrix[row], matrix[pivot_row])]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return tuple(tuple(row) for row in matrix[:pivot_row]), tuple(pivots)


def nullspace(rows, width=9):
    reduced, pivots = rref(rows, width)
    basis = []
    for free in (column for column in range(width) if column not in pivots):
        vector = [Fraction(0)] * width
        vector[free] = 1
        for row, pivot in zip(reversed(reduced), reversed(pivots)):
            vector[pivot] = -sum(row[column] * vector[column]
                                 for column in range(width) if column != pivot)
        basis.append(tuple(vector))
    return tuple(basis)


def dot(left, right):
    return sum((x * y for x, y in zip(left, right)), Fraction(0))


def restrict(row, quotient_basis):
    return tuple(dot(row, vector) for vector in quotient_basis)


def response_block(source, p, q, a, b):
    """Nine output rows of the atomic map rho_ab:C -> F^9."""
    rows = []
    for alpha, beta in product(COLORS, repeat=2):
        row = []
        for i, j in product(COLORS, repeat=2):
            row.append(
                cell(source, p, a, i, alpha) * cell(source, q, b, j, beta)
                + cell(source, p, b, i, beta) * cell(source, q, a, j, alpha)
            )
        rows.append(tuple(row))
    return tuple(rows)


def activity_rows(source, p, q):
    answer = []
    for color in COLORS:
        row = [Fraction(0)] * 9
        row[3 * color + color] = 1
        answer.append(tuple(row))
    answer.append(tuple(cell(source, p, q, i, j)
                        for i, j in product(COLORS, repeat=2)))
    return tuple(answer)


def carrier_forbidden(residual, kind, label):
    residual_edges = tuple(combinations(residual, 2))
    if kind == "star":
        allowed = {edge for edge in residual_edges if label in edge}
    else:
        allowed = set(combinations(label, 2))
    return tuple(edge for edge in residual_edges if edge not in allowed), allowed


def residual_words():
    return tuple(values for values in product(COLORS, repeat=6)
                 if max(values.count(color) for color in COLORS) >= 4)


RESIDUAL_WORDS = residual_words()
require(len(RESIDUAL_WORDS) == 219, "X4 residual packet census")


def projected_carrier(source, p, q, kind, label):
    residual = tuple(site for site in SITES if site not in (p, q))
    atomic = {edge: response_block(source, p, q, *edge)
              for edge in combinations(residual, 2)}
    forbidden, allowed = carrier_forbidden(residual, kind, label)
    rowspace, _ = rref([row for edge in forbidden for row in atomic[edge]])
    quotient_basis = nullspace(rowspace)
    activities = activity_rows(source, p, q)
    restricted = tuple(restrict(row, quotient_basis) for row in activities)
    blocked = tuple(not any(row) for row in restricted)
    active = not any(blocked)

    # Independently project all 219 literal source identities.  Quotient
    # coordinates are restrictions to ann(W_C), hence every forbidden row
    # disappears without choosing a pivot chart.
    defects = 0
    pure_checks = 0
    for values in RESIDUAL_WORDS:
        word = [None] * 8
        for site, color in zip(residual, values):
            word[site] = color
        target = [Fraction(0)] * 9
        if len(set(values)) == 1:
            target[3 * values[0] + values[0]] = 1
            pure_checks += 1
        h6 = hafnian(source, word, residual)
        rhs = [h6 * value for value in activities[3]]
        for a, b in allowed:
            rest = tuple(site for site in residual if site not in (a, b))
            h4 = hafnian(source, word, rest)
            row = atomic[a, b][3 * word[a] + word[b]]
            rhs = [x + h4 * y for x, y in zip(rhs, row)]
        defect = restrict(tuple(x - y for x, y in zip(target, rhs)),
                          quotient_basis)
        defects += any(defect)
    require(pure_checks == 3, "pure projected packet census")
    return {
        "rank": len(rowspace),
        "quotient_dimension": len(quotient_basis),
        "blocked": blocked,
        "active": active,
        "projected_slice_defects": defects,
    }


def carrier_census(source):
    records = []
    for p, q in EDGES:
        residual = tuple(site for site in SITES if site not in (p, q))
        for center in residual:
            records.append(("star", (p, q), (center,),
                            projected_carrier(source, p, q, "star", center)))
        for triangle in combinations(residual, 3):
            records.append(("triangle", (p, q), triangle,
                            projected_carrier(source, p, q, "triangle", triangle)))
    require(len(records) == 728, "carrier census")
    return records


def quotient_profile(records):
    profile = {}
    for kind in ("star", "triangle"):
        chosen = [record for record in records if record[0] == kind]
        profile[kind] = {
            "dimension_histogram": dict(sorted(Counter(
                record[3]["quotient_dimension"] for record in chosen).items())),
            "blocked_dimension_histogram": dict(sorted(Counter(
                record[3]["quotient_dimension"] for record in chosen
                if not record[3]["active"]).items())),
            "active_dimension_histogram": dict(sorted(Counter(
                record[3]["quotient_dimension"] for record in chosen
                if record[3]["active"]).items())),
            "projected_slice_defects": sum(
                record[3]["projected_slice_defects"] for record in chosen),
        }
    return profile


def pure_live_matchings(source):
    answer = []
    for color in COLORS:
        live = tuple(matching for matching in MATCHINGS
                     if all(cell(source, u, v, color, color)
                            for u, v in matching))
        require(live, ("pure liveness", color))
        answer.append(live)
    return tuple(answer)


def permute_matching(matching, permutation):
    return tuple(sorted((min(permutation[u], permutation[v]),
                         max(permutation[u], permutation[v]))
                        for u, v in matching))


def matching_generator_maps():
    maps = []
    for pivot in range(7):
        permutation = list(SITES)
        permutation[pivot], permutation[pivot + 1] = (
            permutation[pivot + 1], permutation[pivot])
        maps.append(tuple(MATCHING_INDEX[permute_matching(matching, permutation)]
                          for matching in MATCHINGS))
    return tuple(maps)


MATCHING_GENERATORS = matching_generator_maps()
STATE_BASE = 105
STATE_COUNT = STATE_BASE ** 3


def encode_state(a, b, c):
    return (a * STATE_BASE + b) * STATE_BASE + c


def decode_state(state):
    ab, c = divmod(state, STATE_BASE)
    a, b = divmod(ab, STATE_BASE)
    return a, b, c


def matching_triple_orbits():
    """BFS the full labelled set under generators of S8 x S3."""
    orbit_of = array("B", [255]) * STATE_COUNT
    records = []
    for seed in range(STATE_COUNT):
        if orbit_of[seed] != 255:
            continue
        orbit_index = len(records)
        queue = deque([seed])
        orbit_of[seed] = orbit_index
        size = 0
        representative = seed
        while queue:
            state = queue.popleft()
            size += 1
            representative = min(representative, state)
            a, b, c = decode_state(state)
            neighbours = [encode_state(mapping[a], mapping[b], mapping[c])
                          for mapping in MATCHING_GENERATORS]
            neighbours.extend((encode_state(b, a, c), encode_state(a, c, b)))
            for neighbour in neighbours:
                if orbit_of[neighbour] == 255:
                    orbit_of[neighbour] = orbit_index
                    queue.append(neighbour)
                else:
                    require(orbit_of[neighbour] == orbit_index,
                            "group orbit collision")
        records.append({"representative_state": representative,
                        "orbit_size": size})
    require(len(records) == 31, ("matching triple orbit count", len(records)))
    require(sum(record["orbit_size"] for record in records) == 105 ** 3,
            "matching triple orbit coverage")
    return records, orbit_of


def graph_mask(edges):
    mask = 0
    for edge in edges:
        mask |= 1 << EDGE_INDEX[edge]
    return mask


def has_edge(mask, u, v):
    return bool(mask & (1 << EDGE_INDEX[min(u, v), max(u, v)]))


def response_site_edges(mask, p, q):
    residual = tuple(site for site in SITES if site not in (p, q))
    answer = []
    for a, b in combinations(residual, 2):
        if ((has_edge(mask, p, a) and has_edge(mask, q, b))
                or (has_edge(mask, p, b) and has_edge(mask, q, a))):
            answer.append((a, b))
    return tuple(answer)


def matching_number_at_least_two(edges):
    return any(set(left).isdisjoint(right)
               for left, right in combinations(edges, 2))


def intersecting_graph_classification():
    """Exhaust all residual graphs: matching number <=1 iff star/triangle."""
    vertices = tuple(range(6))
    edges = tuple(combinations(vertices, 2))
    intersecting = 0
    star_contained = 0
    triangle_only = 0
    for mask in range(1 << len(edges)):
        support = tuple(edge for index, edge in enumerate(edges)
                        if mask & (1 << index))
        low_matching = not matching_number_at_least_two(support)
        in_star = any(all(center in edge for edge in support)
                      for center in vertices)
        in_triangle = any(all(set(edge).issubset(triangle) for edge in support)
                          for triangle in combinations(vertices, 3))
        require(low_matching == (in_star or in_triangle),
                ("intersecting graph classification", support))
        if low_matching:
            intersecting += 1
        if in_star:
            star_contained += 1
        if in_triangle and not in_star:
            triangle_only += 1
    require(triangle_only > 0,
            "star-only mutation incorrectly covered every intersecting graph")
    return {
        "graphs_checked": 1 << len(edges),
        "matching_number_at_most_one": intersecting,
        "star_contained": star_contained,
        "triangle_but_not_star": triangle_only,
    }


def arm_property(mask, selected_edges):
    return all(matching_number_at_least_two(response_site_edges(mask, *edge))
               for edge in selected_edges)


def degrees(mask):
    return tuple(sum(has_edge(mask, site, other)
                     for other in SITES if other != site)
                 for site in SITES)


def minimum_augmentation(initial_mask, selected_edges):
    """Exact monotone search for the fewest added physical pairs."""
    if arm_property(initial_mask, selected_edges):
        return 0, initial_mask, 1
    missing = tuple(index for index in range(28)
                    if not initial_mask & (1 << index))
    deficit = sum(max(0, 3 - degree) for degree in degrees(initial_mask))
    lower = (deficit + 1) // 2
    tested = 0
    for count in range(lower, len(missing) + 1):
        for addition in combinations(missing, count):
            tested += 1
            mask = initial_mask
            for index in addition:
                mask |= 1 << index
            if arm_property(mask, selected_edges):
                return count, mask, tested
    raise RuntimeError("complete graph failed the arm property")


def skeleton_records(orbit_records):
    answer = []
    for index, record in enumerate(orbit_records):
        triple_indices = decode_state(record["representative_state"])
        triple = tuple(MATCHINGS[value] for value in triple_indices)
        selected = tuple(sorted(set(edge for matching in triple for edge in matching)))
        initial = graph_mask(selected)
        additional, witness, tested = minimum_augmentation(initial, selected)
        answer.append({
            "orbit": index,
            "orbit_size": record["orbit_size"],
            "representative": [[list(edge) for edge in matching] for matching in triple],
            "selected_physical_pairs": len(selected),
            "edge_multiplicity_histogram": dict(sorted(Counter(
                sum(edge in matching for matching in triple) for edge in selected
            ).items())),
            "minimum_additional_physical_pairs": additional,
            "minimum_total_physical_pairs": len(selected) + additional,
            "augmentation_witness": [list(EDGES[edge_index])
                                     for edge_index in range(28)
                                     if (witness & (1 << edge_index))
                                     and not (initial & (1 << edge_index))],
            "augmentation_candidates_tested": tested,
        })
    return answer


def source_physical_mask(source):
    return graph_mask(edge for edge in EDGES
                      if any(cell(source, *edge, a, b)
                             for a, b in product(COLORS, repeat=2)))


def source_skeleton_calibration(source, orbit_of):
    lives = pure_live_matchings(source)
    rows = []
    physical = source_physical_mask(source)
    for triple in product(*lives):
        state = encode_state(*(MATCHING_INDEX[matching] for matching in triple))
        selected = tuple(sorted(set(edge for matching in triple for edge in matching)))
        rows.append({
            "orbit": int(orbit_of[state]),
            "selected_pairs": len(selected),
            "physical_pairs": sum(bool(physical & (1 << index)) for index in range(28)),
            "arm_property": arm_property(physical, selected),
        })
    return {
        "live_matching_counts": [len(items) for items in lives],
        "triple_count": len(rows),
        "orbit_histogram": dict(sorted(Counter(row["orbit"] for row in rows).items())),
        "all_arm_property": all(row["arm_property"] for row in rows),
        "first_rows": rows[:20],
    }


def mutation_control(records):
    """Deleting one necessary arm edge must break the witness property."""
    candidates = []
    for record in records:
        triple = tuple(tuple(tuple(edge) for edge in matching)
                       for matching in record["representative"])
        selected = tuple(sorted(set(edge for matching in triple for edge in matching)))
        initial = graph_mask(selected)
        witness = initial | graph_mask(tuple(tuple(edge)
                                            for edge in record["augmentation_witness"]))
        require(arm_property(witness, selected), (record["orbit"], "bad witness"))
        for added in record["augmentation_witness"]:
            edge = tuple(added)
            mutant = witness & ~(1 << EDGE_INDEX[edge])
            if not arm_property(mutant, selected):
                candidates.append((record["orbit"], edge))
                break
    require(candidates, "augmentation deletion mutation did not fire")
    return candidates


def main():
    w40, w25 = load_sources()
    carrier_results = {}
    records_by_source = {}
    for name, source in (("W40", w40), ("W25-F8", w25)):
        records = carrier_census(source)
        records_by_source[name] = records
        carrier_results[name] = quotient_profile(records)

    require(sum(record[3]["active"] for record in records_by_source["W40"]) == 6,
            "W40 active carrier count")
    require(sum(record[3]["active"] for record in records_by_source["W25-F8"]) == 0,
            "W25 all-blocked control")
    require(not any(record[3]["projected_slice_defects"]
                    for record in records_by_source["W40"]),
            "W40 projected X4 identities")
    require(any(record[3]["projected_slice_defects"]
                for record in records_by_source["W25-F8"]),
            "W25 failed-X4 control")

    blocked_w40_dimensions = sorted(set(
        record[3]["quotient_dimension"] for record in records_by_source["W40"]
        if not record[3]["active"]))
    require(blocked_w40_dimensions == list(range(8)), blocked_w40_dimensions)

    orbit_records, orbit_of = matching_triple_orbits()
    skeletons = skeleton_records(orbit_records)
    mutation_fires = mutation_control(skeletons)
    intersecting_control = intersecting_graph_classification()
    calibrations = {
        "W40": source_skeleton_calibration(w40, orbit_of),
        "W25-F8": source_skeleton_calibration(w25, orbit_of),
    }
    require(calibrations["W40"]["all_arm_property"],
            "W40 must satisfy the necessary arm condition")
    require(calibrations["W25-F8"]["all_arm_property"],
            "W25 allblocked support must satisfy the necessary arm condition")

    result = {
        "schema": "codex.x4_quotient_skeleton.v1",
        "status": "PASS",
        "scope": "exact necessary reductions; universal X4-to-cap remains open",
        "theorems": {
            "top_quotient": (
                "If rank(L_C)=0 and A_pq is nonzero, then kappa0,kappa1,kappa2,s "
                "are four nonzero linear forms on C=F^9, hence q_pq is nonzero "
                "over any field. Therefore every carrier on every live pair of "
                "an allblocked source has rank(L_C)>=1."
            ),
            "pure_skeleton_arm_condition": (
                "Choose one live perfect matching in each pure row. For every "
                "selected edge pq, the physical arm-response graph on the six "
                "residual sites has matching number at least two; otherwise it "
                "lies in a star or triangle, gives rank(L_C)=0, and the live-pair "
                "top-quotient lemma gives an active cap."
            ),
            "minimum_degree_corollary": (
                "The occupied physical-pair graph of an allblocked source has "
                "minimum degree at least three."
            ),
            "local_rank_limitation": (
                "W40 is X4 and contains blocked carriers in every quotient "
                "dimension 0 through 7, so X4 alone cannot support a "
                "carrier-local dimension threshold in those ranges."
            ),
        },
        "carrier_calibration": carrier_results,
        "blocked_w40_quotient_dimensions": blocked_w40_dimensions,
        "pure_matching_orbits": {
            "count": len(skeletons),
            "labelled_triples": sum(record["orbit_size"] for record in skeletons),
            "minimum_augmentation_histogram": dict(sorted(Counter(
                record["minimum_additional_physical_pairs"] for record in skeletons
            ).items())),
            "minimum_total_pair_histogram": dict(sorted(Counter(
                record["minimum_total_physical_pairs"] for record in skeletons
            ).items())),
            "minimum_total_labelled_histogram": {
                total: sum(record["orbit_size"] for record in skeletons
                           if record["minimum_total_physical_pairs"] == total)
                for total in sorted(set(record["minimum_total_physical_pairs"]
                                        for record in skeletons))
            },
            "records": skeletons,
        },
        "source_skeleton_calibration": calibrations,
        "controls": {
            "input_hashes": {str(path.relative_to(ROOT)): expected
                             for path, expected in PINS.items()},
            "augmentation_deletion_mutations": [
                {"orbit": orbit, "edge": list(edge)}
                for orbit, edge in mutation_fires
            ],
            "intersecting_graph_classification": intersecting_control,
        },
    }
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    (HERE / "results.json").write_text(payload)
    print(json.dumps({
        "status": result["status"],
        "orbits": len(skeletons),
        "augmentation_histogram": result["pure_matching_orbits"]["minimum_augmentation_histogram"],
        "minimum_total_histogram": result["pure_matching_orbits"]["minimum_total_pair_histogram"],
        "W40_orbits": calibrations["W40"]["orbit_histogram"],
        "sha256": sha256(payload.encode()).hexdigest(),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
