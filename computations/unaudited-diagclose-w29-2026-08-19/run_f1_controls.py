#!/usr/bin/env python3
"""W29 F1 -- the control battery.

 (C1) REPRODUCE W28-T1 on 10 of its 127 sigma-slice free-set cases, from W28's
      own modules but writing only into THIS directory, and compare verdicts.
 (C2) k = 3 MUST NOT BE UNIT in the new T1i formulation (a formulation that
      kills k = 3 is wrong: three-colour X_3 diagonal points exist).
 (C3) the honest-boundary point t^1 = t^2 = 0 must stay colour-0 feasible.
 (C4) ledger batteries with FIRING NEGATIVES: the ledger-13 shadowing guard
      must reject a shadowing script; the ledger-6/11 '?'-scan must reject a
      broken script; the ledger-22 denominator guard must fire.
 (C5) ledger-19: the char-0 verdicts of C1 re-confirmed at two 1-mod-3 primes.
"""
from __future__ import annotations

import json
import sys
import time
from fractions import Fraction
from itertools import combinations

BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-diagclose-w29-2026-08-19")
W28 = ("/Users/rishi/workplace/krenn-conjecture/computations/"
       "unaudited-x4empty-w28-2026-08-18")
for p in (BASE, W28):
    if p not in sys.path:
        sys.path.insert(0, p)
import w28_core as K                                                # noqa: E402
import w28_diag as DG                                               # noqa: E402
import run_t1d_diagelim as D                                        # noqa: E402
import run_t1g_freeelim as G                                        # noqa: E402
import w29_core as C                                                # noqa: E402
import w29_t1i as T                                                 # noqa: E402

RES, RAN = {}, []
OUT = f"{BASE}/results_f1_controls.json"
PRIMES = (32029, 1000003)


def ck(tag=""):
    RES["ran"] = RAN
    with open(OUT, "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
    if tag:
        print(f"      [checkpoint {tag}]", flush=True)


def c1_reproduce_w28t1(nsel=10):
    """Re-run 10 of W28-T1's 127 cases through W28's builder + our Singular."""
    ref = json.load(open(f"{W28}/results_t1g_freeelim_sigma_1234567_k4_all"
                         ".json"))["cases"]
    keys = list(ref.keys())
    sel = [keys[i] for i in range(0, len(keys), max(1, len(keys) // nsel))]
    sel = sel[:nsel]
    t, names0, nv0, xoff = D.build_symbolic("sigma")
    names0 = names0[:xoff]
    out = {}
    for key in sel:
        size, Ystr = key.split(":")
        Y = tuple(int(x) for x in Ystr.strip("()").rstrip(",").split(",")
                  if x.strip() != "")
        gens, ce, nv = G.build_case(t, xoff, Y, 4)
        polys = [g[-1] for g in gens]
        polys = K.clear_denoms(polys)[0]
        polys.sort(key=lambda p: (len(p.t), p.deg()))
        ce = K.clear_denoms([ce])[0][0]
        names = names0 + [f"zx{y}" for y in Y]
        used = set()
        for p in polys + [ce]:
            for k2 in p.t:
                for i, e2 in enumerate(k2):
                    if e2:
                        used.add(i)
        used = sorted(used)
        nvc = len(used)

        def sq(p):
            return K.Poly(nvc, {tuple(k2[v] for v in used): val
                                for k2, val in p.t.items()})
        polys2 = [sq(p) for p in polys]
        ce2 = sq(ce)
        nm = [names[v] for v in used]
        rec = {}
        for char in (0,) + PRIMES:
            r = D.decide(polys2, ce2, nm, char, timeout=900)
            rec[str(char)] = r
        rec["W28_verdict_char0"] = ref[key].get("0", {}).get("isunit")
        rec["AGREE"] = (rec["0"]["isunit"] == rec["W28_verdict_char0"])
        out[key] = rec
        print(f"  [C1] Y={Y}: ours unit={rec['0']['isunit']} "
              f"(p={[rec[str(p)]['isunit'] for p in PRIMES]}), "
              f"W28 unit={rec['W28_verdict_char0']}, agree={rec['AGREE']}",
              flush=True)
    return {"n_cases": len(out), "cases": out,
            "ALL_AGREE": all(v["AGREE"] for v in out.values())}


def c2_k3_not_unit():
    """The T1i singleton case at kmax = 3 must NOT be the unit ideal."""
    out = {}
    for kmax in (3, 4):
        case = T.Case(((), (), ()), kmax=kmax)
        gens = case.build()
        polys = [g for _, g in gens]
        polys.sort(key=lambda p: (len(p.t), p.deg()))
        polys, names = T.compress(polys, case.names)
        try:
            r = T.decide(polys, names, 32003, "std", timeout=2400)
        except Exception as exc:
            r = {"error": str(exc)[:200]}
        out[str(kmax)] = {"n_gens": len(polys), "nv": len(names), **r}
        print(f"  [C2] kmax={kmax}: {len(polys)} gens, unit="
              f"{r.get('isunit')} dim={r.get('dim')} {r.get('error','')}",
              flush=True)
    out["PASS"] = out["3"].get("isunit") == "0"
    return out


def c3_boundary():
    import random
    rng = random.Random(5)
    ts = [{}, {}, {}]
    for e in combinations(range(7), 2):
        ts[0][e] = Fraction(rng.randint(-4, 4), rng.randint(1, 3))
    fe = {c: DG.diag_feasible(ts, c, 4)[0] for c in range(3)}
    fs = {c: DG.free_sites(ts, c) for c in range(3)}
    rec = {"diag_feasible_k4": fe, "free_sites": fs,
           "PASS": fe[0] is True}
    print(f"  [C3] t^1=t^2=0: colour-0 feasible = {fe[0]} (want True)",
          flush=True)
    return rec


def c4_ledger():
    rec = {}
    # ledger 13: the shadowing guard must FIRE
    try:
        C.no_shadow_guard("ring zzR = 0, (zt0_01), dp;\npoly zt0_01 = 1;",
                          {"zt0_01"})
        rec["ledger13_shadow_guard_fires"] = False
    except AssertionError:
        rec["ledger13_shadow_guard_fires"] = True
    # ledger 6/11: the '?'-scan must FIRE on a broken script
    try:
        C.run_singular("ring zzR = 0, (a), dp;\nideal I = notafunction(a);",
                       timeout=60)
        rec["ledger6_question_scan_fires"] = False
    except RuntimeError:
        rec["ledger6_question_scan_fires"] = True
    # ledger 22: Poly.sing must REFUSE a non-integer coefficient
    try:
        K.Poly(1, {(1,): Fraction(1, 3)}).sing(["a"])
        rec["ledger22_denominator_guard_fires"] = False
    except AssertionError:
        rec["ledger22_denominator_guard_fires"] = True
    # independent hafnian engines
    rec["haf_engine_disagreements"] = C.check_haf_agreement(trials=60, seed=3)
    rec["PASS"] = (rec["ledger13_shadow_guard_fires"] and
                   rec["ledger6_question_scan_fires"] and
                   rec["ledger22_denominator_guard_fires"] and
                   rec["haf_engine_disagreements"] == 0)
    print(f"  [C4] ledger battery: {rec}", flush=True)
    return rec


def main():
    t0 = time.time()
    print("=== W29 F1 controls ===", flush=True)
    RES["C4_ledger"] = c4_ledger()
    RAN.append("C4")
    ck("C4")
    RES["C3_boundary"] = c3_boundary()
    RAN.append("C3")
    ck("C3")
    RES["C1_reproduce_W28T1"] = c1_reproduce_w28t1()
    RAN.append("C1")
    ck("C1")
    RES["C2_k3_not_unit"] = c2_k3_not_unit()
    RAN.append("C2")
    ck("C2")
    RES["seconds"] = round(time.time() - t0, 1)
    ck("final")
    manifest = ["C1", "C2", "C3", "C4"]
    missing = [m for m in manifest if m not in RAN]
    if missing:
        raise AssertionError(f"ledger-21: controls did not run: {missing}")
    print(f"wrote {OUT} ({RES['seconds']}s)")


if __name__ == "__main__":
    main()
