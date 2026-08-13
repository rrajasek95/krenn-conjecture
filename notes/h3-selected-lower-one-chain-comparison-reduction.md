# Gate I for the selected marked lift is one chain equation, not a full `U15` map

## Outcome

The determinant-dark marked lift uses one explicit collision vector

\[
                         \ell=u_{024}-u_{012}.
\]

It has twelve nonzero coordinates in the fifteen-dimensional physical
`(matching,repeated edge)` module.  The remaining three coordinates are the
shared repeated-`02` labels, and all three coefficients are exactly zero.

Therefore the full comparison

\[
 \Phi:U_{15}\longrightarrow L_{h=3},\qquad J_3\Phi=A J_{\rm col}
\]

is stronger than this selected marked lift needs.  It is enough to construct
one physical cell `C` satisfying

\[
                         J_3C=A J_{\rm col}(\ell).       \tag{1}
\]

The filtered top has the opposite boundary, so (1) cancels its lower face.
Because `C` is in collision/relative grade, the ordinary marked occurrence
remains one.  No value of `Phi` on a zero-coefficient shared label enters
this calculation.

Checker:
[`verify_h3_selected_lower_one_chain_comparison_reduction.py`](../computations/verify_h3_selected_lower_one_chain_comparison_reduction.py).

## The candidate is already unique and fully typed on the output side

On the twelve nonzero labels, the canonical partial collapse

```text
(4,2,4,1,5,3)
```

has signed image

\[
                    2(B_0+B_2-B_3-B_5).
\]

After the forced factor `1/2`, this is the literal four-corner alpha
aggregate.  Expanding the six canonical pure columns gives exactly 360
distinct seven-edge boundary features.  The physical cell

\[
                         M_v=-O_\alpha+K
\]

has this boundary, with exact augmented typing

```text
ordinary residue       0
D,W,target,ainc         0
eta_z                   1+delta_(vz) u_z/t
sigma                   -q_pq^22.
```

Changing the three shared columns arbitrarily—including inserting the
augmentation-one fixed/pair Hasse repairs—does not change the image of
`ell`.  Thus the shared-loop product-rule cells address extension to a
reusable map on all `U15`; they are not logically required for this one
marked kernel.

## What is still missing

The current twelve-label theorem establishes the occurrence collapse and
the exact candidate on the literal output side.  It does **not** expose the
complete protected/source-labelled input boundary `J_col(ell)`.  Hence (1)
cannot yet be checked row by row.

This is a real gap, not a request for more support enumeration.  The checker
gives two complete input boundary maps with identical disclosed occurrence
rows.  One has hidden/private value zero on `ell`; the other has value one.
Only the first can satisfy a candidate equality with zero in that row.
Consequently occurrence equality and the 360-feature output census do not
determine the full chain equation.

The smallest remaining datum is therefore:

> expose the complete protected differential of the single signed lower
> packet and prove the one equality `J3(M_v)=A J_col(ell)` in the exact
> word/fine/repeated grade.

Equivalently, construct one source-provenant relative Cartan--Spencer cell
whose boundary is that difference.  This is smaller than constructing the
fixed and paired shared-loop cells.

## Effect on the larger proof

For the local determinant-dark marked-kernel branch, the frontier contracts
from two shared-loop orbit cells to one full-row nullhomotopy equation.

A full `U15` comparison is still useful—and may still be required—for:

- uniform reuse on arbitrary collision vectors;
- `q` transport on every protected kernel vector;
- inactive normal-grade and diagonal-Rees propagation.

So this reduction shortens Gate I for the selected proof branch; it does not
claim that the shared-loop construction is globally useless.

## Verification

Run:

```text
python3 computations/verify_h3_selected_lower_one_chain_comparison_reduction.py
python3 -O computations/verify_h3_selected_lower_one_chain_comparison_reduction.py
python3 -I -S computations/verify_h3_selected_lower_one_chain_comparison_reduction.py
```

Frozen ledger digest:

```text
328a8cdb2fed59cc115a218b8ba68d131b764335fed96e06c093d986c74117a1
```
