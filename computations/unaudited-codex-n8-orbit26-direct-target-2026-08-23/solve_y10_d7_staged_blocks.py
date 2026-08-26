#!/usr/bin/env python3
"""Exact target-rooted y7 collision closure for total degree seven.

At total degree seven, the only genuinely new head beyond t times the full
degree-six Macaulay module consists of normalized originals multiplied by a
t-free encoded-y cubic.  Starting from every such column which touches a
homogeneous divisor of y10*t^2, close exact inverse incidence on y7, then
private-row peel the closed components.  Injectivity of this head, together
with the frozen degree-six standardness theorem, proves target standardness
through total degree seven.
"""

from collections import defaultdict
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
STAGE6_PATH = HERE / "solve_y10_d6_staged_blocks.py"
D6_RESULTS = HERE / "results_y10_d6_staged_blocks.json"
D7_RESULTS = HERE / "results_y10_dead_row_complete_d7.json"
RESULTS = HERE / "results_y10_d7_staged_blocks.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


spec = importlib.util.spec_from_file_location("y10_d7_stage6", STAGE6_PATH)
STAGE6 = importlib.util.module_from_spec(spec)
require(spec.loader is not None, "cannot load staged d6 checker")
spec.loader.exec_module(STAGE6)
FIRST = STAGE6.FIRST


def main():
    d6 = json.loads(D6_RESULTS.read_text())
    require(d6["status"] == "EXACT_TARGET_STANDARD_THROUGH_TOTAL_D6"
            and d6["logical_sha256"]
            == "62646275d6847e4f2044a337b6fcf23a37eda7368a57876a259b53d40f75c4db",
            "frozen d6 standardness theorem changed")
    incident = json.loads(D7_RESULTS.read_text())
    require(incident["logical_sha256"]
            == "e1f2b83734e78497104db89da08d2ead950c2f20ae3f40fc6327117fe6dc7815",
            "homogeneous d7 incidence census changed")

    originals, _lead_to_code = FIRST.original_basis()
    top_term_to_codes = defaultdict(list)
    top_occurrences = 0
    for code, polynomial in originals.items():
        for row, coefficient in polynomial.items():
            if len(row) == 4:
                top_term_to_codes[row].append((code, coefficient))
                top_occurrences += 1
    require(top_occurrences == 567_338, "original top occurrence census changed")

    seeds = set()
    seed_target_rows = defaultdict(set)
    original_target_rows = set()
    degree5_target_rows = set()
    for record in incident["incident_records"]:
        rows = {bytes.fromhex(item[0]) for item in record["target_rows"]}
        if record["kind"] == "original_times_homogeneous_d3":
            original_target_rows.update(rows)
            multiplier = bytes.fromhex(record["multiplier_y"])
            if len(multiplier) == 3:
                key = (record["source_code"], multiplier)
                seeds.add(key)
                seed_target_rows[key].update(rows)
        else:
            degree5_target_rows.update(rows)
    require(degree5_target_rows <= original_target_rows,
            "redundant d5 packet introduced a new target row")
    require(len(seeds) == 181, "d7 t-free cubic seed census changed")

    columns, rows, column_to_rows, row_to_columns = STAGE6.close_top_layer(
        seeds, originals, top_term_to_codes, 3
    )
    pivots, residual_columns = STAGE6.singleton_column_peel(
        column_to_rows, row_to_columns
    )
    require(not residual_columns,
            "the target-rooted y7 packet retained a collision core")

    # All target divisors actually touched at this degree are shorter than
    # y7.  Injectivity therefore forces every coefficient in the t-free y3
    # components which could contribute to them to vanish.  Everything else
    # is t times the already-certified full degree-six module.
    require(not any(len(row) == 7 for row in original_target_rows),
            "a t-free target divisor gained direct incidence")
    result = {
        "format": "n8-orbit26-y10-d7-staged-top-closure-v1",
        "status": "EXACT_TARGET_STANDARD_THROUGH_TOTAL_D7",
        "target_y10_row": incident["target_y10_row"],
        "target_total_degree": incident["target_total_degree"],
        "target_t_exponent": incident["target_t_exponent"],
        "homogeneous_d7_divisors": incident["distinct_degree7_divisors"],
        "incident_target_rows": incident["incident_target_rows"],
        "new_t_free_y3_seed_columns": len(seeds),
        "closed_y7_columns": len(columns),
        "closed_y7_rows": len(rows),
        "singleton_pivot_columns": len(pivots),
        "singleton_residual_columns": len(residual_columns),
        "new_head_kernel_dimension": 0,
        "direct_y7_target_incidences": 0,
        "redundant_d5_rows_subset_original_rows": True,
        "column_digest": sha256(b"".join(
            code.to_bytes(2, "big") + multiplier
            for code, multiplier in sorted(columns)
        )).hexdigest(),
        "row_digest": sha256(b"".join(sorted(rows))).hexdigest(),
        "pivot_digest": sha256(b"".join(
            code.to_bytes(2, "big") + multiplier + row
            for (code, multiplier), row in pivots
        )).hexdigest(),
        "theorem": (
            "The only new non-t-multiple d7 columns are originals times t-free "
            "encoded-y cubics. Every such column capable of touching a target "
            "divisor lies in the exact inverse-incidence closure above, whose "
            "private-row ledger peels every column. Thus its y7 head is injective "
            "and contributes no lower target pivot. All remaining d7 columns lie "
            "in t times the full d6 module; multiplication by t preserves the "
            "frozen t-last order, and the target is already standard against every "
            "homogeneous d6 divisor. Hence it is standard through total d7."
        ),
        "scope": (
            "exact target-specific standardness through total degree seven for "
            "the frozen chart26 t-last order; no degree-eight claim"
        ),
        "source_sha256": {
            str(STAGE6_PATH.relative_to(HERE.parents[1])):
                sha256(STAGE6_PATH.read_bytes()).hexdigest(),
            str(D7_RESULTS.relative_to(HERE.parents[1])):
                sha256(D7_RESULTS.read_bytes()).hexdigest(),
        },
    }
    encoded = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    RESULTS.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("y10 d7 staged y7 closure: PASS")
    print("seeds/columns/rows/pivots/residual:", len(seeds), len(columns),
          len(rows), len(pivots), len(residual_columns))
    print("logical sha256:", result["logical_sha256"])


if __name__ == "__main__":
    main()
