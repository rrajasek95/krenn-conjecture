#!/usr/bin/env python3
"""Clean-room exact audit for the three two-pair support profiles.

The primary two-pair builder is deliberately not imported.  This audit uses
a nonlexicographic site order, a different colour order, exact SymPy ranks
only on the small qF matrices, a direct reduction which kills both active
edge blocks, and a sparse monomial-dictionary construction of q^[2]-F.
Singular then checks the resulting unsaturated ideals over QQ.

Profiles are written in descending multiplicity order:

* 211: one colour on both pairs and two singleton colours on distinct pairs;
* 221: two colours on both pairs and one singleton colour; and
* 222: all three colours on both pairs.

No support restriction is placed on q.  Before qF=0 is imposed it has all
15*3*3 endpoint-ordered coordinates.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
from itertools import combinations, product
import shutil
import subprocess
import time

import sympy as sp


# These orders intentionally differ from the primary checker.
SITE_ORDER = (4, 1, 5, 0, 3, 2)
COLOUR_ORDER = (2, 0, 1)
U = frozenset(SITE_ORDER)
POSITION = {site: index for index, site in enumerate(SITE_ORDER)}


def oriented_edge(left: int, right: int) -> tuple[int, int]:
    return (
        (left, right)
        if POSITION[left] < POSITION[right]
        else (right, left)
    )


EDGES = tuple(
    oriented_edge(SITE_ORDER[j], SITE_ORDER[i])
    for i in range(1, 6)
    for j in range(i)
)
assert len(EDGES) == 15 and len(set(EDGES)) == 15

CASES = {
    "adjacent": (
        oriented_edge(SITE_ORDER[0], SITE_ORDER[1]),
        oriented_edge(SITE_ORDER[0], SITE_ORDER[2]),
    ),
    "disjoint": (
        oriented_edge(SITE_ORDER[0], SITE_ORDER[1]),
        oriented_edge(SITE_ORDER[2], SITE_ORDER[3]),
    ),
}

EXPECTED = {
    ("211", "adjacent"): (
        33, "f3a1bb1a22656b22612c095806b35c5bdd66f8449f87738f813c750f7eb01fc6"
    ),
    ("211", "disjoint"): (
        35, "accdf2cd03ae931efe018ee7f3e9857f17404e285cbb9fc5bd97c2e867a7ce5b"
    ),
    ("221", "adjacent"): (
        39, "71054f25fc031313a7a8b12214f484116aeef5a9a93b8bb7026c5d65bb7a75a0"
    ),
    ("221", "disjoint"): (
        43, "8ef0868c49e00e5d82a7af1903dc67e356b4ae2f7e4e95ed7f107c0be2497482"
    ),
    ("222", "adjacent"): (
        45, "7b06d8aad8b9c4eebe180691fc6539643815346265e4dea7857139c2e3b73127"
    ),
    ("222", "disjoint"): (
        51, "e5637a34fc001c205eac4d7e79b547cd1fb3c6a6886c78edc665f639ef685b37"
    ),
}


def has_three_family_sdr(families) -> bool:
    return any(
        len({a, b, c}) == 3
        for a in families[0]
        for b in families[1]
        for c in families[2]
    )


def audit_universal_two_pair_reduction():
    """Finite census of the Hall reduction on a four-element universe.

    The proof is universe-independent: no SDR plus no equal-singleton pair
    gives union size at most two, and nonemptiness makes the size exactly
    two.  Four ambient elements merely provide several labelled copies of
    every surviving two-element shape.
    """
    ambient = tuple(range(4))
    families_available = tuple(
        frozenset(x for x in ambient if mask & (1 << x))
        for mask in range(1, 1 << len(ambient))
    )
    profiles = Counter()
    survivors = 0
    for families in product(families_available, repeat=3):
        equal_singleton = any(
            families[i] == families[j] and len(families[i]) == 1
            for i, j in combinations(range(3), 2)
        )
        if has_three_family_sdr(families) or equal_singleton:
            continue
        union = set().union(*families)
        assert len(union) == 2
        singleton_values = [
            next(iter(family)) for family in families if len(family) == 1
        ]
        assert len(singleton_values) <= 2
        assert len(singleton_values) == len(set(singleton_values))
        profile = tuple(sorted(map(len, families), reverse=True))
        profiles[profile] += 1
        survivors += 1
    assert survivors == 78
    assert profiles == Counter({
        (2, 1, 1): 36,
        (2, 2, 1): 36,
        (2, 2, 2): 6,
    })
    return profiles


def profile_terms(profile: str, pairs: tuple[tuple[int, int], ...]):
    p, q = pairs
    if profile == "211":
        # Colour 2 is double; the two singleton colours occupy distinct
        # physical pairs.  All other labellings are related by pair/colour
        # permutations.
        return ((p, 2), (q, 2), (p, 0), (q, 1))
    if profile == "221":
        # Colours 2 and 0 are double; colour 1 is a singleton on Q.
        return ((p, 2), (q, 2), (p, 0), (q, 0), (q, 1))
    if profile == "222":
        return tuple(
            (pair, colour)
            for colour in COLOUR_ORDER
            for pair in pairs
        )
    raise ValueError(profile)


def endpoint_cell(pair: tuple[int, int], labels: dict[int, int]):
    a, b = pair
    return pair, labels[a], labels[b]


def word_sort_key(word: tuple[int, ...]):
    colour_position = {c: i for i, c in enumerate(COLOUR_ORDER)}
    return tuple(colour_position[c] for c in word)


def qf_matrix(terms, pairs):
    """Collect every literal six-site coordinate of qF.

    Only q-blocks on the missing pair of a target lift can survive.  Columns
    are all 18 endpoint-ordered cells on the two active physical pairs.
    """
    columns = tuple(
        (pair, ca, cb)
        for pair in reversed(pairs)
        for cb in COLOUR_ORDER
        for ca in COLOUR_ORDER
    )
    column_index = {cell: index for index, cell in enumerate(columns)}
    rows_by_word = defaultdict(Counter)

    for pair, base in terms:
        a, b = pair
        for ca, cb in product(COLOUR_ORDER, repeat=2):
            labels = {a: ca, b: cb}
            word_by_site = {site: base for site in SITE_ORDER}
            word_by_site.update(labels)
            word = tuple(word_by_site[site] for site in SITE_ORDER)
            rows_by_word[word][column_index[endpoint_cell(pair, labels)]] += 1

    ordered = tuple(
        (word, rows_by_word[word])
        for word in sorted(rows_by_word, key=word_sort_key)
        if rows_by_word[word]
    )
    dense = sp.Matrix([
        [int(row.get(column, 0)) for column in range(len(columns))]
        for _, row in ordered
    ])
    rank = dense.rank()
    return columns, ordered, dense, rank


def audit_qf_full_active_block_rank(terms, pairs):
    columns, rows, matrix, rank = qf_matrix(terms, pairs)
    assert len(columns) == 18
    assert rank == 18
    # Full column rank means qF=0 sets all 18 cells on P,Q to zero.  Verify
    # this a second way from the exact reduced row echelon form.
    _, pivots = matrix.rref()
    assert pivots == tuple(range(18))
    return columns, rows


def variable_table(pairs):
    """Variables for every q cell off P,Q, in an independent order."""
    active = set(pairs)
    cells = tuple(
        (pair, ca, cb)
        for pair in reversed(EDGES)
        if pair not in active
        for cb in reversed(COLOUR_ORDER)
        for ca in reversed(COLOUR_ORDER)
    )
    assert len(cells) == 13 * 9 == 117
    return {cell: index for index, cell in enumerate(cells)}, cells


def q_cell(variables, u, v, cu, cv):
    pair = oriented_edge(u, v)
    if pair[0] == u:
        cell = pair, cu, cv
    else:
        cell = pair, cv, cu
    return variables.get(cell)


def add_term(polynomial: Counter, monomial: tuple[int, ...],
             coefficient: int) -> None:
    polynomial[monomial] += coefficient
    if polynomial[monomial] == 0:
        del polynomial[monomial]


def matching_polynomials(terms, pairs):
    """Build all 1,215 coefficients of q^[2]-F as sparse dictionaries."""
    variables, cells = variable_table(pairs)
    target = Counter()
    for missing, colour in terms:
        support = frozenset(U - frozenset(missing))
        target[support, colour] += 1

    generators = []
    four_sets = tuple(
        tuple(SITE_ORDER[i] for i in indices)
        for indices in combinations(range(6), 4)
    )
    for support_tuple in four_sets:
        support = frozenset(support_tuple)
        a, b, c, d = support_tuple
        matchings = (
            ((a, b), (c, d)),
            ((a, c), (b, d)),
            ((a, d), (b, c)),
        )
        for local_word in product(COLOUR_ORDER, repeat=4):
            label = dict(zip(support_tuple, local_word))
            polynomial = Counter()
            for (u, v), (x, y) in matchings:
                left = q_cell(variables, u, v, label[u], label[v])
                right = q_cell(variables, x, y, label[x], label[y])
                # qF=0 has already set every active-pair cell to zero.
                if left is None or right is None:
                    continue
                add_term(polynomial, tuple(sorted((left, right))), 1)

            constant = 0
            for colour in COLOUR_ORDER:
                if all(value == colour for value in local_word):
                    constant += target[support, colour]
            if constant:
                add_term(polynomial, (), -constant)
            # Every coefficient happens to remain nontrivial in these cases;
            # retain an assertion so a missing matching cannot pass silently.
            assert polynomial
            generators.append(dict(sorted(polynomial.items())))

    assert len(generators) == 15 * 3**4 == 1215
    return cells, tuple(generators)


def polynomial_string(polynomial: dict[tuple[int, ...], int]) -> str:
    terms = []
    # Constants last gives a stream unlike the primary builder.
    order = sorted(polynomial, key=lambda monomial: (not monomial, monomial))
    for monomial in order:
        coefficient = polynomial[monomial]
        if monomial:
            body = "*".join(f"z{index}" for index in monomial)
            if coefficient == 1:
                terms.append(body)
            elif coefficient == -1:
                terms.append(f"-({body})")
            else:
                terms.append(f"({coefficient})*({body})")
        else:
            terms.append(str(coefficient))
    return "(" + ")+(".join(terms) + ")"


def ledger_digest(profile, case, terms, columns, rows, cells, generators):
    digest = hashlib.sha256()
    digest.update(repr(("profile", profile, "case", case)).encode("ascii"))
    digest.update(b"\nTERMS\n")
    digest.update(repr(terms).encode("ascii"))
    digest.update(b"\nQF_COLUMNS\n")
    digest.update(repr(columns).encode("ascii"))
    digest.update(b"\nQF_ROWS\n")
    for word, row in rows:
        digest.update(repr((word, tuple(sorted(row.items())))).encode("ascii"))
        digest.update(b"\n")
    digest.update(b"VARIABLE_CELLS\n")
    digest.update(repr(cells).encode("ascii"))
    digest.update(b"\nQ2_MINUS_F\n")
    for polynomial in generators:
        digest.update(repr(tuple(polynomial.items())).encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def singular_unit_ideal(generators, variable_count, timeout):
    executable = shutil.which("Singular")
    if executable is None:
        raise SystemExit("Singular is required for the exact ideal audit")
    variables = ",".join(f"z{index}" for index in range(variable_count))
    encoded = ",".join(polynomial_string(poly) for poly in generators)
    # Use reverse variable order and degree reverse lexicographic order.
    program = (
        f"ring independent=0,({variables}),Dp;\n"
        f"ideal J={encoded};\n"
        "ideal G=slimgb(J);\n"
        'print("INDEPENDENT_BASIS_SIZE");\n'
        "print(size(G));\n"
        'print("INDEPENDENT_BASIS_FIRST");\n'
        "print(G[1]);\n"
    )
    started = time.monotonic()
    completed = subprocess.run(
        (executable, "-q"),
        input=program,
        text=True,
        capture_output=True,
        timeout=timeout,
    )
    seconds = time.monotonic() - started
    if completed.returncode != 0:
        raise AssertionError((completed.returncode, completed.stderr))
    lines = [line.strip() for line in completed.stdout.splitlines() if line.strip()]
    size = lines[lines.index("INDEPENDENT_BASIS_SIZE") + 1]
    first = lines[lines.index("INDEPENDENT_BASIS_FIRST") + 1]
    assert size == "1" and first == "1", (size, first, completed.stdout)
    return seconds


def audit_pair_orbits_and_weight_characters():
    orbit_counts = Counter()
    checked = 0
    for left, right in combinations(EDGES, 2):
        orbit_counts[
            "adjacent" if frozenset(left) & frozenset(right) else "disjoint"
        ] += 1
        # The two outside-support characters have a unimodular 2x2 minor,
        # so two coefficients of one colour can be normalized with no roots.
        outside_left = [int(site not in left) for site in SITE_ORDER]
        outside_right = [int(site not in right) for site in SITE_ORDER]
        minors = [
            outside_left[i] * outside_right[j]
            - outside_left[j] * outside_right[i]
            for i, j in combinations(range(6), 2)
        ]
        assert any(abs(minor) == 1 for minor in minors)
        checked += 1
    assert orbit_counts == Counter({"adjacent": 60, "disjoint": 45})
    assert checked == 105
    return orbit_counts


def build_and_run(profile, case, timeout, build_only=False):
    pairs = CASES[case]
    terms = profile_terms(profile, pairs)
    columns, rows = audit_qf_full_active_block_rank(terms, pairs)
    cells, generators = matching_polynomials(terms, pairs)
    digest = ledger_digest(
        profile, case, terms, columns, rows, cells, generators
    )
    expected_rows, expected_digest = EXPECTED[profile, case]
    assert len(rows) == expected_rows
    assert digest == expected_digest
    seconds = None
    if not build_only:
        seconds = singular_unit_ideal(generators, len(cells), timeout)
    return {
        "profile": profile,
        "case": case,
        "terms": len(terms),
        "qf_rows": len(rows),
        "qf_rank": 18,
        "variables": len(cells),
        "generators": len(generators),
        "sha256": digest,
        "seconds": seconds,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", choices=("211", "221", "222"),
                        action="append")
    parser.add_argument("--case", choices=tuple(CASES), action="append")
    parser.add_argument("--timeout", type=int, default=1200)
    parser.add_argument("--build-only", action="store_true")
    args = parser.parse_args()

    print("universal two-pair profile census:",
          dict(sorted(audit_universal_two_pair_reduction().items())))
    print("pair orbit census:",
          dict(sorted(audit_pair_orbits_and_weight_characters().items())))
    profiles = args.profile or ["211", "221", "222"]
    cases = args.case or list(CASES)
    for profile in profiles:
        for case in cases:
            result = build_and_run(
                profile, case, args.timeout, args.build_only
            )
            status = "BUILT" if args.build_only else "UNIT"
            timing = (
                "" if result["seconds"] is None
                else f' seconds {result["seconds"]:.3f}'
            )
            print(
                "profile", profile, case,
                "terms", result["terms"],
                "qF rows/rank", f'{result["qf_rows"]}/{result["qf_rank"]}',
                "variables", result["variables"],
                "generators", result["generators"],
                "sha256", result["sha256"],
                status + timing,
                flush=True,
            )
    print("independent two-pair common-power profile audit: PASS")


if __name__ == "__main__":
    main()
