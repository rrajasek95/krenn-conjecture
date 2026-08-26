#!/usr/bin/env python3
r"""W31 -- LEMMA W31-2 CANDIDATE: does every stratum class embed GHZ_4 copies?
UNAUDITED PROBE.  Exact integer / pattern arithmetic only.  Seconds.

BACKGROUND.  The C_8 stratum member's twelve single cells were found to be two
disjoint copies of the classical N=4 exceptional source GHZ_4^3 -- K_4's three
perfect matchings, one colour each, on diagonal cells -- one copy on
L = {0,1,2,3} and one on R = {4,5,6,7}.  This script asks whether that is a
property of the whole Gamma-forced stratum (75 classes) or an accident of the
one member.

WHAT AN EMBEDDED GHZ_4 IS, EXACTLY.  Let S(T) be the graph of SINGLE-CELL
blocks of T.  A component of S(T) on four sites {a,b,c,d} is an embedded
GHZ_4^3 copy iff
  (i)  it is a complete K_4 (all six edges are single cells), and
  (ii) every one of the six cells is DIAGONAL, cell (r,r), and
  (iii) the three colour classes are exactly the three perfect matchings of
       that K_4 (colour r on both edges of one perfect matching).
(ii)+(iii) are not a stylistic choice: for the constant word r^4 to be
supported inside the component, some perfect matching must have BOTH edges
active at (r,r); K_4 has exactly three perfect matchings, so covering all
three colours forces all six edges diagonal, one colour per matching.  So on a
K_4 component the GHZ_4^3 pattern is the ONLY exact N=4 source made of single
cells -- (i) is the real hypothesis, (ii)+(iii) then follow or fail.

CONTROLS
  E1  the C_8 member must come out as a DOUBLE embedding (two K_4 copies) --
      the finding this generalises.
  E2  the W26/W30 slack-0 m=28 Route-A template must come out with its singles
      forming the CONNECTED cubic graph Q_3 = K_{4,4} minus a perfect
      matching, hence ZERO K_4 components and NO embedding.  If the test
      cannot tell the stratum member from the Route-A template it is useless.
  E3  MUTATION: moving one single cell off the diagonal must break the
      embedding verdict for that component.
  E4  every single graph's cubic iso-class is identified by the same
      invariant used in w31_slack.py, and the K_4 u K_4 class must be the one
      with |Aut| = 1152 (35 labelled) -- cross-checked against that run.
"""
from __future__ import annotations

import json
import os
import sys
from itertools import combinations, permutations, product

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
CENSUS = os.path.join(REPO, "computations",
                      "unaudited-forcing-w19-2026-08-15", "census")
sys.path.insert(0, os.path.join(REPO, "computations",
                                "unaudited-blockers-w26-2026-08-16"))

N, FULL = 8, 511
EDGES = tuple(combinations(range(N), 2))
EIDX = {e: i for i, e in enumerate(EDGES)}


def cells_of(mask):
    return [(c // 3, c % 3) for c in range(9) if (mask >> c) & 1]


def singles_of(T):
    return {EDGES[i]: cells_of(t)[0] for i, t in enumerate(T)
            if t and bin(t).count("1") == 1}


def components(edges):
    adj = {}
    for u, v in edges:
        adj.setdefault(u, set()).add(v)
        adj.setdefault(v, set()).add(u)
    seen, comps = set(), []
    for s in adj:
        if s in seen:
            continue
        st, cur = [s], set()
        while st:
            a = st.pop()
            if a in cur:
                continue
            cur.add(a)
            st.extend(adj[a] - cur)
        seen |= cur
        comps.append(sorted(cur))
    return comps


def ghz_copy(sing, comp):
    """is the component on `comp` an embedded GHZ_4^3 copy?  returns
    (verdict, detail)."""
    if len(comp) != 4:
        return False, "component has %d sites" % len(comp)
    need = [tuple(sorted(p)) for p in combinations(comp, 2)]
    if not all(e in sing for e in need):
        return False, "not a complete K_4 of singles"
    cells = {e: sing[e] for e in need}
    if not all(i == j for (i, j) in cells.values()):
        return False, "a cell is off-diagonal"
    a, b, c, d = comp
    pms = (((a, b), (c, d)), ((a, c), (b, d)), ((a, d), (b, c)))
    colour_of_pm = []
    for p in pms:
        cs = {cells[tuple(sorted(e))][0] for e in p}
        if len(cs) != 1:
            return False, "a perfect matching is not monochromatic"
        colour_of_pm.append(cs.pop())
    if sorted(colour_of_pm) != [0, 1, 2]:
        return False, "colour classes are not the three perfect matchings"
    return True, {"sites": comp,
                  "colour_per_matching": {str(list(p)): col for p, col
                                          in zip(pms, colour_of_pm)}}


def invariant(edges):
    es = [tuple(sorted(e)) for e in edges]
    S = set(es)
    tri = sum(1 for x, y, z in combinations(range(N), 3)
              if (x, y) in S and (x, z) in S and (y, z) in S)
    c4 = 0
    for quad in combinations(range(N), 4):
        for pr in (((0, 1), (1, 2), (2, 3), (3, 0)),
                   ((0, 1), (1, 3), (3, 2), (2, 0)),
                   ((0, 2), (2, 1), (1, 3), (3, 0))):
            if all(tuple(sorted((quad[i], quad[j]))) in S for i, j in pr):
                c4 += 1
    mk = [0] * 5
    for k in range(1, 5):
        for sub in combinations(es, k):
            vs, ok = set(), True
            for u, v in sub:
                if u in vs or v in vs:
                    ok = False
                    break
                vs.add(u)
                vs.add(v)
            if ok:
                mk[k] += 1
    return (tri, c4, tuple(mk))


def analyse(T):
    sing = singles_of(T)
    servers = [EDGES[i] for i, t in enumerate(T) if t and t != FULL]
    deg = [0] * N
    for u, v in sing:
        deg[u] += 1
        deg[v] += 1
    cubic = (len(sing) == 12 and all(d == 3 for d in deg))
    comps = components(list(sing))
    copies, why = [], []
    for cp in comps:
        ok, det = ghz_copy(sing, cp)
        (copies if ok else why).append(det)
    return dict(n_servers=len(servers), n_singles=len(sing),
                single_degrees=deg, singles_cubic=cubic,
                n_components=len(comps),
                component_sizes=sorted(len(c) for c in comps),
                cubic_invariant=str(invariant(list(sing))) if cubic else None,
                n_ghz_copies=len(copies), ghz_copies=copies,
                non_embedding_reasons=why,
                embedding=("double" if len(copies) == 2 else
                           "single" if len(copies) == 1 else "none"))


def main():
    OUT = {"_header": "UNAUDITED W31 GHZ_4 embedding census over the "
                      "Gamma-forced stratum. Exact pattern arithmetic only. "
                      "Nothing here is a proved claim of the repository.",
           "_pinned_head": open(os.path.join(HERE,
                                             "PINNED_HEAD.txt")).read().strip()}

    kill = json.load(open(os.path.join(CENSUS, "results_kill.json")))
    dec = json.load(open(os.path.join(CENSUS, "results_decide.json")))
    inv = {r["gamma_mask"]: r for r in kill["reps_inventory"]}

    per, tally = {}, {}
    byF = {}
    for gm_s, T in dec["reps"].items():
        gm = int(gm_s)
        rec = inv[gm]
        if rec["pms"] > 2:
            continue
        a = analyse(T)
        a.update(gamma_mask=gm, n_gamma=rec["n_edges"], n_F=rec["pms"])
        per[str(gm)] = a
        tally[a["embedding"]] = tally.get(a["embedding"], 0) + 1
        k = (rec["pms"], a["embedding"])
        byF[str(k)] = byF.get(str(k), 0) + 1
    OUT["per_class"] = per
    OUT["embedding_tally"] = tally
    OUT["embedding_by_F"] = byF
    OUT["n_stratum_classes"] = len(per)
    print("[stratum] classes examined:", len(per))
    print("[tally] embedding ->", tally)
    print("[by |F|] (|F|, embedding) ->", byF)

    cub = {}
    for a in per.values():
        cub[str(a["cubic_invariant"])] = cub.get(str(a["cubic_invariant"]),
                                                 0) + 1
    OUT["single_graph_cubic_classes"] = cub
    print("[single graph] cubic invariant ->", cub)

    # E1 : the C_8 member
    c8 = [gm for gm in per if per[gm]["n_gamma"] == 8][0]
    OUT["E1_c8_embedding"] = per[c8]["embedding"]
    OUT["E1_ok"] = (per[c8]["embedding"] == "double")
    print("[E1] C_8 member embedding:", per[c8]["embedding"], "->",
          OUT["E1_ok"])

    # E2 : the Route-A slack-0 template must NOT embed
    import w26_core as C26
    a26 = analyse(list(C26.TEMPLATES[28]))
    OUT["E2_routeA_m28"] = a26
    OUT["E2_ok"] = (a26["n_ghz_copies"] == 0 and a26["singles_cubic"])
    print("[E2] Route-A m=28 template: singles cubic=%s components=%s "
          "ghz_copies=%d -> %s" % (a26["singles_cubic"],
                                   a26["component_sizes"],
                                   a26["n_ghz_copies"], OUT["E2_ok"]))

    # E3 : mutation
    Tm = list(dec["reps"][c8])
    e0 = sorted(singles_of(Tm))[0]
    Tm[EIDX[e0]] = 1 << 1                       # move the cell off-diagonal
    am = analyse(Tm)
    OUT["E3_mutation_breaks_embedding"] = (am["n_ghz_copies"]
                                           < per[c8]["n_ghz_copies"])
    print("[E3] mutation control fires:",
          OUT["E3_mutation_breaks_embedding"])

    # E4 : cross-check the K_4 u K_4 invariant against w31_slack.py
    sl = os.path.join(HERE, "results_slack.json")
    if os.path.exists(sl):
        s = json.load(open(sl))
        k44 = [c for c in s["D1_classes"] if c["aut"] == 1152]
        OUT["E4_K4uK4_invariant_from_slack_run"] = (k44[0]["invariant"]
                                                    if k44 else None)
        OUT["E4_ok"] = any(k["invariant"] in cub for k in k44)
        print("[E4] K_4 u K_4 invariant", OUT["E4_K4uK4_invariant_from_slack_run"],
              "present among stratum single graphs:", OUT["E4_ok"])

    universal = (tally.get("double", 0) == len(per))
    OUT["LEMMA_W31_2_universal_double_embedding"] = universal
    OUT["non_embedding_classes"] = [gm for gm, a in per.items()
                                    if a["embedding"] != "double"]
    print()
    print("[LEMMA W31-2] every Gamma-forced stratum class embeds TWO GHZ_4^3 "
          "copies:", universal)
    if not universal:
        print("   classes that do NOT double-embed:",
              len(OUT["non_embedding_classes"]))

    with open(os.path.join(HERE, "results_ghz_embed.json"), "w") as fh:
        json.dump(OUT, fh, indent=1, sort_keys=True)
    declared = ["E1_ok", "E2_ok", "E3_mutation_breaks_embedding",
                "embedding_tally", "per_class"]
    missing = [d for d in declared if d not in OUT]
    assert not missing, "CONTROL NEVER RAN: %s" % missing
    print("control manifest OK:", declared)


if __name__ == "__main__":
    main()
