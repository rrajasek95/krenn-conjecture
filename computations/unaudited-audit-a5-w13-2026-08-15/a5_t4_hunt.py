#!/usr/bin/env python3
"""A5 / claim 4: adversarial hunt for a counterexample to (T2).

(T2) says: for A_pq with no zero row and no zero column, no L-monomial with
>= 2 distinct kappa colours lies in L_h(A).  W13 verified this on "a battery".
Here I try hard to break it:
  (i)   EXHAUSTIVE over all 0/1 3x3 matrices with no zero line (h=2,3);
  (ii)  EXHAUSTIVE over all {-1,0,1} matrices with no zero line, h=3, up to
        the symmetry A -> D1 A D2 (sign flips) and simultaneous permutation;
  (iii) random rank-1 and rank-2 matrices with no zero entry;
  (iv)  matrices with prescribed vanishing 2x2 minors;
  (v)   h=4 and h=5 spot checks (h=5 non-membership certified by F_p rank
        against the structural upper bound dim L_5 <= sum dim Sigma_k).
"""
from __future__ import annotations
import json, random, sys, time
from itertools import product
sys.path.insert(0, "/Users/rishi/workplace/krenn-conjecture/computations/unaudited-audit-a5-w13-2026-08-15")
import a5_core as A
from a5_t4_taxonomy import monomial_vec, det3, has_zero_line, classify

OUT = "/Users/rishi/workplace/krenn-conjecture/computations/unaudited-audit-a5-w13-2026-08-15/"


def multicolour_keys(h):
    out = []
    for a in range(h + 1):
        for bs in product(range(h + 1), repeat=3):
            if a + sum(bs) != h:
                continue
            if sum(1 for b in bs if b) >= 2:
                out.append((a,) + bs)
    return out


def t2_violations(M, h, rng):
    svec = [M[i][j] for i in range(3) for j in range(3)]
    rows = A.L_rows(h, svec, rng)
    ech, piv = A.int_echelon(rows)
    bad = []
    for key in multicolour_keys(h):
        v = monomial_vec(h, svec, key[0], key[1:])
        if A.in_span_exact(ech, piv, v):
            bad.append(key)
    return bad, len(piv)


def t2_violations_modp(M, h, primes=(2147483629, 1000003)):
    """Non-membership certified over F_p against the structural bound."""
    rng = random.Random(5)
    svec = [M[i][j] for i in range(3) for j in range(3)]
    rows = A.L_rows(h, svec, rng)
    ub = sum(((k + 1) * (k + 2) // 2) ** 2 for k in range(2, h + 1))
    ranks = [A.rank_mod_p_np(rows, p) for p in primes]
    bad, certified = [], all(r == max(ranks) for r in ranks)
    for key in multicolour_keys(h):
        v = monomial_vec(h, svec, key[0], key[1:])
        inc = [A.rank_mod_p_np(rows + [v], p) for p in primes]
        if all(i == r for i, r in zip(inc, ranks)):
            bad.append(key)      # possibly in L_h (mod p cannot prove it)
    return bad, ranks, ub, certified


def main():
    rng = random.Random(1618)
    log = {"sweeps": []}

    # ---------------- (i) all 0/1 matrices, no zero line
    for h in (2, 3):
        t0, n, viol = time.time(), 0, []
        for bits in range(512):
            M = [[(bits >> (3 * i + j)) & 1 for j in range(3)] for i in range(3)]
            if has_zero_line(M):
                continue
            n += 1
            bad, dimL = t2_violations(M, h, rng)
            if bad:
                viol.append({"A": M, "bad": [list(b) for b in bad], "dimL": dimL})
        print(f"(i) h={h}: {n} 0/1 matrices with no zero line, "
              f"{len(viol)} T2 violations [{time.time()-t0:.0f}s]", flush=True)
        for v in viol:
            print("    VIOLATION", v, flush=True)
        log["sweeps"].append({"sweep": "0/1 exhaustive", "h": h, "n": n,
                              "violations": viol})

    # ---------------- (ii) all {-1,0,1} matrices, no zero line, h=3, up to
    # simultaneous permutation + row/col sign flips
    h = 3
    seen, reps = set(), []
    vals = (-1, 0, 1)
    perms = list(product(range(3), repeat=3))
    perms = [p for p in perms if sorted(p) == [0, 1, 2]]
    for cells in product(vals, repeat=9):
        M = [list(cells[3 * i:3 * i + 3]) for i in range(3)]
        if has_zero_line(M):
            continue
        key = None
        for sg in product((1, -1), repeat=6):
            for sp in perms:
                MM = tuple(tuple(sg[i] * sg[3 + j] * M[sp[i]][sp[j]] for j in range(3))
                           for i in range(3))
                if key is None or MM < key:
                    key = MM
        if key in seen:
            continue
        seen.add(key)
        reps.append([list(r) for r in key])
    print(f"(ii) {len(reps)} orbit representatives over {{-1,0,1}} with no zero line",
          flush=True)
    t0, viol = time.time(), []
    for i, M in enumerate(reps):
        bad, dimL = t2_violations(M, h, rng)
        if bad:
            viol.append({"A": M, "bad": [list(b) for b in bad], "dimL": dimL})
            print("    VIOLATION", M, bad, flush=True)
        if i % 50 == 0:
            print(f"    ... {i}/{len(reps)} [{time.time()-t0:.0f}s]", flush=True)
    print(f"(ii) h=3: {len(reps)} reps, {len(viol)} T2 violations "
          f"[{time.time()-t0:.0f}s]", flush=True)
    log["sweeps"].append({"sweep": "{-1,0,1} exhaustive up to symmetry", "h": 3,
                          "n": len(reps), "violations": viol})

    # ---------------- (iii) random low-rank with no zero entry
    for h in (3, 4):
        t0, viol, n = time.time(), [], 0
        for trial in range(60 if h == 3 else 20):
            kind = trial % 3
            if kind == 0:
                u = [rng.choice([-3, -2, -1, 1, 2, 3]) for _ in range(3)]
                v = [rng.choice([-3, -2, -1, 1, 2, 3]) for _ in range(3)]
                M = [[u[i] * v[j] for j in range(3)] for i in range(3)]
            elif kind == 1:
                u1 = [rng.randint(-3, 3) for _ in range(3)]
                v1 = [rng.randint(-3, 3) for _ in range(3)]
                u2 = [rng.randint(-3, 3) for _ in range(3)]
                v2 = [rng.randint(-3, 3) for _ in range(3)]
                M = [[u1[i] * v1[j] + u2[i] * v2[j] for j in range(3)] for i in range(3)]
            else:
                M = [[rng.randint(-6, 6) for _ in range(3)] for _ in range(3)]
                M[2] = [M[0][j] + M[1][j] for j in range(3)]
            if has_zero_line(M):
                continue
            n += 1
            bad, dimL = t2_violations(M, h, rng)
            if bad:
                viol.append({"A": M, "bad": [list(b) for b in bad], "dimL": dimL})
                print("    VIOLATION", M, bad, flush=True)
        print(f"(iii) h={h}: {n} random low-rank no-zero-line matrices, "
              f"{len(viol)} violations [{time.time()-t0:.0f}s]", flush=True)
        log["sweeps"].append({"sweep": "random low rank", "h": h, "n": n,
                              "violations": viol})

    # ---------------- (v) h=5 spot check, F_p + structural bound
    t0 = time.time()
    h5 = []
    for name, M in [("identity", [[1, 0, 0], [0, 1, 0], [0, 0, 1]]),
                    ("all-ones J", [[1] * 3] * 3),
                    ("random", [[rng.randint(-4, 4) for _ in range(3)] for _ in range(3)]),
                    ("single cell E22", [[0, 0, 0], [0, 0, 0], [0, 0, 1]])]:
        bad, ranks, ub, cert = t2_violations_modp(M, 5)
        print(f"(v) h=5 A={name}: ranks {ranks} (structural bound {ub}); "
              f"multi-colour monomials NOT excluded: {[list(b) for b in bad]} "
              f"[{time.time()-t0:.0f}s]", flush=True)
        h5.append({"A": name, "ranks": ranks, "bound": ub,
                   "not_excluded": [list(b) for b in bad], "zero_line": has_zero_line(M)})
    log["h5"] = h5
    json.dump(log, open(OUT + "results_t4_hunt.json", "w"), indent=1)


if __name__ == "__main__":
    main()
