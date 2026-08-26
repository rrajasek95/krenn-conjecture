# Seven-block full-family guard/star counter-obligation

## Outcome

The corrected `active triangle OR active star OR literal full-X5 contradiction`
dichotomy is **not yet closed**, but its all-four-family seven-block boundary is
now an exact finite problem.  The 64 unresolved strata inherit the sealed
reduction to thirteen two-sandwich star patterns.  Expanding the six
all-four-family symmetry representatives gives respectively

```text
8, 10, 8, 10, 10, 10
```

two-sandwich stars, 56 candidates in total.  Every candidate has response row
space `P tensor Q`; its four exact inactivity alternatives and its two
source-labelled response products are stored in the result.

## Uniform guard and cap67 reduction

For each representative there is one outside site `r in {3,4,5}`.  In the
stored-block convention the complete formal cap67/triangle012 guard is

```text
R0r = A06 A_r7^T                         = 0,
R1r = A_r7^T + A17 A_r6^T               = 0,
R2r = A26 A_r7^T + A_r6^T               = 0.
```

Thus

```text
A_r6^T = -A26 A_r7^T,
(I-A17 A26) A_r7^T = 0,
A06 A_r7^T = 0.
```

The guard puts `I3` in the cap67 response kernel, so rank is at most eight and
all three diagonal activities are live.  The only possible triangle failure
is the cap pairing.  It fails exactly when there exist three `3 x 3` response
duals `X,Y,Z` with

```text
A67 = A06^T X A_r7 + Y A_r7 + A_r6^T Y^T A17
    + A26^T Z A_r7 + A_r6^T Z^T.
```

This is the explicit adjoint condition `A67 in Row(L67)`, not a sampled rank
test.  Pairing it with the guard kernel vector also forces `trace(A67)=0`.

## Canonical surviving star

For the canonical support

```text
{06,13,17,24,26,56,57} + {04,12,35,67},
```

cap45 with star center2 factors exactly as

```text
K -> A04 K [A35^T | A56 | A57].
```

Writing `P=Row(A04)` and
`Q=ColSpan(A35^T,A56,A57)`, its response row space is `P tensor Q`.  The guard
gives `A56=-A57 A26^T`, hence `Q=ColSpan(A35^T,A57)`, and the nonzero `A06`
together with `A06 A57^T=0` gives `rank(A57)<=2`.  Since `A45=I3`, this star is
active exactly when `P,Q` are not both full and no coordinate vector belongs
to both.  This proves why the sealed triangle-inactive witness still routes to
an active star; it does not prove the criterion at every dense point.

## Exact remaining systems

For each representative, the result stores:

- the three guard matrix equations and the cap67 adjoint identity;
- every two-sandwich star and its four inactivity incidences;
- the three pure target-one polynomials and six distinguished mixed residuals;
- a SHA-256 commitment to the complete 6,561-equation full-X5 ideal.

Therefore the first unproved branch is precise: impose cap67 pairing failure,
choose one inactivity incidence for every listed star, and show that the full
X5 ideal is inconsistent (or exhibit an exact source).  The order-two guard
symmetry supplies the other six supports.

## Bounded elimination diagnostic

For the canonical representative, a stronger preliminary ideal was generated:
all 6,561 full-X5 equations, 27 guard coordinates, and nine cap67-adjoint
coordinates, with 99 source and 27 response-dual variables.  `slimgb` over
`F_32003` reached the 120-second wall after about 5.51 GB in Darwin's raw
`ru_maxrss` units and produced no basis or result.  This has **zero mathematical
coverage**.  The rational run was intentionally skipped because the easier
modular gate did not finish.

The package consequently seals a smaller exact counter-obligation, not a
seven-block theorem, an X5 point, or a conjecture verdict.  No CEGAR or D12
artifact was read.

Frozen two-sandwich parent manifest:
`056d73cd56818a18e2976707815f902cc433839ce69b192a88b118b7a9a5d707`.
