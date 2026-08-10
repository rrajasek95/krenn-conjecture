#!/usr/bin/env python3
"""Classify the K6 matching-incidence circuits behind global one-bad debt.

The 15 edge-incidence vectors of the 15 perfect matchings of K6 have rank
10.  Their minimal integer circuits are ten unit-coefficient 3+3 relations,
fifteen unit-coefficient 4+4 relations, and thirty primitive multiplicity-2
6+6 relations on eleven distinct columns.  The first family gives odd
plus-binomial holonomy.  The other two give sign-even, nonnegative balanced
circulations, so no strictly positive functional exists on the
label+edge-incidence quotient.

The fifteen even circuits form one S6 orbit and are indexed by the perfect
matching missing from their support graph.  Relative to the distinguished
one-bad hole matching they split 1+6+8.  The aligned class is exactly the
four-tensor rectangle killed by the pinned shared-two-zero-fan theorem;
the fourteen unaligned classes require cross-word transport and are retained
as an explicit scope guard.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import itertools
import json
import math
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
FAN = "computations/verify_n8_one_bad_even_cycle_rectangle_obstruction.py"
FAN_HASH = "970d9a8dcd12a7cf49ac3b956b6c398db1b5dc45b2de62ba116e138e72fcc0fb"
EXPECTED_DIGEST = "57712e1aa8bd06d5d304e7839732c8bbcf90221ed87e2aea4fe66a8d9b6227df"

SITES = tuple(range(6))
EDGES = tuple(itertools.combinations(SITES, 2))


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index, second in enumerate(vertices[1:], 1):
        remainder = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(remainder):
            yield tuple(sorted(((first, second),) + tail))


MATCHINGS = tuple(perfect_matchings(SITES))


def load_fan():
    path = ROOT / FAN
    actual = sha256(path.read_bytes()).hexdigest()
    require(actual == FAN_HASH, f"dependency changed: {FAN}: {actual}")
    spec = spec_from_file_location("one_bad_rectangle_fan", path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def primitive_null_vector(matrix):
    basis = matrix.nullspace()
    require(len(basis) == 1, "a circuit stopped having nullity one")
    vector = basis[0]
    denominator = sp.ilcm(*(entry.q for entry in vector))
    integers = [int(entry * denominator) for entry in vector]
    divisor = math.gcd(*(abs(value) for value in integers))
    integers = [value // divisor for value in integers]
    if next(value for value in integers if value) < 0:
        integers = [-value for value in integers]
    return tuple(integers)


def enumerate_circuits():
    incidence = sp.Matrix([
        [int(edge in matching) for matching in MATCHINGS]
        for edge in EDGES
    ])
    require(incidence.shape == (15, 15), "the K6 incidence shape changed")
    require(incidence.rank() == 10, "the K6 matching incidence rank changed")

    circuits = []
    for size in range(2, 12):
        for support in itertools.combinations(range(15), size):
            submatrix = incidence[:, support]
            if submatrix.rank() != size - 1:
                continue
            if not all(incidence[:, support[:index] + support[index + 1:]].rank()
                       == size - 1 for index in range(size)):
                continue
            coefficients = primitive_null_vector(submatrix)
            circuits.append((support, coefficients))

    size_census = Counter(len(support) for support, coefficients in circuits)
    require(size_census == Counter({6: 10, 8: 15, 11: 30}),
            f"the minimal circuit census changed: {size_census}")

    # Rank ten bounds a minimal vector-matroid circuit by eleven columns, so
    # the direct size-2..11 audit is complete.

    sign_census = Counter()
    for support, coefficients in circuits:
        positive_weight = sum(value for value in coefficients if value > 0)
        negative_weight = -sum(value for value in coefficients if value < 0)
        sign_census[(len(support), positive_weight, negative_weight,
                     max(abs(value) for value in coefficients))] += 1
    require(sign_census == Counter({
        (6, 3, 3, 1): 10,
        (8, 4, 4, 1): 15,
        (11, 6, 6, 2): 30,
    }),
            f"the circuit sign census changed: {sign_census}")
    return incidence, circuits


def missing_matching(support):
    used = set()
    for index in support:
        used.update(MATCHINGS[index])
    missing = frozenset(set(EDGES) - used)
    require(len(missing) == 3,
            "an even-circuit support stopped omitting three edges")
    require(Counter(vertex for edge in missing for vertex in edge)
            == Counter(SITES),
            "the omitted edges stopped forming a perfect matching")
    return missing


def audit_even_orbit(circuits):
    even = [(support, coefficients) for support, coefficients in circuits
            if len(support) == 8]
    indexed = {}
    for support, coefficients in even:
        missing = missing_matching(support)
        require(missing not in indexed,
                "two even circuits acquired the same omitted matching")
        indexed[missing] = (support, coefficients)
        expected = frozenset(
            index for index, matching in enumerate(MATCHINGS)
            if not (set(matching) & set(missing))
        )
        require(frozenset(support) == expected,
                "an even circuit stopped being the octahedral matching set")
    require(set(indexed) == {frozenset(matching) for matching in MATCHINGS},
            "the fifteen omitted-matching labels changed")

    # Relative to the fixed one-bad chart: left pair 01 and diagonal response
    # hole pairs 24,35.  Abstract S6 transitivity does not remove this datum.
    distinguished = frozenset({(0, 1), (2, 4), (3, 5)})
    relative = Counter(len(distinguished & missing) for missing in indexed)
    require(relative == Counter({3: 1, 1: 6, 0: 8}),
            f"the relative even-circuit split changed: {relative}")

    support, coefficients = indexed[distinguished]
    coefficient = dict(zip(support, coefficients))
    cross_edges = ((2, 3), (2, 5), (3, 4), (4, 5))
    pairs = []
    covered = set()
    for cross in cross_edges:
        terms = tuple(index for index in support if cross in MATCHINGS[index])
        require(len(terms) == 2,
                "an aligned cross tensor lost one of its two summands")
        require({coefficient[index] for index in terms} == {-1, 1},
                "an aligned tensor pair stopped crossing the circuit sign")
        covered.update(terms)
        pairs.append({
            "right_pair": list(cross),
            "terms": [
                {
                    "sign": coefficient[index],
                    "matching": [list(edge) for edge in MATCHINGS[index]],
                }
                for index in terms
            ],
        })
    require(covered == set(support),
            "the four aligned tensors stopped partitioning the circuit")

    # The four adjacent pairs of cross edges are precisely the four shared
    # two-zero fans in the pinned coefficient theorem.
    shared_fans = tuple(
        tuple(sorted((left, right)))
        for left, right in itertools.combinations(cross_edges, 2)
        if set(left) & set(right)
    )
    require(len(shared_fans) == 4,
            "the aligned cross rectangle lost its four shared fans")
    return {
        "even_circuits": len(even),
        "abstract_S6_orbits": 1,
        "indexing": "omitted perfect matching",
        "relative_to_01_24_35": {
            "equal": relative[3],
            "share_one_edge": relative[1],
            "disjoint": relative[0],
        },
        "aligned_cross_tensor_pairs": pairs,
        "aligned_shared_zero_fans": len(shared_fans),
        "unaligned_even_circuits": relative[1] + relative[0],
    }


def normalized_coefficient_map(items):
    mapping = dict(items)
    first = mapping[min(mapping)]
    if first < 0:
        mapping = {index: -value for index, value in mapping.items()}
    return tuple(sorted(mapping.items()))


def audit_multiplicity_orbit(circuits):
    large = [(support, coefficients) for support, coefficients in circuits
             if len(support) == 11]
    require(len(large) == 30,
            "the multiplicity-2 circuit count changed")
    keys = {
        normalized_coefficient_map(zip(support, coefficients))
        for support, coefficients in large
    }
    matching_index = {
        frozenset(matching): index
        for index, matching in enumerate(MATCHINGS)
    }

    representative = large[0]
    orbit = set()
    for permutation in itertools.permutations(SITES):
        transformed = []
        for index, coefficient in zip(*representative):
            matching = frozenset(
                tuple(sorted((permutation[left], permutation[right])))
                for left, right in MATCHINGS[index]
            )
            transformed.append((matching_index[matching], coefficient))
        orbit.add(normalized_coefficient_map(transformed))
    require(orbit == keys and len(orbit) == 30,
            "the multiplicity-2 circuits stopped forming one S6 orbit")

    doubled = Counter()
    for support, coefficients in large:
        indices = [support[index] for index, value in enumerate(coefficients)
                   if abs(value) == 2]
        require(len(indices) == 1,
                "a large circuit lost its unique doubled matching")
        require(sum(abs(value) == 1 for value in coefficients) == 10,
                "a large circuit lost its ten unit coefficients")
        doubled[frozenset(MATCHINGS[indices[0]])] += 1
    require(set(doubled) == {frozenset(matching) for matching in MATCHINGS}
            and set(doubled.values()) == {2},
            "the doubled-matching indexing changed")

    distinguished = frozenset({(0, 1), (2, 4), (3, 5)})
    relative = Counter()
    for matching, count in doubled.items():
        relative[len(matching & distinguished)] += count
    require(relative == Counter({3: 2, 1: 12, 0: 16}),
            f"the large-circuit relative split changed: {relative}")
    return {
        "circuits": len(large),
        "abstract_S6_orbits": 1,
        "support_columns": 11,
        "primitive_absolute_coefficients": "one 2 and ten 1s",
        "move_multiplicity_per_side": 6,
        "doubled_matching_occurrences": "two circuits per K6 matching",
        "relative_to_01_24_35_doubled_matching": {
            "equal": relative[3],
            "share_one_edge": relative[1],
            "disjoint": relative[0],
        },
        "translated_target_unit_certified": False,
        "scope_guard": (
            "the shared-two-zero fan theorem is squarefree and does not "
            "by itself identify these repeated-term six-move circuits"
        ),
    }


def audit_balanced_rows(circuits):
    odd = 0
    even_unit = 0
    even_multiplicity = 0
    for support, coefficients in circuits:
        positive = [support[index]
                    for index, value in enumerate(coefficients)
                    for repetition in range(max(value, 0))]
        negative = [support[index]
                    for index, value in enumerate(coefficients)
                    for repetition in range(max(-value, 0))]
        require(len(positive) == len(negative),
                "a circuit lost its balanced sign sides")
        # Pair the two sides arbitrarily.  All terms lie in one output label,
        # so each move has zero label delta; the edge-exponent rows telescope.
        exponent_sum = Counter()
        for plus, minus in zip(positive, negative):
            exponent_sum.update(MATCHINGS[plus])
            exponent_sum.subtract(MATCHINGS[minus])
        require(not +exponent_sum and not -exponent_sum,
                "a circuit stopped balancing endpoint incidence")
        if len(positive) % 2:
            require((-1) ** len(positive) == -1,
                    "an odd circuit lost its sign unit")
            odd += 1
        else:
            require((-1) ** len(positive) == 1,
                    "an even circuit acquired odd holonomy")
            if len(support) == 8:
                even_unit += 1
            else:
                require(len(support) == 11 and len(positive) == 6,
                        "an unexpected even circuit family appeared")
                even_multiplicity += 1
    require((odd, even_unit, even_multiplicity) == (10, 15, 30),
            "the odd/even balanced-row count changed")
    return {
        "odd_three_move_circuits": odd,
        "odd_holonomy": -1,
        "even_four_move_unit_coefficient_circuits": even_unit,
        "even_six_move_multiplicity_2_circuits": even_multiplicity,
        "even_holonomy": 1,
        "strict_positive_functional_on_label_plus_edge_quotient": False,
        "farkas_counterguard": (
            "each even circuit is a four- or six-move nonnegative "
            "combination whose label and endpoint-incidence vector is zero"
        ),
    }


def main():
    fan = load_fan()
    incidence, circuits = enumerate_circuits()
    balanced = audit_balanced_rows(circuits)
    even = audit_even_orbit(circuits)
    multiplicity = audit_multiplicity_orbit(circuits)

    # Replay the exact coefficient obstruction on the one aligned relative
    # class.  Each of the four shared two-zero fans is a unit ideal over QQ.
    fan_result = fan.audit_shared_zero_fans()
    require(len(fan_result["unit_fans"]) == 4,
            "the aligned shared-zero fan theorem changed")
    require(fan_result["complete_rectangle_ideal"] == "unit over QQ",
            "the aligned rectangle ideal stopped being a unit")

    ledger = {
        "fan_dependency": {"path": FAN, "sha256": FAN_HASH},
        "incidence": {"shape": list(incidence.shape), "rank": incidence.rank()},
        "minimal_circuits": {
            "total": len(circuits),
            "support_6_3plus_3minus": 10,
            "support_8_4plus_4minus": 15,
            "support_11_primitive_multiplicity_2": 30,
        },
        "balanced_debt_quotient": balanced,
        "even_circuit_orbit": even,
        "multiplicity_2_circuit_orbit": multiplicity,
        "aligned_coefficient_fan": fan_result,
        "verdict": (
            "the K6 label+endpoint-incidence quotient has fifteen squarefree "
            "and thirty multiplicity-2 sign-even balanced circulations, so "
            "no strict positive linear functional exists there; the one "
            "aligned squarefree class is coefficient-impossible, while "
            "fourteen unaligned squarefree and all multiplicity-2 classes "
            "need cross-word or translated-target coupling"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST,
                f"global debt circuit ledger changed: {digest}")

    print("N=8 one-bad global debt circuit quotient: PASS")
    print("incidence rank / minimal circuits: 10 / 55")
    print("odd3 / even4 / multiplicity-even6 circuits: 10 / 15 / 30")
    print("even relative split equal/share1/disjoint: 1 / 6 / 8")
    print("aligned class: shared-two-zero fan UNIT; unaligned classes: 14")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
