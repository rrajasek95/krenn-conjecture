#!/usr/bin/env python3
"""Strictly referee the k4-cycle characteristic-zero RUR interface.

This is intentionally independent of the shared msolve toolkit while that
toolkit is being hardened.  It checks the exact source/export equivalence,
the fifth-variable Rabinowitsch convention, the known coefficient-order
parser bug, and refuses to interpret msolve's positive-dimensional sentinel
as a rational univariate representation.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import re


HERE = Path(__file__).resolve().parent
DANGER = (HERE.parent /
          "unaudited-codex-n8-dangerous-chart-bridge-2026-08-20")
PRIME_INPUT = (DANGER /
               "branch0_cycle_delta_au_open_all_minors_p1073741827.msolve")
CHAR0_INPUT = DANGER / "branch0_cycle_delta_au_open_all_minors_char0.msolve"
CHAR0_OUTPUT = (DANGER /
                "results_branch0_cycle_delta_au_open_all_minors_char0.param.out")
TOY_BAD_INPUT = HERE / "toy_rur_coefficient_order_left.msolve"
TOY_BAD_OUTPUT = HERE / "toy_rur_coefficient_order_left.out"
TOY_GOOD_INPUT = HERE / "toy_rur_coefficient_order_canonical.msolve"
TOY_GOOD_OUTPUT = HERE / "toy_rur_coefficient_order_canonical.out"
RESULT = HERE / "results_char0_rur_interface.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def file_sha(path):
    return sha256(path.read_bytes()).hexdigest()


def read_input(path):
    lines = path.read_text().splitlines()
    require(len(lines) >= 3, f"short msolve input: {path}")
    variables = tuple(value.strip() for value in lines[0].split(","))
    characteristic = int(lines[1])
    rows = tuple(value.strip() for value in
                 "\n".join(lines[2:]).split(",") if value.strip())
    return variables, characteristic, rows


def parse_expanded_integer(text, variables, *, strict_order=True):
    names = {name: index for index, name in enumerate(variables)}
    answer = Counter()
    value = re.sub(r"\s+", "", text)
    require(not any(token in value for token in ("(", ")", "**")),
            "row is not strict expanded msolve syntax")
    for encoded in re.findall(r"[+-]?[^+-]+", value):
        sign = -1 if encoded.startswith("-") else 1
        if encoded[:1] in "+-":
            encoded = encoded[1:]
        coefficient = sign
        exponent = [0] * len(variables)
        saw_symbol = False
        for factor in encoded.split("*"):
            if re.fullmatch(r"\d+", factor):
                if strict_order and saw_symbol:
                    raise RuntimeError(
                        "integer coefficient follows a symbolic factor")
                coefficient *= int(factor)
                continue
            match = re.fullmatch(r"([A-Za-z_][A-Za-z0-9_]*)(?:\^(\d+))?",
                                 factor)
            require(match is not None and match.group(1) in names,
                    f"unsupported factor {factor!r}")
            saw_symbol = True
            exponent[names[match.group(1)]] += int(match.group(2) or "1")
        answer[tuple(exponent)] += coefficient
    return {monomial: coefficient for monomial, coefficient in answer.items()
            if coefficient}


def classify_output(text, expected_variables):
    compact = re.sub(r"\s+", "", text).removesuffix(":")
    match = re.fullmatch(r"\[1,(\d+),-1,\[\]\]", compact)
    if match:
        require(int(match.group(1)) == expected_variables,
                "sentinel variable count changed")
        return "positive_dimensional_sentinel"
    if compact == "[-1]":
        return "empty_solution_sentinel"
    if compact.startswith("[0,[0,"):
        return "finite_rur_candidate"
    return "unrecognized_output"


def main():
    prime_variables, prime, prime_rows = read_input(PRIME_INPUT)
    char_variables, characteristic, char_rows = read_input(CHAR0_INPUT)
    require(prime_variables == ("b0", "b1", "d1", "x")
            and prime == 1073741827 and len(prime_rows) == 17,
            "frozen prime interface changed")
    require(char_variables == ("b0", "b1", "d1", "x", "z")
            and characteristic == 0 and len(char_rows) == 17,
            "characteristic-zero interface changed")

    prime_parsed = tuple(parse_expanded_integer(
        row, prime_variables) for row in prime_rows)
    char_parsed = tuple(parse_expanded_integer(
        row, char_variables) for row in char_rows)
    for index in range(16):
        lifted = {(*monomial, 0): coefficient
                  for monomial, coefficient in prime_parsed[index].items()}
        require(lifted == char_parsed[index],
                f"literal source equation {index} changed over Q")

    expected_rabinowitsch = {
        (*monomial, 1): coefficient
        for monomial, coefficient in prime_parsed[-1].items()
    }
    constant = (0,) * len(char_variables)
    expected_rabinowitsch[constant] = (
        expected_rabinowitsch.get(constant, 0) - 1)
    require(expected_rabinowitsch == char_parsed[-1],
            "final row is not exactly z*live-1")
    require(all(monomial[-1] == 0 for row in char_parsed[:-1]
                for monomial in row),
            "Rabinowitsch z entered a source equation")

    # The hostile input is syntactically accepted by msolve but must be
    # rejected by this referee.  The two outputs demonstrate the semantic
    # corruption without relying on a fresh engine run.
    bad_variables, _, bad_rows = read_input(TOY_BAD_INPUT)
    good_variables, _, good_rows = read_input(TOY_GOOD_INPUT)
    bad_rejected = False
    try:
        parse_expanded_integer(bad_rows[-1], bad_variables)
    except RuntimeError as error:
        bad_rejected = "coefficient follows" in str(error)
    require(bad_rejected, "hostile coefficient-order input was accepted")
    parse_expanded_integer(good_rows[-1], good_variables)
    bad_output = re.sub(r"\s+", "", TOY_BAD_OUTPUT.read_text())
    good_output = re.sub(r"\s+", "", TOY_GOOD_OUTPUT.read_text())
    require("[[1,[-1,2]],[0,[2]]" in bad_output,
            "hostile toy no longer reports z=1/2")
    require("[[1,[-1,4]],[0,[4]]" in good_output,
            "canonical toy no longer reports z=1/4")

    output_kind = classify_output(CHAR0_OUTPUT.read_text(), 5)
    output_is_fresh = (CHAR0_OUTPUT.stat().st_mtime >=
                       CHAR0_INPUT.stat().st_mtime)
    accepted_as_rur = output_kind == "finite_rur_candidate" and output_is_fresh
    result = {
        "status": "UNAUDITED strict characteristic-zero RUR interface referee",
        "prime_input_sha256": file_sha(PRIME_INPUT),
        "char0_input_sha256": file_sha(CHAR0_INPUT),
        "char0_output_sha256": file_sha(CHAR0_OUTPUT),
        "source_equation_count": 16,
        "rabinowitsch_variable": "z",
        "rabinowitsch_row_exact": True,
        "coefficient_after_symbol_guard": "PASS",
        "hostile_toy": {
            "input_sha256": file_sha(TOY_BAD_INPUT),
            "output_sha256": file_sha(TOY_BAD_OUTPUT),
            "observed_z": "1/2",
        },
        "canonical_toy": {
            "input_sha256": file_sha(TOY_GOOD_INPUT),
            "output_sha256": file_sha(TOY_GOOD_OUTPUT),
            "observed_z": "1/4",
        },
        "current_output_kind": output_kind,
        "current_output_newer_than_input": output_is_fresh,
        "accepted_as_rur": accepted_as_rur,
        "scope": (
            "This checks source/export equivalence and output envelope only. "
            "A fresh finite RUR still requires exact quotient replay of all "
            "sixteen source equations and, decisively, the five literal "
            "cofactors omitted by the all-minor packet."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("characteristic-zero RUR interface referee: PASS")
    print("output:", output_kind, "fresh:", output_is_fresh,
          "accepted:", accepted_as_rur)
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
