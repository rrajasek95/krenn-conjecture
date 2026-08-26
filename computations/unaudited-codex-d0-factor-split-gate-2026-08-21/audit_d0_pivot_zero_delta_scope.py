#!/usr/bin/env python3
"""Correct the pivot-zero factor cover using the upstream Delta-live scope."""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
GENERIC = (HERE.parent / "unaudited-codex-root-integration-2026-08-20" /
           "probe_branch0_cycle_d0_c0_generic.py")
INTERFACE = HERE / "results_d0_pivot_zero_interface.json"
SYMMETRY = HERE / "results_d0_pivot_zero_symmetry.json"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def logical_hash(value):
    return sha256(json.dumps(value, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def load():
    spec = importlib.util.spec_from_file_location("d0_delta_scope_source", GENERIC)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    require(spec.loader is not None, "source loader missing")
    spec.loader.exec_module(module)
    return module


def parse(sp, value):
    return sp.sympify(value.replace("^", "**"))


def encode(sp, value):
    return str(sp.expand(value)).replace("**", "^")


def main():
    P = load()
    sp = P.sp
    interface = json.loads(INTERFACE.read_text())
    interface_hash = interface.pop("logical_sha256")
    require(logical_hash(interface) == interface_hash, "interface digest mismatch")
    symmetry = json.loads(SYMMETRY.read_text())
    symmetry_hash = symmetry.pop("logical_sha256")
    require(logical_hash(symmetry) == symmetry_hash, "symmetry digest mismatch")

    source = P.SOURCE
    raw_rows, _ = source.SOURCE.data()
    rows = {label: source.expression(poly) for label, poly, _ in raw_rows}
    b0, b1, b3, d1, d3, d4 = source.PARAMETERS
    upper = [rows[f"cofactor_{edge}_0"] for edge in range(1, 5)]
    upper_matrix, _ = sp.linear_eq_to_matrix(upper, source.P)
    delta = b1*d3 + b3*d1*d4
    expected_upper = 4*b0**2*b1*b3*d1*d3*d4*delta**2
    require(sp.expand(upper_matrix.det()-expected_upper) == 0,
            "upper Cramer determinant changed")
    p_solution = sp.solve(upper, source.P, dict=True, simplify=False)[0]
    d0 = {d3: -d1*d4}

    def endpoint_core(label):
        top = sp.cancel(rows[label].subs(p_solution).subs(d0)) \
            .as_numer_denom()[0]
        return max((factor for factor, _ in sp.factor_list(top)[1]),
                   key=lambda value:
                   len(sp.Poly(value, b0, b1, b3, d1, d4).terms()))

    endpoint_rows = [endpoint_core(label)
                     for label in ("cofactor_0_0", "cofactor_5_0")]
    endpoint_matrix, _ = sp.linear_eq_to_matrix(endpoint_rows, [b1, b3])
    c0 = b0**2+d4**2
    require(sp.factor(endpoint_matrix.det()) == -2*b0*d1*c0,
            "endpoint determinant changed")
    endpoint = sp.solve(endpoint_rows, [b1, b3], dict=True,
                        simplify=False)[0]
    delta_reduced = sp.cancel(delta.subs(d0).subs(endpoint))
    numerator, denominator = map(sp.factor, delta_reduced.as_numer_denom())
    r_records = interface["coefficient_pivot"]["C0_open_residual_factors"]
    R3 = parse(sp, r_records[3]["polynomial"])
    require(sp.expand(numerator-d4*R3) == 0 and
            sp.expand(denominator-2*b0*c0) == 0,
            "Delta-to-R3 exact relation changed")

    # Source-admissible minimal pairs after imposing the ambient Delta!=0
    # condition, hence R3!=0 on the base-open endpoint chart.
    original_pairs = {tuple(pair) for pair in symmetry["minimal_pairs"]}
    corrected_pairs = {pair for pair in original_pairs if "R3" not in pair}
    expected_pairs = {("R0", "R1"), ("R0", "R2"), ("R0", "S42"),
                      ("R1", "S256"), ("R2", "S256")}
    require(corrected_pairs == expected_pairs, "corrected pair cover changed")
    corrected_orbits = [
        [["R0", "R1"], ["R0", "R2"]],
        [["R0", "S42"]],
        [["R1", "S256"], ["R2", "S256"]],
    ]

    result = {
        "status": "exact Delta-live correction of D0 pivot-zero cover PASS",
        "source": {"path": str(GENERIC),
                   "sha256": sha256(GENERIC.read_bytes()).hexdigest()},
        "interface_logical_sha256": interface_hash,
        "symmetry_logical_sha256": symmetry_hash,
        "upper_Cramer_determinant": encode(sp, expected_upper),
        "endpoint_determinant": encode(sp, -2*b0*d1*c0),
        "exact_reduced_Delta": {
            "formula": "Delta=d4*R3/(2*b0*C0)",
            "numerator": encode(sp, numerator),
            "denominator": encode(sp, denominator),
        },
        "ambient_consequence": ("Delta!=0 and b0*d4*C0!=0 force R3!=0. "
                                "Any R3=0 branch belongs to the separately "
                                "retained Delta=0/upper-Cramer boundary."),
        "aborted_gate": ("R0=R3 was not launched: the pre-pivot row evaluation "
                         "correctly encountered R3 as an upper-solve denominator."),
        "source_admissible_minimal_pairs": [list(pair)
                                            for pair in sorted(corrected_pairs)],
        "source_admissible_pair_orbits": corrected_orbits,
        "source_admissible_pair_count": len(corrected_pairs),
        "source_admissible_orbit_count": len(corrected_orbits),
        "scope_guard": ("This removes only factors excluded by the already-declared "
                        "Delta-live ambient chart. It proves no remaining pair empty."),
        "mutation_control": ("Dropping Delta from the upper determinant incorrectly "
                             "restores the two inadmissible R3 pair branches."),
    }
    result["logical_sha256"] = logical_hash(result)
    (HERE / "results_d0_pivot_zero_delta_scope.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("D0 pivot-zero Delta-scope correction PASS", result["logical_sha256"])
    print("Delta = d4*R3/(2*b0*C0)")
    print("admissible orbits", corrected_orbits)


if __name__ == "__main__":
    main()
