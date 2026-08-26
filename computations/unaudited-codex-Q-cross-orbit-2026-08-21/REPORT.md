# Frozen support-six `Q_0`: exact cross-orbit coordinates

Status: **UNAUDITED exact three-mode PASS**.

## Outcome

For the frozen support-six tensor `Q_0`, the cross-colour equations against a
literal right tensor `g_1 tensor ... tensor g_4 . Q_0` reduce on the dense
local-row chart to two irreducible two-dimensional families (equivalently two
one-dimensional quadratic covers after quotienting a common weight-two
scaling).  Each gives a six-dimensional compatible family in the affine
`GL_2^4` orbit.  This is a direct orbit calculation, not an inference from
four-qubit invariant equality.

The two components are proved in the localized big-cell preimage.  A
disconnected stabilizer could still identify their tensor images; the global
boundary gluing and finite stabilizer action have not been classified.

## Six equations to two quadrics

The only nonzero coordinates of the left tensor are the six weight-two
coordinates.  Write

```
F(t) = sum_{i<j} q_ij t_i t_j
```

for the corresponding quadratic form, and write the two rows of the `i`th
right local matrix as `[1,x_i]`, `[1,y_i]`, with `d_i=y_i-x_i != 0`.
Compatibility is exactly

```
F(x + 1_{ij} d) = 0,  i<j.
```

With `C=F(x)`, `u_i=d_i(Mx)_i`, and `v_i=u_i+C/2`, these six rows become
`v_i+v_j+E_ij=0`, where `E_ij=q_ij d_i d_j`.  Eliminating `v` leaves only

```
E01+E23 = E02+E13 = E03+E12.
```

After fixing the common scaling by `d0=1`, writing `(d1,d2,d3)=(r,u,t)`,
the exact resultant is

```
(4+4*sqrt(2))
*(r+(3-2*sqrt(2))*u)
*(r*u+(1+sqrt(2))*r+(1-sqrt(2))*u+1).
```

Thus there are two rational `d` branches.  Reconstructing `x` requires one
quadratic equation for `C`; on each branch its discriminant has squarefree
part a product of two distinct irreducible quadratics.  Hence each branch is
an irreducible quadratic cover over `Q(sqrt(2))(u)`.  The complete formulas,
excluded determinant-zero parameters, and inverse reconstruction are in the
JSON result.

The exact Lie action at `Q_0` has rank 12 and stabilizer dimension 4.  The
localized solution preimage has dimension 10 (two row-direction parameters
plus eight row scalars), giving compatible tensor-family dimension `10-4=6`.

## Verstraete/Luque--Thibon placement

Over `Q(sqrt(2),i)`, diagonal local gauges put `Q_0` in the usual
`G_abcd` convention with

```
(a,b,c,d) = (2, 2+2*i, 2-2*i, -2).
```

Thus the squared-parameter multiset is `{4,4,8*i,-8*i}`.  The collision
`a^2=d^2` makes this a non-regular stratum.  Equality of polynomial
four-qubit invariants therefore gives only invariant-fibre/closed-orbit data;
it is not used to assert orbit equality here.

## Cofactor obstruction is not a `Q`-only covariant

At the frozen six-block presentation, the exact Jacobian ranks are

```
rank(dQ)=14,  rank(dCof)=23,  rank([dQ;dCof])=24.
```

An explicit seven-entry tangent lies in `ker(dQ)` but has
`dCof_13=-2+sqrt(2) != 0`.  Therefore the 24 edge-entry cofactors vary along
a first-order fibre of the presentation-to-`Q` map.  They cannot be a
regular standard covariant determined by the four-qubit tensor `Q` alone;
they are Hafnian-gradient data of the six-block presentation.  They may
still be treated as covariant data in that larger network representation.

## Reproduction

```
./.venv/bin/python computations/unaudited-codex-Q-cross-orbit-2026-08-21/audit_Q_cross_orbit_coordinates.py
```

Standard, `-O`, and isolated `-I -S` runs all return logical digest

```
3f6029d615c9c975e7d65e18bc9f0d93eacc0bb649c4384adc95fb884baea78a
```
