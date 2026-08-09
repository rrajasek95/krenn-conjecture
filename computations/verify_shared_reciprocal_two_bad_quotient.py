#!/usr/bin/env python3
"""Exact audit of the two-bad shared-reciprocal cofactor quotient.

The checker freezes a rational five-site matching power whose cofactor map
contains two pure tensors, has a genuine kernel, and has a nonzero bilinear
kernel product outside its image.  It also reconstructs the corresponding
q/r six-site cofactors from the same block family.  This is a source-faithful
cofactor packet, not an eight-site exact source.
"""

from __future__ import annotations

import itertools
from collections import defaultdict

import sympy as sp


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        edge = tuple(sorted((first, second)))
        for matching in perfect_matchings(rest):
            yield (edge,) + matching


def matching_tensor(vertices, cells):
    vertices = tuple(vertices)
    answer = defaultdict(lambda: sp.S.Zero)
    for matching in perfect_matchings(vertices):
        choices = []
        for edge in matching:
            entries = [
                (left, right, value)
                for (candidate, left, right), value in cells.items()
                if candidate == edge and value != 0
            ]
            if not entries:
                break
            choices.append(entries)
        else:
            for selected in itertools.product(*choices):
                colouring = {}
                coefficient = sp.S.One
                for edge, (left, right, value) in zip(matching, selected):
                    colouring[edge[0]] = left
                    colouring[edge[1]] = right
                    coefficient *= value
                word = tuple(colouring[site] for site in vertices)
                answer[word] += coefficient
    return {word: sp.simplify(value) for word, value in answer.items()
            if value != 0}


def put(cells, u, v, left, right, value):
    edge = tuple(sorted((u, v)))
    if u > v:
        left, right = right, left
    key = (edge, left, right)
    cells[key] = sp.simplify(cells.get(key, 0) + value)
    if cells[key] == 0:
        del cells[key]


def insert_missing(cofactor, cofactor_sites, missing, vector):
    sites = tuple(sorted(cofactor_sites + (missing,)))
    out = defaultdict(lambda: sp.S.Zero)
    for word, coefficient in cofactor.items():
        partial = dict(zip(cofactor_sites, word))
        for colour, value in vector.items():
            full = dict(partial)
            full[missing] = colour
            out[tuple(full[site] for site in sites)] += coefficient * value
    return {word: sp.simplify(value) for word, value in out.items() if value != 0}


def add_tensors(*tensors):
    out = defaultdict(lambda: sp.S.Zero)
    for tensor in tensors:
        for word, value in tensor.items():
            out[word] += value
    return {word: sp.simplify(value) for word, value in out.items() if value != 0}


def restrict_controller_slice(tensor, vertices, fixed):
    remaining = tuple(site for site in vertices if site not in fixed)
    out = {}
    for word, value in tensor.items():
        colouring = dict(zip(vertices, word))
        if any(colouring[site] != colour for site, colour in fixed.items()):
            continue
        reduced = tuple(colouring[site] for site in remaining)
        out[reduced] = sp.simplify(out.get(reduced, 0) + value)
    return {word: value for word, value in out.items() if value != 0}


def audit_binary_common_power_packet():
    # This is the genuine common power from
    # simultaneous-star-syzygy-boundary.md, with controller zero removed.
    c = sp.Rational(3, 5)
    s = sp.Rational(4, 5)
    C = (1, 2, 3, 4, 5)
    cells = {}
    for u, v, colour, value in (
        (2, 3, 0, c),
        (1, 3, 0, s),
        (4, 5, 0, 1),
        (1, 2, 1, 1),
        (3, 4, 1, 1),
    ):
        put(cells, u, v, colour, colour, value)

    cofactors = {
        x: matching_tensor(tuple(site for site in C if site != x), cells)
        for x in C
    }
    basis = tuple(itertools.product(range(3), repeat=5))
    labels = []
    columns = []
    for x in C:
        sites = tuple(site for site in C if site != x)
        for colour in range(3):
            labels.append((x, colour))
            tensor = insert_missing(cofactors[x], sites, x, {colour: 1})
            columns.append(sp.Matrix([tensor.get(word, 0) for word in basis]))
    Phi = sp.Matrix.hstack(*columns)
    require(Phi.rank() == 11, "binary cofactor-map rank changed")
    require(len(Phi.nullspace()) == 4, "binary cofactor nullity changed")

    X = {
        colour: sp.Matrix([int(word == (colour,) * 5) for word in basis])
        for colour in range(3)
    }
    preimage0 = sp.zeros(15, 1)
    preimage0[labels.index((1, 0))] = c
    preimage0[labels.index((2, 0))] = s
    preimage1 = sp.zeros(15, 1)
    preimage1[labels.index((5, 1))] = 1
    require(Phi * preimage0 == X[0], "pure zero left the image")
    require(Phi * preimage1 == X[1], "pure one left the image")
    require(Phi.row_join(X[2]).rank() == 12,
            "third pure tensor entered the cofactor image")

    kernel = sp.zeros(15, 1)
    kernel[labels.index((1, 0))] = s
    kernel[labels.index((2, 0))] = -c
    require(Phi * kernel == sp.zeros(len(basis), 1),
            "displayed signed kernel ceased to vanish")

    # Trilinear first-response tensor T(P,U,V)=P U V q.  Take U=V equal to
    # the genuine signed cofactor kernel and P=e_2 at site 3.  The two ordered
    # routes leave the same internal 45:00 edge and add rather than cancel.
    P = {3: {2: sp.S.One}}
    U = {1: {0: s}, 2: {0: -c}}
    V = {1: {0: s}, 2: {0: -c}}
    trilinear = defaultdict(lambda: sp.S.Zero)
    for x, pvector in P.items():
        for y, uvector in U.items():
            for z, vvector in V.items():
                if len({x, y, z}) < 3:
                    continue
                remaining = tuple(site for site in C if site not in (x, y, z))
                require(len(remaining) == 2, "five-site complement changed")
                edge = tuple(sorted(remaining))
                for (candidate, left, right), edge_value in cells.items():
                    if candidate != edge:
                        continue
                    for px, pv in pvector.items():
                        for uy, uv in uvector.items():
                            for vz, vv in vvector.items():
                                colouring = {x: px, y: uy, z: vz,
                                            edge[0]: left, edge[1]: right}
                                word = tuple(colouring[site] for site in C)
                                trilinear[word] += pv * uv * vv * edge_value
    trilinear = {word: sp.simplify(value)
                 for word, value in trilinear.items() if value != 0}
    expected_word = (0, 0, 2, 0, 0)
    require(trilinear == {expected_word: -sp.Rational(24, 25)},
            "trilinear kernel class changed")
    trilinear_vector = sp.Matrix([trilinear.get(word, 0) for word in basis])
    require(Phi.row_join(trilinear_vector).rank() == 12,
            "trilinear class fell into the cofactor image")

    # Reconstruct the same class from literal six-site cofactors.  The q and
    # r stars each contain their pure row plus the displayed colour-2 kernel
    # row.  Therefore H_{qC}=X_1 and H_{rC}=X_0 exactly, while their (2,2)
    # pair slices produce the trilinear tensor above.
    q, r, t = 6, 7, 2
    extended = dict(cells)
    put(extended, q, 5, 1, 1, 1)
    put(extended, r, 1, 0, 0, c)
    put(extended, r, 2, 0, 0, s)
    for site, vector in U.items():
        for endpoint_colour, value in vector.items():
            put(extended, q, site, t, endpoint_colour, value)
    for site, vector in V.items():
        for endpoint_colour, value in vector.items():
            put(extended, r, site, t, endpoint_colour, value)

    q_top = matching_tensor((q,) + C, extended)
    r_top = matching_tensor((r,) + C, extended)
    require(q_top == {(1,) * 6: 1}, "q pure deletion changed")
    require(r_top == {(0,) * 6: 1}, "r pure deletion changed")

    reconstructed = {}
    for x, pvector in P.items():
        vertices = (q, r) + tuple(site for site in C if site != x)
        cofactor = matching_tensor(vertices, extended)
        sliced = restrict_controller_slice(cofactor, vertices, {q: t, r: t})
        sites = tuple(site for site in C if site != x)
        reconstructed = add_tensors(
            reconstructed, insert_missing(sliced, sites, x, pvector))
    require(reconstructed == trilinear,
            "literal six-site cofactor reconstruction changed")

    return Phi.rank(), len(Phi.nullspace()), trilinear


def main():
    rank, nullity, trilinear = audit_binary_common_power_packet()
    print("shared reciprocal two-bad cofactor quotient: PASS")
    print(f"common cofactor map rank/nullity={rank}/{nullity}")
    print("pure image colours=0,1; excluded pure colour=2")
    print(f"source-faithful kernel product={trilinear}")
    print("literal q/r pure deletions and six-site cofactors reconstructed")


if __name__ == "__main__":
    main()
