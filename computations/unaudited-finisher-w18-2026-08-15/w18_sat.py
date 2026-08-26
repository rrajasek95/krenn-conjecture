#!/usr/bin/env python3
"""UNAUDITED PROBE (W18) -- per-support-graph SAT layer + fast fibre engine.

Pinned HEAD: see PINNED_HEAD.txt.  Probe output; not a proved project claim.

ENCODING (support graph G fixed, support = |E(G)| = m exactly)
  x[e][k], k = 3i+j          cell (i,j) of edge e in E(G) is occupied
  (NZ)   for e in E(G):      OR_k x[e][k]          (the block is nonzero)
  (THIN) t[e][s][r] -> every occupied cell of e carries colour r at side s
         (only the -> direction: t occurs positively)
  (SC)   for each vertex p, colour r:  OR over incident e in E(G) of
         t[e][far side][r]
  (CONST) for each colour c: OR over perfect matchings M contained in E(G)
         of d[c][M];  d[c][M] -> the four cells (c,c) of M are occupied
  (NOSING, lazy) for one word w at a time, the EXACT constraint
         "the fibre of w does not have size 1":
             z[w][M] <-> all four cells of M at w are occupied   (M in P_G)
             for each M in P_G:  (M supported) -> OR_{M' != M} z[w][M']
  (KILL, lazy) one clause per verified kill certificate: the negation of the
         certificate's reason set.

Every clause of the first four groups is a consequence of "T is the support
pattern of an exact source with support graph G"; the NOSING clauses are the
exact singleton exclusion (O2); the KILL clauses are justified one by one by a
re-verified Lemma W18-A certificate.  So UNSAT = no exact source with a
support graph in this class.
"""

from __future__ import annotations

import numpy as np

import w18_core as C

# --------------------------------------------------------- fast fibres

_W = np.array(C.WORDS, dtype=np.int64)                     # (6561, 8)
CELLIDX = np.zeros((C.NE, len(C.WORDS)), dtype=np.int64)
for _e, (_u, _v) in enumerate(C.EDGES):
    CELLIDX[_e] = 3 * _W[:, _u] + _W[:, _v]
MIXED = np.array([len(set(w)) > 1 for w in C.WORDS], dtype=bool)
CONST_IDX = np.array([C.WIDX[(c,) * C.N] for c in range(C.Q)])


class FibreEngine:
    """Fibre sizes of every word, for templates on a fixed support graph."""

    def __init__(self, edge_list):
        self.edges = list(edge_list)
        self.pms = [n for n, M in enumerate(C.PM_EIDX)
                    if all(e in set(edge_list) for e in M)]
        self.pm_edges = [C.PM_EIDX[n] for n in self.pms]

    def sizes(self, T):
        occ = np.zeros((C.NE, 9), dtype=bool)
        for e in self.edges:
            m = T[e]
            for k in range(9):
                if (m >> k) & 1:
                    occ[e, k] = True
        per = np.zeros((C.NE, len(C.WORDS)), dtype=bool)
        for e in self.edges:
            per[e] = occ[e][CELLIDX[e]]
        total = np.zeros(len(C.WORDS), dtype=np.int16)
        for M in self.pm_edges:
            acc = per[M[0]] & per[M[1]] & per[M[2]] & per[M[3]]
            total += acc
        return total

    def singleton_words(self, T):
        s = self.sizes(T)
        idx = np.nonzero((s == 1) & MIXED)[0]
        return [C.WORDS[i] for i in idx], s

    def constants_ok(self, sizes):
        return bool(np.all(sizes[CONST_IDX] > 0))


# ------------------------------------------------------------- encoder

class ClassEncoder:
    """CNF for one support-graph isomorphism class."""

    def __init__(self, mask):
        self.mask = mask
        self.edges = [e for e in range(C.NE) if (mask >> e) & 1]
        self.edge_set = set(self.edges)
        self.nv = 0
        self.clauses = []
        self.x = {}
        for e in self.edges:
            for k in range(9):
                self.nv += 1
                self.x[(e, k)] = self.nv
        # (NZ)
        for e in self.edges:
            self.clauses.append([self.x[(e, k)] for k in range(9)])
        # (THIN)
        self.t = {}
        for e in self.edges:
            for side in range(2):          # 0: far colour is the row index i
                for r in range(3):         # 1: far colour is the column j
                    self.nv += 1
                    v = self.nv
                    self.t[(e, side, r)] = v
                    for k in range(9):
                        i, j = divmod(k, 3)
                        if (j if side == 1 else i) != r:
                            self.clauses.append([-v, -self.x[(e, k)]])
        # at most one far colour per (edge, side): a resolvent of (THIN) and
        # (NZ), added explicitly because it is what unit propagation needs
        for e in self.edges:
            for side in range(2):
                for r in range(3):
                    for r2 in range(r + 1, 3):
                        self.clauses.append([-self.t[(e, side, r)],
                                             -self.t[(e, side, r2)]])
        # (SC)
        for p in range(C.N):
            for r in range(3):
                lits = []
                for e in C.INCIDENT[p]:
                    if e not in self.edge_set:
                        continue
                    u, v = C.EDGES[e]
                    side = 1 if u == p else 0
                    lits.append(self.t[(e, side, r)])
                self.clauses.append(lits)          # empty => trivially UNSAT
        # (CONST)
        self.pms = [n for n, M in enumerate(C.PM_EIDX)
                    if all(e in self.edge_set for e in M)]
        for c in range(3):
            lits = []
            for n in self.pms:
                self.nv += 1
                d = self.nv
                lits.append(d)
                for e in C.PM_EIDX[n]:
                    self.clauses.append([-d, self.x[(e, 4 * c)]])
            self.clauses.append(lits)
        self.base_clauses = len(self.clauses)
        self.word_done = set()
        self.zvars = {}
        self.kill_clauses = 0
        self.seen_clauses = set()

    # -- lazily added exact constraints ---------------------------------

    def add_word_constraint(self, w):
        """The exact 'fibre(w) != 1' constraint for one word."""
        if w in self.word_done:
            return 0
        self.word_done.add(w)
        cells = {}
        for n in self.pms:
            sel = []
            for e in C.PM_EIDX[n]:
                u, v = C.EDGES[e]
                sel.append(self.x[(e, 3 * w[u] + w[v])])
            cells[n] = sel
        z = {}
        added = 0
        for n in self.pms:
            self.nv += 1
            z[n] = self.nv
            for lit in cells[n]:
                self.clauses.append([-z[n], lit])
                added += 1
            self.clauses.append([-lit for lit in cells[n]] + [z[n]])
            added += 1
        for n in self.pms:
            self.clauses.append([-lit for lit in cells[n]]
                                + [z[k] for k in self.pms if k != n])
            added += 1
        self.zvars[w] = z
        return added

    def add_kill_clause(self, reason):
        """Nogood: the negation of a verified kill certificate's reason set."""
        cl = []
        for (kind, e, i, j) in reason:
            if e not in self.edge_set:
                # cells outside the support graph are unconditionally empty,
                # so an 'off' literal there is a tautology and is dropped; an
                # 'on' literal there cannot occur.
                assert kind == "off", "kill reason wants a cell off-graph ON"
                continue
            lit = self.x[(e, 3 * i + j)]
            cl.append(-lit if kind == "on" else lit)
        assert cl, "empty kill clause"
        key = frozenset(cl)
        if key in self.seen_clauses:
            return None
        self.seen_clauses.add(key)
        self.clauses.append(cl)
        self.kill_clauses += 1
        return cl

    # -- decoding -------------------------------------------------------

    def decode(self, model):
        pos = set(l for l in model if l > 0)
        T = [0] * C.NE
        for e in self.edges:
            m = 0
            for k in range(9):
                if self.x[(e, k)] in pos:
                    m |= 1 << k
            T[e] = m
        return tuple(T)

    def block_template(self, T):
        """Blocking clause forbidding exactly this cell pattern."""
        cl = []
        for e in self.edges:
            for k in range(9):
                lit = self.x[(e, k)]
                cl.append(-lit if (T[e] >> k) & 1 else lit)
        self.clauses.append(cl)
        return cl


def write_cnf(path, nv, clauses):
    with open(path, "w") as fh:
        fh.write("p cnf %d %d\n" % (nv, len(clauses)))
        for cl in clauses:
            fh.write(" ".join(map(str, cl)) + " 0\n")


def lex_constraints(enc, group, prefix=54):
    """Lex-leader symmetry breaking: x <=_lex g(x) for every g in `group`.

    Sound whenever the rest of the formula is closed under `group` (base
    encoding is equivariant; the nogoods must be added for the whole orbit).
    Truncating the comparison to the first `prefix` cells is also sound, since
    x <=_lex g(x) implies the same for any prefix.
    """
    import w18_sym as SY
    order = [(e, k) for e in enc.edges for k in range(9)][:prefix]
    added = 0
    for (pi, sig) in group:
        if (pi, sig) == SY.IDENT:
            continue
        pairs = []
        for (e, k) in order:
            i, j = divmod(k, 3)
            e2, i2, j2 = SY.map_cell(e, i, j, pi, sig)
            if e2 not in enc.edge_set:
                pairs = []
                break
            pairs.append((enc.x[(e, k)], enc.x[(e2, 3 * i2 + j2)]))
        if not pairs:
            continue
        prev = None
        for n, (a, b) in enumerate(pairs):
            enc.nv += 1
            eq = enc.nv                       # "prefix 0..n is equal"
            if prev is None:
                enc.clauses.append([-a, b])
                enc.clauses.append([-eq, -a, b])
                enc.clauses.append([-eq, a, -b])
                enc.clauses.append([eq, a, b])
                enc.clauses.append([eq, -a, -b])
                added += 5
            else:
                enc.clauses.append([-prev, -a, b])
                enc.clauses.append([-eq, prev])
                enc.clauses.append([-eq, -a, b])
                enc.clauses.append([-eq, a, -b])
                enc.clauses.append([eq, -prev, a, b])
                enc.clauses.append([eq, -prev, -a, -b])
                added += 6
            prev = eq
    return added
