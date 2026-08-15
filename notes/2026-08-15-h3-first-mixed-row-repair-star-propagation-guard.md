# The first mixed defect propagates to a smaller rootless guard

## Exact verdict

The first missing row of the 20-cell guard `c8a0383`, together with every
EqSystem row jointly forced by its two rootless-repair stars, does not yet
give a contradiction.  There is a support-minimal literal physical repair
that preserves common (q), the exact labelled GHZ quotient slices, the
direct/(K_*) relation, activity, and projective rootlessness.

The exact monotone propagation is

\[
  20\text{ cells}/106\text{ defects}
  \longrightarrow 22/102
  \longrightarrow 23/100.
\]

At the last node an old 12-row defect orbit has been replaced by a new
six-row private orbit.  Thus the attack makes genuine progress—the defect
orbit strictly shrinks—but it does not produce a unit ideal or a common
root.  No literal recurrence occurs at this stage.

## The complete two-star orbit

In the packet of `c8a0383`, delete either of the two cells

\[
  p_0(4,0)=-1,\qquad s_1(5,1)=-1.
\]

An exhaustive comparison of all 6,561 scalar EqSystem rows shows that the
only changed rows are

\[
  (0,1;01d01),\qquad
  d\in\{00,01,11,22\}.
\]

Each has value (1) in the 20-cell packet and target zero.  This is the
complete source-provenant row family jointly supported by the two repair
stars, not a selected subset.  Deleting either star restores the clean gcd
(z(z+1)) and drops the projective Macaulay rank from six to four.

The first full-source defect preceding this orbit is

\[
  (0,0;000011)=1.
\]

There are 225 absent physical (q,p,s) cells in the fixed chart.  Exact
affine-linear enumeration proves that no single one of them, with any
nonzero rational coefficient, can kill this row while preserving the
original 36 certified rows.  Hence every monotone repair needs at least two
new cells.

## A support-minimal physical repair

Add exactly

\[
  q_{05}^{01}=1,\qquad p_0(4,1)=-1.
\]

These two cells kill the first row and all four two-star rows.  If their
coefficients are denoted (t) and (r), respectively, the literal
EqSystem rows in this two-variable chart are

\[
\begin{aligned}
(0,0;000011)&=1+rt,\\
(0,1;01d01)&=1-t
  &&(d=00,01,11,22),\\
(0,0;000001)&=-t.
\end{aligned}
\]

Thus the repaired rows force (t=1) and (r=-1).  In this two-variable
chart the next private equation would force (t=0), and the ideal is unit:

\[
  (1-t)-(-t)=1.
\]

This is a sharp local terminal for that chart, but not for the full physical
coefficient space: additional cells can cancel the private row.

At (t=1,r=-1), the new negative response term is the branch

\[
  (1,4)\mid(05)(23).
\]

It cancels the old positive branch in (000011), and it cancels the joint
repair-star branch in each (01d01).  At (000001), however, it has no old
mate and gives the new value (-1).  This is the precise propagation face.

## The first continuation and the smaller guard

After imposing the 36 original rows, the repaired first row, the four star
rows, and the first private row, an exact census of the remaining 223 cells
finds exactly three one-cell continuations:

\[
 q_{14}^{00}=-1,\qquad
 q_{34}^{00}=1,\qquad
 q_{45}^{01}=1.
\]

Their full defect counts are (111,100,121), respectively.  The middle
choice is therefore the smallest continuation:

\[
  q_{34}^{00}=1.
\]

For this 23-cell packet, comparison with the original 20-cell ledger removes
exactly the 12 positive rows

\[
\begin{cases}
(0,0;00d11),\\
(0,1;01d01),\\
(0,2;02d11),
\end{cases}
\qquad d\in\{00,01,11,22\},
\]

and creates exactly the six negative rows

\[
\begin{cases}
(0,0;00d01),\\
(0,2;02d01),
\end{cases}
\qquad d\in\{01,11,22\}.
\]

No surviving defect changes coefficient.  The propagation is therefore an
exact (12\to6) orbit replacement, rather than a coarse defect-count
comparison.  The next lexicographic full-source defect is the old row

\[
  (0,0;000022)=1,
\]

while the first newly created private row is
((0,0;000101)=-1).

## Generic and rootless checks

Both the 22-cell node and the 23-cell node have endpoint-star ranks
((3,3,6)), (q^{[3]}) independent from the three pure targets, and the
three exact quotient slices (E_{00},E_{11},E_{22}).  They pass the complete
literal common-(q) audit: all Hessian, first-derivative, ordered Schreyer,
and 6,561 nine-row reconstruction equations.

The direct matrix remains

\[
 a=\begin{pmatrix}-1&-1&0\\0&0&0\\0&0&0\end{pmatrix},
 \qquad K_*=I-E_{01},
\]

and the activity remains (z^3(-1-z)).  At each node the clean gcd is (1),
the projective Macaulay rank is six, and a displayed greedy (6\times6)
minor has determinant (-192).  Hence the smaller packet is still in the
generic rootless branch; the shrinkage is not obtained by falling onto the
common-root terminal.

## Scope and next attack

The 23-cell endpoint is not a full exact GHZ source.  This result proves
support minimality only for repairing the first row from the fixed 20-cell
chart, and gives the complete one-cell continuation census at the next
private row.  It does not classify arbitrary multi-cell repairs elsewhere
in coefficient space.

The next economical attack is to enforce the six-row private orbit as a
family, not one row at a time, together with (00{:}000022).  A contradiction
would show that the (12\to6) shrink cannot repeat; a further rootless packet
would provide the next monotone DAG node.

## Reproduction

```text
python3 computations/verify_h3_first_mixed_row_repair_star_propagation_guard.py
python3 -O computations/verify_h3_first_mixed_row_repair_star_propagation_guard.py
python3 -I computations/verify_h3_first_mixed_row_repair_star_propagation_guard.py
python3 -S computations/verify_h3_first_mixed_row_repair_star_propagation_guard.py
python3 -I -S computations/verify_h3_first_mixed_row_repair_star_propagation_guard.py
python3 -m py_compile computations/verify_h3_first_mixed_row_repair_star_propagation_guard.py
```

Expected ledger hash:

```text
f0da2eedd52d72366273ae5b8f324499bfe0cf4b1aeb0380647018b1e12ea2fd
```
