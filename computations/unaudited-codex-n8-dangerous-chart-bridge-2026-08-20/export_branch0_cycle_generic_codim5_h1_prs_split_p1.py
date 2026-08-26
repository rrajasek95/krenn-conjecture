#!/usr/bin/env python3
"""Export the exact PRS split inside the monic-h1 four-variable quotient."""

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
H1_SOURCE = HERE / "branch0_cycle_generic_codim5_fourrow_h1_sub_c8open_p1073741827.msolve"
H1_RESULT = HERE / "results_branch0_cycle_generic_codim5_fourrow_h1_sub_c8open_export.json"
PRS = HERE / "branch0_cycle_generic_codim5_b1_subresultant_polynomials.json"
OUT_OPEN = HERE / "branch0_cycle_generic_codim5_h1_prs_e1open_p1073741827.msolve"
LABELS_OPEN = HERE / "branch0_cycle_generic_codim5_h1_prs_e1open_labels.json"
OUT_EXCEPTIONAL = HERE / "branch0_cycle_generic_codim5_h1_prs_e1zero_p1073741827.msolve"
LABELS_EXCEPTIONAL = HERE / "branch0_cycle_generic_codim5_h1_prs_e1zero_labels.json"
RESULT = HERE / "results_branch0_cycle_generic_codim5_h1_prs_split_export.json"


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
    return int(max((monomial[variable_index] for monomial in poly.to_dict()), default=-1))


def write_input(path, rows):
    path.write_text("b1,d1,d3,d4\n1073741827\n"
                    + ",\n".join(encode(poly) for poly in rows)+"\n")
    body = path.read_text().split("\n", 2)[2]
    require("(" not in body and "**" not in body,
            f"{path.name} strict syntax guard failed")


def main():
    lines = H1_SOURCE.read_text().splitlines()
    encoded_rows = "\n".join(lines[2:]).strip().split(",\n")
    h1_result = json.loads(H1_RESULT.read_text())
    require(lines[:2] == ["b1,d1,d3,d4", "1073741827"]
            and len(encoded_rows) == 5
            and h1_result["output_sha256"] == sha256(H1_SOURCE.read_bytes()).hexdigest(),
            "monic-h1 source changed")
    ctx4 = fmpz_mpoly_ctx.get(["b1", "d1", "d3", "d4"], ordering="lex")
    h1_rows = [parse(row, ctx4) for row in encoded_rows]

    payload = json.loads(PRS.read_text())
    ctx_parameters = fmpz_mpoly_ctx.get(["b0", "d1", "d3", "d4"], ordering="lex")
    e1 = parse(payload["E1"], ctx_parameters).primitive()[1]
    e0 = parse(payload["E0"], ctx_parameters).primitive()[1]
    b1, d1, d3, d4 = ctx4.gens()
    b0_image = 11-2*b1-3*d1-5*d3-7*d4
    e1_h1 = e1.compose(b0_image, d1, d3, d4).primitive()[1]
    e0_h1 = e0.compose(b0_image, d1, d3, d4).primitive()[1]
    prs_relation = (e1_h1*b1+e0_h1).primitive()[1]
    relation_b1_degree = degree_in(prs_relation, 0)
    e1_b1_degree = degree_in(e1_h1, 0)
    e0_b1_degree = degree_in(e0_h1, 0)
    # The original relation must still be an exact consequence after applying
    # the h1 quotient, even if it is no longer a graph over b1.
    require(not prs_relation.is_zero(), "PRS relation vanished after h1")

    gcd_h1 = e1_h1.gcd(e0_h1).primitive()[1]
    open_saturator = (h1_rows[-1]*e1_h1).primitive()[1]
    open_rows = [*h1_rows[:4], prs_relation, open_saturator]
    exceptional_rows = [*h1_rows[:4], e1_h1, e0_h1, h1_rows[-1]]
    write_input(OUT_OPEN, open_rows)
    write_input(OUT_EXCEPTIONAL, exceptional_rows)
    labels_open = ["P324_h1", "P851_h1", "P1342_h1", "P1846_h1",
                   "PRS_E1_b1_plus_E0_h1", "base_C8_times_E1_saturator"]
    labels_exceptional = ["P324_h1", "P851_h1", "P1342_h1", "P1846_h1",
                          "E1_h1", "E0_h1", "base_C8_saturator"]
    LABELS_OPEN.write_text(json.dumps({"labels": labels_open}, indent=2)+"\n")
    LABELS_EXCEPTIONAL.write_text(
        json.dumps({"labels": labels_exceptional}, indent=2)+"\n")

    result = {
        "status": "UNAUDITED exact PRS split in monic-h1 quotient",
        "h1_source": H1_SOURCE.name,
        "h1_source_sha256": sha256(H1_SOURCE.read_bytes()).hexdigest(),
        "prs_payload": PRS.name,
        "prs_payload_sha256": sha256(PRS.read_bytes()).hexdigest(),
        "E1_h1_profile": record(e1_h1),
        "E0_h1_profile": record(e0_h1),
        "PRS_relation_h1_profile": record(prs_relation),
        "E1_h1_b1_degree": e1_b1_degree,
        "E0_h1_b1_degree": e0_b1_degree,
        "PRS_relation_h1_b1_degree": relation_b1_degree,
        "transformed_relation_is_linear_in_b1": relation_b1_degree == 1,
        "E1_E0_gcd_h1_profile": record(gcd_h1),
        "E1_E0_gcd_h1": encode(gcd_h1) if len(gcd_h1) <= 20 else None,
        "E1_open_input": OUT_OPEN.name,
        "E1_open_input_sha256": sha256(OUT_OPEN.read_bytes()).hexdigest(),
        "E1_open_input_bytes": OUT_OPEN.stat().st_size,
        "E1_open_labels": LABELS_OPEN.name,
        "E1_open_localizer_profile": record(open_saturator),
        "exceptional_input": OUT_EXCEPTIONAL.name,
        "exceptional_input_sha256": sha256(OUT_EXCEPTIONAL.read_bytes()).hexdigest(),
        "exceptional_input_bytes": OUT_EXCEPTIONAL.stat().st_size,
        "exceptional_labels": LABELS_EXCEPTIONAL.name,
        "exceptional_profile_only": True,
        "representation_guard": (
            "After substituting b0=11-2*b1-3*d1-5*d3-7*d4, E1 and E0 "
            "may depend on b1. Solving b1 is allowed only if the transformed "
            "PRS relation has audited b1-degree one."),
        "scope": (
            "Exact split of the monic-h1 four-variable quotient into E1-open "
            "and E1=E0=0 branches. The E1-open file localizes the unchanged "
            "base*C8 product times E1. The exceptional file is exported for "
            "profile/factor audit only. Modular computations remain discovery."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode()).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print("monic-h1 PRS split export: PASS")
    print("b1 degrees E1/E0/relation:", e1_b1_degree, e0_b1_degree,
          relation_b1_degree)
    print("profiles:", result["E1_h1_profile"], result["E0_h1_profile"],
          result["PRS_relation_h1_profile"], result["E1_E0_gcd_h1_profile"])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
