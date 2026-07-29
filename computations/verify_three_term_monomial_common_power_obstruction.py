#!/usr/bin/env python3
"""Exact audit for the (3,1,1) monomial common-power obstruction.

Three unordered distinct missing pairs carry colour zero and two further
ordered distinct pairs carry colours one and two.  All weights are normalized
to one.  The full linear kernel of qF=0 is parameterized explicitly, and every
coefficient of q^[2]-F is sent to Singular over QQ.

The orbit ledger, every ordered generator ledger, the exact qF kernels, and
the five weight-character ranks are audited before the unit-ideal replay.
"""

from __future__ import annotations

import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from fractions import Fraction
import hashlib
from itertools import combinations, permutations, product
import shutil
import subprocess
import time


U = tuple(range(6))
COLOURS = tuple(range(3))
EDGES = tuple(combinations(U, 2))
EDGE_INDEX = {pair: index for index, pair in enumerate(EDGES)}
N_Q_CELL = 15 * 9
SITE_PERMUTATIONS = tuple(permutations(U))

EXPECTED_ZERO_GRAPH_COUNTS = Counter({
    "three_star": 60,
    "triangle": 20,
    "three_path": 180,
    "two_path_plus_edge": 180,
    "three_matching": 15,
})

EXPECTED_CHARACTER_GRAM_DETERMINANTS = {
    "three_star": 10,
    "triangle": 10,
    "three_path": 12,
    "two_path_plus_edge": 20,
    "three_matching": 32,
}

EXPECTED_QF_RANK_KERNEL = {
    "three_star": (39, 96),
    "triangle": (37, 98),
    "three_path": (39, 96),
    "two_path_plus_edge": (41, 94),
    "three_matching": (43, 92),
}

EXPECTED_ORBIT_COUNTS = (
    120, 720, 720, 720, 240, 360, 1440, 720, 360, 360,
    720, 720, 720, 360, 360, 720, 720, 360, 120, 1440,
    360, 1440, 720, 1440, 1440, 720, 720, 720, 720, 1440,
    1440, 1440, 1440, 1440, 1440, 1440, 360, 720, 720, 720,
    1440, 360, 720, 720, 1440, 1440, 1440, 720, 720, 360,
    1440, 720, 720, 1440, 720, 720, 720, 1440, 720, 720,
    1440, 1440, 1440, 360, 1440, 360, 360, 720, 180, 720,
)

EXPECTED_ORBIT_LEDGER_SHA256 = (
    "bf78ec80a487610252f80a447cb7092019c15464b4729ba49af095461b7702f3"
)

EXPECTED_GENERATOR_SHA256 = (
    "c9febe5d3c9d27360adf2f371a34e185ecc045bb4abc4e59439046bf666c019e",
    "a29975b440ff4dbc7676a29777dfd08958d4e722d66a9374f1183de5c64abdc6",
    "6d6f12eda9a077034384a0343515b43f054b7157dde684954784212510a8a170",
    "6859d2f936d8a510593720043ea8ed2d8a980376bdd19d956f56e4c003d2461c",
    "83ab392941fd1d06e98328695248e74fcc96a7b3f9ccfdd6cc15f86fdcfaa15b",
    "41d7b5cd9966e4a0cdb54ce1621a61b2c5e6fe516dd1f9b876fca4b2378c8561",
    "b969b7325c0b95057cc570fa7c22f0d72381f7942f09b5304df4a24829e795d8",
    "c05c057ed5f162aeedd6659bf988ee09798183fc0b83115cf8e6e4d04af7ed62",
    "05ace0e03f83aa1a866fb2541d339d9a40935cdeefdfb131388a29f0217ca0af",
    "46681f5a1248b495686a371b5b13faf70103baa16c9d471eeee945caf94362a8",
    "8f4c4de4d9bb2ba52daeab63ceb375041e97d37cbdb01385a1578166203058f0",
    "b1877d86fa6a98982e4134742f057095067d38b3a144929d02d2120c21e8ef82",
    "09b5c967d964c1af214bc074728078d3915b19e0688cbb881ba8ecefec59e98f",
    "1555d3c7e5a4282b22a3e3d65fa471b2635716fb70f7dc713854638d2dbe884f",
    "799f9257b47bd2ed7f97fa0587e778e789887d5f379eaf78079255e92b86f023",
    "a9645288035eafe4b830003466c572885eab0ba01f8952047d80780afe8686e7",
    "c6715e9801054e4eaa178e4de2b1c69e8c7c1aaedea6b7625596b1462894cd26",
    "cbe7df9131bb7c2a8b3660d023926cae2504f929c4cbdd59846cd4e47c18b51d",
    "5f1f5f5591c00f89685b35024df61cb0ae4dce7df857e6dfc13304e5fe73edec",
    "8e064ed6fb8725c705280b9eb68d3e6e63cdf77b87ec1cd8f1957f468aaa2d6d",
    "a94fd25b335157f44951c4c685c2f1d2fcf449171574db7750538efb842413b3",
    "b9295ae811249e8fb871744362285edb9f3d5fa178ae51f498c67b731f6acc46",
    "1c2a7c51038a927644bebc7db17a5063f6ce4c124d901973438c0228cf4aa117",
    "57cffdd89be4b3fa70679bfdf23ed3a3be4a588c656fac16bd40f8ec286fbb23",
    "c5ddf90101919f47090591a121816847ad20bd7bfc135d400424a457ea143724",
    "ad096b08633e99046db011bfad63b0712ab7848f8253f057036e5807d38c932a",
    "7ee15a7437d9f71312a51536fee3399c897893dca26577806c2a8745891639da",
    "426f37353188477d353ff5c72ec689c3a0fce54832b3b087f10d429845b19746",
    "b4794aeff2e5ea247784efe1e3ad2ecc63df5ebe4ee9ad56cc51b6a80c20f5f0",
    "4c125010894a296658c454def89b96aeaf776853805bd261666ca3744244bc0a",
    "21549d14146bcfaa49f3de0bcf086b1f2903725df69d322389a18c2aa80c3925",
    "bf844ac2961f65dbfaf4f89dbf494ba0fdd3e961dd1083bb2eb40ea32cf57f41",
    "eb45549d0175f52ecbf1b5bb3d904573adb10ed54e88242ccf4f3fb0e0f44087",
    "916fa3fde42f0f4942360d6eb80bd31111d8cd795ac4c89d535a979be3ad64d6",
    "f0b6002122baabc3c41b36db5c703e6e076158b8fdd6fdab711310fbe105ab85",
    "e466eed6d472748c6032440d3e95048d84588e53c711d3151f00074a61e54644",
    "0b25b0372231d9f1c5495a3ac482b067f4dcaaee3f6cbdb7cdc27b37793b65db",
    "c0fb0e475a352c788c1f8560d2212421b8ebf93cb3e95bd2a0676834ec04b680",
    "e95838ff58fe5c56553f92f020c0fe5b227b6b00d566f598f66d0fae3464a168",
    "df93ac1502bdd7e11a716937f08432ada754a0562ab012a322d71e108ab46711",
    "25f6ef0593eac6de746dc80f27911d18260174e238e4d111b9550f365e428475",
    "9464a29db60b7f7082d2264dd5f090da56d6fd1a371346ced22bbd3c6fd595d0",
    "4bb0f64881566ad0b16edb38bb6986ceefcff1779a64b94bab553d9ea86ea0e9",
    "7a0cc70d26b1a99059724f6fcdaf5419c42d82d4637a9b5022ae97208ca207e5",
    "9b32b712062817d083a84616aa24ba63382c262e753fa8196faa54498359ddd5",
    "cb01d575bf5afbf92db08def24073072d59601f8b16e99e69e97f2585269b472",
    "daf2a360796766a4edc2e6291c40d6ef7562082d7f1071950654da3637913594",
    "bcb45e58def5ee926d363119ae7e6d90ab62dacd1071fa326ab7399f696323d3",
    "ba59c3d6429622880d03f5e207098277367d21cb68a8deb34be4b6b538bfe198",
    "c9f983efc3c776485ca34ec870cd326fd77108677f8e362844192d75cc665253",
    "c89c25ad1246fe350481773a6ebece0c4af4d25205031334684ffb46da6e269f",
    "e89686a5372752b6668921e4f6f2ef6ad1bc8af626e9aafcb2e6d5217ed24ff6",
    "edfb7f1b55c18c058ec5248ecd1bef4aef1862b30c125dc3a593bdecda8c51fe",
    "38cae821fad28f01a435e99321bc3e5af470106ae5bc49c0fa4125a6d801be82",
    "de57ff1a7caac501589ec334d426c1b4f0bc13021a975fa5c68ea5196f355809",
    "f1a18f69f4e3a2da2e73749a29a289a1f0b9fdd8ca14636da6e6949f8862fdb1",
    "3dfd21a46e065fcce415e7688ff0356c382e07cbd1e1837790391b8195036888",
    "4bfdb19276abc0b1f8249f3d62d74b1a306cc08d480a0049cd05fb695a2a5f9d",
    "7ee828a974760d6c53f0eea08ab5a1b59be7aedc23f1d58ff9281992c0f87c97",
    "f6c8b39b911301e2b52433aba667eabe5afde09bfcaca3390da2aae2b81ceb15",
    "d33904c93e3cd15d3c07dc1805798779ff7c04077d03fa3fc45017bc579a5295",
    "e41122426188c0ab0543f15450049d161ff4151fa820e1b43496c2bea0bc6a9e",
    "7f9d8a3f39443efa1104985edfb9af28d475e1e610a640d7e176834ff125a8e7",
    "566cd1ef367784c89fa429d9d276633e0f53d334ea65bdb1c28bcfdd1559c498",
    "9f43e06f486eca0f596e52b9f7cbb6ad97516c992fd54d1ed05a67c8d38f38be",
    "577922485fc7af6ad41acfc0210f35c05c9e34f914cdf57121f5a85fdc416191",
    "ef00c47f625b48e9e88e24b9bdf41dcafb78c17cb245c385e7228e265b3ca924",
    "e8098a0873362ee90a77110a1b55a8c0854bf40989452d288b26b850f6c57683",
    "d61ae7aaab32a2b261328c8da6e8ac9879c3555d9dc68d0459f9c7bb3e10bd52",
    "42982d5f2b9296c0bee75a0cd3746f929aa8a22791a75967560774f6f793f168",
)

EXPECTED_GENERATOR_LEDGER_SHA256 = (
    "17ffabc76022262f0ffc2866ccc179e8b7fec5d96ceace239418c24341fcf216"
)


def edge(u, v):
    return (u, v) if u < v else (v, u)


def normalize(zero_edges, c, d):
    return tuple(sorted(zero_edges)) + (c, d)


def support_orbit(support):
    zero_edges, c, d = support[:3], support[3], support[4]
    output = set()
    for permutation in SITE_PERMUTATIONS:
        z = tuple(edge(permutation[u], permutation[v]) for u, v in zero_edges)
        cp = edge(permutation[c[0]], permutation[c[1]])
        dp = edge(permutation[d[0]], permutation[d[1]])
        output.add(normalize(z, cp, dp))
        output.add(normalize(z, dp, cp))
    return output


def representatives():
    all_supports = {
        normalize(zero_edges, c, d)
        for zero_edges in combinations(EDGES, 3)
        for c, d in permutations(
            tuple(pair for pair in EDGES if pair not in zero_edges), 2
        )
    }
    seen = set()
    output = []
    for support in sorted(all_supports):
        if support in seen:
            continue
        orbit = support_orbit(support)
        output.append((support, len(orbit)))
        seen |= orbit
    assert seen == all_supports
    assert len(all_supports) == 60060
    assert len(output) == 70
    return tuple(output)


REPRESENTATIVE_DATA = representatives()
REPRESENTATIVES = tuple(item[0] for item in REPRESENTATIVE_DATA)


def zero_graph_type(zero_edges):
    degrees = Counter(vertex for pair in zero_edges for vertex in pair)
    signature = (len(degrees), tuple(sorted(degrees.values())))
    return {
        (4, (1, 1, 1, 3)): "three_star",
        (3, (2, 2, 2)): "triangle",
        (4, (1, 1, 2, 2)): "three_path",
        (5, (1, 1, 1, 1, 2)): "two_path_plus_edge",
        (6, (1, 1, 1, 1, 1, 1)): "three_matching",
    }[signature]


def determinant3(matrix):
    a, b, c = matrix[0]
    d, e, f = matrix[1]
    g, h, i = matrix[2]
    return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)


def audit_support_and_character_ledgers():
    counts = tuple(count for _, count in REPRESENTATIVE_DATA)
    assert counts == EXPECTED_ORBIT_COUNTS
    assert sum(counts) == 60060

    orbit_digest = hashlib.sha256()
    for support, count in REPRESENTATIVE_DATA:
        orbit_digest.update(f"{support}:{count}\n".encode("ascii"))
    assert orbit_digest.hexdigest() == EXPECTED_ORBIT_LEDGER_SHA256

    graph_counts = Counter(zero_graph_type(edges) for edges in combinations(EDGES, 3))
    assert graph_counts == EXPECTED_ZERO_GRAPH_COUNTS

    determinants = {}
    for name in EXPECTED_ZERO_GRAPH_COUNTS:
        zero_edges = next(
            edges for edges in combinations(EDGES, 3)
            if zero_graph_type(edges) == name
        )
        complements = tuple(tuple(int(u not in pair) for u in U) for pair in zero_edges)
        gram = tuple(
            tuple(sum(x * y for x, y in zip(left, right)) for right in complements)
            for left in complements
        )
        determinants[name] = determinant3(gram)
    assert determinants == EXPECTED_CHARACTER_GRAM_DETERMINANTS
    return counts, orbit_digest.hexdigest(), graph_counts, determinants


def add(*terms):
    nonzero = [term for term in terms if term != "0"]
    if not nonzero:
        return "0"
    if len(nonzero) == 1:
        return nonzero[0]
    return "(" + ")+(".join(nonzero) + ")"


def negative(term):
    return "0" if term == "0" else f"-({term})"


def multiply(left, right):
    if left == "0" or right == "0":
        return "0"
    return f"({left})*({right})"


def q_index(pair, cu, cv):
    return 9 * EDGE_INDEX[pair] + 3 * cu + cv


def endpoint_q_index(pair, vertex, transverse_colour):
    if vertex == pair[0]:
        return q_index(pair, transverse_colour, 0)
    assert vertex == pair[1]
    return q_index(pair, 0, transverse_colour)


def sparse_rank(rows):
    pivots = {}
    for source in rows:
        row = {column: Fraction(value) for column, value in source.items() if value}
        while row:
            column = min(row)
            if column not in pivots:
                scale = row[column]
                pivots[column] = {
                    key: value / scale for key, value in row.items()
                }
                break
            scale = row[column]
            for key, value in pivots[column].items():
                row[key] = row.get(key, Fraction(0)) - scale * value
                if row[key] == 0:
                    del row[key]
    return len(pivots)


def qf_rows(support):
    rows = {}
    for pair, colour in zip(support, (0, 0, 0, 1, 2)):
        u, v = pair
        for cu, cv in product(COLOURS, repeat=2):
            word = [colour] * len(U)
            word[u], word[v] = cu, cv
            row = rows.setdefault(tuple(word), {})
            index = q_index(pair, cu, cv)
            row[index] = row.get(index, 0) + 1
    return tuple(rows.values())


def qf_parameter_basis(support):
    zero_edges = support[:3]
    basis = []

    # Scalar kernel of x_0+x_1+x_2.
    basis.append({
        q_index(zero_edges[0], 0, 0): 1,
        q_index(zero_edges[2], 0, 0): -1,
    })
    basis.append({
        q_index(zero_edges[1], 0, 0): 1,
        q_index(zero_edges[2], 0, 0): -1,
    })

    # Single-transverse incidence kernels, independently at every vertex.
    for vertex in U:
        incident = tuple(pair for pair in zero_edges if vertex in pair)
        for colour in (1, 2):
            for pair in incident[:-1]:
                basis.append({
                    endpoint_q_index(pair, vertex, colour): 1,
                    endpoint_q_index(incident[-1], vertex, colour): -1,
                })

    # Every non-target edge is absent from qF and hence completely free.
    for pair in EDGES:
        if pair in support:
            continue
        for cu, cv in product(COLOURS, repeat=2):
            basis.append({q_index(pair, cu, cv): 1})
    return tuple(basis)


def audit_qf_kernel(support):
    rows = qf_rows(support)
    basis = qf_parameter_basis(support)
    rank = sparse_rank(rows)
    assert rank + len(basis) == N_Q_CELL
    assert sparse_rank(basis) == len(basis)
    for vector in basis:
        for row in rows:
            assert sum(
                Fraction(value) * vector.get(column, 0)
                for column, value in row.items()
            ) == 0
    expected = EXPECTED_QF_RANK_KERNEL[zero_graph_type(support[:3])]
    assert (rank, len(basis)) == expected
    variables, values = qf_parameterization(support)
    assert len(variables) == len(basis)
    actual_basis = []
    for active in variables:
        assignment = {variable: int(variable == active) for variable in variables}
        vector = {}
        for pair in EDGES:
            for cu, cv in product(COLOURS, repeat=2):
                value = eval(
                    values[pair, cu, cv],
                    {"__builtins__": {}},
                    assignment,
                )
                if value:
                    vector[q_index(pair, cu, cv)] = value
        actual_basis.append(vector)
    assert tuple(actual_basis) == basis
    return rank, len(basis)


def qf_parameterization(support):
    zero_edges = support[:3]
    c, d = support[3:]
    values = {}
    variables = []

    # The unique colour-one and colour-two terms force these blocks to zero.
    for pair in (c, d):
        for cu, cv in product(COLOURS, repeat=2):
            values[pair, cu, cv] = "0"

    # Scalar colour-zero equation x_0+x_1+x_2=0.
    variables.extend(("x0", "x1"))
    scalar = ("x0", "x1", negative(add("x0", "x1")))

    # For each used vertex and each transverse coordinate, solve the incidence
    # equation by making the last incident edge minus the preceding sum.
    transverse = {}
    for vertex in U:
        incident = tuple(pair for pair in zero_edges if vertex in pair)
        for colour in (1, 2):
            free = []
            for index, pair in enumerate(incident[:-1]):
                name = f"y{vertex}{colour}_{zero_edges.index(pair)}"
                variables.append(name)
                transverse[pair, vertex, colour] = name
                free.append(name)
            if incident:
                transverse[incident[-1], vertex, colour] = negative(add(*free))

    for index, pair in enumerate(zero_edges):
        u, v = pair
        for cu, cv in product(COLOURS, repeat=2):
            if cu == cv == 0:
                value = scalar[index]
            elif cu != 0 and cv == 0:
                value = transverse[pair, u, cu]
            elif cu == 0 and cv != 0:
                value = transverse[pair, v, cv]
            else:
                value = "0"
            values[pair, cu, cv] = value

    # Every edge outside the five target supports is unrestricted.
    for pair in EDGES:
        if pair in support:
            continue
        u, v = pair
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
    variables, values = qf_parameterization(support)
    target = {}
    for pair, colour in zip(support, (0, 0, 0, 1, 2)):
        sites = tuple(u for u in U if u not in pair)
        target[sites, (colour,) * 4] = 1
    patterns = ((0, 1, 2, 3), (0, 2, 1, 3), (0, 3, 1, 2))
    output = []
    for sites in combinations(U, 4):
        for colours in product(COLOURS, repeat=4):
            terms = tuple(
                multiply(
                    cell(values, sites[i], sites[j], colours[i], colours[j]),
                    cell(values, sites[k], sites[l], colours[k], colours[l]),
                )
                for i, j, k, l in patterns
            )
            polynomial = add(*terms)
            if target.get((sites, colours), 0):
                polynomial = add(polynomial, "-1")
            if polynomial != "0":
                output.append(polynomial)
    return variables, tuple(output)


def ledger_digest(generators):
    digest = hashlib.sha256()
    for generator in generators:
        digest.update(generator.encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def audit_generator_ledger():
    observed = []
    aggregate = hashlib.sha256()
    for orbit, support in enumerate(REPRESENTATIVES, 1):
        _, generators = equations(support)
        digest = ledger_digest(generators)
        observed.append(digest)
        aggregate.update(f"{orbit}:{support}:{digest}\n".encode("ascii"))
    assert tuple(observed) == EXPECTED_GENERATOR_SHA256
    assert aggregate.hexdigest() == EXPECTED_GENERATOR_LEDGER_SHA256
    return aggregate.hexdigest()


def run(orbit, timeout):
    support = REPRESENTATIVES[orbit - 1]
    variables, generators = equations(support)
    digest = ledger_digest(generators)
    assert digest == EXPECTED_GENERATOR_SHA256[orbit - 1]
    program = (
        f"ring r=0,({','.join(variables)}),dp;\n"
        f"ideal I={','.join(generators)};\n"
        "ideal G=slimgb(I);\n"
        'print("BASIS_SIZE"); print(size(G));\n'
        'print("BASIS_FIRST"); print(G[1]);\n'
    )
    executable = shutil.which("Singular")
    if executable is None:
        raise SystemExit("Singular is required")
    started = time.monotonic()
    result = subprocess.run(
        (executable, "-q"), input=program, text=True, capture_output=True,
        check=True, timeout=timeout,
    )
    if result.stderr.strip():
        raise AssertionError(result.stderr)
    lines = tuple(line.strip() for line in result.stdout.splitlines() if line.strip())
    try:
        size = lines[lines.index("BASIS_SIZE") + 1]
        first = lines[lines.index("BASIS_FIRST") + 1]
    except (ValueError, IndexError) as error:
        raise AssertionError(
            f"orbit {orbit}: malformed Singular output:\n{result.stdout}"
        ) from error
    assert size == first == "1", (orbit, result.stdout)
    return (
        orbit, support, len(variables), len(generators), digest,
        time.monotonic() - started,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--orbit", type=int, action="append")
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--skip-ideals", action="store_true")
    args = parser.parse_args()

    counts, orbit_digest, graph_counts, determinants = (
        audit_support_and_character_ledgers()
    )
    generator_digest = audit_generator_ledger()
    qf_audits = tuple(audit_qf_kernel(support) for support in REPRESENTATIVES)

    print("labelled five-distinct-pair supports:", sum(counts))
    print("support orbits:", len(REPRESENTATIVES))
    print("orbit sizes:", counts)
    print("orbit-ledger sha256:", orbit_digest)
    print("zero-graph counts:", dict(sorted(graph_counts.items())))
    print("weight-character Gram determinants:", dict(sorted(determinants.items())))
    print("qF rank/kernel values:", tuple(sorted(set(qf_audits))))
    print("generator-ledger sha256:", generator_digest)

    selected = list(args.orbit or range(1, len(REPRESENTATIVES) + 1))
    if any(orbit < 1 or orbit > len(REPRESENTATIVES) for orbit in selected):
        raise SystemExit(f"--orbit must lie in 1..{len(REPRESENTATIVES)}")
    if args.skip_ideals:
        print("QQ ideals skipped by request")
        return

    outputs = []
    wall_started = time.monotonic()
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {
            pool.submit(run, orbit, args.timeout): orbit for orbit in selected
        }
        for future in as_completed(futures):
            outputs.append(future.result())
    for orbit, support, variable_count, equation_count, digest, elapsed in sorted(outputs):
        print(
            "orbit", orbit, "support", support, "QQ ideal [1]",
            "variables", variable_count, "equations", equation_count,
            "sha256", digest, "seconds", f"{elapsed:.3f}",
        )
    print("parallel wall seconds:", f"{time.monotonic() - wall_started:.3f}")
    print("three-term monomial common-power obstruction exact audit: PASS")


if __name__ == "__main__":
    main()
