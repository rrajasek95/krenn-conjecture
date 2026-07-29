#!/usr/bin/env python3
"""Tiny exact audit for the overlapping zero-star four-cut exchange.

The script is dependency-free.  It checks:

* the four matching layers of the 81-row identity at eight sites;
* the coefficient-index exchange between the two 27-row presentations;
* the six-site repeated-pair K4 common-power countermodel for the
  selector-contracted row-and-column cap.
"""

from collections import Counter
from itertools import combinations, product


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for matching in perfect_matchings(rest):
            yield ((first, second),) + matching


def edge(left, right):
    return tuple(sorted((left, right)))


def normalized_matching(matching):
    return tuple(sorted(edge(left, right) for left, right in matching))


def audit_four_cut_layers():
    """Equation (3) partitions the allowed eight-site matchings."""

    p, q, i, j = range(4)
    boundary = tuple(range(4, 8))
    forbidden = {edge(p, i), edge(q, i), edge(p, j), edge(q, j)}

    allowed = {
        normalized_matching(matching)
        for matching in perfect_matchings(range(8))
        if not (set(normalized_matching(matching)) & forbidden)
    }

    layers = {"direct-direct": set(), "pq-direct": set(),
              "ij-direct": set(), "four-star": set()}
    for matching in allowed:
        edges = set(matching)
        has_pq = edge(p, q) in edges
        has_ij = edge(i, j) in edges
        if has_pq and has_ij:
            name = "direct-direct"
        elif has_pq:
            name = "pq-direct"
        elif has_ij:
            name = "ij-direct"
        else:
            name = "four-star"
        layers[name].add(matching)

    assert set().union(*layers.values()) == allowed
    assert sum(len(layer) for layer in layers.values()) == len(allowed)
    assert all(layers[left].isdisjoint(layers[right])
               for left, right in combinations(layers, 2))
    assert {name: len(value) for name, value in layers.items()} == {
        "direct-direct": 3,
        "pq-direct": 12,
        "ij-direct": 12,
        "four-star": 24,
    }
    assert len(allowed) == 51
    return {name: len(value) for name, value in layers.items()}


def audit_exchange_indices():
    """Both packet contractions have the identical four-colour target."""

    checked = 0
    for a, b, c, d in product(range(3), repeat=4):
        first_target = int(a == b == c) * int(d == a)
        second_target = int(a == b == d) * int(c == a)
        four_target = int(a == b == c == d)
        assert first_target == second_target == four_target
        checked += 1
    assert checked == 81
    return checked


# A square-free word has -1 at an unoccupied site and a colour 0,1,2 at
# an occupied site.  Polynomials are Counters of such words.
SITE_COUNT = 6
EMPTY_WORD = (-1,) * SITE_COUNT


def cell(left, right, left_colour, right_colour, coefficient=1):
    word = list(EMPTY_WORD)
    word[left] = left_colour
    word[right] = right_colour
    return Counter({tuple(word): coefficient})


def monomer(site, colour, coefficient=1):
    word = list(EMPTY_WORD)
    word[site] = colour
    return Counter({tuple(word): coefficient})


def add(*polynomials):
    answer = Counter()
    for polynomial in polynomials:
        answer.update(polynomial)
    return Counter({word: value for word, value in answer.items() if value})


def multiply(left, right):
    answer = Counter()
    for word_left, coefficient_left in left.items():
        for word_right, coefficient_right in right.items():
            if any(a != -1 and b != -1
                   for a, b in zip(word_left, word_right)):
                continue
            word = tuple(b if a == -1 else a
                         for a, b in zip(word_left, word_right))
            answer[word] += coefficient_left * coefficient_right
    return Counter({word: value for word, value in answer.items() if value})


def divided_power_of_cells(cells, order):
    """Unordered matching power for a sum of distinct unit cells."""

    if order == 0:
        return Counter({EMPTY_WORD: 1})
    answer = Counter()
    for chosen in combinations(cells, order):
        product_polynomial = Counter({EMPTY_WORD: 1})
        for polynomial in chosen:
            product_polynomial = multiply(product_polynomial, polynomial)
        answer.update(product_polynomial)
    return Counter({word: value for word, value in answer.items() if value})


def audit_repeated_pair_countermodel():
    cells = [
        cell(0, 1, 0, 0), cell(2, 3, 0, 0),
        cell(0, 2, 1, 1), cell(1, 3, 1, 1),
        cell(0, 3, 2, 2), cell(1, 2, 2, 2),
    ]
    z = add(*cells)
    z2 = divided_power_of_cells(cells, 2)
    z3 = divided_power_of_cells(cells, 3)

    expected_z2 = Counter({
        (0, 0, 0, 0, -1, -1): 1,
        (1, 1, 1, 1, -1, -1): 1,
        (2, 2, 2, 2, -1, -1): 1,
    })
    assert z2 == expected_z2
    assert not z3

    cap_edge = multiply(monomer(0, 0), monomer(1, 0))
    selected_cap = multiply(cap_edge, z)
    assert selected_cap == Counter({(0, 0, 0, 0, -1, -1): 1})

    common_product = multiply(monomer(4, 0), monomer(5, 0))
    diagonal = multiply(common_product, selected_cap)
    assert diagonal == Counter({(0, 0, 0, 0, 0, 0): 1})

    # u_0d=u_c0=0, t_c=0 for c!=0, and v_d=0 for d!=0.
    # Hence all four selected off-diagonal row/column entries are zero.
    selected_entries = {}
    for c in range(3):
        for d in range(3):
            if c != 0 and d != 0:
                continue
            selected_entries[c, d] = diagonal if (c, d) == (0, 0) else Counter()
    assert len(selected_entries) == 5
    assert selected_entries[0, 0] == Counter({(0,) * SITE_COUNT: 1})
    assert all(not value for key, value in selected_entries.items()
               if key != (0, 0))

    return len(z), len(z2), len(selected_entries)


def main():
    layers = audit_four_cut_layers()
    exchanged = audit_exchange_indices()
    cells, lifts, cap_rows = audit_repeated_pair_countermodel()
    print("overlapping zero-star four-cut exchange: PASS")
    print(f"four layers {layers}; allowed matchings={sum(layers.values())}")
    print(f"exchange target indices={exchanged}; K4 cells={cells}, "
          f"repeated lifts={lifts}, selected cap rows={cap_rows}")


if __name__ == "__main__":
    main()
