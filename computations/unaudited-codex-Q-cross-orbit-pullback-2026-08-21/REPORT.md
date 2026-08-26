# Exact pullback of the frozen support-six cross-`Q` families

Status: **UNAUDITED exact three-mode UNIT PASS**.

## Outcome

Both six-dimensional cross-`Q`-compatible orbit families are empty after the
literal six-block data are restored.  In fact the available certificate is
strictly stronger: it excludes an arbitrary right six-block partner, without
assuming that its `Q` lies in the `Q_0` orbit and without localizing at its
pure Hafnian.

## Reduction from the frozen left record

The exact left presentation over `Q[z]/(z^2+2z-1)` has

```
X support   = {1,2,5,6,9,10,13,14,17,18,21,22},
Cof support = {9,10,13,14},
Q support   = {3,5,6,9,10,12}.
```

The `Q` support is invariant under bitwise complement.  Therefore the two
directional entry/cofactor rows and the `Q` rows force on the right:

* all twelve off-diagonal cofactor entries vanish;
* cells `x9,x10,x13,x14` vanish;
* `Q3,Q5,Q6,Q9,Q10,Q12` vanish.

Together with the six permanent and four triangle rows, this is an exact
28-generator ideal in

```
Q[x0,...,x23]/(x9,x10,x13,x14).
```

## Certificate

The frozen certificate

```
computations/unaudited-codex-n8-dangerous-chart-bridge-2026-08-20/
  certificate_support6_fixed_left_partner_unit.json
```

contains the exact identity

```
sum_i coefficient_i * generator_i = 1.
```

All 28 coefficients are nonzero and contain 13,350 characters in total.
The logical certificate digest is

```
a17794ac82f6d4616af28fcf583567f1f92cc67de126b0cfe0b08b279d5cbd87
```

The present referee independently recomputes the left supports, derives all
28 right rows from the literal sources, matches them byte-for-byte to the
certificate, and replays the coefficient identity plus a source mutation.
No finite-field screen, orbit invariant, pure-H localizer, or new Groebner
claim is used.

The exact unit supersedes the requested preliminary tangent/dimension and
large-prime screen: the source scheme is already empty over `Q` before either
the right-orbit constraint or pure liveness is imposed.

Scope: this is for the exact frozen support-six left **presentation** and its
covariant relabellings.  It is not inferred for every tensor in a wider
four-qubit invariant stratum after forgetting its `X/C` presentation.

## Reproduction

```
./.venv/bin/python computations/unaudited-codex-Q-cross-orbit-pullback-2026-08-21/audit_support6_cross_orbit_pullback_unit.py
```

Standard, `-O`, and isolated `-I -S` runs all return logical digest

```
28be627726335bea1f40993cbf7c297d6cb0b383d5768bc301fd9ed838f5c5e8
```
