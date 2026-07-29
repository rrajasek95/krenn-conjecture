#!/usr/bin/env python3
"""Exact pair-cap obstruction for a full block on any invisible pair.

Start with the nine-cell quadratic q and three-cell quadratic z from the
polarized eight-site model.  Add an arbitrary 3 by 3 endpoint-colour block

    E_uv = sum_(i,j=0)^2 x_ij e_(u,i),(v,j).

There are eleven physical pairs uv for which every such E_uv is invisible
to z*(-)*q^[2], so z*(q+E_uv)^[3] remains Delta.  This checker proves for
each of the eleven pairs, with completely unrestricted x_ij (zeros included),
that the same quadratic q+E_uv has no pair-cap preimage

    (a*(q+E) + 4*p*s) * (q+E)^[3] = Delta.

The construction is independent of the earlier one-cell, support-only, and
minimal-support programs.  Divided powers are generated directly as
unordered matchings.  For each physical pair, one unsaturated complete
characteristic-zero coordinate ideal is checked with Singular over QQ.
Thus one unit-ideal calculation includes all 512 support strata and every
exceptional coefficient ratio.  A deterministic ledger hashes every job.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
import hashlib
from itertools import combinations, product
import os
import shutil
import subprocess
import time


SITE_COUNT = 8
COLOURS = (0, 1, 2)
EMPTY = -1
PRIMARY_PAIR = (1, 7)

INVISIBLE_PAIRS = (
    (0, 3), (0, 4), (0, 5), (0, 6), (0, 7),
    (1, 2), (1, 3), (1, 5), (1, 7), (2, 5), (3, 4),
)

Mode = tuple[int, int]
Word = tuple[int, ...]
GramEntry = tuple[Mode, Mode]
ParamMonomial = tuple[str, ...]
ParamPolynomial = Counter[ParamMonomial]


# These literals are intentionally repeated here: this checker imports no
# model construction from another computation.
BASE_Q = (
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

Z_CELLS = (
    (0, 1, 0, 0),
    (2, 4, 1, 1),
    (3, 7, 2, 2),
)

# Collecting repeated identical matching contributions before declaring a
# coordinate singleton strengthens the earlier exploratory support census.
EXPECTED_MINIMAL_OPEN = (261, 291)
EXPECTED_OPEN_COUNT = 80


@dataclass(frozen=True)
class Cell:
    left: int
    right: int
    left_colour: int
    right_colour: int
    parameter: str | None = None

    @property
    def sites(self) -> tuple[int, int]:
        return (self.left, self.right)


def block_cells(pair: tuple[int, int]) -> tuple[tuple[int, int, int, int], ...]:
    return tuple(
        (pair[0], pair[1], left_colour, right_colour)
        for left_colour in COLOURS
        for right_colour in COLOURS
    )


def parameter_name(cell: tuple[int, int, int, int]) -> str:
    return f"x{cell[2]}{cell[3]}"


def selected_cells(
    mask: int, pair: tuple[int, int] = PRIMARY_PAIR,
) -> tuple[tuple[int, int, int, int], ...]:
    return tuple(
        cell for bit, cell in enumerate(block_cells(pair)) if mask & (1 << bit)
    )


def support_label(mask: int, pair: tuple[int, int] = PRIMARY_PAIR) -> str:
    active = selected_cells(mask, pair)
    return ",".join(f"{cell[2]}{cell[3]}" for cell in active) or "empty"


def disjoint(cells: tuple[Cell, ...]) -> bool:
    sites = [site for cell in cells for site in cell.sites]
    return len(sites) == len(set(sites))


def matching_word(cells: tuple[Cell, ...]) -> Word:
    word = [EMPTY] * SITE_COUNT
    for cell in cells:
        assert word[cell.left] == EMPTY and word[cell.right] == EMPTY
        word[cell.left] = cell.left_colour
        word[cell.right] = cell.right_colour
    return tuple(word)


def matching_divided_power(cells: tuple[Cell, ...], degree: int) -> dict[Word, ParamPolynomial]:
    """Expand q^[degree] directly as unordered disjoint cell selections."""
    answer: defaultdict[Word, Counter[ParamMonomial]] = defaultdict(Counter)
    for choice in combinations(cells, degree):
        if not disjoint(choice):
            continue
        monomial = tuple(sorted(
            cell.parameter for cell in choice if cell.parameter is not None
        ))
        answer[matching_word(choice)][monomial] += 1
    return {word: Counter(poly) for word, poly in answer.items()}


def add_polynomial(target: ParamPolynomial, source: ParamPolynomial) -> None:
    target.update(source)
    for monomial in tuple(target):
        if target[monomial] == 0:
            del target[monomial]


def multiply_by_literal_cells(
    poly: dict[Word, ParamPolynomial],
    literals: tuple[tuple[int, int, int, int], ...],
) -> dict[Word, ParamPolynomial]:
    answer: defaultdict[Word, Counter[ParamMonomial]] = defaultdict(Counter)
    for word, coefficient in poly.items():
        for left, right, left_colour, right_colour in literals:
            if word[left] != EMPTY or word[right] != EMPTY:
                continue
            full = list(word)
            full[left] = left_colour
            full[right] = right_colour
            add_polynomial(answer[tuple(full)], coefficient)
    return {word: Counter(value) for word, value in answer.items()}


def build_q(
    mask: int, pair: tuple[int, int] = PRIMARY_PAIR,
) -> tuple[Cell, ...]:
    base = tuple(Cell(*cell) for cell in BASE_Q)
    block = tuple(
        Cell(*cell, parameter_name(cell)) for cell in selected_cells(mask, pair)
    )
    return base + block


def gram_forms(
    q3: dict[Word, ParamPolynomial],
) -> dict[Word, dict[GramEntry, ParamPolynomial]]:
    """Expand the abstract symmetric rank-two Gram form (p*s)*q^[3]."""
    answer: defaultdict[Word, dict[GramEntry, Counter[ParamMonomial]]] = (
        defaultdict(lambda: defaultdict(Counter))
    )
    for word, coefficient in q3.items():
        missing = tuple(index for index, colour in enumerate(word) if colour == EMPTY)
        assert len(missing) == 2
        left, right = missing
        for left_colour, right_colour in product(COLOURS, repeat=2):
            full = list(word)
            full[left] = left_colour
            full[right] = right_colour
            entry = ((left, left_colour), (right, right_colour))
            add_polynomial(answer[tuple(full)][entry], coefficient)
    return {
        word: {entry: Counter(poly) for entry, poly in entries.items()}
        for word, entries in answer.items()
    }


def pure_words() -> set[Word]:
    return {(colour,) * SITE_COUNT for colour in COLOURS}


def beta_expression(entry: GramEntry) -> str:
    (left_site, left_colour), (right_site, right_colour) = entry
    return (
        f"(p{left_site}{left_colour}*s{right_site}{right_colour}"
        f"+s{left_site}{left_colour}*p{right_site}{right_colour})"
    )


def format_parameter_monomial(monomial: ParamMonomial) -> str:
    return "*".join(monomial) if monomial else "1"


def exact_coordinate_system(
    mask: int,
    pair: tuple[int, int] = PRIMARY_PAIR,
    *,
    saturate_active: bool = False,
) -> tuple[list[str], list[str]]:
    q = build_q(mask, pair)
    q3 = matching_divided_power(q, 3)
    q4 = matching_divided_power(q, 4)
    forms = gram_forms(q3)
    targets = pure_words()
    words = sorted(set(forms) | set(q4) | targets)
    equations: list[str] = []
    for word in words:
        terms: list[str] = []
        for entry, polynomial in sorted(forms.get(word, {}).items()):
            beta = beta_expression(entry)
            for monomial, coefficient in sorted(polynomial.items()):
                factor = format_parameter_monomial(monomial)
                terms.append(f"{4 * coefficient}*{factor}*{beta}")
        for monomial, coefficient in sorted(q4.get(word, {}).items()):
            factor = format_parameter_monomial(monomial)
            terms.append(f"{4 * coefficient}*a*{factor}")
        if word in targets:
            terms.append("-1")
        if terms:
            equations.append("+".join(terms))

    parameters = [parameter_name(cell) for cell in selected_cells(mask, pair)]
    if saturate_active:
        assert parameters
        equations.append("u*" + "*".join(parameters) + "-1")
    pair_cap_variables = [
        f"{prefix}{site}{colour}"
        for prefix in ("p", "s")
        for site in range(SITE_COUNT)
        for colour in COLOURS
    ]
    variables = pair_cap_variables + ["a"] + parameters
    if saturate_active:
        variables.append("u")
    assert len(pair_cap_variables) == 48
    return equations, variables


def singular_program(
    mask: int,
    pair: tuple[int, int] = PRIMARY_PAIR,
    *,
    saturate_active: bool = False,
) -> tuple[str, int, int, str]:
    equations, variables = exact_coordinate_system(
        mask, pair, saturate_active=saturate_active
    )
    program = (
        f"ring r=0,({','.join(variables)}),dp;\n"
        f"ideal I={','.join(equations)};\n"
        "option(redSB);\n"
        "ideal G=std(I);\n"
        'print("PAIR");\n'
        f'print("{pair[0]}{pair[1]}");\n'
        'print("MASK");\n'
        f"print({mask});\n"
        'print("BASIS_SIZE");\nprint(size(G));\n'
        'print("BASIS_FIRST");\nprint(G[1]);\n'
    )
    digest = hashlib.sha256(program.encode("utf-8")).hexdigest()
    return program, len(equations), len(variables), digest


def singular_path() -> str:
    executable = shutil.which("Singular")
    if executable is None:
        raise SystemExit("Singular is required for the exact QQ ideal audit")
    return executable


def run_unit_job(
    mask: int,
    timeout: int,
    pair: tuple[int, int] = PRIMARY_PAIR,
    *,
    saturate_active: bool = False,
) -> tuple[tuple[int, int], int, int, int, str, float]:
    program, equation_count, variable_count, digest = singular_program(
        mask, pair, saturate_active=saturate_active
    )
    started = time.monotonic()
    result = subprocess.run(
        [singular_path(), "-q"],
        input=program,
        text=True,
        capture_output=True,
        check=True,
        timeout=timeout,
    )
    elapsed = time.monotonic() - started
    if result.stderr.strip():
        raise AssertionError(f"pair {pair}, mask {mask}: Singular stderr:\n{result.stderr}")
    lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    try:
        pair_value = lines[lines.index("PAIR") + 1]
        mask_value = lines[lines.index("MASK") + 1]
        basis_size = lines[lines.index("BASIS_SIZE") + 1]
        basis_first = lines[lines.index("BASIS_FIRST") + 1]
    except (ValueError, IndexError) as error:
        raise AssertionError(
            f"pair {pair}, mask {mask}: malformed Singular output:\n{result.stdout}"
        ) from error
    assert pair_value == f"{pair[0]}{pair[1]}", (pair, result.stdout)
    assert mask_value == str(mask), (mask, result.stdout)
    assert basis_size == "1" and basis_first == "1", (mask, result.stdout)
    return pair, mask, equation_count, variable_count, digest, elapsed


def term_occurrences(
    entries: dict[GramEntry, ParamPolynomial],
) -> tuple[GramEntry, ...]:
    occurrences: list[GramEntry] = []
    for entry, polynomial in entries.items():
        for monomial, coefficient in polynomial.items():
            assert coefficient > 0
            # A positive integer multiple of an invertible parameter
            # monomial is nonzero in characteristic zero.
            occurrences.append(entry)
    return tuple(occurrences)


def orthogonality_contradiction(
    nonzero_edges: tuple[GramEntry, ...],
    zero_edges: set[GramEntry],
) -> bool:
    """Sound projective closure for a nondegenerate symmetric 2-space."""
    vertices = {vertex for edge in nonzero_edges for vertex in edge}
    parent = {vertex: vertex for vertex in vertices}

    def find(vertex: Mode) -> Mode:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    def union(left: Mode, right: Mode) -> bool:
        left_root, right_root = find(left), find(right)
        if left_root == right_root:
            return False
        if right_root < left_root:
            left_root, right_root = right_root, left_root
        parent[right_root] = left_root
        return True

    relevant = {
        edge for edge in zero_edges if edge[0] in vertices and edge[1] in vertices
    }
    while True:
        neighbours: defaultdict[Mode, set[Mode]] = defaultdict(set)
        isotropic: set[Mode] = set()
        for left, right in relevant:
            left_root, right_root = find(left), find(right)
            if left_root == right_root:
                isotropic.add(left_root)
            else:
                neighbours[left_root].add(right_root)
                neighbours[right_root].add(left_root)
        requested: list[tuple[Mode, Mode]] = []
        for values in neighbours.values():
            ordered = sorted(values)
            requested.extend((ordered[0], value) for value in ordered[1:])
        for root in isotropic:
            requested.extend((root, value) for value in neighbours.get(root, ()))
        if not any(union(left, right) for left, right in requested):
            break

    def class_pair(edge: GramEntry) -> frozenset[Mode]:
        return frozenset((find(edge[0]), find(edge[1])))

    return bool(
        {class_pair(edge) for edge in relevant}
        & {class_pair(edge) for edge in nonzero_edges}
    )


def support_certificate(mask: int) -> tuple[bool, int, int]:
    q = build_q(mask)
    q3 = matching_divided_power(q, 3)
    q4 = matching_divided_power(q, 4)
    forms = gram_forms(q3)
    targets = pure_words()

    zero_edges: set[GramEntry] = set()
    for word, entries in forms.items():
        if word in targets or word in q4:
            continue
        occurrences = term_occurrences(entries)
        if len(occurrences) == 1:
            zero_edges.add(occurrences[0])

    pure_options: list[tuple[GramEntry, ...]] = []
    for word in sorted(targets):
        if word in q4:
            return False, 0, len(zero_edges)
        options = term_occurrences(forms.get(word, {}))
        if not options:
            return False, 0, len(zero_edges)
        pure_options.append(options)

    branches = 0
    for choice in product(*pure_options):
        branches += 1
        if not orthogonality_contradiction(choice, zero_edges):
            return False, branches, len(zero_edges)
    return True, branches, len(zero_edges)


def classify_supports() -> tuple[list[int], str]:
    closed: list[int] = []
    opened: list[int] = []
    branch_histogram: Counter[int] = Counter()
    zero_histogram: Counter[int] = Counter()
    rows: list[str] = []
    for mask in range(1 << 9):
        closes, branches, zero_count = support_certificate(mask)
        (closed if closes else opened).append(mask)
        branch_histogram[branches] += 1
        zero_histogram[zero_count] += 1
        rows.append(
            f"{mask:03d}|{support_label(mask)}|{'closed' if closes else 'open'}"
            f"|{branches}|{zero_count}"
        )
    minimal = tuple(
        mask for mask in opened
        if not any(other != mask and (other & mask) == other for other in opened)
    )
    assert len(closed) == 432
    assert len(opened) == EXPECTED_OPEN_COUNT
    assert minimal == EXPECTED_MINIMAL_OPEN
    digest = hashlib.sha256(("\n".join(rows) + "\n").encode("utf-8")).hexdigest()
    print("pair-17 collected support classification: 432 closed + 80 open: PASS")
    print("minimal exact-ideal masks:", ",".join(map(str, minimal)))
    print("support branch histogram:", dict(sorted(branch_histogram.items())))
    print("support zero-edge histogram:", dict(sorted(zero_histogram.items())))
    print("support ledger SHA-256:", digest)
    return opened, digest


def verify_polarized_identity(pair: tuple[int, int]) -> None:
    # Full symbolic support includes every specialization of the block.
    q3 = matching_divided_power(build_q(511, pair), 3)
    product_poly = multiply_by_literal_cells(q3, Z_CELLS)
    expected = {
        (colour,) * SITE_COUNT: Counter({(): 1}) for colour in COLOURS
    }
    assert product_poly == expected
    q4 = matching_divided_power(build_q(511, pair), 4)
    assert all(len(monomial) <= 1 for poly in q4.values() for monomial in poly)
    print(
        f"pair {pair}: z*(q+E)^[3] = Delta symbolically "
        f"({len(q3)} q^[3] and {len(q4)} q^[4] coordinates): PASS"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--workers",
        type=int,
        default=int(os.environ.get("KRENN_SINGULAR_WORKERS", "3")),
        help="number of parallel Singular processes (default: 3)",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=900,
        help="per-mask Singular timeout in seconds (default: 900)",
    )
    parser.add_argument(
        "--pair17-only",
        action="store_true",
        help="run only the primary physical pair (1,7)",
    )
    parser.add_argument(
        "--pair",
        action="append",
        help="run only this invisible pair, written uv (repeatable)",
    )
    parser.add_argument(
        "--support-census",
        action="store_true",
        help="also replay the earlier 512-mask support classification for pair 17",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    assert args.workers >= 1 and args.timeout >= 1
    if args.pair:
        assert not args.pair17_only
        assert all(len(value) == 2 for value in args.pair)
        parsed_pairs = tuple((int(value[0]), int(value[1])) for value in args.pair)
        assert all(pair in INVISIBLE_PAIRS for pair in parsed_pairs)
        pairs = tuple(dict.fromkeys(parsed_pairs))
    else:
        pairs = (PRIMARY_PAIR,) if args.pair17_only else INVISIBLE_PAIRS
    for pair in pairs:
        verify_polarized_identity(pair)
    support_digest = None
    if args.support_census:
        support_digest = classify_supports()[1]

    # The full mask means that all nine coefficient variables occur in the
    # ring.  They are deliberately *not* inverted: [1] for this affine ideal
    # proves every support stratum and every exceptional ratio at once.
    mask = 511
    workers = min(args.workers, len(pairs))
    completed: dict[tuple[int, int], tuple[int, int, str, float]] = {}
    started = time.monotonic()
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(
                run_unit_job, mask, args.timeout, pair, saturate_active=False
            ): pair
            for pair in pairs
        }
        for number, future in enumerate(as_completed(futures), start=1):
            pair, returned_mask, equations, variables, digest, elapsed = future.result()
            assert returned_mask == mask
            completed[pair] = (equations, variables, digest, elapsed)
            print(
                f"unrestricted QQ ideals completed: {number}/{len(pairs)} "
                f"(latest pair {pair}, {elapsed:.3f}s)",
                flush=True,
            )

    assert sorted(completed) == sorted(pairs)
    equation_histogram = Counter(value[0] for value in completed.values())
    variable_histogram = Counter(value[1] for value in completed.values())
    ledger_rows = [
        f"{pair[0]}{pair[1]}|full-3x3|{completed[pair][0]}"
        f"|{completed[pair][1]}|{completed[pair][2]}|unit"
        for pair in sorted(pairs)
    ]
    exact_digest = hashlib.sha256(
        ("\n".join(ledger_rows) + "\n").encode("utf-8")
    ).hexdigest()
    print("unrestricted equation-count histogram:", dict(sorted(equation_histogram.items())))
    print("unrestricted variable-count histogram:", dict(sorted(variable_histogram.items())))
    print("unrestricted job ledger SHA-256:", exact_digest)
    if support_digest is not None:
        print("pair-17 support ledger SHA-256 (repeated):", support_digest)
    print(f"wall seconds: {time.monotonic() - started:.3f}")
    if pairs == INVISIBLE_PAIRS:
        assert len(pairs) == 11
        print("11/11 unrestricted characteristic-zero ideals reduce to [1]: PASS")
        print("arbitrary full block on every invisible physical pair is excluded: PASS")
    elif pairs == (PRIMARY_PAIR,):
        print("unrestricted full pair-17 block ideal reduces to [1]: PASS")
    else:
        print(f"selected unrestricted full-block ideals {len(pairs)}/{len(INVISIBLE_PAIRS)}: PASS")


if __name__ == "__main__":
    main()
