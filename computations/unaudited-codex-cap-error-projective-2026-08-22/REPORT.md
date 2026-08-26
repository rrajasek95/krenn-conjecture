# Intrinsic clean-cap error ideal as projective algebra

Status: **terminal negative for `block normality + intrinsic cap algebra`; an
exact block-injective local minimum can have a blocked cap ideal.**

For a pair `p,q`, the script rebuilds the committed error formula in the nine
homogeneous cap coordinates `K_ij`:

```text
I_pq = <E_pq,w(K)>,
g_pq = s(K) K_00 K_11 K_22.
```

At `n=8`, every nonzero error generator is cubic.  The active projective
locus is `Proj(V(I_pq)) intersect D(g_pq)`, and it is empty exactly when some
power of `g_pq` belongs to `I_pq`.  The audit computes exact characteristic-
zero standard bases, minimal associated primes, activity saturation, and
membership for `g^m`, `1 <= m <= 6`.  A second evaluator checks every emitted
error polynomial against the committed hafnian formula at an independent
cap.

## Exact lower-arity controls

For exact ternary `n=4` GHZ, the cap-error sum is empty:

```text
I_01 = (0),       Proj V(I_01) = P^8.
```

Thus the active open is nonempty and no power of `g` belongs to the ideal.

The phased `n=6` Fourier/anchor source is the decisive hostile control.  It
is fully isotropic and a smooth block-injective local minimum for its own
non-GHZ output.  At pair `01`, the intrinsic ideal has 24 quadratic
generators, projective dimension three, and exactly the two minimal linear
components

```text
(K_22,K_21,K_20,K_10,K_00),
(K_22,K_12,K_11,K_10,K_02).
```

In particular,

```text
g_01 in I_01
```

already at power one, and `I_01:g_01^infinity=(1)`.  Hence this exact local
minimum has no active cap at the selected pair.  Its failure to be a GHZ
source is precisely its nonzero mixed-output rows; no rank, isotropy, or
minimum-normality hypothesis distinguishes the blocked ideal.

## Exact `n=8` calibrations

For the frozen all-blocked W25/F8 `X3` source at pair `04`, only four cubic
error generators are nonzero.  Its projective base locus has minimal
components

```text
(K_22),
(K_11,K_01),
(K_01,K_00).
```

The scheme is nonreduced in the activity direction:

```text
g_04 not-in I_04,       g_04^2 in I_04.
```

Thus the least blocking exponent is exactly two.  This independently
recovers the unit active saturation while retaining the underlying
projective boundary rather than only a Boolean verdict.

For the positive W40 `X4` control at pair `67`, the cubic ideal has
projective dimension seven, its activity saturation is proper, and no
`g_67^m` belongs to the ideal for `1 <= m <= 6`.  The known rational cap
`K=I_3` lies on this active open.

## Block-normality test and conclusion

At both exact `n=4` GHZ and the phased `n=6` source, every star and triangle
map is injective.  Consequently the minimum-norm equations

```text
A_E orthogonal ker L_E
```

have zero polynomial content on these controls.  They cannot impose a
nonzero scalar contraction or syzygy of the cap error through degree six;
indeed, they impose none in any degree on an injective-block chart.  The
phased ideal above is therefore an explicit minimum-compatible blocked
error ideal.

The projective cap algebra is still the correct local decision mechanism,
but it is not a forcing theorem.  Any proof that an exact `n=8` GHZ fibre has
an active cap must consume the mixed GHZ coefficient equations themselves,
or a source identity derived from them.  Minimum normality plus the intrinsic
error ideal cannot supply that step.
