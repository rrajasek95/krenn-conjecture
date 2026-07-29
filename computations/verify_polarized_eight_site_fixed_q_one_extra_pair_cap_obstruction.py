#!/usr/bin/env python3
"""Exact one-extra-cell audit around the sparse eight-site quadratic.

Among the 243 endpoint-colour cells outside the fixed nine-cell quadratic
q, this checker independently identifies the 99 cells e for which

    z * e * q^[2] = 0.

Thus z*(q+t*e)^[3] is unchanged for arbitrary t.  For every such e it then
checks that

    (a*(q+t*e) + 4*p*s) * (q+t*e)^[3] = Delta_(8,3)

has no characteristic-zero solution.  Sixty-six cases retain the original
seven-coordinate Gram contradiction literally.  For each of the remaining
33 cases a finite orthogonality-closure certificate gives a contradiction.
The optional ``--full-groebner`` audit also reduces every full coordinate
ideal, saturated by t, to [1] with Singular over QQ.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from fractions import Fraction
from itertools import combinations, product
from math import factorial
import os
import shutil
import subprocess


SITE_COUNT = 8
COLOURS = tuple(range(3))
EMPTY = -1
Monomial = tuple[int, ...]
Polynomial = dict[Monomial, Fraction]
Mode = tuple[int, int]
GramEntry = tuple[Mode, Mode]

# q is copied literally rather than imported from either earlier checker.
Q_CELLS = (
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

# The distinguished quadratic in the unrestricted polarized model.
Z_CELLS = (
    (0, 1, 0, 0),
    (2, 4, 1, 1),
    (3, 7, 2, 2),
)

SELECTED_NAMES = ("pure0", "pure1", "pure2", "AF", "BF", "AC", "CF")
SELECTED_WORDS = (
    (0,) * 8,
    (1,) * 8,
    (2,) * 8,
    (0, 2, 0, 0, 2, 2, 2, 2),
    (2, 0, 2, 1, 0, 0, 1, 2),
    (0, 2, 1, 1, 2, 1, 1, 1),
    (1, 1, 1, 1, 0, 0, 1, 2),
)

EXPECTED_SIGNATURE_COUNTS = Counter({
    (): 66,
    ("pure0",): 7,
    ("pure1",): 2,
    ("pure2",): 3,
    ("AF",): 3,
    ("BF",): 3,
    ("AC",): 5,
    ("CF",): 3,
    ("pure0", "AF"): 1,
    ("pure0", "BF"): 1,
    ("pure1", "AC"): 1,
    ("pure1", "CF"): 1,
    ("pure2", "AF"): 1,
    ("pure2", "BF"): 1,
    ("AF", "AC"): 1,
})


def cell_word(left: int, right: int, left_colour: int, right_colour: int) -> Monomial:
    assert 0 <= left < right < SITE_COUNT
    assert left_colour in COLOURS and right_colour in COLOURS
    result = [EMPTY] * SITE_COUNT
    result[left] = left_colour
    result[right] = right_colour
    return tuple(result)


def merge(left: Monomial, right: Monomial) -> Monomial | None:
    result = []
    for left_value, right_value in zip(left, right):
        if left_value != EMPTY and right_value != EMPTY:
            return None
        result.append(right_value if left_value == EMPTY else left_value)
    return tuple(result)


def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    result: defaultdict[Monomial, Fraction] = defaultdict(Fraction)
    for left_word, left_coefficient in left.items():
        for right_word, right_coefficient in right.items():
            word = merge(left_word, right_word)
            if word is not None:
                result[word] += left_coefficient * right_coefficient
    return {word: coefficient for word, coefficient in result.items() if coefficient}


def power(poly: Polynomial, exponent: int) -> Polynomial:
    result: Polynomial = {(EMPTY,) * SITE_COUNT: Fraction(1)}
    for _ in range(exponent):
        result = multiply(result, poly)
    return result


def divided_power(poly: Polynomial, exponent: int) -> Polynomial:
    divisor = factorial(exponent)
    return {word: coefficient / divisor for word, coefficient in power(poly, exponent).items()}


def literal_polynomial(cells: tuple[tuple[int, int, int, int], ...]) -> Polynomial:
    return {
        cell_word(left, right, left_colour, right_colour): Fraction(1)
        for left, right, left_colour, right_colour in cells
    }


def all_endpoint_cells() -> tuple[tuple[tuple[int, int, int, int], Monomial], ...]:
    return tuple(
        (
            (left, right, left_colour, right_colour),
            cell_word(left, right, left_colour, right_colour),
        )
        for left, right in combinations(range(SITE_COUNT), 2)
        for left_colour, right_colour in product(COLOURS, repeat=2)
    )


def pair_word(left: Mode, right: Mode) -> Monomial:
    assert left[0] < right[0]
    return cell_word(left[0], right[0], left[1], right[1])


def gram_coordinate_forms(poly: Polynomial) -> dict[Monomial, Counter[GramEntry]]:
    """Expand R*poly with an abstract off-site Gram entry R_XY."""
    result: defaultdict[Monomial, Counter[GramEntry]] = defaultdict(Counter)
    for left_site, right_site in combinations(range(SITE_COUNT), 2):
        for left_colour, right_colour in product(COLOURS, repeat=2):
            entry = ((left_site, left_colour), (right_site, right_colour))
            basis_word = pair_word(*entry)
            for word, coefficient in poly.items():
                full_word = merge(basis_word, word)
                if full_word is not None:
                    assert coefficient.denominator == 1
                    result[full_word][entry] += int(coefficient)
    return dict(result)


def singular_path() -> str:
    executable = shutil.which("Singular")
    if executable is None:
        raise SystemExit("Singular is required for the exact saturated-ideal audits")
    return executable


def mode_variable(prefix: str, mode: Mode) -> str:
    site, colour = mode
    return f"{prefix}{site}{colour}"


def beta_expression(entry: GramEntry) -> str:
    left, right = entry
    return (
        f"({mode_variable('p', left)}*{mode_variable('s', right)}"
        f"+{mode_variable('s', left)}*{mode_variable('p', right)})"
    )


def singular_ring_variables(include_parameter: bool) -> list[str]:
    variables = [
        mode_variable(prefix, (site, colour))
        for prefix in ("p", "s")
        for site in range(SITE_COUNT)
        for colour in COLOURS
    ]
    if include_parameter:
        variables.extend(("a", "t", "u"))
    return variables


def run_singular_unit(program: str, timeout: int = 300) -> None:
    result = subprocess.run(
        [singular_path(), "-q"],
        input=program,
        text=True,
        capture_output=True,
        check=True,
        timeout=timeout,
    )
    if result.stderr.strip():
        raise AssertionError(result.stderr)
    lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    size_index = lines.index("BASIS_SIZE")
    first_index = lines.index("BASIS_FIRST")
    assert lines[size_index + 1] == "1", result.stdout
    assert lines[first_index + 1] == "1", result.stdout


def fixed_seven_unit_audit() -> None:
    A, B = (0, 0), (1, 0)
    C, D = (2, 1), (4, 1)
    E, F = (3, 2), (7, 2)
    equations = (
        f"4*{beta_expression((A, B))}-1",
        f"4*{beta_expression((C, D))}-1",
        f"4*{beta_expression((E, F))}-1",
        beta_expression((A, F)),
        beta_expression((B, F)),
        beta_expression((A, C)),
        beta_expression((C, F)),
    )
    variables = singular_ring_variables(include_parameter=False)
    program = (
        f"ring r=0,({','.join(variables)}),dp;\n"
        f"ideal I={','.join(equations)};\n"
        "ideal G=std(I);\n"
        'print("BASIS_SIZE");\nprint(size(G));\n'
        'print("BASIS_FIRST");\nprint(G[1]);\n'
    )
    run_singular_unit(program)


def changed_signature(
    perturbation_forms: dict[Monomial, Counter[GramEntry]],
    q4_variation: Polynomial,
) -> tuple[str, ...]:
    return tuple(
        name
        for name, word in zip(SELECTED_NAMES, SELECTED_WORDS)
        if perturbation_forms.get(word) or q4_variation.get(word)
    )


def safe_singleton_zero_edges(
    old_forms: dict[Monomial, Counter[GramEntry]],
    perturbation_forms: dict[Monomial, Counter[GramEntry]],
    q4: Polynomial,
    q4_variation: Polynomial,
) -> set[GramEntry]:
    """Gram entries forced to zero by a t-uniform singleton coordinate.

    We use a non-target word with no direct a-term and one abstract Gram
    entry occurring on exactly one side (old or perturbation).  Its
    coefficient is therefore a nonzero integer or t times one, so t != 0
    forces the entry to vanish without an exceptional parameter value.
    """
    pure_words = {(colour,) * SITE_COUNT for colour in COLOURS}
    result: set[GramEntry] = set()
    for word in set(old_forms) | set(perturbation_forms):
        if word in pure_words or q4.get(word) or q4_variation.get(word):
            continue
        old = old_forms.get(word, Counter())
        perturbation = perturbation_forms.get(word, Counter())
        if bool(old) == bool(perturbation):
            # Either neither side occurs, or the coefficient can depend on
            # 1+t and hence may vanish at an exceptional nonzero t.
            continue
        only_side = old or perturbation
        if len(only_side) == 1:
            result.add(next(iter(only_side)))
    return result


def pure_contributors(
    word: Monomial,
    old_forms: dict[Monomial, Counter[GramEntry]],
    perturbation_forms: dict[Monomial, Counter[GramEntry]],
    q4: Polynomial,
    q4_variation: Polynomial,
) -> tuple[GramEntry, ...]:
    """List the distinct old/t contributors to a pure target word."""
    assert len(set(word)) == 1
    assert not q4.get(word) and not q4_variation.get(word)
    old = old_forms.get(word, Counter())
    perturbation = perturbation_forms.get(word, Counter())
    assert all(coefficient == 1 for coefficient in old.values())
    assert all(coefficient == 1 for coefficient in perturbation.values())
    contributors = tuple(old) + tuple(perturbation)
    assert len(contributors) == len(set(contributors))
    return contributors


def orthogonality_closure_contradiction(
    nonzero_edges: list[GramEntry],
    zero_edges: set[GramEntry],
) -> bool:
    """Close sound proportionality rules in a nondegenerate 2-space.

    Every endpoint of a nonzero Gram edge represents a nonzero vector.
    Two nonzero vectors orthogonal to one nonzero vector are proportional.
    If a proportionality class contains an orthogonal pair, its line is
    isotropic and equals its own orthogonal complement.  Iterating these
    rules is finite.  A zero and a nonzero pairing between the same two
    final classes is a contradiction.
    """
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
        parent[right_root] = left_root
        return True

    relevant_zeros = {
        edge for edge in zero_edges if edge[0] in vertices and edge[1] in vertices
    }
    while True:
        neighbours: defaultdict[Mode, set[Mode]] = defaultdict(set)
        isotropic_classes: set[Mode] = set()
        for left, right in relevant_zeros:
            left_root, right_root = find(left), find(right)
            if left_root == right_root:
                isotropic_classes.add(left_root)
            else:
                neighbours[left_root].add(right_root)
                neighbours[right_root].add(left_root)

        requested_unions: list[tuple[Mode, Mode]] = []
        for orthogonal_classes in neighbours.values():
            ordered = sorted(orthogonal_classes)
            requested_unions.extend(
                (ordered[0], other) for other in ordered[1:]
            )
        for isotropic_class in isotropic_classes:
            requested_unions.extend(
                (isotropic_class, other)
                for other in neighbours.get(isotropic_class, set())
            )

        changed = False
        for left, right in requested_unions:
            changed |= union(left, right)
        if not changed:
            break

    def class_pair(edge: GramEntry) -> frozenset[Mode]:
        return frozenset((find(edge[0]), find(edge[1])))

    zero_class_pairs = {class_pair(edge) for edge in relevant_zeros}
    nonzero_class_pairs = {class_pair(edge) for edge in nonzero_edges}
    return bool(zero_class_pairs & nonzero_class_pairs)


def full_saturated_program(
    old_forms: dict[Monomial, Counter[GramEntry]],
    perturbation_forms: dict[Monomial, Counter[GramEntry]],
    q4: Polynomial,
    q4_variation: Polynomial,
) -> tuple[str, int]:
    """Construct all top-coordinate equations plus u*t-1 over QQ."""
    delta_words = {(colour,) * SITE_COUNT for colour in COLOURS}
    words = sorted(
        set(old_forms)
        | set(perturbation_forms)
        | set(q4)
        | set(q4_variation)
        | delta_words
    )
    equations: list[str] = []
    for word in words:
        terms: list[str] = []
        for entry, coefficient in sorted(old_forms.get(word, {}).items()):
            terms.append(f"{4 * coefficient}*{beta_expression(entry)}")
        for entry, coefficient in sorted(perturbation_forms.get(word, {}).items()):
            terms.append(f"{4 * coefficient}*t*{beta_expression(entry)}")
        if word in q4:
            assert q4[word].denominator == 1
            terms.append(f"{4 * int(q4[word])}*a")
        if word in q4_variation:
            assert q4_variation[word].denominator == 1
            terms.append(f"{4 * int(q4_variation[word])}*a*t")
        if word in delta_words:
            terms.append("-1")
        if terms:
            equations.append("+".join(terms))

    # This Rabinowitsch equation restricts the affine scheme to t != 0.
    equations.append("u*t-1")
    variables = singular_ring_variables(include_parameter=True)
    program = (
        f"ring r=0,({','.join(variables)}),dp;\n"
        f"ideal I={','.join(equations)};\n"
        "ideal G=std(I);\n"
        'print("BASIS_SIZE");\nprint(size(G));\n'
        'print("BASIS_FIRST");\nprint(G[1]);\n'
    )
    return program, len(equations)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--full-groebner",
        action="store_true",
        help="also run all 33 full t-saturated Singular coordinate ideals",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    q = literal_polynomial(Q_CELLS)
    z = literal_polynomial(Z_CELLS)
    assert len(q) == 9 and len(z) == 3

    q2 = divided_power(q, 2)
    q3 = divided_power(q, 3)
    q4 = divided_power(q, 4)
    delta = {(colour,) * SITE_COUNT: Fraction(1) for colour in COLOURS}
    assert multiply(z, q3) == delta
    assert len(q3) == 19
    assert q4 == {
        tuple(map(int, "11000000")): Fraction(1),
        tuple(map(int, "22212111")): Fraction(1),
    }

    extras = tuple(
        (cell, word)
        for cell, word in all_endpoint_cells()
        if word not in q
    )
    assert len(extras) == 252 - 9 == 243

    invisible: list[tuple[tuple[int, int, int, int], Monomial]] = []
    visible: list[tuple[tuple[int, int, int, int], Monomial, Polynomial]] = []
    for cell, word in extras:
        variation = multiply(multiply(z, {word: Fraction(1)}), q2)
        if variation:
            visible.append((cell, word, variation))
        else:
            invisible.append((cell, word))

    assert len(invisible) == 99
    assert len(visible) == 144
    invisible_pair_counts = Counter((cell[0], cell[1]) for cell, _ in invisible)
    assert invisible_pair_counts == Counter({
        (0, 3): 9,
        (0, 4): 9,
        (0, 5): 9,
        (0, 6): 9,
        (0, 7): 9,
        (1, 2): 9,
        (1, 3): 9,
        (1, 5): 9,
        (1, 7): 9,
        (2, 5): 9,
        (3, 4): 9,
    })

    # Every visible perturbation creates one or two coefficient-one words
    # outside Delta.  Hence no cancellation with the old z*q^[3]=Delta is
    # possible when t is nonzero.
    visible_histogram = Counter()
    for _, _, variation in visible:
        debt = {word: coefficient for word, coefficient in variation.items() if word not in delta}
        assert debt == variation
        assert all(coefficient == 1 for coefficient in debt.values())
        visible_histogram[len(debt)] += 1
    assert visible_histogram == Counter({1: 135, 2: 9})

    old_forms = gram_coordinate_forms(q3)
    assert len(old_forms) == 165
    assert Counter(sum(form.values()) for form in old_forms.values()) == {1: 163, 4: 2}

    cases = []
    signature_counts = Counter()
    for cell, word in invisible:
        # Since a cell squares to zero,
        # (q+t*e)^[3] = q^[3] + t*e*q^[2] and
        # (q+t*e)^[4] = q^[4] + t*e*q^[3].
        q3_variation = multiply({word: Fraction(1)}, q2)
        q4_variation = multiply({word: Fraction(1)}, q3)
        perturbation_forms = gram_coordinate_forms(q3_variation)
        signature = changed_signature(perturbation_forms, q4_variation)
        signature_counts[signature] += 1
        cases.append((cell, perturbation_forms, q4_variation, signature))

    assert signature_counts == EXPECTED_SIGNATURE_COUNTS

    # Reconstruct the old seven-entry system, including the absence of the
    # direct a*q^[4] term.  Its finite orthogonality closure is the geometric
    # proof used by all 66 empty-signature cases.
    A, B = (0, 0), (1, 0)
    C, D = (2, 1), (4, 1)
    E, F = (3, 2), (7, 2)
    expected_selected = (
        (A, B),
        (C, D),
        (E, F),
        (A, F),
        (B, F),
        (A, C),
        (C, F),
    )
    for word, entry in zip(SELECTED_WORDS, expected_selected):
        assert old_forms[word] == Counter({entry: 1})
        assert not q4.get(word)
    assert orthogonality_closure_contradiction(
        list(expected_selected[:3]), set(expected_selected[3:])
    )

    changed_cases = [case for case in cases if case[3]]
    assert len(changed_cases) == 33

    # The remaining cases have exact, parameter-uniform support/Gram
    # certificates.  In a cross-colour direction all three pure target
    # words force nonzero pairings.  In a same-colour direction one pure
    # equation has two terms R0+t*R1=1/4, so at least one term is nonzero;
    # both branches close under the two-dimensional orthogonality rules.
    monochromatic_zero_counts = Counter()
    cross_colour_zero_counts = Counter()
    monochromatic_cases = 0
    cross_colour_cases = 0
    for cell, perturbation_forms, q4_variation, _ in changed_cases:
        zero_edges = safe_singleton_zero_edges(
            old_forms, perturbation_forms, q4, q4_variation
        )
        pure_edges = tuple(
            pure_contributors(
                word, old_forms, perturbation_forms, q4, q4_variation
            )
            for word in SELECTED_WORDS[:3]
        )
        if cell[2] != cell[3]:
            cross_colour_cases += 1
            cross_colour_zero_counts[len(zero_edges)] += 1
            assert all(len(contributors) == 1 for contributors in pure_edges)
            assert orthogonality_closure_contradiction(
                [contributors[0] for contributors in pure_edges], zero_edges
            )
        else:
            monochromatic_cases += 1
            monochromatic_zero_counts[len(zero_edges)] += 1
            lengths = [len(contributors) for contributors in pure_edges]
            assert sorted(lengths) == [1, 1, 2]
            altered = lengths.index(2)
            altered_word = SELECTED_WORDS[altered]
            assert len(old_forms[altered_word]) == 1
            assert len(perturbation_forms[altered_word]) == 1
            fixed_nonzero = [
                contributors[0]
                for index, contributors in enumerate(pure_edges)
                if index != altered
            ]
            for branch_edge in pure_edges[altered]:
                assert orthogonality_closure_contradiction(
                    fixed_nonzero + [branch_edge], zero_edges
                )

    assert monochromatic_cases == 18
    assert cross_colour_cases == 15
    assert monochromatic_zero_counts == Counter({
        151: 1,
        154: 1,
        157: 2,
        163: 1,
        164: 2,
        167: 3,
        172: 1,
        173: 2,
        180: 1,
        182: 2,
        183: 1,
        185: 1,
    })
    assert cross_colour_zero_counts == Counter({
        153: 2,
        156: 3,
        163: 1,
        165: 1,
        166: 1,
        169: 1,
        172: 1,
        177: 1,
        179: 1,
        181: 1,
        182: 1,
        194: 1,
    })

    if args.full_groebner:
        # Redundant exhaustive audit: construct every top-coordinate
        # equation, add u*t-1, and check the full ideal over QQ.
        fixed_seven_unit_audit()
        jobs = []
        for cell, perturbation_forms, q4_variation, _ in changed_cases:
            program, equation_count = full_saturated_program(
                old_forms, perturbation_forms, q4, q4_variation
            )
            jobs.append((cell, program, equation_count))

        requested_workers = int(os.environ.get("KRENN_SINGULAR_WORKERS", "3"))
        workers = max(1, min(requested_workers, len(jobs)))
        completed = {}
        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = {
                executor.submit(run_singular_unit, program): (cell, equation_count)
                for cell, program, equation_count in jobs
            }
            for future in as_completed(futures):
                cell, equation_count = futures[future]
                future.result()
                completed[cell] = equation_count

        assert len(completed) == 33
        equation_histogram = Counter(completed.values())
        assert equation_histogram == Counter({
            184: 3,
            190: 6,
            193: 2,
            196: 6,
            199: 3,
            202: 1,
            205: 1,
            208: 4,
            211: 4,
            214: 1,
            217: 2,
        })

    print("fixed-q one-extra-cell pair-cap obstruction: PASS")
    print("243 extras split into 99 z-invisible and 144 visible cells: PASS")
    print("11 invisible physical pairs, with all 9 endpoint-colour orders: PASS")
    print("visible debt histogram 135 one-word + 9 two-word cases: PASS")
    print("66 cases retain the seven-coordinate Gram contradiction: PASS")
    print("15 cross-colour singleton zero-graph closures: PASS")
    print("18 same-colour two-branch zero-graph closures: PASS")
    if args.full_groebner:
        print("33 full coordinate ideals saturated by t all reduce to [1]: PASS")
    print("all arbitrary complex t != 0 excluded; t=0 is inherited: PASS")


if __name__ == "__main__":
    main()
