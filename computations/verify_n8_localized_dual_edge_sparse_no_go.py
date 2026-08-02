#!/usr/bin/env python3
"""Exact localized sparsity no-go on the n=8 dual-edge ansatz.

The twelve properly coloured support coordinates form a perfect matching of
the 24 vertex-colour ports, so the port torus normalizes all twelve to one.
We allow only the 60 coordinate variables occurring in the exact dual from
verify_n8_full_source_cycle_product_membership.py.  This checker proves that
the mixed hafnian coefficients have no common zero in characteristic other
than two when at most thirteen of the remaining 48 coordinates are nonzero.

The proof is finite and standard-library only.  A monotone support search
finds four minimal twelve-coordinate patterns and all 48 admissible
one-coordinate extensions.  In every case three surviving binomials have
an odd signed exponent relation, which forces 1=-1 in the coordinate torus.
"""

from collections import Counter, defaultdict
from hashlib import sha256
from itertools import combinations, product
import importlib.util
import json
from pathlib import Path


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


HERE = Path(__file__).resolve().parent
SOURCE_CHECKER = HERE / "verify_n8_full_source_cycle_product_membership.py"
SPEC = importlib.util.spec_from_file_location("n8_full_source", SOURCE_CHECKER)
SOURCE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SOURCE)

VERTICES = SOURCE.VERTICES
COLOURS = SOURCE.COLOURS
SUPPORT_PRODUCT = SOURCE.SUPPORT_PRODUCT
SUPPORT_SET = SOURCE.SUPPORT_SET
word_terms = SOURCE.word_terms


def variable(code):
    require(len(code) == 4 and all(character.isdigit() for character in code),
            f"invalid variable code {code}")
    return tuple(map(int, code))


DUAL_EDGE_SUPPORT = tuple(map(variable, (
    "0100", "0210", "0211", "0310", "0311", "0520", "0522", "0720",
    "0722", "1220", "1222", "1420", "1422", "1510", "1511", "1610",
    "1611", "2300", "2302", "2320", "2322", "2400", "2401", "2410",
    "2411", "2500", "2501", "2502", "2510", "2520", "2600", "2601",
    "2700", "2702", "3400", "3401", "3402", "3410", "3411", "3420",
    "3422", "3500", "3510", "4500", "4520", "5600", "5602", "5620",
    "5622", "5700", "5701", "5710", "5711", "6700", "6701", "6702",
    "6710", "6711", "6720", "6722",
)))

ZERO_SUPPORT_MATCHING = tuple(map(variable, (
    "0100", "0211", "0520", "1420", "1610", "2322",
    "2702", "3402", "3411", "5622", "5710", "6711",
)))

EXPECTED_MINIMAL_PATTERNS = tuple(tuple(map(variable, pattern)) for pattern in (
    ("0210", "0211", "0310", "2400", "2401", "2410",
     "2510", "3401", "3410", "3411", "3500", "3510"),
    ("0520", "0522", "0720", "2502", "2700", "2702",
     "5600", "5602", "5620", "6702", "6720", "6722"),
    ("1220", "1222", "1420", "2300", "2302", "2320",
     "2520", "3402", "3420", "3422", "4500", "4520"),
    ("1510", "1511", "1610", "2501", "2600", "2601",
     "5700", "5701", "5710", "6701", "6710", "6711"),
))

EXPECTED_LEDGER_SHA256 = (
    "a9c4cbff8f4141b42b186fbd90f7fc91407ec17be961ed61f9ab08b79da837ff"
)


EXTRA_VARIABLES = tuple(
    coordinate for coordinate in DUAL_EDGE_SUPPORT
    if coordinate not in SUPPORT_SET
)
EXTRA_INDEX = {coordinate: index
               for index, coordinate in enumerate(EXTRA_VARIABLES)}


def encode_variable(coordinate):
    return "".join(map(str, coordinate))


def coefficient(word):
    """Specialize one hafnian coefficient to the normalized 60-edge chart."""
    answer = defaultdict(int)
    for term in word_terms(word):
        monomial = []
        for coordinate in term:
            if coordinate in SUPPORT_SET:
                continue
            if coordinate not in EXTRA_INDEX:
                break
            monomial.append(EXTRA_INDEX[coordinate])
        else:
            answer[tuple(sorted(monomial))] += 1
    return tuple(sorted(answer.items()))


def active_terms(polynomial, support):
    return tuple((monomial, scalar) for monomial, scalar in polynomial
                 if frozenset(monomial) <= support)


def support_polynomial(polynomial):
    return tuple(frozenset(monomial) for monomial, _scalar in polynomial)


def support_is_admissible(support, polynomial_supports):
    """A zero cannot have exactly one nonzero monomial in a coefficient."""
    return all(sum(monomial <= support for monomial in polynomial) != 1
               for polynomial in polynomial_supports)


def minimal_admissible_supports(polynomial_supports, maximum_size):
    """Monotone exact search, together with its small proof ledger.

    Each constant-containing mixed coefficient needs a nonconstant active
    term.  Starting with one such term from each, whenever the current set
    activates exactly one term of another coefficient, any admissible
    extension must activate one of its other terms.  Branching on precisely
    those repairs is exhaustive for every admissible support up to the bound.
    """
    constant_polynomials = tuple(
        polynomial for polynomial in polynomial_supports
        if frozenset() in polynomial
    )
    require(len(constant_polynomials) == 2,
            "expected the two mixed boundary coefficients")
    seeds = {
        frozenset().union(*chosen)
        for chosen in product(*(
            tuple(monomial for monomial in polynomial if monomial)
            for polynomial in constant_polynomials
        ))
    }
    seen = set()
    answers = set()

    def search(support):
        if len(support) > maximum_size or support in seen:
            return
        seen.add(support)
        violations = []
        for polynomial in polynomial_supports:
            if sum(monomial <= support for monomial in polynomial) != 1:
                continue
            repairs = {
                monomial - support for monomial in polynomial
                if not monomial <= support
                and monomial - support
                and len(support | monomial) <= maximum_size
            }
            if not repairs:
                return
            violations.append((
                len(repairs), min(map(len, repairs)),
                tuple(sorted(repairs, key=lambda item: tuple(sorted(item)))),
            ))
        if not violations:
            answers.add(support)
            return
        repairs = min(violations, key=lambda item: (item[0], item[1]))[2]
        for repair in repairs:
            search(support | repair)

    for seed in sorted(seeds, key=lambda item: tuple(sorted(item))):
        search(seed)
    return tuple(sorted(answers, key=lambda item: tuple(sorted(item)))), {
        "constant_seed_count": len(seeds),
        "visited_supports": len(seen),
    }


def exponent_difference(first, second, ordered_support):
    position = {coordinate: index
                for index, coordinate in enumerate(ordered_support)}
    difference = [0] * len(ordered_support)
    for index in first:
        difference[position[EXTRA_VARIABLES[index]]] += 1
    for index in second:
        difference[position[EXTRA_VARIABLES[index]]] -= 1
    return tuple(difference)


def odd_binomial_relation(support, mixed_coefficients):
    """Find three equations x^a+x^b=0 whose ratios multiply to -1=1."""
    ordered_support = tuple(sorted(EXTRA_VARIABLES[index]
                                   for index in support))
    equations = []
    for word, polynomial in sorted(mixed_coefficients.items()):
        restricted = active_terms(polynomial, support)
        if len(restricted) != 2:
            continue
        require(restricted[0][1] == restricted[1][1] == 1,
                "binomial coefficients are no longer both one")
        first, second = restricted[0][0], restricted[1][0]
        equations.append((
            word, first, second,
            exponent_difference(first, second, ordered_support),
        ))
    for selected in combinations(range(len(equations)), 3):
        for signs in product((-1, 1), repeat=3):
            if not all(
                sum(signs[index] * equations[equation][3][coordinate]
                    for index, equation in enumerate(selected)) == 0
                for coordinate in range(len(ordered_support))
            ):
                continue
            require(sum(signs) % 2,
                    "three signed unit coefficients should have odd sum")
            relation = []
            for equation, sign in zip(selected, signs):
                word, first, second, difference = equations[equation]
                relation.append({
                    "sign": sign,
                    "word": list(word),
                    "first": [encode_variable(EXTRA_VARIABLES[index])
                              for index in first],
                    "second": [encode_variable(EXTRA_VARIABLES[index])
                               for index in second],
                    "difference": list(difference),
                })
            return {
                "support": [encode_variable(coordinate)
                            for coordinate in ordered_support],
                "binomial_count": len(equations),
                "relation": relation,
            }
    raise RuntimeError("no three-binomial odd exponent relation found")


def encode_polynomial(polynomial):
    return [
        {
            "coefficient": scalar,
            "monomial": [encode_variable(EXTRA_VARIABLES[index])
                         for index in monomial],
        }
        for monomial, scalar in polynomial
    ]


def audit():
    require(len(DUAL_EDGE_SUPPORT) == len(set(DUAL_EDGE_SUPPORT)) == 60,
            "dual edge support is not a 60-element set")
    require(SUPPORT_SET <= frozenset(DUAL_EDGE_SUPPORT),
            "boundary support is missing from the dual edge support")
    require(frozenset(ZERO_SUPPORT_MATCHING) <= frozenset(DUAL_EDGE_SUPPORT),
            "zero-support matching is missing from the dual edge support")
    require(len(EXTRA_VARIABLES) == 48, "off-support variable count")

    coefficients = {
        word: coefficient(word)
        for word in product(COLOURS, repeat=8)
    }
    supported = {word: polynomial for word, polynomial in coefficients.items()
                 if polynomial}
    pure = {word: polynomial for word, polynomial in supported.items()
            if len(set(word)) == 1}
    mixed = {word: polynomial for word, polynomial in supported.items()
             if len(set(word)) > 1}
    require(len(supported) == 931 and len(pure) == 3 and len(mixed) == 928,
            "60-edge coefficient census changed")
    require(Counter(map(len, mixed.values())) == {
        1: 216, 2: 474, 3: 44, 4: 178, 5: 16,
    }, "mixed term histogram changed")
    require(all(any(not monomial for monomial, _scalar in polynomial)
                for polynomial in pure.values()),
            "a normalized pure coefficient lost its constant term")

    # The smaller zero-support-matching seed is already impossible: one of
    # the two supported mixed boundary words remains the literal constant 1.
    zero_extra_support = frozenset(
        EXTRA_INDEX[coordinate] for coordinate in ZERO_SUPPORT_MATCHING
        if coordinate in EXTRA_INDEX
    )
    boundary_word = (1, 2, 0, 1, 2, 0, 0, 0)
    require(active_terms(mixed[boundary_word], zero_extra_support) == (((), 1),),
            "zero-support-matching seed obstruction changed")

    polynomial_supports = tuple(sorted({
        support_polynomial(polynomial) for polynomial in mixed.values()
    }, key=repr))
    require(len(polynomial_supports) == 900,
            "distinct mixed support-polynomial count changed")
    minimal, search_ledger = minimal_admissible_supports(
        polynomial_supports, maximum_size=13
    )
    expected_minimal = tuple(sorted((
        frozenset(EXTRA_INDEX[coordinate] for coordinate in pattern)
        for pattern in EXPECTED_MINIMAL_PATTERNS
    ), key=lambda item: tuple(sorted(item))))
    require(minimal == expected_minimal,
            "minimal admissible support patterns changed")
    require(search_ledger == {
        "constant_seed_count": 16,
        "visited_supports": 98,
    }, "monotone support-search ledger changed")

    extensions = set()
    for support in minimal:
        for index in set(range(len(EXTRA_VARIABLES))) - support:
            extension = support | {index}
            if support_is_admissible(extension, polynomial_supports):
                extensions.add(extension)
    extensions = tuple(sorted(extensions, key=lambda item: tuple(sorted(item))))
    require(len(extensions) == 48 and all(len(item) == 13 for item in extensions),
            "admissible one-coordinate extension census changed")

    cases = minimal + extensions
    relations = tuple(odd_binomial_relation(case, mixed) for case in cases)
    require(len(relations) == 52,
            "not every <=13 admissible support has an odd relation")

    ledger = {
        "vertices": 8,
        "colours": 3,
        "characteristic_excluded": 2,
        "normalized_support_variables": len(SUPPORT_PRODUCT),
        "dual_edge_variables": len(DUAL_EDGE_SUPPORT),
        "off_support_variables": len(EXTRA_VARIABLES),
        "maximum_nonzero_off_support_variables": 13,
        "supported_words": len(supported),
        "mixed_supported_words": len(mixed),
        "distinct_mixed_support_polynomials": len(polynomial_supports),
        "mixed_term_histogram": dict(sorted(Counter(
            map(len, mixed.values())
        ).items())),
        "pure_coefficients": {
            "".join(map(str, word)): encode_polynomial(polynomial)
            for word, polynomial in sorted(pure.items())
        },
        "zero_matching_extra_variables": len(zero_extra_support),
        "zero_matching_constant_mixed_word": list(boundary_word),
        "support_search": search_ledger,
        "minimal_patterns": [
            [encode_variable(EXTRA_VARIABLES[index])
             for index in sorted(support)]
            for support in minimal
        ],
        "admissible_thirteen_extensions": len(extensions),
        "odd_relation_cases": len(relations),
        "relations": relations,
        "conclusion": "no common mixed zero with at most 13 extras",
        "next_open_sparsity": 14,
    }
    return ledger


def main():
    ledger = audit()
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                "frozen localized no-go ledger digest changed")
    print(
        "n=8 localized dual-edge <=13-extra no-go: PASS; "
        f"minimal={len(ledger['minimal_patterns'])}, "
        f"extensions={ledger['admissible_thirteen_extensions']}, "
        f"relations={ledger['odd_relation_cases']}"
    )
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
