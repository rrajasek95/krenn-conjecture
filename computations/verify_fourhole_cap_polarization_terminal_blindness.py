#!/usr/bin/env python3
"""Exact ledger for the cap double-polar / four-hole physical landing (wip).

Proved formally here, as polynomial identities over exact integers in the
thirty edge variables q_e, r_e (plus a formal alpha):

  P1  polarization:  <R, H_k> = (k+1) Q_{k+1}  and  <q, H_k> = (3-k) Q_k
      for k = 0,1,2, where H_k(e) = [t^k] haf((q+tR)|W\\e) and
      Q_j = [t^j] haf(q+tR);
  P2  cap ledger for A_cap = alpha*q + R:
        haf(A_cap)          = a^3 Q0 + a^2 Q1 + a Q2 + Q3,
        <R, H(A_cap)>       = a^2 Q1 + 2 a Q2 + 3 Q3,
        <q, H(A_cap)>       = 3 a^2 Q0 + 2 a Q1 + Q2,
        <A_cap, H(A_cap)>   = 3 haf(A_cap),
      and their exact jet spans, with J_k = [t^k](a(q+tR)^[3] + R(q+tR)^[2]):
        a  * <R, H(A_cap)>  = a^2 J1 + 3 J3          (J2 never appears),
        a^2* <q, H(A_cap)>  = 3 a^3 J0 - a^2 J1 + 3 a J2 - 9 J3,
        a  * chi            = a J2 - 2 J3            (chi = a Q2 + Q3),
        a  * haf(A_cap)     = a^3 J0 + a J2 - 2 J3;
  P3  the double-polar defect identity H(H(A)) = haf(A)*A + 2*B(A) on all
      fifteen edges (independent re-proof of the audited draft identity).

Verified exactly on named packets:

  G   the seven-row chi=-2 guard packet: four-hole vector and its grade
      supports, jets (J0,J1,J2,J3) = (0,-4,-2,0), edgewise defect
      H(H)-2B = chi*A_cap exactly on supp(A_cap), the anchor pairing and
      four-hole complement tables;
  K   the rank-two clean packet (chi=0): H(H)-2B == 0 on all fifteen edges
      while all twenty cut values Theta_S are nonzero; jets (0,8,24,-24)
      all nonzero above order zero although the packet is clean;
  D   a deterministic Fraction packet with true rational alpha = -Q1/Q0.

Standard library only; exact arithmetic; runs in well under a second.
"""

from collections import Counter
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, permutations


W = tuple(range(6))
EDGES = tuple(combinations(W, 2))


def require(condition, detail):
    if not condition:
        raise AssertionError(detail)


def edge(i, j):
    return (i, j) if i < j else (j, i)


def hole(e):
    return tuple(x for x in W if x not in e)


@lru_cache(maxsize=None)
def matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position, partner in enumerate(vertices[1:], start=1):
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in matchings(rest):
            answer.append(((first, partner),) + tail)
    return tuple(answer)


# ---------------------------------------------------------------------------
# Sparse signed integer polynomials.  A monomial is a sorted tuple of
# variable keys.  Counter is used as a plain dict; unary plus is never used
# because it would drop negative coefficients.
# ---------------------------------------------------------------------------

def trim(value):
    return Counter({m: c for m, c in value.items() if c != 0})


def pvar(key):
    return Counter({(key,): 1})


def pconst(scalar):
    return Counter({(): scalar}) if scalar else Counter()


def padd(*values):
    answer = Counter()
    for value in values:
        for monomial, coefficient in value.items():
            answer[monomial] += coefficient
    return trim(answer)


def pscale(value, scalar):
    return trim(Counter({m: scalar * c for m, c in value.items()}))


def pmul(left, right):
    answer = Counter()
    for ml, cl in left.items():
        for mr, cr in right.items():
            answer[tuple(sorted(ml + mr))] += cl * cr
    return trim(answer)


def pmulmany(values):
    answer = pconst(1)
    for value in values:
        answer = pmul(answer, value)
    return answer


def haf_poly(vertices, entries):
    return padd(
        *[
            pmulmany([entries[edge(*pair)] for pair in matching])
            for matching in matchings(tuple(vertices))
        ]
    )


def graded_haf_poly(vertices, q, r, top):
    layers = [Counter() for _ in range(top + 1)]
    for matching in matchings(tuple(vertices)):
        for mask in range(1 << len(matching)):
            weight = bin(mask).count("1")
            if weight > top:
                continue
            term = pmulmany(
                [
                    r[edge(*pair)] if mask >> position & 1 else q[edge(*pair)]
                    for position, pair in enumerate(matching)
                ]
            )
            layers[weight] = padd(layers[weight], term)
    return layers


# ---------------------------------------------------------------------------
# Numeric (exact int / Fraction) versions.
# ---------------------------------------------------------------------------

def haf_num(vertices, entries):
    total = 0
    for matching in matchings(tuple(vertices)):
        term = 1
        for pair in matching:
            term *= entries[edge(*pair)]
        total += term
    return total


def graded_haf_num(vertices, q, r, top):
    layers = [0] * (top + 1)
    for matching in matchings(tuple(vertices)):
        for mask in range(1 << len(matching)):
            weight = bin(mask).count("1")
            if weight > top:
                continue
            term = 1
            for position, pair in enumerate(matching):
                term *= r[edge(*pair)] if mask >> position & 1 else q[edge(*pair)]
            layers[weight] += term
    return layers


def hole_vector(entries):
    return {e: haf_num(hole(e), entries) for e in EDGES}


def double_polar_and_bianchi(entries):
    vector = hole_vector(entries)
    second = {}
    cross = {}
    for i, j in EDGES:
        complement = hole((i, j))
        second[(i, j)] = haf_num(complement, vector)
        value = 0
        for selected in combinations(complement, 2):
            rest = tuple(x for x in complement if x not in selected)
            term = 1
            for s in selected:
                term *= entries[edge(i, s)]
            for u in rest:
                term *= entries[edge(j, u)]
            value += term
        cross[(i, j)] = value
    return vector, second, cross


def jets(alpha, layers):
    q0, q1, q2, q3 = layers
    return (
        alpha * q0 + q1,
        alpha * q1 + 2 * q2,
        alpha * q2 + 3 * q3,
        alpha * q3,
    )


def contract(left, right):
    return sum(left.get(e, 0) * right.get(e, 0) for e in EDGES)


def full(sparse):
    return {e: sparse.get(e, 0) for e in EDGES}


# ---------------------------------------------------------------------------
# P1: polarization identities, formally.
# ---------------------------------------------------------------------------

def audit_formal_polarization():
    q = {e: pvar(("q",) + e) for e in EDGES}
    r = {e: pvar(("r",) + e) for e in EDGES}
    layers = graded_haf_poly(W, q, r, 3)
    hole_layers = {e: graded_haf_poly(hole(e), q, r, 2) for e in EDGES}
    for k in range(3):
        lhs = padd(*[pmul(r[e], hole_layers[e][k]) for e in EDGES])
        require(lhs == pscale(layers[k + 1], k + 1), ("R-polarization", k))
        lhs = padd(*[pmul(q[e], hole_layers[e][k]) for e in EDGES])
        require(lhs == pscale(layers[k], 3 - k), ("q-polarization", k))


# ---------------------------------------------------------------------------
# P2: cap contraction ledger and jet spans, formally (alpha a variable).
# ---------------------------------------------------------------------------

def audit_formal_cap_ledger():
    q = {e: pvar(("q",) + e) for e in EDGES}
    r = {e: pvar(("r",) + e) for e in EDGES}
    a = pvar(("a",))
    a2 = pmul(a, a)
    a3 = pmul(a2, a)
    cap = {e: padd(pmul(a, q[e]), r[e]) for e in EDGES}
    q0, q1, q2, q3 = graded_haf_poly(W, q, r, 3)

    haf_cap = haf_poly(W, cap)
    require(
        haf_cap == padd(pmul(a3, q0), pmul(a2, q1), pmul(a, q2), q3),
        "cap hafnian layers",
    )

    cap_holes = {e: haf_poly(hole(e), cap) for e in EDGES}
    r_contr = padd(*[pmul(r[e], cap_holes[e]) for e in EDGES])
    q_contr = padd(*[pmul(q[e], cap_holes[e]) for e in EDGES])
    self_contr = padd(*[pmul(cap[e], cap_holes[e]) for e in EDGES])
    require(
        r_contr == padd(pmul(a2, q1), pscale(pmul(a, q2), 2), pscale(q3, 3)),
        "R-contraction of the four-hole vector",
    )
    require(
        q_contr == padd(pscale(pmul(a2, q0), 3), pscale(pmul(a, q1), 2), q2),
        "q-contraction of the four-hole vector",
    )
    require(self_contr == pscale(haf_cap, 3), "cap self-pairing = 3 haf")

    j0 = padd(pmul(a, q0), q1)
    j1 = padd(pmul(a, q1), pscale(q2, 2))
    j2 = padd(pmul(a, q2), pscale(q3, 3))
    j3 = pmul(a, q3)
    require(
        pmul(a, r_contr) == padd(pmul(a2, j1), pscale(j3, 3)),
        "R-contraction is spanned by jets 1 and 3 only (J2-blind)",
    )
    require(
        pmul(a2, q_contr)
        == padd(
            pscale(pmul(a3, j0), 3),
            pscale(pmul(a2, j1), -1),
            pscale(pmul(a, j2), 3),
            pscale(j3, -9),
        ),
        "q-contraction jet span",
    )
    chi = padd(pmul(a, q2), q3)
    require(pmul(a, chi) == padd(pmul(a, j2), pscale(j3, -2)), "a*chi = a*J2 - 2*J3")
    require(
        pmul(a, haf_cap) == padd(pmul(a3, j0), pmul(a, j2), pscale(j3, -2)),
        "a*haf(cap) = a^3*J0 + a*J2 - 2*J3",
    )


# ---------------------------------------------------------------------------
# P3: independent formal re-proof of H(H(A)) = haf(A)*A + 2*B(A).
# ---------------------------------------------------------------------------

def audit_formal_double_polar():
    entries = {e: pvar(("A",) + e) for e in EDGES}
    haf_full = haf_poly(W, entries)
    first = {e: haf_poly(hole(e), entries) for e in EDGES}
    for i, j in EDGES:
        complement = hole((i, j))
        second = haf_poly(complement, first)
        cross = Counter()
        for selected in combinations(complement, 2):
            rest = tuple(x for x in complement if x not in selected)
            cross = padd(
                cross,
                pmulmany(
                    [entries[edge(i, s)] for s in selected]
                    + [entries[edge(j, u)] for u in rest]
                ),
            )
        require(
            second == padd(pmul(haf_full, entries[(i, j)]), pscale(cross, 2)),
            ("double-polar defect", (i, j)),
        )


# ---------------------------------------------------------------------------
# G: the seven-row chi = -2 guard packet.
# ---------------------------------------------------------------------------

GUARD_Q = {(0, 1): 1, (4, 5): 1}
GUARD_R = {(0, 2): 1, (0, 3): -1, (1, 2): 1, (1, 3): -1}
GUARD_ANCHOR_EDGES = {
    0: {(0, 5): 1, (1, 5): 1},        # p0*s0 = (z0+z1) z5      (missing row 00)
    1: {(2, 4): 1, (3, 4): -1},       # p1*s1 = z4 (z2-z3)      (missing row 11)
    2: {(2, 3): 1},                   # p2*s2 = z2 z3           (present row 22)
}


def audit_guard_packet():
    q = full(GUARD_Q)
    r = full(GUARD_R)
    alpha = 1
    layers = tuple(graded_haf_num(W, q, r, 3))
    require(layers == (0, 0, -2, 0), ("guard layers", layers))
    j = jets(alpha, layers)
    require(j == (0, -4, -2, 0), ("guard jets", j))
    # The terminal jet J3 = alpha*Q3 vanishes: the guard defect is a pure
    # grade-two phenomenon, strictly below the terminal cubic class.
    chi = alpha * layers[2] + layers[3]
    require(chi == -2, "guard chi")

    cap = {e: alpha * q[e] + r[e] for e in EDGES}
    require(haf_num(W, cap) == chi, "guard cap hafnian")

    vector, second, cross = double_polar_and_bianchi(cap)
    expected_vector = full(
        {(0, 2): -1, (0, 3): 1, (1, 2): -1, (1, 3): 1, (2, 3): 1, (4, 5): -2}
    )
    require(vector == expected_vector, ("guard four-hole vector", vector))

    # Grade supports of the four-hole vector.
    hole_layers = {e: graded_haf_num(hole(e), q, r, 2) for e in EDGES}
    for e in EDGES:
        l0, l1, l2 = hole_layers[e]
        require(
            vector[e] == alpha * alpha * l0 + alpha * l1 + l2,
            ("guard hole grade sum", e),
        )
    require(
        {e for e in EDGES if hole_layers[e][0]} == {(2, 3)},
        "grade-0 support is the present-anchor carrier edge 23",
    )
    require(
        {e for e in EDGES if hole_layers[e][1]} == {(0, 2), (0, 3), (1, 2), (1, 3)},
        "grade-1 support is the response support",
    )
    require(
        {e for e in EDGES if hole_layers[e][2]} == {(4, 5)},
        "grade-2 support (the R^[2] carrier) is edge 45 alone",
    )

    # Edgewise defect: H(H(cap)) - 2 B(cap) = chi * cap exactly.
    support = {(0, 1), (4, 5), (0, 2), (0, 3), (1, 2), (1, 3)}
    require({e for e in EDGES if cap[e]} == support, "guard cap support")
    for e in EDGES:
        require(second[e] - 2 * cross[e] == chi * cap[e], ("guard edgewise defect", e))
    require(
        {e for e in EDGES if second[e] - 2 * cross[e]} == support,
        "defect edges are exactly supp(A_cap)",
    )
    # The Bianchi cross-star vanishes on every defect edge here; the whole
    # defect is carried by the iterated four-hole hafnian.
    for e in sorted(support):
        require(cross[e] == 0, ("guard cross-star on defect edge", e))
    # Structure of the two grade-two defect edges:
    require(
        second[(0, 1)] == vector[(2, 3)] * vector[(4, 5)] == -2,
        "defect at 01 = (grade-0 carrier 23) x (grade-2 carrier 45)",
    )
    require(
        second[(4, 5)]
        == vector[(0, 2)] * vector[(1, 3)] + vector[(0, 3)] * vector[(1, 2)]
        == -2,
        "defect at 45 = grade-1 x grade-1 on the R support",
    )

    # Contraction ledger on the packet.
    require(contract(r, vector) == -4, "guard <R,H(cap)> = J1 (alpha=1, J3=0)")
    require(contract(q, vector) == -2, "guard <q,H(cap)>")
    require(contract(cap, vector) == 3 * chi, "guard cap self-pairing")

    # Anchor pairings: every diagonal-anchor response is orthogonal both to
    # the four-hole vector and to the cap itself, except the present anchor
    # against the four-hole vector.
    pair_hole = {c: contract(GUARD_ANCHOR_EDGES[c], vector) for c in (0, 1, 2)}
    pair_cap = {c: contract(GUARD_ANCHOR_EDGES[c], cap) for c in (0, 1, 2)}
    require(pair_hole == {0: 0, 1: 0, 2: 1}, ("anchor/hole pairings", pair_hole))
    require(pair_cap == {0: 0, 1: 0, 2: 0}, ("anchor/cap pairings", pair_cap))
    # ... whereas the internal quadratic detects the cap (and hence chi).
    require(contract(q, cap) == 2, "q detects the cap")

    # Four-hole complement table for the six defect edges.
    def inside(edges_dict, complement):
        return {
            e
            for e in edges_dict
            if e[0] in complement and e[1] in complement
        }

    present = GUARD_ANCHOR_EDGES[2]
    miss0 = GUARD_ANCHOR_EDGES[0]
    miss1 = GUARD_ANCHOR_EDGES[1]
    u45 = hole((4, 5))
    require(
        inside(miss0, u45) == set() and inside(miss1, u45) == set(),
        "terminal carrier complement {0,1,2,3} contains no missing-anchor edge",
    )
    require(
        inside(present, u45) == {(2, 3)},
        "terminal carrier complement contains only the present anchor edge",
    )
    u01 = hole((0, 1))
    require(
        inside(present, u01) == {(2, 3)}
        and inside(miss1, u01) == {(2, 4), (3, 4)}
        and inside(miss0, u01) == set(),
        "complement of 01 holds the present anchor and both row-11 edges",
    )
    for e in ((0, 2), (0, 3), (1, 2), (1, 3)):
        u = hole(e)
        require(
            len(inside(miss0, u)) == 1
            and len(inside(miss1, u)) == 1
            and inside(present, u) == set(),
            ("grade-3 defect complement anchor content", e),
        )


# ---------------------------------------------------------------------------
# K: the rank-two clean packet — edgewise zero, cutwise nonzero.
# ---------------------------------------------------------------------------

def permanent(rows, columns, entries):
    total = 0
    for assigned in permutations(columns):
        term = 1
        for row, column in zip(rows, assigned):
            term *= entries[edge(row, column)]
        total += term
    return total


def theta(marked, a, b, q):
    marked = tuple(sorted(marked))
    outside = tuple(x for x in W if x not in marked)
    value = 0
    for inside_pair in combinations(marked, 2):
        remaining = next(x for x in marked if x not in inside_pair)
        for y in outside:
            other = tuple(x for x in outside if x != y)
            value += a[edge(*inside_pair)] * b[edge(remaining, y)] * q[edge(*other)]
    return value + permanent(marked, outside, b)


def audit_rank_two_clean_packet():
    q = full({(0, 1): 1, (2, 3): 1, (4, 5): 1})
    u = (1, -1, 2, 0, 1, 1)
    v = (1, 2, -2, 1, -2, 1)
    r = {e: u[e[0]] * v[e[1]] + v[e[0]] * u[e[1]] for e in EDGES}
    alpha = -2

    layers = tuple(graded_haf_num(W, q, r, 3))
    require(layers == (1, 2, 6, 12), ("rank-two layers", layers))
    j = jets(alpha, layers)
    require(j == (0, 8, 24, -24), ("rank-two jets", j))
    chi = alpha * layers[2] + layers[3]
    require(chi == 0, "rank-two chi")
    # Clean, yet every translated jet above order zero is nonzero: the jet
    # route is sufficient-only, never necessary.

    cap = {e: alpha * q[e] + r[e] for e in EDGES}
    require(haf_num(W, cap) == 0, "rank-two cap hafnian")
    vector, second, cross = double_polar_and_bianchi(cap)
    for e in EDGES:
        require(second[e] - 2 * cross[e] == 0, ("rank-two edgewise defect", e))

    # Ledger with a genuine denominator: <R,H(cap)> = alpha*J1 + (3/alpha)*J3.
    r_contr = contract(r, vector)
    require(r_contr == 20, ("rank-two R-contraction", r_contr))
    require(
        Fraction(r_contr) == alpha * j[1] + Fraction(3 * j[3], alpha),
        "rank-two jet-span of the R-contraction",
    )

    # The twenty cut values are individually nonzero (the audited guard),
    # although the edgewise four-hole defect above vanishes identically.
    second_cell = {e: 2 * alpha * r[e] for e in EDGES}
    values = [theta(marked, second_cell, r, q) for marked in combinations(W, 3)]
    expected = [
        -12, -12, -12, -36, -20, 20, -28, 20, -4, -36,
        -44, -4, 20, -28, 20, -12, 20, 44, 52, 52,
    ]
    require(values == expected, ("rank-two cut values", values))
    require(all(values) and sum(values) == 0, "cutwise nonzero, aggregate zero")


# ---------------------------------------------------------------------------
# D: deterministic Fraction packet with true rational alpha.
# ---------------------------------------------------------------------------

def deterministic_arrays(seed):
    q = {}
    r = {}
    for i, j in EDGES:
        q[(i, j)] = ((seed + 2 * i - j) % 7) - 3
        r[(i, j)] = ((2 * seed - i + 3 * j) % 9) - 4
    return q, r


def audit_deterministic_packet():
    q, r = deterministic_arrays(3)
    layers = tuple(graded_haf_num(W, q, r, 3))
    q0, q1, q2, q3 = layers
    require(q0 != 0, "deterministic packet lost Q0")
    alpha = -Fraction(q1, q0)
    j = jets(alpha, layers)
    require(j[0] == 0, "selected source relation")
    chi = alpha * q2 + q3

    cap = {e: alpha * q[e] + r[e] for e in EDGES}
    require(haf_num(W, cap) == chi, "cap hafnian equals chi under E0")
    vector, second, cross = double_polar_and_bianchi(cap)
    for e in EDGES:
        require(second[e] - 2 * cross[e] == chi * cap[e], ("edgewise defect", e))

    require(
        contract(r, vector) == alpha * alpha * q1 + 2 * alpha * q2 + 3 * q3,
        "R-contraction ledger",
    )
    require(
        contract(q, vector) == 3 * alpha * alpha * q0 + 2 * alpha * q1 + q2,
        "q-contraction ledger",
    )
    require(contract(cap, vector) == 3 * chi, "self-pairing ledger")
    require(
        contract(r, vector) == alpha * j[1] + Fraction(3, 1) * j[3] / alpha,
        "jet span of the R-contraction",
    )
    require(alpha * chi == alpha * j[2] - 2 * j[3], "terminal split")

    # Residual theorem shape: Q3 = (1/3) <R, H(R)>.
    r_holes = {e: haf_num(hole(e), r) for e in EDGES}
    require(3 * q3 == contract(r, r_holes), "Q3 polarization through H(R)")


# ---------------------------------------------------------------------------
# B: explicit blindness witness.  Two source-normalized packets sharing
# (alpha, J1, J3) and the R-contraction, with different chi.
# ---------------------------------------------------------------------------

BLIND_A_Q = {
    (0, 1): 2, (0, 3): -2, (0, 4): -2, (0, 5): -1, (1, 2): -2,
    (1, 3): -2, (1, 5): 2, (2, 3): -1, (2, 4): -1, (3, 4): 2, (3, 5): -2,
}
BLIND_A_R = {(0, 1): 1, (0, 2): 2, (0, 3): 1, (1, 3): 2, (2, 3): 1}
BLIND_B_Q = {
    (0, 2): 2, (0, 3): 2, (0, 4): 2, (0, 5): -2, (1, 2): -1, (1, 3): 1,
    (2, 3): 1, (2, 4): -1, (2, 5): 1, (3, 4): -1, (3, 5): -1, (4, 5): 1,
}
BLIND_B_R = {(0, 1): -1, (0, 2): 1, (1, 2): 2, (2, 3): 1}


def blindness_readout(q_sparse, r_sparse):
    q, r = full(q_sparse), full(r_sparse)
    layers = tuple(graded_haf_num(W, q, r, 3))
    require(layers[0] != 0, "witness lost Q0")
    alpha = -Fraction(layers[1], layers[0])
    j = jets(alpha, layers)
    require(j[0] == 0, "witness fails the selected source row")
    cap = {e: alpha * q[e] + r[e] for e in EDGES}
    vector = hole_vector(cap)
    chi = alpha * layers[2] + layers[3]
    require(haf_num(W, cap) == chi, "witness cap hafnian")
    return alpha, layers, j, chi, contract(r, vector), contract(q, vector), contract(cap, vector)


def audit_blindness_witness():
    a = blindness_readout(BLIND_A_Q, BLIND_A_R)
    b = blindness_readout(BLIND_B_Q, BLIND_B_R)
    require(a[0] == b[0] == -1, "witness alpha")
    require(a[1] == (6, 6, 0, 0) and b[1] == (4, 4, -1, 0), "witness layers")
    require(a[2][1] == b[2][1] == -6, "witness J1 must agree")
    require(a[2][3] == b[2][3] == 0, "witness J3 must agree")
    require(a[2][2] == 0 and b[2][2] == 1, "witness J2 must differ")
    require(a[3] == 0 and b[3] == 1, "witness chi must differ")
    # The blind probe: identical on a clean and a non-clean packet.
    require(a[4] == b[4] == 6, "R-contraction fails to separate the packets")
    # The separating probes.
    require(a[5] == 6 and b[5] == 3, "q-contraction separates")
    require(a[6] == 0 and b[6] == 3, "cap self-pairing separates")
    require(a[6] == 3 * a[3] and b[6] == 3 * b[3], "Euler self-pairing = 3 chi")


# ---------------------------------------------------------------------------
# Z: the alpha = 0 corner, where the response contraction is NOT blind.
# ---------------------------------------------------------------------------

def audit_alpha_zero_corner():
    # The source row at alpha = 0 reads Q1 = 0; then A_cap = R and chi = Q3.
    # Polarization at k = 2 gives <R, H(R)> = 3 Q3 = 3 chi exactly, so the
    # response contraction detects cleanliness precisely here.
    checked = 0
    for seed in range(1, 240):
        q, r = deterministic_arrays(seed)
        r = {e: r[e] for e in EDGES}
        layers = graded_haf_num(W, q, r, 3)
        if layers[1] != 0:
            continue
        checked += 1
        alpha = 0
        cap = {e: alpha * q[e] + r[e] for e in EDGES}
        require(cap == r, "alpha=0 cap is the bare response")
        chi = alpha * layers[2] + layers[3]
        require(chi == layers[3], "alpha=0 chi is Q3")
        require(contract(r, hole_vector(cap)) == 3 * chi, ("alpha=0 detection", seed))
    # The deterministic family happens to contain no Q1 = 0 packet, so the
    # corner is exercised by an explicitly constructed one.  This block is
    # unconditional: it always runs, and it always tests the corner.
    # With q = 01+23+45 the internal four-hole vector H_0 is the indicator of
    # the three q-edges, so Q1 = R_01 + R_23 + R_45 and the corner condition
    # is one linear equation.  R still carries the matching (04|15|23), so
    # Q3 = haf(R) is nonzero and the packet is genuinely non-clean.
    q = full({(0, 1): 1, (2, 3): 1, (4, 5): 1})
    r = full({(0, 1): 1, (2, 3): -1, (0, 4): 1, (1, 5): 1})
    layers = graded_haf_num(W, q, r, 3)
    require(layers[1] == 0, ("constructed alpha=0 packet lost Q1=0", layers))
    chi = layers[3]
    require(chi != 0, "constructed alpha=0 packet must be non-clean to be a real test")
    require(contract(r, hole_vector(r)) == 3 * chi, "constructed alpha=0 detection")


# ---------------------------------------------------------------------------
# U: within span{q, R}, the cap is the UNIQUE probe returning chi.
# ---------------------------------------------------------------------------

def audit_probe_uniqueness():
    # Under the source row Q1 = -alpha*Q0, expanding <lam*q + mu*R, H(A_cap)>
    # in the free layers (Q0, Q2, Q3) gives the coefficient system
    #   Q0: lam*a^2 - mu*a^3 = 0,   Q2: lam + 2*a*mu = a,   Q3: 3*mu = 1.
    # Its unique solution is lam = a/3, mu = 1/3, i.e. S = A_cap/3.
    for alpha in (Fraction(1), Fraction(-1), Fraction(-2), Fraction(3, 5)):
        rows = [
            (alpha**2, -(alpha**3), Fraction(0)),
            (Fraction(1), 2 * alpha, alpha),
            (Fraction(0), Fraction(3), Fraction(1)),
        ]
        mu = Fraction(1, 3)
        lam = alpha - 2 * alpha * mu
        require(lam == alpha / 3, ("probe lambda", alpha))
        for a_coefficient, b_coefficient, rhs in rows:
            require(
                a_coefficient * lam + b_coefficient * mu == rhs,
                ("probe solves the system", alpha),
            )
        # Uniqueness: the (Q2, Q3) rows alone already pin (lam, mu), since
        # their 2x2 determinant 1*3 - 2*alpha*0 = 3 is nonzero for every alpha.
        determinant = rows[1][0] * rows[2][1] - rows[1][1] * rows[2][0]
        require(determinant == 3, ("probe uniqueness determinant", alpha))

    # Numeric confirmation of the resulting identity on real packets.
    for seed in (3, 5, 17, 29):
        q, r = deterministic_arrays(seed)
        layers = graded_haf_num(W, q, r, 3)
        if layers[0] == 0:
            continue
        alpha = -Fraction(layers[1], layers[0])
        cap = {e: alpha * q[e] + r[e] for e in EDGES}
        vector = hole_vector(cap)
        chi = alpha * layers[2] + layers[3]
        # Fraction(...) throughout: plain int division would silently
        # introduce floats and destroy exactness.
        probe = {e: Fraction(alpha * q[e] + r[e], 3) for e in EDGES}
        require(
            all(isinstance(probe[e], Fraction) for e in EDGES),
            "probe left exact arithmetic",
        )
        require(contract(probe, vector) == chi, ("unique probe returns chi", seed))


# ---------------------------------------------------------------------------
# C: a clean packet the response contraction cannot tell from the guard.
# ---------------------------------------------------------------------------

CONFUSION_Q = {
    (0, 1): -2, (0, 2): -2, (0, 4): -2, (0, 5): 1, (1, 2): -2, (1, 3): -2,
    (1, 4): -1, (1, 5): -2, (2, 3): 2, (2, 5): 1, (3, 4): 2, (3, 5): -1,
    (4, 5): -1,
}
CONFUSION_R = {(0, 1): 2, (0, 4): 1}


def audit_guard_confusion_packet():
    q, r = full(CONFUSION_Q), full(CONFUSION_R)
    layers = tuple(graded_haf_num(W, q, r, 3))
    require(layers == (4, -4, 0, 0), ("confusion layers", layers))
    alpha = -Fraction(layers[1], layers[0])
    require(alpha == 1, ("confusion alpha", alpha))
    j = jets(alpha, layers)
    require(j == (0, -4, 0, 0), ("confusion jets", j))
    chi = alpha * layers[2] + layers[3]
    require(chi == 0, "confusion packet must be clean")

    cap = {e: alpha * q[e] + r[e] for e in EDGES}
    require(haf_num(W, cap) == chi == 0, "confusion cap hafnian")
    readout = contract(r, hole_vector(cap))
    require(readout == -4, ("confusion R-readout", readout))

    # The audited seven-row guard has the SAME (alpha, J1, J3, <R,H>) readout
    # while being non-clean with chi = -2.
    guard_q, guard_r = full(GUARD_Q), full(GUARD_R)
    guard_layers = graded_haf_num(W, guard_q, guard_r, 3)
    guard_alpha = 1
    guard_j = jets(guard_alpha, guard_layers)
    guard_cap = {e: guard_alpha * guard_q[e] + guard_r[e] for e in EDGES}
    guard_chi = guard_alpha * guard_layers[2] + guard_layers[3]
    guard_readout = contract(guard_r, hole_vector(guard_cap))
    require(
        (guard_alpha, guard_j[1], guard_j[3], guard_readout)
        == (alpha, j[1], j[3], readout),
        "guard and clean packet must share the response readout",
    )
    require(guard_chi == -2 and chi == 0, "the shared readout must hide chi")


def main():
    audit_formal_polarization()
    audit_formal_cap_ledger()
    audit_formal_double_polar()
    audit_guard_packet()
    audit_rank_two_clean_packet()
    audit_deterministic_packet()
    audit_blindness_witness()
    audit_alpha_zero_corner()
    audit_probe_uniqueness()
    audit_guard_confusion_packet()
    print("PASS: formal polarization <R,H_k>=(k+1)Q_{k+1}, <q,H_k>=(3-k)Q_k")
    print("PASS: formal cap ledger; a<R,H(cap)> = a^2 J1 + 3 J3 is J2-blind;"
          " a*chi = a J2 - 2 J3")
    print("PASS: formal double-polar defect H(H(A)) = haf(A)A + 2B(A)")
    print("PASS: seven-row guard geometry; jets (0,-4,-2,0), terminal jet zero;"
          " defect = chi*A_cap on supp(A_cap); anchor tables")
    print("PASS: rank-two clean packet; edgewise defect zero on all 15 edges"
          " while all twenty cuts are nonzero; jets (0,8,24,-24)")
    print("PASS: deterministic Fraction packet ledger and Q3 = <R,H(R)>/3")
    print("PASS: explicit blindness witness - equal alpha/J1/J3 and equal"
          " <R,H(cap)>=6, yet chi = 0 vs 1; <q,H> and <cap,H> separate them")
    print("PASS: alpha=0 corner is NOT blind - there <R,H(cap)> = 3 chi")
    print("PASS: within span{q,R} the cap A_cap/3 is the unique chi-probe")
    print("PASS: a clean packet shares the seven-row guard's exact response"
          " readout (alpha,J1,J3,<R,H>) = (1,-4,0,-4) with chi = 0 vs -2")


if __name__ == "__main__":
    main()
