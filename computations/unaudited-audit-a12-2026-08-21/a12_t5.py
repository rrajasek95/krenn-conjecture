#!/usr/bin/env python3
"""A12 TARGET 3 -- did W36 round 2 actually implement A11's corrections?
UNAUDITED.

L0_manifests -- scan EVERY results_*.json in the W36 lane for the ledger-31
                pattern (ok true with _controls_run empty), for ok fields on
                blocks that never executed, and for declared != run
L1_strides   -- locate every stride in the lane's engines and say which
                reported number is a sample rather than a census
L2_census    -- recompute the 2,124 / 6,561 nonzero-Phi census of the escape
                object on the A12 engine (A11 found this was a 1-in-7 sample)
L3_escobj    -- the escape object's full point: stored?  loadable?  identical
                to the object it claims to be?  clean, all cells nonzero, off
                stratum, and does R6 still deliver 695/743?
L4_stored    -- the two (R25)-failing m=25 points: stored in full and
                re-derivable here
"""
from __future__ import annotations

import glob
import json
import os
import re
import sys
import time

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
W30 = os.path.join(ROOT, "unaudited-exclusion-w30-2026-08-19")
W36 = os.path.join(ROOT, "unaudited-routea-w36-2026-08-20")
sys.path.insert(0, HERE)
import a12_lib as A  # noqa: E402
from a12_t0 import Manifest  # noqa: E402
from a12_t2 import slots  # noqa: E402

DECL = ["L0_manifests", "L1_strides", "L2_census", "L3_escobj", "L4_stored"]
ROUND2 = ("results_full.json", "results_m25full.json", "results_m28fix.json",
          "results_escobj.json", "results_elim_prelaunch.json",
          "results_build_alpha_13.json", "results_build_alpha_31.json",
          "results_build_alpha_Q.json", "results_joint_hunt_13.json",
          "results_joint_hunt_31.json", "results_joint_hunt_Q.json")


def main():
    t0 = time.time()
    man = Manifest(DECL)
    res = os.path.join(HERE, "results_t5.json")

    # ------------------------------------------------------------- L0
    scan = []
    for path in sorted(glob.glob(os.path.join(W36, "results_*.json"))):
        try:
            d = json.load(open(path))
        except Exception as e:
            scan.append(dict(file=os.path.basename(path), error=str(e)))
            continue
        if not isinstance(d, dict):
            continue
        run = d.get("_controls_run")
        decl = d.get("_controls_declared")
        blocks = {k: v for k, v in d.items()
                  if isinstance(v, dict) and "ok" in v}
        scan.append(dict(
            file=os.path.basename(path),
            round2=(os.path.basename(path) in ROUND2),
            declared=decl, n_run=(len(run) if isinstance(run, list) else None),
            manifest_ok=d.get("_manifest_ok"), done=d.get("done"),
            empty_run_with_ok=(isinstance(run, list) and not run
                               and any(v.get("ok") is True
                                       for v in blocks.values())),
            ok_without_executed=sorted(
                k for k, v in blocks.items()
                if v.get("ok") is not None and v.get("executed") is not True),
            declared_not_run=sorted(set(decl or []) - set(run or []))))
    # engines that write _manifest_ok as a LITERAL rather than computing it
    byfiat = []
    for path in sorted(glob.glob(os.path.join(W36, "*.py"))):
        for i, line in enumerate(open(path), 1):
            if re.search(r"_manifest_ok\"\]\s*=\s*True\s*$", line.strip()):
                byfiat.append(dict(file=os.path.basename(path), line=i))
    bad = [r for r in scan if r.get("round2") and (
        r.get("empty_run_with_ok") or r.get("declared_not_run"))]
    lying = [r for r in scan
             if r.get("manifest_ok") is True and r.get("declared_not_run")]
    man.record("L0_manifests", dict(
        n_files=len(scan), per_file=scan,
        round2_files_with_defect=[r["file"] for r in bad],
        round2_ok_without_executed={
            r["file"]: r["ok_without_executed"] for r in scan
            if r.get("round2") and r["ok_without_executed"]},
        manifest_ok_true_but_controls_missing=[
            dict(file=r["file"], missing=r["declared_not_run"]) for r in lying],
        engines_setting_manifest_ok_by_fiat=byfiat,
        ok=(not bad and not lying and not byfiat),
        note="A11's ledger-31 finding was ok=True with _controls_run empty; "
             "this re-checks the whole lane, and additionally flags ok "
             "fields on blocks carrying no executed marker"))
    print("L0: %d files, round-2 defects %s"
          % (len(scan), [r["file"] for r in bad]), flush=True)

    # ------------------------------------------------------------- L1
    strides = []
    for path in sorted(glob.glob(os.path.join(W36, "*.py"))):
        for i, line in enumerate(open(path), 1):
            if "[::" in line:
                strides.append(dict(file=os.path.basename(path), line=i,
                                    code=line.strip()[:110]))
    r2 = [s for s in strides
          if s["file"] in ("w36_full.py", "w36_m25full.py", "w36_m28fix.py",
                           "w36_escobj.py", "w36_elim.py", "w36_build.py")]
    man.record("L1_strides", dict(
        n_strides=len(strides), all_strides=strides,
        round2_engine_strides=r2,
        escobj_stride_removed=not any(s["file"] == "w36_escobj.py"
                                      for s in strides),
        m25full_stride_free=not any(s["file"] == "w36_m25full.py"
                                    for s in strides),
        full_stride_free=not any(s["file"] == "w36_full.py"
                                 for s in strides),
        ok=(not any(s["file"] in ("w36_escobj.py", "w36_m25full.py",
                                  "w36_full.py") for s in strides)),
        note="the m=25 round-2 engines are stride-free; w36_m28fix.py is "
             "NOT -- it samples index choices 1 in 17 (K1/K2) and 1 in 11 "
             "(K3), and those are the numbers the m=28 retraction quotes"))
    print("L1: %d strides total; round-2 engine strides: %s"
          % (len(strides), [(s["file"], s["line"]) for s in r2]), flush=True)

    # ------------------------------------------------------------- L2/L3
    tm = A.T(25)
    idx, by, big = slots(tm)
    esc = None
    for r in json.load(open(os.path.join(W30, "points_hunt.json")))["points"]:
        if r.get("m") == 25 and str(r.get("p")) == '13' and \
                "s1073" in str(r.get("tag")):
            esc = r
            break
    K = A.Fp(13)
    rec = {}
    if esc is not None:
        bl = A.load_point(esc["point"], K)
        rep = tm.vertex_report(bl, 'R', 6, K, choices=idx)
        rec = dict(tag=esc.get("tag"), clean=tm.is_clean(bl, K),
                   allnz=tm.all_nonzero(bl, K),
                   offstratum=tm.off_stratum(bl, K),
                   n_phi_nonzero=tm.n_phi_nonzero(bl, K), n_words=6561,
                   n_idx=rep['n_idx'], n_deliver=rep['n_deliver'],
                   n_zero_scale=rep['n_zero_scale'],
                   DELIVERS=rep['DELIVERS'])
    stored = None
    p = os.path.join(W36, "results_escobj.json")
    if os.path.exists(p):
        d = json.load(open(p))
        v2 = (d.get("V2_point_valid") or {}).get("object") or {}
        stored = dict(keys=sorted(d.keys()),
                      n_phi_nonzero=v2.get("n_phi_nonzero_words"),
                      point_stored=isinstance(d.get("point")
                                              or d.get("object_point"), dict),
                      any_point_key=[k for k, v in d.items()
                                     if isinstance(v, dict)
                                     and ("point" in v
                                          or any(str(kk).startswith("(")
                                                 for kk in v))][:8])
    man.record("L2_census", dict(
        recomputed=rec.get("n_phi_nonzero"), stored=(stored or {}).get(
            "n_phi_nonzero"), n_words=6561,
        agrees=(rec.get("n_phi_nonzero") == (stored or {}).get(
            "n_phi_nonzero")),
        ok=(rec.get("n_phi_nonzero") == (stored or {}).get("n_phi_nonzero")),
        note="A11 found n_phi_nonzero was a 1-in-7 sample; W36 reports the "
             "corrected 2,124 of 6,561.  A12 recomputes it from scratch"))
    man.record("L3_escobj", dict(
        found=(esc is not None), recomputed=rec, stored_summary=stored,
        deliver_matches_reported=(rec.get("n_deliver") == 695
                                  and rec.get("n_idx") == 743),
        ok=(bool(rec) and rec.get("clean") and rec.get("allnz")
            and rec.get("DELIVERS")),
        note="the escape object is a stored W30 hunt point; the question A11 "
             "raised is whether the LANE stores the full point in its own "
             "record so the number can be re-traced"))
    print("L2/L3: n_phi_nonzero recomputed %s (stored %s); escape object "
          "%d/%d deliver" % (rec.get("n_phi_nonzero"),
                             (stored or {}).get("n_phi_nonzero"),
                             rec.get("n_deliver"), rec.get("n_idx")),
          flush=True)

    # ------------------------------------------------------------- L4
    d = json.load(open(os.path.join(W36, "results_m25full.json")))
    m4 = d.get("M4_corpus", {})
    got = []
    for r in (m4.get("R25_failing_points_stored") or []):
        pt = r.get("point")
        if not isinstance(pt, dict):
            got.append(dict(tag=r.get("tag"), stored=False))
            continue
        Kf = A.K_of(r.get("field"))
        try:
            bl = A.load_point(pt, Kf)
        except Exception as e:
            got.append(dict(tag=r.get("tag"), stored=True, error=str(e)))
            continue
        live = {(w[5], w[7]): set() for w in [wq for wq, _f in idx]}
        for (w, fire) in idx:
            if len(fire) == 1 and not Kf.iszero(tm.hafL(bl, tuple(w[:4]), Kf)):
                live[(w[5], w[7])].add(sorted(fire)[0])
        rep = tm.vertex_report(bl, 'R', 6, Kf, choices=idx)
        got.append(dict(tag=r.get("tag"), field=r.get("field"), stored=True,
                        clean=tm.is_clean(bl, Kf), allnz=tm.all_nonzero(
                            bl, Kf), offstratum=tm.off_stratum(bl, Kf),
                        R25_recomputed=any(len(s) >= 2
                                           for s in live.values()),
                        R25_reported=r.get("R25_holds"),
                        n_idx=rep['n_idx'], DELIVERS=rep['DELIVERS'],
                        matches=(rep['DELIVERS'] == r.get("DELIVERS"))))
    man.record("L4_stored", dict(
        n_reported=m4.get("n_R25_fails"), n_stored=len(got), per_point=got,
        ok=(bool(got) and all(r.get("stored") and r.get("clean")
                              and r.get("matches") for r in got)),
        note="A11's defect was that exception objects were not stored; "
             "round 2 stores the (R25)-failing points -- re-derived here"))
    print("L4: %s" % json.dumps([{k: v for k, v in r.items()
                                  if k != 'point'} for r in got]), flush=True)

    man.finish(res, extra={"elapsed_s": round(time.time() - t0, 1)})
    print("T5 DONE in %.1fs" % (time.time() - t0), flush=True)


if __name__ == "__main__":
    main()
