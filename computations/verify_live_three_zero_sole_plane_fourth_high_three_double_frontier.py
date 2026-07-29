#!/usr/bin/env python3
"""Exact frontier audit for the sole-plane residual profile 2^3 1^7.

This checker proves only denominator-free necessary conditions and their
parameter-infinity boundary.  It deliberately does not claim that the full
three-pair system is inconsistent.
"""

from __future__ import annotations

import subprocess

import sympy as sp

from explore_live_three_zero_sole_plane_dense_double import (
    P0,
    Pvw,
    Pv,
    Pwv,
    Pw,
    R0,
    Rvw,
    Rv,
    Rwv,
    Rw,
    affine_row,
    chi,
    eta,
    lam,
    mu,
    normalized_full_pair_system,
    v,
    w,
    x,
)
from verify_live_three_zero_sole_plane_fourth_high_frontier import (
    triple_quadratic_row,
)


LOCAL_VARIABLES = (
    P0, R0, Pv, Rv, Pw, Rw, Pvw, Rvw, Pwv, Rwv, lam, mu,
)
STRUCTURAL_FACTORS = (
    v, w, v - 1, v + 1, w - 1, w + 1, v - w, v + w,
)


def alternative_evaluations(polynomial: sp.Poly) -> tuple[sp.Expr, ...]:
    expression = polynomial.as_expr()
    derivative = sp.diff(expression, x)
    return (
        expression.subs(x, v),
        expression.subs(x, w),
        expression.subs(x, 1),
        expression.subs(x, -1),
        expression.subs(x, -v),
        expression.subs(x, -w),
        expression.subs(x, 0),
        derivative.subs(x, -v),
        derivative.subs(x, -w),
        derivative.subs(x, 0),
    )


def systems() -> tuple[tuple[sp.Expr, ...], tuple[sp.Expr, ...]]:
    first, second, exchanges = normalized_full_pair_system()
    first_system = alternative_evaluations(first)
    full_system = (
        first_system + alternative_evaluations(second) + exchanges
    )
    assert len(first_system) == 10
    assert len(full_system) == 24
    return first_system, full_system


def audit_rows_scale_and_exchange() -> None:
    anchor, first, square_plus_second = sp.symbols("a P R")
    direct = triple_quadratic_row(
        x, anchor, first, square_plus_second - first**2,
    )[:2]
    affine = affine_row(anchor, first, square_plus_second)
    assert all(sp.expand(left - right) == 0 for left, right in zip(
        direct, affine, strict=True,
    ))

    scale, X, A = sp.symbols("c X A", nonzero=True)
    scaled = affine_row(
        scale*A, first/scale, square_plus_second/scale**2,
    )
    scaled = tuple(sp.expand(entry.subs(x, scale*X)) for entry in scaled)
    normalized = affine_row(A, first, square_plus_second)
    normalized = tuple(entry.subs(x, X) for entry in normalized)
    assert sp.expand(scaled[0] - scale**2*normalized[0]) == 0
    assert sp.expand(scaled[1] - scale**3*normalized[1]) == 0

    anchor, selected, replacement = sp.symbols("a b c")
    delta = sp.factor(
        chi(anchor, replacement) - chi(anchor, selected)
    )
    epsilon = sp.factor(
        eta(anchor, replacement) - eta(anchor, selected)
    )
    assert sp.cancel(
        (first + chi(anchor, replacement))
        - (first + chi(anchor, selected) + delta)
    ) == 0
    old_r = square_plus_second
    new_r = old_r + 2*first*delta + delta**2 + epsilon
    assert sp.expand(
        new_r - (
            (first + delta)**2
            + (old_r - first**2)
            + epsilon
        )
    ) == 0


def audit_input_denominators(equations: tuple[sp.Expr, ...]) -> None:
    allowed = {
        sp.Poly(factor, v, w).monic().as_expr()
        for factor in STRUCTURAL_FACTORS
    }
    for equation in equations:
        denominator = sp.cancel(equation).as_numer_denom()[1]
        denominator = sp.Poly(denominator, v, w, domain=sp.QQ)
        for factor, _multiplicity in sp.factor_list(denominator)[1]:
            factor = sp.Poly(factor, v, w, domain=sp.QQ).monic().as_expr()
            assert factor in allowed, (equation, factor)


def singular_exact_frontier(
    first_system: tuple[sp.Expr, ...],
    full_system: tuple[sp.Expr, ...],
) -> str:
    def generators(equations: tuple[sp.Expr, ...]) -> str:
        return ",".join(
            str(sp.Poly(
                equation,
                *LOCAL_VARIABLES,
                domain=sp.QQ.frac_field(v, w),
            ).as_expr()).replace("**", "^")
            for equation in equations
        )

    script = (
        f"ring r=(0,v,w),({','.join(map(str, LOCAL_VARIABLES))}),dp;\n"
        "option(redSB);\n"
        f"ideal IA={generators(first_system)};\n"
        "matrix TA; ideal GA=liftstd(IA,TA);\n"
        "if(size(GA)!=1 || deg(GA[1])!=0) "
        '{ "FIRST GENERIC LIFT FAILED"; exit(1); }\n'
        f"ideal IB={generators(full_system)};\n"
        "matrix TB; ideal GB=liftstd(IB,TB);\n"
        "if(size(GB)!=1 || deg(GB[1])!=0) "
        '{ "FULL GENERIC LIFT FAILED"; exit(1); }\n'
        "list DA,DB; int i,j; poly p; number c;\n"
        "for(i=1;i<=nrows(TA);i++) { for(j=1;j<=ncols(TA);j++) "
        "{ p=TA[i,j]; while(p!=0) { c=leadcoef(p); "
        "DA[size(DA)+1]=denominator(c); p=p-lead(p); } } }\n"
        "for(i=1;i<=nrows(TB);i++) { for(j=1;j<=ncols(TB);j++) "
        "{ p=TB[i,j]; while(p!=0) { c=leadcoef(p); "
        "DB[size(DB)+1]=denominator(c); p=p-lead(p); } } }\n"
        "int rowsA=nrows(TA); int colsA=ncols(TA); "
        "int rowsB=nrows(TB); int colsB=ncols(TB);\n"
        "def HA=GA[1]; def HB=GB[1]; def DAA=DA; def DBB=DB;\n"
        "ring s=0,(t,v,w),dp;\n"
        "list da=imap(r,DAA); list db=imap(r,DBB);\n"
        "poly ad=1; poly bd=1; poly d;\n"
        "for(i=1;i<=size(da);i++) { d=da[i]; ad=ad*d/gcd(ad,d); }\n"
        "for(i=1;i<=size(db);i++) { d=db[i]; bd=bd*d/gcd(bd,d); }\n"
        "if(ad!=1 || bd!=1) { \"NONTRIVIAL LIFT DENOMINATOR\"; "
        "factorize(ad); factorize(bd); exit(1); }\n"
        "poly a1=imap(r,HA); poly ah=homog(a1,t);\n"
        "poly a2=subst(subst(ah,v,1),t,v);\n"
        "poly a3=subst(subst(subst(ah,v,1),w,v),t,w);\n"
        "poly b1=imap(r,HB); poly bh=homog(b1,t);\n"
        "poly b2=subst(subst(bh,v,1),t,v);\n"
        "poly b3=subst(subst(subst(bh,v,1),w,v),t,w);\n"
        "poly L=v*w*(v-1)*(v+1)*(w-1)*(w+1)*(v-w)*(v+w);\n"
    )
    for name in ("a1", "a2", "a3", "b1", "b2", "b3"):
        script += (
            f"d=gcd({name},L); while(d!=1) "
            f"{{ {name}={name}/d; d=gcd({name},L); }}\n"
        )
    script += (
        "if(deg(a1)!=30 || deg(a2)!=30 || deg(a3)!=30 "
        "|| deg(b1)!=48 || deg(b2)!=48 || deg(b3)!=48) "
        '{ "UNEXPECTED RESIDUAL DEGREE"; exit(1); }\n'
        "poly at1=subst(homog(a1,t),t,0);\n"
        "poly at2=subst(homog(a2,t),t,0);\n"
        "poly at3=subst(homog(a3,t),t,0);\n"
        "poly bt1=subst(homog(b1,t),t,0);\n"
        "poly bt2=subst(homog(b2,t),t,0);\n"
        "poly bt3=subst(homog(b3,t),t,0);\n"
        "poly topg=gcd(gcd(gcd(at1,at2),at3),"
        "gcd(gcd(bt1,bt2),bt3));\n"
        "if(topg/leadcoef(topg)!=v^6*w^6) "
        '{ "UNEXPECTED PARAMETER INFINITY GCD"; factorize(topg); exit(1); }\n'
        '"EXACT THREE-DOUBLE FRONTIER AUDIT PASS";\n'
        '"first lift shape"; rowsA; colsA; size(da);\n'
        '"full lift shape"; rowsB; colsB; size(db);\n'
        '"stripped degrees"; deg(a1);deg(a2);deg(a3);'
        'deg(b1);deg(b2);deg(b3);\n'
        '"infinity gcd"; factorize(topg);\n'
    )
    result = subprocess.run(
        ("Singular", "-q"),
        input=script,
        text=True,
        capture_output=True,
        check=True,
        timeout=300,
    )
    if "?" in result.stdout or "PASS" not in result.stdout:
        raise RuntimeError(result.stdout + result.stderr)
    return result.stdout.strip()


def main() -> None:
    audit_rows_scale_and_exchange()
    first_system, full_system = systems()
    audit_input_denominators(full_system)
    print(singular_exact_frontier(first_system, full_system))


if __name__ == "__main__":
    main()
