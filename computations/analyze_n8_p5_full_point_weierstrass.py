#!/usr/bin/env python3
"""Exact rational-point reconnaissance for the full P5 Weierstrass quotient."""

from fractions import Fraction
from hashlib import sha256
import argparse
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


G = load_module(
    "n8_p5_schur_g_for_full_point",
    "verify_n8_p5_schur_generic_L_g_center.py",
)
F2 = G.F2
SCHUR = G.F2.SCHUR
REES = G.REES
P5 = G.P5
QQ = Fraction

EXPECTED_STD_SELECTED_EXPORT_SHA256 = (
    "55a2912b8800d0b3b426dd5f55a7c394b5120e10b81e745883d03067eb370e09"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def add(target, source, scale=QQ(1)):
    REES.add(target, source, scale)


def multiply(left, right):
    return REES.multiply(left, right)


def partial_evaluate(source, values, retained):
    answer = {}
    for monomial, coefficient in source.items():
        output = []
        value = coefficient
        for variable in monomial:
            if variable in retained:
                output.append(variable)
            else:
                require(variable in values,
                        f"point evaluation missed variable {variable}")
                value *= values[variable]
        output = tuple(sorted(output))
        answer[output] = answer.get(output, QQ(0)) + value
        if not answer[output]:
            answer.pop(output)
    return answer


def affine_root(source, variable):
    constant = source.get((), QQ(0))
    slope = source.get((variable,), QQ(0))
    require(set(source).issubset({(), (variable,)}),
            f"relation is not affine in variable {variable}")
    require(slope, f"relation has zero slope in variable {variable}")
    return -constant / slope


def exact_point(center):
    layout = center["layout"]
    values = {
        variable: QQ(parameter + 2)
        for parameter, variable in layout["a"].items()
    }
    values[layout["a"][46]] = (
        values[layout["a"][9]] * values[layout["a"][25]]
        / values[layout["a"][11]]
    )
    first_bend = center["first_bend"]
    second_bend = center["second_bend"]
    first_at_point = partial_evaluate(
        center["first_relation"], values, {first_bend}
    )
    values[first_bend] = affine_root(first_at_point, first_bend)
    second_at_point = partial_evaluate(
        center["second_relation"], values, {second_bend}
    )
    values[second_bend] = affine_root(second_at_point, second_bend)
    require(values[layout["a"][44]] + values[layout["a"][45]],
            "point left the b chart")
    return values


def third_bend_root(layout, point, first, second):
    a = layout["a"]
    z = lambda parameter: point[a[parameter]]
    return (
        z(0) * z(26) * z(30) * z(54)
        - z(26) * z(30) ** 2 * z(54)
        + z(0) * z(7) * z(46) * z(54)
        - z(7) * z(24) * z(46) * z(54)
        - z(7) * z(30) * z(46) * z(54)
        - z(0) * z(26) * z(52) * z(54)
        + z(26) * z(30) * z(52) * z(54)
        + z(7) * z(46) * z(52) * z(54)
        + z(7) * z(26) * z(54) ** 2
        - first * z(0) * z(52)
        + first * z(7) * z(54)
        - second * z(0)
        - second * z(52)
    )


def arc_powers(tau, r_variable, z46, first, second, maximum=4):
    arc = {
        (): z46,
        (tau,): first,
        (tau, tau): second,
        (tau, tau, tau, r_variable): QQ(1),
    }
    powers = [{(): QQ(1)}]
    for _degree in range(maximum):
        powers.append(multiply(powers[-1], arc))
    return powers


def point_arc_substitute(source, layout, point, r_variable, powers):
    tau = layout["tau"]
    z46_variable = layout["a"][46]
    base_variables = frozenset(layout["a"].values())
    answer = {}
    for monomial, coefficient in source.items():
        z46_degree = monomial.count(z46_variable)
        require(z46_degree < len(powers), "z46 arc degree bound changed")
        scalar = coefficient
        local = []
        for variable in monomial:
            if variable == z46_variable:
                continue
            if variable in base_variables:
                scalar *= point[variable]
            else:
                local.append(variable)
        for arc_monomial, arc_coefficient in powers[z46_degree].items():
            output = tuple(sorted(tuple(local) + arc_monomial))
            answer[output] = (
                answer.get(output, QQ(0)) + scalar * arc_coefficient
            )
            if not answer[output]:
                answer.pop(output)
    return answer


def singular_names(layout, r_variable):
    names = [f"x{index}" for index in range(r_variable + 1)]
    names[layout["tau"]] = "tau"
    for parameter, variable in layout["n"].items():
        names[variable] = f"n{parameter}"
    for pivot, variable in layout["y"].items():
        names[variable] = f"y{pivot}"
    names[r_variable] = "r3"
    return names


def export(path, mode="reduce"):
    center = F2.audit(return_data=True)
    schur = SCHUR.audit(return_data=True)
    layout = schur["layout"]
    require(layout == center["layout"], "Schur and center layouts diverged")
    point = exact_point(center)
    r_variable = layout["variable_count"]
    powers = arc_powers(
        layout["tau"], r_variable,
        point[layout["a"][46]],
        point[center["first_bend"]],
        point[center["second_bend"]],
    )

    groups = {
        "N": schur["normal_stricts"],
        "P": schur["transverse_pivots"],
        "M": schur["remaining_rows"],
        "H": schur["pure_stricts"],
    }
    source_z46_degrees = {
        label: max(
            monomial.count(layout["a"][46])
            for source in sources for monomial in source
        )
        for label, sources in groups.items()
    }
    transformed = {
        label: [
            point_arc_substitute(source, layout, point, r_variable, powers)
            for source in sources
        ]
        for label, sources in groups.items()
    }
    require(len(transformed["N"]) == 196
            and len(transformed["P"]) == 11
            and len(transformed["M"]) == 28
            and len(transformed["H"]) == 2,
            "full point family sizes changed")
    names = singular_names(layout, r_variable)
    local = [names[variable] for variable in layout["y"].values()]
    local += [names[variable] for variable in layout["n"].values()]
    local.append("tau")
    ring_order = local + ["r3"]
    encode = REES.AMBIENT.singular_polynomial
    digest = sha256()
    with Path(path).open("w") as output:
        def write(value):
            output.write(value)
            digest.update(value.encode())

        write(
            "// Exact rational generic-L point; r3 retained.\n"
            f"ring R=0,({','.join(ring_order)}),(ds(208),dp(1));\n"
        )
        for label in ("N", "P"):
            write(f"ideal {label}=\n")
            for index, source in enumerate(transformed[label]):
                if index:
                    write(",\n")
                write(encode(source, names))
            write(";\n")
        write("ideal S=N,P;\nint clock=timer;\nideal GS=std(S);\n")
        write('"STD207",size(GS),timer-clock;\n')
        remaining_parameters = [
            row + 1 for row in range(39) if row not in set(P5.B_PIVOT_ROWS)
        ]
        indexed_remaining = dict(zip(remaining_parameters, transformed["M"]))
        reduction_order = [30, 33] + [
            row for row in remaining_parameters if row not in {30, 33}
        ]
        if mode == "reduce":
            for row in reduction_order:
                source = indexed_remaining[row]
                write(f"poly M{row}={encode(source, names)};\n")
                write(f"clock=timer; poly R{row}=reduce(M{row},GS);\n")
                write(f'"MIXED",{row},size(R{row}),timer-clock;\n')
            for colour, source in enumerate(transformed["H"]):
                write(f"poly H{colour}={encode(source, names)};\n")
                write(f"clock=timer; poly RH{colour}=reduce(H{colour},GS);\n")
                write(f'"PURE",{colour},size(RH{colour}),timer-clock;\n')
        else:
            require(mode == "std-selected", f"unknown export mode {mode}")
            write(f"poly M30={encode(indexed_remaining[30], names)};\n")
            write("clock=timer; ideal T=std(GS,M30);\n")
            write(
                '"STDSELECTED",size(T),timer-clock,'
                'lead(T[size(T)-1]),lead(T[size(T)]);\n'
            )
            write(
                "for (int ii=1; ii<=size(T); ii++) { "
                'if (deg(lead(T[ii]))>1) { "HIGHLEAD",ii,lead(T[ii]); } }\n'
            )
        write("quit;\n")
    r0 = third_bend_root(
        layout,
        point,
        point[center["first_bend"]],
        point[center["second_bend"]],
    )
    summary = {
        "point": {
            "z46": str(point[layout["a"][46]]),
            "s": str(point[center["first_bend"]]),
            "t": str(point[center["second_bend"]]),
            "r0": str(r0),
        },
        "transformed_terms": {
            label: sum(map(len, sources))
            for label, sources in transformed.items()
        },
        "maximum_terms": {
            label: max(map(len, sources))
            for label, sources in transformed.items()
        },
        "maximum_r3_degrees": {
            label: max(
                monomial.count(r_variable)
                for source in sources for monomial in source
            )
            for label, sources in transformed.items()
        },
        "source_z46_degrees": source_z46_degrees,
        "selected_M30_r3_degree": max(
            monomial.count(r_variable)
            for monomial in transformed["M"][
                [
                    row + 1 for row in range(39)
                    if row not in set(P5.B_PIVOT_ROWS)
                ].index(30)
            ]
        ),
        "export_sha256": digest.hexdigest(),
        "export_bytes": Path(path).stat().st_size,
        "mode": mode,
    }
    if mode == "std-selected" and EXPECTED_STD_SELECTED_EXPORT_SHA256:
        require(
            summary["export_sha256"] == EXPECTED_STD_SELECTED_EXPORT_SHA256,
            "full point selected standard-basis export changed",
        )
    return summary


def run_singular(path):
    completed = subprocess.run(
        ["/usr/local/bin/Singular", "-q", str(path)],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=180,
        check=False,
    )
    require(completed.returncode == 0,
            "full point selected standard-basis run failed")
    lines = completed.stdout.splitlines()
    require(len(lines) == 3, "selected standard-basis output shape changed")
    standard = lines[0].split()
    selected = lines[1].split()
    high = lines[2].split()
    require(standard[:2] == ["STD207", "207"],
            "full point 207-row basis changed")
    require(selected[:2] == ["STDSELECTED", "209"],
            "selected full row standard-basis size changed")
    require(selected[3:] == [
        "186*n23",
        "154714580602170274968750000000*tau^6*r3",
    ], "selected full row endpoint leads changed")
    require(high == [
        "HIGHLEAD", "209",
        "154714580602170274968750000000*tau^6*r3",
    ], "selected full row no longer has one sixth-saturated high lead")
    return {
        "std207_rows": 207,
        "std_selected_rows": 209,
        "higher_degree_leads": 1,
        "higher_degree_lead": "tau^6*r3",
        "higher_degree_lead_coefficient": (
            "154714580602170274968750000000"
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    parser.add_argument(
        "--mode", choices=("reduce", "std-selected"), default="std-selected"
    )
    parser.add_argument("--run-singular", action="store_true")
    arguments = parser.parse_args()
    summary = export(arguments.path, arguments.mode)
    if arguments.run_singular:
        require(arguments.mode == "std-selected",
                "only the bounded selected mode may be run automatically")
        summary["singular_certificate"] = run_singular(arguments.path)
    encoded = json.dumps(summary, sort_keys=True, separators=(",", ":"))
    print(json.dumps(summary, indent=2, sort_keys=True))
    print(f"ledger_sha256={sha256(encoded.encode()).hexdigest()}")


if __name__ == "__main__":
    main()
