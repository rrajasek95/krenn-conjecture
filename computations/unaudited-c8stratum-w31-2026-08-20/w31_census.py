#!/usr/bin/env python3
r"""W31 -- the C_8 / empty-clean stratum: exact census + frame-degeneracy.

UNAUDITED PROBE.  Nothing here is a proved claim of the repository.
Pinned HEAD: see PINNED_HEAD.txt.  EXACT INTEGER ARITHMETIC ONLY (no floats,
no field arithmetic, no Singular).  Single process, seconds-scale.

MODEL (re-typed from the definition; cross-checked against the stored W19
census and the stored W20 C_8 member -- see CONTROLS below).
  N = 8 sites, alphabet {0,1,2}, one 3x3 block A_uv per edge uv of K_8.
  H_w(A) = sum over the 105 perfect matchings M of K_8 of
           prod_{(u,v) in M} A_uv[w_u][w_v].
  Template T: 9-bit mask per edge, bit 3i+j set <=> cell (i,j) occupied.
  m(T)      = #edges with a nonzero mask ("support").
  Sigma(T)  = #occupied cells.
  Gamma(T)  = the graph of FULL (nine-cell) blocks.
  F(Gamma)  = perfect matchings of K_8 lying inside Gamma; each is supported
              at EVERY word, so F(Gamma) is contained in every fibre.
  k(w)      = fibre(T,w) - |F(Gamma)| = #supported matchings outside Gamma.
  effectively clean: k(w) = 0.
  (R): (SC)-admissible + three constant fibres nonempty + Gamma spanning
       2-connected + every mixed word has fibre >= 3.

WHAT THIS SCRIPT ESTABLISHES (all exact, all reproducible in seconds):
  A. The C_8 member's audit, recomputed from the stored mask list.
  B. |F(Gamma)| recomputed independently for all 794 stored census classes
     and cross-tabulated against the stored 'pms' field (a control on the
     stored census) and against |Gamma|.
  C. The stratum split |F| in {0,2}: NO admissible class has |F| = 1
     (Kotzig: a connected graph with a unique perfect matching has a bridge,
     so a spanning 2-connected Gamma cannot have exactly one).
  D. W18-E's budget bound |Gamma| <= m - 12 recomputed on every stored rep.
  E. FRAME DEGENERACY: for every stratum class and EVERY bipartition of the
     eight sites into two 4-sets, whether Gamma restricted to each half
     contains a perfect matching (2 disjoint edges).  This is exactly the
     nondegeneracy the W26/W30 slice machinery needs (hafL, hafR are the
     hafnians of Gamma's cells inside the two halves; the slice data is
     undefined -- returns None -- when the scale vanishes).
  F. The L-free word count of the C_8 member (W20's reduction input).

CONTROLS
  C1  recomputed |F| == stored 'pms' for all 794 classes (0 mismatches
      required).
  C2  recomputed no-clean status == stored 'n_clean' == 0 for all 794.
  C3  the C_8 member passes in_R and reproduces W19's headline numbers
      (m=28, Sigma=148, |Gamma|=8, |F|=2, min mixed fibre 6, 0 clean words).
  C4  MUTATION: flipping one cell off the C_8 member's Gamma must change the
      audit (guards against a vacuous audit).
  C5  positive control on E: the m=28 W26/W30 template (Gamma = K_4(L) u
      K_4(R) u sigma) must report a NONDEGENERATE bipartition -- if the
      frame test cannot see the frame it is testing, it is worthless.
"""
from __future__ import annotations

import json
import os
import sys
from itertools import combinations, product

sys.dont_write_bytecode = True

N = 8
Q = 3
FULL = 511
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
CENSUS = os.path.join(REPO, "computations",
                      "unaudited-forcing-w19-2026-08-15", "census")

EDGES = tuple(combinations(range(N), 2))
EIDX = {e: i for i, e in enumerate(EDGES)}


def _pms(vs):
    if not vs:
        return [()]
    a, rest = vs[0], vs[1:]
    out = []
    for i, b in enumerate(rest):
        for mm in _pms(rest[:i] + rest[i + 1:]):
            out.append(((a, b),) + mm)
    return out


PMS = tuple(tuple(sorted(m)) for m in _pms(tuple(range(N))))
assert len(PMS) == 105
PM_E = tuple(tuple(EIDX[e] for e in m) for m in PMS)
WORDS = tuple(product(range(Q), repeat=N))
CONSTS = tuple((c,) * N for c in range(Q))
MIXED = tuple(w for w in WORDS if len(set(w)) > 1)
assert len(WORDS) == 6561 and len(MIXED) == 6558

# the C_8 member, verbatim from
# computations/unaudited-lasttwo-w20-2026-08-15/w20_core.py:370
C8_MEMBER = [1, 16, 256, 511, 511, 503, 447, 256, 16, 510, 495, 511, 511, 1,
             383, 511, 510, 511, 511, 255, 511, 383, 1, 16, 256, 256, 16, 1]

# the m=28 Route-A (W8 / W26 / W30) template geometry, from
# computations/unaudited-blockers-w26-2026-08-16/w26_core.py:15-26
W26_L = (0, 1, 2, 3)
W26_SIG = {0: 7, 1: 4, 2: 5, 3: 6}


def cell_index(ei, w):
    u, v = EDGES[ei]
    return 3 * w[u] + w[v]


def support(T, w):
    return [mi for mi, es in enumerate(PM_E)
            if all((T[e] >> cell_index(e, w)) & 1 for e in es)]


def gamma_edges(T):
    return [EDGES[i] for i, t in enumerate(T) if t == FULL]


def pms_inside(edgeset):
    S = set(tuple(sorted(e)) for e in edgeset)
    return [mi for mi, m in enumerate(PMS) if all(e in S for e in m)]


def spanning_2connected(edges, n=N):
    vs = set()
    for u, v in edges:
        vs.add(u)
        vs.add(v)
    if vs != set(range(n)):
        return False
    adj = {v: set() for v in range(n)}
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)

    def connected(skip):
        keep = [v for v in range(n) if v != skip]
        st, seen = [keep[0]], {keep[0]}
        while st:
            a = st.pop()
            for b in adj[a]:
                if b != skip and b not in seen:
                    seen.add(b)
                    st.append(b)
        return len(seen) == len(keep)

    return connected(-1) and all(connected(s) for s in range(n))


def cells_of(mask):
    return [(c // 3, c % 3) for c in range(9) if (mask >> c) & 1]


def forced_far_colour(mask, p_is_first):
    if not mask:
        return None
    seen = {(j if p_is_first else i) for i, j in cells_of(mask)}
    return seen.pop() if len(seen) == 1 else None


def sc_ok(T):
    for p in range(N):
        need = set(range(Q))
        for ei, (u, v) in enumerate(EDGES):
            if p != u and p != v:
                continue
            r = forced_far_colour(T[ei], p_is_first=(u == p))
            if r is not None:
                need.discard(r)
        if need:
            return False
    return True


def in_R(T):
    if not sc_ok(T):
        return False
    if not all(support(T, w) for w in CONSTS):
        return False
    if not spanning_2connected(gamma_edges(T)):
        return False
    return all(len(support(T, w)) >= 3 for w in MIXED)


def audit(T):
    ge = gamma_edges(T)
    F = pms_inside(ge)
    fibs = {w: len(support(T, w)) for w in WORDS}
    mixfib = [fibs[w] for w in MIXED]
    return dict(m=sum(1 for t in T if t),
                Sigma=sum(bin(t).count("1") for t in T),
                n_gamma=len(ge), gamma=[list(e) for e in ge], n_F=len(F),
                gamma_spanning_2conn=spanning_2connected(ge),
                min_mixed_fibre=min(mixfib), max_mixed_fibre=max(mixfib),
                min_k_over_mixed=min(mixfib) - len(F),
                n_eff_clean=sum(1 for f in mixfib if f == len(F)),
                sc=sc_ok(T), in_R=in_R(T))


def half_has_pm(gset, half):
    """does Gamma restricted to `half` (4 sites) contain 2 disjoint edges?"""
    a, b, c, d = sorted(half)
    for (p, q), (r, s) in (((a, b), (c, d)), ((a, c), (b, d)),
                           ((a, d), (b, c))):
        if (p, q) in gset and (r, s) in gset:
            return True
    return False


def frame_bipartitions(gedges):
    """all 35 unordered 4|4 splits; report which give hafL, hafR both != 0."""
    gset = set(tuple(sorted(e)) for e in gedges)
    good, tested = [], 0
    for half in combinations(range(1, N), 3):
        Lh = (0,) + half
        Rh = tuple(v for v in range(N) if v not in Lh)
        tested += 1
        if half_has_pm(gset, Lh) and half_has_pm(gset, Rh):
            good.append([list(Lh), list(Rh)])
    return dict(n_splits=tested, n_nondegenerate=len(good),
                nondegenerate=good)


def w26_m28_template():
    """Gamma = K_4(L) u K_4(R) u sigma; the 12 non-sigma cross edges single."""
    T = [0] * len(EDGES)
    Ls, Rs = set(W26_L), set(range(4, 8))
    sig = {tuple(sorted((a, b))) for a, b in W26_SIG.items()}
    for ei, (u, v) in enumerate(EDGES):
        if (u in Ls and v in Ls) or (u in Rs and v in Rs) or (u, v) in sig:
            T[ei] = FULL
        else:
            T[ei] = 1                       # one cell -- a "single"
    return T


def lfree_words(T):
    """W20's L-free predicate on the C_8 member: L-words activating no
    single-cell block inside L = {0,1,2,3}."""
    sing = {}
    for ei, (u, v) in enumerate(EDGES):
        if u < 4 and v < 4 and bin(T[ei]).count("1") == 1:
            sing[(u, v)] = cells_of(T[ei])[0]
    out = []
    for x in product(range(Q), repeat=4):
        if all(not (x[u] == i and x[v] == j) for (u, v), (i, j) in
               sing.items()):
            out.append(list(x))
    return sing, out


def main():
    OUT = {"_header": "UNAUDITED W31 probe -- the C_8/empty-clean stratum "
                      "census. Exact integer arithmetic only. Nothing here "
                      "is a proved claim of the repository.",
           "_pinned_head": open(os.path.join(HERE, "PINNED_HEAD.txt")).read()
                           .strip()}

    # ---------------------------------------------------------------- A
    print("[A] C_8 member audit")
    a8 = audit(C8_MEMBER)
    OUT["A_c8_member"] = a8
    for k in ("m", "Sigma", "n_gamma", "n_F", "min_mixed_fibre",
              "min_k_over_mixed", "n_eff_clean", "sc", "in_R"):
        print("   ", k, "=", a8[k])
    OUT["C3_matches_W19_headline"] = (
        a8["m"] == 28 and a8["Sigma"] == 148 and a8["n_gamma"] == 8
        and a8["n_F"] == 2 and a8["min_mixed_fibre"] == 6
        and a8["min_k_over_mixed"] == 4 and a8["n_eff_clean"] == 0
        and a8["in_R"] and a8["gamma_spanning_2conn"])
    print("    C3 (reproduces W19 headline):", OUT["C3_matches_W19_headline"])

    # C4 mutation: drop one cell of a Gamma block -> Gamma shrinks
    mut = list(C8_MEMBER)
    gi = [i for i, t in enumerate(mut) if t == FULL][0]
    mut[gi] = FULL ^ 1
    am = audit(mut)
    OUT["C4_mutation_changes_audit"] = (am["n_gamma"] != a8["n_gamma"]
                                        or am["n_F"] != a8["n_F"])
    print("    C4 (mutation fires):", OUT["C4_mutation_changes_audit"])

    # ---------------------------------------------------------------- F
    sing, lf = lfree_words(C8_MEMBER)
    OUT["F_c8_L_singles"] = {str(k): list(v) for k, v in sing.items()}
    OUT["F_c8_n_Lfree"] = len(lf)
    OUT["F_matches_W20_30"] = (len(lf) == 30)
    print("[F] L-free words:", len(lf), "(W20 reported 30):",
          OUT["F_matches_W20_30"])

    # ---------------------------------------------------------------- B,C,D
    print("[B] recomputing |F| for the 794 stored census classes")
    kill = json.load(open(os.path.join(CENSUS, "results_kill.json")))
    dec = json.load(open(os.path.join(CENSUS, "results_decide.json")))
    inv = {r["gamma_mask"]: r for r in kill["reps_inventory"]}
    reps = dec["reps"]

    mism_F = mism_clean = 0
    byGF, stratum, bound_viol = {}, [], 0
    frame_tbl = {}
    for gm_s, T in reps.items():
        gm = int(gm_s)
        rec = inv[gm]
        ge = [EDGES[i] for i in range(len(EDGES)) if (gm >> i) & 1]
        nF = len(pms_inside(ge))
        if nF != rec["pms"]:
            mism_F += 1
        F = pms_inside(gamma_edges(T))
        nclean = sum(1 for w in MIXED if len(support(T, w)) == len(F))
        if (nclean == 0) != (rec["n_clean"] == 0):
            mism_clean += 1
        m = sum(1 for t in T if t)
        if len(ge) > m - 12:
            bound_viol += 1
        key = "%d,%d" % (len(ge), nF)
        byGF[key] = byGF.get(key, 0) + 1
        if nF <= 2:
            fr = frame_bipartitions(ge)
            frame_tbl[str(gm)] = dict(n_gamma=len(ge), n_F=nF, m=m,
                                      Sigma=sum(bin(t).count("1") for t in T),
                                      n_clean=nclean,
                                      n_nondeg=fr["n_nondegenerate"])
            stratum.append((gm, len(ge), nF, m, nclean,
                            fr["n_nondegenerate"]))

    OUT["C1_F_mismatches_vs_stored"] = mism_F
    OUT["C2_clean_mismatches_vs_stored"] = mism_clean
    OUT["B_classes_by_gammaEdges_F"] = byGF
    OUT["C_F_equals_one_count"] = sum(v for k, v in byGF.items()
                                      if k.split(",")[1] == "1")
    OUT["D_W18E_bound_violations"] = bound_viol
    print("    C1 |F| mismatches:", mism_F, " C2 clean mismatches:",
          mism_clean)
    print("    classes with |F| = 1:", OUT["C_F_equals_one_count"],
          "(Kotzig predicts 0)")
    print("    |Gamma| <= m - 12 violations:", bound_viol)

    # ---------------------------------------------------------------- E
    print("[E] stratum (|F| <= 2) -- size, profile, frame degeneracy")
    OUT["E_stratum_size"] = len(stratum)
    prof = {}
    for gm, ng, nF, m, nc, nnd in stratum:
        k = "|Gamma|=%d,|F|=%d" % (ng, nF)
        prof.setdefault(k, {"classes": 0, "all_m28": True,
                            "all_no_clean": True, "max_nondeg_splits": 0})
        prof[k]["classes"] += 1
        prof[k]["all_m28"] &= (m == 28)
        prof[k]["all_no_clean"] &= (nc == 0)
        prof[k]["max_nondeg_splits"] = max(prof[k]["max_nondeg_splits"], nnd)
    OUT["E_stratum_profile"] = prof
    OUT["E_stratum_frame_detail"] = frame_tbl
    OUT["E_stratum_classes_with_a_nondegenerate_split"] = sum(
        1 for *_, nnd in stratum if nnd > 0)
    for k in sorted(prof):
        print("   ", k, prof[k])
    print("    stratum classes admitting ANY nondegenerate 4|4 split:",
          OUT["E_stratum_classes_with_a_nondegenerate_split"], "of",
          len(stratum))

    # C5 positive control: the W26/W30 m=28 frame must be seen as good
    w26T = w26_m28_template()
    w26a = audit(w26T)
    fr26 = frame_bipartitions(gamma_edges(w26T))
    OUT["C5_positive_control"] = dict(
        m=w26a["m"], Sigma=w26a["Sigma"], n_gamma=w26a["n_gamma"],
        n_F=w26a["n_F"], n_eff_clean=w26a["n_eff_clean"], sc=w26a["sc"],
        in_R=w26a["in_R"], n_nondegenerate_splits=fr26["n_nondegenerate"],
        LR_split_is_nondegenerate=([list(W26_L), [4, 5, 6, 7]]
                                   in fr26["nondegenerate"]))
    print("[C5] W26/W30 m=28 frame:", OUT["C5_positive_control"])

    # the C_8 member itself, explicitly
    fr8 = frame_bipartitions(gamma_edges(C8_MEMBER))
    OUT["E_c8_member_frame"] = fr8
    print("[E] C_8 member: nondegenerate 4|4 splits =",
          fr8["n_nondegenerate"], "of", fr8["n_splits"])

    with open(os.path.join(HERE, "results_census.json"), "w") as fh:
        json.dump(OUT, fh, indent=1, sort_keys=True)
    print("wrote results_census.json")

    # manifest assertion (ledger 21): every declared control must have run
    declared = ["C1_F_mismatches_vs_stored", "C2_clean_mismatches_vs_stored",
                "C3_matches_W19_headline", "C4_mutation_changes_audit",
                "C5_positive_control", "F_matches_W20_30"]
    missing = [c for c in declared if c not in OUT]
    assert not missing, "CONTROL NEVER RAN: %s" % missing
    print("control manifest OK:", declared)


if __name__ == "__main__":
    main()
