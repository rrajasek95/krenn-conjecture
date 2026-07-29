#!/usr/bin/env python3
"""Compare modular monomial orders for the exact B16 reconstruction route."""

from __future__ import annotations

import argparse
import subprocess

import sympy as sp

from verify_live_three_zero_sole_plane_fourth_high_three_double_frontier import (
    LOCAL_VARIABLES,
    systems,
)


v, w = sp.symbols("v w")


def generators(equations: tuple[sp.Expr, ...]) -> str:
    return ",".join(
        str(
            sp.Poly(
                equation,
                *LOCAL_VARIABLES,
                domain=sp.QQ.frac_field(v, w),
            ).as_expr()
        ).replace("**", "^")
        for equation in equations
    )


ORDER_RINGS = {
    "dp_tvw": "ring q=32003,(t,v,w),dp;",
    "Dp_tvw": "ring q=32003,(t,v,w),Dp;",
    "lp_tvw": "ring q=32003,(t,v,w),lp;",
    "dp_vwt": "ring q=32003,(v,w,t),dp;",
    "Dp_vwt": "ring q=32003,(v,w,t),Dp;",
    "block_vw_t": "ring q=32003,(v,w,t),(dp(2),dp(1));",
    "block_t_vw": "ring q=32003,(t,v,w),(dp(1),dp(2));",
}


def singular_script(first_system: tuple[sp.Expr, ...], order: str) -> str:
    names = ",".join(map(str, LOCAL_VARIABLES))
    script = (
        f"ring r=(0,v,w),({names}),dp; option(redSB);\n"
        f"ideal I={generators(first_system)};\n"
        "matrix T; ideal G=liftstd(I,T); def H=G[1];\n"
        "if(size(G)!=1 || deg(G[1])!=0) "
        '{ "FIRST LIFT FAILED"; exit(1); }\n'
        "ring s=0,(t,v,w),dp;\n"
        "poly h1=imap(r,H); poly hh=homog(h1,t);\n"
        "poly h2=subst(subst(hh,v,1),t,v);\n"
        "poly h3=subst(subst(subst(hh,v,1),w,v),t,w);\n"
        "poly L=v*w*(v-1)*(v+1)*(w-1)*(w+1)*(v-w)*(v+w); poly d;\n"
    )
    for name in ("h1", "h2", "h3"):
        script += (
            f"d=gcd({name},L); while(d!=1) "
            f"{{ {name}={name}/d; d=gcd({name},L); }}\n"
        )
    script += (
        "def H1=h1; def H2=h2; def H3=h3;\n"
        f"{ORDER_RINGS[order]}\n"
        "map phi=s,t,v,w;\n"
        "poly f1=phi(H1); poly f2=phi(H2); poly f3=phi(H3);\n"
        "ideal J=homog(f1,t),homog(f2,t),homog(f3,t);\n"
        "ideal B=J; B[size(B)+1]=t^16;\n"
        f'"STAGE B16 MODULAR ORDER {order}";\n'
        "timer=1; B=slimgb(B); timer=0;\n"
        "int i,total_terms,max_terms,max_degree; int nterms;\n"
        "for(i=1;i<=size(B);i++) { nterms=size(B[i]); "
        "total_terms=total_terms+nterms; "
        "if(nterms>max_terms) { max_terms=nterms; } "
        "if(deg(B[i])>max_degree) { max_degree=deg(B[i]); } }\n"
        '"ORDER / BASIS / TOTAL TERMS / MAX TERMS / MAX DEGREE";\n'
        f'"{order}"; size(B); total_terms; max_terms; max_degree;\n'
        '"HILBERT NUMERATOR"; hilb(B,1);\n'
        '"BOUNDARY ORDER EXPLORATION COMPLETE";\n'
    )
    return script


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("order", choices=tuple(ORDER_RINGS))
    parser.add_argument("--timeout", type=int, default=1800)
    args = parser.parse_args()
    first_system, _ = systems()
    result = subprocess.run(
        ("Singular", "--cpus=1", "-q"),
        input=singular_script(first_system, args.order),
        text=True,
        capture_output=True,
        check=True,
        timeout=args.timeout,
    )
    if result.stderr or "?" in result.stdout or "COMPLETE" not in result.stdout:
        raise RuntimeError(result.stdout + result.stderr)
    print(result.stdout.strip())


if __name__ == "__main__":
    main()
