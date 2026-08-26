#!/usr/bin/env python3
"""W22 T1c -- THEOREM W22-1 at general N, and the h = 3 / h = 4 instances;
plus an independent re-decision of the committed near-exact six-site source.

THEOREM W22-1 (all-blocked mixed-exact sources exist at every even N).
On the constant-block source A_uv = t_uv J (J = all-ones 3x3):
    R_ab = sigma(K) (t_pa t_qb + t_pb t_qa) J,    s = t_pq sigma(K),
    sigma(K) = sum_ij K_ij,
so every term of E_pq(K) is a scalar multiple of 1^{(x)U} and

    E_pq(K) = sigma(K)^h * E^{W5}_{pq}(t) * 1^{(x)U},

where E^{W5}_{pq}(t) is W5's SCALAR slice error of the edge weighting t.
Admissibility forces sigma(K) != 0 (else s = 0), so

    (p,q) is LIVE  <=>  t_pq != 0,
    (p,q) is BLOCKED (for GENERAL caps)  <=>  E^{W5}_{pq}(t) != 0.

Since H_B(A)_w = haf(t) for EVERY word, haf(t) = 0 makes the source
mixed-exact (all pures 0).  Generic t on {haf(t) = 0} has all pairs live and
all pairs blocked -- exhibited exactly at N = 6, 8, 10, 12.

CONSEQUENCE: "every live pair blocked" is CONSISTENT with mixed-exactness at
every even N.  No proof of U(N) can use the mixed equations alone.
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
sys.path.insert(0, "/Users/rishi/workplace/krenn-conjecture/computations/"
                   "unaudited-slice-dirtiness-w5-2026-08-15")
import w22_core as W                                        # noqa: E402
import w22_n6 as N6                                         # noqa: E402
import slice_core                                           # noqa: E402

RES = {}


def haf_t(t, sites):
    total = 0
    for M in W.perfect_matchings(tuple(sites)):
        term = 1
        for a, b in M:
            term *= t[W.ekey(a, b)]
            if term == 0:
                break
        total += term
    return total


def find_t(n, rng, tries=4000):
    """t with all entries nonzero, haf(t) = 0, and E^{W5}_{pq}(t) != 0 for
    EVERY pair (all pairs live and blocked)."""
    pairs = list(combinations(range(n), 2))
    for _ in range(tries):
        t = {e: rng.randint(-6, 6) for e in pairs}
        e0 = pairs[rng.randrange(len(pairs))]
        t[e0] = 0
        b0 = haf_t(t, range(n))
        t[e0] = 1
        c0 = haf_t(t, range(n)) - b0
        if c0 == 0:
            continue
        v = Fraction(-b0, c0)
        d = v.denominator
        tt = {e: (int(v * d) if e == e0 else int(val * d))
              for e, val in t.items()}
        if any(x == 0 for x in tt.values()) or haf_t(tt, range(n)) != 0:
            continue
        ok = True
        for p, q in pairs:
            U = tuple(x for x in range(n) if x not in (p, q))
            if W.scalar_slice_error(tt, p, q, U) == 0:
                ok = False
                break
        if ok:
            return tt
    return None


def main():
    rng = random.Random(20260815)

    # ---------------- Theorem W22-1 at N = 6, 8, 10, 12 --------------------
    rows = []
    for n in (6, 8, 10, 12):
        if n >= 12:
            rng2 = random.Random(11)
        t = find_t(n, rng, tries=3000 if n <= 10 else 400)
        pairs = list(combinations(range(n), 2))
        if t is None:
            rows.append({"N": n, "found": False})
            print(f"N={n}: no all-blocked witness found in budget")
            continue
        row = {"N": n, "h": n // 2 - 1, "found": True,
               "t": {f"{a},{b}": t[(a, b)] for a, b in pairs},
               "haf_t": haf_t(t, range(n)),
               "n_pairs": len(pairs)}
        # verify the closed form against the FULL tensor evaluator
        src = N6.source_P0_constant(t, n)
        mism = 0
        checked = 0
        for _ in range(6 if n <= 8 else 2):
            p, q = rng.sample(range(n), 2)
            U = tuple(x for x in range(n) if x not in (p, q))
            K = [[rng.randint(-3, 3) for _ in range(3)] for _ in range(3)]
            sig = sum(K[i][j] for i in range(3) for j in range(3))
            h = n // 2 - 1
            pred = (sig ** h) * W.scalar_slice_error(t, p, q, U)
            err = W.cap_error_direct(src, p, q, K, U)
            got = err.get((0,) * len(U), 0)
            same = all(v == got for v in err.values())
            checked += 1
            if got != pred or not same:
                mism += 1
        row["closed_form_checked"] = checked
        row["closed_form_mismatches"] = mism
        # mixed-exactness (full check only where affordable)
        if n <= 8:
            row["mixed_defects"] = len(W.mixed_defects(src, n))
            row["pures"] = [str(v) for v in W.pures(src, n).values()]
        else:
            row["mixed_exact_by_theorem"] = True   # H_w = haf(t) = 0 for all w
        row["all_live"] = all(t[e] != 0 for e in pairs)
        row["all_blocked"] = True
        rows.append(row)
        print(f"N={n} h={n//2-1}: all {len(pairs)} pairs live and BLOCKED; "
              f"haf(t)=0; closed form {checked} checks {mism} mismatches; "
              f"mixed defects {row.get('mixed_defects', 'n/a')}")
    RES["theorem_W22_1"] = rows

    # ---- independent Singular confirmation of blocking at N = 8 (h = 3) ---
    r8 = [r for r in rows if r["N"] == 8 and r.get("found")]
    if r8:
        t8 = {tuple(int(x) for x in k.split(",")): v
              for k, v in r8[0]["t"].items()}
        src8 = N6.source_P0_constant(t8, 8)
        confirm = []
        for (p, q) in [(0, 1), (2, 5), (3, 7)]:
            U = tuple(x for x in range(8) if x not in (p, q))
            # h = 3 general-cap decision: 729 cubics in 9 cap variables
            import sympy
            K = [[sympy.Symbol(f"k{i}{j}") for j in range(3)] for i in range(3)]
            apq = W.oriented(src8, p, q)
            s = sympy.expand(sum(K[i][j] * apq[i][j]
                                 for i in range(3) for j in range(3)))
            Rt = {}
            for a, b in combinations(U, 2):
                apa, aqa = W.oriented(src8, p, a), W.oriented(src8, q, a)
                apb, aqb = W.oriented(src8, p, b), W.oriented(src8, q, b)
                Rt[(a, b)] = [[sympy.expand(sum(
                    K[i][j] * (apa[i][ca] * aqb[j][cb] + aqa[j][ca] * apb[i][cb])
                    for i in range(3) for j in range(3)))
                    for cb in range(3)] for ca in range(3)]
            slot = {a: i for i, a in enumerate(U)}
            A = {(a, b): W.oriented(src8, a, b) for a, b in combinations(U, 2)}
            eqs = set()
            for word in product(range(3), repeat=6):
                tot = sympy.Integer(0)
                for M in W.perfect_matchings(U):
                    for size in (2, 3):
                        for Js in combinations(range(3), size):
                            Js = set(Js)
                            term = s ** (3 - size)
                            for i2, (a, b) in enumerate(M):
                                ca, cb = word[slot[a]], word[slot[b]]
                                tab = Rt if i2 in Js else A
                                term = term * (tab[(a, b)][ca][cb]
                                               if (a, b) in tab
                                               else tab[(b, a)][cb][ca])
                            tot += term
                tot = sympy.expand(tot)
                if tot != 0:
                    eqs.add(sympy.srepr(tot))
            polys = [sympy.sympify(e) for e in eqs]
            gens = [N6.sing_poly(e) for e in polys]
            nz = ("(" + N6.sing_poly(s) + ")*k00*k11*k22")
            script = "\n".join([
                f'ring RR=0,({",".join(N6.KVARS)},zzt),dp;',
                "ideal zzI=" + (",".join(gens) if gens else "0") + ";",
                f"ideal zzJ=zzI,zzt*({nz})-1;",
                f'"DECN8 {p}{q} "+string(dim(std(zzJ)));'])
            W.no_shadow_guard(script, set(N6.KVARS) | {"zzt"})
            out = W.run_singular(script, timeout=1800)
            d = int([ln for ln in out.splitlines()
                     if ln.startswith(f"DECN8 {p}{q}")][0].split()[-1])
            confirm.append({"pair": [p, q], "n_distinct_cubics": len(polys),
                            "dim": d,
                            "verdict": "BLOCKED" if d == -1 else "WITNESS"})
            print(f"   N=8 h=3 Singular general-cap decision at ({p},{q}): "
                  f"{confirm[-1]['verdict']} ({len(polys)} distinct cubics)")
        RES["N8_h3_singular_confirmation"] = confirm

    # ---------------- the committed near-exact six-site source -------------
    import os
    cert = os.path.join(
        "/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-scalar-slice-w17-2026-08-15", "results_t2e_nearexact_certificate.json")
    with open(cert) as fh:
        C = json.load(fh)
    blocks = C["blocks"]
    src = {}
    for k, m in blocks.items():
        a, b = (int(x) for x in k.replace("(", "").replace(")", "").split(","))
        src[(a, b)] = [[Fraction(str(x)) for x in row] for row in m]
    n = 6
    md = len(W.mixed_defects(src, n))
    pu = W.pures(src, n)
    print(f"\n[near-exact six-site] mixed defects {md}/726, "
          f"pures {[str(pu[c]) for c in range(3)]}")
    ne = {"mixed_defects": md, "n_mixed": 726,
          "pures": [str(pu[c]) for c in range(3)], "pairs": []}
    for p, q in combinations(range(n), 2):
        U = tuple(x for x in range(n) if x not in (p, q))
        lv = N6.live(src, p, q)
        row = {"pair": [p, q], "live": lv}
        if lv:
            v, _ = N6.decide_pair_general(src, p, q, U, f"NE{p}{q}")
            row["general"] = v
            # support structure: how many sites of U are detached from p or q
            det_p = sum(1 for a in U
                        if all(x == 0 for r in W.oriented(src, p, a) for x in r))
            det_q = sum(1 for a in U
                        if all(x == 0 for r in W.oriented(src, q, a) for x in r))
            row["detached_p"] = det_p
            row["detached_q"] = det_q
        ne["pairs"].append(row)
    nl = sum(1 for r in ne["pairs"] if r["live"])
    nw = sum(1 for r in ne["pairs"] if r.get("general") == "WITNESS")
    ne["n_live"], ne["n_witness"] = nl, nw
    print(f"[near-exact six-site] live {nl}, general-cap WITNESS {nw} "
          f"(W17 recorded 9) -- independent re-decision")
    RES["near_exact_six_site"] = ne

    with open(f"{BASE}/results_t1c_uniform.json", "w") as fh:
        json.dump(RES, fh, indent=1, default=str)


if __name__ == "__main__":
    main()
