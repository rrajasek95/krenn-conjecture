# The first cost-three companion circuits are three selected-dark octagons

## Outcome

The cell-cost filtration does not remain acyclic at the next grade.  Relative
to the repaired pure-(21) packet, there are exactly

\[
                    28\ \mathrm{PS}+4\ \mathrm{DQ}=32
\]

single paths requiring three new source cells.  Normalize each path so its
change in the selected row (222222:21) is (+1), and retain its complete
difference vector over all (3^6\cdot9) word/head rows.

The off-selected incidence matrix has 62 rows and exact rank 29.  Its
nullspace consists of three disjoint irreducible signed octagons.  Every
octagon has coefficient sum zero, so every circuit is selected-dark.  An
explicit eleven-row integral Fredholm covector reads (+1) on every one of
the 32 columns.  Therefore no linear combination of normalized cost-three
path columns can change the selected row while cancelling all other row
changes.

This is the first recurrent counterguard: a unique-migration potential fails
because genuine octagonal circuits exist, but the selected obstruction still
descends through their quotient.  The result is a normalized path-incidence
theorem.  It is not a simultaneous nonlinear source theorem, because cells
from different paths can create additional cross terms when adjoined in one
packet.

## Cost-three census

Retain

\[
 P_2:\{2\},\qquad S_1:\{5\},\qquad Q_2:\{04,13\}.
\]

For a PS path, count absent endpoint coefficients and absent (Q_2)-edges.
For a DQ path, also count the absent direct head (a_{21}).  Matching
enumeration gives

\[
\begin{array}{c|rrrr}
\text{PS cost}&0&2&3&4\\ \hline
\text{number}&1&11&28&50
\end{array}
\qquad
\begin{array}{c|rrr}
\text{DQ cost}&2&3&4\\ \hline
\text{number}&1&4&10.
\end{array}                                               \tag{1}
\]

The cost-two orbit is the one closed in
[`n8-pure21-minimal-companion-orbit-gate.md`](n8-pure21-minimal-companion-orbit-gate.md).
The present checker constructs all 32 cost-three paths directly from (1).

For each path, set its three new cell values to (1), except that a path
using the old (Y=-1) coefficient receives one compensating sign.  Its
selected change is then exactly (+1).  Subtracting the common base packet
leaves between 7 and 16 nonzero labelled row changes per column.

## The three irreducible circuits

Write

\[
 P[x,y;e|f]
\]

for the normalized PS path with endpoint sites (x,y) and internal edges
(e,f), and (D[e|f|g]) for a DQ path.  The complete row-difference matrix
has the following three relations.

\[
\begin{aligned}
0={}&P[2,0;14|35]-P[2,0;15|34]
    -P[2,1;03|45]+P[2,1;05|34]\\
 &+P[2,3;01|45]-P[2,3;05|14]
    -P[2,4;01|35]+P[2,4;03|15],                       \tag{2}
\end{aligned}
\]

\[
\begin{aligned}
0={}&P[1,2;04|35]-P[1,3;04|25]
    +P[3,1;04|25]-P[3,2;04|15]\\
 &-P[5,1;04|23]+P[5,3;04|12]
    -D[04|12|35]+D[04|15|23],                         \tag{3}
\end{aligned}
\]

\[
\begin{aligned}
0={}&P[0,2;13|45]-P[0,4;13|25]
    +P[4,0;13|25]-P[4,2;05|13]\\
 &-P[5,0;13|24]+P[5,4;02|13]
    -D[02|13|45]+D[05|13|24].                         \tag{4}
\end{aligned}
\]

Equations (2)--(4) hold on every word/head row, not only on the selected
word.  Each support has rank seven, the three supports are disjoint, and
the full nullity is three.  Hence these are all circuits and no relation has
support smaller than eight.  Their signed coefficient sums are all zero;
since every column has selected value (+1), the selected value of each
circuit is zero.

The first circuit is the endpoint-fixed cofactor octagon.  The other two are
its (04)- and (13)-rooted DQ/PS companions.  Their existence is why head
migration alone is not a well-founded potential at cost three.

## Exact eleven-row Fredholm certificate

For a row-difference vector (v), let (v(w;ij)) denote its coefficient at
residual word (w) and head (ij).  Define

\[
\begin{aligned}
\Psi(v)={}&v(000022;20)+v(010012;21)-v(022222;01)\\
 &+v(101200;20)+v(111112;21)+v(121100;21)\\
 &+v(121221;11)+v(121222;01)-v(121222;21)\\
 &-v(121222;22)+v(200000;20).                          \tag{5}
\end{aligned}
\]

Exact replay gives, for every one of the 32 cost-three columns (c),

\[
                         \boxed{\Psi(c)=1
                         =c(222222;21).}               \tag{6}
\]

Consequently, for every formal linear combination (z) of these columns,

\[
                         z(222222;21)=\Psi(z).          \tag{7}
\]

If all off-selected rows of (z) vanish, then its selected row vanishes as
well.  This proves the claimed aggregate exclusion without choosing one of
the migration mechanisms from the cost-two audit.

## Exact boundary of the result

The columns here come from 32 separate normalized source packets.  A formal
linear combination of their row-difference vectors need not be realizable by
adjoining all corresponding cells at once.  In a simultaneous packet,
products between a new endpoint coefficient from one path and a new
(q)-cell from another create additional paths of cost four or less.  Those
cross terms are absent from the linear incidence used in (2)--(7).

Thus (7) closes every additive cost-three path combination, but does not
prove that every nonlinear multi-companion completion decomposes into this
incidence module.  The smallest remaining object is the simultaneous
two-path fibre together with all cross products.  A counterexample there
would be a genuine nonlinear syzygy rather than one of the three dark
octagons above.

## Verification

Run

```text
python computations/verify_n8_pure21_cost3_multicompanion_circuit_gate.py
python computations/verify_n8_pure21_cost3_multicompanion_circuit_gate.py --mode classification
python computations/verify_n8_pure21_cost3_multicompanion_circuit_gate.py --mode incidence
python computations/verify_n8_pure21_cost3_multicompanion_circuit_gate.py --mode circuits
python computations/verify_n8_pure21_cost3_multicompanion_circuit_gate.py --mode dual
```

The dependency-free checker enumerates the cost-three paths, constructs all
32 exact 6561-row differences, verifies rank/nullity and circuit
irreducibility, and checks the eleven coefficients in (5) against every
column.
