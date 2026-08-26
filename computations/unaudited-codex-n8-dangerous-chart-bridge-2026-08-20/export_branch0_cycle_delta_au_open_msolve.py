#!/usr/bin/env python3
"""Export the compact Au-open special-divisor interface for msolve.

The raw system is Q plus the two source-derived consistency-minor cores.
The saturated variant appends the known live-factor product and is intended
for ``msolve -S``.  Variable order b0,b1,d1,x makes ``-e 2`` eliminate the
two fibre variables and expose the exceptional parameter divisor.
"""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
AUDIT_PATH = HERE / "audit_branch0_cycle_delta_au_open_generic.py"
RAW_OUT = HERE / "branch0_cycle_delta_au_open_pair_p1009.msolve"
SAT_OUT = HERE / "branch0_cycle_delta_au_open_pair_sat_p1009.msolve"
SAT_LARGE_OUT = HERE / "branch0_cycle_delta_au_open_pair_sat_p1073741827.msolve"
SPEC_OUT = HERE / "results_branch0_cycle_delta_au_open_msolve_export.json"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


AUDIT = load("n8_cycle_delta_au_open_audit", AUDIT_PATH)
sp = AUDIT.sp
SOURCE = AUDIT.SOURCE


def encode(poly):
    return str(sp.expand(poly)).replace("**", "^")


def msolve_text(polynomials, characteristic):
    return (f"b0,b1,d1,x\n{characteristic}\n"
            + ",\n".join(encode(poly) for poly in polynomials) + "\n")


def file_sha(path):
    return sha256(path.read_bytes()).hexdigest()


def main():
    rows = {label: SOURCE.expression(poly)
            for label, poly, _ in SOURCE.SOURCE.data()[0]}
    derived = AUDIT.derive(rows)
    b0, b1, _, d1, _, _ = SOURCE.PARAMETERS
    x = sp.Symbol("x")
    q = derived["q"]
    left = derived["left"]
    right = derived["right"]
    au = derived["au"]
    d4_numerator = sp.cancel(derived["d4_value"]).as_numer_denom()[0]
    a = derived["a"]
    live = sp.expand(b0*b1*d1*x*(b1+d1)*(x-1)*au*d4_numerator*a)
    raw_polynomials = (q, left, right)
    sat_polynomials = (*raw_polynomials, live)
    RAW_OUT.write_text(msolve_text(raw_polynomials, 1009))
    SAT_OUT.write_text(msolve_text(sat_polynomials, 1009))
    SAT_LARGE_OUT.write_text(msolve_text(sat_polynomials, 1073741827))
    result = {
        "status": "UNAUDITED compact msolve export for Au-open divisors",
        "characteristic": 1009,
        "variables": ["b0", "b1", "d1", "x"],
        "raw_polynomial_terms": [
            len(sp.Poly(poly, b0, b1, d1, x).terms())
            for poly in raw_polynomials],
        "raw_polynomial_degrees": [
            sp.Poly(poly, b0, b1, d1, x).total_degree()
            for poly in raw_polynomials],
        "live_factor": str(live),
        "raw_file": RAW_OUT.name,
        "raw_sha256": file_sha(RAW_OUT),
        "saturated_file": SAT_OUT.name,
        "saturated_sha256": file_sha(SAT_OUT),
        "large_prime_saturated_file": SAT_LARGE_OUT.name,
        "large_prime_saturated_sha256": file_sha(SAT_LARGE_OUT),
        "commands": {
            "raw_elimination": (
                f"msolve -f {RAW_OUT.name} -e 2 -g 2 -t 4"),
            "live_saturation_elimination": (
                f"msolve -f {SAT_OUT.name} -S -e 2 -g 2 -t 4"),
            "large_prime_live_saturation_elimination": (
                f"msolve -f {SAT_LARGE_OUT.name} -S -e 2 -g 2 -t 4")},
        "scope": (
            "The raw system contains every Au-open solution but may retain "
            "boundary components. The -S input removes only displayed "
            "coefficient-field/chart live factors; selected p_i+1 factors "
            "are not represented after projection. A negative result is "
            "therefore not by itself a full-chart obstruction."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    SPEC_OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("branch-0 Delta Au-open msolve export: PASS")
    print("terms:", result["raw_polynomial_terms"])
    print("raw sha256:", result["raw_sha256"])
    print("sat sha256:", result["saturated_sha256"])
    print("large-prime sat sha256:",
          result["large_prime_saturated_sha256"])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
