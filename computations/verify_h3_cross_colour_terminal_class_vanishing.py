#!/usr/bin/env python3
"""Cross-colour star-sector repair: the terminal class cannot survive.

Continues ``notes/h3-cross-colour-repair-internal-edge-localization.md``, whose
C1/C2/C3 leave the unconditional cross-colour case open.  Everything below is
re-derived by an implementation written from the definition of the row
functional; nothing is imported from the committed checkers, and the committed
statements it overlaps (the guard ledger, C1, C2, C3, the monochromatic
infeasibilities, the seven-row guard and the pure-word witness) are reproduced
here as cross-checks.

Setting.  Six residual sites, three colours; the colour-2 slice of the audited
seven-row guard is frozen (q_2 = (01)_2 + (45)_2, p_0 = z_0+z_1, p_1 = z_4,
p_2 = z_2+z_3, s_0 = z_5, s_1 = z_2-z_3, s_2 = (z_2+z_3)/2), and free are the
nine direct scalars, the seventy-two colour-0/1 star entries, the thirty
monochromatic colour-0/1 internal edges and the ninety cross-colour internal
edges: 201 unknowns, 6438 nonzero equations of the 9x729.  Write q(x@a, y@b)
for the internal edge {x,y} carrying colour a at x and b at y.

What is proved here.

  D1  Null response.  Eliminating haf_w(q) between the (0,1) and the (0,2) row
      gives, at *every* one of the 729 words,

          < p_0^w , H_w (d_02 s_1 - d_01 s_2)^w > = 0,

      i.e. the response (p_0, u) with u = d_02 s_1 - d_01 s_2 annihilates the
      grade-zero four-hole pairing at every word.  Its frozen part is
      -(b/2) e_2 - (a/2) e_3 with a = d_01 + 2 d_02, b = d_01 - 2 d_02, and on
      this slice the only admissible caps with a nonzero terminal class are
      (0,1) with chi = -2 d_01 and (0,2) with chi = d_02/2.  So

          chi != 0  <=>  (a, b) != (0, 0)  <=>  u has a nonzero frozen part,

      and that part always sits on the two anchor sites {2,3}.  This is the
      exact complement of C2, which kills the star term instead of the direct
      one, and unlike C2 it holds at every word rather than at fifteen.

  D2  The single-word trade mechanism is exhausted.  For every word w the full
      space of rational 3x3 arrays L with sum_ij L_ij (star part of Row(i,j,w))
      identically zero is computed.  125 words have a nonzero such space; the
      resulting relations (sum_ij L_ij d_ij) haf_w(q) = 0 involve exactly nine
      linear forms in the direct scalars, and the only ones involving d_01 or
      d_02 are proportional to d_01 + 2 d_02 and to d_01 - 2 d_02, with exactly
      the six-word C1-reduced families of C2.  So no linear combination of the
      nine rows at a single word yields a hafnian-vanishing condition beyond
      C2's.

  D3  Sharpened localisation (C3 halved).  C3 needs all twenty 2-mixed edges
      whose non-2 colour sits at site 2 *or* site 3 to vanish.  In fact each
      half suffices on its own: setting the ten edges

          L2 = { q(x@2, 2@c), q(2@c, y@2) : x in {0,1}, y in {3,4,5} }

      to zero closes the whole 9x729 system, and so does the mirror set L3 at
      site 3.  Hence any cross-colour completion has a nonzero 2-mixed edge
      whose non-2 colour sits at site 2 *and* another whose non-2 colour sits
      at site 3 -- twice the localisation of C3.

  D4  The edge {2,3} must be live in both 2-mixed orientations, and the
      terminal class cannot survive.  Each of the two-edge hypotheses

          q(2@0, 3@2) = q(2@1, 3@2) = 0     and     q(2@2, 3@0) = q(2@2, 3@1) = 0

      closes the entire 9x729 cross-colour system on its own -- an exhaustive
      search, decomposed by D3 into 80 branches apiece, each branch owning two
      nonzero declarations.  Neither hypothesis mentions the class, so this is
      unconditional: any cross-colour completion has q(2@c, 3@2) != 0 for some
      c and q(2@2, 3@c) != 0 for some c.  That is C2's live-in-both-orientations
      situation, in which C2 forces d_01 + 2 d_02 = d_01 - 2 d_02 = 0.  Hence
      every solution of the nine-row system on this slice has d_01 = d_02 = 0
      and chi = 0 on every admissible cap: a cross-colour star-sector repair
      cannot preserve the terminal class, which is what the monochromatic trade
      of h3-star-sector-anchor-terminal-class-trade.md proved under its
      monochromatic hypothesis.  D4 also subsumes D3, whose ten-edge families
      contain these two-edge ones; D3 is kept because the D4 search uses it.

What is NOT proved: whether a cross-colour completion exists at all.  D4 is a
vanishing statement about chi, which is the only admissible shape
(``terminal-class-weight-invisibility-and-fourhole-grade-ladder.md``); the
unconditional feasibility question is untouched and stays open.

Krenn's conjecture remains open and no certified dependency changes.  Standard
library only, exact Fraction arithmetic, deterministic across hash seeds, live
under ``python -O`` and ``python -I -S``.

Usage:  python3 verify_h3_cross_colour_terminal_class_vanishing.py [lo hi]
The optional range shards the 160 branch searches of D4 (default: all of them).
D1, D2, D3 and the engine sanity suite always run.  The full run is minutes,
not seconds: the branch searches are the price of the result.
"""

import sys
import time
from fractions import Fraction as F
from itertools import combinations, product


class Contradiction(Exception):
    pass


def require(condition, message):
    if not condition:
        raise AssertionError(message)


COLORS = (0, 1, 2)
SITES = tuple(range(6))
PURE = 2

# ---- the frozen colour-2 slice, from the audited guard checker -------------
Q2 = {(0, 1): F(1), (4, 5): F(1)}
P2 = {0: (F(1), F(1), F(0), F(0), F(0), F(0)),
      1: (F(0), F(0), F(0), F(0), F(1), F(0)),
      2: (F(0), F(0), F(1), F(1), F(0), F(0))}
S2 = {0: (F(0), F(0), F(0), F(0), F(0), F(1)),
      1: (F(0), F(0), F(1), F(-1), F(0), F(0)),
      2: (F(0), F(0), F(1, 2), F(1, 2), F(0), F(0))}

_MATCH = {}


def matchings(vertices):
    vertices = tuple(vertices)
    got = _MATCH.get(vertices)
    if got is not None:
        return got
    if not vertices:
        out = ((),)
    elif len(vertices) % 2:
        out = ()
    else:
        head = vertices[0]
        acc = []
        for pos in range(1, len(vertices)):
            rest = vertices[1:pos] + vertices[pos + 1:]
            for tail in matchings(rest):
                acc.append(((head, vertices[pos]),) + tail)
        out = tuple(acc)
    _MATCH[vertices] = out
    return out


# ---- sparse polynomials over integer-indexed unknowns ----------------------
NAMES = []
INDEX = {}


def vid(name):
    got = INDEX.get(name)
    if got is None:
        got = len(NAMES)
        INDEX[name] = got
        NAMES.append(name)
    return got


def const(value):
    value = F(value)
    return {(): value} if value else {}


def var(name):
    return {(vid(name),): F(1)}


def add(a, b):
    out = dict(a)
    for m, c in b.items():
        t = out.get(m)
        t = c if t is None else t + c
        if t:
            out[m] = t
        else:
            out.pop(m, None)
    return out


def scale(a, k):
    return {} if not k else {m: c * k for m, c in a.items()}


def mul(a, b):
    if not a or not b:
        return {}
    out = {}
    for m1, c1 in a.items():
        for m2, c2 in b.items():
            m = tuple(sorted(m1 + m2))
            t = out.get(m)
            t = c1 * c2 if t is None else t + c1 * c2
            if t:
                out[m] = t
            else:
                out.pop(m, None)
    return out


def degree(p):
    return max((len(m) for m in p), default=0)


def poly_vars(p):
    out = set()
    for m in p:
        out.update(m)
    return out


def substitute(p, sub):
    hit = False
    for m in p:
        for v in m:
            if v in sub:
                hit = True
                break
        if hit:
            break
    if not hit:
        return p
    out = {}
    for m, c in p.items():
        keep = []
        reps = []
        for v in m:
            rep = sub.get(v)
            if rep is None:
                keep.append(v)
            elif not rep:
                reps = None
                break
            else:
                reps.append(rep)
        if reps is None:
            continue
        term = {tuple(keep): c}
        for rep in reps:
            term = mul(term, rep)
            if not term:
                break
        if not term:
            continue
        for mm, cc in term.items():
            t = out.get(mm)
            t = cc if t is None else t + cc
            if t:
                out[mm] = t
            else:
                out.pop(mm, None)
    return out


def evaluate(p, assign):
    total = F(0)
    for m, c in p.items():
        t = c
        for v in m:
            t *= assign.get(NAMES[v], F(0))
            if not t:
                break
        total += t
    return total


# ---- the packet model ------------------------------------------------------
ALLOW_CROSS = [True]


def q_edge(x, y, cx, cy):
    if x > y:
        x, y = y, x
        cx, cy = cy, cx
    if cx == PURE and cy == PURE:
        return const(Q2.get((x, y), 0))
    if cx != cy:
        return var(("X", x, y, cx, cy)) if ALLOW_CROSS[0] else const(0)
    return var(("q", cx, x, y))


def p_entry(i, x, c):
    return const(P2[i][x]) if c == PURE else var(("p", i, x, c))


def s_entry(j, y, c):
    return const(S2[j][y]) if c == PURE else var(("s", j, y, c))


def haf(sites, word):
    total = {}
    for m in matchings(tuple(sites)):
        term = const(1)
        for x, y in m:
            term = mul(term, q_edge(x, y, word[x], word[y]))
            if not term:
                break
        if term:
            total = add(total, term)
    return total


def holes(word):
    out = {}
    for x, y in combinations(SITES, 2):
        comp = tuple(v for v in SITES if v != x and v != y)
        out[(x, y)] = haf(comp, word)
    return out


def star_term(i, j, word, hole):
    total = {}
    for x, y in combinations(SITES, 2):
        piece = hole[(x, y)]
        if not piece:
            continue
        resp = add(mul(p_entry(i, x, word[x]), s_entry(j, y, word[y])),
                   mul(p_entry(i, y, word[y]), s_entry(j, x, word[x])))
        if resp:
            total = add(total, mul(resp, piece))
    return total


def build_system(allow_cross=True, labels=None, extra_pure=()):
    """{(i, j, word): polynomial that must vanish}."""
    ALLOW_CROSS[0] = allow_cross
    keep = tuple(product(COLORS, repeat=2)) if labels is None else tuple(labels)
    out = {}
    for word in product(COLORS, repeat=6):
        full = haf(SITES, word)
        hole = holes(word)
        for i, j in product(COLORS, repeat=2):
            pure = i == j and all(c == i for c in word)
            if (i, j) not in keep and not (pure and (i, j) in extra_pure):
                continue
            total = add(mul(var(("d", i, j)), full), star_term(i, j, word, hole))
            if pure:
                total = add(total, const(-1))
            if total:
                out[(i, j, word)] = total
    return out


# ---- the decision engine ---------------------------------------------------
def poly_key(p):
    return tuple(sorted(p.items()))


class State(object):
    """eqs: {key: poly = 0};  nz: {key: poly != 0};  sub: eliminated vars.

    Sound rules only, valid over any integral domain: a nonzero constant
    equation closes the branch; a single-monomial equation all of whose factors
    are known nonzero closes it; one with a single unknown factor forces that
    factor to zero; a polynomial with a known-nonzero common variable factor
    may be divided by it; an equation c*v + P = 0 with c a nonzero rational and
    v absent from P eliminates v.  Branching splits a single-monomial equation
    into its factors, or an equation with a common variable factor v into
    v = 0 and (v != 0, cofactor = 0).
    """

    __slots__ = ("eqs", "nz", "sub", "nzvars", "occ", "dirty")

    def __init__(self, eqs, nz=None, sub=None, nzvars=None, occ=None,
                 dirty=None):
        self.eqs = eqs
        self.nz = nz if nz is not None else {}
        self.sub = sub if sub is not None else {}
        self.nzvars = nzvars if nzvars is not None else frozenset()
        self.occ = occ
        self.dirty = dirty if dirty is not None else set(eqs)

    def copy(self):
        return State(dict(self.eqs), dict(self.nz), dict(self.sub), self.nzvars,
                     {v: set(s) for v, s in self.occ.items()}
                     if self.occ is not None else None, set(self.dirty))

    def build_occ(self):
        occ = {}
        for k, p in self.eqs.items():
            for v in poly_vars(p):
                occ.setdefault(v, set()).add(k)
        self.occ = occ
        return occ


def _check(p):
    if p and not any(m for m in p):
        raise Contradiction("nonzero constant equation")


def apply_map(state, sub):
    if not sub:
        return
    occ = state.occ if state.occ is not None else state.build_occ()
    keys = set()
    for v in sub:
        keys |= occ.pop(v, set())
    for k in keys:
        p = state.eqs.get(k)
        if p is None:
            continue
        before = poly_vars(p)
        q = substitute(p, sub)
        _check(q)
        if q:
            state.eqs[k] = q
            after = poly_vars(q)
            for u in before - after:
                if u in occ:
                    occ[u].discard(k)
            for u in after - before:
                occ.setdefault(u, set()).add(k)
            state.dirty.add(k)
        else:
            del state.eqs[k]
            for u in before:
                if u in occ:
                    occ[u].discard(k)
            state.dirty.discard(k)
    for k in list(state.nz):
        p = state.nz[k]
        if poly_vars(p) & set(sub):
            q = substitute(p, sub)
            if not q:
                raise Contradiction("a nonzero polynomial reduced to zero")
            del state.nz[k]
            state.nz[poly_key(q)] = q
    for u in list(state.sub):
        if poly_vars(state.sub[u]) & set(sub):
            state.sub[u] = substitute(state.sub[u], sub)
    for v, e in sub.items():
        state.sub[v] = e


def register_nz(state, p):
    if not p:
        raise Contradiction("declared a zero polynomial nonzero")
    state.nz[poly_key(p)] = p
    if len(p) == 1:
        fresh = frozenset(next(iter(p))) - state.nzvars
        if fresh:
            state.nzvars = state.nzvars | fresh
            if state.occ is not None:
                for v in fresh:
                    state.dirty |= state.occ.get(v, set())


def close(state, elim_limit=60, elim_degree=4, batch=32):
    if state.occ is None:
        state.build_occ()
    while True:
        for k in sorted(state.nz):
            p = state.nz[k]
            if not p:
                raise Contradiction("a nonzero polynomial reduced to zero")
            if len(p) == 1:
                fresh = frozenset(next(iter(p))) - state.nzvars
                if fresh:
                    state.nzvars = state.nzvars | fresh
                    for v in fresh:
                        state.dirty |= state.occ.get(v, set())
        if not state.dirty:
            return state
        todo = sorted(state.dirty)
        state.dirty = set()
        forced = {}
        divides = []
        elims = []
        for k in todo:
            p = state.eqs.get(k)
            if p is None:
                continue
            _check(p)
            if len(p) == 1:
                m = next(iter(p))
                unknown = sorted(set(m) - state.nzvars)
                if not unknown:
                    raise Contradiction("a product of nonzero unknowns is zero")
                if len(unknown) == 1:
                    forced[unknown[0]] = {}
                else:
                    state.dirty.add(k)
                continue
            common = None
            for m in p:
                common = set(m) if common is None else (common & set(m))
                if not common:
                    break
            if common:
                good = sorted(common & state.nzvars)
                if good:
                    divides.append((k, good[0]))
                    continue
            for v in sorted(poly_vars(p)):
                coeff = p.get((v,))
                if not coeff:
                    continue
                if any(v in m for m in p if m != (v,)):
                    continue
                rest = {m: c for m, c in p.items() if m != (v,)}
                if len(rest) <= elim_limit and degree(rest) <= elim_degree:
                    elims.append((len(rest), degree(rest), v, k))
                break
        if forced:
            for v in forced:
                if v in state.nzvars:
                    raise Contradiction("forced a nonzero variable to zero")
            state.dirty |= {k for _, _, _, k in elims}
            state.dirty |= {k for k, _ in divides}
            apply_map(state, forced)
            continue
        if divides:
            for k, v in divides:
                p = state.eqs.get(k)
                if p is None or not all(v in m for m in p):
                    state.dirty.add(k)
                    continue
                stripped = {}
                for m, c in p.items():
                    rest = list(m)
                    rest.remove(v)
                    stripped[tuple(sorted(rest))] = c
                _check(stripped)
                state.eqs[k] = stripped
                if not any(v in m for m in stripped):
                    state.occ[v].discard(k)
                state.dirty.add(k)
            state.dirty |= {k for _, _, _, k in elims}
            continue
        if elims:
            elims.sort()
            used = set()
            done = 0
            for _, _, v, k in elims:
                if done >= batch or v in used:
                    state.dirty.add(k)
                    continue
                p = state.eqs.get(k)
                if p is None:
                    continue
                coeff = p.get((v,))
                if not coeff or any(v in m for m in p if m != (v,)):
                    state.dirty.add(k)
                    continue
                rest = {m: c for m, c in p.items() if m != (v,)}
                if poly_vars(rest) & used:
                    state.dirty.add(k)
                    continue
                expr = scale(rest, F(-1) / coeff)
                del state.eqs[k]
                for u in poly_vars(p):
                    if u in state.occ:
                        state.occ[u].discard(k)
                state.dirty.discard(k)
                if v in state.nzvars:
                    if not expr:
                        raise Contradiction("nonzero variable eliminated to 0")
                    register_nz(state, expr)
                apply_map(state, {v: expr})
                used.add(v)
                used |= poly_vars(expr)
                done += 1
            if done:
                continue
        return state


def choose_split(state):
    best = None
    for k in sorted(state.eqs):
        p = state.eqs[k]
        if len(p) != 1:
            continue
        unknown = tuple(sorted(set(next(iter(p))) - state.nzvars))
        if best is None or len(unknown) < len(best):
            best = unknown
    if best is not None:
        return ("mono", best)
    best = None
    for k in sorted(state.eqs):
        p = state.eqs[k]
        common = None
        for m in p:
            common = set(m) if common is None else (common & set(m))
            if not common:
                break
        if common:
            cand = sorted(common - state.nzvars)
            if cand:
                key = (len(p), degree(p), cand[0], k)
                if best is None or key < best:
                    best = key
    if best is not None:
        return ("factor", best[3], best[2])
    return None


def search(state, node_limit=200000, depth_limit=400):
    """Exhaustive DFS.  Returns (nodes, undecided leaves, solution leaves)."""
    try:
        close(state)
    except Contradiction:
        return 1, 0, 0
    stack = [(state, 0)]
    nodes = undecided = solved = 0
    while stack:
        st, depth = stack.pop()
        nodes += 1
        if nodes > node_limit or depth > depth_limit:
            undecided += 1
            continue
        if not st.eqs:
            solved += 1
            continue
        split = choose_split(st)
        if split is None:
            undecided += 1
            continue
        if split[0] == "mono":
            factors = split[1]
            require(factors, "branching on an empty factor list")
            seen = []
            for v in factors:
                child = st.copy()
                for u in seen:
                    register_nz(child, {(u,): F(1)})
                try:
                    apply_map(child, {v: {}})
                    close(child)
                except Contradiction:
                    seen.append(v)
                    continue
                stack.append((child, depth + 1))
                seen.append(v)
        else:
            _, k, v = split
            for action in (0, 1):
                child = st.copy()
                try:
                    if action:
                        register_nz(child, {(v,): F(1)})
                    else:
                        apply_map(child, {v: {}})
                    close(child)
                except Contradiction:
                    continue
                stack.append((child, depth + 1))
    return nodes, undecided, solved


def infeasible(eqs, zeros=(), nonzeros=(), node_limit=200000):
    """True iff an exhaustive search closes every branch."""
    st = State(dict(eqs))
    st.build_occ()
    try:
        apply_map(st, {vid(n): {} for n in zeros})
        for n in nonzeros:
            register_nz(st, {(vid(n),): F(1)})
        close(st)
    except Contradiction:
        return True, 1, 0, 0
    nodes, und, sol = search(st, node_limit=node_limit)
    return (und == 0 and sol == 0), nodes, und, sol


# ===========================================================================
# checks
# ===========================================================================
GUARD_POINT = {("d", 0, 1): F(1)}
WITNESS = {("d", 1, 0): F(-1), ("q", 0, 1, 5): F(1), ("q", 0, 2, 3): F(1),
           ("p", 0, 0, 0): F(1), ("s", 0, 4, 0): F(1)}
SEVEN = [(i, j) for i in COLORS for j in COLORS if i != j] + [(2, 2)]
ALLNINE = [(i, j) for i in COLORS for j in COLORS]


def audit_normalisation():
    require(len(matchings(SITES)) == 15, "all-ones six-site hafnian is not 15")
    require(len(matchings((0, 1, 2, 3))) == 3, "four-site hafnian is not 3")
    require(len(matchings((0, 1))) == 1, "two-site hafnian is not 1")


def audit_model(cross):
    require(len(cross) == 6438, ("cross-colour system size", len(cross)))
    kinds = {}
    for name in NAMES:
        if name[0] == "X":
            key = ("cross-2mixed" if (name[3] == PURE) != (name[4] == PURE)
                   else "cross-01")
        else:
            key = name[0]
        kinds[key] = kinds.get(key, 0) + 1
    require(kinds == {"d": 9, "p": 36, "s": 36, "q": 30,
                      "cross-2mixed": 60, "cross-01": 30},
            ("unknown census", sorted(kinds.items())))
    ledger = sorted((i, j, w, v) for (i, j, w), p in cross.items()
                    for v in (evaluate(p, GUARD_POINT),) if v)
    require(ledger == [(0, 0, (0,) * 6, F(-1)), (1, 1, (1,) * 6, F(-1))],
            ("guard ledger", ledger))


def gauss(rows):
    pivots = {}
    for original in rows:
        r = dict(original)
        while True:
            red = None
            for v in sorted(u for m in r if m for u in m):
                if v in pivots and r.get((v,)):
                    red = v
                    break
            if red is None:
                break
            r = add(r, scale(pivots[red], -r[(red,)]))
        live = sorted(v for m in r if m for v in m)
        if not live:
            require(not r.get(()), "inconsistent linear subsystem")
            continue
        head = live[0]
        pivots[head] = scale(r, F(1) / r[(head,)])
    resolved = {}
    for v in sorted(pivots, reverse=True):
        expr = {}
        for m, c in pivots[v].items():
            if m != (v,):
                expr = add(expr, {m: -c})
        resolved[v] = substitute(expr, resolved)
    return resolved


def audit_c1(cross):
    """The committed C1: 22 degree-one equations force 20 zeros + 2 relations."""
    system = dict(cross)
    sub = {}
    first = [k for k in sorted(system) if degree(system[k]) <= 1]
    require(len(first) == 22, ("degree-one equation count", len(first)))
    require(len({v for k in first for m in system[k] for v in m}) == 24,
            "the degree-one equations do not span 24 unknowns")
    while True:
        rows = [system[k] for k in sorted(system) if degree(system[k]) <= 1]
        if not rows:
            break
        resolved = gauss(rows)
        if not resolved:
            break
        for v in list(sub):
            sub[v] = substitute(sub[v], resolved)
        sub.update(resolved)
        fresh = {}
        for k in sorted(system):
            p = substitute(system[k], resolved)
            require(not p or any(m for m in p), ("linear closure constant", k))
            if p:
                fresh[k] = p
        system = fresh
    zeros = sorted(NAMES[v] for v, e in sub.items() if not e)
    require(len(zeros) == 20, ("C1 forced-zero count", len(zeros)))
    rels = sorted((NAMES[v], sorted((NAMES[m[0]], c) for m, c in e.items()))
                  for v, e in sub.items() if e)
    require(rels == [(("X", 3, 4, 2, 0), [(("X", 2, 4, 2, 0), F(-1))]),
                     (("X", 3, 4, 2, 1), [(("X", 2, 4, 2, 1), F(-1))])],
            ("C1 relations", rels))
    return sub


def cap_layers(i, j, alpha):
    u, v = P2[i], S2[j]
    internal = [[F(0) if x == y else F(Q2.get((min(x, y), max(x, y)), 0))
                 for y in SITES] for x in SITES]
    resp = [[F(0) if x == y else u[x] * v[y] + v[x] * u[y] for y in SITES]
            for x in SITES]
    out = []
    for used in range(4):
        tot = F(0)
        for m in matchings(SITES):
            for flags in product((0, 1), repeat=3):
                if sum(flags) != used:
                    continue
                term = F(1)
                for f, (x, y) in zip(flags, m):
                    term *= resp[x][y] if f else alpha * internal[x][y]
                tot += term
        out.append(tot)
    return tuple(out)


def audit_cap_table():
    live = []
    for i, j in product(COLORS, repeat=2):
        rows = {al: cap_layers(i, j, F(al)) for al in (1, 2, -3)}
        q2c, q3c = rows[1][2], rows[1][3]
        for al, layers in rows.items():
            require(layers[2] == F(al) * q2c and layers[3] == q3c,
                    ("cap layer table", i, j))
        if rows[1][0] == 0 and rows[1][1] == 0 and (q2c or q3c):
            live.append(((i, j), q2c, q3c))
    require(live == [((0, 1), F(-2), F(0)), ((0, 2), F(1, 2), F(0))],
            ("admissible caps with a nonzero class", live))


def audit_null_response(cross):
    """D1: the (0,1)/(0,2) combination that kills the direct term."""
    d01, d02 = var(("d", 0, 1)), var(("d", 0, 2))
    for word in product(COLORS, repeat=6):
        hole = holes(word)
        left = add(mul(d02, cross.get((0, 1, word), {})),
                   scale(mul(d01, cross.get((0, 2, word), {})), F(-1)))
        right = {}
        for x, y in combinations(SITES, 2):
            piece = hole[(x, y)]
            if not piece:
                continue
            ux = add(mul(d02, s_entry(1, x, word[x])),
                     scale(mul(d01, s_entry(2, x, word[x])), F(-1)))
            uy = add(mul(d02, s_entry(1, y, word[y])),
                     scale(mul(d01, s_entry(2, y, word[y])), F(-1)))
            resp = add(mul(p_entry(0, x, word[x]), uy),
                       mul(p_entry(0, y, word[y]), ux))
            if resp:
                right = add(right, mul(resp, piece))
        require(left == right, ("null-response identity fails at", word))
    a = add(d01, scale(d02, F(2)))
    b = add(d01, scale(d02, F(-2)))
    for y in SITES:
        got = add(mul(d02, const(S2[1][y])),
                  scale(mul(d01, const(S2[2][y])), F(-1)))
        want = {2: scale(b, F(-1, 2)), 3: scale(a, F(-1, 2))}.get(y, {})
        require(got == want, ("frozen part of the null response at site", y))


def nullspace(polys):
    mons = sorted({m for p in polys for m in p})
    col = {m: i for i, m in enumerate(mons)}
    n = len(polys)
    width = len(mons)
    aug = []
    for k, p in enumerate(polys):
        row = [F(0)] * width + [F(1) if i == k else F(0) for i in range(n)]
        for m, c in p.items():
            row[col[m]] = c
        aug.append(row)
    pivot = 0
    for c in range(width):
        piv = None
        for r in range(pivot, n):
            if aug[r][c]:
                piv = r
                break
        if piv is None:
            continue
        aug[pivot], aug[piv] = aug[piv], aug[pivot]
        inv = F(1) / aug[pivot][c]
        aug[pivot] = [v * inv for v in aug[pivot]]
        for r in range(n):
            if r != pivot and aug[r][c]:
                f = aug[r][c]
                aug[r] = [x - f * y for x, y in zip(aug[r], aug[pivot])]
        pivot += 1
        if pivot == n:
            break
    return [aug[r][width:] for r in range(n) if not any(aug[r][:width])]


PAIRS = [(i, j) for i in COLORS for j in COLORS]


def audit_trade_exhaustion(c1sub):
    """D2: every single-word star annihilator, and the C2 families."""
    raw = 0
    reduced = 0
    forms = {}
    for word in product(COLORS, repeat=6):
        hole = holes(word)
        plain = [star_term(i, j, word, hole) for (i, j) in PAIRS]
        if nullspace(plain):
            raw += 1
        ker = nullspace([substitute(p, c1sub) for p in plain])
        if ker:
            reduced += 1
        h = substitute(haf(SITES, word), c1sub)
        if not h:
            continue
        for vec in ker:
            forms.setdefault(tuple(vec), []).append((word, h))
    require((raw, reduced) == (125, 149),
            ("words with a nonzero star annihilator", raw, reduced))
    named = {}
    for vec, items in forms.items():
        scalars = {PAIRS[k]: c for k, c in enumerate(vec) if c}
        named[tuple(sorted(scalars.items()))] = sorted(items)
    keys = sorted(named)
    require(len(keys) == 9, ("distinct direct-scalar forms", len(keys)))
    touching = [k for k in keys if any(p in ((0, 1), (0, 2)) for p, _ in k)]
    require(len(touching) == 4, ("forms touching d_01 or d_02", touching))
    plus, minus = [], []
    for k in touching:
        coeff = dict(k)
        c1, c2 = coeff.get((0, 1), F(0)), coeff.get((0, 2), F(0))
        require(len(coeff) == 2 and c1 and c2,
                ("a d_01/d_02 form is not a combination of the two", k))
        ratio = c2 / c1
        require(ratio in (F(2), F(-2)), ("unexpected ratio", ratio))
        (plus if ratio == F(2) else minus).extend(w for w, _ in named[k])
    require(len(set(plus)) == 6 and len(set(minus)) == 6,
            ("reduced C2 family sizes", len(set(plus)), len(set(minus))))
    for word in set(plus) | set(minus):
        require(word[0] == PURE and word[1] == PURE,
                ("a C2 word is not colour 2 at sites 0 and 1", word))
    return sorted(set(plus)), sorted(set(minus))


def audit_c2_identity(cross):
    """The committed C2 identity, re-derived: fifteen words in each sign."""
    d01, d02 = var(("d", 0, 1)), var(("d", 0, 2))
    families = {}
    for lam in (F(2), F(-2)):
        scalar = add(d01, scale(d02, lam))
        found = []
        for word in product(COLORS, repeat=6):
            left = add(cross.get((0, 1, word), {}),
                       scale(cross.get((0, 2, word), {}), lam))
            if left == mul(scalar, haf(SITES, word)):
                found.append(word)
        families[lam] = sorted(found)
        require(len(found) == 15, ("C2 family size", lam, len(found)))
    for lam, pinned in ((F(2), 3), (F(-2), 2)):
        want = sorted(w for w in product(COLORS, repeat=6)
                      if w[0] == PURE and w[1] == PURE and w[pinned] == PURE
                      and (w[4] == PURE or w[5] == PURE))
        require(families[lam] == want, ("C2 family shape", lam))
    for colour in (0, 1):
        w = tuple(colour if x == 2 else PURE for x in SITES)
        require(haf(SITES, w) == var(("X", 2, 3, colour, PURE)),
                ("site-2 flip hafnian", colour))
        w = tuple(colour if x == 3 else PURE for x in SITES)
        require(haf(SITES, w) == var(("X", 2, 3, PURE, colour)),
                ("site-3 flip hafnian", colour))
    return families


def loc_edges(sites):
    out = []
    for name in NAMES:
        if name[0] != "X":
            continue
        x, y, cx, cy = name[1], name[2], name[3], name[4]
        if (cx == PURE) == (cy == PURE):
            continue
        if (x if cx != PURE else y) in sites:
            out.append(name)
    return out            # the model's own construction order, deterministic


def audit_engine_sanity():
    """Two satisfiable systems the engine must not close, three it must."""
    seven = build_system(False, SEVEN)
    bad = [k for k, p in seven.items() if evaluate(p, GUARD_POINT)]
    require(not bad, ("the guard fails a seven-row equation", bad[:3]))
    ok, nodes, und, sol = infeasible(seven, node_limit=40000)
    require(not ok and sol > 0,
            ("the engine wrongly closed the satisfiable seven-row system",
             nodes, und, sol))
    withpure = build_system(False, SEVEN, extra_pure=[(0, 0)])
    bad = [k for k, p in withpure.items() if evaluate(p, WITNESS)]
    require(not bad, ("the witness fails an equation", bad[:3]))
    ok, nodes, und, sol = infeasible(withpure, node_limit=40000)
    require(not ok, "the engine wrongly closed the satisfiable witness system")
    for extra, tag in (([(0, 0)], "colour-0 anchor"), ([(1, 1)], "colour-1"),
                       (None, "nine-row")):
        labels = ALLNINE if extra is None else SEVEN + extra
        ok, nodes, und, sol = infeasible(build_system(False, labels))
        require(ok, ("the monochromatic %s system did not close" % tag,
                     nodes, und, sol))
    ALLOW_CROSS[0] = True


def audit_localisation(cross):
    """D3: L2 alone closes the system, and so does L3 alone."""
    out = {}
    for tag, sites in (("L2", {2}), ("L3", {3})):
        edges = loc_edges(sites)
        require(len(edges) == 10, ("localisation family size", tag, len(edges)))
        ok, nodes, und, sol = infeasible(cross, zeros=edges)
        require(ok, ("%s alone did not close the system" % tag, nodes, und, sol))
        out[tag] = nodes
    return out


def audit_class_vanishing(cross, lo, hi):
    """D4: each of the two C2 hypotheses closes the whole system."""
    L2, L3 = loc_edges({2}), loc_edges({3})
    done = 0
    totals = {}
    for tag, kill in (("A", [("X", 2, 3, c, PURE) for c in (0, 1)]),
                      ("B", [("X", 2, 3, PURE, c) for c in (0, 1)])):
        fam2 = [n for n in L2 if n not in kill]
        fam3 = [n for n in L3 if n not in kill]
        nodes = 0
        for i, j in product(range(len(fam2)), range(len(fam3))):
            index = (0 if tag == "A" else 80) + i * len(fam3) + j
            if not (lo <= index < hi):
                continue
            zeros = kill + fam2[:i] + fam3[:j]
            ok, n, und, sol = infeasible(cross, zeros=zeros,
                                         nonzeros=[fam2[i], fam3[j]])
            require(ok, ("branch %d of case %s survived" % (index, tag),
                         n, und, sol))
            nodes += n
            done += 1
        totals[tag] = nodes
    return done, totals


def main():
    argv = [a for a in sys.argv[1:]]
    lo, hi = (int(argv[0]), int(argv[1])) if len(argv) >= 2 else (0, 160)
    t0 = time.time()
    audit_normalisation()
    cross = build_system(True)
    audit_model(cross)
    c1sub = audit_c1(cross)
    audit_cap_table()
    audit_null_response(cross)
    families = audit_c2_identity(cross)
    plus, minus = audit_trade_exhaustion(c1sub)
    require(set(plus) <= set(families[F(2)]) and
            set(minus) <= set(families[F(-2)]),
            "the reduced trade families are not inside the C2 families")
    audit_engine_sanity()
    loc = audit_localisation(cross)
    done, totals = audit_class_vanishing(cross, lo, hi)
    print(
        "PASS: on the frozen colour-2 slice the (0,1)/(0,2) rows give a null "
        "response u = d_02 s_1 - d_01 s_2 annihilating the four-hole pairing at "
        "all 729 words, with frozen part -(b/2)e_2-(a/2)e_3 and chi != 0 iff "
        "(a,b) != (0,0); the single-word trade mechanism is exhausted at C2's "
        "two six-word families (%d words carry a star annihilator, %d after the "
        "C1 reduction, nine direct forms, only d_01 +- 2d_02 touch the "
        "class); killing the ten 2-mixed edges whose non-2 colour sits at "
        "site 2 closes the whole 9x729 system "
        "(%d nodes) and so does the site-3 mirror (%d nodes), halving C3; and "
        "each of the two-edge hypotheses q(2@c,3@2)=0 and q(2@2,3@c)=0 closes "
        "it as well over %d/160 localisation branches (%d + %d nodes), so the "
        "edge {2,3} is live in both 2-mixed orientations in every completion, "
        "whence by C2 every cross-colour completion of this slice has "
        "d_01 = d_02 = 0 and chi = 0 on every admissible cap."
        % (125, 149, loc["L2"], loc["L3"], done, totals["A"], totals["B"]))
    sys.stderr.write("elapsed %.0fs\n" % (time.time() - t0))


if __name__ == "__main__":
    main()
