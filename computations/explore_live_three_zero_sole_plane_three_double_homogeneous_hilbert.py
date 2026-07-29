#!/usr/bin/env python3
"""Test the fixed-degree homogeneous rank route for the 2^3 1^7 profile.

This is exploratory, not a closure checker.  It constructs the three
degree-30 cyclic obstructions exactly as the frontier checker does, then
computes their homogeneous Hilbert function modulo 32003.  At cutoff D,
``binomial(D+2,2)-HF(D)`` is the rank of the degree-D Macaulay map.
"""

from __future__ import annotations

import argparse
import math
import re
import selectors
import subprocess
import time

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


def singular_script(
    first_system: tuple[sp.Expr, ...], *, exact_candidate: bool,
    boundary_profile: bool, exact_decomposition: bool,
    exact_boundary_only: bool, exact_boundary_order: str,
    exact_affine_only: bool,
) -> str:
    names = ",".join(map(str, LOCAL_VARIABLES))
    script = (
        f"ring r=(0,v,w),({names}),dp;\n"
        "option(redSB);\n"
        f"ideal I={generators(first_system)};\n"
        "matrix T; ideal G=liftstd(I,T); def H=G[1];\n"
        "if(size(G)!=1 || deg(G[1])!=0) "
        '{ "FIRST LIFT FAILED"; exit(1); }\n'
        "ring s=0,(t,v,w),dp;\n"
        "poly h1=imap(r,H); poly hh=homog(h1,t);\n"
        "poly h2=subst(subst(hh,v,1),t,v);\n"
        "poly h3=subst(subst(subst(hh,v,1),w,v),t,w);\n"
        "poly L=v*w*(v-1)*(v+1)*(w-1)*(w+1)*(v-w)*(v+w);\n"
        "poly d;\n"
    )
    for name in ("h1", "h2", "h3"):
        script += (
            f"d=gcd({name},L); while(d!=1) "
            f"{{ {name}={name}/d; d=gcd({name},L); }}\n"
        )
    script += (
        "if(deg(h1)!=30 || deg(h2)!=30 || deg(h3)!=30) "
        '{ "BAD CYCLIC DEGREES"; exit(1); }\n'
        "def H1=h1; def H2=h2; def H3=h3; def LL=L;\n"
        "ring p=32003,(t,v,w),dp;\n"
        "poly f1=imap(s,H1); poly f2=imap(s,H2); poly f3=imap(s,H3);\n"
        "ideal J=homog(f1,t),homog(f2,t),homog(f3,t);\n"
        "if(deg(J[1])!=30 || deg(J[2])!=30 || deg(J[3])!=30) "
        '{ "BAD HOMOGENEOUS DEGREES"; exit(1); }\n'
        '"STAGE homogeneous standard basis mod 32003";\n'
        "timer=1; ideal B=slimgb(J); timer=0;\n"
        "bigintvec hs=hilb(B,1);\n"
        '"MODULAR BASIS SIZE / HILBERT NUMERATOR"; size(B); hs;\n'
        "intvec cutoffs=30,48,64,78,96,128; "
        "int a,D,n,e; bigint hf,macrank;\n"
        "for(a=1;a<=6;a++) { D=cutoffs[a]; hf=0; "
        "for(n=1;n<size(hs);n++) { e=D-(n-1); "
        "if(e>=0) { hf=hf+hs[n]*(e+2)*(e+1)/2; } } "
        "macrank=(D+2)*(D+1)/2-hf; "
        '"CUTOFF / HF / MACAULAY RANK"; D; hf; macrank; }\n'
    )
    if boundary_profile:
        script += (
            '"STAGE modular infinity-thickening profile";\n'
            "intvec powers=1,2,3,4,5,6,8,10,12,16,24,32,40,46; "
            "int z,m,bn,be; bigint bhf78,bhf128; bigintvec bhs; ideal C;\n"
            "for(z=1;z<=size(powers);z++) { m=powers[z]; "
            "C=B; C[size(C)+1]=t^m; C=slimgb(C); bhs=hilb(C,1); "
            "bhf78=0; bhf128=0; "
            "for(bn=1;bn<size(bhs);bn++) { be=78-(bn-1); "
            "if(be>=0) { bhf78=bhf78+bhs[bn]*(be+2)*(be+1)/2; } "
            "be=128-(bn-1); if(be>=0) { "
            "bhf128=bhf128+bhs[bn]*(be+2)*(be+1)/2; } } "
            '"POWER / BOUNDARY BASIS SIZE / HF78 / HF128"; '
            "m; size(C); bhf78; bhf128; "
            'if(m==16) { "BOUNDARY M16 HILBERT NUMERATOR"; bhs; } }\n'
        )
    if exact_boundary_only:
        if exact_boundary_order == "vwt":
            exact_boundary_setup = (
                "ring q=0,(v,w,t),dp; option(redSB);\n"
                '"EXACT B16 VARIABLE ORDER"; var(1); var(2); var(3);\n'
                "if(var(1)!=v || var(2)!=w || var(3)!=t) "
                '{ "EXACT B16 VWT ORDER AUDIT FAILED"; exit(1); }\n'
                "map phi=s,t,v,w;\n"
                "poly f1=phi(H1); poly f2=phi(H2); poly f3=phi(H3);\n"
                "poly l=phi(LL);\n"
            )
        else:
            exact_boundary_setup = (
                "ring q=0,(t,v,w),dp; option(redSB);\n"
                '"EXACT B16 VARIABLE ORDER"; var(1); var(2); var(3);\n'
                "if(var(1)!=t || var(2)!=v || var(3)!=w) "
                '{ "EXACT B16 TVW ORDER AUDIT FAILED"; exit(1); }\n'
                "poly f1=imap(s,H1); poly f2=imap(s,H2); "
                "poly f3=imap(s,H3);\n"
                "poly l=imap(s,LL);\n"
            )
        script += (
            f'"STAGE exact B16-only rational reconstruction '
            f'{exact_boundary_order}";\n'
        )
        script += exact_boundary_setup
        script += (
            "ideal J=homog(f1,t),homog(f2,t),homog(f3,t);\n"
            "poly lh=homog(l,t); "
            "poly target=t^46*lh^4;\n"
            "if(homog(J[1],t)!=J[1] || homog(J[2],t)!=J[2] "
            "|| homog(J[3],t)!=J[3]) "
            '{ "EXACT J GENERATOR HOMOGENEITY FAILED"; exit(1); }\n'
            "if(deg(target)!=78) "
            '{ "EXACT TARGET DEGREE IS NOT 78"; exit(1); }\n'
            "if(subst(target,t,1)!=l^4) "
            '{ "EXACT TARGET DEHOMOGENIZATION FAILED"; exit(1); }\n'
            "ideal BSOURCE=J; BSOURCE[size(BSOURCE)+1]=t^16;\n"
            'LIB "resources.lib"; Resources::setcores(1); LIB "modstd.lib";\n'
            'timer=1; ideal BK0=modGB("slimgb",BSOURCE,0); timer=0;\n'
            '"STAGE exact B16-only candidate normalization";\n'
            "timer=1; ideal BK=slimgb(BK0); timer=0;\n"
            "if(size(reduce(BSOURCE,BK))!=0) "
            '{ "EXACT INCLUSION (J,T16) SUBSET B16 FAILED"; exit(1); }\n'
            "int i; for(i=1;i<=size(BK);i++) { "
            "if(homog(BK[i],t)!=BK[i]) "
            '{ "B16 IS NOT HOMOGENEOUS"; exit(1); } }\n'
            "if(size(reduce(J,BK))!=0) "
            '{ "EXACT HOMOGENEOUS INCLUSION J SUBSET B16 FAILED"; exit(1); }\n'
            "if(reduce(target,BK)!=0) "
            '{ "EXACT TARGET MEMBERSHIP IN B16 FAILED"; exit(1); }\n'
            "bigintvec bkh=hilb(BK,1); "
            '"EXACT B16 HILBERT NUMERATOR"; bkh; '
            '"EXACT B16 BASIS SIZE"; size(BK);\n'
            '"EXACT B16-ONLY CANDIDATE CHECKS PASS";\n'
        )
    elif exact_affine_only:
        script += (
            '"STAGE exact affine-only rational reconstruction";\n'
            "ring qa=0,(v,w),dp; option(redSB);\n"
            "ideal Ha=imap(s,H1),imap(s,H2),imap(s,H3); "
            "poly la=imap(s,LL);\n"
            'LIB "resources.lib"; Resources::setcores(1); LIB "modstd.lib";\n'
            'timer=1; ideal KA0=modGB("slimgb",Ha,0); timer=0;\n'
            '"STAGE exact affine-only candidate normalization";\n'
            "timer=1; ideal KA=slimgb(KA0); timer=0;\n"
            "if(size(reduce(Ha,KA))!=0) "
            '{ "EXACT AFFINE INCLUSION H SUBSET KA FAILED"; exit(1); }\n'
            "if(dim(KA)!=0 || vdim(KA)!=192) "
            '{ "EXACT AFFINE CANDIDATE COLENGTH FAILED"; exit(1); }\n'
            "if(reduce(la^4,KA)!=0) "
            '{ "EXACT AFFINE L4 MEMBERSHIP IN KA FAILED"; exit(1); }\n'
            "def KADATA=KA;\n"
            "ring q=0,(t,v,w),dp; option(redSB);\n"
            "poly f1=imap(s,H1); poly f2=imap(s,H2); poly f3=imap(s,H3);\n"
            "ideal J=homog(f1,t),homog(f2,t),homog(f3,t);\n"
            "poly l=imap(s,LL); poly lh=homog(l,t); "
            "poly target=t^46*lh^4;\n"
            "if(deg(target)!=78 || subst(target,t,1)!=l^4) "
            '{ "EXACT AFFINE TARGET AUDIT FAILED"; exit(1); }\n'
            "ideal A=imap(qa,KADATA); int i; "
            "for(i=1;i<=size(A);i++) { A[i]=homog(A[i],t); } "
            "timer=1; A=slimgb(A); timer=0;\n"
            "for(i=1;i<=size(A);i++) { if(homog(A[i],t)!=A[i]) "
            '{ "A IS NOT HOMOGENEOUS"; exit(1); } }\n'
            "if(size(reduce(J,A))!=0) "
            '{ "EXACT HOMOGENEOUS INCLUSION J SUBSET A FAILED"; exit(1); }\n'
            "if(reduce(target,A)!=0) "
            '{ "EXACT TARGET MEMBERSHIP IN A FAILED"; exit(1); }\n'
            "bigintvec ahs=hilb(A,1); "
            '"EXACT A HILBERT NUMERATOR"; ahs; '
            '"EXACT A BASIS SIZE"; size(A);\n'
            "ideal AT=A; AT[size(AT)+1]=t^16; "
            "timer=1; AT=slimgb(AT); timer=0;\n"
            "bigintvec aths=hilb(AT,1); "
            '"EXACT A+T16 HILBERT NUMERATOR"; aths; '
            '"EXACT A+T16 BASIS SIZE"; size(AT);\n'
            '"EXACT AFFINE-ONLY CANDIDATE CHECKS PASS";\n'
        )
    elif exact_decomposition:
        script += (
            '"STAGE reconstruct affine rational overideal";\n'
            "ring qa=0,(v,w),dp; option(redSB);\n"
            "ideal Ha=imap(s,H1),imap(s,H2),imap(s,H3); "
            "poly la=imap(s,LL);\n"
            'LIB "resources.lib"; Resources::setcores(1); LIB "modstd.lib";\n'
            'timer=1; ideal KA0=modGB("slimgb",Ha,0); timer=0;\n'
            '"STAGE normalize affine candidate exactly";\n'
            "timer=1; ideal KA=slimgb(KA0); timer=0;\n"
            "if(size(reduce(Ha,KA))!=0) "
            '{ "EXACT AFFINE INCLUSION H SUBSET KA FAILED"; exit(1); }\n'
            "if(dim(KA)!=0 || vdim(KA)!=192) "
            '{ "EXACT AFFINE CANDIDATE COLENGTH FAILED"; exit(1); }\n'
            "if(reduce(la^4,KA)!=0) "
            '{ "EXACT AFFINE L4 MEMBERSHIP IN KA FAILED"; exit(1); }\n'
            "def KADATA=KA;\n"
            "ring q=0,(t,v,w),dp; option(redSB);\n"
            "poly f1=imap(s,H1); poly f2=imap(s,H2); poly f3=imap(s,H3);\n"
            "ideal J=homog(f1,t),homog(f2,t),homog(f3,t);\n"
            "poly l=imap(s,LL); poly lh=homog(l,t); "
            "poly target=t^46*lh^4;\n"
            "if(homog(J[1],t)!=J[1] || homog(J[2],t)!=J[2] "
            "|| homog(J[3],t)!=J[3]) "
            '{ "EXACT J GENERATOR HOMOGENEITY FAILED"; exit(1); }\n'
            "if(deg(target)!=78) "
            '{ "EXACT TARGET DEGREE IS NOT 78"; exit(1); }\n'
            "if(subst(target,t,1)!=l^4) "
            '{ "EXACT TARGET DEHOMOGENIZATION FAILED"; exit(1); }\n'
            '"STAGE construct exact homogeneous affine overideal A";\n'
            "ideal A=imap(qa,KADATA); int i; "
            "for(i=1;i<=size(A);i++) { A[i]=homog(A[i],t); } "
            "timer=1; A=slimgb(A); timer=0;\n"
            "for(i=1;i<=size(A);i++) { if(homog(A[i],t)!=A[i]) "
            '{ "A IS NOT HOMOGENEOUS"; exit(1); } }\n'
            "if(size(reduce(J,A))!=0) "
            '{ "EXACT HOMOGENEOUS INCLUSION J SUBSET A FAILED"; exit(1); }\n'
            "if(reduce(target,A)!=0) "
            '{ "EXACT TARGET MEMBERSHIP IN A FAILED"; exit(1); }\n'
            "bigintvec ahs=hilb(A,1); "
            '"EXACT A HILBERT NUMERATOR"; ahs; '
            '"EXACT A BASIS SIZE"; size(A);\n'
            '"STAGE reconstruct exact infinity overideal B16";\n'
            "ideal BSOURCE=J; BSOURCE[size(BSOURCE)+1]=t^16;\n"
            'timer=1; ideal BK0=modGB("slimgb",BSOURCE,0); timer=0;\n'
            '"STAGE normalize infinity candidate exactly";\n'
            "timer=1; ideal BK=slimgb(BK0); timer=0;\n"
            "if(size(reduce(BSOURCE,BK))!=0) "
            '{ "EXACT INCLUSION (J,T16) SUBSET B16 FAILED"; exit(1); }\n'
            "for(i=1;i<=size(BK);i++) { if(homog(BK[i],t)!=BK[i]) "
            '{ "B16 IS NOT HOMOGENEOUS"; exit(1); } }\n'
            "if(size(reduce(J,BK))!=0) "
            '{ "EXACT HOMOGENEOUS INCLUSION J SUBSET B16 FAILED"; exit(1); }\n'
            "if(reduce(target,BK)!=0) "
            '{ "EXACT TARGET MEMBERSHIP IN B16 FAILED"; exit(1); }\n'
            "bigintvec bkh=hilb(BK,1); "
            '"EXACT B16 HILBERT NUMERATOR"; bkh; '
            '"EXACT B16 BASIS SIZE"; size(BK);\n'
            '"STAGE exact degree-78 disjointness A plus B16";\n'
            "ideal AB=A+BK; timer=1; AB=slimgb(AB); timer=0;\n"
            "bigintvec abhs=hilb(AB,1); "
            '"EXACT A+B16 HILBERT NUMERATOR"; abhs; '
            '"EXACT A+B16 BASIS SIZE"; size(AB);\n'
            '"EXACT DECOMPOSED HOMOGENEOUS CANDIDATES BUILT";\n'
        )
    elif exact_candidate:
        script += (
            "ring q=0,(t,v,w),dp; option(redSB);\n"
            "poly f1=imap(s,H1); poly f2=imap(s,H2); poly f3=imap(s,H3);\n"
            "ideal J=homog(f1,t),homog(f2,t),homog(f3,t);\n"
            "poly l=imap(s,LL); poly lh=homog(l,t);\n"
            "poly target=t^46*lh^4;\n"
            "if(homog(J[1],t)!=J[1] || homog(J[2],t)!=J[2] "
            "|| homog(J[3],t)!=J[3]) "
            '{ "EXACT J GENERATOR HOMOGENEITY FAILED"; exit(1); }\n'
            "if(deg(target)!=78) "
            '{ "EXACT TARGET DEGREE IS NOT 78"; exit(1); }\n'
            "if(subst(target,t,1)!=l^4) "
            '{ "EXACT TARGET DEHOMOGENIZATION FAILED"; exit(1); }\n'
            'LIB "resources.lib"; Resources::setcores(1); LIB "modstd.lib";\n'
            '"STAGE reconstruct homogeneous rational overideal";\n'
            'timer=1; ideal K0=modGB("slimgb",J,0); timer=0;\n'
            '"STAGE normalize candidate exactly";\n'
            "timer=1; ideal K=slimgb(K0); timer=0;\n"
            "if(size(reduce(J,K))!=0) "
            '{ "EXACT INCLUSION J SUBSET K FAILED"; exit(1); }\n'
            "int i; for(i=1;i<=size(K);i++) { "
            "if(homog(K[i],t)!=K[i]) "
            '{ "CANDIDATE IS NOT HOMOGENEOUS"; exit(1); } }\n'
            "if(reduce(target,K)!=0) "
            '{ "EXACT HOMOGENEOUS TARGET MEMBERSHIP IN K FAILED"; exit(1); }\n'
            "bigintvec khs=hilb(K,1); bigint khf=0; int kn,ke;\n"
            "for(kn=1;kn<size(khs);kn++) { ke=78-(kn-1); "
            "if(ke>=0) { khf=khf+khs[kn]*(ke+2)*(ke+1)/2; } }\n"
            "if(khf!=318) "
            '{ "EXACT CANDIDATE DEGREE-78 HILBERT VALUE IS NOT 318"; '
            "khf; exit(1); }\n"
            '"EXACT HOMOGENEOUS OVERIDEAL CHECKS PASS"; size(K); khf;\n'
            '"EXACT CANDIDATE HILBERT NUMERATOR"; khs;\n'
            '"EXACT CANDIDATE LEADING MONOMIALS"; lead(K);\n'
        )
    script += '"HOMOGENEOUS HILBERT EXPLORATION COMPLETE";\n'
    return script


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--exact-candidate", action="store_true")
    parser.add_argument("--exact-decomposition", action="store_true")
    parser.add_argument("--exact-boundary-only", action="store_true")
    parser.add_argument("--exact-affine-only", action="store_true")
    parser.add_argument(
        "--exact-boundary-order", choices=("tvw", "vwt"), default="tvw"
    )
    parser.add_argument("--boundary-profile", action="store_true")
    parser.add_argument("--emit-singular", action="store_true")
    parser.add_argument("--stream", action="store_true")
    parser.add_argument("--timeout", type=int, default=1800)
    args = parser.parse_args()
    first_system, _ = systems()
    script = singular_script(
        first_system,
        exact_candidate=args.exact_candidate,
        boundary_profile=args.boundary_profile,
        exact_decomposition=args.exact_decomposition,
        exact_boundary_only=args.exact_boundary_only,
        exact_boundary_order=args.exact_boundary_order,
        exact_affine_only=args.exact_affine_only,
    )
    if args.emit_singular:
        print(script, end="")
        return
    if args.stream:
        process = subprocess.Popen(
            ("Singular", "--cpus=1", "-q"),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        assert process.stdin is not None and process.stdout is not None
        process.stdin.write(script)
        process.stdin.close()
        selector = selectors.DefaultSelector()
        selector.register(process.stdout, selectors.EVENT_READ)
        deadline = time.monotonic() + args.timeout
        chunks: list[str] = []
        while True:
            for key, _ in selector.select(timeout=1.0):
                line = key.fileobj.readline()
                if line:
                    print(line, end="", flush=True)
                    chunks.append(line)
                elif process.poll() is not None:
                    break
            if process.poll() is not None:
                remainder = process.stdout.read()
                if remainder:
                    print(remainder, end="", flush=True)
                    chunks.append(remainder)
                break
            if time.monotonic() >= deadline:
                process.kill()
                process.wait()
                raise subprocess.TimeoutExpired(process.args, args.timeout)
        if process.returncode != 0:
            raise subprocess.CalledProcessError(process.returncode, process.args)
        result = subprocess.CompletedProcess(
            process.args, process.returncode, "".join(chunks), ""
        )
    else:
        result = subprocess.run(
            ("Singular", "--cpus=1", "-q"),
            input=script,
            text=True,
            capture_output=True,
            check=True,
            timeout=args.timeout,
        )
    if result.stderr or "?" in result.stdout or "COMPLETE" not in result.stdout:
        raise RuntimeError(result.stdout + result.stderr)
    if args.exact_decomposition:
        def hilbert_value(label: str, degree: int = 78) -> int:
            match = re.search(
                rf"{re.escape(label)}\s*\n([0-9,\-]+)", result.stdout
            )
            if match is None:
                raise RuntimeError(f"missing {label!r}\n{result.stdout}")
            entries = [int(value) for value in match.group(1).split(",")]
            # Singular documents the final entry as metadata, not a
            # coefficient of the first Hilbert series.
            numerator = entries[:-1]
            return sum(
                coefficient * math.comb(degree - exponent + 2, 2)
                for exponent, coefficient in enumerate(numerator)
                if exponent <= degree
            )

        a_hf = hilbert_value("EXACT A HILBERT NUMERATOR")
        b_hf = hilbert_value("EXACT B16 HILBERT NUMERATOR")
        ab_hf = hilbert_value("EXACT A+B16 HILBERT NUMERATOR")
        if (a_hf, b_hf, ab_hf) != (192, 126, 0):
            raise RuntimeError(
                "bad exact degree-78 Hilbert values: "
                f"A={a_hf}, B16={b_hf}, A+B16={ab_hf}\n{result.stdout}"
            )
        if a_hf + b_hf - ab_hf != 318:
            raise RuntimeError("bad exact degree-78 intersection Hilbert value")
        result.stdout += (
            "PYTHON EXACT DEGREE-78 HILBERT SQUEEZE PASS\n"
            f"A / B16 / A+B16 / intersection: "
            f"{a_hf} / {b_hf} / {ab_hf} / 318\n"
        )
    elif args.exact_boundary_only:
        match = re.search(
            r"EXACT B16 HILBERT NUMERATOR\s*\n([0-9,\-]+)",
            result.stdout,
        )
        if match is None:
            raise RuntimeError("missing exact B16 Hilbert numerator")
        entries = [int(value) for value in match.group(1).split(",")][:-1]
        b_hf = sum(
            coefficient * math.comb(78 - exponent + 2, 2)
            for exponent, coefficient in enumerate(entries)
            if exponent <= 78
        )
        if b_hf != 126:
            raise RuntimeError(f"bad exact B16 degree-78 Hilbert value: {b_hf}")
        result.stdout += "PYTHON EXACT B16 HF78 PASS: 126\n"
    elif args.exact_affine_only:
        def affine_hilbert_value(label: str) -> int:
            match = re.search(
                rf"{re.escape(label)}\s*\n([0-9,\-]+)", result.stdout
            )
            if match is None:
                raise RuntimeError(f"missing {label}")
            entries = [int(value) for value in match.group(1).split(",")][:-1]
            return sum(
                coefficient * math.comb(78 - exponent + 2, 2)
                for exponent, coefficient in enumerate(entries)
                if exponent <= 78
            )

        a_hf = affine_hilbert_value("EXACT A HILBERT NUMERATOR")
        at_hf = affine_hilbert_value("EXACT A+T16 HILBERT NUMERATOR")
        if (a_hf, at_hf) != (192, 0):
            raise RuntimeError(f"bad exact affine Hilbert values: {a_hf}, {at_hf}")
        result.stdout += "PYTHON EXACT A / A+T16 HF78 PASS: 192 / 0\n"
    print(result.stdout.strip())


if __name__ == "__main__":
    main()
