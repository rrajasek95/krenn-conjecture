# The degenerate canonical `C6` leaves one response-silent attachment

## Exact result

At the canonical word `z=012111`, the eight anchor-contained unary
matching classes of `3836903` are

```text
M  = 01:01 | 23:21 | 45:11
N  = 05:01 | 12:12 | 34:11
Q1 = 01:01 | 24:21 | 35:11
Q2 = 02:02 | 13:11 | 45:11
Q3 = 02:02 | 14:11 | 35:11
Q4 = 02:02 | 15:11 | 34:11
Q5 = 05:01 | 13:11 | 24:21
Q6 = 05:01 | 14:11 | 23:21.
```

The complete shifted response rows and unary complement split them into
four signed pairs:

```text
E01=M+Q1,   E13=Q2+Q5,   E34=N+Q4,   E14=Q3+Q6.       (1)
```

The selected classes `M,N` are localized, so their partners `Q1,Q4` are
localized as well.  The remaining pair supports have an exact trichotomy.

1. If both `E13` and `E14` are occupied, the toric identity

   ```text
   Q1*Q2*Q6 = M*Q3*Q5
   ```

   contradicts the four signs in (1).  This is the dense odd-holonomy unit
   of `3836903`.
2. If `E13` alone is occupied, `Q2,Q5` share the literal cell `q13:11`.
   They are the two retained tails in the physical shifted coefficient
   `G21[012211]`.  Hence this is a source-typed `q13` response chord, not a
   merely graph-theoretic bridge; it enters the pinned two-`C4` response
   route.
3. The support with neither optional pair consists of two disconnected
   flat `C4`s, `{M,Q1}` and `{N,Q4}`.  If `E14` alone is occupied the
   matching graph becomes connected, but its common `q14:11` cell is not
   yet a response attachment.  A physical `G11[z]` hole-`14` column also
   requires

   ```text
   p1_1:1*s1_4:1  or  p1_4:1*s1_1:1.                  (2)
   ```

   Without (2), the `Q3+Q6` pair is the minimal response-silent
   spoke-to-hole guard.

Checker:
`computations/verify_h3_c6_degenerate_pair_transport_guard.py`.

## The literal hole-`14` comparison

Deleting sites `1,4` leaves `0,2,3,5`.  The complete hafnian tails are

```text
02:02|35:11 = Q3/q14,
05:01|23:21 = Q6/q14,
03:01|25:21 = the third tail.                          (3)
```

Thus (2) turns the first two summands of (3) into one genuine physical
response column.  If the third tail or a different endpoint hole is
present, it is precisely an asymmetric internal-tail or endpoint
companion.  If (2) is absent, common matching incidence alone cannot
declare a source `2`-cell.  This is why the formal analogy with freely
adjoining a resolution generator is incomplete: the comparison multiplier
must be an occupied physical endpoint product.

The checker gives rational coefficient-level guards for both the minimal
four-class support and the six-class `E14` support.  They satisfy all pairs
in (1) that are present.  They are not asserted to be full one-bad source
points; their role is to prove that the missing hole-`14` endpoint product
is load-bearing.

## Contamination of the minimal-core two-row unit

The normalization correction `34428df` makes the extension formula exact.
Write the two rows from `7320475`, after extra internal-tail terms are
allowed, as

\[
 F_t=aP+\Delta_t-1,\qquad F_z=bP+\Delta_z.
\]

Then the ordinary source combination is

\[
 (a/b)F_z-F_t
   =1+(a/b)\Delta_z-\Delta_t.                         \tag{4}
\]

Consequently:

- proportional contamination, `Delta_z/b=Delta_t/a`, preserves the
  two-row unit exactly;
- otherwise a source zero forces the normalized asymmetric difference in
  (4) to equal `-1`.  At least one literal monomial in that difference is
  nonzero, so the source has acquired a genuine internal-tail/endpoint
  edge.

The second alternative is source-typed existence, but not automatic rank
completion.  The new edge may remain anchor-contained; it must next enter
the complete-column deletion/Fitting/Hall routing.  This is exactly the
source-exhaustivity obligation, with the response-silent `E14` pair as its
smallest canonical guard.

## Scope

This theorem is an exact Laurent matching-class classification plus literal
row typing for the first canonical `h=3` transgression.  It closes the dense
and `E13` strata and isolates the first physical attachment missing in the
other two strata.  It does not infer support deletion from a response-silent
internal cell, nor claim that every asymmetric contaminating tail already
has deleted-star rank three.

## Verification

```text
python3 computations/verify_h3_c6_degenerate_pair_transport_guard.py
python3 -O computations/verify_h3_c6_degenerate_pair_transport_guard.py
python3 -I -S computations/verify_h3_c6_degenerate_pair_transport_guard.py
```

Frozen ledger SHA-256:

```text
06224f08840a7c1211c47fd59efecf18e05787813af4f0252bdc1229d88d0e4e
```
