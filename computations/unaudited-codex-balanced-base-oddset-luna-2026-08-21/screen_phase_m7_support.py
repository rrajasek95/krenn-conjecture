#!/usr/bin/env python3
"""Bounded singleton-closure discovery for the eight phase-base m=7 seeds.

This is a support screen only.  A closed support means every binary mixed
coefficient through order seven has zero or at least two matching monomials;
it does not prove that their coefficients cancel.
"""

from __future__ import annotations

from collections import defaultdict
from heapq import heappop, heappush
from itertools import permutations, product
import argparse
import json
from pathlib import Path
import sys
import time

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from audit_balanced_base_oddset_luna import (  # noqa: E402
    ONE, ZERO, W, W2, PM8, qadd, qmul,
)


OUT = HERE / "results_phase_m7_support_screen.json"

PHASE = {
    (0, 1): ONE, (2, 3): ONE,
    (0, 2): ONE, (1, 3): W,
    (0, 3): ONE, (1, 2): W2,
    (4, 5): ONE, (4, 6): ONE, (4, 7): ONE,
    (5, 6): ONE, (5, 7): ONE, (6, 7): ONE,
}


def base_available(u, v, a, b):
    return a == b == 0 and ((u < 4 and v < 4) or (u >= 4 and v >= 4))


def atom(u, v, a, b, valuation):
    return (u, v, a, b, valuation)


def transform_atom(item, right_perm):
    u, v, a, b, valuation = item
    image = {site: site for site in range(4)}
    image.update({4 + index: 4 + right_perm[index] for index in range(4)})
    uu, vv = image[u], image[v]
    if uu < vv:
        return uu, vv, a, b, valuation
    return vv, uu, b, a, valuation


def seed_stabilizer(seed):
    frozen = frozenset(seed)
    return tuple(
        perm for perm in permutations(range(4))
        if frozenset(transform_atom(item, perm) for item in frozen) == frozen
    )


def canonical_support(state, group):
    return min(
        tuple(sorted(transform_atom(item, perm) for item in state))
        for perm in group
    )


def active_terms(selected):
    by_edge = defaultdict(list)
    for item in selected:
        by_edge[item[:2]].append(item)
    terms = defaultdict(lambda: defaultdict(lambda: ZERO))
    for matching in PM8:
        choices = []
        for u, v in matching:
            edge_choices = list(by_edge[(u, v)])
            edge_choices.append((u, v, 0, 0, 0))
            choices.append(edge_choices)
        for picked in product(*choices):
            valid = True
            word = [None] * 8
            degree = 0
            used = []
            coefficient = ONE
            for u, v, a, b, valuation in picked:
                if valuation == 0 and not base_available(u, v, a, b):
                    valid = False
                    break
                if valuation == 0:
                    coefficient = qmul(coefficient, PHASE[(u, v)])
                word[u], word[v] = a, b
                degree += valuation
                if valuation:
                    used.append((u, v, a, b, valuation))
            if valid and degree <= 7:
                monomial = frozenset(used)
                key = (tuple(word), degree)
                terms[key][monomial] = qadd(terms[key][monomial], coefficient)
    return {
        key: {monomial: coefficient for monomial, coefficient in polynomial.items()
              if coefficient != ZERO}
        for key, polynomial in terms.items()
    }


def first_singleton(selected):
    terms = active_terms(selected)
    keys = sorted(terms, key=lambda key: (key[1], key[0]))
    for word, degree in keys:
        if word in ((0,) * 8, (1,) * 8):
            continue
        if len(terms[(word, degree)]) == 1:
            return word, degree, next(iter(terms[(word, degree)]))
    return None


def alternatives(word, degree, existing_term):
    answers = defaultdict(lambda: ZERO)
    for matching in PM8:
        choices = []
        for u, v in matching:
            a, b = word[u], word[v]
            values = list(range(1, degree + 1))
            if base_available(u, v, a, b):
                values.insert(0, 0)
            choices.append([(u, v, a, b, value) for value in values])
        for picked in product(*choices):
            if sum(item[4] for item in picked) != degree:
                continue
            required = frozenset(item for item in picked if item[4])
            if required != existing_term:
                coefficient = ONE
                for u, v, a, b, valuation in picked:
                    if valuation == 0:
                        coefficient = qmul(coefficient, PHASE[(u, v)])
                answers[required] = qadd(answers[required], coefficient)
    return {required for required, coefficient in answers.items()
            if coefficient != ZERO}


def creates_early_pure(selected):
    terms = active_terms(selected)
    return any(word == (1,) * 8 and degree < 7 and rows
               for (word, degree), rows in terms.items())


def close_seed(seed, state_cap=2500, model_cap=20, seconds=18,
               exhaustive_repairs=False):
    start = time.monotonic()
    group = seed_stabilizer(seed)
    queue = [(len(seed), tuple(sorted(seed)), frozenset(seed))]
    seen = {frozenset(seed)}
    models = []
    model_orbits = set()
    visits = 0
    while queue and visits < state_cap and len(models) < model_cap:
        if time.monotonic() - start > seconds:
            break
        _, _, state = heappop(queue)
        visits += 1
        witness = first_singleton(state)
        if witness is None:
            canonical = canonical_support(state, group)
            if canonical not in model_orbits:
                model_orbits.add(canonical)
                models.append(frozenset(canonical))
            continue
        word, degree, live_term = witness
        candidates = alternatives(word, degree, live_term)
        additions = []
        best = None
        for required in candidates:
            missing = required - state
            if not missing:
                continue
            size = len(missing)
            if exhaustive_repairs:
                additions.append(missing)
            elif best is None or size < best:
                best = size
                additions = [missing]
            elif not exhaustive_repairs and size == best:
                additions.append(missing)
        additions.sort(key=lambda missing: tuple(sorted(missing)))
        for missing in additions if exhaustive_repairs else additions[:80]:
            child = frozenset(set(state) | set(missing))
            if child in seen or creates_early_pure(child):
                continue
            seen.add(child)
            heappush(queue, (len(child), tuple(sorted(child)), child))
    return {
        "visits": visits,
        "seen": len(seen),
        "timed_out": bool(queue) and time.monotonic() - start > seconds,
        "state_cap_hit": bool(queue) and visits >= state_cap,
        "seed_stabilizer_order": len(group),
        "models": [
            ["%d%d:%d%d@%d" % item for item in sorted(model)]
            for model in models
        ],
        "minimum_cells": min((len(model) for model in models), default=None),
    }


def edge_cell(edge, valuation):
    return atom(edge[0], edge[1], 1, 1, valuation)


SEEDS = {
    "1123_k0_L23_R11": [
        edge_cell((0, 1), 2), edge_cell((2, 3), 3),
        edge_cell((4, 5), 1), edge_cell((6, 7), 1),
    ],
    "1123_k2_L2_R1_C13": [
        edge_cell((0, 1), 2), edge_cell((6, 7), 1),
        edge_cell((2, 4), 1), edge_cell((3, 5), 3),
    ],
    "1123_k2_L3_R1_C12": [
        edge_cell((0, 1), 3), edge_cell((6, 7), 1),
        edge_cell((2, 4), 1), edge_cell((3, 5), 2),
    ],
    "1123_k4_C1123": [
        edge_cell((0, 4), 1), edge_cell((1, 5), 1),
        edge_cell((2, 6), 2), edge_cell((3, 7), 3),
    ],
    "1222_k0_L22_R12": [
        edge_cell((0, 1), 2), edge_cell((2, 3), 2),
        edge_cell((4, 5), 1), edge_cell((6, 7), 2),
    ],
    "1222_k2_L2_R1_C22": [
        edge_cell((0, 1), 2), edge_cell((6, 7), 1),
        edge_cell((2, 4), 2), edge_cell((3, 5), 2),
    ],
    "1222_k2_L2_R2_C12": [
        edge_cell((0, 1), 2), edge_cell((6, 7), 2),
        edge_cell((2, 4), 1), edge_cell((3, 5), 2),
    ],
    "1222_k4_C1222": [
        edge_cell((0, 4), 1), edge_cell((1, 5), 2),
        edge_cell((2, 6), 2), edge_cell((3, 7), 2),
    ],
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--branch", choices=sorted(SEEDS))
    parser.add_argument("--state-cap", type=int, default=2500)
    parser.add_argument("--model-cap", type=int, default=20)
    parser.add_argument("--seconds", type=int, default=18)
    parser.add_argument("--exhaustive-repairs", action="store_true")
    parser.add_argument("--output", type=Path, default=OUT)
    args = parser.parse_args()
    result = {
        "status": "bounded support discovery only",
        "guard": (
            "A model means no singleton binary matching monomial through order "
            "seven. It is not a coefficient solution or an UNSAT certificate."
        ),
        "branches": {},
    }
    branches = ({args.branch: SEEDS[args.branch]} if args.branch else SEEDS)
    for label, seed in branches.items():
        result["branches"][label] = close_seed(
            seed, state_cap=args.state_cap, model_cap=args.model_cap,
            seconds=args.seconds, exhaustive_repairs=args.exhaustive_repairs,
        )
        print(label, result["branches"][label]["minimum_cells"],
              result["branches"][label]["visits"])
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
