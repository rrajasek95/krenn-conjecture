# Representative 2: exact design and fail-closed bounded outcome

## Outcome

The next full-family support was treated independently from the closed
canonical representative:

```text
fixed:    {03,16,27,45}
variable: {04,12,35,67}
added:    {06,14,17,23,26,56,57}.
```

Its rank-zero branch is structurally closed, but its rank-one branch remains
unresolved.  A modular unit diagnostic was found for the original rank-one
ideal, while both exact-Q runs stopped at their authorized wall gates.  No
modular result was promoted to characteristic zero.  Successively smaller
exact quotients also timed out, culminating in an 80-variable/265-equation
pair01 chart.  Per the frozen policy, this Gröbner geometry is stopped rather
than widened.  Representative 2 is **not closed**.

## Independent support, guard, and carriers

The stored-edge guard has outside site 5 and reads

```text
A06 A57^T = 0,
A57^T + A17 A56^T = 0,
A26 A57^T + A56^T = 0.
```

Thus `A56^T=-A26 A57^T`, with the same low-rank outside factor `A57` as
representative 0.  This is a shared formula shape, not a support transport.
The primary three-term carrier derived directly from this support is

```text
cap45 / star1: A04 K [A35^T | A56 | A57].
```

The alternate exact two-sandwich carrier is

```text
cap03 / star6: A04^T K [A23^T | A35].
```

The parameterized generator first reproduced every sealed representative-0
rank-one and rank-two input byte-for-byte, then changed only the support.  It
is explicitly scoped to representatives 0 and 2; no transport to the other
four supports is claimed.

## Bounded rank-one outcomes

The original 103-variable/6,582-equation rank-at-most-one ideal returned a
unit over `F_32003` in 37.96 seconds.  This is diagnostic only.  The exact-Q
run stopped at 120.09 seconds; the sole authorized retry on the identical
input stopped at 300.18 seconds with live peak RSS 3,101,962,240 bytes.  Both
have zero mathematical coverage.

A five-chart gauge/minor split was derived.  Its first modular chart also
stopped at 120 seconds, so no Q or sibling chart ran.  Two literal 765-word
X5 subsets, one for each carrier, stopped at 120 seconds.  A tiny pure and
distinguished ladder exposed an underdetermined `dp` pathology and was not
continued.

Rank zero needs no elimination: `A57=0` forces `A56=0`, hence `L67=0`.
Because the full-family stratum has nonzero `A67`, its Frobenius functional is
live on the full kernel and cap67/triangle012 is active.

## Exact graph and incidence quotients

For cap03/star6, the nine cap67 adjoint equations are monic graph equations

```text
a67_ij - g_ij = 0.
```

Substituting them is a quotient-ring isomorphism.  Removing variables absent
after substitution is also exact because they form a polynomial extension.
This reduces the pure subset from 105 variables/24 equations to 84/15, and
the distinguished subset from 105/30 to 90/21.  The pure block-order gate
still stopped at 30 seconds; the distinguished gate was not run.

The two incidence systems are

```text
A04 rho = e0,
A23^T sigma + A35 tau = e0.
```

Both right sides are nonzero, so `rho` and `(sigma,tau)` are nonzero.  Their
3-by-6 principal opens give 18 exact charts.  In each chart, the quotient
solves three entries of `A04` and three entries of `A23` or `A35`, retains two
inverse equations, and keeps the exact A67 graph substitution.  The pure
charts have 72 variables/11 equations; distinguished charts have 82 or 84
variables/17 equations.

For the 257-word pair01 subset, residual color swap `1<->2` reduces the 18
localizations to ten orbits, with pair01 transported to the equally literal
pair02 subset on the mate.  The smallest representative is `rho0_sigma0`,
with 80 variables and 265 equations.  Its modular block-order gate stopped at
60.10 seconds with live peak RSS 630,231,040 bytes.  No Q run followed.

A unit on any literal subset would have been sufficient for the corresponding
full chart.  A timeout or nonunit subset would not be a disproof.  Since every
bounded proof-producing gate stopped, all results here are correctly scoped
as design or zero-coverage diagnostics.

## Remaining obligation

Representative 2 still requires a different algebraic mechanism: for example
a genuinely multigraded/resultant contraction or a new carrier identity.
Repeating these `dp/slimgb` ideals with wider walls is explicitly rejected.
Representatives 1, 3, 4, and 5, and the non-full-family strata, also remain.

Parent full-family manifest:
`21f351085e1650dcf64889103813c869853f47b74a432596a9147d3324536acf`.
