"""A7: final side-by-side of my independently computed census against W19's
stored table (read as DATA from results_CENSUS_SUMMARY.json -- no code reuse)."""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

HERE = os.path.dirname(os.path.abspath(__file__))
W19 = "/Users/rishi/workplace/krenn-conjecture/computations/unaudited-forcing-w19-2026-08-15/census/results_CENSUS_SUMMARY.json"
OUT = os.path.join(HERE, "results_A7_COMPARE.json")


def main():
    mine = json.load(open(os.path.join(HERE, "a7_classes.json")))
    t2b = json.load(open(os.path.join(HERE, "results_A7_TASK2B.json")))
    w = json.load(open(W19))["gamma_census"]

    rows = []
    agree = True
    for k in range(8, 17):
        cs = [c for c in mine if c["n_edges"] == k]
        realised = t2b["realised_by_edgecount"][str(k)]
        wk = w["by_edges"][str(k)]
        row = {
            "n_edges": k,
            "A7_classes": len(cs),
            "W19_classes": wk["classes"],
            "A7_realised": realised,
            "A7_labelled": sum(c["labelled_count"] for c in cs),
            "W19_labelled": wk["labelled"],
            "A7_min_pm": min(c["pm"] for c in cs),
            "W19_min_pms": wk["min_pms"],
            "A7_max_pm": max(c["pm"] for c in cs),
            "W19_max_pms": wk["max_pms"],
            "A7_low_pm_classes(pm<3)": sum(1 for c in cs if c["pm"] < 3),
            "W19_low_pm_classes": wk["low_pm_classes"],
        }
        row["AGREE"] = (row["A7_classes"] == row["W19_classes"] and
                        row["A7_realised"] == row["W19_classes"] and
                        row["A7_labelled"] == row["W19_labelled"] and
                        row["A7_min_pm"] == row["W19_min_pms"] and
                        row["A7_max_pm"] == row["W19_max_pms"] and
                        row["A7_low_pm_classes(pm<3)"] == row["W19_low_pm_classes"])
        agree = agree and row["AGREE"]
        rows.append(row)

    tot = {
        "A7_total_classes": len(mine),
        "W19_total_classes": w["n_admissible_gamma_iso_classes"],
        "A7_realised_total": t2b["realised_total"],
        "W19_n_nonempty": w["n_nonempty"],
        "A7_labelled_total": sum(c["labelled_count"] for c in mine),
        "W19_labelled_total": w["labelled_admissible_gammas"],
        "A7_classes_pm_lt_3": sum(1 for c in mine if c["pm"] < 3),
        "W19_n_classes_with_F_lt_3": w["n_classes_with_F_lt_3"],
    }
    tot["ALL_AGREE"] = (agree and
                        tot["A7_total_classes"] == tot["W19_total_classes"] ==
                        tot["A7_realised_total"] == tot["W19_n_nonempty"] and
                        tot["A7_labelled_total"] == tot["W19_labelled_total"] and
                        tot["A7_classes_pm_lt_3"] == tot["W19_n_classes_with_F_lt_3"])
    res = {"per_edge_count": rows, "totals": tot}
    with open(OUT, "w") as f:
        json.dump(res, f, indent=1)
    hdr = ("|E| | A7cls W19cls | A7real | A7 labelled  W19 labelled | pm[min,max] A7 / W19 "
           "| lowpm A7/W19 | agree")
    print(hdr)
    print("-" * len(hdr))
    for r in rows:
        print("%3d | %5d %6d | %6d | %12d %13d | [%2d,%2d] / [%2d,%2d]     | %3d/%-3d      | %s"
              % (r["n_edges"], r["A7_classes"], r["W19_classes"], r["A7_realised"],
                 r["A7_labelled"], r["W19_labelled"], r["A7_min_pm"], r["A7_max_pm"],
                 r["W19_min_pms"], r["W19_max_pms"], r["A7_low_pm_classes(pm<3)"],
                 r["W19_low_pm_classes"], r["AGREE"]))
    print(json.dumps(tot, indent=1))


if __name__ == "__main__":
    main()
