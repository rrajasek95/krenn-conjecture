#!/usr/bin/env python3
"""Exact three-extra-cell frontier around the fixed polarized countermodel.

For the literal sparse quadratic q and displayed z, enumerate all unordered
triples e,f,g of endpoint-colour cells outside supp(q).  The checker decides
exactly whether there are nonzero complex t,u,v such that

    z*(q+t*e+u*f+v*g)^[3] = Delta_(8,3).

It also gives a projective Gram obstruction for 180 of the 187 genuinely new
one-visible-cell cancellation families.  With ``--full-ideals``, Singular
checks saturated characteristic-zero coordinate ideals for the remaining
seven families.

Only the Python standard library is used for the census and projective
closure.  Singular is required only for the optional seven full ideals.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict, deque
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
from itertools import combinations, permutations, product
import shutil
import subprocess
import time


SITES = tuple(range(8))
COLOURS = tuple(range(3))
EDGES = tuple(combinations(SITES, 2))
ALL_CELLS = tuple(
    (left, right, left_colour, right_colour)
    for left, right in EDGES
    for left_colour, right_colour in product(COLOURS, repeat=2)
)

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
DELTA_WORDS = frozenset(PURE_WORDS)

# The seven cases not closed by the parameter-free projective argument.
EXPECTED_IDEAL_SURVIVORS = (
    ((0, 1, 0, 0), (0, 5, 0, 1), (1, 7, 0, 1), (33,)),
    ((0, 1, 0, 0), (0, 6, 0, 1), (1, 3, 0, 1), (33,)),
    ((0, 1, 0, 0), (0, 7, 0, 1), (1, 5, 0, 1), (33,)),
    ((0, 3, 1, 2), (1, 7, 1, 2), (3, 7, 2, 2), (12,)),
    ((0, 4, 1, 1), (1, 2, 1, 1), (3, 7, 2, 2), (12,)),
    ((0, 6, 1, 2), (1, 5, 1, 2), (3, 7, 2, 2), (68,)),
    ((0, 7, 1, 2), (1, 3, 1, 2), (3, 7, 2, 2), (12,)),
)

EXPECTED_PATTERN_COUNTS = Counter({(12,): 103, (33,): 48, (68,): 27, (66,): 9})
EXPECTED_PROJECTIVE_BRANCH_HISTOGRAM = Counter({1: 159, 2: 20, 3: 1})
EXPECTED_CLASSIFICATION_SHA256 = "26d25bdc52cb84a1905f04cbcb49fd515257d7ec0aa243dbdd93e290e50d1046"
EXPECTED_SOLUTION_SHA256 = "cc7fcbae3ad29af3b35f90faaa9d0a2c5dad616f64c7b24f5b6ec90961831bb1"
EXPECTED_NEW_FAMILY_SHA256 = "0471329f6bf631d816bdeee9dc0419242039ca20475933e4698ef45f658f9abd"
EXPECTED_PROJECTIVE_CLOSURE_SHA256 = "649dcab156a6beb2b7575c9e3b65186807f6354ad755a0729776f9e3da7df645"
EXPECTED_COMPATIBLE_CLOSURE_SHA256 = "e6bdb1bb4adc22b91666c134ae99bb66ae8dfaec2b5ff391ceb052bd7d208555"
EXPECTED_COMPATIBLE_SURVIVOR_SHA256 = "b481e4abddc0e98e8cbde9486d7d384a821430b15964dde6e9b279367988a57a"

EXPECTED_COMPATIBLE_CLOSURE_LEDGER = Counter({
    (1, True, "closed"): 923,
    (1, False, "open_branch"): 1,
    (2, True, "closed"): 28_283,
    (2, False, "open_branch"): 165,
    (2, False, "pure_direct"): 64,
    (3, True, "closed"): 57_078,
    (3, False, "open_branch"): 320,
    (3, False, "pure_direct"): 193,
})
EXPECTED_COMPATIBLE_BRANCH_HISTOGRAM = Counter({
    (1, 1): 469,
    (1, 2): 406,
    (1, 4): 48,
    (2, 1): 15_151,
    (2, 2): 10_689,
    (2, 3): 702,
    (2, 4): 1_603,
    (2, 6): 93,
    (2, 8): 45,
    (3, 1): 31_058,
    (3, 2): 20_236,
    (3, 3): 1_914,
    (3, 4): 3_423,
    (3, 5): 18,
    (3, 6): 299,
    (3, 8): 130,
})

TAG_MONOMIAL = {
    0: "",
    1: "t",
    2: "u",
    3: "t*u",
    4: "v",
    5: "t*v",
    6: "u*v",
    7: "t*u*v",
}
RELATION = {
    (33,): "t+u*v",
    (12,): "v+t*u",
    (68,): "1+t*u",
    (66,): "1+t*v",
}


def cell_sites(cell):
    return cell[0], cell[1]


def cells_are_disjoint(cells):
    endpoints = tuple(site for cell in cells for site in cell_sites(cell))
    return len(endpoints) == len(set(endpoints))


def partial_word(cells):
    word = [-1] * 8
    for left, right, left_colour, right_colour in cells:
        assert word[left] == word[right] == -1
        word[left] = left_colour
        word[right] = right_colour
    return tuple(word)


def normalized_gram_edge(left, right):
    assert left != right
    return tuple(sorted((left, right)))


def base_polarized_expansion():
    result = Counter()
    for z_cell in DISPLAYED_Z:
        for triple in combinations(BASE_Q, 3):
            cells = (z_cell,) + triple
            if cells_are_disjoint(cells):
                result[partial_word(cells)] += 1
    return result


def single_debt(extra):
    """Coefficient of t: z*extra*q^[2]."""
    result = Counter()
    for z_cell in DISPLAYED_Z:
        for pair in combinations(BASE_Q, 2):
            cells = (z_cell, extra) + pair
            if cells_are_disjoint(cells):
                result[partial_word(cells)] += 1
    return result


def cross_debt(left, right):
    """Coefficient of t*u: z*left*right*q."""
    result = Counter()
    for z_cell in DISPLAYED_Z:
        for q_cell in BASE_Q:
            cells = (z_cell, left, right, q_cell)
            if cells_are_disjoint(cells):
                result[partial_word(cells)] += 1
    return result


def triple_debt(first, second, third):
    """Coefficient of t*u*v: z*first*second*third."""
    result = Counter()
    for z_cell in DISPLAYED_Z:
        cells = (z_cell, first, second, third)
        if cells_are_disjoint(cells):
            result[partial_word(cells)] += 1
    return result


def add_debt(rows, debt, column):
    for word, coefficient in debt.items():
        assert coefficient == 1
        rows[word][column] += coefficient


def debt_rows(indices, singles, crosses, extras):
    """Rows in monomials (t,u,v,tu,tv,uv,tuv), stored in that order."""
    first, second, third = indices
    rows = defaultdict(lambda: [0] * 7)
    add_debt(rows, singles[first], 0)
    add_debt(rows, singles[second], 1)
    add_debt(rows, singles[third], 2)
    add_debt(rows, crosses[first, second], 3)
    add_debt(rows, crosses[first, third], 4)
    add_debt(rows, crosses[second, third], 5)
    add_debt(rows, triple_debt(extras[first], extras[second], extras[third]), 6)
    return {word: tuple(row) for word, row in rows.items()}


def row_mask(row):
    assert all(entry in (0, 1) for entry in row)
    return sum((1 << index) for index, entry in enumerate(row) if entry)


def evaluate_rows(rows, parameters):
    t, u, v = parameters
    monomials = (t, u, v, t * u, t * v, u * v, t * u * v)
    return tuple(sum(a * b for a, b in zip(row, monomials)) for row in rows.values())


def tagged_forms(triple):
    """Return the ps*q'^[3] Gram forms and q'^[4], tagged by extra subset."""
    weighted = tuple((cell, 0) for cell in BASE_Q) + tuple(
        (cell, 1 << index) for index, cell in enumerate(triple)
    )
    forms = defaultdict(Counter)
    for chosen in combinations(weighted, 3):
        cells = tuple(item[0] for item in chosen)
        if not cells_are_disjoint(cells):
            continue
        tag = 0
        for _cell, item_tag in chosen:
            tag |= item_tag
        word = list(partial_word(cells))
        missing = tuple(index for index, value in enumerate(word) if value == -1)
        assert len(missing) == 2
        for first_colour, second_colour in product(COLOURS, repeat=2):
            full = list(word)
            full[missing[0]] = first_colour
            full[missing[1]] = second_colour
            edge = normalized_gram_edge(
                (missing[0], first_colour), (missing[1], second_colour)
            )
            forms[tuple(full)][edge, tag] += 1

    q_four = defaultdict(Counter)
    for chosen in combinations(weighted, 4):
        cells = tuple(item[0] for item in chosen)
        if not cells_are_disjoint(cells):
            continue
        tag = 0
        for _cell, item_tag in chosen:
            tag |= item_tag
        q_four[partial_word(cells)][tag] += 1
    return dict(forms), dict(q_four)


def graph_certificate_kind(required, zero_edges):
    """Return an exact projective-line parity contradiction, if present."""
    modes = frozenset(mode for edge in required for mode in edge)
    graph = {mode: set() for mode in modes}
    for left, right in zero_edges:
        if left in modes and right in modes:
            graph[left].add(right)
            graph[right].add(left)

    component = {}
    parity = {}
    bipartite = []
    for root in sorted(modes):
        if root in component:
            continue
        cid = len(bipartite)
        component[root] = cid
        parity[root] = 0
        queue = deque([root])
        is_bipartite = True
        while queue:
            vertex = queue.popleft()
            for neighbour in graph[vertex]:
                if neighbour not in component:
                    component[neighbour] = cid
                    parity[neighbour] = parity[vertex] ^ 1
                    queue.append(neighbour)
                else:
                    assert component[neighbour] == cid
                    if parity[neighbour] == parity[vertex]:
                        is_bipartite = False
        bipartite.append(is_bipartite)

    for left, right in required:
        if component[left] != component[right]:
            continue
        cid = component[left]
        if not bipartite[cid]:
            return "isotropic_component"
        if parity[left] != parity[right]:
            return "odd_zero_path"
    return None


def projective_closure(triple):
    forms, q_four = tagged_forms(triple)
    pure_options = []
    for word in PURE_WORDS:
        if q_four.get(word):
            return False, 0, (), "pure_direct"
        edges = tuple(sorted({edge for edge, _tag in forms.get(word, {})}))
        if not edges:
            return False, 0, (), "pure_missing"
        pure_options.append(edges)

    zeros = set()
    for word, terms in forms.items():
        if word in DELTA_WORDS or q_four.get(word) or len(terms) != 1:
            continue
        (edge, _tag), coefficient = next(iter(terms.items()))
        assert coefficient > 0
        zeros.add(edge)

    kinds = []
    branches = 0
    for required in product(*pure_options):
        branches += 1
        kind = graph_certificate_kind(required, zeros)
        if kind is None:
            return False, branches, tuple(kinds), "open_branch"
        kinds.append(kind)
    return True, branches, tuple(kinds), "closed"


def mode_variable(prefix, mode):
    return f"{prefix}{mode[0]}{mode[1]}"


def beta_expression(edge):
    left, right = edge
    return (
        f"({mode_variable('p', left)}*{mode_variable('s', right)}"
        f"+{mode_variable('s', left)}*{mode_variable('p', right)})"
    )


def ring_variables():
    return [
        mode_variable(prefix, (site, colour))
        for prefix in ("p", "s")
        for site in SITES
        for colour in COLOURS
    ] + ["a", "t", "u", "v", "h"]


def append_term(terms, coefficient, factors):
    pieces = []
    if coefficient != 1:
        pieces.append(str(coefficient))
    pieces.extend(factor for factor in factors if factor)
    terms.append("*".join(pieces) if pieces else "1")


def singular_program(record):
    first, second, third, pattern = record
    forms, q_four = tagged_forms((first, second, third))
    equations = []
    for word in sorted(set(forms) | set(q_four) | set(DELTA_WORDS)):
        terms = []
        for (edge, tag), coefficient in sorted(forms.get(word, {}).items()):
            append_term(
                terms, 4 * coefficient, (TAG_MONOMIAL[tag], beta_expression(edge))
            )
        for tag, coefficient in sorted(q_four.get(word, {}).items()):
            append_term(terms, 4 * coefficient, ("a", TAG_MONOMIAL[tag]))
        if word in DELTA_WORDS:
            terms.append("-1")
        if terms:
            equations.append("+".join(terms))
    equations.extend((RELATION[pattern], "h*t*u*v-1"))
    variables = ring_variables()
    program = (
        f"ring r=0,({','.join(variables)}),dp;\n"
        f"ideal I={','.join(equations)};\n"
        "option(redSB);\nideal G=std(I);\n"
        'print("BASIS_SIZE");\nprint(size(G));\n'
        'print("BASIS_FIRST");\nprint(G[1]);\n'
    )
    return program, len(equations), len(variables)


def singular_job(executable, record):
    program, equation_count, variable_count = singular_program(record)
    start = time.monotonic()
    result = subprocess.run(
        [executable, "-q"], input=program, text=True, capture_output=True,
        check=True, timeout=600,
    )
    elapsed = time.monotonic() - start
    if result.stderr.strip():
        raise AssertionError(result.stderr)
    lines = tuple(line.strip() for line in result.stdout.splitlines() if line.strip())
    size = lines[lines.index("BASIS_SIZE") + 1]
    first = lines[lines.index("BASIS_FIRST") + 1]
    assert size == first == "1", result.stdout
    return record, equation_count, variable_count, elapsed


def run_full_ideals(records, workers):
    executable = shutil.which("Singular")
    if executable is None:
        raise SystemExit("Singular is required for --full-ideals")
    outputs = []
    start = time.monotonic()
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {
            pool.submit(singular_job, executable, record): record for record in records
        }
        for future in as_completed(futures):
            outputs.append(future.result())
    for record, equations, variables, elapsed in sorted(outputs):
        print(
            "ideal", record, "basis [1]", "equations", equations,
            "variables", variables, "seconds", f"{elapsed:.3f}",
        )
    print(
        "three-extra survivor ideals unit:", len(outputs), "/", len(records),
        "parallel wall seconds", f"{time.monotonic() - start:.3f}",
    )


def run_compatible_projective(records):
    """Separate closure census for the identically compatible triples."""
    ledger = Counter()
    branch_histogram = Counter()
    digest = hashlib.sha256()
    survivor_digest = hashlib.sha256()
    survivors = []
    start = time.monotonic()
    for triple in records:
        physical_pair_count = len({cell[:2] for cell in triple})
        closed, branches, kinds, reason = projective_closure(triple)
        ledger[physical_pair_count, closed, reason] += 1
        if closed:
            branch_histogram[physical_pair_count, branches] += 1
        else:
            survivor = (triple, physical_pair_count, reason, branches)
            survivors.append(survivor)
            survivor_digest.update(repr(survivor).encode())
            survivor_digest.update(b"\n")
        digest.update(
            repr((triple, physical_pair_count, closed, branches, kinds, reason)).encode()
        )
        digest.update(b"\n")

    assert ledger == EXPECTED_COMPATIBLE_CLOSURE_LEDGER
    assert branch_histogram == EXPECTED_COMPATIBLE_BRANCH_HISTOGRAM
    assert digest.hexdigest() == EXPECTED_COMPATIBLE_CLOSURE_SHA256
    assert survivor_digest.hexdigest() == EXPECTED_COMPATIBLE_SURVIVOR_SHA256
    assert Counter(item[1] for item in survivors) == Counter({1: 1, 2: 229, 3: 513})
    print("compatible-triple projective closure: PASS")
    print("compatible closure ledger:")
    for key, count in sorted(ledger.items(), key=lambda item: repr(item[0])):
        print(key, count)
    print("compatible closed-branch histogram:", dict(sorted(branch_histogram.items())))
    print("compatible projective survivors:", len(survivors))
    print("compatible-closure sha256:", digest.hexdigest())
    print("compatible-survivor sha256:", survivor_digest.hexdigest())
    for index, survivor in enumerate(survivors):
        print("compatible survivor", index, survivor)
    print("compatible closure seconds:", f"{time.monotonic() - start:.3f}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--full-ideals", action="store_true")
    parser.add_argument("--compatible-projective", action="store_true")
    parser.add_argument("--workers", type=int, default=3)
    args = parser.parse_args()
    assert args.workers >= 1

    assert len(ALL_CELLS) == 252
    assert len(set(BASE_Q)) == 9
    assert base_polarized_expansion() == Counter({word: 1 for word in PURE_WORDS})

    extras = tuple(cell for cell in ALL_CELLS if cell not in BASE_Q)
    assert len(extras) == 243
    singles = tuple(single_debt(cell) for cell in extras)
    assert Counter(map(len, singles)) == Counter({0: 99, 1: 135, 2: 9})
    assert all(coefficient == 1 for debt in singles for coefficient in debt.values())

    crosses = {}
    for first, second in combinations(range(len(extras)), 2):
        debt = cross_debt(extras[first], extras[second])
        assert len(debt) <= 1
        assert all(coefficient == 1 for coefficient in debt.values())
        crosses[first, second] = debt
    assert Counter(map(len, crosses.values())) == Counter({0: 25830, 1: 3573})

    counts = Counter()
    pattern_counts = Counter()
    visibility_counts = Counter()
    intersection_profiles = Counter()
    compatible_physical_pairs = Counter()
    compatible_union_sites = Counter()
    classification_digest = hashlib.sha256()
    solution_digest = hashlib.sha256()
    new_digest = hashlib.sha256()
    new_records = []
    compatible_records = []
    exceptional = []

    for indices in combinations(range(len(extras)), 3):
        triple = tuple(extras[index] for index in indices)
        rows = debt_rows(indices, singles, crosses, extras)
        masks = tuple(sorted(row_mask(row) for row in rows.values()))
        singleton = any(mask & (mask - 1) == 0 for mask in masks)
        if not rows:
            category = "compatible"
            counts[category] += 1
            physical = tuple(cell[:2] for cell in triple)
            compatible_physical_pairs[len(set(physical))] += 1
            compatible_union_sites[len(set().union(*(set(pair) for pair in physical)))] += 1
            solution_digest.update(repr((triple, category)).encode())
            solution_digest.update(b"\n")
            compatible_records.append(triple)
        elif singleton:
            category = "singleton_rejection"
            counts[category] += 1
        elif masks == (3, 6, 56):
            category = "exceptional_rejection"
            counts[category] += 1
            exceptional.append(triple)
        else:
            category = "binomial_cancellation"
            counts[category] += 1
            assert len(masks) == 1 and masks in EXPECTED_PATTERN_COUNTS
            pattern_counts[masks] += 1
            visibility = tuple(bool(singles[index]) for index in indices)
            visibility_counts[visibility] += 1
            assert sum(visibility) == 1
            site_sets = tuple(set(cell[:2]) for cell in triple)
            intersection_profiles[
                tuple(sorted(len(left & right) for left, right in combinations(site_sets, 2)))
            ] += 1
            witness = {
                (33,): (-1, 1, 1),
                (12,): (1, 1, -1),
                (68,): (1, -1, 1),
                (66,): (1, 1, -1),
            }[masks]
            assert all(witness)
            assert not any(evaluate_rows(rows, witness))
            record = triple + (masks,)
            new_records.append(record)
            new_digest.update(repr(record).encode())
            new_digest.update(b"\n")
            solution_digest.update(repr((triple, category, masks)).encode())
            solution_digest.update(b"\n")
        classification_digest.update(repr((triple, category, masks)).encode())
        classification_digest.update(b"\n")

    assert sum(counts.values()) == 2_362_041
    assert counts == Counter({
        "singleton_rejection": 2_274_826,
        "compatible": 87_027,
        "binomial_cancellation": 187,
        "exceptional_rejection": 1,
    })
    assert pattern_counts == EXPECTED_PATTERN_COUNTS
    assert visibility_counts == Counter({
        (False, False, True): 130,
        (True, False, False): 48,
        (False, True, False): 9,
    })
    assert intersection_profiles == Counter({(0, 1, 1): 150, (0, 0, 0): 37})
    assert exceptional == [DISPLAYED_Z]

    # The exceptional triple z_1,z_2,z_3 has equations
    # t+u=0, u+v=0, tu+tv+uv=0.  The first two make the last u^2,
    # impossible when u is nonzero.
    special_rows = debt_rows(
        tuple(extras.index(cell) for cell in DISPLAYED_Z), singles, crosses, extras
    )
    assert tuple(sorted(row_mask(row) for row in special_rows.values())) == (3, 6, 56)

    closure_counts = Counter()
    branch_histogram = Counter()
    certificate_kinds = Counter()
    ideal_survivors = []
    closure_digest = hashlib.sha256()
    for record in new_records:
        triple, pattern = record[:3], record[3]
        closed, branches, kinds, reason = projective_closure(triple)
        closure_counts[closed, pattern, reason] += 1
        if closed:
            branch_histogram[branches] += 1
            certificate_kinds.update(kinds)
        else:
            ideal_survivors.append(record)
        closure_digest.update(repr((record, closed, branches, kinds, reason)).encode())
        closure_digest.update(b"\n")

    assert sum(value for (closed, _pattern, _reason), value in closure_counts.items() if closed) == 180
    assert tuple(ideal_survivors) == EXPECTED_IDEAL_SURVIVORS
    assert branch_histogram == EXPECTED_PROJECTIVE_BRANCH_HISTOGRAM
    assert classification_digest.hexdigest() == EXPECTED_CLASSIFICATION_SHA256
    assert solution_digest.hexdigest() == EXPECTED_SOLUTION_SHA256
    assert new_digest.hexdigest() == EXPECTED_NEW_FAMILY_SHA256
    assert closure_digest.hexdigest() == EXPECTED_PROJECTIVE_CLOSURE_SHA256

    print("three-extra fixed-q polarized frontier: PASS")
    print("all unordered outside-cell triples:", sum(counts.values()))
    print("classification:", dict(sorted(counts.items())))
    print("solutions / rejections:", 87_214, 2_274_827)
    print("fully compatible invisible triples:", counts["compatible"])
    print("compatible distinct physical pairs:", dict(sorted(compatible_physical_pairs.items())))
    print("compatible union-site histogram:", dict(sorted(compatible_union_sites.items())))
    print("new one-visible cancellation families:", counts["binomial_cancellation"])
    print("new pattern counts:", dict(sorted(pattern_counts.items())))
    print("new visibility positions:", dict(sorted(visibility_counts.items())))
    print("new physical intersection profiles:", dict(sorted(intersection_profiles.items())))
    print("exceptional impossible triple:", exceptional[0])
    print("new frontier projectively closed / ideal survivors:", 180, len(ideal_survivors))
    print("projective branch histogram:", dict(sorted(branch_histogram.items())))
    print("projective certificate kinds:", dict(sorted(certificate_kinds.items())))
    print("classification sha256:", classification_digest.hexdigest())
    print("solution sha256:", solution_digest.hexdigest())
    print("new-family sha256:", new_digest.hexdigest())
    print("projective-closure sha256:", closure_digest.hexdigest())
    print("lexicographic representative by pattern:")
    for pattern in sorted(pattern_counts):
        print(pattern, next(record for record in new_records if record[3] == pattern))
    print("seven ideal survivors:")
    for record in ideal_survivors:
        print(record)

    if args.full_ideals:
        run_full_ideals(ideal_survivors, args.workers)
    if args.compatible_projective:
        run_compatible_projective(compatible_records)


if __name__ == "__main__":
    main()
