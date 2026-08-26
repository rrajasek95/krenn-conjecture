#!/usr/bin/env python3
"""Export the exact P26=0 triangle-pendant branch for msolve/F4SAT.

The first twelve polynomials are the eleven exact source rows after E=0 and
the Laurent rescaling x=d4*a4, y=d4*d5*a5, followed by P26.  The F4SAT file
appends exactly the product of the chart/live factors.  The ordinary
Rabinowitsch file instead appends z*live-1.

Finite-field output is discovery only.  An emptiness statement over Q still
requires exact reconstruction/replay or an independently valid lifting
argument.
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
DISCOVERY = HERE / "discover_branch0_triangle_pendant_reduction.py"
RAW = HERE / "branch0_triangle_pendant_p26_boundary_raw_p1073741827.msolve"
SAT = HERE / "branch0_triangle_pendant_p26_boundary_sat_p1073741827.msolve"
SAT2 = HERE / "branch0_triangle_pendant_p26_boundary_sat_p1073741789.msolve"
RAB = HERE / "branch0_triangle_pendant_p26_boundary_rab_p1073741827.msolve"
RAB2 = HERE / "branch0_triangle_pendant_p26_boundary_rab_p1073741789.msolve"
RAB_Q = HERE / "branch0_triangle_pendant_p26_boundary_rab_Q.msolve"
DUMMY_Q = HERE / "branch0_triangle_pendant_p26_boundary_dummy_Q.msolve"
DUMMY = HERE / "branch0_triangle_pendant_p26_boundary_dummy_p1073741827.msolve"
DUMMY2 = HERE / "branch0_triangle_pendant_p26_boundary_dummy_p1073741789.msolve"
DSAT = HERE / "branch0_triangle_pendant_p26_boundary_Dsat_p1073741827.msolve"
DSAT2 = HERE / "branch0_triangle_pendant_p26_boundary_Dsat_p1073741789.msolve"
DRAB = HERE / "branch0_triangle_pendant_p26_boundary_Drab_p1073741827.msolve"
DRAB2 = HERE / "branch0_triangle_pendant_p26_boundary_Drab_p1073741789.msolve"
DRAB_Q = HERE / "branch0_triangle_pendant_p26_boundary_Drab_Q.msolve"
BASE_RAB = HERE / "branch0_triangle_pendant_p26_boundary_base_rab_p1073741827.msolve"
BASE_RAB2 = HERE / "branch0_triangle_pendant_p26_boundary_base_rab_p1073741789.msolve"
BASE_RAB_Q = HERE / "branch0_triangle_pendant_p26_boundary_base_rab_Q.msolve"
OUT = HERE / "results_branch0_triangle_pendant_p26_boundary_msolve_export.json"
PRIME = 1_073_741_827
PRIME2 = 1_073_741_789


def load():
    spec = importlib.util.spec_from_file_location("n8_tp_discovery", DISCOVERY)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


D = load()
C = D.CHART
VARIABLES = ("a4", "a5", "b0", "b1", "b3", "d4", "d5")


def primitive_integer(poly):
    denominator = math.lcm(*(value.denominator for value in poly.values()))
    integers = [value.numerator * (denominator // value.denominator)
                for value in poly.values()]
    content = math.gcd(*map(abs, integers))
    value = C.scale(poly, Fraction(denominator, content))
    first = value[min(value)]
    if first < 0:
        value = C.scale(value, -1)
    return value


def encode(poly):
    return C.singular(primitive_integer(poly)).replace("/1", "")


def encode_z_times_minus_one(poly):
    """Expand z*poly-1; msolve 0.10.1 misparses z*(poly)-1 silently."""
    poly = primitive_integer(poly)
    terms = []
    for exponent in sorted(poly, key=lambda item: (sum(item), item),
                           reverse=True):
        coefficient = int(poly[exponent])
        factors = ["z"]
        factors += [f"{name}^{power}" for name, power in zip(C.names, exponent)
                    if power]
        monomial = "*".join(factors)
        absolute = abs(coefficient)
        body = monomial if absolute == 1 else f"{absolute}*{monomial}"
        if not terms:
            terms.append(body if coefficient > 0 else f"-{body}")
        else:
            terms.append(("+" if coefficient > 0 else "-") + body)
    terms.append("-1")
    return "".join(terms)


def msolve_text(variables, polynomials, characteristic=PRIME):
    return (",".join(variables) + f"\n{characteristic}\n"
            + ",\n".join(polynomials) + "\n")


def file_sha(path):
    return sha256(path.read_bytes()).hexdigest()


def main():
    data = D.cramer_branch_system(7, 12)
    labels = [label for label, _ in data["closed_rows"]]
    if labels != [7, 8, 9, 10, 11, 12, 13, 15, 17, 19, 21, 101]:
        raise RuntimeError(("closed-row labels changed", labels))
    rows = [poly for _, poly in data["closed_rows"]]
    live = C.one
    for factor in data["closed_live_factors"]:
        live = C.multiply(live, factor)
    raw = [encode(poly) for poly in rows]
    live_encoded = encode(live)
    live_D = C.add(C.multiply(C.variable(7), C.variable(C.d_index[4])),
                   C.multiply(C.variable(6), C.variable(C.d_index[5])))
    live_D_encoded = encode(live_D)
    live_base = data["closed_live_factors"][0]
    RAW.write_text(msolve_text(VARIABLES, raw))
    SAT.write_text(msolve_text(VARIABLES, [*raw, live_encoded]))
    SAT2.write_text(msolve_text(VARIABLES, [*raw, live_encoded], PRIME2))
    RAB.write_text(msolve_text(("z", *VARIABLES),
                               [*raw, encode_z_times_minus_one(live)]))
    RAB2.write_text(msolve_text(("z", *VARIABLES),
                                [*raw, encode_z_times_minus_one(live)], PRIME2))
    RAB_Q.write_text(msolve_text(("z", *VARIABLES),
                                 [*raw, encode_z_times_minus_one(live)], 0))
    # The harmless extension z-1=0 changes only the monomial ordering seen by
    # msolve and exposes a much smaller raw-ideal basis.  It is not a
    # localization and is recorded separately from Rabinowitsch.
    DUMMY_Q.write_text(msolve_text(("z", *VARIABLES), [*raw, "z-1"], 0))
    DUMMY.write_text(msolve_text(("z", *VARIABLES), [*raw, "z-1"]))
    DUMMY2.write_text(msolve_text(("z", *VARIABLES), [*raw, "z-1"],
                                  PRIME2))
    DSAT.write_text(msolve_text(VARIABLES, [*raw, live_D_encoded]))
    DSAT2.write_text(msolve_text(VARIABLES, [*raw, live_D_encoded], PRIME2))
    DRAB.write_text(msolve_text(("z", *VARIABLES),
                                [*raw, encode_z_times_minus_one(live_D)]))
    DRAB2.write_text(msolve_text(("z", *VARIABLES),
                                 [*raw, encode_z_times_minus_one(live_D)],
                                 PRIME2))
    DRAB_Q.write_text(msolve_text(("z", *VARIABLES),
                                  [*raw, encode_z_times_minus_one(live_D)], 0))
    BASE_RAB.write_text(msolve_text(
        ("z", *VARIABLES), [*raw, encode_z_times_minus_one(live_base)]))
    BASE_RAB2.write_text(msolve_text(
        ("z", *VARIABLES), [*raw, encode_z_times_minus_one(live_base)],
        PRIME2))
    BASE_RAB_Q.write_text(msolve_text(
        ("z", *VARIABLES), [*raw, encode_z_times_minus_one(live_base)], 0))
    result = {
        "status": "UNAUDITED exact interface; finite-field discovery only",
        "characteristic": PRIME,
        "variables": list(VARIABLES),
        "source_row_labels_plus_split": labels,
        "row_term_counts": [len(poly) for poly in rows],
        "row_degrees": [max(sum(exponent) for exponent in poly)
                        for poly in rows],
        "live_factor_term_count": len(live),
        "live_factor_degree": max(sum(exponent) for exponent in live),
        "live_factors": [C.singular(poly)
                         for poly in data["closed_live_factors"]],
        "files": {
            "raw": {"path": RAW.name, "sha256": file_sha(RAW)},
            "f4sat": {"path": SAT.name, "sha256": file_sha(SAT)},
            "f4sat_second_prime": {"path": SAT2.name,
                                   "sha256": file_sha(SAT2)},
            "rabinowitsch": {"path": RAB.name, "sha256": file_sha(RAB)},
            "rabinowitsch_second_prime": {
                "path": RAB2.name, "sha256": file_sha(RAB2)},
            "rabinowitsch_Q": {"path": RAB_Q.name,
                               "sha256": file_sha(RAB_Q)},
            "dummy_order_Q": {"path": DUMMY_Q.name,
                              "sha256": file_sha(DUMMY_Q)},
            "dummy_order": {"path": DUMMY.name, "sha256": file_sha(DUMMY)},
            "dummy_order_second_prime": {
                "path": DUMMY2.name, "sha256": file_sha(DUMMY2)},
            "D_f4sat": {"path": DSAT.name, "sha256": file_sha(DSAT)},
            "D_f4sat_second_prime": {
                "path": DSAT2.name, "sha256": file_sha(DSAT2)},
            "D_rabinowitsch": {"path": DRAB.name, "sha256": file_sha(DRAB)},
            "D_rabinowitsch_second_prime": {
                "path": DRAB2.name, "sha256": file_sha(DRAB2)},
            "D_rabinowitsch_Q": {"path": DRAB_Q.name,
                                  "sha256": file_sha(DRAB_Q)},
            "base_rabinowitsch": {"path": BASE_RAB.name,
                                   "sha256": file_sha(BASE_RAB)},
            "base_rabinowitsch_second_prime": {
                "path": BASE_RAB2.name, "sha256": file_sha(BASE_RAB2)},
            "base_rabinowitsch_Q": {"path": BASE_RAB_Q.name,
                                     "sha256": file_sha(BASE_RAB_Q)},
        },
        "commands": {
            "raw": f"msolve -f {RAW.name} -g 1 -t 4",
            "f4sat": f"msolve -f {SAT.name} -S -g 1 -t 4",
            "f4sat_second_prime": f"msolve -f {SAT2.name} -S -g 1 -t 4",
            "rabinowitsch": f"msolve -f {RAB.name} -g 1 -t 4",
            "rabinowitsch_second_prime": f"msolve -f {RAB2.name} -g 1 -t 4",
            "rabinowitsch_Q": f"msolve -f {RAB_Q.name} -g 1 -t 4",
            "dummy_order_Q": f"msolve -f {DUMMY_Q.name} -g 2 -t 4",
            "dummy_order": f"msolve -f {DUMMY.name} -g 2 -t 4",
            "dummy_order_second_prime": (
                f"msolve -f {DUMMY2.name} -g 2 -t 4"),
            "D_f4sat": f"msolve -f {DSAT.name} -S -g 1 -t 4",
            "D_f4sat_second_prime": f"msolve -f {DSAT2.name} -S -g 1 -t 4",
            "D_rabinowitsch": f"msolve -f {DRAB.name} -g 1 -t 4",
            "D_rabinowitsch_second_prime": (
                f"msolve -f {DRAB2.name} -g 1 -t 4"),
            "D_rabinowitsch_Q": f"msolve -f {DRAB_Q.name} -g 1 -t 4",
            "base_rabinowitsch": f"msolve -f {BASE_RAB.name} -g 1 -t 4",
            "base_rabinowitsch_second_prime": (
                f"msolve -f {BASE_RAB2.name} -g 1 -t 4"),
            "base_rabinowitsch_Q": (
                f"msolve -f {BASE_RAB_Q.name} -g 1 -t 4"),
        },
        "scope": (
            "The first twelve equations are exact over Q.  The last F4SAT "
            "polynomial localizes precisely the scaled-cell, chain-denominator, "
            "and transported a2/a3 live factors.  A finite-field UNIT is not "
            "by itself a characteristic-zero closure."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("TP P26-boundary msolve export: PASS")
    print("rows / live terms:", len(rows), len(live))
    print("raw sha256:", result["files"]["raw"]["sha256"])
    print("f4sat sha256:", result["files"]["f4sat"]["sha256"])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
