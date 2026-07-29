#!/usr/bin/env python3
"""Independent audit of the compatible three-extra-cell frontier.

This checker is deliberately standalone: it imports neither of the two
fixed-q three-cell verifiers.  It reconstructs the 99 invisible cells, the
3,960 compatible pairs, all 87,027 compatible triples, and their projective
pair-cap closure directly from the displayed (q,z).

For every residual multi-pair triple it also constructs the complete
localized characteristic-zero pair-cap ideal.  The independent Singular
encoding reverses the word, term, coordinate, and parameter orders used by
the primary batch; its torus generator is first.  By default no Singular
job is launched.  ``--ideal-prefix N`` runs only a diagnostic prefix, while
``--all-ideals`` is the explicit heavy 742-job audit.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict, deque
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
from itertools import combinations, product
import json
from pathlib import Path
import shutil
import subprocess
import time


SITES = tuple(range(8))
COLOURS = tuple(range(3))
PHYSICAL_PAIRS = tuple(combinations(SITES, 2))

Cell = tuple[int, int, int, int]
Mode = tuple[int, int]
Word = tuple[int, ...]
Exponent = tuple[int, int, int]
GramEdge = tuple[Mode, Mode]
Triple = tuple[Cell, Cell, Cell]

ALL_CELLS: tuple[Cell, ...] = tuple(
    (i, j, ci, cj)
    for i, j in PHYSICAL_PAIRS
    for ci, cj in product(COLOURS, repeat=2)
)

BASE_Q: tuple[Cell, ...] = (
    (2, 3, 0, 0),
    (4, 5, 0, 0),
    (6, 7, 0, 0),
    (0, 1, 1, 1),
    (3, 6, 1, 1),
    (5, 7, 1, 1),
    (0, 2, 2, 2),
    (1, 4, 2, 2),
    (5, 6, 2, 2),
)

DISPLAYED_Z: tuple[Cell, ...] = (
    (0, 1, 0, 0),
    (2, 4, 1, 1),
    (3, 7, 2, 2),
)

PURE_WORDS: tuple[Word, ...] = tuple((colour,) * 8 for colour in COLOURS)
TARGET_WORDS = frozenset(PURE_WORDS)

# These are the eleven pairs covered by the separately audited arbitrary
# full-block theorem.  They are repeated literally here so coverage of the
# sole one-pair projective survivor is a check, not an import.
INVISIBLE_FULL_BLOCK_PAIRS = frozenset({
    (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (1, 2),
    (1, 3), (1, 5), (1, 7), (2, 5), (3, 4),
})

EXPECTED_COUNTS = {
    "invisible_cells": 99,
    "compatible_pairs": 3_960,
    "compatible_triples": 87_027,
    "projectively_closed": 86_284,
    "projective_survivors": 743,
    "multi_pair_survivors": 742,
}

EXPECTED_PHYSICAL_PAIR_CENSUS = Counter({1: 924, 2: 28_512, 3: 57_591})
EXPECTED_SURVIVOR_CENSUS = Counter({1: 1, 2: 229, 3: 513})

# Shared canonical digest from the primary computation.  It hashes every
# survivor as (triple, number_of_physical_pairs, reason, branches), in the
# common lexicographic triple order.  This clean-room checker must reproduce
# it without importing the primary implementation.
EXPECTED_CANONICAL_SURVIVOR_SHA256 = (
    "b481e4abddc0e98e8cbde9486d7d384a821430b15964dde6e9b279367988a57a"
)

# Filled only after the clean-room reconstruction itself was stable.  These
# pin this checker's own exact compatible-triple, closure, multi-survivor,
# and independently ordered ideal-program ledgers.
EXPECTED_COMPATIBLE_TRIPLE_SHA256 = (
    "47d231f82e3e6bd272e0b440667a06fc6fe110716a916512555330d644e08a22"
)
EXPECTED_INDEPENDENT_CLOSURE_SHA256 = (
    "c3d4eb15e6ad9f53eee400197be8d1e5e68ab7a8b274c5377712935689f6d58a"
)
EXPECTED_MULTI_PAIR_SURVIVOR_SHA256 = (
    "025cb3d4d283ef8bab747ccf587eb97bd8741f0bc5bc642b3524b74dc44cbb0b"
)
EXPECTED_IDEAL_PROGRAM_LEDGER_SHA256 = (
    "ddb50c85a030b693c98d5161a7fcc67ee26f269aaadb07b2013ad0d52d2aab9e"
)
EXPECTED_FULL_IDEAL_RESULT_SHA256 = (
    "2e9ecab9ee8a62e41d6e7683bab9731138a137ca9e2662a6ff843a9f901e4e84"
)


def sites_mask(cell: Cell) -> int:
    return (1 << cell[0]) | (1 << cell[1])


def disjoint(cells: tuple[Cell, ...]) -> bool:
    occupied = 0
    for cell in cells:
        mask = sites_mask(cell)
        if occupied & mask:
            return False
        occupied |= mask
    return True


def partial_word(cells: tuple[Cell, ...]) -> Word:
    result = [-1] * len(SITES)
    for i, j, ci, cj in cells:
        assert i < j and result[i] == result[j] == -1
        result[i], result[j] = ci, cj
    return tuple(result)


def complete_word(cells: tuple[Cell, ...]) -> Word:
    result = partial_word(cells)
    assert -1 not in result
    return result


def base_identity() -> Counter[Word]:
    result: Counter[Word] = Counter()
    for z_cell in DISPLAYED_Z:
        for selected in combinations(BASE_Q, 3):
            cells = (z_cell,) + selected
            if disjoint(cells):
                result[complete_word(cells)] += 1
    return result


def one_cell_debt(cell: Cell) -> Counter[Word]:
    """The literal coefficient of x in z (q+x cell)^[3]."""
    result: Counter[Word] = Counter()
    for z_cell in DISPLAYED_Z:
        for selected in combinations(BASE_Q, 2):
            cells = (z_cell, cell) + selected
            if disjoint(cells):
                result[complete_word(cells)] += 1
    return result


def two_cell_debt(left: Cell, right: Cell) -> Counter[Word]:
    """The literal coefficient of xy in z(q+x left+y right)^[3]."""
    result: Counter[Word] = Counter()
    for z_cell in DISPLAYED_Z:
        for q_cell in BASE_Q:
            cells = (z_cell, left, right, q_cell)
            if disjoint(cells):
                result[complete_word(cells)] += 1
    return result


def three_cell_debt(triple: Triple) -> Counter[Word]:
    """The literal coefficient of xyz in z(q+x e+y f+z g)^[3]."""
    result: Counter[Word] = Counter()
    for z_cell in DISPLAYED_Z:
        cells = (z_cell,) + triple
        if disjoint(cells):
            result[complete_word(cells)] += 1
    return result


def hash_lines(records) -> str:
    digest = hashlib.sha256()
    for record in records:
        digest.update(repr(record).encode("utf-8"))
        digest.update(b"\n")
    return digest.hexdigest()


def reconstruct_compatible_triples() -> dict:
    assert len(ALL_CELLS) == 252 and len(set(ALL_CELLS)) == 252
    assert len(BASE_Q) == len(set(BASE_Q)) == 9
    assert base_identity() == Counter({word: 1 for word in PURE_WORDS})

    outside = tuple(cell for cell in ALL_CELLS if cell not in BASE_Q)
    assert len(outside) == 243
    debts = {cell: one_cell_debt(cell) for cell in outside}
    assert Counter(len(value) for value in debts.values()) == Counter({0: 99, 1: 135, 2: 9})
    assert all(
        coefficient == 1
        for value in debts.values()
        for coefficient in value.values()
    )
    invisible = tuple(cell for cell in outside if not debts[cell])
    assert len(invisible) == EXPECTED_COUNTS["invisible_cells"]

    compatible_edges = set()
    for left, right in combinations(invisible, 2):
        debt = two_cell_debt(left, right)
        assert all(coefficient == 1 for coefficient in debt.values())
        if not debt:
            compatible_edges.add((left, right))
    assert len(compatible_edges) == EXPECTED_COUNTS["compatible_pairs"]

    triples = []
    physical_pair_census = Counter()
    for triple in combinations(invisible, 3):
        if not all(pair in compatible_edges for pair in combinations(triple, 2)):
            continue
        # Pairwise compatibility alone could in principle leave an xyz debt;
        # check its vanishing literally for every triangle.
        debt = three_cell_debt(triple)
        assert not debt, (triple, debt)
        triples.append(triple)
        physical_pair_census[len({cell[:2] for cell in triple})] += 1

    assert len(triples) == EXPECTED_COUNTS["compatible_triples"]
    assert physical_pair_census == EXPECTED_PHYSICAL_PAIR_CENSUS
    triple_hash = hash_lines(triples)
    assert triple_hash == EXPECTED_COMPATIBLE_TRIPLE_SHA256
    return {
        "invisible": invisible,
        "compatible_edges": frozenset(compatible_edges),
        "triples": tuple(triples),
        "physical_pair_census": physical_pair_census,
        "triple_hash": triple_hash,
    }


def add_exponents(items: tuple[Exponent, ...]) -> Exponent:
    return tuple(sum(item[axis] for item in items) for axis in range(3))


def normalized_edge(left: Mode, right: Mode) -> GramEdge:
    assert left[0] != right[0]
    return tuple(sorted((left, right)))


def tagged_quadratic(triple: Triple) -> tuple[tuple[Cell, Exponent], ...]:
    zero = (0, 0, 0)
    tagged_extras = tuple(
        (cell, tuple(int(axis == index) for axis in range(3)))
        for index, cell in enumerate(triple)
    )
    return tuple((cell, zero) for cell in BASE_Q) + tagged_extras


def coordinate_forms(triple: Triple) -> tuple[
    dict[Word, Counter[tuple[GramEdge, Exponent]]],
    dict[Word, Counter[Exponent]],
]:
    """Expand ps Q^[3] and Q^[4], retaining exact t,u,v exponents."""
    tagged = tagged_quadratic(triple)
    gram: defaultdict[Word, Counter[tuple[GramEdge, Exponent]]] = defaultdict(Counter)
    direct: defaultdict[Word, Counter[Exponent]] = defaultdict(Counter)

    for selected in combinations(tagged, 3):
        cells = tuple(item[0] for item in selected)
        if not disjoint(cells):
            continue
        word = partial_word(cells)
        missing = tuple(site for site, colour in enumerate(word) if colour == -1)
        assert len(missing) == 2
        exponent = add_exponents(tuple(item[1] for item in selected))
        for first_colour, second_colour in product(COLOURS, repeat=2):
            completed = list(word)
            completed[missing[0]] = first_colour
            completed[missing[1]] = second_colour
            edge = normalized_edge(
                (missing[0], first_colour), (missing[1], second_colour)
            )
            gram[tuple(completed)][edge, exponent] += 1

    for selected in combinations(tagged, 4):
        cells = tuple(item[0] for item in selected)
        if not disjoint(cells):
            continue
        exponent = add_exponents(tuple(item[1] for item in selected))
        direct[complete_word(cells)][exponent] += 1

    return dict(gram), dict(direct)


def forced_zero_edges(
    gram: dict[Word, Counter[tuple[GramEdge, Exponent]]],
    direct: dict[Word, Counter[Exponent]],
) -> frozenset[GramEdge]:
    zeros = set()
    for word, terms in gram.items():
        if word in TARGET_WORDS or direct.get(word) or len(terms) != 1:
            continue
        (edge, _exponent), coefficient = next(iter(terms.items()))
        assert coefficient > 0
        zeros.add(edge)
    return frozenset(zeros)


def odd_zero_walk(
    edge: GramEdge,
    zero_edges: frozenset[GramEdge],
    active: frozenset[Mode],
) -> tuple[Mode, ...] | None:
    """Find an odd zero-edge walk joining a required-nonzero Gram pair.

    The parity-state BFS is intentionally different from the primary
    bipartiteness/union-find implementation.  Repeated vertices are allowed:
    an odd walk still composes the projective orthogonal-complement involution
    an odd number of times and therefore forces the required Gram entry zero.
    """
    adjacency = {mode: set() for mode in active}
    for left, right in zero_edges:
        if left in active and right in active:
            adjacency[left].add(right)
            adjacency[right].add(left)

    start = (edge[0], 0)
    target = (edge[1], 1)
    parents: dict[tuple[Mode, int], tuple[Mode, int] | None] = {start: None}
    queue = deque([start])
    while queue:
        state = queue.popleft()
        if state == target:
            path = []
            while state is not None:
                path.append(state[0])
                state = parents[state]
            path.reverse()
            assert len(path) % 2 == 0  # odd number of edges
            assert path[0] == edge[0] and path[-1] == edge[1]
            assert all(
                normalized_edge(left, right) in zero_edges
                for left, right in zip(path, path[1:])
            )
            return tuple(path)
        mode, parity = state
        for neighbour in sorted(adjacency[mode]):
            next_state = (neighbour, parity ^ 1)
            if next_state not in parents:
                parents[next_state] = state
                queue.append(next_state)
    return None


def projective_classification(triple: Triple) -> tuple[str, int, tuple]:
    gram, direct = coordinate_forms(triple)

    choices = []
    for word in PURE_WORDS:
        if direct.get(word):
            return "pure_direct", 0, ()
        options = tuple(sorted({edge for edge, _exponent in gram.get(word, {})}))
        if not options:
            return "pure_missing", 0, ()
        choices.append(options)

    zeros = forced_zero_edges(gram, direct)
    certificates = []
    for branches, required in enumerate(product(*choices), 1):
        active = frozenset(mode for edge in required for mode in edge)
        witness = None
        for required_edge in required:
            walk = odd_zero_walk(required_edge, zeros, active)
            if walk is not None:
                witness = (required_edge, walk)
                break
        if witness is None:
            return "open_branch", branches, tuple(certificates)
        certificates.append(witness)
    return "closed", len(certificates), tuple(certificates)


def reconstruct_projective_frontier(triples: tuple[Triple, ...]) -> dict:
    ledger = Counter()
    closed_branch_histogram = Counter()
    survivors = []
    closure_digest = hashlib.sha256()
    canonical_survivor_digest = hashlib.sha256()
    started = time.monotonic()

    for index, triple in enumerate(triples, 1):
        pair_count = len({cell[:2] for cell in triple})
        status, branches, certificates = projective_classification(triple)
        ledger[pair_count, status] += 1
        if status == "closed":
            closed_branch_histogram[pair_count, branches] += 1
        else:
            survivor = (triple, pair_count, status, branches)
            survivors.append(survivor)
            canonical_survivor_digest.update(repr(survivor).encode("utf-8"))
            canonical_survivor_digest.update(b"\n")
        # Pin the independently found witness data by its exact odd-walk
        # lengths, without retaining 86k full certificate objects in memory.
        signature = tuple(
            (required, len(walk) - 1) for required, walk in certificates
        )
        closure_digest.update(
            repr((triple, pair_count, status, branches, signature)).encode("utf-8")
        )
        closure_digest.update(b"\n")
        if index % 10_000 == 0:
            print(
                "projective progress:", index, "/", len(triples),
                "survivors", len(survivors), flush=True,
            )

    survivor_census = Counter(item[1] for item in survivors)
    assert survivor_census == EXPECTED_SURVIVOR_CENSUS
    assert sum(
        count for (pair_count, status), count in ledger.items() if status == "closed"
    ) == EXPECTED_COUNTS["projectively_closed"]
    assert len(survivors) == EXPECTED_COUNTS["projective_survivors"]
    assert canonical_survivor_digest.hexdigest() == EXPECTED_CANONICAL_SURVIVOR_SHA256

    # More detailed expected ledger, reconstructed rather than imported.
    expected_ledger = Counter({
        (1, "closed"): 923,
        (1, "open_branch"): 1,
        (2, "closed"): 28_283,
        (2, "open_branch"): 165,
        (2, "pure_direct"): 64,
        (3, "closed"): 57_078,
        (3, "open_branch"): 320,
        (3, "pure_direct"): 193,
    })
    assert ledger == expected_ledger

    one_pair = tuple(item for item in survivors if item[1] == 1)
    assert len(one_pair) == 1
    one_pair_triple = one_pair[0][0]
    unique_pair = next(iter({cell[:2] for cell in one_pair_triple}))
    assert unique_pair in INVISIBLE_FULL_BLOCK_PAIRS
    # q+t e+u f+v g is a literal specialization of the arbitrary 3x3 block
    # on this pair (all other block entries zero), so the audited theorem
    # covers every nonzero t,u,v here, as well as their boundary values.

    multi_pair = tuple(item[0] for item in survivors if item[1] >= 2)
    assert len(multi_pair) == EXPECTED_COUNTS["multi_pair_survivors"]
    multi_hash = hash_lines(multi_pair)
    independent_hash = closure_digest.hexdigest()
    assert independent_hash == EXPECTED_INDEPENDENT_CLOSURE_SHA256
    assert multi_hash == EXPECTED_MULTI_PAIR_SURVIVOR_SHA256

    return {
        "ledger": ledger,
        "closed_branch_histogram": closed_branch_histogram,
        "survivors": tuple(survivors),
        "survivor_census": survivor_census,
        "one_pair_triple": one_pair_triple,
        "one_pair_physical_pair": unique_pair,
        "multi_pair": multi_pair,
        "canonical_survivor_hash": canonical_survivor_digest.hexdigest(),
        "independent_closure_hash": independent_hash,
        "multi_pair_hash": multi_hash,
        "seconds": time.monotonic() - started,
    }


def variable_name(prefix: str, mode: Mode) -> str:
    return f"{prefix}{mode[0]}{mode[1]}"


def independent_variables() -> tuple[str, ...]:
    coordinates = tuple(
        variable_name(prefix, (site, colour))
        for colour in reversed(COLOURS)
        for site in reversed(SITES)
        for prefix in ("s", "p")
    )
    variables = ("rho", "v", "u", "t", "a") + coordinates
    assert len(variables) == len(set(variables)) == 53
    return variables


def beta_polynomial(edge: GramEdge) -> str:
    left, right = edge
    # Reverse the two summands compared with the primary encoding.
    return (
        f"({variable_name('s', left)}*{variable_name('p', right)}"
        f"+{variable_name('p', left)}*{variable_name('s', right)})"
    )


def parameter_monomial(exponent: Exponent) -> str:
    factors = ("v",) * exponent[2] + ("u",) * exponent[1] + ("t",) * exponent[0]
    return "*".join(factors)


def polynomial_term(coefficient: int, factors: tuple[str, ...]) -> str:
    pieces = []
    if coefficient != 1:
        pieces.append(str(coefficient))
    pieces.extend(factor for factor in factors if factor)
    return "*".join(pieces) if pieces else "1"


def independent_ideal_program(triple: Triple) -> tuple[str, int, int]:
    gram, direct = coordinate_forms(triple)
    coordinate_equations = []
    # Descending word order, direct terms before Gram terms, and descending
    # tagged-term order all differ from the primary batch.
    for word in sorted(set(gram) | set(direct) | set(TARGET_WORDS), reverse=True):
        terms = []
        for exponent, multiplicity in sorted(direct.get(word, {}).items(), reverse=True):
            terms.append(
                polynomial_term(4 * multiplicity, ("a", parameter_monomial(exponent)))
            )
        for (edge, exponent), multiplicity in sorted(gram.get(word, {}).items(), reverse=True):
            terms.append(
                polynomial_term(
                    4 * multiplicity,
                    (parameter_monomial(exponent), beta_polynomial(edge)),
                )
            )
        if word in TARGET_WORDS:
            terms.append("-1")
        if terms:
            coordinate_equations.append("+".join(terms))

    equations = ("rho*v*u*t-1", *coordinate_equations)
    variables = independent_variables()
    program = (
        f"ring R=0,({','.join(variables)}),dp;\n"
        f"ideal J={','.join(equations)};\n"
        "option(redSB);\n"
        "ideal H=std(J);\n"
        'print("SIZE");\n'
        "print(size(H));\n"
        'print("FIRST");\n'
        "print(H[1]);\n"
    )
    return program, len(equations), len(variables)


def ideal_program_ledger(triples: tuple[Triple, ...]) -> tuple[str, Counter]:
    digest = hashlib.sha256()
    equation_histogram = Counter()
    for index, triple in enumerate(triples):
        program, equations, variables = independent_ideal_program(triple)
        assert variables == 53
        program_hash = hashlib.sha256(program.encode("utf-8")).hexdigest()
        record = (index, triple, equations, variables, program_hash)
        digest.update(repr(record).encode("utf-8"))
        digest.update(b"\n")
        equation_histogram[equations] += 1
    result = digest.hexdigest()
    assert result == EXPECTED_IDEAL_PROGRAM_LEDGER_SHA256
    return result, equation_histogram


def cache_file(cache_dir: Path, index: int, triple: Triple) -> Path:
    token = hashlib.sha256(repr(triple).encode("utf-8")).hexdigest()[:16]
    return cache_dir / f"{index:04d}-{token}.json"


def cached_result(
    path: Path, index: int, triple: Triple, program_hash: str,
) -> dict | None:
    if not path.exists():
        return None
    try:
        value = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        return None
    expected = {
        "index": index,
        "triple": [list(cell) for cell in triple],
        "program_sha256": program_hash,
    }
    if any(value.get(key) != item for key, item in expected.items()):
        return None
    if value.get("basis_size") != "1" or value.get("basis_first") != "1":
        return None
    return value


def run_ideal(
    singular: str,
    cache_dir: Path,
    index: int,
    triple: Triple,
    timeout: int,
) -> dict:
    program, equations, variables = independent_ideal_program(triple)
    program_hash = hashlib.sha256(program.encode("utf-8")).hexdigest()
    path = cache_file(cache_dir, index, triple)
    old = cached_result(path, index, triple, program_hash)
    if old is not None:
        old["cached"] = True
        return old

    started = time.monotonic()
    process = subprocess.run(
        [singular, "-q"],
        input=program,
        text=True,
        capture_output=True,
        check=True,
        timeout=timeout,
    )
    elapsed = time.monotonic() - started
    if process.stderr.strip():
        raise AssertionError(process.stderr)
    lines = tuple(line.strip() for line in process.stdout.splitlines() if line.strip())
    size = lines[lines.index("SIZE") + 1]
    first = lines[lines.index("FIRST") + 1]
    assert size == first == "1", (index, triple, process.stdout)
    value = {
        "index": index,
        "triple": [list(cell) for cell in triple],
        "program_sha256": program_hash,
        "equations": equations,
        "variables": variables,
        "basis_size": size,
        "basis_first": first,
        "seconds": elapsed,
        "cached": False,
    }
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(value, sort_keys=True) + "\n")
    temporary.replace(path)
    return value


def stable_result_hash(results: list[dict]) -> str:
    records = []
    for value in sorted(results, key=lambda item: item["index"]):
        records.append((
            value["index"],
            tuple(tuple(cell) for cell in value["triple"]),
            value["program_sha256"],
            value["equations"],
            value["variables"],
            value["basis_size"],
            value["basis_first"],
        ))
    return hash_lines(records)


def run_selected_ideals(
    triples: tuple[Triple, ...],
    selected_count: int,
    workers: int,
    timeout: int,
    cache_dir: Path,
) -> list[dict]:
    singular = shutil.which("Singular")
    if singular is None:
        raise SystemExit("Singular is required for an ideal replay")
    cache_dir.mkdir(parents=True, exist_ok=True)
    selected = tuple(enumerate(triples[:selected_count]))
    results = []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {
            pool.submit(run_ideal, singular, cache_dir, index, triple, timeout): index
            for index, triple in selected
        }
        for completed, future in enumerate(as_completed(futures), 1):
            value = future.result()
            results.append(value)
            print(
                "ideal progress:", completed, "/", len(selected),
                "index", value["index"], "equations", value["equations"],
                "seconds", f"{value['seconds']:.3f}", "cached", value["cached"],
                flush=True,
            )
    assert len(results) == len(selected)
    return results


def main() -> None:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--ideal-prefix", type=int, default=0,
        help="run only the first N of 742 independent ideals (diagnostic)",
    )
    group.add_argument(
        "--all-ideals", action="store_true",
        help="run the complete, intentionally heavy 742-ideal audit",
    )
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--timeout", type=int, default=900)
    parser.add_argument(
        "--cache-dir", type=Path,
        default=Path("/tmp/krenn-compatible-three-extra-independent-ideals"),
    )
    parser.add_argument("--print-survivors", action="store_true")
    args = parser.parse_args()
    assert args.ideal_prefix >= 0 and args.workers >= 1 and args.timeout >= 1

    started = time.monotonic()
    compatible = reconstruct_compatible_triples()
    print("compatible census: PASS", flush=True)
    print("invisible cells:", len(compatible["invisible"]), flush=True)
    print("compatible pairs:", len(compatible["compatible_edges"]), flush=True)
    print("compatible triples:", len(compatible["triples"]), flush=True)
    print(
        "physical-pair census:", dict(sorted(compatible["physical_pair_census"].items())),
        flush=True,
    )
    print("compatible-triple sha256:", compatible["triple_hash"], flush=True)

    frontier = reconstruct_projective_frontier(compatible["triples"])
    print("projective closure: PASS", flush=True)
    print("projective ledger:", dict(sorted(frontier["ledger"].items())), flush=True)
    print(
        "closed branch histogram:",
        dict(sorted(frontier["closed_branch_histogram"].items())), flush=True,
    )
    print("survivor census:", dict(sorted(frontier["survivor_census"].items())), flush=True)
    print("one-pair survivor:", frontier["one_pair_triple"], flush=True)
    print("one-pair block:", frontier["one_pair_physical_pair"], flush=True)
    print("one-pair survivor covered by arbitrary full-block theorem: PASS", flush=True)
    print("multi-pair survivors:", len(frontier["multi_pair"]), flush=True)
    print("canonical-survivor sha256:", frontier["canonical_survivor_hash"], flush=True)
    print("independent-closure sha256:", frontier["independent_closure_hash"], flush=True)
    print("multi-pair-survivor sha256:", frontier["multi_pair_hash"], flush=True)
    print("projective seconds:", f"{frontier['seconds']:.3f}", flush=True)

    if args.print_survivors:
        for index, triple in enumerate(frontier["multi_pair"]):
            print("multi-pair survivor", index, triple)

    program_hash, equation_histogram = ideal_program_ledger(frontier["multi_pair"])
    print("independent ideal-program ledger: PASS", flush=True)
    print("ideal equation histogram:", dict(sorted(equation_histogram.items())), flush=True)
    print("ideal-program-ledger sha256:", program_hash, flush=True)

    selected_count = len(frontier["multi_pair"]) if args.all_ideals else args.ideal_prefix
    if selected_count:
        assert selected_count <= len(frontier["multi_pair"])
        results = run_selected_ideals(
            frontier["multi_pair"], selected_count, args.workers,
            args.timeout, args.cache_dir,
        )
        result_hash = stable_result_hash(results)
        print("unit ideals:", len(results), "/", selected_count)
        print("ideal-result sha256:", result_hash)
        if not args.all_ideals:
            print("DIAGNOSTIC PREFIX ONLY: no complete 742-ideal claim")
        else:
            assert result_hash == EXPECTED_FULL_IDEAL_RESULT_SHA256
            print("all 742 independently ordered ideals are unit: PASS")
    else:
        print("NO SINGULAR JOBS REQUESTED")

    print("total wall seconds:", f"{time.monotonic() - started:.3f}")


if __name__ == "__main__":
    main()
