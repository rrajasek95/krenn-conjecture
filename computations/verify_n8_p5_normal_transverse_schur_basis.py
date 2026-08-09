#!/usr/bin/env python3
"""Certify the 196+11 source-faithful P5 Schur standard-basis block."""

from fractions import Fraction
from hashlib import sha256
import argparse
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def load_module(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


REES = load_module(
    "n8_p5_finite_rees_for_transverse_basis",
    "analyze_n8_p5_finite_rees_chart.py",
)
P5 = REES.P5
QQ = Fraction

EXPECTED_LEDGER_SHA256 = (
    "6d793205d5f727d4aed253aa001b753a3b9faf0fdf694406c26f738fc1ec5636"
)
EXPECTED_QQ_EXPORT_SHA256 = (
    "ae1be4fa4fc3034a5f5695d5db37d7a3db2542445a88731ada0f1db9697727e8"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def add(target, source, scale=QQ(1)):
    REES.add(target, source, scale)


def family_digest(sources):
    digest = sha256()
    for source in sources:
        digest.update(REES.polynomial_digest(source).encode())
    return digest.hexdigest()


def shifted_forms(forms, layout, offsets, tau_power):
    inverse_normals = {}
    for pivot, direction in layout["directions"].items():
        for coordinate, coefficient in direction.items():
            inverse_normals.setdefault(coordinate, []).append(
                (layout["y"][pivot], coefficient)
            )
    tau_prefix = (layout["tau"],) * tau_power
    answer = [dict(source) for source in forms]
    for coordinate, entries in inverse_normals.items():
        for y_variable, coefficient in entries:
            correction = {
                tuple(sorted(tau_prefix + monomial)): value
                for monomial, value in offsets[y_variable].items()
            }
            add(answer[coordinate], correction, -coefficient)
    return answer


def normal_strict(source, forms, tau):
    transformed, maximum = REES.substitute(source, forms)
    valuation = REES.tau_valuation(transformed, tau)
    require(valuation >= 2, "normal generator lost tau^2")
    return REES.divide_tau(transformed, tau, 2), valuation, maximum


def local_degree(monomial, local_variables):
    return sum(variable in local_variables for variable in monomial)


def solve_q_offset(strict, pivot_variable, tau, y_variables):
    tau_zero = {
        monomial: coefficient
        for monomial, coefficient in strict.items()
        if tau not in monomial
    }
    require(tau_zero.get((pivot_variable,)) == QQ(1),
            "unshifted normal row lost its unit pivot")
    tau_zero.pop((pivot_variable,))
    require(
        not any(
            any(variable in y_variables for variable in monomial)
            for monomial in tau_zero
        ),
        "unshifted normal offset contains y",
    )
    return tau_zero


def strict_record(label, number, source, forms, tau):
    transformed, maximum = REES.substitute(source, forms)
    valuation = REES.tau_valuation(transformed, tau)
    strict = REES.divide_tau(transformed, tau, valuation)
    return strict, {
        "label": label,
        "number": number,
        "valuation": valuation,
        "terms": len(strict),
        "maximum_term_product": maximum,
        "sha256": REES.polynomial_digest(strict),
    }


def map_parameter_polynomial(source, layout):
    answer = {}
    for monomial, coefficient in source.items():
        require(all(parameter in layout["a"] for parameter in monomial),
                "P5 first correction left the free parameter block")
        output = tuple(sorted(layout["a"][parameter] for parameter in monomial))
        answer[output] = coefficient
    return answer


def first_transverse_shift(forms, reducer, layout):
    corrections = P5.expected_corrections()[0]
    mapped = {
        parameter: map_parameter_polynomial(source, layout)
        for parameter, source in corrections.items()
    }
    answer = [dict(source) for source in forms]
    tau = layout["tau"]
    for coordinate, tangent in enumerate(reducer._tangent_coordinate_forms):
        for parameter, correction in mapped.items():
            coefficient = tangent.get(parameter, QQ(0))
            if not coefficient:
                continue
            lifted = {
                tuple(sorted((tau, tau) + monomial)): value
                for monomial, value in correction.items()
            }
            add(answer[coordinate], lifted, coefficient)
    return answer, mapped


def local_linear(source, local_variables):
    return {
        monomial: coefficient
        for monomial, coefficient in source.items()
        if local_degree(monomial, local_variables) == 1
    }


def coefficient_of_local_variable(linear, variable, local_variables):
    answer = {}
    for monomial, coefficient in linear.items():
        if variable not in monomial:
            continue
        require(
            sum(item in local_variables for item in monomial) == 1,
            "coefficient extraction received a nonlinear local monomial",
        )
        output = list(monomial)
        output.remove(variable)
        output = tuple(output)
        answer[output] = coefficient
    return answer


def base_multiply(base, source):
    return REES.multiply(base, source)


def singular_polynomial_on_b_chart(source, names, z45, z44):
    terms = []
    for monomial, coefficient in sorted(source.items()):
        coefficient = QQ(coefficient)
        scalar = (
            str(coefficient.numerator)
            if coefficient.denominator == 1
            else f"({coefficient.numerator}/{coefficient.denominator})"
        )
        factors = [
            f"(b-{names[z44]})" if variable == z45 else names[variable]
            for variable in monomial
        ]
        product = "*".join(factors)
        terms.append(scalar if not product else f"{scalar}*{product}")
    return "+".join(terms).replace("+-", "-") or "0"


def export_singular(
    path,
    characteristic,
    layout,
    normals,
    transverse,
    remaining,
    pure,
):
    names = REES.variable_names(layout)
    z45 = layout["a"][45]
    z44 = layout["a"][44]
    local = [names[variable] for variable in layout["y"].values()]
    local += [names[variable] for variable in layout["n"].values()]
    local.append(names[layout["tau"]])
    base = [
        names[variable] for parameter, variable in layout["a"].items()
        if parameter != 45
    ]
    require(len(local) == 208 and len(base) == 44,
            "b-chart Singular block sizes changed")
    digest = sha256()
    with Path(path).open("w") as output:
        def write(value):
            output.write(value)
            digest.update(value.encode())

        write(
            "// Generic b=z44+z45 Schur quotient; exploratory input.\n"
            f"ring R=({characteristic},b),({','.join(local + base)}),"
            "(ds(208),dp(44));\n"
        )
        for ideal_name, sources in (
            ("N", normals),
            ("P", transverse),
            ("M", remaining),
        ):
            write(f"ideal {ideal_name}=\n")
            for number, source in enumerate(sources):
                if number:
                    write(",\n")
                write(singular_polynomial_on_b_chart(
                    source, names, z45, z44
                ))
            write(";\n")
        for colour, source in enumerate(pure):
            write(
                f"poly H{colour}="
                + singular_polynomial_on_b_chart(source, names, z45, z44)
                + ";\n"
            )
        write(
            "ideal S=N,P;\n"
            '"LOADED",size(N),size(P),size(M),size(H0),size(H1);\n'
            "int started=timer;\n"
            "ideal G=std(S);\n"
            '"STD207",size(G),timer-started,lead(G[1]),lead(G[size(G)]);\n'
        )
    return digest.hexdigest()


def audit(singular_path=None, characteristic=0, return_data=False):
    reducer = REES.AMBIENT.LOCAL.LocalReducer()
    normal_sources, obstruction_sources, _cubic = (
        REES.AMBIENT.finite_generators()
    )
    layout = REES.variable_layout(reducer)
    tau = layout["tau"]
    y_variables = frozenset(layout["y"].values())
    n_variables = frozenset(layout["n"].values())
    local_variables = y_variables | n_variables | {tau}
    pivots = tuple(reducer.jacobian_pivots)

    forms0 = REES.coordinate_forms(reducer, layout)
    q_offsets = {}
    for pivot, source in zip(pivots, normal_sources):
        strict, valuation, _maximum = normal_strict(
            source, forms0, tau
        )
        require(valuation == 2, "unshifted normal valuation changed")
        q_offsets[layout["y"][pivot]] = solve_q_offset(
            strict, layout["y"][pivot], tau, y_variables
        )

    forms1 = shifted_forms(forms0, layout, q_offsets, 2)
    forms, first_correction = first_transverse_shift(
        forms1, reducer, layout
    )

    normal_stricts = []
    normal_tau_coefficients = []
    for number, (pivot, source) in enumerate(
        zip(pivots, normal_sources), 1
    ):
        strict, valuation, _maximum = normal_strict(source, forms, tau)
        require(valuation == 2,
                f"shifted normal {number} valuation changed")
        require(
            not any(
                local_degree(monomial, local_variables) == 0
                for monomial in strict
            ),
            f"normal {number} did not vanish at the shifted center",
        )
        linear = local_linear(strict, local_variables)
        require(linear.get((layout["y"][pivot],)) == QQ(1),
                f"normal {number} lost its y pivot")
        for other in y_variables | n_variables:
            if other == layout["y"][pivot]:
                continue
            require(
                not coefficient_of_local_variable(
                    linear, other, local_variables
                ),
                f"normal {number} acquired another y/n local lead",
            )
        tau_coefficient = coefficient_of_local_variable(
            linear, tau, local_variables
        )
        replay = {(layout["y"][pivot],): QQ(1)}
        add(
            replay,
            {
                tuple(sorted((tau,) + monomial)): coefficient
                for monomial, coefficient in tau_coefficient.items()
            },
        )
        require(linear == replay,
                f"normal {number} local linear decomposition failed")
        normal_stricts.append(strict)
        normal_tau_coefficients.append(tau_coefficient)

    obstruction_stricts = []
    for number, source in enumerate(obstruction_sources, 1):
        strict, record = strict_record(
            "obstruction", number, source, forms, tau
        )
        require(record["valuation"] == 3,
                f"obstruction {number} valuation changed")
        require(
            not any(
                local_degree(monomial, local_variables) == 0
                for monomial in strict
            ),
            f"obstruction {number} did not vanish at the shifted center",
        )
        obstruction_stricts.append(strict)

    b = {
        (layout["a"][44],): QQ(1),
        (layout["a"][45],): QQ(1),
    }
    transverse_pivots = []
    for column, row in enumerate(P5.B_PIVOT_ROWS):
        source = dict(obstruction_stricts[row])
        linear = local_linear(source, local_variables)
        # Clear all y-linear terms by exact full-row operations with N.
        for y_variable, normal in zip(
            (layout["y"][pivot] for pivot in pivots), normal_stricts
        ):
            coefficient = coefficient_of_local_variable(
                linear, y_variable, local_variables
            )
            if coefficient:
                add(source, base_multiply(coefficient, normal), QQ(-1))

        reduced_linear = local_linear(source, local_variables)
        require(
            not any(
                local_degree(monomial, local_variables) == 0
                for monomial in source
            ),
            f"pivot obstruction {row + 1} acquired a local constant",
        )
        require(
            not any(
                coefficient_of_local_variable(
                    reduced_linear, variable, local_variables
                )
                for variable in y_variables
            ),
            f"pivot obstruction {row + 1} retained a y-linear term",
        )
        for other, parameter in enumerate(P5.P5_NORMAL_VARIABLES):
            expected = b if column == other else {}
            require(
                coefficient_of_local_variable(
                    reduced_linear,
                    layout["n"][parameter],
                    local_variables,
                ) == expected,
                f"pivot obstruction {row + 1} lost bI at n{parameter}",
            )
        transverse_pivots.append(source)

    pure_stricts = []
    for colour in (0, 1):
        source = REES.pure_residual(reducer, colour)
        strict, record = strict_record(
            f"H{colour}", colour, source, forms, tau
        )
        require(record["valuation"] == 3,
                f"H{colour} valuation changed")
        pure_stricts.append(strict)

    remaining_rows = [
        source for row, source in enumerate(obstruction_stricts)
        if row not in set(P5.B_PIVOT_ROWS)
    ]
    require(len(remaining_rows) == 28, "remaining mixed row count changed")

    export_sha256 = None
    if singular_path is not None:
        export_sha256 = export_singular(
            singular_path,
            characteristic,
            layout,
            normal_stricts,
            transverse_pivots,
            remaining_rows,
            pure_stricts,
        )
        if characteristic == 0:
            require(export_sha256 == EXPECTED_QQ_EXPORT_SHA256,
                    "characteristic-zero Schur export changed")
        print(f"singular_export_sha256={export_sha256}")

    ledger = {
        "chart": {
            "variables": 253,
            "coefficient_base_variables": 45,
            "local_variables": 208,
            "normal_variables": 196,
            "transverse_variables": 11,
            "tau": 1,
            "localized_unit": "b=z44+z45",
        },
        "q_offsets": {
            "terms": sum(map(len, q_offsets.values())),
            "sha256": family_digest(q_offsets.values()),
        },
        "first_transverse_correction": {
            "nonzero_variables": len(first_correction),
            "terms": sum(map(len, first_correction.values())),
            "sha256": family_digest(first_correction.values()),
        },
        "shifted_coordinate_forms": {
            "terms": sum(map(len, forms)),
            "maximum_terms": max(map(len, forms)),
            "sha256": family_digest(forms),
        },
        "normal_standard_basis": {
            "generators": len(normal_stricts),
            "terms": sum(map(len, normal_stricts)),
            "maximum_terms": max(map(len, normal_stricts)),
            "sha256": family_digest(normal_stricts),
            "tau_linear_coefficient_terms": sum(
                map(len, normal_tau_coefficients)
            ),
            "initial_monomials": "196 distinct y_p",
        },
        "transverse_standard_basis": {
            "generators": len(transverse_pivots),
            "terms_after_y_row_operations": sum(map(len, transverse_pivots)),
            "maximum_terms": max(map(len, transverse_pivots)),
            "sha256": family_digest(transverse_pivots),
            "initial_monomials_after_localizing_b": (
                "11 distinct n_j"
            ),
            "jacobian": "b*I_11",
        },
        "combined_standard_basis": {
            "generators": 207,
            "initial_monomials": "196 y_p and 11 n_j, pairwise coprime",
            "coefficient_ring": "Q[z0,...,z55,b^-1]",
            "local_order": "ds(y_196,n_11,tau) over the coefficient ring",
            "consequence": (
                "Buchberger's product criterion proves these selected full "
                "strict transforms form a local standard basis"
            ),
        },
        "remaining_inputs": {
            "mixed_germs": 28,
            "mixed_terms": sum(map(len, remaining_rows)),
            "mixed_sha256": family_digest(remaining_rows),
            "obstruction_terms_before_selected_row_operations": sum(
                map(len, obstruction_stricts)
            ),
            "obstruction_sha256": family_digest(obstruction_stricts),
            "H0_terms": len(pure_stricts[0]),
            "H0_sha256": REES.polynomial_digest(pure_stricts[0]),
            "H1_terms": len(pure_stricts[1]),
            "H1_sha256": REES.polynomial_digest(pure_stricts[1]),
        },
        "scope_guard": (
            "exact characteristic-zero 207-row Schur standard basis; the "
            "28 mixed and H0/H1 normal forms and generic-L saturation remain"
        ),
    }
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 is not None:
        require(digest == EXPECTED_LEDGER_SHA256,
                "normal/transverse Schur ledger changed")
    if return_data:
        return {
            "ledger": ledger,
            "digest": digest,
            "layout": layout,
            "tau": tau,
            "normal_stricts": normal_stricts,
            "transverse_pivots": transverse_pivots,
            "remaining_rows": remaining_rows,
            "pure_stricts": pure_stricts,
            "local_variables": local_variables,
            "pivots": pivots,
        }
    return ledger, digest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--singular", type=Path)
    parser.add_argument("--characteristic", type=int, default=0)
    arguments = parser.parse_args()
    ledger, digest = audit(arguments.singular, arguments.characteristic)
    print(json.dumps(ledger, indent=2, sort_keys=True))
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
