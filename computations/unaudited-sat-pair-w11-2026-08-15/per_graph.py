"""UNAUDITED (W11).  Decide the question with the SUPPORT GRAPH pinned.

For a fixed edge set G (|G| = m) the fibre of every word is contained in
PM(G) = the perfect matchings of K_8 that lie inside G, which is usually tiny.
That makes the FULL word encoding (all 6558 mixed words, no CEGAR) cheap, so
this path carries no lazy-refinement subtleties at all.

Because the problem is S_8 x S_3 equivariant (verified in symmetry_check.py),
it suffices to run one representative per isomorphism class of support graph.

  vars   x[e][cell] for e in G (cells off G are simply absent = false)
  cl.1   every e in G is nonempty
  cl.2   (SC), as in sat_decide
  cl.3   each constant word is supported by some M in PM(G)
  cl.4   for each mixed word w and each M in PM(G):
             y[w][M] <-> AND of the four cells M selects
             prefix/suffix ladder forcing "not exactly one y true"
"""

import time

from pysat.formula import IDPool
from pysat.solvers import Cadical195

import krenn_core as K
import graph_classes as G


class GraphEncoder:
    def __init__(self, mask, diagonal_only=False, single_cell=False,
                 require_multicell=False, max_cells=None, sc_active=False):
        self.max_cells = max_cells
        self.sc_active = sc_active
        self.mask = mask
        self.edges = G.edges_of(mask)
        self.eset = set(self.edges)
        self.P = G.perfect_matchings_in(mask)      # indices into K.MATCHINGS
        self._mw_cache = {}
        self.pool = IDPool()
        self.clauses = []
        self.trivial_unsat = (len(self.P) == 0)
        self.diagonal_only = diagonal_only
        self.single_cell = single_cell
        self.require_multicell = require_multicell
        if not self.trivial_unsat:
            self._build()

    def x(self, e, cell):
        return self.pool.id(("x", e, cell[0], cell[1]))

    def y(self, w, k):
        return self.pool.id(("y", w, k))

    def pre(self, w, k):
        return self.pool.id(("pre", w, k))

    def suf(self, w, k):
        return self.pool.id(("suf", w, k))

    def add(self, cl):
        self.clauses.append(cl)
        return cl

    def _matchable_without(self, p, j):
        """Does the support graph minus {p, j} carry a perfect matching?"""
        key = (min(p, j), max(p, j))
        if key in self._mw_cache:
            return self._mw_cache[key]

        def rec(vs):
            if not vs:
                return True
            u = vs[0]
            for k in range(1, len(vs)):
                w = vs[k]
                if K.EIDX[(min(u, w), max(u, w))] in self.eset:
                    if rec(vs[1:k] + vs[k + 1:]):
                        return True
            return False

        val = rec([v for v in range(K.N) if v not in (p, j)])
        self._mw_cache[key] = val
        return val

    def _cells(self, e):
        if self.diagonal_only:
            return [(c, c) for c in range(3)]
        return K.CELLS

    def _build(self):
        for e in self.edges:                       # stable numbering
            for c in self._cells(e):
                self.x(e, c)

        for e in self.edges:                       # cl.1 nonempty
            self.add([self.x(e, c) for c in self._cells(e)])

        if self.single_cell:
            for e in self.edges:
                cs = self._cells(e)
                for a in range(len(cs)):
                    for b in range(a + 1, len(cs)):
                        self.add([-self.x(e, cs[a]), -self.x(e, cs[b])])

        for p in range(K.N):                       # cl.2 (SC)
            for r in range(K.D):
                dis = []
                for (ei, j) in K.INCIDENT[p]:
                    if ei not in self.eset:
                        continue
                    # (SC+) also demands the serving edge be ACTIVE
                    # (C_pj != 0 in the note); its support-level shadow is
                    # that G - {p, j} still carries a perfect matching.
                    if self.sc_active and not self._matchable_without(p, j):
                        continue
                    gv = self.pool.id(("g", p, r, ei))
                    dis.append(gv)
                    same, other = K.far_cells(p, j, r)
                    cs = set(self._cells(ei))
                    for c in other:
                        if c in cs:
                            self.add([-gv, -self.x(ei, c)])
                    self.add([-gv] + [self.x(ei, c) for c in same if c in cs])
                self.add(dis)                      # empty => UNSAT, correct

        for c in range(K.D):                       # cl.3 constant fibres
            dis = []
            for k, mi in enumerate(self.P):
                kv = self.pool.id(("k", c, mi))
                dis.append(kv)
                for ei in K.MATCHINGS[mi]:
                    dis_ok = (c, c) in set(self._cells(ei))
                    if not dis_ok:
                        dis.pop()
                        break
                    self.add([-kv, self.x(ei, (c, c))])
            self.add(dis)

        if self.require_multicell:
            dis = []
            for e in self.edges:
                cs = self._cells(e)
                for a in range(len(cs)):
                    for b in range(a + 1, len(cs)):
                        pv = self.pool.id(("pair", e, a, b))
                        dis.append(pv)
                        self.add([-pv, self.x(e, cs[a])])
                        self.add([-pv, self.x(e, cs[b])])
            self.add(dis)

        if self.max_cells is not None:
            from pysat.card import CardEnc, EncType
            lits = [self.x(e, c) for e in self.edges for c in self._cells(e)]
            cnf = CardEnc.atmost(lits=lits, bound=self.max_cells,
                                 vpool=self.pool, encoding=EncType.seqcounter)
            for cl in cnf.clauses:
                self.add(cl)

        self._words()

    def _words(self):
        P = self.P
        n = len(P)
        cellset = [set(self._cells(e)) if e in self.eset else set()
                   for e in range(K.NE)]
        for w in K.MIXED_WORDS:
            lit = []          # lit[k] = list of 4 x-vars, or None if impossible
            for k, mi in enumerate(P):
                ls = []
                bad = False
                for ei in K.MATCHINGS[mi]:
                    u, v = K.EDGES[ei]
                    c = (w[u], w[v])
                    if c not in cellset[ei]:
                        bad = True
                        break
                    ls.append(self.x(ei, c))
                lit.append(None if bad else ls)
            act = [k for k in range(n) if lit[k] is not None]
            if not act:
                continue                       # fibre is empty for every T
            if len(act) == 1:
                self.add([-l for l in lit[act[0]]])   # must not be supported
                continue
            for k in act:
                yv = self.y(w, k)
                for l in lit[k]:
                    self.add([-yv, l])
                self.add([-l for l in lit[k]] + [yv])
            for idx, k in enumerate(act):
                cl = [-self.pre(w, k), self.y(w, k)]
                if idx > 0:
                    cl.append(self.pre(w, act[idx - 1]))
                self.add(cl)
                cl = [-self.suf(w, k), self.y(w, k)]
                if idx < len(act) - 1:
                    cl.append(self.suf(w, act[idx + 1]))
                self.add(cl)
            for idx, k in enumerate(act):
                cl = [-self.y(w, k)]
                if idx > 0:
                    cl.append(self.pre(w, act[idx - 1]))
                if idx < len(act) - 1:
                    cl.append(self.suf(w, act[idx + 1]))
                self.add(cl)

    def decode(self, model):
        pos = set(l for l in model if l > 0)
        T = [set() for _ in range(K.NE)]
        for e in self.edges:
            for c in self._cells(e):
                if self.x(e, c) in pos:
                    T[e].add(c)
        return K.template_from_sets(T)

    def block(self, T):
        cl = []
        for e in self.edges:
            for c in self._cells(e):
                v = self.x(e, c)
                cl.append(-v if c in T[e] else v)
        return self.add(cl)


def sc_plus_failures(T):
    """Standalone (SC+) checker, independent of the encoder: slots (p, r) with
    no incident edge pj such that S_pj is nonempty, lies in the far-colour-r
    column, AND the support graph minus {p, j} still has a perfect matching."""
    live = set(e for e in range(K.NE) if T[e])

    def has_pm(vs):
        if not vs:
            return True
        u = vs[0]
        for k in range(1, len(vs)):
            w = vs[k]
            if K.EIDX[(min(u, w), max(u, w))] in live:
                if has_pm(vs[1:k] + vs[k + 1:]):
                    return True
        return False

    bad = []
    for p in range(K.N):
        for r in range(K.D):
            served = False
            for (ei, j) in K.INCIDENT[p]:
                S = T[ei]
                if not S:
                    continue
                same, _ = K.far_cells(p, j, r)
                if S.issubset(set(same)) and \
                        has_pm([v for v in range(K.N) if v not in (p, j)]):
                    served = True
                    break
            if not served:
                bad.append((p, r))
    return bad


def decide_graph(mask, max_solutions=1, **kw):
    enc = GraphEncoder(mask, **kw)
    if enc.trivial_unsat:
        return dict(mask=mask, verdict="UNSAT", reason="no perfect matching",
                    witnesses=[], nclauses=0, nvars=0, npm=0)
    solver = Cadical195(bootstrap_with=enc.clauses)
    wit = []
    while True:
        if not solver.solve():
            solver.delete()
            return dict(mask=mask, verdict="UNSAT" if not wit else "EXHAUSTED",
                        witnesses=wit, nclauses=len(enc.clauses),
                        nvars=enc.pool.top, npm=len(enc.P))
        T = enc.decode(solver.get_model())
        a = K.audit(T)
        ok = (a["admissible"] and a["zero_singleton"] and
              a["support"] == len(enc.edges))
        if kw.get("require_multicell"):
            ok = ok and any(len(S) >= 2 for S in T)
        if kw.get("single_cell"):
            ok = ok and all(len(S) <= 1 for S in T)
        if kw.get("diagonal_only"):
            ok = ok and all(all(c[0] == c[1] for c in S) for S in T)
        if kw.get("max_cells") is not None:
            ok = ok and a["sigma"] <= kw["max_cells"]
        if kw.get("sc_active"):
            ok = ok and not sc_plus_failures(T)
        if not ok:
            solver.delete()
            return dict(mask=mask, verdict="ENCODER_BUG", audit=a, template=T,
                        witnesses=wit)
        wit.append((T, a))
        if len(wit) >= max_solutions:
            solver.delete()
            return dict(mask=mask, verdict="SAT", witnesses=wit,
                        nclauses=len(enc.clauses), nvars=enc.pool.top,
                        npm=len(enc.P))
        solver.add_clause(enc.block(T))


def sweep(masks, max_solutions=1, verbose=True, stop_on_sat=False, **kw):
    """Run every representative; collect verdicts."""
    t0 = time.time()
    sat, unsat, bug = [], [], []
    for i, g in enumerate(masks):
        r = decide_graph(g, max_solutions=max_solutions, **kw)
        if r["verdict"] == "ENCODER_BUG":
            bug.append(r)
            print("  !! ENCODER_BUG on mask %d" % g, flush=True)
            break
        if r["verdict"] in ("SAT", "EXHAUSTED") and r["witnesses"]:
            sat.append(r)
            if verbose:
                print("  [SAT] class %d/%d mask=%d pm=%d witnesses=%d"
                      % (i + 1, len(masks), g, r["npm"], len(r["witnesses"])),
                      flush=True)
            if stop_on_sat:
                break
        else:
            unsat.append(r)
        if verbose and (i + 1) % 100 == 0:
            print("   ... %d/%d classes, %d SAT, %.1fs"
                  % (i + 1, len(masks), len(sat), time.time() - t0), flush=True)
    return dict(n=len(masks), sat=sat, unsat=len(unsat), bug=bug,
                seconds=time.time() - t0)
