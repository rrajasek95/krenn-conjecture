#!/usr/bin/env python3
"""Independent exact audit of the h=3 mixed-word quotient reset.

This replay does not import the primary checker.  It uses a bit-mask hafnian
recursion for the eight-site EqSystem and an independently assembled matrix
for R_1 q^[2] on the five odd sites.
"""

from fractions import Fraction
from hashlib import sha256
from itertools import product
import json


F = Fraction
ZERO = F(0)
ONE = F(1)
COLORS = range(3)
ALL_MASK = (1 << 8) - 1
ODD_SITES = (1, 2, 3, 4, 5)
PURE_WORD = (0, 0, 0, 0, 0)
EXPECTED_DIGEST = "6a45beec7fa5394f8fd2e04847d0f853d4d272add15947b963b5b9ee21b7a2ba"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical_cell(site_a, site_b, color_a, color_b):
    if site_a < site_b:
        return site_a, site_b, color_a, color_b
    return site_b, site_a, color_b, color_a


def build_cells(records):
    result = {}
    for site_a, site_b, color_a, color_b, numerator, denominator in records:
        key = canonical_cell(site_a, site_b, color_a, color_b)
        value = F(numerator, denominator)
        require(site_a != site_b, f"loop in cell record {key}")
        require(value != ZERO, f"zero stored cell {key}")
        require(key not in result, f"duplicate stored cell {key}")
        result[key] = value
    return result


# These are the two frozen rational cell tables themselves, not values copied
# from the primary reset checker's computed ledgers.
DIRECT_FREE_CELLS = build_cells((
    (0, 1, 0, 1, 1, 1), (0, 2, 0, 2, 1, 1),
    (0, 3, 0, 1, 1, 1), (0, 4, 0, 1, 1, 1),
    (0, 5, 0, 2, 1, 1), (0, 6, 0, 0, 1, 1),
    (1, 2, 1, 2, 1, 1), (1, 3, 1, 2, 1, 1),
    (1, 4, 1, 1, 1, 1), (1, 6, 1, 1, 1, 1),
    (2, 3, 2, 0, 1, 1), (2, 6, 2, 2, 1, 1),
    (3, 4, 0, 1, 1, 1), (3, 5, 0, 2, 1, 1),
    (3, 7, 0, 0, 1, 1), (4, 7, 1, 1, 1, 1),
    (5, 7, 2, 2, 1, 1),
    (6, 7, 0, 1, -1, 4), (6, 7, 0, 2, -1, 2),
    (6, 7, 1, 1, -1, 2), (6, 7, 1, 2, -1, 2),
    (6, 7, 2, 0, -1, 4), (6, 7, 2, 1, -1, 4),
    (6, 7, 2, 2, -1, 4),
))


TILTED_CELLS = build_cells((
    (0, 1, 0, 1, 1, 1), (0, 2, 0, 2, 1, 1),
    (0, 4, 0, 1, 1, 1), (0, 5, 0, 2, 1, 1),
    (0, 6, 0, 0, 1, 1), (1, 2, 1, 2, 1, 1),
    (1, 3, 0, 0, 1, 1), (1, 4, 1, 1, 1, 1),
    (1, 5, 2, 2, 1, 1), (1, 6, 0, 2, -1, 4),
    (1, 6, 1, 0, 1, 1), (1, 6, 1, 1, 1, 1),
    (1, 6, 2, 0, 1, 4), (1, 6, 2, 1, 1, 2),
    (1, 6, 2, 2, 1, 8), (2, 3, 2, 0, 1, 1),
    (2, 6, 2, 2, 1, 1), (2, 7, 2, 1, 1, 1),
    (3, 4, 0, 1, 1, 1), (3, 5, 0, 2, 1, 1),
    (3, 7, 0, 0, 1, 1), (4, 7, 1, 1, 1, 1),
    (5, 7, 2, 2, 1, 1),
    (6, 7, 0, 1, -3, 2), (6, 7, 0, 2, -1, 1),
    (6, 7, 1, 1, -1, 1), (6, 7, 1, 2, -1, 2),
    (6, 7, 2, 0, -1, 4), (6, 7, 2, 1, -1, 4),
    (6, 7, 2, 2, -1, 4),
))


PACKETS = {
    "direct_free": (DIRECT_FREE_CELLS, F(-1, 4)),
    "tilted": (TILTED_CELLS, F(-5, 2)),
}


EXPECTED_FAILURES = {
    "direct_free": (
        ("000000", "00", "0", "1"),
        ("012112", "22", "1", "0"),
        ("012212", "21", "1", "0"),
        ("012212", "22", "1", "0"),
        ("111111", "11", "0", "1"),
        ("222222", "22", "0", "1"),
    ),
    "tilted": (
        ("000000", "00", "0", "1"),
        ("002012", "22", "1/2", "0"),
        ("022012", "02", "-3/2", "0"),
        ("022012", "20", "1/2", "0"),
        ("022012", "22", "-1/4", "0"),
        ("111111", "11", "0", "1"),
        ("222222", "22", "0", "1"),
    ),
}


EXPECTED_MIXED = {
    "direct_free": (
        ("12112", "22", F(1)),
        ("12212", "21", F(1)),
        ("12212", "22", F(1)),
    ),
    "tilted": (
        ("02012", "22", F(1, 2)),
        ("22012", "02", F(-3, 2)),
        ("22012", "20", F(1, 2)),
        ("22012", "22", F(-1, 4)),
    ),
}


def cell(cells, site_a, site_b, color_a, color_b):
    return cells.get(
        canonical_cell(site_a, site_b, color_a, color_b), ZERO
    )


def matching_sum(cells, assignment, mask):
    """Perfect-matching sum by least-bit deletion, independent of listings."""
    if mask == 0:
        return ONE
    require(mask.bit_count() % 2 == 0, "matching_sum called on odd set")
    first_bit = mask & -mask
    first = first_bit.bit_length() - 1
    remainder = mask ^ first_bit
    answer = ZERO
    partners = remainder
    while partners:
        second_bit = partners & -partners
        second = second_bit.bit_length() - 1
        edge = cell(
            cells, first, second, assignment[first], assignment[second]
        )
        if edge:
            answer += edge * matching_sum(
                cells, assignment, remainder ^ second_bit
            )
        partners ^= second_bit
    return answer


def pure_target(word, endpoint_left, endpoint_right):
    return ONE if (
        endpoint_left == endpoint_right
        and all(color == endpoint_left for color in word)
    ) else ZERO


def enumerate_eqsystem(cells):
    ledger = []
    for word in product(COLORS, repeat=6):
        for endpoint_left in COLORS:
            for endpoint_right in COLORS:
                assignment = word + (endpoint_left, endpoint_right)
                actual = matching_sum(cells, assignment, ALL_MASK)
                target = pure_target(word, endpoint_left, endpoint_right)
                if actual != target:
                    ledger.append((
                        "".join(map(str, word)),
                        f"{endpoint_left}{endpoint_right}",
                        str(actual),
                        str(target),
                    ))
    return tuple(ledger)


def quotient_words():
    return tuple(product(COLORS, repeat=5))


def denominator_generator(cells, linear_site, linear_color, words):
    """Vector of e_(linear_site,linear_color) q^[2] in word coordinates."""
    other_sites = tuple(site for site in ODD_SITES if site != linear_site)
    other_mask = sum(1 << site for site in other_sites)
    vector = []
    for word in words:
        assignment = {site: word[index] for index, site in enumerate(ODD_SITES)}
        if assignment[linear_site] != linear_color:
            vector.append(ZERO)
        else:
            vector.append(matching_sum(cells, assignment, other_mask))
    return tuple(vector)


def matrix_rank_from_columns(columns):
    if not columns:
        return 0
    row_count = len(columns[0])
    require(
        all(len(column) == row_count for column in columns),
        "ragged column matrix",
    )
    matrix = [
        [columns[column][row] for column in range(len(columns))]
        for row in range(row_count)
    ]
    pivot_row = 0
    for pivot_column in range(len(columns)):
        pivot = next(
            (
                row for row in range(pivot_row, row_count)
                if matrix[row][pivot_column] != ZERO
            ),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        pivot_value = matrix[pivot_row][pivot_column]
        matrix[pivot_row] = [entry / pivot_value for entry in matrix[pivot_row]]
        for row in range(row_count):
            multiplier = matrix[row][pivot_column]
            if row != pivot_row and multiplier:
                matrix[row] = [
                    entry - multiplier * pivot_entry
                    for entry, pivot_entry in zip(
                        matrix[row], matrix[pivot_row]
                    )
                ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def basis_vector(index, size):
    return tuple(ONE if position == index else ZERO for position in range(size))


def audit_packet(name, cells, kappa):
    eqsystem = enumerate_eqsystem(cells)
    require(
        eqsystem == EXPECTED_FAILURES[name],
        f"{name}: independently enumerated EqSystem ledger differs",
    )

    words = quotient_words()
    word_index = {word: index for index, word in enumerate(words)}
    labels = tuple(product(ODD_SITES, COLORS))
    denominator = tuple(
        denominator_generator(cells, site, color, words)
        for site, color in labels
    )
    denominator_rank = matrix_rank_from_columns(denominator)
    expected_rank = 7 if name == "direct_free" else 8
    require(
        denominator_rank == expected_rank,
        f"{name}: denominator rank {denominator_rank}, expected {expected_rank}",
    )

    pure_vector = basis_vector(word_index[PURE_WORD], len(words))
    require(
        matrix_rank_from_columns(denominator + (pure_vector,))
        == denominator_rank + 1,
        f"{name}: pure output [00000] is zero in the quotient",
    )

    mixed_tags = tuple(dict.fromkeys(tag for tag, _, _ in EXPECTED_MIXED[name]))
    witness_ledger = {}
    descended = []
    for tag in mixed_tags:
        word = tuple(map(int, tag))
        coordinate = word_index[word]
        witnesses = tuple(
            (site, color, column[coordinate])
            for (site, color), column in zip(labels, denominator)
            if column[coordinate] != ZERO
        )
        witness_ledger[tag] = witnesses
        if not witnesses:
            descended.append(tag)

    if name == "direct_free":
        require(
            witness_ledger == {"12112": (), "12212": ()},
            "direct_free: exact mixed-coordinate descent ledger differs",
        )
    else:
        require(
            witness_ledger == {
                "02012": (),
                "22012": ((2, 2, ONE), (4, 1, ONE)),
            },
            "tilted: 22012 boundary witnesses differ",
        )

    normalized = []
    for tag, endpoints, expected_residual in EXPECTED_MIXED[name]:
        full_word = (0,) + tuple(map(int, tag))
        endpoint_left, endpoint_right = map(int, endpoints)
        assignment = full_word + (endpoint_left, endpoint_right)
        actual = matching_sum(cells, assignment, ALL_MASK)
        target = pure_target(full_word, endpoint_left, endpoint_right)
        residual = actual - target
        require(target == ZERO, f"{name}: {tag}/{endpoints} target is nonzero")
        require(
            residual == expected_residual and residual != ZERO,
            f"{name}: {tag}/{endpoints} is not the frozen nonzero defect",
        )
        require(
            ("".join(map(str, full_word)), endpoints, str(actual), "0")
            in eqsystem,
            f"{name}: {tag}/{endpoints} is absent from failure ledger",
        )
        if tag in descended:
            scale = -kappa / residual
            output = scale * residual
            require(
                output == -kappa,
                f"{name}: normalized reset at {tag}/{endpoints} differs",
            )
            normalized.append((tag, endpoints, str(scale), str(output)))

    if name == "direct_free":
        require(
            tuple(item[0] for item in normalized)
            == ("12112", "12212", "12212"),
            "direct_free: descended normalized-row set differs",
        )
        # P_12112 - P_12212 sends e_12112 to e_00000.  The input is
        # nonzero because epsilon_12112 kills the entire denominator; the
        # output is nonzero by the augmented-rank check above.
        input_vector = basis_vector(
            word_index[(1, 2, 1, 1, 2)], len(words)
        )
        require(
            matrix_rank_from_columns(denominator + (input_vector,))
            == denominator_rank + 1,
            "direct_free: [12112] unexpectedly vanishes",
        )
        zero_indeterminacy_failure = True
    else:
        require(
            tuple(item[0] for item in normalized) == ("02012",),
            "tilted: a non-descended row was normalized as a quotient map",
        )
        zero_indeterminacy_failure = False

    return {
        "eqsystem_failures": [list(row) for row in eqsystem],
        "denominator_rank": denominator_rank,
        "witnesses": {
            tag: [[site, color, str(value)] for site, color, value in entries]
            for tag, entries in witness_ledger.items()
        },
        "descended": descended,
        "normalized": [list(row) for row in normalized],
        "zero_indeterminacy_failure": zero_indeterminacy_failure,
    }


def main():
    ledger = {
        name: audit_packet(name, cells, kappa)
        for name, (cells, kappa) in PACKETS.items()
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    require(digest == EXPECTED_DIGEST, "independent audit digest differs")
    print("independent h=3 mixed-word reset audit: PASS")
    print("EqSystem ledgers: direct-free 6 failures; tilted 7 failures")
    print("descended tags: direct-free 12112,12212; tilted 02012")
    print("tilted 22012 witnesses: (site 2,color 2), (site 4,color 1)")
    print("quotient reset is not a source-chain lift; zero indeterminacy fails")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
