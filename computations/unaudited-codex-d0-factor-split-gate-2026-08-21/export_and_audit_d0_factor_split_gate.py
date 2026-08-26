#!/usr/bin/env python3
"""Audit the D0 Laurent involution and export one exact residual gate.

The audit is coefficient-ledger based: Laurent images are compared after a
single monomial/scalar normalization, without numerical specialization.
"""

from __future__ import annotations

from collections import defaultdict
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
EXHAUST = ROOT / "unaudited-codex-d0-exhaustiveness-gcd-2026-08-21"
PACKET = ROOT / "unaudited-codex-d0-branchwise-omitted-2026-08-21"
SOURCE = (ROOT / "unaudited-codex-root-integration-2026-08-20" /
          "probe_branch0_cycle_d0_c0_pivot.py")
FACTOR_RESULT = EXHAUST / "results_d0_alternative_resultant_gcd.json"
OMITTED = PACKET / "d0_omitted_rows.json"


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


P = load("d0_factor_split_source", SOURCE)
sp = P.sp


def decode_ledger(record, b0, d1, d4):
    value = sp.Integer(0)
    for term in record["coefficient_ledger"]:
        e0, e1, e2 = term["monomial_b0_d1_d4"]
        value += term["coefficient"] * b0**e0 * d1**e1 * d4**e2
    return sp.expand(value)


def term_dict(poly, variables):
    return {tuple(map(int, exponents)): int(coefficient)
            for exponents, coefficient in sp.Poly(poly, *variables).terms()
            if coefficient}


def image_dict(poly, variables):
    """Image under (b0,d1,d4)->(-b0^-1,-d1,d4^-1)."""
    answer = defaultdict(int)
    for (e0, e1, e2), coefficient in term_dict(poly, variables).items():
        answer[(-e0, e1, -e2)] += coefficient * (-1)**(e0 + e1)
    return {key: value for key, value in answer.items() if value}


def normalized_relation(left, right):
    """Return left = scalar * monomial^shift * right, or fail."""
    if not left or not right or len(left) != len(right):
        return None
    le = min(left)
    re = min(right)
    shift = tuple(a - b for a, b in zip(le, re))
    rc = right[re]
    lc = left[le]
    scalar = sp.Rational(lc, rc)
    for exponent, coefficient in right.items():
        target = tuple(a + b for a, b in zip(exponent, shift))
        if left.get(target) != scalar * coefficient:
            return None
    return {"scalar": [int(scalar.p), int(scalar.q)], "shift": list(shift)}


def relation(poly, target, variables):
    return normalized_relation(image_dict(poly, variables),
                               term_dict(target, variables))


def profile(poly, variables):
    p = sp.Poly(poly, *variables)
    return {"terms": len(p.terms()), "total_degree": p.total_degree(),
            "multidegree": [p.degree(v) for v in variables]}


def encode(poly):
    return str(sp.expand(poly)).replace("**", "^")


def logical_hash(payload):
    return sha256(json.dumps(payload, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def main():
    variables, residual, _ = P.P.derive()
    b0, d1, d4, a0, a5 = variables
    base_variables = (b0, d1, d4)
    equations = [value for _, value in residual]
    matrix, rhs = sp.linear_eq_to_matrix(equations, [a0, a5])
    augmented = matrix.row_join(rhs)
    pivot_rows = (1, 4)
    pivot = sp.primitive(sp.Poly(matrix[list(pivot_rows), :].det(),
                                 *base_variables))[1].as_expr()

    data = json.loads(FACTOR_RESULT.read_text())["exact_pairwise_factorization"]
    A = decode_ledger(data["A"], *base_variables)
    B = decode_ledger(data["B"], *base_variables)
    U = [decode_ledger(row, *base_variables)
         for row in data["reduced_rows_U0_U1_U2_U3"]]
    omitted_json = json.loads(OMITTED.read_text())
    cofactors = {row["source_label"]:
                 sp.sympify(row["polynomial"].replace("^", "**"))
                 for row in omitted_json["rows"]}

    involution = {
        "map": {"b0": "-b0^-1", "d1": "-d1", "d4": "d4^-1"},
        "A_to_B": relation(A, B, base_variables),
        "B_to_A": relation(B, A, base_variables),
        "U2_to_U1": relation(U[2], U[1], base_variables),
        "U1_to_U2": relation(U[1], U[2], base_variables),
        "pivot_to_pivot": relation(pivot, pivot, base_variables),
        "cofactor_relations": {},
    }
    labels = [f"cofactor_{i}_3" for i in range(1, 5)]
    for source_label in labels:
        involution["cofactor_relations"][source_label] = {}
        for target_label in labels:
            answer = relation(cofactors[source_label], cofactors[target_label],
                              base_variables)
            if answer is not None:
                involution["cofactor_relations"][source_label][target_label] = answer

    required = [involution[key] for key in
                ("A_to_B", "B_to_A", "U2_to_U1", "U1_to_U2",
                 "pivot_to_pivot")]
    if any(value is None for value in required):
        raise AssertionError("candidate Laurent involution failed a required row")
    packet0 = ("cofactor_1_3", "cofactor_2_3", "cofactor_3_3")
    # This is the involutive mate among the four already-frozen two-prime
    # minimal triples.  It need not be the packet used by the older exact
    # factor-1 gate.
    packet1 = ("cofactor_1_3", "cofactor_3_3", "cofactor_4_3")
    mapped_packet = set()
    for label in packet0:
        choices = set(involution["cofactor_relations"][label])
        mapped_packet.update(choices & set(packet1))
    involution["packet0_to_packet1_set"] = sorted(mapped_packet)
    involution["packet_covariant"] = mapped_packet == set(packet1)
    if not involution["packet_covariant"]:
        raise AssertionError("minimal cofactor packet is not involution-covariant")

    # One representative residual gate.  The involution covers B=U1=0 iff
    # the packet covariance check above passes.
    z = sp.Symbol("z")
    rows = [A, U[2]] + [cofactors[label] for label in packet0] + [z*pivot - 1]
    gate = HERE / "d0_A_U2_three_cofactor_pivot_open_char0.msolve"
    gate.write_text("z,b0,d1,d4\n0\n" +
                    ",\n".join(encode(row) for row in rows) + "\n")

    result = {
        "involution": involution,
        "gate": {
            "input": gate.name,
            "sha256": sha256(gate.read_bytes()).hexdigest(),
            "rows": ["A", "U2", *packet0, "z*selected_pivot-1"],
            "profiles": [profile(row, (z, *base_variables)) for row in rows],
        },
        "sources": {
            "source": {"path": str(SOURCE),
                       "sha256": sha256(SOURCE.read_bytes()).hexdigest()},
            "factor_result": {"path": str(FACTOR_RESULT),
                              "sha256": sha256(FACTOR_RESULT.read_bytes()).hexdigest()},
            "omitted": {"path": str(OMITTED),
                        "sha256": sha256(OMITTED.read_bytes()).hexdigest()},
        },
        "scope": ("Exact reduced-chart Laurent covariance and one A=U2=0 "
                  "pivot-open source gate.  The A,B-open/all-Ui branch is not touched."),
    }
    result["logical_sha256"] = logical_hash(result)
    (HERE / "results_d0_factor_split_gate_export.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("D0 factor split export PASS", result["logical_sha256"])
    print("packet covariant", involution["packet_covariant"])
    print(json.dumps({key: involution[key] for key in
                      ("A_to_B", "U2_to_U1", "pivot_to_pivot")},
                     indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
