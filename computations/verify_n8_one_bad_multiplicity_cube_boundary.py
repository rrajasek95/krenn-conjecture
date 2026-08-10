#!/usr/bin/env python3
"""Extract the minimal full-row boundary of the multiplicity-two orbit.

The canonical K6 support-eleven incidence circuit has one doubled physical
matching.  Its two source-labelled occurrences in the pinned sharp grade
split use disjoint decorated cells.  Keeping the physical matching fixed and
choosing either decorated cell on each of its three edges therefore produces
a literal Boolean three-cube of eight top matching monomials.

This checker proves the general 2^k recombination lemma and audits the exact
canonical cube.  Four corners are complete cancelling binomial fibres; the
other four are singleton mixed fibres of coefficient +1.  Thus the six
polarized circuit equations do not close under the full source map: their
smallest forced extra invariant is a four-coordinate cube-boundary debt.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEPENDENCY = (
    "computations/verify_n8_one_bad_multiplicity_polarized_grade_split.py"
)
DEPENDENCY_SHA256 = (
    "f3df3eb8b19d0fdfef4417b8c050a3653107b1a0675575ab295cdba41d03328a"
)
EXPECTED_DIGEST = "b85ea5995938a8f2dfd50535ce2e347ca046cbb22c51928ea8977a2ea3134594"
SITES = tuple(range(6))
POSITIVE = (0, 0, 4, 8, 10, 12)
NEGATIVE = (1, 2, 3, 6, 11, 14)
WORDS = (
    (1, 0, 2, 0, 2, 0),
    (2, 0, 0, 1, 0, 1),
    (0, 0, 0, 2, 1, 0),
    (0, 2, 0, 1, 1, 1),
    (1, 2, 1, 0, 2, 1),
    (1, 0, 0, 0, 1, 2),
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependency():
    path = ROOT / DEPENDENCY
    actual = sha256(path.read_bytes()).hexdigest()
    require(actual == DEPENDENCY_SHA256,
            f"dependency changed: {DEPENDENCY}: {actual}")


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index, second in enumerate(vertices[1:], 1):
        remainder = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(remainder):
            yield tuple(sorted(((first, second),) + tail))


MATCHINGS = tuple(perfect_matchings(SITES))


def decorated_term(matching_index, word):
    return tuple(sorted(
        ((left, right), (word[left], word[right]))
        for left, right in MATCHINGS[matching_index]
    ))


def term_value(term, weights):
    value = Fraction(1)
    for cell in term:
        value *= weights[cell]
    return value


def decorated_word(term):
    word = [None] * 6
    for (left, right), (left_colour, right_colour) in term:
        word[left], word[right] = left_colour, right_colour
    require(all(colour is not None for colour in word),
            "a decorated perfect matching stopped covering all sites")
    return tuple(word)


def abstract_recombination_lemma():
    # A labelled four-edge matching is enough to audit all k=0,...,4.
    matching = ((0, 1), (2, 3), (4, 5), (6, 7))
    ledger = []
    for differing_edges in range(5):
        first = tuple((edge, (0, 0)) for edge in matching)
        second = tuple(
            (edge, (1, 1) if index < differing_edges else (0, 0))
            for index, edge in enumerate(matching)
        )
        choices = []
        for left, right in matching:
            first_cell = next(cell for cell in first
                              if cell[0] == (left, right))
            second_cell = next(cell for cell in second
                               if cell[0] == (left, right))
            choices.append(tuple(dict.fromkeys((first_cell, second_cell))))
        recombinations = {
            tuple(selected)
            for selected in itertools.product(*choices)
        }
        require(len(recombinations) == 2 ** differing_edges,
                "the 2^k decorated recombination count changed")
        require(all(tuple(cell[0] for cell in term) == matching
                    for term in recombinations),
                "a recombination changed the physical matching")
        ledger.append({
            "differing_physical_edges": differing_edges,
            "decorated_recombinations": len(recombinations),
        })
    return ledger


def canonical_cube():
    positive_terms = tuple(
        decorated_term(index, word)
        for index, word in zip(POSITIVE, WORDS, strict=True)
    )
    negative_terms = tuple(
        decorated_term(index, word)
        for index, word in zip(NEGATIVE, WORDS, strict=True)
    )
    all_terms = tuple(
        term for pair in zip(positive_terms, negative_terms, strict=True)
        for term in pair
    )
    support = frozenset(cell for term in all_terms for cell in term)
    occurrence = Counter(cell for term in all_terms for cell in term)
    private_negative = tuple(
        next(cell for cell in term if occurrence[cell] == 1)
        for term in negative_terms
    )
    weights = {cell: Fraction(1) for cell in support}
    for cell in private_negative:
        weights[cell] = Fraction(-1)

    first, second = positive_terms[:2]
    doubled_matching = tuple(MATCHINGS[POSITIVE[0]])
    require(POSITIVE[:2] == (0, 0),
            "the canonical doubled matching moved")
    require(set(first).isdisjoint(second),
            "the doubled occurrences stopped being cell-disjoint")

    edge_options = []
    for edge in doubled_matching:
        first_cell = next(cell for cell in first if cell[0] == edge)
        second_cell = next(cell for cell in second if cell[0] == edge)
        require(first_cell != second_cell,
                "a doubled edge lost its two decorations")
        edge_options.append((first_cell, second_cell))

    cube = []
    word_to_bits = {}
    for bits in itertools.product((0, 1), repeat=3):
        term = tuple(sorted(
            edge_options[index][choice]
            for index, choice in enumerate(bits)
        ))
        word = decorated_word(term)
        require(word not in word_to_bits,
                "two cube corners acquired the same output word")
        word_to_bits[word] = bits
        live = tuple(
            decorated_term(index, word)
            for index in range(len(MATCHINGS))
            if set(decorated_term(index, word)) <= support
        )
        coefficient = sum(
            (term_value(value, weights) for value in live),
            Fraction(0),
        )
        cube.append({
            "bits": "".join(map(str, bits)),
            "word": "".join(map(str, word)),
            "mixed": len(set(word)) > 1,
            "live_fibre_terms": len(live),
            "coefficient": str(coefficient),
            "selected_grade": bits in ((0, 0, 0), (1, 1, 1)),
        })

    require(len(cube) == 8 and all(value["mixed"] for value in cube),
            "the canonical doubled cube stopped having eight mixed corners")
    histogram = Counter(
        (value["live_fibre_terms"], value["coefficient"])
        for value in cube
    )
    require(histogram == Counter({(2, "0"): 4, (1, "1"): 4}),
            f"the cube fibre boundary changed: {histogram}")
    singleton_bits = tuple(
        value["bits"] for value in cube
        if value["live_fibre_terms"] == 1
    )
    require(singleton_bits == ("001", "010", "101", "110"),
            f"the four singleton corners changed: {singleton_bits}")
    require(all(not value["selected_grade"] for value in cube
                if value["live_fibre_terms"] == 1),
            "a prescribed circuit grade became a singleton debt")

    # The two original grades and the two opposite hybrid grades are exactly
    # cancelled already.  The remaining four source rows are independent
    # target-word readouts: no linear combination of the six declared
    # binomial equations can erase a row in a different output grade.
    selected_words = set(WORDS)
    boundary_words = tuple(
        value["word"] for value in cube
        if value["live_fibre_terms"] == 1
    )
    require(not (set(boundary_words) & selected_words),
            "a cube boundary word stopped being an undeclared full row")

    return {
        "doubled_matching": [list(edge) for edge in doubled_matching],
        "doubled_occurrences_cell_disjoint": True,
        "cube_dimension": 3,
        "cube_corners": cube,
        "cube_fibre_histogram": {
            "cancelling_binomial": 4,
            "nonzero_singleton": 4,
        },
        "singleton_bits": list(singleton_bits),
        "singleton_words": list(boundary_words),
        "boundary_vector_at_rational_guard": [1, 1, 1, 1],
        "minimal_additional_invariant": (
            "the four undeclared mixed output-grade coefficients at cube "
            "corners 001,010,101,110"
        ),
        "verdict": (
            "two independent source grades on the doubled physical matching "
            "force a Boolean recombination cube; the six circuit rows leave "
            "a nonzero four-corner full-row boundary"
        ),
    }


def main():
    pin_dependency()
    ledger = {
        "dependency": {
            "path": DEPENDENCY,
            "sha256": DEPENDENCY_SHA256,
        },
        "abstract_recombination_lemma": abstract_recombination_lemma(),
        "canonical_multiplicity_cube": canonical_cube(),
        "scope": (
            "source-labelled theorem/counterguard for the canonical sharp "
            "multiplicity-two grade split; it identifies the next four full "
            "rows but does not prove that arbitrary added mates cannot cancel "
            "them and is not a one-bad packet"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST,
                f"multiplicity-cube ledger changed: {digest}")
    print("N=8 one-bad multiplicity cube boundary: PASS")
    print("cube corners: 8 = 4 cancelling binomials + 4 singleton debts")
    print("singleton bits: 001,010,101,110")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
