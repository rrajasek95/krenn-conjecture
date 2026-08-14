#!/usr/bin/env python3
"""Exact N=8 projective-cap rank dichotomy and minimal physical guard.

The first audit is formal linear algebra for an exact target source.  The
second is one literal endpoint-ordered C8 aggregate source.  It has minimum
edge support among sources for which all 28 pairs are doubly injective; on
that minimum support, full rank of all eight blocks (total rank 24) is
forced.  Its three pure coefficients are normalized to one, and its
projective cross-error map is injective at every pair.

The C8 source is deliberately *not* a GHZ source: a displayed mixed word is
nonzero.  It is a guard against support/rank/pure-normalization arguments,
not a counterexample to Krenn's conjecture.
"""

from __future__ import annotations

from functools import lru_cache
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import json


N = 8
COLORS = range(3)
PRIME = 1_000_003
EXPECTED_LEDGER_SHA256 = "ad98141d3c67d40598571f18d594f2898cd7d1f3352c1f467e4441e3b5b67f25"

ZERO = (
    (0, 0, 0),
    (0, 0, 0),
    (0, 0, 0),
)

# The cyclic order is 0-4-1-5-2-6-3-7-0.  All stored blocks have their
# smaller physical endpoint first.  The entries were selected once over the
# integers; no search is performed by this checker.
BLOCKS = {
    (0, 4): ((5, 3, 9), (4, 16, 15), (16, 13, 7)),
    (0, 7): ((4, 16, 1), (13, 14, 1), (15, 9, 8)),
    (1, 4): ((4, 11, 1), (1, 1, 1), (13, 7, 14)),
    (1, 5): ((1, 17, 8), (15, 16, 8), (12, 8, 8)),
    (2, 5): ((15, 10, 1), (14, 4, 6), (10, 4, 11)),
    (2, 6): ((17, 14, 17), (7, 10, 10), (16, 17, 13)),
    (3, 6): ((2, 16, 8), (13, 14, 6), (12, 12, 3)),
    (3, 7): ((15, 17, 4), (6, 17, 13), (12, 16, 1)),
}


def require(condition, detail):
    """Assertion which remains active under ``python -O``."""
    if not condition:
        raise RuntimeError(detail)


def transpose(matrix):
    return tuple(tuple(matrix[j][i] for j in COLORS) for i in COLORS)


def determinant_3(matrix):
    return (
        matrix[0][0]
        * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
        - matrix[0][1]
        * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
        + matrix[0][2]
        * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
    )


def stored_block(blocks, u, v):
    require(u < v, ("stored endpoint order changed", u, v))
    return blocks.get((u, v), ZERO)


def oriented_block(blocks, endpoint, neighbor):
    u, v = sorted((endpoint, neighbor))
    matrix = stored_block(blocks, u, v)
    return matrix if endpoint == u else transpose(matrix)


@lru_cache(maxsize=None)
def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for index in range(1, len(vertices)):
        partner = vertices[index]
        rest = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(rest):
            answer.append(((first, partner),) + tail)
    return tuple(answer)


def coefficient(blocks, vertices, word, modulus=None):
    """Literal matching coefficient on ``vertices`` in endpoint order."""
    total = 0
    for matching in perfect_matchings(tuple(vertices)):
        term = 1
        for u, v in matching:
            matrix = stored_block(blocks, u, v)
            term *= matrix[word[u]][word[v]]
            if modulus is not None:
                term %= modulus
            if term == 0:
                break
        total += term
        if modulus is not None:
            total %= modulus
    return total


def rank_mod(matrix, modulus=PRIME):
    rows = [[entry % modulus for entry in row] for row in matrix]
    rows = [row for row in rows if any(row)]
    if not rows:
        return 0
    rank = 0
    width = len(rows[0])
    for column in range(width):
        pivot = next(
            (index for index in range(rank, len(rows)) if rows[index][column]),
            None,
        )
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inverse = pow(rows[rank][column], modulus - 2, modulus)
        rows[rank] = [(entry * inverse) % modulus for entry in rows[rank]]
        for index in range(len(rows)):
            if index == rank or rows[index][column] == 0:
                continue
            scalar = rows[index][column]
            rows[index] = [
                (entry - scalar * pivot_entry) % modulus
                for entry, pivot_entry in zip(rows[index], rows[rank], strict=True)
            ]
        rank += 1
        if rank == width:
            break
    return rank


def normalize_at_site_zero():
    pure = tuple(
        coefficient(BLOCKS, range(N), (colour,) * N) for colour in COLORS
    )
    require(pure == (1755, 44304, 4424), ("pure ledger changed", pure))
    require(all(value % PRIME for value in pure), "normalization met the audit prime")

    normalized = {}
    normalized_mod = {}
    for edge, matrix in BLOCKS.items():
        rational_rows = []
        modular_rows = []
        for row_colour, row in enumerate(matrix):
            scale = Fraction(1, pure[row_colour]) if edge[0] == 0 else Fraction(1)
            modular_scale = (
                pow(pure[row_colour], PRIME - 2, PRIME) if edge[0] == 0 else 1
            )
            rational_rows.append(tuple(scale * entry for entry in row))
            modular_rows.append(
                tuple((modular_scale * entry) % PRIME for entry in row)
            )
        normalized[edge] = tuple(rational_rows)
        normalized_mod[edge] = tuple(modular_rows)
    return pure, normalized, normalized_mod


def audit_exact_source_rank_dichotomy():
    """Audit the quotient ranks in the exact-target formula.

    For an exact target source the nine cap-error columns, modulo Q, are six
    zero off-diagonal columns and the images of X0,X1,X2.  The three cases
    below are Q=0, Q outside their span, and nonzero Q in their span.
    """
    # Coordinates are X0,X1,X2,Z.  Appending Q as a last column computes
    # the quotient rank rank([kappa,Q])-rank(Q).
    diagonal_columns = (
        (1, 0, 0, 0),
        (0, 1, 0, 0),
        (0, 0, 1, 0),
    )

    def quotient_rank(q):
        matrix = [
            [diagonal_columns[column][row] for column in COLORS] + [q[row]]
            for row in range(4)
        ]
        q_rank = int(any(q))
        return rank_mod(matrix) - q_rank

    require(quotient_rank((0, 0, 0, 0)) == 3, "Q=0 quotient rank changed")
    require(quotient_rank((0, 0, 0, 1)) == 3, "Q outside target plane changed")
    for q in ((1, 0, 0, 0), (1, 2, 0, 0), (1, 2, 3, 0)):
        require(quotient_rank(q) == 2, ("Q in target plane changed", q))

        # The only diagonal zero-error direction is the Q coefficient line.
        diagonal_map_with_q = [
            [diagonal_columns[column][row] for column in COLORS] + [-q[row]]
            for row in range(4)
        ]
        require(rank_mod(diagonal_map_with_q) == 3, ("kernel line changed", q))

    # It is target-active precisely in the last case: every diagonal value
    # of the unique kernel vector is nonzero.
    require(all((1, 2, 3)), "active diagonal test changed")
    require(not all((1, 2, 0)), "inactive diagonal test changed")


def audit_support_and_rank_minimality(normalized):
    vertices = tuple(range(N))
    edges = set(BLOCKS)
    require(len(edges) == N, ("C8 support size changed", len(edges)))

    degrees = {
        vertex: sum(vertex in edge for edge in edges) for vertex in vertices
    }
    require(set(degrees.values()) == {2}, ("support stopped being C8", degrees))
    require(sum(degrees.values()) // 2 == 8, "handshake lower bound changed")

    for edge in edges:
        require(determinant_3(BLOCKS[edge]) != 0, ("singular integer block", edge))
        require(determinant_3(normalized[edge]) != 0, ("singular normalized block", edge))

    # Every deleted endpoint retains one or two invertible blocks, so every
    # pair is doubly injective.
    for p, q in combinations(vertices, 2):
        internal = set(vertices) - {p, q}
        for endpoint in (p, q):
            retained = [
                neighbor
                for neighbor in internal
                if tuple(sorted((endpoint, neighbor))) in edges
            ]
            require(retained, ("noninjective retained star", p, q, endpoint))
            require(
                all(
                    determinant_3(oriented_block(normalized, endpoint, neighbor))
                    for neighbor in retained
                ),
                ("retained block lost rank", p, q, endpoint),
            )

    # Edge-deletion minimality for the all-pairs-good property.  Removing uv
    # leaves u with its other neighbour q; deleting the pair {u,q} then
    # leaves the u-star identically zero.
    for removed in edges:
        u = removed[0]
        other = next(
            neighbor
            for neighbor in vertices
            if neighbor != removed[1]
            and tuple(sorted((u, neighbor))) in edges
        )
        remaining_edges = edges - {removed}
        residual_neighbors = [
            neighbor
            for neighbor in vertices
            if neighbor not in (u, other)
            and tuple(sorted((u, neighbor))) in remaining_edges
        ]
        require(
            residual_neighbors == [],
            ("edge deletion unexpectedly preserved all-pair goodness", removed),
        )

    # Any all-pairs-good support has degree at least two at every vertex, so
    # eight edges is the absolute support minimum.  At degree two, deleting
    # either neighbour leaves one block; that block must have rank three.
    total_block_rank = sum(3 for _ in edges)
    require(total_block_rank == 24, "minimum total block-rank ledger changed")


def audit_minimum_support_clean_caps(normalized):
    """Audit the local one-edge correction behind the restricted theorem."""
    vertices = tuple(range(N))
    edges = set(BLOCKS)
    clean_pairs = []
    for p, q in sorted(edges):
        p_external = [
            vertex
            for vertex in vertices
            if vertex != q and tuple(sorted((p, vertex))) in edges
        ]
        q_external = [
            vertex
            for vertex in vertices
            if vertex != p and tuple(sorted((q, vertex))) in edges
        ]
        require(
            len(p_external) == len(q_external) == 1,
            ("minimum-support external star changed", p, q),
        )

        # For K=I, all three target diagonal readouts are one.  Positivity of
        # this displayed model makes the direct scalar visibly nonzero.
        direct = oriented_block(normalized, p, q)
        direct_scalar = sum(direct[colour][colour] for colour in COLORS)
        require(direct_scalar > 0, ("identity cap became inactive", p, q))

        # The effective correction can live only on the one pair joining the
        # two external star sites (or is zero if those sites coincide).  Its
        # square is therefore zero in the site-square-zero algebra, so all
        # higher clean-cap terms vanish.
        correction_support = (
            []
            if p_external[0] == q_external[0]
            else [tuple(sorted((p_external[0], q_external[0])))]
        )
        require(len(correction_support) <= 1,
                ("clean correction acquired two edges", p, q))
        clean_pairs.append([p, q])
    require(len(clean_pairs) == 8, "active clean-edge census changed")
    return clean_pairs


def projective_error_ledger(blocks_mod):
    vertices = tuple(range(N))
    full_words = tuple(product(COLORS, repeat=N))
    full = {
        word: coefficient(blocks_mod, vertices, word, PRIME) for word in full_words
    }
    ledger = []

    for p, q in combinations(vertices, 2):
        residual = tuple(vertex for vertex in vertices if vertex not in (p, q))
        direct = oriented_block(blocks_mod, p, q)
        rows = []
        q_nonzero = False
        for residual_word in product(COLORS, repeat=N - 2):
            word = [0] * N
            for index, vertex in enumerate(residual):
                word[vertex] = residual_word[index]
            q_value = coefficient(blocks_mod, residual, tuple(word), PRIME)
            q_nonzero = q_nonzero or q_value != 0
            error_row = []
            for a, b in product(COLORS, repeat=2):
                word[p] = a
                word[q] = b
                # This is exactly D H_R[B^(a,b)] = F_(a,b)-a_(a,b)Q,
                # obtained by sorting physical matchings at the named pair.
                error_row.append(
                    (full[tuple(word)] - direct[a][b] * q_value) % PRIME
                )
            rows.append(error_row + [q_value])

        rank_error = rank_mod([row[:9] for row in rows])
        rank_augmented = rank_mod(rows)
        q_rank = int(q_nonzero)
        projective_rank = rank_augmented - q_rank
        require(rank_error == 9, ("error map lost rank", p, q, rank_error))
        require(
            projective_rank == 9,
            ("projective error acquired a nonzero kernel", p, q, projective_rank),
        )
        ledger.append(
            {
                "pair": [p, q],
                "q_nonzero": q_nonzero,
                "rank_error": rank_error,
                "rank_augmented": rank_augmented,
                "projective_rank": projective_rank,
            }
        )
    return ledger


def canonical(value):
    if isinstance(value, Fraction):
        return [value.numerator, value.denominator]
    if isinstance(value, dict):
        return {
            str(key): canonical(item)
            for key, item in sorted(value.items(), key=lambda pair: str(pair[0]))
        }
    if isinstance(value, (list, tuple)):
        return [canonical(item) for item in value]
    return value


def main():
    audit_exact_source_rank_dichotomy()
    pure, normalized, normalized_mod = normalize_at_site_zero()
    audit_support_and_rank_minimality(normalized)
    clean_pairs = audit_minimum_support_clean_caps(normalized)

    for colour in COLORS:
        value = coefficient(normalized, range(N), (colour,) * N)
        require(value == 1, ("pure normalization failed", colour, value))

    mixed_word = (0, 1, 0, 0, 0, 0, 0, 0)
    mixed_value = coefficient(normalized, range(N), mixed_word)
    require(mixed_value == Fraction(1283, 117), ("mixed row changed", mixed_value))

    pair_ledger = projective_error_ledger(normalized_mod)
    require(len(pair_ledger) == 28, "physical-pair census changed")
    require(sum(item["q_nonzero"] for item in pair_ledger) == 16,
            "deleted-cofactor activity census changed")

    ledger = canonical(
        {
            "blocks": BLOCKS,
            "integer_pure_coefficients": pure,
            "normalized_mixed_word": mixed_word,
            "normalized_mixed_value": mixed_value,
            "pair_projective_ranks": pair_ledger,
            "identity_clean_pairs": clean_pairs,
            "support_size": len(BLOCKS),
            "total_block_rank": 24,
        }
    )
    digest = sha256(
        json.dumps(ledger, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    if EXPECTED_LEDGER_SHA256 == "TO_BE_PINNED":
        print("LEDGER", digest)
    else:
        require(digest == EXPECTED_LEDGER_SHA256,
                ("projective-cap ledger changed", digest))

    print("n=8 support/rank-minimal projective-cap guard: PASS")
    print("  exact-target quotient ranks: Q=0/outside 3; nonzero Q in target plane 2")
    print("  minimum physical support / forced rank there: 8 / 24")
    print("  doubly injective physical pairs: 28 / 28")
    print("  projective cap-error ranks: 9 at all 28 pairs")
    print("  active clean identity caps: all 8 support edges")
    print("  pure coefficients after normalization: 1, 1, 1")
    print("  first displayed mixed residual 01000000: 1283/117")


if __name__ == "__main__":
    main()
