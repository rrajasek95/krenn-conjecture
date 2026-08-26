#!/usr/bin/env python3
"""W26 ADVERSARIAL LANE -- the explicit ansatz families.  UNAUDITED.
EXACT ONLY.

Derivation (all of it re-verified by machine in adv_case2b.py /
adv_solo.py; nothing here is taken on faith):

m=25.  Gamma = K4(L) u {(4,5),(4,7),(5,6),(6,7)} u {(0,7),(1,4),(2,5)}.
  Phi(x,y) = A67[y6][y7] * P(x,y4,y5) + A56[y5][y6] * Q(x,y4,y7)
    P = hafL*A45[y4][y5] + A03[x0][x3]*A14[x1][y4]*A25[x2][y5]
    Q = hafL*A47[y4][y7] + A23[x2][x3]*A07[x0][y7]*A14[x1][y4]
  Ansatz "SPLIT25":   A45 = alpha a(x)u,  A47 = -alpha a(x)v,
    A07 = tau(x)v, A25 = sigma(x)u, A03 = tau(x)g, A23 = -sigma(x)g
  ==> P =  u[y5] * Ptil(x,y4),  Q = -v[y7] * Ptil(x,y4),
      Ptil = alpha*hafL*a[y4] + tau[x0]g[x3]sigma[x2]*A14[x1][y4].
  With A56[.][0] = mu A56[.][2] = mu u, A67[0][.] = mu A67[2][.] = mu v:
      Phi = Ptil * ( u[y5]A67[y6][y7] - v[y7]A56[y5][y6] )
          = 0                     for y6 in {0,2}   (identically!)
          = Ptil*(u[y5]q[y7] - v[y7]p[y5])          for y6 = 1.
  The words with y6=1 are non-clean exactly when x1=1 or x2=2 (singles
  (1,6),(2,6)), so cleanliness <=> Ptil(x,.) = 0 whenever x1!=1, x2!=2,
  which is a linear condition on hafL fixed by the L-block recipe below.
  Case-2b <=> col0(A56)=mu col2(A56), row0(A67)=mu row2(A67) (built in)
  and p[y5]/u[y5] != q[y7]/v[y7] for all y5,y7 (checked).

m=26/27.  extra Gamma edge (3,6) (and (4,6) at m=27):
  Phi = A67[y6][y7]P + A56[y5][y6]Q + A36[x3][y6]*Aa (+ A46[y4][y6]*Dd)
  ansatz "SOLO26" below makes Phi vanish for y6 in {0,2} and be
  proportional to c_(2,6) on the whole (2,6)-solo family.
"""
from __future__ import annotations

import os
import sys
from fractions import Fraction

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
UP = os.path.dirname(HERE)
sys.path.insert(0, UP)
sys.path.insert(0, HERE)
import w26_core as C                                              # noqa: E402

F = Fraction


def _z(ring):
    return ring(0) if ring is not None else F(0)


# ------------------------------------------------------------- SPLIT25
def split25(P, ring=None):
    """Build the m=25 Case-2b point from the parameter dict P.

    parameters (all must be nonzero unless noted):
      u,v,p,q,a,tau,sigma,g : 3-vectors        mu, alpha : scalars
      rho : dict {0:.,2:.}   r1 : 3-vector (row 1 of A14)
      h   : dict {0:.,2:.}   A13row1 : 3-vector
      k   : 3-vector (k[0] arbitrary; only differences matter)
      B0  : dict {0:.,2:.}   C0 : dict {0:.,1:.}
      A01col1, A02col2, A12row1, A12col2 : free cells (3-,3-,3-,dict{0,2})
    """
    one = (ring(1) if ring is not None else F(1))
    u, v, p, q = P["u"], P["v"], P["p"], P["q"]
    a, tau, sg, g = P["a"], P["tau"], P["sigma"], P["g"]
    mu, al = P["mu"], P["alpha"]
    rho, r1, h, A13r1 = P["rho"], P["r1"], P["h"], P["A13row1"]
    k, B0, C0 = P["k"], P["B0"], P["C0"]
    bl = {}
    # -- A01
    A01 = [[None] * 3 for _ in range(3)]
    for x0 in range(3):
        for x1 in (0, 2):
            A01[x0][x1] = tau[x0] * (B0[x1] + k[x0] * h[x1])
        A01[x0][1] = P["A01col1"][x0]
    bl[(0, 1)] = A01
    # -- A02
    A02 = [[None] * 3 for _ in range(3)]
    for x0 in range(3):
        for x2 in (0, 1):
            A02[x0][x2] = tau[x0] * (C0[x2] + k[x0] * sg[x2])
        A02[x0][2] = P["A02col2"][x0]
    bl[(0, 2)] = A02
    # -- A03, A07
    bl[(0, 3)] = [[tau[x0] * g[x3] for x3 in range(3)] for x0 in range(3)]
    bl[(0, 7)] = [[tau[x0] * v[y7] for y7 in range(3)] for x0 in range(3)]
    # -- A12
    A12 = [[None] * 3 for _ in range(3)]
    for x1 in (0, 2):
        for x2 in (0, 1):
            A12[x1][x2] = (B0[x1] * sg[x2] - C0[x2] * h[x1]
                           - rho[x1] * sg[x2] / al)
        A12[x1][2] = P["A12col2"][x1]
    for x2 in range(3):
        A12[1][x2] = P["A12row1"][x2]
    bl[(1, 2)] = A12
    # -- A13
    A13 = [[None] * 3 for _ in range(3)]
    for x1 in (0, 2):
        for x3 in range(3):
            A13[x1][x3] = h[x1] * g[x3]
    A13[1] = list(A13r1)
    bl[(1, 3)] = A13
    # -- A14
    A14 = [[None] * 3 for _ in range(3)]
    for x1 in (0, 2):
        for y4 in range(3):
            A14[x1][y4] = rho[x1] * a[y4]
    A14[1] = list(r1)
    bl[(1, 4)] = A14
    # -- A23, A25
    bl[(2, 3)] = [[-sg[x2] * g[x3] for x3 in range(3)] for x2 in range(3)]
    bl[(2, 5)] = [[sg[x2] * u[y5] for y5 in range(3)] for x2 in range(3)]
    # -- R blocks
    bl[(4, 5)] = [[al * a[y4] * u[y5] for y5 in range(3)] for y4 in range(3)]
    bl[(4, 7)] = [[-al * a[y4] * v[y7] for y7 in range(3)] for y4 in range(3)]
    bl[(5, 6)] = [[mu * u[y5], p[y5], u[y5]] for y5 in range(3)]
    bl[(6, 7)] = [[mu * v[y7] for y7 in range(3)],
                  [q[y7] for y7 in range(3)],
                  [v[y7] for y7 in range(3)]]
    assert sorted(bl) == sorted(C.gamma_edges(C.TEMPLATES[25]))
    return bl


def split25_params(rng=None, ring=None, **over):
    """a concrete rational parameter set (deterministic default)."""
    def R(x):
        return ring(x) if ring is not None else F(x)
    Pm = dict(
        u=[R(1), R(2), R(3)], v=[R(1), R(3), R(5)],
        p=[R(1), R(1), R(1)], q=[R(2), R(2), R(2)],
        a=[R(1), R(2), R(5)], tau=[R(1), R(2), R(3)],
        sigma=[R(1), R(2), R(4)], g=[R(1), R(3), R(2)],
        mu=R(2), alpha=R(1),
        rho={0: R(1), 2: R(2)}, r1=[R(3), R(1), R(2)],
        h={0: R(1), 2: R(3)}, A13row1=[R(2), R(5), R(7)],
        k=[R(0), R(1), R(2)], B0={0: R(5), 2: R(7)},
        C0={0: R(3), 1: R(1)},
        A01col1=[R(1), R(4), R(9)], A02col2=[R(2), R(3), R(5)],
        A12row1=[R(1), R(2), R(3)], A12col2={0: R(4), 2: R(6)})
    Pm.update(over)
    return Pm


# ------------------------------------------------------------- SOLO26
def solo26(P, m=26, ring=None):
    """m=26 (and m=27) point whose (2,6)-solo family survives.

    Structure (derived in the module docstring of adv_solo.py):
      A01 = tau (x) B      A02 = tau (x) Cc     A03 = tau (x) g
      A07 = tau (x) v      A12 = mvec (x) sigma A13 = h (x) g
      A14 = rho (x) a      A23 = eps (x) g      A25 = sigma (x) u
      A36 = g (x) (mu*phi, cp*phi - c, phi)
      A45 = alpha a (x) u  A47 = beta a (x) v
      A56 = u (x) (mu, cp, 1)      A67 = (mu, cp+c, 1) (x) v
      A46 (m=27 only) = a (x) (mu*w46, w46_1, w46)  -- see solo27 note
    """
    tau, B, Cc, g = P["tau"], P["B"], P["Cc"], P["g"]
    v, mvec, sg, h = P["v"], P["mvec"], P["sigma"], P["h"]
    rho, a, eps, u = P["rho"], P["a"], P["eps"], P["u"]
    mu, cp, c, phi = P["mu"], P["cp"], P["c"], P["phi"]
    al, be = P["alpha"], P["beta"]
    bl = {}
    bl[(0, 1)] = [[tau[i] * B[j] for j in range(3)] for i in range(3)]
    bl[(0, 2)] = [[tau[i] * Cc[j] for j in range(3)] for i in range(3)]
    bl[(0, 3)] = [[tau[i] * g[j] for j in range(3)] for i in range(3)]
    bl[(0, 7)] = [[tau[i] * v[j] for j in range(3)] for i in range(3)]
    bl[(1, 2)] = [[mvec[i] * sg[j] for j in range(3)] for i in range(3)]
    bl[(1, 3)] = [[h[i] * g[j] for j in range(3)] for i in range(3)]
    bl[(1, 4)] = [[rho[i] * a[j] for j in range(3)] for i in range(3)]
    bl[(2, 3)] = [[eps[i] * g[j] for j in range(3)] for i in range(3)]
    bl[(2, 5)] = [[sg[i] * u[j] for j in range(3)] for i in range(3)]
    f36 = [mu * phi, cp * phi - c, phi]
    bl[(3, 6)] = [[g[i] * f36[j] for j in range(3)] for i in range(3)]
    bl[(4, 5)] = [[al * a[i] * u[j] for j in range(3)] for i in range(3)]
    bl[(4, 7)] = [[be * a[i] * v[j] for j in range(3)] for i in range(3)]
    bl[(5, 6)] = [[u[i] * t for t in (mu, cp, 1)] for i in range(3)]
    bl[(6, 7)] = [[mu * v[j] for j in range(3)],
                  [(cp + c) * v[j] for j in range(3)],
                  [v[j] for j in range(3)]]
    if m == 27:
        d46 = P["d46"]
        bl[(4, 6)] = [[a[i] * t for t in (mu * d46[0], d46[1], d46[0])]
                      for i in range(3)]
    assert sorted(bl) == sorted(C.gamma_edges(C.TEMPLATES[m])), (
        sorted(bl), sorted(C.gamma_edges(C.TEMPLATES[m])))
    return bl
