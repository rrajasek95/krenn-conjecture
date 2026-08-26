#!/usr/bin/env python3
"""Generic four-parameter lift on one labelled perfect-matching slice.

The marked cells are 01:00, 23:11, 45:12, and 67:22.  They are replaced by
``y_ab + t*u_i`` with algebraically independent polynomial variables u_i.
Unlike numeric line tests, reduction in Q[u1,..,u4,y00,..,y22] proves every
coefficient identity simultaneously and introduces no rational-function
denominators.  This remains a four-cell slice, not the full 252-cell lift.
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


RESULTS = HERE / "results_symbolic_matching_path_lift.json"
CLOSURE_RESULTS = HERE / "results_symbolic_matching_path_lift_closure22.json"
PARAMETERS = ("u1", "u2", "u3", "u4")
MARKED = {
    (0, 1, 0, 0): 0,
    (2, 3, 1, 1): 1,
    (4, 5, 1, 2): 2,
    (6, 7, 2, 2): 3,
}


def expansion(poly):
    out = defaultdict(lambda: defaultdict(int))
    for term, coefficient in poly.items():
        ybase = [0] * 9
        for _, _, a, b in term:
            ybase[3 * a + b] += 1
        states = {(0, tuple(ybase), (0, 0, 0, 0)): coefficient}
        for cell in term:
            parameter = MARKED.get(cell)
            if parameter is None:
                continue
            updated = defaultdict(int)
            for (degree, ykey, ukey), value in states.items():
                updated[(degree, ykey, ukey)] += value
                shifted_y = list(ykey)
                shifted_y[3 * cell[2] + cell[3]] -= 1
                shifted_u = list(ukey)
                shifted_u[parameter] += 1
                updated[(degree + 1, tuple(shifted_y), tuple(shifted_u))] += value
            states = {key: value for key, value in updated.items() if value}
        for (degree, ykey, ukey), value in states.items():
            out[degree][(ukey, ykey)] += value
    return {
        degree: {key: value for key, value in terms.items() if value}
        for degree, terms in out.items()
        if any(terms.values())
    }


def param_polynomial(poly):
    pieces = []
    for (ukey, ykey), coefficient in sorted(poly.items()):
        factors = []
        for variable, power in zip(PARAMETERS + VARIABLES, ukey + ykey):
            if power == 1:
                factors.append(variable)
            elif power:
                factors.append(f"{variable}^{power}")
        monomial = "*".join(factors) or "1"
        if coefficient == 1:
            pieces.append(monomial)
        elif coefficient == -1:
            pieces.append("-" + monomial)
        else:
            pieces.append(f"{coefficient}*{monomial}")
    return ("+".join(pieces) or "0").replace("+-", "-")


def run_audit(closure22=False):
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
    words = [word for word, _ in generators]
    projected = [poly for _, poly in generators]
    target_expansion = expansion(literal_target())
    row_expansions = [expansion(literal_word(word)) for word in words]
    max_row_order = max(max(item, default=0) for item in row_expansions)
    assert 1 <= max_row_order <= 4

    ring_variables = PARAMETERS + VARIABLES
    source = [f"ring r=0,({','.join(ring_variables)}),dp;", "option(redSB);"]
    source.append("ideal I=" + ",".join(polynomial(poly) for poly in projected) + ";")
    source.append("ideal G=std(I);")
    source.append("int k;")
    for order in range(1, max_row_order + 1):
        source.append(
            f"ideal D{order}=" + ",".join(
                param_polynomial(item.get(order, {})) for item in row_expansions
            ) + ";"
        )
    source.append("matrix M0[size(I)][1];")
    word_to_index = {"".join(map(str, word)): i + 1 for i, word in enumerate(words)}
    for word in sorted(EXPECTED_ACTIVE):
        source.append(f"M0[{word_to_index[word]},1]={certificate['active_multipliers'][word]};")
    source.append('print("BEGIN_ORDERS");')
    terminal_order = 9 + max_row_order
    for order in range(1, terminal_order + 1):
        source.append(
            f"poly O{order}=" + param_polynomial(target_expansion.get(order, {})) + ";"
        )
        for row_order in range(1, min(order, max_row_order) + 1):
            source.append(
                f"for(k=1;k<=size(I);k++){{O{order}=O{order}"
                f"-D{row_order}[k]*M{order-row_order}[k,1];}}"
            )
        source.append(f"poly R{order}=reduce(O{order},G);")
        source.append(
            f'if(R{order}!=0){{print("FAIL_ORDER={order}");print(string(R{order}));exit(2);}}'
        )
        source.append(f"matrix M{order}[size(I)][1];")
        source.append(f"if(O{order}!=0){{M{order}=lift(I,ideal(O{order}));}}")
        source.append(
            f'if(O{order}==0){{print("ORDER={order},OZERO=1");}}'
            f'else{{print("ORDER={order},OZERO=0");}}'
        )
    source.extend(['print("END_ORDERS");', "quit;"])

    with tempfile.TemporaryDirectory(prefix="krenn-symbolic-path-") as directory:
        script = Path(directory) / "symbolic_path.sing"
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
    order_text = completed.stdout.split("BEGIN_ORDERS\n", 1)[1].split(
        "\nEND_ORDERS", 1
    )[0]
    profile = {}
    for line in order_text.splitlines():
        if not line.startswith("ORDER="):
            continue
        fields = dict(item.split("=", 1) for item in line.split(","))
        profile[fields["ORDER"]] = bool(int(fields["OZERO"]))
    if len(profile) != terminal_order:
        raise RuntimeError("incomplete symbolic order ledger")
    terminal_zero = all(
        profile[str(order)] for order in range(10, terminal_order + 1)
    )
    return {
        "status": (
            ("PASS closure22 generic polynomial four-matching-cell lift"
             if closure22 else "PASS generic polynomial four-matching-cell lift")
            if terminal_zero else
            "NONTERMINAL generic polynomial four-matching-cell lift"
        ),
        "marked_cells": [list(cell) for cell in MARKED],
        "source_rows": len(generators),
        "parameter_variables": list(PARAMETERS),
        "max_source_row_order": max_row_order,
        "max_target_order": max(target_expansion),
        "order_obstruction_is_literal_zero": profile,
        "terminal_orders_zero": terminal_zero,
        "stdout_sha256": hashlib.sha256(completed.stdout.encode()).hexdigest(),
        "scope": (
            "This is an exact polynomial identity over Q[u1,u2,u3,u4] on "
            "one four-cell perfect-matching slice. It is not the full "
            "252-direction edge-deviation theorem."
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--check-results", action="store_true")
    parser.add_argument("--closure22", action="store_true")
    args = parser.parse_args()
    result = run_audit(args.closure22)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    results_path = CLOSURE_RESULTS if args.closure22 else RESULTS
    if args.write_results:
        results_path.write_text(text)
    if args.check_results and results_path.read_text() != text:
        raise RuntimeError("stored symbolic-path result changed")
    print(text, end="")


if __name__ == "__main__":
    main()
