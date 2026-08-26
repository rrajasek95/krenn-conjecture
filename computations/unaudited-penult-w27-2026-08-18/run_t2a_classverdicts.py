#!/usr/bin/env python3
"""W27 T2a -- THE PER-PAIR WITNESS/BLOCKED TABLE OF THE 24 N=6 DIAGONAL CLASSES.

W25 measured only the COUNT of witnesses per class (constant across every
sampled weight point -- the phenomenon this probe has to explain) and the set
of pairs on which its antisymmetric cap is identically zero (a strict subset:
n_uniform < witness count in 13 of the 24 classes).  To find the SKELETON LAW
we need the actual per-pair verdicts, so this runner recomputes them exactly
and stores, alongside each verdict, the structural data of the pair.

Checkpoints after every class (the machine sleeps).
"""
from __future__ import annotations

import json
import os
import random
import sys
import time
from fractions import Fraction
from itertools import combinations

BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-penult-w27-2026-08-18")
W25BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
           "unaudited-x3core-w25-2026-08-15")
sys.path.insert(0, BASE)
sys.path.insert(0, W25BASE)
import w27_core as W                                              # noqa: E402
import w25_core as C                                              # noqa: E402
import w25_decide as D                                            # noqa: E402
import run_t1d_diagonal as T1D                                    # noqa: E402
import run_t1e_diagonal_uniform as T1E                            # noqa: E402

N = 6
OUT = f"{BASE}/results_t2a_classverdicts.json"
RES = {"classes": {}}
RAN = []
NPTS = int(os.environ.get("W27_NPTS", "3"))


def control(name):
    if name not in RAN:
        RAN.append(name)


def ck(tag=""):
    RES["ran"] = RAN
    with open(OUT, "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
    if tag:
        print(f"      [checkpoint {tag}]", flush=True)


# ------------------------------------------------------- structural features

def features(Ls, p, q):
    """Every structural datum of the pair (p,q) in the skeleton Ls."""
    ed = [set(T1D.mask_edges(L)) for L in Ls]
    e = tuple(sorted((p, q)))
    c1 = [c for c in range(3) if e in ed[c]]
    assert len(c1) == 1, (Ls, e, c1)
    c1 = c1[0]
    c2, c3 = [c for c in range(3) if c != c1]

    def deg(v, c):
        return sum(1 for f in ed[c] if v in f)

    def nb(v, c):
        return sorted(x for f in ed[c] for x in f if v in f and x != v)

    degp = [deg(p, c) for c in range(3)]
    degq = [deg(q, c) for c in range(3)]
    cleanp = degp == [1, 1, 1]
    cleanq = degq == [1, 1, 1]
    # the off-colour graph L_c2 u L_c3 (the graph the antisymmetric cap acts on)
    off = ed[c2] | ed[c3]
    adj = {v: set() for v in range(N)}
    for (a, b) in off:
        adj[a].add(b)
        adj[b].add(a)
    seen, comps = set(), []
    for v in range(N):
        if v in seen:
            continue
        st, comp = [v], set([v])
        seen.add(v)
        while st:
            x = st.pop()
            for y in adj[x]:
                if y not in comp:
                    comp.add(y)
                    seen.add(y)
                    st.append(y)
        comps.append(sorted(comp))
    pc = [i for i, cc in enumerate(comps) if p in cc][0]
    qc = [i for i, cc in enumerate(comps) if q in cc][0]
    # distance p->q in the off-colour graph
    import collections
    dist = None
    dq = collections.deque([(p, 0)])
    vis = {p}
    while dq:
        x, d = dq.popleft()
        if x == q:
            dist = d
            break
        for y in adj[x]:
            if y not in vis:
                vis.add(y)
                dq.append((y, d + 1))
    rest = tuple(x for x in range(N) if x not in (p, q))
    npm_rest = [T1D.npm_sub(Ls[c], e) for c in range(3)]
    nclean_other = sum(1 for v in rest
                       if [deg(v, c) for c in range(3)] == [1, 1, 1])
    # PMs of the WHOLE skeleton through pq, and total live edges
    liveedges = ed[0] | ed[1] | ed[2]
    return {
        "colour": c1,
        "profile": sorted(bin(L).count("1") for L in Ls),
        "sizes": [bin(L).count("1") for L in Ls],
        "deg_p": degp, "deg_q": degq,
        "clean_p": cleanp, "clean_q": cleanq,
        "n_clean_endpoints": int(cleanp) + int(cleanq),
        "n_clean_other": nclean_other,
        "live_deg_p": sum(degp), "live_deg_q": sum(degq),
        "deg_c1_p": degp[c1], "deg_c1_q": degq[c1],
        "deg_off_p": sorted([degp[c2], degp[c3]]),
        "deg_off_q": sorted([degq[c2], degq[c3]]),
        "off_comp_sizes": sorted(len(x) for x in comps),
        "off_n_comps": len(comps),
        "off_same_comp": pc == qc,
        "off_comp_p_size": len(comps[pc]),
        "off_comp_q_size": len(comps[qc]),
        "off_dist_pq": dist,
        "off_deg_p": len(adj[p]), "off_deg_q": len(adj[q]),
        "npm_rest": npm_rest,
        "npm_rest_c1": npm_rest[c1],
        "npm_rest_off": sorted([npm_rest[c2], npm_rest[c3]]),
        "n_live_edges": len(liveedges),
    }


def sample_points(Ls, rng, k):
    return T1E.sample_points(Ls, rng, k=k)


def main():
    t0 = time.time()
    rng = random.Random(271828)
    print("rebuilding the diagonal skeleton classes at N=6 ...", flush=True)
    surv = T1E._survivors()
    classes = sorted(set(T1D.canonical(Ls) for Ls in surv))
    print(f"   survivors {len(surv)}, classes {len(classes)} "
          f"(W25 reported 40710 / 24)")
    RES["n_survivors"] = len(surv)
    RES["n_classes"] = len(classes)
    assert len(classes) == 24, len(classes)
    control("T2a0_class_reproduction")
    ck("classes")

    for i, cn in enumerate(classes):
        key = str(i)
        if key in RES["classes"] and RES["classes"][key].get("done"):
            continue
        prof = sorted(bin(L).count("1") for L in cn)
        edges = {c: T1D.mask_edges(L) for c, L in enumerate(cn)}
        live = sorted(set((p, q) for c in range(3) for (p, q) in edges[c]))
        feats = {f"{p},{q}": features(cn, p, q) for (p, q) in live}
        pts = sample_points(cn, rng, NPTS)
        rows = []
        for j, w in enumerate(pts):
            src = T1D.build_source(cn, w)
            assert C.in_Xk(src, N, 2)[0] and C.in_Xk(src, N, 3)[0]
            vv = {}
            for (p, q) in live:
                U = tuple(x for x in range(N) if x not in (p, q))
                v, d, mp = D.decide_pair(src, p, q, U, f"W{i}_{j}_{p}{q}",
                                         primes=())
                vv[f"{p},{q}"] = v
            rows.append({"point": {str(k): str(x) for k, x in w.items()},
                         "verdicts": vv})
            RES["classes"][key] = {"idx": i, "masks": list(cn),
                                   "profile": prof, "live": len(live),
                                   "edges": {c: [list(x) for x in edges[c]]
                                             for c in range(3)},
                                   "features": feats, "points": rows,
                                   "done": False}
            ck(f"class{i}_pt{j}")
        # constancy check
        sets = [tuple(sorted(k for k, v in r["verdicts"].items()
                             if v == "WITNESS")) for r in rows]
        const = len(set(sets)) <= 1
        RES["classes"][key]["constant_across_points"] = const
        RES["classes"][key]["witness_pairs"] = list(sets[0]) if sets else []
        RES["classes"][key]["n_witness"] = len(sets[0]) if sets else None
        RES["classes"][key]["done"] = True
        print(f"   class {i:2d} profile {prof} live {len(live):2d}: witnesses "
              f"{len(sets[0]) if sets else '?'} over {len(rows)} points; "
              f"CONSTANT {const}", flush=True)
        ck(f"class{i}")
    control("T2a1_per_pair_verdicts")

    allconst = all(v.get("constant_across_points")
                   for v in RES["classes"].values())
    print(f"witness set constant across weight points in EVERY class: "
          f"{allconst}")
    RES["all_constant"] = allconst
    control("T2a2_constancy")

    declared = ["T2a0_class_reproduction", "T2a1_per_pair_verdicts",
                "T2a2_constancy"]
    missing = [x for x in declared if x not in RAN]
    RES["manifest"] = {"declared": declared, "ran": RAN, "missing": missing}
    RES["seconds"] = round(time.time() - t0, 1)
    print(f"CONTROL MANIFEST: declared {len(declared)}, ran {len(RAN)}, "
          f"missing {missing}")
    assert not missing
    ck("final")
    print(f"wrote {OUT} ({RES['seconds']}s)")


if __name__ == "__main__":
    if os.path.exists(OUT):
        try:
            with open(OUT) as fh:
                old = json.load(fh)
            if "classes" in old:
                RES.update(old)
                RES["classes"] = old["classes"]
                RAN.extend(old.get("ran", []))
                print(f"resuming: {sum(1 for v in RES['classes'].values() if v.get('done'))} "
                      f"classes already done")
        except Exception as ex:                                   # noqa: BLE001
            print(f"could not resume ({ex}); starting fresh")
    main()
