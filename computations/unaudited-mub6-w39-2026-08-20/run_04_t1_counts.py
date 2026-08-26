"""W39-T1 stage 1: CERTIFIED real-point counts of the MU-vector fibres
V(F_6) (must-SAT calibration) and V(S_6) (the target).

Runs the `realroot` module (VIEW A: our own Hermite trace form + exact
rational congruence reduction) and VIEW B (Singular rootsmr.lib
matbil/symsignature) on each fibre, checkpointing after every stage so the
job is restartable.

Published ground truth to calibrate against (Brierley-Weigert,
https://arxiv.org/abs/0901.4051, 20-significant-digit numerics):
    |V(F_6)| = 48 vectors MU to {I, F_6}
    |V(S_6)| = 90 vectors MU to {I, S_6}
Our numbers are EXACT; if they disagree with the published ones that is a
finding either way and must be reported, not reconciled away (ledger 18).
"""
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "realroot"))

from mub_systems import fibre_system, S6_EXP, F6_EXP          # noqa: E402
from realroot import real_root_count, real_root_count_view_b  # noqa: E402

CKPT = os.path.join(HERE, "results_t1_counts.json")
DECLARED = ["F6_viewA", "F6_viewB", "S6_viewA", "S6_viewB"]


def load():
    if os.path.exists(CKPT):
        with open(CKPT) as fh:
            return json.load(fh)
    return {"executed": [], "stages": {}}


def save(st):
    tmp = CKPT + ".tmp"
    with open(tmp, "w") as fh:
        json.dump(st, fh, indent=2, default=str)
    os.replace(tmp, CKPT)


def stage(st, name, fn):
    if name in st["stages"] and st["stages"][name].get("ok") is not None:
        print(f"[skip] {name} already checkpointed", flush=True)
        return st["stages"][name]
    t0 = time.time()
    print(f"[run ] {name} ...", flush=True)
    r = fn()
    r["wall_seconds"] = round(time.time() - t0, 1)
    st["stages"][name] = r
    if name not in st["executed"]:
        st["executed"].append(name)
    save(st)
    print(f"[done] {name}: status={r.get('status')} "
          f"n_real={r.get('n_real')} rank={r.get('n_distinct_complex')} "
          f"({r['wall_seconds']}s)", flush=True)
    return r


def main():
    st = load()
    for tag, exp, order in [("F6", F6_EXP, 6), ("S6", S6_EXP, 3)]:
        gens, vs = fibre_system(exp, order)
        stage(st, f"{tag}_viewA",
              lambda g=gens, v=vs, t=tag: real_root_count(
                  g, v, workdir=HERE, tag=f"rr_{t}", timeout=100000))
        stage(st, f"{tag}_viewB",
              lambda g=gens, v=vs, t=tag: real_root_count_view_b(
                  g, v, workdir=HERE, tag=f"rrB_{t}", timeout=100000))

    # ledger 26: two independent views must reconcile
    print("\n=== RECONCILIATION ===", flush=True)
    ok = True
    for tag, expected in [("F6", 48), ("S6", 90)]:
        a = st["stages"].get(f"{tag}_viewA", {})
        b = st["stages"].get(f"{tag}_viewB", {})
        ra, rb = a.get("n_real"), b.get("n_real")
        agree = (ra is not None and ra == rb)
        print(f"{tag}: VIEW A n_real={ra} (rank={a.get('n_distinct_complex')}, "
              f"vdim={a.get('vdim')})  VIEW B n_real={rb}  "
              f"agree={agree}  published={expected}", flush=True)
        if not agree:
            ok = False
    st["reconciled"] = ok
    save(st)

    missing = [d for d in DECLARED if d not in st["executed"]]
    if missing:
        print("CONTROL MANIFEST MISMATCH, missing:", missing, flush=True)
        sys.exit(2)
    print(f"CONTROL MANIFEST OK: {len(DECLARED)} declared, "
          f"{len(st['executed'])} executed; views reconciled = {ok}", flush=True)


if __name__ == "__main__":
    main()
