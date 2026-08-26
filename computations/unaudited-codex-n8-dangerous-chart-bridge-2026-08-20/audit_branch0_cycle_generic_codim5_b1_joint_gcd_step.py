#!/usr/bin/env python3
"""One bounded exact joint-gcd compression step at the PRS common root."""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
import sys
import time


_SITE = (Path(sys.executable).parent.parent / "lib" /
         f"python{sys.version_info.major}.{sys.version_info.minor}" /
         "site-packages")
if str(_SITE) not in sys.path:
    sys.path.append(str(_SITE))
from flint import fmpz_mpoly_ctx


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "branch0_cycle_generic_qrstu_codim5_exact.msolve"
PRS_PAYLOAD = HERE / "branch0_cycle_generic_codim5_b1_subresultant_polynomials.json"
STATE = HERE / "results_branch0_cycle_generic_codim5_b1_joint_gcd_state.json"
ROW_INDEX = {"P1846": 3, "Q4098": 4, "R4885": 5, "S4331": 6,
             "T4750": 7, "U3217": 8}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def split_rows(path: Path) -> tuple[list[str], list[str]]:
    lines = path.read_text().splitlines()
    return lines[0].split(","), "\n".join(lines[2:]).strip().split(",\n")


def parse_mpoly(encoded: str, ctx):
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
                    f"unsupported strict factor {factor!r}")
            monomial[names[match.group(1)]] += int(match.group(2) or 1)
        key = tuple(monomial)
        terms[key] = terms.get(key, 0)+coefficient
    return ctx.from_dict(terms)


def parse_b1_coefficients(encoded: str, ctx) -> dict[int, object]:
    names = {name: index for index, name in enumerate(ctx.names())}
    terms_by_degree = {}
    for raw in re.findall(r"[+-]?[^+-]+", encoded.replace(" ", "")):
        sign = -1 if raw.startswith("-") else 1
        body = raw[1:] if raw[:1] in "+-" else raw
        coefficient = sign
        monomial = [0]*ctx.nvars()
        b1_degree = 0
        for factor in body.split("*"):
            if re.fullmatch(r"\d+", factor):
                coefficient *= int(factor)
                continue
            match = re.fullmatch(r"([A-Za-z_][A-Za-z0-9_]*)(?:\^(\d+))?", factor)
            require(match is not None, f"unsupported strict factor {factor!r}")
            name, power = match.group(1), int(match.group(2) or 1)
            if name == "b1":
                b1_degree += power
            else:
                require(name in names, f"unknown parameter {name!r}")
                monomial[names[name]] += power
        terms_by_degree.setdefault(b1_degree, {})[tuple(monomial)] = coefficient
    return {degree: ctx.from_dict(terms)
            for degree, terms in terms_by_degree.items()}


def encode(poly) -> str:
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


def record(poly) -> dict:
    primitive = poly.primitive()[1]
    text = encode(primitive)
    return {"terms": len(primitive), "degree": int(primitive.total_degree()),
            "sha256": sha256(text.encode("ascii")).hexdigest()}


def strip_factor(poly, factor):
    count = 0
    while True:
        quotient, remainder = divmod(poly, factor)
        if not remainder.is_zero():
            return poly.primitive()[1], count
        poly = quotient
        count += 1


def evaluate_at_root(coefficients, e1, e0):
    degree = max(coefficients)
    answer = coefficients.get(degree, e1.context().constant(0))
    e1_power = e1
    for exponent in range(degree-1, -1, -1):
        answer = answer*(-e0) + coefficients.get(
            exponent, e1.context().constant(0))*e1_power
        e1_power *= e1
        print(f"joint-gcd: Horner exponent {exponent}, terms={len(answer)}",
              flush=True)
    return answer.primitive()[1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("row", choices=tuple(ROW_INDEX))
    args = parser.parse_args()
    started = time.monotonic()
    names, rows = split_rows(SOURCE)
    require(names == ["b0", "b1", "d1", "d3", "d4", "z"]
            and len(rows) == 10, "source header/row count changed")
    ctx = fmpz_mpoly_ctx.get(["b0", "d1", "d3", "d4"], ordering="lex")
    payload = json.loads(PRS_PAYLOAD.read_text())
    e1 = parse_mpoly(payload["E1"], ctx).primitive()[1]
    e0 = parse_mpoly(payload["E0"], ctx).primitive()[1]
    j_poly = parse_mpoly(payload["J"], ctx).primitive()[1]
    a_live = parse_mpoly(payload["gcd_J_K"], ctx).primitive()[1]

    if STATE.exists():
        state = json.loads(STATE.read_text())
        require(state["source_sha256"] == sha256(SOURCE.read_bytes()).hexdigest()
                and state["prs_payload_sha256"]
                == sha256(PRS_PAYLOAD.read_bytes()).hexdigest(),
                "joint-gcd state source changed")
        require(args.row not in state["processed_rows"],
                f"{args.row} was already processed")
        accumulator = parse_mpoly(state["accumulator"], ctx).primitive()[1]
    else:
        accumulator = parse_mpoly(payload["K"], ctx).primitive()[1]
        accumulator, removed = strip_factor(accumulator, a_live)
        require(removed >= 1, "K lost its audited live A factor")
        require(accumulator.gcd(j_poly).is_one(),
                "K/A is no longer coprime to J")
        state = {
            "status": "UNAUDITED exact unsaturated joint-gcd compression",
            "source": SOURCE.name,
            "source_sha256": sha256(SOURCE.read_bytes()).hexdigest(),
            "prs_payload": PRS_PAYLOAD.name,
            "prs_payload_sha256": sha256(PRS_PAYLOAD.read_bytes()).hexdigest(),
            "audited_live_factor_removed": "A",
            "A_removed_from_initial_K_power": removed,
            "initial_K_over_A_profile": record(accumulator),
            "J_profile": record(j_poly),
            "initial_gcd_K_over_A_J": "1",
            "processed_rows": [],
            "steps": [],
        }
    print("joint-gcd: accumulator loaded", record(accumulator), flush=True)

    coefficients = parse_b1_coefficients(rows[ROW_INDEX[args.row]], ctx)
    row_degree = max(coefficients)
    print(f"joint-gcd: {args.row} b1-degree={row_degree}", flush=True)
    numerator = evaluate_at_root(coefficients, e1, e0)
    print("joint-gcd: numerator complete", record(numerator), flush=True)
    updated = accumulator.gcd(numerator).primitive()[1]
    updated, removed_a = strip_factor(updated, a_live)
    step = {
        "row": args.row,
        "b1_degree": row_degree,
        "fraction_free_numerator_profile": record(numerator),
        "accumulator_before": record(accumulator),
        "removed_live_A_power": removed_a,
        "accumulator_after": record(updated),
        "accumulator_after_is_one": updated.is_one(),
        "gcd_accumulator_after_J": record(updated.gcd(j_poly)),
        "elapsed_seconds": time.monotonic()-started,
    }
    state["processed_rows"].append(args.row)
    state["steps"].append(step)
    state["accumulator"] = encode(updated)
    state["terminal"] = updated.is_one()
    logical = {key: value for key, value in state.items()
               if key not in {"accumulator", "result_sha256"}}
    state["result_sha256"] = sha256(json.dumps(
        logical, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    STATE.write_text(json.dumps(state, indent=2, sort_keys=True)+"\n")
    print("joint-gcd step: PASS", args.row, step["accumulator_after"])
    print("result sha256:", state["result_sha256"])


if __name__ == "__main__":
    main()
