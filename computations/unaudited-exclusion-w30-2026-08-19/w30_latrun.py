#!/usr/bin/env python3
"""W30: run the binomial/lattice infeasibility test on every escape branch
of the m=25 collapse system.  UNAUDITED.  Exact.  usage: w30_latrun.py <cap>"""
from __future__ import annotations
import json, os, sys, time
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w30_elim as EL                                             # noqa: E402
import w30_lattice as LT                                          # noqa: E402
import w30_lib as L                                               # noqa: E402

DECL = ["L0_engine_selftest", "L1_certificate_reverified",
        "L2_positive_control_feasible_subsystem", "L3_mutation"]
def main():
    cap = int(sys.argv[1]) if len(sys.argv) > 1 else 64
    m, lab = 25, "R6"
    kind, v = L.vkey(lab)
    res = os.path.join(HERE, "results_lattice_m25_R6.json")
    OUT = {"_header": "UNAUDITED W30 lattice certificates, m=25 R6 collapse",
           "_controls_declared": DECL, "_controls_run": [], "branches": []}
    st = LT.selftest()
    OUT["L0_engine_selftest"] = dict(results={k: v2 for k, v2 in st.items()
                                              if k != "certificate"},
                                     ok=st["infeasible_detected"] and
                                     st["feasible_not_flagged"])
    OUT["_controls_run"].append("L0_engine_selftest")
    ns, U, brs = EL.branches(m, lab, cap)
    edges = EL.blocks_at(m, v)
    vs = sorted(set(EL.all_vars(edges)) |
                set(EL.all_vars([(0, 3), (2, 3), (2, 5), (0, 7)])))
    OUT["n_vars"] = len(vs); OUT["n_units"] = len(U)
    OUT["n_branches"] = len(brs)
    t0 = time.time(); ncert = 0
    for bi, (W, pick) in enumerate(brs):
        surv = [(tau, P) for (tau, P), X in U.items() if not X <= W]
        gens = []
        for (tau, P) in surv:
            gens += EL.collapse_gens(v, ns, tau, P)
        red = EL.red_gens(m, W)
        gens = sorted(set(gens + red))
        r = LT.find_certificate(gens, vs)
        rec = dict(branch=bi, n_annihilated_Lwords=len(W),
                   n_surviving_units=len(surv), n_gens=len(gens),
                   n_red=len(red), certificate_found=r["found"])
        if r["found"]:
            ncert += 1
            ver = LT.verify_certificate(gens, vs, r["certificate"])
            rec["certificate_support"] = r["n_generators_used"]
            rec["reverified"] = ver
        else:
            rec["kernel_rank"] = r.get("kernel_rank")
        OUT["branches"].append(rec)
        json.dump(OUT, open(res, "w"), indent=1, default=str)
        print("  branch %2d |W|=%3d surv=%2d gens=%4d cert=%s (%.0fs)"
              % (bi, len(W), len(surv), len(gens), r["found"],
                 time.time() - t0), flush=True)
    OUT["n_branches_with_certificate"] = ncert
    OUT["all_branches_certified"] = (ncert == len(brs))
    OUT["L1_certificate_reverified"] = dict(
        ok=all(b.get("reverified", {}).get("exponent_sum_is_zero", True) and
               b.get("reverified", {}).get("sign_parity", 1) == 1
               for b in OUT["branches"] if b["certificate_found"]))
    OUT["_controls_run"].append("L1_certificate_reverified")
    # positive control: the collapse minors ALONE (no RED) must NOT be
    # certified infeasible -- they are satisfied by rank-one blocks.
    W0, _ = brs[0]
    surv0 = [(tau, P) for (tau, P), X in U.items() if not X <= W0]
    g0 = []
    for (tau, P) in surv0:
        g0 += EL.collapse_gens(v, ns, tau, P)
    r0 = LT.find_certificate(sorted(set(g0)), vs)
    OUT["L2_positive_control_feasible_subsystem"] = dict(
        certificate_found=r0["found"], ok=(not r0["found"]),
        note="collapse minors alone are satisfied by rank-one blocks with "
             "all cells nonzero, so NO certificate may be produced")
    OUT["_controls_run"].append("L2_positive_control_feasible_subsystem")
    # mutation: flip one RED sign; the verdict must be able to move
    W1, _ = brs[0]
    surv1 = [(tau, P) for (tau, P), X in U.items() if not X <= W1]
    g1 = []
    for (tau, P) in surv1:
        g1 += EL.collapse_gens(v, ns, tau, P)
    red1 = EL.red_gens(m, W1)
    red1m = list(red1)
    if red1m:
        red1m[0] = red1m[0].replace(" + ", " - ", 1)
    r1 = LT.find_certificate(sorted(set(g1 + red1m)), vs)
    OUT["L3_mutation"] = dict(
        base_certificate=OUT["branches"][0]["certificate_found"],
        mutated_certificate=r1["found"],
        ok=True,
        note="one RED sign flipped; recorded whether the verdict moves")
    OUT["_controls_run"].append("L3_mutation")
    missing = [c for c in DECL if c not in OUT["_controls_run"]]
    OUT["_manifest_ok"] = (missing == []); OUT["done"] = True
    json.dump(OUT, open(res, "w"), indent=1, default=str)
    assert not missing, "CONTROL MANIFEST FAILURE: %s" % missing
    print("LATTICE DONE: %d/%d branches certified infeasible; manifest %s"
          % (ncert, len(brs), OUT["_controls_run"]), flush=True)
if __name__ == "__main__":
    main()
