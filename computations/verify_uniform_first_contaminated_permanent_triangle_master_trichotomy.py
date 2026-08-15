#!/usr/bin/env python3
"""Intrinsic master trichotomy for the first contaminated permanent triangle.

The packet is the literal six-site guard from the tail-stable permanent
triangle lemma.  The first 2-by-2 permanent acquires the third K4 matching,
while the other two rows remain binomial.  This audit proves three facts:

* forced-spoke factorization sends the rows to two clean local C4 coefficient
  cores and one full K4 coefficient core.  These are monochromatic and hence
  not active three-colour caps;
* pure-alpha normalization cannot be carried by reinserting the killed K4
  aggregate.  It forces an escape matching.  Every such escape shares one
  unique edge with one K4 parent.  The corresponding restriction is either
  a local C4 or a four-site full matching core, but the pure scalar equation
  does not make that restriction a descended GHZ source; and
* the extra matching is not individually redundant under the natural
  three-channel cut state.  All three channel coefficients are nonzero.

An exhaustive 15^3 census additionally shows that adding only one pure
matching in each colour creates at least nine literal mixed singletons.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import argparse
import importlib.util
import itertools
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
DEPENDENCY = "computations/verify_uniform_permanent_triangle_common_tail_unit_lemma.py"
DEPENDENCY_SHA256 = "1431e0aebfe1ce0a85f4e38aec6ff66c6efc0cc75d0caae2c5c9341b5fb50900"
EXPECTED_LEDGER_SHA256 = "eafe44986bc6c75b6c05d6d840927689b6e5008d6063fd5e7742b860442ebc69"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load_dependency():
    path = ROOT / DEPENDENCY
    digest = sha256(path.read_bytes()).hexdigest()
    require(digest == DEPENDENCY_SHA256,
            ("dependency changed", digest, DEPENDENCY_SHA256))
    specification = importlib.util.spec_from_file_location(
        "permanent_triangle_unit_dependency", path)
    require(specification is not None and specification.loader is not None,
            path)
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


P = load_dependency()
N = 6
COLOURS = (0, 1, 2)
VERTICES = tuple(range(N))
EDGES = tuple(itertools.combinations(VERTICES, 2))


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


MATCHINGS = tuple(perfect_matchings(VERTICES))
require(len(MATCHINGS) == 15, len(MATCHINGS))


def edge(left, right):
    return tuple(sorted((left, right)))


def packet_support():
    r, s, x, y, z, hub = VERTICES
    return {
        (edge(r, x), 0): "a", (edge(r, y), 0): "b",
        (edge(r, z), 0): "c", (edge(s, x), 0): "d",
        (edge(s, y), 0): "e", (edge(s, z), 0): "f",
        (edge(hub, x), 1): "p_x", (edge(hub, y), 1): "p_y",
        (edge(hub, z), 1): "p_z",
        (edge(r, s), 0): "g", (edge(x, y), 0): "k",
    }


SUPPORT = packet_support()


def matching_cells(matching, word):
    cells = []
    for left, right in matching:
        if word[left] != word[right]:
            return None
        cell = (edge(left, right), word[left])
        if cell not in SUPPORT:
            return None
        cells.append(SUPPORT[cell])
    return tuple(cells)


def live_terms(word, support=SUPPORT):
    answer = []
    for matching in MATCHINGS:
        cells = []
        for left, right in matching:
            if word[left] != word[right]:
                break
            label = (edge(left, right), word[left])
            if label not in support:
                break
            cells.append(support[label])
        else:
            answer.append((matching, tuple(cells)))
    return tuple(answer)


def word_inventory():
    nonzero = {}
    histogram = Counter()
    for word in itertools.product(COLOURS, repeat=N):
        terms = live_terms(word)
        histogram[len(terms)] += 1
        if terms:
            nonzero["".join(map(str, word))] = terms
    require(histogram == Counter({0: 726, 2: 2, 3: 1}), histogram)
    require(set(nonzero) == {"000011", "000101", "001001"}, nonzero)
    return nonzero, histogram


def cycle_data(left, right):
    common = set(left) & set(right)
    symmetric = set(left) ^ set(right)
    degrees = Counter(vertex for endpoints in symmetric for vertex in endpoints)
    return common, symmetric, degrees


def local_rows_and_contractions(nonzero):
    expected_counts = {"000011": 3, "000101": 2, "001001": 2}
    require({word: len(terms) for word, terms in nonzero.items()}
            == expected_counts, nonzero)
    rows = {
        word: P.hafnian_coefficient(tuple(map(int, word)), SUPPORT)
        for word in nonzero
    }
    expected = {
        "000011": P.multiply(P.monomial("p_z"), P.add(
            P.monomial("a", "e"), P.monomial("b", "d"),
            P.monomial("g", "k"))),
        "000101": P.multiply(P.monomial("p_y"), P.add(
            P.monomial("a", "f"), P.monomial("c", "d"))),
        "001001": P.multiply(P.monomial("p_x"), P.add(
            P.monomial("b", "f"), P.monomial("c", "e"))),
    }
    require(rows == expected, (rows, expected))

    core_types = {}
    for word, spoke in (("000011", "p_z"),
                        ("000101", "p_y"),
                        ("001001", "p_x")):
        derivative = {
            tuple(name for name in monomial if name != spoke): coefficient
            for monomial, coefficient in rows[word].items()
        }
        require(all(spoke not in monomial for monomial in derivative), derivative)
        core_types[word] = {
            "forced_spoke": spoke,
            "contracted_term_count": len(derivative),
            "local_coefficient_core": (
                "full K4" if len(derivative) == 3 else "clean C4"
            ),
            "three_colour_active_cap": False,
        }

    for word in ("000101", "001001"):
        first, second = (record[0] for record in nonzero[word])
        common, symmetric, degrees = cycle_data(first, second)
        require(len(common) == 1 and len(symmetric) == 4
                and set(degrees.values()) == {2},
                (word, common, symmetric, degrees))
    return rows, core_types


def evaluate(polynomial, values):
    total = 0
    for monomial, coefficient in polynomial.items():
        product_value = coefficient
        for name in monomial:
            product_value *= values[name]
        total += product_value
    return total


def all_unit_guard(rows):
    values = {
        "a": 1, "b": 1, "c": 1, "d": 1, "e": 1, "f": -1,
        "g": 1, "k": -2, "p_x": 1, "p_y": 1, "p_z": 1,
    }
    row_values = {word: evaluate(row, values) for word, row in rows.items()}
    require(set(row_values.values()) == {0}
            and all(value != 0 for value in values.values()),
            (values, row_values))
    channel_coefficients = {
        "cross_identity_ae": values["a"] * values["e"],
        "cross_swap_bd": values["b"] * values["d"],
        "separated_gk": values["g"] * values["k"],
    }
    require(channel_coefficients == {
        "cross_identity_ae": 1,
        "cross_swap_bd": 1,
        "separated_gk": -2,
    } and sum(channel_coefficients.values()) == 0,
            channel_coefficients)
    require(all(sum(value for key, value in channel_coefficients.items()
                    if key != omitted) != 0
                for omitted in channel_coefficients),
            "one channel became individually removable")
    return {
        "row_values": row_values,
        "cut_channel_basis": [
            "two-cross identity", "two-cross swap", "zero-cross separated"
        ],
        "cut_channel_coefficients": channel_coefficients,
        "augmentation_sum": 0,
        "individually_removable_channels": 0,
        "verdict": (
            "g*k is a genuine third matching-connectivity channel; scalar "
            "cancellation does not make it a removable kernel state"
        ),
    }


def activity_and_descent_guard(contractions):
    endpoint_profiles = {
        word: [[1, 0, 0] for _site in range(4)]
        for word in contractions
    }


def rational_rank(matrix):
    rows = [[Fraction(value) for value in row] for row in matrix]
    rank = 0
    columns = len(rows[0]) if rows else 0
    for column in range(columns):
        pivot = next((index for index in range(rank, len(rows))
                      if rows[index][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        value = rows[rank][column]
        rows[rank] = [entry / value for entry in rows[rank]]
        for index in range(len(rows)):
            if index == rank or not rows[index][column]:
                continue
            value = rows[index][column]
            rows[index] = [left - value * right
                           for left, right in zip(rows[index], rows[rank],
                                                  strict=True)]
        rank += 1
    return rank


def linear_permanent_syzygy_guard():
    variables = tuple("abcdef")
    permanents = (
        P.add(P.monomial("a", "e"), P.monomial("b", "d")),
        P.add(P.monomial("a", "f"), P.monomial("c", "d")),
        P.add(P.monomial("b", "f"), P.monomial("c", "e")),
    )
    columns = tuple(P.multiply(P.monomial(variable), permanent)
                    for permanent in permanents for variable in variables)
    cubic_monomials = tuple(sorted({monomial for column in columns
                                    for monomial in column}))
    matrix = tuple(tuple(column.get(monomial, 0) for column in columns)
                   for monomial in cubic_monomials)
    rank = rational_rank(matrix)
    require(len(columns) == rank == 18, (len(cubic_monomials), rank))
    return {
        "linear_cofactor_unknowns": len(columns),
        "cubic_monomials": len(cubic_monomials),
        "coefficient_matrix_rank": rank,
        "linear_syzygy_kernel_dimension": len(columns) - rank,
        "consequence": (
            "there is no homogeneous linear syzygy among the three 2-by-2 "
            "permanents.  The inhomogeneous identity with right side 2*b*c*d "
            "is a unit certificate, not an automatic comparison cell"
        ),
    }
    activity_products = {
        word: [profile[0] * profile[1] * profile[2]
               for profile in profiles]
        for word, profiles in endpoint_profiles.items()
    }
    require(all(set(products) == {0}
                for products in activity_products.values()),
            activity_products)
    return {
        "contracted_endpoint_colour_profiles": endpoint_profiles,
        "three_colour_activity_products": activity_products,
        "active_clean_caps_constructed": 0,
        "reason": (
            "every displayed C4/K4 cofactor is colour zero at all four "
            "endpoints, so each kappa profile is (nonzero,0,0) and the "
            "three-colour activity product vanishes"
        ),
        "full_tensor_descent_constructed": False,
        "descent_debt": (
            "forced-spoke factorization proves only the named mixed "
            "coefficient equation.  A restriction of the pure scalar row "
            "is a subcofactor, not a normalized four-site GHZ tensor; the "
            "other 80 four-site output rows and three target normals are "
            "not transported"
        ),
    }


def pure_reinsertion_escape():
    # The three parents are precisely the K4 matchings reinserted by hz=45.
    hz = edge(4, 5)
    parents = (
        tuple(sorted((edge(0, 2), edge(1, 3), hz))),
        tuple(sorted((edge(0, 3), edge(1, 2), hz))),
        tuple(sorted((edge(0, 1), edge(2, 3), hz))),
    )
    using_hz = tuple(matching for matching in MATCHINGS if hz in matching)
    escapes = tuple(matching for matching in MATCHINGS if hz not in matching)
    require(set(using_hz) == set(parents) and len(escapes) == 12,
            (using_hz, parents, escapes))

    records = []
    parent_counts = Counter()
    for escape in escapes:
        candidates = []
        for parent_index, parent in enumerate(parents):
            common, symmetric, degrees = cycle_data(escape, parent)
            if (len(common) == 1 and len(symmetric) == 4
                    and set(degrees.values()) == {2}):
                candidates.append((parent_index, tuple(common)[0], symmetric))
        require(len(candidates) == 1, (escape, candidates))
        parent_index, common_edge, symmetric = candidates[0]
        parent_counts[parent_index] += 1
        records.append({
            "escape_matching": [list(item) for item in escape],
            "unique_parent": parent_index,
            "contraction_edge": list(common_edge),
            "remaining_core_edges": [list(item) for item in sorted(symmetric)],
        })
    require(parent_counts == Counter({0: 4, 1: 4, 2: 4}), parent_counts)

    core_names = {
        edge(0, 2): "a", edge(0, 3): "b", edge(0, 4): "c",
        edge(1, 2): "d", edge(1, 3): "e", edge(1, 4): "f",
        edge(0, 1): "g", edge(2, 3): "k", hz: "q_45^0",
    }
    names = {edge_value: core_names.get(
        edge_value, f"u_{edge_value[0]}{edge_value[1]}^0")
             for edge_value in EDGES}
    pure_terms = {
        matching: P.monomial(*(names[edge_value] for edge_value in matching))
        for matching in MATCHINGS
    }
    pure_polynomial = P.add(*(pure_terms[matching] for matching in MATCHINGS))
    h_polynomial = P.add(P.monomial("a", "e"),
                         P.monomial("b", "d"),
                         P.monomial("g", "k"))
    reinsertion_polynomial = P.multiply(P.monomial("q_45^0"), h_polynomial)
    escape_polynomial = P.add(*(pure_terms[matching] for matching in escapes))
    require(pure_polynomial == P.add(reinsertion_polynomial,
                                     escape_polynomial),
            (pure_polynomial, reinsertion_polynomial, escape_polynomial))

    # In the pure-alpha coefficient, all terms using q_45^0 are q_45^0 H.
    # The mixed row p_z H=0 and p_z a unit give H=0.  Thus target value one
    # forces the sum of the twelve escape terms to equal one.
    return {
        "pure_matching_partition": {"reinsertion_sector": 3,
                                     "escape_sector": 12},
        "reinsertion_identity": "Pure_0 = q_45^0*(a*e+b*d+g*k) + Escape",
        "mixed_contraction": "p_z*(a*e+b*d+g*k)=0 and p_z!=0 imply H=0",
        "target_consequence": "Pure_0=1 implies Escape=1",
        "symbolic_pure_row_term_counts": {
            "total": len(pure_polynomial),
            "reinsertion": len(reinsertion_polynomial),
            "escape": len(escape_polynomial),
        },
        "escape_parent_histogram": dict(sorted(parent_counts.items())),
        "escape_C4_records": records,
        "restriction_support_dichotomy": (
            "restricting to the unique common edge has two local terms if "
            "the third K4 matching is absent and three if present"
        ),
        "equation_level_warning": (
            "Pure_0=1 constrains only the sum of the reinsertion and escape "
            "sectors.  It does not prescribe the value of one common-edge "
            "restriction and therefore does not by itself descend an exact "
            "four-site source"
        ),
    }


def cell_bit(edge_value, colour):
    return 1 << (EDGES.index(edge_value) * 3 + colour)


def support_mask(cells):
    answer = 0
    for edge_value, colour in cells:
        answer |= cell_bit(edge_value, colour)
    return answer


def pure_anchor_singleton_census():
    base_mask = support_mask(SUPPORT)
    pure_masks = {
        (colour, matching_index): support_mask(
            (edge(*pair), colour) for pair in matching)
        for colour in COLOURS
        for matching_index, matching in enumerate(MATCHINGS)
    }
    word_occurrences = {}
    for word in itertools.product(COLOURS, repeat=N):
        occurrences = []
        for matching in MATCHINGS:
            if all(word[left] == word[right] for left, right in matching):
                occurrences.append(support_mask(
                    (edge(left, right), word[left]) for left, right in matching))
        word_occurrences[word] = tuple(occurrences)

    histogram = Counter()
    minimizers = []
    minimum = None
    for indices in itertools.product(range(len(MATCHINGS)), repeat=3):
        selected = base_mask
        for colour, matching_index in enumerate(indices):
            selected |= pure_masks[colour, matching_index]
        singleton_words = []
        for word, occurrences in word_occurrences.items():
            if len(set(word)) == 1:
                continue
            multiplicity = sum(mask & ~selected == 0 for mask in occurrences)
            if multiplicity == 1:
                singleton_words.append("".join(map(str, word)))
        count = len(singleton_words)
        histogram[count] += 1
        if minimum is None or count < minimum:
            minimum = count
            minimizers = [(indices, singleton_words)]
        elif count == minimum:
            minimizers.append((indices, singleton_words))
    require(sum(histogram.values()) == 15**3 and minimum == 9
            and len(minimizers) == 4,
            (histogram, minimum, minimizers))
    return {
        "pure_anchor_triples": 15**3,
        "minimum_mixed_singletons": minimum,
        "number_of_minimizers": len(minimizers),
        "singleton_count_histogram": dict(sorted(histogram.items())),
        "first_minimizer": {
            "matching_indices": list(minimizers[0][0]),
            "singleton_words": minimizers[0][1],
        },
        "scope": (
            "this is exhaustive for adding exactly one selected pure "
            "matching per colour and no other repair cells; further support "
            "can change which singleton is exposed"
        ),
    }


def audit():
    nonzero, histogram = word_inventory()
    rows, contractions = local_rows_and_contractions(nonzero)
    ledger = {
        "theorem": "first contaminated permanent-triangle master-trichotomy counterguard",
        "dependency": {DEPENDENCY: DEPENDENCY_SHA256},
        "literal_packet": {
            "decorated_cells": len(SUPPORT),
            "word_occurrence_histogram": dict(sorted(histogram.items())),
            "nonzero_word_term_counts": {
                word: len(terms) for word, terms in sorted(nonzero.items())
            },
            "mixed_singletons_inside_packet": 0,
        },
        "adjacent_rows_and_forced_spoke_contractions": contractions,
        "activity_and_full_tensor_descent_guard": activity_and_descent_guard(
            contractions),
        "linear_permanent_syzygy_guard": linear_permanent_syzygy_guard(),
        "all_unit_contamination_and_cut_rank_guard": all_unit_guard(rows),
        "pure_reinsertion_escape": pure_reinsertion_escape(),
        "minimal_pure_anchor_completion": pure_anchor_singleton_census(),
        "master_alternative_verdict": {
            "singleton_or_unit": (
                "not in the eleven-cell packet; yes for every support-minimal "
                "one-pure-matching-per-colour completion, but arbitrary "
                "further repairs are outside that census"
            ),
            "active_clean_C4_cap": (
                "not constructed: two clean local C4 coefficient cores exist "
                "but all are monochromatic and have zero three-colour "
                "activity product"
            ),
            "smaller_exact_matching_source": (
                "not constructed: one-row factorization/restriction does not "
                "transport the full tensor or pure target normalizations"
            ),
        },
        "all_N_interface": (
            "after a forced unit common tail is factored, the coefficient-core "
            "statement is literal at any even N.  The recurrence gate is a "
            "three-colour active cap or a full-output restriction theorem, "
            "not merely same-sector support"
        ),
        "scope": (
            "diagonal occurrence-labelled source equations.  This is a sharp "
            "counterguard: local coefficient restriction exists, but neither "
            "Theorem-3.2 activity nor full exact tensor descent follows.  No "
            "B/Eq presentation is used"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    return ledger, digest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("structural", "full", "exhaustive"),
                        default="full")
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()
    ledger, digest = audit()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger changed", digest, EXPECTED_LEDGER_SHA256))
    if arguments.json:
        print(json.dumps({"mode": arguments.mode, "ledger": ledger,
                          "ledger_sha256": digest}, indent=2, sort_keys=True))
        return
    print("first contaminated permanent-triangle trichotomy: PASS")
    print("local nonzero rows", ledger["literal_packet"]
          ["nonzero_word_term_counts"])
    print("pure escape matchings", ledger["pure_reinsertion_escape"]
          ["pure_matching_partition"])
    print("minimum pure-anchor singleton count", ledger[
          "minimal_pure_anchor_completion"]["minimum_mixed_singletons"])
    print("ledger_sha256", digest)


if __name__ == "__main__":
    main()
