# Seven rank-one good pairs force a rank-one curvature wedge

## Outcome

Let endpoint-ordered aggregate blocks satisfy

\[
                         H_8(A)=\Delta_{8,3}.                   \tag{1}
\]

Choose the three active colour witnesses at every site.  In the branch
with no reciprocal witness pair, there are a site `p` and distinct sites
`q,r` such that

* `pq` and `pr` are active rank-one physical pairs;
* both pairs are doubly aggregate-injective; and
* their canonical physical transition is nonzero:

\[
 D_{qr}^a(b,c)=A_{pq}(a,b)S_{r,c}|_{K_{qr}}
              -A_{pr}(a,c)S_{q,b}|_{K_{qr}}\ne0               \tag{2}
\]

for some colours `a,b,c`.

Consequently the literal curvature minor selected from (2) has both fan
arms rank one.  The unconditional N=8 alternative is now

\[
 \boxed{\text{a reciprocal coordinate block, or a nonzero canonical
 transition on two active rank-one good pairs}.}              \tag{3}
\]

This applies in particular to the maximum-anchor/minimum-support
representative used by the unconditional curvature theorem.  No new
minimality assumption is needed in the second branch.

## The exact flat rank-one wedge

Fix two good pairs `pq,pr` and factor their nonzero direct blocks in endpoint
order as

\[
 A_{pq}=x_q\otimes y_q,\qquad A_{pr}=x_r\otimes y_r,            \tag{4}
\]

where the `x` factors are at the shared site `p`.  Put

\[
 T_q=S_q|_{K_{qr}},\qquad T_r=S_r|_{K_{qr}}.                   \tag{5}
\]

If every transition in (2) vanishes, then for every centre covector `a`
and endpoint covectors `beta,gamma`,

\[
 a(x_q)y_q(\beta)T_r(\gamma)
   =a(x_r)y_r(\gamma)T_q(\beta).                              \tag{6}
\]

There are two exact cases.

1. If `x_q,x_r` are independent, choose `a` to kill either factor in
   turn.  Equation (6) gives `T_q=T_r=0`.  Goodness says the full deleted
   stars remain injective, so their sole omitted component, the block
   `A_qr`, must have rank three.
2. If `x_q,x_r` are proportional, (6) says that `T_q` factors through
   `y_q`, `T_r` factors through `y_r`, and the two remaining linear forms
   share one common output.  In particular `T_q` kills the two-plane
   `ker(y_q)`.  The `q`-endpoint good star can inject that plane only through
   `A_qr`, so
   \(\operatorname{rank}A_{qr}\ge2\).  The same conclusion follows at `r`.

Thus in all cases

\[
 \boxed{\text{a flat wedge of two rank-one good arms forces its opposite
 chord to have rank at least two}.}                            \tag{7}
\]

The ranks in (7) are sharp as linear algebra.  Independent centre factors
permit `T_q=T_r=0` with an invertible chord.  Proportional factors permit a
shared rank-one restricted star with a rank-two chord injecting its
two-dimensional kernel.  Therefore an incoming/outgoing factor wedge is
not automatically curved: an exceptional chord can absorb it.  The global
four-exception and essential-star counts are what rule out simultaneous
absorption.

## Four exceptional chords cannot absorb every wedge

Let `R_0` be the graph of the 24 physical pairs selected by the
nonreciprocal colour witnesses, and let `G` be its subgraph of good pairs.
Thus every edge of `R_0` retains one chosen orientation and head colour.
The essential-count theorem gives

\[
                         |E(R_0)|=24,\qquad |E(G)|\ge7.          \tag{8}
\]

Suppose, contrary to the theorem, that every transition between two
adjacent edges of `G` is flat.  A vertex of `G` cannot have degree at least
three: the flat-row classification applied to three good neighbors and a
generic centre covector (nonzero on all three rank-one centre factors)
would allow at most one nonzero direct row, a contradiction.  Hence

\[
                              \Delta(G)\le2.                    \tag{9}
\]

By (7), the endpoints of every length-two path in `G` are joined by a
rank-at-least-two block.  Such a chord is outside `R_0`; (8) leaves at most
four of them.  The finite maximum-degree-two classification on eight
vertices is sharp:

* with seven edges the sole possibility is `C4 disjoint union P4`;
* with eight edges the sole possibility is `C4 disjoint union C4`.

All other path/cycle decompositions have at least five distinct
length-two chords (and a triangle is immediately impossible).  In both
surviving types the four forced higher-rank chords form a perfect matching:
every vertex is incident with exactly one.

Return now to the complete endpoint supports.  At a vertex incident with a
rank-at-least-two chord, three essential neighbors are impossible, because
the equality case of the essential-subspace lemma makes every nonzero
support a line.  If there are two essential neighbors, every nonessential
support lies in their common one-dimensional flag, so the higher-rank chord
must itself be essential.  In either case at most one essential incidence
at that vertex belongs to `R_0`.  Summing over the eight vertices shows
that at most eight `R_0`-edges are bad.  Therefore

\[
                         |E(G)|\ge24-8=16,                       \tag{10}
\]

contrary to (9), which permits at most eight edges.  Some adjacent
rank-one-good transition is nonzero, proving (2).

This proof explicitly handles zero blocks.  They have zero endpoint
support, are never essential, and cannot serve as the nonzero chord forced
by (7).  Higher-rank aggregate blocks and arbitrary endpoint factors are
retained.  Activity is used only to define `R_0` and to obtain (8); no
individual parallel source is selected.

## Consequence and remaining gate

The second branch of (3) supplies a curvature line whose selected direct
block is rank one and whose adjacent chart is also based on a rank-one
direct block.  This is stronger than merely placing seven rank-one pairs
somewhere in E1/E2: the existing two-chart, full-nine, and rootless-cap
packets can now be tested on a literal rank-one/rank-one overlap.

It still does not choose E1 versus E2, make the cap clean, or eliminate the
first reciprocal branch.  The E2 centered rank-one theorems concern ranks
inside the common complement, not just the two direct arms in (2), and the
E1 scalar-matrix-unit boundary can still occur after coordinate alignment.

## Reproduction

```sh
python3 computations/verify_n8_rankone_good_curvature_selection.py
python3 -O computations/verify_n8_rankone_good_curvature_selection.py
```

The checker audits the exact coefficient ranks in both flat-wedge cases,
enumerates all path/cycle component types on eight vertices, verifies the
two four-chord perfect-matching survivors, and replays the final
essential-incidence ledger.
