"""A7 TASK 4: does the per-site colour group S_3^8 preserve (R)?  Does
S_8 x S_3(global) (order 40320*6 = 241920) preserve it?

Transport lemma (proved, and validated here against the direct computation):
  for sigma in S_3^8 acting on templates by relabelling the rows/columns of each
  block, fibre_{sigma.T}(sigma.w) = fibre_T(w) AS SETS OF MATCHINGS.  Hence
    Gamma(sigma.T) = Gamma(T);
    the three constant fibres of sigma.T are the T-fibres of the words
      w^(r)_p = sigma_p^{-1}(r);
    the mixed condition for sigma.T asks fibre_T(w) >= 3 for every w except
      those three preimages;
    (SC) for sigma.T: an edge e=(u,v) column-thin with colour c serves
      (u, sigma_v(c)); row-thin with colour r serves (v, sigma_u(r)).
This is what makes the exhaustive 6^8 = 1679616 sweep cheap.  It is cross-checked
against the direct "permute the blocks and rerun in_R" route on every element of
the structured subgroups and on a large random sample.

Mutation controls:
  MC4-A  the FAST sweep predicate vs the DIRECT in_R on 13104 structured + 20000
         random sigmas -- any disagreement is a failure of the audit tool.
  MC4-B  break the vertex action on purpose (forget to transpose the block when
         the permutation flips the endpoint order) -> S_8 preservation must fail.
  MC4-C  a deliberately non-global sigma must be exhibited that destroys in_R.
"""

import itertools
import json
import os
import random
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a7_core as C

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "results_A7_TASK4.json")

S3 = list(itertools.permutations(range(3)))          # 6 colour permutations
S3_INV = [tuple(sorted(range(3), key=lambda c: s[c])) for s in S3]
for _s, _si in zip(S3, S3_INV):
    assert all(_si[_s[c]] == c for c in range(3))

W19_WITNESS = [1, 16, 256, 511, 511, 503, 447, 256, 16, 510, 495, 511, 511, 1,
               383, 511, 510, 511, 511, 255, 511, 383, 1, 16, 256, 256, 16, 1]


def thin_data(T):
    """[(p, q, colour)] : edge {p,q} serves demand (p, colour) in T, listed as
    (owner p, far vertex q, colour c).  Under sigma the served colour becomes
    sigma_q(c)."""
    out = []
    for ei, (u, v) in enumerate(C.EDGES):
        cu = C.far_thin_colour(T[ei], True)
        if cu is not None:
            out.append((u, v, cu))
        cv = C.far_thin_colour(T[ei], False)
        if cv is not None:
            out.append((v, u, cv))
    return out


def make_fast_predicate(T):
    assert C.in_R(T)
    cnt = C.fibre_counts(T)
    td = thin_data(T)
    by_p = {p: [(q, c) for (pp, q, c) in td if pp == p] for p in range(8)}
    pow3 = [3 ** p for p in range(8)]
    const_idx = C.CONST_WORDS
    const_cnt = [int(cnt[c]) for c in const_idx]

    def pred(sig_idx):
        sig = [S3[k] for k in sig_idx]
        for p in range(8):
            s = set()
            for (q, c) in by_p[p]:
                s.add(sig[q][c])
                if len(s) == 3:
                    break
            if len(s) != 3:
                return False
        inv = [S3_INV[k] for k in sig_idx]
        pre = []
        for r in range(3):
            w = 0
            for p in range(8):
                w += inv[p][r] * pow3[p]
            pre.append(w)
        for w in pre:
            if int(cnt[w]) < 1:
                return False
        preset = set(pre)
        for s in range(3):
            if const_idx[s] not in preset and const_cnt[s] < 3:
                return False
        return True

    return pred


def direct_in_R_sigma(T, sig_idx):
    return C.in_R(C.apply_site_colour_perms(T, [S3[k] for k in sig_idx]))


def main():
    t0 = time.time()
    res = {}
    templates = {"W8_m26": C.W8_M26, "W8_m28": C.W8_M28, "W19_stratum_i": W19_WITNESS}
    for name, T in templates.items():
        assert C.in_R(T), name

    main_name, Tmain = "W8_m26", C.W8_M26
    pred = make_fast_predicate(Tmain)

    # ---------- MC4-A: fast vs direct on structured subgroups + random ----
    rng = random.Random(2718281)
    disagreements = []
    checked = 0

    def cross(sig_idx):
        nonlocal checked
        checked += 1
        a = pred(tuple(sig_idx))
        b = direct_in_R_sigma(Tmain, sig_idx)
        if a != b:
            disagreements.append({"sigma": list(sig_idx), "fast": a, "direct": b})

    # all 6^2 on every pair of sites
    two_site_total = 0
    two_site_preserve = 0
    for (p, q) in itertools.combinations(range(8), 2):
        for a in range(6):
            for b in range(6):
                sig = [0] * 8
                sig[p] = a
                sig[q] = b
                two_site_total += 1
                ok = direct_in_R_sigma(Tmain, sig)
                two_site_preserve += 1 if ok else 0
                cross(sig)
    # all 6^3 on every triple of sites
    three_site_total = 0
    three_site_preserve = 0
    for (p, q, r) in itertools.combinations(range(8), 3):
        for a in range(6):
            for b in range(6):
                for c in range(6):
                    sig = [0] * 8
                    sig[p] = a
                    sig[q] = b
                    sig[r] = c
                    three_site_total += 1
                    ok = direct_in_R_sigma(Tmain, sig)
                    three_site_preserve += 1 if ok else 0
                    cross(sig)
    for _ in range(20000):
        cross([rng.randrange(6) for _ in range(8)])
    res["MC4-A_fast_vs_direct"] = {
        "cross_checked": checked, "disagreements": len(disagreements),
        "examples": disagreements[:5],
        "FIRED_as_agreement_check": len(disagreements) == 0,
    }
    print("cross-check done: %d sigmas, %d disagreements (%.0f s)"
          % (checked, len(disagreements), time.time() - t0), flush=True)

    # ---------- exhaustive 6^8 sweep -----------------------------------
    sweep = {}
    for name, T in templates.items():
        p2 = make_fast_predicate(T)
        n_ok = 0
        survivors = []
        t1 = time.time()
        for sig in itertools.product(range(6), repeat=8):
            if p2(sig):
                n_ok += 1
                if len(survivors) < 64:
                    survivors.append(list(sig))
        n_global = sum(1 for s in survivors if len(set(s)) == 1)
        sweep[name] = {
            "group_order": 6 ** 8,
            "n_preserving_in_R": n_ok,
            "survivors_all_global": all(len(set(s)) == 1 for s in survivors),
            "survivors": survivors,
            "n_global_survivors_listed": n_global,
            "seconds": round(time.time() - t1, 1),
        }
        print("sweep %s: %d / %d preserve in_R (%.0f s)"
              % (name, n_ok, 6 ** 8, time.time() - t1), flush=True)
    res["S3_pow_8_exhaustive_sweep"] = sweep

    # ---------- structured subgroup tallies ----------------------------
    res["structured_subgroups_direct"] = {
        "template": main_name,
        "two_site_elements_tested": two_site_total,
        "two_site_preserving": two_site_preserve,
        "two_site_expected_if_only_global": 28 * 6,
        "three_site_elements_tested": three_site_total,
        "three_site_preserving": three_site_preserve,
        "three_site_expected_if_only_global": 56 * 6,
        "note": ("an element supported on <=k sites preserves (R) iff it is the identity "
                 "on those sites, EXCEPT that the 6 fully global elements are counted "
                 "inside each subgroup only when they move all 8 sites; the two/three-site "
                 "subgroups contain only the identity from the global family"),
    }

    # ---------- MC4-C: an explicit destroying sigma ---------------------
    bad = None
    for sig in itertools.product(range(6), repeat=2):
        s = [0] * 8
        s[0], s[1] = sig
        if len(set(s)) == 1:
            continue
        Tb = C.apply_site_colour_perms(Tmain, [S3[k] for k in s])
        rb = C.in_R_report(Tb)
        if not rb["in_R"]:
            bad = {"sigma": s, "sigma_perms": [list(S3[k]) for k in s],
                   "sc_ok": rb["sc_ok"], "const_fibres": rb["const_fibres"],
                   "min_mixed_fibre": rb["min_mixed_fibre"],
                   "gamma_size": rb["gamma_size"],
                   "gamma_unchanged": rb["gamma_size"] == C.in_R_report(Tmain)["gamma_size"]}
            break
    res["MC4-C_explicit_breaker"] = {"witness": bad, "FIRED": bad is not None}

    # ---------- S_8 x S_3(global) --------------------------------------
    glob = []
    for k in range(6):
        Tg = C.apply_site_colour_perms(Tmain, [S3[k]] * 8)
        glob.append({"colour_perm": list(S3[k]), "in_R": C.in_R(Tg)})
    perms = list(itertools.permutations(range(8)))
    rngv = random.Random(161803)
    sample = [list(perms[rngv.randrange(len(perms))]) for _ in range(200)]
    vtx_ok = 0
    for pi in sample:
        if C.in_R(C.apply_vertex_perm(Tmain, pi)):
            vtx_ok += 1
    # full sweep over all 40320 vertex permutations x 6 global colour perms
    full_ok = 0
    full_tot = 0
    t2 = time.time()
    for pi in perms:
        Tp = C.apply_vertex_perm(Tmain, list(pi))
        for k in range(6):
            Tpg = C.apply_site_colour_perms(Tp, [S3[k]] * 8)
            full_tot += 1
            if C.in_R(Tpg):
                full_ok += 1
    res["S8_x_S3global"] = {
        "template": main_name,
        "global_colour_perms": glob,
        "all_6_global_preserve": all(g["in_R"] for g in glob),
        "random_vertex_perms_tested": len(sample),
        "random_vertex_perms_preserving": vtx_ok,
        "exhaustive_pairs_tested": full_tot,
        "exhaustive_pairs_preserving": full_ok,
        "group_order": 40320 * 6,
        "ALL_PRESERVE": full_ok == full_tot == 241920,
        "seconds": round(time.time() - t2, 1),
    }
    print("S8xS3 exhaustive: %d/%d preserve (%.0f s)" % (full_ok, full_tot, time.time() - t2),
          flush=True)

    # ---------- MC4-B: broken vertex action ----------------------------
    def broken_vertex_perm(T, pi):
        out = [0] * 28
        for ei, (u, v) in enumerate(C.EDGES):
            a, b = pi[u], pi[v]
            out[C.edge_index(a, b)] = T[ei]        # never transposes
        return out

    nb_ok = 0
    for pi in sample:
        if C.in_R(broken_vertex_perm(Tmain, pi)):
            nb_ok += 1
    res["MC4-B_broken_vertex_action"] = {
        "tested": len(sample), "still_in_R": nb_ok,
        "correct_action_in_R": vtx_ok,
        "FIRED": nb_ok < vtx_ok,
    }

    res["seconds_total"] = round(time.time() - t0, 1)
    with open(OUT, "w") as f:
        json.dump(res, f, indent=1)
    print(json.dumps({k: v for k, v in res.items()
                      if k not in ("S3_pow_8_exhaustive_sweep",)}, indent=1)[:4000])
    for k, v in sweep.items():
        print(k, {kk: vv for kk, vv in v.items() if kk != "survivors"})


if __name__ == "__main__":
    main()
