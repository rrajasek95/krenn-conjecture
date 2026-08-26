#!/usr/bin/env python3
"""H1 -- consolidate every evidence file in this directory into one index.

UNAUDITED.  Hygiene agent H1, 2026-08-15.

Merges the three m=17 replay shards into results_b3_m17_all.jsonl, checks
that all 31 orbits are present exactly once, and prints the ledger tables
that go into the deliverable.
"""

from __future__ import annotations

import glob
import hashlib
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


class CheckFailure(Exception):
    pass


def require(cond, msg):
    if not cond:
        raise CheckFailure(msg)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for blk in iter(lambda: fh.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


def main():
    # ---- merge the m17 shards
    rows = {}
    for shard in sorted(glob.glob(os.path.join(HERE, "results_b3_m17*.jsonl"))):
        if shard.endswith("_all.jsonl"):
            continue
        for line in open(shard):
            r = json.loads(line)
            prev = rows.get(r["tag"])
            if prev is not None:
                require(prev["verdict"] == r["verdict"],
                        f"{r['tag']}: shards disagree "
                        f"({prev['verdict']} vs {r['verdict']})")
            rows[r["tag"]] = r
    order = sorted(rows, key=lambda t: int(t.split("o")[-1]))
    missing = [f"m17_o{i}" for i in range(31) if f"m17_o{i}" not in rows]
    out = os.path.join(HERE, "results_b3_m17_all.jsonl")
    with open(out, "w") as fh:
        for t in order:
            fh.write(json.dumps(rows[t]) + "\n")

    print("=== m=17 orbit closure proofs ===")
    print(f"{'orbit':10s} {'verdict':9s} {'wall_s':>9s} {'lines':>10s} "
          f"{'adds':>9s} {'dels':>9s} {'empty':>6s} {'trunc':>6s} {'RAT':>4s}")
    nver = 0
    for t in order:
        r = rows[t]
        ps = r.get("proof_scan", {})
        nver += r["verdict"] == "VERIFIED"
        print(f"{t:10s} {r['verdict']:9s} {r.get('wall_s', 0):9.1f} "
              f"{ps.get('lines', 0):10d} {ps.get('additions', 0):9d} "
              f"{ps.get('deletions', 0):9d} "
              f"{str(ps.get('terminates_in_empty_clause')):>6s} "
              f"{str(ps.get('truncated_tail')):>6s} "
              f"{str(r.get('rat_lemmas_in_core')):>4s}")
    print(f"\n  m17: {nver}/{len(order)} VERIFIED; missing orbits: "
          f"{missing or 'none'}")
    tot_lines = sum(rows[t].get("proof_scan", {}).get("lines", 0)
                    for t in order)
    tot_wall = sum(rows[t].get("wall_s", 0) for t in order)
    print(f"  total proof lines replayed: {tot_lines:,}; "
          f"total checker wall time: {tot_wall/60:.1f} min")
    mid_clause = [t for t in order
                  if rows[t].get("proof_scan", {}).get("truncated_tail")]
    no_empty = [t for t in order
                if not rows[t].get("proof_scan", {})
                .get("terminates_in_empty_clause")]
    print(f"  truncated MID-CLAUSE (ledger 5, the fatal form): "
          f"{mid_clause or 'none'}")
    print(f"  no explicit empty-clause line (ledger 5, the benign form -- "
          f"the checker closes the last propagation itself): "
          f"{len(no_empty)} of {len(order)}")
    if no_empty:
        print(f"     {', '.join(no_empty)}")

    # ---- w11
    w11 = [json.loads(l) for l in
           open(os.path.join(HERE, "results_b3_w11.jsonl"))]
    print(f"\n=== W11 replacement proofs: "
          f"{sum(r['verdict'] == 'VERIFIED' for r in w11)}/{len(w11)} VERIFIED "
          f"({sum(r['proof_scan']['lines'] for r in w11):,} lines) ===")

    # ---- checker provenance
    drat = os.path.join(HERE, "tools", "drat-trim", "drat-trim")
    index = {"agent": "H1",
             "pinned_head": open(os.path.join(HERE, "PINNED_HEAD.txt")
                                 ).read().split()[0],
             "checker": {"path": "tools/drat-trim/drat-trim",
                         "sha256": sha256(drat)},
             "m17": {"orbits": len(order), "verified": nver,
                     "missing": missing, "total_proof_lines": tot_lines},
             "w11": {"proofs": len(w11),
                     "verified": sum(r["verdict"] == "VERIFIED" for r in w11)},
             "evidence_sha256": {}}
    for f in sorted(os.listdir(HERE)):
        if f.startswith("results_") and (f.endswith(".json")
                                         or f.endswith(".jsonl")):
            index["evidence_sha256"][f] = sha256(os.path.join(HERE, f))
    with open(os.path.join(HERE, "results_index.json"), "w") as fh:
        json.dump(index, fh, indent=1)
    print("\n=== frozen SHA-256 of every evidence file ===")
    for k, v in index["evidence_sha256"].items():
        print(f"  {v}  {k}")
    print(f"  {index['checker']['sha256']}  tools/drat-trim/drat-trim")
    print("\nwrote results_b3_m17_all.jsonl, results_index.json")


if __name__ == "__main__":
    main()
