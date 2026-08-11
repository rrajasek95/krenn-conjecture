# One-sided proportionality is unconditionally anchor-safe for `nu`

## Result

The conservative companion boundary in `6dc3bd5` allowed one apparent
exception to its exact one-sided deletion: the proportional update might
cancel a companion decoration used by a selected matching.  That exception
does not survive the actual lexicographic invariant.

Recall that `nu` counts **mutual coordinate anchors**: a nonzero scalar cell
is an anchor only when both of its coordinate endpoints have degree one in
the scalar support graph.  The outside and companion cells are distinct
nonzero components of one `p_i` row (or one `s_j` row).  They therefore share
the coordinate endpoint `(P,i)` (respectively `(S,j)`), whose degree is at
least two.  Neither cell is a mutual anchor.

Checker:
[`verify_h3_axis_target_coloop_proportional_nu_safe_reduction.py`](../computations/verify_h3_axis_target_coloop_proportional_nu_safe_reduction.py).

## Exact finite move

With the common `q` and opposite endpoint fixed, suppose the complete
labelled columns obey

\[
 {\mathcal L}(z_{\rm out})=\lambda{\mathcal L}(z_{\rm cmp}).   \tag{1}
\]

Writing their current scalar coefficients as `x_out,x_cmp`, make the exact
one-sided update

\[
 x_{\rm out}'=0,\qquad
 x_{\rm cmp}'=x_{\rm cmp}+\lambda x_{\rm out}.         \tag{2}
\]

All four response tensors are unchanged by linearity; the unary top and
the other endpoint rows do not change.  No new scalar cell is introduced.
If the second coefficient in (2) is nonzero, one cell is deleted.  If it is
zero, both same-row cells are deleted.

Every old mutual anchor lies on a different cell.  Deleting edges of a
support graph cannot destroy such an anchor: each of its endpoints already
had degree one, so no deleted edge was incident there.  Hence

\[
                         \nu(A')\geq\nu(A),             \tag{3}
\]

while support strictly decreases.  This contradicts maximum `nu`, then
minimum support in both update strata.  The checker exhausts all ambient
support graphs on six coordinate vertices around the two same-row cells
and verifies the inclusion of old anchors into new anchors, with and without
companion cancellation.

The phrase “protected companion decoration” remains meaningful for a fixed
chosen matching witness, but it is not protection under `nu`.  Since the
full response tensor is preserved, target exactness is also preserved and
the witness may be reselected if necessary.

## Consequence and scope

At the synchronized representative, proportional complete columns are
impossible.  The only branch left from `6dc3bd5` is therefore

```text
both one-sided complete-column pairs nonproportional,
then external q mate or selected-word bistar/Fitting carrier.
```

This promotion still requires proportionality of the **complete** labelled
tensor columns.  It does not turn one selected coefficient, or the
selected-word corner determinant, into a complete-column relation.

Run

```text
python3 computations/verify_h3_axis_target_coloop_proportional_nu_safe_reduction.py
python3 -O computations/verify_h3_axis_target_coloop_proportional_nu_safe_reduction.py
python3 -I -S computations/verify_h3_axis_target_coloop_proportional_nu_safe_reduction.py
```

Frozen ledger SHA-256:

```text
151e0588d4047c09da0e385c3c8eae2a577ffc106d0cb8415a577670989e774d
```
