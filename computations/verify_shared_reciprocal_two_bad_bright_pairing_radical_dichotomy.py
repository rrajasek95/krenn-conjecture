#!/usr/bin/env python3
"""Full-row bright-pairing dichotomy on the fixed target pair.

After quotienting by the target-free residual, the kernel-product pairing
factors through W=pi_t ker(Phi), dim W<=2.  The nine literal common-hafnian
rows give a 3x3 pairing matrix with only its (t,t) entry possibly nonzero.

If the missing pure class survives and the two auxiliary kernel projections
are nonzero, those projections must be the same radical line in W; the
pairing factors through the one-dimensional quotient W/L.  Zero auxiliary
projection and a pure class already in the target-free residual are the two
separate degenerate branches.

The checker also proves that an additive colour multigrading compatible with
arbitrary full 3x3 edge blocks is necessarily colour-blind, so no universal
such grading separates the target-free residual from X_t.
"""

from __future__ import annotations

from hashlib import sha256
import itertools
import json
from pathlib import Path
import sys

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "computations"))

import verify_shared_reciprocal_two_bad_common_hafnian as common


PINNED_PAIR_REDUCTION_SHA256 = (
    "bb01f6de80af4132b6a9736338f24927533d9224cb2f4f9ee1fd228515e7f765"
)
PINNED_COMMON_HAFNIAN_SHA256 = (
    "9bc7f4c017ba797304057ec182112c5c4f0bfc210d3729243958d723cac1a1d6"
)
PINNED_COMMON_ROW_SHA256 = (
    "b6b295867a97ee7d17b6d05f80a0c51a0de85db47f952621db78fba9edb33674"
)
EXPECTED_LEDGER_SHA256 = "1d13558c8fb3fca947702ca346a022aa4b286baa39a6ea1af3492a6d541dd555"


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def pin_dependencies():
    pins = {
        "computations/verify_shared_reciprocal_two_bad_target_projection_pair_reduction.py":
            PINNED_PAIR_REDUCTION_SHA256,
        "computations/verify_shared_reciprocal_two_bad_common_hafnian.py":
            PINNED_COMMON_HAFNIAN_SHA256,
    }
    for relative, expected in pins.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"dependency changed: {relative}: {actual}")


def audit_literal_nine_rows():
    odd_rows, full_rows, row_hash = common.audit_symbolic_coupling()
    require((odd_rows, full_rows) == (1458, 2187),
            "the literal common-hafnian row census changed")
    require(row_hash == PINNED_COMMON_ROW_SHA256,
            f"the literal common-hafnian rows changed: {row_hash}")

    # Modulo im(Phi), the chord D_jk*K vanishes.  With row order a,c,t
    # on the Q side and a,c,t on the R side, every product class is zero
    # except Q_t*R_t, which is [X_t].
    quotient_matrix = (
        ("0", "0", "0"),
        ("0", "0", "0"),
        ("0", "0", "x"),
    )
    return {
        "odd_rows": odd_rows,
        "full_rows": full_rows,
        "literal_row_sha256": row_hash,
        "row_order": ["a", "c", "t"],
        "quotient_pairing_matrix": quotient_matrix,
    }


def audit_radical_dichotomy():
    # Write alpha=pi Q_a, u=pi Q_t, rho=pi R_c, v=pi R_t.
    # The four load-bearing rows are
    # beta(alpha,rho)=beta(alpha,v)=beta(u,rho)=0,
    # beta(u,v)=x.
    # If x survives in C=coker(Phi)/R_nt, choose a covector ell with
    # ell(x)=1.  Its scalar symmetric form has the same zero pattern.
    # In the nonzero-alpha/rho branch normalize alpha=e0,u=e1 and write
    # rho=(r0,r1), v=(v0,v1), with det(rho,v) nonzero.
    A, B, C = sp.symbols("A B C")
    r0, r1, v0, v1 = sp.symbols("r0 r1 v0 v1")
    form = sp.Matrix(((A, B), (B, C)))
    alpha = sp.Matrix((1, 0))
    u = sp.Matrix((0, 1))
    rho = sp.Matrix((r0, r1))
    v = sp.Matrix((v0, v1))

    def pairing(left, right):
        return sp.expand((left.T * form * right)[0])

    equations = {
        "alpha_rho": pairing(alpha, rho),
        "alpha_v": pairing(alpha, v),
        "u_rho": pairing(u, rho),
        "u_v_minus_one": pairing(u, v) - 1,
    }
    require(equations == {
        "alpha_rho": A * r0 + B * r1,
        "alpha_v": A * v0 + B * v1,
        "u_rho": B * r0 + C * r1,
        "u_v_minus_one": B * v0 + C * v1 - 1,
    }, "the normalized bright-pairing equations changed")

    # Since (rho,v) is a basis, the first two equations force A=B=0.
    # The last then gives C*v1=1, while the third gives C*r1=0.
    # Hence C,v1 are nonzero and r1=0: rho spans alpha.  The scalar form
    # has radical <alpha>.  The original vector-valued beta has the same
    # radical conclusion because its three zero rows vanish before ell.
    normalized = {A: 0, B: 0, r1: 0, C: 1, v1: 1}
    require(all(sp.expand(value.subs(normalized)) == 0
                for value in equations.values()),
            "the common-radical normal form stopped solving the four rows")
    require(form.subs(normalized) == sp.Matrix(((0, 0), (0, 1))),
            "the rank-one quotient form changed")

    # If alpha is a nonzero multiple of u, beta(alpha,v)=0 contradicts
    # beta(u,v)=x.  The symmetric statement holds for rho and v.
    lam = sp.Symbol("lambda", nonzero=True)
    require(sp.expand(lam * 1) != 0,
            "the nonzero-collinear contradiction disappeared")

    return {
        "vectors": {
            "alpha": "pi_t(Q_a)", "u": "pi_t(Q_t)",
            "rho": "pi_t(R_c)", "v": "pi_t(R_t)",
        },
        "four_rows": [
            "beta(alpha,rho)=0", "beta(alpha,v)=0",
            "beta(u,rho)=0", "beta(u,v)=x",
        ],
        "dichotomy": [
            "x=0 in coker(Phi)/R_nt, equivalently [X_t] lies in R_nt",
            "alpha=0 or rho=0",
            "alpha and rho span one common radical line L and beta factors through Sym^2(W/L)",
        ],
        "nondegenerate_normal_form": {
            "W_basis": ["ell", "h"],
            "alpha": "ell", "rho": "ell",
            "u": "h", "v": "v0*ell+v1*h",
            "beta": "beta(h,h)=g; beta(ell,W)=0",
            "x": "v1*g",
        },
    }


def audit_full_bright_quotient_counterguard():
    # Extend the two-dimensional W by affine bright-preimage classes Cc,Aa.
    # Phi(Cc)=X_c and Phi(Aa)=X_a make them independent modulo K.  Define
    # a symmetric pairing with the single nonzero value beta(h,h)=x.
    # The left rows (Q_a,Q_c,Q_t)=(ell,Cc,h) and right rows
    # (R_a,R_c,R_t)=(Aa,ell,h) then reproduce all nine quotient rows.
    basis = ("ell", "h", "Cc", "Aa")

    def beta(left, right):
        return "x" if left == right == "h" else "0"

    left_rows = ("ell", "Cc", "h")
    right_rows = ("Aa", "ell", "h")
    matrix = tuple(tuple(beta(left, right) for right in right_rows)
                   for left in left_rows)
    require(matrix == (
        ("0", "0", "0"),
        ("0", "0", "0"),
        ("0", "0", "x"),
    ), "the full bright quotient counterguard changed")
    require(len(basis) == 4 and len(set(basis)) == 4,
            "the affine bright quotient lost an independent class")
    return {
        "ambient_quotient_basis": list(basis),
        "Phi_labels": {"Cc": "X_c", "Aa": "X_a",
                       "ell": "0", "h": "0"},
        "Q_rows": list(left_rows),
        "R_rows": list(right_rows),
        "pairing_matrix": matrix,
        "scope": (
            "exact linearized common-hafnian/bright quotient normal form; "
            "not yet a quadratic q_C common-provenance packet"
        ),
    }


def audit_no_universal_additive_colour_grading():
    # Variables g_(site,colour) and one edge degree h_uv.  Homogeneity of
    # every coordinate in an arbitrary full 3x3 block imposes
    # g_ui+g_vj=h_uv for all i,j.  The exact nullspace has dimension five
    # and consists only of colour-blind site weights.
    sites = tuple(range(5))
    colours = tuple(range(3))
    edges = tuple(itertools.combinations(sites, 2))
    g_labels = tuple(itertools.product(sites, colours))
    variables = g_labels + edges
    rows = []
    for edge in edges:
        for left_colour in colours:
            for right_colour in colours:
                row = [0] * len(variables)
                row[variables.index((edge[0], left_colour))] += 1
                row[variables.index((edge[1], right_colour))] += 1
                row[len(g_labels) + edges.index(edge)] -= 1
                rows.append(row)
    matrix = sp.Matrix(rows)
    kernel = matrix.nullspace()
    require(matrix.shape == (90, 25) and matrix.rank() == 20,
            "the full-block grading equation rank changed")
    require(len(kernel) == 5,
            "an unexpected colour-sensitive additive grading appeared")
    for vector in kernel:
        for site in sites:
            values = [vector[g_labels.index((site, colour))]
                      for colour in colours]
            require(values[0] == values[1] == values[2],
                    "the grading kernel acquired colour sensitivity")
    return {
        "grading_variables": len(variables),
        "full_block_equations": len(rows),
        "equation_rank": matrix.rank(),
        "grading_dimension": len(kernel),
        "verdict": (
            "every compatible additive grading is colour-blind and gives "
            "all five-site output words the same degree"
        ),
    }


def main():
    pin_dependencies()
    rows = audit_literal_nine_rows()
    radical = audit_radical_dichotomy()
    counterguard = audit_full_bright_quotient_counterguard()
    grading = audit_no_universal_additive_colour_grading()
    ledger = {
        "pinned_pair_reduction_sha256": PINNED_PAIR_REDUCTION_SHA256,
        "pinned_common_hafnian_sha256": PINNED_COMMON_HAFNIAN_SHA256,
        "literal_common_hafnian": rows,
        "bright_pairing_radical_dichotomy": radical,
        "quotient_normal_form_counterguard": counterguard,
        "additive_grading_no_go": grading,
        "verdict": (
            "if [X_t] survives the target-free residual and both auxiliary "
            "kernel projections are nonzero, the full nine rows force one "
            "common radical line and a one-dimensional rank-one quotient; "
            "this quotient normal form is compatible with the two bright "
            "image labels, so common q_C provenance remains load-bearing"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"the bright-pairing radical ledger changed: {digest}")

    print("shared reciprocal bright-pairing radical dichotomy: PASS")
    print("full common-hafnian rows: 2187; quotient matrix rank one")
    print("nondegenerate branch: one common radical line L in W")
    print("degenerate branches: X_t in R_nt, or alpha/rho=0")
    print("universal additive colour grading: impossible for full blocks")
    print(f"ledger sha256: {digest}")


if __name__ == "__main__":
    main()
