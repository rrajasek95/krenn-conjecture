# The crossed quadratic mate does not land in the curved doubly-good OO branch

Date: 2026-08-11

Checker: `computations/verify_h3_one_bad_crossed_quadratic_oo_landing_guard.py`

## Verdict

The crossed mate from `1ca72d6`,

```text
R_c@1:1,  P_c@2:0,
```

does make the two displayed endpoint-slice minors unimodular: they are
`1,-1`.  The complete one-bad rows also make the two old direct arms active,
and the exact flat-bicase theorem puts their transition on the nonflat side.
Those facts are still insufficient for the curved OO theorem.

The selected bad arm is `pq=56:00`.  In the exact one-bad normal form its
selected-colour endpoint rows are

\[
                         P_a=Q_a=0.                     \tag{1}
\]

The crossed cells live in the complementary `c` rows, so they do not alter
(1).  On the literal crossed calibration the four deleted endpoint-star
ranks, in the order

```text
(p|q), (q|p), (p|r), (r|p),
```

are exactly

```text
2, 2, 3, 3.
```

Thus the old `pq` arm remains bad at both endpoints.  The curved OO theorem
requires `3,3,3,3`.  A nonzero `2x2` response minor is not a replacement for
either missing third row.

## What is automatic

The complete source consequences separate cleanly.

1. `R_a q^[2]=X_a` makes the `pq` cofactor nonzero.
2. `Q_c q^[2]=X_c` makes the `pr` cofactor nonzero.
3. The direct blocks have independent shared factors `e_a,e_c`.  If their
   transition were flat, the independent-factor case of the uniform
   flat-bicase theorem would force both outer restricted stars to vanish.
   The two displayed nonzero target rows rule that out.

Hence activity and nonflatness are automatic on the exact one-bad packet.
Full goodness is not merely unproved: on the selected bad arm it is excluded
by (1).

The two new physical cells lie on edges `17` and `25`.  These edges are
disjoint.  They therefore do not themselves define a second shared
rank-one pair to which the OO theorem could be re-applied.

## Complete source-label calibration

Set the two crossed coefficients to `1` and take the companion family
parameter `t=-1`.  Then `C=Q1=-1`, so the literal companion coefficient is

\[
                 C+(R_c@1)(P_c@2)=-1+1=0.             \tag{2}
\]

The checker expands all `3^8=6561` physical output rows.  It verifies:

```text
direct-arm ranks                  1,1
deleted endpoint-star ranks       2,2,3,3
supported cofactor matchings       4,3
pure target coefficients           1,1,1
companion 21000121                    0
other nonzero mixed rows             10
```

The last line is an essential scope guard.  This smallest calibration is
not a full GHZ source and is not a counterexample.  It shows exactly where
the crossed quadratic obligation sits in the physical row complex: (2) is
closed, while ten further mixed source labels still require completion.

## Minimal missing hypothesis

There is no direct route from this crossed pair to the proved curved branch.
A positive argument must first do one of the following:

1. construct a source-valid modification which leaves the one-bad normal
   form and restores the missing `a` rows at both endpoints of `pq`; or
2. reselect a genuinely shared second physical pair for which all four
   deleted endpoint-star maps have rank three.

Only after that step may nonflatness be promoted to a curved doubly-good
overlap.  Adding more full-row equations without such a rank-changing
source operation does not turn the two selected `2x2` minors into the
required four rank-three stars.

## Reproduction

```bash
python3 computations/verify_h3_one_bad_crossed_quadratic_oo_landing_guard.py
python3 -O computations/verify_h3_one_bad_crossed_quadratic_oo_landing_guard.py
```
