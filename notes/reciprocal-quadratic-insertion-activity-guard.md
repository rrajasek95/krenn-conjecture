# An active reciprocal quadratic insertion need not activate its port arms

## Outcome

At `N=8`, the nonzero quadratic port term forced by the `3x3` permanent-null
no-go has residual cofactor `q^[1]`.  Nonvanishing of that one-edge cofactor
does **not** imply that either original source port arm is active: an original
arm needs a four-site `q^[2]` cofactor after the other deleted endpoint is
matched.  These two activity tests are genuinely different.

An exact source-support packet has

```text
reciprocal direct cofactor q^[3]       nonzero,
quadratic artificial insertion q^[1]  nonzero,
all four original port-arm cofactors  zero,
no internal cubic site.
```

There is a second, complementary guard: all three diagonal port responses
can have active `q^[2]` cofactors while every nonzero mixed permanent lands on
a zero `q^[1]` cofactor.  Thus the algebraic permanent no-go does not itself
force an active quadratic channel in the first place.

Therefore the implication

```text
active reciprocal quadratic insertion
    => active rank-one overlap or adjacent cubic pair
```

is false without further use of the complete target equations.  The packet
is a provenance/activity guard, not an exact GHZ source.

## The packet

Let the removed reciprocal endpoints be `p=6,r=7`, and put six residual
sites `0,...,5`.  Take

```text
q support = 01,23,45,
p ports   = p0,p1,
r ports   = r2,r3,
direct    = pr (a reciprocal coordinate cell).
```

The direct pair is active because

```text
q^[3] = (01)(23)(45) != 0.                                (1)
```

Use the principal-normalized completion matrix from the reciprocal
permanent audit,

```text
C = [ 1  1  1
     -1  1  1
     -1 -1  1 ].
```

Its mixed permanent on rows `0,1` and columns `1,2` is two.  The associated
quadratic port insertion has two artificial pairings

```text
(02)(13)(45),
(03)(12)(45),                                             (2)
```

where `02`, etc. in (2) are residual quadratic cells obtained by multiplying
a `p` port and an `r` port.  Both terms have the active cofactor `q_45`, so
their sum has coefficient two.

## Why the original arms are dead

Consider the original arm `p0`.  After choosing it, endpoint `r` can use
`r2` or `r3`.  The remaining four residual sites are respectively

```text
{1,3,4,5} or {1,2,4,5}.
```

The induced `q` support contains only edge `45`, not a perfect matching.
Thus the deleted cofactor of `p0` is zero.  The same argument applies to
`p1,r2,r3`; the exact census is

```text
p0:0, p1:0, r2:0, r3:0.                                  (3)
```

The original aggregate support degrees are

```text
residual 0,1,2,3: degree 2,
residual 4,5:     degree 1,
p,r:              degree 3.
```

Hence no residual pair is adjacent cubic.  The artificial edges in (2)
must not be counted as original source blocks; doing so is exactly the
provenance error this packet guards.

## Consequence for reciprocal descent

The surviving mixed permanent from the `3x3` no-go is useful only after an
additional theorem upgrades its `q^[h-2]` cofactor to one of the original
`p_i s_j q^[h-1]` response cofactors.  At `N=8` that means upgrading one
residual edge to a four-site perfect matching.  The reciprocal coordinate
block and insertion coefficient alone do not supply this upgrade.

A viable unification theorem must use a complete diagonal/off-diagonal pair
row to force one of the missing `q` edges, or show that the dead-port pattern
is incompatible with the pure target anchors.  Pure incidence and the
permanent survivor are insufficient.

## Complementary cofactor support

The `3x3` no-go proves that some mixed permanent of the completion matrix is
nonzero.  It does not prove that the corresponding source cofactor is
nonzero.  This distinction persists even when all three diagonal response
cofactors are active.

Use the same residual matching

```text
q support = 01,23,45
```

and assign the diagonal colour-`i` port pair to the endpoints of its `i`-th
edge:

```text
colour 0: p0 and r1,
colour 1: p2 and r3,
colour 2: p4 and r5.
```

Removing any one diagonal port pair leaves the other two `q` edges, so each
diagonal `p_i s_i q^[2]` response has cofactor one.  For a quadratic channel
with row pair `I` and column pair `J`:

- if `I=J`, the four ports cover two whole `q` edges and the remaining
  `q^[1]` cofactor is one, but the principal permanent of the normalized
  matrix is zero;
- if `I!=J`, the four ports leave one endpoint from each of two different
  `q` edges, so the `q^[1]` cofactor is zero.  This includes every channel
  whose mixed permanent is `+2` or `-2`.

The complete nine-channel ledger therefore has nonzero permanents and active
diagonal responses, but

```text
sum_(I,J) per(C_IJ) q^[1]_(I,J) = 0.
```

This is source-specific cofactor annihilation, one of the explicit escape
routes left open by the permanent-null no-go.  It is again a support packet,
not a solution of all nine target tensor equations; those equations are the
additional input needed to rule it out.

## Reproduction

```text
python3 computations/verify_reciprocal_quadratic_insertion_activity_guard.py
python3 -O computations/verify_reciprocal_quadratic_insertion_activity_guard.py
```
