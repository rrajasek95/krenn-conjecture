#!/usr/bin/env python3
"""Close the order-at-most-four hybrid-u Spencer-operator escape.

This is a small exact corollary of
``verify_h3_apolarity_operator_split_verdict.py``.  In its bounded h=3
model put I=(A,B), where A is independent of the homogenizer u and B is
linear in u.  Write a polynomial differential operator in left-normal
Weyl form

    D = sum_T c_T partial_T.

For the weight shift which can contribute the unit D(A)=1, an edge-only
term of order <=4 is zero below order four and has constant coefficient at
order four.  The cited exact ideal-level calculation proves that the A^2
condition forces all ninety unit-producing order-four coefficients to
zero.  Every term whose derivative multiset contains partial_u annihilates
both A and A^2, so such terms cannot change either the unit or that forcing
condition.  Derivatives in edge variables absent from A do the same.

Consequently no arbitrary-coefficient operator of total order <=4,
allowing u and every edge variable of the bounded ring, can satisfy

    D(I^2) subset I,       D(A)=1.

The statement is deliberately limited to order <=4.  Edge derivatives of
order 5--8 can annihilate A while acting nontrivially on A^2 and may repair
the order-four obstruction; they are not covered here.
"""

from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXPECTED_BASE_DIGEST = (
    "5330ee72132733966ab93a86740a819ebc7341815122564721adbb8af332b4e5"
)
EXPECTED_LEDGER_SHA256 = (
    "13038f8137f270168ed7c5083d22dcad8c10d7a39f722a8c425d30a56d8094ca"
)


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BASE = load(
    "h3_hybrid_order4_base",
    "verify_h3_apolarity_operator_split_verdict.py",
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def audit():
    base_ledger, base_digest = BASE.audit()
    require(base_digest == EXPECTED_BASE_DIGEST,
            "the pinned apolarity split verdict changed")

    u = BASE.HASSE.HOMOGENIZING_U
    a_variables = {item for term in BASE.A for item in term}
    pure_variables = {
        item for term in BASE.HASSE.H_PURE for item in term
    }
    ring_variables = a_variables | pure_variables | {u}

    require(len(a_variables) == 27,
            "the mixed A-support no longer has 27 edge variables")
    require(len(pure_variables) == 27,
            "the pure B-support no longer has 27 edge variables")
    require(a_variables.isdisjoint(pure_variables),
            "the selected mixed and pure edge supports began to overlap")
    require(len(ring_variables) == 55,
            "the bounded hybrid ring no longer has 55 variables")
    require(all(len(term) == 4 for term in BASE.A),
            "A stopped being quartic")
    require(all(len(set(term)) == 4 for term in BASE.A),
            "A stopped being squarefree")

    # u and every variable outside supp(A) annihilate A.  Since
    # partial_u is the first factor in any commuting derivative multiset
    # containing u, such a multiset also annihilates A^2.
    require(BASE.HASSE.derivative(BASE.A, u) == {},
            "partial_u A became nonzero")
    a_squared = BASE.HASSE.multiply(BASE.A, BASE.A)
    require(BASE.HASSE.derivative(a_squared, u) == {},
            "partial_u(A^2) became nonzero")
    for variable in pure_variables:
        require(BASE.HASSE.derivative(BASE.A, variable) == {},
                "an edge outside supp(A) differentiates A")
        require(BASE.HASSE.derivative(a_squared, variable) == {},
                "an edge outside supp(A) differentiates A^2")

    # Recompute the complete unit-producing order-four support: precisely
    # the ninety matching monomials of A, each with derivative one.
    unit_support = []
    for term in sorted(BASE.A):
        derivative = BASE.HASSE.derivatives(BASE.A, term)
        require(derivative == {(): 1},
                "one A-monomial no longer differentiates A to one")
        unit_support.append(term)
    require(len(unit_support) == 90,
            "the order-four unit support changed")

    ideal = base_ledger["ideal_level"]
    require(ideal["assembled_rank_over_Q"] == 90,
            "the exact A^2 forcing rank changed")
    require(ideal["forced_trace"] == "0",
            "the base theorem no longer forces zero unit trace")

    ledger = {
        "model": base_ledger["model"],
        "base_digest": base_digest,
        "ring_variables": len(ring_variables),
        "A_variables": len(a_variables),
        "pure_B_variables": len(pure_variables),
        "A_degree": 4,
        "A_squarefree": True,
        "unit_support_order4": len(unit_support),
        "u_annihilates_A": True,
        "u_annihilates_A_squared": True,
        "outside_A_edges_annihilate_A_and_A_squared": len(pure_variables),
        "A_squared_forcing_rank_Q": ideal["assembled_rank_over_Q"],
        "forced_unit_trace": ideal["forced_trace"],
        "theorem": (
            "in left-normal Weyl form, every derivative term containing "
            "u or an edge outside supp(A) annihilates A and A^2; the "
            "weight-shift -4 part of every remaining total-order<=4 term "
            "is zero below order4 and constant at order4; the pinned exact "
            "A^2 forcing system has rank90 and kills all 90 unit-producing "
            "coefficients; hence no arbitrary-polynomial-coefficient "
            "operator of total order<=4 on all 55 bounded variables has "
            "D(I^2) subset I and D(A)=1"
        ),
        "scope": (
            "bounded h=3 direct-free model only; closes the hybrid-u "
            "order<=4 coefficient-prolonging/Spencer operator escape; "
            "does not close order5--8 edge corrections, the R-linear "
            "generator-level Hasse totalization, a larger physical source "
            "resolution, or Krenn's conjecture"
        ),
    }
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode("ascii")).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "the hybrid order-four ledger changed")
    return ledger, digest


def main():
    ledger, digest = audit()
    print("h=3 hybrid-u order<=4 operator no-go: PASS (exact)")
    print("bounded variables:", ledger["ring_variables"])
    print("unit-producing order-four terms:",
          ledger["unit_support_order4"])
    print("A^2 forcing rank / forced trace:",
          ledger["A_squared_forcing_rank_Q"],
          ledger["forced_unit_trace"])
    print("sha256:", digest)


if __name__ == "__main__":
    main()
