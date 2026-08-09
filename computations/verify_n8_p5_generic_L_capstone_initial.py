#!/usr/bin/env python3
"""Complete the generic-L P5 strict-seven initial-form certificate.

This checker extends the source-faithful strict-seven calculation from the
eleven b-pivots and Q30/Q33 to all 39 normal-eliminated mixed equations.  It
certifies the unit 12-by-12 initial Jacobian and reduces every strict-seven
compatibility initial form by the old localized branch equations and the
monic scalar equation G.

These are initial forms on the third iterated strict-transform chart, not the
full completed-local germs.  A finite Mora proof still needs an explicit
source chart map from the 252 translated ambient variables.
"""

from fractions import Fraction
from hashlib import sha256
import gc
import importlib.util
import json
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent


def load_module(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SYMBOLIC = load_module(
    "n8_p5_strict7_symbolic_for_capstone",
    "verify_n8_p5_generic_L_strict7_symbolic.py",
)
POINT = SYMBOLIC.POINT
GENERIC = SYMBOLIC.GENERIC
THIRD = SYMBOLIC.THIRD
P5 = SYMBOLIC.P5
COMPAT = SYMBOLIC.COMPAT
QQ = Fraction

EXPECTED_LEDGER_SHA256 = (
    "19e4469d98db50c431102bb6ed8de2a6766cdfde9ae8ade76be13bb003e5012d"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def add(target, source, scale=QQ(1)):
    SYMBOLIC.add(target, source, scale)


def polynomial_digest(source):
    return SYMBOLIC.polynomial_digest(source)


def multiply(left, right):
    return SYMBOLIC.multiply(left, right)


def conormal_certificate(common_factor):
    """Differentiate the committed H0=U*G initial-factor identity."""

    common_monomial = P5.monomial(11, 16, 16, 41)
    b = P5.polynomial((((44,), 1), ((45,), 1)))
    delta = P5.polynomial((((53,), 1), ((51,), -1)))
    multiplier = multiply(multiply(common_monomial, b), delta)
    h0_initial = multiply(multiplier, common_factor)
    for variable in range(60):
        derivative_h0 = P5.derivative(h0_initial, variable)
        multiplier_dg = multiply(
            multiplier, P5.derivative(common_factor, variable)
        )
        difference = dict(derivative_h0)
        add(difference, multiplier_dg, -1)
        expected = multiply(
            common_factor, P5.derivative(multiplier, variable)
        )
        require(difference == expected,
                f"H0 conormal product rule failed at z{variable}")
    require(
        P5.derivative(h0_initial, SYMBOLIC.THIRD_BEND)
        == {monomial: -coefficient
            for monomial, coefficient in multiplier.items()},
        "H0 newest-bend derivative changed",
    )
    return {
        "H0_initial_terms": len(h0_initial),
        "H0_initial_sha256": polynomial_digest(h0_initial),
        "multiplier_terms": len(multiplier),
        "multiplier_sha256": polynomial_digest(multiplier),
        "variables_checked": 60,
        "identity": "d(H0^10)-U*dG=G*dU",
        "quotient_consequence": "d(H0^10)=U*dG mod (G)",
    }


def singular_reduce(first, exceptional, common_factor, rows):
    names = [f"z{index}" for index in range(60)]
    ring_order = [
        names[SYMBOLIC.THIRD_BEND], names[GENERIC.SECOND_BEND],
        names[GENERIC.FIRST_BEND], names[SYMBOLIC.INVERSE_B],
        "w", "p16", "p41",
    ] + names[:56]

    def encode(source):
        return COMPAT.AMBIENT.singular_polynomial(source, names)

    lines = [
        f"ring r=0,({','.join(ring_order)}),dp;",
        "poly ell=z9*z25-z11*z46;",
        f"poly first={encode(first)};",
        f"poly second30={encode(exceptional[0])};",
        f"poly second33={encode(exceptional[1])};",
        f"poly G={encode(common_factor)};",
        "poly loc11=z11*w-1;",
        "poly locb=(z44+z45)*z59-1;",
        "poly loc16=z16*p16-1;",
        "poly loc41=z41*p41-1;",
        "poly second=z59*(second30-second33);",
        "ideal lifted=ell,first,second,loc11,locb,loc16,loc41,G;",
        "ideal gb=std(lifted);",
        '"UNIT",(reduce(1,gb)==0);',
    ]
    for number, source in rows:
        lines.extend((
            f"poly q{number}={encode(source)};",
            f"poly n{number}=reduce(q{number},gb);",
            f'"ROW",{number},size(n{number}),(n{number}==0);',
        ))
    lines.append("quit;")
    completed = subprocess.run(
        ["/usr/local/bin/Singular", "-q"],
        input="\n".join(lines),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
        timeout=1200,
    )
    require(completed.returncode == 0,
            "Singular all-row strict7 reduction failed")
    print(completed.stdout, flush=True)
    require("UNIT 0" in completed.stdout,
            "localized strict7 initial ideal became unit")
    result = {}
    for line in completed.stdout.splitlines():
        if not line.startswith("ROW "):
            continue
        _label, number, terms, zero = line.split()
        result[int(number)] = {"terms": int(terms), "zero": zero == "1"}
    require(len(result) == 39, "Singular did not report all 39 rows")
    require(all(item["zero"] for item in result.values()),
            "a strict7 compatibility initial form survived G")
    return result


def strict7_rows():
    data = GENERIC.symbolic_lift_data()
    degree8 = data["degree8"]
    compatibility = data["compatibility"]
    parts = compatibility["parts"]
    jacobian = compatibility["jacobian"]
    first, exceptional = SYMBOLIC.old_relations(data)

    c1 = {coordinate: dict(value)
          for coordinate, value in data["corrections"][0].items()}
    c2 = {coordinate: dict(value)
          for coordinate, value in data["corrections"][1].items()}
    c3 = {coordinate: dict(value)
          for coordinate, value in data["corrections"][2].items()}
    c3[46] = P5.monomial(SYMBOLIC.THIRD_BEND)
    corrections = [c1, c2, c3]

    pivot_rows = set(P5.B_PIVOT_ROWS)
    series = degree8["degree_seven_data"]["series"]
    old_higher = {
        row: data["strict"].higher_strict_orders(series._state(row + 1))
        for row in pivot_rows
    }

    residual4 = {"jacobian": jacobian}
    for row in pivot_rows:
        value = SYMBOLIC.strict_residual_row(parts, corrections, 4, row)
        add(value, degree8["degree_seven_data"]["degree_six"][row])
        residual4[row] = value
    c4 = SYMBOLIC.transverse_from_pivots(residual4, "strict order four")
    require(SYMBOLIC.restrict_correction(c4, SYMBOLIC.THIRD_BEND)
            == data["corrections"][3],
            "third-bend c4 failed its zero-bend regression")
    corrections.append(c4)

    residual5 = {"jacobian": jacobian}
    for row in pivot_rows:
        value = SYMBOLIC.strict_residual_row(parts, corrections, 5, row)
        add(value, old_higher[row][0])
        residual5[row] = value
    c5 = SYMBOLIC.transverse_from_pivots(residual5, "strict order five")
    require(SYMBOLIC.restrict_correction(c5, SYMBOLIC.THIRD_BEND)
            == data["corrections"][4],
            "third-bend c5 failed its zero-bend regression")
    corrections.append(c5)

    residual6 = {"jacobian": jacobian}
    for row in pivot_rows:
        value = SYMBOLIC.strict_residual_row(parts, corrections, 6, row)
        add(value, old_higher[row][1])
        residual6[row] = value
    c6 = SYMBOLIC.transverse_localized_from_pivots(
        residual6, "strict order six"
    )
    corrections.append(c6)
    del old_higher, residual4, residual5, residual6
    gc.collect()

    third = POINT.third_from_second(
        series.reducer, degree8["second_projector"]
    )
    require(not THIRD.validate_normal_graph(third),
            "symbolic strict7 third normal graph regression returned")
    strict = THIRD.ThirdStrictProjector(third, corrections[:3])
    rows = []
    pivot_residuals = {}

    # The eleven pivot rows are needed first to construct c7.  Release every
    # state cache immediately: polynomial identity, not object equality, is
    # the invariant here.
    for row in sorted(pivot_rows):
        state = series._state(row + 1)
        higher = POINT.higher_mixed_coefficients(strict, state, (9,))[9]
        value = SYMBOLIC.strict_residual_row(parts, corrections, 7, row)
        add(value, higher)
        pivot_residuals[row] = value
        POINT.clear_state_caches(strict)
        print("PIVOT", row + 1, len(value), flush=True)

    localized7 = {"jacobian": jacobian, **pivot_residuals}
    c7 = SYMBOLIC.transverse_localized_from_pivots(
        localized7, "strict order seven"
    )

    for row in range(39):
        if row in pivot_residuals:
            residual = pivot_residuals[row]
        else:
            state = series._state(row + 1)
            higher = POINT.higher_mixed_coefficients(strict, state, (9,))[9]
            residual = SYMBOLIC.strict_residual_row(
                parts, corrections, 7, row
            )
            add(residual, higher)
            POINT.clear_state_caches(strict)
        value = SYMBOLIC.compatibility_row(residual, c7, jacobian[row])
        rows.append((row + 1, value))
        print("ROW", row + 1, len(value), polynomial_digest(value), flush=True)

    return first, exceptional, rows


def audit():
    # The 11 pivot initial equations have Jacobian b*I in their 11 newest
    # transverse variables.  The scalar G has coefficient -1 in r and is
    # independent of those newest transverse variables, hence the block
    # determinant is exactly -b^11, a unit on the b chart.
    common_factor = SYMBOLIC.strict7_common_factor()
    derivative_r = P5.derivative(common_factor, SYMBOLIC.THIRD_BEND)
    require(derivative_r == {(): QQ(-1)}, "G stopped being monic in r")
    require(all(
        not P5.derivative(common_factor, variable)
        for variable in P5.P5_NORMAL_VARIABLES
    ), "G unexpectedly depends on a newest transverse pivot variable")

    conormal = conormal_certificate(common_factor)
    first, exceptional, rows = strict7_rows()
    reduction = singular_reduce(first, exceptional, common_factor, rows)
    ledger = {
        "branch": "P5 generic L",
        "chart": "z16*z41*z11*(z44+z45) != 0",
        "initial_jacobian": {
            "pivot_block": "(z44+z45)*I_11",
            "scalar_derivative": "dG/dr=-1",
            "determinant": "-(z44+z45)^11",
            "unit_on_chart": True,
        },
        "strict7_rows": [
            [number, len(source), polynomial_digest(source)]
            for number, source in rows
        ],
        "strict7_total_terms": sum(len(source) for _number, source in rows),
        "strict7_maximum_terms": max(len(source) for _number, source in rows),
        "localized_initial_reduction": {
            "rows_reduced": len(reduction),
            "all_zero": all(item["zero"] for item in reduction.values()),
            "ideal_nonunit": True,
        },
        "H0_initial_conormal": conormal,
        "scope_guard": (
            "complete strict-order-seven initial-form certificate only; "
            "the full completed-local germs and full H0/H1 membership are "
            "not represented by this finite input"
        ),
        "mora_missing_input": (
            "an explicit finite iterated P5/L strict-transform homomorphism "
            "from the 252 translated ambient variables, retaining the 196 "
            "smooth-normal variables and the radial/remainder coordinates"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "P5 capstone initial ledger changed")
    print(json.dumps(ledger, indent=2, sort_keys=True))
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    audit()
