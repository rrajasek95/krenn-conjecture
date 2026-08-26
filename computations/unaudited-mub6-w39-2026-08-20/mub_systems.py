"""W39: the RATIONAL split model of the MU-vector fibre V(H) for order-6
Butson complex Hadamard matrices with entries in cube/sixth roots of unity.

DERIVATION (exact, no floating point).
A vector MU to the standard basis is v = (1/sqrt6)(1, z_2, ..., z_6) with
|z_j| = 1 (z_1 = 1 fixes the global phase).  MU to the basis of H means
    |sum_j conj(H_{jk}) z_j|^2 = 6,   k = 1..6.

Every entry of H is a root of unity of order 3 or 6, so
    2*H_{jk} = C_{jk} + i*S_{jk}*sqrt3   with C, S INTEGERS
      (2*w^e   : (2,0), (-1,1), (-1,-1)         for e = 0,1,2)
      (2*z6^e  : (2,0), (1,1), (-1,1), (-2,0), (-1,-1), (1,-1))
Write z_j = u_j + i*v_j/sqrt3.  This is a REAL linear change of coordinates
(sqrt3 > 0), so it is a bijection on real points.  Then

    2*L_k := sum_j 2*conj(H_{jk}) z_j = P_k + (i/sqrt3) * Q_k    with
    P_k = sum_j ( C_{jk} u_j + S_{jk} v_j )
    Q_k = sum_j ( C_{jk} v_j - 3 S_{jk} u_j )
and  |2 L_k|^2 = P_k^2 + Q_k^2 / 3 = 4*6 = 24, i.e.

    (MU_k)     3 P_k^2 + Q_k^2 - 72 = 0            k = 1..6
    (CIRC_j)   3 u_j^2 + v_j^2 - 3  = 0            j = 2..6

TEN variables u_2..u_6, v_2..v_6; ELEVEN equations; all coefficients INTEGERS
(ledger 22: nothing for Singular's parser to mangle); every equation of total
degree 2.  The REAL points of this system are exactly the vectors MU to
{I, H/sqrt6}, in bijection.  (Exactly one of the six MU_k is dependent on the
other five modulo CIRC -- see FORMULATIONS.md sec 2a -- so the system is
square: 10 independent equations in 10 unknowns.)
"""
from fractions import Fraction

# 2 * (root of unity), as integer pairs (C, S) meaning C + S*i*sqrt3
TWO_CUBE = {0: (2, 0), 1: (-1, 1), 2: (-1, -1)}
TWO_SIXTH = {0: (2, 0), 1: (1, 1), 2: (-1, 1), 3: (-2, 0), 4: (-1, -1), 5: (1, -1)}

S6_EXP = [
    [0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 2, 2],
    [0, 1, 0, 2, 2, 1],
    [0, 1, 2, 0, 1, 2],
    [0, 2, 2, 1, 0, 1],
    [0, 2, 1, 2, 1, 0],
]
F6_EXP = [[(i * j) % 6 for j in range(6)] for i in range(6)]

VARS = [f"u{j}" for j in range(2, 7)] + [f"v{j}" for j in range(2, 7)]


def _lin(coeffs):
    """coeffs: list of (int, varname or None). Returns a Singular string."""
    parts = []
    for c, name in coeffs:
        if c == 0:
            continue
        parts.append(f"({c})" if name is None else f"({c})*{name}")
    return "+".join(parts) if parts else "0"


def fibre_system(exp, order):
    """Return (generators, variables) of the rational split model."""
    table = TWO_CUBE if order == 3 else TWO_SIXTH
    U = ["1"] + [f"u{j}" for j in range(2, 7)]      # u_1 = 1
    V = ["0"] + [f"v{j}" for j in range(2, 7)]      # v_1 = 0
    gens = []
    for k in range(6):
        pc, qc = [], []
        for j in range(6):
            C, S = table[exp[j][k] % order]
            # conj(H) = C - S i sqrt3 ; the sign of S is flipped by conjugation
            Cc, Sc = C, -S
            if j == 0:
                pc.append((Cc, None))                # u_1 = 1
                qc.append((-3 * Sc, None))           # v_1 = 0, so only -3S u_1
            else:
                pc.append((Cc, U[j]))
                pc.append((Sc, V[j]))
                qc.append((Cc, V[j]))
                qc.append((-3 * Sc, U[j]))
        P = _lin(pc)
        Q = _lin(qc)
        gens.append(f"3*({P})^2+({Q})^2-72")
    for j in range(2, 7):
        gens.append(f"3*u{j}^2+v{j}^2-3")
    return gens, list(VARS)


def check_real_point(exp, order, u, v):
    """Exact verification that (u,v) is a genuine MU vector: returns the list
    of exact residuals (all must be 0).  u, v are lists of 5 Fractions."""
    table = TWO_CUBE if order == 3 else TWO_SIXTH
    U = [Fraction(1)] + [Fraction(x) for x in u]
    V = [Fraction(0)] + [Fraction(x) for x in v]
    res = []
    for k in range(6):
        P = Q = Fraction(0)
        for j in range(6):
            C, S = table[exp[j][k] % order]
            Cc, Sc = C, -S
            P += Cc * U[j] + Sc * V[j]
            Q += Cc * V[j] - 3 * Sc * U[j]
        res.append(3 * P * P + Q * Q - 72)
    for j in range(1, 6):
        res.append(3 * U[j] ** 2 + V[j] ** 2 - 3)
    return res


if __name__ == "__main__":
    for name, exp, order in [("S6", S6_EXP, 3), ("F6", F6_EXP, 6)]:
        g, vs = fibre_system(exp, order)
        print(name, "vars", len(vs), "gens", len(g))
        print("  first MU generator:", g[0][:120], "...")
        print("  first circle generator:", g[6])
    # sanity: the all-ones vector z = (1,1,1,1,1,1) is u_j=1, v_j=0.  It is MU
    # to the standard basis but NOT to F_6 (it is the first column of F_6), so
    # its residuals must NOT all vanish -- an anti-control (ledger 18: a
    # control that can actually fail).
    r = check_real_point(F6_EXP, 6, [1] * 5, [0] * 5)
    print("anti-control all-ones vs F6 residuals:", r)
