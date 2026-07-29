#!/usr/bin/env python3
"""Clean-room audit of the two-invisible-cell polarized pair-cap frontier.

The script reconstructs the displayed eight-site q and z from literal cell
lists.  It does not import any exploration or primary verification module.
It proves, by exhaustive endpoint-colour enumeration, that exactly 3960
unordered pairs of the 99 individually invisible cells preserve

    z * (q + t*e + u*f)^[3] = Delta_(8,3)

for nonzero t and u.  Safe monomial Gram coordinates and the exact
two-dimensional projective orthogonality rule exclude 3944 pairs.  For the
remaining 16 pairs, full coordinate ideals over QQ, localized by t*u, have
reduced Groebner basis [1].

The Singular replay deliberately uses a variable order different from the
discovery calculation: parameters come first, and site-mode variables are
reverse-site, reverse-colour, and s/p interleaved.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict, deque
from concurrent.futures import ThreadPoolExecutor, as_completed
from fractions import Fraction
import hashlib
from itertools import combinations, product
import shutil
import subprocess
import time


SITES = tuple(range(8))
COLOURS = tuple(range(3))
PHYSICAL_EDGES = tuple(combinations(SITES, 2))
ALL_CELLS = tuple(
    (left, right, left_colour, right_colour)
    for left, right in PHYSICAL_EDGES
    for left_colour, right_colour in product(COLOURS, repeat=2)
)

# Each cell records the colour at its smaller endpoint first.
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
DISPLAYED_Z = (
    (0, 1, 0, 0),
    (2, 4, 1, 1),
    (3, 7, 2, 2),
)
PURE_WORDS = tuple((colour,) * 8 for colour in COLOURS)
TARGET_WORDS = frozenset(PURE_WORDS)
EXPECTED_INVISIBLE_PHYSICAL_EDGES = (
    (0, 3), (0, 4), (0, 5), (0, 6), (0, 7),
    (1, 2), (1, 3), (1, 5), (1, 7), (2, 5), (3, 4),
)

EXPECTED_SURVIVORS = (
    ((0, 3, 0, 0), (1, 2, 0, 0)),
    ((0, 3, 0, 1), (1, 3, 0, 1)),
    ((0, 3, 1, 2), (0, 7, 1, 2)),
    ((0, 4, 0, 0), (1, 5, 0, 0)),
    ((0, 4, 1, 1), (2, 5, 1, 0)),
    ((0, 4, 2, 1), (2, 5, 1, 1)),
    ((0, 5, 0, 1), (1, 5, 0, 1)),
    ((0, 5, 0, 2), (1, 5, 0, 0)),
    ((0, 6, 0, 0), (1, 7, 0, 0)),
    ((0, 6, 0, 2), (1, 5, 0, 0)),
    ((0, 7, 0, 1), (1, 7, 0, 1)),
    ((1, 2, 1, 1), (3, 4, 0, 1)),
    ((1, 2, 2, 1), (3, 4, 1, 1)),
    ((1, 3, 1, 2), (1, 7, 1, 2)),
    ((1, 5, 0, 0), (1, 7, 2, 2)),
    ((1, 7, 2, 2), (3, 4, 2, 2)),
)
EXPECTED_EQUATION_COUNTS = {
    ((0, 3, 0, 0), (1, 2, 0, 0)): 248,
    ((0, 3, 0, 1), (1, 3, 0, 1)): 232,
    ((0, 3, 1, 2), (0, 7, 1, 2)): 238,
    ((0, 4, 0, 0), (1, 5, 0, 0)): 242,
    ((0, 4, 1, 1), (2, 5, 1, 0)): 232,
    ((0, 4, 2, 1), (2, 5, 1, 1)): 244,
    ((0, 5, 0, 1), (1, 5, 0, 1)): 214,
    ((0, 5, 0, 2), (1, 5, 0, 0)): 214,
    ((0, 6, 0, 0), (1, 7, 0, 0)): 254,
    ((0, 6, 0, 2), (1, 5, 0, 0)): 220,
    ((0, 7, 0, 1), (1, 7, 0, 1)): 250,
    ((1, 2, 1, 1), (3, 4, 0, 1)): 247,
    ((1, 2, 2, 1), (3, 4, 1, 1)): 262,
    ((1, 3, 1, 2), (1, 7, 1, 2)): 241,
    ((1, 5, 0, 0), (1, 7, 2, 2)): 226,
    ((1, 7, 2, 2), (3, 4, 2, 2)): 269,
}

# Filled from the clean-room canonical ledgers below.  These are deliberately
# not shared with any discovery module.
EXPECTED_COMPATIBLE_SHA256 = (
    "e10f1c380c47a6d0990c734b94c95dbc122c97863cc28d25972957d9f24faf3c"
)
EXPECTED_CLASSIFICATION_SHA256 = (
    "f93db512df4c43f054d4a49cb4f16efb459416dc0265f07aab87acf27fe1e1f5"
)
EXPECTED_CANCELLATION_SHA256 = (
    "f4fe508e4b81010d52c472f8196addff297c9c5c6cf68c93942e6360a5997948"
)
EXPECTED_IDEAL_INPUT_SHA256 = (
    "5cf3203fb376cfe14fc553dad5f9c975438a94979201fe878f6b8754a1d6ecb7"
)

Mode = tuple[int, int]
Cell = tuple[int, int, int, int]
GramEdge = tuple[Mode, Mode]
Tag = tuple[int, int]
Pair = tuple[Cell, Cell]

ONE: Tag = (0, 0)
T: Tag = (1, 0)
U: Tag = (0, 1)
TU: Tag = (1, 1)


def cell_sites(cell: Cell) -> tuple[int, int]:
    return cell[0], cell[1]


def cells_are_disjoint(cells: tuple[Cell, ...]) -> bool:
    endpoints = tuple(site for cell in cells for site in cell_sites(cell))
    return len(endpoints) == len(set(endpoints))


def partial_word(cells: tuple[Cell, ...]) -> tuple[int, ...]:
    word = [-1] * len(SITES)
    for left, right, left_colour, right_colour in cells:
        assert left < right
        assert word[left] == word[right] == -1
        word[left] = left_colour
        word[right] = right_colour
    return tuple(word)


def normalized_gram_edge(left: Mode, right: Mode) -> GramEdge:
    assert left[0] != right[0]
    return tuple(sorted((left, right)))


def base_polarized_expansion() -> Counter[tuple[int, ...]]:
    result: Counter[tuple[int, ...]] = Counter()
    for z_cell in DISPLAYED_Z:
        for triple in combinations(BASE_Q, 3):
            chosen = (z_cell,) + triple
            if cells_are_disjoint(chosen):
                word = partial_word(chosen)
                assert -1 not in word
                result[word] += 1
    return result


def single_debt(extra: Cell) -> Counter[tuple[int, ...]]:
    """The exact coefficient of t in z*(q+t*extra)^[3]."""
    result: Counter[tuple[int, ...]] = Counter()
    for z_cell in DISPLAYED_Z:
        for base_pair in combinations(BASE_Q, 2):
            chosen = (z_cell, extra) + base_pair
            if cells_are_disjoint(chosen):
                word = partial_word(chosen)
                assert -1 not in word
                result[word] += 1
    return result


def mixed_debt(left: Cell, right: Cell) -> Counter[tuple[int, ...]]:
    """The exact coefficient of t*u in z*(q+t*left+u*right)^[3]."""
    result: Counter[tuple[int, ...]] = Counter()
    for z_cell in DISPLAYED_Z:
        for base_cell in BASE_Q:
            chosen = (z_cell, left, right, base_cell)
            if cells_are_disjoint(chosen):
                word = partial_word(chosen)
                assert -1 not in word
                result[word] += 1
    return result


def tagged_q_cells(left: Cell, right: Cell) -> tuple[tuple[Cell, Tag], ...]:
    assert left != right
    assert left not in BASE_Q and right not in BASE_Q
    return (
        tuple((cell, ONE) for cell in BASE_Q)
        + ((left, T), (right, U))
    )


def join_tags(tags: tuple[Tag, ...]) -> Tag:
    result = (
        sum(tag[0] for tag in tags),
        sum(tag[1] for tag in tags),
    )
    assert result in (ONE, T, U, TU)
    return result


def merge_partial_words(
    first: tuple[int, ...], second: tuple[int, ...]
) -> tuple[int, ...] | None:
    result = []
    for first_colour, second_colour in zip(first, second):
        if first_colour != -1 and second_colour != -1:
            return None
        result.append(
            second_colour if first_colour == -1 else first_colour
        )
    return tuple(result)


def divided_power_support(
    weighted: tuple[tuple[Cell, Tag], ...], exponent: int
) -> Counter[tuple[tuple[int, ...], Tag]]:
    """A second construction of q^[exponent], before Gram filling."""
    result: Counter[tuple[tuple[int, ...], Tag]] = Counter()
    for chosen in combinations(weighted, exponent):
        cells = tuple(item[0] for item in chosen)
        if not cells_are_disjoint(cells):
            continue
        result[partial_word(cells), join_tags(tuple(item[1] for item in chosen))] += 1
    return result


def coordinate_forms(
    left: Cell, right: Cell
) -> tuple[
    dict[tuple[int, ...], Counter[tuple[GramEdge, Tag]]],
    dict[tuple[int, ...], Counter[Tag]],
]:
    """Reconstruct ps*q_tu^[3] and q_tu^[4] as tagged incidences."""
    weighted = tagged_q_cells(left, right)
    gram_forms: defaultdict[
        tuple[int, ...], Counter[tuple[GramEdge, Tag]]
    ] = defaultdict(Counter)

    for chosen in combinations(weighted, 3):
        cells = tuple(item[0] for item in chosen)
        if not cells_are_disjoint(cells):
            continue
        tag = join_tags(tuple(item[1] for item in chosen))
        six_word = partial_word(cells)
        missing = tuple(
            site for site, colour in enumerate(six_word) if colour == -1
        )
        assert len(missing) == 2 and missing[0] < missing[1]
        for first_colour, second_colour in product(COLOURS, repeat=2):
            top_word = list(six_word)
            top_word[missing[0]] = first_colour
            top_word[missing[1]] = second_colour
            edge = normalized_gram_edge(
                (missing[0], first_colour),
                (missing[1], second_colour),
            )
            gram_forms[tuple(top_word)][edge, tag] += 1

    direct_forms: defaultdict[tuple[int, ...], Counter[Tag]] = defaultdict(Counter)
    for chosen in combinations(weighted, 4):
        cells = tuple(item[0] for item in chosen)
        if not cells_are_disjoint(cells):
            continue
        tag = join_tags(tuple(item[1] for item in chosen))
        top_word = partial_word(cells)
        assert -1 not in top_word
        direct_forms[top_word][tag] += 1

    return dict(gram_forms), dict(direct_forms)


def audit_power_and_coordinate_forms(left: Cell, right: Cell) -> None:
    """Cross-check Gram filling, direct q^[4], and q*q^[3]=4q^[4]."""
    weighted = tagged_q_cells(left, right)
    q_three = divided_power_support(weighted, 3)
    q_four = divided_power_support(weighted, 4)
    gram_forms, direct_forms = coordinate_forms(left, right)

    reconstructed_gram: defaultdict[
        tuple[int, ...], Counter[tuple[GramEdge, Tag]]
    ] = defaultdict(Counter)
    for (six_word, tag), multiplicity in q_three.items():
        missing = tuple(
            site for site, colour in enumerate(six_word) if colour == -1
        )
        assert len(missing) == 2
        for first_colour, second_colour in product(COLOURS, repeat=2):
            top_word = list(six_word)
            top_word[missing[0]] = first_colour
            top_word[missing[1]] = second_colour
            edge = normalized_gram_edge(
                (missing[0], first_colour),
                (missing[1], second_colour),
            )
            reconstructed_gram[tuple(top_word)][edge, tag] += multiplicity
    assert {
        word: form for word, form in reconstructed_gram.items()
    } == gram_forms

    reconstructed_direct: defaultdict[tuple[int, ...], Counter[Tag]] = defaultdict(Counter)
    for (word, tag), multiplicity in q_four.items():
        assert -1 not in word
        reconstructed_direct[word][tag] += multiplicity
    assert {
        word: form for word, form in reconstructed_direct.items()
    } == direct_forms

    ordinary_product: Counter[tuple[tuple[int, ...], Tag]] = Counter()
    for cell, cell_tag in weighted:
        cell_word = partial_word((cell,))
        for (six_word, triple_tag), multiplicity in q_three.items():
            top_word = merge_partial_words(cell_word, six_word)
            if top_word is None:
                continue
            ordinary_product[top_word, join_tags((cell_tag, triple_tag))] += multiplicity
    assert ordinary_product == Counter({
        key: 4 * multiplicity for key, multiplicity in q_four.items()
    })


def safe_singleton_zeros(
    gram_forms: dict[tuple[int, ...], Counter[tuple[GramEdge, Tag]]],
    direct_forms: dict[tuple[int, ...], Counter[Tag]],
) -> frozenset[GramEdge]:
    """Only infer from one nonzero monomial times one Gram coordinate."""
    result = set()
    for word, form in gram_forms.items():
        if word in TARGET_WORDS or direct_forms.get(word) or len(form) != 1:
            continue
        (edge, tag), multiplicity = next(iter(form.items()))
        assert tag in (ONE, T, U, TU)
        assert multiplicity > 0
        result.add(edge)
    return frozenset(result)


def pure_nonzero_options(
    gram_forms: dict[tuple[int, ...], Counter[tuple[GramEdge, Tag]]],
    direct_forms: dict[tuple[int, ...], Counter[Tag]],
) -> tuple[tuple[GramEdge, ...], ...] | None:
    """Return exhaustive possible nonzero Gram entries for each pure word."""
    options = []
    for word in PURE_WORDS:
        if direct_forms.get(word):
            return None
        edges = tuple(sorted({edge for edge, _tag in gram_forms.get(word, {})}))
        if not edges:
            return None
        options.append(edges)
    return tuple(options)


def graph_contradiction(
    required_nonzero: tuple[GramEdge, ...],
    zero_edges: frozenset[GramEdge],
) -> tuple[str, tuple[Mode, ...]] | None:
    """Apply the exact projective-line parity criterion in dimension two."""
    known_nonzero_modes = frozenset(
        mode for edge in required_nonzero for mode in edge
    )
    adjacency = {mode: set() for mode in known_nonzero_modes}
    for first, second in zero_edges:
        if first in adjacency and second in adjacency:
            adjacency[first].add(second)
            adjacency[second].add(first)

    component = {}
    parity = {}
    nonbipartite = {}
    component_vertices = {}
    for root in sorted(known_nonzero_modes):
        if root in component:
            continue
        component_id = len(component_vertices)
        component[root] = component_id
        parity[root] = 0
        queue = deque([root])
        vertices = []
        odd = False
        while queue:
            current = queue.popleft()
            vertices.append(current)
            for neighbour in sorted(adjacency[current]):
                if neighbour not in component:
                    component[neighbour] = component_id
                    parity[neighbour] = parity[current] ^ 1
                    queue.append(neighbour)
                else:
                    assert component[neighbour] == component_id
                    if parity[neighbour] == parity[current]:
                        odd = True
        component_vertices[component_id] = tuple(sorted(vertices))
        nonbipartite[component_id] = odd

    for first, second in required_nonzero:
        if component[first] != component[second]:
            continue
        component_id = component[first]
        if nonbipartite[component_id]:
            return "isotropic_component", component_vertices[component_id]
        if parity[first] != parity[second]:
            return "odd_zero_path", component_vertices[component_id]
    return None


def classify_pair(
    left: Cell, right: Cell
) -> tuple[bool, int, str, tuple]:
    gram_forms, direct_forms = coordinate_forms(left, right)
    zeros = safe_singleton_zeros(gram_forms, direct_forms)
    options = pure_nonzero_options(gram_forms, direct_forms)
    if options is None:
        return False, 0, "pure_direct", ()

    branch_records = []
    checked = 0
    for required in product(*options):
        checked += 1
        certificate = graph_contradiction(required, zeros)
        branch_records.append((required, certificate))
        if certificate is None:
            return False, checked, "open_branch", tuple(branch_records)
    return True, checked, "closed", tuple(branch_records)


def sha256_records(records) -> str:
    digest = hashlib.sha256()
    for record in records:
        digest.update(repr(record).encode("utf-8"))
        digest.update(b"\n")
    return digest.hexdigest()


def solve_localized_two_variable_system(
    integer_rows: tuple[tuple[int, int, int], ...]
) -> tuple[str, int | None, tuple[Fraction, Fraction] | None]:
    """Solve a*X+b*Y=c on the torus X*Y != 0, exactly over QQ.

    The coefficient and augmented ranks are unchanged after extending QQ to
    C.  In rank one, an affine rational line meets the two-dimensional torus
    over C exactly when it also has a rational torus point, constructed here.
    """
    rows = tuple(
        (Fraction(a), Fraction(b), Fraction(c))
        for a, b, c in integer_rows
        if a or b or c
    )
    if not rows:
        return "rank0_torus", 0, (Fraction(1), Fraction(1))
    if any(not a and not b and c for a, b, c in rows):
        return "inconsistent_constant", None, None

    coefficient_rows = tuple(row for row in rows if row[0] or row[1])
    if not coefficient_rows:
        return "rank0_torus", 0, (Fraction(1), Fraction(1))
    first_a, first_b, first_c = coefficient_rows[0]

    independent = next(
        (
            row for row in coefficient_rows[1:]
            if first_a * row[1] - row[0] * first_b
        ),
        None,
    )
    if independent is not None:
        second_a, second_b, second_c = independent
        determinant = first_a * second_b - second_a * first_b
        x_value = (
            first_c * second_b - second_c * first_b
        ) / determinant
        y_value = (
            first_a * second_c - second_a * first_c
        ) / determinant
        if any(
            a * x_value + b * y_value != c for a, b, c in rows
        ):
            return "inconsistent_rank2", None, None
        if not x_value or not y_value:
            return "rank2_outside_torus", 2, None
        return "rank2_torus", 2, (x_value, y_value)

    # All coefficient rows are proportional.  Test augmented consistency.
    if any(
        first_a * c != a * first_c
        or first_b * c != b * first_c
        for a, b, c in coefficient_rows[1:]
    ):
        return "inconsistent_rank1", None, None

    if not first_a:
        y_value = first_c / first_b
        if not y_value:
            return "rank1_forces_y_zero", 1, None
        return "rank1_torus", 1, (Fraction(1), y_value)
    if not first_b:
        x_value = first_c / first_a
        if not x_value:
            return "rank1_forces_x_zero", 1, None
        return "rank1_torus", 1, (x_value, Fraction(1))

    # At most one nonzero rational x makes y zero, so a tiny deterministic
    # search always finds a torus point.
    for integer in range(1, 4):
        x_value = Fraction(integer)
        y_value = (first_c - first_a * x_value) / first_b
        if y_value:
            assert all(
                a * x_value + b * y_value == c for a, b, c in rows
            )
            return "rank1_torus", 1, (x_value, y_value)
    raise AssertionError("three distinct nonzero x values all forced y=0")


def mode_variable(prefix: str, mode: Mode) -> str:
    return f"{prefix}{mode[0]}{mode[1]}"


def beta_expression(edge: GramEdge) -> str:
    left, right = edge
    return (
        f"({mode_variable('p', left)}*{mode_variable('s', right)}"
        f"+{mode_variable('s', left)}*{mode_variable('p', right)})"
    )


def tag_expression(tag: Tag) -> str:
    factors = ("t",) * tag[0] + ("u",) * tag[1]
    return "*".join(factors)


def product_expression(coefficient: int, factors: tuple[str, ...]) -> str:
    pieces = [str(coefficient)] if coefficient != 1 else []
    pieces.extend(factor for factor in factors if factor)
    return "*".join(pieces) if pieces else "1"


def reversed_interleaved_variables() -> tuple[str, ...]:
    coordinates = tuple(
        mode_variable(prefix, (site, colour))
        for site in reversed(SITES)
        for colour in reversed(COLOURS)
        for prefix in ("s", "p")
    )
    variables = ("rho", "u", "t", "a") + coordinates
    assert len(variables) == 52 and len(set(variables)) == 52
    return variables


def ideal_program(pair: Pair) -> tuple[str, tuple[str, ...]]:
    """Build the full localized QQ ideal in a deliberately changed order."""
    gram_forms, direct_forms = coordinate_forms(*pair)
    words = sorted(
        set(gram_forms) | set(direct_forms) | set(TARGET_WORDS),
        reverse=True,
    )
    equations = []
    for word in words:
        terms = []
        # Put the direct q^[4] contribution before the Gram contribution;
        # this is also the reverse of the discovery generator strategy.
        for tag, multiplicity in sorted(
            direct_forms.get(word, {}).items(), reverse=True
        ):
            terms.append(product_expression(
                4 * multiplicity, ("a", tag_expression(tag))
            ))
        for (edge, tag), multiplicity in sorted(
            gram_forms.get(word, {}).items(), reverse=True
        ):
            terms.append(product_expression(
                4 * multiplicity, (tag_expression(tag), beta_expression(edge))
            ))
        if word in TARGET_WORDS:
            terms.append("-1")
        if terms:
            equations.append("+".join(terms))
    equations.append("rho*t*u-1")

    variables = reversed_interleaved_variables()
    program = (
        f"ring r=0,({','.join(variables)}),dp;\n"
        f"ideal J={','.join(equations)};\n"
        "option(redSB);\n"
        "ideal G=std(J);\n"
        'print("BASIS_SIZE");\n'
        "print(size(G));\n"
        'print("BASIS_FIRST");\n'
        "print(G[1]);\n"
    )
    return program, tuple(equations)


def run_singular_job(
    singular: str, pair: Pair
) -> tuple[Pair, int, int, str, str, float]:
    program, equations = ideal_program(pair)
    start = time.monotonic()
    result = subprocess.run(
        [singular, "-q"],
        input=program,
        text=True,
        capture_output=True,
        check=True,
        timeout=600,
    )
    elapsed = time.monotonic() - start
    if result.stderr.strip():
        raise AssertionError(result.stderr)
    lines = tuple(
        line.strip() for line in result.stdout.splitlines() if line.strip()
    )
    size = lines[lines.index("BASIS_SIZE") + 1]
    first = lines[lines.index("BASIS_FIRST") + 1]
    return pair, len(equations), 52, size, first, elapsed


def exact_frontier():
    assert len(ALL_CELLS) == 28 * 9 == 252
    assert len(set(BASE_Q)) == 9 and len(set(DISPLAYED_Z)) == 3
    assert base_polarized_expansion() == Counter(
        {word: 1 for word in PURE_WORDS}
    )

    invisible = tuple(cell for cell in ALL_CELLS if not single_debt(cell))
    assert len(invisible) == 99
    assert not (set(invisible) & set(BASE_Q))
    invisible_physical_edges = tuple(sorted({cell_sites(cell) for cell in invisible}))
    assert invisible_physical_edges == EXPECTED_INVISIBLE_PHYSICAL_EDGES
    assert all(
        sum(cell_sites(cell) == edge for cell in invisible) == 9
        for edge in invisible_physical_edges
    )

    # Do not assume individual invisibility.  Scan every pair of distinct
    # cells outside supp(q), and solve the complete polarized-debt equation
    #
    #   t D_e + u D_f + t*u D_ef = 0.
    #
    # On t*u != 0 this is D_f X + D_e Y = -D_ef with X=1/t,
    # Y=1/u.  The following exact rank calculation therefore includes all
    # possible cancellation between individually visible debts.
    outside = tuple(cell for cell in ALL_CELLS if cell not in BASE_Q)
    assert len(outside) == 243
    individual_debts = {cell: single_debt(cell) for cell in outside}
    all_outside_pairs = tuple(combinations(outside, 2))
    assert len(all_outside_pairs) == 29403
    cancellation_records = []
    cancellation_solutions = []
    cancellation_status_histogram = Counter()
    visibility_status_histogram = Counter()
    for pair in all_outside_pairs:
        left, right = pair
        left_debt = individual_debts[left]
        right_debt = individual_debts[right]
        cross_debt = mixed_debt(left, right)
        words = tuple(sorted(set(left_debt) | set(right_debt) | set(cross_debt)))
        rows = tuple(
            (
                right_debt[word],
                left_debt[word],
                -cross_debt[word],
            )
            for word in words
        )
        status, rank, point = solve_localized_two_variable_system(rows)
        cancellation_status_histogram[status] += 1
        visibility = (bool(left_debt), bool(right_debt))
        visibility_status_histogram[status, visibility] += 1
        cancellation_records.append((pair, status, rank, point))
        if point is None:
            continue
        x_value, y_value = point
        assert x_value and y_value
        assert all(
            right_debt[word] * x_value
            + left_debt[word] * y_value
            + cross_debt[word] == 0
            for word in words
        )
        cancellation_solutions.append(pair)

    cancellation_solutions = tuple(cancellation_solutions)
    assert cancellation_status_histogram == Counter({
        "rank0_torus": 3960,
        "inconsistent_constant": 3573,
        "rank1_forces_x_zero": 11268,
        "rank1_forces_y_zero": 2421,
        "rank2_outside_torus": 8181,
    })
    assert len(cancellation_solutions) == 3960
    assert all(
        not individual_debts[left] and not individual_debts[right]
        for left, right in cancellation_solutions
    )

    all_pairs = tuple(combinations(invisible, 2))
    compatible = []
    incompatible = []
    mixed_debt_support_histogram = Counter()
    mixed_debt_multiplicity_histogram = Counter()
    for pair in all_pairs:
        debt = mixed_debt(*pair)
        if debt:
            incompatible.append(pair)
            mixed_debt_support_histogram[len(debt)] += 1
            mixed_debt_multiplicity_histogram.update(debt.values())
        else:
            compatible.append(pair)
    compatible = tuple(compatible)
    incompatible = tuple(incompatible)

    assert len(all_pairs) == 4851
    assert len(compatible) == 3960
    assert len(incompatible) == 891
    # Positivity makes this support test an iff on t*u != 0.
    assert all(
        coefficient > 0
        for pair in incompatible
        for coefficient in mixed_debt(*pair).values()
    )
    for pair in compatible:
        audit_power_and_coordinate_forms(*pair)

    overlap_histogram = Counter(
        len(set(cell_sites(left)) & set(cell_sites(right)))
        for left, right in compatible
    )
    same_pair_histogram = Counter(
        cell_sites(left) == cell_sites(right)
        for left, right in compatible
    )
    assert overlap_histogram == Counter({1: 2025, 0: 1539, 2: 396})
    assert same_pair_histogram == Counter({False: 3564, True: 396})
    # This equality is the exact exhaustion statement: every two-cell
    # deformation preserving the displayed z identity is individually
    # invisible and has zero mixed debt.
    assert cancellation_solutions == compatible

    classification_records = []
    branch_histogram = Counter()
    projectively_closed = []
    survivors = []
    reason_histogram = Counter()
    for pair in compatible:
        closed, branches, reason, records = classify_pair(*pair)
        branch_histogram[branches] += 1
        reason_histogram[closed, reason] += 1
        classification_records.append((pair, closed, branches, reason, records))
        if closed:
            projectively_closed.append(pair)
        else:
            survivors.append(pair)

    projectively_closed = tuple(projectively_closed)
    survivors = tuple(survivors)
    assert len(projectively_closed) == 3944
    assert survivors == EXPECTED_SURVIVORS
    assert branch_histogram == Counter({0: 4, 1: 2641, 2: 1171, 3: 50, 4: 94})
    assert reason_histogram == Counter({
        (True, "closed"): 3944,
        (False, "open_branch"): 12,
        (False, "pure_direct"): 4,
    })

    compatible_hash = sha256_records(compatible)
    classification_hash = sha256_records(classification_records)
    cancellation_hash = sha256_records(cancellation_records)
    if EXPECTED_COMPATIBLE_SHA256:
        assert compatible_hash == EXPECTED_COMPATIBLE_SHA256
    if EXPECTED_CLASSIFICATION_SHA256:
        assert classification_hash == EXPECTED_CLASSIFICATION_SHA256
    if EXPECTED_CANCELLATION_SHA256:
        assert cancellation_hash == EXPECTED_CANCELLATION_SHA256

    ideal_records = []
    for pair in survivors:
        program, equations = ideal_program(pair)
        assert len(equations) == EXPECTED_EQUATION_COUNTS[pair]
        ideal_records.append((pair, program))
    ideal_input_hash = sha256_records(ideal_records)
    if EXPECTED_IDEAL_INPUT_SHA256:
        assert ideal_input_hash == EXPECTED_IDEAL_INPUT_SHA256

    return {
        "invisible": invisible,
        "compatible": compatible,
        "incompatible": incompatible,
        "projectively_closed": projectively_closed,
        "survivors": survivors,
        "overlap_histogram": overlap_histogram,
        "same_pair_histogram": same_pair_histogram,
        "cancellation_status_histogram": cancellation_status_histogram,
        "visibility_status_histogram": visibility_status_histogram,
        "mixed_debt_support_histogram": mixed_debt_support_histogram,
        "mixed_debt_multiplicity_histogram": mixed_debt_multiplicity_histogram,
        "branch_histogram": branch_histogram,
        "reason_histogram": reason_histogram,
        "compatible_hash": compatible_hash,
        "classification_hash": classification_hash,
        "cancellation_hash": cancellation_hash,
        "ideal_input_hash": ideal_input_hash,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--support-only",
        action="store_true",
        help="skip the 16 redundant exact Singular ideal computations",
    )
    args = parser.parse_args()

    data = exact_frontier()
    print("independent two-invisible-cell frontier: PASS")
    print("252 endpoint-colour cells scanned; exactly 99 invisible: PASS")
    print("all unordered outside-support pairs:", 29403)
    print(
        "polarized-identity-preserving pairs / involving visible debt:",
        3960,
        "/",
        0,
    )
    print(
        "full cancellation status histogram:",
        dict(sorted(data["cancellation_status_histogram"].items())),
    )
    print("all unordered invisible pairs: 4851")
    print("cross-debt-free / nonzero-debt:", 3960, "/", 891)
    print("all 3960 q^[3], q^[4], Gram-fill, and Euler-form audits: PASS")
    print(
        "shared physical endpoints:",
        dict(sorted(data["overlap_histogram"].items())),
    )
    print(
        "same physical pair:",
        dict(sorted(data["same_pair_histogram"].items())),
    )
    print(
        "mixed-debt support histogram:",
        dict(sorted(data["mixed_debt_support_histogram"].items())),
    )
    print(
        "mixed-debt incidence-multiplicity histogram:",
        dict(sorted(data["mixed_debt_multiplicity_histogram"].items())),
    )
    print("projective singleton closure:", 3944, "/", 3960)
    print("branch histogram:", dict(sorted(data["branch_histogram"].items())))
    print("residual full-ideal cases:", len(data["survivors"]))
    print("compatible-pair SHA-256:", data["compatible_hash"])
    print("classification SHA-256:", data["classification_hash"])
    print("cancellation SHA-256:", data["cancellation_hash"])
    print("ideal-input SHA-256:", data["ideal_input_hash"])

    if args.support_only:
        print("Singular replay skipped by request")
        return

    singular = shutil.which("Singular")
    if singular is None:
        raise SystemExit("Singular is required for the full exact audit")

    started = time.monotonic()
    outputs = []
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = {
            pool.submit(run_singular_job, singular, pair): pair
            for pair in data["survivors"]
        }
        for future in as_completed(futures):
            outputs.append(future.result())

    for pair, equations, variables, size, first, elapsed in sorted(outputs):
        assert size == first == "1"
        print(
            pair,
            "basis",
            size,
            first,
            "equations",
            equations,
            "variables",
            variables,
            "seconds",
            f"{elapsed:.3f}",
        )
    assert len(outputs) == 16
    assert sum(item[1] for item in outputs) == 3833
    print("reverse-variable-order localized QQ unit ideals: 16 / 16")
    print("parallel wall seconds:", f"{time.monotonic() - started:.3f}")
    print(
        "all 3960 exactly-two-cell families exclude pair-cap preimages "
        "for every nonzero complex t,u: PASS"
    )


if __name__ == "__main__":
    main()
