#!/usr/bin/env python3
"""Exact audit of the first two-monomial common-power obstruction.

The four missing pairs are (A,B,C,D), with A and B carrying colour zero
and C,D carrying colours one and two.  All target coefficients are normalized
to one.  The linear equation qF=0 is solved explicitly: q_C=q_D=0, while
q_A and q_B are opposite tensors in the intersection of their two full-word
response spaces.  The script sends the remaining exact equations q^[2]=F to
Singular over QQ.  It independently enumerates the 16,380 labelled support
assignments and verifies that the displayed 25 representatives exhaust their
orbits under site permutations, interchange of A,B, and interchange of C,D.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from fractions import Fraction
from itertools import combinations, permutations, product
import hashlib
import subprocess
import shutil
import time


U = tuple(range(6))
COLOURS = tuple(range(3))
EDGES = tuple(combinations(U, 2))
EDGE_INDEX = {pair: index for index, pair in enumerate(EDGES)}
N_Q_CELL = len(EDGES) * len(COLOURS) ** 2

REPRESENTATIVES = (
    ((0, 1), (0, 2), (0, 3), (0, 4)),
    ((0, 1), (0, 2), (0, 3), (1, 2)),
    ((0, 1), (0, 2), (0, 3), (1, 3)),
    ((0, 1), (0, 2), (0, 3), (1, 4)),
    ((0, 1), (0, 2), (0, 3), (3, 4)),
    ((0, 1), (0, 2), (0, 3), (4, 5)),
    ((0, 1), (0, 2), (1, 2), (1, 3)),
    ((0, 1), (0, 2), (1, 2), (3, 4)),
    ((0, 1), (0, 2), (1, 3), (1, 4)),
    ((0, 1), (0, 2), (1, 3), (2, 3)),
    ((0, 1), (0, 2), (1, 3), (2, 4)),
    ((0, 1), (0, 2), (1, 3), (3, 4)),
    ((0, 1), (0, 2), (1, 3), (4, 5)),
    ((0, 1), (0, 2), (3, 4), (3, 5)),
    ((0, 1), (2, 3), (0, 2), (0, 3)),
    ((0, 1), (2, 3), (0, 2), (0, 4)),
    ((0, 1), (2, 3), (0, 2), (1, 3)),
    ((0, 1), (2, 3), (0, 2), (1, 4)),
    ((0, 1), (2, 3), (0, 2), (4, 5)),
    ((0, 1), (2, 3), (0, 4), (0, 5)),
    ((0, 1), (2, 3), (0, 4), (1, 4)),
    ((0, 1), (2, 3), (0, 4), (1, 5)),
    ((0, 1), (2, 3), (0, 4), (2, 4)),
    ((0, 1), (2, 3), (0, 4), (2, 5)),
    ((0, 1), (2, 3), (0, 4), (4, 5)),
)

EXPECTED_ORBIT_COUNTS = (
    360, 360, 720, 1440, 720,
    360, 720, 360, 720, 360,
    720, 1440, 720, 360, 360,
    1440, 180, 1440, 360, 360,
    360, 360, 720, 720, 720,
)

EXPECTED_ORBIT_LEDGER_SHA256 = (
    "32415c6354cbfeb6626f2a3692e90c935ce8ebc4a3a3cd5e913e2c110658e7a5"
)

EXPECTED_GENERATOR_SHA256 = (
    "6502f608d2664a32136d3c4c01682c797187d14fa65cdbbe7cb1176389f0d858",
    "4f9e9ab82a7fe05cb94537a9b88ac0390f306dfb693e5d4d03372c04d0474c55",
    "54d24699d5309d81a05cc5878343f8d90d104492298c9d46644374c614e4c158",
    "d0c6046311c1cb69ec9290f7c8df29136556d5762450cd0f04e28d595c1d7e84",
    "1b345c2efc2d6565c08458b740377d7a4578d7de83124b710bb7a7a6b15954cb",
    "82bf62e0ba49f3a75f1ec07951e03145197788cb09de77f19e03f399ffc87a44",
    "7274d0f9af964552bbac79ad10fa5bb27b34f29d3209358305e27ec3b1b1e286",
    "5955ca8153ebd7a97f7bf24008735e1658b10315df1f21d81c916cae1a03cc6c",
    "7b7e67fe78d66199596a06371772cfefd5dd66f81abed3f0448c00f5d8380b98",
    "fd84b95d95bed2fc11571e4d534a19b152bac67582f6b9bec3e0bdc636c90768",
    "012995d6fdf428a6c42e44e18b06687d5c2fd271c628af58bd55fdb59951c274",
    "120340691c0c00990125f2d9628f4072438cb82f9d983830d40a058bed076a54",
    "16ac7fe82579f509bb325e8809edeffb303bfd0852b66a4a4d52fb466ad027eb",
    "409fad27550370f37a60d579b1a08f262d20aea93a2d1121c14582562faf2b50",
    "463fa62a1170c51be42afe24d5dceb603da45ba3b19694247e1c037d52959511",
    "4be0d545dde3cc8cef4d4657671ff34f5e7326b095190b631a7f14dbf5ef1bd9",
    "abae83317c0274f9e46f291be054fd3298fabcd31cf38669fca9aedae9cf466f",
    "a7bea7966c32ca1ba455b2d4fa71834d197876c1095a45fbd30d46190e5a4bd7",
    "58c35453afc9f276c78a8ac9b168cbf4bc227aa48a54990b1f86947e93309e6b",
    "320932f809dc29b497bd0b94434615a741333aff26675802a2f35d781fc66178",
    "3d82c3e28397e724b671686dd31ad899219466bfaeabcbd695c902bf17fc778e",
    "2049ec19e6a4cab19cc2c400da53ae9925cefe4f0e62eabbcb35dd0c464a1802",
    "758a3955715cfdbe31baa448745266c5bb4041e98324f31c689eea75fae15fd0",
    "6f2f257d9f78541ac93693f00a76d5fc995152ed4a72f7215ee50967faab2e02",
    "6de33702af8743f684bdd4c9c95f72cf466bfa47acf3b4d117448cddfd6a3c7d",
)

EXPECTED_GENERATOR_LEDGER_SHA256 = (
    "5dee107cd6f6d278c54b796b8e3a70025a8916a057e5a448e051f34cf0904a11"
)


def audit_expected_generator_ledger():
    digest = hashlib.sha256()
    for orbit, (support, generator_digest) in enumerate(
        zip(REPRESENTATIVES, EXPECTED_GENERATOR_SHA256), 1
    ):
        digest.update(f"{orbit}:{support}:{generator_digest}\n".encode("ascii"))
    assert digest.hexdigest() == EXPECTED_GENERATOR_LEDGER_SHA256
    return digest.hexdigest()


def edge(u: int, v: int) -> tuple[int, int]:
    return (u, v) if u < v else (v, u)


def normalized_support(a, b, c, d):
    a, b = sorted((a, b))
    return a, b, c, d


def support_orbit(representative):
    """Orbit under S6, A<->B, and the symmetric colour swap 1<->2."""
    output = set()
    for permutation in permutations(U):
        image = tuple(edge(permutation[u], permutation[v]) for u, v in representative)
        a, b, c, d = image
        output.add(normalized_support(a, b, c, d))
        output.add(normalized_support(a, b, d, c))
    return output


def audit_support_orbits():
    all_supports = {
        normalized_support(a, b, c, d)
        for a, b in combinations(EDGES, 2)
        for c, d in permutations(tuple(e for e in EDGES if e not in (a, b)), 2)
    }
    assert len(all_supports) == 16380

    seen = set()
    counts = []
    for representative in REPRESENTATIVES:
        orbit = support_orbit(representative)
        assert representative == normalized_support(*representative)
        assert representative in orbit
        assert not (seen & orbit)
        assert orbit <= all_supports
        seen |= orbit
        counts.append(len(orbit))
    assert seen == all_supports
    assert tuple(counts) == EXPECTED_ORBIT_COUNTS
    digest = hashlib.sha256()
    for representative, count in zip(REPRESENTATIVES, counts):
        digest.update(f"{representative}:{count}\n".encode("ascii"))
    assert digest.hexdigest() == EXPECTED_ORBIT_LEDGER_SHA256
    return tuple(counts), digest.hexdigest()


def add(left: str, right: str) -> str:
    if left == "0":
        return right
    if right == "0":
        return left
    return f"({left})+({right})"


def multiply(left: str, right: str) -> str:
    if left == "0" or right == "0":
        return "0"
    if left == "1":
        return right
    if right == "1":
        return left
    if left == "-1":
        return f"-({right})"
    if right == "-1":
        return f"-({left})"
    return f"({left})*({right})"


def q_index(pair, cu, cv):
    return 9 * EDGE_INDEX[pair] + 3 * cu + cv


def sparse_rank(rows):
    pivots = {}
    for source in rows:
        row = {column: Fraction(value) for column, value in source.items() if value}
        while row:
            column = min(row)
            if column not in pivots:
                scale = row[column]
                row = {key: value / scale for key, value in row.items()}
                pivots[column] = row
                break
            scale = row[column]
            pivot = pivots[column]
            for key, value in pivot.items():
                row[key] = row.get(key, Fraction(0)) - scale * value
                if row[key] == 0:
                    del row[key]
    return len(pivots)


def qf_rows(support):
    """Coefficient matrix of qF after all four target weights are one."""
    rows = {}
    for pair, colour in zip(support, (0, 0, 1, 2)):
        u, v = pair
        for cu, cv in product(COLOURS, repeat=2):
            word = [colour] * len(U)
            word[u], word[v] = cu, cv
            row = rows.setdefault(tuple(word), {})
            index = q_index(pair, cu, cv)
            row[index] = row.get(index, 0) + 1
    return tuple(rows.values())


def parameter_vectors(support):
    variables, values = parameterization(support)
    columns = {variable: {} for variable in variables}
    for pair in EDGES:
        for cu, cv in product(COLOURS, repeat=2):
            expression = values[pair, cu, cv]
            if expression == "0":
                continue
            sign = -1 if expression.startswith("-(") else 1
            variable = expression[2:-1] if sign == -1 else expression
            columns[variable][q_index(pair, cu, cv)] = sign
    return variables, tuple(columns[variable] for variable in variables)


def audit_qf_kernel(support):
    rows = qf_rows(support)
    variables, basis = parameter_vectors(support)
    rank = sparse_rank(rows)
    assert rank + len(variables) == N_Q_CELL
    assert sparse_rank(basis) == len(basis)
    for vector in basis:
        for row in rows:
            assert sum(
                Fraction(value) * vector.get(column, 0)
                for column, value in row.items()
            ) == 0
    return rank, len(variables)


def parameterization(support):
    a, b, c, d = support
    values = {}
    variables = []

    # The two distinct other-colour summands are linearly independent in qF.
    for special in (c, d):
        for cu, cv in product(COLOURS, repeat=2):
            values[special, cu, cv] = "0"

    common = set(a) & set(b)
    if not common:
        variables.append("z")
        for pair, sign in ((a, "1"), (b, "-1")):
            for cu, cv in product(COLOURS, repeat=2):
                values[pair, cu, cv] = multiply(sign, "z") if cu == cv == 0 else "0"
    else:
        shared = next(iter(common))
        variables.extend(f"z{colour}" for colour in COLOURS)
        for pair, sign in ((a, "1"), (b, "-1")):
            unique = next(iter(set(pair) - {shared}))
            for cu, cv in product(COLOURS, repeat=2):
                local = {pair[0]: cu, pair[1]: cv}
                if local[unique] == 0:
                    values[pair, cu, cv] = multiply(sign, f"z{local[shared]}")
                else:
                    values[pair, cu, cv] = "0"

    for u, v in EDGES:
        pair = (u, v)
        if pair in support:
            continue
        for cu, cv in product(COLOURS, repeat=2):
            name = f"q{u}{v}{cu}{cv}"
            variables.append(name)
            values[pair, cu, cv] = name
    return tuple(variables), values


def cell(values, u, v, cu, cv):
    if u < v:
        return values[(u, v), cu, cv]
    return values[(v, u), cv, cu]


def equations(support):
    variables, values = parameterization(support)
    target = {}
    for pair, colour in zip(support, (0, 0, 1, 2)):
        sites = tuple(u for u in U if u not in pair)
        target[sites, (colour,) * 4] = 1

    matchings = ((0, 1, 2, 3), (0, 2, 1, 3), (0, 3, 1, 2))
    output = []
    labels = []
    for sites in combinations(U, 4):
        for colours in product(COLOURS, repeat=4):
            polynomial = "0"
            for i, j, k, l in matchings:
                polynomial = add(
                    polynomial,
                    multiply(
                        cell(values, sites[i], sites[j], colours[i], colours[j]),
                        cell(values, sites[k], sites[l], colours[k], colours[l]),
                    ),
                )
            if target.get((sites, colours), 0):
                polynomial = add(polynomial, "-1")
            if polynomial != "0":
                output.append(polynomial)
                labels.append((sites, colours))
    return variables, tuple(output), tuple(labels)


def ledger_digest(generators):
    digest = hashlib.sha256()
    for generator in generators:
        digest.update(generator.encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def run(orbit: int, timeout: int, certificate: bool):
    support = REPRESENTATIVES[orbit - 1]
    variables, generators, labels = equations(support)
    digest = ledger_digest(generators)
    assert digest == EXPECTED_GENERATOR_SHA256[orbit - 1], (orbit, digest)
    certificate_program = ""
    if certificate:
        certificate_program = (
            "matrix L=lift(I,G);\n"
            'print("LIFT_NONZERO");\n'
            "int row; for (row=1; row<=nrows(L); row++) { "
            'if (L[row,1] != 0) { print(string(row)+":"+string(L[row,1])); } };\n'
        )
    program = (
        f"ring r=0,({','.join(variables)}),dp;\n"
        f"ideal I={','.join(generators)};\n"
        "ideal G=slimgb(I);\n"
        'print("BASIS_SIZE"); print(size(G));\n'
        'print("BASIS_FIRST"); print(G[1]);\n'
        + certificate_program
    )
    executable = shutil.which("Singular")
    if executable is None:
        raise SystemExit("Singular is required")
    started = time.monotonic()
    result = subprocess.run(
        (executable, "-q"), input=program, text=True, capture_output=True,
        check=True, timeout=timeout,
    )
    elapsed = time.monotonic() - started
    if result.stderr.strip():
        raise AssertionError(f"orbit {orbit}: Singular stderr:\n{result.stderr}")
    lines = tuple(line.strip() for line in result.stdout.splitlines() if line.strip())
    try:
        basis_size = lines[lines.index("BASIS_SIZE") + 1]
        basis_first = lines[lines.index("BASIS_FIRST") + 1]
    except (ValueError, IndexError) as error:
        raise AssertionError(
            f"orbit {orbit}: malformed Singular output:\n{result.stdout}"
        ) from error
    assert basis_size == basis_first == "1", (orbit, result.stdout)

    certificate_lines = []
    if certificate and "LIFT_NONZERO" in result.stdout:
        tail = result.stdout.split("LIFT_NONZERO", 1)[1]
        indices = []
        for line in tail.splitlines():
            if ":" in line and line.split(":", 1)[0].strip().isdigit():
                indices.append(int(line.split(":", 1)[0].strip()))
        for index in indices:
            certificate_lines.append((index, labels[index - 1], generators[index - 1]))
    return (
        orbit, support, len(variables), len(generators), digest, elapsed,
        tuple(certificate_lines), result.stdout.strip(),
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--orbit", type=int, action="append")
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument("--certificate", action="store_true")
    parser.add_argument("--skip-ideals", action="store_true")
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()

    counts, orbit_digest = audit_support_orbits()
    generator_ledger_digest = audit_expected_generator_ledger()
    kernel_dimensions = tuple(audit_qf_kernel(support) for support in REPRESENTATIVES)
    print("labelled four-distinct-pair supports:", sum(counts))
    print("support orbits:", len(counts))
    print("orbit sizes:", counts)
    print("orbit-ledger sha256:", orbit_digest)
    print("generator-ledger sha256:", generator_ledger_digest)
    print("qF ranks/kernel dimensions:", kernel_dimensions)

    selected = args.orbit or list(range(1, len(REPRESENTATIVES) + 1))
    if any(orbit < 1 or orbit > len(REPRESENTATIVES) for orbit in selected):
        raise SystemExit(f"--orbit must lie in 1..{len(REPRESENTATIVES)}")
    if args.skip_ideals:
        print("QQ ideals skipped by request")
        return

    outputs = []
    wall_started = time.monotonic()
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {
            pool.submit(run, orbit, args.timeout, args.certificate): orbit
            for orbit in selected
        }
        for future in as_completed(futures):
            outputs.append(future.result())
    for output in sorted(outputs):
        orbit, support, variable_count, generator_count, digest, elapsed, core, raw = output
        print(
            "orbit", orbit, "support", support, "QQ ideal [1]",
            "variables", variable_count, "equations", generator_count,
            "sha256", digest, "seconds", f"{elapsed:.3f}",
        )
        if args.certificate:
            print(raw)
            print("LIFT_GENERATORS")
            for index, label, generator in core:
                print(index, label, generator)
    print("parallel wall seconds:", f"{time.monotonic() - wall_started:.3f}")
    print("one-multiterm common-power obstruction exact audit: PASS")


if __name__ == "__main__":
    main()
