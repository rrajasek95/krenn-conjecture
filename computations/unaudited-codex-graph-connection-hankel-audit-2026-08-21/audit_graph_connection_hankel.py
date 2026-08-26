#!/usr/bin/env python3
"""Exact bounded audit of graph-connection/Hankel theory for Krenn amplitudes."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = HERE / "results_graph_connection_hankel.json"

PINS = (
    "computations/unaudited-codex-onehot-peps-holant-2026-08-21/audit_onehot_peps_holant.py",
    "computations/unaudited-codex-zeon-contraction-hierarchy-2026-08-21/audit_zeon_contraction_hierarchy.py",
    "computations/unaudited-codex-ghz-rees-boundary-2026-08-21/audit_ghz_rees_boundary.py",
    "notes/global-wick-top-invariant-counterguard.md",
    "computations/verify_global_wick_top_invariant_counterguard.py",
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def file_sha(path):
    return sha256(path.read_bytes()).hexdigest()


def logical_sha(payload):
    raw = json.dumps(payload, sort_keys=True,
                     separators=(",", ":")).encode("ascii")
    return sha256(raw).hexdigest()


def exact_rank(matrix):
    work = [[Fraction(value) for value in row] for row in matrix]
    rank = 0
    width = len(work[0]) if work else 0
    for column in range(width):
        pivot = next((row for row in range(rank, len(work))
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        value = work[rank][column]
        for row in range(rank + 1, len(work)):
            if not work[row][column]:
                continue
            scale = work[row][column] / value
            for later in range(column, width):
                work[row][later] -= scale * work[rank][later]
        rank += 1
        if rank == len(work):
            break
    return rank


def edge(u, v):
    return (u, v) if u < v else (v, u)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            answer.append(tuple(sorted((edge(first, second),) + tail)))
    return tuple(answer)


def flattening_rank(n, terms, subset):
    subset = tuple(subset)
    complement = tuple(site for site in range(n) if site not in subset)
    rows = tuple(product(range(3), repeat=len(subset)))
    columns = tuple(product(range(3), repeat=len(complement)))
    row_index = {word: index for index, word in enumerate(rows)}
    column_index = {word: index for index, word in enumerate(columns)}
    matrix = [[0] * len(columns) for _ in rows]
    for word, coefficient in terms.items():
        left = tuple(word[site] for site in subset)
        right = tuple(word[site] for site in complement)
        matrix[row_index[left]][column_index[right]] += coefficient
    return exact_rank(matrix)


def ghz_connection_blocks():
    result = {}
    for n in (4, 8):
        terms = {(colour,) * n: 1 for colour in range(3)}
        profile = Counter()
        for size in range(1, n):
            for subset in combinations(range(n), size):
                profile[(size, flattening_rank(n, terms, subset))] += 1
        require(all(rank == 3 for size, rank in profile), profile)
        result[str(n)] = {
            "all_nontrivial_labelled_flattenings_rank": 3,
            "cut_count": sum(profile.values()),
            "by_cut_size": {
                str(size): profile[size, 3] for size in range(1, n)
            },
        }
    return result


def k4_boundary_types():
    colour_matchings = {
        0: frozenset(((0, 1), (2, 3))),
        1: frozenset(((0, 2), (1, 3))),
        2: frozenset(((0, 3), (1, 2))),
    }
    records = []
    for left in combinations(range(4), 2):
        if 0 not in left:  # choose one of each complementary pair of cuts
            continue
        left = frozenset(left)
        crossing = {
            colour: sum((u in left) != (v in left) for u, v in matching)
            for colour, matching in colour_matchings.items()
        }
        require(sorted(crossing.values()) == [0, 2, 2], (left, crossing))
        records.append({
            "left_sites": sorted(left),
            "crossing_edges_by_colour": crossing,
        })
    require(len(records) == 3, records)
    return {
        "integer_source": {
            str(colour): [list(value) for value in sorted(matching)]
            for colour, matching in colour_matchings.items()
        },
        "pair_cut_records": records,
        "conclusion": (
            "Every 2+2 cut has one pure colour in the zero-crossing sector "
            "and two pure colours in the two-crossing sector, although the "
            "output flattening is the same rank-three GHZ table."
        ),
    }


def supported_partial_matchings(graph, size):
    graph = frozenset(graph)
    answer = set()
    for vertices in combinations(range(8), 2 * size):
        for matching in perfect_matchings(vertices):
            matching = frozenset(matching)
            if matching <= graph:
                answer.add(tuple(sorted(matching)))
    return answer


def invisible_chord_control():
    base = frozenset(((0, 1), (2, 3), (4, 5), (6, 7)))
    chorded = base | {(0, 2)}
    power_profiles = {}
    for size in range(1, 5):
        left = supported_partial_matchings(base, size)
        right = supported_partial_matchings(chorded, size)
        power_profiles[str(size)] = {
            "base": len(left),
            "chorded": len(right),
            "new": len(right - left),
        }
    require(power_profiles == {
        "1": {"base": 4, "chorded": 5, "new": 1},
        "2": {"base": 6, "chorded": 8, "new": 2},
        "3": {"base": 4, "chorded": 5, "new": 1},
        "4": {"base": 1, "chorded": 1, "new": 0},
    }, power_profiles)
    top_base = supported_partial_matchings(base, 4)
    top_chorded = supported_partial_matchings(chorded, 4)
    require(top_base == top_chorded == {tuple(sorted(base))},
            (top_base, top_chorded))

    # The fixed K8 top cofactor of chord 02 vanishes: on the complementary
    # vertices 1,3,4,5,6,7 there is no edge incident with 1 or 3.
    complement = (1, 3, 4, 5, 6, 7)
    chord_cofactor = [matching for matching in perfect_matchings(complement)
                      if frozenset(matching) <= base]
    require(not chord_cofactor, chord_cofactor)

    # A full graph-connection oracle could glue the missing completion
    # 13|45|67. It would see one additional complete matching in the chorded
    # graph. These values are not supplied by equality of the original K8 top.
    completion = frozenset(((1, 3), (4, 5), (6, 7)))
    completed_base = supported_partial_matchings(base | completion, 4)
    completed_chorded = supported_partial_matchings(chorded | completion, 4)
    require(len(completed_chorded - completed_base) == 1 and
            tuple(sorted(((0, 2), (1, 3), (4, 5), (6, 7))))
            in completed_chorded - completed_base,
            (completed_base, completed_chorded))
    return {
        "base_edges": [list(value) for value in sorted(base)],
        "added_chord": [0, 2],
        "lower_divided_power_supports": power_profiles,
        "fixed_top_output_unchanged": True,
        "fixed_top_chord_cofactor": 0,
        "detecting_labelled_completion": "13|45|67",
        "additional_matching_under_full_completion": "02|13|45|67",
        "dichotomy": (
            "The chord is radical for the fixed-top observation supplied by "
            "the GHZ equation. A full labelled-gluing oracle detects it, but "
            "those extra connection entries are unconstrained source data."
        ),
    }


LAURENT_CELLS = {
    ((0, 1), 0, 0): -1,
    ((0, 3), 1, 1): 0,
    ((0, 7), 2, 2): 0,
    ((1, 4), 2, 2): 0,
    ((1, 6), 1, 1): 0,
    ((2, 3), 2, 2): 0,
    ((2, 4), 1, 1): 0,
    ((2, 5), 0, 0): 1,
    ((3, 4), 0, 0): 0,
    ((5, 6), 2, 2): 0,
    ((5, 7), 1, 1): 0,
    ((6, 7), 0, 0): 0,
}


def laurent_output(valuations):
    answer = defaultdict(Counter)
    for matching in perfect_matchings(range(8)):
        word = [None] * 8
        exponent = 0
        valid = True
        for pair in matching:
            cells = [(left, right, value)
                     for (candidate, left, right), value in valuations.items()
                     if candidate == pair]
            if len(cells) != 1:
                valid = False
                break
            left, right, value = cells[0]
            word[pair[0]], word[pair[1]] = left, right
            exponent += value
        if valid:
            answer[tuple(word)][exponent] += 1
    return answer


def laurent_rank_control():
    expected = {
        (0,) * 8: Counter({0: 1}),
        (1,) * 8: Counter({0: 1}),
        (2,) * 8: Counter({0: 1}),
        tuple(map(int, "12012000")): Counter({1: 1}),
        tuple(map(int, "21000012")): Counter({1: 1}),
    }
    require(laurent_output(LAURENT_CELLS) == expected,
            laurent_output(LAURENT_CELLS))
    for parameter in range(2, 9):
        moved = dict(LAURENT_CELLS)
        moved[((2, 4), 1, 1)] += parameter
        moved[((5, 7), 1, 1)] -= parameter
        require(laurent_output(moved) == expected, parameter)

    special_terms = {(colour,) * 8: 1 for colour in range(3)}
    generic_terms = dict(special_terms)
    generic_terms[tuple(map(int, "12012000"))] = 2
    generic_terms[tuple(map(int, "21000012"))] = 2
    special_profiles = {}
    generic_profiles = {}
    for size in range(1, 5):
        special = Counter()
        generic = Counter()
        for subset in combinations(range(8), size):
            special[flattening_rank(8, special_terms, subset)] += 1
            generic[flattening_rank(8, generic_terms, subset)] += 1
        special_profiles[str(size)] = dict(sorted(special.items()))
        generic_profiles[str(size)] = dict(sorted(generic.items()))
    require(special_profiles == {
        "1": {3: 8}, "2": {3: 28}, "3": {3: 56}, "4": {3: 70}},
        special_profiles)
    require(generic_profiles == {
        "1": {3: 8},
        "2": {3: 1, 4: 14, 5: 13},
        "3": {4: 8, 5: 48},
        "4": {4: 4, 5: 66},
    }, generic_profiles)
    return {
        "exact_output": "Delta_8,3+t*(e_12012000+e_21000012)",
        "ghz_special_flattening_ranks": special_profiles,
        "finite_t_example_flattening_ranks": generic_profiles,
        "output_invisible_valuation_redistributions_checked": list(range(2, 9)),
        "conclusion": (
            "Connection ranks 4 and 5 at finite nonzero parameter collapse "
            "to the rank-three GHZ table at the base-locus limit. Top-Hankel "
            "rank is a closed border datum and does not control finite-source "
            "membership or source valuations."
        ),
    }


def radical_extension_control():
    # Basis e0,e1,e2,n.  The quotient e_i e_j=delta_ij e_i is the three-state
    # copy algebra.  Add a square-zero ideal n with e0*n=n and e1*n=e2*n=0.
    size = 4

    def multiply(left, right):
        if left == 3 and right == 3:
            return {}
        if left == 3 or right == 3:
            other = right if left == 3 else left
            return {3: 1} if other == 0 else {}
        return {left: 1} if left == right else {}

    def product_linear(left, right):
        answer = Counter()
        for i, a in left.items():
            for j, b in right.items():
                for k, c in multiply(i, j).items():
                    answer[k] += a * b * c
        return {key: value for key, value in answer.items() if value}

    basis = [{index: 1} for index in range(size)]
    unit = {0: 1, 1: 1, 2: 1}
    for value in basis:
        require(product_linear(unit, value) == value and
                product_linear(value, unit) == value, (unit, value))
    for left in basis:
        for middle in basis:
            for right in basis:
                require(product_linear(product_linear(left, middle), right) ==
                        product_linear(left, product_linear(middle, right)),
                        (left, middle, right))

    def functional(value):
        return sum(coefficient for index, coefficient in value.items()
                   if index < 3)

    pairing = [[functional(multiply(i, j)) for j in range(size)]
               for i in range(size)]
    require(pairing == [[1, 0, 0, 0], [0, 1, 0, 0],
                        [0, 0, 1, 0], [0, 0, 0, 0]], pairing)
    require(exact_rank(pairing) == 3, pairing)
    return {
        "untrimmed_basis": ["e0", "e1", "e2", "n"],
        "multiplication": "ei*ej=delta_ij ei; e0*n=n; e1*n=e2*n=n^2=0",
        "functional": "lambda(ei)=1; lambda(n)=0",
        "connection_pairing": pairing,
        "connection_rank": 3,
        "radical_ideal": ["n"],
        "quotient": "three-state diagonal copy algebra",
        "theorem": (
            "The same rank-three connection table admits an arbitrary "
            "unobservable square-zero source extension. Therefore connection "
            "rank determines only the observable quotient, never the "
            "untrimmed source, without a separately proved nondegeneracy law."
        ),
    }


def build_result():
    result = {
        "status": "PASS exact graph-connection/Hankel negative audit",
        "classical_theory_interface": {
            "connection_matrix": (
                "For a scalar multiplicative graph parameter f on all "
                "k-labelled graphs, M_k(F,G)=f(F glued_k G)."
            ),
            "graph_algebra": (
                "rank(M_k)=dim(G_k/Rad <x,y>=f(xy)); quotienting the nullspace "
                "is part of the theorem, not an optional source recovery step."
            ),
            "homomorphism_characterization_hypotheses": (
                "A graph parameter on all finite graphs, multiplicativity, "
                "reflection positivity, and exponential connection-rank bounds."
            ),
            "krenn_mismatch": [
                "The conjectural equality supplies one fixed labelled K8 top tensor, not values on every labelled gluing geometry.",
                "The 28 edge blocks are site-pair dependent, not one repeated weighted target graph or vertex model.",
                "Weights are arbitrary complex numbers, so real reflection positivity is unavailable.",
                "Even an abstract finite-rank realization is only the reachable/observable quotient and erases its radical.",
            ],
            "primary_sources": [
                "https://arxiv.org/abs/math/0404468",
                "https://arxiv.org/abs/math/0408232",
                "https://arxiv.org/abs/math/0505035",
            ],
        },
        "ghz_top_connection_blocks": ghz_connection_blocks(),
        "exact_n4_control": k4_boundary_types(),
        "abstract_untrimmed_no_go": radical_extension_control(),
        "fixed_k8_control": invisible_chord_control(),
        "laurent_boundary_control": laurent_rank_control(),
        "terminal_verdict": {
            "three_state_observable_quotient": True,
            "three_state_untrimmed_source_forced": False,
            "precise_no_go": (
                "Top-only connection data either quotients away invisible "
                "source states or, if upgraded to all labelled completions, "
                "asks for values not fixed by the GHZ equation. Finite rank "
                "alone cannot bridge this dichotomy."
            ),
            "strongest_new_replacement": (
                "Build a source-relative connection packet retaining lower "
                "matching sectors q,q^[2],q^[3] together with q^[4], then prove "
                "on the exact X5 fibre that its pairing radical is cap-benign "
                "(generated by inactive/isolated edge directions) or that a "
                "nonzero radical direction itself yields an active clean cap."
            ),
            "scope_guard": (
                "The lower-sector packet is not determined by GHZ and literal "
                "site-downs only rebracket the original 6558 rows. This "
                "replacement requires a genuinely nonlinear source theorem, "
                "not another output-Hankel rank computation."
            ),
        },
        "pinned_sources": {name: file_sha(ROOT / name) for name in PINS},
    }
    result["logical_sha256"] = logical_sha(result)
    return result


def main(write_results=False, print_result=False):
    result = build_result()
    if write_results:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    if print_result:
        print(json.dumps(result, indent=2, sort_keys=True))
        return
    print(json.dumps({
        "status": result["status"],
        "ghz_rank": 3,
        "untrimmed_dimension": 4,
        "untrimmed_connection_rank": result[
            "abstract_untrimmed_no_go"]["connection_rank"],
        "k8_new_lower_supports": {
            degree: profile["new"] for degree, profile in result[
                "fixed_k8_control"]["lower_divided_power_supports"].items()
        },
        "logical_sha256": result["logical_sha256"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--print-result", action="store_true")
    args = parser.parse_args()
    main(args.write_results, args.print_result)
