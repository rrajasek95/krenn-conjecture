#!/usr/bin/env python3
"""W29 C1 -- run the vanishing-pattern abstraction over the whole T1i ledger,
with the positive controls that alone make an UNSAT verdict believable.

argv: [what]   what in {controls, orbits, all4096, everything}
"""
from __future__ import annotations

import json
import random
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
import w28_diag as DG                                               # noqa: E402
import w29_core as C                                                # noqa: E402
import w29_t1i as T                                                 # noqa: E402
import w29_van as V                                                 # noqa: E402

SOLVERS = ("cadical153", "glucose42", "minisat22", "maplesat", "mergesat3")
RES, RAN = {}, []
OUT = None
VP = T.VP


def ck(tag=""):
    RES["ran"] = RAN
    with open(OUT, "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
    if tag:
        print(f"      [checkpoint {tag}]", flush=True)


# --------------------------------------------------- point -> z-assignment
def z_assignment(van, ts, xs=None):
    """The assignment a TRUE point induces; returns (assign, violated)."""
    A = {}
    for key, v in van.lit.items():
        if key[0] == "z":
            _, c, S = key
            A[v] = (C.haf(ts[c], S) == 0)
        elif key[0] == "xnz":
            _, c, y = key
            A[v] = bool(xs and xs.get((c, y), 0) != 0)
        elif key[0] == "q":
            _, c, S, w, u = key
            rest = tuple(x for x in S if x not in (w, u))
            A[v] = (ts[c].get(C.ekey(w, u), 0) != 0
                    and C.haf(ts[c], rest) != 0)
        elif key[0] == "b":
            _, c, y = key
            A[v] = (C.haf(ts[c], tuple(x for x in VP if x != y)) != 0
                    and bool(xs and xs.get((c, y), 0) != 0))
        elif key[0] == "tn":
            _, c, S0, y = key
            A[v] = (C.haf(ts[c], tuple(x for x in S0 if x != y)) != 0
                    and bool(xs and xs.get((c, y), 0) != 0))
        elif key[0] == "u":
            _, c, S0 = key
            F = set(van.case.F[c])
            s = Fraction(0)
            for y in sorted(F & set(S0)):
                s += C.haf(ts[c], tuple(x for x in S0 if x != y)) \
                    * Fraction(xs.get((c, y), 0) if xs else 0)
            A[v] = (s == 0)
        else:
            A[v] = False
    viol = []
    for cl in van.cls:
        ok = False
        for lit in cl:
            val = A.get(abs(lit), False)
            if (lit > 0) == val:
                ok = True
                break
        if not ok:
            viol.append(cl)
    return A, viol


def pt_t1h():
    ts = [{}, {}, {}]
    sp = {0: (1, 2), 1: (0, 2), 2: (0, 1)}
    for c in range(3):
        ts[c][sp[c]] = Fraction(1)
        ts[c][(3, 4)] = Fraction(1)
        ts[c][(5, 6)] = Fraction(1)
    return ts


class T1hVan(V.Van):
    """T1h only: FREE at y_c + h_c(y_c) != 0.  It HAS points (W29-A1), so the
    abstraction MUST be satisfiable -- the sharpest positive control."""

    def build(self):
        for c in range(3):
            for m in (0, 2, 4, 6):
                for S in combinations(VP, m):
                    self.z(c, S)
        for c in range(3):
            for m in (4, 6):
                for S in combinations(VP, m):
                    for w in S:
                        big = [self.z(c, S)]
                        for u in S:
                            if u == w:
                                continue
                            rest = tuple(x for x in S if x not in (w, u))
                            q = self.var(("q", c, S, w, u))
                            self.cls.append([-q, -self.z(c, (w, u))])
                            self.cls.append([-q, -self.z(c, rest)])
                            big.append(q)
                        self.cls.append(big)
        for (tag, _p) in self.case.build():
            if tag[0] == "FREE":
                _, c, y, S1, S2 = tag
                d, e = [x for x in range(3) if x != c]
                self.cls.append(self._factor_clause([(d, S1), (e, S2)]))
            elif tag[0] in ("NORM", "RAB"):
                c = tag[1]
                self.cls.append([-self.z(c, tuple(x for x in VP
                                                  if x != T.YS[c]))])
        return self


def controls():
    print("=== C1 CONTROLS ===", flush=True)
    rec = {}
    # (a) T1h abstraction must be SAT and must ACCEPT the A1 point
    van = T1hVan(T.Case(((), (), ()))).build()
    sat = not van.is_unsat()
    A, viol = z_assignment(van, pt_t1h())
    rec["T1h_abstraction"] = {"n_vars": van.n, "n_clauses": len(van.cls),
                              "SAT": sat, "A1_point_violations": len(viol),
                              "PASS": sat and not viol}
    print(f"[ctrl a] T1h abstraction SAT={sat}; the A1 point violates "
          f"{len(viol)} of its {len(van.cls)} clauses (want 0)", flush=True)
    RAN.append("ctrl_T1h_positive")

    # (b) the FULL singleton abstraction must REJECT the A1 point
    van4 = V.van_for(((), (), ()))
    A, viol4 = z_assignment(van4, pt_t1h())
    rec["singleton_rejects_A1"] = {"violations": len(viol4),
                                   "PASS": len(viol4) > 0,
                                   "example": [str(van4.names.get(abs(l)))
                                               for l in (viol4[0] if viol4
                                                         else [])][:6]}
    print(f"[ctrl b] the A1 point violates {len(viol4)} singleton-case "
          f"clauses (want > 0)", flush=True)
    RAN.append("ctrl_rejects_A1")

    # (c) k = 3 MUST be satisfiable (X_3 points with all three colours exist)
    k3 = {}
    for Rs in (((), (), ()), ((3,), (3,), (3,)), ((3, 4, 5, 6),) * 3):
        v3 = V.van_for(Rs, kmax=3)
        k3[str(Rs)] = {"n_clauses": len(v3.cls), "SAT": not v3.is_unsat()}
        print(f"[ctrl c] k=3 case {Rs}: SAT={k3[str(Rs)]['SAT']} (want True)",
              flush=True)
    rec["k3_must_be_sat"] = k3
    rec["k3_PASS"] = all(v["SAT"] for v in k3.values())
    RAN.append("ctrl_k3")

    # (d) a REAL three-colour X_3 background must be accepted by its own k=3
    #     abstraction -- the end-to-end soundness control
    rng = random.Random(2026)
    found = None
    tries = 0
    while found is None and tries < 60000:
        tries += 1
        ts = [{}, {}, {}]
        for c in range(3):
            for e in combinations(VP, 2):
                if rng.random() < 0.30:
                    ts[c][e] = Fraction(rng.randint(-3, 3), rng.randint(1, 2))
        prof = DG.rung_profile(ts, ks=(3,))
        if prof.get(3, 0) == 3:
            found = ts
    rec["x3_witness_search"] = {"tries": tries, "found": found is not None}
    if found is not None:
        fs = {c: DG.free_sites(found, c) for c in range(3)}
        rec["x3_witness"] = {"free_sites": fs,
                             "supp": {c: [list(e) for e in found[c]]
                                      for c in range(3)}}
        print(f"[ctrl d] found a three-colour X_3 background after {tries} "
              f"draws; free sets {fs}", flush=True)
    else:
        print(f"[ctrl d] no three-colour X_3 background in {tries} draws "
              f"(control not exercised)", flush=True)
    RAN.append("ctrl_x3_witness")

    # (e) cross-solver agreement on the headline UNSAT
    xs = {}
    for nm in SOLVERS:
        try:
            xs[nm] = V.van_for(((), (), ())).is_unsat(solver=nm)
        except Exception as exc:
            xs[nm] = f"error {str(exc)[:80]}"
    rec["cross_solver_singleton_unsat"] = xs
    print(f"[ctrl e] cross-solver UNSAT verdicts: {xs}", flush=True)
    RAN.append("ctrl_cross_solver")
    return rec


def run_orbits(kmax=4):
    reps = T.case_orbit_reps()
    reps.sort(key=lambda r: (sum(len(x) for x in r[0]), r[0]))
    out, nsat = {}, 0
    t0 = time.time()
    for i, (Rs, sz) in enumerate(reps):
        van = V.van_for(Rs, kmax=kmax)
        u = van.is_unsat()
        out[str(Rs)] = {"orbit_size": sz, "UNSAT": u,
                        "n_clauses": len(van.cls)}
        if not u:
            nsat += 1
            mod = van.solve(budget=1)
            out[str(Rs)]["model"] = mod[0] if mod else None
            print(f"  !! SAT case {Rs} (orbit {sz})", flush=True)
    print(f"[orbits k={kmax}] {len(reps)} orbits, {nsat} satisfiable "
          f"({round(time.time()-t0,1)}s)", flush=True)
    return {"n_orbits": len(reps), "n_sat": nsat, "cases": out,
            "secs": round(time.time() - t0, 1)}


def run_all4096(kmax=4):
    allR = [tuple(S) for k in range(5) for S in combinations(T.Q, k)]
    t0 = time.time()
    nsat, sats = 0, []
    n = 0
    for R0 in allR:
        for R1 in allR:
            for R2 in allR:
                van = V.van_for((R0, R1, R2), kmax=kmax)
                n += 1
                if not van.is_unsat():
                    nsat += 1
                    sats.append([list(R0), list(R1), list(R2)])
        print(f"    ... {n}/4096 done, {nsat} SAT "
              f"({round(time.time()-t0,1)}s)", flush=True)
    return {"n_cases": n, "n_sat": nsat, "sat_cases": sats[:50],
            "secs": round(time.time() - t0, 1)}


def main():
    global OUT
    what = sys.argv[1] if len(sys.argv) > 1 else "everything"
    OUT = f"{BASE}/results_c1_van_{what}.json"
    t0 = time.time()
    if what in ("controls", "everything"):
        RES["controls"] = controls()
        ck("controls")
    if what in ("orbits", "everything"):
        RES["orbits_k4"] = run_orbits(4)
        RAN.append("orbits_k4")
        ck("orbits")
    if what in ("all4096", "everything"):
        RES["all4096_k4"] = run_all4096(4)
        RAN.append("all4096_k4")
        ck("all4096")
    RES["seconds"] = round(time.time() - t0, 1)
    ck("final")
    print(f"wrote {OUT} ({RES['seconds']}s)")


if __name__ == "__main__":
    main()
