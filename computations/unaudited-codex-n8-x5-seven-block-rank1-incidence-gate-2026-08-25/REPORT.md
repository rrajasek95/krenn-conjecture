# Exact closure of the canonical rank-one seven-block branch

## Outcome

For the canonical full-family support

```text
{06,13,17,24,26,56,57} + {04,12,35,67},
```

the entire `rank(A57)<=1` branch now satisfies the corrected dichotomy:

```text
active cap67 / triangle012
or
active cap45 / star(center=2).
```

There is no full-X5 point on which both carriers are inactive.  This is an
exact characteristic-zero unit-ideal result.  It closes one rank branch of
one of the six seven-block support orbits; it does not close rank two, the
other five orbits, or all 64 coefficient loci.

## Exact rank-one reduction

Write

```text
A57 = u v^T.
```

The stored-edge guard orientation is load-bearing.  From

```text
A26 A57^T + A56^T = 0
```

one obtains

```text
A56^T = -A26 v u^T,
A56   = -u (A26 v)^T,
```

not a left-multiplied alternative.  The remaining guard equations reduce to

```text
A06 v = 0,
(I-A17 A26)v = 0.
```

Putting `w=A26 v`, every cap67 response has the common right factor `u^T`:

```text
R05(K) = (A06 K v)u^T,
R15(K) = (K v-A17 K^T w)u^T,
R25(K) = (A26 K v-K^T w)u^T.
```

Consequently three arbitrary response-dual matrices reduce exactly to three
dual vectors `x,y,z`, nine variables rather than 27.  The cap67-pairing
failure condition is

```text
A67 = (A06^T x+y+A26^T z)v^T
    - (A26 v)(A17^T y+z)^T.
```

The audit replays these response and adjoint identities on 257 exact integer
samples.

## Cap45 inactivity and color symmetry

For cap45/star2, `P=Row(A04)` and
`Q=ColSpan(A35^T,u)` after the guard substitution.  A diagonal activity
failure is therefore

```text
e_i in Row(A04) and e_i in ColSpan(A35^T,u).
```

Global color permutation preserves the full source equations and acts
transitively on `e_0,e_1,e_2`, so it suffices to impose the `e0` incidence:

```text
A04^T rho = e0,
A35^T sigma + u tau = e0.
```

The other possible cap45 failure is its fixed-identity pairing.  For a
`P tensor Q` response space, `I3 in P tensor Q` forces `P=Q=Q^3`, which in
particular satisfies the `e0` incidence.  Thus the single normalized ideal
covers every way this star can be inactive.

## Exact elimination

Substituting `A56,A57`, reducing the cap67 duals, and adding the two incidence
systems produces

```text
103 variables,
6,582 equations = 6,561 full-X5 + 6 guard + 9 adjoint + 6 incidence.
```

Over `F_32003`, exact `slimgb` returned the unit basis in 26.724 seconds.
Over `Q`, the identical polynomial system returned

```text
INPUT_GENERATORS=6582
GROEBNER_SIZE=1
UNIT_REMAINDER=0
STATUS=UNIT_IDEAL
```

in 28.125 seconds.  The rational result is the mathematical certificate; the
modular run is only a control.  A second rational `std` cross-check timed out
at 120 seconds and has zero coverage, without affecting the completed exact
`slimgb` result.

The parameterization also includes rank zero and permits zero blocks.  A unit
result on this larger closure is stronger than the required nonzero rank-one
stratum.

## Next exact branch

The remaining canonical possibility is `rank(A57)=2`; rank three is excluded
by nonzero `A06` and `A06 A57^T=0`.  The analogous smallest formulation uses

```text
A57=U V^T,  U,V in Mat(3,2),
A56=-U(A26 V)^T,
A06 V=0,
(I-A17 A26)V=0.
```

Its response duals reduce from 27 to 18 variables, and the same normalized
`e0` incidence gives a projected 119-variable ideal.  That branch was not run
in this package.

Parent exact counter-obligation manifest:
`21f351085e1650dcf64889103813c869853f47b74a432596a9147d3324536acf`.
