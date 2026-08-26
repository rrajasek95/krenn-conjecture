#!/usr/bin/env python3
"""Exact universal mate unit on the generic left-Q support stratum.

This is deliberately independent of the two modular slices.  The eight
abstract left coefficients stand for one nonzero Q coordinate in each
complementary pair.  Substitution by the literal left Q polynomials therefore
gives a certificate over the component fraction field; exceptional Q divisors
remain outside this file's scope.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
CORE_PATH = (HERE.parent /
             "unaudited-codex-n8-orbit0-normalized-78-2026-08-20" /
             "audit_polarized_superpair_core_identity.py")
OUT = HERE / "results_generic_Qcover_fraction_field_unit.json"
SELECTED_LEFT_Q = (15, 1, 2, 3, 11, 10, 6, 7)
MATE_VARIABLE_COUNT = 24
U = 32
V = 33


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


CORE = load("generic_qcover_core", CORE_PATH)


def clean(poly):
    return Counter({tuple(sorted(monomial)): coefficient
                    for monomial, coefficient in poly.items() if coefficient})


def add(*polys):
    answer = Counter()
    for poly in polys:
        answer.update(poly)
    return clean(answer)


def scale(poly, coefficient):
    return clean(Counter({monomial: coefficient*value
                          for monomial, value in poly.items()}))


def multiply(*polys):
    answer = Counter({(): 1})
    for poly in polys:
        updated = Counter()
        for left, lc in answer.items():
            for right, rc in poly.items():
                updated[tuple(sorted(left+right))] += lc*rc
        answer = clean(updated)
    return answer


def variable(index):
    return Counter({(index,): 1})


def q(index):
    bits = tuple((index >> (3-site)) & 1 for site in range(4))
    return CORE.q_orientation(bits)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def main():
    pairs = tuple((index, 15-index) for index in range(8))
    require(all(sum(value in pair for value in SELECTED_LEFT_Q) == 1
                for pair in pairs),
            "selected left Q coordinates ceased to cover complementary pairs")
    localizer_by_left_q = {
        left_q: variable(MATE_VARIABLE_COUNT+offset)
        for offset, left_q in enumerate(SELECTED_LEFT_Q)
    }
    left_product = multiply(*localizer_by_left_q.values())
    h = CORE.pure_hafnian()
    t_rows = tuple(CORE.t_triple(*triple)
                   for triple in __import__("itertools").combinations(range(4), 3))
    e_rows = tuple(CORE.e_pair(*edge) for edge in CORE.SUPER_EDGES)

    # Build the exact source combination for L*H.  Direct t/e rows need no
    # left assumptions.  Each B_s=Q_s Q_bar(s) uses the selected directional
    # generator leftQ_j * mateQ_bar(j).
    source_combo = Counter()
    for row in t_rows:
        source_combo = add(source_combo, multiply(left_product, row))
    for (left_edge, right_edge) in CORE.COMPLEMENTARY_EDGE_PAIRS:
        left_index = CORE.SUPER_EDGES.index(left_edge)
        right_index = CORE.SUPER_EDGES.index(right_edge)
        source_combo = add(source_combo,
                           scale(multiply(left_product, e_rows[left_index],
                                          e_rows[right_index]), -1))
    directional_rows = []
    for low, high in pairs:
        chosen = low if low in localizer_by_left_q else high
        forced_mate = 15-chosen
        other_mate = chosen
        coefficient = Counter({tuple(index for index in range(
            MATE_VARIABLE_COUNT, MATE_VARIABLE_COUNT+8)
            if index != MATE_VARIABLE_COUNT+SELECTED_LEFT_Q.index(chosen)): 1})
        generator = multiply(localizer_by_left_q[chosen], q(forced_mate))
        source_combo = add(source_combo,
                           multiply(coefficient, generator, q(other_mate)))
        directional_rows.append((chosen, forced_mate))
    require(source_combo == multiply(left_product, h),
            "cleared universal Q-cover identity failed")

    u = variable(U)
    v = variable(V)
    one = Counter({(): 1})
    mate_h_rab = add(multiply(u, h), scale(one, -1))
    left_product_rab = add(multiply(v, left_product), scale(one, -1))
    unit = add(multiply(u, v, source_combo),
               scale(mate_h_rab, -1),
               scale(multiply(u, h, left_product_rab), -1))
    require(unit == one, "fraction-field Rabinowitsch unit failed")
    require(add(unit, t_rows[0]) != one, "mutation control failed")

    result = {
        "status": "UNAUDITED exact-Q generic left-Q-cover mate UNIT PASS",
        "selected_left_Q": list(SELECTED_LEFT_Q),
        "complementary_pairs": [list(pair) for pair in pairs],
        "directional_rows": [
            {"left_Q": left, "forced_mate_Q": mate}
            for left, mate in directional_rows
        ],
        "ordinary_mate_rows": {
            "triangle": 4,
            "e": 3,
            "directional_Q": 8,
            "total": 15,
        },
        "identity": (
            "L*H_mate is an explicit combination of mate t/e and the eight "
            "rows leftQ_j*mateQ_(15-j), where L=product(leftQ_j). With "
            "u*H_mate-1 and v*L-1 this gives 1 exactly."
        ),
        "literal_replay": True,
        "mutation_control": True,
        "conclusion": (
            "The universal mate incidence is empty over the fraction field "
            "of any left component on which the eight selected Q coordinates "
            "are nonzero."
        ),
        "scope_guard": (
            "This closes only the dense Q-support stratum. It does not assert "
            "that L is a unit on the full generic-cycle A=B=0 component; the "
            "eight exceptional divisors leftQ_j=0 must be reduced separately."
        ),
        "source_sha256": sha256(CORE_PATH.read_bytes()).hexdigest(),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print("generic Q-cover fraction-field mate unit: PASS")
    print("left Q", SELECTED_LEFT_Q)
    print("result", result["result_sha256"])


if __name__ == "__main__":
    main()
