# The three CCE boundary cells are uniformly injective

## 1. Outcome

The complete response has rank (19) everywhere on each of

\[
                         CCE,\qquad CEC,\qquad ECC.
\]

This is certified by exact maximal-minor ideals over the rational parameter
rings of the three four-dimensional cells.  Every selected row avoids source
pair (01), so the conclusion allows an arbitrary direct (B_{01}) scale.

## 2. Exact certificates

For each placement, the checker first chooses 30 sparse 19-row bases at a
fixed list of rational cell points.  It then adds row sets selected at finite
field points:

\[
\begin{array}{c|ccc}
\text{cell}&CCE&CEC&ECC\\ \hline
\text{additional row sets}&21&21&22.
\end{array}
\]

The finite-field coordinates are used only to select row labels.  For every
such label set, the structurally specialized determinant is recomputed by
fraction-free elimination over (\mathbb Q), replaced by its squarefree
support, and adjoined to the rational ideal.  The exact standard basis of
each final ideal is ((1)).  Hence the selected maximal minors have no common
zero over an algebraic closure, which proves uniform rank (19).

The modular discovery has an independently useful audit trail.  For CCE and
CEC, the first 17 additional determinants remove the residual
\(\mathbf F_{17}\)-curve, one removes the remaining \(\mathbf F_{19}\)-points,
and three remove the \(\mathbf F_{23}\)-points.  ECC uses 18, one, and three
row sets at those primes.  These modular exhaustions are not themselves the
proof; the final rational unit ideals are.

## 3. Exact audit

[verify_live_three_zero_minimal_three_extra_cce_cells.py](../computations/verify_live_three_zero_minimal_three_extra_cce_cells.py)
reconstructs all determinants and verifies the three unit ideals.  The
finite-field discovery and exact CAS serialization are in
[explore_live_three_zero_minimal_three_extra_remaining_cells.py](../computations/explore_live_three_zero_minimal_three_extra_remaining_cells.py).
