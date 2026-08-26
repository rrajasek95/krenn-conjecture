#!/usr/bin/env python3
"""Generic nine-parameter lift for the complete cap-edge block A_67.

Every cell A_67[ab] is replaced by y_ab+t*u_ab, while all other physical
edge cells are identified with y_ab.  The rootless holonomy can contain the
cap edge in each of its three cofactor factors and once in the pure cone, so
this slice tests the full fourth-order repeated-edge dependence.
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
    EXPECTED_ACTIVE, VARIABLES, build_generators, polynomial, run_certificate,
)
from audit_first_edge_deviation_lift import literal_target, literal_word


RESULTS = HERE / "results_symbolic_cap_edge_lift.json"
CLOSURE_RESULTS = HERE / "results_symbolic_cap_edge_lift_closure22.json"
PARAMETERS = tuple(f"u{a}{b}" for a in range(3) for b in range(3))
MARKED = {(6, 7, a, b): 3 * a + b for a in range(3) for b in range(3)}


def expansion(poly):
    out = defaultdict(lambda: defaultdict(int))
    for term, coefficient in poly.items():
        ybase = [0] * 9
        for _, _, a, b in term:
            ybase[3 * a + b] += 1
        states = {(0, tuple(ybase), (0,) * 9): coefficient}
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
        for degree, terms in out.items() if any(terms.values())
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
        words = json.loads(
            (HERE / "results_second_order_lift_support.json").read_text()
        )["combined_closure_words"]
        generator_map = {
            "".join(map(str, word)): (word, poly)
            for word, poly in all_generators
        }
        generators = [generator_map[word] for word in words]
    else:
        generators = all_generators
    words = [word for word, _ in generators]
    projected = [poly for _, poly in generators]
    target_expansion = expansion(literal_target())
    row_expansions = [expansion(literal_word(word)) for word in words]
    max_row_order = max(max(item, default=0) for item in row_expansions)
    assert max_row_order == 1

    source = [
        f"ring r=0,({','.join(PARAMETERS + VARIABLES)}),dp;", "option(redSB);",
        "ideal I=" + ",".join(polynomial(poly) for poly in projected) + ";",
        "ideal G=std(I);", "int k;",
    ]
    source.append(
        "ideal D1=" + ",".join(
            param_polynomial(item.get(1, {})) for item in row_expansions
        ) + ";"
    )
    source.append("matrix M0[size(I)][1];")
    word_to_index = {"".join(map(str, word)): i + 1 for i, word in enumerate(words)}
    for word in sorted(EXPECTED_ACTIVE):
        source.append(f"M0[{word_to_index[word]},1]={certificate['active_multipliers'][word]};")
    source.append('print("BEGIN_ORDERS");')
    for order in range(1, 11):
        source.append(
            f"poly O{order}=" + param_polynomial(target_expansion.get(order, {})) + ";"
        )
        source.append(
            f"for(k=1;k<=size(I);k++){{O{order}=O{order}-D1[k]*M{order-1}[k,1];}}"
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

    with tempfile.TemporaryDirectory(prefix="krenn-symbolic-cap-") as directory:
        script = Path(directory) / "symbolic_cap.sing"
        script.write_text("\n".join(source))
        completed = subprocess.run(
            ["Singular", "-q", str(script)], text=True, capture_output=True,
            timeout=120, check=False, stdin=subprocess.DEVNULL,
        )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr + completed.stdout[-6000:])
    order_text = completed.stdout.split("BEGIN_ORDERS\n", 1)[1].split(
        "\nEND_ORDERS", 1
    )[0]
    profile = {}
    for line in order_text.splitlines():
        if line.startswith("ORDER="):
            fields = dict(item.split("=", 1) for item in line.split(","))
            profile[fields["ORDER"]] = bool(int(fields["OZERO"]))
    if len(profile) != 10:
        raise RuntimeError("incomplete cap-edge order ledger")
    return {
        "status": (
            "PASS closure22 generic polynomial cap-edge lift"
            if closure22 else "PASS generic polynomial cap-edge lift"
        ),
        "source_rows": len(generators),
        "marked_edge": "67",
        "parameter_variables": list(PARAMETERS),
        "max_source_row_order": max_row_order,
        "max_target_order": max(target_expansion),
        "order_obstruction_is_literal_zero": profile,
        "terminal_order_zero": profile["10"],
        "order_ledger_sha256": hashlib.sha256(
            json.dumps(profile, sort_keys=True).encode()
        ).hexdigest(),
        "scope": (
            "This is an exact polynomial identity for arbitrary variation of "
            "the nine cap-edge cells around the physical-edge diagonal. It "
            "does not vary the other 27 edge blocks simultaneously."
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
        raise RuntimeError("stored symbolic-cap result changed")
    print(text, end="")


if __name__ == "__main__":
    main()
