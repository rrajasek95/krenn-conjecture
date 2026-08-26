#!/usr/bin/env python3
"""Generic closure22 lift for the complete A_01 and A_67 blocks."""

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


RESULTS = HERE / "results_symbolic_triangle_cap_blocks_lift.json"
TIMEOUT = 120
COEFFICIENT_PARAMETERS = False
PARAMETERS = tuple(
    f"{prefix}{a}{b}" for prefix in ("u", "v")
    for a in range(3) for b in range(3)
)
MARKED = {
    **{(0, 1, a, b): 3 * a + b for a in range(3) for b in range(3)},
    **{(6, 7, a, b): 9 + 3 * a + b for a in range(3) for b in range(3)},
}


def expansion(poly):
    out = defaultdict(lambda: defaultdict(int))
    for term, coefficient in poly.items():
        ybase = [0] * 9
        for _, _, a, b in term:
            ybase[3 * a + b] += 1
        states = {(0, tuple(ybase), (0,) * len(PARAMETERS)): coefficient}
        for cell in term:
            parameter = MARKED.get(cell)
            if parameter is None:
                continue
            updated = defaultdict(int)
            for (degree, ykey, pkey), value in states.items():
                updated[(degree, ykey, pkey)] += value
                shifted_y = list(ykey)
                shifted_y[3 * cell[2] + cell[3]] -= 1
                shifted_p = list(pkey)
                shifted_p[parameter] += 1
                updated[(degree + 1, tuple(shifted_y), tuple(shifted_p))] += value
            states = {key: value for key, value in updated.items() if value}
        for (degree, ykey, pkey), value in states.items():
            out[degree][(pkey, ykey)] += value
    return {
        degree: {key: value for key, value in terms.items() if value}
        for degree, terms in out.items() if any(terms.values())
    }


def param_polynomial(poly):
    pieces = []
    for (pkey, ykey), coefficient in sorted(poly.items()):
        factors = []
        for variable, power in zip(PARAMETERS + VARIABLES, pkey + ykey):
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


def run_audit():
    certificate = run_certificate()
    all_generators = build_generators()
    generator_map = {
        "".join(map(str, word)): (word, poly)
        for word, poly in all_generators
    }
    closure_words = json.loads(
        (HERE / "results_second_order_lift_support.json").read_text()
    )["combined_closure_words"]
    generators = [generator_map[word] for word in closure_words]
    words = [word for word, _ in generators]
    projected = [poly for _, poly in generators]
    target_expansion = expansion(literal_target())
    row_expansions = [expansion(literal_word(word)) for word in words]
    max_row_order = max(max(item, default=0) for item in row_expansions)
    terminal_order = 9 + max_row_order * (2 if COEFFICIENT_PARAMETERS else 1)

    ring_declaration = (
        f"ring r=(0,{','.join(PARAMETERS)}),({','.join(VARIABLES)}),dp;"
        if COEFFICIENT_PARAMETERS else
        f"ring r=0,({','.join(PARAMETERS + VARIABLES)}),dp;"
    )
    source = [
        ring_declaration, "option(redSB);",
        "ideal I=" + ",".join(polynomial(poly) for poly in projected) + ";",
        "ideal G=std(I);", "int k;",
    ]
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
    source.extend([
        'print("END_ORDERS");',
        "int parameter_denominators=0;poly denominator_tmp;number denominator_cf;",
    ])
    for order in range(0, terminal_order + 1):
        source.append(
            f"for(k=1;k<=size(I);k++){{denominator_tmp=M{order}[k,1];"
            "while(denominator_tmp!=0){denominator_cf=leadcoef(denominator_tmp);"
            "if(denominator(denominator_cf)!=1){parameter_denominators++;"
            "print(\"PARAMETER_DENOMINATOR=\"+string(denominator(denominator_cf)));}"
            "denominator_tmp=denominator_tmp-lead(denominator_tmp);}}"
        )
    source.extend([
        'print("PARAMETER_DENOMINATORS="+string(parameter_denominators));',
        "quit;",
    ])
    with tempfile.TemporaryDirectory(prefix="krenn-symbolic-triangle-cap-") as directory:
        script = Path(directory) / "symbolic_triangle_cap.sing"
        script.write_text("\n".join(source))
        completed = subprocess.run(
            ["Singular", "-q", str(script)], text=True, capture_output=True,
            timeout=TIMEOUT, check=False, stdin=subprocess.DEVNULL,
        )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr + completed.stdout[-8000:])
    order_text = completed.stdout.split("BEGIN_ORDERS\n", 1)[1].split(
        "\nEND_ORDERS", 1
    )[0]
    profile = {}
    for line in order_text.splitlines():
        if line.startswith("ORDER="):
            fields = dict(item.split("=", 1) for item in line.split(","))
            profile[fields["ORDER"]] = bool(int(fields["OZERO"]))
    if len(profile) != terminal_order:
        raise RuntimeError("incomplete triangle-cap order ledger")
    parameter_denominators = int(
        completed.stdout.split("PARAMETER_DENOMINATORS=", 1)[1].splitlines()[0]
    )
    denominator_polynomials = sorted(set(
        line.split("=", 1)[1] for line in completed.stdout.splitlines()
        if line.startswith("PARAMETER_DENOMINATOR=")
    ))
    parameter_dependent_denominators = [
        value for value in denominator_polynomials
        if any(character.isalpha() for character in value)
    ]
    terminal_zero = all(
        profile[str(order)]
        for order in range(terminal_order - max_row_order + 1, terminal_order + 1)
    )
    return {
        "status": (
            "PASS closure22 generic polynomial triangle-cap two-block lift"
            if terminal_zero and not parameter_dependent_denominators else
            "NONTERMINAL closure22 triangle-cap two-block lift"
        ),
        "source_rows": len(generators),
        "marked_edges": ["01", "67"],
        "parameter_count": len(PARAMETERS),
        "max_source_row_order": max_row_order,
        "max_target_order": max(target_expansion),
        "terminal_order": terminal_order,
        "order_obstruction_is_literal_zero": profile,
        "terminal_orders_zero": terminal_zero,
        "parameter_denominators": parameter_denominators,
        "unique_parameter_denominators": len(denominator_polynomials),
        "parameter_denominator_polynomials": denominator_polynomials,
        "parameter_dependent_denominators": parameter_dependent_denominators,
        "parameter_dependent_denominator_count": len(
            parameter_dependent_denominators
        ),
        "parameter_denominator_ledger_sha256": hashlib.sha256(
            json.dumps(denominator_polynomials, separators=(",", ":")).encode()
        ).hexdigest(),
        "order_ledger_sha256": hashlib.sha256(
            json.dumps(profile, sort_keys=True).encode()
        ).hexdigest(),
        "scope": (
            "This is exact over 18 independent polynomial parameters for the "
            "complete A01 and A67 blocks. The remaining 26 edge blocks are "
            "still fixed at the physical-edge diagonal."
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--check-results", action="store_true")
    args = parser.parse_args()
    result = run_audit()
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write_results:
        RESULTS.write_text(text)
    if args.check_results and RESULTS.read_text() != text:
        raise RuntimeError("stored symbolic triangle-cap result changed")
    print(text, end="")


if __name__ == "__main__":
    main()
