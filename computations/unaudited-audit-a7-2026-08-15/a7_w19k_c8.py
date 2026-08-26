#!/usr/bin/env python3
"""A7 -- TARGET 2: THEOREM W19-K and the explicit C_8 member of (R).

W19-K (as stated): every matching inside Gamma is supported at every word, so
k(w) = fibre(w) - |F(Gamma)|; if |F(Gamma)| <= 2 then, since an (R) member has
every mixed fibre >= 3, k(w) >= 1 on every mixed word, i.e. the effectively
clean layer is EMPTY.

HAND PROOF (mine).  A FULL block has every cell occupied, so a perfect
matching all of whose edges are Gamma-edges is in the fibre of EVERY word;
hence F(Gamma) is contained in fibre(w) for all w and k(w) := |fibre(w)| -
|F(Gamma)| >= 0 counts exactly the non-Gamma-only matchings.  (R) demands
|fibre(w)| >= 3 on mixed words, so |F(Gamma)| <= 2 gives k(w) >= 3 - 2 = 1
on every mixed word: no mixed word is effectively clean.  QED -- correct and
two lines; the content is entirely in the (R) axiom "every mixed fibre >= 3".

Checks here:
  (K1) k(w) = |fibre(w)| - |F(Gamma)| verified on ALL 6561 words for every
       template in play (m=24..28, C_8 witness, plus mutated templates);
  (K2) the C_8 witness re-audited from raw template data: in_R, m, Sigma,
       |Gamma|, Gamma = Hamilton cycle, |F(Gamma)|, min mixed fibre, number of
       effectively-clean words, min k and its multiplicity;
  (K3) mutation controls.
"""
from __future__ import annotations
import os, sys, json, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a7_core import (W8_IMMUNE, EDGES, EIDX, WORDS, MIXED, CONSTS, FULL,
                     fibre, F_gamma, gamma_edges, k_of, cell_index)

HERE = os.path.dirname(os.path.abspath(__file__))

C8_WITNESS = [1, 16, 256, 511, 511, 503, 447, 256, 16, 510, 495, 511, 511, 1,
              383, 511, 510, 511, 511, 255, 511, 383, 1, 16, 256, 256, 16, 1]


# ------------------------------------------------------- (SC) / (R) ------
def cells_of(mask):
    return [(c // 3, c % 3) for c in range(9) if (mask >> c) & 1]


def far_thin_colour(mask, at_second):
    if not mask:
        return None
    S = {(j if at_second else i) for i, j in cells_of(mask)}
    return S.pop() if len(S) == 1 else None


def sc_servers(T):
    out = {}
    for p in range(8):
        for r in range(3):
            srv = []
            for ei, (u, v) in enumerate(EDGES):
                if p not in (u, v):
                    continue
                if far_thin_colour(T[ei], at_second=(u == p)) == r:
                    srv.append(ei)
            out[(p, r)] = srv
    return out


def sc_ok(T):
    return all(v for v in sc_servers(T).values())


def spanning_2conn(edges, n=8):
    vs = {x for e in edges for x in e}
    if vs != set(range(n)):
        return False

    def conn(skip):
        adj = {v: [] for v in range(n) if v != skip}
        for u, v in edges:
            if u != skip and v != skip:
                adj[u].append(v)
                adj[v].append(u)
        if not adj:
            return False
        st = [next(iter(adj))]
        seen = set(st)
        while st:
            a = st.pop()
            for b in adj[a]:
                if b not in seen:
                    seen.add(b)
                    st.append(b)
        return len(seen) == len(adj)
    return conn(-1) and all(conn(s) for s in range(n))


def in_R(T):
    reasons = {}
    reasons["sc_ok"] = sc_ok(T)
    reasons["constants_nonempty"] = all(fibre(T, w) for w in CONSTS)
    ge = gamma_edges(T)
    reasons["gamma_spanning_2conn"] = spanning_2conn(ge)
    mn = min(len(fibre(T, w)) for w in MIXED)
    reasons["min_mixed_fibre"] = mn
    reasons["min_mixed_fibre_ge_3"] = mn >= 3
    reasons["verdict"] = all(reasons[k] for k in
                             ("sc_ok", "constants_nonempty",
                              "gamma_spanning_2conn", "min_mixed_fibre_ge_3"))
    return reasons


# -------------------------------------------------------------- checks ----
def K1(T):
    Fg = F_gamma(T)
    nF = len(Fg)
    bad = 0
    for w in WORDS:
        if k_of(T, w, Fg) != len(fibre(T, w)) - nF:
            bad += 1
    # also: F(Gamma) really is inside every fibre
    inside = all(set(Fg) <= set(fibre(T, w)) for w in WORDS)
    return dict(nF=nF, identity_mismatches=bad, F_inside_every_fibre=inside)


def cycle_of(edges):
    adj = {v: [] for v in range(8)}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    if any(len(a) != 2 for a in adj.values()):
        return None
    order = [0, adj[0][0]]
    while len(order) < 8:
        a, b = order[-2], order[-1]
        nxt = adj[b][0] if adj[b][0] != a else adj[b][1]
        order.append(nxt)
    return order if adj[order[-1]][0] == 0 or adj[order[-1]][1] == 0 else None


def audit_template(T, label):
    Fg = F_gamma(T)
    kk = {}
    for w in MIXED:
        v = k_of(T, w, Fg)
        kk.setdefault(v, []).append(w)
    mn = min(kk)
    r = dict(label=label,
             m=sum(1 for t in T if t),
             sigma=sum(bin(t).count("1") for t in T),
             n_gamma=len(gamma_edges(T)),
             gamma=[list(e) for e in gamma_edges(T)],
             hamilton_cycle=cycle_of(gamma_edges(T)),
             nF=len(Fg),
             min_mixed_fibre=min(len(fibre(T, w)) for w in MIXED),
             const_fibres=[len(fibre(T, w)) for w in CONSTS],
             n_eff_clean=len(kk.get(0, [])),
             min_k=mn, n_words_at_min_k=len(kk[mn]),
             words_at_min_k=["".join(map(str, w)) for w in kk[mn][:5]],
             k_histogram={str(a): len(b) for a, b in sorted(kk.items())},
             block_classes=None)
    cls = {"zero": 0, "single": 0, "thin": 0, "fat": 0, "full": 0}
    for t in T:
        if t == 0:
            cls["zero"] += 1
        elif t == FULL:
            cls["full"] += 1
        elif bin(t).count("1") == 1:
            cls["single"] += 1
        else:
            cs = cells_of(t)
            rows = {i for i, _ in cs}
            cols = {j for _, j in cs}
            cls["thin" if (len(rows) == 1 or len(cols) == 1) else "fat"] += 1
    r["block_classes"] = cls
    r["in_R"] = in_R(T)
    return r


def main():
    out = {}
    # (K1) on every template in play
    k1 = {}
    for m in range(24, 29):
        k1["m%d" % m] = K1(W8_IMMUNE[m])
    k1["C8"] = K1(C8_WITNESS)
    mutT = list(W8_IMMUNE[26])
    mutT[0] = 510                      # break a FULL block -> |F| must drop
    k1["mutated_m26"] = K1(mutT)
    out["K1"] = k1
    for k, v in k1.items():
        print("K1 %-12s %s" % (k, v))
    # (K2) the C_8 member
    r = audit_template(C8_WITNESS, "C_8 witness (W19 census stratum i)")
    out["K2_C8"] = r
    print("\nK2 C_8 witness")
    for k in ("m", "sigma", "n_gamma", "hamilton_cycle", "nF",
              "min_mixed_fibre", "const_fibres", "n_eff_clean", "min_k",
              "n_words_at_min_k", "words_at_min_k", "block_classes"):
        print("   %-20s %s" % (k, r[k]))
    print("   in_R: %s" % r["in_R"])
    print("   k histogram: %s" % r["k_histogram"])
    # (K3) mutation controls
    ctl = {}
    T2 = list(C8_WITNESS)
    T2[3] = 510                       # 8 cells instead of 9: Gamma loses an edge
    ctl["C8_break_a_full_block"] = audit_template(T2, "C8 mutated")
    print("\nK3 mutation: breaking one FULL block of the C_8 witness ->",
          "n_gamma=%d nF=%d in_R=%s min_mixed=%d"
          % (ctl["C8_break_a_full_block"]["n_gamma"],
             ctl["C8_break_a_full_block"]["nF"],
             ctl["C8_break_a_full_block"]["in_R"]["verdict"],
             ctl["C8_break_a_full_block"]["min_mixed_fibre"]))
    # sc_ok detector control: zero out a single-cell block -> (SC) must fail
    T3 = list(C8_WITNESS)
    T3[0] = 0
    ctl["C8_zero_a_single"] = dict(sc_ok=sc_ok(T3),
                                   fired=(sc_ok(C8_WITNESS) and not sc_ok(T3)))
    print("K3 mutation: zeroing block (0,1) -> sc_ok=%s (fired=%s)"
          % (ctl["C8_zero_a_single"]["sc_ok"],
             ctl["C8_zero_a_single"]["fired"]))
    out["K3_controls"] = ctl
    # W19-K's consequence, stated exactly
    out["W19K_consequence"] = dict(
        statement="|F(Gamma)| <= 2 and (R) => every mixed word has k >= 1 "
                  "=> the effectively-clean layer is empty",
        C8_nF=len(F_gamma(C8_WITNESS)),
        C8_min_mixed_fibre=r["min_mixed_fibre"],
        C8_n_eff_clean=r["n_eff_clean"],
        holds=(len(F_gamma(C8_WITNESS)) <= 2 and r["n_eff_clean"] == 0))
    json.dump(out, open(os.path.join(HERE, "results_w19k_c8.json"), "w"),
              indent=1, default=str)


if __name__ == "__main__":
    main()
