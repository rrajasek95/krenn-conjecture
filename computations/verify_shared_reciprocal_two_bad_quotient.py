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
from collections import Counter, defaultdict
from hashlib import sha256

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

    # Exhaust the stronger *linear-span* oracle at this actual common power:
    # im(Phi) plus every P*U*V*q with U,V in ker(Phi).  This is only 15*4^2
    # exact columns.  It tests the finite theorem-completing invariant without
    # sampling coefficients.
    def vector_as_rows(vector):
        rows = {}
        for index, value in enumerate(vector):
            if value:
                site, colour = labels[index]
                rows.setdefault(site, {})[colour] = value
        return rows

    def kernel_product(P_rows, U_rows, V_rows):
        tensor = defaultdict(lambda: sp.S.Zero)
        for x, pvector in P_rows.items():
            for y, uvector in U_rows.items():
                for z, vvector in V_rows.items():
                    if len({x, y, z}) < 3:
                        continue
                    remaining = tuple(
                        site for site in C if site not in (x, y, z)
                    )
                    edge = tuple(sorted(remaining))
                    for (candidate, left, right), edge_value in cells.items():
                        if candidate != edge:
                            continue
                        for px, pv in pvector.items():
                            for uy, uv in uvector.items():
                                for vz, vv in vvector.items():
                                    colouring = {
                                        x: px, y: uy, z: vz,
                                        edge[0]: left, edge[1]: right,
                                    }
                                    word = tuple(colouring[site] for site in C)
                                    tensor[word] += pv * uv * vv * edge_value
        return sp.Matrix([sp.simplify(tensor[word]) for word in basis])

    product_columns = []
    kernel_basis = Phi.nullspace()
    for p_index in range(len(labels)):
        p_vector = sp.zeros(len(labels), 1)
        p_vector[p_index] = 1
        P_rows = vector_as_rows(p_vector)
        for U_vector in kernel_basis:
            U_rows = vector_as_rows(U_vector)
            for V_vector in kernel_basis:
                product_columns.append(
                    kernel_product(P_rows, U_rows, vector_as_rows(V_vector))
                )
    product_matrix = sp.Matrix.hstack(*product_columns)
    augmented = Phi.row_join(product_matrix)
    pure_matrix = sp.Matrix.hstack(X[0], X[1], X[2])
    phi_pure_intersection = (
        Phi.rank() + 3 - Phi.row_join(pure_matrix).rank()
    )
    augmented_pure_intersection = (
        augmented.rank() + 3 - augmented.row_join(pure_matrix).rank()
    )
    require(phi_pure_intersection == 2,
            "binary cofactor pure-image intersection changed")
    require(augmented_pure_intersection == 2,
            "binary kernel products acquired a new pure class")

    return (Phi.rank(), len(Phi.nullspace()), trilinear,
            augmented.rank(), augmented_pure_intersection)


def audit_one_cell_pure_survivors(base_kind):
    """Exact one-cell falsification around the sparse binary C6 source.

    This is a bounded structural test, not a coefficient grid: every possible
    endpoint-coloured internal cell is adjoined with an independent nonzero
    unit, and we retain exactly those supports for which both old pure tensors
    remain in the common-cofactor image.
    """

    C = (1, 2, 3, 4, 5)
    base = {}
    if base_kind == "Hamilton":
        for u, v, colour in ((2, 3, 0), (4, 5, 0),
                             (1, 2, 1), (3, 4, 1)):
            put(base, u, v, colour, colour, 1)
    elif base_kind == "Pythagorean":
        c = sp.Rational(3, 5)
        s = sp.Rational(4, 5)
        for u, v, colour, value in (
            (2, 3, 0, c), (1, 3, 0, s), (4, 5, 0, 1),
            (1, 2, 1, 1), (3, 4, 1, 1),
        ):
            put(base, u, v, colour, colour, value)
    else:
        raise AssertionError(f"unknown one-cell base {base_kind}")
    basis = tuple(itertools.product(range(3), repeat=5))
    pure = {
        colour: sp.Matrix([int(word == (colour,) * 5) for word in basis])
        for colour in range(3)
    }

    torus_labels = tuple(itertools.product(C, range(3)))

    def cell_character(key):
        edge, left, right = key
        vector = sp.zeros(len(torus_labels), 1)
        vector[torus_labels.index((edge[0], left))] += 1
        vector[torus_labels.index((edge[1], right))] += 1
        return vector

    base_characters = sp.Matrix.hstack(*(
        cell_character(key) for key in base
    ))
    require(base_characters.rank() == len(base),
            f"{base_kind} base torus characters became dependent")

    def matrix_for(cells):
        columns = []
        labels = []
        for x in C:
            sites = tuple(site for site in C if site != x)
            cofactor = matching_tensor(sites, cells)
            for colour in range(3):
                labels.append((x, colour))
                tensor = insert_missing(cofactor, sites, x, {colour: 1})
                columns.append(
                    sp.Matrix([tensor.get(word, 0) for word in basis])
                )
        return sp.Matrix.hstack(*columns), labels

    def vector_as_rows(vector, labels):
        rows = {}
        for index, value in enumerate(vector):
            if value:
                site, colour = labels[index]
                rows.setdefault(site, {})[colour] = value
        return rows

    def product_column(cells, P_rows, U_rows, V_rows):
        tensor = defaultdict(lambda: sp.S.Zero)
        for x, pvector in P_rows.items():
            for y, uvector in U_rows.items():
                for z, vvector in V_rows.items():
                    if len({x, y, z}) < 3:
                        continue
                    edge = tuple(sorted(
                        site for site in C if site not in (x, y, z)
                    ))
                    for (candidate, left, right), edge_value in cells.items():
                        if candidate != edge:
                            continue
                        for px, pv in pvector.items():
                            for uy, uv in uvector.items():
                                for vz, vv in vvector.items():
                                    colours = {
                                        x: px, y: uy, z: vz,
                                        edge[0]: left, edge[1]: right,
                                    }
                                    tensor[tuple(colours[site] for site in C)] += (
                                        pv * uv * vv * edge_value
                                    )
        return sp.Matrix([sp.simplify(tensor[word]) for word in basis])

    base_matrix, _ = matrix_for(base)
    require(base_matrix.row_join(pure[0]).rank() == base_matrix.rank(),
            f"{base_kind} base lost pure zero")
    require(base_matrix.row_join(pure[1]).rank() == base_matrix.rank(),
            f"{base_kind} base lost pure one")

    survivors = []
    new_pure_classes = []
    all_cells = [
        (edge, left, right)
        for edge in itertools.combinations(C, 2)
        for left in range(3)
        for right in range(3)
    ]
    for edge, left, right in all_cells:
        key = (edge, left, right)
        if key in base:
            continue
        require(base_characters.row_join(cell_character(key)).rank() ==
                len(base) + 1,
                f"{base_kind} one-cell coefficient lost torus normalization")
        trial = dict(base)
        trial[key] = sp.S.One
        matrix, labels = matrix_for(trial)
        rank = matrix.rank()
        if (matrix.row_join(pure[0]).rank() == rank and
                matrix.row_join(pure[1]).rank() == rank):
            kernel_basis = matrix.nullspace()
            survivor = (edge, left, right, rank, len(kernel_basis))
            survivors.append(survivor)
            if not kernel_basis:
                continue
            product_columns = []
            kernel_rows = [vector_as_rows(vector, labels)
                           for vector in kernel_basis]
            for p_index in range(len(labels)):
                p_vector = sp.zeros(len(labels), 1)
                p_vector[p_index] = 1
                P_rows = vector_as_rows(p_vector, labels)
                for U_rows in kernel_rows:
                    for V_rows in kernel_rows:
                        product_columns.append(
                            product_column(trial, P_rows, U_rows, V_rows)
                        )
            augmented = matrix.row_join(sp.Matrix.hstack(*product_columns))
            augmented_rank = augmented.rank()
            if augmented.row_join(pure[2]).rank() == augmented_rank:
                new_pure_classes.append(survivor + (augmented_rank,))

    summary = {
        "survivors": len(survivors),
        "rank_nullity": dict(sorted(Counter(
            (entry[3], entry[4]) for entry in survivors
        ).items())),
        "physical_edges": dict(sorted(Counter(
            entry[0] for entry in survivors
        ).items())),
        "sha256": sha256(repr(survivors).encode()).hexdigest(),
    }
    return len(all_cells) - len(base), summary, new_pure_classes


def main():
    rank, nullity, trilinear, augmented_rank, pure_intersection = (
        audit_binary_common_power_packet()
    )
    print("shared reciprocal two-bad cofactor quotient: PASS")
    print(f"common cofactor map rank/nullity={rank}/{nullity}")
    print("pure image colours=0,1; excluded pure colour=2")
    print(f"source-faithful kernel product={trilinear}")
    print(f"full kernel-product span rank={augmented_rank}; pure intersection={pure_intersection}")
    print("literal q/r pure deletions and six-site cofactors reconstructed")
    for base_kind in ("Hamilton", "Pythagorean"):
        one_cell_total, one_cell_summary, new_pure_classes = (
            audit_one_cell_pure_survivors(base_kind)
        )
        print(f"{base_kind} one-cell pure survivors={one_cell_summary['survivors']}/{one_cell_total}")
        print(f"{base_kind} survivor rank/nullity={one_cell_summary['rank_nullity']}")
        print(f"{base_kind} survivor physical edges={one_cell_summary['physical_edges']}")
        print(f"{base_kind} survivor ledger={one_cell_summary['sha256']}")
        print(f"{base_kind} one-cell new pure classes={new_pure_classes}")


if __name__ == "__main__":
    main()
