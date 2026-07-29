#!/usr/bin/env python3
"""Exact degree-78 closure audit for the sole-plane profile 2^3 1^7.

The proof uses one modular Macaulay-rank lower bound and exact rational
homogeneous overideals.  Every characteristic-zero containment, target
membership, homogeneity statement, and Hilbert numerator used in the
squeeze is recomputed over QQ in this run.
"""

from __future__ import annotations

import math
import re
import subprocess

import sympy as sp

from verify_live_three_zero_sole_plane_fourth_high_three_double_frontier import (
    LOCAL_VARIABLES,
    audit_input_denominators,
    audit_rows_scale_and_exchange,
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


def singular_script(first_system: tuple[sp.Expr, ...]) -> str:
    names = ",".join(map(str, LOCAL_VARIABLES))
    script = (
        f"ring r=(0,v,w),({names}),dp; option(redSB);\n"
        f"ideal I={generators(first_system)};\n"
        "matrix T; ideal G=liftstd(I,T);\n"
        "if(size(G)!=1 || deg(G[1])!=0 || nrows(T)!=10 || ncols(T)!=1) "
        '{ "FIRST LIFT AUDIT FAILED"; exit(1); }\n'
        "list DL; int i,j; poly p; number c;\n"
        "for(i=1;i<=nrows(T);i++) { for(j=1;j<=ncols(T);j++) { "
        "p=T[i,j]; while(p!=0) { c=leadcoef(p); "
        "DL[size(DL)+1]=denominator(c); p=p-lead(p); } } }\n"
        "if(size(DL)!=34) { \"FIRST LIFT TERM AUDIT FAILED\"; exit(1); }\n"
        "def H=G[1]; def DD=DL;\n"
        "ring s=0,(t,v,w),dp;\n"
        "list dl=imap(r,DD); poly denominator_lcm=1; poly d;\n"
        "for(i=1;i<=size(dl);i++) { d=dl[i]; "
        "denominator_lcm=denominator_lcm*d/gcd(denominator_lcm,d); }\n"
        "if(denominator_lcm!=1) "
        '{ "FIRST LIFT DENOMINATOR AUDIT FAILED"; exit(1); }\n'
        "poly h1=imap(r,H); poly hh=homog(h1,t);\n"
        "poly h2=subst(subst(hh,v,1),t,v);\n"
        "poly h3=subst(subst(subst(hh,v,1),w,v),t,w);\n"
        "poly L=v*w*(v-1)*(v+1)*(w-1)*(w+1)*(v-w)*(v+w);\n"
    )
    for name in ("h1", "h2", "h3"):
        script += (
            f"d=gcd({name},L); while(d!=1) "
            f"{{ {name}={name}/d; d=gcd({name},L); }}\n"
        )
    script += (
        "if(deg(h1)!=30 || deg(h2)!=30 || deg(h3)!=30) "
        '{ "CYCLIC DEGREE AUDIT FAILED"; exit(1); }\n'
        "def H1=h1; def H2=h2; def H3=h3; def LL=L;\n"

        # One good-prime rank lower bound for the degree-78 Macaulay map.
        "ring p=32003,(t,v,w),dp;\n"
        "ideal Jp=homog(imap(s,H1),t),homog(imap(s,H2),t),"
        "homog(imap(s,H3),t);\n"
        "timer=1; ideal Gp=slimgb(Jp); timer=0;\n"
        "bigintvec jphs=hilb(Gp,1);\n"
        '"MODULAR J HILBERT NUMERATOR"; jphs; '
        '"MODULAR J BASIS SIZE"; size(Gp);\n'

        # Exact affine overideal A in the order (t,v,w).
        "ring qa=0,(v,w),dp; option(redSB);\n"
        "ideal Ha=imap(s,H1),imap(s,H2),imap(s,H3); "
        "poly la=imap(s,LL);\n"
        'LIB "resources.lib"; Resources::setcores(1); LIB "modstd.lib";\n'
        '"STAGE EXACT AFFINE CANDIDATE";\n'
        'timer=1; ideal KA0=modGB("slimgb",Ha,0); timer=0;\n'
        "timer=1; ideal KA=slimgb(KA0); timer=0;\n"
        "if(size(reduce(Ha,KA))!=0 || dim(KA)!=0 || vdim(KA)!=192 "
        "|| reduce(la^4,KA)!=0) "
        '{ "EXACT AFFINE CANDIDATE AUDIT FAILED"; exit(1); }\n'
        "def KADATA=KA;\n"
        "ring qA=0,(t,v,w),dp; option(redSB);\n"
        "ideal JA=homog(imap(s,H1),t),homog(imap(s,H2),t),"
        "homog(imap(s,H3),t);\n"
        "poly lA=imap(s,LL); poly lhA=homog(lA,t); "
        "poly targetA=t^46*lhA^4;\n"
        "if(deg(targetA)!=78 || subst(targetA,t,1)!=lA^4) "
        '{ "EXACT A TARGET DEGREE/DEHOM AUDIT FAILED"; exit(1); }\n'
        "ideal A=imap(qa,KADATA); "
        "for(i=1;i<=size(A);i++) { A[i]=homog(A[i],t); } "
        "timer=1; A=slimgb(A); timer=0;\n"
        "for(i=1;i<=size(A);i++) { if(homog(A[i],t)!=A[i]) "
        '{ "EXACT A HOMOGENEITY AUDIT FAILED"; exit(1); } }\n'
        "if(size(reduce(JA,A))!=0 || reduce(targetA,A)!=0) "
        '{ "EXACT J/TARGET IN A AUDIT FAILED"; exit(1); }\n'
        "bigintvec ahs=hilb(A,1);\n"
        '"EXACT A HILBERT NUMERATOR"; ahs; '
        '"EXACT A BASIS SIZE"; size(A);\n'
        "ideal AT=A; AT[size(AT)+1]=t^16; "
        "timer=1; AT=slimgb(AT); timer=0;\n"
        "bigintvec aths=hilb(AT,1);\n"
        '"EXACT A+T16 HILBERT NUMERATOR"; aths; '
        '"EXACT A+T16 BASIS SIZE"; size(AT);\n'

        # Exact second overideal B in the smaller order (v,w,t).
        "ring qB=0,(v,w,t),dp; option(redSB);\n"
        '"EXACT B VARIABLE ORDER"; var(1); var(2); var(3);\n'
        "if(var(1)!=v || var(2)!=w || var(3)!=t) "
        '{ "EXACT B VARIABLE ORDER AUDIT FAILED"; exit(1); }\n'
        "map phi=s,t,v,w;\n"
        "ideal JB=homog(phi(H1),t),homog(phi(H2),t),homog(phi(H3),t);\n"
        "poly lB=phi(LL); poly lhB=homog(lB,t); "
        "poly targetB=t^46*lhB^4;\n"
        "if(deg(targetB)!=78 || subst(targetB,t,1)!=lB^4) "
        '{ "EXACT B TARGET DEGREE/DEHOM AUDIT FAILED"; exit(1); }\n'
        "ideal BSOURCE=JB; BSOURCE[size(BSOURCE)+1]=t^16;\n"
        'LIB "resources.lib"; Resources::setcores(1); LIB "modstd.lib";\n'
        '"STAGE EXACT B16 CANDIDATE";\n'
        'timer=1; ideal BK0=modGB("slimgb",BSOURCE,0); timer=0;\n'
        "timer=1; ideal B=slimgb(BK0); timer=0;\n"
        "if(size(reduce(BSOURCE,B))!=0 || reduce(t^16,B)!=0 "
        "|| size(reduce(JB,B))!=0 || reduce(targetB,B)!=0) "
        '{ "EXACT J/T16/TARGET IN B AUDIT FAILED"; exit(1); }\n'
        "for(i=1;i<=size(B);i++) { if(homog(B[i],t)!=B[i]) "
        '{ "EXACT B HOMOGENEITY AUDIT FAILED"; exit(1); } }\n'
        "bigintvec bhs=hilb(B,1);\n"
        '"EXACT B16 HILBERT NUMERATOR"; bhs; '
        '"EXACT B16 BASIS SIZE"; size(B);\n'
        '"SOLE-PLANE 2^3 1^7 ALGEBRA AUDIT COMPLETE";\n'
    )
    return script


def hilbert_value(output: str, label: str, degree: int = 78) -> int:
    match = re.search(rf"{re.escape(label)}\s*\n([0-9,\-]+)", output)
    if match is None:
        raise RuntimeError(f"missing {label!r}\n{output}")
    entries = [int(value) for value in match.group(1).split(",")]
    numerator = entries[:-1]  # Singular documents the last entry as metadata.
    return sum(
        coefficient * math.comb(degree - exponent + 2, 2)
        for exponent, coefficient in enumerate(numerator)
        if exponent <= degree
    )


def audit_projective_structural_boundary() -> None:
    t = sp.symbols("t")
    discriminant = sp.expand(
        t * v * w * (v-t) * (v+t) * (w-t) * (w+t) * (v-w) * (v+w)
    )
    assert discriminant.subs({t: 0, v: 1, w: 0}) == 0
    assert discriminant.subs({t: 0, v: 0, w: 1}) == 0


def main() -> None:
    audit_rows_scale_and_exchange()
    first_system, _ = systems()
    audit_input_denominators(first_system)
    audit_projective_structural_boundary()
    result = subprocess.run(
        ("Singular", "--cpus=1", "-q"),
        input=singular_script(first_system),
        text=True,
        capture_output=True,
        check=True,
        timeout=14400,
    )
    output = result.stdout
    if (result.stderr or "?" in output
            or "ALGEBRA AUDIT COMPLETE" not in output):
        raise RuntimeError(output + result.stderr)

    modular_j = hilbert_value(output, "MODULAR J HILBERT NUMERATOR")
    exact_a = hilbert_value(output, "EXACT A HILBERT NUMERATOR")
    exact_at = hilbert_value(output, "EXACT A+T16 HILBERT NUMERATOR")
    exact_b = hilbert_value(output, "EXACT B16 HILBERT NUMERATOR")
    if (modular_j, exact_a, exact_at, exact_b) != (318, 192, 0, 126):
        raise RuntimeError(
            "bad degree-78 Hilbert values: "
            f"Jp={modular_j}, A={exact_a}, A+T16={exact_at}, B={exact_b}"
        )

    number_monomials = math.comb(80, 2)
    modular_rank = number_monomials - modular_j
    intersection_hf = exact_a + exact_b  # A+B has HF 0 since t^16 is in B.
    if modular_rank != 2842 or intersection_hf != 318:
        raise RuntimeError("degree-78 rank/intersection squeeze failed")

    print(output.strip())
    print("SOLE-PLANE 2^3 1^7 EXACT CLOSURE PASS")
    print("degree-78 monomials / modular rank:", number_monomials, modular_rank)
    print("HF(Jp) / HF(A) / HF(A+T16) / HF(B):", 318, 192, 0, 126)
    print("HF(A intersection B):", intersection_hf)


if __name__ == "__main__":
    main()
