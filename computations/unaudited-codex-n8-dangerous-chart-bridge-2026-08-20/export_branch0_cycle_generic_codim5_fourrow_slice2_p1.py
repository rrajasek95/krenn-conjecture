#!/usr/bin/env python3
"""Export the two-slice four-row C8-open containment probe at p1."""

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
SOURCE = HERE / "branch0_cycle_generic_qrstu_codim5_exact.msolve"
OUTPUT = HERE / "branch0_cycle_generic_codim5_fourrow_slice2_c8open_p1073741827.msolve"
LABELS = HERE / "branch0_cycle_generic_codim5_fourrow_slice2_c8open_labels.json"
RESULT = HERE / "results_branch0_cycle_generic_codim5_fourrow_slice2_c8open_export.json"
PRIME = 1073741827


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def parse_terms(encoded, names):
    index = {name: position for position, name in enumerate(names)}
    answer = {}
    for raw in re.findall(r"[+-]?[^+-]+", encoded.replace(" ", "")):
        sign = -1 if raw.startswith("-") else 1
        body = raw[1:] if raw[:1] in "+-" else raw
        coefficient = sign
        monomial = [0]*len(names)
        for factor in body.split("*"):
            if re.fullmatch(r"\d+", factor):
                coefficient *= int(factor)
                continue
            match = re.fullmatch(r"([A-Za-z_][A-Za-z0-9_]*)(?:\^(\d+))?", factor)
            require(match is not None and match.group(1) in index,
                    f"unsupported factor {factor!r}")
            monomial[index[match.group(1)]] += int(match.group(2) or 1)
        key = tuple(monomial)
        answer[key] = answer.get(key, 0)+coefficient
    return answer


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
    text = encode(poly.primitive()[1])
    return {"terms": len(poly), "degree": int(poly.total_degree()),
            "sha256": sha256(text.encode("ascii")).hexdigest()}


def main():
    lines = SOURCE.read_text().splitlines()
    names6 = lines[0].split(",")
    rows = "\n".join(lines[2:]).strip().split(",\n")
    require(names6 == ["b0", "b1", "d1", "d3", "d4", "z"]
            and lines[1] == "0" and len(rows) == 10,
            "exact source header changed")
    names5 = names6[:-1]
    ctx = fmpz_mpoly_ctx.get(names5, ordering="lex")

    # Recover the exact live product from z*live-1 without symbolic parsing.
    live_terms = {}
    constant = 0
    for monomial6, coefficient in parse_terms(rows[-1], names6).items():
        if monomial6[-1] == 0:
            require(not any(monomial6[:-1]), "localizer has a z-free monomial")
            constant += coefficient
        else:
            require(monomial6[-1] == 1, "localizer is not affine in z")
            live_terms[monomial6[:-1]] = coefficient
    require(constant == -1, "Rabinowitsch constant changed")
    full_live = ctx.from_dict(live_terms)

    b0, b1, d1, d3, d4 = ctx.gens()
    c8 = (b0**2*d1*d3-b0**2*d3-b0*d1*d3*d4-b0*d1*d3
          -b0*d1*d4-b0*d3*d4-d1*d3*d4+d1*d4**2)
    d10 = (b0**2*b1*d1*d4+2*b0**2*b1*d3-b0**2*d1**2*d4
           -b0*b1*d1*d4+b0*b1*d3*d4-b0*d1**2*d4
           -b0*d1*d3*d4+2*b1*d1*d4**2+b1*d3*d4+d1*d3*d4)
    quotient, remainder = divmod(full_live, d10)
    require(remainder.is_zero(), "corrected live product lost D10")
    c8_open_live = quotient.primitive()[1]
    require((c8_open_live % c8).is_zero(), "D10 quotient lost C8")
    require(c8_open_live*d10 == full_live
            or c8_open_live*d10 == -full_live,
            "C8-open live quotient replay failed")

    h1 = "b0+2*b1+3*d1+5*d3+7*d4-11"
    h2 = "b0+9*b1+4*d1+22*d3+10*d4-46"
    selected = [rows[2], rows[0], rows[1], rows[3]]
    labels = ["P324", "P851", "P1342", "P1846",
              "slice_h1", "slice_h2", "C8_open_live_saturator"]
    output_rows = [*selected, h1, h2, encode(c8_open_live)]
    OUTPUT.write_text(
        ",".join(names5)+f"\n{PRIME}\n"+",\n".join(output_rows)+"\n")
    LABELS.write_text(json.dumps({"labels": labels}, indent=2)+"\n")
    require("(" not in OUTPUT.read_text().split("\n", 2)[2]
            and "**" not in OUTPUT.read_text().split("\n", 2)[2],
            "strict modular syntax guard failed")
    result = {
        "status": "UNAUDITED p1 four-row two-slice C8-open export",
        "source": SOURCE.name,
        "source_sha256": sha256(SOURCE.read_bytes()).hexdigest(),
        "output": OUTPUT.name,
        "output_sha256": sha256(OUTPUT.read_bytes()).hexdigest(),
        "labels": LABELS.name,
        "labels_sha256": sha256(LABELS.read_bytes()).hexdigest(),
        "prime": PRIME,
        "rows": labels,
        "slices": [h1, h2],
        "full_live_profile": record(full_live),
        "C8_profile": record(c8),
        "D10_profile": record(d10),
        "C8_open_live_profile": record(c8_open_live),
        "live_identity": "full_live=(C8_open_live)*D10",
        "scope": (
            "Modular sliced-flatness discovery for the original four retained "
            "rows on the base*C8-open chart. D10 is deliberately not "
            "localized so it can be tested on any finite factors. The two "
            "affine linears are deterministic generic slices."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode()).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print("four-row two-slice C8-open export: PASS")
    print("live profiles:", result["full_live_profile"],
          result["C8_open_live_profile"])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
