#!/usr/bin/env python3
"""Exact K19 recurrence/interface audit; constructs no K19 rows."""
from hashlib import sha256
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RUN = ROOT / "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23"
K16 = RUN / "results_filtered_k16_run.json"
K17 = RUN / "results_filtered_k17_run.json"
K18 = (ROOT / "computations/unaudited-codex-orbit0-filtered-k18-charge-2026-08-23"
       / "results_k18_charge.json")
K14 = (ROOT / "computations/unaudited-codex-orbit0-k16-literal-collection-2026-08-22"
       / "results_orbit0_k16_literal_residual.json")
OUT = HERE / "results_filtered_k19_interface.json"
S = 281_801_520

def digest(p):
    return sha256(p.read_bytes()).hexdigest()

def main(write=False):
    k16, k17, k18, k14 = [json.loads(p.read_text()) for p in (K16,K17,K18,K14)]
    assert k16["K16_checkpoint"]["removed_pivotable"][0] == 24_003_767
    assert k17["scope"].startswith("Only the K17 normal is computed")
    assert k18["status"] == "PASS_EXACT_K18_CHARGE_ONLY_NO_ROW_COLLECTION"
    uses14 = k14["collection"]["literal_pivot_uses"]
    uses15 = 55_934_080              # exact all-available-pivot census
    uses16 = 129_939_187             # exact combined K16 row/pivot census

    direct19 = 485 * 3 * 32 * 60**2 # profiles 3+4+4
    from15 = uses15 * 60             # K4 tails
    from16 = uses16 * 32             # K3 tails

    # Full K17 source occurrences before its occurrence-wise pivotability filter.
    p17_direct = 485 * (6*12*32*60 + 32**3)
    p17_from14 = uses14 * 32
    p17_from15 = uses15 * 12
    assert p17_direct == 82_938_880
    assert p17_from14 == 211_816_960
    assert p17_from15 == 671_208_960
    # The Rust K17 driver only increments these two counters after child
    # pivotability filtering.  Direct's published raw counter is unconditional.
    kept14 = k17["components"]["K14_valid_average_K3"]["raw_irreducible_occurrences"]
    kept15 = k17["components"]["K15_all_pivot_average_K2"]["raw_irreducible_occurrences"]
    pivotable_precursor_upper = p17_direct + (p17_from14-kept14) + (p17_from15-kept15)
    from17_upper = pivotable_precursor_upper * 78 * 12
    hostile = (direct19 + from15 + from16 + from17_upper) * S*S * 8_448

    result = {
      "status": "PASS_EXACT_K19_INTERFACE_DESIGN_NO_K19_RUN",
      "convention": {
        "polynomial": "P=-R8prime*E0*E1*E2",
        "head_reduction": "a+tail=0, hence a parent coefficient c emits -c/m on each tail for m chosen pivots",
        "K16_combination": "direct minus frozen K14/K2 collector",
        "K17_combination": "direct plus K14/K3 response plus K15/K2 response; frozen K17 files retain only irreducible children",
      },
      "lineages": [
        {"name":"direct_K19_344", "sign":"negative", "denominator_depth":0,
         "raw_occurrences_exact":direct19},
        {"name":"K15_direct_to_K19_K4", "sign":"positive", "denominator_depth":1,
         "parent_pivot_uses_exact":uses15, "raw_occurrences_exact":from15},
        {"name":"K16_direct_to_K19_K3", "sign":"positive", "denominator_depth":1,
         "combined_with_next_line_before_reduction":True},
        {"name":"K14_to_K16_K2_then_K16_to_K19_K3", "sign":"negative",
         "denominator_depth":2, "combined_K16_parent_pivot_uses_exact":uses16,
         "combined_K16_raw_occurrences_exact":from16},
        {"name":"direct_K17_to_K19_K2", "sign":"positive", "denominator_depth":1,
         "full_precursor_occurrences":p17_direct},
        {"name":"K14_to_K17_K3_then_K17_to_K19_K2", "sign":"negative",
         "denominator_depth":2, "full_precursor_occurrences":p17_from14,
         "known_irreducible_precursor_occurrences":kept14},
        {"name":"K15_to_K17_K2_then_K17_to_K19_K2", "sign":"negative",
         "denominator_depth":2, "full_precursor_occurrences":p17_from15,
         "known_irreducible_precursor_occurrences":kept15},
      ],
      "four_bucket_summary": {
        "direct_K19_exact": direct19,
        "K15_K4_exact": from15,
        "K16_K3_exact": from16,
        "K17_K2_exact": None,
        "K17_K2_reason_missing": (
          "checkpoint_reduced_k17.bin and its three component checkpoints contain "
          "only nonpivotable K17 children.  The omitted pivotable aggregate, needed "
          "to count its available pivots and emit K2 tails, was not frozen."
        ),
        "K17_precursor_occurrences_full": p17_direct+p17_from14+p17_from15,
        "K17_pivotable_precursor_occurrences_upper": pivotable_precursor_upper,
        "K17_K2_raw_occurrences_upper": from17_upper,
      },
      "denominators": {
        "uniform_integer_scale_sufficient": S*S,
        "reason": "No K19 lineage contains more than two successive pivot averages; S clears every possible single 78-pivot count.",
        "hostile_i128_absolute_bound": hostile,
        "i128_safety_margin_floor": (2**127-1)//hostile,
      },
      "smallest_sound_next_step": {
        "type":"charge-only source-linear replay, not row collection",
        "required_reconstruction": (
          "Re-enumerate the three literal K17 precursor streams before filtering; "
          "for each pivotable child apply the all-available-pivot K2 response. "
          "Linearity permits separate lineage streams even when rows collide."
        ),
        "cache_key": (
          "K17 child anchor signature + outgoing pivot + labelled eight-endpoint "
          "path lengths/partners + closed-cycle multiset"
        ),
        "feasibility": (
          "Arithmetic fits i128 at scale S^2, but feasibility is not yet certified: "
          "up to 731,799,040 pivotable precursor occurrences and 684,963,901,440 "
          "uncached K2 tail occurrences remain. First run a profile-only unique-key "
          "census with a 180s/8GB hard gate."
        ),
      },
      "scope": "Interface/sign/denominator/cost audit only; no K19 row or charge computation.",
      "pinned": {str(p.relative_to(ROOT)):digest(p) for p in (K14,K16,K17,K18)},
    }
    logical=sha256(json.dumps(result,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    result["logical_sha256"]=logical
    if write: OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"status":result["status"],"exact_first_three":[direct19,from15,from16],
                      "K17_K2_upper":from17_upper,"logical_sha256":logical},indent=2))

if __name__ == "__main__":
    import sys
    main("--write-results" in sys.argv)
