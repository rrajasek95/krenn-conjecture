#!/usr/bin/env python3
"""Referee whether the frozen 16-coordinate Q is a matchgate signature."""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
BASE = HERE.parent / "unaudited-codex-n8-orbit0-normalized-78-2026-08-20"
CORE_PATH = BASE / "audit_polarized_superpair_core_identity.py"
SUPPORT6_PATH = BASE / "audit_weight0_support6_char0_component.py"
SUPPORT8_JSON = BASE / "results_weight0_lowq_char0_parametrization.json"
PAIRWISE_NOTE = HERE.parent.parent / "notes/pairwise-matchgate-compatibility.md"
OUT = HERE / "results_Q_matchgate_spinor_referee.json"
Q = Fraction


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


CORE = load("Q_matchgate_core", CORE_PATH)
S6 = load("Q_matchgate_support6", SUPPORT6_PATH)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def parity(index):
    return index.bit_count() & 1


def k4_add(left, right):
    return tuple(left[i]+right[i] for i in range(4))


def k4_neg(value):
    return tuple(-entry for entry in value)


def k4_mul(left, right):
    answer = [Q(0)]*4
    basis = ((0, 0), (1, 0), (0, 1), (1, 1))
    index_of = {value: index for index, value in enumerate(basis)}
    for i, (ri, gi) in enumerate(basis):
        for j, (rj, gj) in enumerate(basis):
            coefficient = left[i]*right[j]
            rpower, gpower = ri+rj, gi+gj
            if rpower >= 2:
                coefficient *= 2
                rpower -= 2
            if gpower >= 2:
                coefficient *= 65
                gpower -= 2
            answer[index_of[(rpower, gpower)]] += coefficient
    return tuple(answer)


def cartan(values, add, neg, mul, zero):
    # Four-bit even pure-spinor/matchgate quadric in lexicographic bit order:
    # q0000*q1111-q0011*q1100+q0101*q1010-q0110*q1001.
    return add(add(mul(values[0], values[15]),
                   neg(mul(values[3], values[12]))),
               add(mul(values[5], values[10]),
                   neg(mul(values[6], values[9]))))


def support6_values():
    entries = S6.raw_entries()
    return tuple(S6.evaluate(S6.SCREEN.q_poly(index), entries)
                 for index in range(16))


def support8_values():
    frozen = json.loads(SUPPORT8_JSON.read_text())
    values = [(Q(0), Q(0), Q(0), Q(0)) for _ in range(16)]
    for index_text, records in frozen["Q_live_values"].items():
        require(len(records) == 1, "support8 Q value stopped being monomial")
        entries = records[0]["coefficient_1_r_g_rg"]
        values[int(index_text)] = tuple(Q(numerator, denominator)
                                        for numerator, denominator in entries)
    return tuple(values)


def q_jacobian():
    polynomials = [CORE.q_orientation(tuple((index >> (3-site)) & 1
                                             for site in range(4)))
                   for index in range(16)]
    points = [
        tuple(range(1, 25)),
        tuple(((index*37+11) % 101)+1 for index in range(24)),
        tuple(((index*index+17*index+23) % 97)+1 for index in range(24)),
        tuple(((index*index*index+7*index+5) % 103)+1
              for index in range(24)),
    ]
    records = []
    best = None
    for point in points:
        matrix = sp.zeros(16, 24)
        for row, poly in enumerate(polynomials):
            for column in range(24):
                value = 0
                for monomial, coefficient in poly.items():
                    multiplicity = monomial.count(column)
                    if not multiplicity:
                        continue
                    factors = list(monomial)
                    factors.remove(column)
                    term = coefficient*multiplicity
                    for variable in factors:
                        term *= point[variable]
                    value += term
                matrix[row, column] = value
        rank = matrix.rank()
        records.append({"point": point, "rank": rank})
        if best is None or rank > best[0]:
            best = (rank, point, matrix)
    rank, point, matrix = best
    require(rank == 16, ("Q map Jacobian did not reach full rank", records))
    _, pivots = matrix.rref()
    require(len(pivots) == 16, "Q Jacobian pivot count changed")
    determinant = int(matrix[:, list(pivots)].det())
    require(determinant != 0, "stored Q Jacobian minor vanished")
    return point, pivots, determinant, records


def tensor_covariance_check():
    checked = 0
    for index in range(16):
        bits = tuple((index >> (3-site)) & 1 for site in range(4))
        poly = CORE.q_orientation(bits)
        require(len(poly) == 3, "Q coordinate ceased to have three matchings")
        for monomial in poly:
            observed = {}
            for variable in monomial:
                edge_index, entry_index = divmod(variable, 4)
                left, right = CORE.SUPER_EDGES[edge_index]
                left_bit, right_bit = divmod(entry_index, 2)
                require(left not in observed and right not in observed,
                        "Q monomial repeated a site")
                observed[left] = left_bit
                observed[right] = right_bit
            require(tuple(observed[site] for site in range(4)) == bits,
                    "Q monomial is not a four-site tensor coordinate")
            checked += 1
    require(checked == 48, "Q tensor covariance monomial census changed")
    return checked


def main():
    HERE.mkdir(parents=True, exist_ok=True)
    s6 = support6_values()
    s6_support = tuple(index for index, value in enumerate(s6)
                       if value != S6.ZERO)
    require(s6_support == (3, 5, 6, 9, 10, 12),
            "support6 example changed")
    s6_parities = sorted({parity(index) for index in s6_support})
    s6_cartan = cartan(s6, S6.k_add, S6.k_neg, S6.k_mul, S6.ZERO)
    require(s6_parities == [0] and s6_cartan == (Q(4), Q(0)),
            "support6 matchgate countercheck changed")

    s8 = support8_values()
    zero4 = (Q(0), Q(0), Q(0), Q(0))
    s8_support = tuple(index for index, value in enumerate(s8)
                       if value != zero4)
    require(s8_support == (1, 3, 4, 5, 6, 9, 10, 12),
            "support8 example changed")
    s8_parities = sorted({parity(index) for index in s8_support})
    s8_cartan = cartan(s8, k4_add, k4_neg, k4_mul, zero4)
    require(s8_parities == [0, 1] and
            s8_cartan == (Q(4), Q(0), Q(0), Q(0)),
            "support8 matchgate countercheck changed")

    point, pivots, determinant, rank_records = q_jacobian()
    tensor_monomials = tensor_covariance_check()
    result = {
        "status": "UNAUDITED exact Q matchgate/spinor referee PASS",
        "Q_definition": (
            "Q_s is the sum over the three perfect matchings of K4 of the "
            "two selected block entries, one selected clone at each site"),
        "four_tensor_covariance": {
            "representation": "V0 tensor V1 tensor V2 tensor V3",
            "checked_monomials": tensor_monomials,
            "conclusion": (
                "Independent GL2 changes at the four supervertices act on "
                "Q as an ordinary four-qubit tensor."),
        },
        "standard_even_cartan_quadric": (
            "q0000*q1111-q0011*q1100+q0101*q1010-q0110*q1001"),
        "support6": {
            "field": "Q[z]/(z^2+2z-1)",
            "support": list(s6_support), "support_parities": s6_parities,
            "parity_condition": "PASS (even)",
            "cartan_quadric_value": [str(value) for value in s6_cartan],
            "matchgate_verdict": (
                "FAIL: definite parity holds, but the arity-four pure-"
                "spinor/Grassmann-Plucker quadric equals 4, not 0."),
        },
        "support8": {
            "field": "Q(r,g), r^2=2,g^2=65, at u=v=w=t=1",
            "support": list(s8_support), "support_parities": s8_parities,
            "parity_condition": "FAIL (mixed even and odd)",
            "even_cartan_expression_value": [str(value)
                                               for value in s8_cartan],
            "matchgate_verdict": (
                "FAIL twice: mixed parity already excludes a matchgate "
                "signature, and its even coordinates give Cartan value 4."),
        },
        "dominance": {
            "source_dimension": 24, "target_dimension": 16,
            "jacobian_point_entries_1_through_24": list(point),
            "rank_over_Q": 16, "pivot_columns_zero_based": list(pivots),
            "pivot_minor_determinant": determinant,
            "tested_point_ranks": [{"point": list(record["point"]),
                                      "rank": record["rank"]}
                                     for record in rank_records],
            "conclusion": (
                "The polynomial map from six arbitrary 2x2 blocks to Q is "
                "dominant. Hence Q satisfies no universal nonzero polynomial "
                "identity such as a matchgate quadric."),
        },
        "nearest_applicable_theorem": {
            "negative_test": (
                "The arity-four matchgate/pure-spinor characterization: "
                "definite parity plus the single Cartan quadric is necessary "
                "and sufficient in a nonzero chart. It excludes both frozen "
                "examples rather than furnishing an identity for Q."),
            "positive_structure": (
                "Q is an ordinary four-qubit covariant. General four-qubit "
                "tensor invariant/SLOCC theory applies, but dominance means "
                "it provides invariants, not universal vanishing equations."),
            "paired_pfaffian_caution": (
                "Proposition 1.2 of notes/pairwise-matchgate-compatibility.md "
                "applies to a full normalized transversal chart as a paired "
                "restriction of a 2n-node Pfaffian signature; it does not "
                "turn this signless Hafnian Q into a standard four-bit "
                "matchgate signature."),
        },
        "source_hashes": {
            "core": sha256(CORE_PATH.read_bytes()).hexdigest(),
            "support6": sha256(SUPPORT6_PATH.read_bytes()).hexdigest(),
            "support8": sha256(SUPPORT8_JSON.read_bytes()).hexdigest(),
            "paired_note": sha256(PAIRWISE_NOTE.read_bytes()).hexdigest(),
        },
        "must_fire": ["support6 Cartan residual is exactly 4",
                      "support8 parity is mixed",
                      "support8 even Cartan expression is exactly 4",
                      "generic Q Jacobian rank is 16"],
        "scope_guard": (
            "This classifies Q itself. It does not rule out a source-relative "
            "paired-Pfaffian identity retaining the six block matrices or "
            "other lower-sector data."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode()).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print("Q matchgate/spinor referee: PASS")
    print("support6/support8 Cartan", s6_cartan, s8_cartan)
    print("Q Jacobian rank/det", 16, determinant)
    print("result", result["result_sha256"])


if __name__ == "__main__":
    main()
