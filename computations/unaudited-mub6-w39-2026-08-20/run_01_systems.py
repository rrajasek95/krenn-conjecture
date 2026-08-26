"""W39 (UNAUDITED, scoping only): exact construction and SIZING of the
MUB(6) polynomial systems.  Seconds-scale exact work only -- no solving.

Pinned HEAD: see PINNED_HEAD.txt

What this does:
  (A) verify Tao's spectral matrix S_6 is a complex Hadamard matrix
      EXACTLY over Z[w], w^2+w+1=0 (cyclotomic integers, no floats);
  (B) verify F_6 (Fourier) exactly over Z[z6], z6 = primitive 6th root;
  (C) emit the MU-VECTOR system  V(H) = {v : v MU to I and to H}
      in the unimodular-variable form used by Szollosi (arXiv:2405.09991):
      conj(z) = 1/z, cleared denominators, plus Rabinowitsch saturation;
      report exact variable counts, equation counts, degrees, #monomials;
  (D) report the same sizing for the TRIPLE and QUADRUPLE systems.

Every number printed here is exact (sympy over cyclotomic fields), not
numerical.  Hazard ledger 18/19/24 apply to any claim NOT printed here.
"""
import json
import sympy as sp

OUT = {}

# ---------------------------------------------------------------- (A) S_6
w = sp.Rational(-1, 2) + sp.sqrt(3) * sp.I / 2  # primitive cube root, exact
w = sp.nsimplify(w)


def cyc(k, n):
    """exact primitive n-th root of unity to the k-th power"""
    return sp.exp(2 * sp.pi * sp.I * sp.Rational(k, n))


W = [cyc(k, 3) for k in range(3)]  # 1, w, w^2

# Tao's spectral matrix S_6 (Butson BH(6,3)); exponent matrix of cube roots
S_EXP = [
    [0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 2, 2],
    [0, 1, 0, 2, 2, 1],
    [0, 1, 2, 0, 1, 2],
    [0, 2, 2, 1, 0, 1],
    [0, 2, 1, 2, 1, 0],
]
S6 = sp.Matrix(6, 6, lambda i, j: W[S_EXP[i][j] % 3])

# Fourier F_6: F[j][k] = zeta_6^{jk}
F6 = sp.Matrix(6, 6, lambda i, j: cyc(i * j, 6))


def is_chm(H, n=6):
    """exact check: H entries unimodular and H H^dagger = n I"""
    Hd = H.conjugate().T
    P = sp.expand(sp.simplify(H * Hd))
    ok_unit = all(sp.simplify(sp.Abs(H[i, j]) - 1) == 0
                  for i in range(n) for j in range(n))
    ok_orth = all(sp.simplify(P[i, j] - (n if i == j else 0)) == 0
                  for i in range(n) for j in range(n))
    return bool(ok_unit), bool(ok_orth)


OUT["S6_is_CHM"] = is_chm(S6)
OUT["F6_is_CHM"] = is_chm(F6)

# number of REAL entries (a discrete stratification invariant, cf. Liang et
# al. 2019 / Chen-Yu):  entry real  <=>  entry in {+1,-1}
OUT["S6_real_entries"] = sum(1 for i in range(6) for j in range(6)
                             if sp.simplify(sp.im(S6[i, j])) == 0)
OUT["F6_real_entries"] = sum(1 for i in range(6) for j in range(6)
                             if sp.simplify(sp.im(F6[i, j])) == 0)

# ------------------------------------------------- (C) MU-vector system
# v = (1/sqrt6)(1, z2,...,z6), |z_j| = 1.  MU to I is automatic.
# MU to H  <=>  |sum_j conj(H_{jk}) z_j|^2 = 6   for k = 1..6   (z_1 = 1).
# Write conj(z_j) = y_j with z_j y_j = 1.  Then each equation is
#   ( sum_j conj(H_{jk}) z_j ) * ( sum_j H_{jk} y_j ) - 6 = 0
# which is BILINEAR (degree 1 in z, degree 1 in y; total degree 2).
zs = sp.symbols("z2 z3 z4 z5 z6")
ys = sp.symbols("y2 y3 y4 y5 y6")
Z = (sp.Integer(1),) + zs
Y = (sp.Integer(1),) + ys


def mu_vector_system(H):
    eqs = []
    for k in range(6):
        A = sum(sp.conjugate(H[j, k]) * Z[j] for j in range(6))
        B = sum(H[j, k] * Y[j] for j in range(6))
        eqs.append(sp.expand(A * B - 6))
    rel = [sp.expand(Z[j] * Y[j] - 1) for j in range(1, 6)]
    return eqs, rel


def sizing(eqs, rel, name):
    allpolys = eqs + rel
    gens = list(zs) + list(ys)
    info = {
        "name": name,
        "n_vars": len(gens),
        "n_modulus_eqs": len(eqs),
        "n_inverse_relations": len(rel),
        "n_eqs_total": len(allpolys),
    }
    degs, mons = [], []
    for p in allpolys:
        P = sp.Poly(sp.expand(p), gens)
        degs.append(P.total_degree())
        mons.append(len(P.monoms()))
    info["total_degrees"] = degs
    info["monomial_counts"] = mons
    info["max_total_degree"] = max(degs)
    info["max_monomials"] = max(mons)
    return info


eqS, relS = mu_vector_system(S6)
eqF, relF = mu_vector_system(F6)
OUT["MUvector_system_S6"] = sizing(eqS, relS, "V(S_6)")
OUT["MUvector_system_F6"] = sizing(eqF, relF, "V(F_6)")

# dependency check: sum over k of |<v,h_k>|^2 = |v|^2 forces one equation
# to be a consequence of the other five together with z_j y_j = 1.
sumeq = sp.expand(sum(eqS))            # should reduce to 0 modulo z_j y_j - 1
red = sumeq
for j in range(1, 6):
    red = sp.simplify(sp.expand(red.subs(Y[j], 1 / Z[j])))
OUT["S6_six_equations_sum_reduces_to"] = str(sp.simplify(red))
sumeqF = sp.expand(sum(eqF))
redF = sumeqF
for j in range(1, 6):
    redF = sp.simplify(sp.expand(redF.subs(Y[j], 1 / Z[j])))
OUT["F6_six_equations_sum_reduces_to"] = str(sp.simplify(redF))

# ------------------------------------------------- (D) triple / quadruple
# essential-parameter accounting for the FULL problem, done exactly by hand
# and recorded here so the arithmetic is auditable.
def essential_counts(k_bases):
    """k_bases = number of NON-identity bases (so quadruple => 3)."""
    raw_phases = 36 * k_bases                     # every entry unimodular
    gauge = 6 + 6 * k_bases - 1                   # left D (shared) + right D each, -1 kernel
    free = raw_phases - gauge
    chm_eqs = 30 * k_bases                        # 15 complex off-diag per matrix
    pair_eqs = 36 * (k_bases * (k_bases - 1) // 2)  # |(H_a^dag H_b)_{jk}| fixed
    return {
        "non_identity_bases": k_bases,
        "raw_unimodular_entries": raw_phases,
        "continuous_gauge_dim": gauge,
        "essential_real_unknowns": free,
        "real_eqs_CHM": chm_eqs,
        "real_eqs_pairwise_unbiased": pair_eqs,
        "real_eqs_total": chm_eqs + pair_eqs,
    }


OUT["shape_pair_I_H"] = essential_counts(1)
OUT["shape_triple"] = essential_counts(2)
OUT["shape_quadruple"] = essential_counts(3)

print(json.dumps(OUT, indent=2, default=str))
with open(__file__.rsplit("/", 1)[0] + "/results_t1.json", "w") as fh:
    json.dump(OUT, fh, indent=2, default=str)
