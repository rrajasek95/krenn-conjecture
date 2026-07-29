#!/usr/bin/env python3
"""Clean-room audit of the 157 sole-defect packet obstructions.

This checker imports no primary packet code or primary ledger.  It rebuilds
the selector/packet reduction, support quotient, coefficient tori, qF
kernels, and common-power ideals.  Deliberate independent choices include
maximal orbit representatives, descending edge encodings, alternative bad
coordinates and reversed good axes, rightmost-pivot elimination, reversed
equation/variable streams, and Singular's ``Dp`` order.

The 145 constant cases are checked over QQ.  In the twelve full-packet
cases, symbolic elimination is permitted to divide only by Laurent units
``c*mu^k``.  The final ideals live in QQ[mu,eta]/(mu*eta-1), so no factor
other than the stipulated nonzero coefficient parameter is inverted.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
from functools import cache
import hashlib
from itertools import combinations, permutations, product
from math import gcd
import shutil
import subprocess
import time

import sympy as sp

from audit_sole_defect_distinct_common_power_independent import (
    PAIRS,
    SITES,
    all_cells,
    cell_key,
    lift_terms,
    linear_kernel,
    local_model,
    q2_generators,
    right_pivot_rref,
    singular_unit,
)


BAD = 0
GOOD = (5, 4, 3, 2, 1)
GOOD_EDGES = tuple(
    sorted((tuple(sorted(edge, reverse=True))
            for edge in combinations(GOOD, 2)), reverse=True)
)
MU = sp.Symbol("mu")
ETA = "eta"

# The normalized slice and its residual stabilizer.  ``k1`` means one
# selected incident pair, ``k2`` two selected incident pairs.
TYPES = (
    ("rank1_k2", "rank1", 2),
    ("rank1_k1", "rank1", 1),
    ("coincident_k2", "coincident", 2),
    ("coincident_k1", "coincident", 1),
    ("circuit_k2", "circuit", 2),
)

EXPECTED_COUNTS = {
    "circuit_k2": (294, 6, 6, 0),
    "coincident_k1": (85, 14, 14, 0),
    "coincident_k2": (560, 64, 58, 6),
    "rank1_k1": (51, 9, 9, 0),
    "rank1_k2": (294, 64, 58, 6),
}


def edge(u, v):
    return tuple(sorted((u, v), reverse=True))


def map_edge(pair, site_permutation):
    return edge(site_permutation[pair[0]], site_permutation[pair[1]])


def map_family(family, site_permutation):
    return tuple(sorted(
        (map_edge(pair, site_permutation) for pair in family), reverse=True
    ))


def packet(anchor, mask):
    arms = tuple(edge(anchor, site) for site in GOOD if site != anchor)
    return tuple(sorted(
        (edge(BAD, anchor),)
        + tuple(pair for bit, pair in enumerate(arms) if mask & (1 << bit)),
        reverse=True,
    ))


@cache
def transformations(name):
    """Residual stabilizer of the normalized selected-SDR slice."""
    if name.endswith("_k1"):
        site_permutations = tuple(
            (0, 1) + tail for tail in permutations((2, 3, 4, 5))
        )
        field_orders = (
            ((0, 2, 1), (0, 1, 2))
            if name == "rank1_k1" else ((0, 1, 2),)
        )
        return tuple(
            (site_permutation, order)
            for site_permutation in reversed(site_permutations)
            for order in field_orders
        )

    fixed_tail = tuple(permutations((3, 4, 5)))
    output = [
        ((0, 1, 2) + tail, (0, 1, 2))
        for tail in reversed(fixed_tail)
    ]
    if name in {"circuit_k2", "rank1_k2"}:
        output.extend(
            ((0, 2, 1) + tail, (1, 0, 2))
            for tail in reversed(fixed_tail)
        )
    return tuple(output)


def canonical(name, families):
    """Maximal representative, unlike the primary minimal convention."""
    return max(
        tuple(
            map_family(families[old_field], site_permutation)
            for old_field in order
        )
        for site_permutation, order in transformations(name)
    )


def labelled_supports(name):
    if name.endswith("_k1"):
        for mask in reversed(range(16)):
            incident = packet(1, mask)
            for first, second in reversed(tuple(permutations(GOOD_EDGES, 2))):
                yield (incident, (first,), (second,))
        return

    for first_mask in reversed(range(16)):
        for second_mask in reversed(range(16)):
            for outside in reversed(GOOD_EDGES):
                yield (packet(1, first_mask), packet(2, second_mask), (outside,))


def vector_rank(vectors):
    if not vectors:
        return 0
    rows = [list(map(Fraction, vector)) for vector in vectors]
    rank = 0
    for column in range(len(rows[0])):
        pivot = next((row for row in range(rank, len(rows))
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        scale = rows[rank][column]
        rows[rank] = [entry / scale for entry in rows[rank]]
        for row in range(len(rows)):
            if row == rank or not rows[row][column]:
                continue
            scale = rows[row][column]
            rows[row] = [a - scale * b for a, b in zip(rows[row], rows[rank])]
        rank += 1
    return rank


def locally_separable(kind, killed):
    """Existence of a bad-site map killing exactly the requested fields."""
    _, bad_vectors = local_model(kind)
    killed_vectors = [bad_vectors[field] for field in killed]
    killed_rank = vector_rank(killed_vectors)
    for field in range(3):
        if field in killed:
            continue
        if vector_rank(killed_vectors + [bad_vectors[field]]) == killed_rank:
            return False
    return True


def has_separable_sdr(kind, families):
    for choice in product(*tuple(reversed(family) for family in families)):
        if len(set(choice)) != 3:
            continue
        killed = frozenset(
            field for field, pair in enumerate(choice) if BAD in pair
        )
        if locally_separable(kind, killed):
            return True
    return False


@cache
def orbit_data(name, kind):
    counts = Counter()
    labelled = 0
    for families in labelled_supports(name):
        counts[canonical(name, families)] += 1
        labelled += 1
    expected_labelled = 1440 if name.endswith("_k1") else 2560
    assert labelled == expected_labelled == sum(counts.values())
    representatives = tuple(sorted(counts, reverse=True))
    residual = tuple(
        families for families in representatives
        if not has_separable_sdr(kind, families)
    )
    return representatives, residual, counts


def audit_selector_packet_reduction():
    """Exhaust (7) for every labelled distinct selected-pair triple."""
    triples = 0
    isolated = 0
    packets = 0
    for selected in permutations(PAIRS, 3):
        triples += 1
        assert len(set(selected)) == 3
        for chosen in selected:
            killed_good = frozenset(chosen) - {BAD}
            survivors = tuple(
                pair for pair in PAIRS
                if killed_good <= frozenset(pair)
            )
            assert chosen in survivors
            assert all(killed_good <= frozenset(pair) for pair in survivors)
            # Every killed vector is omitted from every surviving lift.
            assert all(
                all(site in pair for site in killed_good)
                for pair in survivors
            )
            if BAD in chosen:
                anchor = next(site for site in chosen if site != BAD)
                expected = {edge(BAD, anchor)} | {
                    edge(anchor, site) for site in GOOD if site != anchor
                }
                assert set(survivors) == expected and len(survivors) == 5
                packets += 1
            else:
                assert survivors == (chosen,)
                isolated += 1
    assert triples == 15 * 14 * 13
    assert isolated + packets == 3 * triples
    return triples, isolated, packets


def determinant(matrix):
    if not matrix:
        return 1
    work = [list(map(Fraction, row)) for row in matrix]
    result = Fraction(1)
    for column in range(len(work)):
        pivot = next((row for row in range(column, len(work))
                      if work[row][column]), None)
        if pivot is None:
            return 0
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            result *= -1
        scale = work[column][column]
        result *= scale
        for entry in range(column, len(work)):
            work[column][entry] /= scale
        for row in range(column + 1, len(work)):
            scale = work[row][column]
            for entry in range(column, len(work)):
                work[row][entry] -= scale * work[column][entry]
    assert result.denominator == 1
    return result.numerator


def coefficient_character(pair):
    return tuple(int(site not in pair) for site in GOOD)


def exponent_audit(family):
    """Rank, saturation, and a no-root unimodular chart for one field."""
    matrix = tuple(coefficient_character(pair) for pair in family)
    rank = vector_rank(matrix)
    minors = []
    for row_selection in combinations(range(len(matrix)), rank):
        for column_selection in combinations(range(5), rank):
            minor = determinant(tuple(
                tuple(matrix[row][column] for column in column_selection)
                for row in row_selection
            ))
            if minor:
                minors.append(abs(minor))
    content = 0
    for minor in minors:
        content = gcd(content, minor)
    assert content == 1 and 1 in minors
    if len(family) < 5:
        assert rank == len(family)
        return "normalizable", None

    assert len(family) == 5 and rank == 4
    assert sum(BAD in pair for pair in family) == 1
    relation = tuple(-3 if BAD in pair else 1 for pair in family)
    assert all(
        sum(relation[row] * matrix[row][column] for row in range(5)) == 0
        for column in range(5)
    )
    return "parameter", relation


def coefficient_classification(residual):
    full_fields = []
    for field, family in enumerate(residual):
        status, relation = exponent_audit(family)
        if status == "parameter":
            full_fields.append((field, relation))
    assert len(full_fields) <= 1
    return "parameter" if full_fields else "normalized"


def constant_weighted(families):
    return tuple(
        tuple((pair, Fraction(1)) for pair in reversed(family))
        for family in reversed(families)
    )


def parameter_weighted(families):
    full_fields = tuple(
        field for field, family in enumerate(families) if len(family) == 5
    )
    assert len(full_fields) == 1
    full_field = full_fields[0]
    # The primary puts mu on its lexicographically maximal ascending arm.
    # Put it on the minimal descending arm of our maximal representative.
    parameter_pair = min(
        pair for pair in families[full_field] if BAD not in pair
    )
    normalized_rows = tuple(
        coefficient_character(pair)
        for pair in families[full_field] if pair != parameter_pair
    )
    assert len(normalized_rows) == 4 and vector_rank(normalized_rows) == 4
    assert any(
        abs(determinant(tuple(
            tuple(row[column] for column in columns)
            for row in normalized_rows
        ))) == 1
        for columns in combinations(range(5), 4)
    )
    weighted = []
    for field in reversed(range(3)):
        entries = []
        for pair in reversed(families[field]):
            weight = MU if field == full_field and pair == parameter_pair else sp.Integer(1)
            entries.append((pair, weight))
        weighted.append((field, tuple(entries)))
    return tuple(weighted), full_field, parameter_pair


def target_terms_weighted(weighted, bad_vectors, symbolic=False):
    zero = sp.Integer(0) if symbolic else Fraction(0)
    target = defaultdict(lambda: zero)
    if symbolic:
        stream = weighted
    else:
        # constant_weighted deliberately stores fields in 2,1,0 order
        stream = tuple((2 - index, family) for index, family in enumerate(weighted))
    for field, family in stream:
        for pair, weight in family:
            for word, coefficient in lift_terms(pair, field, bad_vectors).items():
                target[word] += weight * coefficient
    return {
        word: (sp.cancel(coefficient) if symbolic else coefficient)
        for word, coefficient in target.items() if coefficient != 0
    }


def qf_rows_weighted(weighted, bad_vectors, cells, symbolic=False):
    """Literal multiplication of every q cell by every active lift."""
    zero = sp.Integer(0) if symbolic else Fraction(0)
    rows = defaultdict(lambda: defaultdict(lambda: zero))
    index = {cell: column for column, cell in enumerate(cells)}
    if symbolic:
        stream = weighted
    else:
        stream = tuple((2 - number, family) for number, family in enumerate(weighted))
    for field, family in stream:
        for pair, weight in family:
            for lift_word, coefficient in lift_terms(pair, field, bad_vectors).items():
                occupied = frozenset(
                    site for site, coordinate in enumerate(lift_word)
                    if coordinate is not None
                )
                for cell in reversed(cells):
                    u, v, cu, cv = cell
                    if u in occupied or v in occupied:
                        continue
                    word = list(lift_word)
                    word[u], word[v] = cu, cv
                    rows[tuple(word)][index[cell]] += weight * coefficient
    output = []
    for word in sorted(rows, reverse=True):
        row = {}
        for column, coefficient in rows[word].items():
            coefficient = sp.cancel(coefficient) if symbolic else coefficient
            if coefficient != 0:
                row[column] = coefficient
        if row:
            output.append(row)
    return tuple(reversed(output))


def constant_ledger(name, families, cells, rows, pivots, generators):
    digest = hashlib.sha256()
    digest.update(repr((name, families)).encode("ascii"))
    for title, stream in (
        (b"CELLS", cells),
        (b"ROWS", rows),
        (b"RIGHT_PIVOTS", tuple(pivots.items())),
        (b"Q2_GENERATORS", generators),
    ):
        digest.update(b"\n" + title + b"\n")
        for item in reversed(stream):
            if isinstance(item, dict):
                item = tuple(sorted(item.items(), reverse=True))
            digest.update(repr(item).encode("ascii") + b"\n")
    return digest.hexdigest()


def build_constant_case(name, kind, families):
    dims, bad_vectors = local_model(kind)
    cells = all_cells(dims)
    weighted = constant_weighted(families)
    rows = qf_rows_weighted(weighted, bad_vectors, cells)
    pivots = right_pivot_rref(rows)
    free, expressions = linear_kernel(cells, pivots)
    target = target_terms_weighted(weighted, bad_vectors)
    generators = q2_generators(dims, expressions, target)
    digest = constant_ledger(name, families, cells, rows, pivots, generators)
    return dims, cells, rows, pivots, free, generators, digest


def laurent_unit(expression):
    expression = sp.cancel(expression)
    if expression == 0:
        return False
    numerator, denominator = sp.fraction(expression)
    for part in (numerator, denominator):
        coefficient, exponent = part.as_coeff_exponent(MU)
        if not coefficient.is_Rational or exponent < 0:
            return False
        if sp.expand(part - coefficient * MU**exponent) != 0:
            return False
    return True


def right_laurent_rref(source_rows):
    """Right-pivot RREF, dividing only by units of QQ[mu,mu^-1]."""
    pivots = {}
    inverted = []
    for source in source_rows:
        row = {
            column: sp.cancel(value)
            for column, value in source.items() if sp.cancel(value) != 0
        }
        for column in sorted(pivots, reverse=True):
            if column not in row:
                continue
            scale = row[column]
            for key, value in pivots[column].items():
                updated = sp.cancel(row.get(key, 0) - scale * value)
                if updated == 0:
                    row.pop(key, None)
                else:
                    row[key] = updated
        if not row:
            continue
        available = tuple(
            column for column in sorted(row, reverse=True)
            if laurent_unit(row[column])
        )
        assert available, (
            "independent reduction encountered a non-Laurent pivot row",
            tuple((key, str(value)) for key, value in sorted(row.items())),
        )
        pivot = available[0]
        scale = sp.cancel(row[pivot])
        assert laurent_unit(scale)
        inverted.append(scale)
        row = {key: sp.cancel(value / scale) for key, value in row.items()}
        for old in pivots.values():
            if pivot not in old:
                continue
            scale = old[pivot]
            for key, value in row.items():
                updated = sp.cancel(old.get(key, 0) - scale * value)
                if updated == 0:
                    old.pop(key, None)
                else:
                    old[key] = updated
        pivots[pivot] = row
        pivots = dict(sorted(pivots.items(), reverse=True))
    assert all(laurent_unit(scale) for scale in inverted)
    return pivots, tuple(inverted)


def symbolic_kernel(cells, pivots):
    free = tuple(
        column for column in reversed(range(len(cells))) if column not in pivots
    )
    free_number = {column: number for number, column in enumerate(free)}
    expressions = {}
    for column, cell in enumerate(cells):
        if column in free_number:
            expressions[cell] = {free_number[column]: sp.Integer(1)}
        else:
            expressions[cell] = {
                free_number[key]: sp.cancel(-coefficient)
                for key, coefficient in pivots[column].items()
                if key != column and coefficient != 0
            }
    return free, expressions


def add_symbolic(destination, source, scale=sp.Integer(1)):
    for monomial, coefficient in source.items():
        updated = sp.cancel(destination.get(monomial, 0) + scale * coefficient)
        if updated == 0:
            destination.pop(monomial, None)
        else:
            destination[monomial] = updated


def multiply_symbolic(left, right):
    output = {}
    for first, first_coefficient in left.items():
        for second, second_coefficient in right.items():
            monomial = tuple(sorted((first, second), reverse=True))
            updated = sp.cancel(
                output.get(monomial, 0) + first_coefficient * second_coefficient
            )
            if updated == 0:
                output.pop(monomial, None)
            else:
                output[monomial] = updated
    return output


def symbolic_q2_generators(dims, expressions, target):
    generators = []
    # Reversed supports, coordinate words, and a rotated matching order.
    matchings = ((1, 3, 0, 2), (0, 3, 1, 2), (0, 1, 2, 3))
    for support in reversed(tuple(combinations(SITES, 4))):
        ranges = tuple(reversed(range(dims[site])) for site in support)
        for local in reversed(tuple(product(*ranges))):
            polynomial = {}
            for i, j, k, ell in matchings:
                left = expressions[cell_key(
                    support[i], local[i], support[j], local[j]
                )]
                right = expressions[cell_key(
                    support[k], local[k], support[ell], local[ell]
                )]
                add_symbolic(polynomial, multiply_symbolic(left, right))
            full_word = [None] * 6
            for site, coordinate in zip(support, local):
                full_word[site] = coordinate
            constant = target.get(tuple(full_word), 0)
            if constant != 0:
                add_symbolic(polynomial, {(): -constant})
            if polynomial:
                generators.append(polynomial)
    return tuple(generators)


def rational_text(value):
    value = sp.Rational(value)
    if value.q == 1:
        return str(value.p)
    return f"({value.p}/{value.q})"


def laurent_coefficient_text(expression):
    """Map QQ[mu,mu^-1] into QQ[mu,eta]/(mu*eta-1)."""
    expression = sp.cancel(expression)
    numerator, denominator = sp.fraction(expression)
    denominator_coefficient, denominator_exponent = denominator.as_coeff_exponent(MU)
    assert denominator_coefficient.is_Rational and denominator_exponent >= 0
    assert sp.expand(
        denominator - denominator_coefficient * MU**denominator_exponent
    ) == 0, expression
    polynomial = sp.Poly(sp.expand(numerator / denominator_coefficient), MU)
    pieces = []
    for (numerator_exponent,), coefficient in polynomial.terms():
        factors = []
        if coefficient != 1 or not numerator_exponent and not denominator_exponent:
            factors.append(rational_text(coefficient))
        if numerator_exponent:
            factors.append("mu" if numerator_exponent == 1 else f"mu^{numerator_exponent}")
        if denominator_exponent:
            factors.append(ETA if denominator_exponent == 1 else f"{ETA}^{denominator_exponent}")
        pieces.append("*".join(factors) if factors else "1")
    return "+".join(f"({piece})" for piece in pieces) or "0"


def symbolic_polynomial_text(polynomial):
    pieces = []
    for monomial in sorted(
            polynomial, key=lambda item: (len(item), item), reverse=True):
        coefficient = polynomial[monomial]
        coefficient_text = laurent_coefficient_text(coefficient)
        if monomial:
            variables = "*".join(f"y{index}" for index in monomial)
            pieces.append(f"({coefficient_text})*({variables})")
        else:
            pieces.append(f"({coefficient_text})")
    return "+".join(pieces)


def parameter_ledger(name, families, full_field, parameter_pair, cells, rows,
                     pivots, inverted, generators):
    digest = hashlib.sha256()
    digest.update(
        repr((name, families, full_field, parameter_pair)).encode("ascii")
    )
    for title, stream in (
        (b"CELLS", cells),
        (b"LAURENT_ROWS", rows),
        (b"RIGHT_LAURENT_PIVOTS", tuple(pivots.items())),
        (b"INVERTED", inverted),
        (b"Q2_GENERATORS", generators),
    ):
        digest.update(b"\n" + title + b"\n")
        for item in reversed(stream):
            if isinstance(item, dict):
                item = tuple(
                    (key, str(value))
                    for key, value in sorted(item.items(), reverse=True)
                )
            elif title == b"INVERTED":
                item = str(item)
            digest.update(repr(item).encode("ascii") + b"\n")
    return digest.hexdigest()


def build_parameter_case(name, kind, families):
    dims, bad_vectors = local_model(kind)
    cells = all_cells(dims)
    weighted, full_field, parameter_pair = parameter_weighted(families)
    rows = qf_rows_weighted(weighted, bad_vectors, cells, symbolic=True)
    pivots, inverted = right_laurent_rref(rows)
    # This assertion is the central specialization audit: constants and
    # powers of mu are Laurent units; no mu-1 or other exceptional factor
    # has been inverted.
    assert all(laurent_unit(scale) for scale in inverted)
    free, expressions = symbolic_kernel(cells, pivots)
    target = target_terms_weighted(weighted, bad_vectors, symbolic=True)
    generators = symbolic_q2_generators(dims, expressions, target)
    digest = parameter_ledger(
        name, families, full_field, parameter_pair, cells, rows, pivots,
        inverted, generators,
    )
    return (
        full_field, parameter_pair, dims, cells, rows, pivots, inverted,
        free, generators, digest,
    )


def singular_parameter_unit(free_count, generators, timeout):
    executable = shutil.which("Singular")
    if executable is None:
        raise SystemExit("Singular is required for the full independent audit")
    variables = tuple(f"y{index}" for index in reversed(range(free_count)))
    ring_variables = variables + ("mu", ETA)
    equations = ("(mu)*(eta)-1",) + tuple(
        symbolic_polynomial_text(polynomial) for polynomial in reversed(generators)
    )
    program = (
        f"ring independent=0,({','.join(ring_variables)}),Dp;\n"
        f"ideal I={','.join(equations)};\n"
        "ideal G=slimgb(I);\n"
        'print("AUDIT_SIZE");print(size(G));'
        'print("AUDIT_FIRST");print(G[1]);\n'
    )
    started = time.monotonic()
    result = subprocess.run(
        (executable, "-q"), input=program, text=True, capture_output=True,
        timeout=timeout,
    )
    seconds = time.monotonic() - started
    lines = tuple(line.strip() for line in result.stdout.splitlines() if line.strip())
    status = "ERROR"
    if result.returncode == 0 and "AUDIT_SIZE" in lines and "AUDIT_FIRST" in lines:
        size = lines[lines.index("AUDIT_SIZE") + 1]
        first = lines[lines.index("AUDIT_FIRST") + 1]
        status = "UNIT" if size == first == "1" else f"NONUNIT:{size}:{first}"
    return status, seconds, result.stderr


def audit_local_tables():
    expected_nonseparable = {
        "circuit": {frozenset(choice) for choice in combinations(range(3), 2)},
        "coincident": {
            frozenset((0,)), frozenset((2,)),
            frozenset((0, 1)), frozenset((1, 2)),
        },
        "rank1": {
            frozenset(choice)
            for size in (1, 2) for choice in combinations(range(3), size)
        },
    }
    for kind, expected in expected_nonseparable.items():
        actual = {
            frozenset(choice)
            for size in range(4) for choice in combinations(range(3), size)
            if not locally_separable(kind, frozenset(choice))
        }
        assert actual == expected, (kind, actual, expected)


# Filled from the first clean-room ledger replay and then treated as frozen.
EXPECTED_NORMALIZED = {
    "circuit_k2": "01930f27cbf9199d81364104ca353b40b9b224cbb8869b7e64791b7ab7436a28",
    "coincident_k1": "b64fbcecc520945b18f3b16710dd132a42247415c2f299242fe7b3e190b5b510",
    "coincident_k2": "12a0378f8dfcf2211eaabd423ca79d7111de0f8a690d70ccf4f71a5fd7a8e907",
    "rank1_k1": "5865f563370fbbb03a2769164589d92dd1638bac714d157132a8b7c93332de99",
    "rank1_k2": "5f944b4d6da9bd2e0f4ec66455fc3cb27e7cac59fcf2c855aba2561139136522",
}
EXPECTED_PARAMETER = {
    "coincident_k2": "3d326aede259c83dcffba26fac1544e6af39642c754a01f1b5ad9c35f8558dbb",
    "rank1_k2": "6eb3b36f984366ae470da827ee36fa3b6b26485f13b0d2979a8b82e5dd85c1c8",
}
EXPECTED_GLOBAL = "6d021a3534732e8815b6931a88664862f9b910a6cfa1dd7fdbd009403224022c"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", action="append",
                        choices=tuple(name for name, _, _ in TYPES))
    parser.add_argument("--case", action="append", type=int)
    parser.add_argument("--ledger-only", action="store_true")
    parser.add_argument("--timeout", type=int, default=900)
    parser.add_argument("--quiet-cases", action="store_true")
    args = parser.parse_args()

    audit_local_tables()
    triples, isolated, packets = audit_selector_packet_reduction()
    print({
        "selected_distinct_triples": triples,
        "isolated_field_selections": isolated,
        "anchored_packet_selections": packets,
    }, flush=True)

    selected_types = set(args.type) if args.type else None
    total_initial = total_residual = total_normalized = total_parameter = 0
    total_units = 0
    global_digest = hashlib.sha256()
    all_inverted = Counter()
    rank_census = Counter()

    for name, kind, killed_size in TYPES:
        if selected_types is not None and name not in selected_types:
            continue
        representatives, residual, orbit_counts = orbit_data(name, kind)
        normalized = tuple(
            families for families in residual
            if coefficient_classification(families) == "normalized"
        )
        parameter = tuple(
            families for families in residual
            if coefficient_classification(families) == "parameter"
        )
        counts = (
            len(representatives), len(residual), len(normalized), len(parameter)
        )
        assert counts == EXPECTED_COUNTS[name], (name, counts)
        print(name, {
            "labelled": sum(orbit_counts.values()),
            "initial_orbits": len(representatives),
            "residual": len(residual),
            "normalized": len(normalized),
            "parameter": len(parameter),
            "orbit_sizes": dict(sorted(Counter(orbit_counts.values()).items())),
        }, flush=True)
        total_initial += len(representatives)
        total_residual += len(residual)
        total_normalized += len(normalized)
        total_parameter += len(parameter)

        normalized_digest = hashlib.sha256()
        selected_normalized = args.case if args.case is not None else range(len(normalized))
        for case in selected_normalized:
            families = normalized[case]
            dims, cells, rows, pivots, free, generators, digest = build_constant_case(
                name, kind, families
            )
            status, seconds, stderr = ("SKIPPED", 0.0, "")
            if not args.ledger_only:
                status, seconds, stderr = singular_unit(
                    len(free), generators, args.timeout
                )
                assert status == "UNIT", (name, "normalized", case, status, stderr)
                total_units += 1
            rank_census[name, "N", len(pivots)] += 1
            if not args.quiet_cases:
                print({
                    "type": name, "class": "normalized", "case": case,
                    "families": families, "dims": dims, "cells": len(cells),
                    "rows": len(rows), "rank": len(pivots),
                    "nullity": len(free), "generators": len(generators),
                    "ledger": digest, "status": status,
                    "seconds": round(seconds, 3),
                }, flush=True)
            normalized_digest.update(f"{case}:{digest}\n".encode("ascii"))
            global_digest.update(f"N:{name}:{case}:{digest}\n".encode("ascii"))
        normalized_hexdigest = normalized_digest.hexdigest()
        print(name, "independent normalized ledger", normalized_hexdigest, flush=True)
        if args.case is None and EXPECTED_NORMALIZED[name]:
            assert normalized_hexdigest == EXPECTED_NORMALIZED[name]

        if parameter:
            parameter_digest = hashlib.sha256()
            selected_parameter = args.case if args.case is not None else range(len(parameter))
            for case in selected_parameter:
                families = parameter[case]
                (
                    full_field, parameter_pair, dims, cells, rows, pivots,
                    inverted, free, generators, digest,
                ) = build_parameter_case(name, kind, families)
                status, seconds, stderr = ("SKIPPED", 0.0, "")
                if not args.ledger_only:
                    status, seconds, stderr = singular_parameter_unit(
                        len(free), generators, args.timeout
                    )
                    assert status == "UNIT", (
                        name, "parameter", case, status, stderr
                    )
                    total_units += 1
                rank_census[name, "P", len(pivots)] += 1
                all_inverted.update(map(str, inverted))
                if not args.quiet_cases:
                    print({
                        "type": name, "class": "parameter", "case": case,
                        "families": families, "full_field": full_field,
                        "parameter_pair": parameter_pair, "dims": dims,
                        "cells": len(cells), "rows": len(rows),
                        "rank": len(pivots), "nullity": len(free),
                        "inverted_factors": tuple(sorted(set(map(str, inverted)))),
                        "generators": len(generators), "ledger": digest,
                        "status": status, "seconds": round(seconds, 3),
                    }, flush=True)
                parameter_digest.update(f"{case}:{digest}\n".encode("ascii"))
                global_digest.update(f"P:{name}:{case}:{digest}\n".encode("ascii"))
            parameter_hexdigest = parameter_digest.hexdigest()
            print(name, "independent parameter ledger", parameter_hexdigest, flush=True)
            if args.case is None and EXPECTED_PARAMETER[name]:
                assert parameter_hexdigest == EXPECTED_PARAMETER[name]

    if args.type is None and args.case is None:
        assert (
            total_initial, total_residual, total_normalized, total_parameter
        ) == (1284, 157, 145, 12)
        if not args.ledger_only:
            assert total_units == 157
    global_hexdigest = global_digest.hexdigest()
    print("totals", {
        "initial": total_initial, "residual": total_residual,
        "normalized": total_normalized, "parameter": total_parameter,
        "unit_ideals": total_units,
        "rank_census": {str(key): value for key, value in sorted(rank_census.items())},
        "inverted_laurent_units": dict(sorted(all_inverted.items())),
    }, flush=True)
    print("independent global ledger", global_hexdigest, flush=True)
    if args.type is None and args.case is None and EXPECTED_GLOBAL:
        assert global_hexdigest == EXPECTED_GLOBAL
    print("independent sole-defect packet audit: PASS", flush=True)


if __name__ == "__main__":
    main()
