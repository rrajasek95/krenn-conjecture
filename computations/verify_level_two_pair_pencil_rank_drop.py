#!/usr/bin/env python3
"""Exact audit of the pair-pencil rank drop in a six-vertex L2 block.

Research evidence only. Krenn's conjecture remains open and no certified
dependency changes.

In the four-live/two-dead normal form forced by the pair-pencil rule, write

    M[x,4] = u_x e_{sigma_x}^T,
    M[x,5] = v_x e_{1-sigma_x}^T,
    M[4,5] = 0                         (x = 0,1,2,3).

This checker proves, as formal polynomial identities in the sixteen entries
of u_x and v_x, that dPsi_M has an extra kernel direction supported only on
the live-live edges for every sigma in {0,1}^4. For a 2+2 split it proves two
such directions. Together with the five trace-zero vertex-scaling directions
this gives rank(dPsi_M) <= 54, sharpened to <= 53 in the 2+2 case.

The proof checks 1,408 formal row identities, all 16 support assignments, the
five universal scaling identities, generic independence of the displayed
directions, and exact rank calibrations 35/49/53 for the 4+0, 3+1 and 2+2
assignment types. Standard library only; exact integer/Fraction arithmetic;
live under python -O and python -I -S.
"""

from collections import Counter
from fractions import Fraction as Q
from itertools import combinations, product


def require(condition, message):
    if not condition:
        raise AssertionError(message)


VERTICES = tuple(range(6))
LIVE = tuple(range(4))
DEAD = (4, 5)
COLORS = (0, 1)
EDGES = tuple(combinations(VERTICES, 2))
CELLS = tuple((x, y, a, b) for x, y in EDGES
              for a in COLORS for b in COLORS)
WORDS = tuple(product(COLORS, repeat=6))


def matchings(vertices):
    if not vertices:
        return ((),)
    x = vertices[0]
    out = []
    for slot in range(1, len(vertices)):
        y = vertices[slot]
        rest = vertices[1:slot] + vertices[slot + 1:]
        for tail in matchings(rest):
            out.append(((x, y),) + tail)
    return tuple(out)


MATCHINGS = {subset: matchings(subset)
             for size in (0, 2, 4, 6)
             for subset in combinations(VERTICES, size)}


def canonical_cell(x, y, a, b):
    if x > y:
        x, y, a, b = y, x, b, a
    return x, y, a, b


def poly_var(name):
    return Counter({(name,): 1})


def poly_add(*polys):
    out = Counter()
    for poly in polys:
        out.update(poly)
    return Counter({monomial: coefficient for monomial, coefficient in out.items()
                    if coefficient})


def poly_scale(poly, scalar):
    return Counter({monomial: scalar * coefficient
                    for monomial, coefficient in poly.items()
                    if scalar * coefficient})


def poly_mul(first, second):
    out = Counter()
    for left, a in first.items():
        for right, b in second.items():
            out[tuple(sorted(left + right))] += a * b
    return Counter({monomial: coefficient for monomial, coefficient in out.items()
                    if coefficient})


def edge(table, x, y, a, b):
    return table.get(canonical_cell(x, y, a, b), Counter())


def put(table, x, y, a, b, value):
    key = canonical_cell(x, y, a, b)
    table[key] = poly_add(table.get(key, Counter()), value)


def live_dead_packet(sigma):
    packet = {}
    u = {(x, a): poly_var(("u", x, a)) for x in LIVE for a in COLORS}
    v = {(x, a): poly_var(("v", x, a)) for x in LIVE for a in COLORS}
    for x in LIVE:
        for a, b in product(COLORS, repeat=2):
            if b == sigma[x]:
                put(packet, x, 4, a, b, u[x, a])
            if b == 1 - sigma[x]:
                put(packet, x, 5, a, b, v[x, a])
    return packet, u, v


def cofactor(packet, word, x, y):
    rest = tuple(vertex for vertex in VERTICES if vertex not in (x, y))
    out = Counter()
    for matching in MATCHINGS[rest]:
        term = Counter({(): 1})
        for left, right in matching:
            term = poly_mul(term, edge(packet, left, right,
                                       word[left], word[right]))
        out = poly_add(out, term)
    return out


def differential(packet, tangent, word):
    out = Counter()
    for x, y in EDGES:
        value = edge(tangent, x, y, word[x], word[y])
        if value:
            out = poly_add(out, poly_mul(value, cofactor(packet, word, x, y)))
    return out


def omega(u, v, x, y, a, b):
    return poly_add(poly_mul(u[x, a], v[y, b]),
                    poly_scale(poly_mul(v[x, a], u[y, b]), -1))


def triangle_direction(u, v, triple):
    i, j, k = triple
    tangent = {}
    for (x, y), sign in (((i, j), 1), ((i, k), -1), ((j, k), 1)):
        for a, b in product(COLORS, repeat=2):
            put(tangent, x, y, a, b,
                poly_scale(omega(u, v, x, y, a, b), sign))
    return tangent


def balanced_directions(u, v, sigma):
    zero_side = tuple(x for x in LIVE if sigma[x] == 0)
    one_side = tuple(x for x in LIVE if sigma[x] == 1)
    require(len(zero_side) == len(one_side) == 2, "not a balanced assignment")
    signs_zero = {zero_side[0]: 1, zero_side[1]: -1}
    signs_one = {one_side[0]: 1, one_side[1]: -1}
    ku, kv = {}, {}
    for x in zero_side:
        for y in one_side:
            sign = signs_zero[x] * signs_one[y]
            for a, b in product(COLORS, repeat=2):
                put(ku, x, y, a, b,
                    poly_scale(poly_mul(u[x, a], u[y, b]), sign))
                put(kv, x, y, a, b,
                    poly_scale(poly_mul(v[x, a], v[y, b]), sign))
    return ku, kv


def evaluate(poly, values):
    total = Q(0)
    for monomial, coefficient in poly.items():
        term = Q(coefficient)
        for variable in monomial:
            term *= values[variable]
        total += term
    return total


def vector_support_at(tangent, values):
    return {cell for cell in CELLS
            if evaluate(tangent.get(cell, Counter()), values)}


def audit_formal_extra_directions():
    checked = 0
    categories = Counter()
    canonical_values = {}
    for x in LIVE:
        canonical_values[("u", x, 0)] = Q(1)
        canonical_values[("u", x, 1)] = Q(0)
        canonical_values[("v", x, 0)] = Q(0)
        canonical_values[("v", x, 1)] = Q(1)

    for sigma in product(COLORS, repeat=4):
        packet, u, v = live_dead_packet(sigma)
        fibres = {color: tuple(x for x in LIVE if sigma[x] == color)
                  for color in COLORS}
        sizes = tuple(sorted((len(fibres[0]), len(fibres[1])), reverse=True))
        categories[sizes] += 1
        if sizes == (2, 2):
            directions = balanced_directions(u, v, sigma)
            supports = [vector_support_at(direction, canonical_values)
                        for direction in directions]
            require(all(supports), ("a balanced direction specialized to zero", sigma))
            require(supports[0].isdisjoint(supports[1]),
                    ("balanced directions are not visibly independent", sigma))
        else:
            majority = max(fibres.values(), key=len)
            directions = (triangle_direction(u, v, majority[:3]),)
            require(vector_support_at(directions[0], canonical_values),
                    ("the triangle direction specialized to zero", sigma))

        for number, direction in enumerate(directions):
            require(all(y < 4 for x, y, a, b in direction),
                    "an extra direction left the live-live subspace")
            for word in WORDS:
                require(not differential(packet, direction, word),
                        ("extra direction is not in ker dPsi", sigma, number, word))
                checked += 1

    require(categories == Counter({(3, 1): 8, (2, 2): 6, (4, 0): 2}),
            ("wrong assignment census", categories))
    require(checked == 1408, ("wrong formal identity count", checked))
    return checked, categories


def rational_rank(matrix):
    rows = [[Q(value) for value in row] for row in matrix]
    rank = 0
    width = len(rows[0]) if rows else 0
    for column in range(width):
        pivot = next((slot for slot in range(rank, len(rows))
                      if rows[slot][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        scale = rows[rank][column]
        rows[rank] = [value / scale for value in rows[rank]]
        for slot in range(len(rows)):
            if slot == rank or not rows[slot][column]:
                continue
            multiple = rows[slot][column]
            rows[slot] = [a - multiple * b
                          for a, b in zip(rows[slot], rows[rank])]
        rank += 1
        if rank == len(rows):
            break
    return rank


def audit_scaling_kernel_and_transversality():
    perfect_matchings = MATCHINGS[VERTICES]
    require(len(perfect_matchings) == 15, "K6 must have fifteen perfect matchings")
    for basis in range(5):
        mu = [Q(0)] * 6
        mu[basis] = Q(1)
        mu[5] = Q(-1)
        require(sum(mu) == 0, "scaling vector is not trace zero")
        for matching in perfect_matchings:
            multiplier = sum(mu[x] + mu[y] for x, y in matching)
            require(multiplier == 0,
                    ("a trace-zero scaling changes a matching monomial",
                     basis, matching))

    equations = []
    for x in LIVE:
        for dead in DEAD:
            row = [Q(0)] * 6
            row[x] = row[dead] = Q(1)
            equations.append(row)
    equations.append([Q(1)] * 6)
    require(rational_rank(equations) == 6,
            "a nonzero trace-zero scaling can hide on live-live edges")


def numeric_packet(sigma):
    packet = {}
    for x, y in combinations(LIVE, 2):
        for a, b in product(COLORS, repeat=2):
            packet[canonical_cell(x, y, a, b)] = Q(1 if a != b else 0)
    for x in LIVE:
        u = (Q(4 * x + 2), Q(4 * x + 3))
        v = (Q(4 * x + 4), Q(4 * x + 5))
        for a, b in product(COLORS, repeat=2):
            if b == sigma[x]:
                packet[canonical_cell(x, 4, a, b)] = u[a]
            if b == 1 - sigma[x]:
                packet[canonical_cell(x, 5, a, b)] = v[a]
    return packet


def numeric_hafnian(packet, word, vertices):
    total = Q(0)
    for matching in MATCHINGS[tuple(sorted(vertices))]:
        term = Q(1)
        for x, y in matching:
            term *= packet.get(canonical_cell(x, y, word[x], word[y]), Q(0))
        total += term
    return total


def numeric_differential(packet):
    rows = []
    for word in WORDS:
        row = [Q(0)] * len(CELLS)
        for index, (x, y, a, b) in enumerate(CELLS):
            if word[x] == a and word[y] == b:
                rest = tuple(vertex for vertex in VERTICES
                             if vertex not in (x, y))
                row[index] = numeric_hafnian(packet, word, rest)
        rows.append(row)
    return rows


def audit_rank_calibration():
    expected = {
        (0, 0, 0, 0): 35,
        (0, 0, 0, 1): 49,
        (0, 0, 1, 1): 53,
    }
    found = {sigma: rational_rank(numeric_differential(numeric_packet(sigma)))
             for sigma in expected}
    require(found == expected, ("rank calibration changed", found))
    return found


def main():
    checked, categories = audit_formal_extra_directions()
    audit_scaling_kernel_and_transversality()
    ranks = audit_rank_calibration()
    print("level-two pair-pencil rank drop: all checks passed")
    print("  formal extra-kernel identities :", checked)
    print("  assignment types               :", dict(sorted(categories.items())))
    print("  exact calibration ranks        :", ranks)
    print("  theorem                         : rank dPsi <= 54 in all 16 cases")
    print("                                    rank dPsi <= 53 in every 2+2 case")
    print("  status                          : research evidence; conjecture open")


if __name__ == "__main__":
    main()
