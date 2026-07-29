#!/usr/bin/env python3
"""Clean-room audit of the fixed-(q,z) three-cell cancellation frontier.

This file deliberately does not import the discovery/primary checker.  It
reconstructs the literal endpoint-colour cells, exhausts all C(243,3)
unordered triples, solves their Laurent debt equations on (C*)^3, rebuilds
the parameter-safe projective Gram certificates, and (unless requested
otherwise) asks Singular to reduce the seven residual localized QQ ideals.

The Singular replay changes both ring and generator order: the torus
localizer and binomial relation are placed first, parameters precede the
scalar, and mode variables run in reverse site/colour order with s before p.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
from itertools import combinations, product
import shutil
import subprocess
import time


SITES = tuple(range(8))
COLOURS = tuple(range(3))
PHYSICAL_PAIRS = tuple(combinations(SITES, 2))

# A cell is (smaller endpoint, larger endpoint, colour at smaller endpoint,
# colour at larger endpoint).  Keeping this convention literal is part of the
# endpoint-order audit below.
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

PURE_WORDS: tuple[Word, ...] = tuple((c,) * 8 for c in COLOURS)
TARGET_WORDS = frozenset(PURE_WORDS)

MONOMIALS: tuple[Exponent, ...] = (
    (1, 0, 0),  # t D_e
    (0, 1, 0),  # u D_f
    (0, 0, 1),  # v D_g
    (1, 1, 0),  # tu D_ef
    (1, 0, 1),  # tv D_eg
    (0, 1, 1),  # uv D_fg
    (1, 1, 1),  # tuv D_efg
)

RELATION_NAMES = {
    ((0, 0, 1), (1, 1, 0)): "v+tu",
    ((0, 1, 1), (1, 0, 0)): "t+uv",
    ((0, 0, 0), (1, 0, 1)): "1+tv",
    ((0, 0, 0), (1, 1, 0)): "1+tu",
}

EXPECTED_RELATION_COUNTS = Counter({
    "v+tu": 103,
    "t+uv": 48,
    "1+tv": 9,
    "1+tu": 27,
})

EXPECTED_FIRST_BY_RELATION: dict[str, Triple] = {
    "v+tu": (
        (0, 3, 1, 0), (1, 5, 1, 0), (3, 5, 0, 0),
    ),
    "t+uv": (
        (0, 1, 0, 0), (0, 5, 0, 1), (1, 7, 0, 1),
    ),
    "1+tv": (
        (0, 4, 2, 0), (1, 6, 0, 0), (2, 5, 2, 0),
    ),
    "1+tu": (
        (0, 4, 1, 0), (1, 5, 1, 0), (2, 6, 0, 0),
    ),
}

EXPECTED_EXCEPTIONAL: Triple = (
    (0, 1, 0, 0), (2, 4, 1, 1), (3, 7, 2, 2),
)

EXPECTED_IDEAL_CASES: tuple[Triple, ...] = (
    ((0, 1, 0, 0), (0, 5, 0, 1), (1, 7, 0, 1)),
    ((0, 1, 0, 0), (0, 6, 0, 1), (1, 3, 0, 1)),
    ((0, 1, 0, 0), (0, 7, 0, 1), (1, 5, 0, 1)),
    ((0, 3, 1, 2), (1, 7, 1, 2), (3, 7, 2, 2)),
    ((0, 4, 1, 1), (1, 2, 1, 1), (3, 7, 2, 2)),
    ((0, 6, 1, 2), (1, 5, 1, 2), (3, 7, 2, 2)),
    ((0, 7, 1, 2), (1, 3, 1, 2), (3, 7, 2, 2)),
)

EXPECTED_EQUATION_COUNTS = {
    triple: count for triple, count in zip(
        EXPECTED_IDEAL_CASES,
        (290, 284, 284, 284, 319, 284, 290),
    )
}


def cell_site_mask(cell: Cell) -> int:
    return (1 << cell[0]) | (1 << cell[1])


def disjoint(cells: tuple[Cell, ...]) -> bool:
    mask = 0
    for cell in cells:
        cell_mask = cell_site_mask(cell)
        if mask & cell_mask:
            return False
        mask |= cell_mask
    return True


def partial_word(cells: tuple[Cell, ...]) -> Word:
    result = [-1] * 8
    for i, j, ci, cj in cells:
        assert i < j
        assert result[i] == result[j] == -1
        result[i], result[j] = ci, cj
    return tuple(result)


def full_word(cells: tuple[Cell, ...]) -> Word:
    result = partial_word(cells)
    assert -1 not in result
    return result


def base_identity() -> Counter[Word]:
    result: Counter[Word] = Counter()
    for z_cell in DISPLAYED_Z:
        for chosen_q in combinations(BASE_Q, 3):
            chosen = (z_cell,) + chosen_q
            if disjoint(chosen):
                result[full_word(chosen)] += 1
    return result


def one_debt(cell: Cell) -> Counter[Word]:
    result: Counter[Word] = Counter()
    for z_cell in DISPLAYED_Z:
        for chosen_q in combinations(BASE_Q, 2):
            chosen = (z_cell, cell) + chosen_q
            if disjoint(chosen):
                result[full_word(chosen)] += 1
    return result


def two_debt(first: Cell, second: Cell) -> Counter[Word]:
    result: Counter[Word] = Counter()
    for z_cell in DISPLAYED_Z:
        for q_cell in BASE_Q:
            chosen = (z_cell, first, second, q_cell)
            if disjoint(chosen):
                result[full_word(chosen)] += 1
    return result


def three_debt(first: Cell, second: Cell, third: Cell) -> Counter[Word]:
    result: Counter[Word] = Counter()
    for z_cell in DISPLAYED_Z:
        chosen = (z_cell, first, second, third)
        if disjoint(chosen):
            result[full_word(chosen)] += 1
    return result


def normalized_laurent_support(mask: int) -> tuple[Exponent, ...]:
    """Remove the common torus monomial from a 7-term support mask."""
    exponents = tuple(
        MONOMIALS[index] for index in range(7) if mask & (1 << index)
    )
    minima = tuple(min(exp[axis] for exp in exponents) for axis in range(3))
    return tuple(sorted(
        tuple(exp[axis] - minima[axis] for axis in range(3))
        for exp in exponents
    ))


def equation_masks(
    i: int,
    j: int,
    k: int,
    one: tuple[tuple[Word, ...], ...],
    two: tuple[tuple[tuple[Word, ...], ...], ...],
    outside: tuple[Cell, ...],
) -> tuple[int, ...]:
    by_word: dict[Word, int] = {}

    def add(words: tuple[Word, ...], bit: int) -> None:
        for word in words:
            by_word[word] = by_word.get(word, 0) | bit

    add(one[i], 1)
    add(one[j], 2)
    add(one[k], 4)
    add(two[i][j], 8)
    add(two[i][k], 16)
    add(two[j][k], 32)
    triple_debt = three_debt(outside[i], outside[j], outside[k])
    assert all(coefficient == 1 for coefficient in triple_debt.values())
    add(tuple(triple_debt), 64)
    return tuple(sorted(by_word.values()))


def canonical_relation(masks: tuple[int, ...]) -> str | None:
    normalized = {normalized_laurent_support(mask) for mask in masks}
    if len(normalized) != 1:
        return None
    support = next(iter(normalized))
    return RELATION_NAMES.get(support)


def sha256_lines(records) -> str:
    digest = hashlib.sha256()
    for record in records:
        digest.update(repr(record).encode("utf-8"))
        digest.update(b"\n")
    return digest.hexdigest()


def endpoint_intersection_profile(triple: Triple) -> tuple[int, int, int]:
    site_sets = tuple(frozenset(cell[:2]) for cell in triple)
    return tuple(sorted(
        len(site_sets[a] & site_sets[b])
        for a, b in combinations(range(3), 2)
    ))


def audit_three_cell_expansion(
    triple: Triple,
    masks: tuple[int, ...],
) -> None:
    """Independently re-expand the seven coefficients for one triple."""
    expected: defaultdict[Word, int] = defaultdict(int)
    e, f, g = triple
    for index, debt in enumerate((
        one_debt(e), one_debt(f), one_debt(g),
        two_debt(e, f), two_debt(e, g), two_debt(f, g),
        three_debt(e, f, g),
    )):
        for word, coefficient in debt.items():
            assert coefficient == 1
            expected[word] |= 1 << index

    weighted = tuple((cell, (0, 0, 0)) for cell in BASE_Q) + (
        (e, (1, 0, 0)),
        (f, (0, 1, 0)),
        (g, (0, 0, 1)),
    )
    observed: defaultdict[Word, Counter[Exponent]] = defaultdict(Counter)
    for z_cell in DISPLAYED_Z:
        for chosen in combinations(weighted, 3):
            cells = (z_cell,) + tuple(item[0] for item in chosen)
            if not disjoint(cells):
                continue
            exponent = tuple(sum(item[1][axis] for item in chosen) for axis in range(3))
            observed[full_word(cells)][exponent] += 1

    # Remove the constant base identity.  What remains must be precisely the
    # seven debt terms, with divided-power coefficient one.
    for word in PURE_WORDS:
        observed[word][(0, 0, 0)] -= 1
        if observed[word][(0, 0, 0)] == 0:
            del observed[word][(0, 0, 0)]
        if not observed[word]:
            del observed[word]
    converted = {}
    for word, polynomial in observed.items():
        assert all(coefficient == 1 for coefficient in polynomial.values())
        converted[word] = sum(1 << MONOMIALS.index(exp) for exp in polynomial)
    assert converted == dict(expected)
    assert tuple(sorted(converted.values())) == masks


def exact_torus_frontier() -> dict:
    assert len(ALL_CELLS) == 252 and len(set(ALL_CELLS)) == 252
    assert all(i < j for i, j, _ci, _cj in ALL_CELLS)
    assert all(i < j for i, j, _ci, _cj in BASE_Q + DISPLAYED_Z)
    assert len(set(BASE_Q)) == 9 and len(set(DISPLAYED_Z)) == 3
    assert not set(BASE_Q) & set(DISPLAYED_Z)
    assert base_identity() == Counter({word: 1 for word in PURE_WORDS})

    outside = tuple(cell for cell in ALL_CELLS if cell not in BASE_Q)
    assert len(outside) == 243

    one_counters = tuple(one_debt(cell) for cell in outside)
    assert Counter(len(debt) for debt in one_counters) == Counter({0: 99, 1: 135, 2: 9})
    assert all(value == 1 for debt in one_counters for value in debt.values())
    one = tuple(tuple(sorted(debt)) for debt in one_counters)

    two_rows: list[list[tuple[Word, ...]]] = [
        [tuple() for _ in outside] for _ in outside
    ]
    pair_support_histogram: Counter[int] = Counter()
    for i, j in combinations(range(len(outside)), 2):
        debt = two_debt(outside[i], outside[j])
        assert all(value == 1 for value in debt.values())
        words = tuple(sorted(debt))
        two_rows[i][j] = two_rows[j][i] = words
        pair_support_histogram[len(words)] += 1
    assert pair_support_histogram == Counter({0: 25830, 1: 3573})
    two = tuple(tuple(row) for row in two_rows)

    counts = Counter()
    relation_counts = Counter()
    first_by_relation: dict[str, Triple] = {}
    zero_triples = []
    binomial_families: list[tuple[Triple, str]] = []
    exceptional = []
    classification_digest = hashlib.sha256()

    for i, j, k in combinations(range(len(outside)), 3):
        triple = (outside[i], outside[j], outside[k])
        masks = equation_masks(i, j, k, one, two, outside)
        if not masks:
            category = "zero"
            zero_triples.append(triple)
        elif any(mask & (mask - 1) == 0 for mask in masks):
            category = "singleton_reject"
        else:
            relation = canonical_relation(masks)
            if relation is not None:
                category = relation
                relation_counts[relation] += 1
                first_by_relation.setdefault(relation, triple)
                binomial_families.append((triple, relation))
            else:
                category = "exceptional"
                exceptional.append((triple, masks))
        counts[category] += 1
        classification_digest.update(repr((triple, category, masks)).encode("utf-8"))
        classification_digest.update(b"\n")

    assert counts["zero"] == 87027
    assert counts["singleton_reject"] == 2274826
    assert sum(relation_counts.values()) == 187
    assert relation_counts == EXPECTED_RELATION_COUNTS
    assert first_by_relation == EXPECTED_FIRST_BY_RELATION
    assert len(exceptional) == 1 and exceptional[0][0] == EXPECTED_EXCEPTIONAL

    # The exceptional masks must be t+u, u+v, and tu+tv+uv.  On the torus,
    # the first two give t=-u and v=-u; substitution in the third gives -u^2,
    # which is nonzero.  (The sign is immaterial; the claimed note writes u^2.)
    exceptional_supports = tuple(sorted(
        normalized_laurent_support(mask) for mask in exceptional[0][1]
    ))
    assert exceptional_supports == tuple(sorted((
        ((0, 1, 0), (1, 0, 0)),
        ((0, 0, 1), (0, 1, 0)),
        ((0, 1, 1), (1, 0, 1), (1, 1, 0)),
    )))
    t, u, v = -1, 1, -1
    assert t + u == 0 and u + v == 0 and t * u + t * v + u * v == -1

    # Every binomial has an explicit point of the complex torus, so these
    # support classifications are iff statements, not merely necessary tests.
    witnesses = {
        "v+tu": (1, 1, -1),
        "t+uv": (-1, 1, 1),
        "1+tv": (1, 1, -1),
        "1+tu": (1, -1, 1),
    }
    for triple, relation in binomial_families:
        tv, uv, vv = witnesses[relation]
        assert tv and uv and vv
        assert {
            "v+tu": vv + tv * uv,
            "t+uv": tv + uv * vv,
            "1+tv": 1 + tv * vv,
            "1+tu": 1 + tv * uv,
        }[relation] == 0

    invisible_indices = {index for index, debt in enumerate(one) if not debt}
    zero_set = set(zero_triples)
    compatible_pair = {
        (i, j) for i, j in combinations(sorted(invisible_indices), 2)
        if not two[i][j]
    }
    triangle_count = 0
    for i, j, k in combinations(sorted(invisible_indices), 3):
        if ((i, j) in compatible_pair and (i, k) in compatible_pair
                and (j, k) in compatible_pair):
            triangle_count += 1
            triple = (outside[i], outside[j], outside[k])
            assert triple in zero_set
            assert not three_debt(*triple)
    assert len(compatible_pair) == 3960
    assert triangle_count == len(zero_triples) == 87027

    # Audit the full tagged divided-power expansion for all 188 nontrivial
    # non-singleton cases, including endpoint order and coefficient one.
    for triple, _relation in binomial_families:
        indices = tuple(outside.index(cell) for cell in triple)
        audit_three_cell_expansion(
            triple,
            equation_masks(*indices, one, two, outside),
        )
    triple, masks = exceptional[0]
    audit_three_cell_expansion(triple, masks)

    visibility_profile = Counter()
    intersection_profile = Counter()
    for triple, _relation in binomial_families:
        visibility_profile[sum(bool(one[outside.index(cell)]) for cell in triple)] += 1
        intersection_profile[endpoint_intersection_profile(triple)] += 1
    assert visibility_profile == Counter({1: 187})
    assert intersection_profile == Counter({(0, 1, 1): 150, (0, 0, 0): 37})

    return {
        "outside": outside,
        "one": one,
        "two": two,
        "counts": counts,
        "relation_counts": relation_counts,
        "first_by_relation": first_by_relation,
        "zero_triples": tuple(zero_triples),
        "families": tuple(binomial_families),
        "exceptional": tuple(exceptional),
        "visibility_profile": visibility_profile,
        "intersection_profile": intersection_profile,
        "classification_hash": classification_digest.hexdigest(),
        "zero_hash": sha256_lines(zero_triples),
        "family_hash": sha256_lines(binomial_families),
    }


def normalized_edge(left: Mode, right: Mode) -> GramEdge:
    assert left[0] != right[0]
    return tuple(sorted((left, right)))


def tagged_q(triple: Triple) -> tuple[tuple[Cell, Exponent], ...]:
    return tuple((cell, (0, 0, 0)) for cell in BASE_Q) + tuple(
        (cell, tuple(int(axis == index) for axis in range(3)))
        for index, cell in enumerate(triple)
    )


def add_exponents(exponents: tuple[Exponent, ...]) -> Exponent:
    return tuple(sum(exp[axis] for exp in exponents) for axis in range(3))


def coordinate_forms(triple: Triple) -> tuple[
    dict[Word, Counter[tuple[GramEdge, Exponent]]],
    dict[Word, Counter[Exponent]],
]:
    weighted = tagged_q(triple)
    grams: defaultdict[Word, Counter[tuple[GramEdge, Exponent]]] = defaultdict(Counter)
    directs: defaultdict[Word, Counter[Exponent]] = defaultdict(Counter)

    for chosen in combinations(weighted, 3):
        cells = tuple(item[0] for item in chosen)
        if not disjoint(cells):
            continue
        six_word = partial_word(cells)
        missing = tuple(index for index, colour in enumerate(six_word) if colour == -1)
        assert len(missing) == 2
        exponent = add_exponents(tuple(item[1] for item in chosen))
        for ci, cj in product(COLOURS, repeat=2):
            word = list(six_word)
            word[missing[0]], word[missing[1]] = ci, cj
            edge = normalized_edge((missing[0], ci), (missing[1], cj))
            grams[tuple(word)][edge, exponent] += 1

    for chosen in combinations(weighted, 4):
        cells = tuple(item[0] for item in chosen)
        if disjoint(cells):
            directs[full_word(cells)][add_exponents(tuple(item[1] for item in chosen))] += 1

    return dict(grams), dict(directs)


def audit_euler_factor(triple: Triple) -> None:
    """Check Q*Q^[3]=4Q^[4] tag by tag for the literal Q."""
    weighted = tagged_q(triple)
    q3: Counter[tuple[Word, Exponent]] = Counter()
    q4: Counter[tuple[Word, Exponent]] = Counter()
    for chosen in combinations(weighted, 3):
        cells = tuple(item[0] for item in chosen)
        if disjoint(cells):
            q3[partial_word(cells), add_exponents(tuple(item[1] for item in chosen))] += 1
    for chosen in combinations(weighted, 4):
        cells = tuple(item[0] for item in chosen)
        if disjoint(cells):
            q4[full_word(cells), add_exponents(tuple(item[1] for item in chosen))] += 1

    product_q_q3: Counter[tuple[Word, Exponent]] = Counter()
    for cell, cell_exp in weighted:
        for (six_word, triple_exp), multiplicity in q3.items():
            if cell_site_mask(cell) & sum(
                1 << site for site, colour in enumerate(six_word) if colour != -1
            ):
                continue
            word = list(six_word)
            word[cell[0]], word[cell[1]] = cell[2], cell[3]
            product_q_q3[tuple(word), add_exponents((cell_exp, triple_exp))] += multiplicity
    assert product_q_q3 == Counter({key: 4 * value for key, value in q4.items()})


class ParityDSU:
    """Union-find for constraints line(y)=line(x)^perp."""

    def __init__(self, vertices: set[Mode]):
        self.parent = {vertex: vertex for vertex in vertices}
        self.rank = {vertex: 0 for vertex in vertices}
        self.parity = {vertex: 0 for vertex in vertices}
        self.odd = {vertex: False for vertex in vertices}

    def find(self, vertex: Mode) -> tuple[Mode, int]:
        parent = self.parent[vertex]
        if parent == vertex:
            return vertex, 0
        root, upper = self.find(parent)
        here = self.parity[vertex]
        self.parent[vertex] = root
        self.parity[vertex] = here ^ upper
        return root, self.parity[vertex]

    def impose_odd(self, left: Mode, right: Mode) -> None:
        root_l, parity_l = self.find(left)
        root_r, parity_r = self.find(right)
        if root_l == root_r:
            if (parity_l ^ parity_r) != 1:
                self.odd[root_l] = True
            return
        if self.rank[root_l] < self.rank[root_r]:
            root_l, root_r = root_r, root_l
            parity_l, parity_r = parity_r, parity_l
        self.parent[root_r] = root_l
        self.parity[root_r] = parity_l ^ parity_r ^ 1
        self.odd[root_l] = self.odd[root_l] or self.odd[root_r]
        if self.rank[root_l] == self.rank[root_r]:
            self.rank[root_l] += 1


def graph_certificate(
    required_nonzero: tuple[GramEdge, ...],
    forced_zero: frozenset[GramEdge],
) -> tuple[str, GramEdge] | None:
    active = {mode for edge in required_nonzero for mode in edge}
    dsu = ParityDSU(active)
    for left, right in forced_zero:
        if left in active and right in active:
            dsu.impose_odd(left, right)
    for edge in required_nonzero:
        left, right = edge
        root_l, parity_l = dsu.find(left)
        root_r, parity_r = dsu.find(right)
        if root_l != root_r:
            continue
        if dsu.odd[root_l]:
            return "isotropic_component", edge
        if (parity_l ^ parity_r) == 1:
            return "odd_zero_path", edge
    return None


def projective_classification(triple: Triple) -> tuple[str, int, tuple]:
    grams, directs = coordinate_forms(triple)
    forced_zero = frozenset(
        next(iter(form))[0]
        for word, form in grams.items()
        if word not in TARGET_WORDS and not directs.get(word) and len(form) == 1
    )

    choices = []
    for word in PURE_WORDS:
        if directs.get(word):
            return "direct_a_term", 0, ()
        options = tuple(sorted({edge for edge, _exponent in grams.get(word, {})}))
        assert options
        choices.append(options)

    records = []
    for required in product(*choices):
        certificate = graph_certificate(required, forced_zero)
        records.append((required, certificate))
        if certificate is None:
            return "open_branch", len(records), tuple(records)
    return "closed", len(records), tuple(records)


def exact_projective_frontier(families: tuple[tuple[Triple, str], ...]) -> dict:
    outcomes = []
    status_histogram = Counter()
    branch_histogram = Counter()
    closed = []
    residual = []
    certificate_histogram = Counter()
    for triple, relation in families:
        audit_euler_factor(triple)
        status, branches, records = projective_classification(triple)
        status_histogram[status] += 1
        branch_histogram[branches] += 1
        for _required, certificate in records:
            if certificate:
                certificate_histogram[certificate[0]] += 1
        outcomes.append((triple, relation, status, branches, records))
        if status == "closed":
            closed.append(triple)
        else:
            residual.append(triple)

    assert status_histogram == Counter({"closed": 180, "direct_a_term": 7})
    assert branch_histogram == Counter({1: 159, 2: 20, 3: 1, 0: 7})
    assert certificate_histogram == Counter({"isotropic_component": 202})
    assert tuple(residual) == EXPECTED_IDEAL_CASES
    return {
        "outcomes": tuple(outcomes),
        "closed": tuple(closed),
        "residual": tuple(residual),
        "status_histogram": status_histogram,
        "branch_histogram": branch_histogram,
        "certificate_histogram": certificate_histogram,
        "projective_hash": sha256_lines(outcomes),
    }


def mode_name(prefix: str, mode: Mode) -> str:
    return f"{prefix}{mode[0]}{mode[1]}"


def beta_string(edge: GramEdge) -> str:
    left, right = edge
    return (
        f"({mode_name('s', left)}*{mode_name('p', right)}"
        f"+{mode_name('p', left)}*{mode_name('s', right)})"
    )


def monomial_string(exp: Exponent) -> str:
    factors = ("t",) * exp[0] + ("u",) * exp[1] + ("v",) * exp[2]
    return "*".join(factors)


def term_string(coefficient: int, factors: tuple[str, ...]) -> str:
    pieces = []
    if coefficient != 1:
        pieces.append(str(coefficient))
    pieces.extend(item for item in factors if item)
    return "*".join(pieces) if pieces else "1"


def relation_string(relation: str) -> str:
    return {
        "v+tu": "v+t*u",
        "t+uv": "t+u*v",
        "1+tv": "1+t*v",
        "1+tu": "1+t*u",
    }[relation]


def reversed_ring_variables() -> tuple[str, ...]:
    coordinates = tuple(
        mode_name(prefix, (site, colour))
        for colour in reversed(COLOURS)
        for site in reversed(SITES)
        for prefix in ("s", "p")
    )
    variables = ("rho", "v", "u", "t", "a") + coordinates
    assert len(variables) == 53 and len(set(variables)) == 53
    return variables


def ideal_program(triple: Triple, relation: str) -> tuple[str, tuple[str, ...]]:
    grams, directs = coordinate_forms(triple)
    coordinate_equations = []
    words = sorted(set(grams) | set(directs) | set(TARGET_WORDS), reverse=True)
    for word in words:
        terms = []
        # Direct aQ^[4] terms deliberately precede Gram terms.
        for exp, multiplicity in sorted(directs.get(word, {}).items(), reverse=True):
            terms.append(term_string(4 * multiplicity, ("a", monomial_string(exp))))
        for (edge, exp), multiplicity in sorted(grams.get(word, {}).items(), reverse=True):
            terms.append(term_string(4 * multiplicity, (monomial_string(exp), beta_string(edge))))
        if word in TARGET_WORDS:
            terms.append("-1")
        if terms:
            coordinate_equations.append("+".join(terms))

    # Generator order is intentionally torus, relation, then reversed words.
    equations = (
        "rho*t*u*v-1",
        relation_string(relation),
        *coordinate_equations,
    )
    variables = reversed_ring_variables()
    program = (
        f"ring R=0,({','.join(variables)}),dp;\n"
        f"ideal I={','.join(equations)};\n"
        "option(redSB);\n"
        "ideal G=std(I);\n"
        'print("SIZE");\n'
        "print(size(G));\n"
        'print("FIRST");\n'
        "print(G[1]);\n"
    )
    return program, tuple(equations)


def run_ideal(
    singular: str,
    triple: Triple,
    relation: str,
) -> tuple[Triple, str, int, str, str, float]:
    program, equations = ideal_program(triple, relation)
    started = time.monotonic()
    result = subprocess.run(
        [singular, "-q"],
        input=program,
        text=True,
        capture_output=True,
        check=True,
        timeout=900,
    )
    elapsed = time.monotonic() - started
    if result.stderr.strip():
        raise AssertionError(result.stderr)
    lines = tuple(line.strip() for line in result.stdout.splitlines() if line.strip())
    size = lines[lines.index("SIZE") + 1]
    first = lines[lines.index("FIRST") + 1]
    return triple, relation, len(equations), size, first, elapsed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--support-only",
        action="store_true",
        help="skip the seven localized Singular ideals",
    )
    parser.add_argument("--workers", type=int, default=2)
    args = parser.parse_args()

    started = time.monotonic()
    frontier = exact_torus_frontier()
    print("independent fixed-(q,z) three-cell torus census: PASS")
    print("all outside-support triples:", sum(frontier["counts"].values()))
    print("zero / binomial / exceptional / singleton-rejected:", 87027, 187, 1, 2274826)
    print("binomial relations:", dict(sorted(frontier["relation_counts"].items())))
    print("visible-cell profile:", dict(frontier["visibility_profile"]))
    print("physical-pair profiles:", dict(sorted(frontier["intersection_profile"].items())))
    print("classification SHA-256:", frontier["classification_hash"])
    print("zero-triple SHA-256:", frontier["zero_hash"])
    print("binomial-family SHA-256:", frontier["family_hash"])
    print("census seconds:", f"{time.monotonic() - started:.3f}")

    projective = exact_projective_frontier(frontier["families"])
    print("projective closures:", len(projective["closed"]), "/", len(frontier["families"]))
    print("branch histogram:", dict(sorted(projective["branch_histogram"].items())))
    print("certificate histogram:", dict(projective["certificate_histogram"]))
    print("residual localized ideals:", len(projective["residual"]))
    print("projective SHA-256:", projective["projective_hash"])

    family_relation = dict(frontier["families"])
    ideal_inputs = []
    for triple in projective["residual"]:
        relation = family_relation[triple]
        program, equations = ideal_program(triple, relation)
        assert len(equations) == EXPECTED_EQUATION_COUNTS[triple]
        ideal_inputs.append((triple, relation, program))
    print("ideal-input SHA-256:", sha256_lines(ideal_inputs))

    if args.support_only:
        print("Singular replay skipped by request")
        return
    singular = shutil.which("Singular")
    if singular is None:
        raise SystemExit("Singular is required for the exact localized ideals")

    ideal_started = time.monotonic()
    outputs = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [
            pool.submit(run_ideal, singular, triple, family_relation[triple])
            for triple in projective["residual"]
        ]
        for future in as_completed(futures):
            outputs.append(future.result())
    for triple, relation, equation_count, size, first, elapsed in sorted(outputs):
        assert size == first == "1"
        print(
            triple,
            relation,
            "basis", size, first,
            "equations", equation_count,
            "variables", 53,
            "seconds", f"{elapsed:.3f}",
        )
    assert len(outputs) == 7
    print("changed-order localized QQ unit ideals: 7 / 7")
    print("ideal wall seconds:", f"{time.monotonic() - ideal_started:.3f}")
    print("all 187 binomial-locus families exclude pair-cap preimages: PASS")


if __name__ == "__main__":
    main()
