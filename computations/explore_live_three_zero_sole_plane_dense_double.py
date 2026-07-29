#!/usr/bin/env python3
"""Exact reconnaissance for the sole-plane t=r+6 dense-double tail.

This is deliberately an exploration script until all structural charts of
the simultaneous pair-determinant system have been saturated.
"""

from __future__ import annotations

import argparse
import subprocess

import sympy as sp

from explore_live_three_zero_minimal_three_extra_ccb import singular_status
from verify_live_three_zero_sole_plane_fourth_high_frontier import (
    triple_quadratic_row,
)


x = sp.Symbol("x")
u, v, w = sp.symbols("u v w")
Au, Bu, Av, Bv, Aw, Bw = sp.symbols("Au Bu Av Bv Aw Bw")


def chi(anchor, selected):
    """First logarithmic-derivative increment for a selected double."""
    return 2 / (anchor + selected) - 3 / (selected - anchor)


def eta(anchor, selected):
    """Second logarithmic-derivative increment for a selected double."""
    return 2 / (anchor + selected) ** 2 + 3 / (selected - anchor) ** 2


def effective(anchor, selected, first, second):
    return first + chi(anchor, selected), second + eta(anchor, selected)


def pair_determinant(left, right, left_data, right_data):
    left_first, left_second = effective(left, right, *left_data)
    right_first, right_second = effective(right, left, *right_data)
    left_row = triple_quadratic_row(
        x, left, left_first, left_second
    )[:2]
    right_row = triple_quadratic_row(
        x, right, right_first, right_second
    )[:2]
    return sp.factor(sp.together(
        left_row[0] * right_row[1] - left_row[1] * right_row[0]
    ))


def primitive_numerator(value):
    numerator = sp.cancel(value).as_numer_denom()[0]
    return sp.Poly(numerator, x).primitive()[1].as_expr()


def cross_identity():
    f_uv = primitive_numerator(pair_determinant(
        u, v, (Au, Bu), (Av, Bv)
    ))
    f_uw = primitive_numerator(pair_determinant(
        u, w, (Au, Bu), (Aw, Bw)
    ))
    k_uv = sp.Poly(f_uv, x).coeff_monomial(x**8)
    k_uw = sp.Poly(f_uw, x).coeff_monomial(x**8)
    cross = sp.expand(k_uw * (x-v) * f_uv - k_uv * (x-w) * f_uw)
    return f_uv, f_uw, sp.Poly(cross, x)


P0, R0, Pv, Rv, Pw, Rw, lam = sp.symbols(
    "P0 R0 Pv Rv Pw Rw lambda"
)
mu = sp.Symbol("mu")
Pvw, Rvw, Pwv, Rwv = sp.symbols("Pvw Rvw Pwv Rwv")


def affine_row(anchor, first, square_plus_second):
    """Cleared order-three row in the (P,P^2+W) coordinates."""
    denominator = x**2 - anchor**2
    first_entry = sp.expand(
        square_plus_second * denominator**2
        - 2 * first * denominator * (x + 3*anchor)
        + 4 * (x**2 + 2*anchor*x + 3*anchor**2)
    )
    second_entry = sp.expand(
        2*first*denominator**2
        - 2*denominator*(x + 3*anchor)
        - anchor*first_entry
    )
    return first_entry, second_entry


def affine_pair(left, right, left_data, right_data):
    left_row = affine_row(left, *left_data)
    right_row = affine_row(right, *right_data)
    return sp.expand(
        left_row[0]*right_row[1] - left_row[1]*right_row[0]
    )


def normalized_cross_equations():
    """Return the u=1 simultaneous uv/uw cross-identity equations."""
    one = sp.S.One
    delta = (
        -(w + 5) / (w**2 - 1)
        + (v + 5) / (v**2 - 1)
    )
    epsilon = (
        2/(w+1)**2 + 3/(w-1)**2
        - 2/(v+1)**2 - 3/(v-1)**2
    )
    P0w = P0 + delta
    R0w = R0 + 2*P0*delta + delta**2 + epsilon
    f_uv = affine_pair(one, v, (P0, R0), (Pv, Rv))
    f_uw = affine_pair(one, w, (P0w, R0w), (Pw, Rw))
    cross = sp.Poly(sp.cancel(
        (x-v)*f_uv - lam*(x-w)*f_uw
    ).as_numer_denom()[0], x)
    return f_uv, f_uw, cross, sp.factor(delta), sp.factor(epsilon)


def normalized_triple_cross_equations():
    """Two coupled identities for the three repeated values 1,v,w."""
    one = sp.S.One

    def selected_chi(anchor, selected):
        return 2/(anchor+selected) - 3/(selected-anchor)

    def selected_eta(anchor, selected):
        return 2/(anchor+selected)**2 + 3/(selected-anchor)**2

    delta_1 = selected_chi(one, w) - selected_chi(one, v)
    epsilon_1 = selected_eta(one, w) - selected_eta(one, v)
    P0w = P0 + delta_1
    R0w = R0 + 2*P0*delta_1 + delta_1**2 + epsilon_1

    delta_v = selected_chi(v, w) - selected_chi(v, one)
    epsilon_v = selected_eta(v, w) - selected_eta(v, one)
    Pvw = Pv + delta_v
    Rvw = Rv + 2*Pv*delta_v + delta_v**2 + epsilon_v

    delta_w = selected_chi(w, v) - selected_chi(w, one)
    epsilon_w = selected_eta(w, v) - selected_eta(w, one)
    Pwv = Pw + delta_w
    Rwv = Rw + 2*Pw*delta_w + delta_w**2 + epsilon_w

    f_uv = affine_pair(one, v, (P0, R0), (Pv, Rv))
    f_uw = affine_pair(one, w, (P0w, R0w), (Pw, Rw))
    f_vw = affine_pair(v, w, (Pvw, Rvw), (Pwv, Rwv))
    first = sp.Poly(sp.cancel(
        (x-v)*f_uv - lam*(x-w)*f_uw
    ).as_numer_denom()[0], x)
    second = sp.Poly(sp.cancel(
        (x-one)*f_uv - mu*(x-w)*f_vw
    ).as_numer_denom()[0], x)
    return f_uv, f_uw, f_vw, first, second


def normalized_full_pair_system():
    """Three pair determinants with unspecialized cyclic endpoint rows."""
    f_uv, f_uw, first, _delta, _epsilon = normalized_cross_equations()
    f_vw = affine_pair(v, w, (Pvw, Rvw), (Pwv, Rwv))
    second = sp.Poly(
        (x-1)*f_uv - mu*(x-w)*f_vw, x
    )

    def selected_chi(anchor, selected):
        return 2/(anchor+selected) - 3/(selected-anchor)

    def selected_eta(anchor, selected):
        return 2/(anchor+selected)**2 + 3/(selected-anchor)**2

    delta_v = sp.factor(
        selected_chi(v, w) - selected_chi(v, 1)
    )
    epsilon_v = sp.factor(
        selected_eta(v, w) - selected_eta(v, 1)
    )
    delta_w = sp.factor(
        selected_chi(w, v) - selected_chi(w, 1)
    )
    epsilon_w = sp.factor(
        selected_eta(w, v) - selected_eta(w, 1)
    )
    exchanges = (
        Pvw - Pv - delta_v,
        Rvw - Rv - 2*Pv*delta_v - delta_v**2 - epsilon_v,
        Pwv - Pw - delta_w,
        Rwv - Rw - 2*Pw*delta_w - delta_w**2 - epsilon_w,
    )
    return first, second, exchanges


def singular_generic_status(
    polynomials, variables, lift_during=False, audit_denominators=False,
):
    generators = [
        str(sp.Poly(
            polynomial, *variables, domain=sp.QQ.frac_field(v, w)
        ).as_expr()).replace("**", "^")
        for polynomial in polynomials
    ]
    script = (
        f"ring r=(0,v,w),({','.join(map(str, variables))}),dp;\n"
        f"ideal I={','.join(generators)};\n"
        "option(redSB);\n"
    )
    if lift_during:
        script += "matrix T; ideal G=liftstd(I,T);\n"
    else:
        script += "ideal G=std(I);\n"
    script += (
        'if (size(G)==1 && deg(G[1])==0) { "GENERIC UNIT"; } '
        'else { "GENERIC NONUNIT"; dim(G); size(G); }\n'
    )
    if lift_during:
        if audit_denominators:
            script += (
                'list DL; int ii,jj; poly pp; number cc; '
                '"LIFT MATRIX SHAPE"; nrows(T); ncols(T); '
                'for(ii=1;ii<=nrows(T);ii++) '
                '{ for(jj=1;jj<=ncols(T);jj++) '
                '{ pp=T[ii,jj]; while(pp!=0) '
                '{ cc=leadcoef(pp); DL[size(DL)+1]=denominator(cc); '
                'pp=pp-lead(pp); } } }\n'
                '"LIFT COEFFICIENT COUNT"; size(DL);\n'
                'def DENLIST=DL;\n'
            )
        script += (
            'def H=G[1]; ring s=0,(v,w),dp; poly h=imap(r,H);\n'
            '"FULL CONSTANT FACTORIZATION"; factorize(h);\n'
        )
        if audit_denominators:
            script += (
                'list dl=imap(r,DENLIST); poly alld=1; poly dd; '
                'for(ii=1;ii<=size(dl);ii++) '
                '{ dd=dl[ii]; alld=alld*dd/gcd(alld,dd); }\n'
                '"LIFT DENOMINATOR LCM DEGREE"; deg(alld);\n'
                '"LIFT DENOMINATOR LCM FACTORIZATION"; factorize(alld);\n'
            )
    result = subprocess.run(
        ("Singular", "-q"), input=script, text=True,
        capture_output=True, check=True, timeout=900,
    )
    if "?" in result.stdout:
        raise RuntimeError(result.stdout)
    return result.stdout.strip()


def singular_combined_parameter_status(
    first_system, full_system, variables, prime=32003,
    modular_exact=False, projective_probe=False,
    projective_local_probe=False,
):
    def generators(equations):
        return [
            str(sp.Poly(
                equation, *variables, domain=sp.QQ.frac_field(v, w)
            ).as_expr()).replace("**", "^")
            for equation in equations
        ]

    cleared_full = []
    homogenized_full = []
    sigma = sp.Symbol("sigma")
    polynomial_variables = variables + (v, w)
    for equation in full_system:
        numerator = sp.cancel(equation).as_numer_denom()[0]
        integral = sp.Poly(
            numerator, *polynomial_variables, domain=sp.QQ
        ).clear_denoms()[1].as_expr()
        cleared_full.append(
            str(sp.expand(integral)).replace("**", "^")
        )
        integral_poly = sp.Poly(integral, *polynomial_variables)
        local_degree = max(
            sum(monomial[:len(variables)])
            for monomial, _coefficient in integral_poly.terms()
        )
        homogeneous = sp.S.Zero
        for monomial, coefficient in integral_poly.terms():
            term = coefficient
            for variable, exponent in zip(
                polynomial_variables, monomial, strict=True,
            ):
                term *= variable**exponent
            term *= sigma**(
                local_degree - sum(monomial[:len(variables)])
            )
            homogeneous += term
        homogenized_full.append(
            str(sp.expand(homogeneous)).replace("**", "^")
        )

    certificate_prefix = (
        f"ring r=(0,v,w),({','.join(map(str, variables))}),dp;\n"
        "option(redSB);\n"
        f"ideal IA={','.join(generators(first_system))};\n"
        "matrix TA; ideal GA=liftstd(IA,TA); def HA=GA[1];\n"
        '"STAGE first certificate";\n'
        f"ideal IB={','.join(generators(full_system))};\n"
        "matrix TB; ideal GB=liftstd(IB,TB); def HB=GB[1];\n"
        '"STAGE full certificate";\n'
        'ring s=0,(t,v,w),dp;\n'
        'poly a1=imap(r,HA); poly ah=homog(a1,t);\n'
        'poly a2=subst(subst(ah,v,1),t,v);\n'
        'poly a3=subst(subst(subst(ah,v,1),w,v),t,w);\n'
        'poly b1=imap(r,HB); poly bh=homog(b1,t);\n'
        'poly b2=subst(subst(bh,v,1),t,v);\n'
        'poly b3=subst(subst(subst(bh,v,1),w,v),t,w);\n'
        'def A1=a1; def A2=a2; def A3=a3;\n'
        'def B1=b1; def B2=b2; def B3=b3;\n'
    )
    if projective_probe:
        script = certificate_prefix + (
            f'ring q={prime},(t,v,w),dp;\n'
            'poly a1=imap(s,A1); poly a2=imap(s,A2); poly a3=imap(s,A3);\n'
            'poly b1=imap(s,B1); poly b2=imap(s,B2); poly b3=imap(s,B3);\n'
            'poly L=v*w*(v-1)*(v+1)*(w-1)*(w+1)*(v-w)*(v+w);\n'
            'poly d;\n'
        )
        for name in ("a1", "a2", "a3", "b1", "b2", "b3"):
            script += (
                f"d=gcd({name},L); while(d!=1) "
                f"{{ {name}={name}/d; d=gcd({name},L); }}\n"
            )
        script += (
            'poly at1=subst(homog(a1,t),t,0); '
            'poly at2=subst(homog(a2,t),t,0); '
            'poly at3=subst(homog(a3,t),t,0);\n'
            'poly bt1=subst(homog(b1,t),t,0); '
            'poly bt2=subst(homog(b2,t),t,0); '
            'poly bt3=subst(homog(b3,t),t,0);\n'
            'poly topg=gcd(gcd(gcd(at1,at2),at3),gcd(gcd(bt1,bt2),bt3));\n'
            '"PARAMETER INFINITY TOP GCD"; deg(topg); factorize(topg);\n'
        )
    else:
        script = certificate_prefix + (
        f'ring q={prime},(v,w),dp;\n'
        'poly a1=imap(s,A1); poly a2=imap(s,A2); poly a3=imap(s,A3);\n'
        'poly b1=imap(s,B1); poly b2=imap(s,B2); poly b3=imap(s,B3);\n'
        'poly L=v*w*(v-1)*(v+1)*(w-1)*(w+1)*(v-w)*(v+w);\n'
        'poly d;\n'
        )
        for name in ("a1", "a2", "a3", "b1", "b2", "b3"):
            script += (
                f"d=gcd({name},L); while(d!=1) "
                f"{{ {name}={name}/d; d=gcd({name},L); }}\n"
            )
        parameter_basis = (
            'LIB "resources.lib"; Resources::setcores(1); '
            'LIB "modstd.lib"; '
            'ideal K=modGB("slimgb",ideal(a1,a2,a3,b1,b2,b3),1);\n'
            if modular_exact else
            'ideal K=slimgb(ideal(a1,a2,a3,b1,b2,b3));\n'
        )
        full_basis = (
            'ideal U=modGB("slimgb",Z,1);\n'
            if modular_exact else
            'ideal U=slimgb(Z);\n'
        )
        script += (
        '"STRIPPED DEGREES"; '
        'deg(a1);deg(a2);deg(a3);deg(b1);deg(b2);deg(b3);\n'
        + parameter_basis
        +
        'if (size(K)==1 && K[1]==1) { "COMBINED PARAMETER UNIT"; } '
        'else { "COMBINED PARAMETER NONUNIT"; dim(K); size(K); }\n'
        + ('"PARAMETER BASIS"; K;\n'
           if prime and not projective_local_probe else '')
        +
        'def ParamK=K;\n'
        f"ring z={prime},({','.join(map(str, variables))},v,w,tau),"
        f"(dp({len(variables)}),dp(2),dp(1));\n"
        'ideal PK=imap(q,ParamK);\n'
        f"ideal F={','.join(cleared_full)};\n"
        'poly L=v*w*(v-1)*(v+1)*(w-1)*(w+1)*(v-w)*(v+w);\n'
        'ideal Z=PK,F,1-tau*L;\n'
        '"STAGE finite full fibre";\n'
        + full_basis
        +
        'if (size(U)==1 && U[1]==1) { "FINITE FULL FIBRE UNIT"; } '
        'else { "FINITE FULL FIBRE NONUNIT"; dim(U); size(U); }\n'
        )
        if projective_local_probe:
            boundary_factors = (
                "v", "w", "v-1", "v+1", "w-1", "w+1",
                "v-w", "v+w",
            )
            boundary_code = '"PARAMETER BOUNDARY INTERSECTIONS"; ideal KB;\n'
            for index, factor in enumerate(boundary_factors, 1):
                boundary_code += (
                    f'KB=slimgb(ideal(K,{factor})); '
                    f'if(size(KB)==1 && KB[1]==1) '
                    f'{{ "BOUNDARY EMPTY {index} {factor}"; }} '
                    f'else {{ "BOUNDARY HIT {index} {factor}"; '
                    'dim(KB); size(KB); }\n'
                )
            # Insert before ParamK is transported to the full-system ring.
            marker = 'def ParamK=K;\n'
            script = script.replace(marker, boundary_code + marker, 1)
        if projective_local_probe:
            local_count = len(variables)
            script += (
                'def ParamK2=PK;\n'
                f"ring zp={prime},({','.join(map(str, variables))},sigma,v,w),"
                f"(dp({local_count + 1}),dp(2));\n"
                'ideal PK2=imap(z,ParamK2);\n'
                f"ideal FH={','.join(homogenized_full)};\n"
                '"LOCAL PROJECTIVE AFFINE CHART";\n'
                'ideal IP=PK2,FH,sigma-1; ideal UP=slimgb(IP);\n'
                'if(size(UP)==1 && UP[1]==1) { "AFFINE ALL-PARAMETER UNIT"; } '
                'else { "AFFINE ALL-PARAMETER NONUNIT"; dim(UP); size(UP); }\n'
                '"LOCAL PROJECTIVE INFINITY CHARTS"; int chart; ideal IC,UC;\n'
                f'for(chart=1;chart<={local_count};chart++) '
                '{ IC=PK2,FH,sigma,var(chart)-1; UC=slimgb(IC); '
                'if(size(UC)==1 && UC[1]==1) '
                '{ "INFINITY CHART UNIT"; chart; } '
                'else { "INFINITY CHART NONUNIT"; chart; dim(UC); size(UC); break; } }\n'
            )
    result = subprocess.run(
        ("Singular", "-q"), input=script, text=True,
        check=True, timeout=900,
    )
    return f"Singular exit {result.returncode}"


def singular_coefficient_field(
    equations, lift=False, lift_during=False, audit_denominators=False,
):
    variables = (P0, R0, Pv, Rv, Pw, Rw, lam)
    generators = [
        str(sp.Poly(eq, *variables, domain=sp.QQ.frac_field(v, w)).as_expr())
        .replace("**", "^")
        for eq in equations
    ]
    script = (
        'ring r=(0,v,w),(P0,R0,Pv,Rv,Pw,Rw,lambda),dp;\n'
        f"ideal I={','.join(generators)};\n"
        "option(redSB);\n"
    )
    if lift_during:
        script += "matrix T; ideal G=liftstd(I,T);\n"
    else:
        script += "ideal G=std(I);\n"
    script += (
        'if (size(G)==1 && deg(G[1])==0) { "UNIT"; } '
        'else { "NONUNIT"; dim(G); size(G); G; }\n'
    )
    if lift:
        script += "matrix T=lift(I,G);\n\"LIFT\";\nT;\n"
    if lift_during:
        if audit_denominators:
            script += (
                'list DL; int ii,jj; poly pp; number cc; '
                '"LIFT MATRIX SHAPE"; nrows(T); ncols(T); '
                'for(ii=1;ii<=nrows(T);ii++) '
                '{ for(jj=1;jj<=ncols(T);jj++) '
                '{ pp=T[ii,jj]; while(pp!=0) '
                '{ cc=leadcoef(pp); DL[size(DL)+1]=denominator(cc); '
                'pp=pp-lead(pp); } } }\n'
                '"LIFT COEFFICIENT COUNT"; size(DL);\n'
                'def DENLIST=DL;\n'
            )
        script += (
            'def H=G[1];\n'
            'ring s=0,(v,w),dp;\n'
            'poly h=imap(r,H);\n'
            '"LIFTSTD CONSTANT FACTORIZATION";\n'
            'factorize(h);\n'
        )
        if audit_denominators:
            script += (
                'list dl=imap(r,DENLIST); poly alld=1; poly dd; '
                'for(ii=1;ii<=size(dl);ii++) '
                '{ dd=dl[ii]; alld=alld*dd/gcd(alld,dd); }\n'
                '"LIFT DENOMINATOR LCM DEGREE"; deg(alld);\n'
                '"LIFT DENOMINATOR LCM FACTORIZATION"; factorize(alld);\n'
            )
    result = subprocess.run(
        ("Singular", "-q"), input=script, text=True,
        capture_output=True, check=True, timeout=900,
    )
    if result.stderr:
        print(result.stderr)
    return result.stdout


def singular_plain_status(polynomials, variables, localizer=None):
    generators = []
    for polynomial in polynomials:
        integral = sp.Poly(
            polynomial, *variables, domain=sp.QQ
        ).clear_denoms()[1].as_expr()
        generators.append(str(sp.expand(integral)).replace("**", "^"))
    names = list(map(str, variables))
    if localizer is not None:
        names.append("tau")
        generators.append(
            "1-tau*("
            + str(sp.expand(localizer)).replace("**", "^")
            + ")"
        )
    script = (
        f"ring r=0,({','.join(names)}),dp;\n"
        f"ideal I={','.join(generators)};\n"
        "option(redSB); ideal G=std(I);\n"
        'if (size(G)==1 && G[1]==1) { "UNIT"; } '
        'else { "NONUNIT"; dim(G); size(G); }\n'
    )
    result = subprocess.run(
        ("Singular", "-q"), input=script, text=True,
        capture_output=True, check=True, timeout=900,
    )
    if "?" in result.stdout:
        raise RuntimeError(result.stdout)
    return result.stdout.strip()


def singular_multi_certificate_status(
    systems, variables=(P0, R0, Pv, Rv, Pw, Rw, lam)
):

    def generators(equations):
        return [
            str(sp.Poly(
                equation, *variables, domain=sp.QQ.frac_field(v, w)
            ).as_expr()).replace("**", "^")
            for equation in equations
        ]

    script = (
        f"ring r=(0,v,w),({','.join(map(str, variables))}),dp;\n"
        'option(redSB);\n'
    )
    for index, equations in enumerate(systems, 1):
        script += (
            f"ideal I{index}={','.join(generators(equations))};\n"
            f"matrix T{index}; ideal G{index}=liftstd(I{index},T{index});\n"
            f"if (size(G{index})!=1 || deg(G{index}[1])!=0) "
            f'{{ "GENERIC NONUNIT {index}"; }}\n'
            f"def H{index}=G{index}[1];\n"
        )
    script += 'ring s=0,(tau,v,w),dp;\n'
    for index in range(1, len(systems)+1):
        script += f"poly h{index}=imap(r,H{index});\n"
    structural = "v*w*(v-1)*(v+1)*(w-1)*(w+1)*(v-w)*(v+w)"
    script += (
        "ideal J="
        + ",".join(f"h{index}" for index in range(1, len(systems)+1))
        + f",1-tau*({structural});\n"
        + "ideal K=std(J);\n"
        + 'if (size(K)==1 && K[1]==1) { "PARAMETER SATURATION UNIT"; } '
        + 'else { "PARAMETER SATURATION NONUNIT"; dim(K); size(K); K; }\n'
    )
    result = subprocess.run(
        ("Singular", "-q"), input=script, text=True,
        capture_output=True, check=True, timeout=900,
    )
    if "?" in result.stdout:
        raise RuntimeError(result.stdout)
    return result.stdout.strip()


def singular_orbit_certificate_status(equations, prime=0):
    """Track one parameter certificate and its cyclic scale transform."""
    variables = (P0, R0, Pv, Rv, Pw, Rw, lam)
    generators = [
        str(sp.Poly(
            equation, *variables, domain=sp.QQ.frac_field(v, w)
        ).as_expr()).replace("**", "^")
        for equation in equations
    ]
    script = (
        'ring r=(0,v,w),(P0,R0,Pv,Rv,Pw,Rw,lambda),dp;\n'
        'option(redSB);\n'
        f"ideal I={','.join(generators)};\n"
        "matrix T; ideal G=liftstd(I,T);\n"
        '"STAGE liftstd";\n'
        'if (size(G)!=1 || deg(G[1])!=0) { "GENERIC NONUNIT"; }\n'
        "def H=G[1];\n"
        'ring s=0,(t,v,w),dp;\n'
        'poly h1=imap(r,H);\n'
        'poly hhom=homog(h1,t);\n'
        'poly h2=subst(subst(hhom,v,1),t,v);\n'
        'poly h3=subst(subst(subst(hhom,v,1),w,v),t,w);\n'
        '"STAGE transforms";\n'
        'def HH1=h1; def HH2=h2; def HH3=h3;\n'
        f'ring q={prime},(v,w),dp;\n'
        'poly q1=imap(s,HH1); poly q2=imap(s,HH2); poly q3=imap(s,HH3);\n'
        'poly localizer=v*w*(v-1)*(v+1)*(w-1)*(w+1)*(v-w)*(v+w);\n'
        'poly divisor=gcd(q1,localizer);\n'
        'while (divisor!=1) { q1=q1/divisor; divisor=gcd(q1,localizer); }\n'
        'divisor=gcd(q2,localizer);\n'
        'while (divisor!=1) { q2=q2/divisor; divisor=gcd(q2,localizer); }\n'
        'divisor=gcd(q3,localizer);\n'
        'while (divisor!=1) { q3=q3/divisor; divisor=gcd(q3,localizer); }\n'
        '"STAGE stripped";\n'
        '"STRIPPED DEGREES"; deg(q1); deg(q2); deg(q3);\n'
        "ideal K12=std(ideal(q1,q2));\n"
        '"STAGE K12";\n'
        'poly remainder=reduce(q3,K12);\n'
        '"THIRD REMAINDER"; deg(remainder); size(remainder);\n'
        "ideal J=K12,remainder; ideal K=std(J);\n"
        'if (size(K)==1 && K[1]==1) { "ORBIT IDEAL UNIT"; } '
        'else { "ORBIT IDEAL NONUNIT"; dim(K); size(K); }\n'
    )
    result = subprocess.run(
        ("Singular", "-q"), input=script, text=True,
        check=True, timeout=900,
    )
    return f"Singular exit {result.returncode}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--generic-sample", action="store_true")
    parser.add_argument("--coefficient-field", action="store_true")
    parser.add_argument("--lift", action="store_true")
    parser.add_argument("--liftstd", action="store_true")
    parser.add_argument("--show-normalized", action="store_true")
    parser.add_argument("--full-saturation", action="store_true")
    parser.add_argument("--full-plain", action="store_true")
    parser.add_argument("--minimal-subset", action="store_true")
    parser.add_argument("--evaluation-system", action="store_true")
    parser.add_argument("--multi-cert", action="store_true")
    parser.add_argument("--evaluation-alt", action="store_true")
    parser.add_argument("--triple-cert", action="store_true")
    parser.add_argument("--orbit-cert", action="store_true")
    parser.add_argument("--orbit-modular", action="store_true")
    parser.add_argument("--full-pair-system", action="store_true")
    parser.add_argument("--combined-param", action="store_true")
    parser.add_argument("--combined-param-exact", action="store_true")
    parser.add_argument("--combined-param-modstd", action="store_true")
    parser.add_argument("--denominator-audit", action="store_true")
    parser.add_argument("--projective-probe", action="store_true")
    parser.add_argument("--projective-local-probe", action="store_true")
    parser.add_argument("--show", action="store_true")
    args = parser.parse_args()

    if args.show or args.generic_sample:
        f_uv, f_uw, cross = cross_identity()
        print("pair degrees", sp.degree(f_uv, x), sp.degree(f_uw, x))
        print("cross degree", cross.degree())
        coefficients = tuple(cross.all_coeffs())
        if args.show:
            print("k_uv =", sp.factor(
                sp.Poly(f_uv, x).coeff_monomial(x**8)
            ))
            print("k_uw =", sp.factor(
                sp.Poly(f_uw, x).coeff_monomial(x**8)
            ))
            for degree, coefficient in zip(
                range(cross.degree(), -1, -1), coefficients, strict=True
            ):
                print(f"C{degree} =", sp.factor(coefficient))
        if args.generic_sample:
            sample = {u: 2, v: 3, w: 5}
            specialized = tuple(sp.cancel(c.subs(sample)) for c in coefficients)
            print("generic sample status", singular_status(
                specialized, (Au, Bu, Av, Bv, Aw, Bw)
            ))
    if (args.coefficient_field or args.show_normalized
            or args.full_saturation or args.full_plain
            or args.minimal_subset or args.evaluation_system
            or args.multi_cert or args.evaluation_alt
            or args.triple_cert or args.orbit_cert
            or args.orbit_modular or args.full_pair_system
            or args.combined_param or args.combined_param_exact
            or args.combined_param_modstd or args.denominator_audit
            or args.projective_probe or args.projective_local_probe):
        _fuv, _fuw, normalized, delta, epsilon = (
            normalized_cross_equations()
        )
        print("normalized cross degree", normalized.degree())
        print("delta", delta)
        print("epsilon", epsilon)
        if args.show_normalized:
            for degree in range(9, -1, -1):
                print(f"N{degree} =", sp.factor(
                    normalized.coeff_monomial(x**degree)
                ))
        if args.coefficient_field:
            print(singular_coefficient_field(
                normalized.all_coeffs(), lift=args.lift,
                lift_during=args.liftstd,
            ))
        if args.full_saturation:
            structural = (
                v*w*(v-1)*(v+1)*(w-1)*(w+1)*(v-w)*(v+w)
            )
            print("full saturation", singular_plain_status(
                normalized.all_coeffs(),
                (P0, R0, Pv, Rv, Pw, Rw, lam, v, w),
                localizer=structural,
            ))
        if args.full_plain:
            print("full plain", singular_plain_status(
                normalized.all_coeffs(),
                (P0, R0, Pv, Rv, Pw, Rw, lam, v, w),
            ))
        if args.minimal_subset:
            indexed = list(enumerate(normalized.all_coeffs()))
            changed = True
            while changed:
                changed = False
                for position in range(len(indexed)):
                    trial = indexed[:position] + indexed[position+1:]
                    status = singular_coefficient_field(
                        [equation for _index, equation in trial]
                    ).strip()
                    print("drop", indexed[position][0], status)
                    if status == "UNIT":
                        indexed = trial
                        changed = True
                        break
            print("minimal indices", [index for index, _eq in indexed])
        if args.evaluation_system:
            expression = normalized.as_expr()
            derivative = sp.diff(expression, x)
            evaluations = (
                expression.subs(x, v), expression.subs(x, w),
                expression.subs(x, 1), expression.subs(x, -1),
                expression.subs(x, -v), expression.subs(x, -w),
                expression.subs(x, 0),
                derivative.subs(x, v), derivative.subs(x, w),
                derivative.subs(x, 1), derivative.subs(x, -1),
            )
            print("evaluation status", singular_coefficient_field(
                evaluations, lift=args.lift,
                lift_during=args.liftstd,
            ))
        if args.evaluation_alt:
            expression = normalized.as_expr()
            derivative = sp.diff(expression, x)
            alternative = (
                expression.subs(x, v), expression.subs(x, w),
                expression.subs(x, 1), expression.subs(x, -1),
                expression.subs(x, -v), expression.subs(x, -w),
                expression.subs(x, 0),
                derivative.subs(x, -v), derivative.subs(x, -w),
                derivative.subs(x, 0),
            )
            print("alternative evaluation status", singular_coefficient_field(
                alternative, lift=args.lift,
                lift_during=args.liftstd,
                audit_denominators=args.denominator_audit,
            ))
        if args.multi_cert:
            expression = normalized.as_expr()
            derivative = sp.diff(expression, x)
            special = (
                expression.subs(x, v), expression.subs(x, w),
                expression.subs(x, 1), expression.subs(x, -1),
                expression.subs(x, -v), expression.subs(x, -w),
                expression.subs(x, 0),
                derivative.subs(x, v), derivative.subs(x, w),
                derivative.subs(x, 1), derivative.subs(x, -1),
            )
            constant = tuple(
                expression.subs(x, value) for value in range(10)
            )
            coefficients = tuple(normalized.all_coeffs())
            print(singular_multi_certificate_status(
                (special, constant, coefficients)
            ))
        if args.triple_cert:
            _uv, _uw, _vw, first, second = (
                normalized_triple_cross_equations()
            )

            def alt_evaluations(polynomial):
                expression = polynomial.as_expr()
                derivative = sp.diff(expression, x)
                return (
                    expression.subs(x, v), expression.subs(x, w),
                    expression.subs(x, 1), expression.subs(x, -1),
                    expression.subs(x, -v), expression.subs(x, -w),
                    expression.subs(x, 0),
                    derivative.subs(x, -v), derivative.subs(x, -w),
                    derivative.subs(x, 0),
                )

            print("triple degrees", first.degree(), second.degree())
            print(singular_multi_certificate_status(
                (alt_evaluations(first), alt_evaluations(second)),
                variables=(P0, R0, Pv, Rv, Pw, Rw, lam, mu),
            ))
        if args.orbit_cert or args.orbit_modular:
            expression = normalized.as_expr()
            derivative = sp.diff(expression, x)
            alternative = (
                expression.subs(x, v), expression.subs(x, w),
                expression.subs(x, 1), expression.subs(x, -1),
                expression.subs(x, -v), expression.subs(x, -w),
                expression.subs(x, 0),
                derivative.subs(x, -v), derivative.subs(x, -w),
                derivative.subs(x, 0),
            )
            print(singular_orbit_certificate_status(
                alternative, prime=(32003 if args.orbit_modular else 0)
            ))
        if args.full_pair_system:
            first, second, exchanges = normalized_full_pair_system()

            def alt_evaluations(polynomial):
                expression = polynomial.as_expr()
                derivative = sp.diff(expression, x)
                return (
                    expression.subs(x, v), expression.subs(x, w),
                    expression.subs(x, 1), expression.subs(x, -1),
                    expression.subs(x, -v), expression.subs(x, -w),
                    expression.subs(x, 0),
                    derivative.subs(x, -v), derivative.subs(x, -w),
                    derivative.subs(x, 0),
                )

            variables = (
                P0, R0, Pv, Rv, Pw, Rw, Pvw, Rvw, Pwv, Rwv,
                lam, mu,
            )
            equations = (
                alt_evaluations(first) + alt_evaluations(second)
                + exchanges
            )
            print("full pair equations", len(equations))
            print(singular_generic_status(
                equations, variables, lift_during=args.liftstd
                , audit_denominators=args.denominator_audit
            ))
        if (args.combined_param or args.combined_param_exact
                or args.combined_param_modstd or args.projective_probe
                or args.projective_local_probe):
            first, second, exchanges = normalized_full_pair_system()

            def alt_evaluations(polynomial):
                expression = polynomial.as_expr()
                derivative = sp.diff(expression, x)
                return (
                    expression.subs(x, v), expression.subs(x, w),
                    expression.subs(x, 1), expression.subs(x, -1),
                    expression.subs(x, -v), expression.subs(x, -w),
                    expression.subs(x, 0),
                    derivative.subs(x, -v), derivative.subs(x, -w),
                    derivative.subs(x, 0),
                )

            variables = (
                P0, R0, Pv, Rv, Pw, Rw, Pvw, Rvw, Pwv, Rwv,
                lam, mu,
            )
            first_system = alt_evaluations(first)
            full_system = (
                first_system + alt_evaluations(second) + exchanges
            )
            print(singular_combined_parameter_status(
                first_system, full_system, variables,
                prime=(0 if (args.combined_param_exact
                             or args.combined_param_modstd) else 32003),
                modular_exact=args.combined_param_modstd,
                projective_probe=args.projective_probe,
                projective_local_probe=args.projective_local_probe,
            ))


if __name__ == "__main__":
    main()
