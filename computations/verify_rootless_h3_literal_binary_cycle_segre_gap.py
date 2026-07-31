#!/usr/bin/env python3
"""Exact audit of the literal h=3 binary-cycle Segre gap.

The checker uses only the standard library and explicit failures, including
under ``python -O``.  It verifies a literal eight-site binary C8 source, two
overlapping six-site chart slices, a crossed four-index zero slice, the
near-physical eight-row cap table, the two decisive cubics ``f=v^3`` and
``g=u^3-u^2v``, and the first failed Segre factorization.
"""

from __future__ import annotations

from fractions import Fraction as F
from itertools import product


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


Monomial = tuple[int, int]
Polynomial = dict[Monomial, F]
Word = tuple[int, ...]
Tensor = dict[Word, Polynomial]
Edge = tuple[int, int, int, int, F]
Family = dict[tuple[int, int, int, int], Polynomial]


def padd(left: Polynomial, right: Polynomial) -> Polynomial:
    out = dict(left)
    for monomial, value in right.items():
        out[monomial] = out.get(monomial, F(0)) + value
    return {monomial: value for monomial, value in out.items() if value}


def pmul(left: Polynomial, right: Polynomial) -> Polynomial:
    out: Polynomial = {}
    for (lu, lv), left_value in left.items():
        for (ru, rv), right_value in right.items():
            monomial = (lu + ru, lv + rv)
            out[monomial] = (
                out.get(monomial, F(0)) + left_value * right_value
            )
    return {monomial: value for monomial, value in out.items() if value}


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for matching in perfect_matchings(rest):
            yield ((first, second),) + matching


def edge_key(left: int, right: int, left_colour: int, right_colour: int):
    if left < right:
        return (left, right, left_colour, right_colour)
    return (right, left, right_colour, left_colour)


def add_edge(family: Family, item: Edge, polynomial: Polynomial) -> None:
    left, right, left_colour, right_colour, weight = item
    require(left != right, "a quadratic edge used one site twice")
    key = edge_key(left, right, left_colour, right_colour)
    scaled = {monomial: weight * value
              for monomial, value in polynomial.items()}
    family[key] = padd(family.get(key, {}), scaled)


def family_from_layers(layers: tuple[tuple[tuple[Edge, ...], Polynomial], ...]):
    family: Family = {}
    for edges, polynomial in layers:
        for item in edges:
            add_edge(family, item, polynomial)
    return family


def matching_tensor(site_count: int, family: Family) -> Tensor:
    out: Tensor = {}
    matchings = tuple(perfect_matchings(tuple(range(site_count))))
    for word in product(range(3), repeat=site_count):
        polynomial: Polynomial = {}
        for matching in matchings:
            term: Polynomial = {(0, 0): F(1)}
            for left, right in matching:
                term = pmul(
                    term,
                    family.get(
                        edge_key(left, right, word[left], word[right]), {}
                    ),
                )
                if not term:
                    break
            polynomial = padd(polynomial, term)
        if polynomial:
            out[word] = polynomial
    return out


def layer(tensor: Tensor, monomial: Monomial) -> dict[Word, F]:
    return {
        word: polynomial[monomial]
        for word, polynomial in tensor.items()
        if polynomial.get(monomial, F(0))
    }


def add_scalar_tensors(*items: dict[Word, F]) -> dict[Word, F]:
    out: dict[Word, F] = {}
    for item in items:
        for word, value in item.items():
            out[word] = out.get(word, F(0)) + value
    return {word: value for word, value in out.items() if value}


def scale_scalar_tensor(value: F, item: dict[Word, F]) -> dict[Word, F]:
    return {word: value * coefficient
            for word, coefficient in item.items() if value * coefficient}


def cube_layers(base: tuple[Edge, ...], cap: tuple[Edge, ...]) -> Tensor:
    return matching_tensor(
        6,
        family_from_layers(
            (
                (base, {(1, 0): F(1)}),
                (cap, {(0, 1): F(1)}),
            )
        ),
    )


def audit_global_binary_cycle() -> None:
    # Site order is p,q,0,1,2,3,4,5.  The two displayed one-factors
    # alternate around p-0-q-1-2-3-4-5-p.
    global_edges: tuple[Edge, ...] = (
        (0, 2, 0, 0, F(1)),
        (1, 3, 0, 0, F(1)),
        (4, 5, 0, 0, F(1)),
        (6, 7, 0, 0, F(1)),
        (0, 7, 1, 1, F(1)),
        (1, 2, 1, 1, F(1)),
        (3, 4, 1, 1, F(1)),
        (5, 6, 1, 1, F(1)),
    )
    tensor = matching_tensor(
        8,
        family_from_layers(((global_edges, {(0, 0): F(1)}),)),
    )
    x0 = (0,) * 8
    x1 = (1,) * 8
    require(tensor == {
        x0: {(0, 0): F(1)},
        x1: {(0, 0): F(1)},
    }, "the literal C8 has an unlisted or incorrectly weighted matching")

    def chart_rows(deleted: tuple[int, int]):
        residual = tuple(site for site in range(8) if site not in deleted)
        rows: dict[tuple[int, int], dict[Word, F]] = {}
        for word, polynomial in tensor.items():
            value = polynomial.get((0, 0), F(0))
            if not value:
                continue
            labels = (word[deleted[0]], word[deleted[1]])
            residual_word = tuple(word[site] for site in residual)
            row = rows.setdefault(labels, {})
            row[residual_word] = row.get(residual_word, F(0)) + value
        return rows

    expected = {
        (0, 0): {(0,) * 6: F(1)},
        (1, 1): {(1,) * 6: F(1)},
    }
    require(chart_rows((0, 1)) == expected,
            "the pq chart lost its two physical anchors")
    require(chart_rows((0, 7)) == expected,
            "the overlapping p5 chart lost its two physical anchors")

    # A genuine four-index slice: p,q,5,0 have the crossed boundary
    # labels 0,0,1,1 (and then 1,1,0,0).  The entire complementary tensor
    # must be zero, not merely one scalar coordinate.
    boundary_sites = (0, 1, 7, 2)
    for boundary in ((0, 0, 1, 1), (1, 1, 0, 0)):
        surviving = {
            word: polynomial
            for word, polynomial in tensor.items()
            if tuple(word[site] for site in boundary_sites) == boundary
        }
        require(not surviving,
                f"crossed four-index slice {boundary} should be zero")


Q: tuple[Edge, ...] = (
    (2, 3, 0, 0, F(1)),
    (4, 5, 0, 0, F(1)),
    (1, 2, 1, 1, F(1)),
    (3, 4, 1, 1, F(1)),
)
A0: tuple[Edge, ...] = ((0, 1, 0, 0, F(1)),)
A1: tuple[Edge, ...] = ((0, 5, 1, 1, F(1)),)
B: tuple[Edge, ...] = (
    (0, 2, 2, 2, F(1)),
    (1, 3, 2, 2, F(1)),
    (4, 5, 1, 1, F(1)),
)
R: tuple[Edge, ...] = (
    (0, 4, 2, 2, F(1)),
    (1, 2, 2, 2, F(1)),
    (3, 5, 2, 2, F(1)),
)


def q2_cap(cap: tuple[Edge, ...]) -> dict[Word, F]:
    return layer(cube_layers(Q, cap), (2, 1))


def audit_eight_row_cap_table() -> None:
    x0 = (0,) * 6
    x1 = (1,) * 6

    q_cube = layer(cube_layers(Q, ()), (3, 0))
    require(not q_cube, "q^[3] should vanish because site zero is isolated")
    require(q2_cap(A0) == {x0: F(1)}, "the 00 anchor is not X0")
    require(q2_cap(A1) == {x1: F(1)}, "the 11 anchor is not X1")
    require(not q2_cap(B), "the top-invisible 22 cap became visible")
    require(not q2_cap(R), "the selected 02 cap became visible")

    rows: dict[tuple[int, int], dict[Word, F]] = {}
    for i in range(3):
        for j in range(3):
            cap = ()
            if (i, j) == (0, 0):
                cap = A0
            elif (i, j) == (1, 1):
                cap = A1
            elif (i, j) == (2, 2):
                cap = B
            elif (i, j) == (0, 2):
                cap = R
            row = q2_cap(cap) if cap else {}
            # The only direct entry is a_02=1, and q^[3]=0.
            rows[i, j] = add_scalar_tensors(
                row,
                q_cube if (i, j) == (0, 2) else {},
            )

    for i in range(3):
        for j in range(3):
            expected = {}
            if i == j == 0:
                expected = {x0: F(1)}
            elif i == j == 1:
                expected = {x1: F(1)}
            require(rows[i, j] == expected,
                    f"near-physical row {(i, j)} is incorrect")

    # Sharp row mutation: 04 is invisible, whereas 03 has the cofactor
    # (12)_1(45)_0.  Moving only that endpoint makes the 02 row fail.
    mutated_r = (
        (0, 3, 2, 2, F(1)),
        R[1],
        R[2],
    )
    require(q2_cap(mutated_r),
            "the visible-edge mutation did not break the selected row")


def clean_line_tensor() -> Tensor:
    d = A0 + A1 + B
    family = family_from_layers(
        (
            (Q + R, {(1, 0): F(1)}),
            (d, {(0, 1): F(1)}),
        )
    )
    clean = matching_tensor(6, family)
    # sigma=u and T(u E_02+v I)=v(X0+X1+X2).
    for colour in range(3):
        pure = (colour,) * 6
        polynomial = clean.setdefault(pure, {})
        polynomial[(2, 1)] = polynomial.get((2, 1), F(0)) - F(1)
        clean[pure] = {monomial: value
                       for monomial, value in polynomial.items() if value}
        if not clean[pure]:
            del clean[pure]
    return clean


def pmul_dense(left: tuple[F, ...], right: tuple[F, ...]) -> tuple[F, ...]:
    out = [F(0)] * (len(left) + len(right) - 1)
    for i, left_value in enumerate(left):
        for j, right_value in enumerate(right):
            out[i + j] += left_value * right_value
    return tuple(out)


def det3(rows: tuple[tuple[F, ...], ...]) -> F:
    require(len(rows) == 3 and all(len(row) == 3 for row in rows),
            "det3 requires a 3-by-3 matrix")
    return (
        rows[0][0] * (rows[1][1] * rows[2][2]
                      - rows[1][2] * rows[2][1])
        - rows[0][1] * (rows[1][0] * rows[2][2]
                        - rows[1][2] * rows[2][0])
        + rows[0][2] * (rows[1][0] * rows[2][1]
                        - rows[1][1] * rows[2][0])
    )


def audit_root_coefficient_and_macaulay_block() -> None:
    clean = clean_line_tensor()
    y = (2, 2, 2, 2, 1, 1)
    x2 = (2,) * 6
    require(clean.get(y) == {(0, 3): F(1)},
            "the exposed coordinate is not exactly f=v^3")
    require(clean.get(x2) == {
        (3, 0): F(1),
        (2, 1): F(-1),
    }, "the root-direction coordinate is not g=u^3-u^2v")

    # The exact pre-cancellation identity at [1:0].  The (3,0) and (2,1)
    # layers vanish by q^[3]=0 and R q^[2]=0, leaving R^[2]q+R^[3].
    root_layers = cube_layers(Q, R)
    q3 = layer(root_layers, (3, 0))
    rq2 = layer(root_layers, (2, 1))
    r2q = layer(root_layers, (1, 2))
    r3 = layer(root_layers, (0, 3))
    require(not q3 and not rq2,
            "the two physical top-row layers did not vanish")
    root_value = add_scalar_tensors(q3, rq2, r2q, r3)
    nonlinear_value = add_scalar_tensors(r2q, r3)
    require(root_value == nonlinear_value,
            "the pre-cancellation root identity failed")
    require(root_value.get(x2) == F(1),
            "chi=[X2](q+R)^[3] should equal one")

    # In Q_f for f=v^3, multiplication by g has a lower triangular
    # residual matrix with diagonal chi=1.
    f = (F(0), F(0), F(0), F(1))
    g = (F(1), F(-1), F(0), F(0))
    quadratics = (
        (F(1), F(0), F(0)),
        (F(0), F(1), F(0)),
        (F(0), F(0), F(1)),
    )
    f_columns = tuple(pmul_dense(f, item) for item in quadratics)
    require(all(column[:3] == (F(0), F(0), F(0))
                for column in f_columns),
            "fS2 should vanish in the first three quotient coordinates")
    columns = tuple(pmul_dense(g, item)[:3] for item in quadratics)
    matrix = tuple(tuple(columns[column][row] for column in range(3))
                   for row in range(3))
    require(det3(matrix) == F(1),
            "the residual Macaulay determinant should be chi^3=1")

    # Deleting one matching edge is the sharp chi mutation.
    short_r = R[1:]
    short_root = cube_layers(Q, short_r)
    short_value = add_scalar_tensors(
        layer(short_root, (1, 2)),
        layer(short_root, (0, 3)),
    )
    require(not short_value.get(x2, F(0)),
            "deleting one selected-cap edge did not kill chi")


def matching_completion_lower_bound(
    edges: tuple[Edge, ...], selected_word: Word
) -> int:
    # Restrict to one chosen local port at each site.  Off-diagonal entries
    # are the coefficients of the quadratic on those six ports.
    matrix = [[F(0) for _ in range(6)] for _ in range(6)]
    for left, right, left_colour, right_colour, weight in edges:
        if (left_colour, right_colour) != (
            selected_word[left], selected_word[right]
        ):
            continue
        matrix[left][right] += weight
        matrix[right][left] += weight

    nonzero_pairs = tuple(
        (left, right)
        for left in range(6)
        for right in range(left + 1, 6)
        if matrix[left][right]
    )
    require(len(nonzero_pairs) == 3,
            "the selected port graph is not a three-edge matching")
    require(set(vertex for pair in nonzero_pairs for vertex in pair)
            == set(range(6)),
            "the selected port matching does not cover all six sites")

    # Any diagonal completion remains block diagonal on these three pairs.
    # Each 2-by-2 block has a nonzero off-diagonal entry and hence rank at
    # least one, so every completion has rank at least three.
    for first in range(3):
        for second in range(first + 1, 3):
            require(set(nonzero_pairs[first]).isdisjoint(nonzero_pairs[second]),
                    "the three selected pairs are not disjoint")
    return 3


def audit_first_segre_gap() -> None:
    r_lower_bound = matching_completion_lower_bound(R, (2,) * 6)
    b_lower_bound = matching_completion_lower_bound(
        B, (2, 2, 2, 2, 1, 1)
    )
    require(r_lower_bound == b_lower_bound == 3,
            "the diagonal-completion lower bound should be three")

    # If a quadratic is one product p*s, its completed symmetric port
    # matrix is p s^T+s p^T and has rank at most two.  The lower bound
    # above therefore rules out even individual factorization of B and R,
    # before asking that all nine caps share the same two star triples.
    segre_rank_upper_bound = 2
    require(r_lower_bound > segre_rank_upper_bound,
            "R was not separated from the one-product Segre locus")
    require(b_lower_bound > segre_rank_upper_bound,
            "B was not separated from the one-product Segre locus")


def main() -> None:
    audit_global_binary_cycle()
    audit_eight_row_cap_table()
    audit_root_coefficient_and_macaulay_block()
    audit_first_segre_gap()
    print(
        "rootless h=3 literal binary-cycle Segre gap: PASS; "
        "f=v^3, g=u^3-u^2v, chi=1, first omitted compatibility=shared-star factorization"
    )


if __name__ == "__main__":
    main()
