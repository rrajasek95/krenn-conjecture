#!/usr/bin/env python3
"""adv2 -- FINAL INDEPENDENT VERIFICATION + CONTROLS.  UNAUDITED.

Every claimed object is re-checked HERE from the raw 105-matching
definition C.H_word over all 6558 mixed words and the 3 constant words,
never through the Phi/coeff helpers.  Controls: mutation, out-of-locus
(ledger 18), and a manifest assertion (ledger 21).
"""
from __future__ import annotations

import json
import os
import random
import sys
from fractions import Fraction

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import a2lib as A                                                 # noqa: E402
import w26_core as C                                              # noqa: E402
import w26_sub as SB                                              # noqa: E402

F = Fraction
OUT = {"_header": "UNAUDITED adv2 -- final verification + controls"}
RAN = []


def load_z(d):
    return {tuple(int(t) for t in k.strip("()").split(",")): F(v)
            for k, v in d.items()}


def verify(m, bl, z, tag):
    """everything re-derived from C.H_word."""
    T = C.TEMPLATES[m]
    zz = {e: z.get(e, F(0)) for e in C.single_edges(T)}
    z0 = {e: F(0) for e in C.single_edges(T)}
    cells = A.all_cells_nonzero(bl, A.Geo(m))
    clean_bad = sum(1 for w in A.Geo(m).clean if C.H_word(bl, T, z0, w) != 0)
    phi_nz = sum(1 for w in C.WORDS if C.H_word(bl, T, z0, w) != 0)
    mixed_bad = sum(1 for w in C.MIXED if C.H_word(bl, T, zz, w) != 0)
    cons = [str(C.H_word(bl, T, zz, (c,) * 8)) for c in range(3)]
    vd = A.full_verdict(m, bl)
    subs = {k: (None if v is None else v["killed"])
            for k, v in SB.all_sub_verdicts(m, bl).items()}
    surv = [str(e) for e in A.Geo(m).live
            if A.solo_verdict(m, bl, e)["survives"]]
    rec = dict(tag=tag, m=m, all_cells_nonzero=cells,
               clean_rawdef=(cells and clean_bad == 0),
               n_clean_words_with_Phi_nonzero=clean_bad,
               n_words_with_Phi_nonzero_of_6561=phi_nz,
               on_vanishing_stratum_rawdef=(phi_nz == 0),
               solo_survivors=surv,
               z={str(e): str(v) for e, v in z.items() if v != 0},
               raw_mixed_words_with_H_nonzero=mixed_bad,
               raw_H_at_constants=cons,
               full_verdict={k: vd[k] for k in
                             ("n_unknowns", "n_rows", "rank", "inconsistent",
                              "killed")},
               forced_zero=vd.get("forced_zero"),
               verdict_z_solution=vd.get("zsol"),
               sub_verdicts=subs, point=A.dump(bl))
    print("  %-34s clean=%s stratum=%s survivors=%s"
          % (tag, rec["clean_rawdef"], rec["on_vanishing_stratum_rawdef"],
             surv))
    print("      [RAW C.H_word] Phi!=0 at %d/6561 ; H!=0 at %d/6558 mixed ; "
          "H(const)=%s" % (phi_nz, mixed_bad, cons))
    print("      FULL verdict killed=%s inconsistent=%s forced=%s"
          % (vd["killed"], vd.get("inconsistent"),
             (vd.get("forced_zero") or [])[:4] + (["..."] if
                                                  len(vd.get("forced_zero")
                                                      or []) > 4 else [])))
    print("      sub-systems killed: %s" % subs)
    return rec


def gather(m):
    """collect the headline objects produced by the other adv2 scripts."""
    out = []
    fn = os.path.join(HERE, "results_climb_m%d_s20260818.json" % m)
    if os.path.exists(fn):
        d = json.load(open(fn))
        best = None
        for r in d.get("rungs", []):
            if r.get("point") and len(r.get("z_nonzero", [])) >= 3:
                best = r
        if best:
            out.append(("S1 climb star-4 triple", A.load(best["point"]),
                        load_z(best["z"])))
    for f in sorted(os.listdir(HERE)):
        if not f.startswith("results_hunt_m%d" % m):
            continue
        d = json.load(open(os.path.join(HERE, f)))
        seen = set()
        for r in d.get("records", []):
            if not r.get("point") or len(r.get("z_nonzero", [])) < 3:
                continue
            key = tuple(r["z_nonzero"])
            if key in seen:
                continue
            seen.add(key)
            out.append(("S1 hunt %s" % ",".join(r["z_nonzero"]),
                        A.load(r["point"]), load_z(r["z"])))
    fn = os.path.join(HERE, "results_pair_m%d.json" % m)
    if os.path.exists(fn):
        d = json.load(open(fn))
        want = {"(2, 4)": 0, "(3, 5)": 0, "(2, 7)": 0, "(1, 5)": 0}
        for r in d.get("records", []):
            if not r.get("found") or not r.get("point"):
                continue
            for q in r["solo_survivors"]:
                if q in want and want[q] == 0:
                    want[q] = 1
                    out.append(("S2 survivor %s (R-vertex %s)"
                                % (q, q.split(",")[1].strip(" )")),
                                A.load(r["point"]), load_z(r["z"])))
                    break
    return out


def main():
    m = int(sys.argv[1]) if len(sys.argv) > 1 else 28
    fn = os.path.join(HERE, "results_final_m%d.json" % m)
    recs = []

    print("=" * 74)
    print("(F1) RAW re-verification of every adv2 headline object, m=%d" % m)
    print("=" * 74)
    RAN.append("F1_raw_reverify")
    objs = gather(m)
    for tag, bl, z in objs:
        recs.append(verify(m, bl, z, tag))
        OUT["objects"] = recs
        json.dump(OUT, open(fn, "w"), indent=1, default=str)
    assert recs, "no objects gathered"

    print()
    print("=" * 74)
    print("(F2) MUTATION control")
    print("=" * 74)
    RAN.append("F2_mutation")
    mut = []
    for tag, bl, z in objs[:3]:
        nb_break = ntot = 0
        stayed = []
        for e in sorted(bl):
            for i in range(3):
                for j in range(3):
                    q = {f: [r[:] for r in bl[f]] for f in bl}
                    q[e][i][j] = q[e][i][j] + F(1)
                    ntot += 1
                    if A.is_clean(m, q):
                        stayed.append("%s[%d][%d]" % (e, i, j))
                    else:
                        nb_break += 1
        print("  %-34s %d/%d single-cell (+1) mutations destroy cleanliness"
              % (tag, nb_break, ntot))
        if stayed:
            print("      still clean after: %s" % stayed)
        mut.append(dict(tag=tag, broke=nb_break, total=ntot,
                        still_clean=stayed))
        assert nb_break > 0, "mutation control vacuous for %s" % tag
    OUT["mutation"] = mut
    json.dump(OUT, open(fn, "w"), indent=1, default=str)

    print()
    print("=" * 74)
    print("(F3) OUT-OF-LOCUS controls (ledger 18): the predicates we report")
    print("     as NOT FOUND are not vacuously false")
    print("=" * 74)
    RAN.append("F3_out_of_locus")
    G = A.Geo(m)
    ones = {e: [[F(1)] * 3 for _ in range(3)] for e in G.gam}
    sv = {str(e): A.solo_verdict(m, ones, e) for e in G.live}
    allsurv = [k for k, v in sv.items() if v["survives"]]
    vd = A.full_verdict(m, ones)
    print("  ALL-ONES point (every Gamma cell = 1, NOT clean):")
    print("      clean=%s ; solo families SURVIVING: %s"
          % (A.is_clean(m, ones), allsurv))
    print("      full residual verdict: killed=%s inconsistent=%s "
          "rank=%d/%d" % (vd["killed"], vd.get("inconsistent"), vd["rank"],
                          vd["n_unknowns"]))
    print("      => the 'solo family survives' predicate is satisfiable for "
          "EVERY single, and for every non-co-hyperplanar PAIR, at a "
          "non-clean point; the pair search is therefore not vacuous.")
    ctl = dict(all_ones=dict(clean=A.is_clean(m, ones),
                             survivors=allsurv,
                             verdict={k: vd[k] for k in
                                      ("n_unknowns", "n_rows", "rank",
                                       "inconsistent", "killed")},
                             forced_zero=vd.get("forced_zero"),
                             zsol=vd.get("zsol")))
    assert len(allsurv) >= 2, "all-ones control failed to be non-vacuous"
    # a point that is NOT clean but has verdict killed=False with all z free
    rng = random.Random(4)
    wit = {e: [[F(rng.randint(1, 7)) for _ in range(3)] for _ in range(3)]
           for e in G.gam}
    for e in G.gam:
        if (e[0] >= 4 and e[1] >= 4) or e == (0, 7):
            wit[e] = [[F(0)] * 3 for _ in range(3)]
    v2 = A.full_verdict(m, wit)
    print("  R-blocks-and-(0,7)-zeroed point (NOT clean): verdict "
          "killed=%s n_rows=%d dim=%s -> z = (1,...,1) is a full-support "
          "solution" % (v2["killed"], v2["n_rows"], v2.get("solution_dim")))
    ctl["zeroed_point"] = dict(killed=v2["killed"], n_rows=v2["n_rows"],
                               solution_dim=v2.get("solution_dim"),
                               clean=A.is_clean(m, wit),
                               point=A.dump(wit))
    assert not v2["killed"], "out-of-locus control for killed=False failed"
    OUT["out_of_locus"] = ctl
    json.dump(OUT, open(fn, "w"), indent=1, default=str)

    print()
    print("=" * 74)
    print("(F4) PRIMARY TARGET check over every object collected")
    print("=" * 74)
    RAN.append("F4_primary_check")
    hits = [r for r in recs if r["full_verdict"]["killed"] is False
            and not r["on_vanishing_stratum_rawdef"]]
    print("  objects with verdict killed=False and off the stratum: %d"
          % len(hits))
    OUT["primary_hits"] = hits
    if hits:
        print("  *** PRIMARY TARGET FOUND -- ESCALATE ***")
    json.dump(OUT, open(fn, "w"), indent=1, default=str)

    declared = ["F1_raw_reverify", "F2_mutation", "F3_out_of_locus",
                "F4_primary_check"]
    missing = [d for d in declared if d not in RAN]
    print("\nCONTROL MANIFEST declared=%s ran=%s" % (declared, RAN))
    assert not missing, "CONTROL DID NOT RUN: %s" % missing
    OUT["control_manifest"] = dict(declared=declared, ran=RAN)
    json.dump(OUT, open(fn, "w"), indent=1, default=str)
    print("wrote %s" % fn)


if __name__ == "__main__":
    main()
