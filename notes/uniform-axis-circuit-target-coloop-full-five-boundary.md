# Aggregate full-five rows do not break the affine target coloop

## Exact boundary

The rank-restoration theorem in `001e692` leaves one sharp case: the
selected opposite-colour arm is a physical coloop of a pure target matching
family.  Adding the other diagonal and both crossed tensor equations does
not remove that case by linear algebra on the five aggregate rows.

There is an exact rational `k=3` row module with feature basis

```text
top:X0,
11:X1, 11:A, 11:B, 12:U, 12:V,
22:X2, 22:C, 22:D, 21:W, 21:Z.
```

The three complete columns of the first endpoint row are

\[
 (X_1+A,U),\qquad(-A+B,-U+V),\qquad(-B,-V),             \tag{1}
\]

and the second row has the identical pattern with
`X2,C,D,W,Z`.  Each triple has rank three and sums to its required diagonal
target with crossed sum zero.  The unary row is the independent exact
coordinate `X0`.  Hence all five typed sums are

\[
 q^{[h]}=X_0,quad R_{11}=X_1,quad R_{12}=0,quad
 R_{21}=0,quad R_{22}=X_2.                              \tag{2}
\]

Nevertheless `X1` and `X2` occur only in the first port of their respective
circuits.  Both avoiding columns are nonzero, and the complete-column maps
are injective, so there is neither a deletion nor an affine translation to
an avoiding target port.  An active outside component from one circuit can
therefore be paired with a distinct-head selected component of the other,
while the latter remains a rank-two target coloop at the selected-matching
level.

Checker:
`computations/verify_uniform_axis_circuit_target_coloop_full_five_boundary.py`.

## What the crossed rows do and do not say

The mixed debts in (1) cancel in the **complete** crossed rows; no selected
coefficient has been omitted.  The other diagonal circuit is simultaneously
minimum and exact.  Thus a further linear combination of the five aggregate
tensor identities cannot force an avoiding matching.

This does not construct a physical common-`q` source.  The displayed columns
are a typed rational module, not declared hafnian cofactors.  Its role is to
identify the first indispensable physical datum:

> a literal common-`q` matching-exchange relation must couple a tail in the
> active outside column to the coloop diagonal tail before those terms are
> summed into the aggregate tensor rows.

At `h=3` this is a four-hole Hessian/Pluecker coefficient.  The ordinary
Hessian Euler recurrence within one column is insufficient, as already
shown by the axis-Hessian carrier circuit.  What is missing is the
cross-column, common-tail exchange with both endpoint labels retained.

## Consequence

The global affine accessibility gate now has a precise split.

* If the opposite selected arm is repairable by an alternate diagonal or
  unary matching, `001e692` gives the distinct-head four-good active wedge.
* If it is not repairable, it is a target-family coloop.  All five aggregate
  rows can retain that coloop, so the next theorem must use literal common-q
  cofactor provenance—not another endpoint-support or row-span argument.

The checker does **not** claim a Krenn source or refute a source-level
coloop exclusion.

Run

```text
python3 computations/verify_uniform_axis_circuit_target_coloop_full_five_boundary.py
python3 -O computations/verify_uniform_axis_circuit_target_coloop_full_five_boundary.py
python3 -I -S computations/verify_uniform_axis_circuit_target_coloop_full_five_boundary.py
```

Frozen ledger SHA-256:

```text
14ae260e94c71d1cc99a1063a66ece6cd599cec7496948fce486e34179ce6dba
```
