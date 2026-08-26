"""UNAUDITED (W11, 2026-08-15).  Independent SAT decision for:

  does there exist a (SC)-admissible template on K_8 with support exactly m
  and ZERO singleton mixed words?

Encoding (all mine, derived from the definitions in krenn_core.py):

  x[e][i][j]     template cell variables (28 x 9 = 252)
  live[e]        <-> OR_cells x[e][*]                      (both directions)
  card           sum_e live[e] = m  (sequential counter, pysat CardEnc)
  g[p][r][j]     "edge pj serves slot (p,r)":  forward-only implications
                 g -> (no cell of S_pj with far colour != r)
                 g -> (some cell of S_pj with far colour = r)
                 plus the clause  OR_j g[p][r][j]                      -- (SC)
  kk[c][M]       "matching M lies in the fibre of the constant word c":
                 forward-only  kk -> x[e][c][c] for e in M
                 plus the clause  OR_M kk[c][M]        -- constant fibre != 0
  y[w][M]        <-> AND_{(u,v) in M} x[e][w_u][w_v]        (both directions)
                 plus, for each M,  ~y[w][M] OR (OR_{M' != M} y[w][M'])
                                                       -- w is not a singleton

Derived (redundant but valid, for propagation only -- each is a logical
consequence of (SC), see `_derived`):
  * at most one of g[p][0][e], g[p][1][e], g[p][2][e] for each incident edge
    (a nonempty block cannot lie in two different far-colour columns);
  * every vertex has at least three live incident edges.

Word constraints can be added eagerly (`build_all_words`) or LAZILY (CEGAR).
Every clause ever added is a member of the full encoding, so:
  * UNSAT of any accumulated subset  =>  UNSAT of the full problem;
  * SAT is only ever reported after krenn_core.audit re-verifies the model
    by direct enumeration over the 105 matchings.
"""

import json
import time

from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
from pysat.solvers import Cadical195

import krenn_core as K
import fastcheck as F


class Encoder:
    def __init__(self, m, diagonal_only=False, require_multicell=False,
                 card_mode="equals", single_cell=False, derived=True,
                 stream_path=None):
        self.m = m
        self.diagonal_only = diagonal_only
        self.require_multicell = require_multicell
        self.single_cell = single_cell
        self.card_mode = card_mode          # "equals" or "atmost"
        self.use_derived = derived
        self.pool = IDPool()
        self.clauses = []                   # kept only if stream_path is None
        self.nclauses = 0
        self.stream = open(stream_path, "w") if stream_path else None
        self.words = set()
        self._build_base()

    # ---------------- variables ----------------
    def x(self, e, cell):
        return self.pool.id(("x", e, cell[0], cell[1]))

    def live(self, e):
        return self.pool.id(("live", e))

    def g(self, p, r, e):
        return self.pool.id(("g", p, r, e))

    def kk(self, c, mi):
        return self.pool.id(("k", c, mi))

    def y(self, w, mi):
        return self.pool.id(("y", w, mi))

    def add(self, cl):
        self.nclauses += 1
        if self.stream is not None:
            self.stream.write(" ".join(map(str, cl)) + " 0\n")
        elif self.clauses is not None:
            self.clauses.append(list(cl))
        return cl

    # ---------------- base encoding ----------------
    def _build_base(self):
        for e in range(K.NE):                   # stable variable numbering
            for cell in K.CELLS:
                self.x(e, cell)

        if self.diagonal_only:                  # control 2
            for e in range(K.NE):
                for cell in K.CELLS:
                    if cell[0] != cell[1]:
                        self.add([-self.x(e, cell)])

        if self.single_cell:                    # at most one cell per edge
            for e in range(K.NE):
                for a in range(9):
                    for b in range(a + 1, 9):
                        self.add([-self.x(e, K.CELLS[a]),
                                  -self.x(e, K.CELLS[b])])

        for e in range(K.NE):                   # live[e] <-> OR cells
            cs = [self.x(e, c) for c in K.CELLS]
            self.add([-self.live(e)] + cs)
            for c in cs:
                self.add([-c, self.live(e)])

        for p in range(K.N):                    # (SC)
            for r in range(K.D):
                dis = []
                for (ei, j) in K.INCIDENT[p]:
                    gv = self.g(p, r, ei)
                    dis.append(gv)
                    same, other = K.far_cells(p, j, r)
                    for c in other:
                        self.add([-gv, -self.x(ei, c)])
                    self.add([-gv] + [self.x(ei, c) for c in same])
                self.add(dis)

        for c in range(K.D):                    # constant fibres nonempty
            dis = []
            for mi, M in enumerate(K.MATCHINGS):
                kv = self.kk(c, mi)
                dis.append(kv)
                for ei in M:
                    self.add([-kv, self.x(ei, (c, c))])
            self.add(dis)

        if self.require_multicell:              # some edge carries >= 2 cells
            dis = []
            for e in range(K.NE):
                for a in range(9):
                    for b in range(a + 1, 9):
                        pv = self.pool.id(("pair", e, a, b))
                        dis.append(pv)
                        self.add([-pv, self.x(e, K.CELLS[a])])
                        self.add([-pv, self.x(e, K.CELLS[b])])
            self.add(dis)

        if self.use_derived:
            self._derived()

        lits = [self.live(e) for e in range(K.NE)]   # support cardinality
        if self.card_mode == "equals":
            cnf = CardEnc.equals(lits=lits, bound=self.m, vpool=self.pool,
                                 encoding=EncType.seqcounter)
        else:
            cnf = CardEnc.atmost(lits=lits, bound=self.m, vpool=self.pool,
                                 encoding=EncType.seqcounter)
        for cl in cnf.clauses:
            self.add(cl)

    def _derived(self):
        # (a) a nonempty block lies in at most one far-colour column
        for p in range(K.N):
            for (ei, j) in K.INCIDENT[p]:
                for r in range(K.D):
                    for s in range(r + 1, K.D):
                        self.add([-self.g(p, r, ei), -self.g(p, s, ei)])
        # (b) hence every vertex has >= 3 live incident edges
        for p in range(K.N):
            lits = [self.live(ei) for (ei, j) in K.INCIDENT[p]]
            cnf = CardEnc.atleast(lits=lits, bound=3, vpool=self.pool,
                                  encoding=EncType.seqcounter)
            for cl in cnf.clauses:
                self.add(cl)

    # ---------------- word constraints ----------------
    def pre(self, w, i):
        return self.pool.id(("pre", w, i))

    def suf(self, w, i):
        return self.pool.id(("suf", w, i))

    def add_word(self, w, sink=None):
        """Assert that mixed word w is not a singleton.

        y[w][M] <-> AND of the four cells M selects on w (full Tseitin), then
        a prefix/suffix OR ladder:
            pre[i] -> pre[i-1] OR y[i]        (pre[i]  ==> some y[j], j <= i)
            suf[i] -> suf[i+1] OR y[i]        (suf[i]  ==> some y[j], j >= i)
            ~y[i] OR pre[i-1] OR suf[i+1]     (y[i] ==> some OTHER y is true)
        Only the "->" halves of the ladder are needed because pre/suf occur
        positively; setting them to their true values shows completeness.
        """
        if w in self.words:
            return sink if sink is not None else []
        self.words.add(w)
        out = [] if sink is None else sink
        for mi, M in enumerate(K.MATCHINGS):
            yv = self.y(w, mi)
            lits = [self.x(ei, (w[K.EDGES[ei][0]], w[K.EDGES[ei][1]]))
                    for ei in M]
            for l in lits:
                out.append(self.add([-yv, l]))
            out.append(self.add([-l for l in lits] + [yv]))
        n = K.NM
        for i in range(n):
            cl = [-self.pre(w, i), self.y(w, i)]
            if i > 0:
                cl.append(self.pre(w, i - 1))
            out.append(self.add(cl))
            cl = [-self.suf(w, i), self.y(w, i)]
            if i < n - 1:
                cl.append(self.suf(w, i + 1))
            out.append(self.add(cl))
        for i in range(n):
            cl = [-self.y(w, i)]
            if i > 0:
                cl.append(self.pre(w, i - 1))
            if i < n - 1:
                cl.append(self.suf(w, i + 1))
            out.append(self.add(cl))
        return out

    def build_all_words(self, solver=None, batch=200):
        """Add every mixed word's constraint; feed `solver` in batches."""
        buf = []
        for w in K.MIXED_WORDS:
            self.add_word(w, sink=buf)
            if solver is not None and len(buf) > batch * 900:
                solver.append_formula(buf)
                buf = []
        if solver is not None and buf:
            solver.append_formula(buf)
        return buf

    # ---------------- decoding ----------------
    def decode(self, model):
        pos = set(l for l in model if l > 0)
        return [frozenset(c for c in K.CELLS if self.x(e, c) in pos)
                for e in range(K.NE)]

    def block(self, T):
        cl = []
        for e in range(K.NE):
            for c in K.CELLS:
                v = self.x(e, c)
                cl.append(-v if c in T[e] else v)
        return self.add(cl)

    def finish_stream(self, path):
        """Close the streamed body and prepend the DIMACS header."""
        self.stream.close()
        self.stream = None
        with open(path, "w") as out:
            out.write("p cnf %d %d\n" % (self.pool.top, self.nclauses))
            with open(path + ".body") as body:
                for line in body:
                    out.write(line)

    def write_dimacs(self, path):
        with open(path, "w") as f:
            f.write("p cnf %d %d\n" % (self.pool.top, self.nclauses))
            for cl in self.clauses:
                f.write(" ".join(map(str, cl)) + " 0\n")


def _verify(T, m, card_mode, diagonal_only, require_multicell, single_cell):
    """Independent re-verification of a candidate witness (naive enumeration)."""
    a = K.audit(T)
    ok = a["admissible"] and a["zero_singleton"]
    ok = ok and (a["support"] == m if card_mode == "equals"
                 else a["support"] <= m)
    if require_multicell:
        ok = ok and any(len(S) >= 2 for S in T)
    if single_cell:
        ok = ok and all(len(S) <= 1 for S in T)
    if diagonal_only:
        ok = ok and all(all(c[0] == c[1] for c in S) for S in T)
    return ok, a


def decide(m, diagonal_only=False, require_multicell=False, card_mode="equals",
           max_solutions=1, seed_words=(), verbose=True, time_budget=None,
           single_cell=False, derived=True, eager=False, tag=None,
           progress=50):
    """Decide the support-m question.  Returns a result dict."""
    t0 = time.time()
    enc = Encoder(m, diagonal_only, require_multicell, card_mode, single_cell,
                  derived)
    solver = Cadical195(bootstrap_with=enc.clauses)
    if eager:
        enc.clauses = None            # stop hoarding; solver owns them now
        enc.build_all_words(solver=solver)
    else:
        buf = []
        for w in seed_words:
            enc.add_word(w, sink=buf)
        if buf:
            solver.append_formula(buf)
    if verbose:
        print("   [enc] %d vars %d clauses (%.1fs)"
              % (enc.pool.top, enc.nclauses, time.time() - t0), flush=True)
    witnesses = []
    it = 0
    while True:
        if time_budget is not None and time.time() - t0 > time_budget:
            solver.delete()
            return dict(m=m, tag=tag, verdict="TIMEOUT", iters=it,
                        words=len(enc.words), clauses=enc.nclauses,
                        witnesses=witnesses, seconds=time.time() - t0,
                        encoder=enc)
        it += 1
        if not solver.solve():
            solver.delete()
            return dict(m=m, tag=tag,
                        verdict="UNSAT" if not witnesses else "EXHAUSTED",
                        iters=it, words=len(enc.words), clauses=enc.nclauses,
                        witnesses=witnesses, seconds=time.time() - t0,
                        encoder=enc)
        T = enc.decode(solver.get_model())
        sings = F.singleton_words(T)
        if sings:
            new = []
            for w in sings:
                enc.add_word(w, sink=new)
            solver.append_formula(new)
            if verbose and it % progress == 0:
                print("   it=%d words=%d clauses=%d t=%.1fs"
                      % (it, len(enc.words), enc.nclauses, time.time() - t0),
                      flush=True)
            continue
        ok, a = _verify(T, m, card_mode, diagonal_only, require_multicell,
                        single_cell)
        if not ok:
            solver.delete()
            return dict(m=m, tag=tag, verdict="ENCODER_BUG", audit=a,
                        template=T, iters=it, encoder=enc)
        witnesses.append((T, a))
        if verbose:
            print("   [SAT] witness #%d support=%d Sigma=%d (it=%d words=%d "
                  "%.1fs)" % (len(witnesses), a["support"], a["sigma"], it,
                              len(enc.words), time.time() - t0), flush=True)
        if len(witnesses) >= max_solutions:
            solver.delete()
            return dict(m=m, tag=tag, verdict="SAT", iters=it,
                        words=len(enc.words), clauses=enc.nclauses,
                        witnesses=witnesses, seconds=time.time() - t0,
                        encoder=enc)
        solver.add_clause(enc.block(T))


def save(res, path):
    out = {k: v for k, v in res.items()
           if k not in ("encoder", "witnesses", "template")}
    out["witnesses"] = [
        {"template": K.template_to_json(T),
         "audit": {kk: vv for kk, vv in a.items()
                   if kk != "singleton_examples"}}
        for T, a in res.get("witnesses", [])]
    with open(path, "w") as f:
        json.dump(out, f, indent=1, default=str)
    return out


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("m", type=int)
    ap.add_argument("--diagonal", action="store_true")
    ap.add_argument("--multicell", action="store_true")
    ap.add_argument("--singlecell", action="store_true")
    ap.add_argument("--atmost", action="store_true")
    ap.add_argument("--eager", action="store_true")
    ap.add_argument("--no-derived", action="store_true")
    ap.add_argument("--solutions", type=int, default=1)
    ap.add_argument("--budget", type=float, default=None)
    ap.add_argument("--out", default=None)
    ap.add_argument("--tag", default=None)
    a = ap.parse_args()
    res = decide(a.m, diagonal_only=a.diagonal, require_multicell=a.multicell,
                 single_cell=a.singlecell,
                 card_mode="atmost" if a.atmost else "equals",
                 max_solutions=a.solutions, time_budget=a.budget,
                 derived=not a.no_derived, eager=a.eager, tag=a.tag)
    print(json.dumps({k: v for k, v in res.items()
                      if k not in ("encoder", "witnesses", "template")},
                     default=str))
    if a.out:
        save(res, a.out)
