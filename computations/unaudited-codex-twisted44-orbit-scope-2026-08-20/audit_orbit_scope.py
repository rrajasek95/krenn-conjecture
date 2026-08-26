#!/usr/bin/env python3
"""Independent, exact audit of the W33 twisted-4+4 orbit claim.

UNAUDITED.  This file imports no project code.  It works directly with
endpoint-ordered cells on K_8 and with the defining binary hafnian equations.

The stratum audited here is:

* the diagonal cells are two perfect matchings whose union is two disjoint
  four-cycles;
* all eight diagonal cells are nonzero;
* exactly four endpoint-ordered cross-colour cells are nonzero; and
* the resulting binary source is exact (constant words have amplitude one,
  all other binary words have amplitude zero).

The audit has two logically separate parts.  First, a characteristic-free
singleton-monomial census classifies the possible four-cell supports.  Then a
constructive graph calculation, not a dimension comparison, proves that every
exact point on the surviving support is a target-preserving diagonal-gauge
image of the fixed representative.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "results.json"
N = 8


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def edge(u, v):
    return (u, v) if u < v else (v, u)


EDGES = tuple(itertools.combinations(range(N), 2))


def perfect_matchings_recursive(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    out = []
    for index, partner in enumerate(vertices[1:]):
        rest = vertices[1:index + 1] + vertices[index + 2:]
        for matching in perfect_matchings_recursive(rest):
            out.append((edge(first, partner),) + matching)
    return tuple(out)


def perfect_matchings_permutation_quotient():
    """Independent 8!-permutation construction used as an engine control."""
    out = set()
    for permutation in itertools.permutations(range(N)):
        matching = tuple(sorted(edge(permutation[2 * i], permutation[2 * i + 1])
                                for i in range(N // 2)))
        out.add(matching)
    return tuple(sorted(out))


PMS = tuple(sorted(perfect_matchings_recursive(range(N))))
PMS_SECOND = perfect_matchings_permutation_quotient()
require(len(PMS) == 105, "K8 must have 105 perfect matchings")
require(PMS == PMS_SECOND, "the two perfect-matching engines disagree")


M0 = frozenset((edge(0, 1), edge(2, 3), edge(4, 5), edge(6, 7)))
M1 = frozenset((edge(0, 3), edge(1, 2), edge(4, 7), edge(5, 6)))

# Every tuple is (left site, right site, left colour, right colour), with the
# sites in increasing order.  Thus the two cross types on an edge are truly
# endpoint ordered.
DIAGONAL_CELLS = tuple(
    [(u, v, 0, 0) for (u, v) in sorted(M0)]
    + [(u, v, 1, 1) for (u, v) in sorted(M1)]
)
CROSS_PLACES = tuple(
    (u, v, a, b)
    for (u, v) in EDGES
    for (a, b) in ((0, 1), (1, 0))
)
CROSS_ID = {cell: index for index, cell in enumerate(CROSS_PLACES)}

FIXED_CROSS = frozenset((
    (0, 4, 0, 1),
    (0, 5, 1, 0),
    (1, 7, 0, 1),
    (3, 4, 1, 0),
))
FIXED_CELLS = DIAGONAL_CELLS + tuple(sorted(FIXED_CROSS))
FIXED_VALUE = {cell: Fraction(1) for cell in FIXED_CELLS}
FIXED_VALUE[(1, 7, 0, 1)] = Fraction(-1)
FIXED_VALUE[(3, 4, 1, 0)] = Fraction(-1)


def cell_for_word(edge_value, word):
    u, v = edge_value
    return (u, v, word[u], word[v])


def amplitude(values, word):
    total = Fraction(0)
    for matching in PMS:
        term = Fraction(1)
        for e in matching:
            value = values.get(cell_for_word(e, word), Fraction(0))
            if value == 0:
                term = Fraction(0)
                break
            term *= value
        total += term
    return total


def is_exact(values):
    bad = []
    for word in itertools.product(range(2), repeat=N):
        target = Fraction(1) if len(set(word)) == 1 else Fraction(0)
        got = amplitude(values, word)
        if got != target:
            bad.append((word, got, target))
    return bad


def cross_templates():
    """Matching terms available with the fixed diagonals and arbitrary crosses.

    A term is represented only by the bitmask of cross cells it needs.  We
    retain repeated masks: singleton obstruction means exactly one matching
    term, so its coefficient is literally 1 over Z.
    """
    out = []
    for word in itertools.product(range(2), repeat=N):
        if len(set(word)) == 1:
            continue
        masks = []
        for matching in PMS:
            mask = 0
            valid = True
            for e in matching:
                cell = cell_for_word(e, word)
                if cell in DIAGONAL_CELLS:
                    continue
                cross_index = CROSS_ID.get(cell)
                if cross_index is None:
                    valid = False
                    break
                mask |= 1 << cross_index
            if valid:
                masks.append(mask)
        if masks:
            out.append((word, tuple(masks)))
    return tuple(out)


TEMPLATES = cross_templates()


def tuple_to_mask(indices):
    mask = 0
    for index in indices:
        mask |= 1 << index
    return mask


def support_mask(cells):
    return tuple_to_mask(CROSS_ID[cell] for cell in cells)


def singleton_witness(mask):
    """Return a mixed word having exactly one supported matching term."""
    for word, term_masks in TEMPLATES:
        count = 0
        for term_mask in term_masks:
            if term_mask & ~mask == 0:
                count += 1
                if count > 1:
                    break
        if count == 1:
            return word
    return None


def raw_survivor_census(size):
    survivors = []
    first_killed = None
    total = 0
    for indices in itertools.combinations(range(len(CROSS_PLACES)), size):
        total += 1
        mask = tuple_to_mask(indices)
        witness = singleton_witness(mask)
        if witness is None:
            survivors.append(mask)
        elif first_killed is None:
            first_killed = (mask, witness)
    return total, tuple(survivors), first_killed


def act_edge(permutation, e):
    return edge(permutation[e[0]], permutation[e[1]])


def act_cell(cell, permutation, colour_swap):
    u, v, a, b = cell
    if colour_swap:
        a, b = 1 - a, 1 - b
    pu, pv = permutation[u], permutation[v]
    if pu < pv:
        return (pu, pv, a, b)
    return (pv, pu, b, a)


def standard_stabilizer():
    out = []
    for permutation in itertools.permutations(range(N)):
        image0 = frozenset(act_edge(permutation, e) for e in M0)
        image1 = frozenset(act_edge(permutation, e) for e in M1)
        if image0 == M0 and image1 == M1:
            out.append((permutation, False))
        if image0 == M1 and image1 == M0:
            out.append((permutation, True))
    return tuple(out)


STABILIZER = standard_stabilizer()


def component_sizes(edges_value):
    adjacency = {vertex: set() for vertex in range(N)}
    for u, v in edges_value:
        adjacency[u].add(v)
        adjacency[v].add(u)
    sizes = []
    unseen = set(range(N))
    while unseen:
        root = min(unseen)
        stack = [root]
        component = set()
        while stack:
            vertex = stack.pop()
            if vertex in component:
                continue
            component.add(vertex)
            stack.extend(adjacency[vertex] - component)
        unseen -= component
        sizes.append(len(component))
    return tuple(sorted(sizes))


def all_ordered_44_diagonal_pairs():
    out = set()
    matching_sets = tuple(frozenset(matching) for matching in PMS)
    for first in matching_sets:
        for second in matching_sets:
            if first & second:
                continue
            if component_sizes(first | second) == (4, 4):
                out.add((first, second))
    return frozenset(out)


def standard_diagonal_pair_orbit():
    out = set()
    for permutation in itertools.permutations(range(N)):
        image0 = frozenset(act_edge(permutation, e) for e in M0)
        image1 = frozenset(act_edge(permutation, e) for e in M1)
        out.add((image0, image1))
        out.add((image1, image0))
    return frozenset(out)


def action_maps():
    maps = []
    for permutation, colour_swap in STABILIZER:
        image = tuple(CROSS_ID[act_cell(cell, permutation, colour_swap)]
                      for cell in CROSS_PLACES)
        require(len(set(image)) == len(CROSS_PLACES),
                "a symmetry did not permute the endpoint-ordered cells")
        maps.append(image)
    return tuple(maps)


ACTION_MAPS = action_maps()


def act_mask(mask, action_map):
    out = 0
    index = 0
    remaining = mask
    while remaining:
        if remaining & 1:
            out |= 1 << action_map[index]
        remaining >>= 1
        index += 1
    return out


def orbit(mask):
    return frozenset(act_mask(mask, action_map) for action_map in ACTION_MAPS)


def orbit_count(size):
    seen = set()
    count = 0
    histogram = Counter()
    for indices in itertools.combinations(range(len(CROSS_PLACES)), size):
        mask = tuple_to_mask(indices)
        if mask in seen:
            continue
        this_orbit = orbit(mask)
        seen.update(this_orbit)
        count += 1
        histogram[len(this_orbit)] += 1
    require(len(seen) == _binomial(len(CROSS_PLACES), size),
            "orbit enumeration did not cover all supports")
    return count, dict(sorted(histogram.items()))


def _binomial(n, k):
    if k < 0 or k > n:
        return 0
    answer = 1
    for i in range(1, k + 1):
        answer = answer * (n - k + i) // i
    return answer


VARIABLE_NAMES = tuple("abcdefghijkl")
CELL_NAME = dict(zip(FIXED_CELLS, VARIABLE_NAMES))


def fixed_raw_polynomials():
    """Return every nonzero raw coefficient equation as a sparse polynomial."""
    polynomials = {}
    for word in itertools.product(range(2), repeat=N):
        terms = Counter()
        for matching in PMS:
            monomial = []
            for e in matching:
                name = CELL_NAME.get(cell_for_word(e, word))
                if name is None:
                    break
                monomial.append(name)
            else:
                terms[tuple(sorted(monomial))] += 1
        if len(set(word)) == 1:
            terms[()] -= 1
        polynomial = tuple(sorted((monomial, coefficient)
                                  for monomial, coefficient in terms.items()
                                  if coefficient))
        if polynomial:
            polynomials["".join(map(str, word))] = polynomial
    return polynomials


def polynomial_display(polynomial):
    pieces = []
    for monomial, coefficient in polynomial:
        term = "*".join(monomial) if monomial else "1"
        pieces.append(f"{coefficient:+d}*{term}")
    return " ".join(pieces).lstrip("+")


def exact_point(parameters):
    """Eight-parameter rational point on the fixed support.

    Input order is a,b,c,e,f,g,p,q.  The remaining four entries are forced by
    the two pure equations and two mixed binomials.
    """
    a, b, c, e, f, g, p, q = map(Fraction, parameters)
    require(all(value != 0 for value in (a, b, c, e, f, g, p, q)),
            "parameters must be nonzero")
    d = 1 / (a * b * c)
    h = 1 / (e * f * g)
    r = -(a * g) / p
    s = -(c * e) / q
    by_name = dict(zip(VARIABLE_NAMES, (a, b, c, d, e, f, g, h,
                                        p, q, r, s)))
    return {cell: by_name[CELL_NAME[cell]] for cell in FIXED_CELLS}


def solve_gauge(point):
    """Construct lambda_(site,colour) sending the fixed point to ``point``.

    The support graph has sixteen site-colour vertices, twelve edges, and six
    bipartite connected components.  Propagation along an edge labelled by
    point/fixed solves lambda_x lambda_y = label without taking roots.  Cycle
    consistency is precisely the two mixed binomials.
    """
    adjacency = {(site, colour): []
                 for site in range(N) for colour in range(2)}
    ratios = {}
    for cell in FIXED_CELLS:
        u, v, a, b = cell
        left, right = (u, a), (v, b)
        ratio = point[cell] / FIXED_VALUE[cell]
        require(ratio != 0, "support point contains a zero cell")
        ratios[cell] = ratio
        adjacency[left].append((right, ratio, cell))
        adjacency[right].append((left, ratio, cell))

    lambdas = {}
    components = []
    for root in sorted(adjacency):
        if root in lambdas:
            continue
        lambdas[root] = Fraction(1)
        stack = [root]
        component = []
        while stack:
            current = stack.pop()
            component.append(current)
            for neighbour, ratio, _cell in adjacency[current]:
                forced = ratio / lambdas[current]
                if neighbour in lambdas:
                    require(lambdas[neighbour] == forced,
                            "gauge propagation found an inconsistent cycle")
                else:
                    lambdas[neighbour] = forced
                    stack.append(neighbour)
        components.append(tuple(sorted(component)))

    for cell, ratio in ratios.items():
        u, v, a, b = cell
        require(lambdas[(u, a)] * lambdas[(v, b)] == ratio,
                "constructed gauge misses a support cell")
    product0 = _product(lambdas[(site, 0)] for site in range(N))
    product1 = _product(lambdas[(site, 1)] for site in range(N))
    require(product0 == 1 and product1 == 1,
            "constructed gauge is not target preserving")
    return lambdas, tuple(components)


def _product(values):
    answer = Fraction(1)
    for value in values:
        answer *= value
    return answer


def mask_cells(mask):
    return [list(CROSS_PLACES[index]) for index in range(len(CROSS_PLACES))
            if mask & (1 << index)]


def word_text(word):
    return "".join(map(str, word))


def digest_payload(payload):
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def main():
    controls_declared = (
        "two_pm_engines",
        "diagonal_pair_transitivity",
        "fixed_point_exact",
        "sign_mutation_fires",
        "outside_support_singleton_fires",
        "complete_support_census",
        "complete_symmetry_orbits",
        "survivors_equal_fixed_orbit",
        "raw_equation_rebuild",
        "constructive_gauge",
    )
    controls_ran = []

    controls_ran.append("two_pm_engines")
    all_44_pairs = all_ordered_44_diagonal_pairs()
    diagonal_pair_orbit = standard_diagonal_pair_orbit()
    require(len(all_44_pairs) == 1260,
            "ordered 4+4 diagonal-pair count changed")
    require(diagonal_pair_orbit == all_44_pairs,
            "the standard diagonal pair is not transitive on the 4+4 type")
    controls_ran.append("diagonal_pair_transitivity")
    fixed_bad = is_exact(FIXED_VALUE)
    require(not fixed_bad, f"fixed representative is not exact: {fixed_bad[:1]}")
    controls_ran.append("fixed_point_exact")

    mutation = dict(FIXED_VALUE)
    mutation[(1, 7, 0, 1)] *= -1
    mutation_bad = is_exact(mutation)
    require(mutation_bad and word_text(mutation_bad[0][0]) == "00001111",
            "the must-fire sign mutation did not hit its expected word")
    controls_ran.append("sign_mutation_fires")

    census = {}
    survivors_by_size = {}
    first_killed = {}
    for size in range(5):
        total, survivors, killed = raw_survivor_census(size)
        census[str(size)] = {"total_raw_supports": total,
                             "no_singleton_survivors": len(survivors)}
        survivors_by_size[size] = survivors
        if killed is not None:
            first_killed[str(size)] = {
                "support": mask_cells(killed[0]),
                "singleton_word": word_text(killed[1]),
            }
    require([census[str(k)]["total_raw_supports"] for k in range(5)]
            == [_binomial(56, k) for k in range(5)],
            "support census missed a raw subset")
    require(all(not survivors_by_size[k] for k in range(4)),
            "a <=3-cell support escaped the singleton obstruction")
    require(len(survivors_by_size[4]) == 32,
            "the four-cell singleton-survivor count changed")
    controls_ran.append("complete_support_census")
    controls_ran.append("outside_support_singleton_fires")

    require(len(STABILIZER) == 64,
            "standard 4+4 stabilizer size changed")
    orbit_counts = {}
    orbit_histograms = {}
    for size in range(5):
        count, histogram = orbit_count(size)
        orbit_counts[str(size)] = count
        orbit_histograms[str(size)] = histogram
    require([orbit_counts[str(k)] for k in range(5)]
            == [1, 3, 44, 502, 6123],
            "support orbit counts disagree with the complete census")
    controls_ran.append("complete_symmetry_orbits")

    fixed_mask = support_mask(FIXED_CROSS)
    fixed_orbit = orbit(fixed_mask)
    survivor_set = frozenset(survivors_by_size[4])
    require(len(fixed_orbit) == 32,
            "fixed support orbit size changed")
    require(fixed_orbit == survivor_set,
            "singleton-surviving supports are not exactly the fixed orbit")
    controls_ran.append("survivors_equal_fixed_orbit")

    raw_polynomials = fixed_raw_polynomials()
    expected_words = ("00000000", "00001111", "11110000", "11111111")
    require(tuple(sorted(raw_polynomials)) == expected_words,
            "fixed support does not have exactly the four expected equations")
    displayed_polynomials = {
        word: polynomial_display(raw_polynomials[word])
        for word in expected_words
    }
    require(displayed_polynomials == {
        "00000000": "-1*1 +1*a*b*c*d",
        "00001111": "+1*a*b*g*h +1*b*h*i*k".lstrip("+"),
        "11110000": "+1*c*d*e*f +1*d*f*j*l".lstrip("+"),
        "11111111": "-1*1 +1*e*f*g*h",
    }, f"raw polynomial display changed: {displayed_polynomials}")
    controls_ran.append("raw_equation_rebuild")

    test_points = (
        exact_point((2, 3, 5, 7, 11, 13, 17, 19)),
        exact_point((-2, 5, 7, -3, 11, -13, 17, -19)),
        FIXED_VALUE,
    )
    gauge_components = None
    for point in test_points:
        require(not is_exact(point), "parameterized point is not exact")
        _lambdas, gauge_components = solve_gauge(point)
    require(sorted(map(len, gauge_components)) == [2, 2, 2, 2, 4, 4],
            "support gauge graph component structure changed")
    controls_ran.append("constructive_gauge")

    require(set(controls_ran) == set(controls_declared)
            and len(controls_ran) == len(controls_declared),
            "control manifest is incomplete or duplicated")

    result = {
        "status": "UNAUDITED",
        "scope": ("exact binary K8 sources with diagonal support two disjoint "
                  "4-cycles, all eight diagonal cells nonzero, and exactly "
                  "four nonzero endpoint-ordered cross-colour cells"),
        "perfect_matchings": len(PMS),
        "ordered_44_diagonal_pairs": len(all_44_pairs),
        "ordered_44_pairs_equal_standard_site_palette_orbit": True,
        "endpoint_ordered_cross_places": len(CROSS_PLACES),
        "mixed_words_with_at_least_one_template_term": len(TEMPLATES),
        "support_census": census,
        "first_killed_controls": first_killed,
        "standard_stabilizer_size": len(STABILIZER),
        "support_orbit_counts": orbit_counts,
        "support_orbit_size_histograms": orbit_histograms,
        "fixed_support_orbit_size": len(fixed_orbit),
        "four_cell_survivors_equal_fixed_orbit": True,
        "fixed_support": [list(cell) for cell in sorted(FIXED_CROSS)],
        "fixed_nonzero_cells": {
            "".join(map(str, cell)): str(FIXED_VALUE[cell])
            for cell in FIXED_CELLS
        },
        "fixed_raw_equations": displayed_polynomials,
        "saturated_reduction": [
            "a*b*c*d=1",
            "e*f*g*h=1",
            "a*g+i*k=0",
            "c*e+j*l=0",
        ],
        "constructive_gauge_components": [
            [list(node) for node in component]
            for component in gauge_components
        ],
        "orbit_conclusion": ("Every object in the stated stratum over any "
                             "field is a site-permutation/binary-palette-swap/"
                             "target-preserving diagonal-gauge image of the "
                             "fixed representative."),
        "controls": {
            "declared": list(controls_declared),
            "ran": controls_ran,
            "complete": True,
        },
    }
    result["sha256_without_digest"] = digest_payload(result)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("twisted-4+4 orbit-scope audit: PASS (exact, UNAUDITED)")
    print("raw supports k=4: 367290; singleton survivors: 32")
    print("support orbits k=4: 6123; surviving orbit: 1 (size 32)")
    print("fixed raw equations: 4; gauge proof: constructive")
    print("sha256:", result["sha256_without_digest"])


if __name__ == "__main__":
    main()
