#!/usr/bin/env python3
"""Verify the source-labelled Segre constraint on a recombination cube.

Two decorated occurrences of one physical matching give two cell choices on
each differing edge.  Their selected matching monomials form a rank-one
Boolean tensor.  If every resulting output word is mixed and every complete
source row vanishes, then the *sum of all other physical matchings* in those
rows is the negative of that rank-one tensor.  In particular every flattening
minor of the alternate-sum cube vanishes and every entry is nonzero.

The canonical three-cube from the multiplicity-two K6 circuit is also
replayed.  Its current six-row guard supplies the required alternate sum at
four corners and supplies zero at the other four; an exact full packet must
therefore add alternate total -1 in precisely the four frozen debt grades.
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEPENDENCY = "computations/verify_n8_one_bad_multiplicity_cube_boundary.py"
DEPENDENCY_SHA256 = "7a14bae54df2916ec03e8adf3685cc96f09fe71fdba27d507469b8d2f7715456"
EXPECTED_DIGEST = "f77b6f9f970e4d6f97720030dcbdc8c4c20f438af345d8cf36d77c27e4063d9b"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load_dependency():
    path = ROOT / DEPENDENCY
    actual = sha256(path.read_bytes()).hexdigest()
    require(actual == DEPENDENCY_SHA256,
            f"dependency changed: {DEPENDENCY}: {actual}")
    spec = spec_from_file_location("multiplicity_cube", path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def product(values):
    answer = Fraction(1)
    for value in values:
        answer *= value
    return answer


def abstract_segre_lemma():
    # Distinct nonzero primes make accidental equalities impossible while
    # retaining exact rational arithmetic.  The proof checked here is the
    # literal polynomial factorization behind every flattening minor.
    a = tuple(map(Fraction, (2, 3, 5, 7)))
    b = tuple(map(Fraction, (11, 13, 17, 19)))
    corners = tuple(itertools.product((0, 1), repeat=4))
    selected = {
        bits: product(b[index] if bit else a[index]
                      for index, bit in enumerate(bits))
        for bits in corners
    }
    alternate = {bits: -value for bits, value in selected.items()}

    minors = []
    for coordinate in range(4):
        residual = tuple(itertools.product((0, 1), repeat=3))

        def insert(bit, tail):
            values = list(tail)
            values.insert(coordinate, bit)
            return tuple(values)

        for left_index, left in enumerate(residual):
            for right in residual[left_index + 1:]:
                determinant = (
                    alternate[insert(0, left)]
                    * alternate[insert(1, right)]
                    - alternate[insert(1, left)]
                    * alternate[insert(0, right)]
                )
                require(determinant == 0,
                        "an alternate-sum Segre minor stopped vanishing")
                minors.append((coordinate, left, right))

    require(all(value for value in alternate.values()),
            "the forced alternate-sum cube left the dense torus")
    return {
        "cube_dimension": 4,
        "corners": len(corners),
        "flattening_minors_checked": len(minors),
        "all_forced_alternate_entries_nonzero": True,
        "factorization": "R_bits=-product_i(cell_i[bits_i])",
    }


def canonical_three_cube(module):
    positive_terms = tuple(
        module.decorated_term(index, word)
        for index, word in zip(module.POSITIVE, module.WORDS, strict=True)
    )
    negative_terms = tuple(
        module.decorated_term(index, word)
        for index, word in zip(module.NEGATIVE, module.WORDS, strict=True)
    )
    prescribed = tuple(
        term for pair in zip(positive_terms, negative_terms, strict=True)
        for term in pair
    )
    support = frozenset(cell for term in prescribed for cell in term)

    from collections import Counter
    occurrence = Counter(cell for term in prescribed for cell in term)
    private_negative = tuple(
        next(cell for cell in term if occurrence[cell] == 1)
        for term in negative_terms
    )
    weights = {cell: Fraction(1) for cell in support}
    for cell in private_negative:
        weights[cell] = Fraction(-1)

    first, second = positive_terms[:2]
    matching = module.MATCHINGS[module.POSITIVE[0]]
    options = []
    for edge in matching:
        options.append((
            next(cell for cell in first if cell[0] == edge),
            next(cell for cell in second if cell[0] == edge),
        ))

    table = []
    for bits in itertools.product((0, 1), repeat=3):
        selected_term = tuple(sorted(options[index][bit]
                                     for index, bit in enumerate(bits)))
        word = module.decorated_word(selected_term)
        selected_value = module.term_value(selected_term, weights)
        require(selected_value == 1,
                "the pinned selected recombination monomial changed value")
        other_terms = tuple(
            module.decorated_term(index, word)
            for index in range(len(module.MATCHINGS))
            if index != module.POSITIVE[0]
            and set(module.decorated_term(index, word)) <= support
        )
        current_alternate = sum(
            (module.term_value(term, weights) for term in other_terms),
            Fraction(0),
        )
        required_alternate = -selected_value
        table.append({
            "bits": "".join(map(str, bits)),
            "word": "".join(map(str, word)),
            "current_alternate_sum": str(current_alternate),
            "required_alternate_sum": str(required_alternate),
            "missing_alternate_debt": str(
                required_alternate - current_alternate
            ),
        })

    missing = tuple(row["bits"] for row in table
                    if row["missing_alternate_debt"] != "0")
    require(missing == ("001", "010", "101", "110"),
            f"the canonical four-corner completion debt changed: {missing}")
    require(all(row["required_alternate_sum"] == "-1" for row in table),
            "the canonical required alternate cube stopped being constant")

    # The required alternate array is a dense rank-one 2x2x2 tensor.  Check
    # all six 2x2 flattening minors in each of the three directions.
    required = {
        tuple(map(int, row["bits"])): Fraction(row["required_alternate_sum"])
        for row in table
    }
    minor_count = 0
    for coordinate in range(3):
        residual = tuple(itertools.product((0, 1), repeat=2))

        def insert(bit, tail):
            values = list(tail)
            values.insert(coordinate, bit)
            return tuple(values)

        for left_index, left in enumerate(residual):
            for right in residual[left_index + 1:]:
                require(
                    required[insert(0, left)] * required[insert(1, right)]
                    == required[insert(1, left)] * required[insert(0, right)],
                    "a canonical required alternate minor changed",
                )
                minor_count += 1

    return {
        "table": table,
        "missing_corners": list(missing),
        "required_alternate_flattening_minors_checked": minor_count,
        "exact_full_packet_condition": (
            "the aggregate of all non-doubled physical matchings on the "
            "eight recombination words is the dense rank-one tensor (-1)^8"
        ),
    }


def main():
    module = load_dependency()
    ledger = {
        "dependency": {"path": DEPENDENCY, "sha256": DEPENDENCY_SHA256},
        "abstract_dense_segre_cancellation": abstract_segre_lemma(),
        "canonical_multiplicity_cube": canonical_three_cube(module),
        "verdict": (
            "vanishing of every mixed row on a decorated recombination "
            "cube forces the aggregate cancellation mates to be a dense "
            "rank-one Segre tensor; support mates alone are insufficient"
        ),
        "scope": (
            "uniform source-labelled necessary condition plus the pinned "
            "K6 multiplicity cube; no claim that the Segre condition alone "
            "contradicts arbitrary additional source support"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST,
                f"recombination-cube ledger changed: {digest}")
    print("recombination-cube Segre cancellation: PASS")
    print("forced alternate cube: dense rank one in every flattening")
    print("canonical missing corners: 001,010,101,110; required total -1")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
