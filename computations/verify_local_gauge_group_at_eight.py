#!/usr/bin/env python3
"""The local gauge group of the eight-vertex ternary system, exactly.

Research evidence only.  Krenn's conjecture remains OPEN, `SP-CLEAN-BRIDGE` is
untouched, and no certified dependency changes.  Nothing here is a partial case
of the conjecture, and nothing here bears on whether (8,3) has a solution.

The repository uses three separate scaling arguments that were introduced
independently:

  * the target-stabilizing torus of ``notes/combinatorial-route.md`` section 4,
    X_uv(i,j) -> lambda_{u,i} lambda_{v,j} X_uv(i,j) under prod_v lambda_{v,i}
    = 1;
  * the tau-weight grading of
    ``notes/terminal-class-weight-invisibility-and-fourhole-grade-ladder.md``,
    q -> q/tau, p -> tau p, s -> tau s, d -> tau^3 d, which fixes the matching
    tensor while chi -> tau^6 chi;
  * the endpoint torus of
    ``notes/cap-line-cubic-and-why-the-landing-is-inactive.md`` section 5,
    lambda_{p,l} = g_l, lambda_{q,m} = g_m^{-1}, lambda_{u,c} = 1, which sends
    z -> (g_i/g_j) z on a cap line.

This checker proves they are one object: all three are one-parameter subgroups
of the SAME group, whose identity component is computed here exactly and shown
to be a torus of dimension 21.

    G  =  { (g_0, ..., g_7) in GL_3(C)^8 : (g_0 (x) ... (x) g_7) Delta = Delta }

with Delta = Delta_{8,3} = sum_c e_c^{(x)8} the GHZ target.

  G1  EQUIVARIANCE.  A_uv -> g_u A_uv g_v^T sends the matching tensor H(A) to
      (g_0 (x) ... (x) g_7) H(A).  This holds precisely because a perfect
      matching covers each vertex exactly once, and it is what makes G the
      gauge group of the problem rather than an unrelated symmetry.  Verified
      as a formal polynomial identity in all weight and all group entries at
      N = 4, and numerically at N = 8.

  G2  THE IDENTITY COMPONENT IS A 21-TORUS.  The infinitesimal stabilizer
      Lie(G) = { (X_v) in gl_3(C)^8 : sum_v (I (x) .. X_v .. (x) I) Delta = 0 }
      is computed by exact rational linear algebra on the full 6561 x 72
      system built mechanically from the definition -- no hand-derived
      equations.  Its dimension is

          8 * 3 - 3 = 21,

      and the solution space is exactly

          { X_v diagonal for every v, and sum_v (X_v)_cc = 0 for each colour c }.

      So every infinitesimal gauge transformation is diagonal.  In char 0 the
      Lie algebra of a closed subgroup determines its identity component, so
      G^0 is the torus of ``combinatorial-route.md`` (8).  Relayed, not proved
      here: the full G is that torus extended by the colour permutations S_3,
      by Kruskal uniqueness of the GHZ rank-3 decomposition.

  G3  THE ACTION ON WEIGHTS, AND THE EFFECTIVE DIMENSION.  The torus acts on
      the 28 * 9 = 252 weight entries by A_e(i,j) -> lambda_{u,i} lambda_{v,j}
      A_e(i,j).  Its kernel on a fully supported packet is exactly {+-1}:
      lambda acts trivially iff lambda_{u,i} lambda_{v,j} = 1 for every u != v
      and every i, j; varying j makes lambda_{v,j} = mu_v independent of the
      colour, and mu_u mu_v = 1 for all u != v forces (using n >= 3) all mu_v
      equal to a common eps with eps^2 = 1.  The product condition is then
      automatic, since eps^8 = 1.

      That kernel is FINITE, so it costs no dimension: generic orbits have
      dimension 21 and

          252 - 21 = 231

      is the effective parameter count after gauge fixing.  Both halves are
      verified exactly -- the infinitesimal kernel { h : h(u,i) + h(v,j) = 0
      for all u != v, i, j } is computed and is zero, and the rank of the
      infinitesimal action on fully supported packets is 21.

  G4  ALL THREE KNOWN SCALINGS ARE ONE-PARAMETER SUBGROUPS OF THIS TORUS.
      Writing lambda_{v,i} = t^{h(v,i)}, membership is exactly
      sum_v h(v,i) = 0 for each colour i.
        * tau-weight: h(site, i) = +1 for the six residual sites and
          h(endpoint, i) = -3 for the two endpoints, colour-independent.
          Then q -> t^2 q, p, s -> t^-2 p, s and d -> t^-6 d, which is the
          published grading at tau = t^-2, and sum_v h = 6 - 6 = 0.
        * endpoint torus: h(LEFT, l) = a_l, h(RIGHT, m) = -a_m, h(site, c) = 0.
          sum_v h(., i) = a_i - a_i = 0.
      Both verified to fix all 6561 target coefficients and to reproduce their
      published effect on the chart weights.

  G5  WHAT MAY BE NAMED -- and the trap in stating it.

      Grading a monomial by its site-colour multidegree D in Z^{8 x 3} -- the
      exponent of lambda_{v,i} -- the torus character of a monomial is D
      itself, and D is trivial on G^0 exactly when D(v, i) is independent of v.
      That equivalence is correct and is verified below.

      IT DOES NOT GIVE A CRITERION FOR BEING A FUNCTION OF THE MATCHING TENSOR.
      G^0 stabilizes Delta, not H(A).  A function of H is EQUIVARIANT, not
      invariant, so it need not be G^0-invariant at all.  The counterexample is
      inside the object itself: F(A) = H(A)[iota] for any NON-CONSTANT iota is
      a coordinate of the matching tensor, hence a function of it, and its
      multidegree D(v,i) = [iota_v = i] is not constant in v.  6558 of the 6561
      coordinates of H are counterexamples.  Verified below.

      The correct global statement uses the subgroup that fixes EVERY
      coefficient of H, i.e. { h : sum_v h(v, iota_v) = 0 for all 3^8 words }.
      Solving that exactly gives rank 17 of 24, so the subgroup is

          { h colour-independent, sum_v h(v) = 0 },      dimension 7,

      which is exactly the one-parameter family the tau-weight note used, at
      full strength.  Its characters are trivial precisely on multidegrees
      whose PER-VERTEX TOTAL degree is constant in v.  So:

          F a function of the matching tensor ==> every monomial of F has
          per-vertex total degree constant in v.

      chi has per-vertex total degree (1,1,1,1,1,1,3,3) and fails this, so the
      weight note's conclusion survives -- no landing theorem can produce a
      formula or a bound for chi, only a vanishing statement.  What does NOT
      survive is the claim that the full 21-torus gives that conclusion.

      The 21-torus does say something, but only ON THE SOLUTION LOCUS: G^0
      preserves { H(A) = Delta }, so a polynomial constant there has each of
      its non-trivially-graded components vanishing there.

Standard library only, exact Fraction arithmetic, no floats, no numpy.  Every
check raises rather than asserts, so ``python3 -O`` performs all of them.
"""

from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import combinations, product


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


COLORS = (0, 1, 2)
D = 3


# ----------------------------------------------------------------------
# perfect matchings and the matching tensor, from the definition
# ----------------------------------------------------------------------


def perfect_matchings(vertices):
    """Every perfect matching of the complete graph on ``vertices``."""

    if not vertices:
        yield ()
        return
    head, rest = vertices[0], vertices[1:]
    for k in range(len(rest)):
        pair = (head, rest[k])
        for tail in perfect_matchings(rest[:k] + rest[k + 1:]):
            yield (pair,) + tail


def matching_tensor(weights, n, d):
    """H(A)[iota] = sum over perfect matchings of prod A_uv[iota_u][iota_v]."""

    verts = tuple(range(n))
    matchings = tuple(perfect_matchings(verts))
    out = {}
    for iota in product(range(d), repeat=n):
        total = None
        for m in matchings:
            term = None
            for u, v in m:
                factor = weights[(u, v)][iota[u]][iota[v]]
                term = factor if term is None else term * factor
            total = term if total is None else total + term
        out[iota] = total
    return out


def ghz(n, d):
    return {
        iota: (1 if len(set(iota)) == 1 else 0)
        for iota in product(range(d), repeat=n)
    }


# ----------------------------------------------------------------------
# a tiny exact polynomial ring over Fraction, for the formal identities
# ----------------------------------------------------------------------


class Poly:
    """Sparse multivariate polynomial: monomial (sorted var tuple) -> coeff."""

    __slots__ = ("t",)

    def __init__(self, terms=None):
        self.t = {}
        if terms:
            for mono, coeff in terms.items():
                if coeff:
                    self.t[mono] = coeff

    @staticmethod
    def var(name):
        return Poly({(name,): F(1)})

    @staticmethod
    def const(value):
        value = F(value)
        return Poly({(): value}) if value else Poly()

    def __add__(self, other):
        out = dict(self.t)
        for mono, coeff in other.t.items():
            new = out.get(mono, F(0)) + coeff
            if new:
                out[mono] = new
            else:
                out.pop(mono, None)
        return Poly(out)

    def __sub__(self, other):
        out = dict(self.t)
        for mono, coeff in other.t.items():
            new = out.get(mono, F(0)) - coeff
            if new:
                out[mono] = new
            else:
                out.pop(mono, None)
        return Poly(out)

    def __mul__(self, other):
        out = {}
        for m1, c1 in self.t.items():
            for m2, c2 in other.t.items():
                mono = tuple(sorted(m1 + m2))
                new = out.get(mono, F(0)) + c1 * c2
                if new:
                    out[mono] = new
                else:
                    out.pop(mono, None)
        return Poly(out)

    def is_zero(self):
        return not self.t

    def __eq__(self, other):
        return self.t == other.t


# ----------------------------------------------------------------------
# exact linear algebra over Fraction
# ----------------------------------------------------------------------


def rref(rows, ncols):
    """Reduced row echelon form; returns (matrix, pivot column list)."""

    mat = [list(r) for r in rows if any(r)]
    pivots = []
    r = 0
    for c in range(ncols):
        piv = None
        for i in range(r, len(mat)):
            if mat[i][c]:
                piv = i
                break
        if piv is None:
            continue
        mat[r], mat[piv] = mat[piv], mat[r]
        inv = F(1) / mat[r][c]
        mat[r] = [x * inv for x in mat[r]]
        for i in range(len(mat)):
            if i != r and mat[i][c]:
                f = mat[i][c]
                mat[i] = [a - f * b for a, b in zip(mat[i], mat[r])]
        pivots.append(c)
        r += 1
        if r == len(mat):
            break
    return mat[:r], pivots


def nullspace_basis(rows, ncols):
    mat, pivots = rref(rows, ncols)
    free = [c for c in range(ncols) if c not in pivots]
    basis = []
    for f in free:
        vec = [F(0)] * ncols
        vec[f] = F(1)
        for i, p in enumerate(pivots):
            vec[p] = -mat[i][f]
        basis.append(vec)
    return basis, pivots


# ----------------------------------------------------------------------
# G1: equivariance of the matching tensor under the local group
# ----------------------------------------------------------------------


def audit_G1_equivariance_formal(n=4, d=2):
    """H(g.A) = (g_0 (x) ... (x) g_{n-1}) H(A), as a polynomial identity.

    Every weight entry and every group entry is a distinct formal variable.
    """

    verts = tuple(range(n))
    weights = {}
    for u, v in combinations(verts, 2):
        weights[(u, v)] = [
            [Poly.var(f"A_{u}{v}_{i}{j}") for j in range(d)] for i in range(d)
        ]
    g = [
        [[Poly.var(f"g{v}_{a}{i}") for i in range(d)] for a in range(d)]
        for v in verts
    ]

    transformed = {}
    for u, v in combinations(verts, 2):
        block = [[Poly() for _ in range(d)] for _ in range(d)]
        for a in range(d):
            for b in range(d):
                acc = Poly()
                for i in range(d):
                    for j in range(d):
                        acc = acc + g[u][a][i] * weights[(u, v)][i][j] * g[v][b][j]
                block[a][b] = acc
        transformed[(u, v)] = block

    left = matching_tensor(transformed, n, d)
    base = matching_tensor(weights, n, d)

    checked = 0
    for iota in product(range(d), repeat=n):
        right = Poly()
        for kappa in product(range(d), repeat=n):
            coeff = Poly.const(1)
            for v in verts:
                coeff = coeff * g[v][iota[v]][kappa[v]]
            right = right + coeff * base[kappa]
        require(
            left[iota] == right,
            f"equivariance fails at n={n} d={d} index {iota}",
        )
        checked += 1
    require(checked == d ** n, "wrong number of indices checked")
    require(
        any(base[iota].t for iota in base),
        "the base tensor is identically zero -- the identity would be vacuous",
    )
    return checked


class LCG:
    """Deterministic integer generator; no dependence on hash seed or time."""

    def __init__(self, seed):
        self.state = seed & ((1 << 64) - 1)

    def next(self, bound):
        self.state = (6364136223846793005 * self.state + 1442695040888963407)
        self.state &= (1 << 64) - 1
        return (self.state >> 33) % bound


def random_packet(gen, n=8, d=3, lo=-4, hi=5):
    weights = {}
    for u, v in combinations(range(n), 2):
        weights[(u, v)] = [
            [F(gen.next(hi - lo) + lo) for _ in range(d)] for _ in range(d)
        ]
    return weights


def apply_local_group(tensor, g, n, d):
    """(g_0 (x) ... (x) g_{n-1}) T, applied one mode at a time.

    Mode-by-mode keeps the cost at n * d^{n+1} instead of d^{2n}; at n = 8
    that is the difference between 160 thousand and 43 million products.
    """

    current = dict(tensor)
    for v in range(n):
        updated = {}
        for iota in product(range(d), repeat=n):
            acc = 0
            for c in range(d):
                value = current[iota[:v] + (c,) + iota[v + 1:]]
                if value:
                    acc += g[v][iota[v]][c] * value
            updated[iota] = acc
        current = updated
    return current


def audit_G1_equivariance_numeric_at_eight(trials=1):
    """Integer arithmetic; Fractions buy nothing here and cost a great deal."""

    gen = LCG(20260801)
    for trial in range(trials):
        weights = {
            e: [[gen.next(9) - 4 for _ in range(D)] for _ in range(D)]
            for e in combinations(range(8), 2)
        }
        g = [
            [[gen.next(7) - 3 for _ in range(D)] for _ in range(D)]
            for _ in range(8)
        ]
        transformed = {}
        for u, v in combinations(range(8), 2):
            block = [[0] * D for _ in range(D)]
            for a in range(D):
                for b in range(D):
                    acc = 0
                    for i in range(D):
                        for j in range(D):
                            acc += g[u][a][i] * weights[(u, v)][i][j] * g[v][b][j]
                    block[a][b] = acc
            transformed[(u, v)] = block
        left = matching_tensor(transformed, 8, D)
        base = matching_tensor(weights, 8, D)
        require(
            any(base[iota] for iota in base),
            "the base tensor vanished; the numeric check would be vacuous",
        )
        right = apply_local_group(base, g, 8, D)
        for iota in left:
            require(
                left[iota] == right[iota],
                f"numeric equivariance fails, trial {trial}, index {iota}",
            )
    return trials


# ----------------------------------------------------------------------
# G2: the infinitesimal stabilizer of Delta_{8,3}
# ----------------------------------------------------------------------


def audit_G2_infinitesimal_stabilizer(n=8, d=3):
    """Solve  sum_v (I (x) .. X_v .. (x) I) Delta = 0  exactly.

    The 6561 equations are built mechanically from the definition; none is
    derived by hand.  Unknown (v, a, b) is the entry (X_v)_{ab}, at column
    index v*d*d + a*d + b.
    """

    target = ghz(n, d)
    ncols = n * d * d

    def col(v, a, b):
        return v * d * d + a * d + b

    rows = []
    for iota in product(range(d), repeat=n):
        row = [F(0)] * ncols
        nonzero = False
        for v in range(n):
            for c in range(d):
                shifted = iota[:v] + (c,) + iota[v + 1:]
                if target[shifted]:
                    row[col(v, iota[v], c)] += F(1)
                    nonzero = True
        if nonzero:
            rows.append(row)
    require(rows, "no equations were generated")

    basis, pivots = nullspace_basis(rows, ncols)
    dim = len(basis)
    require(
        dim == n * d - d,
        f"stabilizer dimension is {dim}, expected {n * d - d}",
    )

    # the solution space is exactly {X_v diagonal, sum_v (X_v)_cc = 0}
    for vec in basis:
        for v in range(n):
            for a in range(d):
                for b in range(d):
                    if a != b:
                        require(
                            vec[col(v, a, b)] == 0,
                            "a nullspace element has an off-diagonal entry",
                        )
        for c in range(d):
            total = sum(vec[col(v, c, c)] for v in range(n))
            require(total == 0, "a nullspace element fails the trace condition")

    # and conversely every such matrix is in the nullspace
    explicit = []
    for c in range(d):
        for v in range(1, n):
            vec = [F(0)] * ncols
            vec[col(0, c, c)] = F(1)
            vec[col(v, c, c)] = F(-1)
            explicit.append(vec)
    require(
        len(explicit) == n * d - d,
        "wrong number of explicit generators",
    )
    _, exp_pivots = rref(explicit, ncols)
    require(
        len(exp_pivots) == dim,
        "the explicit generators do not span the nullspace",
    )
    for vec in explicit:
        for row in rows:
            require(
                sum(a * b for a, b in zip(row, vec)) == 0,
                "an explicit diagonal generator is not in the stabilizer",
            )

    # Negative controls.  Without these the dimension count could be produced
    # by an accidentally vacuous system, which is the failure mode that makes a
    # linear-algebra audit worthless.
    #
    # (a) a single off-diagonal elementary matrix must be excluded;
    probe = [F(0)] * ncols
    probe[col(0, 1, 0)] = F(1)
    require(
        any(sum(a * b for a, b in zip(row, probe)) for row in rows),
        "an off-diagonal elementary matrix was not excluded -- system is weak",
    )
    # (b) a diagonal matrix violating the trace condition must be excluded;
    probe = [F(0)] * ncols
    probe[col(0, 0, 0)] = F(1)
    require(
        any(sum(a * b for a, b in zip(row, probe)) for row in rows),
        "a trace-violating diagonal matrix was not excluded",
    )
    # (c) every off-diagonal elementary matrix, at every vertex, is excluded.
    excluded = 0
    for v in range(n):
        for a in range(d):
            for b in range(d):
                if a == b:
                    continue
                probe = [F(0)] * ncols
                probe[col(v, a, b)] = F(1)
                require(
                    any(sum(x * y for x, y in zip(row, probe)) for row in rows),
                    f"off-diagonal ({v},{a},{b}) was not excluded",
                )
                excluded += 1
    require(
        excluded == n * d * (d - 1),
        "wrong number of off-diagonal probes",
    )
    return dim, len(rows)


# ----------------------------------------------------------------------
# G3: the action on weights, its kernel, and the effective dimension
# ----------------------------------------------------------------------


def audit_G3_weight_action(n=8, d=3):
    """Infinitesimal action on the 252 weight entries has rank 21."""

    edges = tuple(combinations(range(n), 2))
    entries = [(e, i, j) for e in edges for i in range(d) for j in range(d)]
    require(
        len(entries) == 252,
        f"weight count is {len(entries)}, expected 252",
    )

    # torus parameters h(v, i); the constraint is sum_v h(v, i) = 0
    params = [(v, i) for v in range(n) for i in range(d)]
    pindex = {p: k for k, p in enumerate(params)}

    # d/dt of  A_e(i,j) * t^{h(u,i) + h(v,j)}  at a generic packet: the
    # infinitesimal action sends A_e(i,j) to (h(u,i) + h(v,j)) A_e(i,j).
    # Its matrix, restricted to the constrained subspace, has rank = orbit dim.
    constraint_rows = []
    for i in range(d):
        row = [F(0)] * len(params)
        for v in range(n):
            row[pindex[(v, i)]] = F(1)
        constraint_rows.append(row)
    tangent, _ = nullspace_basis(constraint_rows, len(params))
    require(
        len(tangent) == n * d - d and n * d - d == 21,
        f"constrained torus has dimension {len(tangent)}, expected 21",
    )

    gen = LCG(777001)
    weights = random_packet(gen)
    for e in edges:
        for i in range(d):
            for j in range(d):
                if weights[e][i][j] == 0:
                    weights[e][i][j] = F(1)  # keep the packet fully supported

    def orbit_dimension(packet):
        action_rows = []
        for h in tangent:
            row = []
            for (u, v), i, j in entries:
                scale = h[pindex[(u, i)]] + h[pindex[(v, j)]]
                row.append(scale * packet[(u, v)][i][j])
            action_rows.append(row)
        _, pivots = rref(action_rows, len(entries))
        return len(pivots)

    measured = orbit_dimension(weights)
    require(measured == 21, f"orbit dimension is {measured}, expected 21")
    for trial in range(4):
        other = random_packet(gen)
        for e in edges:
            for i in range(d):
                for j in range(d):
                    if other[e][i][j] == 0:
                        other[e][i][j] = F(1)
        require(
            orbit_dimension(other) == 21,
            f"orbit dimension dropped on random packet {trial}",
        )

    # the infinitesimal kernel on a fully supported packet is zero: the
    # equations h(u,i) + h(v,j) = 0 for every u != v and every i, j have only
    # the trivial solution, so the finite kernel {+-1} costs no dimension.
    kernel_rows = []
    for (u, v), i, j in entries:
        row = [F(0)] * len(params)
        row[pindex[(u, i)]] += F(1)
        row[pindex[(v, j)]] += F(1)
        kernel_rows.append(row)
    kernel_basis, _ = nullspace_basis(kernel_rows, len(params))
    require(
        not kernel_basis,
        f"the infinitesimal kernel has dimension {len(kernel_basis)}, not 0",
    )

    # NEGATIVE CONTROL, and it must be a real one.  "eps = -1 acts trivially"
    # is the tautology 1 * x == x and cannot fail, so it proves nothing about
    # the measurement.  Instead: degenerate packets must give a STRICTLY
    # SMALLER orbit, which demonstrates orbit_dimension can return != 21.
    dead = {e: [[F(0)] * d for _ in range(d)] for e in edges}
    require(
        orbit_dimension(dead) == 0,
        "the zero packet does not have a zero-dimensional orbit",
    )
    single = {e: [[F(0)] * d for _ in range(d)] for e in edges}
    single[edges[0]][0][0] = F(1)
    lone = orbit_dimension(single)
    require(
        lone == 1,
        f"a one-cell packet has orbit dimension {lone}, expected 1",
    )
    one_colour = {
        e: [[F(1) if (i == 0 and j == 0) else F(0) for j in range(d)]
            for i in range(d)]
        for e in edges
    }
    mono = orbit_dimension(one_colour)
    require(
        0 < mono < 21,
        f"a single-colour packet has orbit dimension {mono}, expected "
        f"strictly between 0 and 21",
    )

    require(
        len(entries) - 21 == 231,
        "effective parameter count is not 231",
    )
    return len(entries), 21


# ----------------------------------------------------------------------
# G4: the three published scalings are one-parameter subgroups
# ----------------------------------------------------------------------


SITES = tuple(range(6))
LEFT, RIGHT = 6, 7


def chart_role(u, v):
    """Which chart family the edge {u,v} belongs to."""

    ends = {u, v} & {LEFT, RIGHT}
    if not ends:
        return "q"
    if len(ends) == 2:
        return "d"
    return "p" if LEFT in ends else "s"


def audit_G4_published_subgroups(n=8, d=3):
    # tau-weight grading: h = +1 on the six sites, -3 on the two endpoints
    h_tau = {}
    for v in range(n):
        for i in range(d):
            h_tau[(v, i)] = F(1) if v in SITES else F(-3)
    for i in range(d):
        require(
            sum(h_tau[(v, i)] for v in range(n)) == 0,
            "the tau grading is not in the target-stabilizing torus",
        )
    expected = {"q": 2, "p": -2, "s": -2, "d": -6}
    for u, v in combinations(range(n), 2):
        role = chart_role(u, v)
        for i in range(d):
            for j in range(d):
                power = h_tau[(u, i)] + h_tau[(v, j)]
                require(
                    power == expected[role],
                    f"tau exponent on a {role} edge is {power}, "
                    f"expected {expected[role]}",
                )
    # published form is q -> q/tau, p, s -> tau p, tau s, d -> tau^3 d.
    # With lambda = t^h the exponents are (q, p, s, d) = (2, -2, -2, -6),
    # i.e. tau = t^-2 gives q -> tau^-1 q, p, s -> tau p, tau s, d -> tau^3 d.
    require(
        (expected["q"], expected["p"], expected["d"]) == (2, -2, -6)
        and expected["p"] == expected["s"],
        "the tau exponents do not match the published grading at tau = t^-2",
    )

    # endpoint torus: h(LEFT, l) = a_l, h(RIGHT, m) = -a_m, h(site, .) = 0
    a = {0: F(5), 1: F(-2), 2: F(3)}
    h_end = {}
    for v in range(n):
        for i in range(d):
            if v == LEFT:
                h_end[(v, i)] = a[i]
            elif v == RIGHT:
                h_end[(v, i)] = -a[i]
            else:
                h_end[(v, i)] = F(0)
    for i in range(d):
        require(
            sum(h_end[(v, i)] for v in range(n)) == 0,
            "the endpoint torus is not in the target-stabilizing torus",
        )
    # every internal edge is fixed; a p edge at label l scales by a_l
    for u, v in combinations(range(n), 2):
        role = chart_role(u, v)
        for i in range(d):
            for j in range(d):
                power = h_end[(u, i)] + h_end[(v, j)]
                if role == "q":
                    require(power == 0, "the endpoint torus moves an internal edge")
                elif role == "d":
                    lab_l = i if u == LEFT else j
                    lab_m = j if v == RIGHT else i
                    require(
                        power == a[lab_l] - a[lab_m],
                        "wrong endpoint-torus weight on a direct scalar",
                    )

    # both fix every one of the 6561 target coefficients
    target = ghz(n, d)
    for h in (h_tau, h_end):
        for iota in product(range(d), repeat=n):
            if not target[iota]:
                continue
            require(
                sum(h[(v, iota[v])] for v in range(n)) == 0,
                "a published subgroup moves a GHZ target coefficient",
            )

    # negative control: a grading that violates the product condition MUST
    # move a target coefficient, or the test above proves nothing.
    h_bad = {(v, i): (F(1) if v == 0 else F(0)) for v in range(n) for i in range(d)}
    moved = [
        iota
        for iota in product(range(d), repeat=n)
        if target[iota] and sum(h_bad[(v, iota[v])] for v in range(n)) != 0
    ]
    require(
        len(moved) == d,
        f"a product-condition violator moved {len(moved)} targets, expected {d}",
    )
    return True


# ----------------------------------------------------------------------
# G5: what a landing theorem may name
# ----------------------------------------------------------------------


def audit_G5_invariance_criterion(n=8, d=3):
    """A monomial is torus-invariant iff its multidegree is constant in v.

    The character of a monomial under lambda_{v,i} is its multidegree
    D(v, i); it is trivial on the constrained torus {sum_v h(v,i) = 0}
    exactly when D(v, i) does not depend on v.
    """

    params = [(v, i) for v in range(n) for i in range(d)]
    pindex = {p: k for k, p in enumerate(params)}
    constraint_rows = []
    for i in range(d):
        row = [F(0)] * len(params)
        for v in range(n):
            row[pindex[(v, i)]] = F(1)
        constraint_rows.append(row)
    tangent, _ = nullspace_basis(constraint_rows, len(params))

    def trivial_on_torus(deg):
        return all(
            sum(deg[pindex[p]] * h[pindex[p]] for p in params) == 0
            for h in tangent
        )

    def constant_in_v(deg):
        for i in range(d):
            values = {deg[pindex[(v, i)]] for v in range(n)}
            if len(values) > 1:
                return False
        return True

    gen = LCG(31337)
    for _ in range(200):
        deg = [F(gen.next(5)) for _ in params]
        require(
            trivial_on_torus(deg) == constant_in_v(deg),
            "the invariance criterion and the constancy test disagree",
        )

    # every target coefficient is a sum of matching monomials, each of
    # multidegree e_{v, c} summed over v -- constant in v.  Check directly.
    for c in range(d):
        deg = [F(0)] * len(params)
        for v in range(n):
            deg[pindex[(v, c)]] = F(1)
        require(
            trivial_on_torus(deg) and constant_in_v(deg),
            "a GHZ target monomial is not torus invariant",
        )

    # THE TRAP.  A coordinate of the matching tensor IS a function of it, and
    # for a non-constant word its multidegree is not constant in v.  So
    # "trivial on G^0" is NOT a necessary condition for being a function of H.
    counterexamples = 0
    for iota in product(range(d), repeat=n):
        deg = [F(0)] * len(params)
        for v in range(n):
            deg[pindex[(v, iota[v])]] += F(1)
        if len(set(iota)) == 1:
            require(constant_in_v(deg),
                    "a constant word is not constant in v")
        else:
            require(not constant_in_v(deg),
                    ("a non-constant word IS constant in v", iota))
            counterexamples += 1
    require(
        counterexamples == d ** n - d,
        f"{counterexamples} counterexamples, expected {d ** n - d}",
    )

    # THE CORRECT SUBGROUP: h fixing every coefficient of H, i.e. with
    # sum_v h(v, iota_v) = 0 for all 3^8 words.  Exactly 7-dimensional.
    fix_rows = []
    for iota in product(range(d), repeat=n):
        row = [F(0)] * len(params)
        for v in range(n):
            row[pindex[(v, iota[v])]] += F(1)
        fix_rows.append(row)
    fix_basis, fix_pivots = nullspace_basis(fix_rows, len(params))
    require(
        len(fix_basis) == n - 1,
        f"the coefficient-fixing subgroup has dimension {len(fix_basis)}, "
        f"expected {n - 1}",
    )
    require(len(fix_pivots) == 17, f"rank is {len(fix_pivots)}, expected 17")
    for vec in fix_basis:
        for v in range(n):
            values = {vec[pindex[(v, i)]] for i in range(d)}
            require(len(values) == 1,
                    "a coefficient-fixing element is colour-dependent")
        require(sum(vec[pindex[(v, 0)]] for v in range(n)) == 0,
                "a coefficient-fixing element has nonzero vertex sum")

    # THE CORRECT CRITERION: per-vertex TOTAL degree constant in v.
    def total_degree_constant(deg):
        totals = {sum(deg[pindex[(v, i)]] for i in range(d)) for v in range(n)}
        return len(totals) == 1

    # chi sits at colour 2 once per site and label degree three at each
    # endpoint, so its per-vertex total degree is (1,1,1,1,1,1,3,3).
    chi_deg = [F(0)] * len(params)
    for v in SITES:
        chi_deg[pindex[(v, 2)]] = F(1)
    chi_deg[pindex[(LEFT, 0)]] = F(3)
    chi_deg[pindex[(RIGHT, 1)]] = F(3)
    require(
        [sum(chi_deg[pindex[(v, i)]] for i in range(d)) for v in range(n)]
        == [1, 1, 1, 1, 1, 1, 3, 3],
        "chi's per-vertex total degree is not (1,1,1,1,1,1,3,3)",
    )
    require(
        not total_degree_constant(chi_deg),
        "chi passes the corrected criterion -- the weight argument would fail",
    )
    # and every coefficient of H passes it, as it must
    for iota in product(range(d), repeat=n):
        deg = [F(0)] * len(params)
        for v in range(n):
            deg[pindex[(v, iota[v])]] += F(1)
        require(total_degree_constant(deg),
                ("a coefficient of H fails the corrected criterion", iota))
    return True


# ----------------------------------------------------------------------
# normalization probe, then everything
# ----------------------------------------------------------------------


def audit_normalization():
    ones = {
        e: [[F(1)] * D for _ in range(D)] for e in combinations(range(8), 2)
    }
    matchings = tuple(perfect_matchings(tuple(range(8))))
    require(len(matchings) == 105, f"K_8 has {len(matchings)} matchings, not 105")
    require(
        all(len({x for p in m for x in p}) == 8 for m in matchings),
        "a listed matching does not partition the eight vertices",
    )
    tensor = matching_tensor(ones, 8, D)
    require(
        all(value == 105 for value in tensor.values()),
        "the all-ones matching tensor is not identically 105",
    )
    small = tuple(perfect_matchings(tuple(range(6))))
    require(len(small) == 15, "K_6 does not have 15 perfect matchings")


def main():
    audit_normalization()
    checked = audit_G1_equivariance_formal(n=4, d=2)
    checked3 = audit_G1_equivariance_formal(n=4, d=3)
    trials = audit_G1_equivariance_numeric_at_eight()
    dim, neqs = audit_G2_infinitesimal_stabilizer()
    nweights, orbit = audit_G3_weight_action()
    audit_G4_published_subgroups()
    audit_G5_invariance_criterion()
    print(
        f"PASS: matching tensor is local-group equivariant "
        f"(formal at n=4 over d=2 and d=3, {checked}+{checked3} indices; "
        f"numeric at n=8, {trials} trials); the infinitesimal stabilizer of "
        f"Delta_(8,3) in gl_3^8 is exactly the diagonal traceless-per-colour "
        f"space, dimension {dim} from {neqs} equations, so G^0 is a "
        f"{dim}-torus; it acts on {nweights} weights with orbit dimension "
        f"{orbit}, leaving {nweights - orbit} effective parameters; the "
        f"tau-weight grading and the endpoint torus are both one-parameter "
        f"subgroups of it; being trivial on G^0 is NOT necessary for being a "
        f"function of the matching tensor -- all 6558 non-constant "
        f"coefficients of H are counterexamples -- the correct subgroup is "
        f"the 7-dimensional colour-independent one, whose criterion is "
        f"per-vertex TOTAL degree constant in v, which every coefficient of H "
        f"passes and chi, at (1,1,1,1,1,1,3,3), fails"
    )


if __name__ == "__main__":
    sys.exit(main())
