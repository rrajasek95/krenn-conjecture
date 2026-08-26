# All-rank-nine minimum-norm counterguard

## Verdict

Minimum norm, its reduced conormal equation, and its full second variation do
not force a triangle rank drop or an active cap on the all-rank-nine open
without the mixed `X5` equations.  There is an exact pure-normalized real
source with:

```text
all 5,040 cyclic five-set response maps rank 9,
all 560 triangle carrier matrices L_T rank 9,
all four blockers in rowspan(L_T) for every carrier,
rank(dPhi)=245 with its kernel exactly the 7D site gauge,
strictly positive constrained second variation.
```

It has all 6,558 mixed amplitudes nonzero, so it is deliberately not `X5`.
This is a counterguard to a minimum-norm-only implication, not a counterexample
to the conjecture.

## Exact source and rank certificate

Start with the pinned positive integral `dense_source`.  Every source cell is
positive.  Consequently every output word has a positive contribution from
each perfect matching, so all 6,561 amplitudes are nonzero.  Its three pure
amplitudes are positive integers.  Scaling the three colour ports at site
zero by their reciprocals makes the pure amplitudes exactly one and preserves
all ranks by source-map equivariance.

The literal 6,561-by-252 Jacobian has rank 245 modulo both 1009 and 1013.
Each modular rank supplies a nonzero 245-minor over `Z`, hence the
characteristic-zero rank is at least 245.  For every sum-zero vector
`a=(a_v)`,

```text
delta A_uv=(a_u+a_v)A_uv
```

is killed by `dPhi`, because every perfect matching contains each site once.
These seven independent gauge vectors give the opposite bound, so

```text
rank_Q(dPhi)=245,        ker(dPhi)=the product-one site-gauge tangent.
```

The existing exact two-prime response census gives rank nine for all 5,040
cyclic maps and carrier corank zero in all 1,680 colour-tagged triangle
groups.  Thus each of the 560 physical `L_T` has full nine-dimensional row
space.  Every diagonal or direct blocker is therefore present vacuously.

## Exact local minimum and second variation

After pure normalization put `w_uv=||A_uv||_F^2>0`.  On the product-one
positive site gauge, write `s_v=exp(x_v)` with `sum x_v=0`.  The norm is

```text
E(x)=sum_(u<v) w_uv exp(2(x_u+x_v)).
```

It is coercive and strictly convex on `sum x_v=0`.  Indeed its quadratic
form in a tangent `a` is

```text
4 sum_(u<v) w_uv exp(2(x_u+x_v)) (a_u+a_v)^2,
```

which vanishes on the sum-zero hyperplane only for `a=0`.  Hence `E` has a
unique balanced minimizer.  Site-gauge scaling preserves the output and all
the ranks above.

At that balanced point, maximal Jacobian rank makes the fibre smooth of
dimension seven.  Its gauge orbit has the same dimension and tangent, so it
is open in the local fibre.  The balanced source is therefore a strict local
norm minimum on its fibre; its smooth reduced-conormal equation holds, and
the displayed positive quadratic form is its complete constrained second
variation.  Moreover no nonzero gauge tangent is supported inside one star
or triangle, so every least-block map is injective and all regularity-free
block-minimum equations hold.

Thus no source-faithful conormal or second-variation identity depending only
on minimum norm and the rank-nine blocker incidence can yield the missing
arrow.  Any valid proof must use the simultaneous vanishing of the 6,558
mixed `X5` amplitudes (or an exact consequence of them).

## Scope and replay

The balanced point is specified exactly by the unique minimizer of the
displayed strictly convex algebraic-exponential gauge problem; the rank and
source claims are certified over characteristic zero by the two modular
minors and source equivariance.  No global minimum on a GHZ fibre is claimed.

```text
python3 computations/unaudited-codex-allrank9-minnorm-counterguard-2026-08-23/audit_allrank9_minnorm_counterguard.py --check-results
```

Logical digest:
`f281d19d320993a5408d7dfb97f40953800d0a58abc2f63d8e0bb08d57abfaa1`.

