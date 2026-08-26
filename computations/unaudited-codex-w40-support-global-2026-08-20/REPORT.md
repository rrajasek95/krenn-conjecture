# W40 fixed-support global classification

Status: **UNAUDITED new exact sublemma.**  No certified or spine file was
changed.

## Result

Fix precisely the twenty endpoint-ordered cells listed in `certificate.json`,
set all other 232 source cells to zero, and require all twenty named values to
be nonzero.  Over **every field** (including characteristic two), the full
level-four locus on this open support stratum is exactly one split
12-dimensional torus.  It is the target-preserving diagonal-gauge orbit of
the W40 integral point.  There is no additional component on this stratum.

More explicitly, a fresh 105-perfect-matching reconstruction gives 4,881 X4
rows.  Exactly 4,869 vanish identically on the support and the other twelve
are binomials.  Cancelling their invertible common monomials leaves ten
Laurent relations `R1,...,R10`.  They have rank eight.  The eight relations

```text
R1, R2, R3, R4, R5, R6, R8, R10
```

on the eight variables

```text
x01_00, x23_00, x45_00, x03_11,
x47_11, x04_01, x17_01, x04_22
```

have exponent determinant `+1`.  The remaining identities are certified by

```text
R7 = R3 - R4 + R5,
R9 = -R2 + R3 + R5,
```

including their signs.  Thus the localized ideal is saturated and its
coordinate ring is a Laurent polynomial ring in the other twelve variables;
the explicit inverse monomial formulas are retained in `certificate.json`.
This is a global classification, not a Jacobian or neighbourhood statement.

For the gauge identification, target-preserving diagonal gauge is
parameterized by `d[u,c]` for `u=0,...,6`, with
`d[7,c]=(product_{u=0}^6 d[u,c])^-1`.  Its 20-by-21 exponent matrix has rank
12 and a stored rank minor of determinant `-1`.  Every relation above
annihilates that matrix, and the relation lattice has the complementary rank
eight and is primitive by its determinant-one minor.  Hence the two lattices
are exact orthogonal complements.  The gauge minor also makes the image
split on field-valued points, so “gauge orbit” does not hide an algebraic
closure or root-extraction assumption.  The previously displayed
four-parameter Laurent family is only a slice of this 12-dimensional orbit.

## Uniform cap on the entire stratum

Every point on the support—even before imposing X4—has the same structural
active clean cap.  At pair `67`, take `K=I_3`.  The direct scalar is the live
unit `x67_00`, and the raw endpoint-ordered contraction has exactly

```text
R_05[0,2] = x06_02 x57_22,
R_15[0,1] = x17_01 x56_11,
R_25[2,2] = x26_22 x57_22,
R_45[1,1] = x47_11 x56_11.
```

All four response cells form the residual star centred at site `5`.
Therefore no two response edges are disjoint, so `r^2=r^3=0`.  A raw
symbolic replay of all 729 cleared clean-error coefficients returns zero.
Activity is `x67_00*K00*K11*K22=x67_00`, nonzero throughout the open
stratum.

## Controls and scope

Two independent raw coefficient engines (the stored 105 matchings and a
recursive hafnian) agree on every X4 row.  The integral W40 point passes all
rows.  Flipping only the forced sign of `x26_22` is a must-fire control and
breaks exactly four rows:

```text
00210222, 02221222, 12221021, 22222222.
```

All nine declared controls executed in standard, optimized, and isolated
no-site modes.  The certificate SHA-256 is
`c5ef9a220d94eb0b7355f25921893c105a86c870ac51831a8970171f3c094dcb`.

This theorem says nothing about a different 20-cell support, a support with
one or more of the 232 currently-zero cells activated, or a remote/singular
component of the full 252-coordinate X4 scheme.  In particular, it does not
prove the universal `X4 => active clean cap` target.  The separate local
Jacobian result rules out infinitesimal support extensions near the integral
point in characteristic zero; that local fact is not used here and must not
be conflated with this fixed-support global classification.

Replay:

```text
PYTHONDONTWRITEBYTECODE=1 python3 computations/unaudited-codex-w40-support-global-2026-08-20/classify_w40_support.py
PYTHONDONTWRITEBYTECODE=1 python3 -O computations/unaudited-codex-w40-support-global-2026-08-20/classify_w40_support.py
PYTHONDONTWRITEBYTECODE=1 python3 -I -S computations/unaudited-codex-w40-support-global-2026-08-20/classify_w40_support.py
```
