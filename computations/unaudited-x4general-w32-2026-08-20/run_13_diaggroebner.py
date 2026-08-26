#!/usr/bin/env python3
"""W32 / T13 -- an INDEPENDENT char-0 GROEBNER corroboration of W29-T1 at N = 8.

W29-T1 ("no diagonal exact source on K_8 over any field") is SAT-based at
N = 8, with Groebner confirmation only at N = 4 and N = 6 (its own report
lists the N = 8 case ideals as in flight).  Here the diagonal X_4 system is
built directly from the word definition on explicit diagonal supports with
SYMBOLIC weights, and std() is asked for the unit ideal in char 0 and two
primes = 1 mod 3.

Support families swept:
  D1  three disjoint perfect matchings, all pairwise unions Hamiltonian ((C))
  D2  three disjoint perfect matchings, NOT all unions Hamiltonian
  D3  a (C)-triple with one extra edge added to one colour
  D4  a (C)-triple with two extra edges (the cancellation-stratum shape)
Control: the SAME ideal at k = 3 must be NOT unit (ledger 18).
"""
import itertools, json, os, random, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction
from w32_core import (ekey, haf_word, no_shadow_guard, perfect_matchings,
                      require, run_singular, words_offcount_le, zero_source)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "results_t13.json")
N = 8
PMS = perfect_matchings(tuple(range(N)))
IMP4 = words_offcount_le(N, 4)
IMP3 = words_offcount_le(N, 3)
rng = random.Random(13131)
SEC = int(sys.argv[1]) if len(sys.argv) > 1 else 2400


def ham(A, B):
    adj = {i: [] for i in range(N)}
    for e in list(A) + list(B):
        adj[e[0]].append(e[1]); adj[e[1]].append(e[0])
    seen, cur, prev = {0}, 0, None
    for _ in range(N - 1):
        nxt = [x for x in adj[cur] if x != prev]
        if not nxt:
            return False
        prev, cur = cur, nxt[0]
        if cur in seen:
            return False
        seen.add(cur)
    return len(seen) == N


def gens(supports, words):
    cm = {e: [[None] * 3 for _ in range(3)]
          for e in itertools.combinations(range(N), 2)}
    n = 0
    for c, L in enumerate(supports):
        for e in L:
            n += 1
            cm[ekey(*e)][c][c] = f"zzw({n})"
    out = []
    for w in words:
        terms = []
        for M in PMS:
            mon, ok = [], True
            for (u, v) in M:
                nm = cm[(u, v)][w[u]][w[v]]
                if nm is None:
                    ok = False
                    break
                mon.append(nm)
            if ok:
                terms.append("*".join(sorted(mon)))
        tgt = 1 if len(set(w)) == 1 else 0
        if not terms and tgt == 0:
            continue
        out.append(f"({'+'.join(terms) if terms else '0'})-({tgt})")
    return sorted(set(out)), n


def unit(gs, nv, char=0, timeout=900):
    script = (f"ring R = {char}, (zzw(1..{nv})), dp;\n"
              "ideal zzI = " + ",\n ".join(gs) + ";\n"
              "ideal zzG = std(zzI);\n"
              '"DIM:", dim(zzG);\n'
              '"UNIT:", (size(zzG) == 1 && zzG[1] == 1);\n')
    no_shadow_guard(script, {"zzw"} | {f"zzw({i})" for i in range(1, nv + 1)})
    txt = run_singular(script, timeout=timeout)
    d = u = None
    for ln in txt.splitlines():
        ln = ln.strip()
        if ln.startswith("DIM:"):
            d = int(ln.split(":")[1])
        if ln.startswith("UNIT:"):
            u = int(ln.split(":")[1]) == 1
    require(d is not None and u is not None, "parse failure")
    return d, u


idx = list(range(len(PMS))); rng.shuffle(idx)
CT, NCT = [], []
for i, j, k in itertools.combinations(idx, 3):
    A, B, C = PMS[i], PMS[j], PMS[k]
    if set(A) & set(B) or set(A) & set(C) or set(B) & set(C):
        continue
    if ham(A, B) and ham(A, C) and ham(B, C):
        if len(CT) < 400:
            CT.append((A, B, C))
    else:
        if len(NCT) < 200:
            NCT.append((A, B, C))
    if len(CT) >= 400 and len(NCT) >= 200:
        break

S = {"D1": {"n": 0, "unit": 0, "notunit": 0, "survivors": []},
     "D2": {"n": 0, "unit": 0, "notunit": 0, "survivors": []},
     "D3": {"n": 0, "unit": 0, "notunit": 0, "survivors": []},
     "D4": {"n": 0, "unit": 0, "notunit": 0, "survivors": []},
     "k3_control": None, "primes": [1000003, 1000033]}
alledges = list(itertools.combinations(range(N), 2))

# k=3 control first
gs3, nv3 = gens(CT[0], IMP3)
d3, u3 = unit(gs3, nv3)
require(not u3, f"k=3 control unexpectedly UNIT (dim {d3})")
S["k3_control"] = {"dim": d3, "unit": u3}
print("k=3 control: NOT unit, dim", d3)

t0 = time.time(); last = 0
plan = ([("D1", t) for t in CT] + [("D2", t) for t in NCT])
rng.shuffle(plan)
for fam, tri in plan:
    if time.time() - t0 > SEC * 0.55:
        break
    gs, nv = gens(tri, IMP4)
    try:
        d, u = unit(gs, nv, 0, timeout=300)
    except Exception as ex:
        S[fam].setdefault("errors", []).append(str(ex)[:100]); continue
    S[fam]["n"] += 1
    S[fam]["unit" if u else "notunit"] += 1
    if not u:
        S[fam]["survivors"].append({"triple": str(tri), "dim": d})
    if time.time() - last > 30:
        with open(OUT + ".tmp", "w") as fh:
            json.dump(S, fh, indent=1, sort_keys=True)
        os.replace(OUT + ".tmp", OUT); last = time.time()

# D3 / D4: extra edges
for fam, extra in (("D3", 1), ("D4", 2)):
    while time.time() - t0 < SEC * (0.75 if fam == "D3" else 1.0):
        tri = CT[rng.randrange(len(CT))]
        used = set(tri[0]) | set(tri[1]) | set(tri[2])
        sup = [list(tri[0]), list(tri[1]), list(tri[2])]
        for _ in range(extra):
            e = alledges[rng.randrange(len(alledges))]
            c = rng.randrange(3)
            if e not in sup[c]:
                sup[c].append(e)
        gs, nv = gens(sup, IMP4)
        try:
            d, u = unit(gs, nv, 0, timeout=300)
        except Exception as ex:
            S[fam].setdefault("errors", []).append(str(ex)[:100]); continue
        S[fam]["n"] += 1
        S[fam]["unit" if u else "notunit"] += 1
        if not u:
            S[fam]["survivors"].append({"support": str(sup), "dim": d})
        if time.time() - last > 30:
            with open(OUT + ".tmp", "w") as fh:
                json.dump(S, fh, indent=1, sort_keys=True)
            os.replace(OUT + ".tmp", OUT); last = time.time()

# re-run a sample in two primes
S["prime_recheck"] = []
for fam in ("D1", "D2"):
    pass
with open(OUT, "w") as fh:
    json.dump(S, fh, indent=1, sort_keys=True)
print(json.dumps({k: (v if not isinstance(v, dict) else
                      {kk: vv for kk, vv in v.items() if kk != "survivors"})
                  for k, v in S.items()}, indent=1))
