# The same-hole inactive cap upgrades to an active clean point

Date: 2026-08-11

Checker: `computations/verify_h3_one_bad_same_hole_active_clean_pencil.py`

## Verdict

The landing `K=E_tt` in `9b2d709` is clean but inactive and therefore does
not by itself feed exact descent.  On the same physical pair `p=5,r=7`, the
nonzero direct anchor `D_pr=E_cc` supplies the canonical active line

```text
L(mu) = E_cc + mu I.
```

For the pencil `K+zL`, the full six-site homogeneous cap error at `h=3`
vanishes identically.  The point `mu=z=1` is

```text
K+L = diag(1,2,2),
s = 2,
kappa = (1,2,2),
E(K+L) = 0.
```

It is therefore an exact active clean cap.  The literal same-hole quadratic
branch, unlike the inactive coordinate landing alone, really does descend.

## Complete response pencil

After deleting `p,r`, retain residual sites `(0,1,2,3,4,6)`.  Write
`gamma` for the arbitrary product of the two same-hole coefficients.  The
three diagonal responses of `L(mu)` have physical supports

```text
A = 26:00,
C = 12:11,
T = 14:22.
```

The q-site collision in `P_a R_a` vanishes; the displayed `A` is its other
summand.  The same-hole geometry is encoded by the incidence graph

```text
A disjoint from T,
C meets A at site 2,
C meets T at site 1.
```

The complete response of `K+zL` is

```text
r(z,mu) = z*mu*A + z*(1+mu)*gamma*C + (1+z*mu)*T.
```

This retains the entire third-colour response and the literal physical
site labels; it is not a binary projection.

## Exact homogeneous cap error

For six residual sites, the clean error is

```text
E = s*r^[2]*q + r^[3],
s = z*(1+mu).
```

The incidence graph gives `r^[3]=0`.  The only nonzero product in `r^[2]`
is

```text
z*mu*(1+z*mu) A*T.
```

It occupies sites `{1,2,4,6}`.  Its complementary physical edge is `03`,
and the literal common-`q` normal form has no decorated cell at all on edge
`03`.  Hence `A*T*q=0` coefficientwise in every ternary word, and

```text
E(K+zL) = 0
```

as a polynomial identity in `z,mu,gamma`.  The checker enumerates the full
ternary matching tensors for both `r^[3]` and `r^[2]q`; neither has a term.
This is not the vacuous stronger condition `r^[2]=0`: the checker separately
pins the nonzero polynomial coefficient of `A*T`.

### Why edge `03` is absent, and the exact stability boundary

The edge absence is stronger than a bare sparse-support observation at the
quadratic layer.  The checker builds the complete `150 x 167` first
derivative of the two diagonal and `ca`/`tt` tensor rows.  Each of the nine
decorated `q03:ab` variables produces the `ca` coefficient

```text
(a,2,1,b,1).
```

For `a=0,2`, no other tangent column hits that coefficient.  For `a=1`,
the only possible repair is `Ra@3:b`, but it also produces the unique
diagonal-`Ra` coefficient `(0,0,1,b,1)`.  Hence the full tangent equations
force all nine `q03` coordinates to zero.  The active-clean calculation is
therefore valid on the actual first filtered same-hole branch, not merely
on an arbitrarily chosen coordinate subspace.

This is not yet an all-order stability theorem.  The exact condition for
the same pencil is

```text
q restricted to physical edge 03 = 0.
```

Indeed, adding any decorated cell `03:ab` creates the distinct clean-error
word `(a,2,0,b,2,0)` with the nonzero scalar factor
`z^2*mu*(1+mu)*(1+z*mu)`.  Thus no cancellation among the nine decorations
is possible.  A completed higher-order branch remains covered precisely if
its nonlinear row corrections do not regenerate edge `03`; that nonlinear
preservation is not proved here.

## Activity

The scalar and target coordinates are

```text
s        = z*(1+mu),
kappa_a  = z*mu,
kappa_c  = z*(1+mu),
kappa_t  = 1+z*mu.
```

Their product is not identically zero.  At `mu=z=1` it equals eight, with
`s=2` and `kappa=(1,2,2)`.  Thus the clean pencil has a concrete active
point, not merely a generic-activity assertion.

Every cap matrix in the pencil is a literal scalar contraction of the same
nine physical rows.  The target ledger and ordinary coefficient rows are
therefore preserved; no target-forgetting or declared principal-parts
column is used.

## Scope

This proves active-clean descent for the exact first filtered same-hole
quadratic normal form of `1ca72d6`, with arbitrary coefficient on the
same-hole product.  The full tangent rows force residual edge `03` to be
absent at this layer.  It does not establish that nonlinear cubic or
quartic corrections preserve `q|_03=0`.  The crossed-good quadratic branch
and that all-order stability question remain separate.
