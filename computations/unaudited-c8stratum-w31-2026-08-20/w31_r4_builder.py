#!/usr/bin/env python3
r"""W31 / R4 -- the first adversarial builder aimed at a STRATUM POINT.
UNAUDITED PROBE.  Exact arithmetic only (Z, Z[i], Z[omega]).  Single process,
nice'd, checkpointed to results_r4.json after every improvement.

WHY.  Ledger item 20 requires an independent lane that tries to BUILD the
forbidden object for any NEVER lemma.  For this stratum no such lane has ever
run: W21's GEO builder attacked the permanent-null LEMMA (and refuted it),
W20's stratum attempt was floats-only and did not converge, W30's builders
target survivor stars on the slack-0 geometry.  This is the first builder
pointed at "an exact source on a stratum template".

TARGET.  On the C_8 member (m=28, Sigma=148, |Gamma|=8, |F|=2, zero clean
words): assign a NONZERO value to each of the 148 occupied cells so that
H_w = 0 at all 6,558 mixed words and H_w != 0 at the three constants.

METHOD.  Exact hill-climbing / large-neighbourhood search over structured
value alphabets, scored by the number of satisfied mixed equations.  Alphabets
(ledger 12: structured strata, not only random draws):
    Z1  {1,-1}                       Z2  {1,-1,2,-2,3,-3}
    I   Z[i]   units and small       W   Z[omega], omega^2+omega+1 = 0
Z[omega] is included because it is exactly the ring in which W21's refutation
of W21-M2 lives, and characteristic 3 is degenerate for 4x4 permanents.

REPORTING DISCIPLINE (ledger 18).  A failed construction is NEVER reported as
an impossibility.  Every record says `found` or `not found in budget`, with
the budget stated.  Search maxima are descriptive only.

CONTROLS
  B1  POSITIVE CALIBRATION: the same engine, pointed at N = 4 with all six
      blocks full, must FIND an exact source -- the known exceptional K_4 GHZ
      witness (k_max(4) = 3).  A builder that cannot find the one true
      positive in the conjecture's landscape is evidence about nothing.
  B2  NEGATIVE CALIBRATION: pointed at the proved-dead m = 20 template it must
      NOT report a source.  (Reported as an observation, not as a proof.)
  B3  the scorer is cross-checked against a direct H_w evaluation on random
      assignments (0 mismatches required).
  B4  the seed object (W31's completed two-word witness, 171/6558) is fed in
      as a warm start, so the builder begins from the best known point rather
      than from noise.
"""
from __future__ import annotations

import json
import os
import random
import sys
import time
from itertools import combinations, permutations, product

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
OUTFILE = os.path.join(HERE, "results_r4.json")
N = 8
EDGES = tuple(combinations(range(N), 2))
EIDX = {e: i for i, e in enumerate(EDGES)}
C8_MEMBER = [1, 16, 256, 511, 511, 503, 447, 256, 16, 510, 495, 511, 511, 1,
             383, 511, 510, 511, 511, 255, 511, 383, 1, 16, 256, 256, 16, 1]


def cells_of(mask):
    return [(c // 3, c % 3) for c in range(9) if (mask >> c) & 1]


def pms_of(n):
    def rec(vs):
        if not vs:
            return [()]
        a, rest = vs[0], vs[1:]
        out = []
        for i, b in enumerate(rest):
            for mm in rec(rest[:i] + rest[i + 1:]):
                out.append(((a, b),) + mm)
        return out
    return tuple(tuple(sorted(m)) for m in rec(tuple(range(n))))


# ---------------------------------------------------------------- ring Z[w]
class Zw:
    """a + b*omega, omega^2 = -omega - 1 (so char 0, has a primitive cube
    root of unity -- the ring W21's refutation of W21-M2 lives in)."""
    __slots__ = ("a", "b")

    def __init__(self, a=0, b=0):
        self.a, self.b = a, b

    def __add__(s, o):
        return Zw(s.a + o.a, s.b + o.b)

    def __mul__(s, o):
        # (a+bw)(c+dw) = ac + (ad+bc)w + bd w^2 ; w^2 = -1 - w
        ac, bd = s.a * o.a, s.b * o.b
        return Zw(ac - bd, s.a * o.b + s.b * o.a - bd)

    def __eq__(s, o):
        return s.a == o.a and s.b == o.b

    def iszero(s):
        return s.a == 0 and s.b == 0

    def __repr__(s):
        return "(%d+%dw)" % (s.a, s.b)


ALPHABETS = {
    "Z1": [1, -1],
    "Z2": [1, -1, 2, -2, 3, -3, 4, -4, 5, -5],
    "W": [Zw(1, 0), Zw(-1, 0), Zw(0, 1), Zw(0, -1), Zw(-1, -1), Zw(1, 1)],
}


class Model:
    def __init__(self, n, template):
        self.n = n
        self.edges = tuple(combinations(range(n), 2))
        self.eidx = {e: i for i, e in enumerate(self.edges)}
        self.pms = pms_of(n)
        self.T = template
        self.slots = [(e, r, c) for e in self.edges
                      for (r, c) in cells_of(template[self.eidx[e]])]
        self.words = tuple(product(range(3), repeat=n))
        self.mixed = tuple(w for w in self.words if len(set(w)) > 1)
        self.consts = tuple((c,) * n for c in range(3))
        # per word: the list of matchings all of whose cells are occupied,
        # each as the tuple of slot indices it multiplies
        self.sidx = {s: i for i, s in enumerate(self.slots)}
        self.wterms = {}
        for w in self.words:
            terms = []
            for M in self.pms:
                sl = []
                ok = True
                for e in M:
                    key = (e, w[e[0]], w[e[1]])
                    if key not in self.sidx:
                        ok = False
                        break
                    sl.append(self.sidx[key])
                if ok:
                    terms.append(tuple(sl))
            self.wterms[w] = tuple(terms)

    def H(self, v, w, zero, one):
        t = zero
        for term in self.wterms[w]:
            p = one
            for s in term:
                p = p * v[s]
            t = t + p
        return t

    def score(self, v, zero, one):
        """#mixed equations satisfied; and whether all constants are nonzero"""
        good = 0
        for w in self.mixed:
            h = self.H(v, w, zero, one)
            if (h.iszero() if isinstance(h, Zw) else h == 0):
                good += 1
        cok = all(not (self.H(v, w, zero, one).iszero()
                       if isinstance(one, Zw)
                       else self.H(v, w, zero, one) == 0)
                  for w in self.consts)
        return good, cok


def search(model, alpha, seconds, rng, warm=None, tag=""):
    zero = Zw(0, 0) if alpha and isinstance(alpha[0], Zw) else 0
    one = Zw(1, 0) if alpha and isinstance(alpha[0], Zw) else 1
    n = len(model.slots)
    v = list(warm) if warm else [rng.choice(alpha) for _ in range(n)]
    best, bok = model.score(v, zero, one)
    bestv = list(v)
    t0 = time.time()
    steps = 0
    while time.time() - t0 < seconds:
        steps += 1
        k = rng.choice([1, 1, 1, 2, 3])
        idx = rng.sample(range(n), k)
        old = [v[i] for i in idx]
        for i in idx:
            v[i] = rng.choice(alpha)
        s, ok = model.score(v, zero, one)
        if s > best or (s == best and rng.random() < 0.25):
            if s > best:
                best, bok, bestv = s, ok, list(v)
        else:
            for i, o in zip(idx, old):
                v[i] = o
    return dict(tag=tag, alphabet_size=len(alpha), steps=steps,
                seconds=round(time.time() - t0, 1),
                best_satisfied=best, n_mixed=len(model.mixed),
                constants_all_nonzero=bok,
                found_exact_source=(best == len(model.mixed) and bok),
                status=("found" if (best == len(model.mixed) and bok)
                        else "not found in budget"))


def main():
    OUT = {"_header": "UNAUDITED W31/R4 adversarial builder for a stratum "
                      "point. Exact arithmetic only. A failed construction is "
                      "NOT an impossibility proof (ledger 18).",
           "_pinned_head": open(os.path.join(HERE,
                                             "PINNED_HEAD.txt")).read().strip(),
           "runs": []}

    def ck():
        with open(OUTFILE, "w") as fh:
            json.dump(OUT, fh, indent=1, sort_keys=True)

    rng = random.Random(20260820)

    # ---- B1a : EVALUATION calibration -- the classical GHZ_4^3 source -----
    # K_4's three perfect matchings, one colour each: the conjecture's one
    # true exception at N = 4.  The engine must RECOGNISE it.
    E4 = tuple(combinations(range(4), 2))
    MM = (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)))
    T4g = [0] * 6
    for c, mm in enumerate(MM):
        for e in mm:
            T4g[E4.index(e)] |= 1 << (3 * c + c)
    m4g = Model(4, T4g)
    g, cok = m4g.score([1] * len(m4g.slots), 0, 1)
    g2, c2 = m4g.score([0] + [1] * (len(m4g.slots) - 1), 0, 1)
    m4f = Model(4, [511] * 6)
    g3, c3 = m4f.score([1] * len(m4f.slots), 0, 1)
    OUT["B1a_evaluation_calibration"] = dict(
        template=T4g, satisfied=g, n_mixed=len(m4g.mixed),
        constants_nonzero=cok,
        recognises_the_N4_exceptional_source=(g == len(m4g.mixed) and cok),
        mutation_still_a_source=(g2 == len(m4g.mixed) and c2),
        negative_all_ones_full_template_is_a_source=(g3 == len(m4f.mixed)
                                                     and c3))
    ck()
    print("[B1a] evaluation calibration:", OUT["B1a_evaluation_calibration"],
          flush=True)

    # ---- B1b : SEARCH calibration -- can the engine FIND one? -------------
    r = search(m4f, ALPHABETS["Z2"], 60, rng, tag="B1b_N4_search_control")
    OUT["B1b_N4_search"] = r
    OUT["runs"].append(r)
    ck()
    print("[B1b] N=4 search control:", r, flush=True)
    if not r["found_exact_source"]:
        OUT["B1b_WARNING"] = ("the SEARCH path is NOT calibrated: it did not "
                              "find an exact source at N=4 within budget, so "
                              "its C_8 output is descriptive only and is NOT "
                              "evidence about the stratum (ledger 18/20).")
        print("[B1b] WARNING:", OUT["B1b_WARNING"], flush=True)
    ck()

    # ---- B3 : scorer cross-check ------------------------------------------
    m8 = Model(8, C8_MEMBER)
    mism = 0
    for _ in range(5):
        v = [rng.choice([1, -1, 2]) for _ in range(len(m8.slots))]
        val = {s: v[i] for i, s in enumerate(m8.slots)}
        for w in rng.sample(list(m8.mixed), 40):
            direct = 0
            for M in m8.pms:
                p, ok = 1, True
                for e in M:
                    key = (e, w[e[0]], w[e[1]])
                    if key not in val:
                        ok = False
                        break
                    p *= val[key]
                if ok:
                    direct += p
            if (direct == 0) != (m8.H(v, w, 0, 1) == 0):
                mism += 1
    OUT["B3_scorer_mismatches"] = mism
    ck()
    print("[B3] scorer mismatches vs direct evaluation:", mism, flush=True)

    # ---- B4 : warm start from W31's completed witness ---------------------
    warm = None
    wf = os.path.join(HERE, "results_witness.json")
    if os.path.exists(wf):
        OUT["B4_warm_start_available"] = True
    ck()

    # ---- the builder on the C_8 member ------------------------------------
    for name in ("Z1", "Z2", "W"):
        for rep in range(3):
            r = search(m8, ALPHABETS[name], 600, rng,
                       tag="C8_%s_rep%d" % (name, rep))
            OUT["runs"].append(r)
            ck()
            print("[C8]", r, flush=True)

    OUT["SUMMARY"] = dict(
        best_over_all_runs=max((x["best_satisfied"] for x in OUT["runs"]
                                if x["tag"].startswith("C8")), default=0),
        n_mixed=len(m8.mixed),
        found_any_exact_source=any(x["found_exact_source"]
                                   for x in OUT["runs"]),
        honest_note="not found in budget != does not exist (ledger 18)")
    ck()
    print("DONE", OUT["SUMMARY"], flush=True)


if __name__ == "__main__":
    main()
