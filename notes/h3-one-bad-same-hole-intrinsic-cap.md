# The quadratic same-hole route already contains the intrinsic one-edge cap

Date: 2026-08-11

Checker: `computations/verify_h3_one_bad_same_hole_intrinsic_cap.py`

## Verdict

The same-hole quadratic branch from `1ca72d6` needs no new principal-parts
normalization.  In the complete physical nine-row packet on the outer pair
`p=5,r=7`, the literal row

```text
K = E_tt
```

already has exactly the hypotheses of the intrinsic theorem `a67ec1d`:

```text
direct scalar s(K) = D_tt = 0,
target ledger       = (0,0,1),
response            = (P_t@1)(R_t@4),
response support    = the single physical edge {1,4}.
```

Its edge response matrix has only `U_tt=1`.  Thus it is on the surviving
inactive-clean boundary of the intrinsic determinant theorem; any departure
from that boundary is an ordinary localized source unit.

The two new same-hole cells `P_c@1,R_c@2` occur in the different outer row
`(c,t,c)`.  They cannot alter the `(t,t)` cap row.  Consequently the shorter
quadratic route closes before any cubic or quartic mate is considered.

## Literal source labels

Delete the selected pair `p=5,r=7` and order the residual sites as

```text
(0,1,2,3,4,6).
```

The selected direct block is

```text
D_pr = E_cc,
```

so `D_tt=0`.  The cap endpoint forms are the singleton rows

```text
P_t = e_t@1,      R_t = e_t@4.
```

Their product is the whole ternary response, not merely a binary
projection.  Hence the response is supported on edge `14`, with edge matrix

```text
U = E_tt.
```

This is a literal one-row contraction of the nine original `p-r` rows.  No
declared jet column, division, Hasse derivative, or target-forgetting row is
used.

## Target and ordinary residue

At the sparse guard point, the full `(t,t)` row has exactly two residual
coefficients:

```text
222222 : 1   (the target),
122221 : 1   (ordinary mixed residue).
```

In global eight-site labels these are

```text
22222222 = (15:22)(47:22)(06:22)(23:22),
12222212 = (15:22)(47:22)(06:11)(23:22).
```

After target subtraction, the sole residue is therefore the mandatory
mixed coefficient `12222212`.  Its value one shows that the displayed
sparse packet is not a full source.  In an actual source the complete row,
including this coefficient and all its possible cancellation mates, is
zero.  The intrinsic single-edge determinant then gives the ordinary
unit/clean-cap dichotomy without having to isolate those mates.

This is why the target and ordinary-residue ledgers must not be conflated:
the target coefficient is correct at the guard point, but the full physical
row is not.

## Relation to the same-hole mate

The quadratic mate has outer source label `(c,t,c)` and word `21000121`.
The cap has selected outer pair label `(t,t)`.  Since the new mate cells
carry outer colours `c`, they do not enter `K=E_tt`, even with arbitrary
coefficients.  The same-hole alignment therefore does not create an
obstruction to the cap; it merely lives in a companion mixed row.

## Scope

This closes the exact literal quadratic same-hole normal form.  It does not
assert that `P_t,R_t` remain singleton after arbitrary higher-order source
deformations.  Such deformations are outside the six quadratic mate layer
and would require a separate filtered stability statement.  No cubic or
quartic support layer was expanded here.
