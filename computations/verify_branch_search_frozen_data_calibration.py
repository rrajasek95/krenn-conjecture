#!/usr/bin/env python3
"""Calibration: the monomial branch search needs frozen data to start at all.

Most h=3 infeasibility results in the star-sector artifacts are produced by the
same decision procedure -- propagate equations that reduce to a single
repeated variable, then split single-monomial equations into their factors.
This checker measures where that procedure has traction, and benchmarks it
against a case whose answer is already proved.

  B1  With the seven-row guard's colour-2 slice frozen, the h=3 system has
      346 equations that are already a single monomial, the collapse cascades
      from them, and the search closes the system outright.
  B2  With nothing frozen, the h=3 monochromatic system has ZERO.  The search
      terminates immediately: one node, one open leaf, nothing decided.
  B3  The same at h=2 -- six vertices, four residual sites -- in both the
      monochromatic and the fully general model: zero single-monomial
      equations, one node, one open leaf.
  B4  Every generator of an unfrozen system has at least two terms, which is
      why: the procedure's only entry point is a one-term equation.

Exceptions to "most": the colour-1 result of the pure-word anchor note is an
explicit ideal-membership certificate, and C1/C2 of the cross-colour note are
formal identities -- neither uses this search.  The cross-colour search also
adds linear elimination and nonzero reasoning, so it is a strictly stronger
procedure than the one measured here.

B3 is the calibration that matters.  At six vertices the obstruction is
PROVED -- see proofs/six-site-arbitrary-complex-obstruction.md, no six-vertex
three-colour GHZ realization exists over arbitrary complex matrices -- so that
system is infeasible and the search still sees nothing.  The procedure is
therefore strictly weaker than an already-proved theorem ON THIS BENCHMARK:
it fails to decide a system the theorem decides.  The converse does not hold
-- with a frozen slice it closes eight-vertex systems the six-site theorem
does not address -- so the two are not comparable in general.

Consequence, and the reason this is worth recording: the committed h=3
infeasibility statements THAT THIS SEARCH PRODUCES are scope-limited to their
frozen slice as a matter of method, not merely of write-up.  "Scope-limited"
rather than "conditional": a theorem about a restricted system is
unconditionally true of that system.  A general attack needs different machinery.

This says nothing about whether any of these systems is feasible.  It is a
statement about the tool.  No certified dependency is changed; Krenn's
conjecture remains open.  Standard library only, exact Fraction arithmetic.
"""

from fractions import Fraction as Q
from itertools import combinations, product


def require(condition, message):
    if not condition:
        raise AssertionError(message)


COLORS = (0, 1, 2)

# the frozen colour-2 slice of the audited seven-row guard
Q2 = {(0, 1): Q(1), (4, 5): Q(1)}
P2 = {0: (Q(1), Q(1), Q(0), Q(0), Q(0), Q(0)),
      1: (Q(0), Q(0), Q(0), Q(0), Q(1), Q(0)),
      2: (Q(0), Q(0), Q(1), Q(1), Q(0), Q(0))}
S2 = {0: (Q(0), Q(0), Q(0), Q(0), Q(0), Q(1)),
      1: (Q(0), Q(0), Q(1), Q(-1), Q(0), Q(0)),
      2: (Q(0), Q(0), Q(1, 2), Q(1, 2), Q(0), Q(0))}


_MATCH = {}


def matchings(vertices):
    vertices = tuple(vertices)
    if vertices in _MATCH:
        return _MATCH[vertices]
    if not vertices:
        answer = ((),)
    elif len(vertices) % 2:
        answer = ()
    else:
        first = vertices[0]
        acc = []
        for position, partner in enumerate(vertices[1:], start=1):
            remainder = vertices[1:position] + vertices[position + 1:]
            for tail in matchings(remainder):
                acc.append(((first, partner),) + tail)
        answer = tuple(acc)
    _MATCH[vertices] = answer
    return answer


class Poly:
    __slots__ = ("terms",)

    def __init__(self, terms=None):
        self.terms = {m: c for m, c in (terms or {}).items() if c}

    @staticmethod
    def const(value):
        value = Q(value)
        return Poly({(): value} if value else {})

    @staticmethod
    def var(name):
        return Poly({(name,): Q(1)})

    def __bool__(self):
        return bool(self.terms)

    def __add__(self, other):
        out = dict(self.terms)
        for m, c in other.terms.items():
            total = out.get(m, Q(0)) + c
            if total:
                out[m] = total
            else:
                out.pop(m, None)
        return Poly(out)

    def __sub__(self, other):
        return self + Poly({m: -c for m, c in other.terms.items()})

    def __mul__(self, other):
        out = {}
        for m1, c1 in self.terms.items():
            for m2, c2 in other.terms.items():
                m = tuple(sorted(m1 + m2))
                total = out.get(m, Q(0)) + c1 * c2
                if total:
                    out[m] = total
                else:
                    out.pop(m, None)
        return Poly(out)

    def kill(self, zeros):
        return Poly({m: c for m, c in self.terms.items()
                     if not any(v in zeros for v in m)})


def build(sites, frozen, monochromatic):
    """The 9 * 3^|sites| GHZ row system on the given residual sites.

    frozen=True installs the guard's colour-2 slice as constants; otherwise
    every star entry, internal edge and direct scalar is an unknown.
    """
    def q_edge(x, y, cx, cy):
        if x > y:
            x, y, cx, cy = y, x, cy, cx
        if frozen and cx == 2 and cy == 2:
            return Poly.const(Q2.get((x, y), 0))
        if monochromatic and cx != cy:
            return Poly.const(0)
        return Poly.var(("q", x, y, cx, cy))

    def p_entry(i, x, c):
        if frozen and c == 2:
            return Poly.const(P2[i][x])
        return Poly.var(("p", i, x, c))

    def s_entry(j, y, c):
        if frozen and c == 2:
            return Poly.const(S2[j][y])
        return Poly.var(("s", j, y, c))

    def haf(subset, word):
        total = Poly.const(0)
        for matching in matchings(tuple(subset)):
            term = Poly.const(1)
            for x, y in matching:
                term = term * q_edge(x, y, word[x], word[y])
                if not term:
                    break
            total = total + term
        return total

    out = {}
    for letters in product(COLORS, repeat=len(sites)):
        word = {site: letters[k] for k, site in enumerate(sites)}
        for i, j in product(COLORS, repeat=2):
            total = Poly.var(("d", i, j)) * haf(sites, word)
            for x, y in combinations(sites, 2):
                response = (p_entry(i, x, word[x]) * s_entry(j, y, word[y])
                            + p_entry(i, y, word[y]) * s_entry(j, x, word[x]))
                piece = haf(tuple(v for v in sites if v not in (x, y)), word)
                if piece:
                    total = total + response * piece
            target = Q(i == j and all(c == i for c in letters))
            out[(i, j, letters)] = total - Poly.const(target)
    return out


def branch_search(equations, cap=200):
    """The decision procedure the trade, monochromatic and transport artifacts
    use; the cross-colour search adds linear elimination and nonzero reasoning."""
    seen = set()
    stack = [frozenset()]
    leaves = []
    nodes = 0
    while stack:
        start = stack.pop()
        if start in seen:
            continue
        seen.add(start)
        nodes += 1
        if nodes > cap:
            return nodes, None
        current = set(start)
        closed = False
        while True:
            live = []
            fresh = set()
            for poly in equations:
                reduced = poly.kill(current)
                if not reduced:
                    continue
                if len(reduced.terms) == 1:
                    monomial = next(iter(reduced.terms))
                    if not monomial:
                        closed = True
                        break
                    if len(set(monomial)) == 1:
                        fresh.add(monomial[0])
                live.append(reduced)
            if closed or not fresh - current:
                break
            current |= fresh
        if closed:
            continue
        branch = None
        for reduced in live:
            if len(reduced.terms) == 1:
                factors = tuple(sorted(set(next(iter(reduced.terms))), key=repr))
                if branch is None or len(factors) < len(branch):
                    branch = factors
        if branch is None:
            leaves.append(frozenset(current))
            continue
        for factor in branch:
            stack.append(frozenset(current | {factor}))
    return nodes, leaves


def census(system):
    live = [poly for poly in system.values() if poly]
    single = [poly for poly in live if len(poly.terms) == 1]
    smallest = min(len(poly.terms) for poly in live)
    return len(live), len(single), smallest


SIX = tuple(range(6))
FOUR = tuple(range(4))


def audit_frozen_h3_has_traction():
    """B1: with the frozen slice there are 346 one-term equations to start from."""
    system = build(SIX, frozen=True, monochromatic=True)
    live, single, smallest = census(system)
    require((live, single, smallest) == (2248, 346, 1),
            ("frozen h=3 census changed", live, single, smallest))
    names = {v for poly in system.values() for m in poly.terms for v in m}
    require(len(names) == 111, ("frozen unknown count changed", len(names)))
    # C8: actually run the search on the frozen system, rather than asserting
    # in prose that the collapse cascades
    nodes, leaves = branch_search(list(system.values()), cap=100000)
    require(leaves is not None and not leaves,
            ("the frozen system did not close", nodes))


def audit_unfrozen_has_no_traction():
    """B2/B3/B4: with nothing frozen there is no entry point, at either size."""
    cases = {
        ("h=3", "monochromatic"): (SIX, True, 6561, 162),
        ("h=2", "monochromatic"): (FOUR, True, 729, 99),
        ("h=2", "general"): (FOUR, False, 729, 135),
    }
    for label, (sites, mono, want_live, want_vars) in cases.items():
        system = build(sites, frozen=False, monochromatic=mono)
        live, single, smallest = census(system)
        require(live == want_live, (label, "equation count changed", live))
        names = {v for poly in system.values() for m in poly.terms for v in m}
        require(len(names) == want_vars, (label, "unknown count changed", len(names)))
        require(single == 0,
                (label, "an unfrozen system unexpectedly has a one-term equation",
                 single))
        require(smallest >= 2,
                (label, "an unfrozen generator has fewer than two terms", smallest))
        nodes, leaves = branch_search(list(system.values()))
        require(nodes == 1 and leaves is not None and len(leaves) == 1,
                (label, "the search unexpectedly made progress", nodes, leaves))


def audit_which_slice_is_the_engine():
    """Partial freezing localizes the traction: the endpoint stars supply it,
    the internal quadratic supplies none."""
    def one_term_count(freeze_q, freeze_p, freeze_s):
        def q_edge(x, y, cx, cy):
            if x > y:
                x, y, cx, cy = y, x, cy, cx
            if freeze_q and cx == 2 and cy == 2:
                return Poly.const(Q2.get((x, y), 0))
            if cx != cy:
                return Poly.const(0)
            return Poly.var(("q", x, y, cx, cy))

        def haf(subset, word):
            total = Poly.const(0)
            for matching in matchings(tuple(subset)):
                term = Poly.const(1)
                for x, y in matching:
                    term = term * q_edge(x, y, word[x], word[y])
                    if not term:
                        break
                total = total + term
            return total

        count = 0
        for letters in product(COLORS, repeat=6):
            word = {site: letters[site] for site in SIX}
            for i, j in product(COLORS, repeat=2):
                total = Poly.var(("d", i, j)) * haf(SIX, word)
                for x, y in combinations(SIX, 2):
                    pe = (Poly.const(P2[i][x]) if (freeze_p and word[x] == 2)
                          else Poly.var(("p", i, x, word[x])))
                    se = (Poly.const(S2[j][y]) if (freeze_s and word[y] == 2)
                          else Poly.var(("s", j, y, word[y])))
                    pe2 = (Poly.const(P2[i][y]) if (freeze_p and word[y] == 2)
                           else Poly.var(("p", i, y, word[y])))
                    se2 = (Poly.const(S2[j][x]) if (freeze_s and word[x] == 2)
                           else Poly.var(("s", j, x, word[x])))
                    piece = haf(tuple(v for v in SIX if v not in (x, y)), word)
                    if piece:
                        total = total + (pe * se + pe2 * se2) * piece
                total = total - Poly.const(Q(i == j and all(c == i for c in letters)))
                if total and len(total.terms) == 1:
                    count += 1
        return count

    require(one_term_count(True, False, False) == 0,
            "freezing the internal quadratic alone unexpectedly gave traction")
    require(one_term_count(False, True, False) == 0,
            "freezing the first star alone unexpectedly gave traction")
    require(one_term_count(False, False, True) == 0,
            "freezing the second star alone unexpectedly gave traction")
    both_stars = one_term_count(False, True, True)
    require(both_stars == 336, ("freezing both stars changed", both_stars))


def audit_six_site_benchmark_is_known_infeasible():
    """B3's point: at h=2 the answer is already proved, and the search still
    sees nothing.  We do not re-prove the six-site obstruction here -- it is
    proofs/six-site-arbitrary-complex-obstruction.md -- we only record that the
    procedure fails on a system whose infeasibility is known, which is what
    makes this a calibration rather than an open question."""
    system = build(FOUR, frozen=False, monochromatic=False)
    nodes, leaves = branch_search(list(system.values()))
    require(nodes == 1 and len(leaves) == 1,
            ("the six-site benchmark unexpectedly decided", nodes, len(leaves)))
    # and the guard packet's slice really is what supplies the constants
    frozen = build(SIX, frozen=True, monochromatic=True)
    unfrozen = build(SIX, frozen=False, monochromatic=True)
    require(census(frozen)[1] > 0 and census(unfrozen)[1] == 0,
            "the frozen slice is not the source of the one-term equations")


def audit_row_multigrading():
    """Homogeneity needs TWO conditions, not one.  The row left-hand sides are
    homogeneous when w_d + w_q = w_p + w_s; but the three generators whose GHZ
    target is nonzero also carry a constant of grade 0, so the generators are
    homogeneous only if the common grade is itself zero, w_d + h*w_q = 0.  The
    family is two-parameter.  The constant monomial is counted below -- leaving
    it out is exactly what would hide the second condition."""
    system = build(SIX, frozen=False, monochromatic=True)
    weights = {"d": 0, "p": 0, "s": 0, "q": 0}

    def inhomogeneous(wd, wp, ws, wq):
        weights.update(d=wd, p=wp, s=ws, q=wq)
        count = 0
        for poly in system.values():
            grades = {sum(weights[v[0]] for v in m) if m else 0
                      for m in poly.terms}
            if len(grades) > 1:
                count += 1
        return count

    # both conditions: genuinely homogeneous generators
    for wq, wp, ws, wd in ((-1, 1, 1, 3), (-2, 2, 2, 6), (-3, 1, 5, 9)):
        require(wd + wq == wp + ws and wd + 3 * wq == 0, "bad conforming test")
        require(inhomogeneous(wd, wp, ws, wq) == 0,
                ("a fully conforming grading left inhomogeneous generators",
                 wq, wp, ws, wd))
    # first condition only: exactly the three target-bearing generators break
    for wq, wp, ws, wd in ((0, 1, 2, 3), (-2, 0, 1, 3), (5, 2, 1, -2), (1, 1, 1, 1)):
        require(wd + wq == wp + ws and wd + 3 * wq != 0, "bad partial test")
        require(inhomogeneous(wd, wp, ws, wq) == 3,
                ("first condition alone did not leave exactly the three "
                 "target-bearing generators", wq, wp, ws, wd))
    # first condition violated: exactly the 9 * 183 all-even rows break
    for wq, wp, ws, wd in ((0, 1, 1, 1), (1, 0, 0, 0), (-1, 1, 1, 2)):
        require(wd + wq != wp + ws, "control grading unexpectedly conforms")
        require(inhomogeneous(wd, wp, ws, wq) == 1647,
                ("a violating grading did not leave exactly the all-even rows",
                 wq, wp, ws, wd))


def main():
    audit_frozen_h3_has_traction()
    audit_unfrozen_has_no_traction()
    audit_six_site_benchmark_is_known_infeasible()
    audit_row_multigrading()
    audit_which_slice_is_the_engine()
    print(
        "PASS: with the guard's colour-2 slice frozen the h=3 system has 346 "
        "one-term equations and the collapse starts; with nothing frozen there "
        "are zero, at h=3 (6561 equations, 162 unknowns) and at h=2 in both the "
        "monochromatic (729, 99) and general (729, 135) models, every generator "
        "having at least two terms, and the search halts at one node with one "
        "open leaf.  At h=2 the obstruction is already proved, so on this "
        "benchmark the procedure is strictly weaker than a known theorem -- "
        "though the two are not comparable in general -- and the committed h=3 "
        "infeasibility results that this search produces are scope-limited to "
        "their frozen slice by method, not merely by wording.  "
        "The generators are homogeneous for the TWO-parameter family "
        "w_d + w_q = w_p + w_s AND w_d + h*w_q = 0; the first condition alone "
        "leaves exactly the three target-bearing generators inhomogeneous and "
        "violating it leaves exactly the 9*183 all-even rows.  Freezing the "
        "internal quadratic alone, or either star alone, gives no traction; "
        "both stars together give 336"
    )


if __name__ == "__main__":
    main()
