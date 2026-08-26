#!/usr/bin/env python3
"""Exact monic-hyperplane substitution for the four-row C8-open p1 core."""

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
OUTPUT = HERE / "branch0_cycle_generic_codim5_fourrow_h1_sub_c8open_p1073741827.msolve"
LABELS = HERE / "branch0_cycle_generic_codim5_fourrow_h1_sub_c8open_labels.json"
RESULT = HERE / "results_branch0_cycle_generic_codim5_fourrow_h1_sub_c8open_export.json"


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


def main():
    lines = SOURCE.read_text().splitlines()
    encoded_rows = "\n".join(lines[2:]).strip().split(",\n")
    require(lines[:2] == ["b0,b1,d1,d3,d4", "1073741827"]
            and len(encoded_rows) == 6,
            "one-slice source header changed")
    source_result = json.loads(SOURCE_RESULT.read_text())
    require(source_result["output_sha256"] == sha256(SOURCE.read_bytes()).hexdigest(),
            "one-slice source hash changed")

    ctx5 = fmpz_mpoly_ctx.get(["b0", "b1", "d1", "d3", "d4"], ordering="lex")
    ctx4 = fmpz_mpoly_ctx.get(["b1", "d1", "d3", "d4"], ordering="lex")
    source_rows = [parse(row, ctx5) for row in encoded_rows]
    b1, d1, d3, d4 = ctx4.gens()
    b0_image = 11-2*b1-3*d1-5*d3-7*d4
    images = [poly.compose(b0_image, b1, d1, d3, d4)
              for poly in source_rows]
    require(images[4].is_zero(), "retained monic hyperplane did not map to zero")
    hostile_b0 = 12-2*b1-3*d1-5*d3-7*d4
    hostile_h1 = source_rows[4].compose(hostile_b0, b1, d1, d3, d4)
    require(hostile_h1.is_one(), "hyperplane hostile constant mutation did not fire")
    require(any(source_rows[index].compose(hostile_b0, b1, d1, d3, d4)
                != images[index] for index in range(4)),
            "source-row hostile substitution mutation did not fire")

    output_rows = [*images[:4], images[5]]
    labels = ["P324_h1", "P851_h1", "P1342_h1", "P1846_h1",
              "C8_open_live_saturator_h1"]
    OUTPUT.write_text(
        "b1,d1,d3,d4\n1073741827\n"
        + ",\n".join(encode(poly) for poly in output_rows)+"\n")
    LABELS.write_text(json.dumps({"labels": labels}, indent=2)+"\n")
    require("(" not in OUTPUT.read_text().split("\n", 2)[2]
            and "**" not in OUTPUT.read_text().split("\n", 2)[2],
            "substituted strict syntax guard failed")

    # Export the test polynomial now so a finite RUR can replay D10 without
    # repeating the representation change.
    b0, sb1, sd1, sd3, sd4 = ctx5.gens()
    d10 = (b0**2*sb1*sd1*sd4+2*b0**2*sb1*sd3-b0**2*sd1**2*sd4
           -b0*sb1*sd1*sd4+b0*sb1*sd3*sd4-b0*sd1**2*sd4
           -b0*sd1*sd3*sd4+2*sb1*sd1*sd4**2+sb1*sd3*sd4
           +sd1*sd3*sd4)
    d10_image = d10.compose(b0_image, b1, d1, d3, d4)
    result = {
        "status": "UNAUDITED exact monic-hyperplane p1 substitution",
        "source": SOURCE.name,
        "source_sha256": sha256(SOURCE.read_bytes()).hexdigest(),
        "output": OUTPUT.name,
        "output_sha256": sha256(OUTPUT.read_bytes()).hexdigest(),
        "labels": LABELS.name,
        "labels_sha256": sha256(LABELS.read_bytes()).hexdigest(),
        "source_variables": ["b0", "b1", "d1", "d3", "d4"],
        "target_variables": ["b1", "d1", "d3", "d4"],
        "hyperplane": "b0+2*b1+3*d1+5*d3+7*d4-11",
        "pivot_coefficient": 1,
        "substitution": "b0=11-2*b1-3*d1-5*d3-7*d4",
        "source_row_profiles": [record(poly) for poly in source_rows[:4]],
        "image_row_profiles": [record(poly) for poly in images[:4]],
        "source_localizer_profile": record(source_rows[5]),
        "image_localizer_profile": record(images[5]),
        "D10_image": encode(d10_image),
        "D10_image_profile": record(d10_image),
        "hyperplane_must_fire": True,
        "hostile_constant_mutation_fired": True,
        "scope": (
            "Exact quotient by a monic affine hyperplane, hence no exceptional "
            "leading-coefficient branch. The original four rows and exact "
            "base*C8 saturator are changed only by this isomorphism. Modular "
            "F4SAT remains discovery only."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode()).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print("four-row monic-hyperplane substitution: PASS")
    print("image profiles:", result["image_row_profiles"],
          result["image_localizer_profile"])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
