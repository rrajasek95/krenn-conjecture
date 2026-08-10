# The genuine third cofactor is the first polynomial anchor attachment

## Outcome

Let (q) be the literal scalar quadratic on the six residual sites of the
(h=3) unary row, let

\[
                         H=q^{[3]},\qquad F_0=H-u,
\]

and retain every source label in the genuine cofactor tower

\[
 H_e=\operatorname{Haf}(q|_{W\setminus e}),\qquad
 G_{e,f}=\operatorname{Haf}(q|_{W\setminus(e\cup f)}),\qquad
 J_{e,f,g}=1.                                             \tag{1}
\]

Here (e,f,g) are pairwise disjoint physical edges and the last equality
holds when they form a perfect matching.  The first, second, and third
cofactors have internal-edge degrees (2,1,0), respectively.

The complete exact Euler tower is

\[
\begin{aligned}
 \sum_e q_eH_e&=3H,\\
 \sum_{e<f,\ e\cap f=\varnothing}q_eq_fG_{e,f}&=3H,\\
 \sum_{M=\{e,f,g\}}q_eq_fq_gJ_M&=H.                    \tag{2}
\end{aligned}
\]

Consequently the first- and second-cofactor attempts both leave exactly the
same pure-anchor incidence:

\[
\boxed{
 3F_0-\sum_eq_eH_e=-3u,
 \qquad
 3F_0-\sum_{e<f}q_eq_fG_{e,f}=-3u.}                    \tag{3}
\]

Modulo the ideal of internal (q)-cells, every (H,H_e,G_{e,f}) vanishes
and (3) remains (-3u).  This is the exact separator: no polynomial
Euler, polar, normal-incidence, or adjacent-chart combination made only of
the unary row and its first/second cofactors can cancel the conormal class
of `04abf04`.

The genuine third cofactor is the first capable coefficient.  For every
literal perfect matching (M), (J_M=1), and therefore

\[
 \boxed{
 3F_0-\sum_eq_eH_e+3uJ_M=0.}                            \tag{4}
\]

Equivalently, the second- and third-Euler versions of (4) hold with the
same (uJ_M) correction.  Equation (4) is an ordinary polynomial identity
with all physical edge labels retained.  It identifies the minimal missing
source type sharply: a lower face carrying (uJ_M).

## What (4) does and does not construct

The identity (4) does not by itself produce the required physical chain.
The cofactor (J_M=1) is a source coefficient, not an already committed
degree-one generator.  To close the conormal gate, the full-nine/two-chart
source resolution must realize a chain (C_M) whose selected Eq face is

\[
                 d_{\rm Eq}C_M=uJ_Me_{\rm Eq}           \tag{5}
\]

and whose (w)-boundary, target, and ordinary residue all vanish.  Declaring
(5) would assume the missing lower face.  What is proved is that no lower
cofactor order can have the needed polynomial incidence, while (5) is
algebraically sufficient and is the first possible order.

The physical response companions do not change the separator.  They occur
in mixed target-zero grades and contain no homogenizing target variable
(u).  They may constrain whether the third face exists, but they cannot
cancel the (-u) class in (3).

There is a useful localization guard.  For a selected live matching
(M=\{e,f,g\}), the second cofactor is literally

\[
                         G_{e,f}=q_g.                   \tag{6}
\]

After inverting the complementary live cell, (q_g^{-1}G_{e,f}=1), so a
*localized formal* second-cofactor correction can emulate (J_M).  This
does not create a polynomial source lower face: it assumes both the inverse
cell chart and a chain realizing (G_{e,f}) with the required zero readouts.
The invariant statement over the universal polynomial source module remains
that order three is first capable without division.

## Bianchi comparison

The same obstruction survives two charts.  Normalize the two chart Euler
packets by their (-3u) residues.  On coordinates

\[
       ([F_{0,D}],[F_{0,L}],\text{desired attachment})
\]

they give

\[
             (1,0,1),\qquad(0,1,1),qquad
             L-D=(-1,1,0).                              \tag{7}
\]

The separator ((1,1,-1)) kills all three available rows and reads (-1)
on ((0,0,1)).  Thus an ordinary adjacent-chart Bianchi difference only
moves the Euler residue between chart labels.  It cannot replace the
degree-zero third-cofactor face in (4).

## Verification

Run

    python3 computations/verify_h3_pure_unary_cofactor_incidence_attachment.py
    python3 -O computations/verify_h3_pure_unary_cofactor_incidence_attachment.py

The checker pins the genuine cofactor-tower and conormal artifacts;
reconstructs all 15 unary matching terms, 15 first cofactors, 45 second
cofactors, and 15 third matching units; verifies every identity in (2)--(4);
checks the internal-edge quotient separator and localized guard (6); and
replays the two-chart rank-one Bianchi obstruction (7).

The frozen ledger digest is

    428935f1f9b4f084710a5e6bc6f3f69b2baf873b82b79669cfe30e5bd170001a
