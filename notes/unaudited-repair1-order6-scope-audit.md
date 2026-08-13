# The repair-1 probe proves an ungraded shadow identity, not the Gate-I chain map

## Sharp interpretation

The external repair-1 computation gives a genuine cross-module check:

\[
          D_2(\Theta_{343})=\operatorname{shadow}_2(K_{\rm phys})
\]

after forgetting the raw fine shift.  Both sides have 16 terms, and the
coefficient vector `(-1,+1,+1,-1)` is derived from the physical involutions
rather than copied into both computations.

This is useful associated-graded evidence, but it is not the selected Gate-I
equation

\[
             J_3(M_v)=A J_{\rm col}(u_{024}-u_{012}).       \tag{1}
\]

The probe domain is the 8,580-column order-six coefficient-operator block.
Its codomain is a coloured codimension-two cell-pair shadow.  Equation (1)
instead starts with one vector in the 15-label collision/repeated-edge
module and lands in the 360-feature literal repeated-`P3+K2` boundary plus
`Eq`, target, `ainc`, ordinary residue and eta/sigma.  The probe never builds
`J_col`, applies it to the selected collision vector, or evaluates those
augmented rows.  It therefore neither proves nor disproves (1).

The frozen checker is
[`verify_unaudited_repair1_order6_scope_audit.py`](../computations/verify_unaudited_repair1_order6_scope_audit.py).

## Three exact warnings

First, the displayed equality does not refine grade by grade.  The two raw
operator shifts have supports 39 and 24, whereas the two physical word rows
used for the proposed `K` have supports 10 and 10.  Neither raw shift is
identified with either physical row.  Thus an identity-on-grade comparison
is false for this representative; a shifted tail or total-degree translation
would be new data.

Second, `shadow_2` does not pin the physical `K`.  In the two-row target
inventory its fibre has dimension 21.  All encoded parity, corner, aggregate
and coarse readouts have rank 14 on that fibre, leaving seven explicit
shadow-zero directions.  In particular the comparison does not establish
termwise `H_w`, private full-nine rows, or eta/sigma on the corner grade.
Those were precisely the inputs used to promote the cap/Cartan signature to
the complete output-side `M_v` claim.  Until one of the higher readouts is
constructed, that promotion must remain conditional.

Third, the whole order-six operator kernel cannot map to a target containing
only direct-free disjoint-cell pairs by the naive shadow comparison.  In both
tested primes, the attainable `D2` space has dimension 488 and its projection
to site-repeating pair coordinates has rank 153.  The robust conclusion is
that the projection is nonzero in both reductions and that a universal target
would need site-repeating terms.  The number 153 is a matching two-prime
modular rank, not an exact rational dimension certificate.

## Selected-class frontier

The selected lower cycle still has the useful reduction

```text
l = u024-u012, with 12 nonzero labels and 3 zero shared labels,
partial collapse(l)/2 = B0+B2-B3-B5.
```

Hence a full map on all 15 labels and the two shared-loop repair columns are
stronger than this one cycle requires.  But the exact remaining datum is not
eliminated: expose the complete physical `J_col(l)` and compare it to a
termwise physical `M_v` in one common word/fine/repeated grade.  The
repair-1 probe checks a different order-six shadow and cannot substitute for
that row-by-row calculation.

## Verification

```text
python3 computations/verify_unaudited_repair1_order6_scope_audit.py
python3 -O computations/verify_unaudited_repair1_order6_scope_audit.py
python3 -I -S computations/verify_unaudited_repair1_order6_scope_audit.py
```

Frozen ledger SHA-256:

```text
f4b46116dc1b766c6d5e9777169fa7d67ac9785214e8ccd860d9f585af01a2de
```
