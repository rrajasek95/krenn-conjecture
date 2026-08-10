#!/usr/bin/env python3
"""Exact filtered lift of the concentrated unary-top diagonal identity.

The diagonal identity checker proves membership after setting every
off-diagonal internal Q cell to zero.  Here we retain all 135 Q cells and
work in the fine multidegree of

    F_01(1111) * F_23(2222) * H(000000).

Filter its monomials by the number of off-diagonal-colour Q cells.  For
cutoffs two and three, this script constructs the complete source-labelled
Macaulay map from the 285 compatible zero coefficient rows and every
fine-degree complementary matching.  A deterministic nonzero maximal minor
modulo 1,000,003 proves that each truncated map is onto over Q.  Thus the
diagonal certificate lifts through the first possible off-diagonal layer
(and one layer farther).  This is only a filtered statement; it is not full
ideal membership.
"""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import product
import json


SITES = tuple(range(6))
TOKENS_BY_SITE = {
    0: (0, 2),
    1: (0, 2),
    2: (0, 1),
    3: (0, 1),
    4: (0, 1, 2),
    5: (0, 1, 2),
}
ALL_TOKENS = tuple(
    (site, colour)
    for site in SITES
    for colour in TOKENS_BY_SITE[site]
)
PRIME = 1_000_003

EXPECTED = {
    2: {
        "rows": 3228,
        "columns": 10314,
        "matrix_sha256": "d851119932eaa1a87a6e1e356f428383b5680c6a229a59f3ae1b9abc75dc8916",
        "minor_columns_sha256": "271d3a5177094e50dc990bc2144cc71a8741709ca0a34d21ced43702a42ed50f",
    },
    3: {
        "rows": 11118,
        "columns": 31182,
        "matrix_sha256": "cebf8a6662cbc17d43bb2171afc161d6187a72b8926ebcc189c076edaf05d4ac",
        "minor_columns_sha256": "8790eb761732ea36cfa8b728d328cf0a37ad0b4ec38b6ad5265ec51c030cf665",
    },
}
EXPECTED_LEDGER_DIGEST = "ed4a6232d00cf907e82be44d7705daf0ba311d2c3c18c3f89477ea94b036b1ea"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


@lru_cache(None)
def token_matchings(tokens):
    """Pair labelled site-colour tokens, never two tokens at one site."""
    tokens = tuple(tokens)
    if not tokens:
        return ((),)
    first = tokens[0]
    answer = []
    for index, mate in enumerate(tokens[1:], 1):
        if first[0] == mate[0]:
            continue
        remainder = tokens[1:index] + tokens[index + 1:]
        left, right = sorted((first, mate))
        cell = (left[0], right[0], left[1], right[1])
        for tail in token_matchings(remainder):
            answer.append(tuple(sorted((cell,) + tail)))
    return tuple(answer)


def offdiagonal_order(monomial):
    return sum(left_colour != right_colour
               for _, _, left_colour, right_colour in monomial)


def cross_colour_signature(monomial):
    counts = Counter()
    for _, _, left_colour, right_colour in monomial:
        if left_colour == right_colour:
            continue
        counts[tuple(sorted((left_colour, right_colour)))] += 1
    return (counts[(0, 1)], counts[(0, 2)], counts[(1, 2)])


@lru_cache(None)
def perfect_matchings(vertices):
    vertices = tuple(sorted(vertices))
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for mate in vertices[1:]:
        remainder = tuple(
            vertex for vertex in vertices if vertex not in (first, mate)
        )
        for tail in perfect_matchings(remainder):
            answer.append((tuple(sorted((first, mate))),) + tail)
    return tuple(answer)


def coefficient_terms(vertices, word):
    """Full 3x3-cell coefficient, as matching monomials with coefficient 1."""
    vertices = tuple(vertices)
    position = {vertex: index for index, vertex in enumerate(vertices)}
    terms = []
    for matching in perfect_matchings(vertices):
        terms.append(tuple(sorted(
            (left, right, word[position[left]], word[position[right]])
            for left, right in matching
        )))
    return tuple(terms)


def build_generators():
    generators = []

    # All compatible mixed top coefficients vanish.
    for word in product(*(TOKENS_BY_SITE[site] for site in SITES)):
        if len(set(word)) == 1:
            continue
        generators.append((
            SITES,
            word,
            "top:" + "".join(map(str, word)),
        ))

    # All compatible non-target direct cofactors and both cross cofactors
    # vanish in the normalized response packet.
    packets = (
        ((0, 1), (1, 1, 1, 1)),
        ((2, 3), (2, 2, 2, 2)),
        ((0, 3), None),
        ((1, 2), None),
    )
    for holes, target in packets:
        vertices = tuple(site for site in SITES if site not in holes)
        for word in product(*(TOKENS_BY_SITE[site] for site in vertices)):
            if target is not None and word == target:
                continue
            generators.append((
                vertices,
                word,
                "cofactor:" + "".join(map(str, holes)) + ":"
                + "".join(map(str, word)),
            ))

    require(len(generators) == 285,
            f"the full compatible generator count changed: {len(generators)}")
    return tuple(generators)


def canonical_bytes(value):
    return json.dumps(
        value, sort_keys=True, separators=(",", ":")
    ).encode()


def reduce_column(vector, pivots):
    """Column elimination over GF(PRIME), with the least row as pivot."""
    while vector:
        lead = min(vector)
        if lead not in pivots:
            inverse = pow(vector[lead], PRIME - 2, PRIME)
            for row in tuple(vector):
                vector[row] = vector[row] * inverse % PRIME
            pivots[lead] = vector
            return True, lead
        scale = vector[lead]
        pivot = pivots[lead]
        for row, value in pivot.items():
            reduced = (vector.get(row, 0) - scale * value) % PRIME
            if reduced:
                vector[row] = reduced
            else:
                vector.pop(row, None)
    return False, None


def target_vector(row_index):
    first = coefficient_terms((2, 3, 4, 5), (1, 1, 1, 1))
    second = coefficient_terms((0, 1, 4, 5), (2, 2, 2, 2))
    top = coefficient_terms(SITES, (0, 0, 0, 0, 0, 0))
    terms = Counter()
    for term_a in first:
        for term_b in second:
            for term_c in top:
                monomial = tuple(sorted(term_a + term_b + term_c))
                terms[row_index[monomial]] += 1
    require(len(terms) == 135 and set(terms.values()) == {1},
            "the target product monomials changed")
    return {row: value % PRIME for row, value in terms.items()}


def analyze_cutoff(cutoff, generators):
    basis = tuple(
        monomial
        for monomial in token_matchings(ALL_TOKENS)
        if offdiagonal_order(monomial) <= cutoff
    )
    row_index = {monomial: index for index, monomial in enumerate(basis)}
    order_counts = Counter(map(offdiagonal_order, basis))
    require(order_counts.get(1, 0) == 0,
            "an off-diagonal-order-one monomial appeared")
    if cutoff >= 3:
        order_three_signatures = Counter(
            cross_colour_signature(monomial)
            for monomial in basis
            if offdiagonal_order(monomial) == 3
        )
        require(order_three_signatures == {(1, 1, 1): 7890},
                f"the order-three cycle class changed: {order_three_signatures}")

    matrix_hash = sha256()
    matrix_hash.update(canonical_bytes({
        "cutoff": cutoff,
        "basis": basis,
        "prime": PRIME,
    }))
    pivots = {}
    pivot_columns = []
    column_count = 0

    for vertices, word, label in generators:
        used_tokens = set(zip(vertices, word))
        complement = tuple(
            token for token in ALL_TOKENS if token not in used_tokens
        )
        source_terms = coefficient_terms(vertices, word)
        for multiplier in token_matchings(complement):
            entries = Counter()
            for source_term in source_terms:
                monomial = tuple(sorted(source_term + multiplier))
                if offdiagonal_order(monomial) <= cutoff:
                    entries[row_index[monomial]] += 1
            if not entries:
                continue

            column_count += 1
            canonical_entries = tuple(sorted(entries.items()))
            matrix_hash.update(canonical_bytes((
                column_count, label, multiplier, canonical_entries
            )))
            vector = {
                row: value % PRIME
                for row, value in canonical_entries
                if value % PRIME
            }
            independent, lead = reduce_column(vector, pivots)
            if independent:
                pivot_columns.append((column_count, lead, label, multiplier))

    expected = EXPECTED[cutoff]
    require(len(basis) == expected["rows"],
            f"cutoff {cutoff} row count changed: {len(basis)}")
    require(column_count == expected["columns"],
            f"cutoff {cutoff} column count changed: {column_count}")
    require(len(pivots) == len(basis),
            f"cutoff {cutoff} lost full row rank: {len(pivots)}/{len(basis)}")
    require(len(pivot_columns) == len(basis),
            "the maximal-minor column count changed")

    vector = target_vector(row_index)
    while vector:
        lead = min(vector)
        require(lead in pivots,
                f"cutoff {cutoff} target has an uncovered row {lead}")
        scale = vector[lead]
        for row, value in pivots[lead].items():
            reduced = (vector.get(row, 0) - scale * value) % PRIME
            if reduced:
                vector[row] = reduced
            else:
                vector.pop(row, None)
    require(not vector, f"cutoff {cutoff} target remainder is nonzero")

    matrix_digest = matrix_hash.hexdigest()
    minor_digest = sha256(canonical_bytes(pivot_columns)).hexdigest()
    if expected["matrix_sha256"] != "TO_BE_FILLED":
        require(matrix_digest == expected["matrix_sha256"],
                f"cutoff {cutoff} matrix changed: {matrix_digest}")
    if expected["minor_columns_sha256"] != "TO_BE_FILLED":
        require(minor_digest == expected["minor_columns_sha256"],
                f"cutoff {cutoff} maximal minor changed: {minor_digest}")

    return {
        "cutoff": cutoff,
        "rows": len(basis),
        "rows_by_offdiagonal_order": dict(sorted(order_counts.items())),
        "source_generators": len(generators),
        "source_label_counts": {
            "top": sum(label.startswith("top:")
                       for _, _, label in generators),
            "cofactor": sum(label.startswith("cofactor:")
                            for _, _, label in generators),
        },
        "columns": column_count,
        "rank_mod_prime": len(pivots),
        "prime": PRIME,
        "target_remainder_terms_mod_prime": 0,
        "matrix_sha256": matrix_digest,
        "minor_columns_sha256": minor_digest,
    }


def diagonal_multiplier_counterguard(generators):
    """Show mod PRIME that diagonal complementary multipliers do not suffice."""
    basis = token_matchings(ALL_TOKENS)
    row_index = {monomial: index for index, monomial in enumerate(basis)}
    pivots = {}
    columns = 0
    for vertices, word, _ in generators:
        used_tokens = set(zip(vertices, word))
        complement = tuple(
            token for token in ALL_TOKENS if token not in used_tokens
        )
        source_terms = coefficient_terms(vertices, word)
        for multiplier in token_matchings(complement):
            if offdiagonal_order(multiplier):
                continue
            entries = Counter(
                row_index[tuple(sorted(source_term + multiplier))]
                for source_term in source_terms
            )
            vector = {
                row: value % PRIME
                for row, value in entries.items()
                if value % PRIME
            }
            columns += 1
            reduce_column(vector, pivots)

    vector = target_vector(row_index)
    while vector:
        lead = min(vector)
        if lead not in pivots:
            break
        scale = vector[lead]
        for row, value in pivots[lead].items():
            reduced = (vector.get(row, 0) - scale * value) % PRIME
            if reduced:
                vector[row] = reduced
            else:
                vector.pop(row, None)
    require(columns == 501 and len(pivots) == 501,
            f"the diagonal-multiplier module changed: {columns}/{len(pivots)}")
    require(len(vector) == 243,
            f"the diagonal-multiplier residual changed: {len(vector)}")
    first_order = offdiagonal_order(basis[min(vector)])
    require(first_order == 2,
            f"the first diagonal-multiplier residual order changed: {first_order}")
    return {
        "prime": PRIME,
        "columns": columns,
        "rank_mod_prime": len(pivots),
        "target_residual_terms_mod_prime": len(vector),
        "first_residual_offdiagonal_order": first_order,
        "interpretation": (
            "modular counterguard only; diagonal complementary multipliers "
            "do not give the required certificate modulo this prime"
        ),
    }


def main():
    generators = build_generators()
    results = [analyze_cutoff(cutoff, generators) for cutoff in (2, 3)]
    counterguard = diagonal_multiplier_counterguard(generators)
    ledger = {
        "fine_tokens": {
            str(site): list(colours)
            for site, colours in TOKENS_BY_SITE.items()
        },
        "results": results,
        "order_three_cross_colour_signature": {"1,1,1": 7890},
        "diagonal_multiplier_counterguard": counterguard,
        "verdict": (
            "the concentrated unary-top diagonal identity lifts through "
            "off-diagonal order three over Q"
        ),
        "scope": (
            "complete 135-cell Q and concentrated holes (01),(23), modulo "
            "terms with at least four off-diagonal-colour cells; no full "
            "ideal-membership or multisite-star conclusion"
        ),
    }
    digest = sha256(canonical_bytes(ledger)).hexdigest()
    if EXPECTED_LEDGER_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_DIGEST,
                f"the filtered-lift ledger changed: {digest}")

    print("N=8 unary-top off-diagonal filtered lift: PASS")
    for result in results:
        print(
            f"order<={result['cutoff']}: rows={result['rows']}; "
            f"columns={result['columns']}; rank mod {PRIME}="
            f"{result['rank_mod_prime']}; target remainder=0"
        )
        print(f"  matrix sha256: {result['matrix_sha256']}")
        print(f"  maximal-minor columns sha256: "
              f"{result['minor_columns_sha256']}")
    print("full ideal membership and multisite stars: OPEN")
    print(f"ledger sha256: {digest}")


if __name__ == "__main__":
    main()
