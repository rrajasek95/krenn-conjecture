#!/usr/bin/env python3
"""Export the exact b1=d1 branch with an alternate Cof(1,3) packet.

The old Cof obstruction vanishes identically on this branch.  We retain Q,
all fifteen literal packet minors, the compact alternate Cramer packet
(rows 0,1,2), and the original open-set saturator.  Substitution is made
termwise over Z, and only integer/declared-live monomial content is removed.
"""

from __future__ import annotations

from collections import defaultdict
from hashlib import sha256
import importlib.util
import json
from math import gcd
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
EXACT = HERE.parent / "unaudited-codex-k4-cycle-cofactor13-exact-2026-08-21"
BASE_PATH = EXACT / "build_cofactor13_b0_resultants_flint.py"
PACKETS_PATH = HERE / "cofactor13_b1eqd1_cramer_packets.jsonl"
LABELS_PATH = HERE / "cofactor13_all_minors_labels.json"
INPUTS = (HERE / "cofactor13_all_minors_p1073741827.msolve",
          HERE / "cofactor13_all_minors_p1073741789.msolve")
OUTPUTS = (HERE / "cofactor13_b1eqd1_p1073741827.msolve",
           HERE / "cofactor13_b1eqd1_p1073741789.msolve")
OUT_LABELS = HERE / "cofactor13_b1eqd1_labels.json"
RESULT = HERE / "results_cofactor13_b1eqd1_export.json"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


BASE = load("cofactor13_b1eqd1_base", BASE_PATH)
from flint import fmpz_mpoly_ctx  # noqa: E402

CTX = fmpz_mpoly_ctx.get(("b0", "d1", "x"))
b0, d1, x = CTX.gens()


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def substitute_b1_d1(text):
    parsed = BASE.parse_b0_coefficients(text)
    values = defaultdict(int)
    for b0_power, coefficient_poly in parsed.items():
        for (b1_power, d1_power, x_power), coefficient in \
                coefficient_poly.to_dict().items():
            values[(int(b0_power), int(b1_power+d1_power), int(x_power))] \
                += int(coefficient)
    return CTX.from_dict({key: value for key, value in values.items() if value})


def primitive_live(poly):
    values = poly.to_dict()
    require(values, "specialized source row vanished")
    scalar = 0
    for coefficient in values.values():
        scalar = gcd(scalar, abs(int(coefficient)))
    monomial = tuple(min(exponent[index] for exponent in values)
                     for index in range(3))
    normalized = {tuple(exponent[index]-monomial[index]
                        for index in range(3)): int(coefficient)//scalar
                  for exponent, coefficient in values.items()}
    sign = 1 if normalized[max(normalized)] > 0 else -1
    core = CTX.from_dict({key: sign*value for key, value in normalized.items()})
    return core, sign*scalar, monomial


def primitive_integer_only(poly):
    """Normalize scalar content but preserve every saturator factor."""
    values = poly.to_dict()
    require(values, "specialized saturator vanished")
    scalar = 0
    for coefficient in values.values():
        scalar = gcd(scalar, abs(int(coefficient)))
    normalized = {exponent: int(coefficient)//scalar
                  for exponent, coefficient in values.items()}
    sign = 1 if normalized[max(normalized)] > 0 else -1
    return CTX.from_dict({key: sign*value for key, value in normalized.items()}), \
        sign*scalar


def profile(poly):
    logical = [[[int(value) for value in exponent], int(coefficient)]
               for exponent, coefficient in sorted(poly.to_dict().items())]
    return {"terms": len(poly),
            "degrees_b0_d1_x": [int(value) for value in poly.degrees()],
            "sha256": sha256(json.dumps(logical, separators=(",", ":"))
                              .encode()).hexdigest()}


def main():
    ledgers = [BASE.read_rows(path) for path in INPUTS]
    require(ledgers[0][0] == 1073741827
            and ledgers[1][0] == 1073741789
            and ledgers[0][1] == ledgers[1][1],
            "two-prime integer source ledgers diverged")
    source_rows = ledgers[0][1]
    source_labels = json.loads(LABELS_PATH.read_text())["labels"]
    packet_records = [json.loads(line) for line in
                      PACKETS_PATH.read_text().splitlines() if line.strip()]
    require([record["row_indices"] for record in packet_records]
            == [[0, 1, 2], [0, 1, 4]],
            "bounded alternate packet ledger changed")

    # Old Cof row 16 is intentionally omitted: it specializes to zero.
    selected_indices = [0, *range(1, 16), 17]
    rows = []
    labels = []
    records = []
    for index in selected_indices:
        raw = substitute_b1_d1(source_rows[index])
        if index == 17:
            core, scalar = primitive_integer_only(raw)
            monomial = (0, 0, 0)
        else:
            core, scalar, monomial = primitive_live(raw)
        rows.append(core)
        labels.append(source_labels[index])
        records.append({"source_index": index,
                        "source_label": source_labels[index],
                        "removed_integer_content_signed": scalar,
                        "removed_live_monomial_b0_d1_x": [int(value) for value in monomial],
                        "profile": profile(core)})
    # Put both independent obstructions before the saturator, which must
    # remain last for the toolkit's F4SAT interface.
    for packet in packet_records:
        packet_raw = substitute_b1_d1(packet["polynomial"])
        packet_core, packet_scalar, packet_monomial = primitive_live(packet_raw)
        packet_label = ("cofactor_1_3_cramer_rows_" +
                        "".join(map(str, packet["row_indices"])) +
                        "_b1eqd1")
        rows.insert(-1, packet_core)
        labels.insert(-1, packet_label)
        records.insert(-1, {"source_index": None,
                            "source_label": packet_label,
                            "removed_integer_content_signed": packet_scalar,
                            "removed_live_monomial_b0_d1_x":
                                [int(value) for value in packet_monomial],
                            "profile": profile(packet_core)})
    require(len(rows) == len(labels) == 19 and labels[-1] == "live_saturator",
            "branch row interface changed")

    encoded = [str(poly).replace("**", "^") for poly in rows]
    for (prime, _), path in zip(ledgers, OUTPUTS, strict=True):
        path.write_text("b0,d1,x\n" + str(prime) + "\n" +
                        ",\n".join(encoded) + "\n")
    OUT_LABELS.write_text(json.dumps({"labels": labels}, indent=2) + "\n")
    result = {
        "status": "UNAUDITED exact b1=d1 branch export PASS",
        "branch_relation": "b1-d1=0",
        "alternate_packet_rows": [record["row_indices"]
                                  for record in packet_records],
        "alternate_packet_source_labels": [record["row_labels"]
                                           for record in packet_records],
        "records": records,
        "outputs": [{"prime": prime, "path": path.name,
                     "sha256": sha256(path.read_bytes()).hexdigest()}
                    for (prime, _), path in zip(ledgers, OUTPUTS, strict=True)],
        "labels_path": OUT_LABELS.name,
        "labels_sha256": sha256(OUT_LABELS.read_bytes()).hexdigest(),
        "scope": ("This is an exact necessary branch system. The alternate "
                  "Cramer row is valid without inverting its determinant. "
                  "Only b0,d1,x monomials, which are live on the chart, and "
                  "integer contents were removed. Modular UNIT is discovery "
                  "only until exact-Q replay."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode()).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("b1=d1 Cof13 branch export: PASS")
    print("row terms", [record["profile"]["terms"] for record in records])
    print("result sha256", result["result_sha256"])


if __name__ == "__main__":
    main()
