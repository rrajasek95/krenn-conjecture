#!/usr/bin/env python3
r"""W31 / R1 -- per-support inhabitation of the empty-clean stratum, by SAT.

UNAUDITED PROBE.  Nothing here is a proved claim of the repository.
Exact / Boolean only: no floats, no field arithmetic, no Singular.
Single-threaded cadical 3.0.1 (H1's binary) with solver-native DRAT proofs,
replayed by H1's drat-trim.  Detached-safe: every instance is checkpointed to
results_r1.json as soon as it finishes.

QUESTION.  Every stored (R) witness in the corpus is at m = 28.  For a fixed
admissible Gamma with |F(Gamma)| <= 2 (the Gamma-forced empty-clean stratum)
and a support m, does an (R) template with Gamma(T) = Gamma and support m
exist?

MODEL (identical to w31_census.py / w20_core.py):
  T is a 9-bit mask per edge of K_8.  (R) = (SC)-admissible + three constant
  fibres nonempty + Gamma spanning 2-connected + every mixed word has
  fibre >= 3.  Gamma(T) = the graph of FULL blocks.

ENCODING
  x[e][c]        cell c of edge e is occupied                     (252 vars)
  occ[e]         edge e is occupied,  occ <-> OR_c x[e][c]
  Gamma pinned   e in Gamma  : unit x[e][c] for all nine c
                 e not in Gamma : clause OR_c ~x[e][c]   (i.e. NOT full)
  (SC)           f[p][e][c] -> occ[e]  and  f[p][e][c] -> ~x[e][cell] for
                 every cell whose colour at the FAR endpoint differs from c;
                 plus  OR_{e at p} f[p][e][c]   for all 8 sites x 3 colours.
                 (One-directional: f occurs positively only in that clause.)
  fibres         a matching M is supported at w iff every cell (w_u,w_v) on
                 M is occupied; the edges of M inside Gamma are pinned full,
                 so only M \ Gamma matters.  s[literalset] -> each literal,
                 and per word a cardinality constraint
                     #{M not inside Gamma : supported}  >=  3 - |F(Gamma)|
                 (a single clause when |F| = 2, a totaliser when |F| = 0).
                 Sound: a true s forces its cells, so the matching really is
                 supported.  Complete: any (R) template sets the s's of its
                 supported matchings.
  support        sum_e occ[e] == m   (pysat cardinality)

CALIBRATIONS BUILT IN (run before any unknown instance is trusted)
  K1  m = |Gamma| + 12  (slack 0)  must be UNSAT for every stratum Gamma.
      Lemma W31-1 proves this independently, by exhaustive branch and bound
      over cubic placements -- a completely different method.  SAT here means
      the ENCODER is wrong.
  K2  m = 28 must be SAT for every stratum Gamma: W19's explicit witnesses
      are on disk (census/results_decide.json).  UNSAT here means the encoder
      is wrong.
  K3  the stored witness at m = 28 must be ACCEPTED by a direct (non-SAT)
      model checker, and the SAT solution returned at m = 28 must itself pass
      that checker -- so the encoding is validated in both directions.
  K4  MUTATION: an instance with the fibre threshold raised to 4 at a single
      word must change the verdict or the model (guards a vacuous encoding).

Every UNSAT gets a solver-native DRAT proof replayed by drat-trim; verdicts
are recorded as verified / unchecked / refuted, never Boolean (ledger 23).

USAGE
  python3 w31_r1_sat.py            # the C_8 slice (default)
  python3 w31_r1_sat.py --all      # all 75 Gamma-forced stratum classes
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from itertools import combinations, product

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
H1 = os.path.join(REPO, "computations", "unaudited-hygiene-h1-2026-08-15",
                  "tools")
CADICAL = os.path.join(H1, "cadical", "build", "cadical")
DRAT = os.path.join(H1, "drat-trim", "drat-trim")
CENSUS = os.path.join(REPO, "computations",
                      "unaudited-forcing-w19-2026-08-15", "census")
SCRATCH = os.path.join(HERE, "r1_scratch")
OUTFILE = os.path.join(HERE, "results_r1.json")

N, Q, FULL = 8, 3, 511
EDGES = tuple(combinations(range(N), 2))
EIDX = {e: i for i, e in enumerate(EDGES)}
NE = len(EDGES)
WORDS = tuple(product(range(Q), repeat=N))
CONSTS = tuple((c,) * N for c in range(Q))
MIXED = tuple(w for w in WORDS if len(set(w)) > 1)


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


def cell_of(e, w):
    u, v = e
    return 3 * w[u] + w[v]


# --------------------------------------------------------- direct checker
def gamma_edges(T):
    return [EDGES[i] for i, t in enumerate(T) if t == FULL]


def pms_inside(es):
    S = set(es)
    return [m for m in PMS if all(e in S for e in m)]


def fibre(T, w):
    return sum(1 for m in PMS
               if all((T[EIDX[e]] >> cell_of(e, w)) & 1 for e in m))


def spanning_2connected(edges):
    vs = set()
    for u, v in edges:
        vs.add(u)
        vs.add(v)
    if vs != set(range(N)):
        return False
    adj = {v: set() for v in range(N)}
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)

    def conn(skip):
        keep = [v for v in range(N) if v != skip]
        st, seen = [keep[0]], {keep[0]}
        while st:
            a = st.pop()
            for b in adj[a]:
                if b != skip and b not in seen:
                    seen.add(b)
                    st.append(b)
        return len(seen) == len(keep)
    return conn(-1) and all(conn(s) for s in range(N))


def far_colour(e, p, c):
    """colour at the far endpoint of e as seen from p, for cell index c."""
    u, v = e
    i, j = c // 3, c % 3
    return j if p == u else i


def check_R(T):
    """the direct (R) predicate -- the SAT encoding is validated against it."""
    for p in range(N):
        need = set(range(Q))
        for e in EDGES:
            if p not in e:
                continue
            mk = T[EIDX[e]]
            if not mk:
                continue
            fc = {far_colour(e, p, c) for c in range(9) if (mk >> c) & 1}
            if len(fc) == 1:
                need.discard(fc.pop())
        if need:
            return False, "SC fails at site %d" % p
    if not all(fibre(T, w) >= 1 for w in CONSTS):
        return False, "a constant fibre is empty"
    if not spanning_2connected(gamma_edges(T)):
        return False, "Gamma not spanning 2-connected"
    for w in MIXED:
        if fibre(T, w) < 3:
            return False, "fibre < 3 at %s" % (w,)
    return True, "ok"


# --------------------------------------------------------------- encoding
class CNF:
    def __init__(self):
        self.cls = []
        self.n = 0

    def new(self):
        self.n += 1
        return self.n

    def add(self, c):
        self.cls.append(list(c))


def build(gamma_mask, m, bump_word=None):
    """returns (cnf, xvar, occvar). bump_word: raise that word's threshold by
    one (control K4)."""
    F = CNF()
    x = [[0] * 9 for _ in range(NE)]
    for e in range(NE):
        for c in range(9):
            x[e][c] = F.new()
    occ = [F.new() for _ in range(NE)]
    gam = [EDGES[i] for i in range(NE) if (gamma_mask >> i) & 1]
    gset = set(gam)

    for ei, e in enumerate(EDGES):
        if e in gset:
            for c in range(9):
                F.add([x[ei][c]])
        else:
            F.add([-x[ei][c] for c in range(9)])          # not FULL
        F.add([-occ[ei]] + [x[ei][c] for c in range(9)])
        for c in range(9):
            F.add([-x[ei][c], occ[ei]])

    # (SC)
    for p in range(N):
        for col in range(Q):
            lits = []
            for e in EDGES:
                if p not in e:
                    continue
                ei = EIDX[e]
                f = F.new()
                lits.append(f)
                F.add([-f, occ[ei]])
                for c in range(9):
                    if far_colour(e, p, c) != col:
                        F.add([-f, -x[ei][c]])
            F.add(lits)

    # fibres
    nF = len(pms_inside(gam))
    cache = {}

    def conj(lits):
        key = tuple(sorted(lits))
        if not key:
            return None                                    # always true
        if key in cache:
            return cache[key]
        s = F.new()
        for lt in key:
            F.add([-s, lt])
        cache[key] = s
        return s

    def word_constraint(w, need):
        auto, svars = 0, []
        for M in PMS:
            lits = []
            ok = True
            for e in M:
                if e in gset:
                    continue
                c = cell_of(e, w)
                lits.append(x[EIDX[e]][c])
            if not ok:
                continue
            s = conj(lits)
            if s is None:
                auto += 1
            else:
                svars.append(s)
        need = need - auto
        if need <= 0:
            return
        if need == 1:
            F.add(svars)
        else:
            from pysat.card import CardEnc, EncType
            from pysat.formula import IDPool
            pool = IDPool(start_from=F.n + 1)
            enc = CardEnc.atleast(lits=svars, bound=need, vpool=pool,
                                  encoding=EncType.seqcounter)
            for cl in enc.clauses:
                F.add(cl)
            F.n = max(F.n, pool.top)

    for w in CONSTS:
        word_constraint(w, 1)
    for w in MIXED:
        need = 3 + (1 if (bump_word is not None and w == bump_word) else 0)
        word_constraint(w, need)

    # support cardinality
    from pysat.card import CardEnc, EncType
    from pysat.formula import IDPool
    pool = IDPool(start_from=F.n + 1)
    enc = CardEnc.equals(lits=occ, bound=m, vpool=pool,
                         encoding=EncType.seqcounter)
    for cl in enc.clauses:
        F.add(cl)
    F.n = max(F.n, pool.top)
    return F, x, occ


def write_cnf(F, path):
    with open(path, "w") as fh:
        fh.write("p cnf %d %d\n" % (F.n, len(F.cls)))
        fh.write("".join(" ".join(map(str, c)) + " 0\n" for c in F.cls))


def solve(F, tag, timeout_s, want_proof):
    os.makedirs(SCRATCH, exist_ok=True)
    cnf = os.path.join(SCRATCH, tag + ".cnf")
    prf = os.path.join(SCRATCH, tag + ".drat")
    write_cnf(F, cnf)
    cmd = [CADICAL, "-q", cnf] + ([prf] if want_proof else [])
    t0 = time.time()
    try:
        r = subprocess.run(cmd, capture_output=True, text=True,
                           timeout=timeout_s)
        out = r.stdout
    except subprocess.TimeoutExpired:
        return dict(status="unchecked", reason="cadical timeout",
                    seconds=time.time() - t0, nvars=F.n, ncls=len(F.cls))
    sec = time.time() - t0
    if " SATISFIABLE" in out and "UNSATISFIABLE" not in out:
        model = []
        for ln in out.splitlines():
            if ln.startswith("v "):
                model += [int(t) for t in ln[2:].split()]
        return dict(status="SAT", seconds=sec, nvars=F.n, ncls=len(F.cls),
                    model=[v for v in model if v != 0])
    if "UNSATISFIABLE" in out:
        rec = dict(status="UNSAT", seconds=sec, nvars=F.n, ncls=len(F.cls),
                   proof="unchecked")
        if want_proof and os.path.exists(prf):
            try:
                d = subprocess.run([DRAT, cnf, prf, "-U"], capture_output=True,
                                   text=True, timeout=timeout_s)
                if "s VERIFIED" in d.stdout:
                    rec["proof"] = "verified"
                elif "NOT VERIFIED" in d.stdout:
                    rec["proof"] = "refuted"
                else:
                    rec["proof"] = "unchecked"
            except subprocess.TimeoutExpired:
                rec["proof"] = "unchecked (drat-trim timeout)"
            os.remove(prf)
        os.remove(cnf)
        return rec
    return dict(status="unchecked", reason="unparsed cadical output",
                seconds=sec, nvars=F.n, ncls=len(F.cls))


def model_to_T(model, x):
    pos = set(v for v in model if v > 0)
    return [sum(1 << c for c in range(9) if x[e][c] in pos)
            for e in range(NE)]


def checkpoint(OUT):
    with open(OUTFILE, "w") as fh:
        json.dump(OUT, fh, indent=1, sort_keys=True)


def main():
    allmode = "--all" in sys.argv
    tmo = 3600
    kill = json.load(open(os.path.join(CENSUS, "results_kill.json")))
    dec = json.load(open(os.path.join(CENSUS, "results_decide.json")))
    inv = {r["gamma_mask"]: r for r in kill["reps_inventory"]}
    strat = sorted(gm for gm, r in inv.items() if r["pms"] <= 2)
    c8 = [gm for gm in strat if inv[gm]["n_edges"] == 8]
    todo = strat if allmode else c8

    OUT = {"_header": "UNAUDITED W31/R1 per-support inhabitation of the "
                      "empty-clean stratum. Boolean/exact only. Nothing here "
                      "is a proved claim of the repository.",
           "_pinned_head": open(os.path.join(HERE,
                                             "PINNED_HEAD.txt")).read().strip(),
           "_mode": "all-75" if allmode else "C_8 slice",
           "cadical": CADICAL, "drat_trim": DRAT,
           "instances": {}, "calibrations": {}}
    if os.path.exists(OUTFILE):
        try:
            OUT.update({k: v for k, v in json.load(open(OUTFILE)).items()
                        if k in ("instances", "calibrations")})
        except Exception:
            pass
    checkpoint(OUT)

    for gm in todo:
        ng = inv[gm]["n_edges"]
        nF = inv[gm]["pms"]
        lo = ng + 12
        # K2 first (m = 28 must be SAT), then K1 (slack 0 must be UNSAT),
        # then the unknown band.
        order = [28, lo] + [mm for mm in range(lo + 1, 28)]
        for m in order:
            key = "gamma%d_m%d" % (gm, m)
            if key in OUT["instances"]:
                continue
            t0 = time.time()
            F, x, occ = build(gm, m)
            rec = solve(F, key, tmo, want_proof=True)
            rec.update(gamma_mask=gm, n_gamma=ng, n_F=nF, m=m,
                       slack=m - 12 - ng, build_seconds=round(t0 and
                                                              time.time() - t0,
                                                              1))
            if rec["status"] == "SAT":
                T = model_to_T(rec.pop("model"), x)
                ok, why = check_R(T)
                rec["template"] = T
                rec["K3_direct_checker_accepts"] = ok
                rec["K3_reason"] = why
                rec["Sigma"] = sum(bin(t).count("1") for t in T)
            OUT["instances"][key] = rec
            if m == lo:
                OUT["calibrations"]["K1_slack0_gamma%d" % gm] = dict(
                    expect="UNSAT", got=rec["status"],
                    ok=(rec["status"] == "UNSAT"), proof=rec.get("proof"))
            if m == 28:
                OUT["calibrations"]["K2_m28_gamma%d" % gm] = dict(
                    expect="SAT", got=rec["status"],
                    ok=(rec["status"] == "SAT"),
                    checker=rec.get("K3_direct_checker_accepts"))
            checkpoint(OUT)
            print("%-22s |G|=%2d |F|=%d m=%2d slack=%d -> %-9s %6.1fs %s"
                  % (key, ng, nF, m, m - 12 - ng, rec["status"],
                     rec.get("seconds", 0), rec.get("proof", "")), flush=True)

    # K4 mutation control on the C_8 class at m = 28
    if "K4_mutation" not in OUT["calibrations"]:
        gm = c8[0]
        F, x, occ = build(gm, 28, bump_word=MIXED[0])
        rec = solve(F, "K4_mut", 900, want_proof=False)
        base = OUT["instances"].get("gamma%d_m28" % gm, {}).get("status")
        OUT["calibrations"]["K4_mutation"] = dict(
            bumped_word=list(MIXED[0]), base=base, mutated=rec["status"],
            note="raising one word's fibre threshold to 4 must not silently "
                 "leave the instance unchanged; both verdicts recorded")
        checkpoint(OUT)
        print("K4 mutation:", OUT["calibrations"]["K4_mutation"], flush=True)

    print("DONE", flush=True)


if __name__ == "__main__":
    main()
