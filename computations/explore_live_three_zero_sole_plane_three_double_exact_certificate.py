#!/usr/bin/env python3
"""Characteristic-zero certificate reconnaissance for the 2^3 1^7 frontier.

This keeps the six cyclic parameter obstructions and the full twenty-four
local equations in one Singular process.  The default run is exploratory:
``modGB(...,0)`` reconstructs a rational parameter basis without certifying
it.  The optional verification stages are deliberately separate so that a
probabilistic reconstruction is never mistaken for a proof.
"""

from __future__ import annotations

import argparse
from itertools import combinations
import subprocess

import sympy as sp

from verify_live_three_zero_sole_plane_fourth_high_three_double_frontier import (
    LOCAL_VARIABLES,
    STRUCTURAL_FACTORS,
    alternative_evaluations,
    systems,
)


v, w = sp.symbols("v w")


def _generators(equations: tuple[sp.Expr, ...]) -> str:
    return ",".join(
        str(sp.Poly(
            equation,
            *LOCAL_VARIABLES,
            domain=sp.QQ.frac_field(v, w),
        ).as_expr()).replace("**", "^")
        for equation in equations
    )


def singular_script(mode: str, cores: int) -> str:
    first_system, full_system = systems()
    names = ",".join(map(str, LOCAL_VARIABLES))
    script = (
        f"ring r=(0,v,w),({names}),dp;\n"
        "option(redSB);\n"
        f"ideal IA={_generators(first_system)};\n"
        "matrix TA; ideal GA=liftstd(IA,TA); def HA=GA[1];\n"
        '"STAGE first lift";\n'
        f"ideal IB={_generators(full_system)};\n"
        "matrix TB; ideal GB=liftstd(IB,TB); def HB=GB[1];\n"
        '"STAGE full lift";\n'
        "ring s=0,(t,v,w),dp;\n"
        "poly a1=imap(r,HA); poly ah=homog(a1,t);\n"
        "poly a2=subst(subst(ah,v,1),t,v);\n"
        "poly a3=subst(subst(subst(ah,v,1),w,v),t,w);\n"
        "poly b1=imap(r,HB); poly bh=homog(b1,t);\n"
        "poly b2=subst(subst(bh,v,1),t,v);\n"
        "poly b3=subst(subst(subst(bh,v,1),w,v),t,w);\n"
        "poly L=v*w*(v-1)*(v+1)*(w-1)*(w+1)*(v-w)*(v+w);\n"
        "poly d;\n"
    )
    for name in ("a1", "a2", "a3", "b1", "b2", "b3"):
        script += (
            f"d=gcd({name},L); while(d!=1) "
            f"{{ {name}={name}/d; d=gcd({name},L); }}\n"
        )
    script += (
        "ideal I=a1,a2,a3,b1,b2,b3;\n"
        "LIB \"resources.lib\"; "
        f"Resources::setcores({cores});\n"
        "LIB \"modstd.lib\";\n"
    )
    if mode == "generator_stats":
        script += (
            '"GENERATOR TERM COUNTS"; '
            'size(a1);size(a2);size(a3);size(b1);size(b2);size(b3);\n'
            '"GENERATOR DEGREES"; '
            'deg(a1);deg(a2);deg(a3);deg(b1);deg(b2);deg(b3);\n'
            'poly ha1=subst(homog(a1,t),t,0); '
            'poly ha2=subst(homog(a2,t),t,0); '
            'poly ha3=subst(homog(a3,t),t,0);\n'
            'poly hg=gcd(gcd(ha1,ha2),ha3);\n'
            '"H-ORBIT INFINITY GCD"; factorize(hg);\n'
        )
    elif mode == "parameter_probabilistic":
        script += (
            '"STAGE probabilistic rational parameter basis";\n'
            'timer=1; ideal K=modGB("slimgb",I,0); timer=0;\n'
            '"PARAMETER BASIS DATA"; size(K); dim(K); vdim(K);\n'
            '"LEADING MONOMIALS"; lead(K);\n'
        )
    elif mode == "parameter_exact":
        script += (
            '"STAGE exact modular rational parameter basis";\n'
            'timer=1; ideal K=modGB("slimgb",I,1); timer=0;\n'
            '"PARAMETER BASIS DATA"; size(K); dim(K); vdim(K);\n'
            '"LEADING MONOMIALS"; lead(K);\n'
        )
    elif mode in (
        "saturated_parameter_modular",
        "nilpotency_modular",
        "subset_saturation_modular",
        "selected_subset_modular",
        "orbit_nilpotency_modular",
        "h_lift_modular",
    ):
        script += (
            "def II=I; def LL=L;\n"
            "ring q=32003,(tau,v,w),(dp(1),dp(2));\n"
            "ideal J=imap(s,II),1-tau*imap(s,LL);\n"
        )
        if mode == "saturated_parameter_modular":
            script += (
                'timer=1; ideal G=slimgb(J); timer=0;\n'
                '"SATURATED MODULAR DATA"; size(G); dim(G); vdim(G);\n'
                "ideal E=eliminate(G,tau);\n"
                '"ELIMINATION DATA"; size(E); dim(E); vdim(E); lead(E);\n'
            )
        elif mode in (
            "nilpotency_modular",
            "orbit_nilpotency_modular",
            "h_lift_modular",
        ):
            script += (
                "ring q2=32003,(v,w),dp;\n"
            )
            if mode == "h_lift_modular":
                script += (
                    "ideal H=imap(s,a1),imap(s,a2),imap(s,a3); "
                    "poly L2=imap(s,LL); ideal target=L2^4; matrix U;\n"
                    'timer=1; matrix T=lift(H,target,U,"slimgb"); timer=0;\n'
                    'if(matrix(target)*U-matrix(H)*T!=0) '
                    '{ "BAD MODULAR LIFT"; exit(1); }\n'
                    '"H LIFT SHAPE"; nrows(T); ncols(T);\n'
                    '"H LIFT DEGREES"; deg(T[1,1]); deg(T[2,1]); deg(T[3,1]);\n'
                    '"H LIFT TERM COUNTS"; size(T[1,1]); size(T[2,1]); size(T[3,1]);\n'
                )
                return script
            subsets = (
                ((("a1", "a2", "a3", "b1", "b2", "b3"), "ALL"),)
                if mode == "nilpotency_modular" else (
                    (("a1", "a2", "a3"), "H_ORBIT"),
                    (("b1", "b2", "b3"), "B_ORBIT"),
                    (("a1", "a2", "b1"), "MIXED_TRIPLE"),
                )
            )
            for subset, tag in subsets:
                joined = ",".join(f"imap(s,{name})" for name in subset)
                script += (
                    f"ideal K=slimgb(ideal({joined})); "
                    "poly L2=imap(s,LL); poly p=1; int n;\n"
                    "for(n=1;n<=40;n++) { p=reduce(p*L2,K); "
                    f'if(p==0) {{ "NILPOTENCY {tag}"; n; break; }} }}\n'
                    f'if(p!=0) {{ "NILPOTENCY ABOVE 40 {tag}"; }}\n'
                    f'"QUOTIENT {tag}"; size(K); dim(K); vdim(K);\n'
                )
        elif mode == "subset_saturation_modular":
            script += '"MINIMAL SATURATED SUBSETS"; ideal G;\n'
            labels = ("a1", "a2", "a3", "b1", "b2", "b3")
            for size in range(1, len(labels) + 1):
                for subset in combinations(labels, size):
                    joined = ",".join(f"imap(s,{name})" for name in subset)
                    tag = ",".join(subset)
                    script += (
                        f"G=slimgb(ideal({joined},1-tau*imap(s,LL))); "
                        f"if(size(G)==1 && G[1]==1) "
                        f'{{ "SATURATED UNIT {tag}"; }}\n'
                    )
        else:
            script += '"SELECTED SATURATED SUBSETS"; ideal G;\n'
            for subset in (
                ("a1", "a2", "a3"),
                ("b1", "b2", "b3"),
                ("a1", "a2", "b1"),
                ("a1", "a2", "b3"),
                ("a1", "a2", "a3", "b1"),
                ("a1", "a2", "a3", "b2"),
                ("a1", "a2", "a3", "b3"),
            ):
                joined = ",".join(f"imap(s,{name})" for name in subset)
                tag = ",".join(subset)
                script += (
                    f"G=slimgb(ideal({joined},1-tau*imap(s,LL))); "
                    f"if(size(G)==1 && G[1]==1) "
                    f'{{ "SATURATED UNIT {tag}"; }} '
                    f'else {{ "SATURATED NONUNIT {tag}"; dim(G); size(G); }}\n'
                )
    elif mode in (
        "saturated_parameter_exact_modular",
        "saturated_parameter_exact_direct",
        "h_lift_exact",
        "h_basis_reconstruct_verify",
        "h_lift_modular_verified",
        "h_lift_batch_verified",
    ):
        script += (
            "def II=I; def LL=L;\n"
            "ring q=0,(tau,v,w),(dp(1),dp(2));\n"
            "ideal J=imap(s,II),1-tau*imap(s,LL);\n"
        )
        if mode == "h_lift_batch_verified":
            script += (
                "ring q2=0,(v,w),dp;\n"
                "ideal H=imap(s,a1),imap(s,a2),imap(s,a3); "
                "poly L2=imap(s,LL); ideal target=L2^4;\n"
                "def characteristic_zero=basering; "
                "list description=ringlist(characteristic_zero); "
                "list modular_lifts,prime_list; int p=536870909; "
                "bigint modulus=1; int i;\n"
                '"STAGE fixed-batch lift reconstruction";\n'
                "for(i=1;i<=128;i++) { p=prime(p-1); prime_list[i]=p; "
                "modulus=modulus*p; description[1]=p; "
                "def prime_ring=ring(description); setring prime_ring; "
                "ideal prime_H=fetch(characteristic_zero,H); "
                "ideal prime_target=fetch(characteristic_zero,target); "
                "matrix units; matrix prime_lift=lift("
                'prime_H,prime_target,units,"slimgb"); '
                "setring characteristic_zero; modular_lifts[i]="
                "fetch(prime_ring,prime_lift); kill prime_ring; }\n"
                "matrix combined=chinrem(modular_lifts,prime_list); "
                "matrix T=farey(combined,modulus);\n"
                "if(matrix(target)-matrix(H)*T!=0) "
                '{ ERROR("128-PRIME LIFT RECONSTRUCTION FAILED"); }\n'
                '"EXACT 128-PRIME H LIFT PASS"; nrows(T);ncols(T);\n'
                '"EXACT H LIFT DEGREES"; '
                'deg(T[1,1]);deg(T[2,1]);deg(T[3,1]);\n'
                '"EXACT H LIFT TERM COUNTS"; '
                'size(T[1,1]);size(T[2,1]);size(T[3,1]);\n'
            )
            return script
        if mode == "h_lift_modular_verified":
            script += (
                "ring q2=0,(v,w),dp;\n"
                "ideal H=imap(s,a1),imap(s,a2),imap(s,a3); "
                "poly L2=imap(s,LL); ideal target=L2^4;\n"
                "proc obstruction_lift(ideal source, ideal wanted) "
                '{ matrix units; return(lift(source,wanted,units,"slimgb")); }\n'
                "proc accept_prime(int p, alias list args) { return(1); }\n"
                "proc keep_all(alias list results) { return(list()); }\n"
                "proc accept_modular(string command, alias list args, "
                "alias def result, int p) "
                "{ def characteristic_zero=basering; "
                "list description=ringlist(characteristic_zero); "
                "description[1]=p; def prime_ring=ring(description); "
                "setring prime_ring; list prime_args=fetch("
                "characteristic_zero,args); matrix prime_result=fetch("
                "characteristic_zero,result); matrix prime_error="
                "matrix(prime_args[2])-matrix(prime_args[1])*prime_result; "
                "int answer=(prime_error==0); setring characteristic_zero; "
                "return(answer); }\n"
                "proc verify_exact(string command, alias list args, "
                "alias def result) "
                "{ matrix error=matrix(args[2])-matrix(args[1])*result; "
                "if(error==0) { return(1); } else { return(0); } }\n"
                "LIB \"modular.lib\";\n"
                '"STAGE modular reconstruction of exact lift";\n'
                "timer=1; matrix T=modular("
                '"obstruction_lift",list(H,target),accept_prime,keep_all,'
                "accept_modular,verify_exact); timer=0;\n"
                "if(matrix(target)-matrix(H)*T!=0) "
                '{ "BAD RECONSTRUCTED LIFT"; exit(1); }\n'
                '"EXACT RECONSTRUCTED H LIFT PASS"; nrows(T);ncols(T);\n'
                '"EXACT H LIFT DEGREES"; '
                'deg(T[1,1]);deg(T[2,1]);deg(T[3,1]);\n'
                '"EXACT H LIFT TERM COUNTS"; '
                'size(T[1,1]);size(T[2,1]);size(T[3,1]);\n'
            )
            return script
        if mode == "h_basis_reconstruct_verify":
            script += (
                "ring q2=0,(v,w),dp;\n"
                "ideal H=imap(s,a1),imap(s,a2),imap(s,a3); "
                "poly L2=imap(s,LL);\n"
                '"STAGE probabilistic basis reconstruction";\n'
                'timer=1; ideal K0=modGB("slimgb",H,0); timer=0;\n'
                '"STAGE exact candidate normalization";\n'
                'timer=1; ideal K=slimgb(K0); timer=0;\n'
                'if(size(reduce(H,K))!=0) '
                '{ "H NOT IN CANDIDATE"; exit(1); }\n'
                'if(dim(K)!=0 || vdim(K)!=192) '
                '{ "BAD CANDIDATE COLENGTH"; exit(1); }\n'
                'if(reduce(L2^4,K)!=0) '
                '{ "L4 NOT IN CANDIDATE"; exit(1); }\n'
                '"EXACT CANDIDATE CHECK PASS"; size(K); dim(K); vdim(K);\n'
                '"EXACT CANDIDATE LEADS"; lead(K);\n'
            )
            return script
        if mode == "saturated_parameter_exact_modular":
            script += (
                '"STAGE exact modular saturation";\n'
                'timer=1; ideal G=modGB("slimgb",J,1); timer=0;\n'
            )
        elif mode == "saturated_parameter_exact_direct":
            script += (
                '"STAGE direct exact saturation";\n'
                'timer=1; matrix T; ideal G=liftstd(J,T); timer=0;\n'
                '"LIFT SHAPE"; nrows(T); ncols(T);\n'
            )
        else:
            script += (
                "ring q2=0,(v,w),dp;\n"
                "ideal H=imap(s,a1),imap(s,a2),imap(s,a3); "
                "poly L2=imap(s,LL); ideal target=L2^4; matrix U;\n"
                '"STAGE direct exact H-orbit lift";\n'
                'timer=1; matrix T=lift(H,target,U,"slimgb"); timer=0;\n'
                'if(matrix(target)*U-matrix(H)*T!=0) '
                '{ "BAD EXACT H LIFT"; exit(1); }\n'
                '"EXACT H LIFT PASS"; nrows(T); ncols(T);\n'
                '"EXACT H LIFT DEGREES"; '
                'deg(T[1,1]);deg(T[2,1]);deg(T[3,1]);\n'
            )
            return script
        script += (
            '"EXACT SATURATION DATA"; size(G); dim(G);\n'
            'if(size(G)==1 && G[1]==1) { "EXACT SATURATION UNIT"; }\n'
        )
    else:
        raise ValueError(mode)
    return script


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "mode",
        choices=(
            "parameter_probabilistic",
            "generator_stats",
            "parameter_exact",
            "saturated_parameter_modular",
            "nilpotency_modular",
            "subset_saturation_modular",
            "selected_subset_modular",
            "orbit_nilpotency_modular",
            "h_lift_modular",
            "saturated_parameter_exact_modular",
            "saturated_parameter_exact_direct",
            "h_lift_exact",
            "h_basis_reconstruct_verify",
            "h_lift_modular_verified",
            "h_lift_batch_verified",
        ),
    )
    parser.add_argument("--cores", type=int, default=8)
    parser.add_argument("--singular-cpus", type=int, default=1)
    parser.add_argument("--timeout", type=int, default=3600)
    args = parser.parse_args()
    result = subprocess.run(
        ("Singular", f"--cpus={args.singular_cpus}", "-q"),
        input=singular_script(args.mode, args.cores),
        text=True,
        capture_output=True,
        timeout=args.timeout,
        check=True,
    )
    if result.stderr or "?" in result.stdout:
        raise RuntimeError(result.stdout + result.stderr)
    print(result.stdout.strip())


if __name__ == "__main__":
    main()
