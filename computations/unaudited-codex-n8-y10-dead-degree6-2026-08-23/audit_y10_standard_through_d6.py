#!/usr/bin/env python3
"""Exact staged proof that the lex y10*t2 row is standard through d6."""

from fractions import Fraction
from hashlib import sha256
from itertools import combinations
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PROBE = HERE / "probe_y10_degree6_prefix.py"
CENSUS = ROOT / "computations/verify_n8_chart26_weighted_degree6_census.py"
RESULT = HERE / "results_y10_standard_through_d6.json"
TARGET = bytes.fromhex("0111202020494f4f50f8")


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, f"cannot load {path}")
    spec.loader.exec_module(module)
    return module


def divisors(row, degree):
    return {bytes(row[index] for index in positions)
            for positions in combinations(range(len(row)), degree)}


def add_value(vector, row, value):
    value = vector.get(row, Fraction(0)) + value
    if value:
        vector[row] = value
    else:
        vector.pop(row, None)


def exact_degree5_elimination(originals, keys):
    pivots = {}
    tails = []
    for code, multiplier_hex in keys:
        multiplier = bytes.fromhex(multiplier_hex)
        work = {}
        for row, coefficient in originals[code].items():
            add_value(work, bytes(sorted(row + multiplier)), Fraction(coefficient))
        while True:
            active = [row for row in work if len(row) == 5]
            if not active:
                if work:
                    tails.append(work)
                break
            lead = min(active)
            reducer = pivots.get(lead)
            if reducer is None:
                scale = work[lead]
                work = {row: value / scale for row, value in work.items()}
                pivots[lead] = work
                break
            scale = work[lead]
            for row, coefficient in reducer.items():
                add_value(work, row, -scale * coefficient)
    return pivots, tails


def audit(mutate=False):
    P = load(PROBE, "y10_d6_probe")
    M = load(CENSUS, "y10_d6_census")
    probe = P.audit(1009)
    require(probe["status"] == "Y5_CLOSED", "target-rooted closure did not close")
    require({key: probe[key] for key in (
        "grades", "grade_columns", "top6_pivots", "top6_kernel_tails",
        "direct5", "generators5", "rank5", "tails4", "rows5"
    )} == {
        "grades": 211,
        "grade_columns": 3002,
        "top6_pivots": 3002,
        "top6_kernel_tails": 0,
        "direct5": 22,
        "generators5": 22,
        "rank5": 22,
        "tails4": 0,
        "rows5": 1629,
    }, "target-rooted staged closure profile changed")
    require(not probe["target_y5_pivots"], "a modular target y5 pivot appeared")

    originals, degree4, _code_to_lead, degree5, _words = M.build_leads()
    candidates = {degree: divisors(TARGET, degree) for degree in (4, 5, 6)}
    require({degree: len(rows) for degree, rows in candidates.items()}
            == {4: 72, 5: 82, 6: 72}, "226-divisor census changed")
    d4_hits = sorted(set(degree4) & candidates[4])
    d5_hits = sorted(set(degree5) & candidates[5])
    require(not d4_hits and not d5_hits,
            "a completed d4/d5 lead divides the target")

    # Exact-Q replay of the only degree-five tail component exposed after the
    # y6 blocks.  Full column rank modulo 1009 already proves the y6 block
    # ranks over Q; here the smaller descended component is replayed literally.
    pivots_Q, tails_Q = exact_degree5_elimination(
        originals, probe["direct5_keys"]
    )
    q_pivots_Q = sorted(row.hex() for row in candidates[5] if row in pivots_Q)
    require(len(pivots_Q) == 22 and not tails_Q and not q_pivots_Q,
            "exact-Q y5 tail component changed")
    require(sorted(row.hex() for row in pivots_Q) == probe["pivot5_rows"],
            "exact-Q/modular y5 pivot rows differ")

    # A t-free source term contains a four-edge perfect matching, hence all
    # eight sites.  Every target divisor misses site 5, so no y6 source row can
    # equal any q.  This is the conceptual zero-incidence theorem.
    coordinates = M.D5.COORDINATES
    target_sites = {site for value in TARGET for site in coordinates[value][:2]}
    require(target_sites == {0, 1, 2, 3, 4, 6, 7},
            "target physical shore changed")
    require(all({site for value in lead for site in coordinates[value][:2]}
                == set(range(8)) for lead in degree4),
            "a t-free original lead stopped spanning all sites")

    if mutate:
        d5_hits.append(b"hostile")
    require(not d5_hits, "hostile target divisor mutation survived")

    result = {
        "format": "n8-chart26-y10-t2-standard-through-d6-v1",
        "status": "EXACT_STANDARD_THROUGH_TOTAL_DEGREE6",
        "target": TARGET.hex(),
        "target_total_degree": 12,
        "target_y_degree": 10,
        "target_t_exponent": 2,
        "target_missing_physical_sites": [5],
        "total_degree6_divisors": {
            "y4_t2": len(candidates[4]),
            "y5_t1": len(candidates[5]),
            "y6_t0": len(candidates[6]),
            "total": sum(map(len, candidates.values())),
        },
        "completed_lower_leads": {
            "degree4": len(degree4),
            "degree5": len(degree5),
            "target_divisors_hit": 0,
        },
        "target_rooted_y6_stage": {
            "fine_grades": probe["grades"],
            "columns": probe["grade_columns"],
            "rank_mod_1009": probe["top6_pivots"],
            "Q_rank": probe["grade_columns"],
            "why_Q": "full column rank modulo 1009 implies full column rank over Q",
            "kernel_tails_to_y5": probe["top6_kernel_tails"],
            "target_y6_incidence": 0,
            "zero_incidence_reason": (
                "every t-free source monomial contains a full matching on all "
                "eight sites, whereas every target divisor misses site 5"
            ),
        },
        "descended_y5_stage": {
            "target_rooted_rows": probe["rows5"],
            "columns": probe["direct5"],
            "rank_over_Q": len(pivots_Q),
            "kernel_tails_to_y4": len(tails_Q),
            "target_pivots": q_pivots_Q,
            "exact_pivot_rows": sorted(row.hex() for row in pivots_Q),
        },
        "y4_stage": {
            "new_descended_columns": 0,
            "remaining_module": "t^2 times the original degree4 module",
            "target_degree4_lead_hits": len(d4_hits),
        },
        "theorem": (
            "None of the 226 total-degree-six divisors of y10*t2 is a pivot "
            "after exact target-rooted prefix reduction. Therefore the lex dead "
            "monomial is standard through the complete degree-six layer."
        ),
        "scope": (
            "exact standardness through total degree6 in the normalized t-last "
            "homogeneous ideal; degree7+ pivots and all-order t-saturation remain open"
        ),
        "source_sha256": {
            str(PROBE.relative_to(ROOT)): sha256(PROBE.read_bytes()).hexdigest(),
            str(CENSUS.relative_to(ROOT)): sha256(CENSUS.read_bytes()).hexdigest(),
        },
    }
    result["logical_sha256"] = sha256(json.dumps(
        result, sort_keys=True, separators=(",", ":")
    ).encode("ascii")).hexdigest()
    return result


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--mutate", action="store_true")
    args = parser.parse_args()
    result = audit(args.mutate)
    if not args.mutate:
        RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n",
                          encoding="ascii")
    print(json.dumps({key: result[key] for key in (
        "status", "total_degree6_divisors", "logical_sha256"
    )}, sort_keys=True))


if __name__ == "__main__":
    main()
