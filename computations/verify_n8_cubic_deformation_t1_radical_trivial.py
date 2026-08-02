#!/usr/bin/env python3
"""Certify the n=8 cubic deformation class in embedded tangent T^1.

The cubic tails of the 39 normal-eliminated obstruction lifts pass every
first Schreyer compatibility equation.  This checker asks the next natural
question: is that cocycle induced by a tangent-to-identity coordinate change
and a change of ideal generators?

The answer is no.  Exact rational module reduction leaves a five-term class.
However, every coefficient of the class lies in the Ferrers radical and the
class restricts to zero on all five reduced tangent branches.  Thus the
nontrivial deformation is supported on the nonreduced/intersection structure.
"""

from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import re


HERE = Path(__file__).resolve().parent


def load_module(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


AMBIENT = load_module(
    "n8_ambient_local_standard_basis",
    "analyze_n8_ambient_local_standard_basis.py",
)
LIFTED = load_module(
    "n8_lifted_cubic_spairs",
    "verify_n8_lifted_cubic_spair_first_tails.py",
)


QQ = Fraction

EXPECTED_LEDGER_SHA256 = (
    "a920cc2d4ddab8e356d0e3a6c1a0985ce7e029799bb6bbad5dd51a1672b20e6f"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def derivative(polynomial, variable):
    answer = {}
    for monomial, coefficient in polynomial.items():
        multiplicity = monomial.count(variable)
        if not multiplicity:
            continue
        output = list(monomial)
        output.remove(variable)
        output = tuple(output)
        answer[output] = (
            answer.get(output, QQ(0)) + multiplicity * coefficient
        )
    return answer


def audit():
    series = LIFTED.NormalObstructionSeries()
    quadratic_rows = [value[0] for _pivot, value in series.items]
    cubic_leads = [
        (20, 46, 46), (19, 46, 46), (18, 46, 46),
        (20, 20, 46), (19, 20, 46), (18, 20, 46),
        (19, 19, 46), (18, 19, 46), (18, 18, 46),
    ]
    for number in range(1, 40):
        series.part(number, 3)

    names = [f"z{index}" for index in range(56)]

    def polynomial_string(polynomial):
        return AMBIENT.singular_polynomial(polynomial, names)

    def vector_string(entries):
        terms = [
            f"({polynomial_string(polynomial)})*gen({component + 1})"
            for component, polynomial in entries if polynomial
        ]
        return "+".join(terms) or "0"

    # The trivial embedded-deformation submodule consists of Jacobian
    # derivations plus arbitrary ideal-valued changes in every equation.
    module_generators = []
    for variable in range(56):
        jacobian_column = vector_string([
            (component, derivative(polynomial, variable))
            for component, polynomial in enumerate(quadratic_rows)
        ])
        if jacobian_column != "0":
            module_generators.append(jacobian_column)

    tangent_groebner_basis = (
        quadratic_rows + [{monomial: QQ(1)} for monomial in cubic_leads]
    )
    for component in range(39):
        for polynomial in tangent_groebner_basis:
            module_generators.append(
                f"({polynomial_string(polynomial)})*gen({component + 1})"
            )

    cubic_tail = vector_string([
        (component, series.part(component + 1, 3))
        for component in range(39)
    ])
    expected = (
        "(-z4*z18*z46+z4*z19*z46)*gen(16)"
        "+(-z5*z18*z46+z5*z19*z46)*gen(22)"
        "-z4*z20*z46*gen(19)"
    )

    # The five minimal primes are the exact primes from the Ferrers-radical
    # certificate, written in the original 56 tangent coordinates.
    singular = f"""
ring r=0,({','.join(names)}),dp;
module M={','.join(module_generators)};
module G=std(M);
vector target={cubic_tail};
vector remainder=reduce(target,G);
vector expected={expected};
poly a=z46;
poly b=z44+z45;
poly c=z27;
poly d=z26-z45;
poly e=z25;
poly q0=z12; poly q1=z13; poly q2=z14;
poly q3=z15-z16; poly q4=z17; poly q5=z18;
poly q6=z19; poly q7=z20; poly q8=z21;
poly q9=z22; poly q10=z23;
ideal P1=a,b,c,d,e; P1=std(P1);
ideal P2=a,b,d,e,q0,q1,q3,q5,q6; P2=std(P2);
ideal P3=a,b,q0,q1,q2,q3,q4,q5,q6,q7; P3=std(P3);
ideal P4=b,q0,q1,q2,q3,q4,q5,q6,q7,q8,q9; P4=std(P4);
ideal P5=q0,q1,q2,q3,q4,q5,q6,q7,q8,q9,q10; P5=std(P5);
poly u1=z4*a*(q6-q5);
poly u2=z5*a*(q6-q5);
poly u3=-z4*a*q7;
int branchzero=(
 (reduce(u1,P1)==0) && (reduce(u2,P1)==0) && (reduce(u3,P1)==0) &&
 (reduce(u1,P2)==0) && (reduce(u2,P2)==0) && (reduce(u3,P2)==0) &&
 (reduce(u1,P3)==0) && (reduce(u2,P3)==0) && (reduce(u3,P3)==0) &&
 (reduce(u1,P4)==0) && (reduce(u2,P4)==0) && (reduce(u3,P4)==0) &&
 (reduce(u1,P5)==0) && (reduce(u2,P5)==0) && (reduce(u3,P5)==0));
"RESULT",(remainder==expected),(remainder!=0),size(M),size(G),size(remainder),
 branchzero;
quit;
"""
    output, returncode, peak_kib, stop_reason, writer_errors = (
        AMBIENT.bounded_singular(singular, 60, 700)
    )
    require(stop_reason is None,
            f"T1 module audit stopped: {stop_reason}, peak={peak_kib} KiB")
    require(returncode == 0 and not writer_errors,
            f"T1 Singular failure: {returncode}, {writer_errors}, {output[-1000:]}")
    match = re.search(
        r"RESULT\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)",
        output,
    )
    require(match is not None, f"could not parse T1 audit: {output[-2000:]}")
    values = tuple(map(int, match.groups()))
    require(values == (1, 1, 1890, 1704, 5, 1),
            f"cubic T1 class changed: {values}")

    return {
        "tangent_variables": 56,
        "quadratic_equations": 39,
        "tangent_groebner_generators": 48,
        "cubic_tail_terms": sum(
            len(series.part(number, 3)) for number in range(1, 40)
        ),
        "trivial_deformation_module_generators": values[2],
        "trivial_deformation_standard_basis_size": values[3],
        "t1_remainder_terms": values[4],
        "t1_remainder": (
            "a*(z4*(s-r)*e16 + z5*(s-r)*e22 - z4*t*e19)"
        ),
        "t1_class_nonzero": bool(values[1]),
        "zero_on_all_five_reduced_branches": bool(values[5]),
        "scope_guard": (
            "the cubic deformation is a compatible but nontrivial embedded "
            "T1 class; radical-triviality does not itself lift all branches"
        ),
    }


def main():
    ledger = audit()
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                "frozen cubic T1 ledger changed")
    print(
        "n=8 cubic deformation T1: PASS; nonzero five-term class, "
        "but zero on all five reduced tangent branches"
    )
    print(json.dumps(ledger, sort_keys=True))
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
