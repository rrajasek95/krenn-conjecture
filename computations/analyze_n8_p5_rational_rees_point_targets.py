#!/usr/bin/env python3
"""Export bounded rational-Rees targets at an exact generic-L P5 point.

The 207 Schur variables remain implicit.  Only the affine bend coordinate is
replaced by R(tau)=N(tau)/P(tau).  Since P(0)=1, cancelling the common P^3
from the uniform source-degree-four clearance does not change the completed
local ideal.
"""

from fractions import Fraction
from hashlib import sha256
import argparse
import importlib.util
import json
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
QQ = Fraction


def load_module(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


POINT = load_module(
    "n8_p5_full_point_for_rational_rees",
    "analyze_n8_p5_full_point_weierstrass.py",
)
SCHUR = POINT.SCHUR
REES = POINT.REES
P5 = POINT.P5


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def add(target, source, scale=QQ(1)):
    REES.add(target, source, scale)


def multiply(left, right):
    return REES.multiply(left, right)


def power(source, exponent):
    answer = {(): QQ(1)}
    for _index in range(exponent):
        answer = multiply(answer, source)
    return answer


def tau_coefficient(source, tau, degree):
    answer = {}
    for monomial, coefficient in source.items():
        if monomial.count(tau) != degree:
            continue
        output = list(monomial)
        for _index in range(degree):
            output.remove(tau)
        answer[tuple(output)] = coefficient
    return answer


def affine_point_parts(source, layout, point):
    """Return A,B with source(point,z46)=A*z46+B over the local variables."""

    base_variables = frozenset(layout["a"].values())
    z46 = layout["a"][46]
    slope = {}
    constant = {}
    for monomial, coefficient in source.items():
        degree = monomial.count(z46)
        require(degree <= 1, "first-Rees source stopped being affine in z46")
        scalar = coefficient
        local = []
        for variable in monomial:
            if variable == z46:
                continue
            if variable in base_variables:
                scalar *= point[variable]
            else:
                local.append(variable)
        target = slope if degree else constant
        output = tuple(sorted(local))
        target[output] = target.get(output, QQ(0)) + scalar
        if not target[output]:
            target.pop(output)
    return slope, constant


def rational_numerator(parts, numerator, denominator):
    slope, constant = parts
    answer = multiply(slope, numerator)
    add(answer, multiply(constant, denominator))
    return answer


def exact_bend_fraction(layout, point, first, second, third):
    tau = layout["tau"]
    a = layout["a"]
    one = {(): QQ(1)}
    denominator = one
    for parameter in (0, 30, 52):
        factor = {(): QQ(1), (tau,): point[a[parameter]]}
        denominator = multiply(denominator, factor)
    initial = {
        (): point[a[46]],
        (tau,): first,
        (tau, tau): second,
        (tau, tau, tau): third,
    }
    product = multiply(denominator, initial)
    numerator = {
        monomial: coefficient
        for monomial, coefficient in product.items()
        if monomial.count(tau) <= 3
    }
    require(
        any(tau_coefficient(product, tau, degree)
            for degree in range(4, 7)),
        "bend numerator truncation unexpectedly became vacuous",
    )
    # The first four Taylor coefficients of N/P are prescribed by the
    # already certified center bends.  The omitted coefficients are exactly
    # what imposes the three-step recurrence.
    replay = multiply(denominator, initial)
    require(
        all(tau_coefficient(numerator, tau, degree)
            == tau_coefficient(replay, tau, degree)
            for degree in range(4)),
        "rational bend numerator lost an initial coefficient",
    )
    return denominator, numerator


def divide_tau(source, tau, valuation):
    answer = {}
    for monomial, coefficient in source.items():
        output = list(monomial)
        for _index in range(valuation):
            output.remove(tau)
        answer[tuple(output)] = coefficient
    return answer


def tau_valuation(source, tau):
    return min((monomial.count(tau) for monomial in source), default=-1)


def family_digest(sources):
    digest = sha256()
    for source in sources:
        digest.update(REES.polynomial_digest(source).encode())
    return digest.hexdigest()


def singular_names(layout):
    names = [f"x{index}" for index in range(layout["variable_count"])]
    names[layout["tau"]] = "tau"
    for parameter, variable in layout["n"].items():
        names[variable] = f"n{parameter}"
    for pivot, variable in layout["y"].items():
        names[variable] = f"y{pivot}"
    return names


def export(path, target="wronskian-blocks", bend_mode="recurrence"):
    center = POINT.F2.audit(return_data=True)
    schur = SCHUR.audit(return_data=True)
    layout = schur["layout"]
    require(layout == center["layout"], "Schur and center layouts diverged")
    point = POINT.exact_point(center)
    first = point[center["first_bend"]]
    second = point[center["second_bend"]]
    third = POINT.third_bend_root(layout, point, first, second)
    denominator, numerator = exact_bend_fraction(
        layout, point, first, second, third
    )
    if bend_mode == "constant-raw-root":
        numerator = {
            monomial: coefficient * point[layout["a"][46]]
            for monomial, coefficient in denominator.items()
        }

    rows = schur["normal_stricts"] + schur["transverse_pivots"]
    transformed_rows = [
        rational_numerator(
            affine_point_parts(source, layout, point), numerator, denominator
        )
        for source in rows
    ]
    remaining_parameters = [
        row + 1 for row in range(39) if row not in set(P5.B_PIVOT_ROWS)
    ]
    remaining = dict(zip(remaining_parameters, schur["remaining_rows"]))
    parts30 = affine_point_parts(remaining[30], layout, point)
    parts33 = affine_point_parts(remaining[33], layout, point)
    transformed30 = rational_numerator(parts30, numerator, denominator)
    transformed33 = rational_numerator(parts33, numerator, denominator)

    # For F=A*N+B*P and G=C*N+D*P the bend numerator cancels exactly:
    # A*G-C*F=P*(A*D-C*B).  This is the affine Wronskian numerator after
    # cancelling the unit P^3 from the uniform P^4 source clearance.
    block_sources = parts30[0], parts30[1], parts33[0], parts33[1]
    wronskian = None
    bend_free = None
    if target == "wronskian":
        wronskian = multiply(parts30[0], transformed33)
        add(wronskian, multiply(parts33[0], transformed30), QQ(-1))
        bend_free = multiply(parts30[0], parts33[1])
        add(bend_free, multiply(parts33[0], parts30[1]), QQ(-1))
        require(wronskian == multiply(denominator, bend_free),
                "affine Wronskian failed to cancel the rational bend numerator")

    pure = [
        rational_numerator(
            affine_point_parts(source, layout, point), numerator, denominator
        )
        for source in schur["pure_stricts"]
    ]
    require(all(not affine_point_parts(source, layout, point)[0]
                for source in schur["pure_stricts"]),
            "a pure target acquired direct z46 dependence")

    targets = {
        "wronskian": wronskian,
        "M30": transformed30,
        "M33": transformed33,
        "H0": pure[0],
        "H1": pure[1],
    }
    selected = targets.get(target)
    if selected is None:
        valuation = None
        strict_target = None
    else:
        valuation = tau_valuation(selected, layout["tau"])
        strict_target = divide_tau(selected, layout["tau"], valuation)

    names = singular_names(layout)
    ring_order = [names[variable] for variable in layout["y"].values()]
    ring_order += [names[variable] for variable in layout["n"].values()]
    ring_order.append("tau")
    encode = REES.AMBIENT.singular_polynomial
    digest = sha256()
    with Path(path).open("w") as output:
        def write(value):
            output.write(value)
            digest.update(value.encode())

        write(
            "// Exact generic-L point and rational P5 bend; 207 variables "
            "remain implicit.\n"
            f"ring R=0,({','.join(ring_order)}),ds;\n"
        )
        write("ideal S=\n")
        for index, source in enumerate(transformed_rows):
            if index:
                write(",\n")
            write(encode(source, names))
        write(";\nint clock=timer; ideal GS=std(S);\n")
        write('"STD207",size(GS),timer-clock;\n')
        if target == "wronskian-blocks":
            for label, source in zip(
                ("A", "B", "C", "D"),
                block_sources,
            ):
                write(f"poly {label}={encode(source, names)};\n")
                write(
                    f"clock=timer; poly R{label}=reduce({label},GS); "
                    f'"BLOCK","{label}",size({label}),size(R{label}),'
                    f'timer-clock,"FORM",R{label};\n'
                )
            write("poly target=RA*RD-RC*RB;\n")
            write("clock=timer; poly remainder=reduce(target,GS);\n")
            write(
                '"WEAKPRODUCT","wronskian-blocks",size(target),'
                "size(remainder),timer-clock,lead(remainder);\n"
            )
            write("poly diffA=A-C; poly diffB=B-D;\n")
            write("clock=timer; poly remainderA=reduce(diffA,GS);\n")
            write(
                '"DIFF","A-C",size(diffA),size(remainderA),'
                "timer-clock,lead(remainderA);\n"
            )
            write("clock=timer; poly remainderB=reduce(diffB,GS);\n")
            write(
                '"DIFF","B-D",size(diffB),size(remainderB),'
                "timer-clock,lead(remainderB);\n"
            )
            write(f"poly bendN={encode(numerator, names)};\n")
            write(f"poly bendP={encode(denominator, names)};\n")
            write("poly candidate30=RA*bendN+RB*bendP;\n")
            write("clock=timer; poly remainder30=reduce(candidate30,GS);\n")
            write(
                '"WEAKRECON","M30",size(candidate30),size(remainder30),'
                "timer-clock,lead(remainder30),remainder30;\n"
            )
            write("poly candidate33=RC*bendN+RD*bendP;\n")
            write("clock=timer; poly remainder33=reduce(candidate33,GS);\n")
            write(
                '"WEAKRECON","M33",size(candidate33),size(remainder33),'
                "timer-clock,lead(remainder33),remainder33;\nquit;\n"
            )
        else:
            write(f"poly target={encode(strict_target, names)};\n")
            write("clock=timer; poly remainder=reduce(target,GS);\n")
            write(
                f'"TARGET","{target}",size(target),size(remainder),'
                "timer-clock,lead(remainder);\nquit;\n"
            )

    summary = {
        "point": {
            "z46": str(point[layout["a"][46]]),
            "s": str(first),
            "t": str(second),
            "r3": str(third),
        },
        "bend_denominator": (
            "(1+z0*tau)*(1+z30*tau)*(1+z52*tau) at the exact point"
        ),
        "bend_mode": bend_mode,
        "denominator_terms": len(denominator),
        "denominator_sha256": REES.polynomial_digest(denominator),
        "numerator_terms": len(numerator),
        "numerator_sha256": REES.polynomial_digest(numerator),
        "uniform_clearance": (
            "P^4*F(N/P)=P^3*(A*N+B*P); P^3 is a completed-local unit"
        ),
        "implicit_schur_rows": len(transformed_rows),
        "implicit_schur_terms": sum(map(len, transformed_rows)),
        "implicit_schur_sha256": family_digest(transformed_rows),
        "M30_numerator_terms": len(transformed30),
        "M33_numerator_terms": len(transformed33),
        "wronskian_bend_independent": (
            "formal identity A*(C*N+D*P)-C*(A*N+B*P)=P*(A*D-C*B)"
        ),
        "wronskian_terms": None if wronskian is None else len(wronskian),
        "wronskian_sha256": (
            None if wronskian is None else REES.polynomial_digest(wronskian)
        ),
        "wronskian_block_terms": {
            label: len(source) for label, source in zip(
                ("A", "B", "C", "D"),
                block_sources,
            )
        },
        "wronskian_block_sha256": {
            label: REES.polynomial_digest(source)
            for label, source in zip(
                ("A", "B", "C", "D"),
                block_sources,
            )
        },
        "H0_numerator_terms": len(pure[0]),
        "H0_numerator_sha256": REES.polynomial_digest(pure[0]),
        "H1_numerator_terms": len(pure[1]),
        "H1_numerator_sha256": REES.polynomial_digest(pure[1]),
        "selected_target": target,
        "selected_tau_valuation": valuation,
        "selected_strict_terms": (
            None if strict_target is None else len(strict_target)
        ),
        "selected_strict_sha256": (
            None if strict_target is None
            else REES.polynomial_digest(strict_target)
        ),
        "export_sha256": digest.hexdigest(),
        "export_bytes": Path(path).stat().st_size,
        "scope_guard": (
            "exact finite rational-Rees point export; membership is decided "
            "only if the optional Singular reduction completes"
        ),
    }
    return summary


def run_singular(path, timeout):
    completed = subprocess.run(
        ["/usr/local/bin/Singular", "-q", str(path)],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        check=False,
    )
    require(completed.returncode == 0,
            "rational-Rees point reduction failed")
    print(completed.stdout)
    return {
        "stdout": completed.stdout,
        "stdout_sha256": sha256(completed.stdout.encode()).hexdigest(),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    parser.add_argument(
        "--target",
        choices=(
            "wronskian", "wronskian-blocks", "M30", "M33", "H0", "H1",
        ),
        default="wronskian-blocks",
    )
    parser.add_argument("--run-singular", action="store_true")
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument(
        "--bend-mode",
        choices=("recurrence", "constant-raw-root"),
        default="recurrence",
    )
    arguments = parser.parse_args()
    summary = export(arguments.path, arguments.target, arguments.bend_mode)
    if arguments.run_singular:
        summary["singular"] = run_singular(arguments.path, arguments.timeout)
    encoded = json.dumps(summary, sort_keys=True, separators=(",", ":"))
    print(json.dumps(summary, indent=2, sort_keys=True))
    print(f"ledger_sha256={sha256(encoded.encode()).hexdigest()}")


if __name__ == "__main__":
    main()
