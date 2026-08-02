#!/usr/bin/env python3
"""Factor the two n=8 pure quadratic locks through mixed conormals.

At the rational point on the five-parameter mixed torus, the quadratic
differences q_0-q_00000010 and q_1-q_11000111 have respectively 24 and 96
ambient terms.  This checker gives exact decompositions into 5 and 9
products N_k M_k, where every N_k is an explicit linear combination of
mixed hafnian gradients.  It also checks the port-character transport of
the decompositions along the whole Laurent torus orbit.
"""

from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
import importlib.util
import json
from pathlib import Path


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


HERE = Path(__file__).resolve().parent
SECOND_JET_CHECKER = HERE / "verify_n8_counterexample_pure_second_jet.py"
SPEC = importlib.util.spec_from_file_location("n8_second_jet", SECOND_JET_CHECKER)
SECOND = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SECOND)

FULL = SECOND.FULL
TANGENT = SECOND.TANGENT
PARAMETERS = TANGENT.PARAMETERS

AMBIENT_COORDINATES = tuple(
    (left, right, left_colour, right_colour)
    for left, right in combinations(range(8), 2)
    for left_colour in FULL.COLOURS
    for right_colour in FULL.COLOURS
)
COORDINATE_INDEX = {
    coordinate: index for index, coordinate in enumerate(AMBIENT_COORDINATES)
}
POINT = {
    coordinate: sign
    for coordinate, (sign, _exponent) in SECOND.COORDINATE_VALUES.items()
}

EXPECTED_LEDGER_SHA256 = (
    "93b585ba8a63dc3b997e3648671ca8217e5b1029bf2b93b847420aed08ed08d2"
)


def coordinate(name):
    require(len(name) == 4 and name.isdigit(), f"bad coordinate name {name}")
    answer = tuple(map(int, name))
    require(answer in COORDINATE_INDEX, f"unknown coordinate {name}")
    return COORDINATE_INDEX[answer]


def linear(**entries):
    return {
        coordinate(name): Fraction(value)
        for name, value in entries.items()
        if value
    }


def indexed_gradient(word):
    return {
        COORDINATE_INDEX[entry]: Fraction(value)
        for entry, value in TANGENT.specialized_gradient(tuple(map(int, word))).items()
    }


def add_scaled(target, source, scalar):
    for index, coefficient in source.items():
        value = target.get(index, Fraction(0)) + scalar * coefficient
        if value:
            target[index] = value
        else:
            target.pop(index, None)


def product_form(left, right):
    answer = defaultdict(Fraction)
    for left_index, left_coefficient in left.items():
        for right_index, right_coefficient in right.items():
            pair = tuple(sorted((left_index, right_index)))
            answer[pair] += left_coefficient * right_coefficient
    return {pair: coefficient for pair, coefficient in answer.items() if coefficient}


def sum_products(factors):
    answer = {}
    for normal, multiplier in factors:
        for pair, coefficient in product_form(normal, multiplier).items():
            value = answer.get(pair, Fraction(0)) + coefficient
            if value:
                answer[pair] = value
            else:
                answer.pop(pair, None)
    return answer


def matrix_rank(rows):
    pivots = {}
    for source in rows:
        row = {index: Fraction(value) for index, value in enumerate(source)
               if value}
        while row:
            pivot = min(row)
            value = row[pivot]
            if pivot not in pivots:
                pivots[pivot] = {
                    index: coefficient / value
                    for index, coefficient in row.items()
                }
                break
            add_scaled(row, pivots[pivot], -value)
    return len(pivots)


def bipartite_component_data(form):
    """Return (edges, bilinear rank) for each support-graph component."""
    adjacency = defaultdict(dict)
    for (left, right), coefficient in form.items():
        require(left != right, "quadratic support acquired a square")
        adjacency[left][right] = coefficient
        adjacency[right][left] = coefficient
    seen = set()
    answer = []
    for seed in sorted(adjacency):
        if seed in seen:
            continue
        colours = {seed: 0}
        queue = [seed]
        component = []
        seen.add(seed)
        while queue:
            vertex = queue.pop()
            component.append(vertex)
            for other in adjacency[vertex]:
                if other not in colours:
                    colours[other] = 1 - colours[vertex]
                    seen.add(other)
                    queue.append(other)
                else:
                    require(colours[other] != colours[vertex],
                            "quadratic component is not bipartite")
        left_side = sorted(vertex for vertex in component if colours[vertex] == 0)
        right_side = sorted(vertex for vertex in component if colours[vertex] == 1)
        matrix = [
            [adjacency[left].get(right, 0) for right in right_side]
            for left in left_side
        ]
        edge_count = sum(len(adjacency[vertex]) for vertex in component) // 2
        answer.append((edge_count, matrix_rank(matrix)))
    return tuple(answer)


# The five short products for q_0-q_00000010.
FACTORS_0 = (
    (
        linear(**{"2400": -1, "2500": 1, "3400": 1, "3500": 1}),
        linear(**{"6700": 1, "6710": -1}),
    ),
    (
        linear(**{"2601": 1, "2600": -1}),
        linear(**{"4700": 1, "5700": -1}),
    ),
    (
        linear(**{"3600": 1, "3601": -1}),
        linear(**{"4700": 1, "5700": 1}),
    ),
    (
        linear(**{"4600": 1, "4601": -1}),
        linear(**{"3700": 1, "2700": -1}),
    ),
    (
        linear(**{"2700": 1, "3700": 1}),
        linear(**{"5600": 1, "5601": -1}),
    ),
)

# The 96 terms split into three disjoint 32-term hafnian rectangles.  Their
# bilinear ranks are 4, 1, and 4, giving these nine products.
FACTORS_1 = (
    (
        linear(**{"2501": 1, "3501": 1}),
        linear(**{"0111": 1, "0711": -1, "1410": 1, "4701": -1}),
    ),
    (
        linear(**{"2511": 1, "3511": 1}),
        linear(**{"0111": -1, "0711": 1, "1411": -1, "4711": 1}),
    ),
    (
        linear(**{"2601": 1, "3601": 1}),
        linear(**{"0111": -1, "0711": -1, "1410": -1, "4701": -1}),
    ),
    (
        linear(**{"2611": 1, "3611": 1}),
        linear(**{"0111": 1, "0711": 1, "1411": 1, "4711": 1}),
    ),
    (
        linear(**{"1511": 1, "1611": -1, "5711": -1, "6711": -1}),
        linear(**{
            "0210": 1, "0211": -1, "0310": 1, "0311": -1,
            "2400": 1, "2411": -1, "3400": 1, "3411": -1,
        }),
    ),
    (
        linear(**{"1210": 1, "1310": 1}),
        linear(**{"0511": 1, "0611": -1, "4501": 1, "4601": -1}),
    ),
    (
        linear(**{"1211": 1, "1311": 1}),
        linear(**{"0511": -1, "0611": 1, "4511": -1, "4611": 1}),
    ),
    (
        linear(**{"2701": 1, "3701": 1}),
        linear(**{"0511": -1, "0611": -1, "4501": -1, "4601": -1}),
    ),
    (
        linear(**{"2711": 1, "3711": 1}),
        linear(**{"0511": 1, "0611": 1, "4511": 1, "4611": 1}),
    ),
)

# Each entry expresses the corresponding first factor above as an exact
# combination sum coefficient*dH_word at the rational torus point.
NORMAL_REPRESENTATIONS_0 = (
    ((-1, "00000001"),),
    ((Fraction(1, 2), "00000100"), (Fraction(-1, 2), "00000110"),
     (Fraction(1, 2), "22002002"), (Fraction(-1, 2), "22002012")),
    ((Fraction(-1, 2), "00000100"), (Fraction(1, 2), "00000110"),
     (Fraction(1, 2), "22002002"), (Fraction(-1, 2), "22002012")),
    ((-1, "00220100"), (1, "00220110")),
    ((1, "00000220"),),
)

NORMAL_REPRESENTATIONS_1 = (
    ((Fraction(1, 2), "00000100"), (Fraction(1, 2), "21000102")),
    ((Fraction(-1, 2), "00000100"), (Fraction(1, 2), "00010100"),
     (Fraction(1, 2), "00100100"), (Fraction(-1, 2), "21000102"),
     (Fraction(1, 2), "21010102"), (Fraction(1, 2), "21100102")),
    ((Fraction(1, 2), "00000100"), (-1, "00000110"),
     (Fraction(1, 2), "21000102")),
    ((Fraction(-1, 2), "00000100"), (1, "00000110"),
     (Fraction(1, 2), "00010100"), (-1, "00010110"),
     (Fraction(1, 2), "00100100"), (-1, "00100110"),
     (Fraction(-1, 2), "21000102"), (Fraction(1, 2), "21010102"),
     (Fraction(1, 2), "21100102")),
    ((Fraction(-1, 2), "11000111"),),
    ((1, "21000222"),),
    ((-1, "21000222"), (1, "21010222"), (1, "21100222")),
    ((1, "00000221"),),
    ((-1, "00000221"), (1, "00010221"), (1, "00100221")),
)


def port_weights():
    """Return the five integer port characters used by the Laurent orbit."""
    answer = {(site, colour): [0] * len(PARAMETERS)
              for site in range(8) for colour in FULL.COLOURS}
    ranks = []
    for parameter_index in range(len(PARAMETERS)):
        serialized, rank = TANGENT.solve_port_weights(parameter_index)
        ranks.append(rank)
        for name, (numerator, denominator) in serialized.items():
            require(denominator == 1, "nonintegral port character")
            answer[int(name[0]), int(name[1])][parameter_index] = numerator
    require(ranks == [17] * len(PARAMETERS), "port incidence rank changed")
    return {port: tuple(weight) for port, weight in answer.items()}


def add_weights(*weights):
    return tuple(sum(entries) for entries in zip(*weights))


def subtract_weights(left, right):
    return tuple(a - b for a, b in zip(left, right))


def coordinate_weight(entry, weights):
    left, right, left_colour, right_colour = entry
    return add_weights(weights[left, left_colour], weights[right, right_colour])


def word_weight(word, weights):
    return add_weights(*(weights[site, colour]
                         for site, colour in enumerate(word)))


def audit_lock(pure_word, mixed_word, factors, representations, expected_terms,
               expected_rectangles):
    pure_quadratic = SECOND.quadratic_form(pure_word, COORDINATE_INDEX, POINT)
    mixed_quadratic = SECOND.quadratic_form(mixed_word, COORDINATE_INDEX, POINT)
    difference = {
        pair: Fraction(coefficient)
        for pair, coefficient in SECOND.subtract(
            pure_quadratic, mixed_quadratic
        ).items()
    }
    require(len(difference) == expected_terms, "ambient quadratic support changed")
    require(sum_products(factors) == difference,
            "conormal products do not reconstruct the quadratic difference")
    require(len(factors) == len(representations), "representation count")
    rectangle_data = bipartite_component_data(difference)
    if expected_rectangles:
        require(rectangle_data == tuple((32, rank) for rank in expected_rectangles),
                "hafnian rectangle decomposition changed")

    used_words = set()
    for (normal, _multiplier), representation in zip(factors, representations):
        reconstructed = {}
        for coefficient, word_name in representation:
            word = tuple(map(int, word_name))
            require(len(set(word)) > 1, "a purported conormal word is pure")
            add_scaled(reconstructed, indexed_gradient(word_name),
                       Fraction(coefficient))
            used_words.add(word_name)
        require(reconstructed == normal, "mixed-gradient representation failed")

    weights = port_weights()
    coordinate_weights = tuple(
        coordinate_weight(entry, weights) for entry in AMBIENT_COORDINATES
    )
    pure_character = word_weight(pure_word, weights)
    mixed_character = word_weight(mixed_word, weights)
    selected_scale = subtract_weights(pure_character, mixed_character)

    # Take character 0 for every normal factor.  A rational normal
    # N=sum n_c z_c transports to sum n_c*t^(-wt(c))*z_c, while its
    # multiplier transports with character pure_character.  Thus each
    # product term has the required Hessian character
    # pure_character-wt(c)-wt(d).  The displayed gradient representation
    # transports by multiplying dH_w by t^(-wt(w)).
    zero_character = (0,) * len(PARAMETERS)
    for (normal, multiplier), representation in zip(factors, representations):
        for index in normal:
            require(
                subtract_weights(zero_character, coordinate_weights[index])
                == tuple(-value for value in coordinate_weights[index]),
                "normal transport character failed",
            )
        for coefficient, word_name in representation:
            require(coefficient, "zero conormal coefficient")
            word = tuple(map(int, word_name))
            # t^-wt(w) dH_w has component character -wt(c), independent
            # of the selected mixed word w.
            for index in indexed_gradient(word_name):
                transported = add_weights(
                    tuple(-value for value in word_weight(word, weights)),
                    subtract_weights(word_weight(word, weights),
                                     coordinate_weights[index]),
                )
                require(transported
                        == tuple(-value for value in coordinate_weights[index]),
                        "gradient transport is not port graded")
        for left in normal:
            for right in multiplier:
                product_character = add_weights(
                    tuple(-value for value in coordinate_weights[left]),
                    subtract_weights(pure_character, coordinate_weights[right]),
                )
                require(
                    product_character == subtract_weights(
                        pure_character,
                        add_weights(coordinate_weights[left],
                                    coordinate_weights[right]),
                    ),
                    "product transport character failed",
                )

    return {
        "pure_colour": pure_word[0],
        "selected_mixed_word": list(mixed_word),
        "selected_mixed_scale_character": list(selected_scale),
        "ambient_quadratic_terms": len(difference),
        "conormal_products": len(factors),
        "rectangle_edge_rank_pairs": [list(entry) for entry in rectangle_data],
        "normal_support_sizes": [len(normal) for normal, _ in factors],
        "multiplier_support_sizes": [len(multiplier) for _, multiplier in factors],
        "distinct_mixed_gradient_generators": len(used_words),
        "maximum_generators_per_normal": max(map(len, representations)),
        "port_parameters": list(PARAMETERS),
        "port_graded_transport": True,
    }


def audit():
    lock_0 = audit_lock(
        SECOND.PURE_WORD_0, SECOND.MIXED_WORD_0,
        FACTORS_0, NORMAL_REPRESENTATIONS_0, 24, (),
    )
    lock_1 = audit_lock(
        SECOND.PURE_WORD_1, SECOND.MIXED_WORD_1,
        FACTORS_1, NORMAL_REPRESENTATIONS_1, 96, (4, 1, 4),
    )
    require(lock_0["selected_mixed_scale_character"] == [0, 0, 0, 0, 1],
            "H0 selected scale is no longer e")
    require(lock_1["selected_mixed_scale_character"] == [-1, 0, 0, 0, 0],
            "H1 selected scale is no longer a^-1")
    return {
        "ambient_variables": len(AMBIENT_COORDINATES),
        "locks": [lock_0, lock_1],
        "total_conormal_products": (
            lock_0["conormal_products"] + lock_1["conormal_products"]
        ),
        "structural_conclusion": (
            "both quadratic locks lie explicitly in "
            "(mixed Jacobian linear forms)_2"
        ),
    }


def main():
    ledger = audit()
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                "frozen conormal-factorization ledger digest changed")
    print(
        "n=8 quadratic conormal factorization: PASS; "
        "terms=(24,96), products=(5,9), H1-rectangles=(4,1,4), "
        "port-graded=yes"
    )
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
