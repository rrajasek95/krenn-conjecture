# The next Tate inventory still misses the primitive rootless anchor

Exact bounded obstruction.  This note tests the physical realization
interface isolated in `5f490c6`.  It does not exclude an arbitrary future
source resolution or prove Krenn's conjecture.

## Outcome

Grant the five cubic repeated-site principal-parts cells, the unique
degree-five odd-cycle compatibility, normalized diagonal-anchor/cap
subtraction, and the closest committed repeated-site source identity.  The
whole resulting typed inventory still misses a relative cell with signature

\[
 (\operatorname {ainc},\widehat w,\operatorname {tgt},
    \operatorname {ores})=(-1,0,0,0).                 \tag{1}
\]

There are two exact reasons.

First, the five physical diagonal-descent defects are

\[
 a-b,\quad c-d,\quad e-a,\quad b-c,\quad d-e.         \tag{2}
\]

With the signs of the minimal resolution, the degree-five Tate face has
boundary coefficients

\[
                 ce,\quad be,\quad bd,\quad ad,\quad ac.
\]

They satisfy the literal polynomial identity

\[
 \begin{split}
 &ce(a-b)+be(c-d)+bd(e-a)\\
 &\hspace{25mm}+ad(b-c)+ac(d-e)=0.                    \tag{3}
 \end{split}
\]

Thus the Tate cell passes \(d^2=0\), including the conormal lower face, but
it cancels the defects rather than creating their missing fifth aggregate.
At \(a=b=c=d=e=1\), every term in (2) vanishes while the primitive anchor
does not.  The obstruction survives localization at the cycle monomials and
at independent selector/curvature units which are nonzero at that point.

Second, the exact 448-row identity in
`n8-rank11-scalar-dark-plane-overlap-degree2-identity.md` really does meet
the missing physical support type.  In its quadratic target choose

\[
 q_{01}(0,1)q_{13}(1,0)
\]

and multiply by the disjoint cell \(q_{45}(0,1)\).  Relabel sites
\(0,1,3,4,5\mapsto1,2,3,4,5\) and colours
\(0,1,2\mapsto1,2,0\).  The product becomes

\[
 q_{12}(1,2)q_{23}(2,1)q_{45}(1,2)=abd,               \tag{4}
\]

one of the required \(P_3\sqcup K_2\) cubic degrees.

But the coefficient of the pure-row generator in that component is
\(-48\), while the clean-error target coefficient is \(+48\).  After the
unique normalization, its coarse readout is exactly

\[
                         (-1,0,1,0),                   \tag{5}
\]

the old pure source row.  It is not (1).  The full identity also retains two
other decorated shared-site quadratic terms, and its pure-row part has
eleven colour-zero and two colour-one multiplier monomials.  Consequently
the identity is a genuine repeated-site ideal-membership certificate, but
not a target/ordinary-residue-invisible relative anchor face.

## 1. The exact Tate differential

Order the companion generators as

\[
 (g_0,g_1,g_2,g_3,g_4)=(bd,ad,ac,ce,be).
\]

The five cubic columns are

\[
\begin{aligned}
 dE_0&=ae_0-be_1,&dE_1&=ce_1-de_2,\\
 dE_2&=ee_2-ae_3,&dE_3&=be_3-ce_4,\\
 dE_4&=de_4-ee_0.
\end{aligned}                                         \tag{6}
\]

Applying the vertex augmentation gives (2).  Define

\[
 dF=ceE_0+beE_1+bdE_2+adE_3+acE_4.                   \tag{7}
\]

The checker verifies both the full multigraded matrix equation
\(d_1d_2=0\) from `5f490c6` and its conormal projection (3).  Hence signs
and integrality are not the problem.  The cubic shifts have site profile
\((2,1,1,1,1)\) up to rotation; the Tate top \(abcde\) has profile
\((2,2,2,2,2)\).  Neither is a literal matching/Hasse coefficient, whose
site degrees are at most one.  The denominator/PP construction reaches the
cubics only as relative pairs, and the Tate top is a compatible algebraic
two-cell rather than a newly constructed literal source coefficient.

Even granting that two-cell does not help: (3) says its total conormal and
anchor augmentation is zero.  The mapping cone remains the pentagon with
one unfilled augmented vertex class.

## 2. Why the repeated-site identity does not fill it

Write a pure source-row generator with coefficient \(c\) in the coarse
coordinates used by the Component III inventory.  Its readout is

\[
                       c(-1,0,1,0).                    \tag{8}
\]

The dark-plane certificate contains the chosen quadratic monomial in the
colour-zero pure generator with coefficient \(-48\), and no chosen term in
the other two pure generators.  Multiplication by the disjoint edge does
not change the readout.  Scaling by \(-1/48\) gives (5).

This is the load-bearing distinction between source ideal membership and a
relative source cell.  The former may manufacture repeated physical-site
degree through polynomial multipliers, but its pure-anchor incidence still
arrives with the same labelled physical target.  Coefficientwise selection
of only (4) would discard the other source-polynomial faces; it is not a new
\(R\)-linear differential.

The old target/cap/ordinary columns are

\[
 r_0=(-1,0,1,0),\qquad
 T=(0,-Y,1,0),\qquad
 \rho=(0,1,0,1).                                      \tag{9}
\]

The primitive covector

\[
                         (Y,1,Y,-1)                    \tag{10}
\]

kills all three columns, and therefore also kills the dark-plane candidate
(5), but evaluates to \(-Y\) on (1).  Exact ranks are three before and four
after adjoining (1), at \(Y=1,2,-3,5\).  Cancelling the target in (5) with
the old cap necessarily leaves normalized boundary or ordinary residue;
cancelling it with another pure row cancels the anchor incidence as well.

The same argument applies to a five-cell cyclic family.  The degree-five
relation only combines the five target-equals-minus-anchor columns.  Target
zero forces total anchor zero, so odd-cycle compatibility cannot turn (5)
into (1).

## 3. Exact scope and next dependency

This closes the complete **next typed inventory** consisting of:

1. the five denominator-marked cubic PP pairs;
2. their unique degree-five Tate/mapping-cone compatibility;
3. normalized diagonal-anchor subtraction and the old split cap;
4. selector/curvature localization active at the diagonal torus point; and
5. the committed 448-row repeated-site degree-two identity, tensored and
   relabelled into one cubic \(P_3\sqcup K_2\) degree.

It does not prove that no larger source resolution can contain (1).  It
proves that neither the obvious Tate completion nor the closest exact
repeated-site source identity supplies it.  The remaining positive object
must be a genuinely new source-labelled repeated-site relative face whose
pure-anchor incidence is not accompanied by the same physical target.

## Verification

Run

```text
python3 computations/verify_h3_rootless_five_cycle_tate_anchor_obstruction.py
python3 -O computations/verify_h3_rootless_five_cycle_tate_anchor_obstruction.py
```

The checker pins `5f490c6`'s positive interface, `dae10d3`'s PP aggregate
no-go, the exact underived conormal separator, and the repeated-site
dark-plane identity.  It reconstructs the full C5 resolution, verifies the
degree-five conormal cancellation, replays all 448 source terms, extracts
their pure-row coefficients, checks the literal relabelling (4), and proves
the typed rank/separator obstruction.
