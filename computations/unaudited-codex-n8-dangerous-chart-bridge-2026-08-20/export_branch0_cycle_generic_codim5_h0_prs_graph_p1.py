#!/usr/bin/env python3
"""Exact PRS graph split after a monic hyperplane omitting b1.

The frozen h1 slice contains b1, so substituting its b0 pivot destroys the
linearity of E1*b1+E0.  This exporter instead uses

    h0 = b0 + 3*d1 + 5*d3 + 7*d4 - 11,

whose monic b0 substitution leaves E1 and E0 independent of b1.  On E1 != 0
we then eliminate b1 fraction-free and obtain a genuine three-variable core.
"""

from hashlib import sha256
import json
from pathlib import Path
import re
import sys


_SITE = (Path(sys.executable).parent.parent / "lib" /
         f"python{sys.version_info.major}.{sys.version_info.minor}" /
         "site-packages")
if str(_SITE) not in sys.path:
    sys.path.append(str(_SITE))
from flint import fmpz_mpoly_ctx


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "branch0_cycle_generic_codim5_fourrow_slice1_c8open_p1073741827.msolve"
SOURCE_RESULT = HERE / "results_branch0_cycle_generic_codim5_fourrow_slice1_c8open_export.json"
PRS = HERE / "branch0_cycle_generic_codim5_b1_subresultant_polynomials.json"
PRS_RESULT = HERE / "results_branch0_cycle_generic_codim5_b1_subresultant_chain.json"
OUT_OPEN = HERE / "branch0_cycle_generic_codim5_h0_prs_e1open_3var_p1073741827.msolve"
LABELS_OPEN = HERE / "branch0_cycle_generic_codim5_h0_prs_e1open_3var_labels.json"
OUT_EXCEPTIONAL = HERE / "branch0_cycle_generic_codim5_h0_prs_e1zero_4var_p1073741827.msolve"
LABELS_EXCEPTIONAL = HERE / "branch0_cycle_generic_codim5_h0_prs_e1zero_4var_labels.json"
RESULT = HERE / "results_branch0_cycle_generic_codim5_h0_prs_graph_export.json"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def parse(encoded, ctx):
    names = {name: index for index, name in enumerate(ctx.names())}
    terms = {}
    for raw in re.findall(r"[+-]?[^+-]+", encoded.replace(" ", "")):
        sign = -1 if raw.startswith("-") else 1
        body = raw[1:] if raw[:1] in "+-" else raw
        coefficient = sign
        monomial = [0]*ctx.nvars()
        for factor in body.split("*"):
            if re.fullmatch(r"\d+", factor):
                coefficient *= int(factor)
                continue
            match = re.fullmatch(r"([A-Za-z_][A-Za-z0-9_]*)(?:\^(\d+))?", factor)
            require(match is not None and match.group(1) in names,
                    f"unsupported factor {factor!r}")
            monomial[names[match.group(1)]] += int(match.group(2) or 1)
        key = tuple(monomial)
        terms[key] = terms.get(key, 0)+coefficient
    return ctx.from_dict(terms)


def encode(poly):
    pieces = []
    for monomial, coefficient in sorted(poly.to_dict().items(), reverse=True):
        coefficient = int(coefficient)
        factors = [] if abs(coefficient) == 1 else [str(abs(coefficient))]
        for name, power in zip(poly.context().names(), monomial, strict=True):
            if power:
                factors.append(name if power == 1 else f"{name}^{power}")
        body = "*".join(factors) or "1"
        pieces.append(("-" if coefficient < 0 else ("+" if pieces else ""))
                      + body)
    return "".join(pieces) or "0"


def record(poly):
    primitive = poly.primitive()[1]
    text = encode(primitive)
    return {"terms": len(primitive), "degree": int(primitive.total_degree()),
            "sha256": sha256(text.encode("ascii")).hexdigest()}


def degree_in(poly, variable_index):
    return int(max((monomial[variable_index] for monomial in poly.to_dict()),
                   default=-1))


def fraction_free_b1(poly4, e1, e0, ctx3):
    """Return E1^m*poly4(-E0/E1,d), primitive, with exact degree m."""
    m = degree_in(poly4, 0)
    coefficients = [ctx3.constant(0) for _ in range(m+1)]
    for monomial, coefficient in poly4.to_dict().items():
        k = int(monomial[0])
        coefficients[k] += ctx3.from_dict({tuple(monomial[1:]): coefficient})
    powers_e1 = [ctx3.constant(1)]
    powers_minus_e0 = [ctx3.constant(1)]
    for _ in range(m):
        powers_e1.append(powers_e1[-1]*e1)
        powers_minus_e0.append(powers_minus_e0[-1]*(-e0))
    numerator = ctx3.constant(0)
    for k, coefficient_poly in enumerate(coefficients):
        numerator += coefficient_poly*powers_minus_e0[k]*powers_e1[m-k]
    require(not numerator.is_zero(), "fraction-free graph image vanished")
    return numerator.primitive()[1], m


def write_input(path, variables, rows):
    path.write_text(",".join(variables)+"\n1073741827\n"
                    + ",\n".join(encode(poly) for poly in rows)+"\n")
    body = path.read_text().split("\n", 2)[2]
    require("(" not in body and "**" not in body,
            f"{path.name} strict syntax guard failed")


def main():
    lines = SOURCE.read_text().splitlines()
    encoded_rows = "\n".join(lines[2:]).strip().split(",\n")
    source_result = json.loads(SOURCE_RESULT.read_text())
    require(lines[:2] == ["b0,b1,d1,d3,d4", "1073741827"]
            and len(encoded_rows) == 6
            and source_result["output_sha256"] == sha256(SOURCE.read_bytes()).hexdigest(),
            "one-slice source changed")

    ctx5 = fmpz_mpoly_ctx.get(["b0", "b1", "d1", "d3", "d4"], ordering="lex")
    ctx4 = fmpz_mpoly_ctx.get(["b1", "d1", "d3", "d4"], ordering="lex")
    ctx3 = fmpz_mpoly_ctx.get(["d1", "d3", "d4"], ordering="lex")
    source_rows = [parse(row, ctx5) for row in encoded_rows]
    b0, sb1, sd1, sd3, sd4 = ctx5.gens()
    b1, d1, d3, d4 = ctx4.gens()
    td1, td3, td4 = ctx3.gens()
    b0_image4 = 11-3*d1-5*d3-7*d4
    b0_image3 = 11-3*td1-5*td3-7*td4
    source_images = [poly.compose(b0_image4, b1, d1, d3, d4)
                     for poly in [*source_rows[:4], source_rows[5]]]

    h0 = b0+3*sd1+5*sd3+7*sd4-11
    require(h0.compose(b0_image4, b1, d1, d3, d4).is_zero(),
            "new monic hyperplane did not fire")
    hostile_image4 = 12-3*d1-5*d3-7*d4
    require(h0.compose(hostile_image4, b1, d1, d3, d4).is_one(),
            "hostile hyperplane mutation did not fire")

    payload = json.loads(PRS.read_text())
    prs_result = json.loads(PRS_RESULT.read_text())
    require(prs_result["result_sha256"] ==
            "e37a43363b854e1eeffd4def3dd2ea6fd3805ea9bac80a48b92c8af49ff166f9",
            "audited PRS result changed")
    ctx_parameters = fmpz_mpoly_ctx.get(["b0", "d1", "d3", "d4"], ordering="lex")
    e1_source = parse(payload["E1"], ctx_parameters).primitive()[1]
    e0_source = parse(payload["E0"], ctx_parameters).primitive()[1]
    e1 = e1_source.compose(b0_image3, td1, td3, td4).primitive()[1]
    e0 = e0_source.compose(b0_image3, td1, td3, td4).primitive()[1]
    # This is the representation-critical guard.  The new hyperplane omits b1.
    require(degree_in(e1, 0) >= 0 and degree_in(e0, 0) >= 0,
            "coefficient images vanished")
    relation4 = (e1.compose(d1, d3, d4)*b1
                 + e0.compose(d1, d3, d4)).primitive()[1]
    require(degree_in(relation4, 0) == 1,
            "transformed PRS relation is not linear in b1")

    graph_rows = []
    graph_degrees = []
    for poly in source_images[:4]:
        numerator, b1_degree = fraction_free_b1(poly, e1, e0, ctx3)
        graph_rows.append(numerator)
        graph_degrees.append(b1_degree)
    localizer_numerator, localizer_b1_degree = fraction_free_b1(
        source_images[4], e1, e0, ctx3)
    graph_localizer = (localizer_numerator*e1).primitive()[1]
    graph_output_rows = [*graph_rows, graph_localizer]
    write_input(OUT_OPEN, ["d1", "d3", "d4"], graph_output_rows)
    labels_open = ["P324_h0_PRSgraph", "P851_h0_PRSgraph",
                   "P1342_h0_PRSgraph", "P1846_h0_PRSgraph",
                   "base_C8_times_E1_PRSgraph_saturator"]
    LABELS_OPEN.write_text(json.dumps({"labels": labels_open}, indent=2)+"\n")

    e1_4 = e1.compose(d1, d3, d4)
    e0_4 = e0.compose(d1, d3, d4)
    exceptional_rows = [*source_images[:4], e1_4, e0_4, source_images[4]]
    write_input(OUT_EXCEPTIONAL, ["b1", "d1", "d3", "d4"], exceptional_rows)
    labels_exceptional = ["P324_h0", "P851_h0", "P1342_h0", "P1846_h0",
                          "E1_h0", "E0_h0", "base_C8_h0_saturator"]
    LABELS_EXCEPTIONAL.write_text(
        json.dumps({"labels": labels_exceptional}, indent=2)+"\n")

    gcd_e1_e0 = e1.gcd(e0).primitive()[1]
    d10_source = (b0**2*sb1*sd1*sd4+2*b0**2*sb1*sd3-b0**2*sd1**2*sd4
                  -b0*sb1*sd1*sd4+b0*sb1*sd3*sd4-b0*sd1**2*sd4
                  -b0*sd1*sd3*sd4+2*sb1*sd1*sd4**2+sb1*sd3*sd4
                  +sd1*sd3*sd4)
    d10_h0 = d10_source.compose(b0_image4, b1, d1, d3, d4)
    d10_graph, d10_b1_degree = fraction_free_b1(d10_h0, e1, e0, ctx3)

    result = {
        "status": "AUDITED exact h0/PRS graph and exceptional split export",
        "source": SOURCE.name,
        "source_sha256": sha256(SOURCE.read_bytes()).hexdigest(),
        "prs_payload": PRS.name,
        "prs_payload_sha256": sha256(PRS.read_bytes()).hexdigest(),
        "prs_audit_result_sha256": prs_result["result_sha256"],
        "hyperplane": "b0+3*d1+5*d3+7*d4-11",
        "hyperplane_omits_b1": True,
        "pivot_coefficient": 1,
        "substitution": "b0=11-3*d1-5*d3-7*d4",
        "E1_h0_profile": record(e1),
        "E0_h0_profile": record(e0),
        "E1_h0_b1_degree": 0,
        "E0_h0_b1_degree": 0,
        "PRS_relation_h0_b1_degree": degree_in(relation4, 0),
        "E1_E0_gcd_h0_profile": record(gcd_e1_e0),
        "E1_E0_gcd_h0": encode(gcd_e1_e0) if len(gcd_e1_e0) <= 20 else None,
        "source_image_profiles": [record(poly) for poly in source_images[:4]],
        "source_image_b1_degrees": [degree_in(poly, 0) for poly in source_images[:4]],
        "graph_row_profiles": [record(poly) for poly in graph_rows],
        "graph_row_denominator_powers_E1": graph_degrees,
        "graph_localizer_profile": record(graph_localizer),
        "graph_localizer_denominator_power_E1_before_extra_live_factor":
            localizer_b1_degree,
        "D10_graph": encode(d10_graph),
        "D10_graph_profile": record(d10_graph),
        "D10_graph_denominator_power_E1": d10_b1_degree,
        "E1_open_input": OUT_OPEN.name,
        "E1_open_input_sha256": sha256(OUT_OPEN.read_bytes()).hexdigest(),
        "E1_open_input_bytes": OUT_OPEN.stat().st_size,
        "E1_open_labels": LABELS_OPEN.name,
        "exceptional_input": OUT_EXCEPTIONAL.name,
        "exceptional_input_sha256": sha256(OUT_EXCEPTIONAL.read_bytes()).hexdigest(),
        "exceptional_input_bytes": OUT_EXCEPTIONAL.stat().st_size,
        "exceptional_labels": LABELS_EXCEPTIONAL.name,
        "exceptional_profile_only": True,
        "hostile_constant_mutation_fired": True,
        "scope": (
            "Exact quotient by the new monic h0, followed on E1!=0 by the "
            "fraction-free graph b1=-E0/E1.  The graph saturator is the "
            "fraction-free image of the unchanged base*C8 product times E1. "
            "The E1=E0 exceptional branch retains b1 and is not solved. "
            "The modular p1 gate is discovery only."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode()).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print("h0 PRS graph split export: PASS")
    print("degree guard E1/E0/relation: 0 0", result["PRS_relation_h0_b1_degree"])
    print("E1/E0/gcd profiles:", result["E1_h0_profile"],
          result["E0_h0_profile"], result["E1_E0_gcd_h0_profile"])
    print("graph profiles:", result["graph_row_profiles"],
          result["graph_localizer_profile"])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
