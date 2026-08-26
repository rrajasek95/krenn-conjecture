#!/usr/bin/env python3
"""AUDIT A6-B10 check 1+2: independent recomputation of (a) general-witness
and (b) rank-one-witness existence on the pairs W14 stored in
results_task3_rankone.json.

Default: the full 120-pair replication (W14's whole fleet slice).
The 5 witness + 5 blocked "featured" rows are marked in the output.
"""
from __future__ import annotations

import json
import sys
import time

HERE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-audit-a6-w15w14-2026-08-15")
W14 = ("/Users/rishi/workplace/krenn-conjecture/computations/"
       "unaudited-monochrome-w14-2026-08-15")
P2 = ("/Users/rishi/workplace/krenn-conjecture/computations/"
      "unaudited-witness-splitting-p2-2026-08-15")
sys.path.insert(0, HERE)
import b10_core as B  # noqa: E402

# 5 witness pairs (all with E NOT identically zero, i.e. the non-trivial ones)
# and 5 blocked pairs, chosen across seeds/modes.
FEATURED = [
    (1002, (2, 5)), (1005, (0, 5)), (1005, (4, 5)), (1008, (0, 3)),
    (1008, (1, 2)),
    (1000, (0, 1)), (1001, (2, 3)), (1003, (1, 4)), (1006, (0, 5)),
    (1007, (3, 4)),
]


def main():
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 10**9
    w14 = json.load(open(W14 + "/results_task3_rankone.json"))
    p2 = json.load(open(P2 + "/results_a.json"))
    p2rec = {r["seed"]: r for r in p2["results"]}
    stored = {(r["seed"], tuple(pr["pair"])): pr
              for r in p2["results"] for pr in r["pairs"]}

    todo = [(d["seed"], tuple(d["pair"])) for d in w14["detail"]]
    lab = {(d["seed"], tuple(d["pair"])): d for d in w14["detail"]}
    # featured first so a truncated run still yields the table
    todo.sort(key=lambda x: (x not in FEATURED,))
    todo = todo[:limit]

    src_cache = {}
    rows = []
    agree_gen = agree_rk1 = 0
    t0 = time.time()
    for seed, pq in todo:
        mode = p2rec[seed]["mode"]
        if seed not in src_cache:
            src_cache[seed] = B.gen_source(seed, mode)
        pd = B.Pair(src_cache[seed], pq[0], pq[1])
        tag = f"{seed}_{pq[0]}{pq[1]}"
        gv, gdim, gt, gst = B.decide(pd, tag, "gen", timeout=120)
        rv, rdim, rt, rst = B.decide(pd, tag, "rk1", timeout=120)
        d = lab[(seed, pq)]
        st = stored[(seed, pq)]
        row = {"seed": seed, "mode": mode, "pair": list(pq),
               "featured": (seed, pq) in FEATURED,
               "w14_witness": d["witness"], "w14_rank_one": d["rank_one_witness"],
               "p2_status": st["status"], "p2_error_zero": st["error_zero"],
               "p2_span": st["span"], "n_quadrics": len(pd.quadrics),
               "b10_general": gv, "b10_general_dim": gdim,
               "b10_general_sec": round(gt, 3), "b10_general_status": gst,
               "b10_rank_one": rv, "b10_rank_one_dim": rdim,
               "b10_rank_one_sec": round(rt, 3), "b10_rank_one_status": rst}
        row["agree_general"] = (gv == d["witness"])
        row["agree_rank_one"] = (rv == d["rank_one_witness"])
        agree_gen += bool(row["agree_general"])
        agree_rk1 += bool(row["agree_rank_one"])
        rows.append(row)
        flag = "" if (row["agree_general"] and row["agree_rank_one"]) \
            else "   <<< DISAGREE"
        print(f"{'*' if row['featured'] else ' '} {seed} {mode:8s} {pq} "
              f"W14[wit={int(d['witness'])},rk1={int(d['rank_one_witness'])}] "
              f"B10[wit={gv},rk1={rv}] dims({gdim},{rdim}) "
              f"nq={len(pd.quadrics):2d} "
              f"[{gt:.2f}s/{rt:.2f}s]{flag}", flush=True)

    n = len(rows)
    # implication check: rank-one witness  =>  general witness
    impl_bad = [r for r in rows if r["b10_rank_one"] and not r["b10_general"]]
    blocked_with_rk1 = [r for r in rows
                        if r["b10_general"] is False and r["b10_rank_one"]]
    wit_no_rk1 = [r for r in rows
                  if r["b10_general"] and r["b10_rank_one"] is False]
    timeouts = [r for r in rows if r["b10_general_status"] != "ok"
                or r["b10_rank_one_status"] != "ok"]
    summ = {"pairs": n, "agree_general": agree_gen, "agree_rank_one": agree_rk1,
            "rank_one_implies_general_violations": len(impl_bad),
            "blocked_with_rank_one": len(blocked_with_rk1),
            "witness_without_rank_one": len(wit_no_rk1),
            "non_ok_singular": len(timeouts),
            "max_general_sec": max((r["b10_general_sec"] for r in rows),
                                   default=0),
            "max_rank_one_sec": max((r["b10_rank_one_sec"] for r in rows),
                                    default=0),
            "total_sec": round(time.time() - t0, 1)}
    print("\n== B10 summary ==")
    for k, v in summ.items():
        print(f"  {k}: {v}")
    json.dump({"summary": summ, "rows": rows},
              open(HERE + "/b10_results_table.json", "w"), indent=1)
    print("wrote b10_results_table.json")


if __name__ == "__main__":
    main()
