# Opposite-shore activity obstruction for the alternating-C8 OO chart

The alternating-C8 packet in
[`oo-doubly-good-two-anchor-counterguard.md`](oo-doubly-good-two-anchor-counterguard.md)
has two adjacent rank-one arms `02` and `04`, four full-rank deleted-star
maps, and nonzero curvature, but both arm cofactors vanish.  This note asks
for the smallest honest repair: keep that packet fixed and add arbitrary
endpoint-coloured cells on the opposite shore

\[
R=\{1,3,5,7\}.
\]

There are six physical pairs in `R` and nine endpoint-colour cells per
pair, hence 54 possible cells.  The exact audit proves that no subset of
these cells can both activate the selected arms and complete the packet to
the ternary target.

## Exact obstruction

Among the 54 cells, 45 enter the output tensor and nine are inert.  Every
productive cell creates exactly two mixed output words, with coefficient
equal to its symbolic cell weight.  The resulting 90 words are pairwise
disjoint across all candidate cells.  The activity census is

\[
\begin{array}{c|rrrr}
\text{active arms}&\varnothing&02&04&02,04\\ \hline
\text{number of cells}&9&9&18&18.
\end{array}                                                   \tag{1}
\]

In particular, every cell that activates either selected arm is
productive.

This one-cell ledger controls arbitrary support subsets, not merely
one-cell perturbations.  Any perfect matching in the enlarged chart uses
at most one new `R--R` cell: shore balance would require an equal number of
internal edges on the left shore, while the only left-shore edges are the
triangle `02,04,24`, none incident to vertex 6.  Two disjoint left-shore
edges therefore do not exist.  Consequently tensor contributions are
linear in the 54 new cell variables.  Since the 90 mixed words have unique
cell owners, a selected nonzero active cell leaves a nonzero mixed
singleton.  No complex cancellation is available.

Thus every one of the `2^54` opposite-shore support extensions that makes
both cofactors nonzero fails the full nine target equations.  The four
star minors, the two rank-one arm heads, and the curvature coordinate are
unchanged by these additions.

## Scope and next boundary

This closes the complete opposite-shore completion chart of the inactive
two-anchor guard.  It is source-faithful and allows arbitrary complex
weights, but it is **not** the full active OO saturation: new cross-shore
cells or additional cells on the left shore can supply mates for the 90
words.  Therefore an actual active guard, if one exists, must leave this
nearest toric chart.

The proposed active-cofactor split

\[
Q_{02}=t z^{[2]},\qquad Q_{04}=y z^{[2]},\qquad
D=A t-B y                                                   \tag{2}
\]

is consistent with the obstruction: within this chart the two cofactor
branches cannot even be made simultaneously active without a unique mixed
term.  Testing whether full-nine head-column rows kill the proportional
branch of (2) now necessarily requires at least one cross-shore or new
left-shore cell.  That is the next honest finite saturation boundary.

## Reproduction

Run

```text
python computations/verify_oo_c8_opposite_shore_activity_obstruction.py
python -O computations/verify_oo_c8_opposite_shore_activity_obstruction.py
```

The checker reconstructs all 54 cells, all supported physical matchings,
both deleted cofactors, and the complete 90-word ownership ledger using
exact rational arithmetic.
