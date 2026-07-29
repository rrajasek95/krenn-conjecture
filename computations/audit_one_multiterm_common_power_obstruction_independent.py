#!/usr/bin/env python3
"""Independent exact audit of the first one-multiterm common-power theorem.

This program deliberately does not import the primary verifier.  It

* reconstructs the literal-product collision argument;
* enumerates all 16,380 four-distinct-pair supports and their S_6 orbits;
* checks the complete 135-column linear kernel of qF=0;
* writes every coefficient of q^[2]-F in an independently chosen order; and
* asks Singular over QQ whether each resulting unsaturated affine ideal is
  the unit ideal.

The first two missing pairs carry colour 0 and are unordered.  The third and
fourth carry colours 1 and 2; swapping them is included in the orbit group.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from fractions import Fraction
import hashlib
from itertools import combinations, permutations, product
import shutil
import subprocess
import time


VERTICES = tuple(range(6))
COLOURS = (0, 1, 2)
ENUM_COLOURS = (2, 0, 1)
PAIRS = tuple(combinations(VERTICES, 2))
PAIR_INDEX = {pair: index for index, pair in enumerate(PAIRS)}
CELL_COUNT = len(PAIRS) * 9

# Filled only after a first clean-room run.  Keeping the data here makes a
# later replay detect changes in support ordering or polynomial generation.
EXPECTED_ORBIT_LEDGER_SHA256 = (
    "b1c5d4bade10cede0c2616f9a64891610b637417d4bda5a606a5152e5eeb4965"
)
EXPECTED_IDEAL_LEDGER_SHA256 = (
    "10b8a308e580332722b54a6fdab9a3220810fec64135427af0b94da76a1ab4f9"
)
EXPECTED_IDEAL_SHA256 = (
    "ed2c3b9885bf733a444003d00a79d47e6c8e78846ea02ce6b1c7abc0725d26e4",
    "d2d80b7210ef530ea21e988f6dabde898bb6395694708768e4ddae0d89911302",
    "069c7d04b4c02d48c8081bd061abc0b0bf24dd43ff364c498138e06b6d0e372e",
    "cdf9009f7a8738b1a1c294ee87c66c579206db74fd0695d1d686cf3020b15f4f",
    "4039323fa3006f8e6d478bde1e28d4a651febd401c6e79490afae1956d19cd4f",
    "553cd60a368974d5f74fb2f87d0eb5879237b0cfbdd7fc75090645186610bd61",
    "6825a655da90b8a88d436d4d315c4b5d4df23b528cf69314bf60f9456f99c449",
    "beb5f39cf2561fa9cdf5cffcf68a22b9ca8f2c2d34897602d06d38ec561df592",
    "e87ba2081ab9d413faf33afecbb3bc7655c5160c91ec04b7a691540ece0ec2cd",
    "6b9e8c4543bcc5e6fa7893933efa32aafea05c1d25f6999bd925202c677846d9",
    "455e5b8238f72c92466a15d715fe255dd8c16deb8073a72b7e1ad8d9779bd3b1",
    "531dfe8c34d64ba1f596ff96f23305666741026564f70b3bbb3df74ce0e07fce",
    "aa739d30a9e0a00c856c6d4bddb8d03b92e264ebf5282a5d125d3ae1ce277529",
    "dce315d5d155c2d7c6526e5259243d43a7ab76f8758398cc9a719502e244f85f",
    "d52d604c91e72ebfbb23ba363da13e7f4fc442c6f53343f4d68f2bc1a83da0d2",
    "4633659a7e7e09011aec7131f5cbf6c7c2cf85ec935207fe6e1e2132e3aa64ae",
    "34b0788e29774837c19b2a3baf62d34e4af5e2cc43ac49df2c7d3d68e56cdbbb",
    "f1712ad531a2ba973f0e44445b791c1b34259d7ae241287a0f13ed1b57a02955",
    "0ebca208567537374f5edbcde869f8c2a6e86d88d22bb591ee08e97f9c4f21cc",
    "96d6950b1da9f3ef1b8831c6acbcea386ded3fa21a20af9f1def6a53ecbe8870",
    "ac0645122e21c42b21a50f9476f62034e551f5083a01f821e3444288ab6c1abb",
    "59482eb20e65a8e3bc4f5af13bd6448dfa699d43512cf2518fca39cf3dfc3950",
    "9360790ec3e659c761d1578d1ea77d92f1d0efda2112d4023179bd6775c207be",
    "818cc5983194534d168caf96cedde216c82bfb81ad23130d40c82045eeac68e8",
    "3c27dc166b7b6883c6c9c02e25dff66fb9e78c8735146b5fed5545335be99699",
)


def edge(u: int, v: int) -> tuple[int, int]:
    return (u, v) if u < v else (v, u)


def normalize_support(a, b, c, d):
    """A,B are unordered; C,D remain colour-labelled."""
    return (*sorted((a, b)), c, d)


def all_four_distinct_supports():
    return {
        normalize_support(a, b, c, d)
        for a, b in combinations(PAIRS, 2)
        for c, d in permutations(tuple(p for p in PAIRS if p not in (a, b)), 2)
    }


def orbit(seed):
    images = set()
    for sigma in permutations(VERTICES):
        transformed = tuple(edge(sigma[u], sigma[v]) for u, v in seed)
        a, b, c, d = transformed
        images.add(normalize_support(a, b, c, d))
        images.add(normalize_support(a, b, d, c))
    return images


def support_orbits():
    universe = all_four_distinct_supports()
    assert len(universe) == 16_380
    unseen = set(universe)
    records = []
    while unseen:
        seed = min(unseen)
        members = orbit(seed)
        assert members <= universe
        assert seed in members
        records.append((max(members), len(members)))
        unseen.difference_update(members)
    # Reverse lexicographic order and lexicographically maximal representatives
    # are intentionally different from the primary verifier's choices.
    records.sort(reverse=True)
    representatives = tuple(rep for rep, _ in records)
    counts = tuple(count for _, count in records)
    assert len(records) == 25
    assert sum(counts) == 16_380
    assert sorted(counts) == (
        [180]
        + [360] * 11
        + [720] * 9
        + [1440] * 4
    )
    digest = hashlib.sha256()
    for number, (representative, count) in enumerate(records, 1):
        digest.update(f"{number}|{representative}|{count}\n".encode("ascii"))
    value = digest.hexdigest()
    if EXPECTED_ORBIT_LEDGER_SHA256:
        assert value == EXPECTED_ORBIT_LEDGER_SHA256
    return representatives, counts, value


def response_word(pair, colour):
    return tuple(colour if u in pair else 0 for u in VERTICES)


def lies_in_colour_zero_response(word, pair):
    return all(word[u] == 0 for u in VERTICES if u not in pair)


def audit_literal_product_collisions():
    """Audit the direct contradictions when the four pairs are not distinct.

    A and B are distinct by the two-term hypothesis.  For row (1,1), C=D
    makes the same endpoint tensor both e1 tensor e1 and zero.  If C=A or B,
    its e1 endpoint word has a nonzero coefficient that cannot lie in the
    other colour-zero response space.  Row (2,2) gives the analogous D test.
    """
    counts = {"C=D": 0, "C in {A,B}": 0, "D in {A,B}": 0, "distinct": 0}
    for a, b in combinations(PAIRS, 2):
        for c in PAIRS:
            for d in PAIRS:
                if c == d:
                    counts["C=D"] += 1
                elif c in (a, b):
                    other = b if c == a else a
                    assert not lies_in_colour_zero_response(response_word(c, 1), other)
                    counts["C in {A,B}"] += 1
                elif d in (a, b):
                    other = b if d == a else a
                    assert not lies_in_colour_zero_response(response_word(d, 2), other)
                    counts["D in {A,B}"] += 1
                else:
                    assert len({a, b, c, d}) == 4
                    counts["distinct"] += 1
    assert counts == {
        "C=D": 1575,
        "C in {A,B}": 2940,
        "D in {A,B}": 2730,
        "distinct": 16_380,
    }
    assert sum(counts.values()) == 23_625
    return counts


def audit_weight_normalization():
    """Check the root-free exponent recipes for all possible pair positions."""
    # Exponent dictionaries stand for arbitrary nonzero symbols alpha and beta.
    for a, b in combinations(PAIRS, 2):
        exponents = [[0, 0] for _ in VERTICES]
        if set(a) & set(b):
            shared = next(iter(set(a) & set(b)))
            ua = next(iter(set(a) - {shared}))
            ub = next(iter(set(b) - {shared}))
        else:
            ua, ub = a[0], b[0]
        exponents[ua][0] += 1
        exponents[ub][1] += 1
        correction = next(u for u in VERTICES if u not in set(a) | set(b))
        exponents[correction][0] -= 1
        exponents[correction][1] -= 1
        assert [sum(exponents[u][j] for u in VERTICES) for j in range(2)] == [0, 0]
        assert [sum(exponents[u][j] for u in a) for j in range(2)] == [1, 0]
        assert [sum(exponents[u][j] for u in b) for j in range(2)] == [0, 1]

    # A single same-colour summand needs pair product gamma and total product 1.
    for pair in PAIRS:
        exponents = [0] * 6
        exponents[pair[0]] = 1
        exponents[next(u for u in VERTICES if u not in pair)] = -1
        assert sum(exponents) == 0
        assert sum(exponents[u] for u in pair) == 1


def cell_index(pair, left_colour, right_colour):
    return 9 * PAIR_INDEX[pair] + 3 * left_colour + right_colour


def qf_matrix(support):
    rows = {}
    for pair, target_colour in zip(support, (0, 0, 1, 2)):
        u, v = pair
        for cu, cv in product(COLOURS, repeat=2):
            word = [target_colour] * 6
            word[u], word[v] = cu, cv
            row = rows.setdefault(tuple(word), {})
            column = cell_index(pair, cu, cv)
            row[column] = row.get(column, 0) + 1
    return tuple(rows.values())


def sparse_rank(rows):
    pivots = {}
    for source in rows:
        row = {k: Fraction(v) for k, v in source.items() if v}
        while row:
            pivot_column = max(row)
            if pivot_column not in pivots:
                scale = row[pivot_column]
                pivots[pivot_column] = {k: v / scale for k, v in row.items()}
                break
            scale = row[pivot_column]
            for k, v in pivots[pivot_column].items():
                row[k] = row.get(k, Fraction(0)) - scale * v
                if not row[k]:
                    del row[k]
    return len(pivots)


def independent_parameterization(support):
    """Solve qF=0 in an order unrelated to the primary generator stream."""
    a, b, c, d = support
    expressions = {}
    variable_names = []

    # Blocks for the transverse-colour summands vanish.
    for pair in (d, c):
        for ca, cb in product(ENUM_COLOURS, repeat=2):
            expressions[pair, ca, cb] = None

    shared = set(a) & set(b)
    if shared:
        x = next(iter(shared))
        kernel_names = tuple(f"h{colour}" for colour in (2, 1, 0))
        for pair, sign in ((b, -1), (a, 1)):
            unique = next(iter(set(pair) - {x}))
            for ca, cb in product(ENUM_COLOURS, repeat=2):
                local = {pair[0]: ca, pair[1]: cb}
                if local[unique] == 0:
                    expressions[pair, ca, cb] = (sign, f"h{local[x]}")
                else:
                    expressions[pair, ca, cb] = None
    else:
        kernel_names = ("h",)
        for pair, sign in ((b, -1), (a, 1)):
            for ca, cb in product(ENUM_COLOURS, repeat=2):
                expressions[pair, ca, cb] = (sign, "h") if ca == cb == 0 else None

    # Put free variables first, traverse edges and colours backwards, and put
    # the kernel parameters last.  This differs from the primary ring order.
    for pair in reversed(PAIRS):
        if pair in support:
            continue
        for ca, cb in product(ENUM_COLOURS, repeat=2):
            name = f"x{pair[0]}{pair[1]}{ca}{cb}"
            variable_names.append(name)
            expressions[pair, ca, cb] = (1, name)
    variable_names.extend(kernel_names)
    assert len(variable_names) == (102 if shared else 100)
    return tuple(variable_names), expressions


def oriented_expression(expressions, u, v, cu, cv):
    if u < v:
        return expressions[(u, v), cu, cv]
    return expressions[(v, u), cv, cu]


def parameter_basis(support):
    variable_names, expressions = independent_parameterization(support)
    columns = {name: {} for name in variable_names}
    for pair in PAIRS:
        for ca, cb in product(COLOURS, repeat=2):
            expression = expressions[pair, ca, cb]
            if expression is not None:
                coefficient, name = expression
                columns[name][cell_index(pair, ca, cb)] = coefficient
    return variable_names, tuple(columns[name] for name in variable_names)


def audit_qf_kernel(support):
    rows = qf_matrix(support)
    names, basis = parameter_basis(support)
    rank = sparse_rank(rows)
    assert rank + len(names) == CELL_COUNT
    assert sparse_rank(basis) == len(basis)
    for vector in basis:
        for row in rows:
            assert sum(value * vector.get(column, 0) for column, value in row.items()) == 0
    expected = (33, 102) if set(support[0]) & set(support[1]) else (35, 100)
    assert (rank, len(names)) == expected
    return expected


def add_term(polynomial, coefficient, variables=()):
    if not coefficient:
        return
    monomial = tuple(sorted(variables, reverse=True))
    polynomial[monomial] = polynomial.get(monomial, 0) + coefficient
    if not polynomial[monomial]:
        del polynomial[monomial]


def add_product(polynomial, left, right):
    if left is None or right is None:
        return
    left_coefficient, left_variable = left
    right_coefficient, right_variable = right
    add_term(
        polynomial,
        left_coefficient * right_coefficient,
        (right_variable, left_variable),
    )


def polynomial_string(polynomial, variable_position):
    def monomial_key(item):
        monomial, coefficient = item
        return (
            len(monomial),
            tuple(variable_position[name] for name in monomial),
            coefficient,
        )

    pieces = []
    for monomial, coefficient in sorted(polynomial.items(), key=monomial_key, reverse=True):
        powers = []
        for name in dict.fromkeys(monomial):
            exponent = monomial.count(name)
            powers.append(name if exponent == 1 else f"{name}^{exponent}")
        body = "*".join(powers) if powers else "1"
        magnitude = abs(coefficient)
        if magnitude != 1 or not powers:
            body = str(magnitude) if not powers else f"{magnitude}*{body}"
        if not pieces:
            pieces.append(body if coefficient > 0 else f"-{body}")
        else:
            pieces.append(("+" if coefficient > 0 else "-") + body)
    assert pieces
    return "".join(pieces)


def ideal_generators(support):
    variables, expressions = independent_parameterization(support)
    variable_position = {name: index for index, name in enumerate(variables)}
    target = {}
    for pair, colour in zip(support, (0, 0, 1, 2)):
        sites = tuple(u for u in VERTICES if u not in pair)
        target[sites, (colour,) * 4] = target.get((sites, (colour,) * 4), 0) + 1

    labels_and_generators = []
    matchings = ((0, 3, 1, 2), (0, 2, 3, 1), (2, 3, 0, 1))
    # Reversed site order and nonstandard colour order are deliberate.
    for sites in reversed(tuple(combinations(VERTICES, 4))):
        for colours in product(ENUM_COLOURS, repeat=4):
            polynomial = {}
            for i, j, k, l in matchings:
                add_product(
                    polynomial,
                    oriented_expression(
                        expressions, sites[i], sites[j], colours[i], colours[j]
                    ),
                    oriented_expression(
                        expressions, sites[k], sites[l], colours[k], colours[l]
                    ),
                )
            wanted = target.get((sites, colours), 0)
            add_term(polynomial, -wanted)
            if polynomial:
                labels_and_generators.append(
                    ((sites, colours), polynomial_string(polynomial, variable_position))
                )
    # Reverse again after filtering, so zero-generator positions cannot mimic
    # the primary stream even accidentally.
    labels_and_generators.reverse()
    labels = tuple(label for label, _ in labels_and_generators)
    generators = tuple(generator for _, generator in labels_and_generators)
    return variables, generators, labels


def generator_digest(generators):
    digest = hashlib.sha256()
    for index, generator in enumerate(generators, 1):
        digest.update(f"{index}:{generator}\n".encode("ascii"))
    return digest.hexdigest()


def run_ideal(number, support, expected_digest, singular, timeout):
    variables, generators, _ = ideal_generators(support)
    digest = generator_digest(generators)
    if expected_digest:
        assert digest == expected_digest, (number, digest)
    program = (
        f"ring R=0,({','.join(variables)}),dp;\n"
        f"ideal J={','.join(generators)};\n"
        "option(redSB); ideal H=slimgb(J);\n"
        'print("AUDIT_SIZE"); print(size(H));\n'
        'print("AUDIT_FIRST"); print(H[1]);\n'
    )
    started = time.monotonic()
    result = subprocess.run(
        (singular, "-q"),
        input=program,
        text=True,
        capture_output=True,
        check=True,
        timeout=timeout,
    )
    elapsed = time.monotonic() - started
    if result.stderr.strip():
        raise AssertionError(f"orbit {number}: Singular stderr:\n{result.stderr}")
    lines = tuple(line.strip() for line in result.stdout.splitlines() if line.strip())
    try:
        size = lines[lines.index("AUDIT_SIZE") + 1]
        first = lines[lines.index("AUDIT_FIRST") + 1]
    except (ValueError, IndexError) as error:
        raise AssertionError(f"orbit {number}: malformed output:\n{result.stdout}") from error
    assert size == first == "1", (number, result.stdout)
    return number, support, len(variables), len(generators), digest, elapsed


def ideal_ledger_digest(outputs):
    digest = hashlib.sha256()
    for number, support, variables, generators, generator_hash, _ in sorted(outputs):
        digest.update(
            f"{number}|{support}|{variables}|{generators}|{generator_hash}\n".encode("ascii")
        )
    return digest.hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--orbit", type=int, action="append")
    parser.add_argument("--skip-ideals", action="store_true")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--timeout", type=int, default=1200)
    args = parser.parse_args()

    collisions = audit_literal_product_collisions()
    audit_weight_normalization()
    representatives, counts, orbit_hash = support_orbits()
    kernels = tuple(audit_qf_kernel(support) for support in representatives)
    generated = tuple(generator_digest(ideal_generators(support)[1]) for support in representatives)
    if EXPECTED_IDEAL_SHA256:
        assert generated == EXPECTED_IDEAL_SHA256

    print("literal-product support census:", collisions)
    print("target-preserving weight normalization: PASS")
    print("four-distinct labelled supports:", sum(counts))
    print("independent support orbits:", len(representatives))
    print("orbit representatives/sizes:")
    for number, (support, count, kernel) in enumerate(zip(representatives, counts, kernels), 1):
        print(number, support, count, "qF rank/kernel", kernel)
    print("orbit-ledger sha256:", orbit_hash)

    selected = args.orbit or list(range(1, len(representatives) + 1))
    if any(number < 1 or number > len(representatives) for number in selected):
        raise SystemExit("--orbit must be between 1 and 25")
    if args.skip_ideals:
        print("ideal generation sha256:", generated)
        print("QQ ideals skipped by request")
        return

    singular = shutil.which("Singular")
    if singular is None:
        raise SystemExit("Singular is required")
    outputs = []
    wall_started = time.monotonic()
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {
            pool.submit(
                run_ideal,
                number,
                representatives[number - 1],
                EXPECTED_IDEAL_SHA256[number - 1] if EXPECTED_IDEAL_SHA256 else "",
                singular,
                args.timeout,
            ): number
            for number in selected
        }
        for future in as_completed(futures):
            outputs.append(future.result())
    for output in sorted(outputs):
        number, support, variables, generators, digest, elapsed = output
        print(
            "orbit", number, support, "unsaturated QQ ideal [1]",
            "variables", variables, "generators", generators,
            "sha256", digest, "seconds", f"{elapsed:.3f}",
        )
    if len(selected) == 25 and len(set(selected)) == 25:
        ledger_hash = ideal_ledger_digest(outputs)
        if EXPECTED_IDEAL_LEDGER_SHA256:
            assert ledger_hash == EXPECTED_IDEAL_LEDGER_SHA256
        print("ideal-ledger sha256:", ledger_hash)
    print("parallel wall seconds:", f"{time.monotonic() - wall_started:.3f}")
    print("independent one-multiterm common-power audit: PASS")


if __name__ == "__main__":
    main()
