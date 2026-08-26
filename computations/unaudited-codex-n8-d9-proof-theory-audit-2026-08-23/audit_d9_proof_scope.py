#!/usr/bin/env python3
"""Freeze the proof-theoretic scope of chart-26 standardness through d9."""

from __future__ import annotations

from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
D9 = ROOT / "computations/unaudited-codex-n8-orbit26-direct-target-2026-08-23/results_y10_d9_referee.json"
D8 = ROOT / "computations/unaudited-codex-n8-orbit26-direct-target-2026-08-23/results_y10_d8_terminal.json"
C10 = ROOT / "computations/unaudited-codex-n8-orbit26-direct-target-2026-08-23/results_full_y10_aggregate.json"
LOCALIZATION = ROOT / "notes/n8-support-normalization-is-exact-localization.md"
RESULT = HERE / "results_d9_proof_scope.json"
EXPECTED = {
    D9: "41824c9eee8bae21808101a6140051ff2e4e01226f518b0ddf8140b1268a9d2e",
    D8: "5bfd5a482d0a53f933c7456d5847b952e58574356c55ae96a9e50d6c941af4f0",
    C10: "fa0bf7ae3d50d232450c0ea3188bd4aad6f6f4b4513d014899b4e1edf67949ed",
    LOCALIZATION: "9aa2d27841666d9819d063d65a46a253f5ebfc47d97a64b3cff28dacfb69ddef",
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def target_divisors(target, total_degree, target_total_degree=12):
    answer = {}
    for t_exponent in range(3):
        y_degree = total_degree - t_exponent
        if not 0 <= y_degree <= len(target):
            continue
        rows = {
            bytes(target[index] for index in positions)
            for positions in combinations(range(len(target)), y_degree)
        }
        if t_exponent <= target_total_degree - len(target):
            answer[t_exponent] = len(rows)
    return answer


def audit(mutate=False):
    for path, digest in EXPECTED.items():
        require(sha256(path.read_bytes()).hexdigest() == digest,
                f"source drift: {path}")
    d9 = json.loads(D9.read_text())
    d8 = json.loads(D8.read_text())
    c10 = json.loads(C10.read_text())
    require(d9["status"] == "EXACT_TARGET_STANDARD_THROUGH_TOTAL_D9"
            and d9["logical_sha256"]
            == "34eaef652c9c8808c0b2a00e26f122b55fbffb74df93fcf2e9547658b32b976e",
            "d9 authority changed")
    require(d8["status"] == "EXACT_TARGET_STANDARD_THROUGH_TOTAL_D8"
            and c10["status"] == "EXACT_CHOSEN_RIGHT_INVERSE_DEAD_AT_Y10"
            and "not nonmembership" in c10["nonclaim"],
            "downstream scope guard changed")
    target = bytes.fromhex(c10["PM4_incidence"]["lex_dead_row"])
    require(target.hex() == "0111202020494f4f50f8"
            and c10["PM4_incidence"]["lex_dead_coefficient"] == -4,
            "C10 target coordinate changed")
    remaining = {
        str(degree): {str(t): count for t, count
                      in target_divisors(target, degree).items()}
        for degree in range(10, 13)
    }
    require(remaining == {
        "10": {"0": 1, "1": 7, "2": 23},
        "11": {"1": 1, "2": 7},
        "12": {"2": 1},
    }, "remaining target-divisor census changed")
    if mutate:
        remaining["10"]["0"] += 1
    require(remaining["10"]["0"] == 1,
            "hostile remaining-degree mutation survived")

    result = {
        "format": "n8-d9-proof-theoretic-scope-audit-v1",
        "status": "D9_IS_LOCAL_STANDARDNESS_ONLY_D10_D12_AND_SATURATION_REMAIN",
        "target_monomial": target.hex() + "*t^2",
        "proved": (
            "In the frozen chart26 homogeneous mixed ideal and t-last order, "
            "no initial monomial of total degree at most nine divides the "
            "selected monomial T. Equivalently T survives division by every "
            "target-relevant homogeneous relation certified through d9."
        ),
        "not_proved": [
            "T is standard for the full initial ideal",
            "the coefficient -4 survives the complete normal form of the 140185881-term C10 representative",
            "C10 or the normalized pure product is outside the homogeneous ideal",
            "the chart26 localized mixed ideal is proper or has a common zero",
            "any statement for the other 30 pure-matching-triple chart orbits",
            "global X5 feasibility or the N8,d3 conjecture",
        ],
        "remaining_fixed_degree12_checks": {
            "degrees": [10, 11, 12],
            "target_divisors_by_degree_and_t_exponent": remaining,
            "new_t_free_multiplier_degrees": {"10": 6, "11": 7, "12": 8},
            "logic": (
                "positive-t degree-d slices reduce to t*M_(d-1), but each d "
                "has a new t-free head whose kernel can descend to a target "
                "tail. These heads are not controlled by d9."
            ),
        },
        "term_order_verdict": (
            "Standard monomials form a divisor-closed order ideal, which gives "
            "only downward propagation. There is no upward lemma: a minimal "
            "generator of in(I) of degree 10, 11, or 12 may still divide T. "
            "D9 would imply the rest only with an additional bound such as "
            "reg(I)<=9 or generation of in(I) through degree9; neither is frozen."
        ),
        "elementary_counterguard": (
            "For the homogeneous ideal J=<x^10> and T=x^10*t^2, T has no "
            "initial-ideal divisor through degree9 but fails at degree10. Thus "
            "finite target degree does not turn d9 standardness into d12 standardness."
        ),
        "C10_scope": (
            "C10 is the residual of one specified deterministic monic right "
            "inverse through y9. Its own frozen artifact explicitly says that "
            "alternative lower-kernel choices may change C10. Standardness of "
            "one selected coordinate through d9 is not a full-row Macaulay "
            "separator and does not yet make the residual coefficient canonical."
        ),
        "chart26_and_global_scope": (
            "A positive degree12 membership certificate for the normalized pure "
            "product would be useful on the orbit26 Laurent chart. A negative "
            "fixed-degree result would still not prove affine/localized "
            "nonmembership without t-saturation: dehomogenized membership is "
            "equivalent to t^k*F^h membership for some k. It also would not cover "
            "the other 30 chart orbits or prove existence of an X5 point."
        ),
        "source_sha256": {str(path.relative_to(ROOT)): digest
                          for path, digest in EXPECTED.items()},
    }
    result["logical_sha256"] = sha256(json.dumps(
        result, sort_keys=True, separators=(",", ":")
    ).encode("ascii")).hexdigest()
    return result


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--check-results", action="store_true")
    parser.add_argument("--mutate", action="store_true")
    args = parser.parse_args()
    result = audit(args.mutate)
    if args.write_results:
        RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    if args.check_results:
        require(RESULT.exists() and json.loads(RESULT.read_text()) == result,
                "stored result changed")
    print(result["status"])
    print("remaining", result["remaining_fixed_degree12_checks"]
          ["target_divisors_by_degree_and_t_exponent"])
    print("logical", result["logical_sha256"])


if __name__ == "__main__":
    main()
