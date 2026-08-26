#!/usr/bin/env python3
"""W40 / T6 -- RESTART of W33's unfinished T9 (level-3 rung).

Verbatim copy of W33 run_09_widest.py with three changes: output goes to
the W40 lane (results_t6_t9.json), each level is checkpointed, and the
LEVEL-5 (full-exactness) decision is added -- W40/T3 showed the level-4
system is not the right target, so a level-4 unit verdict on a support is
still a theorem but a level-5 one is what the conjecture needs.

Original header follows.

W33 / T8 -- the WIDER-SUPPORT rung (LEVEL 2 = own-pair-internal AND
internal to at least one other cycle; LEVEL 3 = own-pair-internal only).
See run_07 for the derivation.  Original header:

W33 / T7 -- the TRIPLE-INTERNAL ideal: the whole cross-cell freedom of a
pairwise-Hamiltonian PM triple in ONE Groebner, i.e. every m at once inside
the support the two linear layers allow.

Set-up.  Let (M_0,M_1,M_2) be pairwise disjoint PMs of K_8 with every union
C_{ab} = M_a u M_b a Hamiltonian cycle (exactly two S_8 x S_3 orbits; the
other six disjoint-triple orbits are already dead at m <= 3 by run_04).  For
a cross cell A_e[c][d] (c != d, e' the third colour) the two linear layers
give three necessary conditions when the corresponding kernels are the null
spans and the pair's own cross support is chord-only:

    e internal to C_{cd}   (its own pair restriction, run_03's |X|=1 lemma)
    e internal to C_{d e'} (Ker at the c-endpoint)
    e internal to C_{c e'} (Ker at the d-endpoint)

"internal" = the endpoints are in the same class of the cycle's bipartition
(W33-D1: a perfect matching of K_8 uses equally many internal edges of the
two classes, so a single internal chord is invisible to every word).  The
triple-internal support has 2 cells per ordered colour pair in one orbit and
4 in the other: 12 resp. 24 cross variables, plus the 12 diagonal weights.

This file decides the resulting system exactly (Q and ZZ).  Controls:
  k3_control   the same support with only off-count <= 3 imposed must be
               NOT unit (the diagonal PM-triple point lives there) -- a
               control outside the asserted locus (ledger 18).
  point_control the diagonal PM-triple point satisfies every k=3 generator.
"""
from __future__ import annotations

import itertools
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
W33D = os.path.join(os.path.dirname(HERE), "unaudited-x4general-w33-2026-08-20")
sys.path.insert(0, W33D)
from w33_core import Manifest, no_shadow_guard, require, run_singular  # noqa

OUT = os.path.join(HERE, "results_t6_t9.json")
N = 8
EDG = list(itertools.combinations(range(N), 2))
SEC = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
LEVEL = int(sys.argv[2]) if len(sys.argv) > 2 else 3


def ek(a, b):
    return (a, b) if a < b else (b, a)


def pm_all(vs):
    vs = list(vs)
    if not vs:
        return [()]
    h, rest = vs[0], vs[1:]
    out = []
    for i, x in enumerate(rest):
        for M in pm_all(rest[:i] + rest[i + 1:]):
            out.append((ek(h, x),) + M)
    return out


PMS = [tuple(sorted(M)) for M in pm_all(range(N))]


def offcount(w):
    return N - max(w.count(c) for c in range(3))


IMP = {k: [w for w in itertools.product(range(3), repeat=N)
           if offcount(w) <= k] for k in (3, 4, 5)}


def cycle_order(ma, mb):
    adj = {i: [] for i in range(N)}
    for e in list(ma) + list(mb):
        adj[e[0]].append(e[1])
        adj[e[1]].append(e[0])
    cyc, prev, cur = [0], None, 0
    for _ in range(N - 1):
        nxt = [x for x in adj[cur] if x != prev]
        if not nxt:
            return None
        prev, cur = cur, nxt[0]
        if cur in cyc:
            return None
        cyc.append(cur)
    return cyc if len(cyc) == N else None


def internal(ma, mb):
    cyc = cycle_order(ma, mb)
    if cyc is None:
        return None
    pos = {v: i for i, v in enumerate(cyc)}
    return {ek(u, v) for (u, v) in EDG if (pos[u] - pos[v]) % 2 == 0}


def gens(tri, cross, words):
    cm = {e: [[None] * 3 for _ in range(3)] for e in EDG}
    nv = 0
    for c in range(3):
        for e in tri[c]:
            nv += 1
            cm[e][c][c] = f"zzv({nv})"
    xnames = []
    for (e, a, b) in cross:
        nv += 1
        cm[e][a][b] = f"zzv({nv})"
        xnames.append(f"zzv({nv})")
    out = []
    for w in words:
        terms = []
        for M in PMS:
            mon, ok = [], True
            for (u, v) in M:
                nm = cm[(u, v)][w[u]][w[v]]
                if nm is None:
                    ok = False
                    break
                mon.append(nm)
            if ok:
                terms.append("*".join(sorted(mon)))
        tgt = 1 if len(set(w)) == 1 else 0
        if not terms and tgt == 0:
            continue
        out.append(f"({'+'.join(terms) if terms else '0'})-({tgt})")
    return sorted(set(out)), nv, xnames


def decide(gs, nv, base, timeout, want_dim=False):
    script = (f"ring R = {base}, (zzv(1..{nv})), dp;\n"
              "ideal zzI = " + ",\n ".join(gs) + ";\n"
              "ideal zzG = std(zzI);\n"
              '"UNIT:", (size(zzG) == 1 && zzG[1] == 1);\n'
              + ('"DIM:", dim(zzG);\n' if want_dim else ""))
    no_shadow_guard(script, {f"zzv({i})" for i in range(1, nv + 1)})
    txt = run_singular(script, timeout=timeout)
    out = {}
    for ln in txt.splitlines():
        ln = ln.strip()
        for k in ("UNIT", "DIM"):
            if ln.startswith(k + ":"):
                out[k] = ln.split(":", 1)[1].strip()
    require("UNIT" in out, "parse failure")
    return out


def main():
    t0 = time.time()
    R = {"status": "UNAUDITED",
         "pinned_head": open(os.path.join(HERE, "PINNED_HEAD.txt")).read()
         .strip()}
    if os.path.exists(OUT):
        try:
            R = json.load(open(OUT))
        except Exception:
            pass
    MAN = Manifest(["point_control", "k3_control", "main_decision"])
    # ---- the two pairwise-Hamiltonian triple classes
    reps = {}
    for i, j, k in itertools.combinations(range(len(PMS)), 3):
        A, B, C = set(PMS[i]), set(PMS[j]), set(PMS[k])
        if A & B or A & C or B & C:
            continue
        I = {}
        ok = True
        for (x, y, key) in ((A, B, (0, 1)), (A, C, (0, 2)), (B, C, (1, 2))):
            s = internal(x, y)
            if s is None:
                ok = False
                break
            I[key] = s
        if not ok:
            continue
        cross = []
        ncls = [0]
        for (c, d) in [(x, y) for x in range(3) for y in range(3) if x != y]:
            e3 = [z for z in range(3) if z not in (c, d)][0]
            own = I[tuple(sorted((c, d)))]
            o1 = I[tuple(sorted((d, e3)))]
            o2 = I[tuple(sorted((c, e3)))]
            if LEVEL == 2:
                S = own & (o1 | o2)
            else:
                S = own
            for e in sorted(S):
                cross.append((e, c, d))
            tin = own & o1 & o2
            ncls[0] += len(tin)
        cls = ncls[0]
        if cls not in reps:
            reps[cls] = ([sorted(A), sorted(B), sorted(C)], cross)
        if len(reps) >= 2:
            break
    print("triple-internal classes:", sorted(reps), flush=True)
    R["classes"] = sorted(reps)
    for cls in sorted(reps):
        tri, cross = reps[cls]
        key = str(cls)
        if key in R.get("done", {}):
            continue
        gs3, nv, xn = gens(tri, cross, IMP[3])
        # point control: the diagonal PM-triple point (all weights 1, all
        # cross cells 0) must satisfy every k=3 generator
        sub = ",".join(["1"] * 12 + ["0"] * len(cross))
        script = (f"ring R = 0, (zzv(1..{nv})), dp;\n"
                  "ideal zzI = " + ",\n ".join(gs3) + ";\n"
                  f"ideal zzP = {sub};\n"
                  "map zzM = R, zzP;\n"
                  "ideal zzE = zzM(zzI);\n"
                  '"UNIT:", 0;\n'
                  '"EVAL:", size(simplify(zzE,2));\n')
        no_shadow_guard(script, {f"zzv({i})" for i in range(1, nv + 1)})
        txt = run_singular(script, timeout=600)
        ev = [ln for ln in txt.splitlines() if ln.strip().startswith("EVAL:")]
        require(ev and ev[0].split(":")[1].strip() == "0",
                f"point control FAILED (class {cls}): the diagonal PM-triple "
                f"does not satisfy the k=3 system: {ev}")
        o3 = decide(gs3, nv, 0, 1800, want_dim=True)
        require(o3["UNIT"] in ("0", "FALSE", "false"),
                f"k=3 control FAILED (class {cls}): unit although a point "
                f"exists: {o3}")
        MAN.mark("point_control")
        MAN.mark("k3_control")
        print(f"class {cls}: k=3 control OK (not unit, dim {o3.get('DIM')})",
              flush=True)
        gs4, nv4, xn4 = gens(tri, cross, IMP[4])
        gs5, nv5, xn5 = gens(tri, cross, IMP[5])
        R.setdefault("systems", {})[key] = {
            "n_cross": len(cross), "n_vars": nv4, "n_gens_k4": len(gs4),
            "n_gens_k3": len(gs3), "k3_dim": o3.get("DIM"),
            "cross_support": [str(c) for c in cross],
            "triple": [[list(e) for e in m] for m in tri]}
        with open(OUT, "w") as fh:
            json.dump(R, fh, indent=1, sort_keys=True)
        R["systems"][key]["n_gens_k5"] = len(gs5)
        for lvl, gsx, nvx in ((5, gs5, nv5), (4, gs4, nv4)):
            for base in (0, "integer"):
                tag = "Q" if base == 0 else "ZZ"
                try:
                    ox = decide(gsx, nvx, base,
                                max(600, int(SEC - (time.time() - t0))))
                except Exception as ex:
                    R["systems"][key][f"k{lvl}_{tag}"] = \
                        f"unchecked {str(ex)[:100]}"
                    print(f"class {cls} k={lvl} {tag}: {str(ex)[:160]}",
                          flush=True)
                    with open(OUT, "w") as fh:
                        json.dump(R, fh, indent=1, sort_keys=True)
                    continue
                R["systems"][key][f"k{lvl}_{tag}_unit"] = ox["UNIT"]
                print(f"class {cls} k={lvl} over {tag}: UNIT = {ox['UNIT']}",
                      flush=True)
                with open(OUT, "w") as fh:
                    json.dump(R, fh, indent=1, sort_keys=True)
        R.setdefault("done", {})[key] = True
        with open(OUT, "w") as fh:
            json.dump(R, fh, indent=1, sort_keys=True)
    MAN.mark("main_decision")
    R["manifest"] = MAN.assert_complete()
    R["elapsed"] = time.time() - t0
    with open(OUT, "w") as fh:
        json.dump(R, fh, indent=1, sort_keys=True)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
