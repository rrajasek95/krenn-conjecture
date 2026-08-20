#!/usr/bin/env python3
"""House checker for the gated delivery lemmas of Section 5
(dependency ID ROUTE-A-RESIDUAL, record SUPERSESSION-2026-08-20-04).

    computations/verify_delivery_lemmas.py

STANDARD LIBRARY ONLY.  No import from any `computations/unaudited-*`
directory and no import of any lane module.  The nine 28-entry template masks
are EMBEDDED (combinatorial data); every derived structural fact is rebuilt
from them and matched against the recorded census.  Steps that need a point
corpus READ it as DATA and are optional-but-loud.

House style: every check goes through the raising `require()`.  There is no
bare `assert` in this file, so the checker is equally strict under
`python3 -O`.

LEDGER 21 / LEDGER 31 DISCIPLINE.  A result block's `ok` field is written
ONLY by the function that actually executed the control: `Report.record()` is
the sole writer of `ok`, and it appends to `_controls_run` in the same call.
The run ends by asserting declared == run, and by re-scanning every emitted
block for an `ok` field whose control is not in `_controls_run`.  Ledger 31
exists because five upstream result files carried `ok: true` with
`_controls_run: []`; this checker cannot do that.

WHAT IS CHECKED

  STEP 1  structure         m=25/R6 template facts rebuilt from the masks:
                            N(6) = {5,7}, the live singles, the firing
                            letters, |T_f| histogram, T_c never empty.
  STEP 2  pigeonhole        branch (R25), EXHAUSTIVELY at n = 2: over every
                            all-nonzero 3x2 matrix over F_13, the two
                            overlapping clean pairs never both fail.
  STEP 3  rank chain        branch (alpha)+(beta), the n = 2 rank step,
                            exhaustively; plus its non-vacuity control.
  STEP 4  n=3 no-go         the same pigeonhole FAILS at n = 3 -- the
                            structural reason m=26/27 keep (Q3).
  STEP 5  W30-Z             the (Z2)-hypothesised implication, synthetic,
                            random n in {2,3,4} over F_31.
  STEP 6  MUT-Z2            dropping (Z2) must make the implication FALSE.
                            The checker FAILS if no counterexample is found.
  STEP 7  coverage          (R25) / (alpha) / (beta) / delivery at the STORED
                            m=25 corpora, with the unstored parts of A11's
                            32-point corpus excluded LOUDLY, never
                            interpolated.
  STEP 8  calibration       the two objects A11 names by name -- the
                            (R25)-failing Q point seed 925024 and the
                            (beta)-escape object s1073 -- must reproduce
                            A11's recorded flags exactly.

Steps 1-6 are mandatory.  Steps 7 and 8 need the stored point corpus: they
run when it is found and print a labelled SKIPPED line otherwise;
`--strict` makes them mandatory.

STEP 8 is not decoration.  (R25) retains W36's |T_f| = 1 condition, and
dropping it -- which A11's correction (ii) can be misread as licensing --
makes (R25) hold at seed 925024, where A11 records it FAILING.  That error
would erase the very asymmetry that makes the promotion object a
disjunction.  It was made while writing this checker and caught by STEP 8.

Exit code 0 iff every mandatory step passes.

UNAUDITED STAGING -- nothing verified here is a proved claim of the
repository.  See computations/unaudited-promotion-p3-2026-08-20/.
"""

import argparse
import json
import os
import random
import sys
import time
from fractions import Fraction
from itertools import combinations, product


# --------------------------------------------------------------- house style
class CheckerError(Exception):
    """Raised by require(); never caught inside a step."""


def require(cond, msg):
    if not cond:
        raise CheckerError(msg)
    return True


class Report(object):
    """The ONLY writer of `ok`.  Ledger 21/31 guard."""

    def __init__(self, declared):
        self.d = {"_header": "UNAUDITED house checker -- ROUTE-A-RESIDUAL "
                             "section 5 (lane P3)",
                  "_controls_declared": list(declared),
                  "_controls_run": []}

    def record(self, name, **fields):
        require(name in self.d["_controls_declared"],
                "control %r was recorded but never declared" % name)
        require(name not in self.d["_controls_run"],
                "control %r was recorded twice" % name)
        require("ok" not in fields,
                "record() is the sole writer of `ok`; caller passed one")
        blk = dict(fields)
        blk["ok"] = True
        self.d[name] = blk
        self.d["_controls_run"].append(name)
        return blk

    def skip(self, name, reason):
        require(name in self.d["_controls_declared"],
                "control %r was skipped but never declared" % name)
        self.d[name] = {"SKIPPED": True, "reason": reason}
        return self.d[name]

    def finish(self, mandatory):
        run = set(self.d["_controls_run"])
        for name in mandatory:
            require(name in run,
                    "mandatory control %r did not run" % name)
        for k, v in self.d.items():
            if k.startswith("_") or not isinstance(v, dict):
                continue
            if "ok" in v:
                require(k in run,
                        "block %r carries `ok` but is not in _controls_run "
                        "(ledger 31)" % k)
        self.d["_manifest_ok"] = True
        self.d["_manifest_missing"] = sorted(
            set(self.d["_controls_declared"]) - run)
        return self.d


# ------------------------------------------------------------------ the model
NV = 8
QQ = 3
FULL = 511

EDG = tuple(combinations(range(NV), 2))
LSIDE = (0, 1, 2, 3)
RSIDE = (4, 5, 6, 7)
SG = {0: 7, 1: 4, 2: 5, 3: 6}

TMPL = {
    25: (511, 511, 511, 1, 2, 4, 511, 511, 511, 511, 8, 16, 4, 511,
         8, 511, 128, 32, 64, 128, 0, 256, 511, 0, 511, 511, 0, 511),
    26: (511, 511, 511, 1, 2, 4, 511, 511, 511, 511, 8, 16, 4, 511,
         8, 511, 128, 32, 64, 128, 511, 256, 511, 0, 511, 511, 0, 511),
    27: (511, 511, 511, 1, 2, 4, 511, 511, 511, 511, 8, 16, 4, 511,
         8, 511, 128, 32, 64, 128, 511, 256, 511, 511, 511, 511, 0, 511),
    28: (511, 511, 511, 1, 2, 4, 511, 511, 511, 511, 8, 16, 4, 511,
         8, 511, 128, 32, 64, 128, 511, 256, 511, 511, 511, 511, 511, 511),
}


def _perfect_matchings(vs):
    if not vs:
        return [()]
    a = vs[0]
    out = []
    for i in range(1, len(vs)):
        b = vs[i]
        e = (a, b) if a < b else (b, a)
        for rest in _perfect_matchings(vs[1:i] + vs[i + 1:]):
            out.append((e,) + rest)
    return out


PM105 = tuple(_perfect_matchings(tuple(range(NV))))
WORDS = tuple(product(range(QQ), repeat=NV))
MIXED = tuple(w for w in WORDS if len(set(w)) > 1)


class Struct(object):
    def __init__(self, m):
        T = TMPL[m]
        require(len(T) == len(EDG), "template %d has wrong length" % m)
        self.m = m
        self.gamma = tuple(e for e, t in zip(EDG, T) if t == FULL)
        self.gs = set(self.gamma)
        self.single = {}
        for e, t in zip(EDG, T):
            if t in (0, FULL):
                continue
            bits = [c for c in range(9) if (t >> c) & 1]
            require(len(bits) == 1,
                    "edge %s of template %d is not a single-cell mask"
                    % (e, m))
            self.single[e] = (bits[0] // 3, bits[0] % 3)
        self.absent = tuple(e for e, t in zip(EDG, T) if t == 0)
        self.live = tuple(sorted(
            e for e in self.single
            if self._has_pm(tuple(v for v in range(NV) if v not in e))))
        self.clean = tuple(w for w in MIXED if not self.active_live(w))
        self.gamma_pms = tuple(M for M in PM105 if all(e in self.gs for e in M))
        self.nbrs = {}
        for v in range(NV):
            self.nbrs[v] = tuple(s for s in range(NV)
                                 if (min(s, v), max(s, v)) in self.gs)

    def _has_pm(self, vs):
        if not vs:
            return True
        a = vs[0]
        for i in range(1, len(vs)):
            b = vs[i]
            e = (a, b) if a < b else (b, a)
            if e in self.gs and self._has_pm(vs[1:i] + vs[i + 1:]):
                return True
        return False

    def active_live(self, w):
        return tuple(e for e in self.live
                     if (w[e[0]], w[e[1]]) == self.single[e])


_S = {}


def S(m):
    if m not in _S:
        _S[m] = Struct(m)
    return _S[m]


# ------------------------------------------------------------------ the field
class Fp(object):
    def __init__(self, p):
        self.p = p
        self.name = "F_%d" % p
        self.zero = 0
        self.one = 1

    def z(self, a):
        return int(a) % self.p

    def add(self, a, b):
        return (a + b) % self.p

    def sub(self, a, b):
        return (a - b) % self.p

    def mul(self, a, b):
        return (a * b) % self.p

    def isz(self, a):
        return a % self.p == 0

    def inv(self, a):
        return pow(a, self.p - 2, self.p)


class Rat(object):
    def __init__(self):
        self.name = "Q"
        self.zero = Fraction(0)
        self.one = Fraction(1)

    def z(self, a):
        return Fraction(a)

    def add(self, a, b):
        return a + b

    def sub(self, a, b):
        return a - b

    def mul(self, a, b):
        return a * b

    def isz(self, a):
        return a == 0

    def inv(self, a):
        return 1 / a


def rank(rows, K):
    mat = [list(r) for r in rows]
    nr = len(mat)
    if nr == 0:
        return 0
    nc = len(mat[0])
    r = 0
    for c in range(nc):
        piv = None
        for i in range(r, nr):
            if not K.isz(mat[i][c]):
                piv = i
                break
        if piv is None:
            continue
        mat[r], mat[piv] = mat[piv], mat[r]
        iv = K.inv(mat[r][c])
        mat[r] = [K.mul(x, iv) for x in mat[r]]
        for i in range(nr):
            if i != r and not K.isz(mat[i][c]):
                f = mat[i][c]
                mat[i] = [K.sub(mat[i][j], K.mul(f, mat[r][j]))
                          for j in range(nc)]
        r += 1
        if r == nr:
            break
    return r


def in_span(vecs, x, K):
    """Is x in the span of vecs?"""
    base = rank(vecs, K)
    return rank(list(vecs) + [list(x)], K) == base


# ------------------------------------------------------------------ Phi, S', Q
def cell(bl, gs, u, v, a, b, K):
    e = (u, v) if u < v else (v, u)
    if e not in gs:
        return K.zero
    if u < v:
        return bl[e][a][b]
    return bl[e][b][a]


def phi_raw(m, bl, w, K):
    st = S(m)
    tot = K.zero
    for M in st.gamma_pms:
        pr = K.one
        for (a, b) in M:
            pr = K.mul(pr, bl[(a, b)][w[a]][w[b]])
            if K.isz(pr):
                break
        tot = K.add(tot, pr)
    return tot


def hafL_at(m, bl, w, K):
    st = S(m)

    def c(u, v, a, b):
        return cell(bl, st.gs, u, v, a, b, K)
    ll = {}
    for i, j in combinations(LSIDE, 2):
        ll[(i, j)] = c(i, j, w[i], w[j])
    return K.add(K.add(K.mul(ll[(0, 1)], ll[(2, 3)]),
                       K.mul(ll[(0, 2)], ll[(1, 3)])),
                 K.mul(ll[(0, 3)], ll[(1, 2)]))


def Sprime(m, bl, v, tau, ns, K):
    st = S(m)
    return [[cell(bl, st.gs, v, s, t, tau[j], K)
             for j, s in enumerate(ns)] for t in range(QQ)]


def Qvec(m, bl, v, w, ns, K):
    st = S(m)
    out = []
    for s in ns:
        rest = tuple(z for z in range(NV) if z not in (v, s))
        tot = K.zero
        for M in _perfect_matchings(rest):
            pr = K.one
            for (a, b) in M:
                e = (a, b) if a < b else (b, a)
                if e not in st.gs:
                    pr = K.zero
                    break
                pr = K.mul(pr, bl[e][w[e[0]]][w[e[1]]])
                if K.isz(pr):
                    break
            tot = K.add(tot, pr)
        out.append(tot)
    return out


# --------------------------------------------------- singles and admissibility
def singles_at(m, v):
    """[(edge, trigger-coordinate, trigger-value, letter-at-v)] over LIVE
    singles incident to v."""
    st = S(m)
    out = []
    for e in st.live:
        if v not in e:
            continue
        a, b = st.single[e]
        if v == e[1]:
            out.append((e, e[0], a, b))
        else:
            out.append((e, e[1], b, a))
    return out


def admissible(m, v):
    """W26's and W30's STRICT filter, ported.  Returns
    [(word-with-v=0, T_f, T_c)]."""
    st = S(m)
    mine = singles_at(m, v)
    others = [c for c in range(NV) if c != v]
    out = []
    for vals in product(range(QQ), repeat=NV - 1):
        w = [0] * NV
        for c, a in zip(others, vals):
            w[c] = a
        fire = set()
        for (e, trig, tv, letter) in mine:
            if w[trig] == tv:
                fire.add(letter)
        if not fire:
            continue
        Tc, Tf, ok = [], [], True
        for t in range(QQ):
            ww = list(w)
            ww[v] = t
            const = len(set(ww)) == 1
            act = st.active_live(tuple(ww))
            if t not in fire:
                if (not const) and (not act):
                    Tc.append(t)
                else:
                    ok = False
                    break
            else:
                if (not const) and all(e[1] == v for e in act):
                    Tf.append(t)
                else:
                    ok = False
                    break
        if not ok or not Tf:
            continue
        out.append((tuple(w), tuple(sorted(Tf)), tuple(sorted(Tc))))
    return out


_ADM = {}


def adm(m, v):
    if (m, v) not in _ADM:
        _ADM[(m, v)] = admissible(m, v)
    return _ADM[(m, v)]


# ---------------------------------------------------------- the n=2 machinery
def _ratio_table(p):
    """Every all-nonzero row of K^2, and its projective class."""
    rows = []
    for a in range(1, p):
        for b in range(1, p):
            rows.append((a, b, (a * pow(b, p - 2, p)) % p))
    return rows


def _exhaustive_n2(p):
    """One enumeration pass over all all-nonzero 3x2 matrices over F_p.

    Collects, in a single sweep, the statistics behind STEP 2 and STEP 3.
    Rows are indexed by letter t in {0,1,2}; the firing letters at m=25/R6
    are {1,2}, so the two overlapping clean pairs are {0,2} (firing 1) and
    {0,1} (firing 2), sharing letter 0.
    """
    rows = _ratio_table(p)
    n = len(rows)
    both = 0
    hist = {}
    n_rank_le1 = 0
    n_rank_le1_all_in_span = 0
    n_rank2 = 0
    n_rank2_with_failing_pair = 0
    for r0 in range(n):
        c0 = rows[r0][2]
        for r1 in range(n):
            c1 = rows[r1][2]
            for r2 in range(n):
                c2 = rows[r2][2]
                # branch (R25): can both overlapping clean pairs fail?
                f1 = (c0 == c2) and (c1 != c0)
                f2 = (c0 == c1) and (c2 != c0)
                if f1 and f2:
                    both += 1
                k = (f1, f2)
                hist[k] = hist.get(k, 0) + 1
                # the rank chain, same sweep
                if c0 == c1 == c2:
                    n_rank_le1 += 1
                    # all rows nonzero and mutually parallel
                    if c0 == c1 and c1 == c2:
                        n_rank_le1_all_in_span += 1
                else:
                    n_rank2 += 1
                    if not (c0 == c1 and c1 == c2):
                        n_rank2_with_failing_pair += 1
    return {"matrices": n ** 3, "both_choices_fail": both,
            "outcome_hist": dict(("(%s, %s)" % k, v)
                                 for k, v in sorted(hist.items())),
            "n_rank_le1": n_rank_le1,
            "n_rank_le1_all_rows_in_span": n_rank_le1_all_in_span,
            "n_rank2": n_rank2,
            "n_rank2_with_a_failing_pair": n_rank2_with_failing_pair}


# ------------------------------------------------------------------ the steps
def step1_structure(rep):
    st = S(25)
    ns = st.nbrs[6]
    require(ns == (5, 7),
            "m=25: N(6) = %s, expected (5, 7)" % (ns,))
    require((3, 6) in st.absent and (4, 6) in st.absent,
            "m=25: N(6)={5,7} should follow from BOTH (3,6) and (4,6) absent")
    sing = singles_at(25, 6)
    letters = sorted(set(x[3] for x in sing))
    require(letters == [1, 2],
            "m=25/R6 firing letters %s, expected [1, 2]" % letters)
    A = adm(25, 6)
    require(len(A) == 823,
            "m=25/R6 has %d admissible index choices, expected 823" % len(A))
    tf_hist = {}
    tc_empty = 0
    for (_w, Tf, Tc) in A:
        tf_hist[len(Tf)] = tf_hist.get(len(Tf), 0) + 1
        if not Tc:
            tc_empty += 1
    require(tf_hist == {1: 671, 2: 152},
            "|T_f| histogram %s, expected {1: 671, 2: 152}" % tf_hist)
    require(tc_empty == 0,
            "T_c was empty at %d admissible choices; the template fact that "
            "letter 0 is no live single's target has failed" % tc_empty)
    never_fires = sorted(set(range(QQ)) - set(letters))
    require(never_fires == [0],
            "expected letter 0 to be the target of no live single, got %s"
            % never_fires)
    rep.record("S1_template_facts",
               N6=list(ns), absent_at_site6=[list((3, 6)), list((4, 6))],
               live_singles_into_R6=[[str(e), t, tv, lt]
                                     for (e, t, tv, lt) in sing],
               firing_letters=letters, n_admissible=len(A),
               Tf_size_hist=dict((str(k), v) for k, v in tf_hist.items()),
               Tc_always_nonempty=True, letter_that_never_fires=0,
               note="rebuilt from the 28-entry masks alone")
    return ("STEP 1  structure      N(6)={5,7}, 823 admissible, "
            "|T_f| {1:671, 2:152}, T_c never empty   PASS")


def step2_pigeonhole(rep, ex, p):
    require(ex["both_choices_fail"] == 0,
            "the pigeonhole FAILED: %d of %d all-nonzero 3x2 matrices over "
            "F_%d have both overlapping clean pairs failing"
            % (ex["both_choices_fail"], ex["matrices"], p))
    single = ex["matrices"] - ex["outcome_hist"].get("(False, False)", 0)
    require(single > 0,
            "no matrix has exactly one choice failing -- the pigeonhole test "
            "is constant-true and therefore vacuous")
    rep.record("S2_pigeonhole_n2", field="F_%d" % p,
               matrices=ex["matrices"],
               both_choices_fail=ex["both_choices_fail"],
               exactly_one_fails=single,
               outcome_hist=ex["outcome_hist"],
               note="EXHAUSTIVE over every all-nonzero 3x2 matrix; branch "
                    "(R25) of the m=25 disjunctive lemma.  No Q hypothesis "
                    "enters.")
    return ("STEP 2  pigeonhole     %d matrices EXHAUSTIVE, both-fail 0, "
            "one-fail %d   PASS" % (ex["matrices"], single))


def step3_rank_chain(rep, ex, p):
    require(ex["n_rank_le1"] == ex["n_rank_le1_all_rows_in_span"],
            "rank <= 1 did not imply every row in every other row's span "
            "(%d of %d)" % (ex["n_rank_le1_all_rows_in_span"],
                            ex["n_rank_le1"]))
    require(ex["n_rank2"] == ex["n_rank2_with_a_failing_pair"],
            "non-vacuity control: only %d of %d rank-2 matrices have a "
            "failing pair" % (ex["n_rank2_with_a_failing_pair"],
                              ex["n_rank2"]))
    require(ex["n_rank_le1"] + ex["n_rank2"] == ex["matrices"],
            "rank partition does not total the enumeration")
    rep.record("S3_rank_chain_n2", field="F_%d" % p,
               n_rank_le1=ex["n_rank_le1"],
               n_rank_le1_all_rows_in_span=ex["n_rank_le1_all_rows_in_span"],
               n_rank2=ex["n_rank2"],
               n_rank2_with_a_failing_pair=ex["n_rank2_with_a_failing_pair"],
               note="the (alpha)+(beta) branch's rank step, exhaustively: "
                    "rank <= 1 => the firing row is inside the clean span; "
                    "the control shows the rank hypothesis is load-bearing")
    return ("STEP 3  rank chain     rank<=1: %d/%d all-in-span; rank2: "
            "%d/%d have a failing pair   PASS"
            % (ex["n_rank_le1_all_rows_in_span"], ex["n_rank_le1"],
               ex["n_rank2_with_a_failing_pair"], ex["n_rank2"]))


def step4_n3_nogo(rep, rng, p, samples):
    """The same pigeonhole must FAIL at n = 3."""
    K = Fp(p)
    both = 0
    example = None
    for _ in range(samples):
        M = [[rng.randrange(1, p) for _ in range(3)] for _ in range(3)]
        f1 = not in_span([M[0], M[2]], M[1], K)
        f2 = not in_span([M[0], M[1]], M[2], K)
        if f1 and f2:
            both += 1
            if example is None:
                example = [[str(x) for x in r] for r in M]
    require(both > 0,
            "the n=3 no-go control found NO matrix with both clean pairs "
            "failing in %d samples -- if the pigeonhole also held at n=3, "
            "the structural note of section 5.3 would be false" % samples)
    frac = both / float(samples)
    require(0.85 < frac < 0.97,
            "at n=3 %.1f%% of samples have both pairs failing; A11 measured "
            "91.6%% over F_13 (183,176/200,000), so this is out of family"
            % (100 * frac))
    rep.record("S4_n3_nogo", field="F_%d" % p, samples=samples,
               both_fail=both, fraction=round(frac, 6), example=example,
               note="at |N| = 3 the slice is 3x3 and both clean pairs CAN "
                    "fail -- exactly why m=26/27 keep a Q hypothesis (Q3) "
                    "and m=25 does not")
    return ("STEP 4  n=3 no-go      %d/%d samples have BOTH pairs failing "
            "(%.1f%%)   PASS" % (both, samples, 100 * frac))


def _w30z_case(Sp, t1, t2, t3, K):
    """(delivers_i1, delivers_i2) for the two firing choices."""
    d1 = in_span([Sp[t2], Sp[t3]], Sp[t1], K)
    d2 = in_span([Sp[t1], Sp[t3]], Sp[t2], K)
    return d1, d2


def step5_w30z(rep, rng, p, trials):
    K = Fp(p)
    tested = 0
    hyp_met = 0
    viol = 0
    for _ in range(trials):
        n = rng.choice((2, 3, 4))
        Sp = [[rng.randrange(0, p) for _ in range(n)] for _ in range(QQ)]
        t3 = 0
        t1, t2 = 1, 2
        tested += 1
        if all(K.isz(x) for x in Sp[t3]):
            continue                      # (Z2) fails; excluded by hypothesis
        if rank(Sp, K) > 2:
            continue                      # (Z1) fails
        hyp_met += 1
        d1, d2 = _w30z_case(Sp, t1, t2, t3, K)
        if not (d1 or d2):
            viol += 1
    require(hyp_met > 0,
            "W30-Z's hypothesis was never met in %d trials -- the test is "
            "vacuous" % trials)
    require(viol == 0,
            "W30-Z FAILED: %d of %d hypothesis-meeting configurations "
            "delivered at neither choice" % (viol, hyp_met))
    rep.record("S5_w30z_implication", field="F_%d" % p, trials=tested,
               hypothesis_met=hyp_met, violations=viol,
               note="rank S'(tau) <= 2 AND S'[t3] != 0 => delivery at i1 or "
                    "i2; random n in {2,3,4}")
    return ("STEP 5  W30-Z          %d/%d configs meet the hypothesis, "
            "0 violations   PASS" % (hyp_met, tested))


def step6_mut_z2(rep, rng, p, trials):
    """Dropping (Z2) must make the implication FALSE."""
    K = Fp(p)
    found = 0
    witness = None
    # (a) by construction: t3 = 0 with t1, t2 independent
    for n in (2, 3, 4):
        Sp = [[0] * n for _ in range(QQ)]
        Sp[1][0] = 1
        Sp[2][1 % n] = 1
        if n == 1:
            continue
        if rank(Sp, K) <= 2:
            d1, d2 = _w30z_case(Sp, 1, 2, 0, K)
            if not (d1 or d2):
                found += 1
                if witness is None:
                    witness = {"n": n, "S_prime": [list(r) for r in Sp],
                               "rank": rank(Sp, K),
                               "S_t3_is_zero": True}
    # (b) by random search, to show it is not a hand-picked artifact
    rand_found = 0
    for _ in range(trials):
        n = rng.choice((2, 3, 4))
        Sp = [[rng.randrange(0, p) for _ in range(n)] for _ in range(QQ)]
        Sp[0] = [0] * n                    # force (Z2) to fail
        if rank(Sp, K) > 2:
            continue
        d1, d2 = _w30z_case(Sp, 1, 2, 0, K)
        if not (d1 or d2):
            rand_found += 1
    require(found > 0,
            "MUT-Z2: the constructed (Z2)-less configurations did NOT "
            "falsify the implication -- hypothesis (Z2) would then be "
            "removable, contradicting A11")
    require(rand_found > 0,
            "MUT-Z2: random search found no (Z2)-less counterexample in %d "
            "trials -- the constructed one may be an artifact" % trials)
    rep.record("S6_mut_z2", constructed_counterexamples=found,
               random_counterexamples=rand_found, trials=trials,
               witness=witness,
               note="WITHOUT S'[t3] != 0 the implication is FALSE: explicit "
                    "rank-2 slices with a zero doubly-clean row at which "
                    "neither firing row lies in its clean span.  This is the "
                    "mutation control for STEP 5 -- if it found nothing, "
                    "STEP 5 would not be testing a load-bearing hypothesis.")
    return ("STEP 6  MUT-Z2         %d constructed + %d random (Z2)-less "
            "counterexamples   PASS" % (found, rand_found))


# ------------------------------------------------------------ the corpus step
def parse_point(pt, K):
    bl = {}
    for key, mat in pt.items():
        a, b = key.strip("()").split(",")
        e = (int(a), int(b))
        bl[e] = [[K.z(Fraction(x)) for x in row] for row in mat]
    return bl


def all_cells_nonzero(m, bl, K):
    st = S(m)
    for e in st.gamma:
        for r in bl[e]:
            for x in r:
                if K.isz(x):
                    return False
    return True


def m25_R6_flags(bl, K):
    """(R25), (alpha), (beta), delivery at m=25 / R6.

    (R25) is W36's hypothesis and RETAINS the |T_f| = 1 condition: a tuple
    must carry two SURVIVING (nonzero-scale) index choices, EACH WITH
    |T_f| = 1, whose single firing letters DIFFER.  A11's correction (ii) --
    "|T_f| = 1 is not needed at m=25" -- applies to the (alpha)+(beta)
    branch, whose rank-1 argument covers the 152 choices with |T_f| = 2.  It
    does NOT loosen (R25); dropping the condition here makes (R25) hold at
    points where A11 records it failing (seed 925024 is the calibration).
    """
    m, v = 25, 6
    st = S(m)
    ns = st.nbrs[v]
    A = adm(m, v)
    unary_by_tau = {}
    live_tuples = set()
    alpha = False
    delivers = False
    for (w, Tf, Tc) in A:
        h = hafL_at(m, bl, w, K)
        if K.isz(h):
            continue                       # zero scale: skipped by convention
        alpha = True
        tau = (w[ns[0]], w[ns[1]])
        live_tuples.add(tau)
        Sp = Sprime(m, bl, v, tau, ns, K)
        ok = True
        for tf in Tf:
            if not in_span([Sp[t] for t in Tc], Sp[tf], K):
                ok = False
                break
        if ok:
            delivers = True
        if len(Tf) == 1:
            unary_by_tau.setdefault(tau, set()).add(Tf[0])
    r25_tuples = sorted(t for t, fl in unary_by_tau.items() if len(fl) >= 2)
    # (beta): at some live tuple, an untriggered word has Q != 0
    beta_tuples = []
    others = tuple(z for z in range(NV) if z != v)
    for tau in sorted(live_tuples):
        hit = False
        for assign in product(range(QQ), repeat=NV - 1):
            w = [0] * NV
            for idx, z in enumerate(others):
                w[z] = assign[idx]
            if (w[ns[0]], w[ns[1]]) != tau:
                continue
            unt = True
            for t in range(QQ):
                w[v] = t
                if not K.isz(phi_raw(m, bl, tuple(w), K)):
                    unt = False
                    break
            if not unt:
                continue
            Q = Qvec(m, bl, v, tuple(w), ns, K)
            if any(not K.isz(x) for x in Q):
                hit = True
                break
        if hit:
            beta_tuples.append(tau)
    return {"R25": bool(r25_tuples), "n_R25_tuples": len(r25_tuples),
            "alpha": alpha, "beta": bool(beta_tuples),
            "n_beta_tuples": len(beta_tuples), "delivers": delivers}


def _load_corpus(here, limit_wide, limit_hunt):
    """Stored m=25 points, as DATA.  Returns (records, sources, missing)."""
    w30 = os.path.join(here, "unaudited-exclusion-w30-2026-08-19")
    if not os.path.isdir(w30):
        w30 = os.path.join(os.path.dirname(here),
                           "unaudited-exclusion-w30-2026-08-19")
    recs = []
    srcs = []
    missing = []
    fw = os.path.join(w30, "points_m25_wide.json")
    if os.path.exists(fw):
        d = json.load(open(fw))
        pts = d.get("points", [])[:limit_wide]
        for q in pts:
            recs.append({"tag": "wide25|s%s" % q.get("seed"), "p": 0,
                         "point": q["point"]})
        srcs.append("points_m25_wide.json (%d of %d)"
                    % (len(pts), len(d.get("points", []))))
    else:
        missing.append("points_m25_wide.json")
    fh = os.path.join(w30, "points_hunt.json")
    if os.path.exists(fh):
        d = json.load(open(fh))
        pts = [q for q in d.get("points", []) if q.get("m") == 25
               and q.get("p")]
        keep = [q for q in pts if "s1073" in str(q.get("tag", ""))]
        keep += [q for q in pts if q not in keep][:max(0, limit_hunt
                                                       - len(keep))]
        for q in keep:
            recs.append({"tag": q.get("tag", ""), "p": q["p"],
                         "point": q["point"]})
        srcs.append("points_hunt.json (m=25: %d of %d)" % (len(keep),
                                                           len(pts)))
    else:
        missing.append("points_hunt.json")
    for nm in ("results_r10_beta_13.json", "results_r10_beta_31.json",
               "results_r10_beta_Q.json", "results_r10_alpha_13.json",
               "results_r10_alpha_Q.json"):
        fp = os.path.join(w30, nm)
        if not os.path.exists(fp):
            missing.append(nm)
            continue
        d = json.load(open(fp))
        hits = [h for h in d.get("hits", []) if "point" in h]
        if not hits:
            missing.append(nm + " (no stored point)")
            continue
        fld = str(d.get("field", ""))
        p = 0 if fld in ("Q", "0") else int(fld.replace("F_", "") or 0)
        recs.append({"tag": "r10|" + nm, "p": p, "point": hits[0]["point"]})
        srcs.append(nm)
    return recs, srcs, missing


CALIB = [
    # (locator, A11's recorded flags)  -- results_t10.json, keys
    # W3_supersession and W2_escape_object.
    ("wide:925024", {"R25": False, "n_R25_tuples": 0, "alpha": True,
                     "beta": True, "delivers": True}),
    ("hunt:s1073", {"R25": True, "n_R25_tuples": 6, "alpha": True,
                    "beta": True, "n_beta_tuples": 6, "delivers": True}),
]


def step8_calibration(rep, here):
    """The two objects A11 names must reproduce A11's recorded flags.

    This control exists because (R25) is easy to get subtly wrong: dropping
    W36's |T_f| = 1 condition makes (R25) hold at seed 925024, where A11
    records it FAILING -- and that error would silently erase the whole
    reason the promotion object is a disjunction.  It was caught here.
    """
    w30 = os.path.join(here, "unaudited-exclusion-w30-2026-08-19")
    if not os.path.isdir(w30):
        w30 = os.path.join(os.path.dirname(here),
                           "unaudited-exclusion-w30-2026-08-19")
    got = {}
    for locator, expect in CALIB:
        kind, key = locator.split(":", 1)
        if kind == "wide":
            fp = os.path.join(w30, "points_m25_wide.json")
            d = json.load(open(fp))
            cand = [q for q in d["points"] if str(q.get("seed")) == key]
            require(cand, "calibration point %s not found in %s"
                    % (locator, fp))
            K = Rat()
            bl = parse_point(cand[0]["point"], K)
        else:
            fp = os.path.join(w30, "points_hunt.json")
            d = json.load(open(fp))
            cand = [q for q in d["points"]
                    if q.get("m") == 25 and key in str(q.get("tag", ""))]
            require(cand, "calibration point %s not found in %s"
                    % (locator, fp))
            K = Fp(cand[0]["p"])
            bl = parse_point(cand[0]["point"], K)
        require(all_cells_nonzero(25, bl, K),
                "calibration point %s is not all-cells-nonzero" % locator)
        f = m25_R6_flags(bl, K)
        for k, want in expect.items():
            require(f[k] == want,
                    "CALIBRATION MISMATCH at %s: %s = %r, A11 records %r"
                    % (locator, k, f[k], want))
        got[locator] = f
    rep.record("S8_calibration", points=got,
               note="reproduces audit A11's recorded (R25)/(alpha)/(beta)/"
                    "delivery flags at the two objects it names -- the "
                    "(R25)-failing point seed 925024 and the (beta)-escape "
                    "object s1073.  Guards the |T_f| = 1 condition in (R25).")
    return ("STEP 8  calibration    2/2 A11-named objects reproduce their "
            "recorded flags   PASS")


def step7_coverage(rep, here, limit_wide, limit_hunt):
    recs, srcs, missing = _load_corpus(here, limit_wide, limit_hunt)
    require(len(recs) > 0, "no stored m=25 point could be loaded")
    rows = []
    n_r25_fail = 0
    n_beta_fail = 0
    n_disj = 0
    for r in recs:
        K = Rat() if not r["p"] else Fp(r["p"])
        bl = parse_point(r["point"], K)
        if not all_cells_nonzero(25, bl, K):
            continue
        f = m25_R6_flags(bl, K)
        disj = f["R25"] or (f["alpha"] and f["beta"])
        if not f["R25"]:
            n_r25_fail += 1
        if not f["beta"]:
            n_beta_fail += 1
        if disj:
            n_disj += 1
        require(not (disj and not f["delivers"]),
                "COVERAGE VIOLATION at %s: the disjunction holds but R6 does "
                "not deliver" % r["tag"])
        rows.append({"tag": r["tag"], "field": K.name, "R25": f["R25"],
                     "n_R25_tuples": f["n_R25_tuples"], "alpha": f["alpha"],
                     "beta": f["beta"], "delivers": f["delivers"],
                     "disjunction": disj})
    n = len(rows)
    require(n > 0, "every loaded point failed the all-cells-nonzero filter")
    require(n_disj == n,
            "the disjunction covered only %d of %d stored points" % (n_disj,
                                                                     n))
    require(n_beta_fail == 0,
            "(beta) failed at %d stored points; A11 measured 0 of 32" %
            n_beta_fail)
    rep.record("S7_coverage", n_points=n, sources=srcs,
               disjunction_covers=n_disj, R25_failures=n_r25_fail,
               beta_failures=n_beta_fail, rows=rows,
               unstored_excluded=[
                   "A11's 16 generated points (never stored; "
                   "results_t2.json V2_A11_family reports them but the "
                   "blocks are not on disk)",
                   "W30's '32/33 independent family' (never stored; not "
                   "re-derivable)",
                   "round 10's most informative exception object (LOST)"],
               note="A11's corpus is 32 points; this step reproduces the "
                    "table over the STORED subset only.  Unstored members "
                    "are excluded loudly, never silently interpolated.")
    return ("STEP 7  coverage       %d stored points: disjunction %d/%d, "
            "(R25) failures %d, (beta) failures %d   PASS"
            % (n, n_disj, n, n_r25_fail, n_beta_fail))


# -------------------------------------------------------------------- driver
DECL = ["S1_template_facts", "S2_pigeonhole_n2", "S3_rank_chain_n2",
        "S4_n3_nogo", "S5_w30z_implication", "S6_mut_z2", "S7_coverage",
        "S8_calibration"]
MANDATORY = ["S1_template_facts", "S2_pigeonhole_n2", "S3_rank_chain_n2",
             "S4_n3_nogo", "S5_w30z_implication", "S6_mut_z2"]


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="House checker for ROUTE-A-RESIDUAL section 5.")
    ap.add_argument("--seed", type=int, default=20260820)
    ap.add_argument("--prime", type=int, default=13,
                    help="small prime for the exhaustive n=2 sweep")
    ap.add_argument("--zprime", type=int, default=31)
    ap.add_argument("--trials", type=int, default=20000)
    ap.add_argument("--n3-samples", type=int, default=200000)
    ap.add_argument("--wide", type=int, default=8,
                    help="stored wide m=25 points to use in step 7")
    ap.add_argument("--hunt", type=int, default=4,
                    help="stored m=25 hunt points to use in step 7")
    ap.add_argument("--strict", action="store_true",
                    help="make step 7 mandatory")
    ap.add_argument("--json", default=None)
    args = ap.parse_args(argv)

    t0 = time.time()
    rng = random.Random(args.seed)
    rep = Report(DECL)
    rep.d["seed"] = args.seed
    rep.d["python"] = sys.version.split()[0]
    rep.d["optimised"] = not __debug__

    here = os.path.dirname(os.path.abspath(__file__))
    print("verify_delivery_lemmas.py  seed=%d  python=%s  -O=%s"
          % (args.seed, sys.version.split()[0], not __debug__))
    print("")

    print(step1_structure(rep), flush=True)
    ex = _exhaustive_n2(args.prime)
    print(step2_pigeonhole(rep, ex, args.prime), flush=True)
    print(step3_rank_chain(rep, ex, args.prime), flush=True)
    # STEP 4 uses the SAME prime as the n=2 sweep, so that the two halves of
    # the structural note are measured in one field (A11 measured F_13).
    print(step4_n3_nogo(rep, rng, args.prime, args.n3_samples), flush=True)
    print(step5_w30z(rep, rng, args.zprime, args.trials), flush=True)
    print(step6_mut_z2(rep, rng, args.zprime, args.trials), flush=True)

    mand = list(MANDATORY)
    try:
        line8 = step8_calibration(rep, here)
        mand.append("S8_calibration")
    except CheckerError:
        raise
    except (IOError, OSError, KeyError, ValueError) as exc:
        if args.strict:
            raise CheckerError("--strict: step 8 could not run: %s" % exc)
        rep.skip("S8_calibration", "corpus unavailable: %s" % exc)
        line8 = ("STEP 8  calibration    SKIPPED (corpus unavailable: %s; "
                 "--strict to require it)" % exc)
    print(line8, flush=True)

    try:
        line = step7_coverage(rep, here, args.wide, args.hunt)
        mand.append("S7_coverage")
    except CheckerError:
        raise
    except (IOError, OSError, KeyError, ValueError) as exc:
        if args.strict:
            raise CheckerError("--strict: step 7 could not run: %s" % exc)
        rep.skip("S7_coverage", "corpus unavailable: %s" % exc)
        line = ("STEP 7  coverage       SKIPPED (corpus unavailable: %s; "
                "--strict to require it)" % exc)
    print(line, flush=True)

    rep.d["elapsed_s"] = round(time.time() - t0, 1)
    rep.finish(mand)
    print("")
    print("ALL MANDATORY STEPS PASS  (%.1f s)" % rep.d["elapsed_s"])
    if args.json:
        fh = open(args.json, "w")
        json.dump(rep.d, fh, indent=1, default=str)
        fh.close()
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except CheckerError as exc:
        sys.stderr.write("CHECKER FAILURE: %s\n" % exc)
        sys.exit(1)
