# The two remaining unary attachments cannot enter at positive Rees order

## Result

The two attachment types left by `efac2b2 + 336492c` are rigid in the
completed neighbourhood of the `c536b88` transfer family.  Neither

1. an off-diagonal decoration on a selected anchor edge, nor
2. a simultaneous deformation of the coordinate-`11/22` slices

can enter with positive Rees order while preserving the unary top and the
aggregate diagonal response.

The proof retains actual source rows.  Put an independent positive-order
coefficient on every non-`00` decorated cell of all 28 physical edges—224
directions in total, including every anchor-edge off-diagonal cell and every
change of the old `11` slice.  For the 22 literal unary/response rows in the
integral `efac2b2` certificate, complete matching expansion gives

\[
                         G_i(\epsilon)=g_i+O(\epsilon), \tag{1}
\]

where the `g_i` are exactly the pinned source generators.  With the same
integral multipliers `A_i(z)`,

\[
 \sum_i A_i(z)G_i(\epsilon)=1+B(\epsilon),
 \qquad B\in(\epsilon).                                \tag{2}

The right side is a unit in the `epsilon`-adic completion.  Hence the full
deformed source ideal is the completed unit ideal.

Checker:
`computations/verify_uniform_axis_circuit_k3_unary_attachment_rees_rigidity.py`.

## Source and deformation inventory

The special fibre is the source-valid system of `efac2b2`:

```text
all 28 pure-00 edge coefficients arbitrary,
the seven c536b88 coordinate-11 cells fixed,
q^[4] = X0,
(e1@0+e1@1+e1@2)(e1@7) q^[3] = X1.
```

For every edge `uv`, the deformed quadratic adds

```text
epsilon*y_uv_ab * (uv:ab),    (a,b) != (0,0).
```

This includes all ordered ternary off-diagonal cells, arbitrary changes to
the existing `11` coefficients, and arbitrary new `11/22` cells.  The
pure-zero coefficients stay in the base ring because `efac2b2` already made
all of them arbitrary.

The checker reconstructs each of the 22 selected coefficient rows directly
from perfect matchings.  It verifies (1) monomial by monomial, forms the
left side of (2), and checks that its degree-zero part is exactly `1`, while
every other monomial has Rees degree between one and four.  Therefore

\[
 (1+B)^{-1}=\sum_{n\ge0}(-B)^n
\]

exists formally.  No tangent-only inference or declaration of higher
cofactor data enters the proof.

## Classification of the attachment gate

The result turns the two apparent deformation types into a leading-face
alternative:

* If either type has strictly positive order over the `c536b88` face, (2)
  is a completed source unit.
* A nonanchor off-diagonal cell already present in the leading face routes
  to a rank-`(3,3)` good pair and an active minor by `336492c`.
* For a leading same-site diagonal switch, `f9b51a9` gives the exact full
  five-row lock.  If that lock vanishes, the switch is an anchor-safe
  support descent.

Thus the smallest genuinely new branch is not a further infinitesimal
deformation of the transfer chart.  It is a **leading** decorated-anchor
edge/diagonal alternating-cycle web with a nonzero unary-or-companion lock.
The two-cycle counterguard in `f9b51a9` shows that cycle combinatorics alone
does not promote such a lock to a transverse head.

This is the sharp next source hypothesis: use the full one-bad unary and
companion rows to turn a nonzero leading lock into either a distinct-head
four-good active overlap or another simultaneous anchor-safe switch.

## Scope

This is a formal/completed initial-face theorem.  It does not claim global
affine emptiness away from the `c536b88` special fibre, and it does not claim
that every leading lock is already clean or curved.  The second colour and
crossed rows are not artificially imposed on a nonexistent attachment;
they enter only in the named leading-lock branch where the unary source is
genuine.

## Verification

Run

```text
python3 computations/verify_uniform_axis_circuit_k3_unary_attachment_rees_rigidity.py
python3 -O computations/verify_uniform_axis_circuit_k3_unary_attachment_rees_rigidity.py
python3 -I -S computations/verify_uniform_axis_circuit_k3_unary_attachment_rees_rigidity.py
```

The checker pins `efac2b2`, `336492c`, and `f9b51a9`; audits the complete
positive-order cell inventory and the exact matching coefficients; and
freezes the combined Rees tail before accepting the formal unit.

Frozen ledger SHA-256:

```text
7149416452410d3329dd0dd3ab2e975a7b152f71a1ce21fb75f8d086bcf2bf06
```
