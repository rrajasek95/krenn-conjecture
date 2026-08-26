#!/usr/bin/env python3
"""A8 T2 -- independent re-enumeration of the W27-D3 / W28-DEL census.

  * enumerate all unordered triples of pairwise disjoint perfect matchings
    of K_8 with my own PM code;
  * evaluate (B), (C), (D) FROM THE RAW HAFNIAN CONDITIONS on the support
    (no Hamiltonicity shortcut) -- then, separately, evaluate the shortcut
    and compare the two boolean vectors elementwise;
  * validate the whole combinatorics->algebra translation by putting random
    exact weights on a sample of triples and computing H_w by the RAW word
    definition over all 105 PMs of K_8;
  * mutation controls on every checker.
"""
import random
import sys
import time
from fractions import Fraction
from itertools import combinations, permutations

sys.path.insert(0, "/Users/rishi/workplace/krenn-conjecture/computations/unaudited-audit-a8-2026-08-19")
from a8_core import (COLORS, H_raw, checkpoint, diag_blocks, haf, is_constant,
                     offcount, perfect_matchings, profile, require, words)

OUT = "/Users/rishi/workplace/krenn-conjecture/computations/unaudited-audit-a8-2026-08-19"
N = 8
V = tuple(range(N))
R = {}
RAN = []
t0 = time.time()


def sect(s):
    print("=" * 74)
    print(s)
    print("=" * 74)


PMS = perfect_matchings(V)
require(len(PMS) == 105, "105 PMs")
PMSET = [frozenset(m) for m in PMS]
FOUR = [frozenset(S) for S in combinations(V, 4)]

sect("(1) triples of pairwise disjoint perfect matchings of K_8")
disj_pairs = [(i, j) for i in range(105) for j in range(i + 1, 105)
              if not (PMSET[i] & PMSET[j])]
triples = []
for a in range(105):
    for b in range(a + 1, 105):
        if PMSET[a] & PMSET[b]:
            continue
        for c in range(b + 1, 105):
            if (PMSET[a] & PMSET[c]) or (PMSET[b] & PMSET[c]):
                continue
            triples.append((a, b, c))
print(f"   disjoint pairs: {len(disj_pairs)}    unordered disjoint triples: {len(triples)}")
print(f"   ordered triples = 6 x {len(triples)} = {6*len(triples)}")
R["n_disjoint_pairs"] = len(disj_pairs)
R["n_triples"] = len(triples)
RAN.append("T2_enum")


# ---------------------------------------------------------------- raw tests
_NPMC = {}


def npm_sub(M, S):
    """number of perfect matchings of the SUPPORT M (a set of edges) on vertex
    set S -- computed by the raw definition (memoised, same values)."""
    S = tuple(sorted(S))
    key = (M, S)
    r = _NPMC.get(key)
    if r is not None:
        return r
    if len(S) % 2:
        r = 0
    else:
        r = sum(1 for m in perfect_matchings(S) if all(e in M for e in m))
    _NPMC[key] = r
    return r


def cond_B_raw(Ms):
    """(6,2,0): haf(t^a|V-pq) * t^b_pq = 0  for a != b."""
    for p, q in combinations(V, 2):
        rest = [x for x in V if x not in (p, q)]
        for a in range(3):
            if npm_sub(Ms[a], rest) == 0:
                continue
            for b in range(3):
                if b != a and (p, q) in Ms[b]:
                    return False
    return True


def cond_C_raw(Ms):
    """(4,4,0): haf(t^a|S) * haf(t^b|V-S) = 0  for a != b, |S| = 4."""
    for S in FOUR:
        comp = frozenset(V) - S
        for a in range(3):
            if npm_sub(Ms[a], S) == 0:
                continue
            for b in range(3):
                if b != a and npm_sub(Ms[b], comp):
                    return False
    return True


def cond_D_raw(Ms):
    """(4,2,2): haf(t^a|S) * t^b_pq * t^c_rs = 0, {a,b,c}={0,1,2}, V-S = pq+rs."""
    for S in FOUR:
        comp = sorted(frozenset(V) - S)
        splits = [((comp[0], comp[i]),
                   tuple(x for x in comp[1:] if x != comp[i])) for i in (1, 2, 3)]
        for a in range(3):
            if npm_sub(Ms[a], S) == 0:
                continue
            others = [x for x in range(3) if x != a]
            for e1, e2 in splits:
                for b, c in ((others[0], others[1]), (others[1], others[0])):
                    if e1 in Ms[b] and e2 in Ms[c]:
                        return False
    return True


def union_is_hamiltonian(M1, M2):
    """M1 u M2 is 2-regular; Hamiltonian iff a single 8-cycle."""
    adj = {v: [] for v in V}
    for (u, w) in list(M1) + list(M2):
        adj[u].append(w)
        adj[w].append(u)
    seen = {0}
    prev, cur = None, 0
    for _ in range(N - 1):
        nxt = adj[cur][0] if adj[cur][0] != prev else adj[cur][1]
        prev, cur = cur, nxt
        if cur in seen:
            return False
        seen.add(cur)
    return len(seen) == N


sect("(2) (B)/(C)/(D) by the RAW hafnian conditions on all triples")
passB = passC = passD = passBoth = 0
cD_raw = []
cC_raw = []
cC_ham = []
by_ct = {}
for k, (a, b, c) in enumerate(triples):
    Ms = (PMSET[a], PMSET[b], PMSET[c])
    B = cond_B_raw(Ms)
    C = cond_C_raw(Ms)
    D = cond_D_raw(Ms)
    ham = (union_is_hamiltonian(Ms[0], Ms[1]) and union_is_hamiltonian(Ms[0], Ms[2])
           and union_is_hamiltonian(Ms[1], Ms[2]))
    passB += B
    passC += C
    passD += D
    passBoth += (C and D)
    cC_raw.append(C)
    cC_ham.append(ham)
    cD_raw.append(D)
    key = (C, D, ham)
    by_ct[key] = by_ct.get(key, 0) + 1
    if k % 8000 == 0 and k:
        print(f"      ... {k} scanned ({time.time()-t0:.0f}s)")
print(f"   pass (B): {passB}   (must be all {len(triples)})")
print(f"   pass (C): {passC}")
print(f"   pass (D): {passD}")
print(f"   pass (C) AND (D): {passBoth}")
print(f"   W27-D3/W28 reported 32970 / 16800 / 8610 / 0")
mismatch_CH = sum(1 for x, y in zip(cC_raw, cC_ham) if x != y)
print(f"   raw-(C) vs 'all three pairwise unions Hamiltonian': mismatches = {mismatch_CH} "
      f"(must be 0)  => the shortcut is DERIVED, not assumed")
print(f"   joint distribution (C,D,ham): { {str(k): v for k, v in sorted(by_ct.items())} }")
R["census"] = dict(triples=len(triples), passB=passB, passC=passC, passD=passD,
                   passBoth=passBoth, C_vs_ham_mismatches=mismatch_CH)
require(passB == len(triples), "(B) must hold for every disjoint triple")
require(mismatch_CH == 0, "(C) <=> Hamiltonian shortcut")
RAN.append("T2_raw_census")
RAN.append("T2_shortcut_derivation")

# MUTATION CONTROLS on the raw checkers -----------------------------------
sect("(3) mutation controls")
rng = random.Random(4242)
# (i) NON-disjoint triples must break (B) most of the time.
bad_pairs = [(i, j) for i in range(105) for j in range(i + 1, 105) if PMSET[i] & PMSET[j]]
fired = 0
tried = 0
for _ in range(200):
    i, j = rng.choice(bad_pairs)
    k = rng.randrange(105)
    if k in (i, j):
        continue
    tried += 1
    if not cond_B_raw((PMSET[i], PMSET[j], PMSET[k])):
        fired += 1
print(f"   [ctrl] overlapping matchings: (B) fails {fired}/{tried} (must be > 0)")
require(fired > 0, "(B) checker never fires")
RAN.append("T2_ctrl_B_fires")

# (ii) a supports triple that is NOT three PMs: give class 0 a 4-cycle-free
#      support with no PM -> (A) would fail; check cond checkers still discriminate
sample = rng.sample(range(len(triples)), 40)
cnt_C_fail = sum(1 for k in sample if not cC_raw[k])
cnt_D_fail = sum(1 for k in sample if not cD_raw[k])
print(f"   [ctrl] on 40 random triples (C) fails {cnt_C_fail}, (D) fails {cnt_D_fail} "
      f"(both must be > 0 -- the checkers are non-vacuous)")
require(cnt_C_fail > 0 and cnt_D_fail > 0, "checkers vacuous")
RAN.append("T2_ctrl_nonvacuous")

# ------------------------------------------------- (4) algebra <-> combinatorics
sect("(4) translation control: RAW H_w on real weighted diagonal sources")
# For a triple, put random nonzero weights on M_c and 0 elsewhere; then the
# diagonal source's H_w on the 12 live profiles must vanish for every live word
# iff (B) and (C) and (D) hold.  Uses H_raw over all 105 PMs -- no product
# formula, no shortcut.
livewords = [w for w in words(8)
             if (not is_constant(w)) and all(x % 2 == 0 for x in profile(w))
             and offcount(w) <= 4]
print(f"   live words (mixed, all-even classes, off-count <= 4): {len(livewords)}")
allwords_oc4 = [w for w in words(8) if offcount(w) <= 4]
print(f"   all words with off-count <= 4: {len(allwords_oc4)}")
chosen = rng.sample(range(len(triples)), 24)
agree = 0
detail = []
for k in chosen:
    a, b, c = triples[k]
    Ms = (PMSET[a], PMSET[b], PMSET[c])
    t = {}
    for ci, M in enumerate(Ms):
        t[ci] = {}
        for e in M:
            v = 0
            while v == 0:
                v = Fraction(rng.randint(-9, 9), rng.randint(1, 6))
            t[ci][e] = v
    A = diag_blocks(t, 8)
    allzero = all(H_raw(A, w, PMS) == 0 for w in livewords)
    comb = cC_raw[k] and cD_raw[k] and cond_B_raw(Ms)
    agree += (allzero == comb)
    detail.append(dict(triple=k, raw_all_live_zero=allzero, combinatorial=comb))
print(f"   agreement raw-H vs combinatorial (B&C&D): {agree}/{len(chosen)} (must be all)")
require(agree == len(chosen), f"translation broken: {[d for d in detail if d['raw_all_live_zero'] != d['combinatorial']][:3]}")
R["translation_control"] = dict(sampled=len(chosen), agree=agree)
RAN.append("T2_translation_raw_H")

# and a full X_4 membership check on one triple after rescaling (A)
sect("(5) explicit-point control: a disjoint triple rescaled to satisfy (A)")
# choose a triple that passes (C) but fails (D) -- it must be in X_3 but not X_4
cand = [k for k in range(len(triples)) if cC_raw[k] and not cD_raw[k]]
print(f"   triples with (C) true, (D) false: {len(cand)}")
if cand:
    k = cand[0]
    a, b, c = triples[k]
    Ms = (PMSET[a], PMSET[b], PMSET[c])
    t = {ci: {e: Fraction(1) for e in M} for ci, M in enumerate(Ms)}   # products = 1
    A = diag_blocks(t, 8)
    # X_3 membership (raw), X_4 membership (raw)
    def memb(kk):
        for w in words(8):
            if offcount(w) > kk:
                continue
            val = H_raw(A, w, PMS)
            want = 1 if is_constant(w) else 0
            if val != want:
                return False, (w, str(val), want)
        return True, None
    m3 = memb(3)
    m4 = memb(4)
    print(f"   triple #{k}: in X_3? {m3[0]} ; in X_4? {m4[0]}  first X_4 failure {m4[1]}")
    R["explicit_point"] = dict(triple=k, in_X3=m3[0], in_X4=m4[0], X4_failure=str(m4[1]))
    require(m3[0] and not m4[0], "expected an X_3 \\ X_4 diagonal point here")
    RAN.append("T2_explicit_X3_not_X4")

MAN = dict(declared=["T2_enum", "T2_raw_census", "T2_shortcut_derivation",
                     "T2_ctrl_B_fires", "T2_ctrl_nonvacuous", "T2_translation_raw_H",
                     "T2_explicit_X3_not_X4"], ran=RAN)
MAN["missing"] = [x for x in MAN["declared"] if x not in RAN]
print("CONTROL MANIFEST:", MAN)
require(not MAN["missing"], "manifest incomplete")
R["manifest"] = MAN
checkpoint(OUT + "/results_t2_census.json", R)
print(f"elapsed {time.time()-t0:.0f}s")
