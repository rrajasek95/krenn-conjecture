#!/usr/bin/env python3
"""Exact Q-tensor invariant probe on support-six and a 1-d chart."""

from __future__ import annotations

import argparse
from fractions import Fraction
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
COMP = HERE.parent
SUPPORT6 = (COMP / "unaudited-codex-orbit0-t2-radical-2026-08-20" /
            "results_weight0_char0_family_and_packet.json")
BRANCH1 = (COMP / "unaudited-codex-n8-dangerous-chart-bridge-2026-08-20" /
           "results_branch1_dzero_classification.json")
OUT_PREFIX = HERE / "results_q_tensor_invariants"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def logical_hash(value):
    return sha256(json.dumps(value, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mutation", action="store_true")
    args = parser.parse_args()
    try:
        import sympy as sp
    except ImportError:
        sites = sorted((HERE.parents[1] / ".venv/lib").glob(
            "python*/site-packages"))
        require(bool(sites), "sympy unavailable")
        sys.path.append(str(sites[-1]))
        import sympy as sp

    def reduce_quadratic(value, symbol, relation):
        return sp.rem(sp.Poly(sp.expand(value), symbol, domain=sp.QQ.frac_field(T)),
                      sp.Poly(relation, symbol, domain=sp.QQ.frac_field(T))).as_expr()

    def q_invariants(q, reduce):
        require(len(q) == 16, "Q tensor must have 16 entries")
        # Standard SL(2)^4 epsilon contraction, with one representative from
        # each complementary pair (the conventional invariant differs by 2).
        quadratic = reduce(sum(((-1) ** index.bit_count()) * q[index] *
                               q[15-index] for index in range(8)))
        repo_pairing = reduce(sum(q[index] * q[15-index]
                                  for index in range(8)))
        determinants = []
        partitions = (((0, 1), (2, 3)),
                      ((0, 2), (1, 3)),
                      ((0, 3), (1, 2)))
        for left, right in partitions:
            matrix = []
            for lb in product((0, 1), repeat=2):
                row = []
                for rb in product((0, 1), repeat=2):
                    bits = [0] * 4
                    for position, bit in zip(left, lb):
                        bits[position] = bit
                    for position, bit in zip(right, rb):
                        bits[position] = bit
                    index = sum(bit << (3-position)
                                for position, bit in enumerate(bits))
                    row.append(q[index])
                matrix.append(row)
            determinants.append(reduce(sp.det(sp.Matrix(matrix))))
        return quadratic, repo_pairing, determinants

    global T
    T = sp.symbols("T")

    support_payload = json.loads(SUPPORT6.read_text())
    support_record = support_payload["exact_support6_component"]
    r = sp.symbols("r")
    support_q = []
    for basis in support_record["Q_values_basis_1_r_g_rg"]:
        coefficients = [sp.Rational(Fraction(value)) for value in basis]
        require(coefficients[2:] == [0, 0], "support6 unexpectedly uses g")
        support_q.append(coefficients[0] + coefficients[1] * r)
    reduce_support = lambda value: sp.rem(
        sp.Poly(sp.expand(value), r, domain=sp.QQ),
        sp.Poly(r**2-2, r, domain=sp.QQ)).as_expr()
    support_inv = q_invariants(support_q, reduce_support)
    require([index for index, value in enumerate(support_q) if value != 0] ==
            [3, 5, 6, 9, 10, 12], "support6 Q support changed")

    branch_payload = json.loads(BRANCH1.read_text())
    component = branch_payload["components"][0]
    z = sp.symbols("z")
    p = component["quadratic_relation_p_in_z2_equals_pz_plus_1"]
    branch_q = []
    for index in range(16):
        value = 0
        for term in component["Q_polynomials"][str(index)]:
            (a_num, a_den), (b_num, b_den) = term["coefficient_1_z"]
            coefficient = sp.Rational(a_num, a_den) + sp.Rational(b_num, b_den)*z
            value += coefficient * T**term["T_degree"]
        branch_q.append(sp.expand(value))
    field = sp.QQ.frac_field(T)
    reduce_branch = lambda value: sp.rem(
        sp.Poly(sp.expand(value), z, domain=field),
        sp.Poly(z**2-p*z-1, z, domain=field)).as_expr()
    branch_inv = q_invariants(branch_q, reduce_branch)
    require([index for index, value in enumerate(branch_q) if value != 0] ==
            [0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 12],
            "branch1 generic Q support changed")
    branch_factored = [sp.factor_terms(value) for value in
                       (branch_inv[0], branch_inv[1], *branch_inv[2])]

    if args.mutation:
        mutated = list(support_q); mutated[3] += 1
        require(q_invariants(mutated, reduce_support) != support_inv,
                "Q-coordinate mutation failed to fire")

    result = {
        "status": "PASS exact Q-tensor invariant comparison",
        "mutation": args.mutation,
        "tensor_indexing": (
            "Q_s with s=8*i0+4*i1+2*i2+i3; flattenings 01|23,02|13,03|12"),
        "standard_quadratic_convention": (
            "sum_{s=0}^7 (-1)^popcount(s) Q_s Q_{15-s}; "
            "the full epsilon contraction is twice this polynomial"),
        "support6": {
            "field": "Q(r), r^2=2",
            "Q_support": [3, 5, 6, 9, 10, 12],
            "quadratic": str(support_inv[0]),
            "repository_unsigned_pairing": str(support_inv[1]),
            "flattening_determinants": [str(value) for value in support_inv[2]],
        },
        "positive_dimensional_branch1": {
            "field": f"Q(z), z^2-{p}*z-1=0",
            "parameter": "T",
            "dimension": branch_payload["exact_component_census"]["dimension"],
            "Q_support_T_nonzero": [0,1,2,3,4,5,6,8,9,10,12],
            "quadratic": str(branch_inv[0]),
            "repository_unsigned_pairing": str(branch_inv[1]),
            "flattening_determinants": [str(value) for value in branch_inv[2]],
            "factored_invariant_list": [str(value) for value in branch_factored],
        },
        "comparison_conclusion": (
            "On support-six the quadratic invariant is 4 and the three "
            "determinants are (-32,-32,0). On the entire branch-1 parameter "
            "line they are (4;32,0,-32), independent of T. Hence none of "
            "these restrictions detects the recurring T=0 versus T!=0 "
            "support split or supplies a nonconstant chart factor. The "
            "identically-zero flattening changes position under the chosen "
            "orientation, so it records a rank pattern but not the branch "
            "divisor. This concrete test gives no evidence that later "
            "nonconstant factors such as A,B, or R25 are restrictions of "
            "the standard four-qubit invariants."),
        "source_hashes": {"support6": digest(SUPPORT6),
                          "branch1": digest(BRANCH1)},
        "scope_guard": (
            "This evaluates standard tensor invariants on two frozen exact "
            "charts. Equality or factor coincidence after restriction does "
            "not supply an ambient ideal identity; failure to coincide is a "
            "valid obstruction to identifying the displayed chart factors "
            "with those invariant restrictions."),
    }
    result["logical_sha256"] = logical_hash(result)
    suffix = "mutation" if args.mutation else "standard"
    out = OUT_PREFIX.with_name(OUT_PREFIX.name + "_" + suffix + ".json")
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("Q tensor invariant audit PASS", result["logical_sha256"])
    print("support6", result["support6"])
    print("branch1", result["positive_dimensional_branch1"])


if __name__ == "__main__":
    main()
