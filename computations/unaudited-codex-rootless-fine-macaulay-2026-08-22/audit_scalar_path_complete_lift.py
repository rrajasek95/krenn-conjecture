#!/usr/bin/env python3
"""Exact recursive colour-certificate lift along selected scalar edge paths.

Each path replaces a small list of literal cells by ``y_ab + c*t`` and every
other physical cell by ``y_ab``.  The known degree-nine colour multipliers
are lifted recursively against the exact colour-only X5 ideal.  Homogeneity
forces correction degree d to have y-degree 9-d; consequently orders 10 and
11 are terminal guards (two are needed when a source row has t-degree two).

This proves identities only on the listed one-parameter physical slices.
It is evidence for, not a substitute for, a multivariate formal-lifting
theorem in the full edge-deviation ideal.
"""

from collections import defaultdict
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from audit_colour_only_hamming_certificate import (
    EXPECTED_ACTIVE,
    VARIABLES,
    build_generators,
    polynomial,
    run_certificate,
)
from audit_first_edge_deviation_lift import literal_target, literal_word


RESULTS = HERE / "results_scalar_path_complete_lift.json"
DEFAULT_PATHS = {
    "adjacent_triangle_00": (((0, 1, 0, 0), 1), ((0, 2, 0, 0), 1)),
    "disjoint_cone_00_11": (((0, 1, 0, 0), 1), ((2, 3, 1, 1), 1)),
    "triangle_cap_01_22": (((0, 1, 0, 1), 1), ((6, 7, 2, 2), 1)),
    "cross_disjoint_weighted": (((0, 3, 0, 1), 1), ((1, 4, 1, 2), 2)),
    "three_disjoint_mixed": (
        ((0, 1, 0, 0), 1), ((2, 3, 1, 1), 2), ((4, 5, 1, 2), 3),
    ),
    "four_matching_mixed": (
        ((0, 1, 0, 0), 1), ((2, 3, 1, 1), 2),
        ((4, 5, 1, 2), 3), ((6, 7, 2, 2), 5),
    ),
}
DENSE_ALL_CELLS = tuple(
    ((u, v, a, b), 1 + ((edge_index * 9 + 3 * a + b) % 5))
    for edge_index, (u, v) in enumerate(
        (edge for u in range(8) for edge in ((u, v) for v in range(u + 1, 8)))
    )
    for a in range(3) for b in range(3)
)
ALL_PATHS = {**DEFAULT_PATHS, "dense_all_cells": DENSE_ALL_CELLS}


def path_expansion(poly, path):
    selected = dict(path)
    out = defaultdict(lambda: defaultdict(int))
    for term, coefficient in poly.items():
        base = [0] * 9
        for _, _, a, b in term:
            base[3 * a + b] += 1
        states = {(0, tuple(base)): coefficient}
        for cell in term:
            scalar = selected.get(cell)
            if scalar is None:
                continue
            index = 3 * cell[2] + cell[3]
            updated = defaultdict(int)
            for (degree, key), value in states.items():
                updated[(degree, key)] += value
                shifted = list(key)
                shifted[index] -= 1
                updated[(degree + 1, tuple(shifted))] += value * scalar
            states = {key: value for key, value in updated.items() if value}
        for (degree, key), value in states.items():
            out[degree][key] += value
    return {
        degree: {key: value for key, value in terms.items() if value}
        for degree, terms in out.items()
        if any(terms.values())
    }


def run_path(path, generators, multipliers, target):
    words = [word for word, _ in generators]
    projected = [poly for _, poly in generators]
    literal_rows = [literal_word(word) for word in words]
    target_expansion = path_expansion(target, path)
    row_expansions = [path_expansion(row, path) for row in literal_rows]
    max_row_order = max(max(expansion, default=0) for expansion in row_expansions)
    assert max_row_order <= len(path)

    source = [f"ring r=0,({','.join(VARIABLES)}),dp;", "option(redSB);"]
    source.append("ideal I=" + ",".join(polynomial(poly) for poly in projected) + ";")
    source.append("ideal G=std(I);")
    source.append("int k;")
    for order in range(1, max_row_order + 1):
        entries = [
            polynomial(expansion.get(order, {}), signed_coefficients=True)
            for expansion in row_expansions
        ]
        source.append(f"ideal D{order}=" + ",".join(entries) + ";")

    source.append("matrix M0[size(I)][1];")
    word_to_index = {"".join(map(str, word)): i + 1 for i, word in enumerate(words)}
    for word in sorted(EXPECTED_ACTIVE):
        source.append(f"M0[{word_to_index[word]},1]={multipliers[word]};")
    source.append('print("BEGIN_ORDERS");')
    terminal_order = 9 + max_row_order
    for order in range(1, terminal_order + 1):
        source.append(
            f"poly O{order}=" + polynomial(
                target_expansion.get(order, {}), signed_coefficients=True
            ) + ";"
        )
        for row_order in range(1, min(order, max_row_order) + 1):
            source.append(
                f"for(k=1;k<=size(I);k++){{O{order}=O{order}"
                f"-D{row_order}[k]*M{order - row_order}[k,1];}}"
            )
        source.append(f"poly R{order}=reduce(O{order},G);")
        source.append(
            f'if(R{order}!=0){{print("FAIL_ORDER={order}");print(string(R{order}));quit;}}'
        )
        source.append(f"matrix M{order}[size(I)][1];")
        if order <= 9:
            expected_degree = 9 - order
            source.append(f"if(O{order}!=0){{M{order}=lift(I,ideal(O{order}));}}")
            if expected_degree == 0:
                source.append(
                    f"for(k=1;k<=size(I);k++){{M{order}[k,1]=jet(M{order}[k,1],0);}}"
                )
            else:
                source.append(
                    f"for(k=1;k<=size(I);k++){{M{order}[k,1]="
                    f"jet(M{order}[k,1],{expected_degree})"
                    f"-jet(M{order}[k,1],{expected_degree - 1});}}"
                )
            source.append(
                f"if(matrix(I)*M{order}-matrix(ideal(O{order}))!=0)"
                f'{{print("HOMOGENEOUS_LIFT_FAILED={order}");'
                f'print("ODEG="+string(deg(O{order})));'
                f'print(matrix(I)*M{order}-matrix(ideal(O{order})));quit;}}'
            )
        else:
            source.append(
                f'if(O{order}!=0){{print("POST_HOMOGENEITY_TAIL={order}");quit;}}'
            )
        source.append(
            f'if(O{order}==0){{print("ORDER={order},OZERO=1");}}'
            f'else{{print("ORDER={order},OZERO=0");}}'
        )
    source.extend(['print("END_ORDERS");', "quit;"])

    with tempfile.TemporaryDirectory(prefix="krenn-scalar-path-lift-") as directory:
        script = Path(directory) / "path_lift.sing"
        script.write_text("\n".join(source))
        completed = subprocess.run(
            ["Singular", "-q", str(script)],
            text=True,
            capture_output=True,
            timeout=120,
            check=False,
            stdin=subprocess.DEVNULL,
        )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr + completed.stdout[-6000:])
    if "   ?" in completed.stdout:
        raise RuntimeError("Singular reported an internal script error:\n" + completed.stdout[-8000:])
    orders_text = completed.stdout.split("BEGIN_ORDERS\n", 1)[1].split(
        "\nEND_ORDERS", 1
    )[0]
    order_rows = [line for line in orders_text.splitlines() if line.startswith("ORDER=")]
    parsed = {}
    for line in order_rows:
        fields = dict(item.split("=", 1) for item in line.split(","))
        parsed[fields["ORDER"]] = {
            "zero_obstruction": bool(int(fields["OZERO"])),
        }
    if any(str(order) not in parsed for order in range(1, terminal_order + 1)):
        raise RuntimeError("missing order ledger:\n" + completed.stdout[-6000:])
    terminal = [not parsed[str(order)]["zero_obstruction"]
                for order in range(10, terminal_order + 1)]
    return {
        "max_target_order": max(target_expansion),
        "max_source_row_order": max_row_order,
        "terminal_order": terminal_order,
        "terminal_corrections_nonzero": terminal,
        "correction_profile": parsed,
        "stdout_sha256": hashlib.sha256(completed.stdout.encode()).hexdigest(),
    }


def run_audit(paths, closure22=False):
    certificate = run_certificate()
    all_generators = build_generators()
    if closure22:
        closure_words = json.loads(
            (HERE / "results_second_order_lift_support.json").read_text()
        )["combined_closure_words"]
        generator_map = {
            "".join(map(str, word)): (word, poly)
            for word, poly in all_generators
        }
        generators = [generator_map[word] for word in closure_words]
    else:
        generators = all_generators
    target = literal_target()
    path_results = {
        name: run_path(path, generators, certificate["active_multipliers"], target)
        for name, path in paths.items()
    }
    terminal = [
        value for result in path_results.values()
        for value in result["terminal_corrections_nonzero"]
    ]
    return {
        "status": (
            ("PASS closure22 polynomial lifts on every selected scalar path"
             if closure22 else "PASS exact polynomial lifts on every selected scalar path")
            if not any(terminal) else
            "NONTERMINAL scalar-path recursive lift"
        ),
        "paths": {
            name: [list(cell) + [scalar] for cell, scalar in path]
            for name, path in paths.items()
        },
        "path_results": path_results,
        "source_rows": len(generators),
        "scope": (
            "The identities are exact on the listed one-parameter physical "
            "slices. They do not prove a simultaneous multivariate lift or "
            "membership in the full decorated X5 ideal."
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", choices=tuple(ALL_PATHS))
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--check-results", action="store_true")
    parser.add_argument("--closure22", action="store_true")
    args = parser.parse_args()
    paths = ({args.path: ALL_PATHS[args.path]} if args.path else DEFAULT_PATHS)
    result = run_audit(paths, args.closure22)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write_results:
        if args.path or args.closure22:
            raise RuntimeError("refusing to store a single-path run")
        RESULTS.write_text(text)
    if args.check_results and RESULTS.read_text() != text:
        raise RuntimeError("stored scalar-path lift result changed")
    print(text, end="")


if __name__ == "__main__":
    main()
