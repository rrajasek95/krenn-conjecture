#!/usr/bin/env python3
"""A5 final checks:
 (1) exact characterisation of the (T2) failures at h=3 (my predicted rule
     vs the measured answer, on every 0/1 matrix with no zero line);
 (2) hunt for a (T2) failure with A_pq of FULL SUPPORT (no zero entry);
 (3) claim-8 control: W13's F1 shape WITH A_pq(c,c) = 0 (their trials 0,1);
 (4) the K_{2,3} structural facts at every even N in [8,50], without
     enumerating matchings (per-colour induced-matching counts).
"""
from __future__ import annotations
import json, random, sys
from itertools import combinations, product
sys.path.insert(0, "/Users/rishi/workplace/krenn-conjecture/computations/unaudited-audit-a5-w13-2026-08-15")
import a5_core as A
from a5_t4_taxonomy import monomial_vec, has_zero_line, det3
from a5_t6_k23 import family_F, family_Fprime

OUT = "/Users/rishi/workplace/krenn-conjecture/computations/unaudited-audit-a5-w13-2026-08-15/"
res = {}
rng = random.Random(2026)


# ---------------------------------------------------------------- (1)
def predicted_violation(M, c, cprime):
    """my rule for kappa_c kappa_{c'}^{h-1}: A_cc != 0 and A_ij = 0 for every
    (i,j) with i != c' and j != c', except (c,c)."""
    if M[c][c] == 0:
        return False
    for i in range(3):
        for j in range(3):
            if i == cprime or j == cprime:
                continue
            if (i, j) == (c, c):
                continue
            if M[i][j] != 0:
                return False
    return True


h = 3
mism, n = [], 0
for bits in range(512):
    M = [[(bits >> (3 * i + j)) & 1 for j in range(3)] for i in range(3)]
    if has_zero_line(M):
        continue
    n += 1
    svec = [M[i][j] for i in range(3) for j in range(3)]
    ech, piv = A.int_echelon(A.L_rows(h, svec, rng))
    for c in range(3):
        for cp in range(3):
            if c == cp:
                continue
            bs = tuple((h - 1) if t == cp else (1 if t == c else 0) for t in range(3))
            got = A.in_span_exact(ech, piv, monomial_vec(h, svec, 0, bs))
            want = predicted_violation(M, c, cp)
            if got != want:
                mism.append({"A": M, "c": c, "cprime": cp, "measured": got, "rule": want})
print(f"(1) 0/1 matrices, no zero line: {n}; rule-vs-measurement mismatches: {len(mism)}",
      flush=True)
for m in mism[:6]:
    print("   MISMATCH", m, flush=True)
res["rule_check"] = {"n": n, "mismatches": mism}

# ---------------------------------------------------------------- (2)
def multicolour_keys(hh):
    out = []
    for a in range(hh + 1):
        for bs in product(range(hh + 1), repeat=3):
            if a + sum(bs) != hh:
                continue
            if sum(1 for b in bs if b) >= 2:
                out.append((a,) + bs)
    return out


viol, tested = [], 0
NZ = [-3, -2, -1, 1, 2, 3]
for trial in range(220):
    kind = trial % 5
    if kind == 0:
        M = [[rng.choice(NZ) for _ in range(3)] for _ in range(3)]
    elif kind == 1:                     # rank 1, full support
        u = [rng.choice(NZ) for _ in range(3)]
        v = [rng.choice(NZ) for _ in range(3)]
        M = [[u[i] * v[j] for j in range(3)] for i in range(3)]
    elif kind == 2:                     # rank 2, full support
        while True:
            u1 = [rng.choice(NZ) for _ in range(3)]
            v1 = [rng.choice(NZ) for _ in range(3)]
            u2 = [rng.choice(NZ) for _ in range(3)]
            v2 = [rng.choice(NZ) for _ in range(3)]
            M = [[u1[i] * v1[j] + u2[i] * v2[j] for j in range(3)] for i in range(3)]
            if not has_zero_line(M) and all(M[i][j] for i in range(3) for j in range(3)):
                break
    elif kind == 3:                     # a vanishing 2x2 minor, full support
        M = [[rng.choice(NZ) for _ in range(3)] for _ in range(3)]
        M[1][1] = M[0][1] * M[1][0] // M[0][0] if M[0][0] and (M[0][1] * M[1][0]) % M[0][0] == 0 else M[1][1]
    else:                               # symmetric / circulant-ish
        a, b, cc = (rng.choice(NZ) for _ in range(3))
        M = [[a, b, cc], [cc, a, b], [b, cc, a]]
    if has_zero_line(M) or any(M[i][j] == 0 for i in range(3) for j in range(3)):
        continue
    tested += 1
    svec = [M[i][j] for i in range(3) for j in range(3)]
    ech, piv = A.int_echelon(A.L_rows(3, svec, rng))
    bad = [k for k in multicolour_keys(3)
           if A.in_span_exact(ech, piv, monomial_vec(3, svec, k[0], k[1:]))]
    if bad:
        viol.append({"A": M, "bad": [list(b) for b in bad]})
        print("   FULL-SUPPORT VIOLATION", M, bad, flush=True)
print(f"(2) full-support A tested at h=3: {tested}; T2 violations: {len(viol)}", flush=True)
res["full_support_hunt"] = {"tested": tested, "violations": viol}

# ---------------------------------------------------------------- (3)
import a5_fast as F
from a5_t8_transfer import build_clean_source, analyse
r3 = []
for c in (0, 1):
    src = build_clean_source(3, rng, c, "F1", zero_diag=True)
    rec = analyse(src, 3, c, f"F1 shape with A_cc = 0, colour {c}", rng=rng)
    print("(3)", json.dumps({k: v for k, v in rec.items() if k != "A_pq"}), flush=True)
    r3.append(rec)
res["F1_zero_diag"] = r3

# ---------------------------------------------------------------- (4)
def count_pm(verts, edges):
    verts = sorted(verts)
    if not verts:
        return 1
    idx = {v: i for i, v in enumerate(verts)}
    adj = [0] * len(verts)
    for (a, b) in edges:
        if a in idx and b in idx:
            adj[idx[a]] |= 1 << idx[b]
            adj[idx[b]] |= 1 << idx[a]
    from functools import lru_cache

    @lru_cache(maxsize=None)
    def rec(mask):
        if mask == 0:
            return 1
        i = (mask & -mask).bit_length() - 1
        tot = 0
        m2 = mask & ~(1 << i)
        cand = adj[i] & m2
        while cand:
            j = (cand & -cand).bit_length() - 1
            tot += rec(m2 & ~(1 << j))
            cand &= cand - 1
        return tot
    return rec((1 << len(verts)) - 1)


rows4 = []
for kind, ns in (("F", range(4, 26, 2)), ("Fprime", range(5, 26, 2))):
    for nn in ns:
        N, cs, marks = (family_F(nn) if kind == "F" else family_Fprime(nn))
        if kind == "F":
            v, u = (nn - 3, nn - 2, nn - 1), (2 * nn - 2, 2 * nn - 1)
            partner = {}
            for e in cs[1]:
                partner[e[0]] = e[1]
                partner[e[1]] = e[0]
        else:
            v, u = (nn - 3, nn - 2, nn - 1), (2 * nn - 3, 2 * nn - 2)
            partner = {}
            for e in cs[1]:
                partner[e[0]] = e[1]
                partner[e[1]] = e[0]
        ok = {"kind": kind, "n": nn, "N": N}
        ok["six_edges_colour0"] = all(tuple(sorted((x, y))) in cs[0] for x in v for y in u)
        ok["colour1_pm"] = (len(cs[1]) == N // 2
                            and sorted(x for e in cs[1] for x in e) == list(range(N)))
        if kind == "Fprime":
            ok["defect_unmarked"] = marks["a"] not in set(v) | set(u)
        sizes = []
        for x, y in ((v[0], v[1]), (v[1], v[2]), (v[2], v[0])):
            mk = [x, y, u[0], u[1]]
            orph = [partner[z] for z in mk if partner[z] not in mk]
            c0 = count_pm(mk, cs[0])
            c2 = count_pm(orph, cs[2])
            rest = [z for z in range(N) if z not in mk and z not in orph]
            partner_closed = all(partner[z] in rest for z in rest)
            c1 = 1 if partner_closed else count_pm(rest, cs[1])
            sizes.append([c0, c1, c2, partner_closed])
        ok["per_colour_counts"] = sizes
        ok["all_fibres_exactly_2"] = all(s[0] == 2 and s[1] == 1 and s[2] == 1 and s[3]
                                         for s in sizes)
        rows4.append(ok)
        print(f"(4) {kind}_{nn} N={N}: six0={ok['six_edges_colour0']} c1pm={ok['colour1_pm']} "
              f"fibres 2x1x1 = {ok['all_fibres_exactly_2']} counts={sizes}", flush=True)
res["k23_structural"] = rows4
json.dump(res, open(OUT + "results_final_checks.json", "w"), indent=1, default=str)
print("DONE")
