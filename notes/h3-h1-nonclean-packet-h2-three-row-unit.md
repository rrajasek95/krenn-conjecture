# Three Hamming-two rows kill the Hamming-one-complete nonclean packet

## Outcome

The packet in
[`h3-hamming-two-tangent-or-clean-boundary.md`](h3-hamming-two-tangent-or-clean-boundary.md)
and `verify_h3_hamming_two_sum_clean_tail_boundary.py` has good shared
stars, satisfies all 351 pure and Hamming-one coefficients, and has selected
response layers

\[
                         (Q_0,Q_1,Q_2,Q_3)=(1,-1,-12,0).
\]

Thus its admitted selected top row is zero while its clean tail is
\(\chi_2=-12\).  Freeze its pure diagonal \(q\)-cells, direct block, and
stars, but free all 90 ordered cross-colour cells on the 15 physical
\(q\)-blocks.  Write \(F_{ij}(w)\) for the literal full-nine residual.
Exact expansion gives

\[
 \boxed{
 F_{00}(001111)-F_{01}(000011)-F_{01}(001100)=1.}       \tag{1}
\]

Every one of the 90 free cross-cell coefficients cancels in (1).  All
three words are at Hamming distance two from a pure word.  Consequently
there is no Hamming-two lift of this packet over any solution of its
Hamming-one rows—or indeed over any assignment of the cross-colour cells.

This is the requested literal Fredholm/unit certificate.  It uses three
full source-labelled rows with constant integral weights and no division,
localization, support restriction, Hasse truncation, or Hamming-one
multiplier.  For context, the nonzero Hamming-one system in the 90 free
cells has 70 equations, exact rank 34, and nullity 56; none of that
elimination is needed for (1).

## Consequence and scope

Together with the five-row Hamming-one obstruction for the earlier
pure-nine family, (1) removes both known nonzero-tail packets from the
candidate counterexample lane at their first missing physical layer.  In
particular, the seven selected-row Hamming-two residuals previously listed
for this packet cannot be simultaneously repaired by changing unexposed
cross-colour cells; two companion rows supply the unit.

The fixed pure slices and stars remain load-bearing.  Equation (1) does
not yet prove the universal tangent-or-clean theorem

\[
   \text{all nine full tensor rows and goodness}\Longrightarrow\chi_c=0.
\]

A universal proof must show that every nonzero-tail pure/Hamming-one normal
form admits a transported version of this three-row unit, or derive a
packet-independent weighted Hamming-two identity from the marked
normal-incidence maps.

## Verification

Run

```text
.venv/bin/python computations/verify_h3_h1_guard_h2_three_row_unit.py
```

The checker re-verifies the 351 admitted coefficients, good Segre stars,
the layer ledger and \(\chi_2=-12\); expands all 90 cross-cell variables;
checks (1) as a literal polynomial identity; and independently recomputes
the Hamming-one rank/nullity ledger over \(\mathbf Q\).
