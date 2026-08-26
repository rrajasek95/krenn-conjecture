#!/usr/bin/env python3
"""Exact Q(omega) replay of the bounded phase-base m=7 support screen.

The input supports are discovery objects.  This script quotients them by the
literal right-block seed stabilizer, combines matching terms with their exact
phase weights, and detects a decisive Laurent-monomial mixed equation.  A
remaining support is exported as a finite coefficient system; it is not
declared soluble.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
from itertools import permutations, product
import argparse
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from audit_balanced_base_oddset_luna import (  # noqa: E402
    ONE, ZERO, W, W2, PM8, qadd, qmul, qlabel,
)
from screen_phase_m7_support import SEEDS, base_available  # noqa: E402


INPUT = HERE / "results_phase_m7_support_screen.json"
OUTPUT = HERE / "results_phase_m7_support_coefficients.json"


Atom = tuple[int, int, int, int, int]


def parse_atom(label: str) -> Atom:
    match = re.fullmatch(r"([0-7])([0-7]):([01])([01])@([1-7])", label)
    if match is None:
        raise ValueError(label)
    return tuple(map(int, match.groups()))  # type: ignore[return-value]


def atom_label(item: Atom) -> str:
    return "%d%d:%d%d@%d" % item


PHASE = {
    (0, 1): ONE, (2, 3): ONE,
    (0, 2): ONE, (1, 3): W,
    (0, 3): ONE, (1, 2): W2,
    (4, 5): ONE, (4, 6): ONE, (4, 7): ONE,
    (5, 6): ONE, (5, 7): ONE, (6, 7): ONE,
}


def qneg(x):
    return (-x[0], -x[1])


def transform_atom(item: Atom, right_perm: tuple[int, ...]) -> Atom:
    u, v, a, b, valuation = item
    image = {site: site for site in range(4)}
    image.update({4 + index: 4 + right_perm[index] for index in range(4)})
    uu, vv = image[u], image[v]
    if uu < vv:
        return uu, vv, a, b, valuation
    return vv, uu, b, a, valuation


def stabilizer(seed: frozenset[Atom]):
    answer = []
    for perm in permutations(range(4)):
        if frozenset(transform_atom(item, perm) for item in seed) == seed:
            answer.append(perm)
    return tuple(answer)


def canonical(model: frozenset[Atom], group):
    images = []
    for perm in group:
        images.append(tuple(sorted(transform_atom(item, perm) for item in model)))
    return min(images)


def active_polynomials(selected: frozenset[Atom]):
    """Return (word,degree) -> Laurent polynomial over Q(omega).

    A monomial is the tuple of selected source-cell labels.  Equal monomials
    from different base completions are combined before singleton testing.
    """
    by_edge = defaultdict(list)
    for item in selected:
        by_edge[item[:2]].append(item)
    raw = defaultdict(lambda: defaultdict(lambda: ZERO))
    for matching in PM8:
        choices = []
        for u, v in matching:
            edge_choices = list(by_edge[(u, v)])
            edge_choices.append((u, v, 0, 0, 0))
            choices.append(edge_choices)
        for picked in product(*choices):
            word = [None] * 8
            degree = 0
            coefficient = ONE
            variables = []
            valid = True
            for u, v, a, b, valuation in picked:
                if valuation == 0:
                    if not base_available(u, v, a, b):
                        valid = False
                        break
                    coefficient = qmul(coefficient, PHASE[(u, v)])
                else:
                    variables.append(atom_label((u, v, a, b, valuation)))
                word[u], word[v] = a, b
                degree += valuation
            if valid and degree <= 7:
                key = (tuple(word), degree)
                monomial = tuple(sorted(variables))
                raw[key][monomial] = qadd(raw[key][monomial], coefficient)
    return {
        key: {monomial: coefficient for monomial, coefficient in polynomial.items()
              if coefficient != ZERO}
        for key, polynomial in raw.items()
    }


def word_label(word):
    return "".join(map(str, word))


def polynomial_json(polynomial):
    return [
        {"coefficient": qlabel(coefficient), "monomial": list(monomial)}
        for monomial, coefficient in sorted(polynomial.items())
    ]


def replay_model(model: frozenset[Atom]):
    polynomials = active_polynomials(model)
    mixed = {
        (word, degree): polynomial
        for (word, degree), polynomial in polynomials.items()
        if word not in ((0,) * 8, (1,) * 8) and polynomial
    }
    singleton_rows = [
        (word, degree, polynomial)
        for (word, degree), polynomial in mixed.items()
        if len(polynomial) == 1
    ]
    profile = Counter(len(polynomial) for polynomial in mixed.values())
    pure7 = polynomials.get(((1,) * 8, 7), {})
    equations = [
        {
            "word": word_label(word),
            "degree": degree,
            "terms": polynomial_json(polynomial),
        }
        for (word, degree), polynomial in sorted(
            mixed.items(), key=lambda item: (item[0][1], item[0][0]))
    ]
    return {
        "variables": sorted(atom_label(item) for item in model),
        "variable_count": len(model),
        "mixed_equation_count": len(mixed),
        "mixed_term_count_profile": {str(key): profile[key] for key in sorted(profile)},
        "singleton_rows": [
            {
                "word": word_label(word), "degree": degree,
                "terms": polynomial_json(polynomial),
            }
            for word, degree, polynomial in sorted(
                singleton_rows, key=lambda row: (row[1], row[0]))
        ],
        "pure7": polynomial_json(pure7),
        "pure7_term_count": len(pure7),
        "equations": equations,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=INPUT)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    input_data = json.loads(args.input.read_text())
    output = {
        "status": "exact coefficient replay of bounded support discovery",
        "field": "Q(omega), omega^2+omega+1=0",
        "guards": [
            "A Laurent singleton row proves that discovered support impossible because every listed source coefficient is required nonzero.",
            "A support with no singleton row is only a finite coefficient target, not a solution.",
            "No-model at a bounded support-search cap is unresolved, not UNSAT.",
        ],
        "branches": {},
    }
    for label in input_data["branches"]:
        seed_items = SEEDS[label]
        seed = frozenset(seed_items)
        group = stabilizer(seed)
        raw_models = [
            frozenset(parse_atom(item) for item in model)
            for model in input_data["branches"][label]["models"]
        ]
        orbit_map = {}
        for model in raw_models:
            orbit_map.setdefault(canonical(model, group), model)
        replays = []
        for canonical_key, model in sorted(orbit_map.items(), key=lambda item: (len(item[0]), item[0])):
            replay = replay_model(model)
            replay["canonical_support"] = [atom_label(item) for item in canonical_key]
            replays.append(replay)
        impossible = [replay for replay in replays if replay["singleton_rows"]]
        survivors = [replay for replay in replays
                     if not replay["singleton_rows"] and replay["pure7_term_count"]]
        survivors.sort(key=lambda replay: (
            replay["variable_count"], replay["mixed_equation_count"],
            replay["canonical_support"],
        ))
        source = input_data["branches"][label]
        output["branches"][label] = {
            "seed_stabilizer_order": len(group),
            "raw_discovery_models": len(raw_models),
            "discovered_orbits": len(replays),
            "minimum_cells": source["minimum_cells"],
            "support_search_visits": source["visits"],
            "support_search_seen": source["seen"],
            "support_search_state_cap_hit": source["visits"] >= 2500,
            "exact_singleton_impossible_orbits": len(impossible),
            "coefficient_target_orbits": len(survivors),
            "pure7_zero_orbits": len(replays) - len(impossible) - len(survivors),
            "impossible_witnesses": [
                {"support": replay["canonical_support"],
                 "row": replay["singleton_rows"][0]}
                for replay in impossible
            ],
            "smallest_coefficient_system": survivors[0] if survivors else None,
            "coefficient_systems": survivors,
            "survivor_profiles": [
                {
                    "support": replay["canonical_support"],
                    "variables": replay["variable_count"],
                    "equations": replay["mixed_equation_count"],
                    "term_profile": replay["mixed_term_count_profile"],
                    "pure7_terms": replay["pure7_term_count"],
                }
                for replay in survivors
            ],
        }
        print(label, len(replays), len(impossible), len(survivors))
    args.output.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
