# Anchor-first minimization still forces a physical curvature line

## 1. Outcome

Let \(B\) have even size \(N\geq8\), let every colour space be
\(V_u\cong\mathbb C^3\), and suppose that the endpoint-ordered aggregate
blocks satisfy

\[
                         H_B(A)=\Delta_{B,3}.             \tag{1}
\]

Write \(\nu(A)\) for the number of mutual coordinate anchors: nonzero
scalar cells whose two coordinate endpoints both have degree one in the
scalar support graph.  Among all solutions of (1), choose \(A\)
lexicographically so that

\[
       \boxed{\nu(A)\text{ is maximum, and then }
       |\operatorname{supp}A|\text{ is minimum}.}        \tag{2}
\]

Such a representative exists because there are only
\(9\binom N2\) aggregate scalar positions.  It synchronizes two choices
which were previously kept separate.

> **Theorem 1.1 (anchor--curvature synchronization).**  The representative
> (2) has a nonzero canonical good-fan transition.  Consequently it admits
> the same generically active, source-provenant physical curvature line
> \(K_z=E_{ab}+zI\) as the minimum-entry-support representative in the
> unconditional curvature-line theorem.

The new input is an anchor-persistence lemma for the exact pure-port merge
used in the globally flat branch.  Entry minimality is not needed anywhere
else in the flat boundary-core contradiction once every bad-only star has
been made diagonal cubic.

There is a second synchronized conclusion at an intrinsic scalar-unit good
pair.  Retain the full-nine notation

\[
 \alpha\delta_{ia}\delta_{ja}q^{[h]}
       +R_{ij}q^{[h-1]}=\delta_{ij}X_i,
 \qquad R_{ij}=p_i s_j,\qquad \alpha\ne0,                \tag{3}
\]

and put

\[
 \begin{aligned}
 G_a&=\alpha q+R_{aa},\\
 U_a&=G_a^{[h]}-\alpha^{h-1}X_a,\\
 \Theta_a&=G_a^{[h-1]}-\alpha^{h-1}q^{[h-1]}.
 \end{aligned}                                           \tag{4}
\]

Then the same representative obeys

\[
                         \boxed{(U_a,\Theta_a)\ne(0,0).} \tag{5}
\]

In particular a clean unary scalar-unit cap has \(\Theta_a\ne0\).  The
proof is the established exact row deletion, together with the observation
that deleting the selected star row preserves every old mutual anchor.

Thus maximum-anchor extremality, physical curvature selection, and the
nonzero scalar-unit normal class may all be imposed on one exact source.
This removes the representative-selection gap named in the scalar-unit
pivot ledger.  It does **not** prove that the selected curvature line lands
in the intrinsic scalar-unit chart, that it has an active clean point, or
that the surviving class transgresses to the full carrier.  Krenn's
conjecture remains open.

## 2. Mutual anchors and exact pure-port stars

At a physical site \(p\), suppose every active incident pair is bad and
the exact essential-edge argument has put its star in pure-port form.  Thus
the active neighbours form a set \(J\), there is a map
\(\kappa:J\to\{0,1,2\}\), and, after absorbing nonzero cofactor scalars,

\[
       A_{pj}=v_j^{(p)}\otimes e_{\kappa(j)}^{(j)},
       \qquad
       \sum_{\kappa(j)=c}v_j=e_c
       \quad(c=0,1,2).                                  \tag{6}
\]

Every fibre of \(\kappa\) is nonempty and every \(v_j\ne0\).  The exact
port merge chooses one representative \(a_c\in\kappa^{-1}(c)\), replaces
the whole \(c\)-fibre by one nonzero diagonal cell on \(pa_c\), and sets
the other blocks in that fibre to zero.  The complementary cofactors in
the star expansion do not change, so the resulting source is again exact.

The following refinement is the point of this note.

> **Lemma 2.1 (anchor-preserving port merge).**  The representatives
> \(a_c\) can be chosen so that every mutual coordinate anchor of the old
> source remains a mutual coordinate anchor after the exact port merge.
> Consequently
> \[
>                         \nu(A')\geq\nu(A).             \tag{7}
> \]

**Proof.**  First consider an old anchor on a pair not incident with
\(p\).  All blocks away from \(p\) are unchanged.  The merge inserts at a
representative \(a_c\) only the coordinate \((a_c,c)\).  Before the merge,
the nonzero vector \(v_{a_c}\) already made the block \(A_{pa_c}\) incident
with \((a_c,c)\).  Hence that coordinate could not have been the endpoint
of an old mutual anchor on another pair.  Deleting the other port blocks
cannot destroy an anchor.  Thus anchors away from \(p\) persist.

Now suppose an old anchor lies on \(pj\), where \(\kappa(j)=c\), and uses
the coordinate \((p,d)\).  Its scalar is \(v_j(d)\ne0\).  Since
\((p,d)\) has degree one, every other incident scalar in the \(d\)-row at
\(p\) is zero.  In particular

\[
                         v_k(d)=0\qquad(k\ne j).         \tag{8}
\]

Taking the \(d\)-coordinate of the fibre identity in (6) gives

\[
                         v_j(d)=\delta_{dc}.             \tag{9}
\]

Therefore \(d=c\) and the normalized anchor cell is the diagonal
\(cc\)-cell.  There is at most one such anchored port in each colour
fibre.  If it exists, choose it as \(a_c\); otherwise choose any member of
the nonempty fibre.  The merge then retains every anchor incident with
\(p\), while the first paragraph retains every other anchor.  This proves
(7). \(\square\)

There is also a strict support statement.  The merged star has exactly
three nonzero scalar cells.  If the old star was not already a diagonal
cubic star, it had more than three cells.  Indeed, a pure-port star with
only three nonzero cells has one cell in each nonempty fibre, and (6)
forces those cells to be precisely \(e_c\otimes e_c\).  Hence

\[
 p\text{ not diagonal cubic}
 \quad\Longrightarrow\quad
 |\operatorname{supp}A'|<|\operatorname{supp}A|.        \tag{10}
\]

## 3. The flat branch is incompatible with (2)

Assume every canonical transition on every good fan is zero.  The audited
flat-fan and essential-edge theorems give the pure-port description (6)
at every bad-only star with at least three good neighbours; this part does
not use entry minimality.  Apply Lemma 2.1.  Maximality of \(\nu(A)\) in
(2) forces \(\nu(A')=\nu(A)\), and the secondary support minimality then
forbids (10).  Thus

\[
 \boxed{\text{every vertex with at least three good neighbours is
 diagonal cubic.}}                                      \tag{11}
\]

This is exactly the only conclusion for which entry minimality is used in
the existing global-flat proof chain.  Once (11) is available, the
boundary-core theorem uses only exactness, flatness, the 4-degeneracy of
the bad-pair graph, and forced constant-colour coefficients.  It excludes
all even \(N\ge10\) and reduces \(N=8\) to \(1\le|C|\le4\).  The audited
small- and large-core obstructions then exclude \(|C|=1,2\) and
\(|C|=3,4\), respectively.  Their stated entry-minimality hypothesis is
used only through (11); their remaining arguments are support-free exact
incidence and cofactor calculations.

Global flatness is therefore impossible for the representative (2).  A
nonzero canonical transition exists.  The coefficient extraction and
active-line argument in the unconditional curvature-line theorem use no
minimality: they give four physical sites with a nonzero ordered minor and,
after swapping the two fan neighbours if needed, a line

\[
                             K_z=E_{ab}+zI               \tag{12}
\]

whose direct scalar and three target diagonals are simultaneously nonzero
away from finitely many parameters.  This proves Theorem 1.1.

## 4. Scalar-unit row deletion also preserves anchors

Continue at a good pair \(p,q\) satisfying (3).  The full normal-jet
identity proves that if

\[
                              U_a=\Theta_a=0,             \tag{13}
\]

then setting the complete residual star row \(p_a\) to zero, while leaving
all other aggregate entries unchanged, produces another exact ternary
source.  Goodness makes \(p_a\ne0\), so this operation strictly lowers
aggregate-entry support.

It does not lower \(\nu\).  An old mutual anchor away from \(p\) had no
other scalar incident with either of its coordinate endpoints, so every
deleted \(p_a\)-cell at such an endpoint was already zero.  An anchor at
\(p\) cannot use the selected coordinate \(a\): the direct nonzero
\(aa\)-cell on \(pq\) and the nonzero residual row \(p_a\) give
\((p,a)\) degree at least two.  Anchors in either complementary coordinate
row at \(p\) are untouched.  At their opposite endpoints, mutuality again
says every deleted \(p_a\)-cell was zero.  Hence every old anchor remains
literal and

\[
                         \nu(A^{\rm del})\geq\nu(A).     \tag{14}
\]

Equations (13)--(14) contradict the two stages of (2): \(\nu\) cannot
increase beyond its maximum, and at equal \(\nu\) the support cannot
decrease.  This proves (5).  Notice that the proof does not claim an
individual matching term vanishes.  Exactness of the deletion is the
tensor equality already established from all nine rows.

## 5. Relation to generalized pivots

The same representative is compatible with the generalized-pivot result.
The basic scalar-unit pivot preserves all old coordinate anchors
structurally and creates the selected direct anchor.  If a target-only
surviving jet packet satisfies the exact \(GL_2\)-absorption criterion,
the dense endpoint row changes transport the old anchors as split
one-dimensional edge summands.  Exactness of the final source forces every
such summand back to a monochromatic coordinate anchor.  Therefore the
generalized pivot raises \(\nu\), contradicting (2).

This does not eliminate a packet which fails the simultaneous rank-one
and transversality criterion, nor an off-target jet proportional to
\(Q=q^{[h]}\).  It merely shows that the curvature and anchor ledgers now
apply to the same representative before those sharp resonance branches
are considered.

## 6. Exact scope and audit

The theorem is an explicit supersession of the **representative-selection
gap** in the research pivot ledger.  It does not supersede the certified
clean-point dependency: (12) is generically active but need not contain an
active zero of the clean error.

The dependency-free checker
[`verify_anchor_lexicographic_curvature_synchronization.py`](../computations/verify_anchor_lexicographic_curvature_synchronization.py)
audits pure-port anchor preservation, the strict three-cell support test,
scalar-unit row-deletion persistence, and adversarial mutations in which
one chooses the wrong representative or inserts a cell on a previously
free coordinate.  The uniform flat-branch contradiction is supplied by
the cited independently audited theorems; the checker does not replace
their proofs.
