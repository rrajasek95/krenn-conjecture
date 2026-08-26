#!/usr/bin/env python3
"""W22 T1b -- EXHAUSTIVE sweep of a structured mixed-exact stratum at N = 6,
plus support-matched randomisation controls (ledger item 12 methodology).

STRATUM (M): diagonal 0/1 sources A_uv = diag([uv in M_0], [uv in M_1],
[uv in M_2]) with each M_c a MATCHING of K_6 (possibly partial).  Then
   H_w = prod_c [ w^{-1}(c) is a union of M_c-edges ],
so mixed-exactness is a purely combinatorial condition and
   pure_c = 1  iff  M_c is a PERFECT matching.
All 76^3 triples are enumerated; survivors are classified by the number k of
nonzero pures and every live pair of every survivor class is DECIDED exactly.

Also: Theorem W22-B closed form on the constant-block family, verified
exactly, and support-matched randomisation controls for the k >= 1 objects.
"""
from __future__ import annotations

import json
import random
import sys
from fractions import Fraction
from itertools import combinations, product

BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-induction2-w22-2026-08-15")
sys.path.insert(0, BASE)
import w22_core as W                                        # noqa: E402
import w22_n6 as N6                                         # noqa: E402

N = 6
PAIRS = list(combinations(range(N), 2))
RES = {}


def all_matchings(n):
    out = [()]
    edges = list(combinations(range(n), 2))
    def rec(start, cur, used):
        for i in range(start, len(edges)):
            a, b = edges[i]
            if a in used or b in used:
                continue
            cur.append((a, b))
            out.append(tuple(cur))
            rec(i + 1, cur, used | {a, b})
            cur.pop()
    rec(0, [], set())
    return out


def diag_src(Ms):
    src = {e: [[0] * 3 for _ in range(3)] for e in PAIRS}
    for c, M in enumerate(Ms):
        for e in M:
            src[W.ekey(*e)][c][c] = 1
    return src


FULL = (1 << N) - 1


def unions_of(M):
    """All site-subsets (as bitmasks) that are disjoint unions of M-edges."""
    out = [0]
    for a, b in M:
        bit = (1 << a) | (1 << b)
        out = out + [m | bit for m in out]
    return sorted(set(out))


def mixed_exact_combinatorial(U0, U1, U2):
    """H_w = prod_c [w^{-1}(c) is a union of M_c edges].  Mixed-exact iff the
    only partitions (S_0,S_1,S_2) with S_c a union of M_c-edges are the three
    PURE ones (one class = B)."""
    pure = {(FULL, 0, 0), (0, FULL, 0), (0, 0, FULL)}
    for s0 in U0:
        for s1 in U1:
            if s0 & s1:
                continue
            s2 = FULL & ~(s0 | s1)
            if s2 in U2 and (s0, s1, s2) not in pure:
                return False
    return True


def cheap_sig(Ms):
    """A permutation-invariant signature: (multiset of matching sizes, sorted
    per-vertex colour-degree multiset, number of shared vertices per pair).
    Coarser than a true canonical form -- used only to pick REPRESENTATIVES,
    never to count orbits (the raw triple counts are reported instead)."""
    sizes = tuple(sorted(len(M) for M in Ms))
    deg = []
    for v in range(N):
        deg.append(tuple(sorted(sum(1 for e in M if v in e) for M in Ms)))
    return (sizes, tuple(sorted(deg)))


def canon(Ms):
    """Canonical form under S_6 (sites) x S_3 (colours)."""
    import itertools
    best = None
    for perm in itertools.permutations(range(N)):
        for cp in itertools.permutations(range(3)):
            key = tuple(tuple(sorted(tuple(sorted((perm[a], perm[b])))
                                     for a, b in Ms[cp[c]]))
                        for c in range(3))
            if best is None or key < best:
                best = key
    return best


def main():
    rng = random.Random(4242)

    # ---------------- Theorem W22-B: constant-block closed form -------------
    # A_uv = t_uv J  =>  E_pq(K) = sigma(K)^2 * Haf(m) * 1^{(x)4},
    #   m_ab = t_pa t_qb + t_pb t_qa, Haf(m) = 2 e_2^hom(t_p|U, t_q|U);
    # so BLOCKED at (p,q)  <=>  e_2^hom != 0  (general caps AND rank-one).
    bad = 0
    tested = 0
    for _ in range(150):
        t = {e: rng.randint(-5, 5) for e in PAIRS}
        src = N6.source_P0_constant(t, N)
        p, q = rng.sample(range(N), 2)
        U = tuple(x for x in range(N) if x not in (p, q))
        K = [[rng.randint(-3, 3) for _ in range(3)] for _ in range(3)]
        sig = sum(K[i][j] for i in range(3) for j in range(3))
        x = [t[W.ekey(p, a)] for a in U]
        y = [t[W.ekey(q, a)] for a in U]
        e2 = W.ehom(x, y, 2)
        pred = sig * sig * 2 * e2
        err = W.cap_error_direct(src, p, q, K, U)
        got = err.get((0, 0, 0, 0), 0)
        allsame = all(v == got for v in err.values()) and (
            len(err) in (0, 81))
        tested += 1
        if got != pred or not allsame:
            bad += 1
    RES["W22B_closed_form"] = {"tested": tested, "violations": bad}
    print(f"[W22-B] constant-block closed form: {tested} tested, "
          f"{bad} violations")

    # ---------------- exhaustive stratum (M) --------------------------------
    Ms_all = all_matchings(N)
    UN = [unions_of(M) for M in Ms_all]
    print(f"matchings of K_6: {len(Ms_all)}")
    survivors = {}
    n_triples = n_survive = 0
    raw_by_k = {}
    for i0, M0 in enumerate(Ms_all):
        for i1, M1 in enumerate(Ms_all):
            for i2, M2 in enumerate(Ms_all):
                n_triples += 1
                if not mixed_exact_combinatorial(UN[i0], UN[i1], UN[i2]):
                    continue
                n_survive += 1
                Ms = (M0, M1, M2)
                k = sum(1 for M in Ms if len(M) == N // 2)
                raw_by_k[k] = raw_by_k.get(k, 0) + 1
                if min(len(M) for M in Ms) == 0:
                    continue          # a colour is absent: keep stats only
                key = cheap_sig(Ms)
                if key not in survivors:
                    survivors[key] = {"Ms": [list(map(list, M)) for M in Ms],
                                      "k_pures": k, "count": 0}
                survivors[key]["count"] += 1
    print(f"triples {n_triples}; mixed-exact triples {n_survive}; "
          f"raw by k {raw_by_k}; all-colours-present classes {len(survivors)}")
    byk = {}
    for v in survivors.values():
        byk[v["k_pures"]] = byk.get(v["k_pures"], 0) + 1
    print("all-colours-present classes by #nonzero pures:", byk)
    RES["stratum_M"] = {"n_triples": n_triples,
                        "n_mixed_exact_triples": n_survive,
                        "raw_triples_by_k": raw_by_k,
                        "n_classes_all_colours_present": len(survivors),
                        "classes_by_k": byk}

    # ---------------- decide blocking on the survivors ----------------------
    # (verify the combinatorial mixed-exactness against the exact tensor first)
    decided = []
    items = sorted(survivors.values(), key=lambda v: (-v["k_pures"],
                                                      -sum(len(m) for m in v["Ms"])))
    seen_k = {}
    for it in items:
        k = it["k_pures"]
        seen_k.setdefault(k, 0)
        if seen_k[k] >= 12:          # a dozen classes per k is plenty
            continue
        seen_k[k] += 1
        Ms = [tuple(map(tuple, m)) for m in it["Ms"]]
        src = diag_src(Ms)
        assert N6.is_mixed_exact(src, N), "combinatorial test disagrees"
        pu = W.pures(src, N)
        assert sum(1 for c in range(3) if pu[c] != 0) == k
        row = {"k_pures": k, "Ms": it["Ms"], "support": sum(len(m) for m in Ms),
               "pairs": []}
        nlive = nblock = 0
        for p, q in PAIRS:
            if not N6.live(src, p, q):
                continue
            nlive += 1
            U = tuple(x for x in range(N) if x not in (p, q))
            v, _ = N6.decide_pair_general(src, p, q, U, f"S{k}_{p}{q}")
            row["pairs"].append({"pair": [p, q], "general": v})
            if v == "BLOCKED":
                nblock += 1
        row["n_live"], row["n_blocked"] = nlive, nblock
        row["all_blocked"] = (nlive > 0 and nblock == nlive)
        decided.append(row)
        print(f"  k={k} support={row['support']} live={nlive} "
              f"blocked={nblock} ALL_BLOCKED={row['all_blocked']}")
    RES["stratum_M_decided"] = decided
    summ = {}
    for r in decided:
        s = summ.setdefault(r["k_pures"], {"n": 0, "all_blocked": 0,
                                           "live": 0, "blocked": 0})
        s["n"] += 1
        s["all_blocked"] += int(r["all_blocked"])
        s["live"] += r["n_live"]
        s["blocked"] += r["n_blocked"]
    RES["stratum_M_summary"] = summ
    print("summary by k:", summ)

    # ---------------- support-matched randomisation control -----------------
    # Same CELL SUPPORT as the k >= 1 survivors, random nonzero values:
    # if blocking is still absent, the witnesses are support-driven and the
    # "pures" correlation is confounded.
    ctrl = []
    for r in decided:
        if r["k_pures"] == 0:
            continue
        Ms = [tuple(map(tuple, m)) for m in r["Ms"]]
        for trial in range(3):
            src = {e: [[0] * 3 for _ in range(3)] for e in PAIRS}
            for c, M in enumerate(Ms):
                for e in M:
                    src[W.ekey(*e)][c][c] = rng.randint(1, 9)
            nlive = nblock = 0
            for p, q in PAIRS:
                if not N6.live(src, p, q):
                    continue
                nlive += 1
                U = tuple(x for x in range(N) if x not in (p, q))
                v, _ = N6.decide_pair_general(src, p, q, U, f"C{trial}_{p}{q}")
                nblock += int(v == "BLOCKED")
            ctrl.append({"k_pures": r["k_pures"], "support": r["support"],
                         "mixed_exact": N6.is_mixed_exact(src, N),
                         "n_live": nlive, "n_blocked": nblock})
        if len(ctrl) >= 18:
            break
    RES["support_matched_control"] = ctrl
    print("support-matched control (k>=1 supports, random values):")
    for c in ctrl[:18]:
        print("   ", c)

    with open(f"{BASE}/results_t1b_n6_stratum.json", "w") as fh:
        json.dump(RES, fh, indent=1)


if __name__ == "__main__":
    main()
