#!/usr/bin/env python3
"""Prove the closed all-h value of the actual Gram projector composite.

The matching and endpoint projectors were proved spectrally, but their
composition on the literal all-role Gram row had only been executed at
h=3,4.  The missing uniform calculation is elementary once the insertion
charts are counted with their actual multiplicities.

For a marked occurrence f=(p_f,s_f,F) and g=(p,s,R), the literal Gram row is

    k_f(g) = |F intersect R| + C_(p,s),

where C is 4h^2+4h at the marked ordered endpoints, 2h-1 when exactly the
marked p- or s-endpoint is retained, and zero otherwise.  The residual
two-switch numerator sends this to

    q_(p,s) + (2h-1) C_(p,s),

with q the number of marked residual edges avoiding p,s.  The endpoint
cubic then sends this actual row to the constant

    56 h^3 (2h-1)

for every h>=2.  This closes the coefficient/evidence gap only; the
augmented physical Cartan/Hasse totalization remains open.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_centered_occurrence_full_endpoint_transfer_gate.py":
        "6f5686298143b584a4edcb350145bf9d648277972aa96b90443c4ce254cb1d30",
    "notes/uniform-centered-occurrence-full-endpoint-transfer-gate.md":
        "9c363714cc24c7ac17aa08c1260dc36c9c63cc794132817ecb59106685dd59db",
    "computations/verify_uniform_centered_occurrence_matching_eigenspace_correction.py":
        "6e9c665e2c42b23e1910963b030de2f6c4b16dfe4951eae6e0e79b7fcf1e6921",
    "notes/uniform-centered-occurrence-matching-eigenspace-correction.md":
        "914a5ae493f78bdab7fa88bfcafd5e80254709a7f373d8bade0f70660dfb8f3f",
    "computations/verify_uniform_centered_occurrence_endpoint_association_projector.py":
        "0ef88312cead100120e4600ea3a2d0616262a96bf27726d07817610d11b43f59",
    "notes/uniform-centered-occurrence-endpoint-association-projector.md":
        "6be3edc16be3b429f517fe007886fd3289281f8e8acdde1f13ebebf2a20bb836",
    "computations/audit_external_spine2_claims.py":
        "ed39f9ca05841222db98132face3949b89839422500d77bfdc8c52545e7eab03",
    "notes/external-spine-audit-2-adversarial-readout.md":
        "6eed5b4a1cb6bae0fc298e5c0db28b7ebe74fc9b0aad6cc395060e5385350619",
}
EXPECTED_LEDGER_SHA256 = "2af217853fc91385eebf8587e0b3354a7ed0323dca530af3d6a6b39142e110fd"


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def chart_count_formula(h: int, marked, occurrence) -> tuple[int, int, int]:
    """Return t_F, C and their sum for the actual insertion-chart Gram row."""
    marked_p, marked_s, marked_matching = marked
    p_site, s_site, matching = occurrence
    common = len(set(marked_matching) & set(matching))
    if (p_site, s_site) == (marked_p, marked_s):
        endpoint = 4 * h * h + 4 * h
    elif p_site == marked_p or s_site == marked_s:
        endpoint = 2 * h - 1
    else:
        endpoint = 0
    return common, endpoint, common + endpoint


def literal_bounded_audit(base, matching, endpoint) -> dict[str, object]:
    records = []
    for h in (2, 3, 4):
        occurrences, marked, gram = matching.full_gram_row(h)
        lookup = {value: index for index, value in enumerate(occurrences)}
        vector = tuple(Q(gram[value]) for value in occurrences)

        # Check the uniform chart formula on every actual decorated
        # occurrence.  This includes the multiplicity 2h of the `both new
        # endpoints' chart, whose Gram contribution is 4h^2.
        formula = tuple(Q(chart_count_formula(h, marked, value)[2])
                        for value in occurrences)
        require(vector == formula,
                ("literal Gram chart formula changed", h))

        eigenvalue = Q(h * h - 3 * h + 1)
        matching_numerator = []
        matching_closed = []
        for occurrence in occurrences:
            p_site, s_site, residual = occurrence
            switched = sum((
                vector[lookup[(p_site, s_site, neighbor)]]
                for neighbor in matching.switch_neighbors(residual)
            ), Q(0))
            matching_numerator.append(
                switched - eigenvalue * vector[lookup[occurrence]])

            _common, endpoint_constant, _value = chart_count_formula(
                h, marked, occurrence)
            q_value = sum(
                int(p_site not in edge and s_site not in edge)
                for edge in marked[2]
            )
            matching_closed.append(
                Q(q_value + (2 * h - 1) * endpoint_constant))
        matching_numerator = tuple(matching_numerator)
        matching_closed = tuple(matching_closed)
        require(matching_numerator == matching_closed
                and matching_numerator == endpoint.matching_flat_row(
                    h, occurrences, marked),
                ("actual matching numerator formula changed", h))

        sites = tuple(range(2 * h + 2))
        endpoint_operator = lambda values: endpoint.apply_endpoint(
            values, occurrences, lookup, sites)
        projected = endpoint.polynomial_apply(
            matching_numerator, (-2, 2 * h - 2, 2 * h),
            endpoint_operator)
        predicted = Q(56 * h**3 * (2 * h - 1))
        require(set(projected) == {predicted},
                ("actual composite constant changed", h,
                 set(projected), predicted))
        records.append({
            "h": h,
            "literal_occurrences": len(occurrences),
            "actual_Gram_formula_checked_on_every_occurrence": True,
            "matching_numerator_matches_closed_formula": True,
            "endpoint_composite_constant": int(predicted),
        })
    return {
        "literal_orders": records,
        "h3_previous_constant": 7560,
        "h4_previous_constant": 25088,
        "both_recovered_by_closed_formula": True,
    }


def uniform_symbolic_audit() -> dict[str, object]:
    records = []
    for h in range(2, 1001):
        n = 2 * h + 2
        ordered_pairs = n * (n - 1)

        # Sum q_(p,s) by fixing one of the h marked residual edges: the
        # ordered endpoints can be any two distinct sites outside that edge.
        q_sum = h * (n - 2) * (n - 3)

        # There is one marked ordered pair and 2(n-2)=4h pairs sharing the
        # marked p or marked s in the correct orientation.
        endpoint_sum = (4 * h * h + 4 * h) + 4 * h * (2 * h - 1)
        require(endpoint_sum == 12 * h * h,
                ("endpoint constant sum changed", h))
        matching_flat_sum = q_sum + (2 * h - 1) * endpoint_sum
        require(matching_flat_sum == 14 * h * h * (2 * h - 1),
                ("matching-flat augmentation changed", h))
        mean = Q(matching_flat_sum, ordered_pairs)
        require(mean == Q(7 * h * h * (2 * h - 1),
                          (h + 1) * (2 * h + 1)),
                ("matching-flat mean changed", h))

        # The endpoint cubic kills every nonconstant ordered-pair sector.
        # Its value on the constant sector B=4h is P_h(4h).
        endpoint_eigenvalue = 4 * h
        cubic_constant = ((endpoint_eigenvalue + 2)
                          * (endpoint_eigenvalue - (2 * h - 2))
                          * (endpoint_eigenvalue - 2 * h))
        require(cubic_constant == 8 * h * (h + 1) * (2 * h + 1),
                ("endpoint cubic normalization changed", h))
        output = mean * cubic_constant
        require(output == 56 * h**3 * (2 * h - 1),
                ("closed composite formula changed", h, output))
        if h <= 8 or h in (10, 20, 50, 100, 1000):
            records.append({
                "h": h,
                "ordered_pairs": ordered_pairs,
                "sum_q": q_sum,
                "sum_C": endpoint_sum,
                "P_h(4h)": cubic_constant,
                "output": int(output),
            })
    return {
        "actual_Gram_formula": "k_f(g)=|F intersect R|+C_(p,s)",
        "chart_contributions": {
            "residual charts": "one indicator for each common marked edge",
            "one new p endpoint": "2h or 2h-1 according to the s endpoint",
            "one new s endpoint": "2h or 2h-1 according to the p endpoint",
            "both new endpoints": "multiplicity product (2h)^2=4h^2",
        },
        "matching_numerator":
            "(A_h-(h^2-3h+1)I)k_f=q_(p,s)+(2h-1)C_(p,s)",
        "matching_flat_sum": "14h^2(2h-1)",
        "ordered_pair_count": "(2h+2)(2h+1)",
        "endpoint_cubic_constant_eigenvalue": "8h(h+1)(2h+1)",
        "closed_actual_composite": "56h^3(2h-1) times the constant row",
        "nonzero_for_every_h_at_least_2": True,
        "symbolic_integer_orders_checked": "2<=h<=1000",
        "sample_records": records,
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    base = load(
        "computations/verify_uniform_centered_occurrence_full_endpoint_transfer_gate.py",
        "actual_gram_composite_base",
    )
    matching = load(
        "computations/verify_uniform_centered_occurrence_matching_eigenspace_correction.py",
        "actual_gram_composite_matching",
    )
    endpoint = load(
        "computations/verify_uniform_centered_occurrence_endpoint_association_projector.py",
        "actual_gram_composite_endpoint",
    )
    ledger = {
        "theorem": "uniform actual-Gram matching/endpoint projector formula",
        "uniform_chart_and_spectral_calculation": uniform_symbolic_audit(),
        "literal_bounded_crosscheck": literal_bounded_audit(
            base, matching, endpoint),
        "verdict": (
            "The actual all-role Gram row has the uniform literal chart formula "
            "k_f(g)=|F intersect R|+C_(p,s).  The matching numerator and "
            "endpoint cubic therefore compose to the nonzero constant "
            "56h^3(2h-1) for every h>=2.  This replaces the prior h=3,4-only "
            "execution by a closed all-order coefficient proof.  It does not "
            "construct the augmented physical two-switch/endpoint/mixed cubic "
            "totalization."
        ),
        "scope": (
            "exact coefficient theorem for the literal all-role insertion Gram "
            "row; physical word/fine/repeated, target, residue, q, anchor, W, "
            "ridge, eta/sigma and terminal lifting remain separate"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    return ledger, digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()
    ledger, digest = audit()
    require(digest == EXPECTED_LEDGER_SHA256,
            ("actual Gram projector ledger changed", digest))
    if arguments.json:
        print(json.dumps({"ledger": ledger, "sha256": digest},
                         indent=2, sort_keys=True))
    else:
        print("uniform actual-Gram projector composite: PASS")
        print("literal Gram formula: |F intersect R| + C_(p,s)")
        print("closed output: 56*h^3*(2h-1) times the constant row")
        print("physical augmented cubic totalization: STILL OPEN")
        print(f"ledger sha256 {digest}")


if __name__ == "__main__":
    main()
