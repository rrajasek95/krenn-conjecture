#!/usr/bin/env python3
"""W29 A1 -- IS THE T1h IDEAL THE UNIT IDEAL?  (the explicit-point control that
W28's non-terminating run never got.)

W28's T1h encodes the THREE-FREE-SITE relaxation of the diagonal X_4 problem:
sites y_0, y_1, y_2 of V' = {0..6} (WLOG 0, 1, 2), and

   (F_c)  haf(t^d | S_1) haf(t^e | S_2) = 0  for every even split (S_1,S_2)
          of W_c = V' - y_c            ({d,e} = the two colours != c)
   (N_c)  haf(t^c | W_c) != 0                          [Rabinowitsch zt_c]

96 cubics + 3 Rabinowitsch relations, 66 variables; it timed out at 900 s.
The campaign's plan is to make it terminate.  THE CLAIM TESTED HERE: it cannot
terminate with a unit verdict, because the variety is NON-EMPTY.

THE CONSTRUCTION (W29-A1).  Write Q = {3,4,5,6} and put

    t^0 = a0 * e_{12}  +  (any weights on the six Q-edges),
    t^1 = a1 * e_{02}  +  (any weights on the six Q-edges),
    t^2 = a2 * e_{01}  +  (any weights on the six Q-edges),

everything else zero -- 3 + 18 = 21 free parameters.  Then inside W_0 =
{1,...,6} the ONLY t^1- and t^2-edges are Q-edges, so haf(t^1|S_1) != 0 forces
S_1 subset Q and haf(t^2|S_2) != 0 forces S_2 subset Q, which is impossible
for a split of a set containing {1,2}: EVERY product in (F_0) vanishes
identically.  Cyclically for (F_1), (F_2).  And
haf(t^c|W_c) = a_c * haf(t^c|Q) != 0 generically, so (N_c) holds.

This script proves that SYMBOLICALLY (the 96 generators of T1h are identically
zero on the 21-parameter family), and again NUMERICALLY at an explicit integer
point through W28's OWN generator builder, and then checks what the point does
to the true system.

argv: none.
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
import w29_core as C                                                # noqa: E402
import w28_core as K                                                # noqa: E402
import w28_diag as DG                                               # noqa: E402
import run_t1d_diagelim as D                                        # noqa: E402

NS = 7
VP = tuple(range(NS))
Q = (3, 4, 5, 6)
QE = tuple(combinations(Q, 2))
YS = (0, 1, 2)
SPECIAL = {0: (1, 2), 1: (0, 2), 2: (0, 1)}     # the non-Q edge of colour c
RES = {}
OUT = f"{BASE}/results_a1_t1h_refute.json"
RAN = []


def ck(tag=""):
    RES["ran"] = RAN
    with open(OUT, "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
    if tag:
        print(f"      [checkpoint {tag}]", flush=True)


def even_splits(W):
    out = []
    for m in range(0, len(W) + 1, 2):
        for S1 in combinations(W, m):
            out.append((S1, tuple(x for x in W if x not in S1)))
    return out


# ------------------------------------------------------------ the family
def family_names():
    nm = [f"a{c}" for c in range(3)]
    for c in range(3):
        for e in QE:
            nm.append(f"q{c}_{e[0]}{e[1]}")
    return nm


def family_symbolic():
    """t[c] as dicts edge -> Poly in the 21 family parameters."""
    nv = 3 + 3 * len(QE)
    t = [{}, {}, {}]
    for c in range(3):
        t[c][C.ekey(*SPECIAL[c])] = K.Poly.var(nv, c)
    i = 3
    for c in range(3):
        for e in QE:
            t[c][e] = K.Poly.var(nv, i)
            i += 1
    return t, family_names(), nv


def family_point(kind="unit", seed=7):
    """Exact rational specialisation of the family."""
    import random
    rng = random.Random(seed)
    t = [{}, {}, {}]
    for c in range(3):
        t[c][C.ekey(*SPECIAL[c])] = Fraction(1)
    for c in range(3):
        if kind == "unit":                 # the perfect matching {34},{56}
            t[c][(3, 4)] = Fraction(1)
            t[c][(5, 6)] = Fraction(1)
        else:                              # dense random Q-block
            for e in QE:
                t[c][e] = Fraction(rng.randint(-5, 5), rng.randint(1, 3))
    return t


# ----------------------------------------------------- step 1: symbolic proof
def step_symbolic():
    t, nm, nv = family_symbolic()
    zero, one = K.Poly.const(nv, 0), K.Poly.const(nv, 1)
    nz, tot = [], 0
    for c in range(3):
        d, e = [x for x in range(3) if x != c]
        W = tuple(x for x in VP if x != YS[c])
        for (S1, S2) in even_splits(W):
            g = C.haf(t[d], S1, zero, one) * C.haf(t[e], S2, zero, one)
            tot += 1
            if g.t:
                nz.append((c, S1, S2, len(g.t)))
    rab = []
    for c in range(3):
        W = tuple(x for x in VP if x != YS[c])
        h = C.haf(t[c], W, zero, one)
        rab.append((c, len(h.t), sorted(h.t.items())[:3]))
    RES["A1_symbolic"] = {
        "n_free_generators": tot,
        "n_nonzero_on_family": len(nz),
        "nonzero_examples": nz[:5],
        "rabinowitsch_haf_terms": [(c, k) for (c, k, _) in rab],
        "verdict": ("ALL 96 T1h FREE GENERATORS VANISH IDENTICALLY ON THE "
                    "21-PARAMETER FAMILY" if not nz else "FAMILY FAILS"),
    }
    RAN.append("A1_symbolic")
    print(f"[A1 symbolic] {tot} free generators, {len(nz)} nonzero on the "
          f"family; haf(t^c|W_c) has {[k for (_, k, _) in rab]} terms")
    ck("A1_symbolic")
    return not nz


# ------------------------------------------- step 2: W28's own builder, exact
def t1h_generators_w28(ys=YS):
    """EXACTLY W28 run_t1h_triplefree's generator list (mode 'full')."""
    t, names0, nv0, xoff = D.build_symbolic("full")
    names0 = names0[:xoff]
    nv = xoff + 3

    def lift(p):
        return K.Poly(nv, {k2 + (0, 0, 0): v for k2, v in p.t.items()})

    hc = {}

    def haf_c(c, S):
        key = (c, S)
        if key not in hc:
            hc[key] = lift(D.haf_poly(t[c], S, xoff))
        return hc[key]

    gens, tags = [], []
    for c in range(3):
        d, e = [x for x in range(3) if x != c]
        y = ys[c]
        W = tuple(x for x in VP if x != y)
        for (S1, S2) in even_splits(W):
            P = haf_c(d, S1) * haf_c(e, S2)
            if P.t:
                gens.append(P)
                tags.append(("FREE", c, y, S1, S2))
    rab = []
    for c in range(3):
        W = tuple(x for x in VP if x != ys[c])
        rab.append(haf_c(c, W))
    names = names0 + ["zt0", "zt1", "zt2"]
    return gens, tags, rab, names, nv, xoff


def point_vector(t, nv, xoff):
    """W28 'full' variable order: index 3*edge_index + colour."""
    vals = [Fraction(0)] * nv
    for i, (a, b) in enumerate(combinations(VP, 2)):
        for c in range(3):
            vals[3 * i + c] = Fraction(t[c].get((a, b), 0))
    return vals


def step_numeric(kind, seed=7):
    t = family_point(kind, seed)
    gens, tags, rab, names, nv, xoff = t1h_generators_w28()
    vals = point_vector(t, nv, xoff)
    nzero = 0
    firstbad = None
    for g, tg in zip(gens, tags):
        v = g.subs_num(vals)
        if v != 0:
            nzero += 1
            if firstbad is None:
                firstbad = (str(tg), str(v))
    hs = [r.subs_num(vals) for r in rab]
    rec = {"kind": kind, "seed": seed, "n_generators": len(gens),
           "n_violated": nzero, "first_violation": firstbad,
           "haf_c_Wc": [str(h) for h in hs],
           "rabinowitsch_ok": all(h != 0 for h in hs),
           "T1H_POINT": (nzero == 0 and all(h != 0 for h in hs))}
    RES.setdefault("A1_numeric", {})[f"{kind}_{seed}"] = rec
    RAN.append(f"A1_numeric_{kind}_{seed}")
    print(f"[A1 numeric {kind}/{seed}] {len(gens)} W28 generators, "
          f"{nzero} violated; haf(t^c|W_c) = {[str(h) for h in hs]}; "
          f"IS A T1h POINT: {rec['T1H_POINT']}")
    ck(f"A1_numeric_{kind}_{seed}")
    return rec["T1H_POINT"]


# ---------------------------------------------- step 3: what the point is NOT
def step_truth(kind, seed=7):
    """The point satisfies T1h but must NOT be X_4-feasible (else escalate)."""
    t = family_point(kind, seed)
    ts = [t[0], t[1], t[2]]
    rec = {}
    rec["free_sites"] = {c: DG.free_sites(ts, c) for c in range(3)}
    rec["h_c_of_y"] = {c: {y: str(C.haf(ts[c], tuple(x for x in VP if x != y)))
                           for y in VP} for c in range(3)}
    fe = {}
    for k in (2, 3, 4):
        fe[k] = {c: DG.diag_feasible(ts, c, k)[0] for c in range(3)}
    rec["diag_feasible"] = fe
    rec["n_colours_feasible_k4"] = sum(1 for c in range(3) if fe[4][c])
    RES.setdefault("A1_truth", {})[f"{kind}_{seed}"] = rec
    RAN.append(f"A1_truth_{kind}_{seed}")
    print(f"[A1 truth {kind}/{seed}] free sets {rec['free_sites']}; "
          f"X_4-feasible colours: {fe[4]}")
    ck(f"A1_truth_{kind}_{seed}")
    return rec


# ------------------------------------------------ step 4: Singular confirmation
def step_singular(kind="unit", seed=7, char=0):
    """Substitute the point into the T1h ideal inside Singular and check that
    the generators reduce to 0 there (an engine-independent confirmation)."""
    t = family_point(kind, seed)
    gens, tags, rab, names, nv, xoff = t1h_generators_w28()
    vals = point_vector(t, nv, xoff)
    sub = []
    for i, nmv in enumerate(names[:xoff]):
        sub.append(f"{nmv}-({vals[i].numerator})")   # all integers here
    lines = [f"ring zzR = {char}, ({','.join(names)}), dp;",
             "ideal zzPT = " + ",".join(sub) + ";",
             "ideal zzJ = " + ",".join(g.sing(names) for g in
                                       K.clear_denoms(gens)[0]) + ";",
             "ideal zzR2 = reduce(zzJ, std(zzPT));",
             '"MAXRED "; size(zzR2);',
             'int zzs = 0; int zzi; for (zzi=1; zzi<=size(zzR2); zzi++)'
             ' { if (zzR2[zzi]!=0) { zzs = zzs+1; } }',
             '"NONZERO "; zzs;']
    sc = "\n".join(lines)
    C.no_shadow_guard(sc, set(names))
    out = C.run_singular(sc, timeout=900)
    tk = out.split()
    rec = {"char": char, "nonzero_after_substitution":
           tk[tk.index("NONZERO") + 1]}
    RES.setdefault("A1_singular", {})[f"{kind}_{seed}_c{char}"] = rec
    RAN.append(f"A1_singular_{kind}_{seed}_c{char}")
    print(f"[A1 Singular char {char}] generators nonzero at the point: "
          f"{rec['nonzero_after_substitution']}")
    ck(f"A1_singular_{kind}_{seed}_c{char}")
    return rec


def main():
    t0 = time.time()
    print("=== W29 A1: the T1h explicit-point control ===", flush=True)
    bad = C.check_haf_agreement()
    RES["control_haf_engines_disagree"] = bad
    RAN.append("control_haf_engines")
    print(f"[control] independent hafnian engines disagree on {bad} draws "
          f"(want 0)", flush=True)
    ck("haf")
    ok_sym = step_symbolic()
    ok_num = step_numeric("unit", 7)
    for sd in (1, 2, 3):
        step_numeric("random", sd)
    step_truth("unit", 7)
    step_truth("random", 1)
    try:
        step_singular("unit", 7, 0)
    except Exception as exc:
        RES.setdefault("A1_singular", {})["error"] = str(exc)[:400]
        print(f"[A1 Singular] FAILED {str(exc)[:200]}")
    RES["CONCLUSION"] = (
        "W29-A1 [PROVED-HERE]: the W28 T1h three-free-site ideal is NOT the "
        "unit ideal -- its variety contains an explicit 21-parameter family "
        "of rational points.  No amount of Groebner effort can make T1h "
        "return 'unit'; the formulation is too weak to close the diagonal "
        "family and must be strengthened."
        if (ok_sym and ok_num) else
        "A1 did NOT establish the T1h point -- see the records")
    RES["seconds"] = round(time.time() - t0, 1)
    ck("final")
    print(">>> " + RES["CONCLUSION"])
    print(f"wrote {OUT} ({RES['seconds']}s)")
    manifest = ["control_haf_engines", "A1_symbolic", "A1_numeric_unit_7",
                "A1_truth_unit_7"]
    missing = [m for m in manifest if m not in RAN]
    require(not missing, f"ledger-21: controls did not run: {missing}")


def require(c, d):
    if not c:
        raise AssertionError(d)


if __name__ == "__main__":
    main()
