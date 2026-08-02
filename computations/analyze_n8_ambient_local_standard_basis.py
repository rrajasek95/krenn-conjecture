#!/usr/bin/env python3
"""Attempt the finite 252-variable local standard-basis formulation.

The formal normal-coordinate reducer can be replaced in principle by a Mora
standard-basis calculation in the original translated polynomial ring.  This
analyzer constructs exactly that finite input:

* 196 literal mixed-equation combinations with independent linear leads;
* 39 literal zero-gradient obstruction lifts; and
* the nine compact cubic combinations completing the tangent basis.

It then asks Singular for a local ``ds`` standard basis.  The subprocess is
time- and RSS-bounded because this is an exploratory route, not a frozen
certificate.  No claim is made unless Singular returns a parsed result.
"""

from fractions import Fraction
import argparse
import importlib.util
from pathlib import Path
import re
import subprocess
import threading
import time

HERE = Path(__file__).resolve().parent
LOCAL_SPEC = importlib.util.spec_from_file_location(
    "n8_local_standard_basis", HERE / "analyze_n8_counterexample_local_standard_basis.py"
)
LOCAL = importlib.util.module_from_spec(LOCAL_SPEC)
LOCAL_SPEC.loader.exec_module(LOCAL)


CUBIC = LOCAL.CUBIC
QQ = Fraction


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def full_polynomial(reducer, functional):
    answer = {}
    for degree in range(5):
        CUBIC.add_scaled(answer, reducer.functional_hasse(functional, degree))
    return answer


def singular_polynomial(polynomial, names, rees_base_degree=None):
    terms = []
    for monomial, coefficient in sorted(polynomial.items()):
        coefficient = Fraction(coefficient)
        scalar = (
            str(coefficient.numerator)
            if coefficient.denominator == 1
            else f"({coefficient.numerator}/{coefficient.denominator})"
        )
        variable_factors = [names[index] for index in monomial]
        if rees_base_degree is not None:
            rees_power = len(monomial) - rees_base_degree
            require(rees_power >= 0, "negative Rees exponent")
            variable_factors = ["t"] * rees_power + variable_factors
        variables = "*".join(variable_factors)
        terms.append(scalar if not variables else f"{scalar}*{variables}")
    return "+".join(terms).replace("+-", "-") or "0"


def finite_generators():
    reducer = LOCAL.LocalReducer()
    jacobian_pivots = list(reducer.jacobian_pivots)
    normal_generators = [
        full_polynomial(reducer, reducer.jacobian_functional(pivot))
        for pivot in jacobian_pivots
    ]
    for pivot, polynomial in zip(jacobian_pivots, normal_generators):
        linear = {m: c for m, c in polynomial.items() if len(m) == 1}
        require(
            min(linear) == (pivot,) and linear[pivot,] == 1,
            f"normal generator at {pivot} lost its echelon lead",
        )

    obstruction_items = list(reducer.data["obstruction_pivots"].items())
    obstruction_generators = [
        full_polynomial(reducer, reducer.obstruction_functional(pivot))
        for pivot, _value in obstruction_items
    ]
    require(
        all(not any(len(m) < 2 for m in polynomial)
            for polynomial in obstruction_generators),
        "an obstruction lift acquired degree below two",
    )

    desired_quadrics = {
        1: {(12, 25): QQ(1), (18, 46): QQ(-1)},
        5: {(12, 46): QQ(1)},
        6: {(13, 25): QQ(1), (19, 46): QQ(-1)},
        10: {(13, 46): QQ(1)},
        11: {(14, 25): QQ(1), (20, 46): QQ(-1)},
        14: {(14, 46): QQ(1)},
        24: {(18, 25): QQ(1)},
        28: {(19, 25): QQ(1)},
        32: {(20, 25): QQ(1)},
    }
    quadratic_number = {}
    for name, desired in desired_quadrics.items():
        matches = [
            number
            for number, (_pivot, (row, _representative))
            in enumerate(obstruction_items, 1)
            if row == desired
        ]
        require(len(matches) == 1,
                f"sparse obstruction Q{name} match changed: {matches}")
        quadratic_number[name] = matches[0]

    definitions = {
        40: ((-46, 11), (25, 14)),
        41: ((-46, 6), (25, 10)),
        42: ((-46, 1), (25, 5)),
        43: ((-20, 11), (14, 32)),
        44: ((-20, 6), (13, 32)),
        45: ((-20, 1), (12, 32)),
        46: ((-19, 6), (13, 28)),
        47: ((-19, 1), (12, 28)),
        48: ((-18, 1), (12, 24)),
    }
    cubic_generators = []
    for number in range(40, 49):
        polynomial = {}
        for signed_tangent_variable, quadratic_name in definitions[number]:
            ambient_variable = reducer.free_columns[abs(signed_tangent_variable)]
            CUBIC.add_scaled(
                polynomial,
                CUBIC.multiply_polynomials(
                    {(ambient_variable,): QQ(1)},
                    obstruction_generators[
                        quadratic_number[quadratic_name] - 1
                    ],
                ),
                -1 if signed_tangent_variable < 0 else 1,
            )
        require(not any(len(m) < 3 for m in polynomial),
                f"C{number} acquired degree below three")
        cubic_generators.append(polynomial)

    return normal_generators, obstruction_generators, cubic_generators


def singular_source(characteristic, rees):
    normal, quadratic, cubic = finite_generators()
    names = [f"x{index}" for index in range(252)]
    generators = normal + quadratic + cubic
    base_degrees = [1] * len(normal) + [2] * len(quadratic) + [3] * len(cubic)
    encoded = [
        singular_polynomial(
            polynomial, names, base_degree if rees else None
        )
        for polynomial, base_degree in zip(generators, base_degrees)
    ]
    ring_names = (["t"] + names) if rees else names
    ordering = "(ls(1),dp(252))" if rees else "ds"
    source = f"""
ring r={characteristic},({','.join(ring_names)}),{ordering};
ideal F={','.join(encoded)};
int started=timer;
ideal G=std(F);
int elapsed=timer-started;
int n1=0; int n2=0; int n3=0; int n4=0; int nhi=0; int i; int d;
for (i=1;i<=size(G);i++)
{{
  d=deg(lead(G[i]));
  if (d==1) {{ n1=n1+1; }}
  else {{ if (d==2) {{ n2=n2+1; }}
  else {{ if (d==3) {{ n3=n3+1; }}
  else {{ if (d==4) {{ n4=n4+1; }} else {{ nhi=nhi+1; }} }} }} }}
}}
"RESULT",size(F),size(G),n1,n2,n3,n4,nhi,elapsed;
quit;
"""
    ledger = {
        "ambient_variables": 252,
        "characteristic": characteristic,
        "rees_parameter": rees,
        "normal_generators": len(normal),
        "normal_terms": sum(map(len, normal)),
        "quadratic_generators": len(quadratic),
        "quadratic_terms": sum(map(len, quadratic)),
        "cubic_generators": len(cubic),
        "cubic_terms": sum(map(len, cubic)),
        "singular_source_characters": len(source),
    }
    return source, ledger


def resident_kib(pid):
    completed = subprocess.run(
        ["ps", "-o", "rss=", "-p", str(pid)],
        text=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
        check=False,
    )
    try:
        return int(completed.stdout.strip())
    except ValueError:
        return 0


def bounded_singular(source, timeout_seconds, memory_mib):
    process = subprocess.Popen(
        ["Singular", "-q"], stdin=subprocess.PIPE,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True,
    )
    writer_error = []

    def write_source():
        try:
            process.stdin.write(source)
            process.stdin.close()
        except (BrokenPipeError, OSError) as error:
            writer_error.append(str(error))

    writer = threading.Thread(target=write_source, daemon=True)
    writer.start()
    started = time.monotonic()
    peak_kib = 0
    stop_reason = None
    while process.poll() is None:
        peak_kib = max(peak_kib, resident_kib(process.pid))
        if peak_kib > memory_mib * 1024:
            stop_reason = f"memory cap {memory_mib} MiB"
            process.kill()
            break
        if time.monotonic() - started > timeout_seconds:
            stop_reason = f"timeout {timeout_seconds} seconds"
            process.kill()
            break
        time.sleep(0.05)
    process.wait()
    writer.join(timeout=1)
    output = process.stdout.read()
    return output, process.returncode, peak_kib, stop_reason, writer_error


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit-singular", action="store_true")
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--memory-mib", type=int, default=700)
    parser.add_argument("--characteristic", type=int, default=32003)
    parser.add_argument("--rees", action="store_true")
    arguments = parser.parse_args()
    source, ledger = singular_source(arguments.characteristic, arguments.rees)
    if arguments.emit_singular:
        print(source, end="")
        return
    print(f"finite ambient input: {ledger}", flush=True)
    output, returncode, peak_kib, stop_reason, writer_error = bounded_singular(
        source, arguments.timeout, arguments.memory_mib
    )
    match = re.search(
        r"RESULT\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+"
        r"(\d+)\s+(\d+)\s+(\d+)\s+(\d+)",
        output,
    )
    if match:
        values = tuple(map(int, match.groups()))
        print(
            "finite ambient local standard basis returned: "
            f"input={values[0]}, basis={values[1]}, "
            f"lead degrees 1/2/3/4/higher={values[2:7]}, "
            f"Singular ticks={values[7]}, peak={peak_kib / 1024:.1f} MiB"
        )
        return
    detail = stop_reason or f"Singular exit {returncode}"
    print(
        "finite ambient local standard basis: INCOMPLETE; "
        f"{detail}, peak={peak_kib / 1024:.1f} MiB, "
        f"writer_errors={writer_error}"
    )
    if output.strip():
        print(output[-4000:])


if __name__ == "__main__":
    main()
