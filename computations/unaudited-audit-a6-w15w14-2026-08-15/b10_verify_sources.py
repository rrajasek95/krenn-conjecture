#!/usr/bin/env python3
"""AUDIT A6-B10 step 0: is my rebuilt source the SAME source P2 measured?

Two independent anchors:
  (1) my generator's blocks == P2's build_source blocks (byte-for-byte),
  (2) my *own* quadric construction reproduces P2's STORED derived data in
      results_a.json: live, error_zero and span (= rank of the span of the
      81 error components).  (2) uses no P2 code at all, only their numbers.
Also cross-checks E_word against the general |J|<=h-2 formula.
"""
from __future__ import annotations

import json
import sys

HERE = "/Users/rishi/workplace/krenn-conjecture/computations/unaudited-audit-a6-w15w14-2026-08-15"
P2 = "/Users/rishi/workplace/krenn-conjecture/computations/unaudited-witness-splitting-p2-2026-08-15"
sys.path.insert(0, HERE)

import b10_core as B  # noqa: E402

SEEDS_OF_INTEREST = None  # all seeds appearing in W14's detail


def main():
    w14 = json.load(open("/Users/rishi/workplace/krenn-conjecture/computations/"
                         "unaudited-monochrome-w14-2026-08-15/"
                         "results_task3_rankone.json"))
    seeds = sorted({d["seed"] for d in w14["detail"]})
    a = json.load(open(P2 + "/results_a.json"))
    p2rec = {r["seed"]: r for r in a["results"]}

    # ---- anchor (1): my generator vs P2's build_source
    sys.path.insert(0, P2)
    from run_a_dichotomy import build_source  # noqa: E402  (P2 code, once)
    gen_ok, gen_bad = 0, []
    for seed in seeds:
        mode = p2rec[seed]["mode"]
        mine = B.gen_source(seed, mode)
        theirs = build_source(seed, mode).blocks
        if all(mine[pr] == theirs[pr] for pr in B.ALLPAIRS):
            gen_ok += 1
        else:
            gen_bad.append((seed, mode))
    print(f"[anchor 1] generator agrees on {gen_ok}/{len(seeds)} seeds "
          f"(mismatches: {gen_bad})")

    # ---- anchor (2): my quadrics reproduce P2's STORED live/error_zero/span
    tot = ok_live = ok_ez = ok_span = 0
    bad = []
    for seed in seeds:
        mode = p2rec[seed]["mode"]
        blocks = B.gen_source(seed, mode)
        stored = {tuple(pr["pair"]): pr for pr in p2rec[seed]["pairs"]}
        for pq, pr in stored.items():
            pd = B.Pair(blocks, pq[0], pq[1])
            tot += 1
            ok_live += (pd.live() == pr["live"])
            ok_ez += ((len(pd.quadrics) == 0) == pr["error_zero"])
            sp = pd.span_rank()
            ok_span += (sp == pr["span"])
            if sp != pr["span"] or pd.live() != pr["live"]:
                bad.append((seed, pq, sp, pr["span"]))
    print(f"[anchor 2] over {tot} pairs of {len(seeds)} seeds: "
          f"live {ok_live}/{tot}, error_zero {ok_ez}/{tot}, "
          f"span {ok_span}/{tot}")
    if bad:
        print("  MISMATCHES:", bad[:10])

    # ---- cross-check: E_word (h=2 shortcut) vs general |J|<=h-2 formula
    blocks = B.gen_source(seeds[0], p2rec[seeds[0]]["mode"])
    pd = B.Pair(blocks, 0, 5)
    same = all(pd.E_word(w) == pd.E_word_general(w) for w in pd.words)
    print(f"[cross-check] E_word == E_word_general on all 81 words: {same}")

    json.dump({"generator_seeds_ok": gen_ok, "seeds": len(seeds),
               "pairs": tot, "live_ok": ok_live, "error_zero_ok": ok_ez,
               "span_ok": ok_span, "mismatches": bad[:20],
               "E_formula_crosscheck": same},
              open(HERE + "/b10_verify_sources.json", "w"), indent=1)


if __name__ == "__main__":
    main()
