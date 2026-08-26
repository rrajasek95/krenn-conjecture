#!/usr/bin/env python3
"""AUDIT A6-B10: collate every b10_* result into one summary JSON."""
from __future__ import annotations

import json

HERE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-audit-a6-w15w14-2026-08-15")
W14 = ("/Users/rishi/workplace/krenn-conjecture/computations/"
       "unaudited-monochrome-w14-2026-08-15")
P2 = ("/Users/rishi/workplace/krenn-conjecture/computations/"
      "unaudited-witness-splitting-p2-2026-08-15")


def load(path, default=None):
    try:
        return json.load(open(path))
    except Exception:                                        # noqa: BLE001
        return default


def main():
    tab = load(HERE + "/b10_results_table.json")
    w14 = load(W14 + "/results_task3_rankone.json")
    p2 = load(P2 + "/results_a.json")
    stored = {(r["seed"], tuple(pr["pair"])): pr
              for r in p2["results"] for pr in r["pairs"]}

    rows = tab["rows"]
    feat = [r for r in rows if r["featured"]]
    wit = [r for r in rows if r["b10_general"]]
    blk = [r for r in rows if r["b10_general"] is False]
    vac = [r for r in wit if r["n_quadrics"] == 0]
    seeds = sorted({r["seed"] for r in rows})
    wit_seeds = sorted({r["seed"] for r in wit})

    summary = {
        "scope": {
            "pairs_recomputed": len(rows),
            "w14_pairs_claimed": w14["stats"]["checked"],
            "sources_actually_touched_by_w14": seeds,
            "w14_docstring_claims_results_slice": "data['results'][:70]",
            "note": ("W14's loop breaks at 120 checked pairs, which happens "
                     "inside seed 1008: only 9 of the 70 sources are sampled"),
            "skipped_pairs_all_explained_by_dead_s": True,
        },
        "replication": {
            "agree_general": tab["summary"]["agree_general"],
            "agree_rank_one": tab["summary"]["agree_rank_one"],
            "disagreements": [r for r in rows
                              if not (r["agree_general"]
                                      and r["agree_rank_one"])],
            "witness_pairs": len(wit), "blocked_pairs": len(blk),
            "witness_without_rank_one": tab["summary"][
                "witness_without_rank_one"],
            "blocked_with_rank_one": tab["summary"]["blocked_with_rank_one"],
            "rank_one_implies_general_violations": tab["summary"][
                "rank_one_implies_general_violations"],
        },
        "vacuity": {
            "witness_pairs_with_E_identically_zero": len(vac),
            "of_total_witness_pairs": len(wit),
            "comment": ("for these the rank-one query has an EMPTY quadric "
                        "ideal, so 'rank-one witness exists' is automatic and "
                        "carries no information"),
            "witness_pairs_live_on_seeds": wit_seeds,
            "comment2": ("all 29 witness pairs come from 3 of the 9 sources "
                         "(1002 lowrank, 1005 mixed, 1008 lowrank), so the "
                         "29/29 statistic is 3 independent random draws"),
        },
        "timing": {
            "max_general_query_sec": tab["summary"]["max_general_sec"],
            "max_rank_one_query_sec": tab["summary"]["max_rank_one_sec"],
            "total_sec_240_queries": tab["summary"]["total_sec"],
            "singular_timeout_used": 120,
            "queries_that_timed_out": tab["summary"]["non_ok_singular"],
            "w14_timeout_handling": ("run_singular raises on "
                                     "subprocess.TimeoutExpired; W14 wraps it "
                                     "in `except Exception: continue`, so a "
                                     "timeout SKIPS the pair silently (it is "
                                     "not counted as 'no witness' and not "
                                     "counted in stats['checked']) -- safe for "
                                     "the ratio but leaves no record"),
        },
        "controls": {
            "i_saturation": load(HERE + "/b10_controls.json", {}).get(
                "i_saturation", {}).get("n_changed"),
            "ii_mutations": {
                "addconst_flips": load(HERE + "/b10_controls.json", {}).get(
                    "ii_mutations", {}).get("n_addconst_flips"),
                "dropmatch_flips": load(HERE + "/b10_controls.json", {}).get(
                    "ii_mutations", {}).get("n_dropmatch_flips")},
            "iii_dim_convention": load(HERE + "/b10_controls.json", {}).get(
                "iii_dim_convention", {}).get("raw"),
            "iv_handmade": load(HERE + "/b10_controls.json", {}).get(
                "iv_handmade", {}).get("passes"),
            "extra": load(HERE + "/b10_controls_extra.json", {}).get("summary"),
        },
        "certificates": {
            "explicit_rational_rank_one_witnesses":
                load(HERE + "/b10_certificates.json", {}).get("found"),
            "plus_wider_search": load(HERE + "/b10_certificates2.json", []),
            "modp_consistency": load(HERE + "/b10_modp.json", {}).get(
                "all_consistent"),
            "modp_points": load(HERE + "/b10_modp_point.json", {}).get("rows"),
            "bad_prime": load(HERE + "/b10_badprime.json", {}),
        },
        "featured_table": [
            {"seed": r["seed"], "mode": r["mode"], "pair": r["pair"],
             "w14_label": ("witness + rank-one" if r["w14_witness"]
                           else "blocked, no rank-one"),
             "b10_general_witness": r["b10_general"],
             "b10_rank_one_witness": r["b10_rank_one"],
             "agreement": bool(r["agree_general"] and r["agree_rank_one"]),
             "n_quadrics": r["n_quadrics"], "p2_span": r["p2_span"],
             "sec_general": r["b10_general_sec"],
             "sec_rank_one": r["b10_rank_one_sec"]}
            for r in sorted(feat, key=lambda x: (not x["w14_witness"],
                                                 x["seed"], x["pair"]))],
    }
    json.dump(summary, open(HERE + "/b10_summary.json", "w"), indent=1,
              default=str)
    print(json.dumps(summary["scope"], indent=1))
    print(json.dumps(summary["replication"]["disagreements"], indent=1))
    print(json.dumps(summary["vacuity"], indent=1))
    print("wrote b10_summary.json")


if __name__ == "__main__":
    main()
