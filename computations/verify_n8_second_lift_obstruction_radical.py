#!/usr/bin/env python3
"""Certify the five linear branches of the n=8 second-lift tangent cone.

The 39 exact quadratic obstruction forms are reconstructed by the existing
third-jet checker.  Singular is used only for exact rational Groebner
reduction.  The checker supplies a direct radical certificate:

* the obstruction ideal is contained in a 42-generator Ferrers edge ideal;
* every Ferrers generator, or its square, reduces to zero modulo the
  obstruction ideal (exactly six require a square); and
* the Ferrers ideal is the irredundant intersection of five explicitly
  displayed linear prime ideals.

Thus the reduced second-liftable tangent cone has exactly five linear
components.  This is a local n=8 statement, not a proof of the conjecture.
"""

from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import re
import shutil
import subprocess


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


HERE = Path(__file__).resolve().parent
SOURCE_PATH = HERE / "verify_n8_counterexample_pure_cubic_conormal.py"
SPEC = importlib.util.spec_from_file_location("n8_cubic_conormal", SOURCE_PATH)
SOURCE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SOURCE)

EXPECTED_LEDGER_SHA256 = (
    "2ec19dbb7e7b203683c35389b9c764398e00419e0c51509208ee2d1a017e7513"
)


def singular_polynomial(polynomial, names):
    terms = []
    for monomial, coefficient in sorted(polynomial.items()):
        coefficient = Fraction(coefficient)
        scalar = (
            str(coefficient.numerator)
            if coefficient.denominator == 1
            else f"({coefficient.numerator}/{coefficient.denominator})"
        )
        terms.append(scalar + "*" + "*".join(names[index] for index in monomial))
    return "+".join(terms).replace("+-", "-")


def exact_singular_audit(obstructions):
    singular = shutil.which("Singular")
    require(singular is not None, "Singular is required for this exact audit")
    names = [f"z{index}" for index in range(56)]
    generators = [singular_polynomial(form, names)
                  for form in obstructions.values()]
    incomparability_checks = "\n".join(
        f"if (zeroideal(reduce(P{left},P{right}))) {{ incomparable=0; }}"
        for left in range(1, 6) for right in range(1, 6) if left != right
    )

    # After the displayed linear change, the radical is the edge ideal of a
    # Ferrers graph with left vertices a,b,c,d,e and right vertices q0,...,q10.
    source = f"""
ring r=0,({','.join(names)}),dp;
option(redSB);
ideal I={','.join(generators)};
ideal G=std(I);
poly a=z46;
poly b=z44+z45;
poly c=z27;
poly d=z26-z45;
poly e=z25;
poly q0=z12; poly q1=z13; poly q2=z14;
poly q3=z15-z16; poly q4=z17; poly q5=z18;
poly q6=z19; poly q7=z20; poly q8=z21;
poly q9=z22; poly q10=z23;
ideal J=
 a*q0,a*q1,a*q2,a*q3,a*q4,a*q5,a*q6,a*q7,a*q8,a*q9,
 b*q0,b*q1,b*q2,b*q3,b*q4,b*q5,b*q6,b*q7,b*q8,b*q9,b*q10,
 c*q0,c*q1,c*q3,c*q5,c*q6,
 d*q0,d*q1,d*q2,d*q3,d*q4,d*q5,d*q6,d*q7,
 e*q0,e*q1,e*q2,e*q3,e*q4,e*q5,e*q6,e*q7;
J=std(J);
ideal C=a^2*q5,a^2*q6,a^2*q7,
 a*q5^2,a*q5*q6,a*q5*q7,a*q6^2,a*q6*q7,a*q7^2;
C=std(C);
ideal P1=a,b,c,d,e;
ideal P2=a,b,d,e,q0,q1,q3,q5,q6;
ideal P3=a,b,q0,q1,q2,q3,q4,q5,q6,q7;
ideal P4=b,q0,q1,q2,q3,q4,q5,q6,q7,q8,q9;
ideal P5=q0,q1,q2,q3,q4,q5,q6,q7,q8,q9,q10;
P1=std(P1); P2=std(P2); P3=std(P3); P4=std(P4); P5=std(P5);
ideal K=std(intersect(intersect(P1,P2),intersect(P3,intersect(P4,P5))));
proc zeroideal(ideal A)
{{
  int i;
  for (i=1;i<=ncols(A);i++) {{ if (A[i]!=0) {{ return(0); }} }}
  return(1);
}}
int good=1; int i;
int iInJ=zeroideal(reduce(I,J));
int jInK=zeroideal(reduce(J,K));
int kInJ=zeroideal(reduce(K,J));
if (!iInJ || !jInK || !kInJ) {{ good=0; }}
int quadraticGB=0; int cubicGB=0; int cubicShape=1;
for (i=1;i<=size(G);i++)
{{
  if (deg(G[i])==2) {{ quadraticGB=quadraticGB+1; }}
  if (deg(G[i])==3)
  {{
    cubicGB=cubicGB+1;
    if ((size(G[i])!=1) || (reduce(G[i],C)!=0)) {{ cubicShape=0; }}
  }}
}}
if ((quadraticGB!=39) || (cubicGB!=9) || (!cubicShape)) {{ good=0; }}
int squares=0; poly h;
for (i=1;i<=size(J);i++)
{{
  h=reduce(J[i],G);
  if (h!=0)
  {{
    if (reduce(J[i]^2,G)==0) {{ squares=squares+1; }}
    else {{ good=0; }}
  }}
}}
int incomparable=1;
{incomparability_checks}
if (!incomparable) {{ good=0; }}
"RESULT",good,size(G),size(J),squares,
 dim(P1),dim(P2),dim(P3),dim(P4),dim(P5),size(K),
 iInJ,jInK,kInJ,incomparable,quadraticGB,cubicGB,cubicShape;
quit;
"""
    completed = subprocess.run(
        [singular, "-q"], input=source, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True,
    )
    match = re.search(
        r"RESULT\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+"
        r"(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+"
        r"(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+"
        r"(\d+)\s+(\d+)\s+(\d+)",
        completed.stdout,
    )
    require(match is not None, "could not parse Singular radical audit")
    values = tuple(map(int, match.groups()))
    require(values == (
        1, 48, 42, 6, 51, 47, 46, 45, 45, 42, 1, 1, 1, 1, 39, 9, 1
    ),
            f"second-lift radical audit changed: {values}")
    return values


def audit():
    free_columns, _tangent_basis, obstruction_pivots = (
        SOURCE.second_lift_obstruction_basis()
    )
    require(len(free_columns) == 56, "mixed tangent dimension changed")
    require(len(obstruction_pivots) == 39, "second-lift obstruction rank changed")
    require(sum(map(len, obstruction_pivots.values())) == 68,
            "second-lift obstruction support changed")
    values = exact_singular_audit(obstruction_pivots)
    return {
        "tangent_variables": 56,
        "quadratic_obstruction_rank": 39,
        "quadratic_obstruction_terms": 68,
        "obstruction_groebner_basis_size": values[1],
        "quadratic_groebner_generators": values[14],
        "cubic_groebner_generators": values[15],
        "cubic_groebner_shape": "a*(r,s,t)*(a,r,s,t)",
        "radical_ferrers_generators": values[2],
        "radical_generators_requiring_square": values[3],
        "linear_component_dimensions": list(values[4:9]),
        "minimal_linear_prime_count": 5,
        "ferrers_left_neighbourhood_sizes": [10, 11, 5, 8, 8],
        "scope_guard": (
            "reduced second-lift tangent cone only; higher Hasse equations "
            "and full local mixed-fibre branches remain to be imposed"
        ),
    }


def main():
    ledger = audit()
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                "frozen second-lift radical ledger changed")
    print(
        "n=8 second-lift obstruction radical: PASS; "
        "39 quadrics/68 terms -> GB48, radical42, "
        "five linear branches dims=51,47,46,45,45; squares=6"
    )
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
