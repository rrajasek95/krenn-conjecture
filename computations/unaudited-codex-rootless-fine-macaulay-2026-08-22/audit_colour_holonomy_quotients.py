#!/usr/bin/env python3
"""Exact quotient census for the alternating rootless holonomy packet.

The calculation deliberately starts from the literal decorated monomials and
only then forgets colour data.  It tests a ladder of quotients between the
uncoloured physical multigraph and the full decorated monomial.
"""

from collections import defaultdict
from itertools import permutations
from pathlib import Path
import argparse
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from audit_physical_graph_quotient import P, PM8, chi, holonomy, localizers


RESULTS = HERE / "results_colour_holonomy_quotients.json"


def add(row, key, value):
    row[key] = (row[key] + value) % P
    if row[key] == 0:
        del row[key]


def edge_data(term):
    return tuple((u, v, a, b) for u, v, a, b in term)


def physical(term):
    return tuple((u, v) for u, v, _, _ in term)


def site_colour_counts(term):
    counts = [[0] * 3 for _ in range(8)]
    for u, v, a, b in term:
        counts[u][a] += 1
        counts[v][b] += 1
    return tuple(tuple(row) for row in counts)


def colour_pair_histogram(term):
    counts = [0] * 9
    for _, _, a, b in term:
        counts[3 * a + b] += 1
    return tuple(counts)


def edge_relation(term):
    # Retain, on every labelled physical edge occurrence, equality versus the
    # two oriented nonzero differences in Z/3.
    return tuple((u, v, (b - a) % 3) for u, v, a, b in term)


def edge_unordered_pair(term):
    return tuple((u, v, min(a, b), max(a, b)) for u, v, a, b in term)


def apply_colour_perm(term, perm):
    return tuple(sorted((u, v, perm[a], perm[b]) for u, v, a, b in term))


COLOUR_PERMS = tuple(permutations(range(3)))


def global_s3_orbit(term):
    return min(apply_colour_perm(term, perm) for perm in COLOUR_PERMS)


def global_c3_orbit(term):
    cyclic = ((0, 1, 2), (1, 2, 0), (2, 0, 1))
    return min(apply_colour_perm(term, perm) for perm in cyclic)


QUOTIENTS = {
    "physical": lambda term: physical(term),
    "global_colour_pair_histogram": colour_pair_histogram,
    "physical_site_colour_counts": lambda term: (physical(term), site_colour_counts(term)),
    "physical_global_colour_pair_histogram": lambda term: (physical(term), colour_pair_histogram(term)),
    "edge_z3_difference": edge_relation,
    "edge_unordered_colour_pair": edge_unordered_pair,
    "full_mod_global_s3": global_s3_orbit,
    "full_mod_global_c3": global_c3_orbit,
    "full": edge_data,
}


FIRST_FORCED_CLEAN_QUOTIENTS = (
    ((0, 3, 0, 1), (1, 4, 0, 0), (2, 3, 0, 0), (3, 5, 0, 0),
     (4, 5, 0, 0), (4, 5, 1, 1), (6, 7, 0, 0)),
    ((0, 3, 0, 1), (1, 5, 0, 0), (2, 3, 0, 0), (3, 4, 0, 0),
     (4, 5, 0, 0), (4, 5, 1, 1), (6, 7, 0, 0)),
    ((0, 4, 0, 1), (1, 3, 0, 0), (2, 3, 0, 0), (3, 5, 1, 1),
     (4, 5, 0, 0), (4, 5, 0, 0), (6, 7, 0, 0)),
    ((0, 4, 0, 1), (1, 5, 0, 0), (2, 3, 0, 0), (3, 4, 0, 0),
     (3, 5, 1, 1), (4, 5, 0, 0), (6, 7, 0, 0)),
)

HAMMING_CERTIFICATE_WORDS = tuple(
    tuple(int(ch) for ch in word)
    for word in (
        "10000000", "11111110", "12111111", "12121111", "20000000",
        "21111110", "21111111", "21112111", "22111111",
    )
)


def localised_clean():
    out = defaultdict(int)
    for term, coefficient in chi().items():
        for multiplier in localizers():
            add(out, tuple(sorted(term + multiplier)), coefficient)
    return dict(out)


def project(poly, key):
    out = defaultdict(int)
    for term, coefficient in poly.items():
        add(out, key(term), coefficient)
    return dict(out)


def multiset_difference(term, divisor):
    remaining = list(term)
    for item in divisor:
        try:
            remaining.remove(item)
        except ValueError:
            return None
    return tuple(sorted(remaining))


def matching_term(word, matching):
    return tuple(sorted((u, v, word[u], word[v]) for u, v in matching))


def word_code(word):
    out = 0
    power = 1
    for value in word:
        out += value * power
        power *= 3
    return out


def divisor_candidates(term):
    by_edge = defaultdict(set)
    for u, v, a, b in term:
        by_edge[(u, v)].add((a, b))
    out = set()
    for matching_index, matching in enumerate(PM8):
        if any(edge not in by_edge for edge in matching):
            continue
        choices = [tuple(by_edge[edge]) for edge in matching]
        # Four edges only; keeping this explicit is faster than a generic
        # Cartesian-product helper in the 18,630-term hot loop.
        for c0 in choices[0]:
            for c1 in choices[1]:
                for c2 in choices[2]:
                    for c3 in choices[3]:
                        word = [0] * 8
                        for (u, v), (a, b) in zip(matching, (c0, c1, c2, c3)):
                            word[u], word[v] = a, b
                        if len(set(word)) == 1:
                            continue
                        out.add((word_code(word), matching_index, tuple(word)))
    return out


def semigroup_key(term):
    graph = [0] * 28
    pairs = [0] * 9
    edge_index = {(u, v): i for i, (u, v) in enumerate(
        (edge for u in range(8) for edge in ((u, v) for v in range(u + 1, 8)))
    )}
    for u, v, a, b in term:
        graph[edge_index[(u, v)]] += 1
        pairs[3 * a + b] += 1
    return tuple(graph + pairs)


def key_add(left, right):
    return tuple(a + b for a, b in zip(left, right))


def row_add(row, column, coefficient):
    value = (row.get(column, 0) + coefficient) % P
    if value:
        row[column] = value
    elif column in row:
        del row[column]


def inverse(value):
    return pow(value, P - 2, P)


def reduce_row(row, basis):
    while row:
        pivot = min(row)
        base = basis.get(pivot)
        if base is None:
            break
        scale = row[pivot]
        for column, coefficient in base.items():
            row_add(row, column, -scale * coefficient)
    return row


def first_exchange_pair_histogram(h, clean):
    cone = matching_term((0,) * 8, PM8[0])
    exchange = set()
    for term in h:
        product = tuple(sorted(term + cone))
        for code, matching_index, word in divisor_candidates(product):
            divisor = matching_term(word, PM8[matching_index])
            quotient = multiset_difference(product, divisor)
            assert quotient is not None and len(quotient) == 9
            exchange.add((code, word, quotient))

    # The quotient is a semigroup homomorphism.  Rows which become identical
    # are deduplicated before exact sparse elimination.
    projected_rows = {}
    for _, word, quotient in exchange:
        qkey = semigroup_key(quotient)
        row = {}
        for matching in PM8:
            column = key_add(qkey, semigroup_key(matching_term(word, matching)))
            row_add(row, column, 1)
        frozen = tuple(sorted(row.items()))
        projected_rows[frozen] = row

    # Include every literal clean-error multiplier that shares at least one
    # degree-13 target monomial.  This is the complete clean packet in the
    # connected target component at this Macaulay degree, not merely the four
    # quotients discovered by a particular peeling order.
    clean_by_first = defaultdict(list)
    for divisor in clean:
        clean_by_first[min(divisor)].append(divisor)
    clean_quotients = set()
    for term in h:
        product = tuple(sorted(term + cone))
        for first in set(product):
            for divisor in clean_by_first.get(first, ()):
                quotient = multiset_difference(product, divisor)
                if quotient is not None:
                    assert len(quotient) == 7
                    clean_quotients.add(quotient)
    projected_clean_rows = {}
    for quotient in clean_quotients:
        qkey = semigroup_key(quotient)
        row = {}
        for term, coefficient in clean.items():
            row_add(row, key_add(qkey, semigroup_key(term)), coefficient)
        frozen = tuple(sorted(row.items()))
        projected_clean_rows[frozen] = row
    for quotient in FIRST_FORCED_CLEAN_QUOTIENTS:
        qkey = semigroup_key(quotient)
        row = {}
        for term, coefficient in clean.items():
            row_add(row, key_add(qkey, semigroup_key(term)), coefficient)
        frozen = tuple(sorted(row.items()))
        projected_clean_rows[frozen] = row

    target = {}
    cone_key = semigroup_key(cone)
    for term, coefficient in h.items():
        row_add(target, key_add(cone_key, semigroup_key(term)), coefficient)

    # Strengthen the test: allow every abstract semigroup multiplier which
    # can make a projected clean term meet a projected target term.  This is
    # a superset of literal degree-seven monomial multipliers, so failure of
    # membership here is a fortiori a failure for every literal clean row at
    # this degree.
    clean_projected = project(clean, semigroup_key)
    abstract_clean_quotients = set()
    for target_key in target:
        for clean_key in clean_projected:
            difference = tuple(a - b for a, b in zip(target_key, clean_key))
            if min(difference) >= 0:
                abstract_clean_quotients.add(difference)
    abstract_clean_rows = {}
    for quotient_key in abstract_clean_quotients:
        row = {}
        for clean_key, coefficient in clean_projected.items():
            row_add(row, key_add(quotient_key, clean_key), coefficient)
        frozen = tuple(sorted(row.items()))
        abstract_clean_rows[frozen] = row

    basis = {}
    for row in (tuple(projected_rows.values()) + tuple(projected_clean_rows.values())
                + tuple(abstract_clean_rows.values())):
        reduced = reduce_row(dict(row), basis)
        if reduced:
            pivot = min(reduced)
            scale = inverse(reduced[pivot])
            reduced = {column: coefficient * scale % P for column, coefficient in reduced.items()}
            basis[pivot] = reduced
    remainder = reduce_row(dict(target), basis)
    return {
        "literal_exchange_rows": len(exchange),
        "projected_exchange_rows": len(projected_rows),
        "literal_clean_quotients_touching_target": len(clean_quotients),
        "first_forced_clean_quotients": len(FIRST_FORCED_CLEAN_QUOTIENTS),
        "projected_clean_rows": len(projected_clean_rows),
        "abstract_semigroup_clean_quotients_touching_target": len(abstract_clean_quotients),
        "abstract_semigroup_clean_rows": len(abstract_clean_rows),
        "projected_rank": len(basis),
        "target_terms": len(target),
        "remainder_terms": len(remainder),
        "target_in_projected_x5_plus_clean_span": not remainder,
        "remainder_digest": digest(sorted(remainder.items())),
    }


def projected_word_polynomial(word):
    row = {}
    for matching in PM8:
        row_add(row, semigroup_key(matching_term(word, matching)), 1)
    return row


def hamming_shell_joint_certificate(h):
    cone = matching_term((0,) * 8, PM8[0])
    cone_key = semigroup_key(cone)
    target = {}
    for term, coefficient in h.items():
        row_add(target, key_add(cone_key, semigroup_key(term)), coefficient)

    generators = [(word, projected_word_polynomial(word)) for word in HAMMING_CERTIFICATE_WORDS]
    quotient_sets = []
    rows = {}
    for word, generator in generators:
        quotients = set()
        for target_key in target:
            for term_key in generator:
                difference = tuple(a - b for a, b in zip(target_key, term_key))
                if min(difference) >= 0:
                    quotients.add(difference)
        quotient_sets.append((word, len(quotients)))
        for quotient in quotients:
            row = {}
            for term_key, coefficient in generator.items():
                row_add(row, key_add(quotient, term_key), coefficient)
            rows[(word, quotient)] = row

    basis = {}
    for row in rows.values():
        reduced = reduce_row(dict(row), basis)
        if reduced:
            pivot = min(reduced)
            scale = inverse(reduced[pivot])
            basis[pivot] = {column: coefficient * scale % P
                            for column, coefficient in reduced.items()}
    remainder = reduce_row(dict(target), basis)
    return {
        "words": ["".join(map(str, word)) for word in HAMMING_CERTIFICATE_WORDS],
        "quotient_counts": {"".join(map(str, word)): count for word, count in quotient_sets},
        "rows": len(rows),
        "rank": len(basis),
        "target_terms": len(target),
        "remainder_terms": len(remainder),
        "target_in_nine_word_joint_span": not remainder,
        "remainder_digest": digest(sorted(remainder.items())),
    }


def digest(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--check-results", action="store_true")
    args = parser.parse_args()
    h = holonomy()
    c_raw = chi()
    c = localised_clean()
    rows = {}
    for name, key in QUOTIENTS.items():
        hp = project(h, key)
        cp = project(c, key)
        hs = set(hp)
        cs = set(cp)
        rows[name] = {
            "holonomy_nonzero_terms": len(hp),
            "clean_nonzero_terms": len(cp),
            "common_support": len(hs & cs),
            "holonomy_only": len(hs - cs),
            "clean_only": len(cs - hs),
            "holonomy_coefficient_digest": digest(sorted(hp.items(), key=lambda item: repr(item[0]))),
        }

    assert rows["physical"]["holonomy_nonzero_terms"] == 0
    assert rows["full"]["holonomy_nonzero_terms"] == len(h)
    result = {
        "status": "PASS exact colour-holonomy quotient ladder",
        "prime": P,
        "literal_holonomy_terms": len(h),
        "literal_localised_clean_terms": len(c),
        "quotients": rows,
        "first_exchange_pair_histogram": first_exchange_pair_histogram(h, c_raw),
        "hamming_shell_joint_certificate": hamming_shell_joint_certificate(h),
        "scope": (
            "Each quotient is applied only after exact decorated collection. "
            "The census is a support/coefficient projection theorem, not ideal membership."
        ),
    }
    output = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write_results:
        RESULTS.write_text(output)
    if args.check_results and RESULTS.read_text() != output:
        raise RuntimeError("stored colour-holonomy result changed")
    print(output, end="")


if __name__ == "__main__":
    main()
