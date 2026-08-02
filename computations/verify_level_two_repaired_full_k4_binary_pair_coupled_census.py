#!/usr/bin/env python3
"""Exhaust the binary (M_05,M_14) grid on the repaired 6R packet.

For all 16x16 pairs of binary 2x2 blocks, retain M_04=M_15=E_10 and
the rest of the repaired sharp packet.  The checker classifies exact
differential rank, the two localized pure L0 columns, and the fixed six-root
R2 witnesses.  On rank-55 cases it computes the *actual vertex-sum-coupled*
four-slice factor ideal on the full K4={0,1,4,5}; independent edge scalars
are not used.

F_101 is the discovery field.  Every modular nonunit survivor is rerun over
Q and F_32003.  Python is standard-library; Singular is the sole external
dependency.  Research evidence only; checks remain live under -O and
-I -S.
"""

from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from hashlib import sha256
from itertools import product
from pathlib import Path
from runpy import run_path
from shutil import which
import subprocess


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


HERE = Path(__file__).resolve().parent
REPAIRED = run_path(str(
    HERE
    / "verify_level_two_six_rank_one_isotropic_pencil_repaired_factored_pure_boundary.py"
))
SHARP = REPAIRED["SHARP"]
BASE = REPAIRED["M"]
SITES = REPAIRED["SITES"]
COLOURS = REPAIRED["COLOURS"]
WORDS = REPAIRED["WORDS"]
CELLS = REPAIRED["CELLS"]
WITNESSES = REPAIRED["WITNESSES"]

VARIABLE_EDGES = ((0, 5), (1, 4))
K4_VERTICES = (0, 1, 4, 5)
K4_EDGES = tuple(
    (left, right)
    for position, left in enumerate(K4_VERTICES)
    for right in K4_VERTICES[position + 1:]
)
SLICES = ((0, 0), (0, 1), (1, 0), (1, 1))
MASKS = tuple(range(16))
CASES = tuple(product(MASKS, repeat=2))
DISCOVERY_PRIME = 101
EXACT_MODULUS = 32_003
MAX_WORKERS = 8

EXPECTED_RANK_DISTRIBUTION = Counter({
    55: 172,
    54: 40,
    52: 20,
    51: 12,
    53: 8,
    50: 3,
    48: 1,
})
EXPECTED_RANK_MIXED_DISTRIBUTION = Counter({
    (55, 53): 172,
    (54, 52): 40,
    (52, 50): 20,
    (51, 49): 12,
    (53, 51): 8,
    (50, 48): 3,
    (48, 46): 1,
})
EXPECTED_RANK55_DIGEST = (
    "ce4d50c94e3ee71ca79da513234d214894705835ac72afad45426b60bc4315de"
)
EXPECTED_DISCOVERY_DIGEST = (
    "fc43415ba36a41f1af993b3f66d4cb8b9d6df496f07b44b7ce593795e54a10a3"
)


def mask_block(mask):
    entries = tuple((mask >> index) & 1 for index in range(4))
    return (entries[:2], entries[2:])


def packet_for_case(case):
    packet = dict(BASE)
    for edge, mask in zip(VARIABLE_EDGES, case):
        block = mask_block(mask)
        for a, b in product(COLOURS, repeat=2):
            packet[edge + (a, b)] = block[a][b]
    return packet


def gauge_rows(packet):
    rows = []
    for basis in range(5):
        mu = [0] * 6
        mu[basis] = 1
        mu[5] = -1
        tangent = {
            (u, v, a, b): (mu[u] + mu[v]) * packet[u, v, a, b]
            for u, v, a, b in CELLS
        }
        require(SHARP["apply_differential"](packet, tangent) == [0] * 64,
                ("a binary-grid gauge left the kernel", basis))
        rows.append([tangent[cell] for cell in CELLS])
    return rows


def pure_column(packet, root, neighbour, output):
    return REPAIRED["BOUNDARY"]["pure_column"](
        packet, root, neighbour, output
    )


def audit_rank_incidence_and_r2():
    pure_zero = [int(word == (0,) * 6) for word in WORDS]
    pure_one = [int(word == (1,) * 6) for word in WORDS]
    zero_column = CELLS.index((0, 1, 0, 0))
    one_column = CELLS.index((4, 5, 1, 1))
    rank_distribution = Counter()
    rank_mixed_distribution = Counter()
    rank55 = []
    cofactor_minima = {}

    for case in CASES:
        packet = packet_for_case(case)
        derivative = SHARP["differential_matrix"](packet)
        rank_101 = SHARP["modular_rank"](derivative, 101)
        rank_32003 = SHARP["modular_rank"](derivative, EXACT_MODULUS)
        require(rank_101 == rank_32003,
                ("the two discovery ranks disagree", case,
                 rank_101, rank_32003))
        gauges = gauge_rows(packet)
        require(SHARP["modular_rank"](gauges, 101) == 5,
                ("the binary-grid gauges lost independence", case))
        if rank_101 < 55:
            exact_rank = SHARP["rational_rank"](derivative)
            require(exact_rank == rank_101,
                    ("a modular rank drop did not lift exactly",
                     case, rank_101, exact_rank))
        else:
            exact_rank = 55
            rank55.append(case)
        mixed = [
            row for row, word in zip(derivative, WORDS)
            if word not in ((0,) * 6, (1,) * 6)
        ]
        mixed_rank = SHARP["modular_rank"](mixed, 101)
        rank_distribution[exact_rank] += 1
        rank_mixed_distribution[exact_rank, mixed_rank] += 1

        require([row[zero_column] for row in derivative] == pure_zero,
                ("a binary pair lost the pure-zero tangent", case))
        require([row[one_column] for row in derivative] == pure_one,
                ("a binary pair lost the pure-one tangent", case))
        require(mixed_rank == exact_rank - 2,
                ("the two pure rows did not split from the mixed rows",
                 case, exact_rank, mixed_rank))

        minimum = len(WORDS)
        for root, by_output in WITNESSES.items():
            require(by_output[0] != by_output[1],
                    ("binary-grid R2 neighbours collided", case, root))
            for output, neighbour in by_output.items():
                require(pure_column(packet, root, neighbour, output),
                        ("a binary pair lost a physical pure column",
                         case, root, output, neighbour))
                edge = tuple(sorted((root, neighbour)))
                complement = tuple(site for site in SITES if site not in edge)
                count = sum(
                    SHARP["hafnian"](packet, complement, word) != 0
                    for word in WORDS
                )
                require(count > 0,
                        ("a binary pair killed an R2 cofactor",
                         case, root, output, neighbour))
                minimum = min(minimum, count)
        cofactor_minima[case] = minimum

    require(sum(rank_distribution.values()) == len(CASES),
            "the binary-grid rank census is incomplete")
    require(rank_distribution == EXPECTED_RANK_DISTRIBUTION,
            ("the binary-grid rank census changed", rank_distribution))
    require(rank_mixed_distribution == EXPECTED_RANK_MIXED_DISTRIBUTION,
            ("the binary-grid mixed-rank census changed",
             rank_mixed_distribution))
    require(len(rank55) == rank_distribution[55],
            "the binary-grid rank-55 list is inconsistent")
    rank55_ledger = ";".join(
        f"{left_mask:x}{right_mask:x}"
        for left_mask, right_mask in rank55
    )
    require(sha256(rank55_ledger.encode("utf-8")).hexdigest()
            == EXPECTED_RANK55_DIGEST,
            "the binary-grid rank-55 case ledger changed")
    cofactor_census = Counter(cofactor_minima.values())
    require(cofactor_census == Counter({4: len(CASES)}),
            ("the binary-grid R2 cofactor census changed",
             cofactor_census))
    return (
        rank_distribution,
        rank_mixed_distribution,
        tuple(rank55),
        cofactor_census,
    )


def star_and_alpha_names():
    u_names = tuple(
        f"u{s}r{root}a{a}"
        for s in COLOURS for root in K4_VERTICES for a in COLOURS
    )
    v_names = tuple(
        f"v{t}r{root}a{a}"
        for t in COLOURS for root in K4_VERTICES for a in COLOURS
    )
    alpha_names = tuple(
        f"z{s}{t}r{root}"
        for s, t in SLICES for root in K4_VERTICES
    )
    names = u_names + v_names + alpha_names
    require(len(names) == len(set(names)) == 48,
            "the coupled binary-grid variable census changed")
    return names


NAMES = star_and_alpha_names()


def block_entry(packet, edge, a, b):
    return packet[edge + (a, b)]


def coupled_equations(case):
    packet = packet_for_case(case)
    equations = []
    for s, t in SLICES:
        for r, u in K4_EDGES:
            for a, b in product(COLOURS, repeat=2):
                left = (
                    f"u{s}r{r}a{a}*v{t}r{u}a{b}"
                    f"+v{t}r{r}a{a}*u{s}r{u}a{b}"
                )
                right = (
                    f"(z{s}{t}r{r}+z{s}{t}r{u})"
                    f"*({block_entry(packet, (r, u), a, b)})"
                )
                if (s, t, r, u, a, b) == (0, 0, 0, 1, 0, 0):
                    right = f"({right})+1"
                if (s, t, r, u, a, b) == (1, 1, 4, 5, 1, 1):
                    right = f"({right})+1"
                equations.append(f"({left})-({right})")
    require(len(equations) == len(set(equations)) == 96,
            ("the coupled binary-grid equation census changed", case))
    return tuple(equations)


def chunked(sequence, chunks):
    buckets = [[] for _ in range(chunks)]
    for index, value in enumerate(sequence):
        buckets[index % chunks].append(value)
    return tuple(tuple(bucket) for bucket in buckets if bucket)


def singular_chunk_program(characteristic, cases, label):
    lines = [
        f"ring grid_ring={characteristic},({','.join(NAMES)}),dp;",
        "option(redSB);",
    ]
    for left_mask, right_mask in cases:
        case_label = f"{label}_{left_mask}_{right_mask}"
        lines.extend((
            "ideal grid_ideal="
            + ",\n".join(coupled_equations((left_mask, right_mask))) + ";",
            "ideal grid_basis=std(grid_ideal);",
            f'print("BEGIN_{case_label}");',
            "print(size(grid_basis));",
            "if (size(grid_basis)==1) { print(grid_basis[1]); }",
            f'print("END_{case_label}");',
            "kill grid_ideal;",
            "kill grid_basis;",
        ))
    lines.extend(("exit;", ""))
    return "\n".join(lines)


def parse_chunk_output(output, cases, label):
    lines = tuple(line.strip() for line in output.splitlines())
    results = {}
    for left_mask, right_mask in cases:
        case_label = f"{label}_{left_mask}_{right_mask}"
        begin, end = f"BEGIN_{case_label}", f"END_{case_label}"
        require(lines.count(begin) == lines.count(end) == 1,
                ("a coupled-grid result marker changed", case_label, lines))
        first, last = lines.index(begin), lines.index(end)
        payload = tuple(line for line in lines[first + 1:last] if line)
        require(payload, ("an empty coupled-grid payload appeared", case_label))
        results[left_mask, right_mask] = payload
    return results


def run_chunk(executable, characteristic, cases, label, timeout):
    program = singular_chunk_program(characteristic, cases, label)
    try:
        completed = subprocess.run(
            (executable, "-q"), input=program, text=True,
            capture_output=True, timeout=timeout, check=False,
        )
    except subprocess.TimeoutExpired as error:
        raise RuntimeError(("coupled-grid Singular chunk timed out",
                            characteristic, cases)) from error
    require(completed.returncode == 0,
            ("coupled-grid Singular chunk failed", characteristic,
             completed.returncode, completed.stderr))
    return (
        parse_chunk_output(completed.stdout, cases, label),
        sha256(program.encode("utf-8")).hexdigest(),
    )


def run_parallel_census(executable, characteristic, cases, label, timeout=180):
    chunks = chunked(cases, min(MAX_WORKERS, len(cases)))
    results = {}
    digests = []
    with ThreadPoolExecutor(max_workers=len(chunks)) as executor:
        futures = {
            executor.submit(
                run_chunk, executable, characteristic, chunk,
                f"{label}_{index}", timeout,
            ): index
            for index, chunk in enumerate(chunks)
        }
        for future in as_completed(futures):
            chunk_results, digest = future.result()
            results.update(chunk_results)
            digests.append((futures[future], digest))
    require(set(results) == set(cases),
            ("the coupled-grid Singular census is incomplete",
             characteristic, len(results), len(cases)))
    combined = "\n".join(
        digest for _index, digest in sorted(digests)
    )
    return results, sha256(combined.encode("utf-8")).hexdigest()


def is_unit_payload(payload):
    return payload == ("1", "1")


def audit_coupled_ideals(rank55_cases):
    executable = which("Singular")
    require(executable is not None,
            "external dependency missing: Singular is not on PATH")
    discovery, discovery_digest = run_parallel_census(
        executable, DISCOVERY_PRIME, rank55_cases, "F101"
    )
    modular_survivors = tuple(
        case for case in rank55_cases if not is_unit_payload(discovery[case])
    )
    discovery_sizes = Counter(
        int(payload[0]) for payload in discovery.values()
    )
    require(discovery_digest == EXPECTED_DISCOVERY_DIGEST,
            ("the F101 Singular-program ledger changed",
             discovery_digest))

    exact = {}
    exact_digests = {}
    for characteristic, label in ((0, "Q"), (EXACT_MODULUS, "F32003")):
        if modular_survivors:
            results, digest = run_parallel_census(
                executable, characteristic, modular_survivors, label
            )
        else:
            results, digest = {}, sha256(b"").hexdigest()
        exact[label] = results
        exact_digests[label] = digest
    exact_survivors = tuple(
        case for case in modular_survivors
        if not is_unit_payload(exact["Q"][case])
    )
    require(discovery_sizes == Counter({1: len(rank55_cases)}),
            ("the F101 basis-size census changed", discovery_sizes,
             exact))
    require(not exact_survivors,
            ("an exact nonunit survivor appeared", exact_survivors))
    require(not modular_survivors,
            ("a new F101 nonunit survivor appeared", modular_survivors,
             exact))
    return {
        "discovery_sizes": discovery_sizes,
        "modular_survivors": modular_survivors,
        "exact_Q": exact["Q"],
        "exact_F32003": exact["F32003"],
        "exact_survivors": exact_survivors,
        "digests": {
            "F101": discovery_digest,
            **exact_digests,
        },
    }


def main():
    rank_data = audit_rank_incidence_and_r2()
    ideals = audit_coupled_ideals(rank_data[2])
    print("repaired full-K4 binary-pair coupled census: passed")
    print(f"  exact differential ranks       : {rank_data[0]}")
    print(f"  rank/mixed-rank pairs          : {rank_data[1]}")
    print(f"  rank-55 cases                  : {len(rank_data[2])}/256")
    print(f"  R2 cofactor-minimum census     : {rank_data[3]}")
    print(f"  F101 basis-size census         : {ideals['discovery_sizes']}")
    print(f"  F101 nonunit survivors         : {ideals['modular_survivors']}")
    print(f"  exact Q payloads               : {ideals['exact_Q']}")
    print(f"  exact F32003 payloads          : {ideals['exact_F32003']}")
    print(f"  exact nonunit survivors        : {ideals['exact_survivors']}")
    print(f"  chunk-ledger digests           : {ideals['digests']}")


if __name__ == "__main__":
    main()
