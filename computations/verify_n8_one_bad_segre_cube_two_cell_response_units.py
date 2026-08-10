#!/usr/bin/env python3
"""Exclude the four proper Segre two-cell top packets by the responses.

The proper top packets from ``af4c340`` add the cells 10 and 20 on one
physical edge 0k.  For each packet this checker constructs all four literal
one-bad response tensors with arbitrary endpoint-star forms.  An exact top
source lift kills every 11 and 22 cell.  Composing those lifts with either
pure diagonal response row reconstructs the unit 1.
"""

from __future__ import annotations

from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import itertools
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
DEPENDENCY = (
    "computations/"
    "verify_n8_one_bad_segre_cube_pinned_lift_critical_pairs.py"
)
DEPENDENCY_SHA256 = (
    "36c32de4ccc2cd3b3c1d56a97a138549a130e9dee7bfe989574b9fa4656d8658"
)
PACKETS = (
    ("02:10", "02:20"),
    ("03:10", "03:20"),
    ("04:10", "04:20"),
    ("05:10", "05:20"),
)
TOP_BASIS_SIZE = {
    "02:10+02:20": 70,
    "03:10+03:20": 70,
    "04:10+04:20": 80,
    "05:10+05:20": 75,
}
EXPECTED = {
    "02:10+02:20": {
        "lift_11_sha256":
            "bdbc00232c4902e4be5e89dcf9f1267ea9f245ca5e72dabe9a8a21655355edc5",
        "lift_22_sha256":
            "848d8d5f9edaf512cb3d460dde9fd109f0a29019d0a76fff431efc5bea76ac53",
        "active_11": 26,
        "active_22": 22,
    },
    "03:10+03:20": {
        "lift_11_sha256":
            "f9bce675a111269d69fa6c9a0f5f572a2556c157d17157b1df8b415cf22ce700",
        "lift_22_sha256":
            "41f9e2aac61333fd70f7b9cf72be21639b0090d6e301a8571bbd0260d794c86a",
        "active_11": 28,
        "active_22": 38,
    },
    "04:10+04:20": {
        "lift_11_sha256":
            "aa5fb636ccc070517025792a501af4982234ca69ec90dd02ba7ebae0dab261c1",
        "lift_22_sha256":
            "23b0ba484b9b2759ab06e37f2622489901d3bce5a8236986ccc6b13bf45a86bf",
        "active_11": 28,
        "active_22": 25,
    },
    "05:10+05:20": {
        "lift_11_sha256":
            "eca4d73a05270b94d5554ae25330a5f2807f9c6ab0b1ae6289bb6b5766f87c61",
        "lift_22_sha256":
            "5cb0d2b9891be78dd833542ade33a50a4bccc0c12a129c1e73e97f4f0e2ae548",
        "active_11": 27,
        "active_22": 28,
    },
}
EXPECTED_LEDGER_SHA256 = (
    "8b08d14efe95f1e1f604a0463ee699fe33715f9cefefb5f6b87fa476866fc29d"
)

STAR_DATA = {
    "11": (1, 47, 1, 53, (1,) * 6),
    "12": (1, 47, 2, 65, None),
    "21": (2, 59, 1, 53, None),
    "22": (2, 59, 2, 65, (2,) * 6),
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load_dependency():
    path = ROOT / DEPENDENCY
    actual = sha256(path.read_bytes()).hexdigest()
    require(actual == DEPENDENCY_SHA256,
            f"dependency changed: {DEPENDENCY}: {actual}")
    spec = spec_from_file_location("critical_pairs", path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def perfect_matchings(vertices):
    vertices = tuple(sorted(vertices))
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index, second in enumerate(vertices[1:], 1):
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


def response_rows(first_variation, support, response):
    p_colour, p_start, s_colour, s_start, target_word = STAR_DATA[response]
    rows = {}
    for word in itertools.product(range(3), repeat=6):
        terms = []
        for p_site in range(6):
            if word[p_site] != p_colour:
                continue
            for s_site in range(6):
                if s_site == p_site or word[s_site] != s_colour:
                    continue
                residual = tuple(site for site in range(6)
                                 if site not in (p_site, s_site))
                for matching in perfect_matchings(residual):
                    cells = tuple(
                        (edge, (word[edge[0]], word[edge[1]]))
                        for edge in matching
                    )
                    if not all(cell in support for cell in cells):
                        continue
                    terms.append(first_variation.poly_product((
                        first_variation.poly_variable(p_start + p_site),
                        first_variation.poly_variable(s_start + s_site),
                        *(support[cell] for cell in cells),
                    )))
        polynomial = first_variation.poly_add(*terms)
        if target_word is not None and word == target_word:
            polynomial = first_variation.poly_add(
                polynomial, first_variation.poly_constant(-1)
            )
        if polynomial:
            rows["".join(map(str, word))] = polynomial
    return rows


def singular_program(critical_pairs, first_variation, top_rows, responses):
    variables = ",".join(f"x{index}" for index in range(71))
    code = f"ring r=0,({variables}),dp; option(redSB);\n"
    code += "ideal I=" + critical_pairs.ideal_expression(top_rows) + ";\n"
    code += "ideal G=std(I);\n"
    code += "int j;\n"
    for index in range(15, 45):
        code += (
            f"if(reduce(x{index},G)!=0)"
            f"{{ print(\"MISSING_DIAGONAL x{index}\"); }}\n"
        )

    for response, target in (("11", "111111"), ("22", "222222")):
        diagonal_polynomial = first_variation.poly_add(
            responses[response][target], first_variation.poly_constant(1)
        )
        require(len(diagonal_polynomial) == 90,
                f"the pure {response} response monomial count changed")
        diagonal = critical_pairs.singular_polynomial(diagonal_polynomial)
        code += f"poly D{response}={diagonal};\n"
        code += f"matrix U{response}=lift(I,ideal(D{response}));\n"
        code += (
            f"if((matrix(I)*U{response})[1,1]-D{response}!=0)"
            f"{{ print(\"UNIT_{response}_FAILED\"); }}\n"
        )
        code += (
            f"if((matrix(I)*U{response})[1,1]-(D{response}-1)!=1)"
            f"{{ print(\"RESPONSE_UNIT_{response}_FAILED\"); }}\n"
        )
        code += f"int nz{response}=0;\n"
        code += (
            f"for(j=1;j<=nrows(U{response});j++)"
            f"{{ if(U{response}[j,1]!=0){{ nz{response}=nz{response}+1; }} }}\n"
        )
        code += f"print(\"ACTIVE_{response}\"); print(nz{response});\n"
        code += (
            f"print(\"BEGIN_LIFT_{response}\"); print(U{response}); "
            f"print(\"END_LIFT_{response}\");\n"
        )
    code += "quit;\n"
    return code


def marker_value(output, marker):
    lines = output.splitlines()
    return lines[lines.index(marker) + 1]


def run_packet(critical_pairs, first_variation, source, edges, base, pair):
    key = "+".join(pair)
    support = dict(base)
    support[critical_pairs.parse_cell(pair[0])] = (
        first_variation.poly_variable(45)
    )
    support[critical_pairs.parse_cell(pair[1])] = (
        first_variation.poly_variable(46)
    )
    top_rows = critical_pairs.coefficient_rows(
        first_variation, source, support
    )
    responses = {
        name: response_rows(first_variation, support, name)
        for name in STAR_DATA
    }
    require("111111" in responses["11"] and
            "222222" in responses["22"],
            f"a diagonal target row disappeared for {key}")
    require("111111" not in responses["12"] and
            "222222" not in responses["21"],
            f"a crossed response acquired a diagonal target for {key}")

    program = singular_program(
        critical_pairs, first_variation, top_rows, responses
    )
    result = subprocess.run(
        ("/usr/local/bin/Singular", "-q"),
        input=program,
        text=True,
        capture_output=True,
        check=False,
        timeout=120,
    )
    require(result.returncode == 0,
            f"Singular failed for {key}: {result.stderr or result.stdout}")
    for failure in (
        "MISSING_DIAGONAL", "UNIT_11_FAILED", "UNIT_22_FAILED",
        "RESPONSE_UNIT_11_FAILED", "RESPONSE_UNIT_22_FAILED",
    ):
        require(failure not in result.stdout,
                f"{failure} on {key}: {result.stdout}")

    audit = {
        "top_source_rows": len(top_rows),
        "top_basis_size": TOP_BASIS_SIZE[key],
        "response_rows": {name: len(rows)
                          for name, rows in responses.items()},
        "response_terms": {
            name: sum(len(polynomial) for polynomial in rows.values())
            for name, rows in responses.items()
        },
        "pure_diagonal_source_monomials": {"11": 90, "22": 90},
        "top_forces_zero": list(range(15, 45)),
    }
    for response in ("11", "22"):
        active = int(marker_value(result.stdout, f"ACTIVE_{response}"))
        lift = result.stdout.split(
            f"BEGIN_LIFT_{response}\n", 1
        )[1].split(f"\nEND_LIFT_{response}", 1)[0]
        digest = sha256(lift.encode()).hexdigest()
        expected = EXPECTED[key]
        if expected[f"active_{response}"] != -1:
            require(active == expected[f"active_{response}"],
                    f"the {response} lift support changed for {key}")
        if expected[f"lift_{response}_sha256"] != "TO_BE_FILLED":
            require(digest == expected[f"lift_{response}_sha256"],
                    f"the {response} lift changed for {key}: {digest}")
        audit[f"unit_{response}"] = {
            "constant": 1,
            "active_top_rows": active,
            "lift_sha256": digest,
        }
    return audit


def main():
    critical_pairs = load_dependency()
    four_residual, _digest = critical_pairs.load_dependency()
    one_cell = four_residual.load_dependency()
    first_variation = one_cell.load_dependency()
    first_variation.VARIABLE_COUNT = 71
    first_variation.ZERO_EXPONENT = (0,) * 71
    diagonal_unit = first_variation.load_dependency()
    source, edges, _variables, base, _multipliers = first_variation.setup(
        diagonal_unit
    )

    audits = {
        "+".join(pair): run_packet(
            critical_pairs, first_variation, source, edges, base, pair
        )
        for pair in PACKETS
    }
    ledger = {
        "dependency": {"path": DEPENDENCY,
                       "sha256": DEPENDENCY_SHA256},
        "packets": audits,
        "verdict": (
            "all four proper two-cell top packets become unit ideals after "
            "the literal one-bad responses are imposed; each top ideal "
            "already forces all 11 and 22 q-cells to zero, and either "
            "diagonal target response supplies an exact unit lift"
        ),
        "scope": (
            "the four source-labelled packets 0k:10+0k:20 with arbitrary "
            "endpoint-star forms p1,p2,s1,s2; no third q-cell direction is "
            "adjoined and no normalization of general one-bad sources is "
            "claimed"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"two-cell response-unit ledger changed: {digest}")
    print("N=8 Segre-K4 two-cell response units: PASS")
    print("four proper top packets: all response-incompatible")
    print("each packet: independent exact unit lifts from 11 and 22 rows")
    for key, audit in audits.items():
        print(f"{key}: 11 {audit['unit_11']['active_top_rows']} rows "
              f"{audit['unit_11']['lift_sha256']}; "
              f"22 {audit['unit_22']['active_top_rows']} rows "
              f"{audit['unit_22']['lift_sha256']}")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
