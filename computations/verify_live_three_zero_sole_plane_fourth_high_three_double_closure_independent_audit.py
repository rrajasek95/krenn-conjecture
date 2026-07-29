#!/usr/bin/env python3
"""Independent audit of the sole-plane 2^3 1^7 closure.

This file deliberately does not import the primary closure checker or the
three-double frontier checker.  It rebuilds the cleared rows, the first
cross-identity evaluation system, the three cyclic parameter obstructions,
and the degree-78 Hilbert squeeze from their definitions.  The modular rank
check uses the different prime 31991 and permuted variable orders.  Every
ideal containment used in characteristic zero is checked over QQ.
"""

from __future__ import annotations

import math
import re
import subprocess

import sympy as sp


x, v, w = sp.symbols("x v w")
P0, R0, Pv, Rv, Pw, Rw = sp.symbols("P0 R0 Pv Rv Pw Rw")
Pvw, Rvw, Pwv, Rwv = sp.symbols("Pvw Rvw Pwv Rwv")
lam, mu = sp.symbols("lambda mu")

LOCAL_VARIABLES = (
    P0, R0, Pv, Rv, Pw, Rw, Pvw, Rvw, Pwv, Rwv, lam, mu,
)
STRUCTURAL_FACTORS = (
    v, w, v - 1, v + 1, w - 1, w + 1, v - w, v + w,
)
AUDIT_PRIME = 31991


def chi(anchor: sp.Expr, selected: sp.Expr) -> sp.Expr:
    return 2 / (anchor + selected) - 3 / (selected - anchor)


def eta(anchor: sp.Expr, selected: sp.Expr) -> sp.Expr:
    return 2 / (anchor + selected) ** 2 + 3 / (selected - anchor) ** 2


def cleared_row(
    anchor: sp.Expr, first: sp.Expr, square_plus_second: sp.Expr,
) -> tuple[sp.Expr, sp.Expr]:
    denominator = x**2 - anchor**2
    first_entry = sp.expand(
        square_plus_second * denominator**2
        - 2 * first * denominator * (x + 3 * anchor)
        + 4 * (x**2 + 2 * anchor * x + 3 * anchor**2)
    )
    second_entry = sp.expand(
        2 * first * denominator**2
        - 2 * denominator * (x + 3 * anchor)
        - anchor * first_entry
    )
    return first_entry, second_entry


def pair_determinant(
    left: sp.Expr,
    right: sp.Expr,
    left_data: tuple[sp.Expr, sp.Expr],
    right_data: tuple[sp.Expr, sp.Expr],
) -> sp.Expr:
    left_row = cleared_row(left, *left_data)
    right_row = cleared_row(right, *right_data)
    return sp.expand(
        left_row[0] * right_row[1] - left_row[1] * right_row[0]
    )


def first_cross_polynomial() -> sp.Poly:
    """Rebuild C1 after normalizing the first double value to one."""
    delta = sp.factor(chi(sp.S.One, w) - chi(sp.S.One, v))
    epsilon = sp.factor(eta(sp.S.One, w) - eta(sp.S.One, v))
    p0w = P0 + delta
    r0w = R0 + 2 * P0 * delta + delta**2 + epsilon
    f_1v = pair_determinant(1, v, (P0, R0), (Pv, Rv))
    f_1w = pair_determinant(1, w, (p0w, r0w), (Pw, Rw))
    assert sp.Poly(f_1v, x).degree() <= 8
    assert sp.Poly(f_1w, x).degree() <= 8
    numerator = sp.cancel(
        (x - v) * f_1v - lam * (x - w) * f_1w
    ).as_numer_denom()[0]
    return sp.Poly(numerator, x)


def evaluation_system(polynomial: sp.Poly) -> tuple[sp.Expr, ...]:
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


def audit_row_and_exchange() -> None:
    anchor, first, second = sp.symbols("a P W")
    denominator = x**2 - anchor**2
    log_first_numerator = first * denominator - x - 3 * anchor
    log_second_numerator = (
        second * denominator**2 + (x - anchor) ** 2
        + 2 * (x + anchor) ** 2
    )
    direct_first = sp.expand(log_first_numerator**2 + log_second_numerator)
    direct_second = sp.expand(
        2 * log_first_numerator * denominator - anchor * direct_first
    )
    rebuilt = cleared_row(anchor, first, first**2 + second)
    assert sp.expand(rebuilt[0] - direct_first) == 0
    assert sp.expand(rebuilt[1] - direct_second) == 0

    scale, X, A = sp.symbols("c X A", nonzero=True)
    scaled = tuple(sp.expand(entry.subs(x, scale * X)) for entry in
                   cleared_row(A * scale, first / scale,
                               (first**2 + second) / scale**2))
    unscaled = tuple(entry.subs(x, X) for entry in
                     cleared_row(A, first, first**2 + second))
    assert sp.expand(scaled[0] - scale**2 * unscaled[0]) == 0
    assert sp.expand(scaled[1] - scale**3 * unscaled[1]) == 0

    selected, replacement = sp.symbols("b c")
    delta = chi(anchor, replacement) - chi(anchor, selected)
    epsilon = eta(anchor, replacement) - eta(anchor, selected)
    old_effective_first = first + chi(anchor, selected)
    old_effective_r = old_effective_first**2 + second + eta(anchor, selected)
    new_effective_first = old_effective_first + delta
    new_effective_r = old_effective_r + 2 * old_effective_first * delta
    new_effective_r += delta**2 + epsilon
    assert sp.cancel(
        new_effective_first - (first + chi(anchor, replacement))
    ) == 0
    assert sp.cancel(
        new_effective_r
        - ((first + chi(anchor, replacement)) ** 2
           + second + eta(anchor, replacement))
    ) == 0


def audit_input_denominators(equations: tuple[sp.Expr, ...]) -> None:
    allowed = {
        sp.Poly(factor, v, w, domain=sp.QQ).monic().as_expr()
        for factor in STRUCTURAL_FACTORS
    }
    for equation in equations:
        denominator = sp.Poly(
            sp.cancel(equation).as_numer_denom()[1], v, w, domain=sp.QQ
        )
        for factor, _multiplicity in sp.factor_list(denominator)[1]:
            normalized = sp.Poly(factor, v, w, domain=sp.QQ).monic().as_expr()
            assert normalized in allowed, normalized


def singular_generators(equations: tuple[sp.Expr, ...]) -> str:
    field = sp.QQ.frac_field(v, w)
    return ",".join(
        str(sp.Poly(equation, *LOCAL_VARIABLES, domain=field).as_expr())
        .replace("**", "^")
        for equation in equations
    )


def singular_script(equations: tuple[sp.Expr, ...]) -> str:
    names = ",".join(map(str, LOCAL_VARIABLES))
    script = (
        f"ring cf=(0,v,w),({names}),dp; option(redSB);\n"
        f"ideal E={singular_generators(equations)};\n"
        "matrix U; ideal G=liftstd(E,U);\n"
        "if(size(G)!=1 || deg(G[1])!=0 || nrows(U)!=10 || ncols(U)!=1) "
        "{ \"INDEPENDENT GENERIC LIFT SHAPE FAILED\"; exit(1); }\n"
        "if(matrix(E)*U-matrix(G)!=0) "
        "{ \"INDEPENDENT GENERIC LIFT IDENTITY FAILED\"; exit(1); }\n"
        "list CD; int i,j; poly scan; number coeff,den;\n"
        "for(i=1;i<=nrows(U);i++) { for(j=1;j<=ncols(U);j++) { "
        "scan=U[i,j]; while(scan!=0) { coeff=leadcoef(scan); "
        "den=denominator(coeff); if(deg(den)>0) "
        "{ \"NONCONSTANT CERTIFICATE DENOMINATOR\"; den; exit(1); } "
        "CD[size(CD)+1]=den; scan=scan-lead(scan); } } }\n"
        "if(size(CD)!=34) "
        "{ \"INDEPENDENT CERTIFICATE TERM COUNT FAILED\"; exit(1); }\n"
        "def RAW=G[1];\n"

        "ring s=0,(t,v,w),dp; option(redSB);\n"
        "poly raw1=imap(cf,RAW); poly rawh=homog(raw1,t);\n"
        "poly raw2=subst(subst(rawh,v,1),t,v);\n"
        "poly raw3=subst(subst(subst(rawh,v,1),w,v),t,w);\n"
        "poly h1=raw1; poly h2=raw2; poly h3=raw3;\n"
        "poly L=v*w*(v-1)*(v+1)*(w-1)*(w+1)*(v-w)*(v+w); poly d;\n"
    )
    for name in ("h1", "h2", "h3"):
        script += (
            f"d=gcd({name},L); while(d!=1) "
            f"{{ {name}={name}/d; d=gcd({name},L); }}\n"
        )
    script += (
        "poly removed1=raw1/h1; poly removed2=raw2/h2; "
        "poly removed3=raw3/h3;\n"
        "if(raw1!=removed1*h1 || raw2!=removed2*h2 || raw3!=removed3*h3) "
        "{ \"STRUCTURAL FACTOR QUOTIENT FAILED\"; exit(1); }\n"
        "if(gcd(h1,L)!=1 || gcd(h2,L)!=1 || gcd(h3,L)!=1) "
        "{ \"STRUCTURAL FACTOR STRIP INCOMPLETE\"; exit(1); }\n"
        "ideal RR=std(ideal(removed1)); if(reduce(L^60,RR)!=0) "
        "{ \"H1 REMOVED A NONSTRUCTURAL FACTOR\"; exit(1); }\n"
        "RR=std(ideal(removed2)); if(reduce(L^60,RR)!=0) "
        "{ \"H2 REMOVED A NONSTRUCTURAL FACTOR\"; exit(1); }\n"
        "RR=std(ideal(removed3)); if(reduce(L^60,RR)!=0) "
        "{ \"H3 REMOVED A NONSTRUCTURAL FACTOR\"; exit(1); }\n"
        "if(deg(h1)!=30 || deg(h2)!=30 || deg(h3)!=30 "
        "|| size(h1)!=319 || size(h2)!=319 || size(h3)!=319) "
        "{ \"CYCLIC OBSTRUCTION SHAPE FAILED\"; exit(1); }\n"
        "poly top1=subst(homog(h1,t),t,0); "
        "poly top2=subst(homog(h2,t),t,0); "
        "poly top3=subst(homog(h3,t),t,0);\n"
        "poly topg=gcd(gcd(top1,top2),top3); topg=topg/leadcoef(topg);\n"
        "if(topg!=v^6*w^6) "
        "{ \"PROJECTIVE INFINITY GCD FAILED\"; topg; exit(1); }\n"
        "poly Delta=t*v*w*(v-t)*(v+t)*(w-t)*(w+t)*(v-w)*(v+w);\n"
        "if(subst(subst(subst(Delta,t,0),v,1),w,0)!=0 "
        "|| subst(subst(subst(Delta,t,0),v,0),w,1)!=0) "
        "{ \"PROJECTIVE STRUCTURAL BOUNDARY FAILED\"; exit(1); }\n"
        "def H1=h1; def H2=h2; def H3=h3; def LL=L; "
        "poly namemark=t+2*v+3*w; poly affmark=v+2*w; "
        "def NAMEMARK=namemark; def AFFMARK=affmark;\n"

        # Use another good prime and a permuted variable order.
        f"ring fp={AUDIT_PRIME},(w,t,v),dp; option(redSB);\n"
        "map rho=s,t,v,w;\n"
        "if(rho(NAMEMARK)!=t+2*v+3*w) "
        "{ \"MODULAR NAME MAP FAILED\"; exit(1); }\n"
        "ideal Jp=homog(rho(H1),t),homog(rho(H2),t),homog(rho(H3),t);\n"
        "if(deg(Jp[1])!=30 || deg(Jp[2])!=30 || deg(Jp[3])!=30) "
        "{ \"MODULAR GENERATOR DEGREE FAILED\"; exit(1); }\n"
        "ideal Gp=slimgb(Jp); bigintvec jnum=hilb(Gp,1);\n"
        '"AUDIT PRIME / MODULAR J BASIS SIZE"; charstr(basering); size(Gp);\n'
        '"INDEPENDENT MODULAR J HILBERT NUMERATOR"; jnum;\n'

        # Exact affine overideal, with the affine variables reversed.
        "ring aff=0,(w,v),dp; option(redSB);\n"
        "map alpha=s,0,v,w;\n"
        "if(alpha(AFFMARK)!=v+2*w) "
        "{ \"AFFINE NAME MAP FAILED\"; exit(1); }\n"
        "ideal H=alpha(H1),alpha(H2),alpha(H3); poly la=alpha(LL); "
        "def AFFMARKDATA=alpha(AFFMARK);\n"
        'LIB "resources.lib"; Resources::setcores(1); LIB "modstd.lib";\n'
        '"STAGE INDEPENDENT EXACT AFFINE RECONSTRUCTION";\n'
        'ideal K0=modGB("slimgb",H,0); ideal K=slimgb(K0);\n'
        "if(size(reduce(H,K))!=0 || dim(K)!=0 || vdim(K)!=192 "
        "|| reduce(la^4,K)!=0) "
        "{ \"INDEPENDENT AFFINE OVERIDEAL FAILED\"; exit(1); }\n"
        "def KDATA=K;\n"

        "ring qA=0,(w,t,v),dp; option(redSB);\n"
        "map froms=s,t,v,w; map fromaff=aff,w,v;\n"
        "if(froms(NAMEMARK)!=t+2*v+3*w "
        "|| fromaff(AFFMARKDATA)!=v+2*w) "
        "{ \"EXACT A NAME MAP FAILED\"; exit(1); }\n"
        "ideal JA=homog(froms(H1),t),homog(froms(H2),t),homog(froms(H3),t);\n"
        "poly lA=froms(LL); poly lhA=homog(lA,t); "
        "poly targetA=t^46*lhA^4;\n"
        "if(deg(targetA)!=78 || subst(targetA,t,1)!=lA^4) "
        "{ \"EXACT A TARGET FAILED\"; exit(1); }\n"
        "ideal A=fromaff(KDATA); for(i=1;i<=size(A);i++) "
        "{ A[i]=homog(A[i],t); } A=slimgb(A);\n"
        "for(i=1;i<=size(A);i++) { if(homog(A[i],t)!=A[i]) "
        "{ \"EXACT A HOMOGENEITY FAILED\"; exit(1); } }\n"
        "if(size(reduce(JA,A))!=0 || reduce(targetA,A)!=0) "
        "{ \"EXACT A INCLUSION OR TARGET FAILED\"; exit(1); }\n"
        "bigintvec anum=hilb(A,1); ideal AT=A,t^16; AT=slimgb(AT); "
        "bigintvec atnum=hilb(AT,1);\n"
        '"INDEPENDENT EXACT A HILBERT NUMERATOR"; anum;\n'
        '"INDEPENDENT EXACT A+T16 HILBERT NUMERATOR"; atnum;\n'
        '"INDEPENDENT EXACT A BASIS SIZES"; size(A); size(AT);\n'

        # Exact infinity overideal, again with a different name order.
        "ring qB=0,(w,v,t),dp; option(redSB);\n"
        '"INDEPENDENT EXACT B VARIABLE ORDER"; var(1); var(2); var(3);\n'
        "if(var(1)!=w || var(2)!=v || var(3)!=t) "
        "{ \"EXACT B VARIABLE ORDER FAILED\"; exit(1); }\n"
        "map beta=s,t,v,w;\n"
        "if(beta(NAMEMARK)!=t+2*v+3*w) "
        "{ \"EXACT B NAME MAP FAILED\"; exit(1); }\n"
        "ideal JB=homog(beta(H1),t),homog(beta(H2),t),homog(beta(H3),t);\n"
        "poly lB=beta(LL); poly lhB=homog(lB,t); "
        "poly targetB=t^46*lhB^4;\n"
        "if(deg(targetB)!=78 || subst(targetB,t,1)!=lB^4) "
        "{ \"EXACT B TARGET FAILED\"; exit(1); }\n"
        "ideal BS=JB,t^16;\n"
        'LIB "resources.lib"; Resources::setcores(1); LIB "modstd.lib";\n'
        '"STAGE INDEPENDENT EXACT B RECONSTRUCTION";\n'
        'ideal B0=modGB("slimgb",BS,0); ideal B=slimgb(B0);\n'
        "if(size(reduce(BS,B))!=0 || size(reduce(JB,B))!=0 "
        "|| reduce(t^16,B)!=0 || reduce(targetB,B)!=0) "
        "{ \"EXACT B INCLUSION OR TARGET FAILED\"; exit(1); }\n"
        "for(i=1;i<=size(B);i++) { if(homog(B[i],t)!=B[i]) "
        "{ \"EXACT B HOMOGENEITY FAILED\"; exit(1); } }\n"
        "bigintvec bnum=hilb(B,1);\n"
        '"INDEPENDENT EXACT B HILBERT NUMERATOR"; bnum;\n'
        '"INDEPENDENT EXACT B BASIS SIZE"; size(B);\n'
        '"SOLE-PLANE THREE-DOUBLE INDEPENDENT ALGEBRA COMPLETE";\n'
    )
    return script


def hilbert_value(output: str, label: str, degree: int = 78) -> int:
    match = re.search(rf"{re.escape(label)}\s*\n([0-9,\-]+)", output)
    if match is None:
        raise RuntimeError(f"missing Hilbert vector {label!r}\n{output}")
    entries = [int(entry) for entry in match.group(1).split(",")]
    numerator = entries[:-1]
    return sum(
        coefficient * math.comb(degree - exponent + 2, 2)
        for exponent, coefficient in enumerate(numerator)
        if exponent <= degree
    )


def main() -> None:
    audit_row_and_exchange()
    polynomial = first_cross_polynomial()
    equations = evaluation_system(polynomial)
    assert polynomial.degree() <= 9
    assert len(equations) == 10
    audit_input_denominators(equations)

    result = subprocess.run(
        ("Singular", "--cpus=1", "-q"),
        input=singular_script(equations),
        text=True,
        capture_output=True,
        check=True,
        timeout=14400,
    )
    output = result.stdout
    if (result.stderr or "?" in output
            or "INDEPENDENT ALGEBRA COMPLETE" not in output):
        raise RuntimeError(output + result.stderr)

    modular_j = hilbert_value(
        output, "INDEPENDENT MODULAR J HILBERT NUMERATOR"
    )
    exact_a = hilbert_value(output, "INDEPENDENT EXACT A HILBERT NUMERATOR")
    exact_at = hilbert_value(
        output, "INDEPENDENT EXACT A+T16 HILBERT NUMERATOR"
    )
    exact_b = hilbert_value(output, "INDEPENDENT EXACT B HILBERT NUMERATOR")
    if (modular_j, exact_a, exact_at, exact_b) != (318, 192, 0, 126):
        raise RuntimeError(
            "unexpected degree-78 Hilbert values: "
            f"Jmod={modular_j}, A={exact_a}, A+t16={exact_at}, B={exact_b}"
        )

    ambient = math.comb(80, 2)
    modular_rank = ambient - modular_j
    # J is contained in C=A intersection B.  Since t^16 is in B,
    # A+(t^16) is contained in A+B; exact_at=0 therefore gives HF(A+B)=0.
    intersection_hf = exact_a + exact_b
    if (ambient, modular_rank, intersection_hf) != (3160, 2842, 318):
        raise RuntimeError("independent degree-78 squeeze arithmetic failed")

    print(output.strip())
    print("SOLE-PLANE 2^3 1^7 INDEPENDENT CLOSURE AUDIT PASS")
    print("audit prime / ambient / modular rank:",
          AUDIT_PRIME, ambient, modular_rank)
    print("HF(Jmod), HF(A), HF(A+t^16), HF(B), HF(A intersect B):",
          modular_j, exact_a, exact_at, exact_b, intersection_hf)


if __name__ == "__main__":
    main()
